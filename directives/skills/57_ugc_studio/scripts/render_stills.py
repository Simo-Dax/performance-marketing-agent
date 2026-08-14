#!/usr/bin/env python3
"""
render_stills.py - still-insert lane preparer (UGC Studio).

WHY THIS EXISTS (render laws, lane 2): every fidelity-critical beat -- labels,
variant runs, box stacks, open/eaten states, before-states, product-touches-lens
-- routes through a 2K STILL generated FROM the member's real photo, because
label fidelity comes ONLY from an attached real photo (text-to-image invents
labels) and stills are cheap enough to member-approve BEFORE any video credit
is spent. When a still animates, the still carries the LOOK and the prompt
carries ONLY the MOTION -- restating subject or framing in an image-to-video
prompt invites the model to redraw both.

This script PREPARES and TRACKS the lane; it never dispatches. For every
kind=="still" entry in render_plan.json it:
  1. resolves `source_photo` through inputs{} to a real file and HARD-FAILS if
     the photo is missing -- a still never builds from text,
  2. writes prompts/still_<still_id>.txt in the house still shape (an existing
     prompt file is left verbatim) plus, when `animate` is set, the MOTION-ONLY
     prompts/still_<still_id>_motion.txt,
  3. writes stills/stills_plan.json tracking each still's expected outputs,
  4. prints the member checklist. Re-running after stills/<still_id>.png lands
     flips that still's status to "rendered" -- idempotent, no prompt rewrites.

Actual rendering goes through the order's chosen path (A manual paste, B CLI,
C fal, D web UI) with the source photo attached as the image reference; the
member approves every still before video spend.

render_plan.json still entry (see references/pipeline-contracts.md #1):

  { "kind": "still",
    "still_id": "label_macro_coconut",
    "source_photo": "product_variant_coconut",
    "prompt_file": "prompts/still_label_macro_coconut.txt",
    "animate": "slow 4% push-in",
    "duration": 2 }

Usage: python3 render_stills.py render_plan.json work_dir stills_dir
  work_dir is the ad folder ($WORK); relative plan paths resolve against it.
"""
import json
import os
import sys

HOUSE_SHAPE = ("A 2K photorealistic product still built from the attached real photo. "
               "%s. Keep every label, color and proportion exactly as the reference "
               "photo. No on-screen text or captions.")
MOTION_SHAPE = "%s. The subject and framing stay exactly as the input image."
DISPATCH_NOTE = ("render via the order's chosen path, attach the source photo as the "
                 "image reference, approve before video spend")


def _resolve(work, rel):
    if not rel:
        return None
    if os.path.isabs(rel):
        return rel if os.path.exists(rel) else None
    cand = os.path.join(work, rel)
    return cand if os.path.exists(cand) else None


def _fragment(text):
    """One sentence fragment, no trailing period (the shape adds its own)."""
    return str(text).strip().rstrip(".") if text else ""


def _write_once(path, text):
    """Write only if absent -- an existing prompt is member-approved territory."""
    if os.path.exists(path):
        return False
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return True


def main():
    if len(sys.argv) < 4:
        sys.stderr.write("usage: render_stills.py render_plan.json work_dir stills_dir\n")
        return 2
    plan_path, work, stills_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        with open(plan_path, encoding="utf-8") as f:
            plan = json.load(f)
    except Exception as e:
        sys.stderr.write("FAIL: could not read plan %s (%s)\n" % (plan_path, e))
        return 1
    if not isinstance(plan, dict):
        sys.stderr.write("FAIL: %s is not a render_plan object\n" % plan_path)
        return 1
    if not os.path.isdir(work):
        sys.stderr.write("FAIL: work_dir %s is not a directory\n" % work)
        return 1

    inputs = plan.get("inputs") or {}
    entries = plan.get("entries") or []
    stills = [e for e in entries if isinstance(e, dict) and e.get("kind") == "still"]

    # ---- validate EVERY still before writing anything: the real-photo gate ----
    problems, seen, todo = [], set(), []
    for e in stills:
        sid = e.get("still_id")
        if not sid:
            problems.append("a still entry has no still_id: %s" % json.dumps(e)[:100])
            continue
        if sid in seen:
            problems.append("duplicate still_id '%s' -- outputs would collide" % sid)
            continue
        seen.add(sid)
        handle = e.get("source_photo")
        if not handle:
            problems.append("still '%s': no source_photo handle -- a still ALWAYS "
                            "builds from a real photo, never from text" % sid)
            continue
        rel = inputs.get(handle)
        if not rel:
            problems.append("still '%s': source_photo handle '%s' is not in the "
                            "plan's inputs{}" % (sid, handle))
            continue
        photo = _resolve(work, rel)
        if not photo:
            problems.append("still '%s': source photo MISSING -- handle '%s' -> %s "
                            "does not exist under %s" % (sid, handle, rel, work))
            continue
        todo.append((e, sid, os.path.abspath(photo)))
    if problems:
        sys.stderr.write("FAIL: %d problem(s) in the still lane -- nothing written:\n"
                         % len(problems))
        for p in problems:
            sys.stderr.write("  - %s\n" % p)
        return 1

    os.makedirs(stills_dir, exist_ok=True)
    if not stills:
        plan_out = os.path.join(stills_dir, "stills_plan.json")
        with open(plan_out, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
            f.write("\n")
        print("no kind=\"still\" entries in %s -- still lane empty (%s written)"
              % (plan_path, plan_out))
        return 0

    # ---- prepare prompts + track status ----
    rows, n_rendered = [], 0
    print("STILL LANE -- %s -- %d still(s)\n" % (plan.get("ad_id", "?"), len(todo)))
    for e, sid, photo in todo:
        default_rel = "prompts/still_%s.txt" % sid
        declared = e.get("prompt_file")
        if declared and _resolve(work, declared):
            prompt_rel = declared            # exists: leave it verbatim
        else:
            prompt_rel = default_rel
            shot = _fragment(e.get("shot")) or ("A clean, tightly framed shot: %s"
                                                % sid.replace("_", " ").replace("-", " "))
            _write_once(os.path.join(work, prompt_rel), HOUSE_SHAPE % shot)

        animate = _fragment(e.get("animate"))
        motion_rel = None
        if animate:
            motion_rel = "prompts/still_%s_motion.txt" % sid
            _write_once(os.path.join(work, motion_rel), MOTION_SHAPE % animate)

        png_path = os.path.join(stills_dir, "%s.png" % sid)
        mp4_path = os.path.join(stills_dir, "%s.mp4" % sid)
        rendered = os.path.exists(png_path)
        n_rendered += 1 if rendered else 0
        rows.append({
            "still_id": sid,
            "source_photo_path": photo,
            "prompt_file": prompt_rel,
            "motion_prompt_file": motion_rel,
            "duration": e.get("duration", 2),
            "expected_output": "stills/%s.png" % sid,
            "expected_motion_output": ("stills/%s.mp4" % sid) if animate else None,
            "status": "rendered" if rendered else "pending_render",
        })

        print("[%s] %s  (%ss, %s)" % ("rendered" if rendered else "pending ", sid,
                                      e.get("duration", 2),
                                      ("animated: %s" % animate) if animate
                                      else "static -- Ken-Burns at composite"))
        print("    photo : %s" % photo)
        print("    prompt: %s" % prompt_rel)
        if motion_rel:
            print("    motion: %s" % motion_rel)
        print("    output: stills/%s.png%s" % (sid, (" + stills/%s.mp4" % sid) if animate else ""))
        if rendered and animate and not os.path.exists(mp4_path):
            print("    note  : still approved-renderable; motion clip stills/%s.mp4 "
                  "not yet present" % sid)
        print()

    plan_out = os.path.join(stills_dir, "stills_plan.json")
    with open(plan_out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
        f.write("\n")
    print("plan    : %s" % plan_out)
    print("dispatch: %s" % DISPATCH_NOTE)
    print("%d/%d rendered, %d pending" % (n_rendered, len(rows), len(rows) - n_rendered))
    return 0


if __name__ == "__main__":
    sys.exit(main())
