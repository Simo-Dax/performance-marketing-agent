# Shot vocabulary, Testimonial

Measured from the ten banked testimonial ads in this skill's own bank, 2026-08: 106 shots, 43
distinct shot-type phrases clustered into six types.

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
FORMAT: TESTIMONIAL UGC

This kind of ad is simple. One person tells you what changed for her, like she is telling a
friend, and shows you the thing that changed it.

The rules:

1. One person. No interviewer, no second voice, no other hands.
2. She films herself on her own phone, in her own room.
3. She says what her life was like before. She admits it.
4. She gives one small detail only someone who really used it would know.
5. She never claims to be an expert.
6. One ask, at the end, and the ad stops there.
7. Never make her sound like an advert.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Her talking to camera. The bottle close to the lens. The dropper, the product on her fingers.
Her hands putting it on. The bottle held up beside her face. Her skin after. Use them however
you want. Two things hold: most of her talking shots are very short, and the ad keeps cutting
from her straight back to her at the same framing with her head jumped slightly, because the
pauses were cut out. That jump cut is what makes it look edited by a person.

The camera is still and at eye level. The crop changes between shots, never inside one.

HOW THEY PLAY IT
Talking to one person, not an audience. She hesitates, half-smiles, gestures small, and she
means it. Alive and warm in any shot her face is in.

TIMING
At least two shots run under half a second and at least one runs over five seconds. A
third-of-a-second cut and an eight-second talking shot belong in the same ad. Every shot change
is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## WHO IS ON SCREEN

**ONE PERSON, and she films herself.** No interviewer, no second speaker, no hands but hers.
Nine of ten banked ads carry a single woman in her late twenties to early thirties. One carries
no face at all, only hands and forearms applying the product outdoors, which is a legitimate
version of the format.

**She is not made up for a shoot.** The bank runs minimal makeup or none, and one prompt insists
"skin remains realistic with ordinary pores." Where makeup exists it is everyday makeup, not a
beauty campaign face.

**Her clothes are what someone owns.** T-shirts, sleeveless tops, a knit jumper, a camisole, a
bathrobe. Nothing styled, nothing new, nothing that reads as wardrobe.

## WHAT IS ALWAYS IN FRAME

- Her, chest-up, close to the phone
- The product, entering and leaving her hands repeatedly through the ad, label facing the lens
  whenever it is held
- An ordinary room behind her, soft and secondary and slightly out of focus. Bedrooms and
  bathrooms dominate the bank; the background is never the point and is never decorated for the
  shot

## HOW THE CAMERA BEHAVES

**Locked and static, at eye level.** Every banked ad describes static phone framing, and one
says "locked phone at eye level, no cinematic depth blur or stylized movement." The phone is
propped or held still and it does not drift, pan or push in. This is the opposite of the street
interview format and it is not interchangeable.

**The crop changes between shots, never during them.** The framing jumps from chest-up to a
tight product macro to hands on a face and back, and each of those holds its own position
absolutely still while it runs.

## THE FRAMING CYCLE

```
TALKING HEAD       chest-up, straight to the lens                  four in ten shots
JUMP CUT           same framing, her position jumps slightly       the format's most common move
PRODUCT MACRO      the container close to the lens, label forward
DISPENSE           the pump, the dropper, product on fingertips
APPLICATION        hands to face or body, product going on
PRODUCT BY FACE    the container raised beside her head
```

The ad lives in the talking head and leaves it in short runs of B-roll, then comes straight
back. It does not tour a house and it does not change location for variety.

---

## THE HOOK, shot one

```
duration, banked:   median 2.50s, range 0.7 to 24.5   house rule overrides: 1 to 2 seconds
opens on:           a talking head in 8 of 10
first frame holds:  the product or the visible RESULT in 7 of 10
```

**The house rule is deliberately tighter than the bank.** Banked hooks run a median of 2.50
seconds and only 3 of 10 come in under 2. The rule is 1 to 2 seconds anyway, because a slow open
loses viewers who would have stayed. Doctrine, not measurement, and written here as doctrine so
nobody re-derives it from the bank and softens it.

**Something physically happens in it.** In the bank she flips her hair, drinks the product,
presents it toward the lens, touches her own face, or is already mid-gesture. Not one banked
hook is a person sitting still beginning a sentence.

**The picture and the words carry different jobs.** The spoken hook may be the confession the
format opens on. The VISUAL hook is the product or the result, in frame from the first moment.
Seven of ten do exactly that while saying something else entirely.

**The first words are a promise, a claim or news.** Never a slow wind-up.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| TALKING HEAD | always | ~40% | mostly under 2s, many 0.3 to 0.5 | on camera |
| JUMP CUT on the talking head | always | see below | 0.3 to 0.5s | on camera |
| PRODUCT MACRO | always | ~9% | 0.4 to 2.2s, usually under 1 | voiceover |
| DISPENSE AND TEXTURE | when the product is poured, pumped or dropped | ~7% | about 1.3s | voiceover |
| APPLICATION | when the product goes onto a body | ~11% | 0.2 to 5.6s | voiceover |
| PRODUCT BY FACE | optional | ~5% | about 1.7s | on camera |
| RESULT SHOT, the changed state | when the ad shows a visible result | ~11% | short to medium | either |

**JUMP CUT ON THE TALKING HEAD.** The most common move in the entire format: talking head
straight into talking head at the same framing, her head and hands jumping position, because the
pauses and breaths between sentences were cut out. It is 29 of the bank's transitions, more than
every other transition combined. Twenty-four of the bank's thirty-nine talking heads run under
two seconds for this reason. It is what makes an ad read as edited by a person rather than
filmed in one take, and it is the single thing a generated testimonial most often lacks.

**RESULT SHOT.** Twelve banked shots are typed as a reveal, a result or a finished state: the
styled hair turned to the lens, the finished face, the skin after. Where the product produces
something a viewer can SEE, the ad shows it plainly near the end, and often flashes it early as
the hook too.

**APPLICATION.** Arrives in runs of two or three back to back, almost never as a single shot,
and often broken by micro cuts of a fraction of a second as her hands shift position.

A conditional row is DROPPED when the product does not support it. No row is added or renamed.

## WHAT USUALLY HAPPENS

She talks, and the edit keeps cutting her off and rejoining her. Somewhere in the first half the
product arrives in her hands, gets shown close, gets opened, gets used on her, and the ad
returns to her face. She addresses one person, not an audience. She hesitates, half-smiles,
gestures small. Toward the end the framing settles and the shots get slightly longer. She ends
on the ask, looking at the lens.

---

## SOUND

```
Across the bank: 34 on-camera lines, 43 voiceover.
```

Her voice throughout, and only hers. She speaks ON CAMERA in the talking heads and PRODUCT BY
FACE shots, and her voice carries as VOICEOVER over the macros, the dispensing and the
application. Under it is quiet indoor room tone. No music anywhere.

## RHYTHM

```
banked CV of shot lengths:   0.77          shortest 0.10s, longest 24.50s, ratio 245x
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.3 seconds and at least one runs over 5.6 seconds.
```

The most uneven format in the family. Real testimonials hold a third-of-a-second jump cut and an
eight-second talking shot inside the same ad. A shot list where every span sits within a second
of the mean has failed even when the count is right, and it is the clearest tell that an ad was
generated rather than edited.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut. Anything else is an
effect the user adds in their editor afterwards.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
You decide which lines she speaks on camera and which are carried as voiceover over the product and application shots.
```
