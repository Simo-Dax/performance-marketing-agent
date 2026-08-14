#!/usr/bin/env python3
"""
build_manifest.py — UGC Studio two-rail assembly resolver (edl -> manifest).

    python3 build_manifest.py edl.json render_plan.json clips/cut_report.json --out manifest.json

WHY THIS FILE EXISTS (the verified physics): the banked winners cut every
1.1-3.2s while generations run 4-9s — a generation is RAW FOOTAGE, never a
timeline shot. Density comes from TWO RAILS: the AUDIO RAIL (base clips'
own audio joined at line boundaries, lip-sync untouched) and the VIDEO RAIL
(punch-in overlays replacing the PICTURE while the host audio runs
uninterrupted underneath). This builder resolves every edit decision against
MEASURED clip truth (cut_report.json word timeline + durations) into absolute
timeline seconds, so stitch.sh executes verbatim with zero lookups.

STRUCTURAL LAWS (violations exit 1, NOTHING written):
  - Every base clip resolves to <clips_dir>/<clip>.mp4 with a measured
    duration from the cut report; base clip ids never repeat.
  - Cuts land on words, not guesses: a word anchor that cannot be resolved
    against the host clip's whisper words[] is a hard fail.
  - A punch-in rides ONE host clip's continuing audio: it never crosses the
    host's join, never overlaps another overlay, and NEVER covers any part
    of the final base clip — the close is never covered.
  - Interior trims (jump-cut manufacture) must be real interior windows
    (resume > cut, both inside the clip); every trim subtracts from every
    downstream absolute time, and nothing may anchor inside removed content.
  - THE TYPED CLOSE: the final base clip must trace (cut_report gen_id ->
    render_plan gen entry) to role=="close". QC means "ends on the approved
    close beat", never a blanket literal CTA.

RHYTHM (recorded, not fatal): cut_points = base joins + trim seams + overlay
in/out + the report's reconciled internal cuts, all absolute. Shot lengths
derive from THIS deterministic list, never scene detection. verdict is
scored against the format's RHYTHM CARD targets (the close is exempt from
shot_max when close_exempt — the payoff is the only legal long hold). A
rhythm FAIL still writes the manifest (verdict recorded; stitch refuses),
because the fix is edit-side — more punch-ins, trims, slices — not here.

Silent plans (no words anywhere) set audio.loudnorm=false: SFX-only or no
audio ships as-is — loudnorm on a silent rail only boosts noise.

Stdlib only. Exit 0 = manifest written; exit 1 = structural fail.
"""

import argparse
import json
import os
import re
import statistics
import subprocess
import sys

EPS = 1e-6
POINT_MERGE = 0.01        # cut points closer than this are one cut
TARGET_LUFS = -14         # narrated ads normalize here, two-pass, at stitch


def die(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(1)


def warn(msg):
    sys.stderr.write("WARN: " + msg + "\n")


def load_json(path, what):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        die(what + " not found: " + path)
    except json.JSONDecodeError as exc:
        die(what + " is not valid JSON (" + path + "): " + str(exc))
    if not isinstance(data, dict):
        die(what + " must be a JSON object: " + path)
    return data


def fnum(val, where):
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        die(where + " must be a number, got " + type(val).__name__)
    return float(val)


def norm_word(w):
    """Whisper words carry punctuation/case; anchors match the bare token."""
    return re.sub(r"[^a-z0-9']+", "", str(w).lower())


# ---------------------------------------------------------------------------
# cut_report: the measured truth per clip
# ---------------------------------------------------------------------------

def index_report(report, report_path):
    clips_in = report.get("clips")
    if not isinstance(clips_in, list) or not clips_in:
        die("cut_report.json has no clips[] — run whisper_cut.py first")
    clips_dir = os.path.dirname(report_path) or "clips"
    idx = {}
    for i, c in enumerate(clips_in):
        where = "cut_report.clips[%d]" % i
        if not isinstance(c, dict):
            die(where + " must be an object")
        name = str(c.get("clip") or "")
        if not name:
            die(where + " missing 'clip'")
        dur = fnum(c.get("duration"), where + ".duration")
        if dur <= EPS:
            die(where + " ('%s') has non-positive duration %.3f" % (name, dur))
        words = c.get("words")
        if words is None:
            words = []
        if not isinstance(words, list):
            die(where + ".words must be a list (empty for silent clips)")
        internal = c.get("internal_cuts") or []
        if not isinstance(internal, list):
            die(where + ".internal_cuts must be a list")
        idx[name] = {
            "gen_id": str(c.get("gen_id") or ""),
            "duration": dur,
            "words": words,
            "internal_cuts": [fnum(t, where + ".internal_cuts") for t in internal],
        }
    return idx, clips_dir


# ---------------------------------------------------------------------------
# THE AUDIO RAIL: base clips + interior trims -> absolute layout
# ---------------------------------------------------------------------------

def resolve_base(edl, idx, clips_dir):
    base_in = edl.get("base")
    if not isinstance(base_in, list) or not base_in:
        die("edl.base must be a non-empty list — the AUDIO RAIL is the spine")
    rail, seen, cursor = [], set(), 0.0
    for i, entry in enumerate(base_in):
        where = "edl.base[%d]" % i
        if not isinstance(entry, dict):
            die(where + " must be an object")
        clip = str(entry.get("clip") or "")
        if not clip:
            die(where + " missing 'clip'")
        if clip in seen:
            die(where + ": clip '%s' appears twice on the base rail — spine "
                "slicing reuses a GEN as multiple clips, a clip id at most once"
                % clip)
        seen.add(clip)
        rec = idx.get(clip)
        if rec is None:
            die(where + ": clip '%s' is not in cut_report.json — every base "
                "clip needs a measured duration (run whisper_cut.py, or fix "
                "the clip id)" % clip)
        file_rel = os.path.join(clips_dir, clip + ".mp4")
        if not os.path.exists(file_rel):
            die(where + ": clip file not found on disk: %s" % file_rel)
        dur = rec["duration"]

        trims = []
        for j, tr in enumerate(entry.get("trim") or []):
            tw = where + ".trim[%d]" % j
            if not isinstance(tr, dict):
                die(tw + " must be an object")
            cut = fnum(tr.get("cut_dead_air_at"), tw + ".cut_dead_air_at")
            resume = fnum(tr.get("resume"), tw + ".resume")
            if resume <= cut + EPS:
                die(tw + ": resume (%.3f) must be AFTER the cut point (%.3f) "
                    "— a trim removes a real dead-air window" % (resume, cut))
            if cut <= EPS or resume >= dur - EPS:
                die(tw + ": trim [%.3f..%.3f] must be strictly INSIDE clip "
                    "'%s' (duration %.3f) — head/tail slack is whisper_cut's "
                    "job, interior trims manufacture jump cuts"
                    % (cut, resume, clip, dur))
            trims.append([round(cut, 3), round(resume, 3)])
        trims.sort()
        for a, b in zip(trims, trims[1:]):
            if b[0] < a[1] - EPS:
                die(where + ": trims [%.3f..%.3f] and [%.3f..%.3f] overlap "
                    "in clip '%s'" % (a[0], a[1], b[0], b[1], clip))

        eff = dur - sum(r - c for c, r in trims)
        rail.append({
            "clip": clip, "file": file_rel, "duration": dur, "trims": trims,
            "eff": eff, "start_abs": cursor,
            "gen_id": rec["gen_id"], "words": rec["words"],
            "internal_cuts": rec["internal_cuts"],
        })
        cursor += eff
    return rail, cursor


def rel_to_abs(bc, t, where):
    """Map a clip-relative time onto the absolute timeline, honoring interior
    trims: every trim ending at/before t shifts it earlier; a time INSIDE a
    trim window points at removed content and is a hard fail."""
    if t < -EPS or t > bc["duration"] + EPS:
        die(where + ": time %.3f is outside clip '%s' (0..%.3f)"
            % (t, bc["clip"], bc["duration"]))
    shift = 0.0
    for c, r in bc["trims"]:
        if c + EPS < t < r - EPS:
            die(where + ": time %.3f lands inside the interior trim "
                "[%.3f..%.3f] of clip '%s' — that moment was cut out; anchor "
                "before the cut or after the resume" % (t, c, r, bc["clip"]))
        if r <= t + EPS:
            shift += r - c
    return bc["start_abs"] + t - shift


# ---------------------------------------------------------------------------
# THE VIDEO RAIL: punch-in overlays resolved to absolute seconds
# ---------------------------------------------------------------------------

def resolve_overlays(edl, rail, edl_dir):
    by_clip = dict((bc["clip"], bc) for bc in rail)
    final = rail[-1]
    out = []
    for i, ov in enumerate(edl.get("overlays") or []):
        where = "edl.overlays[%d]" % i
        if not isinstance(ov, dict):
            die(where + " must be an object")
        insert = str(ov.get("insert") or "")
        if not insert:
            die(where + " missing 'insert'")
        # resolve like every other contract file: against $WORK (cwd in the
        # canonical flow) first, then against the EDL's own directory — the
        # same answer when everything lives in $WORK, and no cwd surprise
        # when argv paths are absolute.
        insert_disk = insert
        if not os.path.isabs(insert_disk) and not os.path.exists(insert_disk):
            cand = os.path.join(edl_dir, insert)
            if os.path.exists(cand):
                insert_disk = cand
        if not os.path.exists(insert_disk):
            die(where + ": insert file not found: %s (stills render first; "
                "b-roll slices come from whisper_cut.py)" % insert)
        dur = fnum(ov.get("duration"), where + ".duration")
        if dur <= EPS:
            die(where + ".duration must be positive")
        insert_in = fnum(ov.get("insert_in", 0.0), where + ".insert_in")
        # A shorter-than-planned insert stitches (stitch's eof_action=pass
        # falls back to the base picture) but silently shrinks the punch-in
        # the member approved on the cut map — say so NOW.
        try:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", insert_disk],
                capture_output=True, text=True)
            idur = float(probe.stdout.strip())
            if idur + EPS < insert_in + dur:
                warn(where + ": insert '%s' is %.3fs but insert_in+duration "
                     "needs %.3fs — the punch-in will run short (base picture "
                     "shows through the tail)" % (insert, idur, insert_in + dur))
        except Exception:
            pass  # unprobeable inserts fail loudly at stitch time instead
        anchor = ov.get("anchor")
        if not isinstance(anchor, dict):
            die(where + " missing 'anchor' object")
        host_id = str(anchor.get("clip") or "")
        bc = by_clip.get(host_id)
        if bc is None:
            die(where + ": anchor clip '%s' is not on the base rail" % host_id)
        if host_id == final["clip"]:
            die(where + ": anchored on the FINAL base clip '%s'. THE CLOSE IS "
                "NEVER COVERED — the ad ends on the approved close beat, clean. "
                "Move the punch-in to an earlier host clip." % host_id)

        has_word = anchor.get("word") is not None
        has_time = anchor.get("time") is not None
        if has_word == has_time:
            die(where + ".anchor needs exactly one of 'word' or 'time'")
        if has_word:
            target = norm_word(anchor["word"])
            occurrence = anchor.get("occurrence", 1)
            if isinstance(occurrence, bool) or not isinstance(occurrence, int) or occurrence < 1:
                die(where + ".anchor.occurrence must be a positive integer")
            offset = fnum(anchor.get("offset", 0.0), where + ".anchor.offset")
            n, start = 0, None
            for w in bc["words"]:
                if isinstance(w, dict) and norm_word(w.get("w", "")) == target:
                    n += 1
                    if n == occurrence:
                        start = fnum(w.get("start"), where + " word.start")
                        break
            if start is None:
                die(where + ": word anchor unresolvable — '%s' occurrence %d "
                    "not found in clip '%s' (found %d occurrence(s)). Cuts "
                    "land on words from the measured timeline; fix the anchor "
                    "or re-check cut_report.json."
                    % (str(anchor["word"]), occurrence, host_id, n))
            t_rel = start + offset
        else:
            t_rel = fnum(anchor["time"], where + ".anchor.time")

        at = rel_to_abs(bc, t_rel, where)
        host_end = bc["start_abs"] + bc["eff"]
        if at < bc["start_abs"] - EPS:
            die(where + ": resolves to %.3f, before its host clip '%s' starts "
                "at %.3f (offset too negative)" % (at, host_id, bc["start_abs"]))
        if at + dur > host_end + EPS:
            die(where + ": crosses its host base clip's join — overlay "
                "[%.3f..%.3f] vs '%s' ending at %.3f. A punch-in rides ONE "
                "host clip's continuing audio; shorten it or re-anchor."
                % (at, at + dur, host_id, host_end))
        out.append({"file": insert, "at": round(at, 3),
                    "duration": round(dur, 3), "insert_in": round(insert_in, 3)})

    out.sort(key=lambda o: o["at"])
    for a, b in zip(out, out[1:]):
        if b["at"] < a["at"] + a["duration"] - EPS:
            die("overlays overlap: [%.3f..%.3f] and [%.3f..%.3f] — one video "
                "rail, one picture at a time"
                % (a["at"], a["at"] + a["duration"], b["at"], b["at"] + b["duration"]))
    # Belt-and-braces: nothing reaches into the final clip's window.
    for o in out:
        if o["at"] + o["duration"] > final["start_abs"] + EPS:
            die("overlay [%.3f..%.3f] covers part of the final base clip "
                "(starts %.3f) — the close is never covered"
                % (o["at"], o["at"] + o["duration"], final["start_abs"]))
    return out


# ---------------------------------------------------------------------------
# THE TYPED CLOSE
# ---------------------------------------------------------------------------

def enforce_typed_close(rail, plan, close_type):
    last = rail[-1]
    gid = last["gen_id"]
    entry = None
    for e in plan.get("entries") or []:
        if isinstance(e, dict) and e.get("kind") == "gen" and str(e.get("gen_id")) == gid:
            entry = e
            break
    if entry is None:
        die("THE TYPED CLOSE: final base clip '%s' traces to gen_id '%s', "
            "which has no gen entry in render_plan.json. The ad must end on "
            "a planned role=\"close\" generation — stills/footage/composites "
            "never close." % (last["clip"], gid))
    role = str(entry.get("role") or "")
    if role != "close":
        die("THE TYPED CLOSE: final base clip '%s' traces to gen '%s' with "
            "role \"%s\", not \"close\". Every ad ends on its format's "
            "approved close beat (close_type=%s) — reorder the base rail so "
            "the close is last." % (last["clip"], gid, role, close_type))


# ---------------------------------------------------------------------------
# RHYTHM: the deterministic cut list and the RHYTHM CARD verdict
# ---------------------------------------------------------------------------

def compute_cut_points(rail, overlays, total):
    pts = []
    for k, bc in enumerate(rail):
        if k < len(rail) - 1:                       # base join (line boundary)
            pts.append(bc["start_abs"] + bc["eff"])
        shift = 0.0
        for c, r in bc["trims"]:                    # trim seam = the jump cut
            pts.append(bc["start_abs"] + c - shift)
            shift += r - c
        for t in bc["internal_cuts"]:               # reconciled sub-shot cuts
            if any(c + EPS < t < r - EPS for c, r in bc["trims"]):
                continue                            # that cut was trimmed out
            if t < POINT_MERGE or t > bc["duration"] - POINT_MERGE:
                continue                            # boundary == the join itself
            pts.append(rel_to_abs(bc, t, "internal cut in '%s'" % bc["clip"]))
    for o in overlays:                              # overlay in + out
        pts.extend([o["at"], o["at"] + o["duration"]])

    uniq = []
    for p in sorted(round(p, 3) for p in pts):
        if p < POINT_MERGE or p > total - POINT_MERGE:
            continue
        if uniq and p - uniq[-1] < POINT_MERGE:
            continue
        uniq.append(p)
    return uniq


def score_rhythm(edl, cut_points, total):
    t_in = edl.get("rhythm_targets")
    if not isinstance(t_in, dict):
        die("edl.rhythm_targets missing — every format's bank RHYTHM CARD "
            "supplies median_max / shot_max / close_exempt")
    median_max = fnum(t_in.get("median_max"), "rhythm_targets.median_max")
    shot_max = fnum(t_in.get("shot_max"), "rhythm_targets.shot_max")
    close_exempt = bool(t_in.get("close_exempt", True))

    edges = [0.0] + cut_points + [round(total, 3)]
    shots = []
    for a, b in zip(edges, edges[1:]):
        d = round(b - a, 3)
        if d > EPS:
            shots.append(d)
    if not shots:
        die("empty timeline — no shots to score")
    median = round(statistics.median(shots), 3)
    if close_exempt and len(shots) > 1:
        max_non_close = round(max(shots[:-1]), 3)   # the held close is legal
    else:
        max_non_close = round(max(shots), 3)
    verdict = ("PASS" if median <= median_max + EPS
               and max_non_close <= shot_max + EPS else "FAIL")
    return {
        "targets": {"median_max": median_max, "shot_max": shot_max,
                    "close_exempt": close_exempt},
        "shots": shots, "median": median,
        "max_non_close": max_non_close, "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Silent detection: loudnorm on a wordless rail only boosts noise
# ---------------------------------------------------------------------------

def plan_is_silent(idx, plan):
    for rec in idx.values():
        if rec["words"]:
            return False
    for e in plan.get("entries") or []:
        if isinstance(e, dict) and e.get("kind") == "gen" and e.get("lines"):
            return False
    return True


# ---------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(
        prog="build_manifest.py",
        description="UGC Studio: resolve edl+render_plan+cut_report into the "
                    "absolute-time manifest.json stitch.sh executes verbatim. "
                    "Enforces the typed close and the overlay laws; records "
                    "the rhythm verdict (stitch refuses on FAIL).")
    p.add_argument("edl")
    p.add_argument("render_plan")
    p.add_argument("cut_report")
    p.add_argument("--out", required=True)
    args = p.parse_args(argv if argv is not None else sys.argv[1:])

    edl = load_json(args.edl, "edl.json")
    plan = load_json(args.render_plan, "render_plan.json")
    report = load_json(args.cut_report, "cut_report.json")

    ad_id = str(edl.get("ad_id") or plan.get("ad_id") or "")
    if not ad_id:
        die("no ad_id in edl.json or render_plan.json")
    if edl.get("ad_id") and plan.get("ad_id") and edl["ad_id"] != plan["ad_id"]:
        warn("ad_id mismatch: edl='%s' vs render_plan='%s' (using edl's)"
             % (edl["ad_id"], plan["ad_id"]))
    close_type = str(edl.get("close_type") or plan.get("close_type") or "")
    if not close_type:
        die("no close_type in edl.json or render_plan.json — the close is TYPED")

    idx, clips_dir = index_report(report, args.cut_report)
    rail, total = resolve_base(edl, idx, clips_dir)
    overlays = resolve_overlays(edl, rail, os.path.dirname(args.edl) or ".")
    enforce_typed_close(rail, plan, close_type)
    cut_points = compute_cut_points(rail, overlays, total)
    rhythm = score_rhythm(edl, cut_points, total)

    manifest = {
        "ad_id": ad_id,
        "close_type": close_type,
        "base": [{"file": bc["file"], "duration": round(bc["duration"], 3),
                  "trims": bc["trims"]} for bc in rail],
        "overlays": overlays,
        "cut_points": cut_points,
        "rhythm": rhythm,
        "audio": ({"loudnorm": False} if plan_is_silent(idx, plan)
                  else {"loudnorm": True, "target_lufs": TARGET_LUFS}),
        "expected_total": round(total, 3),
    }

    try:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        die("could not write manifest to " + args.out + ": " + str(exc))

    print("Wrote manifest: " + args.out)
    print("  base rail : %d clip(s), %.3fs total (%d interior trim(s))"
          % (len(rail), total, sum(len(bc["trims"]) for bc in rail)))
    print("  video rail: %d punch-in overlay(s)" % len(overlays))
    print("  close     : '%s' (typed %s) — verified role=close"
          % (rail[-1]["clip"], close_type))
    print("  audio     : loudnorm=%s" % str(manifest["audio"]["loudnorm"]).lower())
    print("  rhythm    : shots=[%s]" % ", ".join("%.2f" % s for s in rhythm["shots"]))
    print("              median=%.3f (max %.1f)  max_non_close=%.3f (max %.1f)"
          "  verdict=%s"
          % (rhythm["median"], rhythm["targets"]["median_max"],
             rhythm["max_non_close"], rhythm["targets"]["shot_max"],
             rhythm["verdict"]))
    if rhythm["verdict"] != "PASS":
        print("RHYTHM FAIL (recorded in the manifest): stitch.sh will REFUSE "
              "this manifest. Fix edit-side — add punch-in overlays, interior "
              "trims, or spine slices; never re-render for timing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
