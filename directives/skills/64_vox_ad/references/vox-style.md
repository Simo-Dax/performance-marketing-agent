# VOX style — the locked look and the measured model behavior

## THE STYLE BLOCK (byte-identical in every keyframe prompt)

> Mixed-media hand-cut PAPER COLLAGE, editorial zine style. Torn and scissor-cut paper
> edges, halftone print dots, real paper drop shadows. Every object is a matte
> printed-texture paper cutout sticker, NOT CGI, NOT a 3D render, no glow.

Follow it with the palette line (locked hexes) and a composition line ("Simple and bold,
lots of empty space." / "Densely packed like a detective's evidence board." — per frame).
The hero frame swaps "Every object" for "Every object except the logo/product" and drops
"no glow" for the anchor only.

## Palette law

2–4 hexes pulled from the Brand DNA: one dark background, one light paper, one bright
accent; warm gold reserved for review stars. Named AND hex in the prompt ("deep navy
background (#18284A)"). Repeat "No red anywhere" style exclusions explicitly — models
sneak accent colors otherwise. Between two VOX ads for the same brand, shift the
background shade (banked: #081425 ad 1 → #18284A ad 2) so the pair never reads as a
repeat.

## Paper physics (why it reads as collage, not vector)

Torn/scissor edges on every cutout; halftone dot texture; REAL drop shadows (each cutout
its own); tape corners sparingly; small paper-fragment bursts on hard landings; torn
edges "flutter" and halftone dots "pulse" in the hold. Flat 2D always: camera parallel to
the poster, no 3D rotation, no photoreal, no depth of field.

## Pop-in vocabulary (the motion verbs the model executes well)

pop in with a snappy overshoot bounce · SLAM down with a hard bounce and paper fragments ·
deal outward one after another · stamp down flat like a rubber stamp · slide in and settle ·
draw itself on (arrows, strings) · fan in page after page · stream continuously (conveyors) ·
pulse in place (badges) · grow out word by word (speech bubbles). Beats land 0.4–0.8s
apart on the schedule; every arrival gets its own timeline line.

## Text law

Banners ONLY for spoken words (the CTA) or an undrawable codename. Huge bold condensed
lettering, letters at least ONE TWELFTH of frame height (one tenth for a single-word
banner). Two stacked lines beat one long line — 26 characters on one line melts at 1080p.
Banners are BAKED INTO the keyframe, never video-added. Card faces: blank bars + icon
rows, never lettering. Numbers on props (calendar "6", badge "99+") are markings, fine.
Close every image prompt with the only-text clause or "NO TEXT AT ALL anywhere in this
image."

## People

Halftone duotone MAGAZINE-PHOTO cutouts in the ad's palette, scissored with a thick clean
white outline, waist-up, expressive poses (holding a sheet up, mid-sentence). In video
prompts ALWAYS: "The people stay as flat printed cutouts, no realistic motion, only
slight paper bobbing." Without the guard the model animates them like humans and the
collage dies.

## Product and anchors

- Physical product = PHOTOGRAPHIC sticker: "reproduced exactly as supplied, cut out with
  a thick clean white paper edge and a real drop shadow. Do not re-letter, re-colour,
  redraw or re-typeset any part of the packaging." Real photo attached as the image
  reference on every keyframe that shows it. Hero scale in its frames — packaging small
  print melts at ANY resolution; never promise it.
- Brand logo (software hero frame): "reproduced exactly as supplied… it sits directly on
  the background, and it is the only glowing thing in the picture." If the file has a
  background tile, match the ad background to the tile's hex and the composite seam
  disappears.
- Third-party tool logos: same reproduce-exactly clause, "each cut out as a paper sticker
  with a torn white edge." Caution at the gate: paid Meta creative with third-party logos
  risks rejection; organic/community is fine.
- Video prompts guard every anchor: "stays perfectly sharp, stable and unchanged once it
  lands."

## MEASURED Seedance 2.5 behaviors (from the two banked builds — plan around these)

1. **Order is obeyed; the back half compresses.** Elements arrive in prompted order
   nearly always, but late-clip beats land 0.5–1.3s EARLY (measured: logo asked 2.9s →
   1.6s; RESEARCH asked 4.1s → 3.0s). Front-of-clip beats are near-exact.
2. **Beat density fixes pacing.** Clips with 5–7 scheduled arrivals track their schedule
   (banked clip 2: coins/flames/calendar all within 0.2s, zero correction). Clips with 2
   beats and a long gap compress worst. Fill the timeline.
3. **Dead holds appear** (0.8–1.1s flatlines mid-clip when the model finishes early).
   Frame-diff finds them; cutting them is free and invisible.
4. **Final frames land.** The reference-as-final-frame contract holds; judge content by
   the landing, not mid-flight wobble.
5. **Occasional late element** (banked: a banner 1.0s late) — fixed by cutting the hold
   before it, not by stretching.
6. **Foley comes back loud** (impacts peaking -1.6 to -4.5 dB vs VO mean -16.7). Always
   remix: sfx ~0.11 gain under the untouched VO, loudnorm -16 LUFS.
7. **Text in generated video survives when it entered via the keyframe** at banner scale;
   never ask the video step to CREATE text.
