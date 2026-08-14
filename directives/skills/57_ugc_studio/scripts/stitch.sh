#!/usr/bin/env bash
# =============================================================================
# stitch.sh — UGC Studio two-rail assembler: manifest.json -> finished 9:16 ad
# =============================================================================
#
# USAGE
#   stitch.sh <manifest.json> <output.mp4>
#
# WHAT THIS EXECUTES (the manifest is already fully resolved — no lookups):
#   AUDIO RAIL  base clips, each keeping its OWN audio, joined at line
#               boundaries; interior trims (jump-cut manufacture) cut both
#               picture and sound at the planned dead-air windows.
#   VIDEO RAIL  punch-in overlays REPLACE THE PICTURE for their window while
#               the base audio runs uninterrupted underneath. This is the
#               winners' signature move: the host's audio (and hidden lips)
#               never stop, so overlays are applied VIDEO-ONLY and the base
#               audio stream is carried across every overlay boundary
#               bit-continuously (stream-copied through the composite pass).
#
# REFUSAL: a manifest whose rhythm verdict is not PASS never stitches. Shot
# density is the AI tell — dropping whole 4-9s gens reads as AI instantly —
# and the fix is edit-side (more punch-ins/trims), not an encode.
#
# LOUDNESS: narrated ads two-pass loudnorm to the manifest's target LUFS
# (measure, then linear gain — a single dynamic pass cannot guarantee the
# target). Silent/SFX-only ads (audio.loudnorm=false) skip normalization
# entirely: normalizing a wordless rail only boosts noise.
#
# QC AFTER ENCODE: stream layout (video always; audio required for narrated),
# duration within DURATION_TOLERANCE of the manifest's expected_total, the
# rhythm table, and "ENDS ON" naming the typed close verified at manifest time.
#
# DEPENDENCIES: ffmpeg, ffprobe, python3 (no jq; manifest parsed inline).
# EXIT CODES:   0 success · 2 missing dependency · 1 anything else (with a
#               printed, actionable reason).
# =============================================================================

set -euo pipefail

OUT_W=1080
OUT_H=1920
OUT_FPS=30
DURATION_TOLERANCE="0.5"
LOUDNORM_TP="${LOUDNORM_TP:--1.5}"
LOUDNORM_LRA="${LOUDNORM_LRA:-7}"

log() { printf '[stitch %s] %s\n' "${OUTPUT:-?}" "$1"; }
die() { printf '[stitch %s] ERROR: %s\n' "${OUTPUT:-?}" "$1" >&2; exit 1; }

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found on PATH"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found on PATH" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found on PATH" >&2; exit 2; }

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <manifest.json> <output.mp4>" >&2
  exit 1
fi
MANIFEST="$1"
OUTPUT="$2"
[ -f "$MANIFEST" ] || die "manifest not found: $MANIFEST"

# Relative paths in the manifest resolve against the manifest's own directory
# (the ad's $WORK folder), never the caller's cwd.
MANIFEST_DIR="$(cd "$(dirname "$MANIFEST")" && pwd)"

# -----------------------------------------------------------------------------
# Parse the manifest into a TAB-separated line protocol (argv-passed path, so
# no shell-into-python quoting hazards). Interior trims are expanded HERE into
# the kept sub-segments: a clip with trims [[c,r]] becomes [0..c] + [r..end],
# which concatenated back-to-back IS the jump cut — picture and sound together.
# -----------------------------------------------------------------------------
PARSE_PY='
import json, sys
try:
    d = json.load(open(sys.argv[1], "r", encoding="utf-8"))
except Exception as exc:
    sys.stderr.write("manifest unreadable: %s\n" % exc); sys.exit(3)
def out(*f): sys.stdout.write("\t".join(str(x) for x in f) + "\n")
rhythm = d.get("rhythm") or {}
audio  = d.get("audio") or {}
t      = rhythm.get("targets") or {}
base   = d.get("base") or []
if not base:
    sys.stderr.write("manifest has an empty base rail\n"); sys.exit(3)
out("META", d.get("ad_id",""), d.get("close_type",""),
    rhythm.get("verdict","MISSING"),
    1 if audio.get("loudnorm") else 0, audio.get("target_lufs", -14),
    d.get("expected_total", 0))
out("TARGETS", t.get("median_max","?"), t.get("shot_max","?"),
    t.get("close_exempt","?"))
out("SHOTS", ", ".join("%.2f" % s for s in (rhythm.get("shots") or [])))
out("STATS", rhythm.get("median","?"), rhythm.get("max_non_close","?"))
for b in base:
    f, dur = b["file"], float(b["duration"])
    pos = 0.0
    for c, r in (b.get("trims") or []):
        c, r = float(c), float(r)
        if c > pos + 1e-6: out("SEG", f, "%.3f" % pos, "%.3f" % (c - pos))
        pos = r
    if dur > pos + 1e-6: out("SEG", f, "%.3f" % pos, "%.3f" % (dur - pos))
out("CLOSE", base[-1]["file"])
for o in d.get("overlays") or []:
    out("OV", o["file"], "%.3f" % float(o["at"]),
        "%.3f" % float(o["duration"]), "%.3f" % float(o.get("insert_in", 0)))
'
if ! PARSED="$(python3 -c "$PARSE_PY" "$MANIFEST")"; then
  die "could not parse manifest (see message above)"
fi

VERDICT=""; LOUDNORM=0; TARGET_LUFS="-14"; EXPECTED_TOTAL="0"
AD_ID=""; CLOSE_TYPE=""; CLOSE_FILE=""
T_MEDIAN_MAX="?"; T_SHOT_MAX="?"; T_CLOSE_EXEMPT="?"
SHOTS_STR=""; MEDIAN="?"; MAX_NON_CLOSE="?"
SEG_SRC=(); SEG_SS=(); SEG_T=()
OV_SRC=(); OV_AT=(); OV_DUR=(); OV_IN=()

while IFS=$'\t' read -r KIND F1 F2 F3 F4 F5 F6; do
  case "$KIND" in
    META)    AD_ID="$F1"; CLOSE_TYPE="$F2"; VERDICT="$F3"; LOUDNORM="$F4"
             TARGET_LUFS="$F5"; EXPECTED_TOTAL="$F6" ;;
    TARGETS) T_MEDIAN_MAX="$F1"; T_SHOT_MAX="$F2"; T_CLOSE_EXEMPT="$F3" ;;
    SHOTS)   SHOTS_STR="$F1" ;;
    STATS)   MEDIAN="$F1"; MAX_NON_CLOSE="$F2" ;;
    SEG)     SEG_SRC+=("$F1"); SEG_SS+=("$F2"); SEG_T+=("$F3") ;;
    OV)      OV_SRC+=("$F1"); OV_AT+=("$F2"); OV_DUR+=("$F3"); OV_IN+=("$F4") ;;
    CLOSE)   CLOSE_FILE="$F1" ;;
  esac
done <<EOF
$PARSED
EOF

print_rhythm_table() {
  log "RHYTHM (deterministic, from the manifest cut list):"
  log "  targets : median<=${T_MEDIAN_MAX}s  shot<=${T_SHOT_MAX}s  close_exempt=${T_CLOSE_EXEMPT}"
  log "  shots   : ${SHOTS_STR}"
  log "  median  = ${MEDIAN}s   max_non_close = ${MAX_NON_CLOSE}s   verdict = ${VERDICT}"
}

# --- THE REFUSAL: rhythm verdict gates every encode --------------------------
if [ "$VERDICT" != "PASS" ]; then
  print_rhythm_table
  die "REFUSING to stitch: manifest rhythm verdict is '$VERDICT'. Winner cut \
density is 1.1-3.2s median and this timeline misses its RHYTHM CARD. Fix \
edit-side (punch-in overlays, interior trims, spine slices), rebuild the \
manifest, then stitch — never re-render for timing."
fi

NUM_SEGS="${#SEG_SRC[@]}"
NUM_OVS="${#OV_SRC[@]}"
[ "$NUM_SEGS" -ge 1 ] || die "manifest produced no base segments"

log "ad_id=$AD_ID  close_type=$CLOSE_TYPE  segments=$NUM_SEGS  overlays=$NUM_OVS"
log "geometry ${OUT_W}x${OUT_H}@${OUT_FPS}  expected_total=${EXPECTED_TOTAL}s"

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/stitch.XXXXXX")"
cleanup() { rm -rf "$WORKDIR"; }
trap cleanup EXIT

resolve_path() {
  case "$1" in
    /*) [ -f "$1" ] || die "file not found (absolute): $1"; printf '%s' "$1" ;;
    *)  [ -f "$MANIFEST_DIR/$1" ] || die "file not found (relative to manifest): $1"
        printf '%s' "$MANIFEST_DIR/$1" ;;
  esac
}

has_audio_stream() {
  _codec="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type \
            -of default=nw=1:nk=1 "$1" 2>/dev/null)"
  [ "$_codec" = "audio" ]
}

probe_duration() {
  ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$1"
}

VF_GEOM="scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=decrease,pad=${OUT_W}:${OUT_H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=${OUT_FPS}"

# -----------------------------------------------------------------------------
# PASS 0: does the AUDIO RAIL carry audio at all? Silent formats (display-loop
# closes etc.) legally ship picture-only; narrated clips always carry their own
# voice. If ANY segment has audio, audio-less segments are padded with silence
# so the rail stays time-true; if NONE do, the rail is video-only end to end.
# -----------------------------------------------------------------------------
ANY_AUDIO=0
for src in "${SEG_SRC[@]}"; do
  if has_audio_stream "$(resolve_path "$src")"; then ANY_AUDIO=1; break; fi
done
if [ "$LOUDNORM" -eq 1 ] && [ "$ANY_AUDIO" -eq 0 ]; then
  die "manifest is narrated (audio.loudnorm=true) but NO base clip has an \
audio stream — the audio rail lost its voice. Check the clips, do not stitch."
fi
log "audio rail: $([ "$ANY_AUDIO" -eq 1 ] && echo 'present (clips keep their own audio)' || echo 'none (silent plan, picture-only)')"

# -----------------------------------------------------------------------------
# PASS 1: normalize every kept segment (trim window + uniform geometry/fps +
# concat-compatible audio). Interior trims arrive pre-expanded as segments, so
# concatenating these back-to-back IS the planned jump cut.
# -----------------------------------------------------------------------------
SEG_FILES=()
i=0
while [ "$i" -lt "$NUM_SEGS" ]; do
  SRC="$(resolve_path "${SEG_SRC[$i]}")"
  SS="${SEG_SS[$i]}"; T="${SEG_T[$i]}"
  OUTSEG="$WORKDIR/seg_$(printf '%03d' "$i").mp4"
  log "segment $i  [${SS}s +${T}s]  $SRC"
  if [ "$ANY_AUDIO" -eq 1 ]; then
    if has_audio_stream "$SRC"; then
      ffmpeg -nostdin -y -v error -ss "$SS" -t "$T" -i "$SRC" \
        -vf "$VF_GEOM" \
        -af "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo" \
        -r "$OUT_FPS" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
        -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUTSEG" \
        || die "ffmpeg failed normalizing segment $i (${SEG_SRC[$i]})"
    else
      log "WARN: segment $i (${SEG_SRC[$i]}) has NO audio on a rail that carries audio; padding silence to keep time — CHECK THIS CLIP."
      ffmpeg -nostdin -y -v error -ss "$SS" -t "$T" -i "$SRC" \
        -f lavfi -t "$T" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
        -map 0:v:0 -map 1:a:0 -vf "$VF_GEOM" \
        -r "$OUT_FPS" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
        -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUTSEG" \
        || die "ffmpeg failed normalizing (silence-padded) segment $i"
    fi
  else
    ffmpeg -nostdin -y -v error -ss "$SS" -t "$T" -i "$SRC" \
      -vf "$VF_GEOM" -an \
      -r "$OUT_FPS" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
      -movflags +faststart "$OUTSEG" \
      || die "ffmpeg failed normalizing (video-only) segment $i"
  fi
  SEG_FILES+=("$OUTSEG")
  i=$((i + 1))
done

# -----------------------------------------------------------------------------
# PASS 2: concatenate the AUDIO RAIL. Video hard cuts; audio joined STRAIGHT
# (each clip keeps its own voice; joins were planned at line-boundary pauses,
# so there is nothing to crossfade — and nothing ever ducks the voice).
# -----------------------------------------------------------------------------
BASE="$WORKDIR/base.mp4"
FF_INPUTS=()
for f in "${SEG_FILES[@]}"; do FF_INPUTS+=(-i "$f"); done
CONCAT_IN=""
i=0
while [ "$i" -lt "$NUM_SEGS" ]; do
  if [ "$ANY_AUDIO" -eq 1 ]; then
    CONCAT_IN="${CONCAT_IN}[${i}:v:0][${i}:a:0]"
  else
    CONCAT_IN="${CONCAT_IN}[${i}:v:0]"
  fi
  i=$((i + 1))
done
if [ "$ANY_AUDIO" -eq 1 ]; then
  FILTER="${CONCAT_IN}concat=n=${NUM_SEGS}:v=1:a=1[vcat][acat]"
  MAPS=(-map "[vcat]" -map "[acat]" -c:a aac -b:a 192k -ar 48000 -ac 2)
else
  FILTER="${CONCAT_IN}concat=n=${NUM_SEGS}:v=1:a=0[vcat]"
  MAPS=(-map "[vcat]")
fi
log "concatenating audio rail ($NUM_SEGS segment(s), straight joins)"
ffmpeg -nostdin -y -v error "${FF_INPUTS[@]}" -filter_complex "$FILTER" \
  "${MAPS[@]}" -r "$OUT_FPS" \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  -movflags +faststart "$BASE" \
  || die "ffmpeg failed concatenating the base rail"

# -----------------------------------------------------------------------------
# PASS 3: the VIDEO RAIL — punch-in overlays. Each insert is conformed
# video-only (overlay slices are always MUTE), pts-shifted to its absolute
# window, and composited with enable='between(t,at,end)' so it replaces the
# base PICTURE only. The base audio is STREAM-COPIED (-c:a copy) through this
# pass: bit-for-bit continuous across every overlay boundary — the host's
# voice (and hidden lips) never stop.
# -----------------------------------------------------------------------------
if [ "$LOUDNORM" -eq 1 ]; then
  STAGE3_OUT="$WORKDIR/pre.mp4"   # loudnorm still to come
else
  STAGE3_OUT="$OUTPUT"            # silent/SFX-only ships as-is
fi

if [ "$NUM_OVS" -gt 0 ]; then
  OV_FILES=()
  k=0
  while [ "$k" -lt "$NUM_OVS" ]; do
    OSRC="$(resolve_path "${OV_SRC[$k]}")"
    OCONF="$WORKDIR/ov_$(printf '%02d' "$k").mp4"
    log "overlay $k  at=${OV_AT[$k]}s dur=${OV_DUR[$k]}s insert_in=${OV_IN[$k]}s  $OSRC"
    ffmpeg -nostdin -y -v error -ss "${OV_IN[$k]}" -t "${OV_DUR[$k]}" -i "$OSRC" \
      -vf "$VF_GEOM" -an \
      -r "$OUT_FPS" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
      -movflags +faststart "$OCONF" \
      || die "ffmpeg failed conforming overlay $k (${OV_SRC[$k]})"
    OV_FILES+=("$OCONF")
    k=$((k + 1))
  done

  OV_INPUTS=(-i "$BASE")
  for f in "${OV_FILES[@]}"; do OV_INPUTS+=(-i "$f"); done
  OFILTER=""
  PREV="0:v:0"
  k=0
  while [ "$k" -lt "$NUM_OVS" ]; do
    AT="${OV_AT[$k]}"
    # End the enable window a hair early so the boundary frame is the base's.
    END="$(python3 -c 'import sys; print(round(float(sys.argv[1])+float(sys.argv[2])-0.001,3))' "$AT" "${OV_DUR[$k]}")"
    IN=$((k + 1))
    OFILTER="${OFILTER}[${IN}:v:0]setpts=PTS+${AT}/TB[op${k}];"
    OFILTER="${OFILTER}[${PREV}][op${k}]overlay=eof_action=pass:enable='between(t,${AT},${END})'[vc${k}];"
    PREV="vc${k}"
    k=$((k + 1))
  done
  OFILTER="${OFILTER%;}"
  if [ "$ANY_AUDIO" -eq 1 ]; then
    AMAPS=(-map 0:a:0 -c:a copy)   # THE bit-continuity guarantee
  else
    AMAPS=()
  fi
  log "compositing $NUM_OVS punch-in(s); base audio stream-copied (bit-continuous)"
  ffmpeg -nostdin -y -v error "${OV_INPUTS[@]}" \
    -filter_complex "$OFILTER" -map "[${PREV}]" "${AMAPS[@]}" \
    -r "$OUT_FPS" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
    -movflags +faststart "$STAGE3_OUT" \
    || die "ffmpeg failed compositing overlays"
else
  if [ "$LOUDNORM" -eq 1 ]; then
    cp "$BASE" "$STAGE3_OUT"
  else
    # No overlays, no loudnorm: the concatenated rail IS the deliverable.
    ffmpeg -nostdin -y -v error -i "$BASE" -c copy -movflags +faststart "$STAGE3_OUT" \
      || die "ffmpeg failed finalizing (copy) the base rail"
  fi
fi

# -----------------------------------------------------------------------------
# PASS 4: loudness. Narrated -> TWO-PASS loudnorm to the manifest target
# (measure, then linear gain; a dynamic single pass cannot hit the target
# reliably and sibling ads would ship at different volumes). Video is
# stream-copied — this pass touches audio only. Silent plans skip entirely.
# -----------------------------------------------------------------------------
if [ "$LOUDNORM" -eq 1 ]; then
  log "loudnorm pass 1/2: measuring integrated loudness (target ${TARGET_LUFS} LUFS)"
  MEAS="$(ffmpeg -nostdin -hide_banner -v info -i "$STAGE3_OUT" \
            -af "loudnorm=I=${TARGET_LUFS}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}:print_format=json" \
            -f null - 2>&1 || true)"
  LN_VALUES="$(printf '%s\n' "$MEAS" | python3 -c '
import sys, json, re
m = re.findall(r"\{[^{}]*\}", sys.stdin.read(), re.S)
if not m: sys.exit(1)
d = json.loads(m[-1])
print(" ".join([d.get("input_i","0"), d.get("input_tp","0"),
                d.get("input_lra","0"), d.get("input_thresh","0"),
                d.get("target_offset","0")]))
' 2>/dev/null || true)"
  if [ -n "$LN_VALUES" ]; then
    # shellcheck disable=SC2086
    set -- $LN_VALUES
    log "loudnorm pass 2/2: applying linear gain (measured_I=$1)"
    AOUT="loudnorm=I=${TARGET_LUFS}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}:measured_I=$1:measured_TP=$2:measured_LRA=$3:measured_thresh=$4:offset=$5:linear=true"
  else
    log "WARN: could not parse loudnorm measurement; single dynamic pass (approximate)"
    AOUT="loudnorm=I=${TARGET_LUFS}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}"
  fi
  ffmpeg -nostdin -y -v error -i "$STAGE3_OUT" \
    -af "$AOUT" -c:v copy \
    -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUTPUT" \
    || die "ffmpeg failed during loudness normalization"
else
  log "audio: normalization SKIPPED (silent/SFX-only plan ships as-is; never boost noise)"
fi

[ -f "$OUTPUT" ] || die "ffmpeg reported success but output is missing: $OUTPUT"
log "wrote $OUTPUT"

# -----------------------------------------------------------------------------
# QC AFTER ENCODE
# -----------------------------------------------------------------------------
log "QC: probing output streams and duration"
VSTREAMS="$(ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
ASTREAMS="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
[ "${VSTREAMS:-0}" -ge 1 ] || die "QC FAIL: output has no VIDEO stream"
if [ "$LOUDNORM" -eq 1 ]; then
  [ "${ASTREAMS:-0}" -ge 1 ] || die "QC FAIL: narrated ad has no AUDIO stream — the voice is the ad"
  log "QC: streams video=$VSTREAMS audio=$ASTREAMS (narrated) OK"
else
  log "QC: streams video=$VSTREAMS audio=$ASTREAMS (silent plan; audio optional) OK"
fi

ACTUAL_DUR="$(probe_duration "$OUTPUT")"
if python3 - "$ACTUAL_DUR" "$EXPECTED_TOTAL" "$DURATION_TOLERANCE" <<'PYEOF'
import sys
actual, expected, tol = (float(a) for a in sys.argv[1:4])
diff = abs(actual - expected)
sys.stderr.write("QC duration: actual=%.3fs expected=%.3fs diff=%.3fs tol=%.3fs\n"
                 % (actual, expected, diff, tol))
sys.exit(0 if diff <= tol else 1)
PYEOF
then
  log "QC: duration ${ACTUAL_DUR}s within ${DURATION_TOLERANCE}s of expected ${EXPECTED_TOTAL}s OK"
else
  die "QC FAIL: output duration ${ACTUAL_DUR}s deviates from expected ${EXPECTED_TOTAL}s by more than ${DURATION_TOLERANCE}s (an overlay must never add or remove time — it replaces picture only)"
fi

print_rhythm_table
log "ENDS ON: ${CLOSE_FILE} (typed close verified at manifest time)"
log "SUCCESS: '$AD_ID' assembled -> $OUTPUT"
exit 0
