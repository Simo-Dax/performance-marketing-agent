# Scene Bank — TESTIMONIAL (UGC Studio format 01), full teardown of two winning ads

Two member-supplied winning testimonial UGC ads, torn down word-for-word and frame-by-frame
on 2026-07-10 (faster-whisper word timestamps + 2fps contact sheets, the spy-video method run
locally). This is the seed bank for the TESTIMONIAL format in the UGC Studio skill. Same
rules as the studio's other scene banks (the `scene-bank-*.md` files): every shell below
recreates its source scene exactly; at fill time the skill swaps the product, the mechanism,
the story specifics, the settings, and the wardrobe for the member's brand while keeping the
STRUCTURE. One shell serves at most ONE scene per ad, never copy a bank ad's full sequence
verbatim, and record `source_shell` (T01…, L01…, or "synthesized") in every storyboard.
Render constraints and edit mechanics live in this skill's `render-laws.md`; the verdict
lines below apply them shell by shell.

THE DURATION LAW applies to every fill: one generation is an integer 4–9 seconds, always —
15-second single generations produce extremely bad output (member-confirmed). Short beats
merge into a neighbor per the merge law; the word-accurate cutter restores the snap.

THE CAPTION LAW: source ad A burns phrase-synced captions (including a styled hook card).
Those are editor-side design layers — our renders ALWAYS ship clean, no on-screen text, no
captions; the member adds captions in their editor if they want them.

THE CLAIMS LAW: the sources' brand names, ingredient claims, retailer names, and offers
("coconut castaway", "arrowroot powder", "Sephora.com", "six pack for a huge discount",
"compliments are guaranteed") belong to their brands and are legal-risk slots — every fill
swaps them for the member's own sanctioned claims per `_shared/creative-constraints.md`.

THE VERDICT KEY (render audit folded in 2026-07-10): every shell carries an inline verdict.
**GREEN** = renders as specced. **YELLOW** = renders with the named adaptation. **RED** =
replaced by a still-insert or real-footage route (the still-insert lane in `render-laws.md`).
Label-legibility beats and macro product beats are the usual REDs — never rendered as video,
always built as member-approved 2K stills from the real photos and cut in as punch-in
overlays.

## What these two ads prove (measured)

| | Ad A "car deodorant" | Ad B "fragrance layering" |
|---|---|---|
| Length | 30.1s | 38.4s |
| Words / pace | 118 / **3.93 wps** | 138 / **3.59 wps** |
| Hook length | 12 words in 2.3s | 11 words in 2.3s |
| Settings | TWO (car home base + bedroom insert ×2) | ONE (bedroom, take-jump cuts) |
| Camera | handheld selfie, passenger seat | propped/held selfie, standing, chest-to-waist reframes |
| Captions | burned, phrase-synced (source-only) | none |
| Product on screen | ~90% of runtime, label to lens | ~95%, two-bottle choreography |
| Close | OFFER close (bundle + discount) | AVAILABILITY + social proof + trust close |

Both hooks land inside 2.5 seconds. Both pace FASTER than the 3.5 house constant — this bank's
measured default is **3.6–3.9 wps** for the testimonial format.

---

## AD A — "If I smell this at the bar" (deodorant, car testimonial with inserts)

Creator: young woman, long blonde hair, black tank top, silver jewelry. Home base: parked-car
passenger seat, handheld selfie, daylight through windows, headrest and seatbelt visible.
Insert set: bright white-wall bedroom (framed art, white pants visible), used twice for
product macros. Sunglasses ON for the hook only — taking them off IS the first take change.

### The voiceover (verbatim, whisper-timed)

"If I smell this at the bar, he is getting my number. One of the best things about using
this deodorant is that it smells extremely attractive. Like when a guy passes by, you can
smell it. My coworker wears this one, coconut castaway, and I'm not gonna lie, he gets my
attention even when he's wearing a hoodie, I can smell it. He said something about arrowroot
powder so he doesn't have to worry about sweat stains. And look how smooth the texture is.
Look, I can knock it over how they smell just with the cap off. How can you not get these
when you can get like a whole six pack for a huge discount?"

### The arc map

| # | t | Role | What's on screen | Setting |
|---|---|---|---|---|
| T01 | 0.0–2.6 | hook | Sunglasses on, product at chest, finger-point at lens; flirty confidence | car |
| T02 | 2.7–6.6 | benefit | Sunglasses off (take change), label tilted to lens, savoring half-smile | car |
| T03 | 6.9–9.0 | mini-scenario | Points off-frame ("a guy passes by"), product tracks the gesture | car |
| T04a | 9.1–11.5 | social story pt.1 | MACRO INSERT: product label fills frame, fingers turning it | bedroom |
| T04b | 11.7–15.8 | social story pt.2 | Back in car; conspiratorial lean-in, "not gonna lie" energy | car |
| T05 | 16.1–19.5 | mechanism | Open-palm emphasis gestures, product lowered; casual recall tone | car |
| T06 | 20.1–25.4 | demo | Texture puck held OVER her face to lens; open stick tilt; cap-off sniff + playful knock gesture | car |
| T07a | 25.7–27.5 | offer pt.1 | INSERT #2: puck over face, then a SECOND SCENT variant label to lens | bedroom |
| T07b | 27.5–30.1 | offer close | Back in car, product at chest, direct ask to lens | car |

~10 camera setups in 30s. The inserts are where the label gets its legibility; the car is
where the personality lives.

### The systems this ad banks

- **Home base + macro inserts.** One primary setting carries the personality; a second,
  brighter setting is inserted TWICE purely for product legibility (label macro, variant
  reveal) while the narration runs continuously over the cut. In our fills these inserts
  assemble as PUNCH-IN OVERLAYS: the insert picture (a member-approved still) lays over the
  host generation's continuing audio, and the return cut lands mid-sentence at a word onset
  per the EDL — the voice never pauses at the location change. Mechanics in `render-laws.md`.
- **The hook is a persona claim, not a product claim.** "If I smell this at the bar, he is
  getting my number" — the product is the means, the viewer's aspiration is the subject.
  Sunglasses-on adds the pattern-interrupt; taking them off marks the pivot to the pitch.
- **Second-hand social proof.** The proof witness is a named-role third party ("my
  coworker") with one hyper-specific detail ("even when he's wearing a hoodie") — cheaper
  and more believable than a self-claim.
- **The mechanism is hearsay, one line.** "He said something about arrowroot powder" —
  the ingredient enters as casual recall, not a lecture. One line, never more.
- **The demo beat is physical and lens-close.** Texture puck covering her face, the cap-off
  sniff, the knock-over gesture — believability spikes when the product touches the lens.
  Product-touches-lens macros are still-insert territory in our fills (see T06's verdict).
- **The second-scent flash.** A different variant's label appears for ~1s inside the offer
  beat — it plants "there's a range" right before the bundle ask. Every shown variant needs
  its own real photo (see the intake list).
- **The offer close.** A rhetorical question + the bundle + the discount, spoken to the
  lens, no end card. The ad ends on her face, not a graphic.

### Scene shells (fill = swap the slots, keep the structure)

House prompt shape applies (less-is-more): "A realistic, authentic UGC ad." + "Keep the
character consistent with the reference images." + ONE setting line + ONE delivery emotion +
the EXACT quote + product size inline when on screen + "No on-screen text or captions."

**Shell T01 — THE PERSONA-CLAIM HOOK (car, prop pattern-interrupt).**
VERDICT: GREEN — one clear action, product at chest (no macro); the sunglasses come off
ACROSS the hard cut into T02, never on camera (mid-shot state changes morph), and the clean
bare face lives in T02's sub-shot, satisfying the identity checkpoint.
Mechanic: an aspiration/identity claim spoken with total confidence, one styling prop
(sunglasses) as the visual interrupt, product already in hand.
> Parked-car passenger seat, handheld selfie, daylight. She wears sunglasses, holds [PRODUCT
> (size)] at chest height and points a finger at the lens. Delivery: flirty, certain.
> She says: "[PERSONA-CLAIM HOOK LINE, 8–13 words]."
Fill slots: the claim (from the member's VOC desire language), the prop, the product.

**Shell T02 — THE BENEFIT PIVOT (glasses-off take change).**
VERDICT: GREEN — single action at conversational distance; label fidelity rides the attached
real product photo, and label LEGIBILITY is not this shot's job (that is the T04a
still-insert's).
Mechanic: the first "real talk" beat; removing the prop signals sincerity; label to lens.
> Same car seat, sunglasses now off, she tilts [PRODUCT (size)] so the label faces the
> lens. Delivery: savoring, half-smile. She says: "[SINGLE BIGGEST BENEFIT LINE]."

**Shell T03 — THE MINI-SCENARIO.** One imagined everyday moment, gestured off-frame.
VERDICT: GREEN — one clear gesture at home base, no product macro, no witness in frame.
> Same car seat, she points off-frame mid-thought, product tracking the gesture. Delivery:
> gossipy. She says: "[ONE-SENTENCE SCENARIO the viewer recognizes]."

**Shell T04 — THE SECOND-HAND PROOF STORY (still overlay + return).** ONE generation + ONE
still-insert at fill time: (b) a continuous home-base take carries the WHOLE line's audio;
(a) is a 2K label still that overlays the take's opening words.
VERDICT: RED (a) / GREEN (b) — (a) is a fine-print label macro with fingers in frame (macro
bans: fine print, near-macro fingers): it never renders as video and becomes still-insert S1
built from the member's real product photo. (b) renders as specced.
> (a) STILL-INSERT S1: bright [SECOND SETTING], the [PRODUCT (size)] label filling the
> frame — generated as a 2K still from the member's real product photo, member-approved,
> then cut in (optionally animated with a motion-only prompt).
> (b) One continuous car-seat take, conspiratorial lean toward the lens. Delivery:
> not-gonna-lie. She says: "[WITNESS + PRODUCT NAME line]. [THE WITNESS PAYOFF with one
> hyper-specific detail]."
EDIT-GRAMMAR HOOK: S1 assembles as a PUNCH-IN OVERLAY — the still lays over the host take's
continuing audio (lips hidden) for the witness-name words, and the return cut lands
mid-sentence at a word onset per the EDL (the winner's return at 11.6s lands between
"castaway," and "and"). Mechanics in `render-laws.md`.
Fill slots: the witness role (coworker / roommate / husband), the specific detail, the
second setting.

**Shell T05 — THE HEARSAY MECHANISM.** One line, casual recall, open-hand gestures.
VERDICT: YELLOW — the source's gesture-on-the-key-word is a word-action lock, a render
promise: direct the offhand FEELING instead, and place any word sync in the edit on the
whisper timeline.
> Same car seat, product lowered, loose open-palm gestures. Delivery: offhand.
> She says: "[He/They said something about [MECHANISM] so [PLAIN-ENGLISH PAYOFF]]."
COMPLIANCE: the mechanism must be the member's sanctioned claim.

**Shell T06 — THE LENS DEMO.** The product physically performs at the lens.
VERDICT: YELLOW — the puck-over-face beat is a product-touches-lens texture macro: RED,
displaced to still-insert S2 (built from the member's real texture/demo-state photo) and
punched in as an overlay. The remaining demo renders as ONE continuous take that starts with
the cap ALREADY off (product manipulation ladder: open/close needs its own real-photo state;
mid-shot state changes morph).
> Same car seat, cap already off. She holds [PRODUCT PART] up toward the lens, tilts it,
> then a playful sniff and knock gesture — one continuous demo flow. Delivery: look-at-this.
> She says: "[DEMO NARRATION, imperative 'look' phrasing]."
EDIT-GRAMMAR HOOK: S2 flashes as a punch-in overlay over the take's continuing audio; the
return lands at a word onset per the EDL.

**Shell T07 — THE OFFER CLOSE (variant flash + return).** ONE generation + ONE still-insert:
a ~1s second-variant still flash inside the offer beat, hard cut home for the spoken ask.
VERDICT: RED (a) / GREEN (b) — (a) is a second-variant label-legibility flash: still-insert
S3 from that variant's OWN real photo (one-product-reference rule: variant 2 never shares a
generation with variant 1, and no variant renders without its own photo). (b) is the typed
`cta` close and renders as specced — the ad ends on her face, never an end card.
> (a) STILL-INSERT S3: bright [SECOND SETTING], [SECOND VARIANT (size)] label to lens — a 2K
> still from that variant's real photo, member-approved.
> (b) One continuous car-seat take, product at chest, direct to lens. Delivery:
> obviously-do-this. She says: "[RHETORICAL QUESTION + BUNDLE/OFFER ask]." — the member's
> real offer only.
EDIT-GRAMMAR HOOK: S3 rides as a ~1s punch-in overlay over the continuing offer audio; the
winner's return cut lands INSIDE the word "get" — a literal mid-word return, per the EDL.

### How Ad A banks into 4–9s generations (worked render plan, corrected to the sub-shot ceiling)

THE CONSERVATION RULE governs this table: the 2–3 hard-cut sub-shots-per-generation ceiling
displaces setups out of over-packed generations, and displaced setups are recovered as extra
generations or still flashes — NEVER silently deleted. The fill's timeline stays at the
winner's measured count: **10 shots**.

| gen / still | shells | sub-shots (≤3) | words | speech | size |
|---|---|---|---|---|---|
| gen 1 | T01+T02 (hook always merges) | 2 — glasses on → hard cut → glasses off | 27 | ~6.6s | 7s |
| gen 2 | T03 + T04 host take | 2 — scenario point / continuous story take (hosts the S1 overlay) | 37 | ~8.6s | 9s |
| gen 3 | T05 | 1 | 15 | ~3.4s | 4s |
| gen 4 | T06 | 1 — continuous demo take (hosts the S2 overlay) | 22 | ~5.3s | 5s |
| gen 5 | T07 host take | 1 — continuous offer take (hosts the S3 overlay) | 20 | ~4.4s | 5s |
| still S1 | T04a label macro | punch-in overlay (2.4s in the winner) | — | — | 2K still |
| still S2 | T06 puck-over-face | punch-in overlay | — | — | 2K still |
| still S3 | T07a second-variant flash | punch-in overlay (~1s) | — | — | 2K still |

Shot ledger — the EDL's 10 timeline shots, conserved at the winner's count:
T01 · T02 · T03 · S1 flash · T04 return · T05 · S2 flash · T06 demo · S3 flash · T07 close.
The displaced macro setups (T04a, the puck beat, T07a) all survive as still flashes; nothing
was deleted to satisfy the ceiling. (Exact merges follow the segmenter + merge law at run
time; this table shows the law-legal shape.)

---

## AD B — "My latest combo" (fragrance layering, single-set testimonial)

Creator: woman, brunette bob, white bralette set, rings. ONE setting the whole ad: warm
bedroom, full-length black-frame mirror and orange balloons behind, standing chest-to-waist
selfie framing. NO captions, no end card. Variety comes from take-jump cuts (~12+ takes),
subtle reframes (closer ↔ wider), and TWO-BOTTLE choreography: one bottle up, cap off, both
bottles paired, labels to lens, spray-wrist gesture, savoring eyes-closed face.

### The voiceover (verbatim, whisper-timed)

"I have to tell you about my latest combo that smells insane. Layer the Mochi Milk
Fragrance, Marshmello-y, Vanilla goodness, genuinely can't understand how good this smells.
Also, my husband's favorite perfume that I wear layered with extra milk is an unbeatable
combo. Extra Milk Fragrance has an amber bergamot scent. It's just literally chic and
playful and a scent. I love layering fragrances. I feel like it's one of the chicest things
you can do and it really solidifies a signature scent. Compliments are guaranteed. I just
got back from Pilates and a girl literally stopped me and asked me what I was wearing after
a 45 minute class. They're available at Sephora.com and in stores, dozens of messages away
from you guys saying it's now your new favorite. So trust me on this one."

### The arc map

| # | t | Role | What's on screen |
|---|---|---|---|
| L01 | 0.0–2.3 | hook | Big smile, first bottle raised mid-gesture, insider-secret energy |
| L02 | 3.6–9.7 | product 1 reveal | Cap off, bottle to lens, then BOTH bottles up; eyes close savoring on "how good this smells" |
| L03 | 10.1–14.4 | product 2 + pair | Second bottle forward, the two held together as THE COMBO |
| L04 | 15.1–17.2 | scent notes | Single bottle label to lens, closer framing |
| L05 | 17.9–25.3 | identity beat | Freer gestures, bottles lowered and raised, slight wider reframe; "chicest thing / signature scent" |
| L06 | 26.1–31.5 | proof story | Animated storytelling, bottles as props; the Pilates girl story |
| L07 | 32.1–36.9 | availability + social CTA | Both bottles held up as the pair, labels forward |
| L08 | 37.5–38.4 | trust close | Direct eye contact, pair held still: "So trust me on this one." |

### The systems this ad banks

- **Single-set take-jump grammar.** One location, many takes. The jump cuts are native to
  the format BECAUSE something changes at every cut: which bottle is up, cap on/off, framing
  closer/wider, gesture energy. That visible-state-change requirement is the take-jump law
  (`render-laws.md`) — the banned cut is the one where NOTHING visibly changes. This ad's
  joins all sit in trimmed breath pauses at sentence boundaries (see the rhythm card: the
  bank's documented exception to mid-word cutting). Product choreography is the scene ladder
  when there is only one scene.
- **The insider-secret hook.** "I have to tell you about…" — a confession-family opener
  that frames the ad as a tip between friends, not a pitch. Product already in hand.
- **Two-product COMBO staging.** The offer is a ritual (layering), so both bottles appear
  together at every proof beat — the pair IS the product: a multi-product offer stages all
  its products together, labels legible. At render time the pair is ONE member-approved 2K
  PAIR STILL composed from both real bottle photos, attached as the generation's single
  product reference (the one-product-reference rule).
- **Sensory acting carries the claim.** Eyes closed, head tilt, "mmh" face exactly on the
  scent words — the believability beat is performed, not stated. (In our fills the feeling
  is directed and the word sync is placed in the edit — see L02's verdict.)
- **The identity beat.** Mid-ad, the pitch widens from the product to who it makes you
  ("one of the chicest things you can do", "signature scent") — identity language pulled
  straight from the desire layer.
- **The hyper-specific proof story.** Place + time + stranger: "just got back from Pilates…
  a girl literally stopped me… after a 45 minute class." The specificity does the proving.
  This is the VOC goldmine slot.
- **Availability close + borrowed crowd.** Where to buy (retailer + in stores) then a
  social-mass line ("dozens of messages… your new favorite") and a 6-word trust close held
  on eye contact. No offer math — this close sells certainty, not price.

### Scene shells

**Shell L01 — THE INSIDER-SECRET HOOK.**
VERDICT: GREEN — one clear action, product in hand, clean bare face: this generation is the
format's natural identity checkpoint.
> Warm bedroom, standing selfie, mirror behind. She raises [PRODUCT 1 (size)] mid-gesture,
> grinning like she's about to share a secret. Delivery: can't-hold-it-in. She says:
> "[I have to tell you about… HOOK LINE, 8–13 words]."

**Shell L02 — THE FIRST REVEAL + SENSORY BEAT.**
VERDICT: YELLOW — two adaptations: the cap is ALREADY off at shot start (mid-shot state
changes morph; the open/close rung of the manipulation ladder needs its own real cap-off
photo), and the eyes-closed savoring is directed as a FEELING, never locked to named words —
word sync is an edit-side guarantee on the whisper timeline.
> Same room, cap already off. She holds [PRODUCT 1 (size)] to the lens, then closes her
> eyes and tilts her head back, genuinely savoring. Delivery: genuinely savoring.
> She says: "[PRODUCT 1 NAME + 2–3 sensory descriptors + can't-believe line]."

**Shell L03 — THE PAIR / COMBO REVEAL.** (Multi-product offers only.)
VERDICT: YELLOW — two products in one frame is legal only with the member-approved 2K PAIR
STILL (composed from BOTH real bottle photos) attached as the generation's single product
reference; any label-LEGIBLE pair beat routes to the still-insert lane instead.
> Same room. She brings [PRODUCT 2 (size)] into frame and holds BOTH together toward the
> lens as one unit. Delivery: unbeatable-combo certainty. She says: "[PRODUCT 2 intro +
> the combo claim]."

**Shell L04 — THE NOTES CLOSE-UP.** One line of concrete specifics, label legible.
VERDICT: RED — a label-legibility notes close-up is fine print at macro distance: it never
renders as video. It becomes still-insert S1, a 2K still from the real bottle photo,
member-approved; the spoken notes line rides the neighboring take's continuous audio.
> STILL-INSERT S1: [PRODUCT (size)] label filling the frame, tighter than the takes around
> it — generated from the member's real bottle photo. The host take continues underneath;
> she says (as continuing audio): "[NAMED CONCRETE DETAILS — notes / ingredients / spec]."
EDIT-GRAMMAR HOOK: S1 assembles as a punch-in overlay spanning the whole notes sentence —
this single-set format enters and returns at breath-pause sentence boundaries (the rhythm
card's exception), not mid-word. Mechanics in `render-laws.md`.

**Shell L05 — THE IDENTITY BEAT.** The camera widens slightly; the pitch becomes about her.
VERDICT: GREEN — talking beat, freer gestures, no product macro; it runs past 4s of speech,
so the plan schedules a take-jump inside it (the max-solo-shot rule) with the wider reframe
as the jump's visible state change.
> Same room, slightly wider framing, bottles lowered, freer gestures. Delivery: this-is-me.
> She says: "[IDENTITY LINES — what the ritual says about the person, desire language from
> VOC]."

**Shell L06 — THE STRANGER-PROOF STORY.**
VERDICT: GREEN — animated storytelling take, product as a hand prop; interior dead-air trims
manufacture its take-jumps for free, each jump covered by a visible gesture/energy change.
> Same room, animated storytelling energy, product as a prop in the gesturing hand.
> Delivery: you-won't-believe-this. She says: "[PROOF STORY with place + timeframe +
> stranger reaction, hyper-specific]." — sourced or member-supplied stories only.

**Shell L07+L08 — THE AVAILABILITY + TRUST CLOSE.** (L08 is 0.9s — it ALWAYS merges into
L07's generation; the cutter's CTA tail lets it breathe.)
VERDICT: YELLOW — the pair-up renders with the approved 2K pair still as the generation's
single product reference (label legibility already earned by the approved still, not the
render); the trust close itself renders as specced: this is the typed close, HELD, ending on
her face in direct eye contact — never a still, never an end card.
> Same room. She holds [THE PRODUCT / THE PAIR] up, labels to lens, then lands the last
> line on still, direct eye contact. Delivery: certain, warm. She says: "[WHERE TO GET IT +
> social-mass line]. [6-word trust close]."
EDIT-GRAMMAR HOOK: the L07→L08 join is a take jump in a trimmed breath pause; the visible
state change is the pair going from presented-forward to held-still on eye contact.

### How Ad B banks into 4–9s generations (worked render plan, corrected to the sub-shot ceiling)

THE CONSERVATION RULE governs this table: the winner runs ~12 takes, and the fill's take
count stays there. The L04 notes setup displaced by the RED verdict is recovered as still S1
plus one extra generation (L05 splits across two gens to carry the notes line's audio) —
never silently deleted.

| gen / still | shells | sub-shots (≤3) | speech | size |
|---|---|---|---|---|
| gen 1 | L01+L02a (hook always merges) | 2 — raise-bottle grin / cap-already-off to lens | ~6.0s | 6s |
| gen 2 | L02b+L03 | 2 — savoring beat / pair-up | ~8.0s | 8s |
| gen 3 | L04 host + L05a | 2 — host take under the S1 overlay / identity opener, wider | ~5.5s | 6s |
| gen 4 | L05b | 1 — identity payoff; the wider reframe is the join's visible state change | ~4.0s | 4s |
| gen 5 | L06 | 1 take + interior dead-air trims (free take-jumps) | ~5.5s | 6s |
| gen 6 | L07+L08 (L08 always merges) | 2 — pair-up availability / held trust close | ~5.7s | 6s |
| still S1 | L04 notes/label | sentence-spanning punch-in overlay | — | 2K still |

Take ledger — ~12 timeline takes, conserved at the winner's count:
L01 · L02a · L02b · L03 · S1 notes flash · L05a · L05b · L06a · L06b · L06c · L07 · L08.
Every join sits in a trimmed breath pause at a sentence boundary (this format's rhythm
exception), and every jump changes a visible state — which bottle is up, cap on/off, one vs
the pair, closer↔wider reframe. (Exact merges follow the segmenter + merge law at run time;
this table shows the law-legal shape.)

---

## RHYTHM CARD — TESTIMONIAL (measured 2026-07-10; the stitcher's QC reads from here)

**Ad A — car deodorant, 30.1s.** 10 distinct shots; median shot 2.6s; shortest 0.8s; longest
5.3s. Insert flashes: 2.4s label macro, ~1.0s second-variant flash, 0.8s. Mid-sentence cuts:
YES on insert-return cuts — the return at 11.6s lands between "castaway," and "and"
mid-sentence, and the return at 27.5s lands INSIDE the word "get" (a literal mid-word cut);
same-setting take joins sit in 0.24–0.46s breath gaps at sentence boundaries. Audio: ONE
continuous voice performance — lip-sync at the car home base, the same voice continuing as
VO over the bedroom macro inserts. ~7 same-seat take jumps, each masked by a visible state
change (the sunglasses coming off IS the hook pivot). Spine-and-return: car → bedroom insert
→ car, twice; the ad ends on her face in the car, no end card. Hero product on screen ~90%
of runtime.

**Ad B — fragrance layering, 38.4s.** ~12+ takes; take-level median ~3.2s; longest single
take under 7.4s; shortest beat 0.9s (the trust close). ALL cuts at sentence boundaries in
breath pauses trimmed to 0.16–0.38s — this single-set take-jump variant gets its density
from take count, NOT mid-word cuts (the bank's documented exception to mid-word cutting).
Every jump covered by a visible state change (which bottle is up, cap on/off, one vs the
pair, closer↔wider reframe). Choreographic callback: the two-bottle COMBO pair staged at L03
returns at L07 and holds through the 0.9s close. Product on screen ~95%; ends on her face,
direct eye contact.

**Format pace:** 3.6–3.9 wps measured.

**QC targets the stitcher reads from this card:** median shot ≤3.2s; no shot >4s except the
typed close; breath-pause joins 0.15–0.45s.

---

## Cross-ad laws for the TESTIMONIAL format (what a fill must keep)

1. **Hook inside 2.5s, 8–13 words, product already in hand.** Both winners open with the
   creator mid-energy, never settling in. Persona-claim (A) and insider-secret (B) are the
   two banked hook families — both sit in the verified strong families (offer/confession).
2. **The product lives at the lens.** In frame for ~90% of the runtime, label forward at
   least twice, and it TOUCHES the lens once (macro, puck-over-face, cap-off, pair-up) —
   in our fills every lens-touching macro beat routes through the still-insert lane and
   assembles as a punch-in overlay (`render-laws.md`).
3. **One believability spike mid-ad**: a physical demo (A) or performed sensory beat (B).
4. **One hyper-specific proof story** with a named witness role or place+time. This is the
   VOC slot — fill it with the customer's real language, never invented numbers.
5. **The mechanism is one casual line**, hearsay-toned, sanctioned claims only.
6. **Two legal set strategies**: home base + brighter macro inserts (A), or single set +
   take-jump choreography (B). In BOTH, something visible changes at every cut — the
   take-jump law's visible-state-change requirement, this format's expression of the
   re-hook-every-cut law. Set strategy A cuts mid-sentence on insert returns; set strategy
   B cuts only in trimmed breath pauses (the rhythm card's exception).
7. **Two legal closes**: the OFFER close (bundle/discount ask, rhetorical question) or the
   AVAILABILITY + social-mass + trust close. Both are the format's typed `cta` close, both
   end HELD on the creator's face. No end cards.
8. **Pace 3.6–3.9 wps** (measured) — write testimonial scripts a notch faster than the 3.5
   house default; the segmenter takes `--wps 3.7` for this format unless the brand's own
   teardowns say otherwise.
9. **First person throughout.** Contractions, spoken tics, gossip register — then run the
   natural-voice banlist; the sources' filler ("literally", "not gonna lie") is authentic
   at ONE use, slop at three.
10. **Ships clean.** No captions, no on-screen text, no end card — the sources' caption
    layers are editor-side; ours never render text.

Batch orders: a testimonial script may fan into up to 4 genuinely distinct timelines — the
studio's own batch feature, specified in `variant-fanout.md`.

## TESTIMONIAL INTAKE — what the member must supply for this format

Collected at Step 1 before any script is written; enforced per ordered testimonial:

- **Face + body references** for the creator — and ONE body reference per DISTINCT outfit
  shown (a second outfit needs a second body ref, or the fill keeps one outfit).
- **Product photo(s)** — a separate REAL photo for EVERY variant that appears on screen:
  the ~1s second-variant flash (T07a) needs its own photo, and a two-product combo (L03)
  needs BOTH bottles' photos (the approved 2K pair still is composed from them).
- **Manipulation-state photos** for any demo beat above "hold" on the manipulation ladder:
  cap-off state, open/texture state (T06's demo and L02's cap-already-off start depend on
  them; without them those beats downgrade to still-inserts or simpler holds).
- **Product dimensions** — real sizes are stated inline in every prompt that shows product.
- **Voice clip ≤15s** — this is a narrated format, so the clip is required.
- **The TRUE proof story and sanctioned claims** — the witness story (T04), the stranger
  story (L06), and the mechanism line (T05) are member-supplied and legally sanctioned,
  never invented.
- **The real offer** (for the OFFER close) or real availability/retailer (for the
  AVAILABILITY + trust close).

No photo → that beat becomes a still-insert from what exists, or is cut. Never invented.

## Provenance

- Ad A: `~/Downloads/1897f33f-3d04-4043-b114-506f6955a6d2.mp4`, 30.06s, 360x640 (9:16), torn down 2026-07-10.
- Ad B: `~/Downloads/f08f3fab-0f21-4a20-909b-f86f56a403ce.mp4`, 38.40s, 360x640 (9:16), torn down 2026-07-10.
- Method: faster-whisper `small.en` word timestamps + 2fps frame grids, read manually. The
  source files stay with the member; this bank carries the structure, not the footage.
