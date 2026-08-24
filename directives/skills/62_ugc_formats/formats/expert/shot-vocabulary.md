# Shot vocabulary, Expert and Authority

Measured from the ten banked expert ads in this skill's own bank, 2026-08: 68 shots, 6.8 shots per ad. The second-fewest shots in the family, after POV at 5.8.

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
FORMAT: EXPERT UGC

This kind of ad is simple. One person who knows what they are talking about explains why the
product works, holding it while they talk.

The rules:

1. One person, talking to camera, from the first shot to the last.
2. The product is already in their hands when the ad starts.
3. Explain WHY it works. Never just say that it works.
4. Let them finish a thought. Long shots are correct here.
5. Almost never cut away. Whatever they show, they show in their own frame.
6. Raise the product up beside their head when it matters.
7. End on what they would tell you to do, in the framing they started in.

THE HOOK
Shot 1, 1 to 2 seconds. Make it stop the scroll. A lot should happen in it.

THE SHOTS THIS FORMAT USUALLY USES
Them chest-up talking to camera. A wider shot of the same person. The product raised
beside their head. Them showing the thing they are explaining, on themselves. Use them however
you want. Two things hold: this format barely cuts and a single shot running twenty seconds is
right rather than lazy; and the product enters the ad by being lifted into their frame, never as
a separate close-up of the bottle on its own.

The camera never moves. Every change of size or pose comes from a cut.

HOW THEY PLAY IT
Calm, certain, and interested in what he is telling you. Someone who knows the answer and is
glad to explain it, never someone performing expertise.

TIMING
At least two shots run under one second and at least one runs over ten seconds. A few long
explaining holds with short shots between them. Every shot change is a hard cut or a jump cut.
<!-- PROMPT-BLOCK-END -->

---

## THE MEASUREMENTS, engine-facing, never pasted


## WHO IS ON SCREEN

**ONE PERSON, explaining.** Four of the ten banked ads put the speaker in medical scrubs and
several film in clinical rooms with real equipment: an examination chair, a dermatoscope, a
cryotherapy canister. One sits the speaker behind a large foam-covered microphone.

**A HARD LIMIT ON THAT LOOK, and it is a compliance rule rather than a style note.** Those banked
creators are real licensed professionals. A generated one is not. This format's own spec states
it plainly: no licensed title may be spoken OR SHOWN without a real credentialed person supplied
by the user, and its first failure mode is "the costume expert: a lab coat and no mechanism."

So:

- **With a real credentialed person supplied by the user**, the professional setting and their
  actual uniform are correct and are what the bank shows.
- **Without one**, the ad renders NO scrubs, NO lab coat, NO clinical room and NO medical
  equipment. Authority then comes only from the MECHANISM being explained clearly, which is what
  the format actually sells. A costume that implies a licence nobody holds is the failure this
  format was built to avoid.

**They are groomed but not styled.** Natural makeup, hair worn normally, short natural nails. The
authority comes from competence, not from polish.

## WHAT IS ALWAYS IN FRAME

- The speaker, chest-up, square to the lens, from the first frame to the last
- The product, usually already in their hands at the open, held label-forward while they talk
- A plain consistent background that does not change: one wall, one door, one room
- Enough of the setting to read the credential without anyone announcing it

## HOW THE CAMERA BEHAVES

**Locked, and it never moves.** One banked prompt states the rule for the whole format: "every
shot is static; all changes in scale and pose come from cuts." Another: "locked phone and fixed
background; all shots static."

**The light is soft, even and frontal**, with minimal shadow. This format is the least
photographically interesting in the family on purpose. Nothing about the picture should compete
with what is being explained.

---

## THIS FORMAT BARELY CUTS

```
6.8 shots per ad          the family average is 11 to 19
longest banked shot       27.1 seconds
on-camera 26  :  voiceover 2
```

Expert is a talking format and almost nothing else. There is no B-roll run, no montage, almost
no cutaway. The bank holds a two-shot ad averaging fifteen seconds a shot and a nineteen-shot ad
averaging 1.6, and both are correct: what is not correct is chopping the explanation into evenly
spaced fragments, which reads as an edit covering for a speaker who never said anything.

Nearly every line is spoken ON CAMERA by the person in frame.

---

## THE HOOK, shot one

```
duration, banked:   median 3.40s, range 1.1 to 19.0
under 2 seconds:    1 of 10   <-- the bank strongly disagrees with a fast hook here
```

**A conflict worth knowing about.** The house rule across every format is a hook under 2
seconds. This bank is the one place that rule fights the evidence: banked expert hooks run a
median of 3.40 seconds and one opener holds for 19. The reason is structural, because the hook
here is a CREDENTIAL plus a TOPIC and both have to land before anything else can.

Keep the hook as short as the credential allows and no shorter. Do not cut the credential to hit
a number.

**What the hook contains.** Who is speaking and what is about to be explained: "As a
dermatologist, I've been getting a lot of questions about red light", "I'm a dermatologist. Of
course I always have one of these in my hand", "Today, we're going to talk about skin care for
teens, acne edition." The product is usually already in shot.

---

## THE SHOT TYPES

| Shot type | Required | Share | Duration | Who speaks |
|---|---|---|---|---|
| MEDIUM CLOSE-UP, chest-up to camera | always | ~50% | 3 to 27s | on camera |
| MEDIUM, seated or standing wider | always | ~22% | long | on camera |
| PRODUCT AND FACE, held beside the head | always | ~9% | medium | on camera |
| DEMONSTRATION, showing what is explained | when there is something to show | ~7% | medium | on camera |
| EXTREME CLOSE-UP, the area under discussion | optional | small | short | either |

**PRODUCT AND FACE.** The product raised into frame beside their head, label forward, while they
keep talking. This is how a product enters an expert ad, not as a separate studio macro.

**DEMONSTRATION.** Lifting a section of hair, indicating a spot on skin, showing an applicator or
a device. The hands stay in the same frame as the face; the ad does not cut away to them.

A conditional row is DROPPED when there is nothing to demonstrate. No row is added or renamed.

## WHAT USUALLY HAPPENS

They state who they are and what they are about to explain, with the product already in hand.
Then they explain the MECHANISM: why this works, what is actually happening, what most people
get wrong. They hold shots while they do it. The product is raised into frame when it becomes
relevant rather than being cut to. They may demonstrate on themselves. They end on a
recommendation delivered in the same framing they started in.

---

## SOUND

One voice, on camera, continuous. Quiet room tone underneath: a clinical room, an office, a
bathroom. No music anywhere.

## RHYTHM

```
banked CV of shot lengths:   0.46          shortest 0.10s, longest 27.10s
```

**Stated as counts in the prompt, because "make it uneven" does not land.** A live run
asked for uneven shots in prose and returned every shot within a second of the mean. Say this
instead:

```
At least two shots run under 0.8 seconds and at least one runs over 10.5 seconds.
```

Uneven in a particular way: a few very long explanatory holds with short shots between them.
This is the one format where a single shot running twenty seconds is correct rather than lazy.

## NEVER RENDERED

**Transitions are post-production, not generation.** No dissolves, fades, wipes, whip pans, zoom
transitions or speed ramps. Every shot change is a hard cut or a jump cut.

## DELIVERY LINE, pasted into the render prompt

This is the last line of the video engine's V.4a pacing block. It replaces the generic one,
because this format does not offer a free choice:

```
Every line is spoken ON CAMERA by the person in frame, including the lines said while the product is raised into shot.
```
