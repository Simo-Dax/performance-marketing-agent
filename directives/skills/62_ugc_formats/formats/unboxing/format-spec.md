# Format spec, Unboxing

```
format_id:          ugc-unboxing
command:            /pm-ugc-unboxing
one_line:           Sealed to revealed, with the first reaction as the payoff.

duration_s:         16 to 25            # measured range 16.0 to 25.1, median 21.6
script_default:     default-sound       # 8 of 10 banked ads carry no dialogue
wps:                3.43
word_budget:        71 to 80
words_per_sentence: 16 to 22            # measured, longest banked 22; only 2 of 10 speak, so thin

audio_treatment:    sound-led
delivery:           voiceover
on_camera_share:    0%                  # no speaking face in any of the ten
rig:                static
shots_per_10s:      3.5 to 4.8          # measured median (a FLOOR) to p75 (the target)

anchor_role:        PLATE SET, see the anchor plates section below
voice_source:       brand-led
requires:           the container sealed, the container open, plus one in-use photo per product the ad opens or uses
funnel_role:        consideration
authenticity:       high
generation_honesty: unconstrained
```

## What this format is

The first physical encounter, from sealed container to reveal to first handling. The container is
either a BOX or a BRANDED BAG, and it holds one product or several. Several is the normal case:
five of the ten banked ads are multi-product hauls, and nearly every one has an outer shipping or
retail container around whatever is inside.
It removes the doubt "what is this actually like to own", and it asks the viewer to trust an
unmediated first reaction. The curiosity loop is the engine: something is hidden, then it is not.

## When it fits, and when it does not

```
fits:  the packaging is worth seeing and the product is worth revealing
not:   digital products and services, which have nothing to open
       the value is in using it       -> route to /pm-ugc-tutorial
       the texture is the story       -> route to /pm-ugc-asmr
```

## Beat order

1. **Sealed arrival.** The package, closed. The product is not visible and must not be.
2. **Anticipation.** Weight, size, handling. Buying the reveal a few seconds of tension.
3. **Opening.** The actual opening, with the sound it makes.
4. **Reveal.** The payoff. What is inside, seen properly for the first time. This beat gets the
   LONGEST hold in the ad.
5. **Handling.** Products out and shown FAST. With several in one container, each gets a beat of
   its own and the run through them is quick.
6. **Ask.** Soft, and the ad ends on it.

## Hard rules

1. The product is concealed at the start and never visible before the reveal beat.
2. The reveal is the payoff moment, not a step passed through.
3. Packaging sound is preserved. It is most of this format's sensory content.
4. A close-up follows the reveal. A product revealed and never examined wastes the reveal.
5. Nothing is swapped: the thing that comes out is the thing that went in.
6. **Quick front, quick handling, slow reveal.** The arrival and anticipation are brisk, the
   products come out and are shown fast, and the reveal beat itself still holds longest. These
   are not in tension: what must never be rushed is the single moment the container opens and its
   contents land. Everything around that moment moves.
7. Every product the ad opens or uses has its own in-use plate in the reference stack. A product
   the model has only seen sealed is a product whose interior it invents.

## The anchor plates

This format does NOT use a single anchor still. It declares a SET, because the ad has two visually
distinct phases and one still cannot hold both.

| Plate | Required | What it locks |
|---|---|---|
| 1. Container | always | the bag or box, sealed and unopened, in its setting |
| 2. Interior | always | the container open, showing what is inside |
| 3. In-use, one per product | conditional | a product the ad actually opens, applies or handles |

Plates 1 and 2 are always required. Plate 3 is per product and only for products the shot list
genuinely uses; an ad that never opens the serum needs no serum plate.

Each plate carries a named range of shots, and the render prompt says which. A run on 2026-08-20
did exactly this: the sealed plate carried shots 1 to 4, the open plate carried shots 5 to 9, and
two in-use plates covered a serum with its dropper drawn and a gloss with its wand out. Identity
held across all nine cuts on a single paid generation.

## Compliance flags

| Flag | Rule |
|---|---|
| Proof | this format proves ownership and packaging, nothing more. Efficacy claims belong elsewhere |

## Failure modes

1. **Revealed in the hook.** The product is shown up front and the whole loop collapses.
2. **The silent open.** No packaging sound, so the most tactile beat plays flat.
3. **The rushed reveal.** The payoff gets a second and lands on nobody. This is the one beat that
   is never hurried, and it does not contradict the quick handling around it: the front end and
   the product run are fast precisely so the reveal can be held.
4. **No handling.** The product appears and is never touched, which reads as a product shot.
5. **The invented interior.** The model has never seen the box open and guesses.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, words per sentence, rig, and the 0% speaking-face share: measured from
  this skill's own ten banked ads, 2026-08. The band was corrected from 18 to 27 down to 16 to 25
  on 2026-08-20: the ten measure 16.0 to 25.1, so the old band missed at both ends.
- Container is a box or branded bag holding one or more products: measured, 2026-08-20. Pair 22 is
  a branded tira shopping bag, and pairs 22, 26, 27, 28 and 29 are multi-product hauls.
- The plate set, and quick handling against a held reveal: house craft, adopted 2026-08-20 from a
  live two-product run that had to invent both because the spec did not support them.
- Beat order: house craft for this release.
