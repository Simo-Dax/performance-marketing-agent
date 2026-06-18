# Hook Library

PINNED: Hooks are uniformly SHORT (about 3 to 5 seconds, ~8 to 13 words each), rendered fast at ~3.5 words/sec. There is NO hook-length ladder (no 4 / 6 / 8 / 10). Hook length is not a distinctness lever — distinctness comes from 4 UNIQUE hooks plus the b-roll-count ladder. See `references/andromeda-variation.md` and `references/generation-architecture.md`. Every generation stays under 10 seconds.

This file holds the raw hook material the factory pulls from in Steps 1 and 3. It has two halves, then a pairing note. Hooks are NOT scraped from TikTok or any external source — mine them here plus the member's VOC.

- HALF A is the VERBAL hook: the first spoken line. Short, punchy, first-person UGC. The mouth says it.
- HALF B is the VISUAL hook: something dramatic that happens on screen in the first 1 to 2 seconds. Not a talking head. The eye sees it.
- The PAIRING NOTE combines one verbal + one visual into a single hook, and enforces the hard rule: every hook carries a visual action, never just a spoken line.

How the rest of the skill uses this file:

- Step 1 (Hook Mining) populates a Hook Bank of verbal lines from HALF A + the member's VOC. No scraping.
- Step 2 (Scripts First) writes the body beat sheet (ending on the CTA) using ONE framework from `references/scripting-frameworks.md`, plus the 2 product-only b-roll voiceover lines.
- Step 3 (Andromeda Variation) builds 4 ads with 4 UNIQUE hooks (one per ad), each a different HALF A angle + a different KIND of HALF B visual action. Hooks are uniformly short (~3 to 5s); there is NO hook-length ladder. Distinctness comes from the unique hooks + the b-roll-count ladder (0/1/2/2), and every ad ends on the CTA.
- Step 5 (Generation) renders the 4 hooks as 2 REELS (about 2 hooks per generation, under 10s), described as scenes with a hard cut, then SPLITS each reel at its cut into individual hook clips. The visual prompt fragment in HALF B goes into the talking render prompt for that hook scene.
- assembly-manifest.json carries `verbal_hook`, `visual_hook`, `hook_clip`, plus the `distinctness_fingerprint` (a hash of visual_hook + sorted broll_set + b-roll count + placement indices + ordered roles). The free-text verbal hook is not in the hash.

Cross references:
- Frameworks (the 12): `references/scripting-frameworks.md`
- Seedance 2.0 hard limits and the per-render duration rules: `references/seedance-2.0-limits.md`
- The 4-axis variation logic and distinctness scoring: `references/andromeda-variation.md`
- Character lock, the one shared voice reference clip, audio-on assembly, the manifest: `references/consistency-and-assembly.md`

Hard rules pinned here so no one forgets them:

1. NEVER send a video input on any render. A visual hook is achieved through the IMAGE prompt and camera/motion language, not by feeding a reference video. HOOK renders are TALKING renders: the verbal hook is spoken over the action, so a hook gets the locked face + body images + the product image (when the product is on screen) + the uploaded voice clip as the voice reference, and ZERO video inputs. Identity comes from the re-sent face + body bytes.
2. B-ROLLS ARE PRODUCT-ONLY. A b-roll is NOT a character render — it shows only the product (held by an anonymous hand or standing on a surface) with a voiceover, and attaches the product image + voice clip ONLY (no face, no body). See `references/consistency-and-assembly.md`.
3. Every hook must carry a visual action. A spoken line over a static talking head is not a hook. If a hook has no dramatic first-1-to-2s action from HALF B, it is rejected in Step 3.

---

## HALF A. Verbal Hook Archetypes (the spoken opening line)

The verbal hook is the single most important line in the ad. It goes into the hook scene's spoken line. Keep hooks SHORT: about 8 to 13 words, which renders at roughly 3 to 5 seconds at the fast ~3.5 wps pace (the hook scene gets 1 to 2 extra seconds for its visual action). There is no hook-length ladder — all four hooks are short and differ by ANGLE and visual action, not length. Write it the way a real person talks, contractions and all, not the way ad copy reads.

Awareness stages referenced below use the standard 5: Unaware, Problem-Aware, Solution-Aware, Product-Aware, Most-Aware. Framework names refer to the 12 named entries in `references/scripting-frameworks.md`: CROWD (Bandwagon), DISRUPT (Industry Contrarian), CURE (Listicle), FOUNDER, SIMPLE (X Without Y), PURE (Organic), PAS, UGLY, PROVE (Founder Objections), SHOW (Us vs Them), Triple G, TEASE (Curiosity Loop). PURE and UGLY are style modifiers that can ride on top of any of the others. Use the chosen framework's own beats for length; the hook is just the first beat.

### A1. POV / Callout
- Pattern: name the exact person watching, or frame the shot as their point of view, so they feel seen in the first second. Often literally starts with "POV:" or "If you're someone who...". Calls out a tribe, a habit, or a situation.
- Example lines:
  - "POV: you've tried every gut health thing and your stomach still hates you."
  - "If you sit at a desk eight hours a day, this is for your lower back."
- Awareness stage: Problem-Aware to Solution-Aware. Works on Unaware when the callout is an identity, not a problem.
- Pairs with: PAS, SIMPLE, SHOW (Us vs Them), PURE. The callout names the buyer, which sets up PAS's Problem beat or SIMPLE's State-the-escape beat cleanly.

### A2. Contrarian / Pattern-Break Opinion
- Pattern: say the opposite of the category's accepted wisdom, hard and fast, so the scroll stops to argue. Attacks a belief the viewer holds or has been sold.
- Example lines:
  - "Stop drinking more water. That is not why you're tired."
  - "Collagen powder is mostly a waste of money, and here's what actually worked."
- Awareness stage: Solution-Aware to Product-Aware (they know the category, you flip it). Can hit Problem-Aware when the belief is mainstream.
- Pairs with: DISRUPT (Industry Contrarian), CROWD (Reject-the-old-way beat), SHOW (Us vs Them), PROVE. Needs a body that backs the claim or it reads as clickbait. This is the natural opener for DISRUPT's Declassify beat.

### A3. Curiosity Loop / Open Question
- Pattern: open a loop the brain needs to close. Tease a result, a secret, or a "the reason is not what you think" without paying it off until the body. Never resolve the loop in the hook.
- Example lines:
  - "The real reason your skin breaks out at 30 has nothing to do with your face wash."
  - "I figured out why I kept waking up at 3am and it took me way too long."
- Awareness stage: Problem-Aware to Solution-Aware. Strong on Unaware because curiosity does not require a known problem.
- Pairs with: TEASE (Curiosity Loop), CURE (Listicle), DISRUPT, FOUNDER. TEASE is the home framework here, its whole structure is one open loop. Pay the loop in a later beat (TEASE's Satisfy) or you lose them.

### A4. Confession / Vulnerable Admission
- Pattern: admit something slightly embarrassing or private in a low, honest tone. The unguarded delivery reads as real, not scripted, which is the whole point of UGC.
- Example lines:
  - "Okay I was embarrassed to buy this, but I have to tell you."
  - "I didn't think I had a problem until my husband recorded me snoring."
- Awareness stage: Problem-Aware (the confession IS the problem reveal). Works Unaware when the admission surfaces a problem they share but never named.
- Pairs with: FOUNDER, PROVE (Founder Objections), PAS, PURE. The honesty earns the pitch later. A confession is the natural way into FOUNDER's Feature-the-founder beat or PROVE's Problem beat.

### A5. Number / List
- Pattern: lead with a specific number that promises structure and a finite payoff. Odd numbers and specific figures beat round ones. Sets an expectation the body must deliver fast.
- Example lines:
  - "Three things I wish I knew before I spent $400 on supplements."
  - "I tested this for 14 days, here's exactly what changed."
- Awareness stage: Solution-Aware to Product-Aware. List structure assumes they are shopping or comparing.
- Pairs with: CURE (Listicle), SHOW (Us vs Them), CROWD, Triple G. CURE is the home framework, its Curiosity beat IS a numbered hook. The number sets the body's beat count.

### A6. Challenge / Dare
- Pattern: throw down a test or a dare the viewer can mentally take, or that the creator is visibly taking on camera. Implies proof is coming, which buys attention.
- Example lines:
  - "I dare you to find a cleaner ingredient list than this. I'll wait."
  - "Try this for one week and tell me your energy doesn't change."
- Awareness stage: Product-Aware to Most-Aware (they need to be close to buying for a dare to land). Comparison dares can work Solution-Aware.
- Pairs with: SHOW (Us vs Them), PROVE, DISRUPT, Triple G. SHOW is the home framework, its Set-the-challenge beat IS a dare. Back the dare with a visible result (lean on a B14 demo visual hook).

### A7. Direct Claim / Big Promise
- Pattern: state the single biggest benefit as a flat, confident claim in the first second. No throat-clearing. The promise has to be specific enough to be believable and bold enough to stop the scroll.
- Example lines:
  - "This fixed my bloating in four days and I'm not exaggerating."
  - "This is the only planner I've actually used past January."
- Awareness stage: Product-Aware to Most-Aware. The viewer can evaluate a claim only if they know the category.
- Pairs with: SIMPLE, PURE, CROWD, Triple G. The body is the proof for the claim, so pair it with a payoff framework (SIMPLE's Prove beat, CROWD's Wave-the-proof beat). A B14 demo or B3 before/after visual hook makes the claim land instantly.

### A8. Genuine Reaction
- Pattern: open mid-reaction, as if the camera caught a true response. Surprise, delight, disbelief. The unpolished, in-the-moment delivery is the credibility. Often a half-sentence.
- Example lines:
  - "Wait, no way. Look at this."
  - "I genuinely did not expect that to work."
- Awareness stage: Solution-Aware to Product-Aware. The reaction implies a product moment, so they need category context.
- Pairs with: PURE (Organic), SHOW, TEASE, CURE. PURE is the home framework, its raw-discovery energy is built for caught-on-camera reactions. Pairs naturally with a visual hook that earns the reaction (B2 pour, B7 transform, B14 demo).

### A9. Problem Rant / Frustration
- Pattern: vent a specific, relatable frustration with energy, fast and a little fed up. The shared annoyance bonds the viewer before any product appears.
- Example lines:
  - "I am so tired of every protein bar tasting like wet cardboard."
  - "Why is it impossible to find jeans that fit my waist and my thighs."
- Awareness stage: Problem-Aware. Can reach Unaware when the rant names a frustration they feel but tolerate.
- Pairs with: PAS, PURE (Organic), SIMPLE, DISRUPT. The rant IS the problem beat, so the body jumps straight to PAS's Agitate or SIMPLE's Identify-pain. PURE makes the rant feel unfiltered and real.

### A10. Unboxing / First-Impression
- Pattern: narrate the moment of opening or trying for the first time, in real time. Implies a reveal is seconds away, which is its own open loop. Casual, present-tense.
- Example lines:
  - "Okay this just got here, let's see if it's worth the hype."
  - "First time trying this, I'll tell you exactly what I think."
- Awareness stage: Product-Aware to Most-Aware (they know the product exists and want a verdict). Solution-Aware if framed as "trying the thing everyone recommends."
- Pairs with: PURE (Organic), CROWD (Bandwagon), TEASE, SHOW. PURE's genuine-discovery arc fits an unboxing best. Almost always paired with a reveal visual hook (B7 peel/crack/open, B6 object reveal).

Quick chooser:

| If the Hook Bank line is...           | Archetype | Default awareness     |
|---------------------------------------|-----------|-----------------------|
| naming the viewer or their situation  | A1 POV    | Problem-Aware         |
| flipping accepted wisdom              | A2 Contrarian | Solution-Aware    |
| teasing an unresolved reason          | A3 Curiosity | Problem-Aware      |
| admitting something private           | A4 Confession | Problem-Aware     |
| leading with a number                 | A5 Number | Solution-Aware        |
| daring the viewer to test it          | A6 Challenge | Product-Aware      |
| stating the big benefit flat          | A7 Direct Claim | Product-Aware   |
| caught mid-reaction                   | A8 Reaction | Solution-Aware      |
| venting a frustration                 | A9 Rant   | Problem-Aware         |
| opening or trying for the first time  | A10 Unboxing | Product-Aware      |

---

## HALF B. Visual Hook Archetypes (the dramatic first 1 to 2 seconds)

This is the part the factory cares about most: something physically dramatic in the opening, not a person standing still and talking. The verbal hook is spoken OVER this action. Because the verbal hook is present, the hook clip is a TALKING render, so: locked character image(s) + product image if shown + uploaded voice message as the voice reference, and NO video_urls (rule 1 above).

For each archetype below:
- What happens on screen: the literal physical action.
- Why it stops the scroll: the attention mechanism.
- Prompt fragment: a concrete chunk to drop into the Seedance image/render prompt for that hook clip. Always combine it with the verbatim character lock line from `references/consistency-and-assembly.md` ("The person in this video must exactly match the reference image, face, hair, body, clothing.") plus your wardrobe and lighting descriptors. Keep camera and motion language explicit so the model produces movement, not a frozen pose.
- Natural length: how long the action reads cleanly. Use this together with the hook line's word band to pick the canonical ladder rung (4 / 6 / 8 / 10 integer seconds) for that variant.

A note on framing for all of these: target vertical 1080x1920, 30fps, handheld UGC energy unless stated. The motion verbs (slams, pours, whips, snaps) are doing the work, keep them in the prompt.

### B1. Product slammed on a table
- What happens: a hand brings the product down onto a hard surface with a sharp stop, items around it jump slightly, then settle.
- Why it stops the scroll: the abrupt impact and micro-bounce read as a sound even on mute; the eye locks onto the sudden stop.
- Prompt fragment: "Close-up, a hand firmly sets [PRODUCT] down onto a wood table with a decisive thud, nearby objects jolt slightly from the impact, handheld camera, natural daylight, the person leans into frame and starts speaking to camera."
- Natural length: the action reads in about 1.5 to 2.5s, so it sits comfortably inside the 4s rung (the hook line plays over and after the slam).

### B2. Slow-motion liquid pour
- What happens: a liquid streams in slow motion, the product (serum, drink, oil, milk) pours into a glass, onto skin, or over a surface, light catching the stream.
- Why it stops the scroll: slow-mo on a fast feed is a pace break; glossy liquid is a known dopamine trigger.
- Prompt fragment: "Macro slow-motion, [PRODUCT/liquid] pours in a smooth glossy stream into a clear glass, light refracts through the liquid, droplets suspended, then cut to the person holding the glass and speaking to camera, natural light."
- Natural length: the action reads in about 2.5 to 4s, fits the 6s rung (the pour runs while the line is spoken).

### B3. Before / after hard cut
- What happens: a fast, jarring cut from a "before" state to an "after" state on the same subject (messy to clean, dull to glowing, cluttered to organized), no transition.
- Why it stops the scroll: the brain auto-compares the two frames; the contrast is the message.
- Prompt fragment: "Hard cut, frame one shows [BEFORE STATE] in flat dull light, instant cut to frame two showing [AFTER STATE] in brighter light from the same angle, then the person enters frame and addresses the camera." Note: render this as two short shots and butt-cut them; do not feed a reference video.
- Natural length: the cut itself reads in about 2 to 3.5s. The 6s rung.

### B4. A mess or spill
- What happens: something spills, drops, scatters, or overflows in the opening, a deliberate small disaster (powder dusts the counter, a drawer of tangled product, coffee rings everywhere).
- Why it stops the scroll: mess violates the polished-feed expectation and reads as raw and real, which is the UGC currency.
- Prompt fragment: "Handheld, [SUBSTANCE] spills and scatters across the counter in a small mess, the person reacts and gestures at it while starting to speak to camera, candid kitchen lighting, slightly imperfect framing."
- Natural length: the action reads in about 2 to 3s. The 4s or 6s rung.

### B5. Fast push-in to the face
- What happens: the camera rushes in toward the creator's face (or a quick step toward the lens) so the framing snaps from wide to close.
- Why it stops the scroll: rapid scale change triggers motion attention; suddenly a face fills the screen mid-sentence.
- Prompt fragment: "Quick punch-in, camera rapidly pushes from a medium shot to a tight close-up on the person's face as they begin speaking directly to camera with urgency, handheld, natural light." Pairs especially well with confession (A4) and contrarian (A2) lines.
- Natural length: the move reads in about 1 to 2s. The 4s rung.

### B6. Unexpected object reveal
- What happens: the creator pulls an out-of-context object into frame to make a point (a stack of empty competitor bottles, a giant prop, a surprising before-photo on their phone) before introducing the product.
- Why it stops the scroll: the object does not match the expected frame, so the brain pauses to resolve it.
- Prompt fragment: "The person pulls [UNEXPECTED OBJECT] up into frame from below, holds it toward camera with a knowing look, then sets it down and starts speaking, handheld, bright daylight."
- Natural length: the action reads in about 2.5 to 4s. The 6s rung.

### B7. Transformation / peel / crack / open
- What happens: a satisfying physical change on the product itself, peeling a seal, cracking a lid, snapping a bar, twisting a cap with a visible click, the package opening for the first time.
- Why it stops the scroll: a reveal-in-progress is an open loop the eye stays for; the tactile snap is sensory.
- Prompt fragment: "Macro close-up, fingers peel back the foil seal on [PRODUCT] / snap [PRODUCT] cleanly in half / twist the cap until it clicks open, slow deliberate motion, then the person lifts it toward camera and speaks, soft natural light." Top pairing for unboxing (A10) and reaction (A8).
- Natural length: the action reads in about 2 to 4s. The 6s rung.

### B8. Drop and catch
- What happens: the product is tossed up or dropped a short distance and caught, a single confident beat of motion.
- Why it stops the scroll: the falling object hijacks tracking attention; the catch resolves it with a beat of satisfaction.
- Prompt fragment: "The person tosses [PRODUCT] up a few inches and catches it cleanly in one hand, casual and confident, then holds it up and starts speaking to camera, handheld, daylight."
- Natural length: the action reads in about 1.5 to 2.5s. The 4s rung.

### B9. Pattern-interrupt motion across frame
- What happens: a fast object or hand swipes across the whole frame, left to right or toward the lens, briefly blocking the view, then clearing to reveal the creator or product.
- Why it stops the scroll: the full-frame wipe is a hard visual interrupt that breaks the scroll rhythm; the reveal after the wipe restarts attention.
- Prompt fragment: "A hand swipes quickly across the lens from left to right, briefly filling the frame, and as it clears the person is revealed mid-gesture beginning to speak to camera, handheld, natural light." Use as a clean seam-friendly opener.
- Natural length: the action reads in about 1 to 2s. The 4s rung.

### B10. Phone flip to back camera
- What happens: the creator starts on the front (selfie) camera, then visibly flips the phone to the rear camera to show something, the framing and image quality shift on the flip.
- Why it stops the scroll: the flip is a familiar real-creator gesture that signals "I'm about to show you the actual thing," promising proof.
- Prompt fragment: "The person holds the phone selfie-style speaking to camera for a beat, then flips the phone to the rear camera, the view swings and reframes onto [PRODUCT / RESULT], handheld, the voice continues over the flip." Keep it one continuous render so the voice does not break.
- Natural length: the action reads in about 2.5 to 4s. The 6s rung.

### B11. Satisfying texture close-up
- What happens: an extreme close-up of a satisfying texture in motion, cream swirling, gel dipping, powder sifting, fabric stretching, foam building.
- Why it stops the scroll: ASMR-grade texture is a strong sensory magnet; macro detail looks premium.
- Prompt fragment: "Extreme macro, [TEXTURE: cream swirls / gel stretches / powder sifts] in slow motion filling the frame, rich detail and soft highlights, then cut to the person applying or holding [PRODUCT] and speaking to camera, soft diffused light."
- Natural length: the action reads in about 2.5 to 4.5s. The 6s or 8s rung.

### B12. Walking into frame mid-action
- What happens: the frame starts empty or on a scene, and the creator walks in already talking and already doing something (carrying the product, mid-gesture), as if you caught them in motion.
- Why it stops the scroll: human motion entering an empty frame is a strong attention cue; "already in progress" energy feels candid.
- Prompt fragment: "Frame starts on an empty room, the person walks briskly into frame already mid-sentence holding [PRODUCT], sits or stops and continues speaking to camera, handheld follow, natural window light."
- Natural length: the action reads in about 2.5 to 4s. The 6s or 8s rung.

### B13. Holding the product up to the lens
- What happens: the creator brings the product right up close to the camera so it briefly dominates the frame, label or detail readable, then pulls it back to talk.
- Why it stops the scroll: an object filling the lens is a scale and focus break; it puts the product on screen in second one.
- Prompt fragment: "The person raises [PRODUCT] close to the lens so it fills the frame and the label is sharp, holds for a beat, then lowers it and begins speaking to camera, handheld, bright even light." Strongest when the product image is the locked reference so the label matches exactly.
- Natural length: the action reads in about 1.5 to 3s. The 4s or 6s rung.

### B14. Quick demo / instant result in hand
- What happens: a fast, real demonstration of the product working in the opening, a swatch wiped clean, a stain lifting, water beading off, a spray absorbing instantly.
- Why it stops the scroll: visible proof up front collapses skepticism before a single claim is spoken.
- Prompt fragment: "Close-up, the person performs [QUICK ACTION: wipes the swatch and it lifts clean / sprays and it absorbs instantly / pours water and it beads off], the result is visible immediately, then they look to camera and speak, handheld, natural light." Best with direct-claim (A7) and challenge (A6) lines, the visual pays the claim.
- Natural length: the action reads in about 2.5 to 4.5s. The 6s or 8s rung.

Hook length note (NO ladder): every hook is SHORT, about 8 to 13 words, rendering at roughly 3 to 5 seconds at ~3.5 wps plus 1 to 2s for the visual action. All four hooks are short; they differ by ANGLE and by KIND of visual action, never by length. Any HALF B visual works on a short hook — keep the action quick (1 to 2s). The "natural length / rung" notes in the B1 to B14 entries above are just hints about how long an action reads; ignore the rung labels, there is no ladder.

Drama tiering (use to keep the four opens genuinely different KINDS of action, not two near-identical camera moves):
- HIGH-DRAMA / pattern-interrupt: B2 pour, B3 before/after, B4 mess, B6 object reveal, B7 transform, B12 walk-in, B14 demo.
- LOWER-DRAMA / slight camera move: B5 push-in, B8 drop-catch, B13 lens-hold (these read alike to a vision model, so do not use two of them across the four variants).
- Across the 4 variants, use at least 3 high-drama hooks, and never pair two lower-drama moves. Prefer a mix: one cold-open-in-action, one problem-state or mess, one product-transform or demo, one reveal or walk-in.

---

## PAIRING (verbal + visual into one hook)

A hook = one VERBAL line (HALF A) + one VISUAL action (HALF B), kept SHORT (~3 to 5s). The body is shared across all 4 ads; the hooks are the per-ad opener, and the b-roll-count ladder (0/1/2/2) plus the 4 unique hooks make the ads distinct. Every ad ends on the CTA.

### The non-negotiable rule
Every hook MUST carry a visual action from HALF B. A spoken line over a static talking head is NOT a hook and is rejected in Step 3.

### How to combine, step by step
1. Pull a verbal line from the Hook Bank (Step 1) and tag its HALF A archetype. That gives `verbal_hook`.
2. Pick a HALF B visual that EARNS it (e.g. reaction A8 with a reveal B7, direct-claim A7 with a demo B14, confession A4 with an object reveal B6). That gives `visual_hook`.
3. Keep the line short (~8 to 13 words). There is no length rung to hit.
4. Do this for all 4 ads with 4 DIFFERENT verbal angles and 4 DIFFERENT KINDS of visual action. Never reuse a hook.
5. Render the 4 hooks as 2 REELS (~2 hooks per generation, under 10s), each described as scenes with a hard cut, then SPLIT each reel at its cut into hook clips. Each hook scene is a TALKING render: locked face + body + product (if shown) + voice clip, and NO video input.

Distinctness across the 4 ads = 4 unique hooks + the b-roll-count ladder (0/1/2/2). build_manifest.py enforces unique fingerprints, that every ad ends on the CTA, and that V3/V4 place their (two) b-rolls differently.

### Worked example: a sample product (greens powder)

Shared body (PAS or SIMPLE), ending on the CTA, reused under all 4 ads. The 2 product-only b-rolls (e.g. the pouch standing on a counter; an extreme label close-up) are reused. Only the hook and the b-roll count/placement change:

| Ad | Verbal hook (HALF A, short) | Archetype | Visual action (HALF B) | B-rolls |
|---|---|---|---|---|
| V1 | "Okay, I literally owned like thirty supplement bottles." | A4 Confession | B6 object reveal (armful of unbranded bottles) | 0 |
| V2 | "Stop buying ten supplements that just cancel each other out." | A2 Contrarian | B1 product slam | 1 (bA) |
| V3 | "This one pouch replaced every supplement I used to take." | A7 Direct claim | B13 lift product to lens | 2 (bA + bB) |
| V4 | "I finally threw out my entire cabinet of supplements." | A3 Curiosity | B4 mess (tosses a cabinet of bottles into a bin) | 2 (bA + bB, placed differently) |

Across V1 to V4: 4 different verbal angles, 4 different KINDS of visual action, the b-roll-count ladder 0/1/2/2, and every ad ending on the CTA. On the feed these read as four creators, which is what Andromeda needs.
