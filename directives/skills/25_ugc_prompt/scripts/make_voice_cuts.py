#!/usr/bin/env python3
"""
make_voice_cuts.py - one uniquely-fingerprinted voice WAV per generation (UGC factory).

WHY THIS EXISTS (the _sfx dedup bug, hard-won on the podcast factory):
Higgsfield fingerprints the SPEECH CONTENT of an uploaded audio and lazily
transforms it into a processed `_sfx.wav` variant after its first use. Any later
or parallel generation that resolves to that transformed variant FAILS SILENTLY
(status: failed, empty error). Re-uploading the same file, padding silence, or a
fresh `upload create` id all collapse to the SAME poisoned asset, because the
fingerprint is on the speech itself. The only reliable fix: give every
generation a genuinely different speech fingerprint of the SAME voice.

This script reads the UGC render_plan.json and, for each generation, re-cuts the
member's ONE uploaded voice clip with a DISTINCT trim offset + tempo-shift
(pitch preserved, so the voice/timbre is unchanged but the fingerprint differs).
Output: voice_cuts/<gen_id>.wav (clean mono 44.1k pcm_s16le).

render_plan.json shape (authored by the orchestrator from the approved pacing
table; see references/voice-and-parallel.md):

  { "concept": "...",
    "resolution": "1080p",
    "inputs": { "face": "inputs/face.png", "body": "inputs/body.png",
                "product": "inputs/product.png", "voice": "inputs/voice.mp3" },
    "generations": [
      { "gen_id": "hook_reel_A", "role": "hook_reel", "duration": 8,
        "voice_cut": "hook_reel_A.wav",
        "images": ["face", "body", "product"],
        "prompt_file": "prompts/hook_reel_A.txt",
        "lines": [ {"line": "<hook 1 spoken line>", "clip": "hook_1"},
                   {"line": "<hook 2 spoken line>", "clip": "hook_2"} ] },
      ...
    ] }

Usage: python3 make_voice_cuts.py render_plan.json work_dir voice_cuts_dir
  work_dir is the concept folder ($WORK); input paths in the plan resolve
  relative to it.
"""
import json
import os
import subprocess
import sys


def _resolve(work, rel):
    if not rel:
        return None
    if os.path.isabs(rel) and os.path.exists(rel):
        return rel
    cand = os.path.join(work, rel)
    return cand if os.path.exists(cand) else None


def _dur(f):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "json", f], capture_output=True, text=True).stdout
        return float(json.loads(out)["format"]["duration"])
    except Exception:
        return 15.0


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: make_voice_cuts.py render_plan.json work_dir voice_cuts_dir\n")
        return 2
    plan_path, work, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    plan = json.load(open(plan_path, encoding="utf-8"))

    vp = _resolve(work, (plan.get("inputs") or {}).get("voice"))
    if not vp:
        sys.stderr.write("FAIL: could not resolve inputs.voice from the plan (looked under %s)\n" % work)
        return 1
    vd = _dur(vp)
    if vd > 15.5:
        sys.stderr.write("FAIL: voice clip is %.1fs; the reference must be 15s or under.\n" % vd)
        return 1

    failures = 0
    for i, g in enumerate(plan["generations"]):
        cut = g.get("voice_cut") or (g["gen_id"] + ".wav")
        # distinct fingerprint per generation: vary trim offset + tempo (pitch preserved)
        off = round((i * 0.6) % max(0.1, vd - 3.5), 2) if vd > 4.5 else 0.0
        tempo = round(0.93 + ((i * 0.021) % 0.16), 3)  # 0.93 .. 1.09
        out = os.path.join(outdir, cut)
        # -t 14.5 caps the OUTPUT under the 15s voice-reference limit even when a
        # slow tempo stretches a full-length clip (15s at atempo 0.93 = 16.1s).
        rc = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(off), "-i", vp,
                             "-af", "atempo=%s,aresample=44100" % tempo, "-ar", "44100", "-ac", "1",
                             "-c:a", "pcm_s16le", "-t", "14.5", out],
                            capture_output=True, text=True).returncode
        ok = rc == 0 and os.path.exists(out)
        failures += 0 if ok else 1
        print("%-16s <- %-24s ss=%.2f atempo=%.3f  %s" %
              (cut, os.path.basename(vp)[:24], off, tempo, "OK" if ok else "FAIL"))
    print("\n%d/%d unique voice cuts -> %s" % (len(plan["generations"]) - failures,
                                               len(plan["generations"]), outdir))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
