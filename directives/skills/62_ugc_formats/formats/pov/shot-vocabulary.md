# Shot vocabulary, POV Skits

Measured from the ten banked POV ads in this skill's own bank, 2026-08: 58 shots, 5.8 shots per
ad. The FEWEST shots of any format in the family.

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
FORMAT: POV SKIT UGC

This kind of ad is simple. It is a little scene between two people, something annoying
happens, and the product sorts it out.

The rules:

1. It is played, not presented. Nobody talks to the audience.
2. One performer plays both people. A change of top tells them apart.
3. The camera is a person in the scene. It sees what they see.
4. Set the situation up first. A joke with no setup is just confusing.
5. Let the scene run. Never chop it into fast pieces.
6. The product turns up late and casually, as the thing that fixes it.
7. Film it somewhere ordinary, in the light that is already there.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
The scene playing with both people in it. A wider shot so you can see bodies and space. Close on
a face reacting. The product on its own when it lands. Use them however you want. Two things
hold: takes run long here and a whole ad can be one unbroken shot; and the reaction close-up is
the punchline, so it comes after the thing happens, never before.

Handheld and deliberately unpolished. The framing is wherever someone happened to be standing.

HOW THEY PLAY IT
Played, not presented. Broad enough to read in two seconds but never theatrical: real
irritation, a real eye-roll. Committed to it, never reciting.

TIMING
At least two shots run under one second and at least one runs over six seconds. Long scene shots
with a few very short reaction cuts. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## THIS IS A SCENE WITH ROLES, NOT A CREATOR TALKING

POV is played, not presented. The banked ads are small scenes: a bartender behind a counter,
someone leaning into a colleague's desk, a shop assistant on a stockroom floor, two people on a
mat, a woman feeding a dog in a barn.

**One performer often plays BOTH roles.** Two banked ads do this: "performing two coworker
roles through alternating [shots]", "he plays two roles", with wardrobe or a prop distinguishing
them. The camera cuts between the two positions and the same person appears in each. This is a
signature of the format, not a shortcut.

**The camera is frequently a character.** The lens is the point of view of someone in the scene,
which is what the format is named after. Someone off-camera may speak to the person on screen.

## WHERE IT HAPPENS: ORDINARY WORKING AND LIVING PLACES

The bank runs: an open-air bar, a retail shop floor and its stockroom, an office meeting-room
corner, a bedroom filmed from bed height, a home office, a barn and dog run, a living room, a
bathroom. Real places with real practical light: overhead shop fluorescents, coloured LED
strips, daylight through a window.

## HOW THE CAMERA BEHAVES

**Handheld and deliberately unpolished.** The bank describes "casual handheld phone footage",
"handheld-phone/selfie-style framing", "an intentionally unpolished handheld" look. The framing
is not composed; it is where someone happened to be standing.

**Takes run long.** One banked ad is a single continuous 20-second shot with no cuts at all.
Another is three shots for the whole ad. This format holds a scene while it plays out rather
than cutting around it, and cutting a skit into fast fragments kills the joke.

---

## THE HOOK, shot one

```
duration, banked:   median 4.15s, range 1.4 to 20.0
under 2 seconds:    2 of 10   <-- this format opens SLOWER than the house rule
```

**A conflict worth knowing about.** The house rule is a hook under 2 seconds. POV's bank runs a
median of 4.15 and only 2 of 10 come in under 2. The reason is structural: a skit has to
establish a SITUATION before anything can be funny, and a situation cannot be established in a
second and a half.

Open as fast as the setup allows. Do not cut the setup to hit a number, because a joke without a
premise is not a fast ad, it is a confusing one.

**What the hook contains.** A recognisable everyday situation already in progress, with the roles
legible immediately: who these people are to each other and what is happening between them.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| MEDIUM, the scene playing | always | ~25% | 2 to 20s | either |
| MEDIUM-FULL or FULL BODY, the situation | always | ~12% | medium | either |
| CLOSE-UP, a reaction | always | ~14% | short | either |
| PRODUCT CLOSE-UP | always | ~12% | short | voiceover |
| WIDE, the place | optional | ~5% | short | voiceover |
| EXTREME CLOSE-UP, a detail or a beat | optional | small | very short | silent |

**MEDIUM-FULL or FULL BODY.** Needed more here than in any format except founder story, because
a skit needs body language and physical space to read.

**CLOSE-UP REACTION.** The punchline shot: the face after the thing happens.

**PRODUCT CLOSE-UP.** The product arrives as the RESOLUTION of the situation, not as a
demonstration. It gets its own shot when it lands.

A conditional row is DROPPED when the skit does not need it. No row is added or renamed.

## WHAT USUALLY HAPPENS

A familiar irritation or exchange plays out between two people, or between one person and their
own second role. It escalates or turns. The product resolves it, often arriving late and
casually rather than being presented. The performances are broad enough to read in two seconds
but not theatrical. The ad ends on the reaction or on the product, and the ask is usually light.

---

## SOUND

```
Across the bank: 33 on-camera lines, 26 voiceover.
```

Roughly half and half, because a POV often has someone speaking from BEHIND the lens, which
reads as voiceover in the shot list but is a character talking in the scene. Under it: the real
sound of the place. No music.

## RHYTHM

```
banked CV of shot lengths:   0.62          shortest 0.10s, longest 20.00s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.8 seconds and at least one runs over 6.1 seconds.
```

Wide and unevenly distributed, though testimonial and before-after both run more uneven: long held scene shots with a few very
short reaction cuts punctuating them. The unevenness comes from letting the scene play and then
cutting hard on the beat.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
You decide which lines are spoken on camera and which come from someone off-camera, behind the lens.
```
