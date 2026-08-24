# Shot vocabulary, Unboxing

Measured from the ten banked unboxing ads in this skill's own bank, 2026-08: 83 shots, 8.3 shots per ad. Among the fewest in the family: only POV at 5.8 and expert at 6.8 run leaner.

This file has two halves.

**The PROMPT BLOCK below is the only part that reaches the video model.** It is pasted verbatim
into the render prompt. A conditional shot row may be DROPPED when the product cannot support
it; nothing is ever added, renamed, or given a different number.

**Everything under THE MEASUREMENTS is engine-facing** and is never pasted: provenance, the raw
counts the prompt block was derived from, doctrine notes, and the reasoning behind house rules
that override the bank. It exists so the numbers can be re-checked, not so a model can read them.

---

## PROMPT BLOCK

<!-- PROMPT-BLOCK-START -->
FORMAT: UNBOXING UGC

This kind of ad is simple. A sealed parcel arrives, hands open it, and you watch everything
come out of it one thing at a time.

The rules:

1. Hands only. Never show a face and never show anyone talking.
2. Start with the parcel still sealed.
3. Open it on camera. Never cut to it already open.
4. Take each item out, turn its label to the lens, put it down.
5. Let the moment the inside is first seen run longer than anything else.
6. Put it on a real surface someone actually owns.
7. Never tidy the packaging. Let the paper crumple and the tape tear.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
The sealed parcel from above. Hands on the lid. What is inside, first seen. Each item lifted out
close. An item turned over in the hands. The product being used at the end. Use them however you
want. Two things hold: the ad is filmed looking down at the surface rather than at eye level,
and the shot of the inside being seen for the first time is the longest one in it.

Nothing moves except the hands and the things they touch.

HOW THEY PLAY IT
The hands are unhurried and genuinely curious, opening it the way someone opens their own
parcel. Never brisk, never the smooth hands of a product video.

TIMING
At least two shots run under half a second and at least one runs over five seconds. Cut quickly
through the parcel arriving and opening, then let the reveal breathe. Every shot change is a
hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## WHO IS ON SCREEN

**HANDS. Almost never a face.** Eight of the ten banked ads say it outright: "no face, hair,
eyes or full outfit are visible", "No face appears", "no face or body is shown." One shows a
face only in the final use shots. One has a dog as the living subject because it is pet food.

```
Across the bank: 0 on-camera lines, 16 voiceover lines.
```

Nobody talks to camera in this format, ever. Eight of ten carry no dialogue at all. When the ad
does speak, the voice arrives as VOICEOVER over the hands.

**The nails are described in every banked ad**, because the hands are the performer: neat
natural, pale nude, bright green, short manicured. Whatever they are, they stay the same
throughout.

## WHAT IS ALWAYS IN FRAME

- The container and the hands opening it
- A real domestic surface underneath: a duvet, a wooden table, a sofa cushion, a carpet, a
  countertop. Never a studio sweep and never a styled prop shelf
- Product labels turned toward the lens as each item comes out
- Packing material behaving like packing material: tissue crumpling, paper rustling, cardboard
  holding a crease

## HOW THE CAMERA BEHAVES

**Locked, and usually looking DOWN.** Top-down or oblique-overhead is this format's home angle,
not eye level. Every banked ad describes a locked camera: "static camera throughout", "camera is
locked above/oblique to the box", "camera stays locked close to the product." One ad is a single
continuous 24-second locked shot.

**Nothing moves except the hands and the products.** One prompt states it plainly: "all movement
is from the hand and products."

---

## THE HOOK, shot one

```
duration, banked:   median 1.90s, range 0.7 to 9.5   house rule: 1 to 2 seconds
what it is:         the sealed container, already being touched
```

Every banked opener is the unopened package with hands arriving on it: a shipping carton on a
duvet with a hand presenting it, a kraft box on a wood table with fingers under the flaps, a
retail carton held up to hard light. The seal is intact and the opening has already begun.

The container is the hook. Not a person, not a claim, not a caption.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Sound |
|---|---|---|---|---|
| SEALED CONTAINER, top-down | always | ~20% | 0.7 to 3.5s | cardboard, tape, film |
| OPENING, hands on the lid or flaps | always | ~25% | short | tearing, lifting, rustling |
| INTERIOR REVEAL, what is inside | always | ~15% | 1 to 9s | tissue, packing, first sight |
| PRODUCT CLOSE-UP, item lifted out | always | ~20% | short | handling, weight, surfaces |
| PRODUCT ROTATION, turned in hand | optional | small | short | the object being examined |
| IN USE, opened, applied or handled | when the ad opens or uses a product | ~10% | can run long | the product working |

A conditional row is DROPPED when the ad does not do that thing. No row is added or renamed.

## WHAT USUALLY HAPPENS

The bank runs the same loop, and the loop IS the format. One prompt states it exactly: **open
the box, remove each item, turn its label toward the lens, set it aside.** Then repeat for the
next item.

Where a container holds several products they come out FAST, each getting a brief moment rather
than one being studied. Many banked ads finish by arranging everything into a flat lay, the
whole haul laid out together as the closing image. Where the ad uses a product, that comes last,
after everything has been shown.

---

## SOUND

The format is sound-carried by default. The track is packaging and handling: tape pulling, a lid
lifting, tissue crumpling, a jar set down on wood, a cap unscrewing. Real, diegetic, made by the
things on screen. No music anywhere.

## RHYTHM

```
banked CV of shot lengths:   0.58          shortest 0.40s, longest 24.10s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.7 seconds and at least one runs over 5.6 seconds.
```

Uneven with a specific shape: the front of the ad cuts quickly through arriving and opening,
then the reveal is allowed to breathe. A nine-second hold on an interior is normal here. What is
wrong is eight shots of equal length marching through the box.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
Every line is VOICEOVER, laid over the hands. No speaking face ever appears in this format.
```
