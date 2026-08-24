#!/usr/bin/env bash
# =============================================================================
# frame_check.sh  --  contact sheet for the pre-stitch FRAME CHECK (Step 6.5)
# =============================================================================
#
# Tiles a clip's frames into one PNG so the orchestrator can LOOK at what each
# generation actually contains and map every visible beat against the VO word
# timeline (timing.json) BEFORE stitching. Never declare "the picture matches
# the voice" from the prompt or a single sampled frame — read the whole sheet.
#
# Reading the sheet: frames are row-major (left→right, top→bottom) at FPS
# frames per second, so frame N sits at N/FPS seconds INTO THE CLIP. Add the
# scene's `start` from scenes.json to place a frame on the ad's absolute VO
# timeline. A beat that lands off its spoken word is fixed by RE-CUTTING the
# existing clip (ffmpeg trim/concat/freeze-pad) — never by re-rendering.
#
# USAGE   frame_check.sh <clip.mp4> <out.png> [fps]     (fps default 5)
# DEPS    ffmpeg, ffprobe, python3
# EXIT    0 success · 2 missing dependency · 1 any other failure
# =============================================================================
set -euo pipefail

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 2; }

[ "$#" -ge 2 ] || { echo "Usage: $0 <clip.mp4> <out.png> [fps]" >&2; exit 1; }
CLIP="$1"; OUT="$2"; FPS="${3:-5}"
[ -f "$CLIP" ] || { echo "ERROR: clip not found: $CLIP" >&2; exit 1; }

DUR="$(ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$CLIP")"
COLS=6
N="$(python3 -c 'import math,sys;print(max(1,int(math.ceil(float(sys.argv[1])*float(sys.argv[2])))))' "$DUR" "$FPS")"
ROWS="$(python3 -c 'import math,sys;print(max(1,int(math.ceil(float(sys.argv[1])/6.0))))' "$N")"

ffmpeg -nostdin -y -v error -i "$CLIP" \
  -vf "fps=${FPS},scale=160:-2,tile=${COLS}x${ROWS}" -frames:v 1 "$OUT" \
  || { echo "ERROR: contact sheet failed for $CLIP" >&2; exit 1; }

echo "wrote $OUT  (~${N} frames @ ${FPS}fps in a ${COLS}x${ROWS} grid; frame N = N/${FPS}s into the clip)"
exit 0
