#!/usr/bin/env python3
"""
validate_payload.py  --  pre-flight validator for ONE Seedance 2.0 generation.

Runs right before every generation: every hook reel, every body shot, every
product-only b-roll. It asserts the LOCKED model and the sub-10s ceiling BEFORE a
generation is dispatched, so the pipeline never spends credits on a call that
violates the model.

THE LOCKED MODEL THIS ENFORCES (Seedance 2.0):
  - Inputs uploaded once, re-sent every time: ONE face, ONE body, ONE product
    image, ONE voice clip (<=15s, attached as the voice reference on EVERY
    generation including b-roll voiceover).
  - CHARACTER generations (hooks, body) carry face + body (+ product when the
    product is on screen) + voice. Identity = the re-sent face + body bytes.
  - PRODUCT-ONLY b-rolls carry the PRODUCT IMAGE + VOICE ONLY. No face, no body.
    Set "product_only": true on those payloads; the face/body requirement is then
    intentionally skipped.
  - EVERY generation is an integer 4..9 seconds (UNDER 10). Never auto, never 10+.
  - Pace is fast and punchy (~3.5 wps). If a payload includes "pace_wps" it must land
    in [2.4, 4.0].
  - Audio is expected on every generation; a dialogue payload must attach the voice
    clip. No clone step, no TTS, no spine, no force-muting, no video inputs.

Usage:
    python validate_payload.py payload.json

payload.json shape (missing keys get safe defaults):
    {
      "product_only": false,           # true for product-only b-rolls (no character)
      "images": [ {"path":"face.png","role":"face"},
                  {"path":"body.png","role":"body"},
                  {"path":"prod.png","role":"product"} ],
      "product_on_screen": true,
      "voice_clip_seconds": 14,
      "duration": 6,                   # integer 4..9
      "pace_wps": 3.4,                # optional; if present must be 2.4..4.0
      "has_dialogue": true
    }

Exit 0 on PASS, 1 on any FAIL. Stdlib only.
"""

import argparse
import json
import sys

MIN_CHARACTER_IMAGES = 2     # a face AND a body, on character generations
DURATION_MIN = 4
DURATION_MAX = 9             # UNDER 10 seconds, hard rule for this factory
VOICE_CLIP_MAX_SECONDS = 15
MAX_TOTAL_FILES = 12
PACE_MIN = 2.4               # below this it drags
PACE_MAX = 4.0               # above this it rushes (house pace is ~3.5 wps)

FACE_ROLES = {"face", "face_image", "headshot", "portrait"}
BODY_ROLES = {"body", "body_image", "fullbody", "full_body"}
PRODUCT_ROLES = {"product", "product_image", "pack", "packshot", "pouch"}


def _as_list(v):
    return v if isinstance(v, list) else []


def _as_number(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _role_of(image):
    if not isinstance(image, dict):
        return ""
    role = image.get("role", "")
    return (role if isinstance(role, str) else str(role or "")).strip().lower()


def validate(payload):
    failures = []

    product_only = bool(payload.get("product_only", False))
    images = _as_list(payload.get("images"))
    product_on_screen = bool(payload.get("product_on_screen", False)) or product_only
    voice_clip_seconds = _as_number(payload.get("voice_clip_seconds", 0), 0.0)
    duration = payload.get("duration", None)
    has_pace = "pace_wps" in payload and payload.get("pace_wps") is not None
    pace = _as_number(payload.get("pace_wps"), None)
    has_dialogue = bool(payload.get("has_dialogue", False))

    roles = [_role_of(img) for img in images]
    n_face = sum(1 for r in roles if r in FACE_ROLES)
    n_body = sum(1 for r in roles if r in BODY_ROLES)
    n_product = sum(1 for r in roles if r in PRODUCT_ROLES)
    n_character = n_face + n_body
    n_images = len(images)
    voice_attached = voice_clip_seconds is not None and voice_clip_seconds > 0

    if product_only:
        # CHECK 1p: a product-only b-roll has the PRODUCT + VOICE only, NO character.
        if n_product < 1:
            failures.append(
                "FAIL [product image required]: product_only b-roll has no image with "
                "role 'product'. Attach the product image.")
        if n_face > 0 or n_body > 0:
            failures.append(
                "FAIL [no character on a b-roll]: product_only is true but a face/body "
                "image is attached. B-rolls are product-only: attach the product image "
                "+ voice clip ONLY, no face, no body.")
        if not voice_attached:
            failures.append(
                "FAIL [b-roll needs voice]: product_only b-roll has no voice clip "
                "(voice_clip_seconds 0/missing). The voiceover uses the 15s reference.")
    else:
        # CHECK 1: character generations need a face AND a body reference.
        if n_face < 1:
            failures.append(
                "FAIL [face image required]: no image with role 'face'. The face image "
                "is the identity anchor on every character generation.")
        if n_body < 1:
            failures.append(
                "FAIL [body image required]: no image with role 'body'. The body image "
                "is the identity anchor on every character generation.")
        if n_character < MIN_CHARACTER_IMAGES:
            failures.append(
                "FAIL [>=2 character images]: found %d (face=%d, body=%d); a face and a "
                "body reference are both required." % (n_character, n_face, n_body))
        # CHECK 2: a product image is allowed only when the product is on screen.
        if n_product > 0 and not product_on_screen:
            failures.append(
                "FAIL [product image only when on screen]: %d product image(s) attached "
                "but product_on_screen is false." % n_product)

    # CHECK 3: voice reference clip capped at 15 seconds.
    if voice_clip_seconds is not None and voice_clip_seconds > VOICE_CLIP_MAX_SECONDS:
        failures.append(
            "FAIL [voice_clip_seconds<=15]: voice clip is %g s, max is %d s."
            % (voice_clip_seconds, VOICE_CLIP_MAX_SECONDS))

    # CHECK 4: duration must be an explicit integer 4..9 (UNDER 10). Never auto.
    if duration is None:
        failures.append(
            "FAIL [duration]: duration is missing. Always request an explicit integer "
            "4..9; never auto, never 10+.")
    else:
        dur_num = _as_number(duration, None)
        if dur_num is None:
            failures.append("FAIL [duration]: %r is not a number; request an integer 4..9."
                            % (duration,))
        elif dur_num != int(dur_num):
            failures.append("FAIL [duration]: %g is not an integer. Duration is an integer "
                            "4..9." % dur_num)
        else:
            di = int(dur_num)
            if not (DURATION_MIN <= di <= DURATION_MAX):
                failures.append(
                    "FAIL [duration in 4..9]: duration %d is outside 4..9. EVERY generation "
                    "must be UNDER 10 seconds; split longer content into more generations."
                    % di)

    # CHECK 5 (PACING): if pace_wps is provided it must be fast, in [2.4, 4.0].
    if has_pace:
        if pace is None:
            failures.append("FAIL [pace_wps]: present but not a number; use 2.4..4.0 or omit.")
        elif not (PACE_MIN <= pace <= PACE_MAX):
            guide = ("the shot DRAGS; shorten the seconds or lengthen the line"
                     if pace < PACE_MIN else
                     "the shot RUSHES; add a second or shorten the line")
            failures.append(
                "FAIL [pace 2.4..4.0 wps]: pace_wps is %.2f, outside the fast band. "
                "%s." % (pace, guide))

    # CHECK 6: total reference files <= 12.
    if n_images > MAX_TOTAL_FILES:
        failures.append("FAIL [total files<=12]: %d image file(s) attached, max %d."
                        % (n_images, MAX_TOTAL_FILES))

    # CHECK 7 (audio): a dialogue payload must attach the voice clip.
    if has_dialogue and not voice_attached:
        failures.append(
            "FAIL [dialogue needs voice clip]: has_dialogue is true but no voice clip is "
            "attached. Attach the 15s voice reference so Seedance speaks in the consistent voice.")

    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate_payload.py",
        description="Validate one Seedance 2.0 payload against the locked model "
                    "(sub-10s, slightly-fast pace, product-only b-rolls) before dispatch.")
    parser.add_argument("payload")
    args = parser.parse_args(argv)

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
        print("FAIL [payload file]: top-level JSON must be an object, got %s."
              % type(payload).__name__)
        return 1

    failures = validate(payload)
    if failures:
        for line in failures:
            print(line)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
