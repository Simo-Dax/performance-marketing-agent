#!/usr/bin/env python3
"""
build_manifest.py - write the Pixar Ad assembly contract.

Reads spec.json and writes pixar-ad-manifest.json in the LOCKED schema:

  { concept, niche, date, fps:30, resolution:"1080x1920", media_type:"video",
    framework, vo_track, total_seconds, keep_sfx, references,
    scenes:[ {scene_id, role, clip, trim_in, trim_out, reference, on_screen_text, sfx} ] }

LOCKED MODEL (do not contradict):
  - The ElevenLabs VO is the master audio spine: `vo_track` is REQUIRED. (This is the
    inverse of the UGC factory, which refuses a voice track.)
  - Scene order IS the timeline order. The last scene's role is `cta`; nothing follows
    it. No scene carries an uploaded voice.
  - Each scene plays trim_in..trim_out (its picture-locked VO span); that length is
    > 0 and <= 9s (it came from a sub-10s render).
  - keep_sfx true -> clip SFX is ducked under the VO at stitch; false -> silent picture.

spec.json: top-level {concept, niche, date, framework, vo_track, keep_sfx, references?}
plus EITHER an inline "scenes" array OR "scenes_from":"scenes.json" (loads that file's
"scenes"; typically the output of segment_scenes.py).

Usage: build_manifest.py spec.json out_manifest.json
"""

import argparse
import datetime
import json
import os
import sys

FPS = 30
RESOLUTION = "1080x1920"
MEDIA_TYPE = "video"
MAX_SPAN = 9.5
VOICE_KEYS = ("voice_clip", "voice", "voice_reference", "voice_url", "voice_sample")


def die(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(1)


def warn(msg):
    sys.stderr.write("WARN: " + msg + "\n")


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        die("file not found: " + path)
    except json.JSONDecodeError as exc:
        die("not valid JSON (%s): %s" % (path, exc))


def req(obj, key, where):
    if not isinstance(obj, dict) or key not in obj or obj[key] in (None, ""):
        die("missing required field '%s' in %s" % (key, where))
    return obj[key]


def get_scenes(spec, spec_path):
    if isinstance(spec.get("scenes"), list) and spec["scenes"]:
        return spec["scenes"]
    src = spec.get("scenes_from")
    if src:
        # resolve relative to the spec file
        if not os.path.isabs(src):
            src = os.path.join(os.path.dirname(os.path.abspath(spec_path)), src)
        data = load(src)
        sc = data.get("scenes") if isinstance(data, dict) else None
        if not isinstance(sc, list) or not sc:
            die("scenes_from file '%s' has no 'scenes' array" % src)
        return sc
    die("spec needs either an inline 'scenes' array or 'scenes_from' path")


def build(spec, spec_path):
    vo_track = req(spec, "vo_track", "spec")  # REQUIRED master voice spine
    scenes_in = get_scenes(spec, spec_path)

    scenes_out = []
    total = 0.0
    for i, sc in enumerate(scenes_in):
        where = "scenes[%d]" % i
        if not isinstance(sc, dict):
            die(where + " must be an object")
        for vk in VOICE_KEYS:
            if vk in sc:
                die("%s carries '%s'; Pixar scenes never upload a voice." % (where, vk))
        sid = str(sc.get("scene_id") or ("scene_%02d" % (i + 1)))
        role = str(sc.get("role") or "")
        clip = str(sc.get("clip") or ("clips/%s.mp4" % sid))
        trim_in = float(sc.get("trim_in") or 0.0)
        if sc.get("trim_out") in (None, ""):
            die("%s (%s) missing trim_out (the picture-locked span)" % (where, sid))
        trim_out = float(sc["trim_out"])
        span = trim_out - trim_in
        if span <= 0:
            die("%s (%s) has non-positive span (trim_in=%g trim_out=%g)"
                % (where, sid, trim_in, trim_out))
        if span > MAX_SPAN:
            die("%s (%s) span %.2fs exceeds %.1fs; a clip can't be longer than a sub-10s "
                "render. Re-run segment_scenes.py (it auto-splits)." % (where, sid, span, MAX_SPAN))
        scenes_out.append({
            "scene_id": sid, "role": role, "clip": clip,
            "trim_in": round(trim_in, 3), "trim_out": round(trim_out, 3),
            "reference": sc.get("reference") or {"type": "none"},
            "on_screen_text": str(sc.get("on_screen_text") or ""),
            "sfx": bool(sc.get("sfx", False)),
        })
        total += span

    if not scenes_out:
        die("no scenes")
    if scenes_out[-1]["role"].lower() != "cta":
        die("the ad does not end on the CTA: last scene role is '%s', not 'cta'. The CTA "
            "scene must be last." % (scenes_out[-1]["role"] or "(none)"))
    # no other scene may be the final beat after a cta (only one trailing cta allowed)
    for j, s in enumerate(scenes_out[:-1]):
        if s["role"].lower() == "cta":
            warn("scene '%s' is a CTA but is not last; the ad should end on a single CTA."
                 % s["scene_id"])

    date = spec.get("date")
    if not date:
        date = datetime.date.today().isoformat()
        warn("spec had no 'date'; using today (%s)" % date)

    manifest = {
        "concept": str(req(spec, "concept", "spec")),
        "niche": str(spec.get("niche") or ""),
        "date": str(date),
        "fps": FPS, "resolution": RESOLUTION, "media_type": MEDIA_TYPE,
        "framework": str(spec.get("framework") or ""),
        "vo_track": str(vo_track),
        "total_seconds": round(total, 3),
        "keep_sfx": bool(spec.get("keep_sfx", True)),
        "references": spec.get("references") or {},
        "scenes": scenes_out,
    }

    vo_total = spec.get("vo_total") or spec.get("total_seconds")
    if isinstance(vo_total, (int, float)) and abs(float(vo_total) - total) > 0.75:
        warn("scene spans sum to %.2fs but the VO is %.2fs (off by %.2fs); the final video "
             "will be padded/trimmed to the VO." % (total, float(vo_total), abs(float(vo_total) - total)))
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(prog="build_manifest.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("out_manifest")
    args = ap.parse_args(argv)

    spec = load(args.spec)
    if not isinstance(spec, dict):
        die("spec must be a JSON object")
    manifest = build(spec, args.spec)

    try:
        with open(args.out_manifest, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        die("could not write %s: %s" % (args.out_manifest, exc))

    print("Wrote manifest: " + args.out_manifest)
    print("Summary: %s (%s), %d scenes, %.2fs total, ends on CTA, vo_track=%s, keep_sfx=%s, %s @ %dfps"
          % (manifest["concept"], manifest["framework"] or "n/a", len(manifest["scenes"]),
             manifest["total_seconds"], manifest["vo_track"], manifest["keep_sfx"],
             manifest["resolution"], manifest["fps"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
