#!/usr/bin/env python3
"""
align_vo.py - map an ElevenLabs voiceover onto the known script, line by line.

The Clay Ad is voiceover-first: the user voices the approved script once, and the
audio is the master clock. This tool measures WHERE each script line begins in that
audio so each clay scene can be cut to the voice (picture-lock).

OUTPUT MODEL (contiguous spans, no gaps):
  Each line "owns" the audio from its own start until the NEXT line's start, so the
  spans tile [0, total] with no holes. Inter-line pauses are absorbed into the
  preceding line's span, so the picture never goes black during a pause. The last
  line owns up to the audio's end. This is exactly what segment_scenes.py needs.

METHOD:
  1. ffprobe -> exact total audio duration.
  2. faster-whisper transcribes with WORD timestamps (run inside a dedicated venv;
     this script self-bootstraps into ~/.cache/pm-agent/whisper-venv if the current
     interpreter lacks faster_whisper).
  3. The KNOWN script tokens are aligned onto the recognized word stream (difflib),
     so each line's first word gets a real start time -> the line boundaries.
  4. Fallback when whisper is unavailable: split the total duration across lines by
     word count (exact total, approximate per-line). method = "proportional".

Usage:
  align_vo.py transcript.json audio_file out_timing.json [--model base.en] [--proportional]

transcript.json: {"concept","niche","framework","lines":[{"id","role","vo"} ...]}
out_timing.json: {"audio_file","total_seconds","method","lines":[
                   {"id","role","vo","start","end","dur","word_count"} ...]}

Exit 0 on success, 2 on bad input / missing audio, 1 on an unexpected failure.
"""

import argparse
import difflib
import json
import os
import re
import subprocess
import sys

DEFAULT_MODEL = os.environ.get("CLAY_AD_WHISPER_MODEL", "base.en")
_TOK = re.compile(r"[a-z0-9']+")


def toks(s):
    return _TOK.findall((s or "").lower())


def die(msg, code=2):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(code)


# --- self-bootstrap into the whisper venv ------------------------------------
def bootstrap_into_venv():
    """If the current interpreter can't import faster_whisper, re-exec through the
    dedicated venv. Guarded by an env sentinel so it never loops."""
    try:
        import faster_whisper  # noqa: F401
        return
    except Exception:
        pass
    if os.environ.get("CLAY_AD_BOOTSTRAPPED") == "1":
        return  # already tried; main() will fall back to proportional
    candidates = []
    env_venv = os.environ.get("CLAY_AD_VENV")
    if env_venv:
        candidates.append(os.path.join(env_venv, "bin", "python"))
    candidates.append(os.path.expanduser("~/.cache/pm-agent/whisper-venv/bin/python"))
    here = os.path.abspath(__file__)
    for py in candidates:
        if not os.path.exists(py):
            continue
        # A venv's bin/python is a symlink to the base interpreter, so comparing the
        # binary realpath against sys.executable wrongly says "same interpreter" and
        # skips the re-exec. Compare the environment ROOT (sys.prefix) instead: if we
        # are not already inside this venv, re-exec into it.
        venv_root = os.path.dirname(os.path.dirname(py))
        if os.path.realpath(venv_root) == os.path.realpath(sys.prefix):
            continue  # already running inside this venv
        os.environ["CLAY_AD_BOOTSTRAPPED"] = "1"
        try:
            os.execv(py, [py, here] + sys.argv[1:])
        except Exception:
            continue


def audio_duration(path):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nokey=1:noprint_wrappers=1", path],
            stderr=subprocess.STDOUT)
    except Exception as exc:
        die("ffprobe could not read '%s' (%s). Is it an audio/video file?" % (path, exc))
    try:
        return float(out.decode("utf-8", "replace").strip())
    except ValueError:
        die("ffprobe returned no duration for '%s'." % path)


def load_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        die("transcript not found: " + path)
    except json.JSONDecodeError as exc:
        die("transcript is not valid JSON: " + str(exc))
    raw = data.get("lines") if isinstance(data, dict) else None
    if not isinstance(raw, list) or not raw:
        die("transcript.json needs a non-empty 'lines' array")
    lines = []
    for i, ln in enumerate(raw):
        if not isinstance(ln, dict):
            die("lines[%d] is not an object" % i)
        vo = ln.get("vo")
        if vo is None:
            vo = ln.get("text")
        vo = (vo or "").strip()
        if not vo:
            die("lines[%d] has an empty 'vo'" % i)
        lines.append({
            "id": str(ln.get("id") or ("l%02d" % (i + 1))),
            "role": str(ln.get("role") or ""),
            "vo": vo,
        })
    return data, lines


# --- whisper word stream -----------------------------------------------------
def whisper_words(audio, model_name):
    """Return [(token, start, end), ...] for every recognized word, or None if
    faster-whisper is unavailable / produced nothing."""
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return None
    try:
        import warnings
        warnings.filterwarnings("ignore")  # silence benign numpy matmul RuntimeWarnings
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        segments, _info = model.transcribe(
            audio, word_timestamps=True, language="en", vad_filter=True)
        words = []
        for seg in segments:
            for w in (getattr(seg, "words", None) or []):
                raw = (getattr(w, "word", "") or "").strip()
                wt = toks(raw)
                if not wt:
                    continue
                words.append({"word": raw, "tok": wt[0],
                              "start": float(w.start), "end": float(w.end)})
        return words or None
    except Exception as exc:
        sys.stderr.write("WARN: whisper failed (%s); using proportional fallback.\n" % exc)
        return None


# --- boundaries --------------------------------------------------------------
def line_boundaries_whisper(lines, words, total):
    """Start time of each line's first word -> contiguous boundaries [0..total]."""
    flatT, T = [], []
    for i, ln in enumerate(lines):
        for t in toks(ln["vo"]):
            flatT.append(i)
            T.append(t)
    R = [w["tok"] for w in words]
    if not T or not R:
        return None
    sm = difflib.SequenceMatcher(None, T, R, autojunk=False)
    map_t2r = [None] * len(T)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                map_t2r[i1 + k] = j1 + k

    firsts = [None] * len(lines)
    for idx, li in enumerate(flatT):
        if firsts[li] is None:
            firsts[li] = idx

    def mapped_start(i):
        lo = firsts[i]
        hi = firsts[i + 1] if (i + 1 < len(lines) and firsts[i + 1] is not None) else len(T)
        if lo is None:
            return None
        cands = [words[map_t2r[k]]["start"] for k in range(lo, hi) if map_t2r[k] is not None]
        return min(cands) if cands else None

    n = len(lines)
    wc = [max(1, len(toks(ln["vo"]))) for ln in lines]
    cum = [0]
    for w in wc:
        cum.append(cum[-1] + w)

    # boundary[i] for i in 0..n ; boundary[0]=0, boundary[n]=total
    b = [None] * (n + 1)
    b[0] = 0.0
    b[n] = total
    for i in range(1, n):
        b[i] = mapped_start(i)

    known = [(i, b[i]) for i in range(n + 1) if b[i] is not None]

    def interp(i):
        x = cum[i]
        left = right = None
        for ki, kt in known:
            if ki <= i:
                left = (ki, kt)
            if ki >= i and right is None:
                right = (ki, kt)
        if left and right and left[0] != right[0]:
            x0, t0 = cum[left[0]], left[1]
            x1, t1 = cum[right[0]], right[1]
            return t0 if x1 == x0 else t0 + (t1 - t0) * (x - x0) / (x1 - x0)
        return left[1] if left else (right[1] if right else 0.0)

    for i in range(n + 1):
        if b[i] is None:
            b[i] = interp(i)

    # clamp into [0,total], force non-decreasing, pin the ends
    b = [min(max(x, 0.0), total) for x in b]
    for i in range(1, n + 1):
        if b[i] < b[i - 1]:
            b[i] = b[i - 1]
    b[0], b[n] = 0.0, total
    return b


def line_boundaries_proportional(lines, total):
    n = len(lines)
    wc = [max(1, len(toks(ln["vo"]))) for ln in lines]
    cum = [0]
    for w in wc:
        cum.append(cum[-1] + w)
    totw = cum[-1]
    return [round(total * cum[i] / totw, 6) for i in range(n + 1)]


def main(argv=None):
    bootstrap_into_venv()
    p = argparse.ArgumentParser(prog="align_vo.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("transcript")
    p.add_argument("audio")
    p.add_argument("out_timing")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--proportional", action="store_true",
                   help="skip whisper, split by word count")
    args = p.parse_args(argv)

    if not os.path.exists(args.audio):
        die("audio file not found: " + args.audio)

    data, lines = load_lines(args.transcript)
    total = audio_duration(args.audio)
    if total <= 0:
        die("audio duration is zero")

    method = "proportional"
    b = None
    words = None
    if not args.proportional:
        words = whisper_words(args.audio, args.model)
        if words:
            b = line_boundaries_whisper(lines, words, total)
            if b is not None:
                method = "whisper-aligned"
    if b is None:
        b = line_boundaries_proportional(lines, total)

    out_lines = []
    for i, ln in enumerate(lines):
        start, end = round(b[i], 3), round(b[i + 1], 3)
        out_lines.append({
            "id": ln["id"], "role": ln["role"], "vo": ln["vo"],
            "start": start, "end": end, "dur": round(end - start, 3),
            "word_count": len(toks(ln["vo"])),
        })

    out = {
        "audio_file": args.audio,
        "total_seconds": round(total, 3),
        "method": method,
        "model": args.model if method == "whisper-aligned" else None,
        "concept": data.get("concept") if isinstance(data, dict) else None,
        "lines": out_lines,
        "words": ([{"word": w["word"], "start": round(w["start"], 3), "end": round(w["end"], 3)}
                   for w in words] if (method == "whisper-aligned" and words) else []),
    }
    try:
        with open(args.out_timing, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        die("could not write " + args.out_timing + ": " + str(exc), 1)

    w = sys.stderr.write
    w("\n=== VO TIMING (%s, total %.2fs) ===\n" % (method, total))
    w("line  role        start    end    dur   words  vo\n")
    for ol in out_lines:
        w("%-5s %-10s %6.2f %6.2f %5.2f  %4d   %s\n" % (
            ol["id"], ol["role"][:10], ol["start"], ol["end"], ol["dur"],
            ol["word_count"], (ol["vo"][:48] + ("…" if len(ol["vo"]) > 48 else ""))))
    w("wrote %s\n" % args.out_timing)
    if method == "proportional":
        w("NOTE: proportional fallback (whisper unavailable). Per-line timing is "
          "approximate; install faster-whisper for true sync.\n")
    w("====================================\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
