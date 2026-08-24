# Format spec, Expert and Authority

```
format_id:          ugc-expert
command:            /pm-ugc-expert
one_line:           Someone knowledgeable explains why it works, not that it works.

duration_s:         22 to 30            # measured median 29.9
script_default:     default-voice       # 7 of 10 banked ads speak
wps:                3.37
word_budget:        91 to 102
words_per_sentence: 7 to 17             # measured, longest banked 54; the range is the point, not the mean

audio_treatment:    sync-to-camera
delivery:           on-camera
on_camera_share:    92%
rig:                static              # 68 of 68 banked Shot Type lines are static; four prompts rule handheld out by name
shots_per_10s:      2.0 to 2.8          # measured median (a FLOOR) to p75 (the target)

anchor_role:        expert + product
voice_source:       voc-required
requires:           VOC document, product photo
funnel_role:        consideration, conversion
authenticity:       medium              # polish HELPS here, the inverse of street interview
generation_honesty: voc-sourced
```

## What this format is

A knowledgeable person explains the mechanism. It removes the doubt "why would this work", and it
asks the viewer to trust competence rather than experience. Source-credibility research treats
expertise and trustworthiness as genuinely separate dimensions, which is why this is not a
Testimonial variant: a peer says it worked for them, an authority says why it works at all.

**Fourteen words a line, four lines an ad.** The longest sentences and the fewest of them in the
whole family. An authority speaks in complete thoughts and does not get cut off, and that rhythm
carries more of the format than the word count does.

## When it fits, and when it does not

```
fits:  there is a real mechanism worth explaining
not:   the speaker is talking about their own use -> route to /pm-ugc-testimonial
       the value is in the steps                  -> route to /pm-ugc-tutorial
```

## Beat order

1. **Standing.** Why this person is worth listening to, established early.
2. **The myth or the problem.** What most people get wrong.
3. **Mechanism.** Why the product works, in plain terms.
4. **Evidence.** What supports it.
5. **Recommendation.** Bounded to what they actually know.
6. **Ask.** One action, and the ad ends on it.

## Hard rules

**Read the bank knowing this one rule diverges from it, on purpose.** Five of the ten banked ads
are built on a stated credential: dermatologist, trichologist, dermatology. Those are real people
with real licences. Yours is generated, so the credential is the single thing that cannot carry
across. Take everything else from them, the register, the pacing, the long complete sentences,
the mechanism-first structure, and leave the title behind.

1. **No licensed title is ever claimed.** The speaker is generated. They speak as experienced and
   knowledgeable and never say dermatologist, doctor, MD, nurse, pharmacist, CFP or any other
   credential, unless the user supplies a real credentialed person. This is not a style note.
2. Every claim traces to the VOC or the Brand DNA. Substance is never invented.
3. Claims stay inside what the speaker could plausibly know.
4. The mechanism is actually explained. An authority who only asserts is a testimonial with a
   costume.
5. **No humour.** Humour measurably reduces source credibility, which is the only currency this
   format has.

## Compliance flags

| Flag | Rule |
|---|---|
| Credential | no licensed title spoken or shown without a real credentialed person supplied by the user |
| Health | structure and function language only, no diagnosis, no treatment claims |
| Proof | every stated fact traces to a sanctioned source under the claims law C.1 |

## Failure modes

1. **The costume expert.** A lab coat and no mechanism.
2. **The claimed license.** A generated person saying "as a dermatologist", which is the failure
   with actual consequences.
3. **Out-of-domain claims.** Authority in one area spent on another.
4. **Jargon.** Precision that stops communicating.
5. **A joke.** One line of humour and the credibility this format runs on is gone.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, sentence length and on-camera share: measured from this
  skill's own ten banked ads, 2026-08.
- Expertise and trustworthiness as separate dimensions: Hovland and Weiss 1951; Pornpitakpan 2004.
- Humour reducing source credibility: Eisend meta-analysis, Journal of the Academy of Marketing
  Science 2009, 369 correlations.
