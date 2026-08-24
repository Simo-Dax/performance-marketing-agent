#!/usr/bin/env python3
"""Shared caption engine — the house subtitle style.

User-locked rules (spec: `the agent/_meta/caption-style.md`):
  - MOSTLY 2-3 words per card; 1 or 4 allowed only when it genuinely reads better
  - ALWAYS one row. Never wraps. Enforced on rendered pixel width, not characters.
  - split on real speech pauses and punctuation; never end a card on a word that
    binds to the next one
  - no dots and no commas anywhere
  - only the very first word of the whole video is capitalised
  - proper nouns keep their capitals; multi-word names never split across cards
  - white text, soft blurred drop shadow, NO hard outline
  - 58px, baseline y=1275 at 1080x1920, scaled proportionally for other sizes

Splitting is a dynamic-programming search that minimises
    (cards outside 2-3) + (cards ending on a binding word)
subject to a hard one-row width limit.

This machine's ffmpeg has no drawtext/libass, so cards render as transparent PNGs
and composite with overlay+enable.
"""
import pathlib, re, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# The locked face is Avenir Next Heavy (the Montserrat stand-in, see
# caption-style.md). It is tried FIRST and never silently replaced: FONT_NAME
# below reports what actually loaded so a run can say so out loud.
#
# The ladder exists because this ships inside a cross-platform agent. Loading a
# single macOS path at import time made `import caption_lib` a hard crash on
# every Windows and Linux machine, before any argument was even parsed.
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
FONT_INDEX = 8                      # Heavy
FONT_FALLBACKS = [
    # (path, index) in descending order of fidelity to the locked look
    ("/System/Library/Fonts/Avenir Next.ttc", 8),          # macOS, the locked face
    ("/Library/Fonts/Montserrat-Bold.ttf", 0),             # if the user installs it
    ("C:\\Windows\\Fonts\\montserrat-bold.ttf", 0),
    ("C:\\Windows\\Fonts\\arialbd.ttf", 0),               # Windows Arial Bold
    ("C:\\Windows\\Fonts\\ariblk.ttf", 0),                # Windows Arial Black
    ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
    ("/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf", 0),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 0),
]
FONT_NAME = ""                      # filled by _resolve_font(), reported in the audit


def _resolve_font():
    """Return (path, index) for the best available face, locked font first.

    Never raises. A machine with none of these still renders through Pillow's
    default face, which looks wrong but keeps the pipeline alive and says so.
    """
    import os as _os
    candidates = [(FONT_PATH, FONT_INDEX)] + FONT_FALLBACKS
    for path, index in candidates:
        if not path or not _os.path.exists(path):
            continue
        try:
            ImageFont.truetype(path, 24, index=index)
            return path, index
        except Exception:
            continue
    return None, 0
REF_W, REF_H = 1080, 1920
REF_FONT_SIZE = 58
REF_BASELINE_Y = 1275
REF_STROKE = 2
REF_SHADOW_OFFSET = (0, 5)
REF_SHADOW_BLUR = 7
SHADOW_ALPHA = 170
MAX_LINE_FRAC = 0.88                # one row must fit inside this share of frame width

MIN_WORDS, MAX_WORDS = 1, 4
TARGET_WORDS = (2, 3)
COST_OFF_TARGET = 1.0               # penalty for a 1- or 4-word card
COST_BINDING = 2.0                  # penalty for ending a card on a binding word
PAUSE_SPLIT = 0.20
MAX_HOLD = 0.60

# Generic proper nouns only. The BRAND's own names are never hardcoded here --
# this agent is brand-agnostic. Load them per campaign with load_brand_vocab().
ATOMIC = [
    (["claude", "code"], "Claude Code", False),
]
PROPER = [
    (r"\bai\b", "AI"),
    (r"\bclaude code\b", "Claude Code"), (r"\bclaude\b", "Claude"),
    (r"\broas\b", "ROAS"), (r"\bchatgpt\b", "ChatGPT"),
    (r"\bcanva\b", "Canva"), (r"\bikea\b", "IKEA"), (r"\bmeta\b", "Meta"),
    (r"\bbrand dna\b", "Brand DNA"), (r"\bdna\b", "DNA"),
]
FIXES = [
    (["row", "ass"], ["ROAS"]), (["rowass"], ["ROAS"]),
    (["cloud", "code"], ["Claude", "Code"]), (["minds", "what"], ["mines", "what"]),
    (["metaflagged"], ["Meta flagged"]), (["chat", "gpt"], ["ChatGPT"]),
]


def load_brand_vocab(path):
    """Teach the captioner this campaign's own names, so they render with the right
    capitals and never get split across two cards.

    JSON shape (every key optional):
      {
        "brand_names":  ["Acme Coffee Co"],           # atomic, never split, marked brand
        "proper_nouns": ["Nespresso", "Arabica"],     # capitals preserved
        "fixes":        {"acme coffee": "Acme Coffee"} # whisper mishears -> truth
      }

    Returns the number of entries loaded. Missing file is not an error: brand vocab
    is optional and the generic list still applies.
    """
    import json, os, re as _re
    if not path or not os.path.isfile(path):
        return 0
    data = json.loads(open(path, encoding="utf-8").read())
    n = 0
    for name in data.get("brand_names", []):
        parts = [bare(w) for w in str(name).split() if bare(w)]
        if not parts:
            continue
        ATOMIC.insert(0, (parts, str(name), True))
        PROPER.insert(0, (r"\b" + _re.escape(str(name).lower()) + r"\b", str(name)))
        n += 1
    for word in data.get("proper_nouns", []):
        w = str(word)
        PROPER.insert(0, (r"\b" + _re.escape(w.lower()) + r"\b", w))
        n += 1
    for heard, truth in (data.get("fixes") or {}).items():
        h = [bare(x) for x in str(heard).split() if bare(x)]
        t = str(truth).split()
        if h and t:
            FIXES.insert(0, (h, t))
            n += 1
    return n
BIND = {"a", "an", "the", "to", "of", "in", "on", "for", "than", "and", "but", "that",
        "his", "her", "my", "your", "its", "our", "their", "with", "at", "from", "as",
        "is", "was", "so", "he", "she", "they", "we", "you", "it", "more", "just",
        "inside", "into", "or", "if", "when", "up", "out", "by", "about"}

_FONT_PATH, _FONT_INDEX = _resolve_font()
FONT_NAME = _FONT_PATH or "PIL default (no bold face found on this machine)"
if _FONT_PATH:
    _MFONT = ImageFont.truetype(_FONT_PATH, REF_FONT_SIZE, index=_FONT_INDEX)
else:
    _MFONT = ImageFont.load_default()
_MDRAW = ImageDraw.Draw(Image.new("RGB", (8, 8)))
MAX_LINE_PX = REF_W * MAX_LINE_FRAC


def bare(s):
    return "".join(ch for ch in str(s).lower() if ch.isalpha())


def styled(text, first=False):
    """Exactly the text that gets drawn: no punctuation, lowercase, proper nouns kept."""
    t = text.lower()
    t = re.sub(r"\ba\.m\.", "am", t)
    t = re.sub(r"\bp\.m\.", "pm", t)
    t = " ".join(re.sub(r"[.,!?;:]", " ", t).split())
    for pat, rep in PROPER:
        t = re.sub(pat, rep, t)
    if first:
        for k, ch in enumerate(t):
            if ch.isalpha():
                return t[:k] + ch.upper() + t[k + 1:]
    return t


def line_px(text):
    b = _MDRAW.textbbox((0, 0), text, font=_MFONT, stroke_width=REF_STROKE)
    return b[2] - b[0]


def fits_one_row(text):
    return line_px(styled(text)) <= MAX_LINE_PX


def apply_fixes(words):
    out, i = [], 0
    while i < len(words):
        hit = None
        for pat, rep in FIXES:
            n = len(pat)
            if i + n <= len(words) and [bare(w["word"]) for w in words[i:i + n]] == pat:
                hit = (n, rep); break
        if not hit:
            out.append(words[i]); i += 1; continue
        n, rep = hit
        span = words[i:i + n]
        tail = str(span[-1]["word"]).strip()[-1:]
        tail = tail if tail in ",.!?;:" else ""
        if len(rep) == n:
            for w, r in zip(span, rep):
                nw = dict(w); nw["word"] = r
                out.append(nw)
            if tail:
                out[-1]["word"] += tail
        else:
            out.append({"word": rep[0] + tail, "start": float(span[0]["start"]),
                        "end": float(span[-1]["end"])})
        i += n
    return out


def _split_segment(seg):
    """Min-cost partition of one phrase into 1-4 word cards that each fit one row."""
    n = len(seg)
    INF = float("inf")
    best = [INF] * (n + 1); best[0] = 0.0
    back = [0] * (n + 1)
    for end in range(1, n + 1):
        for size in range(MIN_WORDS, MAX_WORDS + 1):
            start = end - size
            if start < 0 or best[start] == INF:
                continue
            text = " ".join(str(w["word"]) for w in seg[start:end])
            if size > 1 and not fits_one_row(text):
                continue                          # would wrap onto a second row
            c = 0.0 if size in TARGET_WORDS else COST_OFF_TARGET
            if end < n and bare(seg[end - 1]["word"]) in BIND:
                c += COST_BINDING
            if best[start] + c < best[end]:
                best[end] = best[start] + c
                back[end] = size
    if best[n] == INF:
        return [1] * n
    sizes, e = [], n
    while e > 0:
        sizes.append(back[e]); e -= back[e]
    return list(reversed(sizes))


def build_chunks(words):
    words = apply_fixes(words)

    toks, i = [], 0
    while i < len(words):
        hit = None
        for pat, disp, own in ATOMIC:
            n = len(pat)
            if i + n <= len(words) and [bare(w["word"]) for w in words[i:i + n]] == pat:
                hit = (n, disp, own); break
        if hit:
            n, disp, own = hit
            toks.append({"word": disp, "start": float(words[i]["start"]),
                         "end": float(words[i + n - 1]["end"]), "brand": own,
                         "tail": str(words[i + n - 1]["word"]).strip()[-1:]})
            i += n
        elif (bare(words[i]["word"]) == "would" and i + 1 < len(words)
              and bare(words[i + 1]["word"]) == "have"):
            toks.append({"word": "would've", "start": float(words[i]["start"]),
                         "end": float(words[i + 1]["end"]), "brand": False,
                         "tail": str(words[i + 1]["word"]).strip()[-1:]})
            i += 2
        else:
            w = dict(words[i]); w["brand"] = False
            w["tail"] = str(w["word"]).strip()[-1:]
            toks.append(w); i += 1

    segs, cur = [], []
    for t in toks:
        gap = float(t["start"]) - float(cur[-1]["end"]) if cur else 0.0
        if cur and (gap >= PAUSE_SPLIT or t["brand"]):
            segs.append(cur); cur = []
        cur.append(t)
        if t["brand"] or t["tail"] in (",", ".", "!", "?", ":", ";"):
            segs.append(cur); cur = []
    if cur:
        segs.append(cur)

    chunks = []
    for seg in segs:
        idx = 0
        for sz in _split_segment(seg):
            part = seg[idx:idx + sz]; idx += sz
            if part:
                chunks.append({"text": " ".join(str(x["word"]) for x in part).strip(),
                               "start": float(part[0]["start"]), "end": float(part[-1]["end"])})

    for k, c in enumerate(chunks):
        c["text"] = styled(c["text"], k == 0)
    chunks = [c for c in chunks if c["text"]]

    for k, c in enumerate(chunks):
        nxt = chunks[k + 1]["start"] if k + 1 < len(chunks) else c["end"] + MAX_HOLD
        c["end"] = min(nxt - 0.02, c["end"] + MAX_HOLD)
        if c["end"] <= c["start"]:
            c["end"] = c["start"] + 0.25
    return chunks


def render_cards(chunks, outdir, vw, vh):
    """One transparent PNG per card. Single row, always."""
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    sc = vh / REF_H
    size = max(12, round(REF_FONT_SIZE * sc))
    stroke = max(1, round(REF_STROKE * sc))
    baseline = round(REF_BASELINE_Y * sc)
    off = (round(REF_SHADOW_OFFSET[0] * sc), round(REF_SHADOW_OFFSET[1] * sc))
    blur = max(1, REF_SHADOW_BLUR * sc)
    font = (ImageFont.truetype(_FONT_PATH, size, index=_FONT_INDEX)
            if _FONT_PATH else ImageFont.load_default())

    for i, c in enumerate(chunks):
        txt = c["text"]                                   # never wrapped
        img = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        b = d.textbbox((0, 0), txt, font=font, stroke_width=stroke)
        x = (vw - (b[2] - b[0])) // 2 - b[0]
        y = baseline - (b[3] - b[1]) // 2

        shadow = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).text((x + off[0], y + off[1]), txt, font=font,
                                    fill=(0, 0, 0, SHADOW_ALPHA), stroke_width=stroke,
                                    stroke_fill=(0, 0, 0, SHADOW_ALPHA))
        img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(blur)))
        ImageDraw.Draw(img).text((x, y), txt, font=font, fill=(255, 255, 255, 255),
                                 stroke_width=stroke, stroke_fill=(0, 0, 0, 190))
        img.save(outdir / ("cap_%03d.png" % i))
    return outdir


def composite(src, chunks, carddir, dst):
    carddir = pathlib.Path(carddir)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src)]
    for i in range(len(chunks)):
        cmd += ["-i", str(carddir / ("cap_%03d.png" % i))]
    parts, cur = [], "0:v"
    for i, c in enumerate(chunks):
        nxt = "v%d" % i
        parts.append("[%s][%d:v]overlay=0:0:enable='between(t,%.3f,%.3f)'[%s]"
                     % (cur, i + 1, c["start"], c["end"], nxt))
        cur = nxt
    cmd += ["-filter_complex", ";".join(parts), "-map", "[%s]" % cur, "-map", "0:a?",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", str(dst)]
    return subprocess.run(cmd).returncode
