# Format spec, Educational and Tutorial

```
format_id:          ugc-tutorial
command:            /pm-ugc-tutorial
one_line:           Teach one outcome, step by step, with the product as the tool.

duration_s:         22 to 30            # measured median 30.0, the longest in the family
script_default:     default-voice       # a capability override, see below
wps:                3.71
word_budget:        92 to 129           # the largest budget in the family
words_per_sentence: 7 to 19             # measured, longest banked 31; 1 of 5 unpunctuated, excluded

audio_treatment:    vo-over-scenes
delivery:           voiceover
on_camera_share:    5%
rig:                mixed               # 95 static to 13 handheld; the steps are locked, the B-roll drifts
shots_per_10s:      4.7 to 5.9          # measured median (a FLOOR) to p75 (the target)

anchor_role:        character + product through the process
voice_source:       brand-led
requires:           product photo, a photo of every step state the ad shows
funnel_role:        consideration, retention
authenticity:       medium
generation_honesty: unconstrained
```

## What this format is

It teaches the viewer to achieve one specific outcome using the product. It removes the doubt
"could I actually do this", and it asks the viewer to trust demonstrated competence. It also buys
goodwill by giving something away before asking for anything.

**Why the voice default overrides the data.** Exactly 5 of 10 banked ads speak, a true coin flip.
But a wordless tutorial has to carry its steps with on-screen text, and no text is ever rendered
into these videos because generated text garbles. The silent variant depends on a capability the
renderer does not reliably have, so voice is the default. This is capability beating measurement,
recorded here so nobody 'corrects' it back.

## When it fits, and when it does not

```
fits:  there is a real outcome a viewer could reproduce
not:   nothing is teachable        -> route to /pm-ugc-problem-solution
       why it works is the story   -> route to /pm-ugc-expert
       the appeal is sensory       -> route to /pm-ugc-asmr
```

## Beat order

1. **Outcome promise.** What the viewer will be able to do, stated at the top.
2. **Starting point.** Where they begin, honestly.
3. **Steps.** In order, each one shown rather than described.
4. **Result.** The promised outcome, achieved on camera.
5. **Ask.** Soft, and the ad ends on it.

## Hard rules

1. The outcome is genuinely reproducible by a viewer with the product.
2. Steps run in order and every one is shown. A skipped step is a broken tutorial.
3. The result appears on camera. A promised outcome never shown fails the format.
4. The product is integral to the steps, not adjacent to them.
5. Show, do not tell. A narrated instruction over unrelated footage is not a demonstration.

## Compliance flags

| Flag | Rule |
|---|---|
| Proof | the outcome shown is the outcome the steps produce, unaccelerated and unfaked |
| Health | structure and function language only for ingestibles and topicals |

## Failure modes

1. **No achievable outcome.** It looks instructional and teaches nothing.
2. **Steps out of order.** The viewer cannot follow, and trust in the competence goes.
3. **The faked result.** An outcome the shown steps could not produce.
4. **Too many steps.** Thirty seconds fits three or four, not eight.
5. **Talking instead of showing.** The commonest failure, and the one the format exists to avoid.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, rig (re-measured 2026-08-23) and on-camera share: measured from this skill's own ten banked
  ads, 2026-08.
- Process demonstration beating outcome-only: Journal of the Academy of Marketing Science, 2023.
- The voice default: capability constraint of the renderer, documented above.
