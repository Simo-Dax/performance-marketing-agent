#!/usr/bin/env python3
"""
segment_scenes.py - turn a storyboard + VO timing into picture-locked clay scenes.

INPUT
  storyboard.json: { "scenes": [ {
      "scene_id", "line_ids":[...], "role",
      "visual", "on_screen_text", "reference":{...}, "sfx", "span_share"
  } ] }
  timing.json: produced by align_vo.py (contiguous line spans tiling [0, total]).

WHAT IT DOES
  - Computes each scene's audio SPAN:
      * a scene covering whole line(s)      -> [first line.start, last line.end]
      * several scenes splitting ONE line   -> that line's span divided by span_share
  - requested_seconds = clamp(round_half_up(span), 4, 9)   (ROUND TO NEAREST: >=.5 up,
    <.5 down — never blanket-ceil; credits are not wasted on rounded-up tails). When the
    generation rounds DOWN below the span (a shortfall of at most ~0.5s), the stitcher (stitch_pixar.sh)
    freeze-holds that scene's last frame to its exact span — the VO is NEVER altered.
  - ENFORCES THE MERGE LAW: a scene whose span is under 3.5s (it would round below
    Seedance's 4s floor) must NOT be its own generation — that wastes most of a forced
    4s render. It is a structural error (exit 3): merge that line with an adjacent line
    into ONE scene (one generation carrying both beats as hard-cut sub-shots).
    THE HOOK ALWAYS MERGES: scene 1 covers the hook line PLUS the adjacent next line
    (the clip opens on the hook's continuous 1-2s beat, then hard-cuts into the merged
    line's beats). A hook scene covering ONLY the hook line is a structural error.
    Exception: the CTA when it is the last scene (the ad must end on the CTA alone;
    a short CTA renders at the 4s floor with a warning, not an error).
  - trim_in = 0, trim_out = span                   (picture-lock; trim_out-trim_in = span)
  - AUTO-SPLITS any scene whose span reaches 10s into equal sub-scenes (scene_id + a/b/…),
    each keeping the parent scene's reference (the hook still), so every generation stays UNDER
    10s. A single line can be ONE clip for any span up to just under 10s (rendered at an integer 4-9s).
  - Verifies the spans tile [0, total] (no gaps/overlaps), every line is covered, and
    the last scene is the CTA.

OUTPUT scenes.json: { concept, vo_total, n_scenes, scenes:[ {
    scene_id, role, covers, start, end, span_seconds, requested_seconds,
    trim_in, trim_out, reference, on_screen_text, sfx, visual, clip } ] }

Exit 0 clean, 2 on bad input, 3 when a structural problem needs a storyboard fix
(uncovered line, shares that don't sum to 1, a gap/overlap in coverage, or the ad
not ending on the CTA).
"""

import argparse
import json
import math
import sys

MIN_RENDER = 4
MAX_RENDER = 9          # max integer render duration per clip (Seedance integer 4-9s, under 10)
MAX_SPAN = 10          # a line can SPAN up to just under 10s as ONE clip before it must be split
TILE_TOL = 0.5          # gap/overlap larger than this between scenes is a structural error
MERGE_BELOW = 3.5       # a span under this rounds below the 4s floor: merge it (exit 3; hook enforced via the solo-hook check)


def die(msg, code=2):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(code)


def load(path, what):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        die("%s not found: %s" % (what, path))
    except json.JSONDecodeError as exc:
        die("%s is not valid JSON: %s" % (what, exc))


def words_in(words, s, e):
    """The exact spoken words whose midpoint falls in [s, e) — so each scene knows the VO
    it must direct its action to."""
    out = []
    for w in words:
        mid = (float(w.get("start", 0)) + float(w.get("end", 0))) / 2.0
        if s <= mid < e:
            out.append(str(w.get("word", "")).strip())
    return " ".join(t for t in out if t)


def main(argv=None):
    p = argparse.ArgumentParser(prog="segment_scenes.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("storyboard")
    p.add_argument("timing")
    p.add_argument("out_scenes")
    args = p.parse_args(argv)

    sb = load(args.storyboard, "storyboard")
    tm = load(args.timing, "timing")

    scenes_in = sb.get("scenes") if isinstance(sb, dict) else None
    if not isinstance(scenes_in, list) or not scenes_in:
        die("storyboard.json needs a non-empty 'scenes' array")
    tlines = tm.get("lines") if isinstance(tm, dict) else None
    if not isinstance(tlines, list) or not tlines:
        die("timing.json needs a non-empty 'lines' array (run align_vo.py first)")

    total = float(tm.get("total_seconds") or (tlines[-1].get("end", 0)))
    words_tl = tm.get("words") or []
    line_span = {}
    line_order = {}
    for idx, ln in enumerate(tlines):
        line_span[str(ln["id"])] = (float(ln["start"]), float(ln["end"]))
        line_order[str(ln["id"])] = idx

    flags = []   # must-fix (exit 3)
    warns = []   # informational (exit 0)

    # validate line_ids + collect per-line scene membership (in storyboard order)
    per_line = {}
    for si, sc in enumerate(scenes_in):
        if not isinstance(sc, dict):
            die("scenes[%d] is not an object" % si)
        ids = sc.get("line_ids") or ([sc["line_id"]] if sc.get("line_id") else [])
        if not ids:
            die("scenes[%d] (%s) has no line_ids" % (si, sc.get("scene_id", "?")))
        for lid in ids:
            if str(lid) not in line_span:
                die("scenes[%d] references unknown line_id '%s'" % (si, lid))
            per_line.setdefault(str(lid), []).append(si)

    # any line never covered?
    for lid in line_span:
        if lid not in per_line:
            flags.append("line '%s' is never covered by any scene" % lid)

    # compute each scene's [start, end]
    spans = [None] * len(scenes_in)
    for lid, members in per_line.items():
        if len(members) == 1:
            continue  # handled in the whole-coverage pass below
        # split-line group: several scenes share ONE line; each must cover only it
        ls, le = line_span[lid]
        shares = []
        for si in members:
            sc = scenes_in[si]
            ids = sc.get("line_ids") or [sc.get("line_id")]
            if [str(x) for x in ids] != [lid]:
                flags.append("scene '%s' splits line '%s' but also covers other lines; "
                             "a split-line scene must cover exactly that one line"
                             % (sc.get("scene_id", "?"), lid))
            sh = sc.get("span_share")
            shares.append(float(sh) if isinstance(sh, (int, float)) and sh > 0 else None)
        if any(s is None for s in shares):
            shares = [1.0 / len(members)] * len(members)   # default equal split
        ssum = sum(shares)
        if abs(ssum - 1.0) > 0.01:
            warns.append("span_shares for line '%s' summed to %.2f; normalized to 1.0"
                         % (lid, ssum))
        shares = [s / ssum for s in shares]
        cur = ls
        for si, sh in zip(members, shares):
            seg = (le - ls) * sh
            spans[si] = (round(cur, 3), round(cur + seg, 3))
            cur += seg

    # whole-coverage scenes (their lines are each owned only by them)
    for si, sc in enumerate(scenes_in):
        if spans[si] is not None:
            continue
        ids = [str(x) for x in (sc.get("line_ids") or [sc.get("line_id")])]
        starts = [line_span[i][0] for i in ids]
        ends = [line_span[i][1] for i in ids]
        spans[si] = (round(min(starts), 3), round(max(ends), 3))

    # order scenes by start, check tiling
    order = sorted(range(len(scenes_in)), key=lambda i: spans[i][0])
    if order != list(range(len(scenes_in))):
        warns.append("storyboard scene order does not match audio order; reordering by time")
    prev_end = 0.0
    for i in order:
        s, e = spans[i]
        if abs(s - prev_end) > TILE_TOL:
            sid = scenes_in[i].get("scene_id", "scene_%d" % (i + 1))
            kind = "gap" if s > prev_end else "overlap"
            flags.append("%s of %.2fs before scene '%s' (coverage must be continuous)"
                         % (kind, abs(s - prev_end), sid))
        prev_end = e
    if abs(prev_end - total) > TILE_TOL:
        flags.append("scenes end at %.2fs but the VO is %.2fs (coverage must reach the end)"
                     % (prev_end, total))

    # build output, auto-splitting > 9s spans
    out = []
    for i in order:
        sc = scenes_in[i]
        s, e = spans[i]
        span = round(e - s, 3)
        base_id = str(sc.get("scene_id") or ("scene_%02d" % (i + 1)))
        role = str(sc.get("role") or "")
        ref = sc.get("reference") or {"type": "none"}
        ost = str(sc.get("on_screen_text") or "")
        sfx = bool(sc.get("sfx", False))
        visual = str(sc.get("visual") or "")
        action = str(sc.get("action") or "")
        sfx_note = str(sc.get("sfx_note") or "")
        covers = [str(x) for x in (sc.get("line_ids") or [sc.get("line_id")])]

        if span < MAX_SPAN:
            parts = [(base_id, s, e, ref)]
        else:
            k = int(math.ceil(span / MAX_RENDER))
            warns.append("scene '%s' span %.2fs >= %ds; auto-split into %d sub-scenes"
                         % (base_id, span, MAX_SPAN, k))
            step = span / k
            parts = []
            for j in range(k):
                ps = round(s + j * step, 3)
                pe = round(s + (j + 1) * step, 3) if j < k - 1 else e
                pid = "%s%s" % (base_id, chr(ord("a") + j))
                pref = ref  # every sub-scene keeps the parent's reference, no chaining
                parts.append((pid, ps, pe, pref))

        for (pid, ps, pe, pref) in parts:
            sp = round(pe - ps, 3)
            # ROUND TO NEAREST integer (>=.5 up, <.5 down), clamped 4-9 — never blanket
            # ceil. A round-down shortfall (at most ~0.5s) is reconciled at stitch: the
            # scene's last frame is freeze-held to its exact span. The VO is never altered.
            req = max(MIN_RENDER, min(MAX_RENDER, int(math.floor(sp + 0.5))))
            if role.lower() == "hook":
                # THE HOOK ALWAYS MERGES: scene 1 covers the hook line PLUS the adjacent
                # next line — the clip opens on the hook's continuous 1-2s beat, then
                # hard-cuts into the merged line's beats. A solo hook line is a
                # structural error.
                if len(covers) < 2:
                    flags.append("hook scene '%s' covers only the hook line (%s); the hook "
                                 "line never renders solo — merge it with the adjacent next "
                                 "line into ONE scene (line_ids: [hook, next]; the clip opens "
                                 "on the 1-2s hook beat, then hard-cuts), then re-run"
                                 % (pid, ",".join(covers)))
            out.append({
                "scene_id": pid, "role": role, "covers": covers,
                "start": ps, "end": pe, "span_seconds": sp,
                "requested_seconds": req, "trim_in": 0.0, "trim_out": sp,
                "reference": pref, "on_screen_text": ost, "sfx": sfx,
                "visual": visual, "action": action, "sfx_note": sfx_note,
                "vo_text": words_in(words_tl, ps, pe), "clip": "clips/%s.mp4" % pid,
            })

    # ends-on-CTA check
    if not out or out[-1]["role"].lower() != "cta":
        last = out[-1]["role"] if out else "(none)"
        flags.append("the ad does not end on the CTA: last scene role is '%s', not 'cta'" % last)

    # MERGE LAW: a scene whose span rounds below the 4s floor never renders solo
    # (a 2.6s beat in a forced 4s render wastes a third of the clip). Merge its line with
    # an adjacent line into ONE scene: one generation, both beats as hard-cut sub-shots.
    # The hook is exempt from THIS span check only because the solo-hook check above
    # already enforces its merge; a short CTA in last position renders at the 4s floor
    # with a warning (the ad must end on the CTA alone).
    for j, o in enumerate(out):
        sp = o["span_seconds"]
        r = o["role"].lower()
        if r == "hook" or sp >= MERGE_BELOW:
            continue
        if j == len(out) - 1 and r == "cta":
            warns.append("CTA scene '%s' span %.2fs is under the 4s floor; it renders at 4s "
                         "and ~%.2fs is trimmed (allowed: the ad must end on the CTA alone)"
                         % (o["scene_id"], sp, 4 - sp))
        else:
            flags.append("scene '%s' (%s) span %.2fs rounds below the 4s floor; never render "
                         "it solo — merge its line with an adjacent line into ONE scene (one "
                         "generation, both beats as hard-cut sub-shots), then re-run"
                         % (o["scene_id"], o["role"] or "?", sp))

    payload = {
        "concept": tm.get("concept") if isinstance(tm, dict) else None,
        "vo_total": round(total, 3),
        "n_scenes": len(out),
        "total_render_seconds": sum(o["requested_seconds"] for o in out),
        "scenes": out,
    }
    try:
        with open(args.out_scenes, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        die("could not write %s: %s" % (args.out_scenes, exc), 1)

    w = sys.stderr.write
    w("\n=== SCENE PLAN (%d scenes, VO %.2fs, render %ds) ===\n"
      % (len(out), total, payload["total_render_seconds"]))
    w("scene       role        span   render  trim_out  ref           text\n")
    for o in out:
        ref = o["reference"]
        rs = "%s:%s" % (ref.get("type", "?"), str(ref.get("source", ""))[:8])
        w("%-11s %-10s %5.2f   %2ds    %6.2f   %-12s %s\n" % (
            o["scene_id"], o["role"][:10], o["span_seconds"], o["requested_seconds"],
            o["trim_out"], rs, (o["on_screen_text"][:18])))
    for m in warns:
        w("WARN: %s\n" % m)
    for m in flags:
        w("FLAG: %s\n" % m)
    w("wrote %s\n=================================================\n\n" % args.out_scenes)
    return 3 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
