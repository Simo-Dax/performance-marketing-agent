# UGC script engine, the words stage for the eleven format skills

This module owns ONE stage: turning a brief into an approved set of words (or an approved
decision that there are no words). Every UGC format skill loads it and runs U.0 through U.9.

It stops at the transcript gate. Anchor stills, render prompts, generation paths, spend and
assembly are NOT this module's business and are never decided here.

The rule that makes this work, stated once and binding throughout:

> **The format beats this module.** This module supplies craft, math, sourcing law and
> review. The calling format supplies runtime, beat order, hook family, word budget, sentence
> length, product timing, CTA hardness and position, and authenticity level. Where the two
> disagree on any of those, the FORMAT wins and this module goes silent. This module may
> never add a beat the format's grammar does not have.
>
> **One carve-out, because it is not the same axis.** A format owns how LONG its sentences run.
> It does not own whether they sound like speech. `natural-voice.md` governs connective tissue,
> contractions and flow in every format, including the terse ones, and no number in a format
> spec overrides it. A four-word POV line and a nineteen-word testimonial line are both spoken
> by a person or the ad has failed.

---

## U.0 REQUIRED parameters, halt if unset

The calling skill passes all eight from its own format spec. If any is missing, STOP and ask
for it. Never assume a default, and never infer one from a sibling format.

| Parameter | Example | Supplied by |
|---|---|---|
| `format_id` | `ugc-testimonial` | the skill |
| `script_mode` | `required` / `default-voice` / `default-sound` / `forbidden` | format spec |
| `duration_target` | 25 seconds | format spec, user may override |
| `word_budget` | 79 to 102 | format spec, measured |
| `words_per_sentence` | 7 to 19 | format spec, measured |
| `wps` | 3.9 | format spec, measured |
| `voice_source` | `voc-required` / `brand-led` | format spec |
| `delivery` | `on-camera` / `voiceover` / `mixed` | format spec |

Then load `script-structure.md` with `mode=format-led` and the `wps` above. That mode exists
for exactly this caller: it switches off the universal skeleton and the twelve-framework
library at their own gates, keeps the word math, and drops the ten-second segment ceiling
because these skills render in one pass.

## U.1 Study the bank BEFORE writing a word

Read all ten pairs in this skill's own `references/recreation-prompts/`, both halves. Ten
real scripts of this exact format, with their real dialogue, their real line lengths and
their real beat order, teach more than any framework name.

Two hard limits on that reading:

1. **Own bank only.** Never read, cite or borrow from another format's bank. Each format was
   studied separately on purpose, and a script built from a sibling's examples is that
   sibling's format wearing this one's name.
2. **Never copy.** Not a line, not a beat, not a phrase. The bank teaches structure,
   specificity and length. A script that reuses a bank line is a failed script.

Report in one line what the ten taught: the dominant beat order, the line-length feel, and
where the CTA lands. That line goes in the transcript file.

## U.2 Resolve the script mode

`script_mode` decides whether this stage produces words at all.

| Mode | Behavior |
|---|---|
| `required` | The ad speaks. No silent variant exists; do not offer one. |
| `default-voice` | The ad speaks unless the user says otherwise. State the default in one line, accept a one-word override, ask no question. |
| `default-sound` | The ad carries no dialogue unless the user asks for it. Same one-line statement, same one-word override. |
| `forbidden` | The ad never speaks. Narration would disqualify the format. Go to U.3 and stop. |

State the resolved mode plainly before writing. A user who says nothing gets the default.

## U.3 The sound-carried branch

A format carrying no dialogue is NOT silent, because music is banned from every render. It is
sound-carried: the world and the product make the whole track. This stage still produces an
artifact, just not a script.

Write a **sound plan**: an ordered list of the sounds the ad is built on, each tied to the
beat that makes it and the physical action that produces it. Real, diegetic, product-made.
No music, no library sound, no score, and nothing the scene could not physically make.

Then skip U.4 through U.6 and go to U.7. The sound plan passes the same review and the same
gate a script does.

## U.4 Source the language

`voice_source` decides where the words are allowed to come from.

**`voc-required`.** Every substantive line traces to the VOC document: what real customers
actually said about this product or a comparable one. Wording may be adjusted for rhythm and
length. Substance is never invented. With no VOC document on file the skill STOPS and routes
the user to build one; it does not write a customer from imagination.

The line C.4 draws, and it is load-bearing:

> A spoken line is a PERFORMANCE and may be reworded. Anything framed as a QUOTATION, on
> screen in quote marks, called a real review, or shown as a review card, is customer
> language under `creative-constraints.md` C.4 and stays verbatim with its `voc:S4` style ref.

Record the ref for every sourced line in the transcript file.

**`brand-led`.** Language comes from the Brand DNA, the Foundation Pack and the product's own
facts. `creative-constraints.md` C.1, the FTC 2024 proof gate, still binds every count,
rating, testimonial, statistic and dollar figure to one of its four sanctioned sources.

**Casting, both cases.** Where the format puts a person on camera, the casting brief is the
brand's ideal customer from the VOC or the Foundation Pack avatar sheet, so the face, age,
register and setting suit that brand's actual buyers.

## U.5 Write to the budget

**Write in voice first, then fit. Not the other way round.** Load `natural-voice.md` BEFORE the
first line, not after the draft. Its HARD RULE 1 decides whether this reads as a person or as an
ad: real speech carries connective tissue, the "you just", "and it", "so then" that ad copy
strips out. A draft written clipped and filtered afterwards stays clipped, because a filter can
only cut, and connective tissue is not something you cut to reach.

1. **Beat order comes from the format's scene grammar.** Not from a skeleton, not from a
   framework, not from the bank's example order. One line at least per beat.
2. **Total words land inside `word_budget`.** The band is measured from real ads of this
   format at this duration. Outside the band is a failure even when the words are good.
3. **Sentence length sits inside `words_per_sentence`.** This carries more of the format's
   voice than the total does: fourteen-word sentences and four-word fragments are different
   formats even at identical word counts. The band is a DISTRIBUTION, not a target. Real speech
   varies, so a script whose every sentence lands on the same count has failed the band even
   while satisfying it, and the longest sentence named in the spec's comment is there to be
   used. Do not count the shot list: one sentence often runs across three shots, and writing
   to the cut instead of to the breath is exactly how this goes wrong.
4. **One CTA, and the ad ends on it.** Hardness and position are the format's call.
5. **Beats are never labeled** in anything the viewer hears or sees.

## U.6 Craft filters, run silently

- `natural-voice.md`, its second pass. It was already loaded at U.5 and written UNDER, so this
  is verification rather than rescue: read every line aloud in your head, and rewrite anything
  you would not say to a friend at a kitchen table. Its RULE 2 check is the one that catches
  what U.5 missed, three clipped sentences in a row collapsing into one flowing thought. Its
  RULE 3 check is comprehension, and it is a different question from cadence: mark every word a
  twelve-year-old would not use, then find it in the VOC, land it in the same breath, or cut it.
- `dr-discipline.md` DR.1 on every line: it moves a stranger toward the sale or it goes. Where
  the format is entertainment-led, DR.2 governs, and the joke has to carry the selling
  argument rather than decorate it.
- `creative-constraints.md` C.1 proof gate, C.2 niche gates, C.3 no fake urgency, C.8 clarity.

None of these is announced to the user. They run, then the output is what it is.

## U.7 Review

Load `director-review.md`. Run D.2c with its format-led substitution: check 1 tests the script
against this format's scene grammar instead of the skeleton. Apply D.3's kill floor, D.5a's
dual-lens chief pass, and D.4's two-cycle revision bound. A script failing any check is
rewritten before the user sees it; still failing after two cycles, it goes to the user
with the failing check named honestly.

## U.8 The artifact

Write `transcript.json` into the run folder:

```
{ "format": "ugc-testimonial", "concept": "...", "script_mode": "voice",
  "duration_target_s": 25, "wps": 3.9, "word_budget": [79, 102], "word_count": 91,
  "voice_source": "voc-required", "bank_read": "<the one line from U.1>",
  "lines": [ {"id":"l01","beat":"admission","delivery":"on-camera",
              "text":"<exact spoken line>","voc_ref":"S4"} ] }
```

Sound-carried runs write the same file with `"script_mode":"sound"`, an empty `lines` array,
and a `sound_plan` array of `{"id","beat","source","action"}`.

## U.9 Handoff, NOT a user stop

The words do not get their own approval round. They are approved at GATE 1 as part of THE PLAN,
alongside the shape of the ad and the anchor prompt, because a user judging a script wants to
see what it will look like at the same time.

So this stage ends silently: write `transcript.json`, hand it to the video engine's phase 1, and
say nothing to the user yet. The script engine never presents anything on its own.

The obligation this creates downstream: at gate 1 the spoken lines are shown FIRST, in plain
form, line by line, as the first of the three things in that message. Never inside a prompt,
never abbreviated, never summarised. A user checks their ad's words by reading them, and they
should be the first thing on the screen.

## U.10 Self-check before the handoff

- the ten pairs in THIS format's bank were read, and no other bank was touched
- no line reproduces bank text
- every beat in the format's grammar has at least one line, and no beat exists that the
  grammar does not have
- word count inside the budget, and sentence length spread across the format's band rather
  than parked on one value
- the read-aloud test was actually run: every line is one a person would say to a friend at a
  kitchen table, connective tissue intact, no stack of three clipped sentences in a row
- every line lands on FIRST hearing for a twelve-year-old, and every hard word left in the script
  is either in the VOC or landed in the same breath. The product and category keywords survived
  the simplification rather than being smoothed away
- `voc-required` formats: every substantive line carries a ref, and nothing framed as a
  quotation was reworded
- exactly one CTA, and the ad ends on it
- no beat labels leaked into spoken text
- no music anywhere in the plan, and no sound the scene could not physically make
