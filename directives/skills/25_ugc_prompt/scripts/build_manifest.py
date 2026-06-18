#!/usr/bin/env python3
"""
build_manifest.py — Seedance 2.0 Andromeda UGC assembly manifest builder.

Reads a spec.json (concept, niche, framework, character refs, the shared body
shots, and the 4 ads) and writes assembly-manifest.json per the LOCKED schema:

  {
    concept, niche, date, fps:30, resolution:"1080x1920", media_type:"video",
    framework, voice_ref_clip,
    character:{face_image, body_image, product_image},
    body:{ shots:[{shot_id, clip, words, word_count, seconds}] },
    variants:[ {
      variant_id, verbal_hook, visual_hook, hook_clip,
      broll_set:[clip...],
      ordered_timeline:[{role, clip, trim_in, trim_out}],   # MUST end on the CTA body beat
      total_seconds, distinctness_fingerprint
    } ]
  }

LOCKED MODEL baked into this builder (do not contradict):
  - There is NO voice_track. The same voice clip drove every clip; each keeps its
    own audio. This file refuses to emit or accept a voice_track key.
  - Identity = the same face + body bytes on character generations. B-ROLLS are
    product-only (no character) — at the manifest level they are just clip paths.
  - Distinctness comes from 4 UNIQUE hooks + a b-roll-COUNT ladder (0/1/2/2), not
    from hook length (there is NO 4/6/8/10 ladder). The fingerprint is a sha256 of
    RENDER-AFFECTING axes ONLY: visual_hook + sorted broll_set + b-roll count +
    b-roll placement indices + ordered roles, truncated to 16 hex chars. The
    free-text verbal_hook is excluded.
  - EVERY ad ENDS ON THE CTA: the last entry of every ordered_timeline must be a
    'body' role (the CTA beat is the last body shot), and no 'broll' may sit after
    the last 'body'. This builder enforces that.
  - Every generation is under 10s (body shot seconds are integers 4..9).

Stdlib only. Usage:
    python build_manifest.py spec.json out_manifest.json
"""

import argparse
import hashlib
import json
import sys

FPS = 30
RESOLUTION = "1080x1920"
MEDIA_TYPE = "video"
DUR_MIN = 4
DUR_MAX = 9               # UNDER 10s


def warn(msg):
    sys.stderr.write("WARN: " + msg + "\n")


def die(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(1)


def load_spec(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        die("spec file not found: " + path)
    except json.JSONDecodeError as exc:
        die("spec file is not valid JSON (" + path + "): " + str(exc))
    if not isinstance(data, dict):
        die("spec must be a JSON object, got " + type(data).__name__)
    return data


def require(obj, key, where, types=None):
    if not isinstance(obj, dict) or key not in obj:
        die("missing required field '" + key + "' in " + where)
    val = obj[key]
    if val is None or (isinstance(val, str) and val.strip() == ""):
        die("required field '" + key + "' in " + where + " is empty")
    if types is not None and not isinstance(val, types):
        die("field '" + key + "' in " + where + " has the wrong type")
    return val


def optional(obj, key, default=None):
    if isinstance(obj, dict) and key in obj and obj[key] not in (None, ""):
        return obj[key]
    return default


def as_number(val, where):
    if isinstance(val, bool):
        die("numeric field in " + where + " must be a number, got bool")
    if isinstance(val, (int, float)):
        return float(val)
    die("numeric field in " + where + " must be a number, got " + type(val).__name__)


def normalize_words(raw, where):
    if isinstance(raw, list):
        tokens = [str(t).strip() for t in raw if str(t).strip() != ""]
        return " ".join(tokens), len(tokens)
    if isinstance(raw, str):
        text = raw.strip()
        return text, len([t for t in text.split() if t != ""])
    die("'words' in " + where + " must be a string or a list of tokens")


def build_body(spec):
    body_in = require(spec, "body", "spec", dict)
    shots_in = require(body_in, "shots", "spec.body", list)
    if not shots_in:
        die("spec.body.shots is empty; need at least one body shot")
    shots_out = []
    for idx, shot in enumerate(shots_in):
        where = "spec.body.shots[" + str(idx) + "]"
        if not isinstance(shot, dict):
            die(where + " must be an object")
        shot_id = str(optional(shot, "shot_id", "shot_" + str(idx + 1)))
        clip = str(optional(shot, "clip", shot_id + ".mp4"))
        raw_words = optional(shot, "words")
        if raw_words is None:
            raw_words = optional(shot, "vo_text")
        if raw_words is None:
            die("missing 'words' (or 'vo_text') in " + where)
        words, parsed = normalize_words(raw_words, where)
        word_count = int(optional(shot, "word_count", parsed))
        raw_sec = optional(shot, "seconds")
        if raw_sec is None:
            raw_sec = optional(shot, "requested_seconds")
        if raw_sec is None:
            die("missing 'seconds' (or 'requested_seconds') in " + where)
        seconds = int(round(as_number(raw_sec, where)))
        if seconds < DUR_MIN or seconds > DUR_MAX:
            die(where + " seconds=" + str(seconds) + " is outside 4..9 (every generation "
                "must be UNDER 10s)")
        shots_out.append({"shot_id": shot_id, "clip": clip, "words": words,
                          "word_count": word_count, "seconds": seconds})
    return {"shots": shots_out}


def ordered_roles(timeline):
    return [str(step.get("role", "")) for step in timeline]


def broll_placements(roles):
    """Indices of every 'broll' role within the ordered roles."""
    return [i for i, r in enumerate(roles) if str(r).lower() == "broll"]


def normalize_broll_set(raw, where):
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw] if raw.strip() else []
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    die("'broll_set' in " + where + " must be a string or a list of clips")


def build_timeline(variant, where, body_shots):
    raw_tl = optional(variant, "ordered_timeline")
    if isinstance(raw_tl, list) and raw_tl:
        timeline = []
        for jdx, step in enumerate(raw_tl):
            sw = where + ".ordered_timeline[" + str(jdx) + "]"
            if not isinstance(step, dict):
                die(sw + " must be an object")
            role = str(require(step, "role", sw))
            clip = str(require(step, "clip", sw))
            trim_in = round(as_number(optional(step, "trim_in", 0), sw), 3)
            to_raw = optional(step, "trim_out")
            trim_out = round(as_number(to_raw, sw), 3) if to_raw is not None else None
            timeline.append({"role": role, "clip": clip, "trim_in": trim_in,
                             "trim_out": trim_out})
        return timeline
    # Synthesize a 0-b-roll ad: hook then every body shot in order (ends on the
    # last body shot = the CTA). B-roll ads MUST pass an explicit ordered_timeline.
    hook_clip = str(require(variant, "hook_clip", where))
    timeline = [{"role": "hook", "clip": hook_clip, "trim_in": 0, "trim_out": None}]
    for shot in body_shots:
        timeline.append({"role": "body", "clip": shot["clip"], "trim_in": 0,
                         "trim_out": None})
    return timeline


def compute_total_seconds(variant, timeline, body_shots, where):
    supplied = optional(variant, "total_seconds")
    if supplied is not None:
        return round(as_number(supplied, where + ".total_seconds"), 3)
    clip_seconds = {s["clip"]: s["seconds"] for s in body_shots}
    broll_seconds = {}
    raw = variant.get("broll_seconds") if isinstance(variant, dict) else None
    if isinstance(raw, dict):
        for c, s in raw.items():
            try:
                broll_seconds[str(c)] = float(s)
            except (TypeError, ValueError):
                pass
    hook_seconds = optional(variant, "hook_seconds")
    total = 0.0
    for step in timeline:
        clip, role = step.get("clip"), step.get("role")
        if step.get("trim_out") is not None:
            total += max(0.0, float(step["trim_out"]) - float(step.get("trim_in") or 0))
        elif role == "hook" and hook_seconds is not None:
            total += float(hook_seconds)
        elif clip in clip_seconds:
            total += float(clip_seconds[clip])
        elif clip in broll_seconds:
            total += float(broll_seconds[clip])
        else:
            warn(where + ": '" + str(clip) + "' has no known duration; total_seconds "
                 "will under-count it (add total_seconds, broll_seconds, or hook_seconds).")
    return round(total, 3)


def fingerprint(visual_hook, broll_set, roles):
    """Stable 16-hex sha256 over RENDER-AFFECTING axes ONLY. The free-text verbal
    hook and the hook clip path are EXCLUDED (they vary by construction)."""
    sep = "\x1f"
    parts = [
        "visual=" + str(visual_hook),
        "broll=" + ",".join(sorted(broll_set)),
        "brollcount=" + str(len(broll_placements(roles))),
        "brollplaces=" + ",".join(str(i) for i in broll_placements(roles)),
        "roles=" + ">".join(roles),
    ]
    return hashlib.sha256(sep.join(parts).encode("utf-8")).hexdigest()[:16]


def build_variants(spec, body_shots):
    variants_in = require(spec, "variants", "spec", list)
    if not variants_in:
        die("spec.variants is empty; Andromeda needs 4 distinct ads")
    if len(variants_in) < 4:
        warn("only " + str(len(variants_in)) + " variant(s); the structure expects 4.")

    out, seen_fp, seen_visual, seen_hook = [], {}, {}, {}
    for idx, var in enumerate(variants_in):
        where = "spec.variants[" + str(idx) + "]"
        if not isinstance(var, dict):
            die(where + " must be an object")
        variant_id = str(optional(var, "variant_id", "v" + str(idx + 1)))
        verbal_hook = str(require(var, "verbal_hook", where))
        visual_hook = str(require(var, "visual_hook", where))
        hook_clip = str(require(var, "hook_clip", where))
        broll_set = normalize_broll_set(optional(var, "broll_set"), where)

        timeline = build_timeline(var, where, body_shots)
        roles = ordered_roles(timeline)

        # ENFORCE: every ad ENDS ON THE CTA -> last timeline entry must be a body beat,
        # and no b-roll may sit after the last body beat.
        if not roles or roles[-1].lower() != "body":
            die("ad '" + variant_id + "' does not end on the CTA: the last ordered_timeline "
                "entry is role '" + (roles[-1] if roles else "(none)") + "', not 'body'. "
                "Every ad must end on the CTA body beat; b-rolls go in the middle only.")
        last_body = max(i for i, r in enumerate(roles) if r.lower() == "body")
        if any(i > last_body for i in broll_placements(roles)):
            die("ad '" + variant_id + "' has a b-roll AFTER the final body beat. B-rolls "
                "are inserted only in the middle; the ad ends on the CTA.")

        total_seconds = compute_total_seconds(var, timeline, body_shots, where)
        fp = fingerprint(visual_hook, broll_set, roles)
        if fp in seen_fp:
            die("distinctness collision: ads '" + variant_id + "' and '" + seen_fp[fp]
                + "' produce the same fingerprint " + fp + ". Give them a different visual "
                "hook, b-roll count, or b-roll placement (two ads with the same b-roll count "
                "must place them differently).")
        seen_fp[fp] = variant_id

        if visual_hook in seen_visual:
            warn("ads '" + seen_visual[visual_hook] + "' and '" + variant_id
                 + "' share the same visual_hook; use 4 different KINDS of visual action.")
        seen_visual[visual_hook] = variant_id
        if verbal_hook in seen_hook:
            warn("ads '" + seen_hook[verbal_hook] + "' and '" + variant_id
                 + "' reuse the same verbal hook; each ad must have a UNIQUE hook.")
        seen_hook[verbal_hook] = variant_id

        out.append({
            "variant_id": variant_id,
            "verbal_hook": verbal_hook,
            "visual_hook": visual_hook,
            "hook_clip": hook_clip,
            "broll_set": broll_set,
            "ordered_timeline": timeline,
            "total_seconds": total_seconds,
            "distinctness_fingerprint": fp,
        })

    # The b-roll-count ladder should not be flat across all ads.
    counts = [len(broll_placements(ordered_roles(v["ordered_timeline"]))) for v in out]
    if len(set(counts)) == 1:
        warn("every ad uses the same number of b-rolls (" + str(counts[0]) + "); the "
             "intended ladder is 0/1/2/2 so the ads differ in length and structure.")
    return out


def build_character(spec):
    char_in = require(spec, "character", "spec", dict)
    return {
        "face_image": str(require(char_in, "face_image", "spec.character")),
        "body_image": str(require(char_in, "body_image", "spec.character")),
        "product_image": str(require(char_in, "product_image", "spec.character")),
    }


def build_manifest(spec):
    if "voice_track" in spec:
        die("spec contains 'voice_track'. The locked model has NO voice track; each clip "
            "keeps its own audio. Remove voice_track.")
    body = build_body(spec)
    character = build_character(spec)
    variants = build_variants(spec, body["shots"])
    manifest = {
        "concept": str(require(spec, "concept", "spec")),
        "niche": str(require(spec, "niche", "spec")),
        "date": str(require(spec, "date", "spec")),
        "fps": FPS, "resolution": RESOLUTION, "media_type": MEDIA_TYPE,
        "framework": str(require(spec, "framework", "spec")),
        "voice_ref_clip": str(require(spec, "voice_ref_clip", "spec")),
        "character": character,
        "body": body,
        "variants": variants,
    }
    assert "voice_track" not in manifest
    return manifest


def write_manifest(manifest, out_path):
    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        die("could not write manifest to " + out_path + ": " + str(exc))


def parse_args(argv):
    p = argparse.ArgumentParser(
        prog="build_manifest.py",
        description="Build the Seedance 2.0 Andromeda assembly-manifest.json. Enforces "
                    "unique fingerprints, that every ad ends on the CTA, and no b-roll "
                    "after the CTA. Each clip keeps its own audio (no voice_track).")
    p.add_argument("spec")
    p.add_argument("out_manifest")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    spec = load_spec(args.spec)
    manifest = build_manifest(spec)
    write_manifest(manifest, args.out_manifest)
    n_v = len(manifest["variants"])
    n_s = len(manifest["body"]["shots"])
    counts = [len(broll_placements(ordered_roles(v["ordered_timeline"]))) for v in manifest["variants"]]
    print("Wrote manifest: " + args.out_manifest)
    print("Summary: " + manifest["concept"] + " (" + manifest["framework"] + "), "
          + str(n_v) + " ads on " + str(n_s) + " body shots, b-roll counts "
          + str(counts) + ", every ad ends on the CTA, " + manifest["resolution"]
          + " @ " + str(manifest["fps"]) + "fps, each clip keeps its own audio.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
