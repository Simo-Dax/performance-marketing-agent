# Shot vocabulary, Tutorial

Measured from the ten banked tutorial ads in this skill's own bank, 2026-08: 108 shots, 10.8
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
FORMAT: TUTORIAL UGC

This kind of ad is simple. She shows you the finished thing first, then teaches you how to do
it while she does it.

The rules:

1. Show the finished result before you teach anything.
2. Never open on step one.
3. Do the steps in the real order they happen in.
4. Never skip a step to save time.
5. Film each step close enough that someone could copy it.
6. Narrate over the work. She is doing it, not sitting talking about it.
7. End on the same result you opened on, in the same framing.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Her hands doing the step. Very close on the part being worked on. The finished result. The
product on its own, label to the lens. Use them however you want. Two things hold: the result
appears twice, at the start and the end in the same framing, and that repeat is the spine of the
ad; and the steps that need watching are allowed to run while the moves between them are quick.

The camera is still at eye level inside every step. Only the bits between steps drift.

HOW THEY PLAY IT
Alive, warm, and enjoying herself. She is pleased to be showing you this and it shows in any
shot her face is in. Telling a mate something good, never reading to a lens.

TIMING
At least two shots run under half a second and at least one runs over five seconds. Shots of
roughly equal length are wrong. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## A VOICE OVER A PAIR OF HANDS

```
voiceover 57  :  on-camera 3
```

The most voiceover-led format in the family. Nineteen out of twenty spoken lines are narration
over the work. The creator is almost never sitting and talking; they are DOING the thing while
explaining it.

**Two of the ten banked ads show no face at all** — only hands and forearms, with "age, hair,
eyes and face never shown." The hands and the subject carry the picture; the face appears as part
of the work rather than as a delivery position.

## WHAT IS ALWAYS IN FRAME

- The hands, doing the actual step, close enough to copy
- The subject being worked on: hair, a face, a surface, a garment, a pan
- The product or tool being used, entering and leaving the frame as each step needs it
- A plain consistent background that does not compete. The bank runs bathroom tile, a bedroom
  vanity, a kitchen, a plain wall, and in two cases a clean matte studio backdrop

## HOW THE CAMERA BEHAVES

**Static within every shot.** The bank says it repeatedly: "static camera within every shot",
"static camera in every shot", "static camera with...". One banked tutorial is a single unbroken
30-second locked take.

**The B-roll is the exception.** One prompt: "opening/final shots are steady, close B-roll mostly
handheld with small background drift." So the steps themselves are locked and the connective
material can drift.

**Top-down appears when the work is flat**, on a table, a deck, a countertop. Eye level when the
work is on a person.

---

## THE HOOK, shot one

```
duration, banked:   median 1.90s, range 0.6 to 30.0   house rule: 1 to 2 seconds
under 2 seconds:    5 of 9
```

**The result comes first.** The banked openers show the finished thing before a single step is
taught: three finished curls hanging against a white surface, the completed hairstyle turned
toward the lens, the clean surface. The viewer is shown the destination, then told how to get
there.

The alternative opener is a flat promise or a dare: "The best stain remover you'll ever own and
it's only three ingredients", "Watch this."

**Never open on step one.** Step one is not interesting until the result has been seen.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| MEDIUM CLOSE-UP, the work in progress | always | ~32% | 1 to 6s | voiceover |
| CLOSE-UP, hands on the subject | always | ~10% | short | voiceover |
| FACE CLOSE-UP, the area being worked on | when the product goes on a body | ~8% | short | voiceover |
| RESULT SHOT, the finished thing | always | ~8% | medium | voiceover |
| PRODUCT MACRO or STILL LIFE | always | ~5% | short | voiceover |
| TOOL OR TECHNIQUE CLOSE-UP | when a tool is used | ~5% | short | voiceover |

**MEDIUM CLOSE-UP.** The home position, and a third of every banked tutorial sits here: close
enough to see exactly what the hands are doing, wide enough to keep the subject in context.

**RESULT SHOT.** Appears at the top as the hook and again at the end as the payoff. The same
thing shown twice is the format's spine.

A conditional row is DROPPED when the tutorial does not involve it. No row is added or renamed.

## WHAT USUALLY HAPPENS

The finished result is shown first. Then the steps run in their real order, each one filmed
closely enough to be copied, each one held long enough to be understood. The product or tool
enters when that step needs it and leaves when it is done. Nothing is skipped and nothing is
reordered for pace. The ad closes by returning to the result, in the same framing it opened on.

**Step order is the structure.** A tutorial that cuts a step to save time has taught the viewer
something that will not work.

**Steps are never numbered on screen.** Numbering is a text overlay and belongs in
post-production, where the delivery note recommends it with timecodes.

---

## SOUND

The creator's voice over the work, almost continuously. Under it, the real sound of the task:
water, a dryer, brushing, scrubbing, a lid, fabric. The sound confirms the step is genuinely
happening. No music.

## RHYTHM

```
banked CV of shot lengths:   0.53          shortest 0.30s, longest 30.00s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.7 seconds and at least one runs over 5.2 seconds.
```

Uneven with room to work: the steps that need watching run several seconds, the moves between
them are quick. One banked tutorial is a single 30-second shot, so holding is legitimate here
when the hands are genuinely doing something.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps, and no time-lapse or speed-up between steps. Every shot change is a
hard cut or a jump cut.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
You decide which lines are spoken on camera and which are carried as voiceover over the work.
```
