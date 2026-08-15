#!/usr/bin/env python3
"""
validate_prompt.py - pre-flight validator for ONE Pixar Ad Seedance 2.0 scene.

Runs before every scene render. It enforces the Pixar world model and the sub-10s
ceiling so the pipeline never spends credits on a call that breaks the rules.

THE LOCKED MODEL THIS ENFORCES (Pixar Ad — the whole world is animated):
  - The WORLD and every character in it are Pixar-style 3D animated. The prompt must
    read as a Pixar scene (a pixar marker) inside a 3D animated render, and must NOT
    request horror/uncanny styling, photoreal humans/live action, clay/plasticine looks,
    or any other art style that breaks the format.
  - NO on-screen text, EVER. No captions, no day labels, no banner words, no legible UI.
    The only readable text in frame is the real product's own label. The payload's
    on_screen_text field must be empty, and the prompt must carry the no-text line.
  - NO dialogue, NO talking head, NO lip-sync inside a clip. The voice is the external
    ElevenLabs VO; the generator is never given a voice clip / voice reference.
  - NO real humans, EVER (member hard rule). Every character is a Pixar-style 3D
    animated character; witnesses may take the desaturated "elsewhere people" treatment.
    The prompt must carry a no-real-people line.
  - Duration is an explicit integer 4..9 (UNDER 10), set by the call, NEVER written into
    the prompt text. Aspect 9:16, resolution 1080p.
  - Reference is image|none — a VIDEO reference is BANNED (member hard rule: a video ref
    drags its scene/composition onto the new shot). The hook uses the approved hook still
    as its start image; every other character-visible scene attaches the hook still in
    `images` as its identity reference. Product scenes (the CTA always) also attach the
    approved product still; the product is never re-stylized and never renders from text.
  - THE SCREEN LAW (member hard rule): a close, LEGIBLE screen renders ONLY in a scene
    that attaches the real screenshot (the product still). A prompt asking for legible/
    readable screen content without a product still in `images` FAILS; everywhere else
    screens are ambient out-of-focus glow, never a readable close-up.

Usage: validate_prompt.py payload.json     (exit 0 PASS, 1 FAIL)

payload.json:
  { "scene_id","role","prompt","negative_prompt","duration":6,
    "aspect_ratio":"9:16","resolution":"1080p",
    "reference":{"type":"image|none","source":"inputs/hook-still.png"},
    "images":["inputs/hook-still.png", "inputs/product-still.png", ...],
    "on_screen_text":"", "sfx":true }
"""

import argparse
import json
import re
import sys

DUR_MIN, DUR_MAX = 4, 9
PIXAR_MARKER = re.compile(r"\bpixar\b", re.I)
WORLD_MARKER = re.compile(r"(3d animated|3d render|animated render)", re.I)
NO_TEXT_LINE = re.compile(r"no on-screen text", re.I)
NO_HUMANS_LINE = re.compile(r"no real (people|humans?|person)", re.I)
DUR_IN_PROMPT = re.compile(r"\b\d+\s*(seconds?|sec)\b", re.I)

BANNED_LOOK = [
    "claymation", "plasticine", "clay texture", "stop motion clay",
    "horror", "terrifying", "creepy", "nightmare", "gore", "uncanny",
    "dead eyes", "photorealistic human", "photoreal human", "live action",
    "live-action", "real photograph",
    "2d illustration", "anime style", "flat cartoon",
]
BANNED_TALK = [
    "talking head", "talking to camera", "speaking to camera",
    "speaking to the camera", "lip sync", "lip-sync", "lipsync", "voiceover",
]
BANNED_TEXT = [
    "caption reading", "text reading", "banner reading", "sign reading",
    "words on screen", "subtitle", "on-screen caption", "text overlay",
]
FORBIDDEN_KEYS = ["voice_clip", "voice", "voice_reference", "voice_url",
                  "audio_url", "audio_clip", "voice_sample"]
REF_TYPES = {"image", "none"}   # "video" is BANNED (member hard rule)

# THE SCREEN LAW (member hard rule): a close, LEGIBLE screen may only render in a scene
# that attaches the real screenshot (the product still). A prompt that asks for legible/
# readable screen content without that reference invents a fake UI — the #1 AI tell.
LEGIBLE_SCREEN = re.compile(
    r"\b(legible|readable|reads|crisp)\b[^.]{0,80}\b(screen|laptop|monitor|phone|app|ui|"
    r"interface|display)\b|\b(screen|laptop|monitor|phone|app|ui|interface|display)\b"
    r"[^.]{0,80}\b(legible|readable|crisp)\b", re.I)


def validate(p):
    fails, warns = [], []

    prompt = str(p.get("prompt") or "")
    neg = str(p.get("negative_prompt") or "")
    low = prompt.lower()

    if not prompt.strip():
        fails.append("FAIL [prompt]: empty prompt.")
    if not PIXAR_MARKER.search(prompt):
        fails.append("FAIL [pixar look]: prompt has no Pixar marker. It must read as a "
                     "Pixar scene ('Cute Pixar style ultra detailed 3D animated render').")
    if not WORLD_MARKER.search(prompt):
        fails.append("FAIL [world look]: prompt has no 3D-animated-render marker. The "
                     "whole world is a Pixar-style 3D animated render ('Cute Pixar style "
                     "ultra detailed 3D animated render').")
    for bad in BANNED_LOOK:
        if bad in low:
            fails.append("FAIL [banned look]: prompt contains '%s'. The Pixar format is "
                         "a premium cinematic 3D render — never horror, never clay, never "
                         "flat 2D." % bad)
    for bad in BANNED_TALK:
        if bad in low:
            fails.append("FAIL [no dialogue/lip-sync]: prompt contains '%s'. No character "
                         "talks on camera; voice is the external ElevenLabs VO." % bad)
    for bad in BANNED_TEXT:
        if bad in low:
            fails.append("FAIL [no on-screen text]: prompt contains '%s'. No generation "
                         "ever contains text; the VO carries the milestones and the offer. "
                         "Only the real product's own label may be legible." % bad)
    if not NO_TEXT_LINE.search(prompt):
        fails.append("FAIL [no-text line missing]: every prompt must state 'No on-screen "
                     "text' (the text law is absolute in this skill).")
    if not NO_HUMANS_LINE.search(prompt):
        fails.append("FAIL [no-humans line missing]: every prompt must state the no-real-"
                     "people law (e.g. 'No real people anywhere in frame — every character "
                     "is a Pixar-style 3D animated character'); real humans are banned in "
                     "Pixar ads.")
    if DUR_IN_PROMPT.search(prompt):
        fails.append("FAIL [duration in prompt]: the prompt names a duration in seconds. "
                     "Duration is set only by the call's duration field, never in text.")
    if not neg.strip():
        warns.append("negative_prompt is empty — optional; relying on the prompt itself "
                     "(some members skip it).")

    # duration: integer 4..9
    dur = p.get("duration")
    if dur is None:
        fails.append("FAIL [duration]: missing. Use an explicit integer 4..9.")
    else:
        try:
            d = float(dur)
        except (TypeError, ValueError):
            d = None
        if d is None:
            fails.append("FAIL [duration]: %r is not a number." % (dur,))
        elif d != int(d):
            fails.append("FAIL [duration]: %g is not an integer (4..9)." % d)
        elif not (DUR_MIN <= int(d) <= DUR_MAX):
            fails.append("FAIL [duration 4..9]: %d is outside 4..9; every generation is "
                         "UNDER 10s. Split the scene." % int(d))

    if str(p.get("aspect_ratio") or "") != "9:16":
        fails.append("FAIL [aspect]: aspect_ratio must be '9:16' (got %r)."
                     % p.get("aspect_ratio"))
    if str(p.get("resolution") or "") != "1080p":
        fails.append("FAIL [resolution]: resolution must be '1080p' (got %r)."
                     % p.get("resolution"))

    # reference shape — image (the hook's start image) or none; VIDEO IS BANNED
    ref = p.get("reference") or {"type": "none"}
    if not isinstance(ref, dict):
        fails.append("FAIL [reference]: reference must be an object {type, source}.")
    else:
        rt = str(ref.get("type") or "none").lower()
        if rt == "video":
            fails.append("FAIL [reference.type]: video references are BANNED (member hard "
                         "rule) — a video ref drags its scene and composition onto the new "
                         "shot. Use the hook still: the hook scene takes it as its start "
                         "image (type 'image'); every other scene lists it in 'images' as "
                         "the identity reference with reference type 'none'.")
        elif rt not in REF_TYPES:
            fails.append("FAIL [reference.type]: '%s' not in image|none." % rt)
        if rt == "image" and not str(ref.get("source") or "").strip():
            fails.append("FAIL [reference.source]: type 'image' needs a source (the "
                         "approved inputs/hook-still.png).")

    # no uploaded voice anywhere
    for k in FORBIDDEN_KEYS:
        if k in p:
            fails.append("FAIL [no voice upload]: payload has '%s'. The Pixar model "
                         "never uploads a voice clip; the voice is the external VO." % k)

    # the text law: the field itself must be empty in this skill
    ost = str(p.get("on_screen_text") or "").strip()
    if ost:
        fails.append("FAIL [no on-screen text]: on_screen_text is %r. This skill never "
                     "renders or overlays text — the VO carries the milestones and the "
                     "offer. Empty the field." % ost)

    # product grounding: the CTA (and any product scene) must attach the product still,
    # generated from the real photo; the product never renders from text description.
    imgs = p.get("images") or []
    if not isinstance(imgs, list):
        fails.append("FAIL [images]: images must be a list of file paths.")
        imgs = []
    img_strs = [str(i.get("path") if isinstance(i, dict) else i or "") for i in imgs]
    role = str(p.get("role") or "").lower()
    if role == "cta" and not any("product-still" in s for s in img_strs):
        fails.append("FAIL [product grounding]: the CTA scene must attach the approved "
                     "product still (inputs/product-still.png) in images; the product "
                     "never renders from text and is never re-stylized.")
    if role != "hook" and not any("hook-still" in s for s in img_strs):
        warns.append("WARN [identity anchor]: non-hook scene has no hook still in images. "
                     "Every character-visible scene must attach inputs/hook-still.png as "
                     "its identity reference; only a character-free shot (e.g. a pure "
                     "product macro) may skip it.")

    # THE SCREEN LAW (member hard rule): a prompt that asks for legible/readable screen
    # content must attach the real screenshot (the product still) — otherwise the model
    # invents a fake UI. Negated phrasings ("no readable text", "never a readable
    # close-up") are the COMPLIANT form and are scrubbed before matching.
    scrubbed = re.sub(r"\b(no|not|never a?n?|without)\s+(readable|legible|crisp)\b", "",
                      low)
    if LEGIBLE_SCREEN.search(scrubbed) and not any("product-still" in s
                                                   for s in img_strs):
        fails.append("FAIL [screen law]: the prompt asks for legible/readable screen "
                     "content but the scene attaches no product still. A close, legible "
                     "screen may only render in a scene that attaches the real screenshot "
                     "(inputs/product-still.png); everywhere else screens are ambient "
                     "out-of-focus glow, never a readable close-up.")

    if "sfx" not in p:
        warns.append("WARN: 'sfx' flag missing; defaulting to no SFX for this scene.")

    return fails, warns


def main(argv=None):
    ap = argparse.ArgumentParser(prog="validate_prompt.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload")
    args = ap.parse_args(argv)

    try:
        with open(args.payload, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except FileNotFoundError:
        print("FAIL [payload file]: %s not found." % args.payload)
        return 1
    except json.JSONDecodeError as exc:
        print("FAIL [payload file]: %s is not valid JSON (%s)." % (args.payload, exc))
        return 1
    if not isinstance(payload, dict):
        print("FAIL [payload file]: top-level JSON must be an object.")
        return 1

    fails, warns = validate(payload)
    for line in warns:
        print(line)
    if fails:
        for line in fails:
            print(line)
        return 1
    print("PASS (%s)" % payload.get("scene_id", "scene"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
