# Shot vocabulary, Before and After

Measured from the ten banked before-and-after ads in this skill's own bank, 2026-08: 119 shots,
11.9 shots per ad.

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
FORMAT: BEFORE AND AFTER UGC

This kind of ad is simple. You see how something looked before, you watch it change, and you
see how it looks after.

The rules:

1. The thing that changes is the subject. Not the person. The thing itself.
2. Film the before and the after from the same distance, in the same light, at the same angle.
3. Get close enough that nobody could argue with what they are seeing.
4. Show the change actually happening in between.
5. Let the clothes change between clips. That is how weeks show.
6. Never blend or morph the before into the after. Cut between them.
7. Hold the after longer than any other shot.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Very close on the thing that is changing. The product going on. Her in ordinary framing. The
bottle on its own. The finished state. Use them however you want. Two things hold: the same
extreme close-up appears on both sides of the change and it is what proves it, and the finished
state is the longest shot in the ad.

The camera is still inside every shot. It can move between setups, never during one.

HOW THEY PLAY IT
Unguarded and ordinary. The before shown without embarrassment, the after without triumph.
Matter-of-fact, never a reveal performance.

TIMING
At least two shots run under half a second and at least one runs over five seconds. The very
short frames are used deliberately, as flashes. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## THE SUBJECT IS THE THING THAT CHANGES

Not the person. The hair, the skin, the nails, the surface. One banked prompt puts it exactly:
"the visual focus is her long dense natural dark hair." The face appears in service of the
change, and in one ad only a hand and wrist are visible at all.

**The change must be visible at texture level.** The bank films it close enough that it cannot
be argued with: "the face is filmed extremely close so real pores, blemishes, redness and later
dewy skin texture remain visible", "keep hair fibers and oil sheen realistic rather than overly
glossy."

## THE FORMAT'S ONE INTEGRITY RULE, and how the bank actually does it

The before and the after are the SAME subject under MATCHED conditions: the same framing, the
same distance, the same light. A change that only appears because the second shot was lit better
is not a change, and a viewer reads that instantly.

**But time is allowed to show.** The bank separates its clips by DAY, and lets the wardrobe and
small background details shift between them: "each early clip is a separate take with small
wardrobe/appearance changes", "outfit/background fragments may shift." Meanwhile one prompt is
explicit that "soft neutral indoor light remains similar across days."

So: **the light and the framing stay locked, the clothes change.** That is what reads as weeks
passing rather than as one afternoon with better lighting.

**One thing carries continuity across every clip.** In the bank it is stated directly: "hair
remains the continuity anchor." Whatever is transforming is the thing that must be
unmistakably the same thing throughout.

## HOW THE CAMERA BEHAVES

**Static within each setup, and very close.** "Camera is locked extremely near the face and
product", "static phone at roughly eye level", "same doorway framing through almost the entire
clip", "camera stays close and static." The camera may move between setups; it does not move
inside a shot.

---

## THE HOOK, shot one

```
duration, banked:   median 1.65s, range 0.1 to 4.9   house rule: 1 to 2 seconds
under 2 seconds:    6 of 10, the fastest openers in the family
```

Three openers appear in the bank and any of them works:

1. **The BEFORE state, extreme close-up.** Blemishes, redness, dry hair, a bare nail.
   Uncomfortably close.
2. **A flash of the AFTER.** Two banked ads open on a 0.1 second frame of the finished result
   before cutting away. A tenth of a second, then gone.
3. **The product, macro.** The bottle before anything has happened.

No banked opener starts with a person explaining what they are about to do.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| EXTREME CLOSE-UP of the affected area | always | ~19% | 0.1 to 4s | voiceover or silent |
| PROCESS SHOT, the change happening | always | ~15% | can run long | voiceover |
| MEDIUM CREATOR, subject in frame | always | ~15% | short | either |
| TALKING HEAD | optional | ~5% | short | on camera |
| PRODUCT CLOSE-UP | always | ~7% | short | voiceover or silent |
| TEXTURE / DETAIL | optional | small | very short | silent |
| THE AFTER REVEAL, the finished state | always | ~15% | the longest shot in the ad | either |

**EXTREME CLOSE-UP.** The most common shot and the one that carries the proof. It appears on
BOTH sides of the change, matched.

**THE AFTER REVEAL.** Sixteen banked shots are typed explicitly as a reveal, a result, an after
or a final shot. It is the payoff and it is a distinct shot rather than just the second half of
a matched pair: the subject turned toward the lens, the hair moving, the hand posed, the skin in
the same light as the opening. It is held longer than anything else in the ad, and it is often
also flashed at the top as the hook.

**PROCESS SHOT.** The middle of the transformation and the reason a viewer stays: the applying,
the styling, the working-in, the drying. Allowed to run.

A conditional row is DROPPED when the ad does not do that thing. No row is added or renamed.

## WHAT USUALLY HAPPENS

The starting state is shown close and honestly. The product appears and is used, in real time,
with hands doing recognisable work. Clips separated by days stack up, the wardrobe changing
between them while the light and framing hold. The change accumulates rather than jumping. The
final state is shown in the same framing as the first, and held longer than anything before it.

---

## SOUND

```
Across the bank: 10 on-camera lines, 22 voiceover.
```

Two thirds of the spoken lines are VOICEOVER over the process and the states. Eight of ten
banked ads carry no dialogue at all and are led by picture and sound. When a face does talk to
camera it is brief and never the whole ad. Under it: room tone, water, hands working, a dryer.
No music.

## RHYTHM

```
banked CV of shot lengths:   0.73          shortest 0.10s, longest 13.40s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.7 seconds and at least one runs over 3.7 seconds.
```

Among the most uneven in the family, second only to testimonial: a one-tenth-of-a-second flash and an eleven-second process
hold inside the same ad. The very short frames are used deliberately, as flashes of the result.
Even spans are wrong here more than anywhere.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps, and above all **no morph or blend between the before and the after**.
The change is shown by a hard cut between two matched shots.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
You decide which lines are spoken on camera and which are carried as voiceover over the states and the process.
```
