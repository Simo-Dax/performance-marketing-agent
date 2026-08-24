# Format spec, Green Screen Reaction

```
format_id:          ugc-green-screen
command:            /pm-ugc-green-screen
one_line:           A creator reacting to something, filmed clean so the something can be added later.

duration_s:         20 to 30            # measured median 29.6, above the source research's stated band
script_default:     required            # 10 of 10 banked ads speak; a silent reaction is not one
wps:                3.12
word_budget:        80 to 114
words_per_sentence: 8 to 16             # measured, longest banked 44

audio_treatment:    sync-to-camera
delivery:           on-camera
on_camera_share:    95%
rig:                static              # 84 of 84 banked Shot Type lines are static; a drifting plate cannot be keyed
shots_per_10s:      3.0 to 3.7          # measured median (a FLOOR) to p75 (the target)

anchor_role:        the creator only
voice_source:       brand-led
requires:           nothing beyond the creator; product photo ONLY if the ad holds one, and 8 of 10 banked ads hold none
funnel_role:        consideration, conversion
authenticity:       medium-high
generation_honesty: unconstrained
```

## What this format is

A creator talks to camera about external evidence: a review, a screenshot, an article, a chart.
It removes the doubt "does anything outside this ad back the claim", and it asks the viewer to
trust third-party evidence plus the creator's reading of it.

**This skill produces the FOOTAGE ONLY.** It does not remove the background, does not source or
generate the evidence, and never fabricates a screenshot or a review. It renders a person talking
in a clean, keyable environment, and hands over a timed note saying what belongs behind them and
when. The user does the composite in their editor.

That is also what resolves the format's honesty problem: nothing is fabricated because nothing is
generated except the person.

## When it fits, and when it does not

```
fits:  the user HAS real evidence worth showing behind a creator
not:   there is no showable evidence   -> route to /pm-ugc-testimonial
       the product is tactile          -> route to /pm-ugc-asmr
```

## Beat order

1. **The claim.** What the creator is reacting to, stated so it makes sense with or without a
   visual behind them.
2. **The reaction.** Their honest read of it.
3. **The walkthrough.** Talking through the substance, point by point.
4. **The product tie.** Why any of it matters for this product.
5. **Ask.** One action, and the ad ends on it.

Every beat has to play as a complete piece of footage on its own, because the background may not
be there when it is watched.

## Hard rules

1. **The creator is centered** in frame, so the user can key the background out and reposition
   them anywhere on the canvas afterwards.
2. **The environment is clean and keyable**: even light, uncluttered, clear separation between
   subject and background, no busy patterns and nothing behind them that reads as intentional.
3. **Gestures stay generic and body-centred.** Never point at a specific spot on screen. The
   thing being pointed at may not exist yet, and may end up somewhere else entirely.
4. **The footage works uncomposited.** A person talking in a room, watchable as-is.
5. **No evidence is generated, ever.** No screenshots, no review cards, no charts, no article
   headlines. Not in the render, not as a reference.
6. The spoken lines never describe something on screen that the render does not contain.
7. **Never write the background into the prompt.** Not the screenshot, not the dashboard, not the
   article, not "behind her". Anything described behind the creator gets RENDERED behind them,
   which makes the footage un-keyable and destroys the only thing this skill produces.

**How to read this bank, and it is the opposite of every other format.** All ten banked ads are
FINISHED composites: they describe the screens, dashboards, reviews and web pages sitting behind
the creator, because that is what the viewer saw. Read those passages as a record of what the
MEMBER will composite later, never as prompt material. What you take from this bank is the
creator: their delivery, their framing, their gestures, the room. What you leave is everything
behind them, which goes into the delivery note with timecodes instead.

## Compliance flags

| Flag | Rule |
|---|---|
| Evidence | the skill never creates evidence. Whatever the user composites is theirs, and its accuracy is theirs |
| Proof | every claim spoken traces to a sanctioned source under the claims law C.1 |

## Failure modes

1. **Pointing at nothing.** The creator gestures at a spot, and the composite lands elsewhere.
2. **The busy room.** A background nobody can key cleanly, which makes the footage unusable.
3. **Language that assumes the visual.** "As you can see here" over a frame with nothing in it.
4. **Off-centre framing.** Cannot be repositioned freely once keyed.
5. **Generated evidence.** The one failure with real consequences, and the reason rule 5 exists.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, words per sentence, rig (re-measured 2026-08-23) and the 95% on-camera share: measured from this
  skill's own ten banked ads, 2026-08. The measured median of 29.6s sits above the source
  research's stated 18 to 28 band, so the measurement wins.
- Footage-only scope, centered framing and the composite handover: user decision, 2026-08.
