# Format spec, Before and After

```
format_id:          ugc-before-after
command:            /pm-ugc-before-after
one_line:           Two states of the same thing, compared honestly, so the change speaks.

duration_s:         15 to 24            # measured median 23.2
script_default:     default-sound       # 8 of 10 banked ads carry no dialogue
wps:                4.15                # the densest talker in the family, when it talks
word_budget:        91 to 100
words_per_sentence: 9 to 19             # measured, longest banked 41; only 2 of 10 speak, so thin

audio_treatment:    sound-led
delivery:           voiceover
on_camera_share:    31%
rig:                static              # 9 of 10, and the comparison depends on it
shots_per_10s:      4.9 to 7.3          # measured median (a FLOOR) to p75 (the target)

anchor_role:        the thing that CHANGES, in its starting state, plus the product; the person only when they recur
voice_source:       brand-led
requires:           product photo, a real before state, a real after state
funnel_role:        consideration, conversion
authenticity:       high
generation_honesty: unconstrained
```

## What this format is

An earlier state and a later state of the same subject, framed so the viewer can compare them.
It removes the doubt "does this actually work", and it asks the viewer to trust the comparison
itself. The comparison geometry IS the format: same angle, same light, same framing. Change any
of those and the ad is proving the lighting, not the product.

## When it fits, and when it does not

```
fits:  the change is visible, and the product plausibly caused it in the time claimed
not:   the change is instant                    -> progression detail backfires, route to /pm-ugc-problem-solution
       nothing visible changes                  -> route to /pm-ugc-testimonial
       the mechanism is the interesting part     -> route to /pm-ugc-expert
```

**Platform warning, given once before building.** Meta restricts before-and-after imagery in
weight loss, health and beauty. This is the one format in the family that risks an account
restriction rather than a weak ad. Say so plainly, name the category, and continue only if the
user decides to.

## Beat order

1. **Result tease.** The change, glimpsed, so the viewer knows what they are waiting for.
2. **Baseline.** The honest before, under the conditions the after will repeat.
3. **Treatment.** The product being used, which is what connects the two states.
4. **After.** The later state. When the ad claims a result, match the baseline's angle, light and
   framing exactly. When it shows a process, land the finished state the way the bank does.
5. **Ask.** One action, and the ad ends on it.

## Hard rules

1. **When the ad makes a RESULTS CLAIM** (skin, teeth, hair condition, body, cleaning), the before
   and after share angle, distance, lighting and framing, and nothing else changes between them.
   That matching is what makes the claim provable, and it is what protects the user.
2. **When the ad is a PROCESS transformation** (styling, application, assembly, a makeover), the
   bank's own pattern governs instead: none of the ten banked ads uses matched-pair framing, and
   one moves between two rooms entirely. Follow the process, and do not fake a forensic comparison
   the ad is not making.
3. Elapsed time is stated honestly whenever it matters to the claim.
4. The product appears in the treatment beat, not only at the end.
5. No digital alteration of either state.

## Compliance flags

| Flag | Rule |
|---|---|
| Platform policy | Meta restricts before-and-after in weight loss, health and beauty. Warn, name it, proceed only on the user's word |
| Proof | a change explained by lighting, angle, styling or retouching is not proof and does not ship |
| Health | structure and function language only |

## Failure modes

1. **The lighting did it.** The after is brighter, and everyone can tell.
2. **The staged before.** A deliberately worse baseline, which reads instantly and poisons the ad.
3. **The implausible window.** A timeframe the category cannot support.
4. **The hidden change.** New makeup or a new top in the after, so the comparison proves nothing.
5. **No product in the middle.** Two states and no visible cause connecting them.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, rig, on-camera share and the 8-of-10 silence: measured from this
  skill's own ten banked ads, 2026-08.
- Progression beating two-state comparison under skepticism, and backfiring where instant results
  are expected: Cian, Longoni and Krishna, Journal of Marketing Research 2020, 57(3).
- Platform restriction: Meta advertising policy on before-and-after imagery.
