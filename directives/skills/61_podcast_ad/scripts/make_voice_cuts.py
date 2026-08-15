#!/usr/bin/env python3
"""
make_voice_cuts.py - one uniquely-fingerprinted voice WAV per generation.

Reads render_plan.json; for each generation, re-cuts that host's UPLOADED voice
clip with a DISTINCT trim offset + tempo-shift (pitch preserved, so the voice is
unchanged but the speech fingerprint differs). This is the trick that lets every
generation render in PARALLEL without colliding on Higgsfield's lazy _sfx audio
dedup (see references/voice-and-parallel.md). Output: voice_cuts/<gen_id>.wav
(clean mono 44.1k pcm_s16le).

Usage: python3 make_voice_cuts.py render_plan.json inputs_dir voice_cuts_dir
"""
import glob, json, os, subprocess, sys


def _resolve(inputs, rel):
    if not rel:
        return None
    if os.path.isabs(rel) and os.path.exists(rel):
        return rel
    cand = os.path.join(os.path.dirname(inputs.rstrip("/")), rel)  # rel to project root
    if os.path.exists(cand):
        return cand
    b = os.path.join(inputs, os.path.basename(rel))
    return b if os.path.exists(b) else None


def _voice_for(inputs, host, spk):
    vp = _resolve(inputs, (host or {}).get("voice"))
    if vp:
        return vp
    pool = (glob.glob(os.path.join(inputs, "*%s*oice*" % spk)) or
            glob.glob(os.path.join(inputs, "*%s*" % spk)))
    pool = [x for x in pool if x.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".ogg"))]
    if not pool:
        pool = sum((glob.glob(os.path.join(inputs, "*" + e)) for e in (".mp3", ".wav", ".m4a")), [])
    return pool[0] if pool else None


def _dur(f):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "json", f], capture_output=True, text=True).stdout
        return float(json.loads(out)["format"]["duration"])
    except Exception:
        return 15.0


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: make_voice_cuts.py render_plan.json inputs_dir voice_cuts_dir\n")
        return 2
    plan_path, inputs, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    plan = json.load(open(plan_path, encoding="utf-8"))
    hosts = plan.get("hosts") or {}
    for i, g in enumerate(plan["generations"]):
        spk = g["speaker"]
        vp = _voice_for(inputs, hosts.get(spk), spk)
        if not vp:
            print("NO VOICE found for speaker %s (gen %s)" % (spk, g["gen_id"]))
            continue
        vd = _dur(vp)
        # distinct fingerprint per generation: vary trim offset + tempo (pitch preserved)
        off = round((i * 0.6) % max(0.1, vd - 3.5), 2) if vd > 4.5 else 0.0
        tempo = round(0.93 + ((i * 0.021) % 0.16), 3)  # 0.93 .. 1.09
        out = os.path.join(outdir, g["voice_cut"])
        rc = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(off), "-i", vp,
                             "-af", "atempo=%s,aresample=44100" % tempo, "-ar", "44100", "-ac", "1",
                             "-c:a", "pcm_s16le", out], capture_output=True, text=True).returncode
        ok = rc == 0 and os.path.exists(out)
        print("%-12s <- %-24s ss=%.2f atempo=%.3f  %s" %
              (g["voice_cut"], os.path.basename(vp)[:24], off, tempo, "OK" if ok else "FAIL"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
