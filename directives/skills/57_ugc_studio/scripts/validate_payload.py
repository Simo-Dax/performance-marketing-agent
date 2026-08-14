#!/usr/bin/env python3
"""
validate_payload.py  --  UGC Studio whole-plan preflight for render_plan.json.

Runs once at Step 5, after the orchestrator authors the plan and BEFORE any voice
cut, still, or generation is dispatched: one pass over the entire procurement
contract so the pipeline never spends credits on an entry that violates the
render laws. Every rule below is verified physics (references/render-laws.md).

PLAN LEVEL
  - format / close_type / backend from their typed enums; close_type must be the
    format's default close (cta / delight / display-loop / button) unless the plan
    sets "close_type_explicit": true -- QC enforces "ends on the APPROVED close
    beat", never a blanket literal CTA.
  - exactly ONE entry carries role "close" (build_manifest refuses a timeline
    whose final clip does not trace to it) and exactly ONE gen sets
    is_identity_checkpoint (it renders ALONE first and must contain the clean
    bare face frame -- the whole batch is graded against it).
  - every handle an entry references exists in "inputs" (entries reference stable
    handles, never raw paths; every shown variant/outfit gets its own handle +
    real photo).
  - wps in [2.4, 4.4] -- the sprint formats' measured band tops at 4.4.

kind "gen" (one Seedance 2.0 generation)
  - duration is an INTEGER 4..9 -- never "auto", never 10+ (10s+ single
    generations produce very bad output, owner-verified; longer content = MORE
    generations).
  - attachment rules by beat_type: talking / character_broll carry face + body
    (identity = the re-sent reference bytes; a product handle is welcome but must
    exist in inputs -- label fidelity comes only from the real photo);
    product_only carries the product and NO character; green_screen carries
    face + body and NO product (props near the face render as AI slop,
    owner-verified) and its prompt must say "chroma"/"green screen" or the model
    drifts to grass green and the key deletes the person (live-verified).
  - on backend "higgsfield" every gen WITH lines names its OWN .wav voice_cut:
    one voice file reused across gens collides on the lazy _sfx audio dedup and
    fails silently; re-uploading the same clip does NOT dodge it. fal has no
    dedup, so the check is skipped there.
  - silent gens (no lines) instead REQUIRE the sub-shot map with a "clip" name on
    every item -- plan-cut mode has no words to cut on; the map IS the cut list.
  - a gen planning 2+ lines or 2+ sub_shots must ship a prompt_file that EXISTS
    and carries hard-cut markup ("HARD CUT" and/or [t..] / [0-3s] timestamps): a
    planned multi-shot gen with a collapsed prompt renders one continuous take
    and the credits are gone before anyone notices.
  - sub_shots: max 3 (one clear action per shot -- more morphs), first t 0.0,
    strictly increasing, every offset strictly inside the duration.

kind "still"   source_photo is a real-photo handle in inputs (stills generate
               FROM real photos, never from text); duration >= 1s; animate is a
               motion-only prompt string or null (null = static cut-in).
kind "footage" source handle exists in inputs -- moving UI is NEVER generated.
kind "composite"
  - pattern from the typed four; gen_id / footage_id reference sibling entries.
  - chromakey / matting / pip key a green_screen gen ONLY.
  - on backend "fal" pattern "matting" FAILS outright: Path C has no Higgsfield
    matting -- the lane falls back to chromakey (on the SAMPLED green) or pip.

CROSS  gen_ids unique; clip names unique across the WHOLE plan (every clip is a
       file, clips/<clip>.mp4 -- a duplicate silently overwrites a cut).

Relative prompt_file paths resolve against the plan file's own folder ($WORK).

Usage:
    python3 validate_payload.py render_plan.json

Exit 0 on PASS, 1 on any FAIL (every failure printed, actionable). Stdlib only.
"""

import argparse
import json
import os
import re
import sys

FORMATS = ("testimonial", "before-after", "unboxing", "direct-to-camera")
CLOSE_TYPES = ("cta", "delight", "display-loop", "button")
DEFAULT_CLOSE = {                     # the typed close each format's bank measured
    "testimonial": "cta",             # on-camera offer close (~4.3s legal hold)
    "before-after": "delight",        # delight / naked proof
    "unboxing": "display-loop",       # ~6s silent display loop
    "direct-to-camera": "button",     # ~1.9s narrative button
}
BACKENDS = ("higgsfield", "fal")
BEAT_TYPES = ("talking", "character_broll", "product_only", "green_screen")
PATTERNS = ("chromakey", "matting", "pip", "fullframe")
KEYED_PATTERNS = ("chromakey", "matting", "pip")   # all three key a green talker
DURATION_MIN = 4
DURATION_MAX = 9                      # UNDER 10 seconds, hard rule
WPS_MIN = 2.4                         # below this the read drags
WPS_MAX = 4.4                         # sprint formats' band top
SUB_SHOTS_MAX = 3                     # 2-3 hard-cut sub-shots max, one action each

# Hard-cut markup a multi-shot prompt must carry: "HARD CUT" between segments
# and/or bracketed timestamps like "[0-3s]" / "[t=3.0]".
_MARKUP_RE = re.compile(r"hard\s*cut|\[\s*[t\d]", re.IGNORECASE)
# Green-lane prompt wording that keeps the render key-able.
_GREEN_RE = re.compile(r"chroma|green\s*screen", re.IGNORECASE)


def _as_list(v):
    return v if isinstance(v, list) else []


def _as_number(v, default=None):
    if isinstance(v, bool):
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _handle_class(handle):
    """Classify an inputs handle by its naming convention (face / body_outfit2 /
    product_variant_coconut ...)."""
    h = (handle if isinstance(handle, str) else "").strip().lower()
    if h.startswith("face"):
        return "face"
    if h.startswith("body"):
        return "body"
    if h.startswith("product"):
        return "product"
    return "other"


_ID_KEY = {"gen": "gen_id", "still": "still_id",
           "footage": "footage_id", "composite": "composite_id"}


def _entry_name(entry, idx):
    if not isinstance(entry, dict):
        return "entries[%d]" % idx
    kind = entry.get("kind")
    # the entry's OWN id key first (a composite also carries a gen_id REFERENCE)
    keys = [_ID_KEY[kind]] if kind in _ID_KEY else list(_ID_KEY.values())
    for key in keys:
        v = entry.get(key)
        if isinstance(v, str) and v.strip():
            return '%s "%s"' % (kind if isinstance(kind, str) else "entry", v)
    return "%s entries[%d]" % (kind if isinstance(kind, str) else "entry", idx)


def _read_text(path, plan_dir):
    p = path if os.path.isabs(path) else os.path.join(plan_dir, path)
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def _register_clip(clip, owner, clip_owner, failures):
    if clip in clip_owner and clip_owner[clip] != owner:
        failures.append(
            'FAIL [duplicate clip]: clip "%s" is named by both %s and %s. Every clip '
            "is a file (clips/<clip>.mp4) -- clip names are unique across the WHOLE "
            "plan or one cut silently overwrites another." % (clip, clip_owner[clip], owner))
    elif clip in clip_owner:
        failures.append(
            'FAIL [duplicate clip]: %s names clip "%s" twice. Every clip is a file '
            "(clips/<clip>.mp4) -- clip names are unique across the WHOLE plan."
            % (owner, clip))
    else:
        clip_owner[clip] = owner


def _check_gen_duration(name, entry, failures):
    """Integer 4..9 or bust. Returns the int duration when valid, else None."""
    duration = entry.get("duration", None)
    if duration is None:
        failures.append(
            "FAIL [duration]: %s has no duration. EVERY generation is an explicit "
            'integer 4..9 seconds -- never "auto", never 10+.' % name)
        return None
    num = _as_number(duration)
    if num is None:
        failures.append(
            "FAIL [duration]: %s duration %r is not a number. Request an explicit "
            'integer 4..9 -- never "auto".' % (name, duration))
        return None
    if num != int(num):
        failures.append(
            "FAIL [duration]: %s duration %g is not an integer. Duration is an "
            "integer 4..9." % (name, num))
        return None
    di = int(num)
    if not (DURATION_MIN <= di <= DURATION_MAX):
        failures.append(
            "FAIL [duration in 4..9]: %s requests %d s, outside 4..9. 10s+ single "
            "generations produce very bad output (owner-verified); longer content "
            "means MORE generations, and sub-3.5s beats merge as sub-shots."
            % (name, di))
        return None
    return di


def _check_gen(entry, name, inputs, backend, plan_dir, failures, clip_owner):
    di = _check_gen_duration(name, entry, failures)

    # -- attachments: every images item is a handle into inputs -----------------
    classes = {"face": 0, "body": 0, "product": 0}
    for h in _as_list(entry.get("images")):
        if not (isinstance(h, str) and h.strip()):
            failures.append(
                "FAIL [images]: %s has a non-string image handle %r; images list "
                'input HANDLES (keys of plan "inputs"), never raw paths.' % (name, h))
            continue
        cls = _handle_class(h)
        if h not in inputs:
            extra = (" The product renders only from its real photo -- add that "
                     "photo to inputs under this handle." if cls == "product" else "")
            failures.append(
                'FAIL [unknown handle]: %s references images handle "%s" but plan '
                "inputs has no such key.%s" % (name, h, extra))
        if cls in classes:
            classes[cls] += 1

    beat = entry.get("beat_type")
    if beat not in BEAT_TYPES:
        failures.append(
            "FAIL [beat_type]: %s beat_type %r is not one of %s."
            % (name, beat, "|".join(BEAT_TYPES)))
    elif beat in ("talking", "character_broll"):
        if classes["face"] < 1:
            failures.append(
                "FAIL [face handle required]: %s (beat_type %s) attaches no face "
                "handle. The face reference is the identity anchor on every "
                "character generation." % (name, beat))
        if classes["body"] < 1:
            failures.append(
                "FAIL [body handle required]: %s (beat_type %s) attaches no body "
                "handle. The body reference is the identity anchor on every "
                "character generation." % (name, beat))
    elif beat == "product_only":
        if classes["product"] < 1:
            failures.append(
                "FAIL [product handle required]: %s is product_only but attaches no "
                "product handle. The product renders from its real photo, never from "
                "a text description." % name)
        if classes["face"] > 0 or classes["body"] > 0:
            failures.append(
                "FAIL [product_only has character]: %s is product_only but attaches "
                "a face/body handle. Product-only b-roll carries the product "
                "reference ONLY; a shot featuring the character is beat_type "
                "character_broll (face + body)." % name)
    else:  # green_screen
        if classes["face"] < 1 or classes["body"] < 1:
            failures.append(
                "FAIL [face+body required]: %s (green_screen) needs both a face and "
                "a body handle -- it is a chest-up TALKER, and wardrobe is checked "
                "non-green on the body reference FIRST." % name)
        if classes["product"] > 0:
            failures.append(
                "FAIL [green_screen no product]: %s attaches a product handle. "
                "Green-screen gens carry NO props -- props near the face render as "
                "AI slop (owner-verified). Route the product to a still-insert or "
                "the b-roll lane." % name)
        pf = entry.get("prompt_file")
        if isinstance(pf, str) and pf.strip():
            text = _read_text(pf, plan_dir)
            if text is None:
                failures.append(
                    'FAIL [green wording]: %s prompt_file "%s" not found (resolved '
                    "against the plan's folder), so the chroma wording cannot be "
                    "verified." % (name, pf))
            elif not _GREEN_RE.search(text):
                failures.append(
                    'FAIL [green wording]: %s prompt "%s" never says "chroma" or '
                    '"green screen". Without the bright-saturated-chroma wording the '
                    "model drifts to grass green and the key deletes the person "
                    "before the green (live-verified)." % (name, pf))

    # -- lines and their clip names ---------------------------------------------
    lines = _as_list(entry.get("lines"))
    for i, ln in enumerate(lines):
        clip = ln.get("clip") if isinstance(ln, dict) else None
        if not (isinstance(clip, str) and clip.strip()):
            failures.append(
                'FAIL [clip name]: %s lines[%d] has no "clip" name; whisper_cut.py '
                "writes clips/<clip>.mp4 from it." % (name, i))
        else:
            _register_clip(clip.strip(), name, clip_owner, failures)

    # -- sub_shots: structure, and clip registration -----------------------------
    sub_shots = _as_list(entry.get("sub_shots"))
    ts = []
    for i, ss in enumerate(sub_shots):
        if not isinstance(ss, dict):
            failures.append(
                "FAIL [sub_shots]: %s sub_shots[%d] is not an object; each item is "
                '{"t": <sec>, "shot": "..."}.' % (name, i))
            continue
        t = _as_number(ss.get("t"))
        if t is None:
            failures.append(
                'FAIL [sub_shots]: %s sub_shots[%d] has no numeric "t" (the expected '
                "internal hard-cut offset in seconds)." % (name, i))
        else:
            ts.append(t)
        clip = ss.get("clip")
        if isinstance(clip, str) and clip.strip():
            _register_clip(clip.strip(), name, clip_owner, failures)
    if len(sub_shots) > SUB_SHOTS_MAX:
        failures.append(
            "FAIL [sub_shots max 3]: %s plans %d sub-shots; 2-3 hard-cut sub-shots "
            "per generation MAXIMUM, one clear action per shot -- more morphs."
            % (name, len(sub_shots)))
    if ts and len(ts) == len(sub_shots):
        if abs(ts[0]) > 1e-9:
            failures.append(
                "FAIL [sub_shots t0]: %s first sub-shot t is %g; the first item is "
                "always t 0.0 (the generation opens IN shot 1)." % (name, ts[0]))
        for a, b in zip(ts, ts[1:]):
            if b <= a:
                failures.append(
                    "FAIL [sub_shots order]: %s sub-shot offsets must strictly "
                    "increase (%g -> %g)." % (name, a, b))
                break
        if di is not None:
            bad = [t for t in ts if t >= di]
            if bad:
                failures.append(
                    "FAIL [sub_shots inside duration]: %s plans a sub-shot at t=%g "
                    "in a %d s generation; every internal cut lands strictly inside "
                    "the clip." % (name, bad[0], di))

    # -- voice: per-gen unique cut on Higgsfield paths; silent gens use the map --
    silent = len(lines) == 0
    if not silent and backend != "fal":
        vc = entry.get("voice_cut")
        if not (isinstance(vc, str) and vc.strip()):
            failures.append(
                "FAIL [voice_cut required]: %s speaks lines on backend higgsfield "
                "but names no voice_cut. Run make_voice_cuts.py and set voice_cut "
                "to this generation's OWN WAV -- one voice file reused across gens "
                "collides on the lazy _sfx audio dedup and fails silently, and "
                "re-uploading the same clip does NOT dodge it (the fingerprint is "
                "on the speech)." % name)
        elif not vc.strip().lower().endswith(".wav"):
            failures.append(
                "FAIL [voice_cut format]: %s voice_cut %r is not a .wav; use the "
                "clean per-gen WAV make_voice_cuts.py wrote (mono 44.1k pcm_s16le)."
                % (name, vc))
    if silent:
        if not sub_shots:
            failures.append(
                "FAIL [silent gen sub_shots]: %s has no lines and no sub_shots. A "
                "silent gen cuts in plan-cut mode -- the sub-shot map (each item "
                'with a "clip" name) is its only cut list.' % name)
        else:
            for i, ss in enumerate(sub_shots):
                clip = ss.get("clip") if isinstance(ss, dict) else None
                if not (isinstance(clip, str) and clip.strip()):
                    failures.append(
                        'FAIL [silent gen clip names]: %s sub_shots[%d] has no '
                        '"clip" name. Silent gens have no lines to name clips -- '
                        "every sub-shot names its cut output clips/<clip>.mp4."
                        % (name, i))

    # -- planned multi-shot gens must ship the hard-cut markup BEFORE credits ----
    if len(lines) >= 2 or len(sub_shots) >= 2:
        pf = entry.get("prompt_file")
        if not (isinstance(pf, str) and pf.strip()):
            failures.append(
                "FAIL [sub-shot markup]: %s plans %d line(s) / %d sub-shot(s) but "
                "names no prompt_file. A multi-shot gen ships a prompt with "
                'timestamped hard-cut lines ("[0-3s] ... HARD CUT [3-8s] ...") or '
                "it renders one continuous take." % (name, len(lines), len(sub_shots)))
        else:
            text = _read_text(pf, plan_dir)
            if text is None:
                failures.append(
                    'FAIL [sub-shot markup]: %s prompt_file "%s" not found (resolved '
                    "against the plan's folder). The multi-shot prompt must exist at "
                    "validation time -- it is checked BEFORE credits are spent."
                    % (name, pf))
            elif not _MARKUP_RE.search(text):
                failures.append(
                    'FAIL [sub-shot markup]: %s plans a multi-shot gen but prompt '
                    '"%s" carries no hard-cut markup (no "HARD CUT", no [t..] '
                    "timestamp). A collapsed prompt renders one continuous take and "
                    "the planned cuts never exist -- fix the prompt, not the render."
                    % (name, pf))


def _check_still(entry, name, inputs, failures):
    sp = entry.get("source_photo")
    if not (isinstance(sp, str) and sp.strip()):
        failures.append(
            "FAIL [source_photo]: %s names no source_photo handle. Stills are "
            "generated FROM a real photo in inputs, never from text." % name)
    elif sp not in inputs:
        failures.append(
            'FAIL [unknown handle]: %s source_photo "%s" is not a key of plan '
            "inputs. Every shown state/variant gets its own handle + real photo."
            % (name, sp))
    dur = _as_number(entry.get("duration"))
    if dur is None or dur < 1:
        failures.append(
            "FAIL [still duration]: %s duration %r; a still-insert books at least "
            "1 s of timeline (the EDL may use less)." % (name, entry.get("duration")))
    if "animate" in entry:
        an = entry.get("animate")
        if an is not None and not isinstance(an, str):
            failures.append(
                "FAIL [animate]: %s animate %r must be a MOTION-ONLY prompt string "
                "or null (null = static cut-in, Ken-Burns applied at composite "
                "time)." % (name, an))


def _check_footage(entry, name, inputs, failures):
    src = entry.get("source")
    if not (isinstance(src, str) and src.strip()):
        failures.append(
            "FAIL [footage source]: %s names no source handle. Real footage "
            "conforms from a member recording in inputs -- moving UI is NEVER "
            "generated." % name)
    elif src not in inputs:
        failures.append(
            'FAIL [unknown handle]: %s source "%s" is not a key of plan inputs.'
            % (name, src))


def _check_composite(entry, name, gens_by_id, footage_ids, backend, failures):
    pattern = entry.get("pattern")
    if pattern not in PATTERNS:
        failures.append(
            "FAIL [pattern]: %s pattern %r is not one of %s."
            % (name, pattern, "|".join(PATTERNS)))
        pattern = None
    if backend == "fal" and pattern == "matting":
        failures.append(
            'FAIL [matting on fal]: %s uses pattern "matting" on backend fal. Path '
            "C has NO Higgsfield matting -- the green lane falls back to chromakey "
            "(keyed on the SAMPLED green) or pip there; route this composite "
            "accordingly." % name)
    gid = entry.get("gen_id")
    if gid is not None and gid not in gens_by_id:
        failures.append(
            'FAIL [unknown gen_id]: %s references gen_id %r but no kind "gen" entry '
            "has that id." % (name, gid))
    fid = entry.get("footage_id")
    if fid is not None and fid not in footage_ids:
        failures.append(
            'FAIL [unknown footage_id]: %s references footage_id %r but no kind '
            '"footage" entry has that id.' % (name, fid))
    if pattern in KEYED_PATTERNS:
        if gid is None:
            failures.append(
                'FAIL [composite gen]: %s pattern "%s" keys a talker over footage '
                "but names no gen_id." % (name, pattern))
        elif gid in gens_by_id and gens_by_id[gid].get("beat_type") != "green_screen":
            failures.append(
                'FAIL [composite beat_type]: %s pattern "%s" references gen "%s" '
                "whose beat_type is %r -- chromakey/matting/pip key a green_screen "
                "gen ONLY (the chest-up chroma talker)."
                % (name, pattern, gid, gens_by_id[gid].get("beat_type")))


def validate(plan, plan_dir):
    failures = []

    # ---- plan level ------------------------------------------------------------
    ad_id = plan.get("ad_id")
    if not (isinstance(ad_id, str) and ad_id.strip()):
        failures.append(
            "FAIL [ad_id]: missing or empty. The ad_id names the work folder and "
            "every output file.")

    fmt = plan.get("format")
    if fmt not in FORMATS:
        failures.append(
            "FAIL [format]: %r is not one of %s." % (fmt, "|".join(FORMATS)))

    close = plan.get("close_type")
    if close not in CLOSE_TYPES:
        failures.append(
            "FAIL [close_type]: %r is not one of %s. The close is TYPED per format; "
            'QC enforces "ends on the approved close beat".'
            % (close, "|".join(CLOSE_TYPES)))
    elif fmt in DEFAULT_CLOSE and close != DEFAULT_CLOSE[fmt] \
            and not plan.get("close_type_explicit"):
        failures.append(
            'FAIL [close_type default]: format "%s" closes on "%s" by default but '
            'the plan says "%s". A deliberate off-default close sets '
            '"close_type_explicit": true.' % (fmt, DEFAULT_CLOSE[fmt], close))

    backend = str(plan.get("backend", "higgsfield") or "higgsfield").strip().lower()
    if backend not in BACKENDS:
        failures.append(
            "FAIL [backend]: %r is not higgsfield|fal." % (plan.get("backend"),))
        backend = "higgsfield"

    wnum = _as_number(plan.get("wps"))
    if wnum is None:
        failures.append(
            "FAIL [wps]: %r is not a number. wps is the format band's approved "
            "words-per-second, in [2.4, 4.4]." % (plan.get("wps"),))
    elif not (WPS_MIN <= wnum <= WPS_MAX):
        failures.append(
            "FAIL [wps in 2.4..4.4]: wps %.2f is outside the band -- below 2.4 the "
            "read DRAGS, above 4.4 it outruns even the sprint formats' measured "
            "winners." % wnum)

    inputs = plan.get("inputs")
    if not isinstance(inputs, dict):
        failures.append(
            "FAIL [inputs]: missing or not an object. inputs maps stable handles to "
            "real files; entries reference handles, never raw paths.")
        inputs = {}

    entries = plan.get("entries")
    if not isinstance(entries, list) or not entries:
        failures.append(
            "FAIL [entries]: missing or empty. A plan procures at least one entry.")
        entries = []

    # ---- first pass: index gens and footage for cross-references ----------------
    gens_by_id = {}
    footage_ids = set()
    gen_id_at = {}
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        if entry.get("kind") == "gen":
            gid = entry.get("gen_id")
            if not (isinstance(gid, str) and gid.strip()):
                failures.append(
                    'FAIL [gen_id]: entries[%d] (kind "gen") has no gen_id; every '
                    "generation is addressed by a stable id (payloads, voice cuts, "
                    "downloads all key on it)." % idx)
            elif gid in gen_id_at:
                failures.append(
                    'FAIL [duplicate gen_id]: gen_id "%s" appears at entries[%d] and '
                    "entries[%d]; gen_ids are unique across the plan."
                    % (gid, gen_id_at[gid], idx))
            else:
                gen_id_at[gid] = idx
                gens_by_id[gid] = entry
        elif entry.get("kind") == "footage":
            fid = entry.get("footage_id")
            if isinstance(fid, str) and fid.strip():
                footage_ids.add(fid)

    # ---- second pass: per-entry checks ------------------------------------------
    closes = []
    checkpoints = []
    clip_owner = {}
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            failures.append("FAIL [entry]: entries[%d] is not an object." % idx)
            continue
        name = _entry_name(entry, idx)
        kind = entry.get("kind")
        if entry.get("role") == "close":
            closes.append(name)
        if kind == "gen":
            if entry.get("is_identity_checkpoint"):
                checkpoints.append(name)
            _check_gen(entry, name, inputs, backend, plan_dir, failures, clip_owner)
        elif kind == "still":
            _check_still(entry, name, inputs, failures)
        elif kind == "footage":
            _check_footage(entry, name, inputs, failures)
        elif kind == "composite":
            _check_composite(entry, name, gens_by_id, footage_ids, backend, failures)
        else:
            failures.append(
                "FAIL [kind]: entries[%d] kind %r is not gen|still|footage|composite."
                % (idx, kind))

    # ---- cross checks ------------------------------------------------------------
    if len(closes) == 0:
        failures.append(
            'FAIL [close]: no entry has role "close". Every ad ends on ONE typed '
            "close beat -- build_manifest refuses a timeline whose final clip does "
            "not trace to it.")
    elif len(closes) > 1:
        failures.append(
            'FAIL [close]: %d entries claim role "close" (%s); exactly ONE.'
            % (len(closes), ", ".join(closes)))

    if len(checkpoints) == 0:
        failures.append(
            "FAIL [identity checkpoint]: no gen sets is_identity_checkpoint true. "
            "Exactly ONE gen renders ALONE first and must contain the clean bare "
            "face frame -- the whole batch is graded against it.")
    elif len(checkpoints) > 1:
        failures.append(
            "FAIL [identity checkpoint]: %d gens set is_identity_checkpoint (%s); "
            "exactly ONE renders alone first." % (len(checkpoints), ", ".join(checkpoints)))

    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate_payload.py",
        description="UGC Studio whole-plan preflight: validate every "
                    "render_plan.json entry (gen/still/footage/composite) against "
                    "the render laws before any credits are spent.")
    parser.add_argument("plan", help="render_plan.json (the whole plan, all kinds)")
    args = parser.parse_args(argv)

    try:
        with open(args.plan, "r", encoding="utf-8") as fh:
            plan = json.load(fh)
    except FileNotFoundError:
        print("FAIL [plan file]: %s not found." % args.plan)
        return 1
    except json.JSONDecodeError as exc:
        print("FAIL [plan file]: %s is not valid JSON (%s)." % (args.plan, exc))
        return 1
    except OSError as exc:
        print("FAIL [plan file]: cannot read %s (%s)." % (args.plan, exc))
        return 1

    if not isinstance(plan, dict):
        print("FAIL [plan file]: top-level JSON must be an object, got %s."
              % type(plan).__name__)
        return 1

    plan_dir = os.path.dirname(os.path.abspath(args.plan))
    failures = validate(plan, plan_dir)
    if failures:
        for line in failures:
            print(line)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
