#!/usr/bin/env python3
"""
segment_turns.py - transcript.json -> render_plan.json for the podcast factory.

Groups each host's turns into generations of 2-3 lines (base 2; a trailing single
line is merged up so a generation is NEVER a lone 1-line clip), each rendered as a
multi-scene clip with a hard cut, sizes each generation (round(words/3.5) per
line + ~1s trailing so the last line has room for the 0.2s cut, every generation
an integer 4..9s UNDER 10s), and assigns each generation a UNIQUE voice-cut id so
the parallel renders can't collide on Higgsfield's _sfx audio dedup.

Usage: python3 segment_turns.py transcript.json render_plan.json [--lines-per-gen 2] [--wps 3.5]
Exit: 0 ok, 2 bad input, 3 a generation fell outside 4..9s (split a line).
"""
import argparse, json, sys


def main(argv=None):
    p = argparse.ArgumentParser(prog="segment_turns.py")
    p.add_argument("transcript")
    p.add_argument("out_plan")
    p.add_argument("--lines-per-gen", type=int, default=2)
    p.add_argument("--wps", type=float, default=3.5)
    a = p.parse_args(argv)

    try:
        t = json.load(open(a.transcript, encoding="utf-8"))
    except Exception as e:
        sys.stderr.write("ERROR reading transcript: %s\n" % e)
        return 2
    turns = t.get("turns") or []
    if not turns:
        sys.stderr.write("ERROR: transcript has no 'turns'\n")
        return 2

    by = {}
    for tn in turns:
        by.setdefault(tn["speaker"], []).append(tn)

    gens = []
    flagged = []
    for spk in sorted(by):
        items = by[spk]
        chunks = [items[i:i + a.lines_per_gen] for i in range(0, len(items), a.lines_per_gen)]
        if len(chunks) >= 2 and len(chunks[-1]) == 1:
            tail = chunks.pop()                      # pop first, THEN append to the new last
            chunks[-1] = chunks[-1] + tail           # never a 1-line gen -> 2-3 lines each
        for ci, chunk in enumerate(chunks, 1):
            gid = "%s%d" % (spk, ci)
            lines, secs = [], 0
            for tn in chunk:
                wc = len(str(tn["line"]).split())
                secs += max(1, int(round(wc / a.wps)))
                lines.append({"turn": tn["turn"], "line": tn["line"], "word_count": wc})
            dur = secs + 1  # trailing beat so the last line has room for the 0.2s cut
            if dur < 4:
                dur = 4
            if dur > 9:
                dur = 9
                flagged.append(gid)
            gens.append({"gen_id": gid, "speaker": spk, "voice_cut": gid + ".wav",
                         "duration": dur, "lines": lines})

    plan = {"concept": t.get("concept"), "brand": t.get("brand"), "hosts": t.get("hosts"),
            "lines_per_gen": a.lines_per_gen, "wps": a.wps, "generations": gens}
    json.dump(plan, open(a.out_plan, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    w = sys.stderr.write
    w("\n=== RENDER PLAN ===\ngen   spk  lines  sec\n")
    for g in gens:
        w("%-5s %-3s  %-5d  %d\n" % (g["gen_id"], g["speaker"], len(g["lines"]), g["duration"]))
    tot = sum(g["duration"] for g in gens)
    w("total generated seconds: %d across %d generations (~%d credits @1080p)\n" % (tot, len(gens), tot * 9))
    if flagged:
        w("FLAGGED (>9s, split a line into more turns): %s\n" % ", ".join(flagged))
    w("wrote %s\n" % a.out_plan)
    return 3 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
