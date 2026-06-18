#!/usr/bin/env python3
"""
segment_script.py - the pacing engine of the Seedance 2.0 UGC factory.

THE MODEL (fast, punchy, sub-10s generations). Read this before changing anything.

Seedance 2.0 STRETCHES the spoken line to fill the duration you request, so the
duration you choose IS the talking speed. There is no clipping to protect against,
so there is NO "fill / breath buffer" (that old idea just made delivery DRAG).
Instead we target a pace directly:

    requested_seconds = round(word_count / WPS)        WPS = 3.5 (fast, punchy UGC)
    pace_wps          = word_count / requested_seconds

EVERY generation must be UNDER 10 seconds (integer 4..9). A longer body is split
into more, shorter generations. Action seconds for a hook's visual move (a dump,
a slam, a toss) are added OUTSIDE this tool when you set the hook reel's seconds.

This script splits the body into shots where:
  1. Every shot is a whole number of complete sentences (never mid-thought).
  2. Every shot's seconds = round(words / 3.5) and lands UNDER 10s at a pace in
     the band [2.4, 4.0] wps (below drags, above rushes).
  3. No content is dropped (an explicit word-accounting assert guards this).

PACKING: greedily add whole sentences to a shot while the packed word count still
fits one sub-10s generation at the target pace, i.e. while packed_words <=
floor(MAX_SECONDS * WPS) (= 9 * 3.5 = 31 words). When the next sentence would
exceed that, close the shot and start a new one. A single sentence longer than
that ceiling is clause-split; if it cannot be split it is clamped and flagged.

NOTE: body beats should each be segmented as their OWN generation (one beat per
call) so the greedy packer never merges the CTA's first sentence onto the proof
beat. Pass one beat at a time when you need strict one-beat-per-clip mapping.

Usage:
  python3 segment_script.py beat_sheet.json out_shots.json
      [--wps 3.5] [--min-seconds 4] [--max-seconds 9]
      [--pace-low 2.4] [--pace-high 4.0] [--shot-prefix body_shot]

Input beat_sheet.json:
  {"framework": "...", "beats": [
     {"beat_name": "...", "vo_line": "...", "on_screen_text": "", "broll_note": ""}, ...]}

Output out_shots.json:
  {"framework": "...", "n_shots": N, "total_seconds": T,
   "shots": [ {"shot_id", "beat_names", "vo_text", "words", "word_count",
               "requested_seconds", "seconds", "pace_wps", "on_screen_text",
               "broll_note", "needs_trim"} ]}

Exit codes: 0 ok, 2 bad input, 3 plan written but at least one shot is flagged
(pace out of band, or it could not be kept under 10s) so a caller can react.
"""

import argparse
import json
import math
import re
import sys

DEFAULT_WPS = 3.5          # fast, punchy UGC pace (house default)
MIN_SECONDS = 4            # Seedance per-generation floor
MAX_SECONDS = 9            # UNDER 10 seconds, hard rule for this factory
PACE_LOW = 2.4             # below this the shot drags (short lines clamped to the 4s floor are exempt in practice)
PACE_HIGH = 4.0            # above this the shot rushes / risks skipping

_CLAUSE_RE = re.compile(r"(?<=,)\s+|(?<=;)\s+|\s+(?=and\s)|\s+(?=but\s)|\s+(?=so\s)", re.I)


class BeatSheetError(Exception):
    """Malformed input so main() can exit cleanly with a message."""


def _word_count(text):
    return len(text.split())


def _max_words(wps, max_s):
    """Most words that fit one sub-10s generation at the target pace."""
    return int(math.floor(max_s * wps + 1e-9))


def _choose_duration(word_count, wps, min_s, max_s):
    """Integer seconds = round(words / wps), clamped to [min_s, max_s] (4..9)."""
    if word_count <= 0:
        return min_s
    d = int(round(word_count / wps))
    if d < min_s:
        d = min_s
    if d > max_s:
        d = max_s
    return d


def _pace(word_count, seconds):
    return word_count / seconds if seconds > 0 else 0.0


def _split_sentences(text):
    """Split on . ? ! keeping the terminator; never returns an empty fragment."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _split_long_sentence(sentence, max_words):
    """A single sentence over the per-generation word ceiling. Try clause splits.
    Returns a list of chunks; [sentence] unchanged if no clean break (caller flags)."""
    if _word_count(sentence) <= max_words:
        return [sentence]
    pieces = [p.strip() for p in _CLAUSE_RE.split(sentence) if p.strip()]
    if len(pieces) <= 1:
        return [sentence]
    chunks, cur = [], ""
    for piece in pieces:
        cand = (cur + " " + piece).strip() if cur else piece
        if _word_count(cand) <= max_words:
            cur = cand
        else:
            if cur:
                chunks.append(cur)
            cur = piece
    if cur:
        chunks.append(cur)
    return chunks


def _normalize_beats(raw):
    if not isinstance(raw, dict):
        raise BeatSheetError("top level must be a JSON object with a 'beats' array")
    beats = raw.get("beats")
    if not isinstance(beats, list) or not beats:
        raise BeatSheetError("'beats' must be a non-empty array")
    clean = []
    for idx, b in enumerate(beats):
        if not isinstance(b, dict):
            raise BeatSheetError("beat %d is not an object" % idx)
        vo = b.get("vo_line")
        vo = "" if vo is None else (vo if isinstance(vo, str) else str(vo))
        vo = vo.strip()
        clean.append({
            "beat_name": str(b.get("beat_name") or "beat_%d" % idx),
            "vo_line": vo,
            "on_screen_text": str(b.get("on_screen_text") or ""),
            "broll_note": str(b.get("broll_note") or ""),
        })
    return clean


def _rebalance_drags(shots, wps, min_s, max_s, max_words):
    """One pass: cure a DRAGS shot (pace below PACE_LOW, e.g. a short line clamped
    up to the 4s floor) by merging it with its smaller-word neighbour when the
    combined shot still fits under 10s. A short shot wedged between two near-max
    shots stays flagged so the exit code catches it."""
    def words(s):
        return _word_count(" ".join(u["text"] for u in s))

    def pace(s):
        wc = words(s)
        return _pace(wc, _choose_duration(wc, wps, min_s, max_s))

    changed = True
    while changed and len(shots) > 1:
        changed = False
        for i, s in enumerate(shots):
            if pace(s) >= PACE_LOW:
                continue
            neighbours = []
            if i - 1 >= 0:
                neighbours.append((words(shots[i - 1]), i - 1))
            if i + 1 < len(shots):
                neighbours.append((words(shots[i + 1]), i + 1))
            neighbours.sort()
            for _, j in neighbours:
                if words(s) + words(shots[j]) <= max_words:
                    a, b = (j, i) if j < i else (i, j)
                    shots[a] = shots[a] + shots[b]
                    del shots[b]
                    changed = True
                    break
            if changed:
                break
    return shots


def segment(beats, wps, min_s, max_s, shot_prefix="body_shot"):
    max_words = _max_words(wps, max_s)

    units = []
    for b in beats:
        if not b["vo_line"]:
            continue
        for sent in _split_sentences(b["vo_line"]):
            for chunk in _split_long_sentence(sent, max_words):
                units.append({
                    "text": chunk,
                    "beat_name": b["beat_name"],
                    "on_screen_text": b["on_screen_text"],
                    "broll_note": b["broll_note"],
                })
    if not units:
        raise BeatSheetError("no spoken lines found in any beat (all vo_line empty)")

    # Greedily pack whole sentences while the shot stays under 10s at the pace.
    shots, cur = [], []
    for u in units:
        cand = cur + [u]
        wc = _word_count(" ".join(x["text"] for x in cand))
        if cur and wc > max_words:
            shots.append(cur)
            cur = [u]
        else:
            cur = cand
    if cur:
        shots.append(cur)

    shots = _rebalance_drags(shots, wps, min_s, max_s, max_words)

    out_shots = []
    for i, units_in_shot in enumerate(shots, 1):
        vo_text = " ".join(x["text"] for x in units_in_shot).strip()
        wc = _word_count(vo_text)
        dur = _choose_duration(wc, wps, min_s, max_s)
        pace = _pace(wc, dur)
        needs_trim = (dur >= 10) or (pace < PACE_LOW) or (pace > PACE_HIGH)
        osts = [x["on_screen_text"] for x in units_in_shot if x["on_screen_text"]]
        brolls = [x["broll_note"] for x in units_in_shot if x["broll_note"]]
        beat_names = []
        for x in units_in_shot:
            if x["beat_name"] not in beat_names:
                beat_names.append(x["beat_name"])
        out_shots.append({
            "shot_id": "%s_%02d" % (shot_prefix, i),
            "beat_names": beat_names,
            "vo_text": vo_text,
            "words": vo_text,                 # alias build_manifest.py reads
            "word_count": wc,
            "requested_seconds": dur,
            "seconds": dur,                   # alias build_manifest.py reads
            "pace_wps": round(pace, 2),
            "on_screen_text": " | ".join(dict.fromkeys(osts)),
            "broll_note": " | ".join(dict.fromkeys(brolls)),
            "needs_trim": needs_trim,
        })

    in_words = sum(_word_count(u["text"]) for u in units)
    out_words = sum(s["word_count"] for s in out_shots)
    if in_words != out_words:
        raise BeatSheetError(
            "INTERNAL: word accounting mismatch, input %d != output %d."
            % (in_words, out_words))

    return {
        "shots": out_shots,
        "n_shots": len(out_shots),
        "total_seconds": sum(s["requested_seconds"] for s in out_shots),
    }


def _print_table(payload, args):
    w = sys.stderr.write
    w("\n=== PACING TABLE (framework: %s) ===\n" % (payload.get("framework") or "n/a"))
    w("shot            words  sec   wps    status\n")
    for s in payload["shots"]:
        if s["requested_seconds"] >= 10:
            status = "OVER 10s, split the line into more shots"
        elif s["pace_wps"] > PACE_HIGH:
            status = "RUSHES, shorten the line or split it"
        elif s["pace_wps"] < PACE_LOW:
            status = "DRAGS, lengthen the line or merge with a neighbour"
        else:
            status = "OK"
        w("%-15s %5d  %3d   %.2f   %s\n"
          % (s["shot_id"], s["word_count"], s["requested_seconds"], s["pace_wps"], status))
    w("total render seconds: %d across %d shots\n"
      % (payload["total_seconds"], payload["n_shots"]))
    flagged = [s["shot_id"] for s in payload["shots"] if s["needs_trim"]]
    if flagged:
        w("FLAGGED (fix before generating): %s\n" % ", ".join(flagged))
    w("target pace %.1f wps, band %.1f to %.1f, every shot must be under 10s\n"
      % (args.wps, PACE_LOW, PACE_HIGH))
    w("=====================================\n\n")


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="segment_script.py",
        description="Pace a UGC body beat sheet into sub-10s Seedance 2.0 shots at "
                    "a fast, punchy ~3.5 wps, so nothing drags or rushes.")
    p.add_argument("beat_sheet")
    p.add_argument("out_shots")
    p.add_argument("--wps", type=float, default=DEFAULT_WPS)
    p.add_argument("--min-seconds", type=int, default=MIN_SECONDS)
    p.add_argument("--max-seconds", type=int, default=MAX_SECONDS)
    p.add_argument("--pace-low", type=float, default=PACE_LOW)
    p.add_argument("--pace-high", type=float, default=PACE_HIGH)
    p.add_argument("--shot-prefix", default="body_shot")
    a = p.parse_args(argv)
    if a.wps <= 0:
        p.error("--wps must be > 0")
    if a.max_seconds > 9:
        p.error("--max-seconds cannot exceed 9 (every generation must be UNDER 10s)")
    if a.min_seconds < 1 or a.min_seconds > a.max_seconds:
        p.error("--min-seconds must be in [1, max-seconds]")
    return a


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    global PACE_LOW, PACE_HIGH
    PACE_LOW, PACE_HIGH = args.pace_low, args.pace_high
    try:
        with open(args.beat_sheet, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except FileNotFoundError:
        sys.stderr.write("ERROR: beat sheet not found: %s\n" % args.beat_sheet)
        return 2
    except json.JSONDecodeError as e:
        sys.stderr.write("ERROR: beat sheet is not valid JSON: %s\n" % e)
        return 2
    try:
        beats = _normalize_beats(raw)
        payload = segment(beats, args.wps, args.min_seconds, args.max_seconds,
                          args.shot_prefix)
    except BeatSheetError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return 2

    framework = raw.get("framework") if isinstance(raw, dict) else None
    if framework:
        payload["framework"] = framework

    try:
        with open(args.out_shots, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as e:
        sys.stderr.write("ERROR: could not write %s: %s\n" % (args.out_shots, e))
        return 2

    _print_table(payload, args)
    sys.stderr.write("wrote %s\n" % args.out_shots)
    return 3 if any(s["needs_trim"] for s in payload["shots"]) else 0


if __name__ == "__main__":
    sys.exit(main())
