# Scene Bank — BEFORE & AFTER (UGC Studio format 02), full teardown of two winning ads

Two member-supplied winning before/after UGC ads, torn down word-for-word and frame-by-frame
on 2026-07-10 (faster-whisper word timestamps + frame grids, the local method). Second seed
bank for the UGC Studio skill. Same rules as `scene-bank-testimonial.md`: shells recreate
their source scenes exactly; fills swap the product, category, story specifics, settings,
and wardrobe while keeping the STRUCTURE; one shell serves at most ONE scene per ad; record
`source_shell` (B01…, D01…, or "synthesized") in every storyboard. Every shell below carries
its render-audit verdict (2026-07-10): GREEN renders as written, YELLOW renders with the
stated adaptation, RED never renders and the stated replacement fills the slot. Render
mechanics — the three lanes, the macro bans, THE EDIT GRAMMAR — live in `render-laws.md`;
this bank applies them.

THE DURATION LAW: every generation is an integer 4–9 seconds, always. THE CAPTION LAW: our
renders ship CLEAN — source A's title sticker and source D's caption spine are editor-side
layers; at fill time a caption-carried source converts to a VO spine by default (the caption
text ships as a sidecar `captions.txt` for the member's editor — burned captions only if the
member explicitly asks). THE CLAIMS LAW: the sources' brand names and results ("Olimon
June's spring collection", visible lash growth in 2 months) are legal-risk slots — fills use
the member's sanctioned claims only, and any results shown follow the compliance gates.

Two laws this format adds on top of those:

**THE PROOF-ANCHOR LAW.** The transformation proof anchors — the frames a viewer inspects
to believe the change — are ALWAYS the member's real before/after photos, never generated.
Both banked winners prove in macro-ban territory (fingernails, eyes/lash line — zones that
NEVER render, per `render-laws.md`), so every proof frame in a fill is a 2K still-insert
built FROM the real photos, animated motion-only or cut in as a still.

**THE ONE-GEN RHYME LAW.** A pose-rhyme comparison NEVER spans two generations. There is no
set-lock — sets, wardrobe, and light drift between generations, and a drifted frame kills
the very diff that IS this format. The before pose and the after pose render as hard-cut
sub-shots of ONE generation (one prompt, the same references: "[t1] same pose, hands over
face, bare nails / [t2] same pose, finished nails"); the cutter slices them apart and the
EDL places [t1] at the timeline's head and [t2] at its tail. This is the law for every
pose-rhyme comparison this bank fills, not a per-ad trick.

## What these two ads prove (measured)

| | Ad A "manicure reset" (narrated) | Ad D "lash serum" (silent dump) |
|---|---|---|
| Length | 17.5s | 10.5s |
| Words / pace | 75 / **4.30 wps** | 0 (music only, caption-carried) |
| Hook | disbelief-retrospective, lands by 2.2s | timestamp-origin caption, frame one |
| Shots | **16 distinct shots**, median 0.95s (2 couch blocks + a 7-cut macro run) | **4 near-still selfie clips**, median 2.53s |
| The comparison device | POSE RHYME (after mirrors the before pose) | TIME JUMP (a different day per clip — see the calendar downgrade for fills) |
| Product on screen | color fan to lens + macro application | serum wand in shot 1 only |
| Close | "truly obsessed with how they turned out" | "and after WITHOUT" (the strongest proof last) |

This is the SHORTEST format banked so far: 10–20 seconds total. Before/after ads spend no
time persuading — the picture is the argument; the words (when present) only narrate it.

## RHYTHM CARD (measured 2026-07-10 — the stitcher's QC targets read from here)

**Ad A (manicure reset, 17.4s narrated):** 16 distinct shots, median 0.95s (!), shortest
0.67s, longest 2.03s. The process montage is a run of 7 consecutive macro cuts at
0.80–1.03s, each a DIFFERENT nail/color (repetition with variety is the mechanic). 14 of
15 cuts land mid-sentence, ~12 mid-WORD, over one continuous first-person VO (75 words,
4.30 wps, longest inter-word gap 0.34s) — audio is the spine, picture free-floats. The ONE
sentence-boundary cut is the world change (couch→macro at 6.07s on "reset."): setting
changes get the period, nothing else does. Jump cuts: the couch hook block is medium →
punch-in ECU → medium (same pose, tighter crop — one gen, three shots via crop punch-in);
the fan block is 4 same-setup take jumps. Word-action lock: the pearl placed as "pearls"
lands at 12.80s, cut 0.03s after word onset. Spine-and-return: couch (shots 1–6) → macro
world (7 cuts) → couch return at 12.83 for the pose-rhyme after-reveal, escalating (reveal
→ spread → claw wiggle). Payoff hold: closing shots 1.73–2.03s ≈ 2x median. Shot length is
U-SHAPED: ~2s hook, 0.7–1.0s middle, 1.7–2.0s payoff.

**Ad D (lash serum, 10.5s silent):** 4 shots, median 2.53s, cuts at 3.27/6.10/8.27s. Zero
speech; the caption spine changes exactly ON each cut (converts to a VO spine at fill per
the caption law). Music-only, continuous. Every cut is a TIME JUMP (a different day via
light/location/hair per the calendar downgrade). Soft pose rhyme: same face angle across
clips 2–4 so only the lashes read as changed. The strongest proof (after-WITHOUT-mascara)
lands last and is held. Near-still photo energy invites inspection.

**Format pace:** ~4.3 wps narrated.

**QC targets the stitcher reads:** narrated median ≤1.2s, no shot >4s except the close;
silent variant median ~2.5s.

---

## AD A — "Spring manicure reset" (narrated before/after with process montage)

Creator: woman, long brown hair, floral top + dark overalls. Home base: living-room couch
selfie, gallery wall of framed prints behind. Macro set: warm neutral close-up surface for
the application shots (source footage — fills never render this set; see B03). First-person
VO narrates continuously OVER the footage (she is on camera but the words play as
voiceover — no lip-sync dependence). Source burns a persistent "SPRING NAILS" title sticker
top-center (source-only; ours ship clean).

### The voiceover (verbatim, whisper-timed)

"I still can't believe my nails looked like this just this morning, dull and chipped so I
decided it was time for a spring manicure reset. With a little bit of reconstruction and
the best color combo from Olimon June's spring collection, this was the reset my nails
needed. I had to add some pearls just to be a little extra and I have to say I am truly
obsessed with how they turned out."

### The arc map

| # | t | Role | What's on screen |
|---|---|---|---|
| B01 | 0.0–3.4 | hook + BEFORE reveal | She raises BOTH hands over her face, bare dull nails filling the lens on "looked like this"; the before IS the hook |
| B02 | 3.5–6.0 | decision + product fan | Back to couch smile, then a fan of 4–5 pastel polishes held up covering her face, peek + point |
| B03 | 6.1–9.9 | process montage pt.1 | MACRO: thin art brush paints a colored french tip, ~1s per cut, a DIFFERENT nail + color each cut (pink, red, yellow, teal) |
| B04 | 10.0–14.1 | process montage pt.2 + detail | More macro tips; on "add some pearls" a tweezer places a white pearl on the red tip — the VO's words land exactly on the matching micro-action |
| B05 | 14.4–17.5 | AFTER reveal (pose rhyme) | The EXACT opening pose repeated with finished nails — hands over face → hands spread wide → bent-finger claw wiggle |

### The systems this ad banks

- **The POSE RHYME.** The after reveal repeats the before reveal's exact pose and framing
  (hands over face, couch, same distance). The comparison needs no split screen and no
  labels — the brain diffs the two identical frames automatically. This is the format's
  core mechanic, and at fill time the match is GUARANTEED, never hoped for: B01 and B05
  are hard-cut sub-shots of ONE generation (the ONE-GEN RHYME LAW above), sliced apart
  and placed at the timeline's head and tail.
- **Audio is the spine.** The VO plays continuously over everything with zero lip-sync
  dependence — which is why every still flash and punch-in overlay below rides it for
  free. 14 of 15 cuts land mid-sentence; the picture free-floats on the word timeline.
- **The before IS the hook.** No setup: frame one is the flaw while the VO says "I still
  can't believe… looked like this just this morning." Disbelief-retrospective phrasing
  (confession family) + the visual evidence, inside 2.2s. At fill the couch pose carries
  the hook and the lens-filling proof frame is the REAL before photo, flashed as a
  still-insert punch-in (fingernails never render).
- **The process montage sells the transformation.** ~1s macro cuts, each a DIFFERENT nail
  and color — repetition with variety. In the source this is real macro footage; in a fill
  fingernail macro NEVER renders (banned zone), so the run assembles as 0.8–1.0s
  still-insert flashes from the member's real process/finished photos, punched in over the
  continuous VO. The repetition-with-variety mechanic survives intact; the render risk
  doesn't.
- **Word-action lock — edit-side only.** "add some pearls" lands on the exact frame a
  pearl is placed (cut 0.03s after word onset). At fill time this is an EDIT-side
  guarantee: the detail still-flash is CUT at its named word's onset on the whisper
  timeline. It is never a render promise — in-generation timing is unreliable.
- **The color-fan product beat.** All variants held up as one fan covering her face —
  product-as-mask, range-in-one-frame. A 4–5-variant fan breaks the
  one-product-reference-per-generation law, so fills build the fan as a 2K variant-run
  still-insert from EVERY shown variant's real photo. The "extra" detail ("just to be a
  little extra") adds personality to the process.
- **The obsessed close.** No CTA ask at all — the close is pure satisfaction ("truly
  obsessed with how they turned out") over the after poses, HELD ≈2x the median per the
  rhythm card. Before/after ads may legally end on delight; the member's offer can ride a
  caption or the ad copy instead.
- **4.3 wps.** The fastest measured pace in the bank — narrated before/afters sprint.

### Scene shells

House prompt shape applies (less-is-more; product size inline when on screen; "No
on-screen text or captions." always).

**Shell B01 — THE BEFORE-AS-HOOK ([t1] of the rhyme generation).**
VERDICT: **YELLOW (adaptation)** — never renders alone and never in macro: it is [t1] of
the ONE rhyme generation shared with B05, and the lens-filling nail proof is the member's
real before photo as a still-insert flash, never a rendered frame.
Mechanic: the flaw fills frame one while a disbelief-retrospective line plays — the pose
carries the hook, the real-photo flash carries the proof.
> THE RHYME GENERATION (B01 [t1] + B05 [t2] — one prompt, the same references):
> Living-room couch selfie, gallery wall behind. [t1] She raises both hands and covers her
> face, [THE BEFORE STATE: dull chipped nails / the flawed thing] showing toward the lens,
> pose held. [t2] HARD CUT: the exact same pose, same framing, same distance — hands over
> face with [THE AFTER STATE] — then hands spread wide, face bare and unobstructed, then a
> playful show-off claw wiggle. Delivery: can't-believe-it into obsessed. Voiceover
> carries the words.
Fill slots: the before state, the after state, the flaw words, the satisfaction words.
Sizing: 8s (≈6.7s of speech → 7s round-to-nearest, +1s hook buffer, ≤9s). Two hard-cut
sub-shots — within the 2–3 ceiling. This gen is also the ad's IDENTITY CHECKPOINT: [t2]'s
hands-spread beat must show the clean, bare, unobstructed face (a hands-over-face frame
can never be the checkpoint, per `render-laws.md`). And its internal cut is the one
content-critical cut in this bank: scene-detect must find the [t1]/[t2] hard cut — a MORPH
(the before state transforming on screen) is wrong content and goes to the member as a
re-render proposal, not an edit-side rescue.

**Shell B02 — THE DECISION + RANGE FAN.**
VERDICT: **YELLOW (adaptation)** — a 4–5-variant fan breaks the one-product-reference-
per-generation law and label fidelity needs every real photo; the fan fills as a
still-insert, and the decision line rides it as voiceover (this format has no lip-sync
dependence).
> 2K still-insert, built from EVERY shown variant's real photo: [ALL VARIANTS / THE KIT]
> fanned together toward the lens, filling the frame, product-as-mask. Animated
> motion-only (slight hand sway, a peek past the fan) or cut as a still. VO carries:
> "[so I decided it was time for + THE RESET NAME]."
At stitch the fan footage is sliced into 3–4 take-jump shots (interior trims + crop
punch-ins), each jump a visible state change: fan up / peek / point.

**Shell B03 — THE PROCESS MONTAGE (still-flash run).**
VERDICT: **RED (replacement)** — fingernail macro is a banned zone and NEVER renders
(`render-laws.md`). The montage assembles instead as ~1s still-insert flashes from the
member's REAL process/finished photos.
> 6 still-inserts, 2K, each built from a DIFFERENT real photo: [THE APPLICATION / THE
> PIECE: a painted tip, a color, a smoothed edge] — one variant per still. Cut in as
> 0.8–1.0s flashes / punch-in overlays over the continuous VO: "[the process + the
> range/brand line]."
Fewer real photos than planned flashes → crop punch-ins on the stills you have make up
the count, or the run shortens honestly. Never invent a photo.
COMPLIANCE: the named collection/brand is the member's own.

**Shell B04 — THE DETAIL BEAT (word-locked still flash).**
VERDICT: **RED (replacement)** — same macro ban as B03; the signature micro-action never
renders. It lands as ONE still-insert flash cut AT its named word's onset on the whisper
timeline — the word-action lock is an edit-side guarantee, never a render promise.
> One 2K still from the real photo of [THE SIGNATURE DETAIL: the pearl on the tip / the
> final swipe / the clasp closed]. The cutter places it ON "[THE NAMED WORD]" (the
> winner's pearl cut lands 0.03s after word onset). VO: "[I had to add + THE DETAIL +
> just to be a little extra]."

**Shell B05 — THE AFTER REVEAL (pose rhyme, [t2] of the rhyme generation).**
VERDICT: **YELLOW (adaptation)** — never its own generation: it renders only as [t2] of
B01's rhyme generation (the ONE-GEN RHYME LAW), and the lens-filling after proof is the
member's real after photo as a still-insert flash, mirroring the before flash.
Prompt: see B01 — one prompt carries both poses. The escalation (reveal → spread → claw
wiggle) plays inside [t2] as one continuous arc; the cutter slices it into the three
closing shots with interior trims (jump cuts with visible state changes).
LAW: same setting, same pose, same distance as [t1] — guaranteed by sharing the
generation, never by hoping two generations match.

### How Ad A fills — corrected procurement (conservation rule applied)

The source runs 16 measured shots. The macro ban displaces the montage, the detail beat,
and the fan from the video lane — under the CONSERVATION RULE those setups come back as
still-insert flashes and crop punch-ins, never deleted. One generation plus ~10 approved
stills buys the full 16-shot density.

| lane | id | covers | spec | size |
|---|---|---|---|---|
| gen | G1 — THE RHYME GEN | B01 [t1] + B05 [t2] | one prompt, same references, 2 hard-cut sub-shots; identity checkpoint ([t2] spread = clean bare face) | 8s |
| still | S1 | B01 proof | 2K from the REAL before photo — the flaw legible, nails to lens | ~1s flash |
| still | S2 | B02 | 2K variant-run fan from every shown variant's real photo, motion-only | ~2.5s, sliced ×3 |
| stills | S3a–S3f | B03 | 6 stills from real process/finished photos, each a different piece/color | 0.8–1.0s flashes |
| still | S3g | B04 | the DETAIL still, cut at its named word's onset | ~1s flash |
| still | S4 | B05 proof | 2K from the REAL after photo — the finished state to lens | ~1s flash |

### The shot-level cut map (what the EDL places — 16 shots, median ≈0.9s)

| # | source | shot | ~len |
|---|---|---|---|
| 1 | G1 [t1] | medium hook — hands over face, before state | 2.0s |
| 2 | S1 | punch-in overlay: REAL before photo, the flaw fills the lens | 0.9s |
| 3 | G1 [t1] | overlay return to medium — lands mid-word | 0.9s |
| 4–6 | S2 | fan take-jumps ×3 — fan up / peek / point (interior trims + crop punch-ins) | 0.8–1.0s each |
| 7–12 | S3a–f | the macro run: 6 flashes, each a DIFFERENT piece/color | 0.8–1.0s each |
| 13 | S3g | the DETAIL flash, cut ON its named word's onset | 1.0s |
| 14 | G1 [t2] | couch return — the after reveal, the exact opening pose | 1.7s |
| 15 | S4 | punch-in overlay: REAL after photo, the finished state fills the lens | 0.9s |
| 16 | G1 [t2] | hands spread wide → claw wiggle, HELD; 0.6–0.8s reaction tail after the last word | 2.0s |

G1 legally feeds four non-adjacent shots (1, 3, 14, 16 — spine-and-return, no frame
reuse); the [t1] before block and the [t2] after block bookend the timeline exactly as the
ONE-GEN RHYME LAW requires. Shots 2 and 15 are the proof anchors — both REAL photos, both
punch-in overlays riding G1's continuing audio (zero audio surgery). Cut-rhythm QC:
median ≈0.9s (target ≤1.2s narrated), longest 2.0s (≤4s); the ONE sentence-boundary cut is
the world change into the macro run (6→7, on the "reset."-equivalent period) — every other
cut lands at a word onset, most mid-sentence, over the continuous VO. Ends on the
creator's gesture, never an end card.

---

## AD D — "Lash serum, 2 months" (silent clip-dump, caption-carried)

Creator: young woman, long dark hair. NO VOICE — music only (hot mix, peaks at 0dB). FOUR
near-still selfie clips, ~2.6s each, every one a DIFFERENT day (different outfit, location,
light in the source footage) — the visible day changes ARE the elapsed time. A small
creator-handle watermark sits mid-frame (source-only). The caption spine carries the whole
story:

1. "2 months ago randomly started using lash serum every night" — golden-hour close-up,
   serum wand applying along the lash line (the only product appearance).
2. "before with mascara" — cool indoor light, blue top, pearl necklace, direct stare,
   sparse mascara'd lashes.
3. "after with mascara" — grey hoodie, hoop earrings, new location, dramatic full lashes,
   same face angle and eye contact.
4. "and after WITHOUT" — soft daylight close crop, pearl earring, bare lashes visibly long
   and curled. The strongest frame is saved for LAST.

### The systems this ad banks

- **Time-jump proof — with THE CALENDAR DOWNGRADE (fill law).** Nothing claims the
  result — visibly different days do. In the source the timestamp is outfit + light +
  location per clip. At fill time, on any GENERATED clip, elapsed time reads through
  lighting + location + hairstyle changes per clip; an outfit change requires its own body
  reference — a second outfit REQUIRES a second body ref, no ref, no outfit change (see
  intake). The member's real photos are exempt: they carry their own honest timestamps,
  outfits included, because they are real.
- **The comparison ladder.** Not one before and one after: before-with-help →
  after-with-help → after-WITHOUT-help. The ladder escalates believability and saves the
  strongest proof for the final frame — and every rung is a REAL photo (the proof-anchor
  law).
- **The timestamp-origin hook.** "2 months ago randomly started…" — origin-story line over
  the application shot. "Randomly" does the authenticity work (no sponsorship energy).
- **Near-still photo energy — the still-insert lane's home turf.** Each clip is almost a
  photograph: micro head movement, held eye contact, no gestures. A 2K still built from
  the member's real photo, animated motion-only, IS this energy — the format and the lane
  are the same shape. The stillness invites the viewer to inspect, and what they inspect
  is real.
- **Same-pose comparability.** Face angle and eye contact match across clips 2–4 (the pose
  rhyme again, softer). Only the lashes change. At fill the soft rhyme lives in the
  member's photo SELECTION — pick ladder photos with matching face angles — not in
  prompts; real photos cannot drift, which is the whole point.
- **The caption→VO conversion law (fill-time).** Our renders never burn captions. Default
  fill: the caption spine becomes a third- or first-person VO spine with the same four
  lines' content (the words are already beat-sized), and the caption text ships as
  `captions.txt` for the member's editor. A member who explicitly wants the silent version
  gets clean clips + the sidecar, never burned text.

### Scene shells

**Shell D01 — THE ORIGIN APPLICATION.**
VERDICT: **YELLOW (adaptation)** — the eyes/lash line are a banned macro zone: the
wand-on-lash-line contact never renders legibly. Preferred fill: a 2K still-insert from
the member's real application photo, motion-only. Only if no such photo exists does the
beat generate — reframed, and standing alone at the 4s floor (every neighbor beat is a
still, so there is no gen to merge with; the plan-cut trims the floor slack).
> Still route (preferred): 2K still from the real application photo — golden-hour
> close-up selfie, [THE APPLICATOR: serum wand / dropper / tool] at [THE TREATED AREA],
> eyes steady at the lens. Motion-only: micro head movement.
> Gen route (fallback, 4s): Golden-hour selfie, face and shoulders in frame. She raises
> [THE APPLICATOR] toward [THE TREATED AREA], eyes steady at the lens, near-still, micro
> movement only. [THE TREATED AREA] never fills the frame.
VO (converted spine): "[N months ago I randomly started + THE HABIT + every night]."

**Shell D02 — BEFORE, WITH HELP.**
VERDICT: **RED (replacement)** — the proof is the lash line, a banned macro zone, and the
proof-anchor law forbids generating it anyway. Fills as a 2K still-insert from the
member's REAL before-with-aid photo, animated motion-only (micro head movement, held eye
contact) or cut as a still.
> 2K still from the real photo: a different day, [the photo's own outfit and light].
> Direct-to-lens stare, the face angle every later rung will match. [THE BEFORE STATE
> with the usual aid visible]. VO: "[before, with THE USUAL AID]."

**Shell D03 — AFTER, WITH HELP.**
VERDICT: **RED (replacement)** — same ban, same law: the member's REAL after-with-aid
photo as a 2K still-insert, motion-only. Pick a photo whose face angle matches D02's —
the soft rhyme is a selection decision, not a prompt.
> 2K still from the real photo: a different day again. The SAME face angle and eye
> contact. [THE AFTER STATE with the usual aid — visibly improved]. VO: "[after, with
> THE USUAL AID]."

**Shell D04 — AFTER, WITHOUT (the closer).**
VERDICT: **RED (replacement)** — the strongest proof frame is ALWAYS real (the
proof-anchor law): the member's REAL after-no-aid photo as a 2K still-insert, closer
crop, held longest.
> 2K still from the real photo: soft daylight, closer crop, same angle. [THE AFTER STATE,
> no aid at all — the strongest honest frame]. Held a beat longer. VO: "[and after,
> WITHOUT it]."
COMPLIANCE: the shown result must be the member's true result; results language follows
the health/typicality gates (FTC).

### How Ad D fills — corrected procurement (conservation rule applied)

The source is 4 shots; the fill keeps all 4 — nothing deleted. Three are real-photo
still-inserts by law; the fourth generates only when no real application photo exists.
(The old packing — D01+D02 and D03+D04 as two sub-shot-pair generations — is retired: it
rendered the proof rungs, which the macro ban and the proof-anchor law forbid, and it
spanned the soft pose rhyme across two generations — the exact drift the ONE-GEN RHYME
LAW exists to kill.)

| lane | id | covers | spec | size |
|---|---|---|---|---|
| still (preferred) | SD0 | D01 | real application photo → 2K, motion-only | ~3.3s |
| gen (fallback only) | G1 | D01 | selfie distance, treated area never legible; stands alone at the 4s floor; as the ad's only gen it is the identity checkpoint (clean bare face in frame) | 4s |
| still | SD1 | D02 | REAL before-with photo, 2K, motion-only, the ladder's reference face angle | ~2.8s |
| still | SD2 | D03 | REAL after-with photo, same face angle | ~2.2s |
| still | SD3 | D04 | REAL after-without photo, closer crop, HELD | ~2.2s+ |

The zero-generation fill (all four rungs from real photos) is legal, the cheapest ad in
the entire studio, and the strongest — every frame the viewer inspects is real. Cut points
per the rhythm card (3.27 / 6.10 / 8.27); the VO spine line changes exactly ON each cut;
each cut reads as a time jump via the calendar downgrade (generated clips: light +
location + hair; real photos: their own days).

---

## Cross-ad laws for the BEFORE & AFTER format (what a fill must keep)

1. **The before IS the hook.** Frame one shows the flaw (A) or the origin moment (D) —
   never a greeting, never settling in. Hook families banked: disbelief-retrospective and
   timestamp-origin (both confession-family, verified strong).
2. **The comparison needs a RHYME — and the rhyme never spans two generations.** Same pose
   + framing before and after (A), or same face angle across the ladder (D). The viewer's
   brain does the diff; split screens and labels are unnecessary. THE ONE-GEN RHYME LAW:
   hard-pose rhymes render as [t1]/[t2] sub-shots of ONE generation, sliced apart and
   placed at the timeline's head and tail; soft rhymes ride real-photo stills, which
   cannot drift.
3. **Proof escalates, the strongest frame lands LAST — and every proof anchor is a REAL
   photo** (after → after-WITHOUT; reveal → spread → wiggle). Never open with the best
   after, and never generate the frame the viewer inspects: this bank's proof zones
   (fingernails, lash line) are banned macro territory, so 2K still-inserts from the real
   before/after photos are the anchors in every fill.
4. **Time must be visible — at the downgraded reading.** Elapsed time is shown, not told.
   On generated clips it reads through lighting + location + hairstyle changes per clip;
   an outfit change requires its own body reference (a second outfit REQUIRES a second
   body ref — no ref, no outfit change). Real photos carry their own honest days. A
   compresses time with "just this morning" honesty instead.
5. **Process beats are ~1s micro-cuts, assembled in the edit.** Each cut a different
   variant/piece — but in this bank's banned zones they are real-photo still flashes and
   punch-in overlays over the continuous VO, never rendered macro. ONE micro-action is
   word-locked to its named VO word — as an edit-side cut on the whisper timeline, never
   a render promise.
6. **This format sprints: 10–20s total.** Narrated fills write at ~4.0–4.3 wps (measured);
   silent-source fills convert the caption spine to VO by default and ship `captions.txt`
   as a sidecar. Never burn captions.
7. **The close is delight or the naked proof, HELD.** A satisfaction line (A) or the
   strongest after frame (D), held ≈2x the median per the rhythm card, ending on the
   creator with a 0.6–0.8s reaction tail. No hard offer ask inside the ad; the offer rides
   the ad copy.
8. **Results compliance.** Any depicted transformation must be honestly renderable and
   sanctioned for the member's product; the shown result is the member's true result
   (FTC typicality), and health-adjacent categories keep structure-function language per
   the shared gates.

## Intake — what a BEFORE & AFTER order collects (enforced at Step 1)

- **REAL before photo(s) AND real after photo(s) — MANDATORY.** They are the proof anchors
  (the proof-anchor law): every 2K proof still is built FROM them, and no fill ships
  without them. No real pair → no before/after ad.
- **Every shown variant/color's own photo.** The range fan and the macro run draw only
  from these; fewer photos than planned flashes → crop punch-ins make up the count or the
  run shortens honestly.
- **The signature detail's photo** when the fill scripts a word-locked detail beat (the
  pearl on the tip, the final swipe, the clasp).
- **Product photo + real dimensions** (stated inline in any prompt that shows the product).
- **Face + body references** for the creator.
- **ONE body reference per distinct outfit shown.** A second outfit REQUIRES a second body
  ref — no ref, no outfit change: the fill downgrades to lighting + location + hairstyle
  changes per clip (the calendar downgrade).
- **Voice clip ≤15s** for narrated fills (each generation gets its own uniquely
  fingerprinted cut per `voice-and-parallel.md`); a purely silent/music-carried fill skips
  it and ships `captions.txt`.
- **Sanctioned claims + a true, FTC-safe result story** (typicality gates).

No photo for a beat → that beat becomes a still-insert from what exists, or is cut. Never
invented.

## Edit-grammar hooks (mechanics live in `render-laws.md`)

- The macro run assembles as ~1s still-insert flashes / punch-in overlays over the
  continuous VO — the host clip's audio (and hidden lips) never stop; zero audio surgery.
- The crop punch-in (medium → ECU → medium from one generation) is a legal free shot —
  the winner's couch hook block is exactly that — and it also stretches a short still
  supply into extra flashes.
- Word-action locks are edit-side cuts at word onsets on the whisper timeline; boundary-
  aligned cuts are reserved for the world change.
- The head/tail placement of the rhyme gen's sub-shots, the overlay in/outs, and the
  spine slice lists travel in the shot-level EDL — the assembly contract in
  `pipeline-contracts.md`.

## Provenance

- Ad A: `~/Downloads/1353a5fb-caf6-436b-9e00-a16504f7ee34.mp4`, 17.47s, 360x640 (9:16), narrated, torn down 2026-07-10.
- Ad D: `~/Downloads/d5263ef5878019e164bea026dd11961a.mp4`, 10.50s, 576x1024 (9:16), music-only + caption spine, torn down 2026-07-10.
- Method: faster-whisper `small.en` word timestamps (A; D confirmed zero speech) + frame
  grids at 2–3fps, read manually; shot lengths and cut times measured 2026-07-10 (the
  rhythm card above). Source files stay with the member; this bank carries the structure,
  not the footage.
