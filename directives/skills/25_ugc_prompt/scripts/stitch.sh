#!/usr/bin/env bash
# =============================================================================
# stitch.sh  --  Seedance 2.0 Andromeda UGC factory, per-variant assembler
# =============================================================================
#
# WHAT THIS DOES
#   Takes ONE variant out of an assembly-manifest.json and concatenates that
#   variant's ordered_timeline (hook clip, body shots, b-roll inserted at the
#   variant's chosen point) into a single 9:16 1080x1920 30fps H.264 + AAC MP4.
#
# THE AUDIO RULE (this factory NEVER mutes)
#   Every Seedance clip was generated with the SAME 15s voice reference, so
#   every clip ALREADY carries its own voice audio in a consistent voice.
#   There is no separate authored voice track, no spine, no muting. We KEEP
#   each clip's audio and concatenate audio straight through, so the voice
#   plays continuously across the whole timeline. The only post step on audio
#   is a single loudness normalization to -14 LUFS at the very end so the
#   levels of the different clips match.
#
# PACING
#   Pacing was already solved upstream (segment_script.py / validate_payload.py)
#   and baked into each clip at generation time. This script does NOT re-pace.
#   It only trims (trim_in/trim_out from the manifest), normalizes geometry to
#   1080x1920@30, concatenates, and loudness-normalizes the final mix.
#
# USAGE
#   stitch.sh <manifest.json> <variant_id> <output.mp4>
#
# DEPENDENCIES
#   ffmpeg, ffprobe, python3   (jq is intentionally NOT required; we parse the
#   manifest with an inline python3 -c so this runs on machines without jq).
#
# EXIT CODES
#   0  success
#   2  a required dependency (ffmpeg / ffprobe / python3) is missing
#   1  any other failure (bad args, variant not found, ffmpeg error, QC fail)
# =============================================================================

# Strict mode: stop on errors, stop on unset vars, fail a pipeline if any
# stage fails (not just the last). This is what makes the script trustworthy.
set -euo pipefail

# -----------------------------------------------------------------------------
# Optional knobs (environment overridable, sane defaults)
# -----------------------------------------------------------------------------
# XFADE_DURATION: if > 0, apply a short PICTURE-ONLY crossfade between video
# segments using the xfade filter. Audio is ALWAYS concatenated straight (no
# acrossfade by default) so we never duck or dip the voice. Default 0 = plain
# hard cuts, which is the safest, most predictable behavior for UGC.
XFADE_DURATION="${XFADE_DURATION:-0}"

# AUDIO_SEAM_MS: a very short EQUAL-POWER audio crossfade (acrossfade) applied at
# each seam on the clips' OWN audio. Because each clip is a separate Seedance
# generation that only shares the voice REFERENCE, the synthesized voice can jump
# in pitch/room-tone at a hard cut. ~80ms is far below a spoken word so it never
# ducks the voice; it only smooths the seam and absorbs head/tail silences. This
# is NOT a separate spine. Set to 0 for pure hard-cut audio.
AUDIO_SEAM_MS="${AUDIO_SEAM_MS:-80}"

# Final loudness target. Locked at -14 LUFS so every variant matches. We run a
# TWO-PASS loudnorm (measure, then apply with linear gain) so every variant lands
# within ~0.1 LU of the target; a single dynamic pass cannot guarantee that and
# different variants would settle at different volumes. Set LOUDNORM_TWO_PASS=0
# to fall back to a single pass (documented as approximate).
LOUDNORM_I="${LOUDNORM_I:--14}"
LOUDNORM_TP="${LOUDNORM_TP:--1.5}"   # true peak ceiling, dBTP
LOUDNORM_LRA="${LOUDNORM_LRA:-7}"    # loudness range; UGC voice wants a tighter
                                     # range than the EBU broadcast default of 11
LOUDNORM_TWO_PASS="${LOUDNORM_TWO_PASS:-1}"

# Output geometry, locked by the factory spec.
OUT_W=1080
OUT_H=1920
OUT_FPS=30

# Duration QC tolerance in seconds. Final output must be within this of the
# sum of trimmed segment durations.
DURATION_TOLERANCE="0.3"

# -----------------------------------------------------------------------------
# Tiny logging helper. Every step echoes using the OUTPUT path so logs from
# parallel variant builds never get confused with each other.
# -----------------------------------------------------------------------------
log() {
  # $1 = message; we prefix with the output file we are building.
  printf '[stitch %s] %s\n' "${OUTPUT:-?}" "$1"
}

die() {
  # Fatal error to stderr, then exit 1.
  printf '[stitch %s] ERROR: %s\n' "${OUTPUT:-?}" "$1" >&2
  exit 1
}

# -----------------------------------------------------------------------------
# Dependency checks. Missing ffmpeg/ffprobe/python3 is a HARD environment fail
# and exits 2 (distinct from a runtime failure) so a wrapper can tell the
# difference between "tool not installed" and "this clip is broken".
# -----------------------------------------------------------------------------
command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found on PATH"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found on PATH" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found on PATH" >&2; exit 2; }

# -----------------------------------------------------------------------------
# Argument parsing. Quote everything; paths may contain spaces (e.g. a
# "Performance Marketing Team" folder).
# -----------------------------------------------------------------------------
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <manifest.json> <variant_id> <output.mp4>" >&2
  exit 1
fi

MANIFEST="$1"
VARIANT_ID="$2"
OUTPUT="$3"

[ -f "$MANIFEST" ] || die "manifest not found: $MANIFEST"

# Resolve the manifest's directory so any RELATIVE clip paths in the manifest
# resolve relative to the manifest itself, not to the caller's cwd.
MANIFEST_DIR="$(cd "$(dirname "$MANIFEST")" && pwd)"

log "manifest    = $MANIFEST"
log "variant_id  = $VARIANT_ID"
log "output      = $OUTPUT"
log "geometry    = ${OUT_W}x${OUT_H} @ ${OUT_FPS}fps"
log "loudnorm    = I=${LOUDNORM_I} TP=${LOUDNORM_TP} LRA=${LOUDNORM_LRA}"
log "xfade       = ${XFADE_DURATION}s (0 = hard cuts, audio always straight)"

# -----------------------------------------------------------------------------
# Parse the chosen variant's ordered_timeline out of the manifest using an
# inline python3 script (jq may be absent). We emit one TAB-separated line per
# timeline entry:  role <TAB> clip <TAB> trim_in <TAB> trim_out
#
# trim_in / trim_out are OPTIONAL in the schema. When trim_out is null/absent
# we emit the literal string "END" and resolve the real clip duration later
# with ffprobe. trim_in defaults to 0.
#
# The python reads the manifest path and variant id from argv so we never have
# to interpolate shell strings into python source (no quoting hazards).
# -----------------------------------------------------------------------------
PARSE_PY='
import json, sys
manifest_path, variant_id = sys.argv[1], sys.argv[2]
with open(manifest_path, "r") as fh:
    data = json.load(fh)

variants = data.get("variants") or []
match = None
for v in variants:
    if str(v.get("variant_id")) == variant_id:
        match = v
        break
if match is None:
    have = ", ".join(str(v.get("variant_id")) for v in variants) or "(none)"
    sys.stderr.write("variant_id not found: %s ; available: %s\n" % (variant_id, have))
    sys.exit(3)

timeline = match.get("ordered_timeline") or []
if not timeline:
    sys.stderr.write("variant %s has an empty ordered_timeline\n" % variant_id)
    sys.exit(3)

for entry in timeline:
    role = str(entry.get("role", "clip"))
    clip = entry.get("clip")
    if not clip:
        sys.stderr.write("timeline entry missing clip: %r\n" % entry)
        sys.exit(3)
    ti = entry.get("trim_in", 0)
    if ti is None:
        ti = 0
    to = entry.get("trim_out", None)
    # trim_out null OR 0 both mean "play to the natural end of the clip" (matches
    # the documented manifest contract). Only a positive number is a real trim.
    to_str = "END" if (to is None or float(to) == 0) else repr(float(to))
    # TAB-separated; clip paths can contain spaces but not tabs in practice.
    sys.stdout.write("%s\t%s\t%s\t%s\n" % (role, clip, repr(float(ti)), to_str))
'

# Run the parser. If python exits 3 the variant is bad; surface that as a
# normal failure (exit 1) with python stderr already shown to the user.
if ! TIMELINE_RAW="$(python3 -c "$PARSE_PY" "$MANIFEST" "$VARIANT_ID")"; then
  die "could not parse variant '$VARIANT_ID' from manifest (see message above)"
fi

[ -n "$TIMELINE_RAW" ] || die "variant '$VARIANT_ID' produced an empty timeline"

# -----------------------------------------------------------------------------
# Scratch workspace for the per-segment normalized intermediates. Cleaned up
# on ANY exit via trap so we never leave temp files behind.
# -----------------------------------------------------------------------------
WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/stitch.XXXXXX")"
cleanup() { rm -rf "$WORKDIR"; }
trap cleanup EXIT
log "workdir     = $WORKDIR"

# -----------------------------------------------------------------------------
# Helper: resolve a clip path. If it is absolute and exists, use it. Otherwise
# try it relative to the manifest's directory. Print the resolved path or fail.
# -----------------------------------------------------------------------------
resolve_clip() {
  _clip="$1"
  case "$_clip" in
    /*)
      # Absolute path.
      [ -f "$_clip" ] || die "clip not found (absolute): $_clip"
      printf '%s' "$_clip"
      ;;
    *)
      # Relative: resolve against the manifest directory.
      _candidate="$MANIFEST_DIR/$_clip"
      [ -f "$_candidate" ] || die "clip not found (relative to manifest): $_clip"
      printf '%s' "$_candidate"
      ;;
  esac
}

# -----------------------------------------------------------------------------
# Helper: ffprobe a clip's duration in seconds (float). Used to turn "END"
# trim_out into a real number and to compute the expected total duration.
# -----------------------------------------------------------------------------
probe_duration() {
  ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$1"
}

# Whether a clip even HAS an audio stream. Seedance clips always do (audio is
# enabled on every generation, b-rolls included), so this should essentially
# never be false. We detect it ROBUSTLY by reading the first audio stream's
# codec_type (not by counting lines, which can miscount on some containers and
# wrongly route a voiced clip into the silence-pad branch, deleting its voice).
has_audio_stream() {
  _codec="$(ffprobe -v error -select_streams a:0 \
            -show_entries stream=codec_type \
            -of default=nw=1:nk=1 "$1" 2>/dev/null)"
  [ "$_codec" = "audio" ]
}

# -----------------------------------------------------------------------------
# PASS 1: normalize every segment independently.
#
# For each timeline entry we:
#   - resolve and trim the clip (trim_in .. trim_out),
#   - scale to FIT inside 1080x1920 preserving aspect, then PAD to exactly
#     1080x1920 (let/pillarbox with black) so geometry is uniform,
#   - force 30fps and SAR 1,
#   - KEEP the clip's own audio, resampled to a uniform 48k stereo so the
#     later concat has matching audio params (this is NOT muting; it is just
#     making the existing voice tracks concat-compatible),
#   - if a clip lacks audio, generate matching silence for its trimmed length.
#
# We accumulate the per-segment trimmed durations to compute the QC total.
# Writing uniform intermediates first makes the concat step bulletproof and
# also makes the optional xfade math trivial.
# -----------------------------------------------------------------------------

# Geometry filter applied to every segment's video. scale with
# force_original_aspect_ratio=decrease fits inside the box, pad centers it,
# setsar=1 keeps pixels square, fps pins the frame rate.
VF_GEOM="scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=decrease,pad=${OUT_W}:${OUT_H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=${OUT_FPS}"

SEG_FILES=()        # paths to normalized intermediate segments, in order
SEG_DURATIONS=()    # trimmed duration of each segment (seconds, float)
EXPECTED_TOTAL="0"  # running sum of trimmed durations
SEG_INDEX=0

# Read the TAB-separated timeline line by line. IFS set to TAB only and read -r
# so spaces in clip paths survive intact. We pipe via a here-string of the
# captured variable so the loop runs in THIS shell (arrays persist).
while IFS="$(printf '\t')" read -r ROLE CLIP TRIM_IN TRIM_OUT; do
  # Skip accidental blank lines defensively.
  [ -n "${CLIP:-}" ] || continue

  SRC="$(resolve_clip "$CLIP")"

  # Resolve trim window. trim_in defaults handled in python; trim_out may be
  # the sentinel "END" meaning "to the natural end of the clip".
  if [ "$TRIM_OUT" = "END" ]; then
    TRIM_OUT="$(probe_duration "$SRC")"
  fi

  # Compute this segment's trimmed length and validate it is positive.
  SEG_DUR="$(python3 -c 'import sys; a=float(sys.argv[1]); b=float(sys.argv[2]); print(round(b-a,6))' "$TRIM_IN" "$TRIM_OUT")"
  # Guard: trimmed length must be > 0.
  case "$SEG_DUR" in
    -*|0|0.0|0.000000) die "segment '$ROLE' ($CLIP) has non-positive trimmed duration: trim_in=$TRIM_IN trim_out=$TRIM_OUT" ;;
  esac

  OUTSEG="$WORKDIR/seg_$(printf '%03d' "$SEG_INDEX").mp4"

  log "segment $SEG_INDEX  role=$ROLE  trim=[${TRIM_IN}..${TRIM_OUT}] (${SEG_DUR}s)  src=$SRC"

  # Build the per-segment ffmpeg command.
  #   -ss before -i is fast (keyframe) seek; we then re-encode so frames are
  #    exact. -t limits to the trimmed length. We re-encode here because we
  #    must normalize geometry/fps anyway, so accurate trimming is free.
  #   Video: VF_GEOM. Audio: keep + resample to a uniform 48k stereo so concat
  #    inputs match. yuv420p for universal playback.
  if has_audio_stream "$SRC"; then
    # Clip has its own voice audio: KEEP it, just conform the format.
    ffmpeg -nostdin -y -v error \
      -ss "$TRIM_IN" -t "$SEG_DUR" -i "$SRC" \
      -vf "$VF_GEOM" \
      -af "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo" \
      -r "$OUT_FPS" \
      -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 48000 -ac 2 \
      -movflags +faststart \
      "$OUTSEG" \
      || die "ffmpeg failed normalizing segment $SEG_INDEX ($CLIP)"
  else
    # This should never happen: every Seedance clip carries voice. If it does,
    # surface it LOUDLY (it means a clip lost its voiceover) rather than silently
    # papering over it, then pad with silence so the OTHER clips' voice survives.
    log "WARN: segment $SEG_INDEX ($CLIP) has NO audio stream; this factory expects voice on every clip. Padding with silence to keep alignment, but CHECK/RE-ROLL THIS CLIP."
    ffmpeg -nostdin -y -v error \
      -ss "$TRIM_IN" -t "$SEG_DUR" -i "$SRC" \
      -f lavfi -t "$SEG_DUR" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
      -map 0:v:0 -map 1:a:0 \
      -vf "$VF_GEOM" \
      -r "$OUT_FPS" \
      -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 48000 -ac 2 \
      -movflags +faststart \
      "$OUTSEG" \
      || die "ffmpeg failed normalizing (silent) segment $SEG_INDEX ($CLIP)"
  fi

  SEG_FILES+=("$OUTSEG")
  SEG_DURATIONS+=("$SEG_DUR")
  EXPECTED_TOTAL="$(python3 -c 'import sys; print(round(float(sys.argv[1])+float(sys.argv[2]),6))' "$EXPECTED_TOTAL" "$SEG_DUR")"
  SEG_INDEX=$((SEG_INDEX + 1))
done <<EOF
$TIMELINE_RAW
EOF

NUM_SEGS="${#SEG_FILES[@]}"
[ "$NUM_SEGS" -ge 1 ] || die "no usable segments were produced"
log "normalized $NUM_SEGS segment(s); expected total = ${EXPECTED_TOTAL}s"

# -----------------------------------------------------------------------------
# PASS 2: concatenate.
#
# Two paths:
#   (A) PLAIN CONCAT (default, XFADE_DURATION=0): use the concat filter with
#       BOTH video and audio (n=NUM v=1 a=1). This keeps every clip's audio
#       and plays the voice continuously across the timeline. Hard cuts on
#       video, straight concatenation on audio. This is the locked default.
#
#   (B) PICTURE-ONLY XFADE (XFADE_DURATION>0): chain xfade between successive
#       video segments for a short dissolve, while AUDIO is still concatenated
#       STRAIGHT via the concat filter (a=1) so the voice is never ducked or
#       crossfaded. Note: each xfade overlaps neighbors by XFADE_DURATION, so
#       the final video is shorter than the straight sum by
#       (NUM_SEGS-1)*XFADE_DURATION; we account for that in the QC expectation.
#
# Either way audio is concat-straight: this factory does not duck the voice.
# -----------------------------------------------------------------------------

# Decide whether xfade is actually requested AND meaningful (needs >=2 segs and
# a positive duration). Use python for the float comparison portability.
USE_XFADE=0
if [ "$NUM_SEGS" -ge 2 ] && python3 -c 'import sys; sys.exit(0 if float(sys.argv[1])>0 else 1)' "$XFADE_DURATION"; then
  USE_XFADE=1
fi

# Build the ffmpeg input list (-i per segment) as an array so paths with
# spaces stay intact.
FF_INPUTS=()
for f in "${SEG_FILES[@]}"; do
  FF_INPUTS+=(-i "$f")
done

# The QC expected total may be reduced by xfade overlaps; start from the
# straight sum and subtract overlaps if xfade is in play.
QC_EXPECTED="$EXPECTED_TOTAL"

# Seam crossfade duration in seconds (from AUDIO_SEAM_MS). When > 0 and there
# are >= 2 segments, audio is joined with acrossfade instead of straight concat
# so the voice does not click/jump at a cut. This overlaps neighbours, so the
# audio total shrinks by (NUM_SEGS-1)*seam, which we fold into QC_EXPECTED.
SEAM_S="$(python3 -c 'import sys; print(round(float(sys.argv[1])/1000.0,6))' "$AUDIO_SEAM_MS")"
USE_ASEAM=0
if [ "$NUM_SEGS" -ge 2 ] && python3 -c 'import sys; sys.exit(0 if float(sys.argv[1])>0 else 1)' "$SEAM_S"; then
  USE_ASEAM=1
fi

# Build the AUDIO half of the filtergraph, producing label [apre] (pre-loudnorm).
# With the seam crossfade we chain acrossfade (equal-power, c1=tri:c2=tri) across
# successive audio streams; this is NOT a separate spine and at ~80ms is far
# below a spoken word so it never ducks the voice. Otherwise we straight-concat.
build_audio_filter() {
  if [ "$USE_ASEAM" -eq 1 ]; then
    # acrossfade chain: [0:a:0][1:a:0]acrossfade...[ax1]; [ax1][2:a:0]acrossfade...
    _af="[0:a:0]anull[ax0];"
    _prev="ax0"
    _m=1
    while [ "$_m" -lt "$NUM_SEGS" ]; do
      _next="ax${_m}"
      _af="${_af}[${_prev}][${_m}:a:0]acrossfade=d=${SEAM_S}:c1=tri:c2=tri[${_next}];"
      _prev="$_next"
      _m=$((_m + 1))
    done
    printf '%s[%s]anull[apre];' "$_af" "$_prev"
  else
    _af=""
    _m=0
    while [ "$_m" -lt "$NUM_SEGS" ]; do
      _af="${_af}[${_m}:a:0]"
      _m=$((_m + 1))
    done
    printf '%sconcat=n=%s:v=0:a=1[apre];' "$_af" "$NUM_SEGS"
  fi
}

AFILTER="$(build_audio_filter)"

# The pre-loudnorm intermediate (video + joined audio, NO loudnorm yet) so the
# loudnorm pass(es) run once on the final concatenated track. This makes a clean,
# reliable two-pass possible.
PRE="$WORKDIR/pre.mp4"

if [ "$USE_XFADE" -eq 0 ]; then
  # ---- Path A: plain concat on video, seam-crossfaded (or straight) audio ---
  log "concatenating (video straight cuts; audio seam=${AUDIO_SEAM_MS}ms)"

  VCONCAT=""
  i=0
  while [ "$i" -lt "$NUM_SEGS" ]; do
    VCONCAT="${VCONCAT}[${i}:v:0]"
    i=$((i + 1))
  done
  VCONCAT="${VCONCAT}concat=n=${NUM_SEGS}:v=1:a=0[vcat];"
  FILTER="${VCONCAT}${AFILTER}"

  ffmpeg -nostdin -y -v error \
    "${FF_INPUTS[@]}" \
    -filter_complex "$FILTER" \
    -map "[vcat]" -map "[apre]" \
    -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
    -r "$OUT_FPS" \
    -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -movflags +faststart \
    "$PRE" \
    || die "ffmpeg failed during plain concat"

else
  # ---- Path B: picture-only xfade on video, seam-crossfaded audio ----------
  log "concatenating (video xfade=${XFADE_DURATION}s; audio seam=${AUDIO_SEAM_MS}ms)"

  # VIDEO chain: progressively xfade segment k into the running result.
  # The xfade 'offset' for each step is the cumulative duration of everything
  # already in the chain MINUS the accumulated overlaps so far. We track the
  # running visible length in RUN_LEN.
  #
  # First label is the raw [0:v:0]. Each step produces [vx<k>].
  VFILTER="[0:v:0]format=yuv420p[vx0];"
  RUN_LEN="${SEG_DURATIONS[0]}"
  PREV_LABEL="vx0"
  k=1
  while [ "$k" -lt "$NUM_SEGS" ]; do
    # offset = current running length - xfade duration (start the dissolve so
    # it ends right as the previous segment ends).
    OFFSET="$(python3 -c 'import sys; print(round(float(sys.argv[1])-float(sys.argv[2]),6))' "$RUN_LEN" "$XFADE_DURATION")"
    NEXT_LABEL="vx${k}"
    VFILTER="${VFILTER}[${k}:v:0]format=yuv420p[vin${k}];"
    VFILTER="${VFILTER}[${PREV_LABEL}][vin${k}]xfade=transition=fade:duration=${XFADE_DURATION}:offset=${OFFSET}[${NEXT_LABEL}];"
    # New running visible length = old + this segment - one overlap.
    RUN_LEN="$(python3 -c 'import sys; print(round(float(sys.argv[1])+float(sys.argv[2])-float(sys.argv[3]),6))' "$RUN_LEN" "${SEG_DURATIONS[$k]}" "$XFADE_DURATION")"
    PREV_LABEL="$NEXT_LABEL"
    k=$((k + 1))
  done
  # Final video label.
  VOUT_LABEL="$PREV_LABEL"

  FILTER="${VFILTER}${AFILTER}"

  ffmpeg -nostdin -y -v error \
    "${FF_INPUTS[@]}" \
    -filter_complex "$FILTER" \
    -map "[${VOUT_LABEL}]" -map "[apre]" \
    -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
    -r "$OUT_FPS" \
    -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -movflags +faststart \
    "$PRE" \
    || die "ffmpeg failed during xfade concat"

  log "xfade overlaps total = $(python3 -c 'import sys; print(round((int(sys.argv[1])-1)*float(sys.argv[2]),6))' "$NUM_SEGS" "$XFADE_DURATION")s (video shortened; audio handled separately)"
fi

[ -f "$PRE" ] || die "ffmpeg reported success but intermediate is missing: $PRE"

# The muxed container duration tracks the LONGER of the two streams. The audio
# seam crossfade overlaps neighbours, shortening AUDIO by (NUM_SEGS-1)*seam; a
# picture xfade (Path B) shortens VIDEO by (NUM_SEGS-1)*xfade. With hard video
# cuts (Path A, the default) the video keeps its full length, so it governs and
# QC_EXPECTED must NOT be reduced by the audio seam, otherwise every ad with >=5
# segments false-fails QC. Expect max(video_total, audio_total).
QC_EXPECTED="$(python3 -c '
import sys
total=float(sys.argv[1]); segs=int(sys.argv[2])
seam=float(sys.argv[3]); xfade=float(sys.argv[4])
use_aseam=sys.argv[5]=="1"; use_xfade=sys.argv[6]=="1"
seams=max(segs-1,0)
audio=total-(seams*seam if use_aseam else 0.0)
video=total-(seams*xfade if use_xfade else 0.0)
print(round(max(audio,video),6))
' "$EXPECTED_TOTAL" "$NUM_SEGS" "$SEAM_S" "$XFADE_DURATION" "$USE_ASEAM" "$USE_XFADE")"

# -----------------------------------------------------------------------------
# LOUDNESS NORMALIZATION to -14 LUFS.
#   Two-pass (default): measure the concatenated track, then apply loudnorm with
#   linear=true so a single static gain lands within ~0.1 LU of target on EVERY
#   variant (a single dynamic pass cannot guarantee this, so the 4 deliverables
#   could otherwise differ in volume). Single-pass fallback when
#   LOUDNORM_TWO_PASS=0 (documented as approximate, identical settings per run).
# -----------------------------------------------------------------------------
if [ "$LOUDNORM_TWO_PASS" -eq 1 ]; then
  log "loudnorm pass 1/2: measuring integrated loudness on the joined audio"
  MEAS="$(ffmpeg -nostdin -hide_banner -v info \
            -i "$PRE" \
            -af "loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}:print_format=json" \
            -f null - 2>&1 || true)"
  # Pull the measured_* values out of the JSON ffmpeg printed to stderr.
  LN_VALUES="$(printf '%s\n' "$MEAS" | python3 -c '
import sys, json, re
text = sys.stdin.read()
# The JSON object is the last {...} block ffmpeg prints.
m = re.findall(r"\{[^{}]*\}", text, re.S)
if not m:
    sys.exit(1)
d = json.loads(m[-1])
print(" ".join([
    d.get("input_i", "0"),
    d.get("input_tp", "0"),
    d.get("input_lra", "0"),
    d.get("input_thresh", "0"),
    d.get("target_offset", "0"),
]))
' 2>/dev/null || true)"

  if [ -n "$LN_VALUES" ]; then
    # shellcheck disable=SC2086
    set -- $LN_VALUES
    M_I="$1"; M_TP="$2"; M_LRA="$3"; M_THRESH="$4"; M_OFFSET="$5"
    log "loudnorm pass 2/2: applying linear gain (measured_I=${M_I})"
    AOUT_FILTER="loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}:measured_I=${M_I}:measured_TP=${M_TP}:measured_LRA=${M_LRA}:measured_thresh=${M_THRESH}:offset=${M_OFFSET}:linear=true:print_format=summary"
  else
    log "WARN: could not parse loudnorm measurement; falling back to single-pass loudnorm"
    AOUT_FILTER="loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}"
  fi
else
  # Single-pass fallback. Identical settings across all variants, but only an
  # approximation of -14 LUFS (it cannot measure first). Noted in the doc.
  log "loudnorm single-pass (approximate; set LOUDNORM_TWO_PASS=1 for exact match)"
  AOUT_FILTER="loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}"
fi

# Apply the loudnorm to the joined audio, copy the already-finished video.
ffmpeg -nostdin -y -v error \
  -i "$PRE" \
  -af "$AOUT_FILTER" \
  -c:v copy \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -movflags +faststart \
  "$OUTPUT" \
  || die "ffmpeg failed during loudness normalization"

[ -f "$OUTPUT" ] || die "ffmpeg reported success but output is missing: $OUTPUT"
log "wrote $OUTPUT"

# -----------------------------------------------------------------------------
# FINAL QC with ffprobe.
#   1) Output MUST contain BOTH a video stream AND an audio stream. (If audio
#      were missing the factory's core promise, the voice, would be broken.)
#   2) Output duration MUST be within DURATION_TOLERANCE of the expected sum
#      of trimmed segment durations.
# -----------------------------------------------------------------------------
log "QC: probing output streams and duration"

VSTREAMS="$(ffprobe -v error -select_streams v -show_entries stream=index \
            -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
ASTREAMS="$(ffprobe -v error -select_streams a -show_entries stream=index \
            -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"

[ "${VSTREAMS:-0}" -ge 1 ] || die "QC FAIL: output has no VIDEO stream"
[ "${ASTREAMS:-0}" -ge 1 ] || die "QC FAIL: output has no AUDIO stream (this factory never mutes)"
log "QC: video streams=$VSTREAMS  audio streams=$ASTREAMS  OK"

ACTUAL_DUR="$(probe_duration "$OUTPUT")"

# Compare |actual - expected| <= tolerance. python returns exit 0 on pass.
if python3 - "$ACTUAL_DUR" "$QC_EXPECTED" "$DURATION_TOLERANCE" <<'PYEOF'
import sys
actual, expected, tol = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
diff = abs(actual - expected)
sys.stderr.write("QC duration: actual=%.3fs expected=%.3fs diff=%.3fs tol=%.3fs\n"
                 % (actual, expected, diff, tol))
sys.exit(0 if diff <= tol else 1)
PYEOF
then
  log "QC: duration within tolerance (${ACTUAL_DUR}s vs expected ${QC_EXPECTED}s, tol ${DURATION_TOLERANCE}s) OK"
else
  die "QC FAIL: output duration ${ACTUAL_DUR}s deviates from expected ${QC_EXPECTED}s by more than ${DURATION_TOLERANCE}s"
fi

# -----------------------------------------------------------------------------
# Done. Cleanup runs via the EXIT trap.
# -----------------------------------------------------------------------------
log "SUCCESS: variant '$VARIANT_ID' assembled -> $OUTPUT"
exit 0
