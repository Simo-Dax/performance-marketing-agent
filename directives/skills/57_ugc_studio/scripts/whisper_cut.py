#!/usr/bin/env python3
"""
whisper_cut.py - UGC Studio word-accurate cutter + cut_report.json (the measured
truth). EDIT-ONLY (spends no credits): it measures what actually rendered and
cuts it; it NEVER re-renders and NEVER auto-truncates - a missing or mistimed
internal cut is rescued in the edit (slice, crop punch-in, overlay); only wrong
CONTENT justifies a proposed re-render.

Reads render_plan.json and processes every entry with kind "gen":

NARRATED gens (have lines[]):
  - faster-whisper transcribes gens/<gen_id>.mp4 with WORD timestamps,
  - the KNOWN script lines are aligned to the recognized words (difflib) to get
    each line's real [start, end] (robust to mis-heard middle words; NOT
    silence-guessing, which a dramatic in-line pause defeats),
  - each line becomes one clip: clips/<clip>.mp4,
  - a per-line MATCH RATIO is printed (recognized vs scripted words). <75% means
    Seedance garbled or swapped words - LISTEN to that clip before assembly and
    re-render only if the words are actually wrong.
  CUT RULES (the studio house style):
  - The FIRST line of a gen keeps the clip's natural head (starts at 0.0) so a
    hook's visual action is NEVER chopped off. Later lines start ~0.08s before
    their first word - the word-accurate split.
  - Every line ends ~0.20s after its LAST word (snappy, the word rings out, no
    dead tail). Per-line override: "tail" on the line (closes get ~0.6 so the
    ad breathes). A clip never bleeds into the next line (bounded at
    next_start - 0.05).

SILENT gens (no lines[]; sub_shots[] carry clip names) - PLAN-CUT MODE:
  - cut at the planned sub_shot `t` offsets, RECONCILED first: scene-detect is
    the reconciliation source for silent gens (in-generation timing is
    unreliable - the model lands hard cuts NEAR, not ON, the planned offset).
    A detected cut within +/-0.5s of a planned t wins and the cut SNAPS to the
    detected time; otherwise the planned t cuts and the gen is flagged. The
    last sub-shot runs to end of file.

cut_report.json (written into clips_dir) is what the EDL and manifest anchor
on: per clip {src range, match_ratio (null for silent), CLIP-RELATIVE word
timestamps (overlay word-anchors resolve against these), clip-relative
internal_cuts}; per gen {planned_sub_shots, detected_cuts, reconcile}.
Reconcile: every planned t>0 needs a detected cut within +/-0.5s (else
"MISSING <t>"); a detected cut >0.3s from every planned t is "EXTRA <t>"
(inspect the frame grid). Single-shot gens (no sub_shots map) reconcile "OK"
trivially - detected cuts there are EXTRA, informational.

Self-bootstraps faster-whisper into the plugin's shared venv
(~/.cache/pm-agent/whisper-venv; falls back to ~/.cache/pm-agent/whisper
if that one already exists).

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


def fmt_t(t):
    s = ("%.2f" % t).rstrip("0").rstrip(".")
    return s or "0"


def reconcile_gen(planned, detected):
    """Planned sub-shot map vs scene-detected reality. Report-only by law:
    timing misses are fixed in the edit, never with credits."""
    miss = [t for t in planned if t > 0 and not any(abs(c - t) <= 0.5 for c in detected)]
    extra = [c for c in detected
             if not planned or min(abs(c - t) for t in planned) > 0.3]
    parts = (["MISSING %s" % fmt_t(t) for t in miss] +
             ["EXTRA %s" % fmt_t(c) for c in extra])
    notes = []
    if miss:
        notes.append("planned cut never rendered - rescue edit-side "
                     "(slice/crop punch-in/overlay), never re-render for timing")
    if extra:
        notes.append("unplanned cut - inspect the frame grid" if planned else
                     "informational: cuts detected in a single-shot gen - inspect the frame grid")
    return (", ".join(parts) if parts else "OK"), "; ".join(notes)


def clip_row(name, gen_id, cs, ce, ratio, ws, detected):
    """One cut_report clip object. Word times are CLIP-RELATIVE (the EDL anchors
    overlays on them); internal_cuts likewise."""
    return {
        "clip": name, "gen_id": gen_id,
        "src_start": round(cs, 2), "src_end": round(ce, 2),
        "duration": round(ce - cs, 2),
        "match_ratio": None if ratio is None else round(ratio, 2),
        "words": [{"w": w, "start": round(max(0.0, s - cs), 3), "end": round(max(0.0, e - cs), 3)}
                  for (s, e, w) in ws if cs - 1e-6 <= s < ce],
        "internal_cuts": [round(t - cs, 2) for t in detected if cs + 0.3 < t < ce - 0.1],
    }


def cut_narrated(g, mp4, d, detected, a, low_matches, report_clips):
    ws = words_of(mp4)
    lines = [ln["line"] for ln in g["lines"]]
    st, en, matched = align(lines, ws)
    prev, ok = 0.0, True
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
        rc = enc(["-ss", str(round(cs, 3)), "-to", str(round(ce, 3)), "-i", mp4] + ENC + [out])
        if rc != 0 or not os.path.exists(out):
            print("ENCODE FAILED %s (ffmpeg rc %d) - check %s" % (ln["clip"], rc, mp4))
            ok = False
        hit, total = matched.get(li, (0, 0))
        ratio = (hit / total) if total else 0.0
        flag = ""
        if ratio < 0.75:
            flag = "  <<LOW MATCH %.0f%% - LISTEN, words may be garbled>>" % (ratio * 100)
            low_matches.append(ln["clip"])
        row = clip_row(ln["clip"], g["gen_id"], cs, ce, ratio, ws, detected)
        report_clips.append(row)
        cut_note = ("  [internal cut @ %s]" % ",".join("%.1f" % t for t in row["internal_cuts"])
                    ) if row["internal_cuts"] else ""
        print("%-12s [%.2f-%.2f] %.2fs  words %d/%d (%.0f%%)%s%s  \"%s\"" %
              (ln["clip"], cs, ce, ce - cs, hit, total, ratio * 100, cut_note, flag,
               ln["line"][:48]))
        prev = ce
    return ok


def cut_silent(g, mp4, d, detected, a, report_clips):
    subs = sorted(g["sub_shots"], key=lambda s: float(s.get("t", 0.0)))
    bounds = [0.0]                                    # first sub-shot always owns the head
    for s in subs[1:]:
        t = float(s["t"])
        near = [c for c in detected if abs(c - t) <= 0.5]
        if near:
            b = min(near, key=lambda c: abs(c - t))   # the detected cut is the truth; snap to it
            print("  plan-cut %s: t=%s snapped to detected cut %.2f" % (g["gen_id"], fmt_t(t), b))
        else:
            b = t
            print("  plan-cut %s: t=%s has NO detected cut within 0.5s - cutting at planned "
                  "time, verify frames" % (g["gen_id"], fmt_t(t)))
        bounds.append(b)
    # monotonic + inside the file: a mis-planned t still yields a bounded clip
    for i in range(1, len(bounds)):
        bounds[i] = min(max(bounds[i], bounds[i - 1] + 0.1), max(0.1, d - 0.1))
    bounds.append(d)                                  # last sub-shot runs to end of file
    ok = True
    for i, s in enumerate(subs):
        cs, ce = bounds[i], bounds[i + 1]
        out = os.path.join(a.clips, "%s.mp4" % s["clip"])
        rc = enc(["-ss", str(round(cs, 3)), "-to", str(round(ce, 3)), "-i", mp4] + ENC + [out])
        if rc != 0 or not os.path.exists(out):
            print("ENCODE FAILED %s (ffmpeg rc %d) - check %s" % (s["clip"], rc, mp4))
            ok = False
        row = clip_row(s["clip"], g["gen_id"], cs, ce, None, [], detected)
        report_clips.append(row)
        cut_note = ("  [internal cut @ %s]" % ",".join("%.1f" % t for t in row["internal_cuts"])
                    ) if row["internal_cuts"] else ""
        print("%-12s [%.2f-%.2f] %.2fs  silent plan-cut%s  \"%s\"" %
              (s["clip"], cs, ce, ce - cs, cut_note, str(s.get("shot", ""))[:48]))
    return ok


def main():
    ap = argparse.ArgumentParser(prog="whisper_cut.py")
    ap.add_argument("plan")
    ap.add_argument("gens")
    ap.add_argument("clips")
    ap.add_argument("--lead", type=float, default=0.08)
    ap.add_argument("--tail", type=float, default=0.20)
    a = ap.parse_args()
    try:
        with open(a.plan, encoding="utf-8") as f:
            plan = json.load(f)
    except (OSError, ValueError) as e:
        print("BAD PLAN %s: %s" % (a.plan, e))
        return 2
    entries = plan.get("entries")
    if not isinstance(entries, list):
        print("BAD PLAN %s: no entries[] list (see pipeline-contracts.md section 1)" % a.plan)
        return 2
    os.makedirs(a.clips, exist_ok=True)

    report_clips, report_gens, low_matches = [], [], []
    failures = 0
    for g in entries:
        if not isinstance(g, dict) or g.get("kind") != "gen":
            continue
        gid = g.get("gen_id")
        if not gid:
            print("PLAN ERROR: a gen entry has no gen_id - fix render_plan.json")
            failures += 1
            continue
        mp4 = os.path.join(a.gens, gid + ".mp4")
        if not os.path.exists(mp4):
            print("MISSING generation %s (skipping)" % gid)
            continue
        d = dur_of(mp4)
        if d is None or d <= 0:
            print("BROKEN generation %s (unreadable mp4, skipping - re-download it)" % gid)
            continue
        detected = scene_cuts(mp4)
        lines = g.get("lines") or []
        subs = g.get("sub_shots") or []
        if lines:
            ok = cut_narrated(g, mp4, d, detected, a, low_matches, report_clips)
        elif subs:
            if any(not s.get("clip") for s in subs):
                print("PLAN ERROR: silent gen %s sub_shots missing 'clip' names - plan-cut mode "
                      "cannot name its outputs (contracts section 1, sub_shots)" % gid)
                failures += 1
                continue
            ok = cut_silent(g, mp4, d, detected, a, report_clips)
        else:
            print("PLAN ERROR: silent gen %s has no sub_shots map - plan-cut mode needs it "
                  "(each sub_shot carries t + clip)" % gid)
            failures += 1
            continue
        if not ok:
            failures += 1
        planned = [round(float(s.get("t", 0.0)), 2) for s in subs]
        rec, notes = reconcile_gen(planned, detected)
        report_gens.append({"gen_id": gid,
                            "planned_sub_shots": planned,
                            "detected_cuts": [round(c, 2) for c in detected],
                            "reconcile": rec,
                            "notes": notes})
        print("gen %-16s detected cuts [%s]  reconcile: %s" %
              (gid, ",".join("%.2f" % c for c in detected), rec))

    rp = os.path.join(a.clips, "cut_report.json")
    with open(rp, "w", encoding="utf-8") as f:
        json.dump({"clips": report_clips, "gens": report_gens}, f, indent=2)
    if low_matches:
        print("\nLOW-MATCH clips to review before assembly: %s" % ", ".join(low_matches))
    print("\ncut word-accurate clips -> %s (report: %s)" % (a.clips, rp))
    return 3 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
