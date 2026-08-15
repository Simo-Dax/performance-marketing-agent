# Generation Architecture — Talking-Object Ad Factory (Seedance 2.0, dialogue-first)

Single source of truth for how a Talking-Object Ad is built. Read it before any step.
This factory shares the family's gates, banks, and verification discipline with the
Clay/Skeleton/Pixar factories — but its AUDIO MODEL IS INVERTED: **there is no external
voiceover. The characters speak on camera, and Seedance generates their voices and the
picture TOGETHER, in the same generation.** Do not import the VO-first factories' audio
rules; they do not apply here.

## Member-locked HARD RULES (override anything below that conflicts)

1. **THE CAST CARRIES THE AD.** Every word is spoken by a character on screen, in first
   person, mouth animated and loosely synced. Dialogue clips render AUDIO ON with the
   exact line and the locked voice casting in the prompt. No external VO is recorded, no
   voice file is ever uploaded. (A narrator is legal only confined to ONE clip — a
   narrator spread across clips comes back as a different voice each time.)
2. **THE REFERENCE LADDER (member-locked, the three tiers):**
   - **Tier 1 — generic character, no real product in frame, speaks once:** NO reference
     of any kind. Pure text-to-video; the character bible in the prompt carries the
     design. (Proven: the enzyme test.)
   - **Tier 2 — a real product in frame (talking or not):** the reference image is
     REQUIRED — the approved CASTING STILL (full-cast mode: the product with the face
     built into its real label) or the approved PRODUCT STILL (dignity mode), each
     generated FROM the member's real photo. Real shape, label, text and colors must
     read; a product never renders from text description.
   - **Tier 3 — a speaking character appearing in a SECOND clip:** its FIRST rendered
     dialogue clip is attached as the VIDEO reference — an image carries the face, but
     only the video carries the VOICE. The prompt changes everything else: a brand-new
     environment and a never-used angle (the escalation law fully applies).
   **Tier 3 is this skill's ONE exception to the family's video-reference ban** — allowed
   ONLY for a recurring speaker, ONLY for voice+face continuity. A video reference for
   any other purpose (style, composition, scene continuation) stays BANNED.
3. **DIALOGUE IS THE ONE PLACE RE-RENDER REPLACES RE-CUT.** The voice is baked into the
   pixels — if the rendered character speaks the wrong words, no edit can fix it. Every
   dialogue clip is whisper-verified against its script line (`dialogue_check.py`) before
   it counts as done; a flubbed line = a re-render (with its own fresh yes). Timing and
   visual issues are still fixed in the edit, never with credits.
4. **Never repeat a camera angle+scale anywhere in the ad**, and **every speaking
   character gets its OWN world — no environment repeats**; worlds alternate domestic ↔
   inside-the-body (the primary bank's world grammar).
5. **Re-hook every cut** — a new character, a new world, a new register on every scene.
6. **Scene simplicity + emotion-first.** One clear signature action per scene, renderable
   by current models. Direct the FEELING ("The emotion is the subject" in every prompt);
   the dialogue speaks the facts, the eyes/posture/light show what they feel like.
7. **NEVER render a computer/phone screen close-up without a reference image** — legible
   screens only in scenes attaching the real screenshot; ambient glow everywhere else.
8. **NO on-screen text — except the CTA's in-scene 3D promo text.** No captions, no
   subtitles, no burned word-overlays (the source ads' caption style is NOT reproduced;
   the stitcher has no caption path). The single exception: the CTA clip may stage the
   offer as diegetic glowing 3D text IN the scene — a prop, not an overlay — and the
   payload's `on_screen_text` names it (the only scene where that field may be non-empty).

## The model in one breath

- A Talking-Object Ad is a **character-driven direct-response commercial**: the
  customer's problem personified self-roasts (the hook), 2–4 ingredient/feature heroes
  introduce themselves and their mechanism ("Hi, I'm ___. I may help ___…"), the
  product(s) enter as the assembled answer, and the product itself asks for the sale,
  pointing at the link. 5–8 scenes, 30–60s, vertical 9:16 at 1080p.
- **The world is one cohesive cute Pixar-style 3D animated world** (the app's locked
  talking-object style block). Every character is the object itself with a face built
  into its own body — big expressive eyes, a visible animated mouth, tiny arms. NO real
  humans, ever.
- **Audio is native.** Each clip's dialogue (and its world's soft ambience) comes out of
  the generation. The stitcher KEEPS the clips' audio, concatenates, and
  loudness-normalizes to ~-14 LUFS. Nothing is overlaid on top. No music (an editor-side
  choice after delivery, never part of this pipeline).
- **Scenes come from the SCENE BANK, never from nothing.** The PRIMARY bank
  (`scene-bank-ingredient-parade.md`) outranks everything: fill its shells first, or
  synthesize in its grammar, and record `source_shell` ("T01".."T07" or "synthesized")
  per scene.
- **Durations come from the WORDS** (~2.8 words/second including acting pauses):
  `requested_seconds = clamp(round(words / 2.8), 4, 9)`. There is no upfront audio to
  align — the performance IS the clock. After rendering, `dialogue_check.py` measures
  the real speech span; trims land at stitch (`trim_out` = speech end + a beat of hold,
  never past the clip).
- **Render waves replace full parallelism.** Wave 1 = every speaker's FIRST scene; wave 2
  = recurring speakers' later scenes, each carrying its own speaker's wave-1 clip as the
  video reference. The HOOK renders first, alone, as the checkpoint.

## Why the ladder is shaped this way

A generic one-off speaker needs nothing: the bible IS the design, the voice casting IS
the voice, and nobody sees the character twice — drift cannot exist. A real product's
label CAN drift, and label drift kills trust — so the real still is non-negotiable the
moment the product is in frame. A recurring speaker's VOICE drifts because Seedance casts
it fresh per generation — and the primary bank's own source proves the face drifts too
(its product characters' eye style visibly changes between their two scenes). The video
reference carries both. That is the whole ladder: **reference exactly what can drift,
and nothing else.**

## The flow, end to end

```
INTAKE (product/offer + photo, the customer's problem, ingredients/features, mode full-cast|dignity)
   │
   ▼  THE CAST (Step 1): villain + heroes by personality=mechanism, worlds assigned
   │   (alternate domestic ↔ inside-body), a prop per claim, a voice casting per character
   │
   ▼  SCRIPT (Step 2): script.json — pure dialogue, the formula chorus, 11–25 words/line
   │
   ▼  GATE 1: member approves the SCRIPT + CAST (lines, voices, worlds, props, mode)
   │
   ▼  CASTING STILLS (Step 3, tier 2 only): personified-product casting still (and/or
   │   product still) from the real photo via the Studio talking-object template; approved
   │   cheap before any video. Tier-1 characters need NO still.
   │
   ▼  STORYBOARD (Step 4): fill/synthesize from the PRIMARY bank; storyboard.json
   ▼  segment_scenes.py → scenes.json  (word-count durations, waves, voice_ref, tiers)
   │
   ▼  PROMPTS (Step 5): dialogue prompt per scene → payload_*.json; validate_prompt.py each
   │
   ▼  GATE 2: storyboard + the EXACT per-clip table (words, est. seconds, wave, references,
   │          per-scene cost) + the RE-RENDER CONTINGENCY note + path A/B/C/D
   │
   ▼  GENERATION:
   │     1. describe the HOOK's shot plan → approve → render the hook ALONE (tier 1: no ref)
   │     2. dialogue_check.py + frame_check.sh on the hook → ask "happy with the character,
   │        the voice, and the line?" → re-roll until yes (wrong words = re-render, rule 3)
   │     3. describe every remaining scene's plan → "render wave 1?"
   │     4. on yes: render ALL remaining wave-1 scenes IN PARALLEL (tier-2 scenes attach
   │        their approved stills)
   │     5. dialogue_check + frame_check each; flubbed lines re-render (fresh yes each)
   │     6. WAVE 2 (recurring speakers): each scene renders with its speaker's approved
   │        wave-1 clip as the VIDEO reference + a new environment; verify the voice matches
   │
   ▼  VERIFY (Step 6.5): frame_check.sh sheets + dialogue_check.py reports, every clip
   │
   ▼  build_manifest.py → talking-object-ad-manifest.json
   ▼  stitch_talking.sh → out/talking_object_ad.mp4  (native audio kept, hard concat,
       -14 LUFS, no caption path)
```

TWO hard stops: GATE 1 (script + cast) and GATE 2 (storyboard + cost). During generation:
the hook checkpoint, the "render wave 1" yes, and a fresh yes per re-render.

## The data files (all under `$WORK`)

| File | Written by | Purpose |
|---|---|---|
| `script.json` | you (Step 2) | The cast + the dialogue: `{concept, niche, mode, target_seconds, characters:[{id, name, kind, tier, bible, voice, world, prop}], lines:[{id, role, speaker, dialogue}]}`. Approved at Gate 1. |
| `inputs/casting-still.png` / `inputs/product-still.png` | Step 3, the Studio talking-object template | The approved tier-2 references, generated from the member's real photo. |
| `storyboard.json` | you (Step 4) | `{scenes:[{scene_id, line_ids, role, speaker, visual, action, prop, world, emotion, sfx_note, on_screen_text, source_shell}]}`. |
| `scenes.json` | `segment_scenes.py` | Per-scene `{scene_id, role, speaker, dialogue, voice, word_count, est_seconds, requested_seconds, wave, tier, voice_ref_source, trim_in, trim_out, clip, …}` (reference/images live in the Step-5 payloads, not here). |
| `payload_<scene_id>.json` | you (Step 5) | The dispatch contract per scene. Validated before render. |
| `checks/<scene_id>.json` | `dialogue_check.py` | The whisper verdict per rendered clip: transcript, match ratio, missing/extra words, speech_end. |
| `spec.json` | you (Step 7) | Input to the manifest builder. |
| `talking-object-ad-manifest.json` | `build_manifest.py` | The assembly contract (native audio; no vo_track exists in this skill). |
| `out/talking_object_ad.mp4` | `stitch_talking.sh` | The final 9:16 1080p ad. |

## Reference types (per scene — the ladder, encoded)

- **Tier 1 scene** (generic speaker, first appearance, no product in frame):
  `reference: {type:"none"}`, `images: []`. Nothing attached.
- **Tier 2 scene** (real product in frame): `reference: {type:"none"}`, `images` carrying
  `inputs/casting-still.png` (full-cast) and/or `inputs/product-still.png` (dignity /
  un-personified product shots). The CTA is ALWAYS tier 2.
- **Tier 3 scene** (recurring speaker, wave 2): `reference: {type:"video",
  source:"clips/<the speaker's first scene>.mp4"}` + `voice_ref_source` naming that clip
  — plus the tier-2 images when a product is in frame (a recurring product character
  carries BOTH its wave-1 clip and its casting still). The prompt commands a brand-new
  environment and angle: the reference carries the character and the voice, never the
  scene.
- A video reference in ANY other configuration is a validation FAIL — `validate_prompt.py`
  rejects `type:"video"` without a legal `voice_ref_source`.
- **Tier semantics in `scenes.json`:** the `tier` field records the STILL tier (1 =
  generic, no stills; 2 = real product, still required). RECURRENCE is what makes a
  scene ladder-tier-3: any wave-2 scene carries the video voice reference, whatever its
  still tier — a recurring generic speaker is wave 2 + tier 1 (video ref, images empty);
  a recurring product speaker is wave 2 + tier 2 (video ref + its approved still).

## Roles & structure

`role` ∈ `hook, mechanism, product, cta` (DR labels legal). The first scene is the
villain HOOK; the last is the CTA — the product asking for the sale, pointing down;
nothing follows it. `build_manifest.py` enforces ends-on-CTA. One speaker per scene
(a declared duo counts as one speaker); a scene mixing two speakers' lines is a
structural error (exit 3).

## Sizing: the words are the clock

- `est_seconds = word_count / 2.8` (the flagship's measured rate, acting pauses included).
- `requested_seconds = clamp(round_half_up(est_seconds), 4, 9)`.
- A line over 25 words CANNOT fit a 9s clip — `segment_scenes.py` hard-fails (exit 3):
  trim the line, or split it into two scenes (the split makes the speaker recurring —
  wave 2, video ref, new environment).
- A line under ~11 words renders at the 4s floor with silent acting business padding the
  clip (a WARN, not an error — the footage is used, not wasted; direct the business in
  the prompt).
- After render, `dialogue_check.py` reports the real `speech_end`; set the scene's
  `trim_out` to speech_end + 0.3–0.6s of hold (never past the clip's end, never cutting
  a word). The stitcher trims video+audio together.

## Directing dialogue clips (the prompt anatomy)

Every dialogue prompt carries, in order (the proven enzyme-test shape):

1. **One continuous shot line** — "One single continuous shot. No cuts, no camera changes
   mid-shot." (Dialogue scenes hold ONE shot — the character's performance IS the
   footage; sub-shot montage grammar belongs to the VO-first factories. NEVER state the
   clip's total duration in seconds — the duration field sets it.)
2. **CAMERA** — the angle+scale (checked against the ad's angle map; never repeated) +
   one slow move (push-in is the format's native).
3. **WORLD** — this character's own world, concrete props and light, "charming and
   storybook-like, never gross" for body-interiors.
4. **CHARACTER** — the bible VERBATIM.
5. **ACTION** — timestamped beats: the signature business, the turn to lens (the hook
   beat: eyes meet the lens inside the first 1–2s), the line delivery, the prop payoff on
   the claim words, the button (a blink, a flex, the point-down).
6. **THE EMOTION IS THE SUBJECT:** the named feeling, carried by eyes/posture/light.
7. **DIALOGUE** — `The [character] says, in [the locked voice casting]: "<the exact line,
   word for word>"` + "mouth animating naturally with the words, loosely synced".
8. **AUDIO** — "Only the character's voice and [the world's soft ambience] underneath.
   No music, no narrator, no other voices."
9. **VISUAL STYLE** — the locked Studio talking-object block (drop the product-surface
   clause for organic characters).
10. **The law lines** — "No real people anywhere in frame — every character is a cute
    3D animated talking object. No on-screen text or captions." (the no-text sentence
    drops on the CTA scene only — its staged offer text is legal there). **The master
    negative goes in the payload's `negative_prompt` FIELD, never inside the prompt
    text** — embedded there, its banned-look tokens would read as requests (and fail
    validation); on Path A it is handed over as its own separate block.

Tier-3 prompts open with one extra line FIRST: "Match the attached reference video's
character EXACTLY — the same face, the same body, and the SAME VOICE — but this is a
brand-new scene in a brand-new location: do NOT copy the reference's environment,
framing, or camera."

## Audio model (inverted from the VO-first family)

- **The clips' native audio IS the ad's audio.** Dialogue + each world's soft ambience,
  generated by Seedance, kept at stitch. `keep_sfx` does not exist here; there is no
  ducking pass because there is nothing to duck under.
- **No voice file is ever uploaded** (`--audio` is never used). The voice is cast by the
  prompt's description; continuity for recurring speakers comes from the tier-3 video
  reference.
- **No captions, no overlay text** — the one text allowance is the CTA's in-scene 3D
  promo text, rendered by the generator as part of the scene.
- Final mix loudness-normalized to ~**-14 LUFS** across the concatenated whole.

## The manifest (assembly contract)

```
talking-object-ad-manifest.json = {
  concept, niche, date, fps: 30, resolution: "1080x1920", media_type: "video",
  framework, audio_mode: "native", total_seconds, references,
  scenes: [ { scene_id, role, speaker, clip, trim_in, trim_out, reference,
              voice_ref_source, on_screen_text } ]
}
```

`build_manifest.py` enforces: audio_mode "native" (a `vo_track` in the spec is an ERROR —
wrong factory); the last scene's role is `cta`; every span > 0 and ≤ a sub-10s render;
`on_screen_text` empty everywhere except the CTA.

## Generation order & the human checkpoints

1. **Describe the hook's plan** in plain language (the villain, its world, the business,
   the line) → approval → **render the HOOK alone** (tier 1 — no reference).
2. **Verify the hook twice:** `frame_check.sh` (does the character land, mouth visible,
   world right) AND `dialogue_check.py` (does it SAY the line, word for word). Show the
   member: "Happy with the character, the voice, and the delivery?" Wrong words =
   re-render (hard rule 3), with its own fresh yes.
3. On yes: **describe every remaining scene's plan** → "render wave 1?"
4. On yes: **render all remaining wave-1 scenes IN PARALLEL** (tier-2 scenes attach their
   approved stills). `dialogue_check` + `frame_check` each as it lands.
5. **Wave 2** (only if a speaker recurs): each scene attaches its speaker's APPROVED
   wave-1 clip as the video reference (`voice_ref_source`), new environment, new angle.
   Verify the voice matches by ear on top of the standard checks.
6. Flubbed lines re-render with a fresh yes each; visual/timing issues fix in the edit.
7. Assemble once with `build_manifest.py` + `stitch_talking.sh`.

If the member asks a question at ANY point, answer fully and STOP; never render while a
question is pending. Every render, including re-rolls, needs its own fresh explicit yes.

## Cost & the re-render contingency

Same engine economics as the family: ~**9 credits/sec at 1080p** on Higgsfield (Path
B/D), per-second dollars on fal (Path C), free on Path A. Two talking-object-specific
lines in every Gate 2 table:

- **Wave structure**: wave-2 scenes render only after their voice_ref clip is approved —
  they cannot join the parallel batch.
- **RE-RENDER CONTINGENCY**: dialogue can flub — Seedance occasionally drops, swaps, or
  invents words, and only a re-render fixes it (hard rule 3). Quote the total with a
  ~+30% contingency line ("if N clips flub their lines, +X credits") so a re-render is
  never a surprise. `dialogue_check.py` is the judge; the member gives the yes.

## Hard "never"s

- Never record, upload, or overlay an external voiceover — the characters' native
  dialogue IS the audio. Never upload a voice file or attach a voice reference.
- Never render a dialogue clip AUDIO OFF, and never strip a dialogue clip's audio at
  stitch.
- Never attach a video reference EXCEPT a recurring speaker's own wave-1 clip (tier 3,
  voice_ref_source) — and never let that reference carry the scene: new environment, new
  angle, always.
- Never render a recurring speaker's second scene before its first clip is approved.
- Never render a real product (talking or not) without its approved still attached —
  tier 2 is non-negotiable; a product never renders from text.
- Never attach any reference to a tier-1 scene — a generic one-off speaker renders from
  the bible alone (a needless reference just narrows the render).
- Never accept a dialogue clip whose whisper check fails — wrong words = re-render (the
  one place re-render replaces re-cut); and never re-render for TIMING (trim to
  speech_end instead).
- Never let two speakers share a scene (a declared duo is one speaker); never let a
  narrator span more than one clip.
- Never repeat an environment or an angle+scale anywhere in the ad.
- Never render a real human or photoreal person in any frame.
- Never generate burned captions/subtitles, and never add text at assembly — the one
  legal text is the CTA's in-scene 3D promo text (and the real product's own label).
- Never render a computer/phone screen close-up without the real screenshot attached.
- Never make a character uncanny, gross, or scary — cute, charming, lovable is the law.
- Never break a character's bible or voice-casting wording between scenes.
- Never state the clip's total duration in the prompt text; timestamped action beats are
  fine.
- Never let a generation hit 10s or more; a >25-word line is a script bug (exit 3).
- Never end the ad on anything but the CTA — the product pointing at the link.
- Never generate before Gate 2's approval, never render on a changed plan without
  re-presenting the table (the re-approval law), and never start any render while a
  member question is unanswered.
