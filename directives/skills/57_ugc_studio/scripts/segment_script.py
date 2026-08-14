#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""segment_script.py - UGC Studio sizing: approved transcript -> render_plan skeleton.

WHY (owner-verified physics, 2026-07-10 audit): Seedance 2.0 stretches a spoken
line to fill the requested duration, so the requested seconds ARE the talking
pace, and 10s+ single generations produce very bad output. Hence THE SIZING LAW:

    every generation is an INTEGER 4..9 seconds;
    seconds = round-to-NEAREST of words/wps (a blanket ceil pads dead air the
    word-accurate cutter then has to eat).

THE MERGE LAW: a beat under ~3.5s of speech never renders solo - stretched to
the 4s floor it drags and reads as AI. It merges FORWARD with its neighbor as
hard-cut sub-shots inside ONE generation (max 3 sub-shots, one action each).
The FIRST beat (the hook) always merges forward; the LAST beat (the close) may
stand alone at the 4s floor - the typed close is the one legal long hold. A
merge that would exceed 9s splits at the best sentence boundary instead.

MAX-SOLO-SHOT: the banked winners cut every 1-3s and no shot exceeds ~4s except
the typed close, so any solo gen over 4s is marked needs_subshot_or_overlay -
the orchestrator adds a sub-shot map or schedules an overlay before Gate 2.
Merged gens already carry their internal cut.

Hook gens get +1s of action-buffer room (the hook's visual move), still <=9s;
the word-accurate cutter trims the slack. Noted in the entry's "buffer" field.

PACE band [2.4, 4.4] wps: below drags, above rushes; the sprint formats'
measured band tops at 4.4 so bank-measured scripts do not false-flag. An
out-of-band beat prints a PACE FLAG and NEVER blocks - pace is fixed in the
words, not by refusing to plan.

Input: a transcript file - the approved words in play order, one BEAT per line
(a beat = one shell's spoken text). Blank lines and '#'-prefixed comment/label
lines are ignored.

Usage:
  python3 segment_script.py transcript.txt --format testimonial [--wps 3.7] \
      --out render_plan.skeleton.json

Output --out: a render_plan SKELETON per pipeline-contracts.md:
  {format, close_type, wps, entries: [{kind:"gen", gen_id, role, duration,
   buffer (hook only), lines: [{line, clip}], sub_shots (pre-seeded from merges,
   t proportional to word counts rounded to 0.5s), needs_subshot_or_overlay}]}
The orchestrator fills beat_type, images, prompt_file, voice_cut, the sub-shot
descriptions, and the identity checkpoint at Step 5. close_type is the format's
typed close (render-laws section 5).

Exit codes: 0 ok (pace flags included), 2 bad input or impossible sizing.
"""

import argparse
import json
import math
import re
import sys

#                    format             typed close     wps (measured from winners)
FORMATS = {
    "testimonial":      ("cta",          3.7),
    "before-after":     ("delight",      4.15),
    "unboxing":         ("display-loop", 3.7),
    "direct-to-camera": ("button",       4.0),
}

MIN_S = 4              # Seedance per-generation floor
MAX_S = 9              # integer 4..9, always; 10s+ output is very bad
MERGE_UNDER_S = 3.5    # speech under this never renders solo
PACE_LOW = 2.4         # below drags
PACE_HIGH = 4.4        # above rushes (sprint band top)
MAX_SUBSHOTS = 3       # 2-3 hard-cut sub-shots per generation maximum
HOOK_BUFFER_S = 1      # hook action buffer, cutter trims the slack

_SENT_SPLIT_RE = re.compile(r'(?<=[.!?])["\')\]]*\s+')


class TranscriptError(Exception):
    """Bad input so main() exits cleanly with an actionable message."""


def _wc(text):
    return len(text.split())


def _round_nearest(x):
    """Round-half-up. The sizing law is round-to-NEAREST; Python's round()
    banker-rounds x.5 toward even, which silently under-sizes half the halves."""
    return int(math.floor(x + 0.5))


def _half(x):
    """Round to the nearest 0.5s (sub-shot t grid; whisper reconciles +/-0.5s)."""
    return math.floor(x * 2.0 + 0.5) / 2.0


def _dur_for(words, wps):
    """Integer seconds = round(words/wps), clamped up to the 4s floor only."""
    return max(MIN_S, _round_nearest(words / wps))


def parse_transcript(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw_lines = fh.readlines()
    except FileNotFoundError:
        raise TranscriptError("transcript not found: %s" % path)
    except OSError as e:
        raise TranscriptError("could not read %s: %s" % (path, e))
    beats = []
    for ln in raw_lines:
        t = ln.strip()
        if not t or t.startswith("#"):
            continue
        beats.append({"beat": len(beats) + 1, "text": t, "words": _wc(t)})
    if not beats:
        raise TranscriptError(
            "no beats in %s (every line is blank or '#'-prefixed); "
            "one beat per line, the approved words in play order" % path)
    return beats


def group_beats(beats, wps):
    """Forward walk applying THE MERGE LAW: a sub-3.5s beat absorbs its next
    neighbor(s) until the group speaks >=3.5s (cap: 3 sub-shots). The hook can
    only merge forward by construction; the close, with no forward neighbor,
    stands alone at the 4s floor - both boundary rules fall out of the walk."""
    groups, i, n = [], 0, len(beats)
    while i < n:
        grp = [beats[i]]
        raw = beats[i]["words"] / wps
        while raw < MERGE_UNDER_S and len(grp) < MAX_SUBSHOTS and i + 1 < n:
            i += 1
            grp.append(beats[i])
            raw += beats[i]["words"] / wps
        groups.append(grp)
        i += 1
    return groups


def _explode(group):
    """Group -> sentence units (beat kept on each) for boundary splitting."""
    units = []
    for b in group:
        for s in _SENT_SPLIT_RE.split(b["text"]):
            s = s.strip()
            if s:
                units.append({"beat": b["beat"], "text": s, "words": _wc(s)})
    return units


def split_units(units, wps):
    """A group sized over 9s splits at the sentence boundary that minimizes the
    longer side (tie-break: most balanced words), recursively. One unsplittable
    sentence over 9s is a script problem, not a render problem - refuse."""
    total = sum(u["words"] for u in units)
    if _dur_for(total, wps) <= MAX_S:
        return [units]
    if len(units) < 2:
        raise TranscriptError(
            "beat %d runs %d words (~%.1fs at %.2f wps) with no sentence "
            "boundary to split on; a generation is an integer 4..9s - add "
            "punctuation or shorten the line" % (
                units[0]["beat"], total, total / wps, wps))
    best_k, best_score = None, None
    for k in range(1, len(units)):
        wl = sum(u["words"] for u in units[:k])
        wr = total - wl
        score = (max(_dur_for(wl, wps), _dur_for(wr, wps)), abs(wl - wr))
        if best_score is None or score < best_score:
            best_score, best_k = score, k
    return split_units(units[:best_k], wps) + split_units(units[best_k:], wps)


def _lines_from_units(units):
    """Adjacent same-beat sentence units rejoin into one line (one clip);
    units from different beats stay separate lines (the merge's sub-shots)."""
    lines = []
    for u in units:
        if lines and lines[-1]["beat"] == u["beat"]:
            lines[-1]["text"] += " " + u["text"]
            lines[-1]["words"] += u["words"]
        else:
            lines.append(dict(u))
    return lines


def build_plan(beats, fmt, wps):
    close_type = FORMATS[fmt][0]

    pieces = []
    for grp in group_beats(beats, wps):
        units = [{"beat": b["beat"], "text": b["text"], "words": b["words"]}
                 for b in grp]
        if _dur_for(sum(u["words"] for u in units), wps) > MAX_S:
            for p in split_units(_explode(grp), wps):
                pieces.append({"units": p, "split": True})
        else:
            pieces.append({"units": units, "split": False})

    entries, metas = [], []
    clip_n, n_p = 0, len(pieces)
    for gi, piece in enumerate(pieces):
        lines = _lines_from_units(piece["units"])
        words = sum(l["words"] for l in lines)
        dur = _dur_for(words, wps)
        role = "hook" if gi == 0 else ("close" if gi == n_p - 1 else "body")
        buffer_s = 0
        if role == "hook":
            buffer_s = min(HOOK_BUFFER_S, MAX_S - dur)
            dur += buffer_s
        gen_id = "gen_%02d" % (gi + 1)
        out_lines = []
        for l in lines:
            clip_n += 1
            out_lines.append({"line": l["text"], "clip": "c%02d" % clip_n})
        merged = len(lines) > 1

        sub_shots = []
        if merged:
            # Pre-seed the planned sub-shot map: t proportional to word counts
            # over the speech span (duration minus hook buffer), 0.5s grid.
            span = dur - buffer_s
            sub_shots.append({"t": 0.0, "shot": ""})
            cum, prev_t = 0, 0.0
            for l in lines[:-1]:
                cum += l["words"]
                t = _half(span * cum / float(words))
                t = min(max(t, 0.5), max(span - 0.5, 0.5))
                if t <= prev_t:
                    t = prev_t + 0.5
                if t > span - 0.5 + 1e-9:
                    # no room left on the 0.5s grid (word-heavy early lines in a
                    # short gen) - drop this pre-seeded cut rather than emit a
                    # t at/after the duration; the orchestrator re-seats it when
                    # authoring the sub-shot descriptions at Step 5
                    continue
                sub_shots.append({"t": t, "shot": ""})
                prev_t = t

        entry = {"kind": "gen", "gen_id": gen_id, "role": role, "duration": dur}
        if role == "hook":
            entry["buffer"] = buffer_s
        entry["lines"] = out_lines
        entry["sub_shots"] = sub_shots
        # the typed close is the one legal long hold (rhythm card close_exempt),
        # so a solo close never demands an internal cut
        entry["needs_subshot_or_overlay"] = (not merged) and dur > MIN_S \
            and role != "close"
        entries.append(entry)
        metas.append({
            "gen_id": gen_id, "role": role, "dur": dur, "buffer": buffer_s,
            "beats": [l["beat"] for l in lines], "merged": merged,
            "split": piece["split"], "n_lines": len(lines), "words": words,
            "needs": entry["needs_subshot_or_overlay"],
            "eff": words / float(dur - buffer_s),
        })

    in_words = sum(b["words"] for b in beats)
    out_words = sum(m["words"] for m in metas)
    if in_words != out_words:
        raise TranscriptError(
            "INTERNAL: word accounting mismatch, input %d != output %d"
            % (in_words, out_words))

    plan = {"format": fmt, "close_type": close_type, "wps": wps,
            "entries": entries}
    return plan, metas


def _beat_notes(b, gens, wps):
    notes = []
    g0 = gens[0]
    if len(gens) > 1:
        notes.append("split at sentence boundary")
    if g0["role"] == "hook" and b["beat"] == g0["beats"][0]:
        notes.append("hook%s (+%ds buffer)"
                     % (": merged forward" if g0["merged"] else "", g0["buffer"]))
    else:
        partners = sorted(set(x for m in gens for x in m["beats"]) - {b["beat"]})
        if partners:
            notes.append("merged with %s" % "+".join("b%d" % x for x in partners))
    if b["words"] / wps < MERGE_UNDER_S:
        if len(gens) == 1 and not g0["merged"]:
            if g0["role"] == "close":
                notes.append("close: stands alone at 4s floor")
            else:
                notes.append("sub-3.5s SOLO - should not happen, report this")
        else:
            notes.append("sub-3.5s: never solo")
    if len(gens) == 1 and not g0["merged"] and g0["needs"]:
        notes.append("solo >4s: needs sub-shot or overlay")
    return "; ".join(notes) if notes else "solo"


def _print_table(plan, metas, beats):
    w = sys.stdout.write
    w("\n=== SIZING TABLE (%s @ %.2f wps, close: %s) ===\n"
      % (plan["format"], plan["wps"], plan["close_type"]))
    w("%-5s %5s  %5s  %-15s %-5s %s\n"
      % ("beat", "words", "wps", "gen", "dur", "notes"))
    for b in beats:
        gens = [m for m in metas if b["beat"] in m["beats"]]
        gen_lbl = "+".join(m["gen_id"] for m in gens)
        dur_lbl = "+".join(str(m["dur"]) for m in gens)
        w("%-5s %5d  %5.2f  %-15s %-5s %s\n"
          % ("b%d" % b["beat"], b["words"], gens[0]["eff"], gen_lbl, dur_lbl,
             _beat_notes(b, gens, plan["wps"])))
    w("total: %d gens, %d render seconds (hook buffer incl.), %d clips\n"
      % (len(metas), sum(m["dur"] for m in metas),
         sum(m["n_lines"] for m in metas)))
    w("=" * 54 + "\n")


def _print_flags(metas):
    for m in metas:
        if PACE_LOW <= m["eff"] <= PACE_HIGH:
            continue
        print("PACE FLAG: %s (%s) runs %.2f wps over its %ds speech span - %s "
              "(band %.1f-%.1f). Flag only, plan written; fix the words or --wps "
              "if it reads wrong."
              % (m["gen_id"], "+".join("b%d" % b for b in m["beats"]),
                 m["eff"], m["dur"] - m["buffer"],
                 "drags" if m["eff"] < PACE_LOW else "rushes",
                 PACE_LOW, PACE_HIGH))


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="segment_script.py",
        description="UGC Studio sizing: one beat per transcript line -> a "
                    "render_plan skeleton of integer 4..9s generations "
                    "(round-to-nearest, sub-3.5s beats merged, hooks buffered).")
    p.add_argument("transcript", help="approved words, one beat per line")
    p.add_argument("--format", required=True, choices=sorted(FORMATS),
                   help="the shell format (sets default wps and typed close)")
    p.add_argument("--wps", type=float, default=None,
                   help="words-per-second override (default: the format's)")
    p.add_argument("--out", required=True, help="render_plan skeleton JSON path")
    a = p.parse_args(argv)
    if a.wps is not None and a.wps <= 0:
        p.error("--wps must be > 0")
    return a


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    wps = args.wps if args.wps is not None else FORMATS[args.format][1]
    try:
        beats = parse_transcript(args.transcript)
        plan, metas = build_plan(beats, args.format, wps)
    except TranscriptError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return 2
    except RecursionError:
        sys.stderr.write("ERROR: transcript could not be split into 4..9s "
                         "generations; shorten the longest beat\n")
        return 2

    try:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(plan, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as e:
        sys.stderr.write("ERROR: could not write %s: %s\n" % (args.out, e))
        return 2

    _print_table(plan, metas, beats)
    _print_flags(metas)
    if len(metas) == 1:
        print("WARNING: single-gen plan - no separate close beat; the manifest "
              "law needs a final role:\"close\" entry. Add a close beat.")
    print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
