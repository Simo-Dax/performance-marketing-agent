# Shot vocabulary, Problem and Solution

Measured from the ten banked problem-and-solution ads in this skill's own bank, 2026-08: 102
shots, 10.2 shots per ad.

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
FORMAT: PROBLEM AND SOLUTION UGC

This kind of ad is simple. Someone has a problem, you watch it happen to her, then you watch
the product make it stop.

The rules:

1. One problem only. Never two.
2. Show the problem. Do not let anyone just talk about it.
3. Let the problem land before anything gets called the answer.
4. Show the fix working, for real, on camera.
5. Show the problem gone at the end. Do not just say it is gone.
6. Film it where the problem actually happens.
7. Never stage another product failing.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Close-ups of the bottle. Very close on the problem itself. Her talking to camera. The problem
happening where she lives. The product going on and working. Use them however you want. Two
things hold: the bottle ends up on screen more than her face does, and the shot of it working is
the longest one in the ad, because the fix has to be watched rather than claimed.

When she talks the camera is still. When she demonstrates it is handheld and close.

HOW THEY PLAY IT
Fed up with the problem, genuinely relieved when it works. She reacts, she does not present.
Never an infomercial.

TIMING
At least two shots run under half a second and at least one runs over five seconds. Cut fast
through the problem, then let the fix breathe. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## WHO IS ON SCREEN, AND IT IS OFTEN NOT A PRESENTER

This format has the most varied cast in the family, because the subject is the PROBLEM and
whoever has it:

- **Hands only**, in four of ten banked ads: "no face, hair, eyes or clothing enter frame"
- **A creator on camera**, appearing at the open and close and narrating the middle
- **Children**, in one, with no adult on camera at all
- **A pet**, in one, as the entire visible subject

The nails are described in every hands-only ad, because the hands are the performer.

## WHERE IT HAPPENS: REAL PLACES, INCLUDING OUTSIDE

The widest location range of any talking format. The bank runs: a residential backyard, a home
kitchen, the inside of a retail chemist under fluorescent light, a resort pool, a porch, a
bedroom, a children's play space, a poolside deck, the floor beside a door.

**The ad goes where the problem is.** It does not stay in one room and describe the problem; it
films it happening in the place it happens.

## WHAT IS ALWAYS IN FRAME

- The problem, shown rather than described: the mess, the stain, the discomfort, the failing
- The product, more often than anything else. Close-up product shots are the single most common
  shot type in the format, more common than any human face
- The real environment, ungraded, with ordinary phone exposure and blown highlights where the
  sun is strong

## HOW THE CAMERA BEHAVES

**Mixed, and split by purpose.** The bank is consistent about which is which: "home shots are
locked and frontal; store inserts...", "the camera is static in creator scenes and steady in
outdoor macros", "mostly close handheld inserts", "camera stays low near the floor with natural
handheld micro-drift."

So: **the person talking is filmed locked. The demonstration is filmed handheld**, close, and
often from an awkward practical angle because that is where the problem is.

---

## THE HOOK, shot one

```
duration, banked:   median 1.60s, range 0.1 to 5.7   house rule: 1 to 2 seconds
under 2 seconds:    5 of 9
```

Three openers appear in the bank:

1. **The problem, live.** Children about to make a mess, a poolside about to go wrong.
2. **The product, extreme close-up.** One banked ad opens on a 0.1 second macro of the product
   pinched close to the lens. Another describes "an intentionally rapid macro hook" for the first
   two seconds before the pacing opens out.
3. **The product arriving.** A delivery box on a doorstep, the product in hand at a counter.

**The product is allowed in the first frame, and usually is.** What must not arrive early is the
CLAIM, not the object.

**The first words name the problem or the discovery.** "My girls absolutely love to paint and I
absolutely hate the mess", "I saw these at CVS the other week and I had to snag them", "Not to
be dramatic, but if you don't have one..."

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| CLOSE-UP PRODUCT | always | ~25% | short | voiceover |
| EXTREME CLOSE-UP, the problem area | always | ~12% | 0.1 to 3s | voiceover |
| MEDIUM CREATOR or TALKING HEAD | always | ~14% | short | on camera |
| THE PROBLEM HAPPENING, where it happens | always | ~12% | medium | voiceover |
| PRODUCT IN USE, solving it | always | ~15% | can run long | voiceover |
| B-ROLL of the setting | optional | ~8% | short | voiceover |

**PRODUCT IN USE.** The turn of the ad, and it is allowed to run longer than the shots around it.
The fix has to be watched, not asserted.

A conditional row is DROPPED when the ad does not do that thing. No row is added or renamed.

## WHAT USUALLY HAPPENS

The problem is shown happening, in the place it happens, close enough to be uncomfortable. The
product arrives, often already in frame from the start. It gets shown close, then used. The fix
is filmed in real time with hands doing recognisable work, and it is allowed the longest shot in
the ad. Then a short return to the creator or to the resolved state, and the ask.

---

## SOUND

```
Across the bank: 9 on-camera lines, 55 voiceover.
```

Six of seven spoken lines are VOICEOVER over the problem and the product. The creator talks
to camera at the open and close; the middle is narrated. Underneath: the real sound of the place,
which changes as the ad moves between locations. No music.

## RHYTHM

```
banked CV of shot lengths:   0.68          shortest 0.10s, longest 16.70s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.5 seconds and at least one runs over 5.0 seconds.
```

Uneven and shaped by the argument: quick cuts through the problem, then the solution shot
breathes. A tenth-of-a-second product flash and an eleven-second demonstration sit inside the
same ad.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
You decide which lines are spoken on camera and which are carried as voiceover over the problem and the product.
```
