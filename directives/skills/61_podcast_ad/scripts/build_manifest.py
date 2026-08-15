#!/usr/bin/env python3
"""
build_manifest.py - turn-ordered assembly manifest for the podcast ad.

Reads transcript.json (the approved turns) and the clips dir, and emits
assembly-manifest.json whose ordered_timeline lists each clip
(clips/<turn>_<speaker>.mp4) in CONVERSATION (turn) order. stitch_podcast.sh
consumes this. Reports any missing clips.

Usage: python3 build_manifest.py transcript.json clips_dir out_manifest.json
"""
import json, os, sys


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 3:
        sys.stderr.write("usage: build_manifest.py transcript.json clips_dir out_manifest.json\n")
        return 2
    tpath, clips, out = argv[0], argv[1], argv[2]
    t = json.load(open(tpath, encoding="utf-8"))
    turns = t.get("turns") or []

    timeline, missing = [], []
    for tn in turns:
        name = "%d_%s.mp4" % (tn["turn"], tn["speaker"])
        if not os.path.exists(os.path.join(clips, name)):
            missing.append(name)
            continue
        timeline.append({"turn": tn["turn"], "speaker": tn["speaker"],
                         "clip": os.path.join("clips", name), "line": tn["line"]})

    man = {"concept": t.get("concept"), "brand": t.get("brand"), "fps": 30,
           "resolution": "1080x1920", "loudness_lufs": -14, "ordered_timeline": timeline}
    json.dump(man, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("wrote %s (%d clips in order)" % (out, len(timeline)))
    if missing:
        print("MISSING clips (not stitched):", ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
