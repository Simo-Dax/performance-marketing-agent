# Shot vocabulary, Green Screen Reactions

Measured from the ten banked green screen ads in this skill's own bank, 2026-08: 84 shots, 8.4
shots per ad.

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
FORMAT: GREEN SCREEN REACTION UGC

This kind of ad is simple. One person talks straight to camera and reacts to something. You only
film the person. The thing they are reacting to gets added afterwards.

The rules:

1. Film the person and nothing else. Never render what they are reacting to.
2. Never put a screen, a graphic or a picture in the frame.
3. Hold one framing for the whole ad: same distance, same crop, same position, same pose.
4. Never move, rescale or reframe the camera. It has to be composited later.
5. Light them flat and straight on, with no shadow, so they cut out cleanly.
6. They gesture at the empty space beside them where the thing will go.
7. They start with an opinion and stay on camera the whole way through.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Them chest-up talking. The same frame with them out of it. The product lifted into the same
frame. Use them however you want. Two things hold: there is only one camera position in the
whole ad, so every cut is a jump cut inside that framing; and the empty frame with nobody in it
is a real shot, filmed from the same spot, so it cuts against the others.

The camera is completely still and stays where it is.

HOW THEY PLAY IT
She has an opinion and she is enjoying having it. Animated and reactive, talking straight at
one person. Never blank, never neutral, never reading.

TIMING
At least two shots run under one second and at least one runs over five seconds. Reactions are
allowed to run. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## THE RENDER IS THE PERSON ONLY

This format is half an ad. The render produces the REACTOR and nothing else. What they are
reacting to, the article, the screenshot, the video, the comment, is added by the user
afterwards in their editor, and the delivery note names what belongs behind them and at what
timecode.

**Never render the background. Never render what is being reacted to.** Not as a screen in
frame, not as a graphic, not as an inset. A generated version of the evidence is fabricated
evidence, and it also cannot be swapped later, which is the entire reason for shooting this way.

```
on-camera 79  :  voiceover 4
```

Nineteen out of twenty lines are spoken on camera by the reactor. There is no narrator.

## THE LIGHT IS A TECHNICAL REQUIREMENT, NOT A LOOK

Every banked ad describes the same thing: "soft even frontal indoor light, minimal shadow",
"soft bright frontal creator light", "even frontal exposure, minimal shadow", "soft even frontal
phone light on her face and glasses, minimal shadow."

Flat, frontal, shadowless light is what makes a person cleanly separable from their background.
Hard side light or a strong shadow makes the cutout ragged. Skin still reads as skin: the bank
insists "skin remains naturally textured."

## ONE FRAMING, ONE POSE, HELD THROUGHOUT

The banked ads show the reactor at different SIZES and in different PARTS of the frame across a
single ad. **That variation is the EDITOR's, not the camera's.** The creator filmed themselves
once, in one position, and the editor scaled and repositioned the keyed cutout to make room for
whatever was going behind them.

So the render does the opposite of what the finished ads look like:

**Hold one framing for the entire render.** Same distance, same crop, same position in frame,
same seated or standing pose, from the first frame to the last. The reactor stays put. What
changes is their face, their hands and what they are saying.

A render that drifts, rescales or repositions the person cannot be composited, because the
user has no way to place the background behind a moving target. A consistent plate is the
deliverable.

**The scale and position changes are recommended in `post-production.md`**, with timecodes,
exactly like the background footage, the on-screen text and the music. The banked distribution
is there to inform that recommendation:

```
medium chest-up          19   the default
tight chest-up cutout    13   pushed in, face large
small chest-up cutout     8   reactor reduced into a corner or lower frame
tight selfie close-up     6   very close
empty reactor plate       4   the reactor is not in frame at all
```

**The EMPTY PLATE is the one legitimate framing change.** Four banked ads include intervals where
the reactor is absent and the background carries the ad alone. Render those as clean empty frames
of the same setting, from the same camera position, so they cut against the reactor shots.

---

## THE HOOK, shot one

```
duration, banked:   median 5.00s, range 1.7 to 30.0
under 2 seconds:    2 of 10   <-- this format opens SLOWER than the house rule
```

**A conflict worth knowing about.** The house rule is a hook under 2 seconds and this bank runs a
median of 5.00. The reason is structural: the hook here is a spoken CLAIM plus the reaction to
it, and both need room. One banked ad is a single unbroken 30-second reaction with no cuts.

Open as fast as the claim allows.

**What the hook contains.** The reactor square to the lens, already talking, with a stated
position: "Never felt overwhelmed trying to boost your business's online presence", "Writing
emails is a waste of valuable time", "If you think losing weight is just about discipline, that
might surprise you."

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| REACTOR, the one held framing | always | ~90% | 2 to 30s | on camera |
| EMPTY PLATE, same framing, no reactor | optional | ~5% | short | silent |
| FACE AND PRODUCT, product raised into the same frame | when a product is held | small | short | on camera |

Only three rows, because this format renders one camera position. The cutting between them is
the only shot change the render produces.

A conditional row is DROPPED when the ad does not use it. No row is added or renamed.

## WHAT USUALLY HAPPENS

The reactor states a position straight to the lens and then works through it: reacting,
disagreeing, explaining, pointing at things that are not there yet. They stay in the same place in frame
throughout. They gesture toward the space beside them where the evidence will go, and they may
leave frame entirely for a beat. The ad ends with them delivering the ask from the same position
it started in.

Their clothing is ordinary and the setting is a real room: a home, an office, a clinic, outdoors
in a coat. Nothing about the person or the place is keyed, coloured or special.

---

## SOUND

The reactor's voice, on camera, near-continuous. Quiet room tone underneath. No music, and
nothing from the footage they are reacting to, since that footage does not exist yet.

## RHYTHM

```
banked CV of shot lengths:   0.51          shortest 0.20s, longest 30.00s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 1.0 seconds and at least one runs over 5.4 seconds.
```

Calmer than the cut-heavy formats. Reactions are allowed to run, and in the finished ads the
variation comes from the editor rescaling the cutout rather than from rapid cutting. In the
RENDER, which holds one framing, the cuts are jump cuts within that framing. Banked averages run
from 1.6 to 4.9 seconds a shot, and one ad has no cuts at all.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

**No background, no keying colour, no overlay.** The reactor is filmed in an ordinary real
setting; the user keys and composites afterwards.

**No camera move, no rescale, no reframe.** One position, held. Every change of the reactor's
size or placement is a post-production decision and is recommended in the delivery note.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
Every line is spoken ON CAMERA by the reactor. This format has no voiceover; the empty-plate intervals carry no words.
```
