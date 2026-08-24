# Shot vocabulary, Street Interview

Measured from the ten banked street interview ads in this skill's own bank, 2026-08: 125 shots,
12.5 shots per ad.

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
FORMAT: STREET INTERVIEW UGC

This kind of ad is simple. Someone stands in the street with a microphone, asks strangers a
question, and you watch them answer.

The rules:

1. The interviewer holds a black handheld microphone the whole time.
2. Every word is spoken on camera by someone you can see. Never a narrator.
3. The strangers come one at a time. Never a group.
4. Each stranger answers once and is never seen again.
5. Film it outside, in a real public place, with people walking past.
6. Let the answers be messy. Nobody is word-perfect.
7. Open on the question. No introduction, no explaining what is being filmed.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
The interviewer and the stranger together with the mic between them. Just the stranger
answering. Just the interviewer asking. The product in someone's hand. Use them however you
want. Two things hold: the shot with both of them in it is where the ad lives and it is used
more than any other, and a good answer is allowed to run for ten seconds while a weak one is cut
to almost nothing.

A third person films the pair on a phone, so the frame drifts. There is no tripod anywhere.

HOW THEY PLAY IT
Real and unrehearsed. People smile, hesitate, look away, say something unexpected. Nobody is
word-perfect and nobody is performing.

TIMING
At least two shots run under half a second and at least one runs over five seconds. Evenly
spaced shots are the clearest sign the footage was made up. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## WHO IS ON SCREEN

**THE INTERVIEWER.** The only person who recurs, present in almost every shot. They hold a
**black handheld microphone** in 9 of 10 banked ads, and in one the mic carries a small branded
flag on it. That mic is the single most repeated object in the format and it is what identifies
the ad as a street interview in the first frame. The interviewer asks, reacts, and closes.

**THE RESPONDENTS.** Strangers who appear ONE AT A TIME and never return. The bank runs from one
respondent to four or more; where there are several they arrive **sequentially**, each answering
and giving way to the next, never as a group. They are generated inside the render and none of
them gets an anchor still.

**A THIRD PERSON HOLDS THE CAMERA.** Not a tripod and not a selfie. Someone is standing there
filming the pair on a phone, which is why the frame drifts.

**Anyone else on screen is a real passer-by**, not a cast user.

## WHAT IS ALWAYS IN FRAME

- The microphone, held by the interviewer, moving toward whoever is speaking
- A real public place behind the pair, with people walking through it while the take runs
- Ordinary outdoor clothing appropriate to the actual weather, including coats and beanies when
  it is cold. Nobody is dressed for a shoot
- A product only when the ad has one. Four of the ten banked ads show no product at all, and
  their prompts say so explicitly rather than inventing one

## HOW THE CAMERA BEHAVES

**Handheld, always.** Every banked ad describes phone drift, mild handheld movement, or quick
handheld reframes. There is no static tripod framing anywhere in this format, and a locked-off
camera is the fastest way to make a street interview read as staged.

**The crop changes between takes rather than the camera moving during them.** The operator
recrops between answers: in tighter on a good line, wider when both people are reacting.

## THE FRAMING CYCLE

The format cycles three positions and this cycling IS the edit:

```
TWO-SHOT           both people in frame, mic between them        the home position, over half of all shots
RESPONDENT SINGLE  cut in on the person answering
INTERVIEWER SINGLE the ask, the reaction, or the closing line
```

The ad moves between these continuously while the location stays the same. Both people are NOT
always visible; the two-shot is where it lives, and it cuts to singles for the answers that
land and for the follow-up questions.

---

## THE HOOK, shot one

```
duration, banked:   median 2.45s, range 0.1 to 4.8   house rule: 1 to 2 seconds
what it is:         the interviewer ASKING, mic already extended
first words:        a question, in 9 of 10
```

The hook is the question, straight in, with no introduction and no explanation of what is being
filmed. Banked openers: "Do you struggle with food cravings?", "If you could change one thing
about college, what would it be?", "Have you ever seen a wallet that can hold your Zyns?"

The mic is already moving toward the stranger as the question lands.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| TWO-SHOT, interviewer and respondent | always | ~55% | 0.1 to 12.4s | either, on camera |
| RESPONDENT SINGLE | always | ~15% | short | the respondent, on camera |
| INTERVIEWER SINGLE | always | ~10% | short | the interviewer, on camera |
| PRODUCT IN HAND | when the ad has a product | small | short | whoever holds it, on camera |

**PRODUCT IN HAND.** Held by the interviewer or handed to a respondent, and it stays in a human
hand. This format has almost no cutaways to an object sitting on its own, and no studio macros.

A conditional row is DROPPED when the ad does not have one. No row is added or renamed.

## WHAT USUALLY HAPPENS

The interviewer asks. A stranger answers in their own words, often badly, often with a laugh or
a pause. A follow-up may come. Another stranger takes their place. Answers are short and
overlapping and nobody is word-perfect. Reactions are real: people smile, hesitate, look away,
say something unexpected. If a product exists it arrives late, handed over or held up, and the
ad closes on an ask that may come from the interviewer or from a respondent.

---

## SOUND

Every line is spoken ON CAMERA by someone visible in frame.

```
Across the bank: 122 on-camera lines, 0 voiceover.
```

There is no narrator in this format and nobody ever speaks over pictures. Under every line is
the real ambience of wherever this is: traffic, crowd noise, wind, surf, campus chatter. It
changes with the location and it never stops. No music anywhere.

## RHYTHM

```
banked CV of shot lengths:   0.69          shortest 0.10s, longest 12.40s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.7 seconds and at least one runs over 4.8 seconds.
```

Wildly uneven, for a reason particular to this format: a good answer is allowed to run for ten
seconds and a weak one is cut to a fraction of a second. The unevenness is the edit deciding
what was worth keeping, and evenly spaced shots are the clearest tell that the footage was
generated rather than found.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
Every line is spoken ON CAMERA by someone visible in frame. This format has no narrator; a line that cannot be said by a person in shot does not belong in it.
```
