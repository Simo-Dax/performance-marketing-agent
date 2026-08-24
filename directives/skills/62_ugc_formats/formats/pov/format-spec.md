# Format spec, POV Skit and Comedy

```
format_id:          ugc-pov
command:            /pm-ugc-pov
one_line:           A relatable situation, played for a laugh, that resolves with the product.

duration_s:         15 to 25            # measured median 19.6
script_default:     default-voice       # 7 of 10 banked ads speak
wps:                2.45                # by far the sparsest talker in the family
word_budget:        33 to 57            # the smallest budget here, and deliberately so
words_per_sentence: 4 to 9              # measured, longest banked 27; genuinely terse, this one is real

audio_treatment:    sync-to-camera
delivery:           mixed
on_camera_share:    55%
rig:                mixed               # 49 static to 9 handheld across the bank
shots_per_10s:      3.9 to 5.5          # measured median (a FLOOR) to p75 (the target)

anchor_role:        character + product at the payoff
voice_source:       brand-led
requires:           product photo
funnel_role:        awareness
authenticity:       stylized            # relatability beats realism here
generation_honesty: unconstrained
```

## What this format is

A recognisable situation, escalated for comedy, resolved by the product. It removes no doubt at
all, and that is the point: it buys attention and affection rather than belief. What it asks the
viewer to trust is that you understand their life.

**It carries the least dialogue in the family by a distance**, 33 to 57 words against a
family average near 90. Physical comedy and timing do the work; the words are punctuation.

## When it fits, and when it does not

```
fits:  low-ticket, mass-market, and a situation the audience will recognise instantly
not:   high-ticket or high-trust categories  -> route to /pm-ugc-expert
       anything with a regulated claim       -> humour and proof do not mix
       the product needs demonstrating       -> route to /pm-ugc-problem-solution
```

## Beat order

1. **Setup.** The situation, recognisable within two seconds.
2. **Escalation.** It gets worse, or more absurd.
3. **Punchline.** The turn.
4. **Product resolution.** The product resolves it, and the resolution has to be the joke's
   logic, not an advert glued to the end.
5. **Ask.** Soft, and often nothing more than the product being there.

## Hard rules

1. **Humour never carries efficacy proof.** Humour measurably reduces source credibility, so any
   claim made inside a joke is a claim made at a discount. This format asserts nothing it needs
   believed.
2. The punchline connects to the product. Comedy that would work with any product is a sketch.
3. The product enters at the payoff, never front-loaded.
4. No hard CTA. It breaks the register and undoes the goodwill the joke bought.
5. The situation is specific. Generic relatability is not relatable.

## Compliance flags

| Flag | Rule |
|---|---|
| Proof | this format proves nothing. Any efficacy claim belongs in a different format |
| Category | avoid entirely for regulated categories where credibility is the currency |

## Failure modes

1. **The bolted-on product.** The joke ends, then an ad starts.
2. **Not funny.** The most common one, and the hardest to fix in review.
3. **Over-explaining.** The ad tells you why it was funny.
4. **The hard CTA.** Register breaks in the last two seconds.
5. **Humour doing proof.** A claim smuggled inside a joke, which converts worse than no claim.

## Provenance

- Sentence length was RE-measured 2026-08-20 and the earlier figure was wrong. It had been
  taken from the banked prompts' per-shot `Dialogue` fields, which split one spoken sentence
  across several cuts, so it recorded the edit rather than the speech. The current band is
  p25 to p75 of sentences from the rejoined transcripts, and the comment names the longest
  sentence the bank contains.
- Duration, wps, word budget, words per sentence, rig (re-measured 2026-08-23) and on-camera share: measured from this skill's
  own ten banked ads, 2026-08. The 2.45 wps is measured on the seven ads that speak.
- Humour reducing source credibility: Eisend meta-analysis, JAMS 2009.
- Narrative transportation lowering counter-argument: Green and Brock 2000; Van Laer et al. 2014.
