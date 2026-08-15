#!/usr/bin/env bash
# =============================================================================
# last_frame.sh <input.mp4> <output.png>
# -----------------------------------------------------------------------------
# Extract a clip's FINAL frame as a still image. Used ONLY as a fallback for an
# image-only Path C backend (fal) that cannot accept a video reference: take the
# HOOK clip's last frame and pass it as the style reference. Not used for chaining;
# the skill always references the hook clip and hard-cuts.
#
# DEPS  ffmpeg, ffprobe
# EXIT  0 success - 2 missing dependency - 1 any other failure
# =============================================================================
set -euo pipefail

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found" >&2; exit 2; }

[ "$#" -eq 2 ] || { echo "Usage: $0 <input.mp4> <output.png>" >&2; exit 1; }
IN="$1"; OUT="$2"
[ -f "$IN" ] || { echo "ERROR: input not found: $IN" >&2; exit 1; }
mkdir -p "$(dirname "$OUT")"

# Fast path: seek to ~0.15s before the end and grab one frame.
if ffmpeg -nostdin -y -v error -sseof -0.15 -i "$IN" -update 1 -frames:v 1 "$OUT" 2>/dev/null \
   && [ -s "$OUT" ]; then
  :
else
  # Robust fallback: decode the whole clip writing every frame to the same file;
  # whatever remains is the true last frame. Slower but never wrong.
  ffmpeg -nostdin -y -v error -i "$IN" -update 1 "$OUT" \
    || { echo "ERROR: could not extract last frame from $IN" >&2; exit 1; }
fi
[ -s "$OUT" ] || { echo "ERROR: produced no frame from $IN" >&2; exit 1; }

DIMS="$(ffprobe -v error -select_streams v -show_entries stream=width,height \
        -of csv=p=0:s=x "$OUT" 2>/dev/null || true)"
echo "last frame -> $OUT (${DIMS:-?})"
