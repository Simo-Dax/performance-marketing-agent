# Shot vocabulary, ASMR

Measured from the ten banked ASMR ads in this skill's own bank, 2026-08: 113 shots, 11.3 shots per ad.

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
FORMAT: ASMR UGC

This kind of ad is simple. Two hands use one product very slowly, filmed extremely close, and
the sound the product makes is the whole ad.

The rules:

1. Nobody speaks. No narrator, no whispering, not one word.
2. The sound the hands and the product make is the point. Film the actions that make good noise.
3. Everything is a close-up. Never a wide shot.
4. The camera never moves. Only what is inside the frame moves.
5. Light it hard and direct so wet and glossy things catch the light.
6. Take one product all the way through: pick up, open, dispense, spread, put down.
7. Never rush the hands. They handle it like someone actually using it.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Very close on skin as the product goes on. Hands and the product filling the frame. The
container being opened. The product on its own. Extreme close on the texture. Use them however
you want. Two things hold: each stage of using the product gets its own shot and its own noise;
and one satisfying action is allowed to run for ten seconds, which would be dead air anywhere
else.

Put it on a hard surface that makes sound. Nothing in the background matters.

HOW THEY PLAY IT
The hands do not rush and do not perform. They handle it like someone genuinely using it, with
the pauses and adjustments of real handling. Deliberate and unhurried.

TIMING
At least two shots run under half a second and at least one runs over three seconds. Uneven but
calmer than the talking formats. A row of identical medium-length shots is wrong. Every shot
change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## WHO IS ON SCREEN

**Usually only HANDS.** Three of the ten banked ads show nothing else: "no face, age, hair, eyes
or clothing appear." Hands and forearms do the entire ad.

**When a person appears, they appear in pieces.** A face close enough that it is a surface, not
a portrait. Cheeks, a jaw, a forehead, an eye. Never a full head-and-shoulders talking position,
because nobody is talking.

**The nails are part of the subject.** Every banked ad describes them, because the hands are the
performer: short natural unpainted, long almond glossy deep red, long pale-pink with a glitter
accent. Whatever they are, they are consistent and deliberate.

**The people are not always women and the products are not always beauty.** One banked ad is a
man in cleaning gloves detailing a car wheel. The format is defined by sound and texture, not by
category.

## WHAT IS ALWAYS IN FRAME

- The product, very close, with its label legible and facing the lens whenever it is held
- Hands touching, pressing, opening, lifting, spreading
- A real surface underneath: tile, marble, a mirrored shelf, a countertop, concrete. Hard
  surfaces that make sound
- Nothing in the background that matters. It is plain, shallow, and often falls away entirely

## HOW THE CAMERA BEHAVES

**Locked and completely still.** Every banked ad says static, and several say "locked static
camera throughout." The camera never moves. What moves is inside the frame.

**Very close, always.** There are no wide shots and no establishing shots in this format at all.
The frame is filled by a hand, an object, or a patch of skin.

**The light is hard and direct.** This is the format's visual signature and it is in every
banked ad: "hard-edged diagonal shadows", "strong direct warm sunlight with crisp shadows and
glossy highlights", "bright direct flash-like light gives wet skin, plastic and product peaks
hard glossy highlights." Soft flat light kills ASMR, because the specular glint on a wet or
glossy surface is half of what the format sells.

---

## THE HOOK, shot one

```
duration, banked:   median 2.00s, range 1.4 to 10.9   house rule: 1 to 2 seconds
what it is:         a physical action already in progress, with a sound
```

Every banked opener is a hand doing something: a hand entering an empty frame, palms rubbing
foam over wet cheeks, a thumb pressing a pump, two hands loosening a ribbon, a spatula drawn up
through cream. Not one opens on a still object waiting to be picked up.

**The hook is the first SOUND as much as the first picture.** Open on the action that makes the
best noise.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Sound it makes |
|---|---|---|---|---|
| FACE CLOSE-UP, product on skin | when the product goes on a body | ~31% | 0.3 to 10.9s | wet spread, tapping, patting |
| MEDIUM CLOSE-UP | always | ~18% | short to medium | movement, fabric, handling |
| HAND AND PRODUCT MACRO | always | ~16% | short | the pump, the lid, the squeeze |
| PACKAGE CLOSE-UP | always | ~8% | short | cardboard, film, ribbon, glass |
| PRODUCT CLOSE-UP, object alone | always | ~7% | short | placement on a surface |
| EXTREME MACRO, texture | optional | small | very short | the texture itself |

**PACKAGE CLOSE-UP.** The container being opened, unwrapped, untied, unscrewed. Most of the
format's best sound lives here, and the bank spends real time on it.

**FACE CLOSE-UP.** The most common shot. Very close on skin while the product is worked in, close
enough that it reads as material rather than as a person.

A conditional row is DROPPED when the product does not support it. No row is added or renamed.

## WHAT USUALLY HAPPENS

One product is handled slowly and completely: picked up, opened, dispensed, spread, worked in,
put down. Each stage gets its own shot and each shot makes its own noise. The hands do not rush
and they do not perform; they behave like someone genuinely using the thing. Where there are
several products, the ad works through them one at a time in the same way.

---

## SOUND, and a warning about the bank

```
Across the bank: 0 on-camera lines, 0 voiceover lines.
```

Not one banked ASMR ad contains a spoken word. There is no narrator, no creator talking, no
whispered voiceover. A word anywhere disqualifies the format.

**All ten banked ads read "Ambient music only."** Every one of them was carried by a music bed,
and this agent bans music in every render. So the bank teaches this format's PICTURES and
teaches nothing whatsoever about its sound. Never read a track, a bed or a mood out of those
Audio fields.

Our ASMR ads are **sound-carried**: the plan is built from what the objects and hands physically
make. The lid unscrewing, the pump, the suction release, the wet spread of cream on skin,
fabric, cardboard, glass set down on stone. Real, diegetic, product-made, and nothing the scene
could not physically produce.

## RHYTHM

```
banked CV of shot lengths:   0.49          shortest 0.30s, longest 20.00s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.5 seconds and at least one runs over 2.7 seconds.
```

Uneven, but calmer than the talking formats, and the shot COUNT swings enormously between ads:
the bank holds a 4-shot ad averaging 4.6 seconds a shot and a 26-shot ad averaging 0.7. Both are
correct. ASMR lets a satisfying action run, and a ten-second hold on one continuous sound is
normal here where it would be dead air in a testimonial. What is wrong is a row of identical
medium-length shots.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

**No music, in the render or in the plan.** This is the one format whose entire bank had music
and whose renders must have none. The product makes the track.

## DELIVERY LINE, pasted into the render prompt

**This format has NO pacing block and NO delivery line.** Nobody speaks, so there is no
transcript to place and nothing to decide. The video engine's V.4a block is omitted entirely
for this format.
