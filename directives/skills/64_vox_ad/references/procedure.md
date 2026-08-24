---
name: vox-ad
description: "A voiceover-first VOX paper-collage ad factory — the editorial-zine format where the voice tells the story and familiar paper-cutout objects POP onto the poster exactly on the words that name them. Writes a short concrete-noun script (default 25 seconds, user picks 10–40 at intake), the user voices it once in ElevenLabs and drops the audio back in, then this skill aligns the voice with faster-whisper, builds a WORD-TO-OBJECT beat map (every strong noun, number, brand and verb gets a familiar object: real logos, feed ad cards, calendars, coins, magnifying glasses, trash bins, halftone magazine-cutout people), generates one approved 2K collage KEYFRAME per clip on Nano Banana 2, renders each clip on Seedance 2.5 from an empty background so the elements assemble INTO the approved keyframe as its final frame, then MEASURES every element's actual arrival frame-by-frame and retimes the footage in a single ffmpeg filter graph so every pop lands within a quarter second of its spoken word. LITERAL-first: whatever the voice names is what appears — the product itself when the voice names the product (physical products ride as pixel-faithful photographic stickers from the real photo, packaging never re-lettered; software brands end on the real glowing logo). Text is rationed, not banned: banners only for spoken words, huge condensed lettering, baked into keyframes, everything readable at 1080p. No music ever — the finished ad is the untouched voiceover plus the clips' own retimed paper-foley under it. Camera locked in every clip; nothing moves position after it lands. Trigger on /pm-vox-ad, /pm-vox-ad, /pm-vox-ad, and natural language like make a vox ad, vox collage ad, paper collage ad, paper cutout ad, editorial collage video. Output under 21_Vox_Ads/: one word-synced assembled ad plus raw clips, keyframes, beat map, timing and arrivals reports, and manifest. Seedance 2.5 + Nano Banana 2, via the agent's paths: A manual paste, B Higgsfield CLI, C fal.ai pay-per-result (gated by fal-ai-prerun-check),  If the user names a different skill, command, plugin, or tool for the job, or is building or testing their own skill, do not trigger this skill; use what they named instead."
---

# the agent VOX Collage Ad Factory (Seedance 2.5, voiceover-first, keyframe-anchored, word-synced)

You are the orchestrator of a **VOX collage ad** factory — the editorial paper-cutout
format: a voiceover tells the whole story, and matte paper-cutout objects pop onto a flat
poster **exactly on the words that name them**. You write the script, the user voices it
once in ElevenLabs, and you turn that voice into one polished 9:16 1080p commercial:
approved collage keyframes assemble themselves clip by clip, measured and retimed until
every element lands on its word.

**Read `references/generation-architecture.md` first — it is the single source of truth.**
Then read `references/vox-style.md` (the style block, palette law, paper physics, and the
measured Seedance behaviors) and `references/vox-scripting.md` (the nouns-you-can-cut
writing rule and the swipe scripts). The two banked builds
(`references/beat-bank-andromeda.md`, `references/beat-bank-same-tools.md`) are real
shipped ads torn down beat by beat — the structural source for beat maps.

There are TWO mandatory hard stops. END YOUR TURN at each and wait for an explicit human
reply:
- **GATE 1 (Step 2.5):** the user approves the transcript — the exact words they will
  voice (no visuals yet) — before they spend any ElevenLabs effort.
- **GATE 2 (Step 4.5):** the user approves the beat map (the word-to-object map), the
  keyframe list, the exact per-clip span/generation/waste/cost table, and the path before
  a single image or clip renders.

Never spend Higgsfield credits or fal.ai dollars without an explicit yes
at GATE 2 (and a fresh yes for every render after it).

## HARD RULES (user-locked — these override anything below that conflicts)

1. **LITERAL-FIRST: whatever the voice names is what appears on screen.** The voice says
   tool → a tool pops in. Says review → a gold-star review card. Says reads → a magnifying
   glass. This is the exact INVERSE of the skeleton/pixar emotion-first law — in VOX the
   named thing IS the picture. No abstract metaphors unless the user asks for one.
2. **THE WORD-TO-OBJECT LAW: every strong noun, number, brand name and punchy verb in the
   transcript gets its own familiar object, landing ON that word.** The beat map is a
   table: spoken words → object → target time. An unmapped strong word is a validation
   failure. Weak words ("of", "the", "so") get nothing — that is the rhythm.
3. **FAMILIAR OBJECTS ONLY.** Things a viewer recognizes in half a second: real logos,
   social feed ad cards, calendars, coins, flames, trophies, arrows, notification badges,
   trash bins, magnifying glasses, push-pin evidence boards, speech bubbles, halftone
   magazine-cutout people. Every card face carries blank bars, never lettering.
4. **THE PRODUCT IS THE OBJECT.** When the voice names the product, the product itself
   appears — never a proxy. A physical product renders as a pixel-faithful PHOTOGRAPHIC
   sticker with a torn white paper edge, generated with the real product photo attached as
   the image reference: packaging never re-lettered, re-colored, redrawn, or re-typeset.
   The product enters at the turn and owns the final frame (the hero frame).
5. **ONE KEYFRAME PER CLIP, AND THE CLIP ENDS ON IT.** Every clip renders from an EMPTY
   background and assembles INTO its approved keyframe: the prompt always carries "START
   on the empty flat background with NOTHING on it" and "The FINAL FRAME must match the
   reference image exactly: same objects, same positions, same scale." The keyframe is
   attached as an IMAGE REFERENCE — never as a start image (a start image would open the
   clip on the finished poster).
6. **CAMERA STATIC, LOCKED, in every clip.** The energy is pop-ins: overshoot bounces,
   slams, deals, stamps, draw-ons, with small bursts of paper fragments. Every video
   prompt carries "Nothing moves position after it lands."
7. **TEXT IS RATIONED, NOT BANNED** (the family break). A banner may exist ONLY for words
   the voice actually speaks (the CTA line) or a codename that cannot be drawn. Banners
   are huge bold condensed lettering, at least one twelfth of the frame tall, BAKED INTO
   THE KEYFRAME — never added in the video step, never added at assembly. No small print
   anywhere, no lettering on card faces, everything readable at 1080p. Packaging small
   print melts at any resolution — never promise it; keep the product at hero scale.
8. **MATTE PAPER EVERYWHERE; GLOW IS RESERVED FOR THE HERO.** Every generated element is
   matte — "no glow, no light effects" in every non-hero prompt. Exactly one frame may
   glow: the brand logo (software) or the lit product hero (physical), anchored from the
   real file, the only luminous thing in the whole film.
9. **PEOPLE ARE PRINTED CUTOUTS.** Halftone duotone magazine-photo cutouts with a thick
   clean white outline, in the ad's palette. Every video prompt with people carries "The
   people stay as flat printed cutouts, no realistic motion" — without it the model brings
   them to life and breaks the collage.
10. **NO MUSIC, EVER.** The finished ad is the untouched ElevenLabs voiceover plus the
    clips' own paper-foley sfx, retimed with the picture and mixed well under the voice.
    Every prompt ends "No music, no added audio." No voice is ever uploaded to a
    generator; no character ever lip-syncs.
11. **SYNC IS FIXED IN POST, NEVER BY RE-RENDERING.** Seedance compresses the back half
    of every clip (measured: pops arrive 0.5–1.3s early). That is EXPECTED. The sync step
    measures every element's real arrival and retimes the footage free. A re-render is
    only for wrong or missing CONTENT, and needs its own fresh explicit yes.
12. **THE WASTE LAW.** Seedance's floor is 4 seconds. The gate table shows every clip's
    voice span, generation length, and wasted seconds, and the beat split is chosen to
    minimize total generated seconds. Phrases under 3.5s NEVER get their own clip — they
    merge with a neighbor (the merge law). Never generate 23 seconds for an 18-second ad
    when 20 is possible.
13. **Third-party logos are allowed with a caution.** Real tool/platform logos ride as
    image references and land as paper stickers. Fine for organic and community posts;
    NOTE to the user in the gate that paid Meta creative containing third-party logos
    risks rejection.

## The model in one breath

- A VOX ad is **voiceover-driven and word-synced**. One continuous ElevenLabs voiceover
  (default ~25 seconds) tells the story; the screen shows the named things popping in on
  their words. The voice is laid OVER the picture at assembly and is never altered.
- **The look is one locked style block** — mixed-media hand-cut paper collage, torn
  edges, halftone dots, real drop shadows, matte, NOT CGI — pasted BYTE-IDENTICAL into
  every keyframe prompt, with a palette pulled from the Brand DNA hex codes. That block,
  not a character, is the consistency anchor (`vox-style.md`).
- **One clip per phrase group.** Phrase boundaries come from the real recorded voice
  (faster-whisper alignment). Each clip has one approved 2K keyframe (Nano Banana 2) and
  renders on Seedance 2.5 from empty background INTO that keyframe, 9:16 1080p, integer
  4–9s sized by CEIL over the voice span (the waste law picks the split).
- **Anchors ride as image references only on the frames that show them:** the real
  product photo (physical), the real brand logo (the hero frame), any third-party tool
  logos. Everything else is pure text-to-image.
- **Generation: clip 1 first as the checkpoint, then the rest in PARALLEL** — every clip
  depends only on its own approved keyframe, never on another clip. Video references are
  never attached.
- **Then the sync pass:** measure arrivals frame-by-frame per element region, compare to
  the word timeline, retime in ONE ffmpeg filter graph (per-segment stretch/compress plus
  dead-hold cuts, sfx retimed with inverse atempo), mix sfx ~19 dB under the voice,
  loudness-normalize to -16 LUFS, re-measure, and show the user the offset table as
  proof. Target: every element within 0.25s of its word.
- **The ad ends on the hero frame** — the product (physical) or the glowing logo
  (software) plus the spoken CTA banner.

Cost on Higgsfield (Path B) is about **9 credits/sec at 1080p**; keyframes on Nano
Banana 2 are cheap (a few credits / cents each); fal bills per result, confirmed at
runtime. The leverage is a tight script, approved keyframes, parallel clips, and fixing
all timing free in post.

---

## Step 0.5. Resolve the project folder, the scripts, and the whisper venv (RUN FIRST)

Outputs land in the working folder Claude Code is open in, under `the agent/`. Run:

```
PWD_ABS="$(pwd)"
TARGET="${PWD_ABS}/the agent"
PROTECTED=0
case "$PWD_ABS" in
  "$HOME"|"$HOME/"|"/"|"/tmp"|"/tmp/"|"$HOME/Downloads"|"$HOME/Desktop")
    PROTECTED=1 ;;
esac
if [ "$PROTECTED" = "1" ] && [ ! -d "$TARGET" ]; then
  echo "PROTECTED:$PWD_ABS"
elif [ ! -f "$TARGET/_meta/folder-confirmed.flag" ] && [ ! -d "$TARGET" ]; then
  echo "FIRSTRUN:$TARGET"
else
  mkdir -p "$TARGET/23_VOX_Ads" "$TARGET/_meta"
  echo "READY:$TARGET"
fi

# Seed brand memory (CLAUDE.md) if the brand folder exists and the file
# is missing. Idempotent and silent when there is nothing to do.
```

- `PROTECTED:<path>`: refuse and tell the user to open Claude Code in a brand-specific
  subfolder. Stop.
- `FIRSTRUN:<path>`: ask "I'll save outputs to `<path>/`. First time saving in this folder, is that correct? (yes/no)". On yes, create the folders and write `<path>/_meta/folder-confirmed.flag`, then continue. On no, stop.
- `READY:<path>`: capture it as `$AILAB` and continue silently.

Resolve the skill's scripts and the shared whisper venv:

```
SCRIPTS="directives/skills/64_vox_ad/scripts"
echo "SCRIPTS=$SCRIPTS"
WHISPER_VENV="$HOME/.cache/pm-agent/whisper-venv"
[ -x "$WHISPER_VENV/bin/python" ] && echo "whisper venv: ready" || echo "whisper venv: created at Step 3"
```

Once the concept is named (Step 2), set `$WORK="$AILAB/23_VOX_Ads/<concept-slug>"` and
`mkdir -p "$WORK/clips" "$WORK/keyframes" "$WORK/out" "$WORK/inputs" "$WORK/audio"`.

### Auto-discover saved assets

- **VOC & Brand DNA** (the script's pain language and the palette's hex codes):
  ```
  ls -t "$AILAB/01_VOC_Research/voc-"*.html "$AILAB/01_VOC_Research/"*.md 2>/dev/null | head -n 1
  ls -t "$AILAB/01_VOC_Research/foundation-"*.html 2>/dev/null | head -n 1
  ls -t "$AILAB/02_Brand_DNA/"*.html "$AILAB/02_Brand_DNA/"*.md 2>/dev/null | head -n 1
  ```
- **Product photo and brand logo** — scan `$AILAB/_assets/` (and the Brand Brain asset
  index) before asking the user to upload anything.

---

## Brand Brain, the compiled brand memory (when present)

If `$AILAB/_knowledge/context-pack.md` exists, load `../../_shared/brand_brain.md` and follow it before any creative decision: the pack's hard rules and forbidden phrasing are binding, its winning and losing angles steer concepting, and its inventory lists what already exists so nothing gets recreated. Check its `assets-index.md` for existing product photos and logos BEFORE asking the user to upload anything. If `_knowledge/` does not exist, skip silently and continue — never create it (the desktop app compiles it).

---

## Step 0. INTAKE

When VOC and Brand DNA exist, DERIVE the niche and the pain from them. Ask the user
only what cannot be derived:

| Input | Required | One-line purpose |
|---|---|---|
| Product / offer | Yes | What is being sold. Drives the turn and the CTA line. |
| Product type | Yes | physical / software / service — decides the hero frame: physical ends on the product sticker, software/service ends on the glowing brand logo. |
| **Ad length** | **Ask, default 25 seconds** | "How long should the ad be? (default 25 seconds)" — accepted 10–40s. Sets the word budget (~2.2 words/sec; 25s ≈ 55 words). |
| Product photo | Yes when physical (the hero frame always shows it) | The real photo — the image reference for every keyframe that shows the product. |
| Brand logo file | Yes when software/service | The real logo file — anchored in the hero keyframe, the only glowing thing in the film. |
| Third-party logos | Optional | Real tool/platform logos the script names (each rides as an image reference). Note the paid-Meta caution (hard rule 13). |
| Niche / audience / pain | Derived | From VOC/Brand DNA; ask only if no research exists. |

No voice clip is collected here — the voice is rendered later in ElevenLabs and dropped
in at Step 3.

---

## Step 1. THE ANGLE + THE PALETTE LOCK

Mine the VOC for the highest-intensity pain and the verbatim customer language; honor the
brand voice rules and the forbidden phrases. Pick ONE story shape (the banks show two:
the platform-villain arc and the sameness-vs-input arc) and state it in one sentence.

If a Foundation Pack turned up (`foundation-*.html`, built by /pm-dati-qualitativi Phase 3), apply `../../_shared/voc_brand_reader.md` R.9: it decides WHAT to say (the avatar, the big idea, the named mechanisms, the objection responses, and which of the 6 purchase beliefs this piece installs); the VOC document stays the source of verbatim customer language.

**Palette lock:** extract 2–4 hex codes from the Brand DNA (background dark, paper light,
one bright accent; gold reserved for review stars when reviews appear). Write them into
`palette.json` under `$WORK`. If the brand already shipped a VOX ad, SHIFT the background
shade (the banks shifted #081425 → #18284A) so no two VOX ads look identical.

---

## Step 2. SCRIPT (the voiceover transcript only)

Load `../../_shared/hook_anatomy.md` before writing any hook: the three-ingredient weights (the written line carries most of the hook; the first frame is a floor, never a substitute), the text-candidate rule (draft at least 3 written hook candidates and keep the best; rendered hook assets stay at exactly one), and the HA.3 first-frame gate, which runs as a named criterion at this skill's existing approval checkpoint and never triggers a render on its own.

Also load `../../_shared/natural_voice.md` and run its filter silently on every line before the
transcript is written. It is the house voice law and it binds this skill exactly as it binds the
other script factories: HARD RULE 1 for flowing spoken sentences, HARD RULE 2 for the anti-AI
pattern filter, and HARD RULE 3 for comprehension, a twelve-year-old getting every line on the
first hearing, with each hard word either present in the VOC or landed in the same breath.

Its "short punchy sentences" note below is about the WORD-TO-OBJECT map, not a licence to write
fragments. Sentences stay spoken and connected; what stays short is the distance between cuttable
nouns.

Write ONLY the spoken voiceover. Read `references/vox-scripting.md` and obey its one law:

**WRITE NOUNS YOU CAN CUT OUT OF PAPER.** Every sentence must name concrete, drawable
things — tools, ads, calendars, reviews, coins, a bin, a loop. A sentence with no
cuttable noun is a rewrite. This is what makes the word-to-object map possible.

- Length: the user's target (default 25s ≈ 55 words at ~2.2 words/sec). Err short.
- Short punchy sentences; every strong word earns screen time. The turn names the brand;
  the last line is the spoken CTA (it becomes the only banner).
- Carry at least one verbatim VOC phrase or the product's named mechanism when research
  exists, and clear every forbidden phrase.
- Name the concept, set `$WORK`, create its folders, copy the product photo / logo files
  into `$WORK/inputs/`.

Write `transcript.json` under `$WORK`:

```
{ "concept": "...", "product_type": "physical|software|service",
  "target_seconds": 25,
  "lines": [ {"id": "l01", "role": "hook", "vo": "<exact spoken line>"}, ... ] }
```

Roles: `hook, problem, agitate, turn, mechanism, payoff, cta` — the final line's role is
always `cta`.

---

## Step 2.5. GATE 1 — TRANSCRIPT APPROVAL (mandatory hard stop)

Give the user EXACTLY two things:

1. **The transcript**, line by line with roles, confirming the estimated length against
   their target. Name which line is the VOC anchor and where the turn lands.
2. **The ElevenLabs hand-off**: the transcript as one copy-pasteable block (one line per
   beat for natural pauses) plus a voice design ("Male or female to match the brand,
   direct, confident, conversational narrator — never salesy"), with:

   > Create this voice in ElevenLabs, render the transcript as ONE continuous voiceover
   > (one voice, no music baked in), leave a clear breath after the problem's last line,
   > and drop the file into `21_Vox_Ads/<concept>/audio/`. Tell me when it's in.

Then STOP and END YOUR TURN. No visuals, no beat map, no prompts yet.

---

## Step 3. AUDIO ANALYSIS (align the voice to the script)

PREREQUISITE: the user approved the script and dropped a VO file into `$WORK/audio/`.

Provision the shared voice-alignment engine once (idempotent — shared with the clay,
skeleton and pixar skills):

```
WHISPER_VENV="$HOME/.cache/pm-agent/whisper-venv"
if ! "$WHISPER_VENV/bin/python" -c "import faster_whisper" 2>/dev/null; then
  echo "Setting up the voice-alignment engine (one time, about 1 to 2 minutes)..."
  python3 -m venv "$WHISPER_VENV" 2>/dev/null \
    && "$WHISPER_VENV/bin/python" -m pip install -q -U pip wheel 2>/dev/null \
    && "$WHISPER_VENV/bin/python" -m pip install -q faster-whisper 2>/dev/null \
    && echo "voice-alignment engine ready" \
    || echo "NOTE: align_vo.py will fall back to proportional timing."
fi
python3 "$SCRIPTS/align_vo.py" "$WORK/transcript.json" "$WORK/audio/<vo-file>" "$WORK/timing.json"
echo "exit=$?"
```

`timing.json` carries each line's `start`, `end`, `dur`, plus `total_seconds` and
`method`. Report the real total against the user's target (over-target means cut a line
and re-voice — the picture is never rushed to fit). Show the per-line timing table. The
real recorded length IS the film length from here on; the plan follows the voice.

---

## Step 4. THE BEAT MAP (word-to-object map + clip split + keyframe list)

This is the storyboard of a VOX ad. Three artifacts, built in order:

Before mapping a single word, load `../../_shared/visual_invention.md`. In VOX the free
axes are the OBJECT choice, its scale against the poster, and where it lands in the
composition, so an unexpected-but-instantly-readable object beats the obvious one every
time. The format's own law bounds it: objects stay familiar and simple in silhouette,
because a cutout has to read in the quarter second it pops. Push the choice, never the
complexity, and never let invention break the word it is illustrating.

1. **The word-to-object map** — a table over the transcript: `spoken words → object →
   target time` (times from `timing.json`). Apply hard rules 1–4: literal-first, every
   strong word mapped, familiar objects only, the product itself when named. Check the
   two beat banks for proven object choices before inventing one. Explicitly list the
   UNMAPPED words and confirm each is weak (function words) — an unmapped strong word is
   a bug.
2. **The clip split** — group phrases into clips at natural sentence boundaries. THE
   MERGE LAW: a phrase under 3.5s never gets its own clip; pair it with its neighbor.
   Write `beatmap.json` (`clips: [{id, line_ids:[...]}]`) and run:
   ```
   python3 "$SCRIPTS/segment_beats.py" "$WORK/beatmap.json" "$WORK/timing.json" "$WORK/beats.json"
   echo "exit=$?"
   ```
   It computes each clip's film span (boundaries at the midpoint of the silence between
   lines), sizes the generation by **CEIL over the span, clamped to integer 4–9s**,
   hard-fails on a mergeable short clip or a span over 9s, prints the
   span/generation/waste table, and totals the waste. **Pick the split with the least
   total waste** (the waste law); the table is shown at the gate.
3. **The keyframe list** — one composition per clip, described in a sentence each:
   which mapped objects, where, which anchors ride as references (product photo / brand
   logo / tool logos), which frame carries the banner (the CTA hero frame only, plus a
   codename frame when one exists), and which frame is the HERO (glow/product exception).

---

## Step 4.5. GATE 2 — BEAT MAP + COST (mandatory hard stop)

Present in chat:
1. The word-to-object map (the full table — this is what the user is really approving).
2. The clip split table from `segment_beats.py`: per clip its voice span, generation
   seconds, waste, and film position — plus totals (film seconds, generated seconds,
   total waste). State it in one line: "generating Xs for a Y.Ys film, the minimum this
   split allows."
3. The keyframe list with anchors and the hero frame named. Note the third-party-logo
   caution when tool logos appear (hard rule 13).
4. The **path** (A / B / C) and a cost preview in that path's unit: keyframes
   (Nano Banana 2, one per clip + rerolls) AND clips (Seedance, total generated seconds).
   Path C reads fal.ai pricing first.

Then STOP and END YOUR TURN. Treat silence as rejection. THE RE-APPROVAL LAW: any change
after this gate — an object, a clip split, a duration, a path — voids the approval;
re-present the updated tables and get a fresh explicit yes.

---

## Step 5. KEYFRAMES (wave A — every still approved before any video)

Read `references/vox-style.md`. For each clip write one image prompt and build
`kf_<clip_id>.json`:

- **The style block from `vox-style.md`, BYTE-IDENTICAL in every prompt**, followed by
  the palette line with the locked hex codes. This is the consistency anchor — any
  variation between frames is a bug.
- The scene: the mapped objects in their final composition, sizes and positions explicit,
  generous empty space, "matte, NOT CGI, NOT a 3D render, no glow" (except the hero
  frame).
- Text law per frame: banner words verbatim in double quotes with the size floor (one
  twelfth of frame height), and the closing line "This is the ONLY text in the image…"
  or "NO TEXT AT ALL anywhere in this image." Card faces are blank bars. Numbers a
  calendar or badge carries (a "6", a "99+") count as markings, not lettering.
- People frames: the halftone duotone magazine-cutout treatment with the white outline.
- Anchor frames: name the attachment and the reproduce-exactly clause ("Do not re-letter,
  re-colour, redraw or re-typeset…"). The HERO frame: the real logo "the only glowing
  thing in the picture" (software) or the product sticker at hero scale (physical).
- 9:16, 2k resolution, on Nano Banana 2 (the chosen path's shared implementation doc
  names the image model id; GPT Image 2 is the fallback renderer).

Validate every payload, passing the transcript so banner words are checked against the
spoken words:

```
python3 "$SCRIPTS/validate_vox_prompt.py" "$WORK/kf_clip_01.json" "$WORK/transcript.json"
```

Render wave A on the approved path, then show EVERY keyframe and iterate free-form until
the user approves each one ("Happy? (yes / tell me what to change)"). Save approved
stills to `$WORK/keyframes/<clip_id>.png`. **All keyframes approved is the precondition
for any video.** Rerolls of an image are cheap; say the price anyway and get the yes.

---

## Step 5.5. CLIP PROMPTS

For each clip write the video prompt from the template (and validate):

> Animate this still as a paper collage motion graphic. START on the empty flat
> <background color> background with NOTHING on it. Every element arrives as a paper
> cutout sticker popping in with a snappy overshoot bounce and a small burst of paper
> fragments. The FINAL FRAME must match the reference image exactly: same objects, same
> positions, same scale.
>
> BEAT TIMELINE:
> <t1>s: <first object> pops in and settles.
> <t2>s: <next object> SLAMS / deals / stamps / draws itself in…
> <…one line per mapped object, in spoken order, timestamps from timing.json relative to
> the clip start…>
> <tail>s to end: everything holds in the reference layout, torn edges fluttering,
> halftone dots pulsing.
>
> Camera static, locked off. Flat 2D paper, no 3D rotation, no photoreal, no glow. <the
> people guard when people are in frame> <the anchor guard: "The logo/product/lettering
> stays perfectly sharp, stable and unchanged once it lands."> Nothing moves position
> after it lands. No jump-cuts. No music, no added audio.

- Timestamps are TARGETS, not promises — the model compresses the back half (hard rule
  11); spread beats across the full generation length and fix the landing in Step 6.5.
- More beats pace better: the banks measured that a clip with 5–7 mapped objects follows
  its schedule far more closely than a clip with 2 (the model fills gaps by rushing).
- `payload_<clip_id>.json`: prompt, duration (from `beats.json`), `aspect_ratio "9:16"`,
  `resolution "1080p"`, `reference {"type":"image","source":"keyframes/<clip_id>.png"}` —
  the keyframe as an IMAGE REFERENCE, never a start image, never a video reference.

```
python3 "$SCRIPTS/validate_vox_prompt.py" "$WORK/payload_clip_01.json" "$WORK/transcript.json"
```

---

## Step 6. GENERATION (Seedance 2.5 — clip 1 first, then the rest in PARALLEL)

PREREQUISITE: Gate 2 approved, every keyframe approved, every payload validated. Common
settings: Seedance 2.5, 9:16, 1080p, integer duration from `beats.json`, the clip's
keyframe attached as the image reference, no voice ever uploaded; clip audio (paper
foley) generates automatically and is kept for the mix.

1. **Render CLIP 1 ALONE** (fresh yes with its cost). Frame-check it (Step 6.5's
   contact sheet), show the user, ask "Happy with how the collage moves?" Re-roll only
   on their yes-to-spend.
2. On yes, **render every remaining clip in PARALLEL** — each depends only on its own
   approved keyframe. Download to `$WORK/clips/<clip_id>.mp4`; assert each returned
   duration ≈ requested.

- **Path A — manual paste.** Hand over each prompt with its duration, 9:16, 1080p, and
  which keyframe to attach as the image reference. The user drops each result into
  `clips/<clip_id>.mp4`. No automation cost.
- **Path B — Higgsfield CLI.** Load `../../_shared/path_b_cli_implementation.md`. Seedance
  id `seedance_2_5`; `--aspect_ratio 9:16 --resolution 1080p --duration <n>`; **attach the
  keyframe with `--image "$WORK/keyframes/<clip_id>.png"` — NEVER `--start-image`**, and pass
  **`--mode omni_reference`** with it (2.5's default `t2v` refuses reference media) (a
  start image opens the clip on the finished poster and kills the assembly). Keyframes
  render first with the Nano Banana model id from the shared doc. Launch the parallel
  wave with `&` + `wait`.
- **Path C — fal.ai.** Gate with `fal-ai-prerun-check`. Model
  `bytedance/seedance-2-5.0/reference-to-video`; verify the input shape with the fal-ai
  MCP `get_model_schema`; the keyframe goes in the image-reference slot. Confirm cost
  with `get_pricing`; submit the wave as a batch.
> **There is no Path K in this agent.** KIE AI is mapped but not wired --- see
> `execution/kie_api_map.md`. Do not attempt to route a render through it.

### Never-do for any path
- Never generate without a fresh explicit yes (keyframes, clip 1, the parallel wave,
  every re-roll).
- Never attach a keyframe as a start image, and never attach any video as a reference.
- Never render clips before every keyframe is approved.
- Never render while a user question is unanswered.
- Never silently switch paths on an error — ask.

---

## Step 6.5. SYNC (measure, retime, verify — the step that makes it a VOX ad)

Never declare sync from the prompt. Measure it:

1. **Frame-check each clip** (`bash "$SCRIPTS/frame_check.sh" clips/<id>.mp4 …`), read
   the contact sheet, confirm every mapped object actually rendered and the final frame
   matches the keyframe. A dropped object or mangled anchor is a CONTENT problem — the
   user decides on a re-render (fresh yes). Everything else proceeds.
2. **Measure arrivals.** Write `checks_<id>.json` — one entry per mapped object with its
   normalized frame region, search window, and target time (clip-relative from
   `timing.json`) — then:
   ```
   python3 "$SCRIPTS/measure_pops.py" "$WORK/clips/<id>.mp4" "$WORK/checks_<id>.json" "$WORK/arrivals_<id>.json"
   ```
3. **Author the retime plan** (`sync-plan.json`): per-clip segments with speed factors
   that put each measured arrival on its word — stretch early sections, compress late
   ones, CUT dead holds (a frame-diff flatline is free footage to remove; the tool
   prints them). The film boundaries are the spans from `beats.json`; the tail of the
   last clip may hold ~0.5–1.5s past the last word as the end card.
4. **Build.** `python3 "$SCRIPTS/build_sync.py" "$WORK/sync-plan.json" "$WORK/out/vox_ad.mp4"`
   — ONE ffmpeg filter graph: per-segment video trim + setpts, the clips' own foley
   retimed with the inverse atempo, straight concat, sfx at ~0.11 gain under the
   untouched VO, loudnorm to -16 LUFS, 24fps CFR. (The graph exists because concat
   demuxers and `-ss` before `-i` corrupt retimed timestamps — never assemble any other
   way.)
5. **Verify.** Re-run `measure_pops.py` against the FINISHED film with absolute targets
   and show the user the offset table — every element, its word, target, actual, and
   the miss. The bar: every element within **0.25s**; re-plan and re-build (free) until
   it holds. The two banked ads shipped at 10/10 and 10/10 within 0.12s median.

---

## Step 7. DELIVER + VALIDATION CHECKLIST

Deliver under `$WORK` (`$AILAB/23_VOX_Ads/<concept-slug>/`), printing absolute paths:
- `out/vox_ad.mp4` — 9:16 1080p, -16 LUFS, voice + retimed paper foley, ends on the hero
  frame with the spoken CTA banner.
- `keyframes/*.png`, `clips/*.mp4`, `audio/` (the untouched VO), `transcript.json`,
  `timing.json`, `beatmap.json`, `beats.json`, `arrivals_*.json`, `sync-plan.json`,
  `palette.json`, and the inputs in `inputs/`.

Confirm every line:

- [ ] Every strong noun, number, brand and verb in the transcript has an object that
      lands within 0.25s of its word (the final offset table proves it).
- [ ] The voice names the product → the product itself appeared (photographic sticker
      from the real photo, packaging untouched); the hero frame is the product (physical)
      or the real glowing logo (software), the only luminous thing in the film.
- [ ] Every clip started on empty background and ended matching its approved keyframe;
      keyframes rode as image references only — never start images, never videos.
- [ ] The style block was byte-identical across every keyframe prompt; the palette hexes
      came from the Brand DNA.
- [ ] Camera locked everywhere; nothing moved after landing; people (if any) stayed flat
      printed cutouts.
- [ ] The only text anywhere: spoken-word banners (and undrawable codenames), huge
      condensed, baked into keyframes; card faces blank; no small print; readable at 1080p.
- [ ] No music anywhere; the VO was never trimmed, stretched, or re-voiced; sfx are the
      clips' own foley, retimed with the picture, ~19 dB under the voice; -16 LUFS.
- [ ] Every generation was an integer 4–9s sized by ceil-over-span; no mergeable phrase
      rendered solo; the gate table showed the waste and it was the minimum split.
- [ ] All timing fixes were cuts/stretches in the sync graph — zero re-renders for
      timing.
- [ ] The ad ends on the hero frame + CTA; nothing follows it.


### Offer captions

The ad is finished and clean. Ask once, then respect the answer:

> Want captions burned on? I'll add them in your locked house style, mostly 2-3 words a
> card, and keep this clean master untouched as a separate file.

On yes, run the `auto-captions` skill on the finished file. It force-aligns to
this ad's own script on disk, so the captions match the copy word for word instead of
inheriting whisper's guesses. On no, deliver as is. Never caption without asking, and
never replace the clean master.

## NEVER DO
- Never map a strong word to nothing, and never put an abstract metaphor where the named
  thing could pop in instead (literal-first).
- Never show a proxy when the voice names the product; never re-letter, re-color, or
  redraw packaging or logos; never promise small-print legibility at 1080p.
- Never bake a banner for words the voice does not speak (codenames excepted); never add
  text in the video step or at assembly; never letter a card face.
- Never let anything glow except the single hero frame's logo/product.
- Never attach a keyframe as a start image; never attach a video reference; never render
  a clip before its keyframe is approved; never render anything before GATE 2.
- Never move the camera, and never let elements drift after landing.
- Never render a person as anything but a flat halftone magazine cutout, and never omit
  the no-realistic-motion guard when people are in frame.
- Never add music, upload a voice, or alter the VO file in any way.
- Never fix timing with a re-render; measure, cut, stretch, re-verify — free.
- Never skip the offset table; "it looks synced" is not a measurement.
- Never generate more total seconds than the minimum split allows without saying so at
  the gate (the waste law), and never blanket-round durations up past the ceil.
- Never assemble with a concat demuxer over retimed segments or trim with `-ss` before
  `-i` — one filter graph, always.
- Never edit another skill, and never write outputs outside the `23_VOX_Ads/` tree.

## Helper files
- `references/generation-architecture.md` — the single source of truth. READ FIRST.
- `references/vox-style.md` — the byte-identical style block, palette law, paper physics,
  pop-in vocabulary, people/product/anchor treatments, and the MEASURED Seedance
  behaviors (back-half compression, beat-density pacing, dead holds).
- `references/vox-scripting.md` — nouns-you-can-cut, length/word budget, structure, the
  ElevenLabs hand-off, both swipe scripts.
- `references/beat-bank-andromeda.md` — banked build 1 (23.6s, 5 clips): the full
  word-to-object map, timings, corrections, final offsets.
- `references/beat-bank-same-tools.md` — banked build 2 (17.6s, 4 clips): ditto, with
  people frames, an evidence board, and an assembly-side dead-hold cut.
- `scripts/align_vo.py` — voice-to-line timing map (shared engine; Step 3).
- `scripts/segment_beats.py` — clip spans, ceil-sized generations, the merge law, the
  waste table (Step 4).
- `scripts/validate_vox_prompt.py` — keyframe + clip payload validation: style block,
  palette, text law vs the transcript, empty-start/final-frame laws, camera lock, no
  music (Steps 5 and 5.5).
- `scripts/measure_pops.py` — per-element arrival measurement from frame regions
  (Step 6.5; self-bootstraps Pillow into the shared venv).
- `scripts/build_sync.py` — the single retime + mix + loudnorm filter graph (Step 6.5).
- `scripts/frame_check.sh` — per-clip contact sheet (Steps 6 and 6.5).
- `../../_shared/natural_voice.md` — the house voice law: flowing spoken sentences, the anti-AI
  filter, and the comprehension bar (Step 2, on every VO line).
- `../../_shared/path_b_cli_implementation.md` — shared Higgsfield CLI workflow (Path B).
