#!/usr/bin/env python3
"""Clip spans, ceil-sized generations, the merge law, the waste table.

Usage: segment_beats.py <beatmap.json> <timing.json> <out beats.json>

beatmap.json: {"clips":[{"id":"clip_01","line_ids":["l01","l02"]}, ...]}
timing.json:  align_vo.py output ({"lines":[{"id","start","end",...}], "total_seconds"})

Film boundaries sit at the midpoint of the silence between adjacent clips' lines.
Generation = ceil(span), clamped to the integer 4..9 window (Seedance 2.5).
Exit 3 on: a non-final clip whose span < 3.5s (merge law), a span > 9s (split it),
or line ids that are missing/out of order.
"""
import json, math, sys

def die(msg, code=3):
    print(f"segment_beats: {msg}", file=sys.stderr)
    sys.exit(code)

def main():
    if len(sys.argv) != 4:
        die("usage: segment_beats.py <beatmap.json> <timing.json> <out.json>", 2)
    bm = json.load(open(sys.argv[1]))
    tm = json.load(open(sys.argv[2]))
    lines = {l["id"]: l for l in tm["lines"]}
    order = [l["id"] for l in tm["lines"]]
    total = float(tm.get("total_seconds") or max(l["end"] for l in tm["lines"]))
    clips = bm["clips"]
    if not clips:
        die("no clips in beatmap")
    seen = []
    for c in clips:
        for lid in c["line_ids"]:
            if lid not in lines:
                die(f"unknown line id {lid}")
            seen.append(lid)
    if seen != order:
        die(f"clips must cover every line exactly once, in order (got {seen}, want {order})")

    out, rows = [], []
    prev_end = 0.0
    for i, c in enumerate(clips):
        first = lines[c["line_ids"][0]]
        last = lines[c["line_ids"][-1]]
        start = prev_end
        if i + 1 < len(clips):
            nxt = lines[clips[i + 1]["line_ids"][0]]
            end = (last["end"] + nxt["start"]) / 2.0
        else:
            end = total
        span = end - start
        if span > 9.0:
            die(f"{c['id']}: span {span:.2f}s exceeds 9s — split this clip")
        if span < 3.5 and i + 1 < len(clips):
            die(f"{c['id']}: span {span:.2f}s is under 3.5s — merge it with a neighbor (merge law)")
        gen = max(4, min(9, math.ceil(span - 1e-6)))
        if gen < span:
            die(f"{c['id']}: span {span:.2f}s cannot be covered by a {gen}s generation")
        out.append({"id": c["id"], "line_ids": c["line_ids"],
                    "film_start": round(start, 3), "film_end": round(end, 3),
                    "span": round(span, 3), "generate_seconds": gen,
                    "waste": round(gen - span, 3)})
        rows.append((c["id"], span, gen, gen - span))
        prev_end = end

    total_gen = sum(r[2] for r in rows)
    total_waste = sum(r[3] for r in rows)
    json.dump({"total_seconds": round(total, 3), "total_generated": total_gen,
               "total_waste": round(total_waste, 3), "clips": out},
              open(sys.argv[3], "w"), indent=2)
    print(f"{'clip':10s} {'span':>7s} {'gen':>4s} {'waste':>6s}")
    for cid, span, gen, waste in rows:
        print(f"{cid:10s} {span:7.2f} {gen:4d} {waste:6.2f}")
    print(f"{'TOTAL':10s} {total:7.2f} {total_gen:4d} {total_waste:6.2f}")
    print(f"generating {total_gen}s for a {total:.2f}s film")

if __name__ == "__main__":
    main()
