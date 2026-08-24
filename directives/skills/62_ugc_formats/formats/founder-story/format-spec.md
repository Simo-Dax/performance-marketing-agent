# Format spec, Founder Story

```
format_id:          ugc-founder-story
command:            /pm-ugc-founder-story
one_line:           The founder tells you why this exists at all.

duration_s:         24 to 30            # measured median 29.6
script_default:     default-voice       # 9 of 10 banked ads speak
wps:                3.31
word_budget:        90 to 127
words_per_sentence: 9 to 17             # measured, longest banked 68; the old 4 counted shots, not sentences

audio_treatment:    vo-over-scenes
delivery:           voiceover
on_camera_share:    19%
rig:                mixed               # 122 static to 64 handheld; interview static, B-roll handheld
shots_per_10s:      6.8 to 8.6          # measured median (a FLOOR) to p75 (the target)

anchor_role:        founder + product in the origin's context
voice_source:       brand-led
requires:           a real photograph of the founder, product photo
funnel_role:        awareness, consideration
authenticity:       high
generation_honesty: real-input-required
```

## What this format is

The founder tells the origin: the problem they hit, the turning point, and what they built. It
removes the doubt "who is behind this and why should I care", and it asks the viewer to trust
personal stake. It is the only format whose subject is the company rather than the product.

**A real founder photograph is mandatory.** The founder is a real person, so the anchor is built
from their actual photo and never invented. No photo, no run. This is what makes the format
honest, and it is not negotiable.

**Four words a line across nineteen lines** is the shortest, most fragmentary rhythm in the
family, and it is not an accident. People telling their own difficult story speak in pieces.
Smooth, complete sentences read as a brand talking about a founder rather than a founder talking.

## When it fits, and when it does not

```
fits:  there is a real founder, a real origin, and a turning point worth telling
not:   the founder is not credible or relevant to the buyer
       the story is about the product working -> route to /pm-ugc-testimonial
       there is no origin, only a mission     -> that is brand copy, not this format
```

## Beat order

1. **Origin problem.** What was wrong, in their life, before any of this existed.
2. **Personal stake.** What it cost them. This beat is the format.
3. **Turning point.** The moment it changed.
4. **What was built.** The product enters here, as the answer to the problem above.
5. **Values.** What the company refuses to do, or insists on.
6. **Ask.** Soft, values-aligned, and the ad ends on it.

## Hard rules

1. A real founder photo is supplied and the anchor is built from it. Never a generated founder.
2. The personal stake is explicit. A story with no cost is corporate copy in first person.
3. The chronology is specific: real dates, real places, real details.
4. The product is not CREDITED before "what was built". It may be on screen earlier, and the bank
   brings it in around a fifth of the way through, but the story reaches it as the answer to the
   origin problem rather than opening on it as a pitch.
5. **The story could not be told by another brand.** If it could, it is not an origin, it is a
   template.

## Compliance flags

| Flag | Rule |
|---|---|
| Founder likeness | built from the user's supplied photograph, used with their authority |
| Proof | any business claim traces to a sanctioned source under the claims law C.1 |
| Earnings | no income claims about the business without written substantiation |

## Failure modes

1. **Corporate copy.** An About Us page read aloud in first person.
2. **No stake.** A story where nothing was risked and nothing hurt.
3. **The interchangeable origin.** True, and true of a hundred other brands.
4. **Smoothed delivery.** Complete, polished sentences where fragments belong.
5. **No turning point.** A gradual story with no moment in it.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, sentence length, rig (re-measured 2026-08-23) and on-camera share: measured from this
  skill's own ten banked ads, 2026-08. This format cuts fastest in the entire family, which
  contradicts the source research's advice of slow emotional pacing; the measurement wins.
- Founder authenticity through values and motive: founder-story research.
- Real founder photo requirement: user decision, 2026-08.
