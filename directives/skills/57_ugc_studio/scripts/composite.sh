#!/usr/bin/env bash
# =============================================================================
# composite.sh  --  the green-screen / app lane (UGC Studio)
# =============================================================================
#
# Moving UI is NEVER generated — it comes from the member's real screen
# recording, conformed and composited. This script is the whole lane: it
# samples a render's actual background color (THE GREEN GATE), keys or
# composites the talker over the real footage, and conforms every output to
# the one house format: 1080x1920 @ 30fps, yuv420p H.264, faststart.
#
# WHY each recipe is what it is (live-verified 2026-07-10):
#   * sample-green   Models drift from the prompted chroma green toward muted
#                    grass green. Widening key radii on a muted background
#                    deletes the PERSON before the green (verified), so the
#                    gate measures the real sampled color first and routes:
#                    saturated -> free local chromakey; muted -> matting/PiP.
#   * chromakey      UV key on the SAMPLED hex (never the assumed prompt
#                    color) at radius 0.10, plus despill and a border
#                    garbage matte — edge junk (vignettes, soft rolloff)
#                    lives in the outer ~1% of frame, so a crop-in mask
#                    kills it without touching the key.
#   * matting-key    The matting service returns subject-on-pure-black.
#                    Razor-tight black colorkey 0.05 blend 0.03 is the
#                    live-verified recipe — anything looser eats pupils.
#   * pip            The zero-risk default: a circular talker bubble over
#                    the full-frame footage. No keying, nothing to fail.
#   * fullframe      Screen recordings are scaled + padded, NEVER stretched
#                    — a stretched UI reads as fake instantly.
#   * still          Approved stills are punch-in overlay food; a subtle 3%
#                    Ken-Burns push-in hides the stillness for the ~1s the
#                    overlay is on screen.
#
# Talker patterns (chromakey / matting-key / pip) KEEP the talker's own
# audio — lip-sync integrity is untouchable — and MUTE the footage.
# fullframe and still are silent (they ride under the audio rail).
#
# USAGE
#   composite.sh sample-green  <gen.mp4>
#   composite.sh chromakey     <gen.mp4> <bg.mp4> <out.mp4> [0xRRGGBB] [radius]
#   composite.sh matting-key   <matted.mp4> <bg.mp4> <out.mp4>
#   composite.sh pip           <gen.mp4> <bg.mp4> <out.mp4>
#   composite.sh fullframe     <src.mov> <out.mp4>
#   composite.sh still         <img.png> <out.mp4> [seconds]
#
# DEPS    ffmpeg, ffprobe, python3
# EXIT    0 success · 2 missing dependency · 1 any other failure
# =============================================================================
set -euo pipefail

command -v ffmpeg  >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found"  >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found" >&2; exit 2; }

USAGE="Usage: $0 sample-green|chromakey|matting-key|pip|fullframe|still ...  (see header)"
[ "$#" -ge 1 ] || { echo "$USAGE" >&2; exit 1; }
SUB="$1"; shift

# ---- house conform: fit inside 1080x1920, pad (never stretch), 30fps -------
CONFORM="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=30"
ENC=(-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -movflags +faststart)
AUD=(-c:a aac -b:a 192k -ar 48000)

need_file() { [ -f "$1" ] || { echo "ERROR: input not found: $1" >&2; exit 1; }; }

# =============================================================================
# sample-green — THE GREEN GATE measurement
# Samples the four frame corners + both edges at mid-height (10x10 patches on
# a 108x192 downscale) at 1s intervals, clusters the samples, and reports the
# dominant background color. Corners can catch set furniture (desks, floors),
# which is exactly why we cluster instead of averaging everything.
# Threshold: measured muted-drift renders sit at sat 0.38-0.42; true chroma
# green survives encoding at sat >= ~0.9. SATURATED = sat >= 0.60 AND hue in
# the green band (70-170 deg).
# =============================================================================
if [ "$SUB" = "sample-green" ]; then
  [ "$#" -eq 1 ] || { echo "Usage: $0 sample-green <gen.mp4>" >&2; exit 1; }
  need_file "$1"
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  ffmpeg -nostdin -y -v error -i "$1" -vf "fps=1,scale=108:192" \
    -f rawvideo -pix_fmt rgb24 "$TMP/f.rgb" \
    || { echo "ERROR: frame extraction failed for $1" >&2; exit 1; }
  python3 - "$TMP/f.rgb" <<'PYEOF'
import sys
data = open(sys.argv[1], 'rb').read()
W, H, PS = 108, 192, 10
fsz = W * H * 3
n = len(data) // fsz
if n < 1:
    print("ERROR: no frames sampled", file=sys.stderr); sys.exit(1)
pts = [(2, 2), (W-PS-2, 2), (2, H-PS-2), (W-PS-2, H-PS-2),
       (2, H//2 - PS//2), (W-PS-2, H//2 - PS//2)]          # corners + mid edges
samples = []
for f in range(n):
    fr = data[f*fsz:(f+1)*fsz]
    for (x0, y0) in pts:
        rs = gs = bs = 0
        for y in range(y0, y0+PS):
            row = (y*W + x0) * 3
            for x in range(PS):
                i = row + x*3
                rs += fr[i]; gs += fr[i+1]; bs += fr[i+2]
        c = PS * PS
        samples.append((rs/c, gs/c, bs/c))
# cluster on 32-step quantized RGB; dominant = biggest cluster (kills the
# desk/floor corners that sneak into the sample set)
buckets = {}
for s in samples:
    buckets.setdefault(tuple(int(v)//32 for v in s), []).append(s)
best = max(buckets.values(), key=len)
r = sum(s[0] for s in best)/len(best)
g = sum(s[1] for s in best)/len(best)
b = sum(s[2] for s in best)/len(best)
mx, mn = max(r, g, b), min(r, g, b)
sat = (mx - mn)/mx if mx > 0 else 0.0
if mx == mn:
    hue = 0.0
elif mx == g:
    hue = 60*(b - r)/(mx - mn) + 120
elif mx == r:
    hue = (60*(g - b)/(mx - mn)) % 360
else:
    hue = 60*(r - g)/(mx - mn) + 240
hexc = "0x%02X%02X%02X" % (int(round(r)), int(round(g)), int(round(b)))
is_green = 70 <= hue <= 170
print("sampled %d patches across %d frames (corners + mid-height edges @ 1s)"
      % (len(samples), n))
print("dominant background: %s  (rgb %.0f,%.0f,%.0f  %d/%d samples)"
      % (hexc, r, g, b, len(best), len(samples)))
print("saturation %.2f   hue %.0f deg%s" % (sat, hue, "" if is_green
      else "  (WARNING: background is not green)"))
if sat >= 0.60 and is_green:
    print("VERDICT: SATURATED -> chromakey 0.10 fast path")
    print("VERDICT=SATURATED")
else:
    print("VERDICT: MUTED -> matting or PiP, do NOT widen radii")
    print("VERDICT=MUTED")
print("KEY_COLOR=%s" % hexc)
PYEOF
  exit 0
fi

# =============================================================================
# chromakey — talker keyed ON TOP of the full-frame footage
# UV chromakey on the sampled color, despill (keyed edges bleed green onto
# skin/hair), then a border garbage matte: crop 12px in and pad back with
# transparent so edge junk can never survive the key. Talker audio kept,
# footage muted.
# =============================================================================
if [ "$SUB" = "chromakey" ]; then
  [ "$#" -ge 3 ] && [ "$#" -le 5 ] || {
    echo "Usage: $0 chromakey <gen.mp4> <bg.mp4> <out.mp4> [0xRRGGBB] [radius]" >&2; exit 1; }
  GEN="$1"; BG="$2"; OUT="$3"; COLOR="${4:-0x00FF00}"; RADIUS="${5:-0.10}"
  need_file "$GEN"; need_file "$BG"
  echo "$COLOR" | grep -Eq '^0x[0-9A-Fa-f]{6}$' || {
    echo "ERROR: key color must be 0xRRGGBB (use the hex from sample-green), got: $COLOR" >&2; exit 1; }
  echo "$RADIUS" | grep -Eq '^0?\.[0-9]+$|^1(\.0+)?$' || {
    echo "ERROR: radius must be a number in (0,1], got: $RADIUS" >&2; exit 1; }
  M=12; CW=$((1080 - 2*M)); CH=$((1920 - 2*M))
  ffmpeg -nostdin -y -v error -i "$GEN" -i "$BG" -filter_complex \
    "[0:v]${CONFORM},chromakey=${COLOR}:${RADIUS}:0.05,despill=type=green,format=rgba,crop=${CW}:${CH}:${M}:${M},pad=1080:1920:${M}:${M}:color=black@0.0[fg];[1:v]${CONFORM}[bg];[bg][fg]overlay=0:0:shortest=1,format=yuv420p[v]" \
    -map "[v]" -map "0:a?" "${ENC[@]}" "${AUD[@]}" -shortest "$OUT" \
    || { echo "ERROR: chromakey composite failed ($GEN over $BG)" >&2; exit 1; }
  echo "wrote $OUT  (chromakey ${COLOR} radius ${RADIUS}, talker audio kept, bg muted)"
  exit 0
fi

# =============================================================================
# matting-key — matted subject-on-pure-black over the footage
# The matting service is the primary removal route for muted-green renders.
# Black colorkey 0.05 blend 0.03 exactly: pupils and dark hair are near-black,
# so any looser radius keys the eyes out of the face (live-verified).
# The conform pad is black too — it keys itself away for free. Talker audio
# kept when the matted file carries one (the service usually strips it).
# =============================================================================
if [ "$SUB" = "matting-key" ]; then
  [ "$#" -eq 3 ] || { echo "Usage: $0 matting-key <matted.mp4> <bg.mp4> <out.mp4>" >&2; exit 1; }
  MAT="$1"; BG="$2"; OUT="$3"
  need_file "$MAT"; need_file "$BG"
  ffmpeg -nostdin -y -v error -i "$MAT" -i "$BG" -filter_complex \
    "[0:v]${CONFORM},format=rgba,colorkey=0x000000:0.05:0.03[fg];[1:v]${CONFORM}[bg];[bg][fg]overlay=0:0:shortest=1,format=yuv420p[v]" \
    -map "[v]" -map "0:a?" "${ENC[@]}" "${AUD[@]}" -shortest "$OUT" \
    || { echo "ERROR: matting composite failed ($MAT over $BG)" >&2; exit 1; }
  echo "wrote $OUT  (black colorkey 0.05/0.03, talker audio kept if present, bg muted)"
  exit 0
fi

# =============================================================================
# pip — circular talker bubble over the full-frame footage
# The zero-risk default when the green gate says MUTED and matting is
# unavailable: nothing is keyed, so nothing can halo. ~30% width (324px),
# bottom-left with a 40px margin, square-cropped biased toward the face
# (chest-up talkers carry the face in the upper third). Talker audio kept.
# =============================================================================
if [ "$SUB" = "pip" ]; then
  [ "$#" -eq 3 ] || { echo "Usage: $0 pip <gen.mp4> <bg.mp4> <out.mp4>" >&2; exit 1; }
  GEN="$1"; BG="$2"; OUT="$3"
  need_file "$GEN"; need_file "$BG"
  D=324; MARGIN=40; PX=$MARGIN; PY=$((1920 - MARGIN - D))
  ffmpeg -nostdin -y -v error -i "$GEN" -i "$BG" -filter_complex \
    "[0:v]fps=30,crop='min(iw\,ih)':'min(iw\,ih)':'(iw-ow)/2':'(ih-oh)*0.30',scale=${D}:${D},format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*lte(pow(X-W/2,2)+pow(Y-H/2,2),pow(W/2-2,2))'[fg];[1:v]${CONFORM}[bg];[bg][fg]overlay=${PX}:${PY}:shortest=1,format=yuv420p[v]" \
    -map "[v]" -map "0:a?" "${ENC[@]}" "${AUD[@]}" -shortest "$OUT" \
    || { echo "ERROR: pip composite failed ($GEN over $BG)" >&2; exit 1; }
  echo "wrote $OUT  (${D}px circular bubble bottom-left, talker audio kept, bg muted)"
  exit 0
fi

# =============================================================================
# fullframe — conform a screen recording to the house format
# Scale + pad only. Stretching UI is the single fastest way to make real
# footage read as fake. Audio stripped: full-frame footage rides UNDER the
# voiceover on the audio rail, never alongside its own sound.
# =============================================================================
if [ "$SUB" = "fullframe" ]; then
  [ "$#" -eq 2 ] || { echo "Usage: $0 fullframe <src.mov> <out.mp4>" >&2; exit 1; }
  SRC="$1"; OUT="$2"
  need_file "$SRC"
  ffmpeg -nostdin -y -v error -i "$SRC" -vf "${CONFORM}" -an "${ENC[@]}" "$OUT" \
    || { echo "ERROR: fullframe conform failed for $SRC" >&2; exit 1; }
  echo "wrote $OUT  (1080x1920@30 scale+pad, audio stripped)"
  exit 0
fi

# =============================================================================
# still — a static still to a silent video clip with a 3% Ken-Burns push-in
# Stills are punch-in overlay food: on screen ~1s while the host clip's audio
# runs underneath. The subtle push-in hides the stillness for exactly that
# window. Zoompan runs on a 2x upscale — zooming at native res makes the pan
# quantize to whole pixels and visibly jitter.
# =============================================================================
if [ "$SUB" = "still" ]; then
  [ "$#" -ge 2 ] && [ "$#" -le 3 ] || {
    echo "Usage: $0 still <img.png> <out.mp4> [seconds]" >&2; exit 1; }
  IMG="$1"; OUT="$2"; SECS="${3:-2}"
  need_file "$IMG"
  echo "$SECS" | grep -Eq '^[0-9]+(\.[0-9]+)?$' || {
    echo "ERROR: seconds must be a positive number, got: $SECS" >&2; exit 1; }
  N="$(python3 -c 'import sys;n=int(round(float(sys.argv[1])*30));print(n)' "$SECS")"
  [ "$N" -ge 1 ] || { echo "ERROR: duration too short: $SECS s" >&2; exit 1; }
  DM1=$(( N > 1 ? N - 1 : 1 ))
  ffmpeg -nostdin -y -v error -loop 1 -framerate 30 -i "$IMG" -vf \
    "${CONFORM},scale=2160:3840:flags=lanczos,zoompan=z='1+0.03*on/${DM1}':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':d=${N}:s=1080x1920:fps=30,format=yuv420p" \
    -frames:v "$N" -an "${ENC[@]}" "$OUT" \
    || { echo "ERROR: still clip failed for $IMG" >&2; exit 1; }
  echo "wrote $OUT  (${SECS}s @30fps, 3% Ken-Burns push-in, silent)"
  exit 0
fi

echo "ERROR: unknown subcommand '$SUB'" >&2
echo "$USAGE" >&2
exit 1
