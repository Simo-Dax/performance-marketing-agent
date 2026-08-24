# Format spec, Problem and Solution

```
format_id:          ugc-problem-solution
command:            /pm-ugc-problem-solution
one_line:           Name a pain, show it failing, then show the product ending it.

duration_s:         20 to 27            # measured median 22.8
script_default:     default-voice       # 7 of 10 banked ads speak
wps:                3.28
word_budget:        59 to 96
words_per_sentence: 7 to 21             # measured, longest banked 25

audio_treatment:    vo-over-scenes
delivery:           voiceover
on_camera_share:    14%
rig:                mixed               # static in 5 of 10, the least settled rig in the family
shots_per_10s:      5.3 to 6.4          # measured median (a FLOOR) to p75 (the target)

anchor_role:        the product in the problem's context, plus the person ONLY when one recurs; 5 of 10 banked ads have no adult on camera
voice_source:       brand-led
requires:           product photo, photos of every product state the ad shows
funnel_role:        consideration, conversion
authenticity:       medium-high
generation_honesty: unconstrained
```

## What this format is

It names one specific pain, shows the status quo failing at it, and positions the product as the
direct cause of the fix. It removes the doubt "will this actually solve MY problem", and it asks
the viewer to trust a causal chain they watched happen.

Problem/Solution proves a CAUSE. Before/After proves a RESULT. That is the whole difference, and
it decides which one a brief belongs in.

## When it fits, and when it does not

```
fits:  the product solves one nameable, showable problem
not:   the problem is invisible and only the outcome shows -> route to /pm-ugc-before-after
       the value is in learning to use it                   -> route to /pm-ugc-tutorial
       there is no functional problem, only desire          -> route to /pm-ugc-pov
```

## Beat order

1. **Pain.** One problem, named and shown, before the product exists in the ad.
2. **Consequence.** What the pain costs. This is what makes the fix worth watching.
3. **Mechanism.** The product enters, and why it works rather than that it works.
4. **Demonstration.** It working, on camera. Not described, shown.
5. **Resolved state.** The pain visibly gone.
6. **Ask.** One action, and the ad ends on it.

## Hard rules

1. The PROBLEM lands before the product is positioned as its fix. This is about the argument's
   order, not the object's: the bank shows the product in hand from the first frame in most ads,
   often held to camera while the pain is being stated, and that is fine. What is not fine is
   presenting it as the solution to a problem the viewer has not yet felt.
2. ONE problem. A second problem halves the first one.
3. The demonstration happens on camera. A claimed fix is not this format.
4. The resolved state is SHOWN, not stated.
5. No staged failure of a named competitor or alternative.

## Compliance flags

| Flag | Rule |
|---|---|
| Proof | the demonstration must be of the real product doing the real thing |
| Health | structure and function language only for ingestibles and topicals |

## Failure modes

1. **The product arrives too early.** Tension never builds, so the fix lands on nobody.
2. **The vague problem.** "Feeling tired" is not a problem, it is a category.
3. **Two problems.** Attention splits and neither resolves.
4. **The told fix.** The ad says it works instead of showing it working.
5. **The staged failure.** Faking the alternative failing reads as dishonest and is.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, words per sentence, rig and on-camera share: measured from this
  skill's own ten banked ads, 2026-08.
- Process demonstration beating outcome-only on purchase intention: Journal of the Academy of
  Marketing Science, July 2023, five studies.
- Beat order: house craft for this release.
