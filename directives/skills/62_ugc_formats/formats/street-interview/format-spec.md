# Format spec, Street Interview

```
format_id:          ugc-street-interview
command:            /pm-ugc-street-interview
one_line:           Strangers in public, answering unscripted, with no stake in the answer.

duration_s:         22 to 30            # measured median 29.5
script_default:     required            # 10 of 10 banked ads speak; a vox pop with no answers is not one
wps:                3.44
word_budget:        93 to 119
words_per_sentence: 4 to 9              # measured, longest banked 37; short turns are real here

audio_treatment:    two-speaker-turns
delivery:           on-camera
on_camera_share:    100%                # the highest in the family
rig:                handheld            # 10 of 10; polish destroys this format
shots_per_10s:      4.7 to 5.6          # measured median (a FLOOR) to p75 (the target)

anchor_role:        interviewer, who recurs
voice_source:       voc-required
requires:           VOC document; product photo ONLY if the ad shows one, and 4 of 10 banked ads show none
funnel_role:        awareness, consideration
authenticity:       very high
generation_honesty: voc-sourced
```

## What this format is

An interviewer stops strangers and asks them something. It removes the doubt "does anyone outside
this brand actually think so", and it asks the viewer to trust apparent independence. That
borrowed impartiality is the whole mechanism, which is why polish kills it: a studio-clean vox pop
reads as staged, and staged independence is worth nothing.

## When it fits, and when it does not

```
fits:  the product benefits from sounding like consensus rather than a claim
not:   the product needs explaining     -> route to /pm-ugc-expert
       one committed advocate is enough -> route to /pm-ugc-testimonial
```

## Beat order

1. **Pattern interrupt.** The interviewer's question, landing before anything is explained. The ad
   always opens on the question, never on an answer.
2. **Intercept.** The approach, in public, visibly uncontrolled.
3. **Reactions.** Three to six respondents, each answering in their own register.
4. **Reveal.** The product or the price, at the moment interest peaks.
5. **Ask.** One action, and the ad ends on it. The ask may come from the interviewer OR from a
   respondent. A respondent recommending the product is the stronger version of this format's
   independence mechanism, since the ask then arrives from someone with no stake in it, but it
   is not mandatory.

**Further questions are optional.** After the opening question the interviewer MAY ask more, and
may equally ask none. A straight run of respondents all answering the one question is legitimate,
and so is a second question later, usually to set up the reveal or the ask. This is a per-ad
choice made from what the ad needs, not a rule.

**Respondent count: three to six.** What makes a higher count fit inside thirty seconds is SHORT
ANSWERS, not a low headcount, so the binding constraint is the word budget and not the number of
people. The research this format was specced from says four to eight, and its numbers could not
both hold, because it also set an eight-second minimum per person: four respondents at eight
seconds each is thirty-two seconds against a thirty-second cap. The eight-second minimum was the
broken part, not the headcount. This skill's own bank shows the same thing: pair 50 carries four
respondents inside 29.5 seconds, pairs 46 and 47 run a montage of several more, and pairs 43, 46,
48 and 50 each fit fifteen to eighteen dialogue turns inside 29.5 to 29.9 seconds by keeping every
answer to a few words.

## Hard rules

1. Every answer traces to the VOC: what real people actually said about this product or a
   comparable one. Wording may shift, substance is never invented.
2. Respondents differ from each other in age, register and appearance. Three variations of one
   person is one person.
3. The setting is public and visibly uncontrolled. No studio, no clean backdrop.
4. Handheld. A locked-off tripod reads as production.
5. The product appears at the reveal, not before. Early product turns strangers into salespeople.
6. The anchor locks the INTERVIEWER only. Respondents appear once each and are generated inside
   the render; do not build a still for a face that is never seen twice.

## Compliance flags

| Flag | Rule |
|---|---|
| Testimonial claims | respondent opinions are sourced from the VOC, never invented |
| Independence | the ad shows generated people. Their words are real customer sentiment, performed. Nothing may claim these are documented real interviews |

## Failure modes

1. **The scripted answer.** Too fluent, too on-message, and the independence evaporates.
2. **One person, three haircuts.** Respondents who are visibly the same casting.
3. **The clean location.** A background that looks arranged reads as arranged.
4. **The early product.** Shown before the reveal, and every answer after it sounds paid for.
5. **Answers written long for the headcount.** Six respondents given testimonial-length answers, so
   the ad overruns or the last people are cut off mid-sentence. The count is not the fault; the
   word budget is.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, rig, and the 100% on-camera share: measured from this skill's own
  ten banked ads, 2026-08.
- Respondent count, three to six, set 2026-08 from this skill's own bank rather than the source
  research, whose four-to-eight range shipped with an eight-second-per-person minimum that puts
  four respondents past the thirty-second cap. The bank shows headcount is not the constraint:
  pair 50 carries four respondents in 29.5 seconds, pairs 46 and 47 run a montage of several more
  without stating a number, and pairs 43, 46, 48 and 50 each fit fifteen to eighteen dialogue
  turns inside 29.5 to 29.9 seconds. Short answers are what buys the room.
- Independence as a distinct trust mechanism: source-credibility research.
