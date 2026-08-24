#!/usr/bin/env python3
"""Auto Captions — burn house-style captions onto any finished video.

    autocaption.py <video> [<video> ...] [options]

    --script PATH   transcript.json / timing.json / .txt to force-align against
    --out DIR       where to write (default: <video dir>/../out, else alongside)
    --model NAME    whisper model (default: medium)
    --dry-run       print the cards and the audit, render nothing
    --no-align      ignore any script and caption straight from the transcription

WHY FORCE-ALIGNMENT: speech recognition is good at WHEN a word was said and only
approximate about WHICH word it was. When the real script is available, this uses
whisper purely for timing and takes every word from the script, so the burned
captions match the copy exactly instead of approximately.

Script auto-discovery: for a video inside an the agent concept folder, the script
is looked up at ../transcript.json, ./transcript.json, ../timing.json and the
sibling out/ and audio/ folders, so the ad skills need no wiring.
"""
import argparse, difflib, json, os, pathlib, re, subprocess, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import caption_lib as CL

# Shared whisper venv, same one the other video skills build. First that exists wins.
_VENVS = ["~/.cache/pm-agent/whisper-venv", "~/.cache/pm-agent/whisper"]
WHISPER_VENV = next(
    (pathlib.Path(v).expanduser() for v in _VENVS if pathlib.Path(v).expanduser().exists()),
    pathlib.Path(_VENVS[0]).expanduser())


def die(msg, code=2):
    sys.stderr.write("ERROR: %s\n" % msg); sys.exit(code)


def ensure_whisper():
    """Re-exec inside the shared whisper venv if faster_whisper isn't importable."""
    try:
        import faster_whisper  # noqa: F401
        return
    except ImportError:
        pass
    # POSIX puts the interpreter in bin/, Windows in Scripts/. Try both rather
    # than assuming, so this works wherever the agent is installed.
    for rel in (("bin", "python"), ("Scripts", "python.exe")):
        py = WHISPER_VENV.joinpath(*rel)
        if py.exists() and os.environ.get("_AC_REEXEC") != "1":
            os.environ["_AC_REEXEC"] = "1"
            os.execv(str(py), [str(py), os.path.abspath(__file__)] + sys.argv[1:])
    sub = "Scripts\\python.exe" if os.name == "nt" else "bin/python"
    die("faster-whisper is not installed.\n"
        "  python3 -m venv %s && %s%s%s -m pip install faster-whisper"
        % (WHISPER_VENV, WHISPER_VENV, os.sep, sub))


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x",
                          str(path)], capture_output=True, text=True).stdout.strip()
    try:
        w, h = (int(x) for x in out.split("x")[:2])
        return w, h
    except Exception:
        die("could not read video dimensions: %s" % path)


def norm(tok):
    return re.sub(r"[^a-z0-9]", "", str(tok).lower())


def load_script(path):
    """transcript.json (lines[].vo) | timing.json (lines[].vo) | plain text."""
    p = pathlib.Path(path)
    if not p.exists():
        return None
    if p.suffix.lower() == ".json":
        try:
            d = json.load(open(p))
        except Exception:
            return None
        lines = d.get("lines")
        if isinstance(lines, list) and lines:
            txt = " ".join(str(l.get("vo", "")).strip() for l in lines)
            return " ".join(txt.split()) or None
        if isinstance(d.get("transcript"), str):
            return " ".join(d["transcript"].split()) or None
        return None
    return " ".join(p.read_text(errors="ignore").split()) or None


def discover_script(video):
    v = pathlib.Path(video).resolve()
    for cand in [v.parent / "transcript.json", v.parent.parent / "transcript.json",
                 v.parent / "timing.json", v.parent.parent / "timing.json",
                 v.parent.parent / "audio" / "transcript.json"]:
        s = load_script(cand)
        if s:
            return s, cand
    return None, None


def align(script_words, asr):
    """Every SCRIPT word gets a (start, end): borrowed where whisper agrees,
    interpolated across the surrounding anchors where it doesn't."""
    S = [norm(w) for w in script_words]
    A = [norm(w["word"]) for w in asr]
    times = [None] * len(S)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, S, A,
                                                       autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                a = asr[j1 + k]
                times[i1 + k] = (float(a["start"]), float(a["end"]))
    n, i = len(times), 0
    while i < n:
        if times[i] is not None:
            i += 1; continue
        j = i
        while j < n and times[j] is None:
            j += 1
        lo = times[i - 1][1] if i > 0 else (float(asr[0]["start"]) if asr else 0.0)
        hi = times[j][0] if j < n else (float(asr[-1]["end"]) if asr else lo + 1.0)
        if hi <= lo:
            hi = lo + 0.25 * (j - i)
        step = (hi - lo) / max(1, j - i)
        for k in range(i, j):
            times[k] = (lo + step * (k - i), lo + step * (k - i + 1))
        i = j
    return times


def audit(chunks, script):
    sizes = [len(c["text"].split()) for c in chunks]
    n = len(sizes) or 1
    in_target = sum(1 for s in sizes if s in CL.TARGET_WORDS)
    wide = [c["text"] for c in chunks if CL.line_px(c["text"]) > CL.MAX_LINE_PX]
    punct = [c["text"] for c in chunks if re.search(r"[.,!?;:]", c["text"])]
    over = [c["text"] for c in chunks if len(c["text"].split()) > CL.MAX_WORDS]
    exact = None
    if script:
        def flat(t):
            t = t.lower().replace("a.m.", "am").replace("p.m.", "pm")
            return re.sub(r"[^a-z0-9 ]", " ", t).split()
        exact = flat(" ".join(c["text"] for c in chunks)) == flat(script)
    return {"cards": len(chunks), "pct_2_3": round(100.0 * in_target / n, 1),
            "two_row": wide, "punctuation": punct, "over_max": over,
            "matches_script": exact}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--script"); ap.add_argument("--out")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-align", action="store_true")
    ap.add_argument("--brand-vocab", default=None,
                    help="JSON with this campaign's brand_names / proper_nouns / fixes. "
                         "Defaults to context/brand/caption_vocab.json when present.")
    a = ap.parse_args()

    vocab = a.brand_vocab
    if vocab is None:
        for cand in ("context/brand/caption_vocab.json",
                     os.path.join(os.path.expanduser("~"), ".config", "pm-agent",
                                  "caption_vocab.json")):
            if os.path.isfile(cand):
                vocab = cand; break
    if vocab:
        n = CL.load_brand_vocab(vocab)
        print("brand vocab: %d entries from %s" % (n, vocab), flush=True)

    ensure_whisper()
    from faster_whisper import WhisperModel

    print("loading whisper (%s)..." % a.model, flush=True)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    rc_all = 0

    for vp in a.videos:
        src = pathlib.Path(vp).resolve()
        if not src.exists():
            print("!! missing: %s" % src); rc_all = 1; continue
        t0 = time.time()
        vw, vh = probe(src)
        outdir = pathlib.Path(a.out) if a.out else (
            src.parent.parent / "out" if (src.parent.parent / "out").is_dir() else src.parent)
        outdir.mkdir(parents=True, exist_ok=True)
        tmp = outdir / "_captmp" / src.stem
        tmp.mkdir(parents=True, exist_ok=True)

        script, spath = (None, None)
        if not a.no_align:
            script = load_script(a.script) if a.script else None
            spath = a.script if script else None
            if not script:
                script, spath = discover_script(src)

        wav = tmp / "audio.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn",
                        "-ac", "1", "-ar", "16000", str(wav)], check=True)
        segs, _ = model.transcribe(str(wav), word_timestamps=True, vad_filter=True,
                                   language="en")
        asr = [{"word": w.word.strip(), "start": float(w.start), "end": float(w.end)}
               for s in segs for w in (s.words or []) if w.word.strip()]
        if not asr:
            print("!! no speech in %s, skipped" % src.name); rc_all = 1; continue

        if script:
            sw = script.split()
            words = [{"word": w, "start": t[0], "end": t[1]}
                     for w, t in zip(sw, align(sw, asr))]
            sim = difflib.SequenceMatcher(None, [norm(w) for w in sw],
                                          [norm(x["word"]) for x in asr]).ratio()
            mode = "script-aligned (%s, asr agreement %.3f)" % (
                pathlib.Path(spath).name if spath else "given", sim)
        else:
            words = asr
            mode = "transcription only (no script found)"

        chunks = CL.build_chunks(words)
        rep = audit(chunks, script)
        print("\n=== %s  (%dx%d) ===" % (src.name, vw, vh))
        print("  %s" % mode)
        if CL.FONT_NAME != CL.FONT_PATH:
            print("  FONT: locked face unavailable on this machine, rendered in %s" % CL.FONT_NAME)
        print("  %d cards | %.1f%% at 2-3 words | two-row: %s | punctuation: %s | script match: %s"
              % (rep["cards"], rep["pct_2_3"], rep["two_row"] or "none",
                 rep["punctuation"] or "none", rep["matches_script"]))

        if a.dry_run:
            for c in chunks:
                print("   %6.2f-%6.2f  (%d) %s"
                      % (c["start"], c["end"], len(c["text"].split()), c["text"]))
            continue

        CL.render_cards(chunks, tmp / "cards", vw, vh)
        dst = outdir / (src.stem + "_captioned.mp4")
        rc = CL.composite(src, chunks, tmp / "cards", dst)
        rc_all |= rc
        json.dump({"video": src.name, "res": "%dx%d" % (vw, vh), "mode": mode,
                   "script": script, "words": words, "cards": chunks, "audit": rep},
                  open(outdir / (src.stem + ".captions.json"), "w"), indent=2)
        print("  -> %s  (%.0fs, rc=%d)" % (dst.name, time.time() - t0, rc))

        for f in (tmp / "cards").glob("*.png"):
            f.unlink()
        wav.unlink(missing_ok=True)
        try:
            (tmp / "cards").rmdir(); tmp.rmdir(); (outdir / "_captmp").rmdir()
        except OSError:
            pass

    sys.exit(1 if rc_all else 0)


if __name__ == "__main__":
    main()
