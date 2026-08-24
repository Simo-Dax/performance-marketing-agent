# Format spec, Testimonial

```
format_id:          ugc-testimonial
command:            /pm-ugc-testimonial
one_line:           A real customer says what changed, in their own words, to camera.

duration_s:         20 to 30            # measured median 25.2
script_default:     default-voice       # 8 of 10 banked ads speak
wps:                3.9                 # measured, on ads that speak
word_budget:        79 to 102           # measured p25 to p75 at 25s
words_per_sentence: 7 to 19             # measured, longest banked 43

audio_treatment:    sync-to-camera
delivery:           on-camera
on_camera_share:    44%
rig:                static              # 10 of 10 banked ads
shots_per_10s:      3.7 to 6.8          # measured median (a FLOOR) to p75 (the target)

anchor_role:        character + product
voice_source:       voc-required
requires:           VOC document, product photo
funnel_role:        consideration, conversion
authenticity:       high
generation_honesty: voc-sourced
```

## What this format is

One person tells you what changed for them. It removes the doubt "did this work for someone like
me", and it asks you to trust a peer's lived experience rather than a demonstration or a
credential. That is why it is not an Expert ad and not a Before/After: nothing is proven on
screen, someone is simply believed.

Polish is the enemy here. A testimonial that sounds produced triggers the reflex that recognises
an ad, and the trust it was carrying goes with it.

## When it fits, and when it does not

```
fits:  the VOC carries real customer language and one believable, specific result
not:   no VOC document on file        -> stop, run /voc first, do not invent a customer
       the result has to be SEEN      -> route to /pm-ugc-before-after
       the mechanism needs explaining -> route to /pm-ugc-expert
       the speaker would cite a credential -> route to /pm-ugc-expert
```

## Beat order

1. **Admission.** The old state, said as a confession rather than a complaint. Earns the next
   three seconds.
2. **Turn.** The moment something changed and what caused it. This is where the product gets
   CREDITED; it may have been in her hands from the first frame, and in half the bank it is.
3. **Specific.** ONE concrete detail only a real user would say. This beat carries the whole ad.
4. **Verdict.** What they would tell someone still in their old position.
5. **Ask.** One action, and the ad ends on it.

The Specific beat is the format. Without it this is an endorsement, and viewers discount
endorsements automatically.

## Hard rules

1. Every substantive line traces to the VOC. Wording may be adjusted, substance is never invented.
2. The Specific beat carries a detail traceable to a named VOC line, and the skill says which at
   gate 1.
3. The TURN is where the story turns, not where the object is allowed on screen. Half the banked
   ads open with the product already in hand, and that is proven; what must not arrive early is
   the claim. Hold it, show it, but do not credit it before the admission has landed.
4. Exactly one ask, and the ad ends on it.
5. The speaker never claims expertise, a credential, or knowledge beyond their own use.
6. The speaker addresses the viewer, never the brand.
7. Nothing framed as a quotation is reworded. A spoken line is a performance and may be; a line
   shown or introduced as a real review is customer language under the claims law C.4 and stays
   verbatim with its ref.

## Compliance flags

| Flag | Rule |
|---|---|
| Testimonial claims | every result stated is sourced, with typicality context where the niche requires it |
| Health | structure and function language only for ingestibles and topicals, never cure or treat |
| Earnings | for coaching and info offers, no stated or implied income without written substantiation |

## Failure modes

1. **The brochure.** Every line accurate, nobody would say any of them. Cause: writing benefits
   instead of mining the VOC for how a person actually talks.
2. **The endorsement.** Warm, positive, no Specific beat. Cause: the specific detail was cut for
   time. Cut the Verdict instead; it is the cheapest beat in the ad.
3. **The early PITCH.** Not the product being visible early, which the bank does constantly, but
   the product being sold early: crediting it before the admission has landed, so the confession
   reads as an ad and the viewer leaves before the turn.
4. **Two asks.** A nudge in the middle and a real one at the end. The closing one stops working.
5. **Borrowed specificity.** A detail that sounds concrete and traces to nothing. This is the one
   that creates real exposure rather than a weak ad.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, words per sentence, rig and on-camera share: measured from the ten
  banked ads in this skill's own bank, 2026-08.
- Beat order and the Specific-beat doctrine: house craft, written for this release.
- Peer-trust versus expertise as separate mechanisms: source-credibility research
  (Hovland and Weiss 1951; Pornpitakpan 2004).
- Polish triggering ad-recognition: persuasion-knowledge research (Boerman et al. 2017;
  Eisend et al. 2020).
- Compliance rules: inherited from the shared claims law and the script skill's evidence layer.
