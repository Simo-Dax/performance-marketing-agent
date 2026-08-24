# The UGC format contract

Every UGC format skill ships exactly one format spec, a file named **format-spec.md** in its own
references folder, and that file fills this contract. The spec is the ONLY place a format differs; the engines are written once and shared.

The line this contract draws: a spec that describes HOW to render is out of bounds, that is the
engine's job. An engine that knows the word "unboxing" is out of bounds, that is the spec's job.

A spec has two halves. The **facts block** at the top is data, so it can be checked
mechanically across all eleven files. The **craft below** is prose, because hard rules and
failure modes are arguments, not numbers.

---

## Part 1, the facts block

Every key below is required. A missing key is a build failure, not a judgment call, because the
engines read these directly and have nothing to fall back on.

```
format_id:         ugc-testimonial
command:           /pm-ugc-testimonial
one_line:          A real customer says what changed, in their own words, to camera.

duration_s:        20 to 30            # measured; 30 is the hard cap on every format
script_default:    default-voice       # required | default-voice | default-sound | forbidden
wps:               3.9                 # measured; omit when script_default is forbidden
word_budget:       79 to 102           # measured, at the default duration
words_per_sentence: 7 to 19           # measured; see the note below on how

audio_treatment:   sync-to-camera      # vo-over-scenes | sync-to-camera | two-speaker-turns | sound-led
delivery:          on-camera           # on-camera | voiceover | mixed | none
on_camera_share:   44%                 # measured; drives how hard the anchor has to work
rig:               static              # static | handheld | mixed
shots_per_10s:     3.7 to 6.8          # measured median (a FLOOR) to p75 (the target)

anchor_role:       character + product # what the anchor still must lock
voice_source:      voc-required        # voc-required | brand-led
requires:          VOC document, character, product photo
funnel_role:       consideration, conversion
authenticity:      high                # polish helps or hurts, per format

generation_honesty: voc-sourced        # real-input-required | voc-sourced | unconstrained
```

`audio_treatment`, `script_default`, `delivery`, `rig`, `voice_source` and
`generation_honesty` are fixed vocabularies. Anything outside them fails the check.

Formats with `script_default: forbidden` omit `wps`, `word_budget`, `words_per_sentence` and
`voice_source`, and set `delivery: none`: there is no script to budget and no voice to source.

**`shots_per_10s` is a cut-density floor, not a description.** The low number is the measured
MEDIAN of this format's own bank, so half the banked ads already beat it; an ad that falls below
it is slower than half the real ads of its own format, which is the definition of the boring
half. The high number is the measured p75 and is what a run should aim for. Multiply by the
duration in tens of seconds to get the shot count: a 25-second testimonial at the 3.7 floor is 9
shots, and the 6.8 target is 17.

A format may be intrinsically slow and still be right. Expert sits at 2.0 because it is one
person explaining a mechanism, and cutting it like a founder story would wreck it. The floor is
per-format for exactly that reason, and it is never borrowed from a sibling.

**`words_per_sentence` is measured on SENTENCES, and the measurement has one trap in it.** The
banked prompts carry a `Dialogue` field per SHOT, and a shot is not a sentence: an ad cutting
every 2.3 seconds splits one spoken sentence across three or four shots. Measuring those fields
gives words per shot, which is a fact about the EDIT, not about how the person talks.

So: rejoin every `Dialogue` field in an ad into one continuous transcript, split THAT on sentence
endings, and measure the result. Two guards. Skip any banked ad whose transcript carries no
terminal punctuation, because sentence boundaries cannot be recovered from it and treating the
whole VO as one sentence corrupts the number in the opposite direction. And state the band as p25
to p75 of real sentence lengths, never a single average, because one number reads as a target and
produces ten sentences of identical length, which is its own kind of robotic.

The comment on the line names the longest sentence the bank actually contains. That number is not
decoration: it is the writer's explicit licence to run long, and without it the band's upper bound
gets read as a ceiling.

**`anchor_role` may declare a PLATE SET instead of a single still.** Most formats lock one anchor
and name what it holds. A format whose ad has visually distinct phases may instead set
`anchor_role: PLATE SET` and define the plates in its own prose section, saying which are always
required, which are conditional, and what each one locks. The image engine builds the set the spec
declares. Only unboxing uses this today; the other ten declare a single anchor and are unaffected.

A format can be `sound-led` by DEFAULT and still keep a word budget. `audio_treatment` describes
what the ad normally sounds like; `script_default` decides whether words exist at all. Unboxing
and Before/After are both sound-led by default and both keep their budgets, because a user may
ask for voice and the numbers have to be there when they do.

## Part 2, the craft

### What this format is

The one doubt it removes and the one thing it asks the viewer to trust. Two or three sentences.
This is what the front door prints and what a user reads to know they picked right.

### When it fits, and when it does not

Two short lists. The second matters more, because it stops the front door routing someone into
the wrong format, and it names the format that IS right instead.

```
fits:  the brand has verbatim customer language and one believable, specific result
not:   the result has to be SEEN     -> route to /pm-ugc-before-after
       the mechanism needs explaining -> route to /pm-ugc-expert
```

### Beat order

The named steps this format moves through, IN ORDER. Three to six of them, each with the job it
does.

**No time shares, no percentages, no durations per beat.** The order is what makes a format that
format: a reveal before the anticipation is not an unboxing. How long each beat runs is decided
per ad, from what that product actually needs shown, informed by the ten examples in the bank. A
jar of face cream and a six-foot cat tree are both unboxings and should not spend the same
fraction of the ad on the opening.

### Hard rules

The format's non-negotiables, written as binary checks. Not preferences, not craft advice. A
hard rule is something that makes the output NOT THIS FORMAT when broken, and every one is
checkable by reading the finished prompt or watching the cut.

### Compliance flags

Which gates in the shared claims law this format trips, and the binding rule for each. A format
with none says `none` explicitly rather than omitting the section.

### Failure modes

Three to five, each naming the symptom and its cause. These give the review pass something to
test against, and they are where a format's real craft lives.

### Provenance

Where this format's numbers and rules came from, dated. A rule with no provenance is a guess and
gets labelled as house craft, out loud.

---

## Part 3, the shot vocabulary

Every format ALSO ships a shot-vocabulary file in its own references folder, measured from its
own ten banked ads. The facts block is what the ENGINES read. The shot vocabulary is what
teaches the VIDEO MODEL what this format is made of.

**The file has two halves and only one of them ships.**

### The PROMPT BLOCK

Fenced by `<!-- PROMPT-BLOCK-START -->` and `<!-- PROMPT-BLOCK-END -->`, and it is the only part
that ever reaches a model. **2,100 to 2,430 characters**, validated, because the render prompt
has a hard 4,800 to 5,000 budget and this block is the largest fixed item in it.

It is written in PROMPT VOICE, addressed to the model, and carries:

```
FORMAT: <NAME> UGC          one paragraph: what this format is, and what it is not
the hook                    what shot one runs and what it contains
ALWAYS IN FRAME             the cast, the props, the background
THE SHOTS IT IS BUILT FROM  one entry per shot type, in prose
the signature move          where the format has one, WITH the reason it exists
HOW IT SEQUENCES            the beat flow and how shots cluster
PERFORMANCE                 how the people behave, mode-neutral
RHYTHM                      the two shot-length counts, and the failure named out loud
the cut rule                hard cuts and jump cuts, and the text ban
```

**Measurements go in as SPEC, never as statistics.** "About four in every ten shots", not "share
~40%". "0.4 to 2.2 seconds, usually under one", not a duration column. The numbers survive; the
grammar changes. A model reads a percentage as a fact about a dataset and a sentence as an
instruction about this ad.

**Every shot entry states who speaks on it**, on camera or voiceover, so B-roll never acquires a
talking mouth.

**Each entry is marked required or conditional.** A skill may DROP a conditional entry when the
product cannot support it. It may never add one, rename one, or change a number: those came from
counting the bank and the skill's judgement is worse than the count.

**PERFORMANCE is required and is written mode-neutral.** It says how the people in this format
behave, not what they look like, and it never assumes the subject is on camera speaking, because
the delivery line hands that choice to the model. It exists because a prompt carrying only
physical description renders a mannequin, measured on a live render whose subject never smiled.

**The RHYTHM entry names the failure.** "Shots of equal length are wrong" does work that a count
alone does not, and both go in.

### THE MEASUREMENTS

Everything below the fence, and none of it is ever pasted: provenance, the raw bank counts the
block was derived from, the CV of shot lengths, doctrine notes, and the reasoning behind house
rules that override the bank. It exists so the numbers can be re-checked and so nobody later
re-derives a rule from the bank and quietly softens it.

**The DELIVERY LINE lives here and is per-format**, and it is not a free choice everywhere. Four
formats have none: street interview is 122 on-camera to 0 voiceover, green screen 79 to 4,
unboxing 0 to 16, and ASMR has no dialogue at all and omits the pacing block entirely. Handing a
free choice to a format that has none is how a vox pop acquires a narrator.

**A format may document a measured conflict with a house rule.** Expert, POV and green screen all
open slower than the universal sub-2-second hook rule, for structural reasons their files
explain. Doctrine that overrides measurement is always labelled as doctrine.


## The check

A validator asserts, across all eleven specs: every facts-block key present; every fixed
vocabulary respected; `duration_s` inside 10 to 30; `sound-led` specs carrying no word budget
and script-carrying specs carrying one; every prose section present and non-empty; no beat
carrying a percentage, since that would reintroduce the template the beat order exists to avoid;
and every format shipping a shot-vocabulary file whose sections are all present, whose shot-type
rows each declare `always` or a condition, and whose delivery line matches the on-camera to
voiceover split actually counted in that format's bank.
