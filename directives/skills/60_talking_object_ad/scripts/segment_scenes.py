#!/usr/bin/env python3
"""
segment_scenes.py - turn a storyboard + the dialogue script into sized, wave-assigned
talking-object scenes.

THIS FACTORY IS DIALOGUE-FIRST: there is no voiceover audio to align against. The WORDS
are the clock — each scene's duration derives from its line's word count at the primary
bank's measured rate (~2.8 words/second including acting pauses).

INPUT
  storyboard.json: { "scenes": [ {
      "scene_id", "line_ids":[...], "role", "speaker",
      "visual", "action", "prop", "world", "emotion",
      "sfx_note", "on_screen_text", "source_shell"
  } ] }
  script.json: { "concept", "mode", "target_seconds",
      "characters":[ {"id","name","kind","tier","bible","voice","world","prop"} ],
      "lines":[ {"id","role","speaker","dialogue"} ] }

WHAT IT DOES
  - Sizes every scene from its dialogue words:
        est_seconds       = word_count / 2.8
        requested_seconds = clamp(round_half_up(est_seconds), 4, 9)
  - ENFORCES THE LINE-LENGTH LAW: a line over 25 words cannot fit a 9s clip — exit 3
    (trim the line, or split it into two scenes; a split makes the speaker RECURRING:
    its second scene becomes wave 2 with the first clip as its video reference).
    A line under 11 words renders at the 4s floor with silent acting business padding
    the clip (a WARN — direct the business in the prompt; the footage is used, not
    wasted).
  - ONE SPEAKER PER SCENE: a scene mixing lines from different speakers is a structural
    error (a declared duo is one speaker id). A narrator speaker may appear in at most
    ONE scene (Seedance casts the narrator voice fresh per generation; a narrator spread
    across clips comes back as a different voice each time).
  - ASSIGNS WAVES + VOICE REFS (the member's reference ladder, tier 3):
        wave 1 = the speaker's FIRST scene (renders in the parallel batch)
        wave 2 = a recurring speaker's later scene — voice_ref_source is set to the
                 speaker's first scene's clip; it renders only AFTER that clip is
                 approved, with a brand-new environment.
  - ASSIGNS TIERS from the cast: tier 1 (generic, render reference-free) or tier 2
    (real product in frame — the approved still is required). Product/CTA scenes are
    always tier 2.
  - Checks: every line covered exactly once, worlds never repeat, on_screen_text empty
    everywhere except the CTA, the ad ends on the CTA.

OUTPUT scenes.json: { concept, mode, n_scenes, total_render_seconds, scenes:[ {
    scene_id, role, speaker, covers, dialogue, voice, word_count, est_seconds,
    requested_seconds, wave, tier, voice_ref_source, trim_in, trim_out,
    on_screen_text, sfx_note, world, prop, emotion, visual, action, source_shell,
    clip } ] }

trim_out is provisional (the full requested render). After the clip renders,
dialogue_check.py reports the real speech_end — update trim_out to speech_end + 0.3-0.6s
before building the manifest, so dead tail air never pads the ad.

Exit 0 clean, 2 on bad input, 3 when a structural problem needs a script/storyboard fix.
"""

import argparse
import json
import math
import sys

WORDS_PER_SEC = 2.8     # the primary bank's measured speaking rate, acting pauses included
MIN_RENDER = 4
MAX_RENDER = 9          # Seedance integer window; every generation is UNDER 10s
MAX_WORDS = 25          # over this cannot fit a 9s clip (25/2.8 ≈ 8.9s)
COMFORT_WORDS = 11      # under this renders at the 4s floor with acting business (WARN)
NARRATOR_IDS = {"narrator", "vo", "announcer"}


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


def word_count(text):
    return len([w for w in str(text).split() if any(c.isalnum() for c in w)])


def main(argv=None):
    p = argparse.ArgumentParser(prog="segment_scenes.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("storyboard")
    p.add_argument("script")
    p.add_argument("out_scenes")
    args = p.parse_args(argv)

    sb = load(args.storyboard, "storyboard")
    sc = load(args.script, "script")

    scenes_in = sb.get("scenes") if isinstance(sb, dict) else None
    if not isinstance(scenes_in, list) or not scenes_in:
        die("storyboard.json needs a non-empty 'scenes' array")
    lines_in = sc.get("lines") if isinstance(sc, dict) else None
    if not isinstance(lines_in, list) or not lines_in:
        die("script.json needs a non-empty 'lines' array")
    chars_in = sc.get("characters") if isinstance(sc, dict) else None
    if not isinstance(chars_in, list) or not chars_in:
        die("script.json needs a non-empty 'characters' array (the cast)")

    chars = {}
    for i, ch in enumerate(chars_in):
        if not isinstance(ch, dict) or not ch.get("id"):
            die("characters[%d] needs an 'id'" % i)
        chars[str(ch["id"])] = ch

    lines = {}
    line_order = {}
    for i, ln in enumerate(lines_in):
        if not isinstance(ln, dict) or not ln.get("id"):
            die("lines[%d] needs an 'id'" % i)
        lid = str(ln["id"])
        if lid in lines:
            die("duplicate line id '%s'" % lid)
        if not str(ln.get("dialogue") or "").strip():
            die("line '%s' has an empty 'dialogue'" % lid)
        spk = str(ln.get("speaker") or "")
        if not spk:
            die("line '%s' has no 'speaker'" % lid)
        if spk not in chars and spk.lower() not in NARRATOR_IDS:
            die("line '%s' names unknown speaker '%s' (not in the cast, not a narrator id)"
                % (lid, spk))
        lines[lid] = ln
        line_order[lid] = i

    flags = []   # must-fix (exit 3)
    warns = []   # informational

    # THE LINE-LENGTH LAW (per line, before scene mapping)
    for lid, ln in lines.items():
        wc = word_count(ln["dialogue"])
        if wc > MAX_WORDS:
            flags.append("line '%s' (%s) is %d words — over the %d-word ceiling (~%ds of "
                         "speech cannot fit a 9s clip). Trim the line, or split it into "
                         "two scenes (the split makes '%s' a recurring speaker: wave 2, "
                         "video reference, new environment)."
                         % (lid, ln.get("speaker"), wc, MAX_WORDS,
                            int(math.ceil(wc / WORDS_PER_SEC)), ln.get("speaker")))

    # line coverage: every line in exactly one scene
    covered = {}
    for si, s in enumerate(scenes_in):
        if not isinstance(s, dict):
            die("scenes[%d] is not an object" % si)
        ids = s.get("line_ids") or ([s["line_id"]] if s.get("line_id") else [])
        if not ids:
            die("scenes[%d] (%s) has no line_ids" % (si, s.get("scene_id", "?")))
        for lid in ids:
            lid = str(lid)
            if lid not in lines:
                die("scene '%s' references unknown line '%s'"
                    % (s.get("scene_id", "?"), lid))
            if lid in covered:
                flags.append("line '%s' is covered by two scenes ('%s' and '%s'); every "
                             "line belongs to exactly one scene"
                             % (lid, covered[lid], s.get("scene_id", "?")))
            covered[lid] = str(s.get("scene_id") or ("scene_%02d" % (si + 1)))
    for lid in lines:
        if lid not in covered:
            flags.append("line '%s' is never covered by any scene" % lid)

    # build scenes in line order
    def scene_key(s):
        ids = [str(x) for x in (s.get("line_ids") or [s.get("line_id")])]
        return min(line_order[i] for i in ids if i in line_order)

    ordered = sorted(range(len(scenes_in)), key=lambda i: scene_key(scenes_in[i]))
    if ordered != list(range(len(scenes_in))):
        warns.append("storyboard scene order does not match script order; reordering")

    out = []
    speaker_first_scene = {}
    narrator_scenes = 0
    worlds_seen = {}
    for pos, i in enumerate(ordered):
        s = scenes_in[i]
        sid = str(s.get("scene_id") or ("scene_%02d" % (pos + 1)))
        ids = [str(x) for x in (s.get("line_ids") or [s.get("line_id")])]
        role = str(s.get("role") or lines[ids[0]].get("role") or "")

        # one speaker per scene
        speakers = []
        for lid in ids:
            spk = str(lines[lid].get("speaker"))
            if spk not in speakers:
                speakers.append(spk)
        if len(speakers) > 1:
            flags.append("scene '%s' mixes lines from speakers %s; one speaker per scene "
                         "(declare a duo as ONE speaker id in the cast)" % (sid, speakers))
        speaker = speakers[0]
        sb_speaker = str(s.get("speaker") or "")
        if sb_speaker and sb_speaker != speaker:
            warns.append("scene '%s' storyboard speaker '%s' differs from its lines' "
                         "speaker '%s'; using the lines'" % (sid, sb_speaker, speaker))

        is_narrator = speaker.lower() in NARRATOR_IDS
        if is_narrator:
            narrator_scenes += 1
            if narrator_scenes > 1:
                flags.append("scene '%s' is a SECOND narrator scene; a narrator is legal "
                             "only confined to ONE clip (Seedance casts the voice fresh "
                             "per generation — a narrator across clips changes voice). "
                             "Give the extra lines to on-camera characters." % sid)

        dialogue = " ".join(str(lines[lid]["dialogue"]).strip() for lid in ids)
        wc = word_count(dialogue)
        est = wc / WORDS_PER_SEC
        req = max(MIN_RENDER, min(MAX_RENDER, int(math.floor(est + 0.5))))
        if wc > MAX_WORDS:
            # the per-LINE ceiling above catches single long lines; this catches a
            # scene whose combined line_ids total more speech than a 9s clip holds
            # (e.g. two narrator lines merged into the single legal narrator clip)
            flags.append("scene '%s' totals %d words across its lines (~%ds of speech) "
                         "— over the %d-word ceiling a 9s clip can hold. Trim the "
                         "lines or move one to another scene."
                         % (sid, wc, int(math.ceil(est)), MAX_WORDS))
        if wc < COMFORT_WORDS:
            warns.append("scene '%s' line is %d words (~%.1fs of speech) — renders at the "
                         "%ds floor; direct silent acting business to fill the clip"
                         % (sid, wc, est, req))

        ch = chars.get(speaker, {})
        kind = str(ch.get("kind") or ("narrator" if is_narrator else ""))
        tier = ch.get("tier")
        if role.lower() in ("product", "cta") or kind == "product":
            tier = 2
        if tier not in (1, 2):
            tier = 1 if kind in ("villain", "ingredient", "narrator", "") else 2
            warns.append("scene '%s' speaker '%s' had no ladder tier; assigned tier %d"
                         % (sid, speaker, tier))

        # waves + voice refs (the ladder's tier 3)
        if is_narrator or speaker not in speaker_first_scene:
            wave = 1
            voice_ref = None
            if not is_narrator:
                speaker_first_scene[speaker] = sid
        else:
            wave = 2
            voice_ref = "clips/%s.mp4" % speaker_first_scene[speaker]

        world = str(s.get("world") or ch.get("world") or "")
        wkey = world.strip().lower()
        if wkey:
            if wkey in worlds_seen and wave != 2:
                flags.append("scene '%s' reuses the world '%s' (first used by '%s'); one "
                             "world per speaker, no environment repeats"
                             % (sid, world, worlds_seen[wkey]))
            elif wkey in worlds_seen and wave == 2:
                flags.append("scene '%s' (wave 2, recurring speaker '%s') reuses the world "
                             "'%s' — a recurring speaker's second scene must change the "
                             "environment (the video reference carries the character, "
                             "never the scene)" % (sid, speaker, world))
            else:
                worlds_seen[wkey] = sid

        ost = str(s.get("on_screen_text") or "")
        if ost and role.lower() != "cta":
            flags.append("scene '%s' (%s) has on_screen_text %r; the CTA is the ONLY "
                         "scene where in-scene text is legal" % (sid, role, ost))

        out.append({
            "scene_id": sid, "role": role, "speaker": speaker, "covers": ids,
            "dialogue": dialogue, "voice": str(ch.get("voice") or ""),
            "word_count": wc, "est_seconds": round(est, 2),
            "requested_seconds": req, "wave": wave, "tier": tier,
            "voice_ref_source": voice_ref,
            "trim_in": 0.0, "trim_out": float(req),
            "on_screen_text": ost, "sfx_note": str(s.get("sfx_note") or ""),
            "world": world, "prop": str(s.get("prop") or ch.get("prop") or ""),
            "emotion": str(s.get("emotion") or ""),
            "visual": str(s.get("visual") or ""), "action": str(s.get("action") or ""),
            "source_shell": str(s.get("source_shell") or "synthesized"),
            "clip": "clips/%s.mp4" % sid,
        })

    if not out or out[-1]["role"].lower() != "cta":
        last = out[-1]["role"] if out else "(none)"
        flags.append("the ad does not end on the CTA: last scene role is '%s'" % last)
    if out and out[0]["role"].lower() != "hook":
        flags.append("the ad does not open on the villain hook: first scene role is "
                     "'%s', not 'hook' — the hook opens this format and is the render "
                     "checkpoint everything else waits on" % out[0]["role"])

    payload = {
        "concept": sc.get("concept"),
        "mode": sc.get("mode") or "full-cast",
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
    w("\n=== SCENE PLAN (%d scenes, render %ds total) ===\n"
      % (len(out), payload["total_render_seconds"]))
    w("scene       role       speaker        words  est    render  wave  tier  voice_ref\n")
    for o in out:
        w("%-11s %-10s %-14s %4d  %5.1fs   %2ds     %d     %d    %s\n" % (
            o["scene_id"], o["role"][:10], o["speaker"][:14], o["word_count"],
            o["est_seconds"], o["requested_seconds"], o["wave"], o["tier"],
            o["voice_ref_source"] or "-"))
    for m in warns:
        w("WARN: %s\n" % m)
    for m in flags:
        w("FLAG: %s\n" % m)
    w("wrote %s\n=================================================\n\n" % args.out_scenes)
    return 3 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
