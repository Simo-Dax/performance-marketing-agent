#!/usr/bin/env bash
# =============================================================================
# stitch_podcast.sh  --  assemble the per-turn clips into the finished ad.
#
# Reads an assembly-manifest.json (ordered_timeline of clips in conversation
# order), conforms every clip to 1080x1920@30, concatenates KEEPING each clip's
# own baked audio (never mutes, no separate spine), two-pass loudness-normalizes
# the final mix to -14 LUFS, and QC-checks the output has video + audio.
#
# Usage:  stitch_podcast.sh  <assembly-manifest.json>  <output.mp4>
# Exit:   0 ok, 2 missing dependency, 1 any other failure.
# =============================================================================
set -euo pipefail

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not on PATH"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not on PATH" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not on PATH" >&2; exit 2; }

[ "$#" -eq 2 ] || { echo "Usage: $0 <manifest.json> <output.mp4>" >&2; exit 1; }
MAN="$1"; OUT="$2"
[ -f "$MAN" ] || { echo "manifest not found: $MAN" >&2; exit 1; }
MANDIR="$(cd "$(dirname "$MAN")" && pwd)"

TMP="$(mktemp -d "${TMPDIR:-/tmp}/podstitch.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

# Resolve the ordered clip paths (relative to the manifest dir) with python.
python3 - "$MAN" "$MANDIR" > "$TMP/paths.txt" <<'PY'
import json, os, sys
man = json.load(open(sys.argv[1])); base = sys.argv[2]
for step in man.get("ordered_timeline", []):
    c = step["clip"]
    print(c if os.path.isabs(c) else os.path.join(base, c))
PY

[ -s "$TMP/paths.txt" ] || { echo "manifest has no clips" >&2; exit 1; }

VF="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30"
i=0
: > "$TMP/concat.txt"
while IFS= read -r clip; do
  [ -n "$clip" ] || continue
  [ -f "$clip" ] || { echo "missing clip: $clip" >&2; exit 1; }
  seg="$TMP/seg_$(printf '%03d' "$i").mp4"
  ffmpeg -nostdin -y -v error -i "$clip" \
    -vf "$VF" -af "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo" \
    -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$seg" \
    || { echo "ffmpeg failed conforming $clip" >&2; exit 1; }
  printf "file '%s'\n" "$seg" >> "$TMP/concat.txt"
  i=$((i + 1))
done < "$TMP/paths.txt"

JOIN="$TMP/join.mp4"
ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$TMP/concat.txt" -c copy "$JOIN" \
  || { echo "ffmpeg concat failed" >&2; exit 1; }

# -14 LUFS loudness normalization. TWO-PASS (measure, then apply with linear gain) so the
# final mix lands exactly on target -- matches the house standard across the video skills.
# Falls back to single-pass if the measurement can't be parsed.
LN_I=-14; LN_TP=-1.5; LN_LRA=11
MEAS="$(ffmpeg -nostdin -hide_banner -v info -i "$JOIN" \
          -af "loudnorm=I=${LN_I}:TP=${LN_TP}:LRA=${LN_LRA}:print_format=json" \
          -f null - 2>&1 || true)"
LN="$(printf '%s\n' "$MEAS" | python3 -c '
import sys, json, re
t = sys.stdin.read(); m = re.findall(r"\{[^{}]*\}", t, re.S)
if not m: sys.exit(1)
d = json.loads(m[-1])
print(" ".join([d.get("input_i","0"), d.get("input_tp","0"), d.get("input_lra","0"),
                d.get("input_thresh","0"), d.get("target_offset","0")]))
' 2>/dev/null || true)"
if [ -n "$LN" ]; then
  # shellcheck disable=SC2086
  set -- $LN
  AF="loudnorm=I=${LN_I}:TP=${LN_TP}:LRA=${LN_LRA}:measured_I=$1:measured_TP=$2:measured_LRA=$3:measured_thresh=$4:offset=$5:linear=true:print_format=summary"
else
  echo "WARN: could not measure loudness; single-pass loudnorm" >&2
  AF="loudnorm=I=${LN_I}:TP=${LN_TP}:LRA=${LN_LRA}"
fi
ffmpeg -nostdin -y -v error -i "$JOIN" -af "$AF" \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT" \
  || { echo "ffmpeg loudnorm failed" >&2; exit 1; }

V=$(ffprobe -v error -select_streams v -show_entries stream=index -of csv=p=0 "$OUT" | wc -l | tr -d ' ')
A=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$OUT" | wc -l | tr -d ' ')
[ "${V:-0}" -ge 1 ] || { echo "QC FAIL: no video stream" >&2; exit 1; }
[ "${A:-0}" -ge 1 ] || { echo "QC FAIL: no audio stream (this factory never mutes)" >&2; exit 1; }
D=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OUT")
echo "stitched $i clips -> $OUT (${D}s, 9:16 1080p, -14 LUFS)"
