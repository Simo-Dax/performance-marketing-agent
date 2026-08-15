#!/usr/bin/env python3
"""
build_manifest.py - write the Talking-Object Ad assembly contract.

Reads spec.json and writes talking-object-ad-manifest.json in the LOCKED schema:

  { concept, niche, date, fps:30, resolution:"1080x1920", media_type:"video",
    framework, audio_mode:"native", total_seconds, references,
    scenes:[ {scene_id, role, speaker, clip, trim_in, trim_out, reference,
              voice_ref_source, on_screen_text} ] }

LOCKED MODEL (do not contradict):
  - AUDIO IS NATIVE: the clips' own dialogue audio IS the ad's soundtrack. There is NO
    vo_track in this factory — a spec that carries one is an ERROR (that's the VO-first
    family; wrong skill).
  - Scene order IS the timeline order. The last scene's role is `cta`; nothing follows
    it. No scene carries an uploaded voice.
  - Each scene plays trim_in..trim_out (> 0 and <= 9.5s; set trim_out to the clip's
    dialogue_check speech_end + 0.3-0.6s so dead tail air never pads the ad).
  - on_screen_text stays EMPTY everywhere except the CTA (the one in-scene text
    exception).

spec.json: top-level {concept, niche, date, framework, references?} plus EITHER an
inline "scenes" array OR "scenes_from":"scenes.json" (typically segment_scenes.py's
output with trim_out updated from the dialogue checks).

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
VOICE_KEYS = ("voice_clip", "voice_reference", "voice_url", "voice_sample",
              "audio_url", "audio_clip")


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
        if not os.path.isabs(src):
            src = os.path.join(os.path.dirname(os.path.abspath(spec_path)), src)
        data = load(src)
        sc = data.get("scenes") if isinstance(data, dict) else None
        if not isinstance(sc, list) or not sc:
            die("scenes_from file '%s' has no 'scenes' array" % src)
        return sc
    die("spec needs either an inline 'scenes' array or 'scenes_from' path")


def build(spec, spec_path):
    if spec.get("vo_track"):
        die("spec carries a vo_track — the talking-object factory has NO external "
            "voiceover; the clips' native dialogue IS the audio. (A VO spine belongs to "
            "the clay/skeleton/pixar factories.)")
    scenes_in = get_scenes(spec, spec_path)

    scenes_out = []
    total = 0.0
    for i, sc in enumerate(scenes_in):
        where = "scenes[%d]" % i
        if not isinstance(sc, dict):
            die(where + " must be an object")
        for vk in VOICE_KEYS:
            if vk in sc:
                die("%s carries '%s'; talking-object scenes never upload a voice — the "
                    "voice is generated natively." % (where, vk))
        sid = str(sc.get("scene_id") or ("scene_%02d" % (i + 1)))
        role = str(sc.get("role") or "")
        clip = str(sc.get("clip") or ("clips/%s.mp4" % sid))
        trim_in = float(sc.get("trim_in") or 0.0)
        if sc.get("trim_out") in (None, ""):
            die("%s (%s) missing trim_out (set it to the dialogue check's speech_end "
                "+ 0.3-0.6s)" % (where, sid))
        trim_out = float(sc["trim_out"])
        span = trim_out - trim_in
        if span <= 0:
            die("%s (%s) has non-positive span (trim_in=%g trim_out=%g)"
                % (where, sid, trim_in, trim_out))
        if span > MAX_SPAN:
            die("%s (%s) span %.2fs exceeds %.1fs; a clip can't be longer than a "
                "sub-10s render." % (where, sid, span, MAX_SPAN))
        ost = str(sc.get("on_screen_text") or "")
        if ost and role.lower() != "cta":
            die("%s (%s, role '%s') carries on_screen_text %r; the CTA is the only "
                "scene where in-scene text is legal." % (where, sid, role, ost))
        scenes_out.append({
            "scene_id": sid, "role": role,
            "speaker": str(sc.get("speaker") or ""),
            "clip": clip,
            "trim_in": round(trim_in, 3), "trim_out": round(trim_out, 3),
            "reference": sc.get("reference") or {"type": "none"},
            "voice_ref_source": sc.get("voice_ref_source") or None,
            "on_screen_text": ost,
        })
        total += span

    if not scenes_out:
        die("no scenes")
    if scenes_out[-1]["role"].lower() != "cta":
        die("the ad does not end on the CTA: last scene role is '%s', not 'cta'."
            % (scenes_out[-1]["role"] or "(none)"))
    for s in scenes_out[:-1]:
        if s["role"].lower() == "cta":
            warn("scene '%s' is a CTA but is not last; the ad should end on a single "
                 "CTA." % s["scene_id"])

    date = spec.get("date")
    if not date:
        date = datetime.date.today().isoformat()
        warn("spec had no 'date'; using today (%s)" % date)

    return {
        "concept": str(req(spec, "concept", "spec")),
        "niche": str(spec.get("niche") or ""),
        "date": str(date),
        "fps": FPS, "resolution": RESOLUTION, "media_type": MEDIA_TYPE,
        "framework": str(spec.get("framework") or ""),
        "audio_mode": "native",
        "total_seconds": round(total, 3),
        "references": spec.get("references") or {},
        "scenes": scenes_out,
    }


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
    print("Summary: %s (%s), %d scenes, %.2fs total, native dialogue audio, ends on "
          "CTA, %s @ %dfps"
          % (manifest["concept"], manifest["framework"] or "n/a",
             len(manifest["scenes"]), manifest["total_seconds"],
             manifest["resolution"], manifest["fps"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
