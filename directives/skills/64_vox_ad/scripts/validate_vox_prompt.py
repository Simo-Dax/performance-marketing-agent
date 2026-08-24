#!/usr/bin/env python3
"""Validate a VOX keyframe or clip payload against the format's laws.

Usage: validate_vox_prompt.py <payload.json> [transcript.json]

Keyframe payload: {"kind":"image","clip_id":"clip_01","prompt":"...","hero":false,
                   "anchors":["inputs/product.png"],"aspect_ratio":"9:16","resolution":"2k"}
Clip payload:     {"kind":"video","clip_id":"clip_01","prompt":"...","duration":5,
                   "aspect_ratio":"9:16","resolution":"1080p",
                   "reference":{"type":"image","source":"keyframes/clip_01.png"},
                   "has_people":false}

Checks (non-zero exit + message list on failure):
- image: the collage style block present; a palette hex present; "NOT CGI"; matte/no-glow
  unless hero; the text law close ("ONLY text" clause or NO TEXT AT ALL); every ALL-CAPS
  quoted banner phrase appears in the transcript (spoken-words law; single quoted words
  on props are allowed as markings when numeric); 9:16 + 2k.
- video: empty-start line; final-frame law; camera static; nothing-moves law; no-music
  line; people guard when has_people; duration integer 4..9; 1080p; 9:16; reference is an
  image (never video, never absent).
"""
import json, re, sys, unicodedata

STYLE_MARK = "PAPER COLLAGE"

def words_of(text):
    # NFKD-fold accents so a "GRUNS" banner matches a spoken "gr\u00fcns" and vice versa.
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return set(re.sub(r"[^a-z0-9 ]", " ", text.lower()).split())

def main():
    if len(sys.argv) not in (2, 3):
        print("usage: validate_vox_prompt.py <payload.json> [transcript.json]", file=sys.stderr)
        sys.exit(2)
    p = json.load(open(sys.argv[1]))
    transcript_words = set()
    if len(sys.argv) == 3:
        t = json.load(open(sys.argv[2]))
        transcript_words = words_of(" ".join(l["vo"] for l in t["lines"]))
    prompt = p.get("prompt", "")
    kind = p.get("kind")
    errs = []

    if kind == "image":
        if STYLE_MARK not in prompt:
            errs.append("style block missing (PAPER COLLAGE marker)")
        if not re.search(r"#[0-9A-Fa-f]{6}", prompt):
            errs.append("no palette hex in prompt")
        if "NOT CGI" not in prompt:
            errs.append("missing NOT CGI guard")
        if not p.get("hero") and "no glow" not in prompt:
            errs.append("non-hero frame missing the no-glow law")
        low = prompt.lower()
        if "only text" not in low and "no text at all" not in low:
            errs.append("missing the text-law close (ONLY text / NO TEXT AT ALL)")
        if p.get("aspect_ratio") != "9:16":
            errs.append("aspect_ratio must be 9:16")
        if str(p.get("resolution", "")).lower() != "2k":
            errs.append("keyframes render at 2k")
        if transcript_words:
            for m in re.findall(r"\"([A-Z0-9][A-Z0-9 .!'+-]{1,40})\"", prompt):
                caps = [w for w in words_of(m) if w and not w.isdigit()]
                if caps and not set(caps) <= transcript_words:
                    missing = set(caps) - transcript_words
                    errs.append(f'banner "{m}" contains unspoken words: {sorted(missing)} (spoken-words law)')
    elif kind == "video":
        checks = [
            ("START on the empty", "missing the empty-start line"),
            ("FINAL FRAME must match the reference", "missing the final-frame law"),
            ("static, locked off", "camera must be static, locked off"),
            ("Nothing moves position after it lands", "missing the nothing-moves law"),
            ("No music", "missing the no-music line"),
        ]
        for needle, msg in checks:
            if needle not in prompt:
                errs.append(msg)
        if p.get("has_people") and "flat printed cutouts" not in prompt:
            errs.append("people in frame but the flat-printed-cutouts guard is missing")
        d = p.get("duration")
        if not isinstance(d, int) or not (4 <= d <= 9):
            errs.append("duration must be an integer 4..9")
        if p.get("resolution") != "1080p":
            errs.append("resolution must be 1080p")
        if p.get("aspect_ratio") != "9:16":
            errs.append("aspect_ratio must be 9:16")
        ref = p.get("reference") or {}
        if ref.get("type") != "image" or not ref.get("source"):
            errs.append("reference must be an image (the clip's keyframe); video references are banned")
    else:
        errs.append("kind must be image or video")

    if errs:
        for e in errs:
            print(f"FAIL {p.get('clip_id','?')}: {e}")
        sys.exit(1)
    print(f"OK {p.get('clip_id','?')} ({kind})")

if __name__ == "__main__":
    main()
