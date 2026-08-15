# Generation Architecture — Pixar Ad Factory (Seedance 2.0, VO-first, hook-anchored)

Single source of truth for how a Pixar Ad is built. Read it before any step. The
production pipeline is IDENTICAL to the Clay and Skeleton factories'; the world model is
one cohesive Pixar-style 3D animated world (everything animated, nothing photoreal). Do
not import the UGC factory's rules.

## Member-locked HARD RULES (override anything below that conflicts)

1. **NO real humans, ever** — no photoreal person or live-action element in any frame;
   the whole world is Pixar-style 3D animated. Witnesses/peers are OTHER Pixar-style
   characters (optionally desaturated "elsewhere people"). Every prompt carries a
   no-real-people line; "any real human being or photoreal person" sits in every negative.
2. **The hook always contains the character, and the hook BEAT is ONE single continuous
   1–2s shot** — never a flash montage. The hook line never renders solo: it MERGES with
   the adjacent next line into one generation (scene 1) — the clip opens on the hook beat
   from the start image, then hard-cuts into the merged line's beats. The hook beat itself
   is never multi-shot.
3. **NEVER attach a video clip as a reference.** The only references in the whole build:
   the approved HOOK STILL (start image on the hook; identity image reference on every
   character-visible scene) and the approved PRODUCT STILL (product scenes).
4. **Never repeat a camera angle+scale anywhere in the ad.**
5. **Re-hook every cut** — something big changes on every shot.
6. **Scene simplicity law:** different ≠ complicated. Environments may vary and may return
   to the home set; variety comes from the camera. **Visuals are EMOTION-FIRST — direct
   the FEELING the hero (the viewer's surrogate) experiences at each beat (dread,
   false comfort, burnout, a spark of hope, relief, pride), carried by the cartoon eyes,
   posture, hands, and light/grade. The VO speaks the facts; the picture never literally
   stages the thing the narrator names.** One clear action per shot, easily renderable by
   current video models: no complex choreography, no extreme VFX, no crowded detail.
7. **NEVER render a computer/phone screen CLOSE-UP without a reference image.** A close,
   legible screen appears ONLY in a scene attaching the real screenshot (the product
   still) — typically the turn and the CTA. Everywhere else screens are ambient
   out-of-focus glow, never a readable close-up; "legible computer screen, detailed
   screen close-up, fake user interface" sits in every negative.

## The model in one breath

- A Pixar Ad is a **voiceover-driven direct-response commercial**. One continuous
  ElevenLabs voiceover narrates a DR arc built on ONE framework from the scripting
  library (hook → agitate → turn → mechanism/proof → CTA; a "Day 1… Day 30…" progression
  ladder is one legal framework choice, never the default). **No character talks on
  camera. No lip-sync, no dialogue in any clip.** The voice is laid OVER the picture at
  assembly.
- The video is a sequence of **cute, premium Pixar-style 3D animated scenes**: warm
  vibrant rooms, streets, and light, all one cohesive animated world — and a **cast
  Pixar-style hero** (ONE locked Character Bible cast from the brand's ideal customer)
  living the journey unremarked. **Every character in frame is a Pixar-style 3D animated
  character**: witnesses and peers are OTHER Pixar-style characters (optionally
  desaturated "elsewhere people"), never real humans. The world never reacts to the art
  style, only to the story — the deadpan conceit.
- **The product renders as a polished Pixar-style 3D PROP** from the member's real product
  photo — its real shape, label, logo, text and colors stay fully readable and
  recognizable (the Studio Pixar product rule).
- **Scenes come from the SCENE BANKS, never from nothing.** `scene-bank-191xt.md` and
  `scene-bank-tutorial-trap.md` hold two winning ads torn down into recreation-grade
  shells — one escalating-progression ad ported to the Pixar material law, and one
  native Pixar origin-scenario/collapse ad whose prompts shipped as-is; pick the bank
  whose story grammar fits the script. Each storyboard scene
  either FILLS a matching shell (keep the shot structure and cut rhythm, swap character
  state, product, palette, set, story for the member's brand) or is SYNTHESIZED in the
  banks' grammar. Every scene records its `source_shell`.
- **The HOOK is the character anchor, rendered IMAGE-TO-VIDEO from an approved still.** Step
  3.5 generates the HOOK STILL with the Studio Pixar template (`hook-still-template.md`,
  Nano Banana 2), the member approves it cheap, then scene 1 animates FROM it. The approved
  still is the **START IMAGE** — the clip's literal first frame (Path B renders with
  `--start-image`). The hook-beat portion of the prompt is **MOTION-ONLY**: the still
  already carries the character, set and light, so the prompt never re-describes them.
  Scene 1 covers the hook line MERGED with the adjacent next line: it opens on the hook's
  1–2s beat as **ONE single continuous shot — never a flash montage** (hard rule 2; Bank 01's X01 is the grammar, Bank 02's F01 is RETIRED as a hook shape), then
  HARD-CUTS into the merged line's beats, directed like any other sub-shots. Everything else inherits its
  identity from that same approved still, so the still must be right before anything
  renders.
- **Consistency = the locked Character Bible + the hook STILL as a shared IDENTITY image
  reference.** The chosen Bible's wording is pasted VERBATIM into every prompt (only the
  emotion-state slot changes), and every other character-visible scene attaches the **hook
  still** (`inputs/hook-still.png`) as an IMAGE reference. The prompt opens by telling the
  model to study the reference and lock the character exactly — then build a BRAND-NEW
  dynamic scene, never copying the still's pose, framing, or set. **A video clip is NEVER
  attached as a reference** — a video ref makes the model continue/match that clip's scene
  and composition (chimera characters, repeated framings). **Any scene that shows the
  product attaches the PRODUCT STILL** (`inputs/product-still.png`, the product staged as
  a polished Pixar-style 3D prop with its real label fully readable, generated from the
  real photo in Step 3.5; always the CTA,
  any earlier reveal too). Nothing about voice is ever uploaded to the generator.
- **The face is the dashboard.** The hero's expression, posture, and the world's COLOR grade
  are per-scene fill variables that narrate the arc: warm vibrant = thriving, cool
  desaturated = decline, re-saturation = recovery, golden-hour glow = the CTA peak. State
  moves only forward through the arc and never mixes inside one sub-shot.
- **Hard cuts between scenes.** Each non-hook scene is a brand-new shot — a hard cut — whose
  first frame is already the new scene. The prompt says this explicitly. NOT a morph.
- **Fast pacing is the standard for non-hook clips (multi-shot).** Every non-hook clip is a
  sequence of hard-cut sub-shots — a brand-new camera angle or mini-scene roughly every ~3
  seconds (the banks average ~2.4s) — never one static held shot. Beats are written as
  `SHOT ONE … HARD CUT to SHOT TWO …`, timestamped to the VO words. **Angles are tracked
  across the WHOLE ad and never repeat** (hard rule 4); every cut changes something big
  (hard rule 5); every sub-shot is one clear simple action (hard rule 6). The clip is ONE
  generation mapped to ONE VO span — do NOT split the sub-shots into separate clips.
- **Generation: hook first, then the rest in PARALLEL.** Describe the hook's shot plan → get
  approval → render the hook → get the member's OK on the character → describe the remaining
  scenes' shot plans → get approval → render every other scene at once (they depend only on
  the approved stills, not each other). Any scene showing the product also attaches the
  product still.
- The VO timing (faster-whisper, with word timestamps) sets each scene's on-screen length
  and gives the exact words per scene to direct the action to. **The VO file itself is
  untouchable** — never trimmed, silence-cut, stretched, or re-voiced to fit the picture;
  sync is reconciled on the picture side (per-scene freeze-holds at stitch).
- **One clip per voiceover line**, sized to that line by **ROUND-TO-NEAREST (≥.5 up, <.5
  down, clamped to the integer 4–9s window — never blanket-ceil)**, each a fast-cut sequence
  of sub-shots with timestamped action beats. **THE MERGE LAW: a line whose span is under
  3.5s never gets its own clip — merge it with an adjacent line into ONE generation
  carrying both beats as hard-cut sub-shots. The hook line ALWAYS merges with the next
  line (its beat is 1–2s by design); the last-position CTA is the only exception.**
  Vertical 9:16, **1080p**.
- **NO on-screen text, EVER.** No captions, no day/week labels, no banner words, no legible
  UI — not in the generations and not at assembly. The VO carries every milestone and the
  offer. The only readable text in any frame is the real product's own label.
- **The ad opens on the hook and ends on the CTA / product.**

## Why hook-still identity references + hard cuts (not video refs, not morph chaining)

The approved hook STILL is the one place the character lives. The hook renders from it as
the literal first frame (the member approves the character in motion), and every other
character-visible scene attaches that SAME still as an image reference — an identity
anchor. The prompt explicitly says *"study the attached reference image and lock onto the
character exactly — but this is a brand-new dynamic scene: do NOT copy the reference's
pose, framing or set."* A VIDEO reference is never used: it drags the source clip's scene,
composition, and grade onto the new shot (chimera witnesses, repeated framings, static
sameness). Because each scene depends only on the approved stills, the non-hook scenes
**render in parallel** once the hook is approved. Body-state continuity on top of that
comes from the verbatim Bible + the named state in each prompt.

## The flow, end to end

```
INTAKE (product/offer, product photo, HERO CASTING confirm) → ANGLE (the playbook) → SCRIPT (VO only)
   │
   ▼  GATE 1: member approves the transcript (+ a quick voice design: a calm dramatic narrator)
   │
   ▼  member renders ONE VO in ElevenLabs, drops it into audio/
   │
   ▼  align_vo.py → timing.json   (per-line spans + per-WORD timestamps)
   │
   ▼  CHARACTER & WORLD PLAN (the Bible locked, the emotion-state arc, the witness list)
   ▼  REFERENCE STILLS (Studio Pixar template): hook still + product still, approved cheap
   ▼  STORYBOARD (one clip per VO line; every scene fills a bank shell or synthesizes in the
       banks' grammar; scene 1 = hook anchor MERGED with the next line, the rest hard-cut
       off it; emotion state + the beat's EMOTION per scene)
   │
   ▼  segment_scenes.py → scenes.json   (round-to-nearest seconds, merge law, vo_text per scene)
   │
   ▼  PROMPTS (hook = MOTION-ONLY off the start image; the rest = identity-locked to the hook STILL) → payload_*.json
   │   validate_prompt.py each
   │
   ▼  GATE 2: storyboard + the EXACT per-clip table (VO span, generation seconds, per-scene
   │          cost, totals) + path A/B/C/D. Any later plan change re-runs this table + yes.
   │
   ▼  GENERATION:
   │     1. describe scene 1's shot plan (the 1–2s hook beat + the merged line's cuts) → approve
   │     2. render the HOOK alone
   │     3. ask "happy with the character?" → re-roll until yes
   │     4. describe each remaining scene's shot plan (plain language, not prompts) → "render everything else?"
   │     5. on yes: render the rest IN PARALLEL off the hook STILL (any product scene + product still)
   │
   ▼  FRAME CHECK: frame_check.sh per clip → read every contact sheet against the word
   │              timeline; timing misses are RE-CUT from existing footage, never re-rendered
   │
   ▼  build_manifest.py → pixar-ad-manifest.json
   ▼  stitch_pixar.sh → out/pixar_ad.mp4  (hard concat with per-scene freeze-holds, VO
       over top, SFX ducked, NO captions — the stitcher has no caption path, -14 LUFS, 1080x1920)
```

TWO hard stops: GATE 1 (transcript) and GATE 2 (storyboard + cost). During generation there
are TWO human checkpoints: approving the hook's character, and the "render everything else"
yes.

## The data files (all under `$WORK`)

| File | Written by | Purpose |
|---|---|---|
| `transcript.json` | you (Step 2) | VO ONLY — `{concept, niche, framework, angle, belief, voice_mode, target_seconds, voc_anchors, lines:[{id, role, vo}]}`. Approved at Gate 1. |
| `audio/vo.*` | the member | One continuous ElevenLabs render. |
| `timing.json` | `align_vo.py` | Per-line `{id, role, vo, start, end, dur, word_count}` + a top-level `words:[{word,start,end}]` + `total_seconds`, `method`. |
| `character-plan.md` | you (Step 3.5) | The locked Bible + emotion-state arc + witness list + world plan. |
| `inputs/hook-still.png`, `inputs/product-still.png` | Step 3.5, the Studio Pixar template | The approved reference stills: the hook's image-to-video seed, and the attached image for every product scene. |
| `storyboard.json` | you (Step 4) | `{scenes:[{scene_id, line_ids, role, visual, action, sfx_note, reference, sfx, span_share, source_shell, emotion_state}]}`. `source_shell` is the bank shell id (X05, F07) or "synthesized". |
| `scenes.json` | `segment_scenes.py` | Per-scene `{scene_id, role, covers, start, end, span_seconds, requested_seconds, trim_in, trim_out, reference, action, sfx_note, vo_text, sfx, clip}`. |
| `payload_<scene_id>.json` | you (Step 5) | Dispatch contract per scene (prompt, duration, reference, images, …). Validated before render. |
| `spec.json` | you (Step 7) | Input to the manifest builder. |
| `pixar-ad-manifest.json` | `build_manifest.py` | The assembly contract. |
| `out/pixar_ad.mp4` | `stitch_pixar.sh` | The final 9:16 1080p ad. |

There is NO captions file in this skill — the stitcher cannot burn text.

## Reference types (per scene)

- Hook (scene 1, merged with the next line): `{type:"image", source:"inputs/hook-still.png"}`,
  the approved Step 3.5 still. That still is the **START IMAGE, the clip's literal first
  frame** (Path B renders it with `--start-image`, not `--image`). The hook-beat portion
  of the prompt directs motion only; the merged line's beats follow as hard-cut sub-shots.
- Every other scene: `{type:"none"}` with `images` carrying `"inputs/hook-still.png"` —
  the hook still attached as the IDENTITY image reference (Path B: `--image`) on every
  character-visible scene. **Any scene that shows the product** (always the CTA, and any
  earlier product reveal) additionally lists the **product still** in `images` (rendered
  with `--image inputs/hook-still.png --image inputs/product-still.png`).
- **A video clip is NEVER a reference type in this skill** — video refs drag the source
  clip's scene and composition onto the new shot. The skill does NOT use
  last-frame→first-frame chaining either; the only start image in the build is the hook's
  approved still. (`last_frame.sh` is legacy, unused in the current reference model.)

## Roles & structure

`role` is a journey label (`hook, problem, decline, turn, discovery, recovery, proof,
milestone, mechanism, payoff, cta` — DR labels like `agitate/solution` are also legal). The
first scene is the **hook** (the character anchor). The last scene is the **CTA / product**;
nothing follows it. `build_manifest.py` enforces ends-on-CTA.

## Picture-lock: how scene length is decided

`align_vo.py` gives each VO line an exact `[start, end]` plus per-word timestamps. Each
scene covers one line (or a `span_share` of one).
`requested_seconds = clamp(round_half_up(span), 4, 9)` — **round to NEAREST (≥.5 up, <.5
down: 4.42s → 4s, 6.62s → 7s), never blanket-ceil** — then **trim to the exact span at
stitch**; a round-down generation that runs a hair short is **freeze-held** (its last frame
cloned to the exact span) so nothing downstream desyncs. A span under 3.5s never renders
solo (the MERGE LAW — `segment_scenes.py` hard-fails; merge the line with a neighbor).
The spans sum to ≈ the VO total; `stitch_pixar.sh` pads/trims the final video to the
VO duration. The VO itself is never altered.

Scene 1 ALWAYS covers the hook line MERGED with the adjacent next line (`line_ids:
[hook, next]`): the clip opens on the hook's continuous 1–2s beat, then hard-cuts into
the merged line's beats. `segment_scenes.py` hard-fails a hook scene that covers only
the hook line.

## Directing to the words (emotion-first)

`scenes.json` carries each scene's exact `vo_text`. Direct the clip's motion to HIT those
words IN TIME with **timestamped action beats** (`[0.0-2.3s] … [2.3-7.0s] …`) derived from
the word timeline — never write the clip's TOTAL duration in the prompt. **What each beat
SHOWS is the EMOTION of that moment, not a literal act-out of the words (hard rule 6):**
name the feeling the hero/viewer experiences (dread, false comfort, burnout, a spark
of hope, relief, pride) and let the cartoon eyes, posture, hands and light/grade carry it —
the VO speaks the facts; the picture never literally stages the thing the narrator names
(no acted-out charts, metrics, or data events). Include "The emotion is the subject" in
every prompt. Something is always moving; every sub-shot is a never-repeated angle+scale
delivering one clear, simply-renderable change; environments may vary and may return to
the home set; **screens stay ambient out-of-focus glow except in scenes attaching the real
screenshot (hard rule 7)**. Pace follows the EMOTION STATE (decline cuts slower and moodier,
recovery cuts faster and brighter — the banks' law). The hook BEAT is the only exception
to multi-beat direction: it is ONE continuous shot with a single motion beat, no internal
cuts — the cuts begin when scene 1 transitions into its merged line's beats.

## Audio model (identical to the clay factory)

- The **ElevenLabs VO is the master spine**, laid over the whole picture at full level. The
  generator is never given a voice clip.
- Clips carry **real-world ambience/foley only** (gym clatter, street hum, room tone — no
  music, no speech). Seedance generates the audio automatically; `stitch_pixar.sh` ducks
  it under the VO (`keep_sfx`). **No captions, no overlay text — ever.**
- Final mix normalized to about **-14 LUFS**.

## The manifest (assembly contract)

```
pixar-ad-manifest.json = {
  concept, niche, date, fps: 30, resolution: "1080x1920", media_type: "video",
  framework, vo_track, total_seconds, keep_sfx, references,
  scenes: [ { scene_id, role, clip, trim_in, trim_out, reference, on_screen_text, sfx } ]
}
```

`build_manifest.py` enforces: `vo_track` present; the last scene's role is `cta`; every span
> 0 and <= a sub-10s render; total within tolerance of the VO. `on_screen_text` stays empty
in this skill.

## Generation order & the human checkpoints

1. **Describe scene 1's shot plan** in plain language (the single continuous 1-2s hook
   beat and what moves in it, then the merged line's hard-cut beats, NOT the full prompt);
   get approval.
2. **Render SCENE 1 alone**, image-to-video from the approved hook still as the START
   IMAGE (the character anchor; Path B `--start-image`).
3. **Ask the member "happy with the character and the result?"** Re-roll until yes (each
   re-roll needs its own fresh explicit yes with cost).
4. **Describe the shot plan of every remaining scene** (a plain-language line or two per
   scene — its sub-shots, emotion state, witnesses, NOT the full prompts); ask **"render
   everything else?"**
5. **On yes, render the rest IN PARALLEL** off the hook STILL as the identity image
   reference (any scene showing the product also attaches the product still; never a video
   reference). Save clips as `clips/scene_NN.mp4`.
6. **FRAME CHECK every clip** (`frame_check.sh` → read each contact sheet against the word
   timeline). Timing misses are fixed by RE-CUTTING the existing clip (trim/concat/
   freeze-pad); a re-render is only for missing/wrong content and needs its own fresh yes.
7. Assemble once with `build_manifest.py` + `stitch_pixar.sh` (1080x1920).

If the member asks a question at ANY point in this flow, answer it fully and STOP; never
render while a question is pending. Every render, including re-rolls and single-scene
re-dos, needs its own fresh explicit yes.

## Hard "never"s

- Never put dialogue, a talking head, or lip-sync into a clip. Voice is the external VO.
- Never upload a voice clip / voice reference to the generator.
- Never render any video before the reference stills are approved; the hook renders
  image-to-video from the approved hook still, never bare text.
- Never render the other scenes before the hook's character is approved.
- Never attach a video clip as a generation reference — the only references are the two
  approved stills (hook still = identity, product still = product).
- Never render a real human or photoreal person in any frame — every character is a Pixar-style 3D animated character.
- Never repeat a camera angle+scale anywhere in the ad, and never cut without a big change.
- Never overcomplicate a shot — one clear action, easily renderable; variety comes from
  the camera, and environments may return to the home set.
- Never direct a beat as a literal act-out of the VO's words — direct the EMOTION of the
  beat (eyes, posture, hands, light); the VO carries the facts.
- Never render a computer/phone screen close-up without a reference image — a legible
  screen appears only in scenes attaching the real screenshot (the product still);
  everywhere else screens are ambient out-of-focus glow.
- Never let the product's identity drift — it is the polished Pixar-style 3D prop from the real photo — real shape, label, logo,
  text and colors fully readable — in every product scene.
- Never make a character uncanny: dead eyes, uncanny-valley faces, horror styling, and
  gore are banned; large expressive appealing eyes are the law.
- Never break the Character Bible's wording between scenes; only the emotion-state slot moves,
  and only forward through the arc.
- Never let witnesses react to the art style — they react to the story only (the deadpan
  conceit), and every witness is a Pixar-style character.
- Never generate on-screen text of any kind, and never add captions, day labels, or offer
  banners at assembly — the VO carries the milestones and the offer; the stitcher has no
  caption path.
- Never blanket-ceil a duration — round to nearest (≥.5 up, <.5 down, clamped 4–9).
- Never render a line under 3.5s as its own generation — merge it with a neighbor. The
  hook line ALWAYS merges with the next line; the last-position CTA is the only exception.
- Never trim, silence-cut, stretch, or re-voice the VO to fit the picture — the voice is
  the untouchable master; fit the picture to it (freeze-holds at stitch).
- Never stitch before frame-checking every clip against the word timeline, and never fix a
  timing mismatch by re-rendering — re-cut the existing footage.
- Never render on a changed plan without re-presenting the per-clip span/generation/cost
  table and getting a fresh yes.
- Never let a generation run 10s+; size it to the VO line.
- Never end the ad on anything but the CTA / product beat.
- Never let a clip's generated audio contain music or speech — real-world SFX only.
- Never re-describe the start image's contents in scene 1's hook-beat direction — motion
  only; the still carries the look. Never render the hook line as its own solo clip, and
  never make the hook BEAT itself multi-shot (it is one continuous 1-2s shot before the
  merged line's cuts begin).
- Never start a render (including re-rolls) while a member question is unanswered or
  without a fresh explicit yes.
