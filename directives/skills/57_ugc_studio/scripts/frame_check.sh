#!/usr/bin/env bash
# =============================================================================
# frame_check.sh  --  contact sheets for the pre-assembly FRAME CHECK (UGC Studio)
# =============================================================================
#
# Tiles every generation's frames into one PNG per clip so the orchestrator
# can LOOK at what each generation actually contains BEFORE cutting and
# assembly. Never declare "the clip is right" from the prompt or a single
# sampled frame — read the whole sheet, for every clip.
#
# The sheet is a CONTENT check against the plan: is the character on-model
# with the locked references, did each planned sub-shot's hard cut actually
# render (whisper_cut.py reconciles the timing; the SHEET confirms the
# content on either side of the cut), did any text sneak into a frame, is
# the product at a believable scale, did a green-screen background drift
# muted. A content miss is rescued in the EDIT (slice, crop punch-in,
# overlay) whenever possible — a re-render is the member's call and needs
# its own fresh yes.
#
# Reading a sheet: frames are row-major (left-to-right, top-to-bottom) at
# 2fps, so frame N sits at N/2 seconds INTO THE CLIP.
#
# USAGE   frame_check.sh <gens_dir> <frames_dir>
# DEPS    ffmpeg, ffprobe, python3
# EXIT    0 success · 2 missing dependency · 1 any other failure
# =============================================================================
set -euo pipefail

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 2; }

[ "$#" -eq 2 ] || { echo "Usage: $0 <gens_dir> <frames_dir>" >&2; exit 1; }
GENS="$1"; FRAMES="$2"
[ -d "$GENS" ] || { echo "ERROR: gens dir not found: $GENS" >&2; exit 1; }
mkdir -p "$FRAMES"

FPS=2      # 2fps reads a 4-9s gen as 8-18 tiles: dense enough to catch a bad
COLS=6     # sub-shot, small enough to read at a glance

FOUND=0
FAILED=0
for CLIP in "$GENS"/*.mp4 "$GENS"/*.MP4; do
  [ -f "$CLIP" ] || continue
  FOUND=$((FOUND + 1))
  BASE="$(basename "$CLIP")"
  OUT="$FRAMES/${BASE%.*}.png"

  DUR="$(ffprobe -v error -show_entries format=duration \
        -of default=nokey=1:noprint_wrappers=1 "$CLIP" || true)"
  case "$DUR" in
    ''|N/A) echo "ERROR: could not read duration of $CLIP (corrupt download?)" >&2
            FAILED=$((FAILED + 1)); continue ;;
  esac
  N="$(python3 -c 'import math,sys;print(max(1,int(math.ceil(float(sys.argv[1])*float(sys.argv[2])))))' "$DUR" "$FPS")"
  ROWS="$(python3 -c 'import math,sys;print(max(1,int(math.ceil(float(sys.argv[1])/float(sys.argv[2])))))' "$N" "$COLS")"

  if ffmpeg -nostdin -y -v error -i "$CLIP" \
       -vf "fps=${FPS},scale=160:-2,tile=${COLS}x${ROWS}" -frames:v 1 "$OUT"; then
    echo "wrote $OUT  (~${N} frames @ ${FPS}fps in a ${COLS}x${ROWS} grid; frame N = N/${FPS}s into the clip)"
  else
    echo "ERROR: contact sheet failed for $CLIP" >&2
    FAILED=$((FAILED + 1))
  fi
done

if [ "$FOUND" -eq 0 ]; then
  echo "ERROR: no .mp4 files in $GENS — nothing to check (wrong dir, or gens not downloaded yet?)" >&2
  exit 1
fi
if [ "$FAILED" -gt 0 ]; then
  echo "ERROR: $FAILED of $FOUND sheets failed" >&2
  exit 1
fi
echo "OK: $FOUND contact sheets in $FRAMES — read EVERY sheet before assembly"
exit 0
