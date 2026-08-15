#!/usr/bin/env python3
"""
whisper_cut.py - cut each rendered generation into per-turn clips, word-accurate.

EDIT-ONLY (spends no credits). For each generation in render_plan.json:
  - faster-whisper transcribes the clip with WORD timestamps,
  - the KNOWN script lines are aligned to the recognized words (difflib) to get
    each line's real [start, end] (robust to mis-heard middle words; NOT silence-
    guessing, which a dramatic in-line pause defeats),
  - each line is cut to start ~0.08s before its first word (dropping any front
    startup "peep") and end ~0.20s after its last word (never bleeding into the
    next line), and
  - each output clip is scene-detected to confirm it is a SINGLE shot.

Output: clips/<turn>_<speaker>.mp4. Self-bootstraps faster-whisper into
~/.cache/pm-agent/whisper-venv (durable + namespaced, so the model is not
re-downloaded every reboot the way a /tmp venv would be).

Usage: python3 whisper_cut.py render_plan.json gens_dir clips_dir [--lead 0.08] [--tail 0.20]
"""
import argparse, difflib, json, os, re, subprocess, sys


def _bootstrap():
    try:
        import faster_whisper  # noqa: F401
        return
    except Exception:
        pass
    venv = os.path.expanduser("~/.cache/pm-agent/whisper-venv")
    py = os.path.join(venv, "bin", "python")
    if not (os.path.exists(py) and
            subprocess.run([py, "-c", "import faster_whisper"], capture_output=True).returncode == 0):
        os.makedirs(os.path.dirname(venv), exist_ok=True)
        subprocess.run(["python3", "-m", "venv", venv], capture_output=True)
        subprocess.run([os.path.join(venv, "bin", "pip"), "install", "-q", "faster-whisper"],
                       capture_output=True)
    if os.path.exists(py) and os.path.abspath(sys.executable or "") != os.path.abspath(py):
        os.execv(py, [py, os.path.abspath(__file__)] + sys.argv[1:])


_bootstrap()
import warnings  # noqa: E402
warnings.filterwarnings("ignore")
from faster_whisper import WhisperModel  # noqa: E402

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]
_MODEL = None


def model():
    global _MODEL
    if _MODEL is None:
        _MODEL = WhisperModel("small.en", device="cpu", compute_type="int8")
    return _MODEL


def enc(args):
    return subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error"] + args,
                          capture_output=True, text=True).returncode


def dur_of(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "json", f], capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def words_of(mp4):
    wav = mp4 + ".wav"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", mp4, "-ar", "16000",
                    "-ac", "1", wav], capture_output=True)
    segs, _ = model().transcribe(wav, word_timestamps=True)
    ws = []
    for s in segs:
        for w in (s.words or []):
            ws.append((w.start, w.end, w.word.strip()))
    return ws


def align(lines, ws):
    sc = []
    for li, ln in enumerate(lines):
        for tok in str(ln).split():
            n = norm(tok)
            if n:
                sc.append((n, li))
    s2w = {}
    sm = difflib.SequenceMatcher(a=[x[0] for x in sc], b=[norm(w[2]) for w in ws], autojunk=False)
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            s2w[b.a + k] = b.b + k
    first, last = {}, {}
    for si, (n, li) in enumerate(sc):
        last[li] = si
        first.setdefault(li, si)
    st, en = {}, {}
    for li in range(len(lines)):
        si = last.get(li)
        while si is not None and si >= first[li] and si not in s2w:
            si -= 1
        if si is not None and si in s2w:
            en[li] = ws[s2w[si]][1]
        si = first.get(li)
        while si is not None and si <= last[li] and si not in s2w:
            si += 1
        if si is not None and si in s2w:
            st[li] = ws[s2w[si]][0]
    return st, en


def scene_cuts(mp4, thr=0.3):
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", mp4, "-vf",
                        "select='gt(scene,%g)',showinfo" % thr, "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def main():
    ap = argparse.ArgumentParser(prog="whisper_cut.py")
    ap.add_argument("plan")
    ap.add_argument("gens")
    ap.add_argument("clips")
    ap.add_argument("--lead", type=float, default=0.08)
    ap.add_argument("--tail", type=float, default=0.20)
    a = ap.parse_args()
    os.makedirs(a.clips, exist_ok=True)
    plan = json.load(open(a.plan, encoding="utf-8"))

    for g in plan["generations"]:
        mp4 = os.path.join(a.gens, g["gen_id"] + ".mp4")
        if not os.path.exists(mp4):
            print("MISSING generation %s (skipping)" % g["gen_id"])
            continue
        d = dur_of(mp4)
        ws = words_of(mp4)
        lines = [ln["line"] for ln in g["lines"]]
        st, en = align(lines, ws)
        cuts = scene_cuts(mp4)
        prev = 0.0
        for li, ln in enumerate(g["lines"]):
            ls = st.get(li, prev)
            le = en.get(li, min(d, ls + 1.0))
            cs = max(0.0, ls - a.lead, prev)
            ce = min(d, le + a.tail)
            if (li + 1) in st:
                ce = min(ce, st[li + 1] - 0.05)          # never bleed into next line
            internal = [t for t in cuts if cs + 0.2 < t < ce - 0.05]
            if internal:
                ce = min(ce, min(internal) - 0.03)        # keep it a single shot
            if ce < cs + 0.4:
                ce = min(d, cs + 0.4)
            out = os.path.join(a.clips, "%d_%s.mp4" % (ln["turn"], g["speaker"]))
            enc(["-ss", str(round(cs, 3)), "-to", str(round(ce, 3)), "-i", mp4] + ENC + [out])
            dbl = "  <<DOUBLE-SHOT, CHECK>>" if scene_cuts(out) else ""
            print("turn %-2d %s  [%.2f-%.2f] %.2fs  tail %.2f%s  \"%s\"" %
                  (ln["turn"], g["speaker"], cs, ce, ce - cs, ce - le, dbl, ln["line"]))
            prev = ce
    print("\ncut per-turn clips -> %s" % a.clips)
    return 0


if __name__ == "__main__":
    sys.exit(main())
