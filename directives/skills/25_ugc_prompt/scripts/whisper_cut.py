#!/usr/bin/env python3
"""
whisper_cut.py - cut each rendered UGC generation into word-accurate clips AND
verify the spoken words against the approved script. EDIT-ONLY (spends no credits).

For each generation in render_plan.json:
  - faster-whisper transcribes the mp4 with WORD timestamps,
  - the KNOWN script lines are aligned to the recognized words (difflib) to get
    each line's real [start, end] (robust to mis-heard middle words; NOT
    silence-guessing, which a dramatic in-line pause defeats),
  - each line becomes one clip, named by its `clip` field: clips/<clip>.mp4,
  - a per-line MATCH RATIO is printed (recognized words vs the script). A low
    ratio means Seedance garbled or swapped words — LISTEN to that clip before
    assembly and re-render it only if the words are actually wrong.

CUT RULES (the UGC house style):
  - The FIRST line of a generation keeps the clip's natural head (starts at 0.0)
    so a hook's visual action is NEVER chopped off. Later lines in a multi-line
    generation (a hook reel) start ~0.08s before their first word — that is the
    word-accurate reel split.
  - Every line ends ~0.20s after its LAST word (snappy, the word rings out, no
    dead tail). Per-line override: set "tail" on the line in the plan (the CTA
    line should get ~0.6s so the ad breathes at the end).
  - A clip never bleeds into the next line (bounded at next_start - 0.05).
  - Internal scene cuts are DETECTED and printed as info, never auto-truncated:
    a UGC hook may legally contain a deliberate hard cut (e.g. a before/after).

Output: clips/<clip>.mp4 per line. Self-bootstraps faster-whisper into the
shared venv (~/.cache/pm-agent/whisper-venv — the same engine the
clay/skeleton factories use; falls back to the podcast venv if that one already
exists).

Usage: python3 whisper_cut.py render_plan.json gens_dir clips_dir [--lead 0.08] [--tail 0.20]
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys

_VENVS = ["~/.cache/pm-agent/whisper-venv", "~/.cache/pm-agent/whisper"]


def _bootstrap():
    try:
        import faster_whisper  # noqa: F401
        return
    except Exception:
        pass
    target = None
    for v in _VENVS:
        py = os.path.join(os.path.expanduser(v), "bin", "python")
        if os.path.exists(py) and subprocess.run(
                [py, "-c", "import faster_whisper"], capture_output=True).returncode == 0:
            target = py
            break
    if target is None:
        venv = os.path.expanduser(_VENVS[0])
        py = os.path.join(venv, "bin", "python")
        os.makedirs(os.path.dirname(venv), exist_ok=True)
        subprocess.run(["python3", "-m", "venv", venv], capture_output=True)
        subprocess.run([os.path.join(venv, "bin", "pip"), "install", "-q", "faster-whisper"],
                       capture_output=True)
        if os.path.exists(py) and subprocess.run(
                [py, "-c", "import faster_whisper"], capture_output=True).returncode == 0:
            target = py
    if target and os.path.abspath(sys.executable or "") != os.path.abspath(target):
        os.execv(target, [target, os.path.abspath(__file__)] + sys.argv[1:])


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
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "json", f], capture_output=True, text=True).stdout
        return float(json.loads(out)["format"]["duration"])
    except Exception:
        return None  # unreadable/zero-byte mp4; caller skips the generation


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
    try:
        os.remove(wav)
    except OSError:
        pass
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
    st, en, matched = {}, {}, {}
    for li in range(len(lines)):
        toks = [si for si in range(first.get(li, 0), last.get(li, -1) + 1)] if li in first else []
        matched[li] = (sum(1 for si in toks if si in s2w), len(toks))
        # bounds-checked walks: a fully-garbled line must get NO timing rather than
        # borrowing a neighbor line's word (which would also chop the next clip's head)
        si = last.get(li)
        while si is not None and si >= first[li] and si not in s2w:
            si -= 1
        if si is not None and first.get(li, 0) <= si <= last.get(li, -1) and si in s2w:
            en[li] = ws[s2w[si]][1]
        si = first.get(li)
        while si is not None and si <= last[li] and si not in s2w:
            si += 1
        if si is not None and first.get(li, 0) <= si <= last.get(li, -1) and si in s2w:
            st[li] = ws[s2w[si]][0]
    return st, en, matched


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

    low_matches = []
    for g in plan["generations"]:
        mp4 = os.path.join(a.gens, g["gen_id"] + ".mp4")
        if not os.path.exists(mp4):
            print("MISSING generation %s (skipping)" % g["gen_id"])
            continue
        d = dur_of(mp4)
        if d is None or d <= 0:
            print("BROKEN generation %s (unreadable mp4, skipping — re-download it)" % g["gen_id"])
            continue
        ws = words_of(mp4)
        lines = [ln["line"] for ln in g["lines"]]
        st, en, matched = align(lines, ws)
        cuts = scene_cuts(mp4)
        prev = 0.0
        for li, ln in enumerate(g["lines"]):
            ls = st.get(li, prev)
            le = en.get(li, min(d, ls + 1.0))
            tail = float(ln.get("tail", a.tail))
            # first line keeps the clip's natural head (never chop the hook action)
            cs = 0.0 if li == 0 else max(0.0, ls - a.lead, prev)
            ce = min(d, le + tail)
            if (li + 1) in st:
                ce = min(ce, st[li + 1] - 0.05)          # never bleed into the next line
            if ce < cs + 0.4:
                ce = min(d, cs + 0.4)
            out = os.path.join(a.clips, "%s.mp4" % ln["clip"])
            enc(["-ss", str(round(cs, 3)), "-to", str(round(ce, 3)), "-i", mp4] + ENC + [out])
            hit, total = matched.get(li, (0, 0))
            ratio = (hit / total) if total else 0.0
            flag = ""
            if ratio < 0.75:
                flag = "  <<LOW MATCH %.0f%% - LISTEN, words may be garbled>>" % (ratio * 100)
                low_matches.append(ln["clip"])
            internal = [t for t in cuts if cs + 0.3 < t < ce - 0.1]
            cut_note = ("  [internal cut @ %s]" % ",".join("%.1f" % t for t in internal)) if internal else ""
            print("%-12s [%.2f-%.2f] %.2fs  words %d/%d (%.0f%%)%s%s  \"%s\"" %
                  (ln["clip"], cs, ce, ce - cs, hit, total, ratio * 100, cut_note, flag,
                   ln["line"][:48]))
            prev = ce
    if low_matches:
        print("\nLOW-MATCH clips to review before assembly: %s" % ", ".join(low_matches))
    print("\ncut word-accurate clips -> %s" % a.clips)
    return 0


if __name__ == "__main__":
    sys.exit(main())
