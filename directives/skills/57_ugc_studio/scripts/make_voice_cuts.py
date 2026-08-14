#!/usr/bin/env python3
"""
make_voice_cuts.py - one uniquely-fingerprinted voice WAV per TALKING generation
(UGC Studio).

WHY THIS EXISTS (the _sfx dedup physics, verified in production):
Higgsfield fingerprints the SPEECH CONTENT of an uploaded audio and lazily
transforms it into a processed `_sfx.wav` variant after its first use. Any later
or parallel generation that resolves to that transformed variant FAILS SILENTLY
(status: failed, empty error). Re-uploading the same file, padding silence, or a
fresh `upload create` id all collapse to the SAME poisoned asset, because the
fingerprint is on the speech itself. The only reliable fix: give every
generation a genuinely different speech fingerprint of the SAME voice.

This script reads the studio render_plan.json (pipeline-contracts.md #1) and,
for every `kind: "gen"` entry that actually SPEAKS (non-empty `lines` plus a
`voice_cut` name), re-cuts the member's ONE uploaded voice clip with a DISTINCT
trim offset + tempo-shift (pitch preserved, so the voice/timbre is unchanged
but the fingerprint differs). Output: voice_cuts/<gen_id>.wav, clean mono
44.1k pcm_s16le, capped at 14.5s so a slow atempo never stretches a full clip
past the 15s voice-reference limit (15s at atempo 0.93 = 16.1s).

Skipped, each with a printed reason:
  - silent gens (no `lines`): b-roll/insert beats render with NO audio at all;
  - gens with no `voice_cut` in the plan (a plan defect on Higgsfield paths -
    validate_payload.py owns that flag; this script never invents filenames);
  - still / footage / composite entries (never carry voice);
  - the ENTIRE plan when `backend` is "fal": fal has no per-asset _sfx dedup,
    the one source voice rides every generation unmodified.

Usage: python3 make_voice_cuts.py render_plan.json work_dir voice_cuts_dir
  work_dir is the ad's work folder ($WORK); plan paths resolve relative to it.
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
    try:
        plan = json.load(open(plan_path, encoding="utf-8"))
    except Exception as e:
        sys.stderr.write("FAIL: cannot read plan %s (%s)\n" % (plan_path, e))
        return 1
    if not isinstance(plan, dict) or not isinstance(plan.get("entries"), list):
        sys.stderr.write("FAIL: plan has no entries[] list (see pipeline-contracts.md #1)\n")
        return 1

    if plan.get("backend") == "fal":
        print("backend=fal: skipping ALL voice cuts - fal has no per-asset _sfx dedup, "
              "so the one source voice rides every generation unmodified. Nothing to do.")
        return 0

    gens = [e for e in plan["entries"] if e.get("kind") == "gen"]
    todo = []
    for i, g in enumerate(gens):
        gid = g.get("gen_id") or ("gen_%d" % i)
        if not (g.get("lines") or []):
            print("SKIP %-16s silent gen (no lines) - renders with no audio at all" % gid)
            continue
        if not g.get("voice_cut"):
            print("SKIP %-16s talking gen with no voice_cut in the plan - "
                  "run validate_payload.py; not inventing a filename" % gid)
            continue
        todo.append((i, g))
    if not todo:
        print("\n0 talking gens carry a voice_cut - no cuts to make.")
        return 0

    vp = _resolve(work, (plan.get("inputs") or {}).get("voice"))
    if not vp:
        sys.stderr.write("FAIL: could not resolve inputs.voice from the plan (looked under %s)\n" % work)
        return 1
    vd = _dur(vp)
    if vd > 15.5:
        sys.stderr.write("FAIL: voice clip is %.1fs; the reference must be 15s or under.\n" % vd)
        return 1

    os.makedirs(outdir, exist_ok=True)
    failures = 0
    for i, g in todo:
        cut = g["voice_cut"]
        # distinct fingerprint per generation: vary trim offset + tempo (pitch preserved);
        # i indexes the FULL gen list so fingerprints stay stable when silent gens interleave
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
    print("\n%d/%d unique voice cuts -> %s (%d gen entries skipped)" %
          (len(todo) - failures, len(todo), outdir, len(gens) - len(todo)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
