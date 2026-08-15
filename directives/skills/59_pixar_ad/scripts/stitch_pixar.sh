#!/usr/bin/env bash
# =============================================================================
# stitch_pixar.sh  --  Pixar Ad assembler (voiceover-first)
# =============================================================================
#
# WHAT THIS DOES
#   Takes pixar-ad-manifest.json and assembles ONE 9:16 1080x1920 30fps ad:
#     1. Concatenate each scene's VIDEO, trimmed to its picture-locked VO span,
#        scaled+padded to 1080x1920 (the clips are silent or SFX-only). A clip that
#        runs SHORTER than its span (round-to-nearest generations may run up to
#        ~0.5s short) is freeze-held: its last frame is cloned out to exactly the
#        span, so every later scene still lands on its own VO words.
#     2. Lay the single ElevenLabs VO over the WHOLE picture as the master audio.
#     3. If keep_sfx is true, duck each scene's own SFX UNDER the VO (sidechain
#        compression keyed off the VO) so the narration always sits on top.
#     4. Lock the picture to the VO length (pad the last frame / trim to fit).
#     5. Loudness-normalize the final mix to about -14 LUFS.
#
# THE AUDIO RULE (inverse of the UGC factory)
#   The voice is EXTERNAL: one ElevenLabs VO is the master spine, laid over the
#   top. Clips never carry dialogue. SFX (if any) is ducked beneath the VO.
#
# THE VOICE IS UNTOUCHABLE
#   The VO file is never trimmed, stretched, silence-cut, sped up, or altered in
#   any way to fit the picture. Sync is always reconciled on the PICTURE side
#   (per-segment freeze-holds, the final tpad/trim). Re-voicing is a member
#   decision, never an assembly step.
#
# THERE ARE NO CAPTIONS
#   This assembler has NO caption path at all. The Pixar skill never burns
#   text of any kind — no captions, no day labels, no offer banners. The VO
#   carries the milestones and the offer; the footage ships clean.
#
# USAGE   stitch_pixar.sh <pixar-ad-manifest.json> <output.mp4>
# DEPS    ffmpeg, ffprobe, python3   (jq NOT required)
# EXIT    0 success · 2 missing dependency · 1 any other failure
# =============================================================================
set -euo pipefail

# ---- tunables (env-overridable) --------------------------------------------
OUT_W=1080; OUT_H=1920; OUT_FPS=30
LOUDNORM_I="${LOUDNORM_I:--14}"
LOUDNORM_TP="${LOUDNORM_TP:--1.5}"
LOUDNORM_LRA="${LOUDNORM_LRA:-11}"
LOUDNORM_TWO_PASS="${LOUDNORM_TWO_PASS:-1}"
SFX_DUCK_VOL="${SFX_DUCK_VOL:-0.45}"     # static attenuation on the ducked SFX
DURATION_TOLERANCE="${DURATION_TOLERANCE:-0.6}"

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 2; }

[ "$#" -eq 2 ] || { echo "Usage: $0 <manifest.json> <output.mp4>   (no caption flag exists — this skill never burns text)" >&2; exit 1; }
MANIFEST="$1"; OUTPUT="$2"
[ -f "$MANIFEST" ] || { echo "ERROR: manifest not found: $MANIFEST" >&2; exit 1; }
MDIR="$(cd "$(dirname "$MANIFEST")" && pwd)"

log() { printf '[pixar %s] %s\n' "$(basename "$OUTPUT")" "$1"; }
die() { printf '[pixar %s] ERROR: %s\n' "$(basename "$OUTPUT")" "$1" >&2; exit 1; }

# ---- read manifest with python (no jq) -------------------------------------
VO_TRACK="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("vo_track") or "")' "$MANIFEST")"
[ -n "$VO_TRACK" ] || die "manifest has no vo_track (the Pixar Ad requires a voice spine)"
KEEP_SFX="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(1 if d.get("keep_sfx",True) else 0)' "$MANIFEST")"

SCENES_TSV="$(python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
for s in d.get("scenes",[]):
    ti=float(s.get("trim_in") or 0); to=float(s.get("trim_out"))
    sys.stdout.write("%s\t%s\t%s\t%s\n" % (s.get("clip"), repr(ti), repr(to), 1 if s.get("sfx") else 0))
' "$MANIFEST")"
[ -n "$SCENES_TSV" ] || die "manifest has no scenes"

# resolve a possibly-relative path against the manifest dir
resolve() { case "$1" in /*) printf '%s' "$1";; *) printf '%s' "$MDIR/$1";; esac; }
VO_ABS="$(resolve "$VO_TRACK")"; [ -f "$VO_ABS" ] || die "vo_track not found: $VO_ABS"
VO_DUR="$(ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$VO_ABS")"
log "vo=$VO_ABS (${VO_DUR}s)  keep_sfx=$KEEP_SFX  geometry=${OUT_W}x${OUT_H}@${OUT_FPS}"

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/skelstitch.XXXXXX")"
trap 'rm -rf "$WORKDIR"' EXIT

VF_GEOM="scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=decrease,pad=${OUT_W}:${OUT_H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=${OUT_FPS}"

has_audio() {
  [ "$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of default=nw=1:nk=1 "$1" 2>/dev/null)" = "audio" ]
}

# ---- PASS 1: normalize each scene to a silent video seg + an SFX wav --------
VLIST="$WORKDIR/vlist.txt"; ALIST="$WORKDIR/alist.txt"
: > "$VLIST"; : > "$ALIST"
i=0; PIC_TOTAL=0
while IFS="$(printf '\t')" read -r CLIP TI TO SFX; do
  [ -n "${CLIP:-}" ] || continue
  SRC="$(resolve "$CLIP")"; [ -f "$SRC" ] || die "clip not found: $SRC"
  DUR="$(python3 -c 'import sys;print(round(float(sys.argv[2])-float(sys.argv[1]),6))' "$TI" "$TO")"
  case "$DUR" in -*|0|0.0|0.000000) die "scene $i ($CLIP) has non-positive span";; esac
  SEGV="$WORKDIR/seg_$(printf '%03d' "$i").mp4"
  SEGA="$WORKDIR/seg_$(printf '%03d' "$i").wav"

  # tpad clones the last frame (2s headroom) and the output -t cuts at exactly DUR:
  # a source clip shorter than its span (round-to-nearest generations) is freeze-held
  # to the span instead of silently shortening the timeline and desyncing every
  # scene after it. The VO itself is never touched.
  ffmpeg -nostdin -y -v error -ss "$TI" -t "$DUR" -i "$SRC" -an \
    -vf "$VF_GEOM,tpad=stop_mode=clone:stop_duration=2" -r "$OUT_FPS" -t "$DUR" \
    -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
    "$SEGV" || die "failed normalizing video seg $i ($CLIP)"
  printf "file '%s'\n" "$SEGV" >> "$VLIST"

  if [ "$KEEP_SFX" = "1" ] && [ "$SFX" = "1" ] && has_audio "$SRC"; then
    # apad + output -t mirrors the video freeze-hold: silence fills any SFX shortfall.
    ffmpeg -nostdin -y -v error -ss "$TI" -t "$DUR" -i "$SRC" -vn \
      -af "aresample=48000,apad=pad_dur=2" -t "$DUR" -ac 2 -ar 48000 "$SEGA" || die "failed SFX seg $i"
  else
    ffmpeg -nostdin -y -v error -f lavfi -t "$DUR" -i "anullsrc=r=48000:cl=stereo" \
      "$SEGA" || die "failed silence seg $i"
  fi
  printf "file '%s'\n" "$SEGA" >> "$ALIST"

  PIC_TOTAL="$(python3 -c 'import sys;print(round(float(sys.argv[1])+float(sys.argv[2]),6))' "$PIC_TOTAL" "$DUR")"
  i=$((i+1))
done <<EOF
$SCENES_TSV
EOF
[ "$i" -ge 1 ] || die "no usable scenes"
log "normalized $i scene(s); picture total ${PIC_TOTAL}s vs VO ${VO_DUR}s"

# ---- PASS 2: concat (copy, segments already uniform) -----------------------
PICTURE="$WORKDIR/picture.mp4"; SFXTRACK="$WORKDIR/sfx.wav"
ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$VLIST" -c copy "$PICTURE" \
  || die "video concat failed"
HAVE_SFX=0
if [ "$KEEP_SFX" = "1" ]; then
  ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$ALIST" -c copy "$SFXTRACK" \
    && HAVE_SFX=1 || HAVE_SFX=0
fi

# ---- PASS 3: lock picture to VO length + mix VO over (ducked) SFX -----------
PRE="$WORKDIR/pre.mp4"
# pad the last frame up to +5s so a slightly-short picture covers the VO; -t trims exact.
VPAD="[0:v]tpad=stop_mode=clone:stop_duration=5[vpad]"
if [ "$HAVE_SFX" = "1" ]; then
  log "mixing VO over ducked SFX"
  FILTER="${VPAD};\
[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,asplit=2[vo_main][vo_key];\
[2:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[sfx_in];\
[sfx_in][vo_key]sidechaincompress=threshold=0.03:ratio=12:attack=5:release=250[sfx_duck];\
[sfx_duck]volume=${SFX_DUCK_VOL}[sfx_low];\
[vo_main][sfx_low]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
  ffmpeg -nostdin -y -v error -i "$PICTURE" -i "$VO_ABS" -i "$SFXTRACK" \
    -filter_complex "$FILTER" -map "[vpad]" -map "[aout]" -t "$VO_DUR" \
    -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r "$OUT_FPS" \
    -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$PRE" \
    || die "mix (with SFX) failed"
else
  log "laying VO over silent picture"
  FILTER="${VPAD};[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]"
  ffmpeg -nostdin -y -v error -i "$PICTURE" -i "$VO_ABS" \
    -filter_complex "$FILTER" -map "[vpad]" -map "[aout]" -t "$VO_DUR" \
    -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r "$OUT_FPS" \
    -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$PRE" \
    || die "mix (VO only) failed"
fi
[ -f "$PRE" ] || die "intermediate missing: $PRE"

# ---- PASS 4: loudness normalize to -14 LUFS --------------------------------
if [ "$LOUDNORM_TWO_PASS" = "1" ]; then
  log "loudnorm pass 1/2 (measure)"
  MEAS="$(ffmpeg -nostdin -hide_banner -v info -i "$PRE" \
            -af "loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}:print_format=json" \
            -f null - 2>&1 || true)"
  LN="$(printf '%s\n' "$MEAS" | python3 -c '
import sys,json,re
t=sys.stdin.read(); m=re.findall(r"\{[^{}]*\}",t,re.S)
if not m: sys.exit(1)
d=json.loads(m[-1])
print(" ".join([d.get("input_i","0"),d.get("input_tp","0"),d.get("input_lra","0"),d.get("input_thresh","0"),d.get("target_offset","0")]))
' 2>/dev/null || true)"
  if [ -n "$LN" ]; then
    # shellcheck disable=SC2086
    set -- $LN
    AF="loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}:measured_I=$1:measured_TP=$2:measured_LRA=$3:measured_thresh=$4:offset=$5:linear=true:print_format=summary"
    log "loudnorm pass 2/2 (apply linear, measured_I=$1)"
  else
    log "WARN: could not measure loudness; single-pass"
    AF="loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}"
  fi
else
  AF="loudnorm=I=${LOUDNORM_I}:TP=${LOUDNORM_TP}:LRA=${LOUDNORM_LRA}"
fi

# No caption pass exists in this assembler: the Pixar skill never burns text.
ffmpeg -nostdin -y -v error -i "$PRE" -af "$AF" -c:v copy \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUTPUT" \
  || die "loudnorm failed"
[ -f "$OUTPUT" ] || die "output missing: $OUTPUT"

# ---- QC --------------------------------------------------------------------
VS="$(ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
AS="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
[ "${VS:-0}" -ge 1 ] || die "QC: output has no video stream"
[ "${AS:-0}" -ge 1 ] || die "QC: output has no audio stream (the VO must be present)"
ACT="$(ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$OUTPUT")"
if python3 - "$ACT" "$VO_DUR" "$DURATION_TOLERANCE" <<'PY'
import sys
a,e,t=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])
sys.stderr.write("QC duration: actual=%.3fs vo=%.3fs diff=%.3fs tol=%.3fs\n"%(a,e,abs(a-e),t))
sys.exit(0 if abs(a-e)<=t else 1)
PY
then log "QC ok: ${ACT}s ≈ VO ${VO_DUR}s, v=$VS a=$AS"
else die "QC: output ${ACT}s deviates from VO ${VO_DUR}s by more than ${DURATION_TOLERANCE}s"
fi

log "SUCCESS -> $OUTPUT"
exit 0
