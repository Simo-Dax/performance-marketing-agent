#!/usr/bin/env bash
# =============================================================================
# stitch_talking.sh  --  Talking-Object Ad assembler (dialogue-first, native audio)
# =============================================================================
#
# WHAT THIS DOES
#   Takes talking-object-ad-manifest.json and assembles ONE 9:16 1080x1920 30fps ad:
#     1. Trim each scene to trim_in..trim_out KEEPING ITS NATIVE AUDIO — the
#        characters' dialogue IS the soundtrack (there is no external VO in this
#        factory). Video is scaled+padded to 1080x1920; a clip a hair shorter than
#        its span is freeze-held (video) / silence-padded (audio) to the span.
#     2. Hard-concat the scenes in manifest order. No crossfades.
#     3. Loudness-normalize the whole mix to about -14 LUFS (dialogue levels vary
#        between generations; this pass makes the cast sound like one ad).
#
# THE AUDIO RULE (inverted from the VO-first family)
#   There is NO overlay pass: no VO track, no music bed, nothing laid over the
#   picture. Each clip's own generated dialogue+ambience is kept end to end. A
#   dialogue scene arriving with NO audio stream is a build error upstream
#   (dialogue_check.py fails it) — here it is filled with silence and WARNED
#   loudly so a broken concat never ships silently.
#
# THERE ARE NO CAPTIONS
#   This assembler has NO caption path at all. The one legal text in the ad (the
#   CTA's in-scene 3D offer text) is RENDERED by the generator inside the scene,
#   never burned at assembly.
#
# USAGE   stitch_talking.sh <talking-object-ad-manifest.json> <output.mp4>
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
DURATION_TOLERANCE="${DURATION_TOLERANCE:-0.6}"

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 2; }

[ "$#" -eq 2 ] || { echo "Usage: $0 <manifest.json> <output.mp4>   (no caption flag exists — this skill never burns text)" >&2; exit 1; }
MANIFEST="$1"; OUTPUT="$2"
[ -f "$MANIFEST" ] || { echo "ERROR: manifest not found: $MANIFEST" >&2; exit 1; }
MDIR="$(cd "$(dirname "$MANIFEST")" && pwd)"

log() { printf '[talking %s] %s\n' "$(basename "$OUTPUT")" "$1"; }
die() { printf '[talking %s] ERROR: %s\n' "$(basename "$OUTPUT")" "$1" >&2; exit 1; }

# ---- read manifest with python (no jq) -------------------------------------
AUDIO_MODE="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("audio_mode") or "")' "$MANIFEST")"
[ "$AUDIO_MODE" = "native" ] || die "manifest audio_mode is '$AUDIO_MODE', expected 'native' (run build_manifest.py from THIS skill)"
VO_TRACK="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("vo_track") or "")' "$MANIFEST")"
[ -z "$VO_TRACK" ] || die "manifest carries a vo_track — the talking-object factory has no external voiceover"

SCENES_TSV="$(python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
for s in d.get("scenes",[]):
    ti=float(s.get("trim_in") or 0); to=float(s.get("trim_out"))
    sys.stdout.write("%s\t%s\t%s\n" % (s.get("clip"), repr(ti), repr(to)))
' "$MANIFEST")"
[ -n "$SCENES_TSV" ] || die "manifest has no scenes"

resolve() { case "$1" in /*) printf '%s' "$1";; *) printf '%s' "$MDIR/$1";; esac; }

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/tobjstitch.XXXXXX")"
trap 'rm -rf "$WORKDIR"' EXIT

VF_GEOM="scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=decrease,pad=${OUT_W}:${OUT_H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=${OUT_FPS}"

has_audio() {
  [ "$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of default=nw=1:nk=1 "$1" 2>/dev/null)" = "audio" ]
}

# ---- PASS 1: normalize each scene to a uniform seg WITH its native audio ----
SEGLIST="$WORKDIR/segs.txt"
: > "$SEGLIST"
i=0; PIC_TOTAL=0; SILENT_SCENES=0
while IFS="$(printf '\t')" read -r CLIP TI TO; do
  [ -n "${CLIP:-}" ] || continue
  SRC="$(resolve "$CLIP")"; [ -f "$SRC" ] || die "clip not found: $SRC"
  DUR="$(python3 -c 'import sys;print(round(float(sys.argv[2])-float(sys.argv[1]),6))' "$TI" "$TO")"
  case "$DUR" in -*|0|0.0|0.000000) die "scene $i ($CLIP) has non-positive span";; esac
  SEG="$WORKDIR/seg_$(printf '%03d' "$i").mp4"

  if has_audio "$SRC"; then
    # tpad clones the last video frame / apad pads the audio (2s headroom); the
    # output -t cuts both at exactly DUR — trim_out lands at speech_end + hold
    # without ever cutting a word or desyncing the concat.
    ffmpeg -nostdin -y -v error -ss "$TI" -t "$DUR" -i "$SRC" \
      -vf "$VF_GEOM,tpad=stop_mode=clone:stop_duration=2" \
      -af "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,apad=pad_dur=2" \
      -t "$DUR" -r "$OUT_FPS" \
      -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 48000 -ac 2 \
      "$SEG" || die "failed normalizing seg $i ($CLIP)"
  else
    SILENT_SCENES=$((SILENT_SCENES+1))
    log "WARN: scene $i ($CLIP) has NO AUDIO STREAM — a dialogue clip should never reach the stitcher silent (dialogue_check.py fails these). Filling with silence."
    ffmpeg -nostdin -y -v error -ss "$TI" -t "$DUR" -i "$SRC" \
      -f lavfi -t "$DUR" -i "anullsrc=r=48000:cl=stereo" \
      -map 0:v:0 -map 1:a:0 \
      -vf "$VF_GEOM,tpad=stop_mode=clone:stop_duration=2" -t "$DUR" -r "$OUT_FPS" \
      -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
      -c:a aac -b:a 192k -ar 48000 -ac 2 \
      "$SEG" || die "failed normalizing silent seg $i ($CLIP)"
  fi
  printf "file '%s'\n" "$SEG" >> "$SEGLIST"

  PIC_TOTAL="$(python3 -c 'import sys;print(round(float(sys.argv[1])+float(sys.argv[2]),6))' "$PIC_TOTAL" "$DUR")"
  i=$((i+1))
done <<EOF
$SCENES_TSV
EOF
[ "$i" -ge 1 ] || die "no usable scenes"
log "normalized $i scene(s) with native audio; timeline total ${PIC_TOTAL}s"

# ---- PASS 2: hard concat (segments already uniform) -------------------------
PRE="$WORKDIR/pre.mp4"
ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$SEGLIST" -c copy "$PRE" \
  || die "concat failed"

# ---- PASS 3: loudness normalize to -14 LUFS ---------------------------------
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

# No caption pass exists in this assembler: the talking-object skill never burns text.
ffmpeg -nostdin -y -v error -i "$PRE" -af "$AF" -c:v copy \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUTPUT" \
  || die "loudnorm failed"
[ -f "$OUTPUT" ] || die "output missing: $OUTPUT"

# ---- QC --------------------------------------------------------------------
VS="$(ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
AS="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$OUTPUT" | wc -l | tr -d ' ')"
[ "${VS:-0}" -ge 1 ] || die "QC: output has no video stream"
[ "${AS:-0}" -ge 1 ] || die "QC: output has no audio stream (the dialogue must be present)"
ACT="$(ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$OUTPUT")"
if python3 - "$ACT" "$PIC_TOTAL" "$DURATION_TOLERANCE" <<'PY'
import sys
a,e,t=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])
sys.stderr.write("QC duration: actual=%.3fs planned=%.3fs diff=%.3fs tol=%.3fs\n"%(a,e,abs(a-e),t))
sys.exit(0 if abs(a-e)<=t else 1)
PY
then log "QC ok: ${ACT}s ≈ planned ${PIC_TOTAL}s, v=$VS a=$AS"
else die "QC: output ${ACT}s deviates from the planned ${PIC_TOTAL}s by more than ${DURATION_TOLERANCE}s"
fi
[ "$SILENT_SCENES" -eq 0 ] || log "WARN: $SILENT_SCENES scene(s) shipped with silence-filled audio — check the dialogue_check reports before delivering"

log "SUCCESS -> $OUTPUT"
exit 0
