#!/usr/bin/env python3
"""
validate_prompt.py - pre-flight validator for ONE Talking-Object Ad Seedance 2.0 scene.

Runs before every scene render. It enforces the dialogue-first world model, the member's
REFERENCE LADDER, and the sub-10s ceiling so the pipeline never spends credits on a call
that breaks the rules.

THE LOCKED MODEL THIS ENFORCES (Talking-Object Ad — the cast carries the ad):
  - The WORLD is a cute Pixar-style 3D animated world; every character is the object
    itself with a face built into its own body. The prompt must carry the Pixar +
    3D-animated markers and must NOT request horror/uncanny/photoreal-human/clay/anime
    looks.
  - DIALOGUE IS NATIVE: a dialogue scene's prompt must contain the EXACT quoted line
    (matching the payload's `dialogue`), a voice casting, and the loose mouth-sync law.
    No external voiceover exists; no voice/audio file is ever attached.
  - THE REFERENCE LADDER (member hard rule):
      tier 1 (generic one-off speaker)  -> NO reference of any kind (type none, no images)
      tier 2 (real product in frame)    -> the approved casting/product still in images
      tier 3 (recurring speaker, wave 2)-> the speaker's own wave-1 clip as the VIDEO
                                           reference (voice_ref_source) — the ONE legal
                                           video reference in the plugin family
    A video reference in any other shape FAILS.
  - TEXT LAW: no on-screen text — except the CTA, whose offer may render as in-scene 3D
    text (on_screen_text non-empty ONLY on the CTA, and its text must be echoed in the
    prompt as a staged prop).
  - THE SCREEN LAW: a close, LEGIBLE screen renders only in a scene attaching the real
    screenshot/still; everywhere else screens are ambient out-of-focus glow.
  - Duration is an explicit integer 4..9 (UNDER 10), set by the call, NEVER written into
    the prompt text. Aspect 9:16, resolution 1080p.

Usage: validate_prompt.py payload.json     (exit 0 PASS, 1 FAIL)

payload.json:
  { "scene_id","role","speaker","wave":1,"tier":1,
    "prompt","negative_prompt","duration":6,"aspect_ratio":"9:16","resolution":"1080p",
    "reference":{"type":"none|image|video","source":"clips/scene_01.mp4"},
    "images":["inputs/casting-still.png", ...],
    "dialogue":"<the exact line>","voice":"<the locked casting>",
    "voice_ref_source":"clips/scene_01.mp4",
    "on_screen_text":"", "sfx_note":"..." }
"""

import argparse
import json
import re
import sys

DUR_MIN, DUR_MAX = 4, 9
PIXAR_MARKER = re.compile(r"\bpixar\b", re.I)
WORLD_MARKER = re.compile(r"(3d animated|3d render|animated render)", re.I)
FACE_MARKER = re.compile(r"(faces? built into|visible animated mouths?|visible mouths?)", re.I)
MOUTH_SYNC = re.compile(r"mouth[^.]{0,80}(sync|animat)", re.I)
EMOTION_LINE = re.compile(r"the emotion is the subject", re.I)
NO_HUMANS_LINE = re.compile(r"no real (people|humans?|person)", re.I)
NO_MUSIC_LINE = re.compile(r"no music", re.I)
NO_TEXT_TOKENS = re.compile(r"no (on-screen text|captions)", re.I)
DUR_IN_PROMPT = re.compile(r"\b\d+([.,]\d+)?[- ]*(seconds?|sec)\b", re.I)
DIALOGUE_VERB = re.compile(r"\b(says?|saying|speaks?|delivers)\b", re.I)
VOICE_WORD = re.compile(r"\bvoice\b", re.I)

BANNED_LOOK = [
    "claymation", "plasticine", "clay texture", "stop motion clay",
    "horror", "terrifying", "nightmare", "gore", "uncanny",
    "dead eyes", "photorealistic human", "photoreal human", "live action",
    "live-action", "real photograph",
    "2d illustration", "anime style", "flat cartoon",
]
BANNED_TEXT = [
    "caption reading", "subtitle", "subtitles", "burned-in caption",
    "text overlay", "caption overlay", "word-by-word caption",
]
FORBIDDEN_KEYS = ["voice_clip", "voice_reference", "voice_url",
                  "audio_url", "audio_clip", "voice_sample", "audio_file"]
REF_TYPES = {"image", "none", "video"}   # video is legal ONLY as a tier-3 voice ref
NARRATOR_IDS = {"narrator", "vo", "announcer"}
STILL_PAT = re.compile(r"(casting|product)-still|screenshot", re.I)

# THE SCREEN LAW: a close, LEGIBLE screen may only render in a scene that attaches the
# real screenshot. Negated phrasings ("never a readable close-up") are the COMPLIANT
# form and are scrubbed before matching.
LEGIBLE_SCREEN = re.compile(
    r"\b(legible|readable|reads|crisp)\b[^.]{0,80}\b(screen|laptop|monitor|phone|app|ui|"
    r"interface|display)\b|\b(screen|laptop|monitor|phone|app|ui|interface|display)\b"
    r"[^.]{0,80}\b(legible|readable|crisp)\b", re.I)


def _norm_tokens(text):
    return re.findall(r"[a-z0-9']+", str(text).lower())


def validate(p):
    fails, warns = [], []

    prompt = str(p.get("prompt") or "")
    neg = str(p.get("negative_prompt") or "")
    combined = prompt + "\n" + neg
    # The master negative belongs in the negative_prompt FIELD, never inside the prompt
    # text — but if a prompt embeds a "NEGATIVE PROMPT:" section anyway, scan only what
    # precedes it for banned looks / screen-law asks (the negative's own tokens are the
    # compliant form, not a request).
    prompt_body = re.split(r"negative\s+prompt\s*:", prompt, maxsplit=1,
                           flags=re.I)[0]
    low = prompt_body.lower()
    role = str(p.get("role") or "").lower()
    speaker = str(p.get("speaker") or "")
    is_narrator = speaker.lower() in NARRATOR_IDS
    wave = p.get("wave")
    tier = p.get("tier")

    if not prompt.strip():
        fails.append("FAIL [prompt]: empty prompt.")
    if not PIXAR_MARKER.search(prompt):
        fails.append("FAIL [pixar look]: prompt has no Pixar marker ('Cute Pixar style "
                     "ultra detailed 3D animated render').")
    if not WORLD_MARKER.search(prompt):
        fails.append("FAIL [world look]: prompt has no 3D-animated-render marker.")
    for bad in BANNED_LOOK:
        if bad in low:
            fails.append("FAIL [banned look]: prompt contains '%s'. The talking-object "
                         "format is cute, charming, premium 3D — never horror, never "
                         "photoreal humans, never clay or 2D." % bad)
    for bad in BANNED_TEXT:
        if bad in low:
            fails.append("FAIL [burned text]: prompt contains '%s'. This skill never "
                         "burns captions; the characters' dialogue carries every word. "
                         "The one legal text is the CTA's in-scene 3D offer text." % bad)
    if not NO_HUMANS_LINE.search(combined):
        fails.append("FAIL [no-humans line missing]: every prompt (or its negative) must "
                     "state the no-real-people law; real humans are banned.")
    if not EMOTION_LINE.search(prompt):
        fails.append("FAIL [emotion line missing]: every prompt must state 'The emotion "
                     "is the subject' with the scene's named feeling.")
    if not NO_MUSIC_LINE.search(prompt):
        fails.append("FAIL [audio line missing]: every prompt must carry the audio law "
                     "('Only the character's voice and ... No music, no narrator, no "
                     "other voices.' — adapt the narrator clause for a narrator scene).")
    if DUR_IN_PROMPT.search(prompt):
        fails.append("FAIL [duration in prompt]: the prompt names a duration in seconds. "
                     "Duration is set only by the call's duration field. (Timestamped "
                     "beats like [0.0-3.4s] are fine; 'a 4-second shot' is not.)")

    # THE DIALOGUE BLOCK (the format's core)
    dialogue = str(p.get("dialogue") or "").strip()
    if not dialogue:
        fails.append("FAIL [dialogue]: payload has no 'dialogue'. Every talking-object "
                     "scene is a spoken performance; the exact line is required.")
    else:
        d_toks = _norm_tokens(dialogue)
        p_toks = set(_norm_tokens(prompt))
        missing = [t for t in d_toks if t not in p_toks]
        if missing:
            fails.append("FAIL [dialogue in prompt]: the prompt does not contain the "
                         "exact line — missing word(s): %s. Quote the payload's "
                         "'dialogue' verbatim inside the DIALOGUE block."
                         % ", ".join(missing[:8]))
        if not DIALOGUE_VERB.search(prompt):
            fails.append("FAIL [dialogue block]: the prompt never SAYS anyone speaks "
                         "(no 'says/speaks' verb). Use: The <character> says, in <the "
                         "voice casting>: \"<the line>\".")
        if not str(p.get("voice") or "").strip():
            fails.append("FAIL [voice casting]: payload has no 'voice'. Every speaker's "
                         "voice casting (4-7 words) is locked in the script and named "
                         "in the prompt.")
        elif not VOICE_WORD.search(prompt):
            fails.append("FAIL [voice in prompt]: the prompt never names the VOICE. "
                         "The dialogue block must carry the locked voice casting.")
        if not is_narrator and not MOUTH_SYNC.search(prompt):
            fails.append("FAIL [mouth sync]: an on-camera speaker needs the loose "
                         "mouth-sync law in the prompt ('mouth animating naturally with "
                         "the words, loosely synced').")
        if not is_narrator and not FACE_MARKER.search(prompt):
            fails.append("FAIL [character law]: the prompt never gives the speaker a "
                         "face built into its own body / a visible animated mouth — the "
                         "app's talking-object character law.")

    # duration / aspect / resolution
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
                         "UNDER 10s. Trim or split the line." % int(d))

    if str(p.get("aspect_ratio") or "") != "9:16":
        fails.append("FAIL [aspect]: aspect_ratio must be '9:16' (got %r)."
                     % p.get("aspect_ratio"))
    if str(p.get("resolution") or "") != "1080p":
        fails.append("FAIL [resolution]: resolution must be '1080p' (got %r)."
                     % p.get("resolution"))

    # images list
    imgs = p.get("images") or []
    if not isinstance(imgs, list):
        fails.append("FAIL [images]: images must be a list of file paths.")
        imgs = []
    img_strs = [str(i.get("path") if isinstance(i, dict) else i or "") for i in imgs]

    # THE REFERENCE LADDER
    ref = p.get("reference") or {"type": "none"}
    voice_ref = str(p.get("voice_ref_source") or "").strip()
    if not isinstance(ref, dict):
        fails.append("FAIL [reference]: reference must be an object {type, source}.")
    else:
        rt = str(ref.get("type") or "none").lower()
        rsrc = str(ref.get("source") or "").strip()
        if rt not in REF_TYPES:
            fails.append("FAIL [reference.type]: '%s' not in image|none|video." % rt)
        if rt == "video":
            if wave != 2 or not voice_ref:
                fails.append("FAIL [ladder tier 3]: a VIDEO reference is legal ONLY for a "
                             "recurring speaker's later scene (wave 2) carrying its own "
                             "wave-1 clip as voice_ref_source — voice+face continuity "
                             "only. This payload is wave=%r, voice_ref_source=%r."
                             % (wave, voice_ref or None))
            elif rsrc != voice_ref:
                fails.append("FAIL [ladder tier 3]: reference.source (%s) must be the "
                             "voice_ref_source clip (%s) — the speaker's own first "
                             "scene." % (rsrc or "?", voice_ref))
            if not re.search(r"(brand-new (scene|location)|do not copy the reference|"
                             r"new environment)", low):
                fails.append("FAIL [ladder tier 3]: a voice-ref prompt must command a "
                             "brand-new environment ('...but this is a brand-new scene "
                             "in a brand-new location: do NOT copy the reference's "
                             "environment, framing, or camera').")
        if rt == "image" and not rsrc:
            fails.append("FAIL [reference.source]: type 'image' needs a source.")
        if wave == 2 and rt != "video":
            fails.append("FAIL [ladder tier 3]: a wave-2 scene (recurring speaker) MUST "
                         "carry its speaker's wave-1 clip as the video reference — only "
                         "the video carries the voice.")
        # NOTE: scenes.json's `tier` records the STILL tier (1 generic / 2 product).
        # Recurrence is what makes a scene ladder-tier-3: a wave-2 scene carries the
        # video voice reference REGARDLESS of its still tier (a recurring generic
        # speaker = wave 2 + tier 1 + video ref + no images; a recurring product
        # speaker = wave 2 + tier 2 + video ref + its approved still).
        if tier == 1:
            if img_strs:
                fails.append("FAIL [ladder tier 1]: a generic speaker has no stills — "
                             "images must be empty (only real products carry approved "
                             "casting/product stills).")
            if wave != 2 and rt != "none":
                fails.append("FAIL [ladder tier 1]: a generic speaker's first "
                             "appearance renders with NO reference of any kind (member "
                             "hard rule; a needless reference narrows the render). The "
                             "one exception is its wave-2 recurrence, which carries its "
                             "own wave-1 clip as the video voice reference.")

    # tier 2: real product in frame -> the approved still is required
    if (tier == 2 or role in ("product", "cta")) and not any(
            STILL_PAT.search(s) for s in img_strs):
        fails.append("FAIL [ladder tier 2]: this scene shows the real product but "
                     "attaches no approved casting/product still. A product never "
                     "renders from text — its label must come from the real photo.")

    # no voice/audio uploads anywhere
    for k in FORBIDDEN_KEYS:
        if k in p:
            fails.append("FAIL [no voice upload]: payload has '%s'. The voice is cast "
                         "by the prompt's description and generated natively; no "
                         "voice/audio file is ever attached." % k)

    # THE TEXT LAW + the CTA exception
    ost = str(p.get("on_screen_text") or "").strip()
    if ost and role != "cta":
        fails.append("FAIL [text law]: on_screen_text is %r on a non-CTA scene. The CTA "
                     "is the ONLY scene where in-scene text is legal." % ost)
    if role == "cta" and ost:
        o_toks = _norm_tokens(ost)
        p_toks = set(_norm_tokens(prompt))
        if any(t not in p_toks for t in o_toks):
            fails.append("FAIL [CTA text]: on_screen_text %r is not echoed in the prompt. "
                         "The offer must be STAGED as in-scene 3D text (a glowing prop "
                         "in the scene), not left to the field alone." % ost)
        if NO_TEXT_TOKENS.search(prompt) or "no on-screen text" in neg.lower():
            fails.append("FAIL [CTA text]: this CTA stages in-scene offer text but the "
                         "prompt/negative still bans on-screen text — use the "
                         "CTA-adjusted negative (drop the no-text clauses for this "
                         "scene only).")
    if role != "cta" and not NO_TEXT_TOKENS.search(combined):
        fails.append("FAIL [text law]: every non-CTA prompt (or its negative) must ban "
                     "on-screen text/captions.")

    # THE SCREEN LAW
    scrubbed = re.sub(r"\b(no|not|never a?n?|without)\s+(readable|legible|crisp)\b", "",
                      low)
    if LEGIBLE_SCREEN.search(scrubbed) and not any(STILL_PAT.search(s)
                                                   for s in img_strs):
        fails.append("FAIL [screen law]: the prompt asks for legible/readable screen "
                     "content but the scene attaches no real screenshot/still. Legible "
                     "screens only with the real reference; ambient glow everywhere "
                     "else.")

    if not neg.strip():
        warns.append("negative_prompt is empty — attach the master negative from "
                     "talking-object-style.md (CTA/screenshot adjustments per scene).")

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
        print("WARN: " + line if not line.startswith(("WARN", "negative")) else line)
    if fails:
        for line in fails:
            print(line)
        return 1
    print("PASS (%s)" % payload.get("scene_id", "scene"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
