#!/usr/bin/env python3
"""
validate_payload.py - preflight ONE podcast generation before dispatch.

Enforces the locked model: exactly one IMAGE reference + one AUDIO (voice) cut,
NO video reference (this skill never uses video), duration an integer 4..9 (UNDER
10s). Run it on each generation's payload.json before rendering.

payload.json: {"image": "path", "audio": "path", "duration": 5}
Exit 0 PASS, 1 FAIL.
"""
import json, os, sys


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: validate_payload.py payload.json")
        return 1
    try:
        d = json.load(open(argv[0], encoding="utf-8"))
    except Exception as e:
        print("FAIL [payload]: %s" % e)
        return 1

    fails = []
    img, aud, vid, dur = d.get("image"), d.get("audio"), d.get("video"), d.get("duration")

    if not img:
        fails.append("FAIL [image]: missing reference image (identity anchor).")
    elif not os.path.exists(img):
        fails.append("FAIL [image]: not found: %s" % img)

    if not aud:
        fails.append("FAIL [audio]: missing voice reference (the per-generation unique cut).")
    elif not os.path.exists(aud):
        fails.append("FAIL [audio]: not found: %s" % aud)

    if vid:
        fails.append("FAIL [video]: a video reference is set. This skill NEVER uses a video "
                     "reference — identity is the image, voice is the audio cut. Remove it.")

    if dur is None:
        fails.append("FAIL [duration]: missing. Always an explicit integer 4..9.")
    else:
        try:
            f = float(dur)
            if f != int(f) or not (4 <= int(f) <= 9):
                fails.append("FAIL [duration]: %r must be an integer 4..9 (UNDER 10s)." % dur)
        except (TypeError, ValueError):
            fails.append("FAIL [duration]: %r is not a number 4..9." % dur)

    if fails:
        for x in fails:
            print(x)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
