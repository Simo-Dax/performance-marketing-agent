#!/usr/bin/env python3
"""
dialogue_check.py - whisper-verify a rendered dialogue clip against its script line.

THE LAW THIS SERVES (member hard rule 3): in the talking-object factory the voice is
baked into the pixels — Seedance generates the character's speech WITH the picture. If
the rendered character speaks the wrong words, no edit can fix it: a failed check means
a RE-RENDER (with its own fresh member yes). This is the one place in the plugin family
where re-render replaces re-cut. Timing/visual problems stay edit-side as always.

WHAT IT DOES
  1. Extracts the clip's audio (ffmpeg -> 16k mono wav). A dialogue clip with NO audio
     stream is an automatic FAIL — it rendered without its voice.
  2. Transcribes with faster-whisper (word timestamps), self-bootstrapping into the
     shared venv (~/.cache/pm-agent/whisper-venv) exactly like the family's align tool.
  3. Aligns the EXPECTED line's tokens onto the recognized stream (difflib) after a
     light canonicalization (digit/letter splits, % -> percent, small number words) so
     "3pm" vs "3 pm" or "70%" vs "seventy percent" don't false-fail.
  4. Verdict:
       PASS    match_ratio >= 0.85 AND no more than one missing CONTENT word
               (a content word is 4+ letters — dropped articles and whisper mishears
               don't kill a good take). THE ORCHESTRATOR STILL READS missing_words:
               if the one tolerated miss is load-bearing (the claim verb, the "may
               help" hedge, the offer), treat the clip as a FAIL and re-render.
       FAIL    the line is wrong -> re-render
       SKIPPED whisper unavailable -> verify by ear before accepting the clip
  5. Reports speech_start / speech_end (the recognized words' bounds) — set the scene's
     trim_out to speech_end + 0.3-0.6s so dead tail air never pads the ad.

USAGE
  dialogue_check.py <clip.mp4> <scenes.json> <scene_id> <out_report.json> [--model base.en]
  dialogue_check.py <clip.mp4> <out_report.json> --text "<expected line>" [--model base.en]

OUTPUT (out_report.json)
  { "scene_id", "clip", "verdict": "PASS|FAIL|SKIPPED", "match_ratio",
    "expected", "transcript", "missing_words", "extra_words",
    "speech_start", "speech_end", "clip_seconds", "words":[{word,start,end}] }

Exit 0 on PASS or SKIPPED, 3 on FAIL (re-render needed), 2 on bad input.
"""

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

DEFAULT_MODEL = os.environ.get("CLAY_AD_WHISPER_MODEL", "base.en")
PASS_RATIO = 0.85
_TOK = re.compile(r"[a-z0-9']+")

_NUM_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "twenty": "20", "thirty": "30", "forty": "40",
    "fifty": "50", "sixty": "60", "seventy": "70", "eighty": "80", "ninety": "90",
}


def die(msg, code=2):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(code)


def canon(text):
    """Canonical token stream: lowercase, digit/letter splits ('3pm' -> '3 pm'),
    % -> percent, small number words -> digits, possessives kept."""
    t = str(text).lower().replace("%", " percent ")
    t = re.sub(r"(\d)([a-z])", r"\1 \2", t)
    t = re.sub(r"([a-z])(\d)", r"\1 \2", t)
    toks = _TOK.findall(t)
    return [_NUM_WORDS.get(tok, tok) for tok in toks]


# --- self-bootstrap into the shared whisper venv (family pattern) -------------
def bootstrap_into_venv():
    try:
        import faster_whisper  # noqa: F401
        return
    except Exception:
        pass
    if os.environ.get("CLAY_AD_BOOTSTRAPPED") == "1":
        return  # already tried; main() reports SKIPPED
    candidates = []
    env_venv = os.environ.get("CLAY_AD_VENV")
    if env_venv:
        candidates.append(os.path.join(env_venv, "bin", "python"))
    candidates.append(os.path.expanduser("~/.cache/pm-agent/whisper-venv/bin/python"))
    here = os.path.abspath(__file__)
    for py in candidates:
        if not os.path.exists(py):
            continue
        venv_root = os.path.dirname(os.path.dirname(py))
        if os.path.realpath(venv_root) == os.path.realpath(sys.prefix):
            continue  # already inside this venv
        os.environ["CLAY_AD_BOOTSTRAPPED"] = "1"
        try:
            os.execv(py, [py, here] + sys.argv[1:])
        except Exception:
            continue


def has_audio_stream(clip):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=codec_type",
             "-of", "default=nw=1:nk=1", clip], stderr=subprocess.STDOUT)
        return out.decode("utf-8", "replace").strip() == "audio"
    except Exception:
        return False


def clip_duration(clip):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nokey=1:noprint_wrappers=1", clip],
            stderr=subprocess.STDOUT)
        return float(out.decode("utf-8", "replace").strip())
    except Exception:
        return None


def extract_wav(clip):
    fd, wav = tempfile.mkstemp(suffix=".wav", prefix="dlgchk.")
    os.close(fd)
    try:
        subprocess.check_output(
            ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", clip,
             "-vn", "-ac", "1", "-ar", "16000", wav], stderr=subprocess.STDOUT)
        return wav
    except Exception as exc:
        try:
            os.unlink(wav)
        except OSError:
            pass
        die("could not extract audio from '%s' (%s)" % (clip, exc))


def whisper_words(wav, model_name):
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return None
    try:
        import warnings
        warnings.filterwarnings("ignore")
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        segments, _info = model.transcribe(
            wav, word_timestamps=True, language="en", vad_filter=True)
        words = []
        for seg in segments:
            for w in (getattr(seg, "words", None) or []):
                raw = (getattr(w, "word", "") or "").strip()
                if not _TOK.findall(raw.lower()):
                    continue
                words.append({"word": raw,
                              "start": round(float(w.start), 3),
                              "end": round(float(w.end), 3)})
        return words
    except Exception as exc:
        sys.stderr.write("WARN: whisper failed (%s)\n" % exc)
        return None


def main(argv=None):
    bootstrap_into_venv()
    ap = argparse.ArgumentParser(prog="dialogue_check.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip")
    ap.add_argument("rest", nargs="+",
                    help="scenes.json scene_id out_report — or just out_report with "
                         "--text")
    ap.add_argument("--text", default=None,
                    help="expected line given directly (skips scenes.json lookup)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args(argv)

    if not os.path.exists(args.clip):
        die("clip not found: " + args.clip)

    # resolve the expected line + the report path (two legal shapes)
    if args.text is not None:
        if len(args.rest) not in (1, 2):
            die('with --text give just the report path: dialogue_check.py <clip.mp4> '
                '<out_report.json> --text "<expected line>"')
        out_report = args.rest[-1]
        expected = args.text.strip()
        scene_id = os.path.splitext(os.path.basename(args.clip))[0]
    else:
        if len(args.rest) != 3:
            die('give scenes.json, a scene_id, and the report path — or use --text '
                '"<expected line>"')
        scenes_path, scene_id, out_report = args.rest
        try:
            with open(scenes_path, "r", encoding="utf-8") as fh:
                scenes = json.load(fh)
        except FileNotFoundError:
            die("scenes file not found: " + scenes_path)
        except json.JSONDecodeError as exc:
            die("scenes file is not valid JSON: %s" % exc)
        match = None
        for s in (scenes.get("scenes") or []):
            if str(s.get("scene_id")) == scene_id:
                match = s
                break
        if match is None:
            die("scene '%s' not found in %s" % (scene_id, scenes_path))
        expected = str(match.get("dialogue") or "").strip()
    if not expected:
        die("the expected line is empty — every talking-object scene has dialogue")

    report = {
        "scene_id": scene_id, "clip": args.clip, "verdict": None,
        "match_ratio": None, "expected": expected, "transcript": "",
        "missing_words": [], "extra_words": [],
        "speech_start": None, "speech_end": None,
        "clip_seconds": clip_duration(args.clip), "words": [],
    }

    def emit(code):
        try:
            with open(out_report, "w", encoding="utf-8") as fh:
                json.dump(report, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        except OSError as exc:
            die("could not write %s: %s" % (out_report, exc), 1)
        w = sys.stderr.write
        w("\n=== DIALOGUE CHECK (%s) — %s ===\n" % (scene_id, report["verdict"]))
        w("expected:   %s\n" % expected)
        w("heard:      %s\n" % (report["transcript"] or "(nothing)"))
        if report["match_ratio"] is not None:
            w("match:      %.2f   missing: %s   extra: %s\n"
              % (report["match_ratio"],
                 ", ".join(report["missing_words"]) or "-",
                 ", ".join(report["extra_words"]) or "-"))
        if report["speech_end"] is not None:
            w("speech:     %.2fs -> %.2fs  (set trim_out ≈ %.2fs; clip runs %.2fs)\n"
              % (report["speech_start"], report["speech_end"],
                 report["speech_end"] + 0.4, report["clip_seconds"] or -1))
        if report["verdict"] == "FAIL":
            w("VERDICT: FAIL — the rendered line is wrong. The voice is baked into the "
              "pixels: this clip needs a RE-RENDER (member hard rule 3), with its own "
              "fresh yes.\n")
        elif report["verdict"] == "SKIPPED":
            w("VERDICT: SKIPPED — whisper unavailable. Verify the line BY EAR before "
              "accepting this clip; do not skip the check silently.\n")
        w("wrote %s\n==============================================\n\n"
          % out_report)
        return code

    if not has_audio_stream(args.clip):
        report["verdict"] = "FAIL"
        report["transcript"] = ""
        report["missing_words"] = canon(expected)
        sys.stderr.write("ERROR: clip has NO AUDIO STREAM — a dialogue clip must render "
                         "with its voice baked in.\n")
        return emit(3)

    wav = extract_wav(args.clip)
    try:
        words = whisper_words(wav, args.model)
    finally:
        try:
            os.unlink(wav)
        except OSError:
            pass

    if words is None:
        report["verdict"] = "SKIPPED"
        return emit(0)
    if not words:
        report["verdict"] = "FAIL"
        report["missing_words"] = canon(expected)
        sys.stderr.write("ERROR: whisper heard no speech in the clip.\n")
        return emit(3)

    report["words"] = words
    report["transcript"] = " ".join(w["word"] for w in words)
    report["speech_start"] = words[0]["start"]
    report["speech_end"] = words[-1]["end"]

    exp = canon(expected)
    rec = []
    for w in words:
        rec.extend(canon(w["word"]))
    sm = difflib.SequenceMatcher(None, exp, rec, autojunk=False)
    ratio = sm.ratio()
    matched_exp = set()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            matched_exp.update(range(i1, i2))
    missing = [exp[i] for i in range(len(exp)) if i not in matched_exp]
    rec_set = set(rec)
    # a "missing" token that still appears somewhere in the recognition is a mere
    # ordering blip, not a dropped word
    missing = [m for m in missing if m not in rec_set]
    exp_set = set(exp)
    extra = [t for t in rec if t not in exp_set]

    report["match_ratio"] = round(ratio, 3)
    report["missing_words"] = missing
    report["extra_words"] = extra[:12]

    missing_content = [m for m in missing if len(m) >= 4]
    if ratio >= PASS_RATIO and len(missing_content) <= 1:
        report["verdict"] = "PASS"
        return emit(0)
    report["verdict"] = "FAIL"
    return emit(3)


if __name__ == "__main__":
    sys.exit(main())
