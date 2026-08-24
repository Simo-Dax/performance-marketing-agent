# UGC video engine, the render prompt

One job: turn an approved transcript and an approved anchor into the single prompt that renders
the whole ad. This engine runs in TWO PHASES, at two different points in the run.

| Phase | When | Produces |
|---|---|---|
| **Phase 1, the plan** | after the script, BEFORE gate 1 | the shot count, which conditional shot-type rows apply, and the hook approach. No shot list |
| **Phase 2, the render prompt** | after the anchor is approved at gate 2 | the full 5,000-character prompt, assembled from approved parts |

Phase 1 is what the user reviews. Phase 2 is assembly, and it invents nothing: every shot,
every spoken line and the anchor were all approved before it runs.

Most of what you need is not in this file. It is in the ten video prompts in this skill's own
`references/recreation-prompts/video/`. READ ALL TEN before writing anything, and never read
another format's bank. Those ten teach the layout, the level of detail, how the shots are cut
and how dialogue sits against picture. The rules below are only what the bank cannot teach.

---

## V.0 The ten teach the craft, then you write an original

Read all ten video prompts in this skill's bank. They are there to answer one question: what
does a well-written prompt for a winning ad in THIS format look like. They are teachers, not
templates, and no single one of them is the lesson.

**What the ten teach you.** How the anatomy is laid out. How physically specific the writing
gets, and where it stops. The realism language that keeps an ad looking filmed rather than
produced. How a shot is described in one paragraph. How a product is brought into frame,
handled and shown. In one phrase: HOW THIS FORMAT IS SHOT.

**What the ten no longer teach you.** Pacing, shot proportions, shot durations and cut rhythm.
Where this skill ships a shot-vocabulary file in its own references folder, those are MEASURED there and go into
the prompt as facts. Reading ten prompts and inferring a rhythm badly, when the number is in a
table two files away, is how a generated ad ends up with twelve evenly spaced shots. Do not
re-derive what is already measured, and never let a reading of the bank override it.

**What you never take from them.** Any ad's shot list. Its span pattern. Its scene order. Its
setting, its actions, its props, its words, its people, its product. Not one of the ten is a
skeleton to fill in, and none of them is pasted, quoted or adapted.

**Then design this ad from scratch**, for this product and this format. The shot count, the
cuts, the pacing and the beats are decided by what THIS product needs shown and what the
format's own scene grammar calls for, not by what any banked ad happened to do.

**The test before rendering:** could this ad only be this brand's ad? If lifting the product
out and dropping another one in would leave a working commercial, it was built from a template
rather than from the product, and it gets rewritten.

## V.0a The PROMPT BLOCK, the only thing pasted

Every UGC format ships a shot-vocabulary file in its own references folder, carrying a section
fenced by
`<!-- PROMPT-BLOCK-START -->` and `<!-- PROMPT-BLOCK-END -->`. **Paste that block, and only that
block, verbatim into the render prompt.** It already carries the format definition, the hook
rule, what is always in frame, the shot types, the sequencing, the performance register, the
rhythm counts and the cut rule, written in prompt voice and sized to the budget in V.5.

**Everything else in that file is engine-facing and is NEVER pasted**: provenance, the raw bank
counts the block was derived from, doctrine notes, and the reasoning behind house rules that
override the bank. It exists so the numbers can be re-checked. It is not material for a model,
and pasting it is how a prompt ends up at nine thousand characters telling a video model that
nineteen out of twenty banked lines were narration.

**Measurements go in as SPEC, never as statistics.** The block already does this and it is why it
reads the way it does: "about four in every ten shots", not "share ~40%"; "0.4 to 2.2 seconds,
usually under one", not a duration column. Same numbers, different grammar. A model reads a
percentage as a fact about a dataset and a sentence as an instruction about this ad.

The one freedom: a shot row marked conditional may be DROPPED when the product does not support
it, a dispensing row for a product that is never poured. No row is ever added, renamed or given a
different number, and no sentence in the block is rewritten, summarised or reordered.

**TWO freedoms, not one.** Dropping a conditional shot row is the first. The second is REQUIRED
rather than permitted: **every remaining choice in the block must be resolved to the one option
this ad is using before the block is pasted.** A block cannot know in advance which cast, which
location or which variant a given ad has, so where a sentence still offers alternatives, this
engine picks one and writes it flat.

A render prompt containing an unresolved choice is a FAILED prompt and is rebuilt. Search the
assembled prompt for "one of", " or ", "sometimes", "often" and "usually", read every hit, and
resolve it. The only survivors are "a hard cut or a jump cut", which is a fixed pair rather than
a menu, and the header "THE SHOTS THIS FORMAT USUALLY USES".

### The boundary, stated as a ban list

The render prompt says WHAT THE OUTPUT IS and WHAT SHOTS THE FORMAT IS BUILT FROM. It does not
describe what the ad should look like. That is the video model's decision and it is better at it
than a written description is, which is the same reason the static skill hands layout to the
image model. Banned in every render prompt:

- No shot type, duration, share or sequencing rule this engine authored rather than pasted
- No per-shot span list. The model assembles the shots; that is the whole point
- No aesthetic direction: no mood, no vibe, no "cinematic", no "authentic", no "natural" as an
  instruction. Tested and true of image models too, a single taste word leaks into literal
  styling
- No palette, no colour, no lighting design, no set description
- No pacing adjectives. "Cut it fast" is an opinion; the rhythm block is a measurement

Physical realism is NOT aesthetic direction and stays: phone exposure, autofocus behaviour,
contact shadows, real-time movement, gravity. Those describe how a camera and a body behave,
not how the ad should feel.

If a finished prompt tells the video model how the ad should LOOK, or carries a number this
engine wrote rather than pasted, the prompt has failed and is rebuilt.

## V.1 The shape of the render prompt

**This engine does NOT write a shot list.** It never assigns a shot type to a position, never
writes a span, and never produces a scene breakdown. Deciding what each shot is, how long it
runs and what order the shots come in is the VIDEO MODEL's job, and it is better at it than a
text model writing timecodes.

What the prompt does instead is teach the format and hand over the ingredients. The format's
sections and this ad's sections INTERLEAVE, in this order:

```
 1  the output line       duration, aspect, pixels, shot COUNT, audio, phone never in frame
 2  FORMAT + the rules    PASTED from the prompt block
 3  THE <X> IN THIS AD    authored: the one problem, the one thing changing, what is in the box
 4  THE ORDER             authored: this ad's beats, in a single sentence
 5  THE HOOK              PASTED from the prompt block
 6  WHERE                 authored: one sentence, the place and the time of day
 7  THE SHOTS ... + the camera line   PASTED from the prompt block
 8  HOW THEY PLAY IT      PASTED from the prompt block
 9  TIMING                PASTED from the prompt block
10  SUBJECT               authored, and it ENDS on an energy line, see V.3
11  LOCATION              authored, physical facts only
12  PRODUCT               authored, plus what the attached photos show
13  TRANSCRIPT, 0:00 to 0:NN   authored, each line in quotation marks
14  the pacing block      PASTED, V.4a, with the delivery line and the rushing guard
15  YOU ARE THE DIRECTOR  PASTED, V.4b
16  the ban line          PASTED, V.4c, and it is the last text in the prompt
```

Sections 2, 5, 7, 9, 14, 15 and 16 are PASTED, not authored. Sections 3, 4, 6, 8, 10, 11, 12 and
13 are the strategy and are the only place this engine writes anything.

**The header on section 13 carries the real duration**, written `TRANSCRIPT, 0:00 to 0:23`. Never
`23:00`, which a model reads as twenty-three minutes and which fights the duration in line 1.

**The format definition, the shot types, the performance register, the rhythm and the bans all
live INSIDE the prompt block.** This engine does not restate any of them, and a prompt that
carries a second copy of something already in the block has failed.

**A `script_default: forbidden` format swaps blocks 6 and 7.** ASMR has no transcript and no
pacing block, which removes roughly 1,300 characters from the prompt and puts the window out of
reach. In its place goes a SOUND PLAN: the ordered list of sounds the ad is built on, each tied
to the action that makes it, written by the script engine at U.3. It is real content, not
filler, and it is what carries a sound-led ad the way a transcript carries a spoken one.

**LOCATION is not optional and it is not scenery.** With no anchor attached, the subject and
location blocks are the only thing holding the same person in the same room from the first shot
to the last. State the place as physical facts: what furniture, what light source, what is on the
surfaces. Never a mood, never a palette, never a lighting design.

**The shot COUNT is stated, the shot ASSIGNMENT is not.** Take the count from the format's
`shots_per_10s` band times the duration. Saying "in 14 shots" is a constraint the model obeys
precisely; saying "shot 6 is a product macro at 1.4 seconds" is this engine doing the model's
job with worse information.

## V.1a Where identity lives

**The person is described ONCE, in the character block.** Full physical detail: age range, skin,
hair, build, wardrobe, and the accessories that must persist. The banks run a median of 290
characters describing the subject and 354 on props, so land in that neighbourhood; that density
is doing real work and it is why the person stays the same person at second 29.

**Their features are never restated anywhere else in the prompt.** Across 1,155 banked Action
fields, only 22% carry any identifying word at all. Repeating the wardrobe makes the model
fixate on whatever gets repeated, and here there is no per-shot text to repeat it in anyway.

**The product is the deliberate exception**, and the vocabulary handles it: 82% of banked ads
name the object every time it is in frame, which is why the shot-type rows say things like
"label facing camera" and why the product line instructs naming the container in any shot where
it is held. The person rides the character block and the reference stack.

## V.2 What the prompt says about shots, and what it does not

Four things, and none of them is a shot list.

1. **The COUNT.** "in 14 shots." Take it from the format's `shots_per_10s` band times the
   duration in tens of seconds. The model hits a stated count precisely; this was measured on a
   live render that was asked for twelve and delivered exactly twelve with perfectly tiling
   spans.

2. **The HOOK.** One sentence: that the first shot is the hook, how long it runs, and what the
   format's hook usually contains. The detail comes from the vocabulary's own hook block, which
   is measured. Do not describe a specific opening image; describe what this format's openings
   DO.

3. **The RHYTHM, as numbers rather than as an adjective.** This is the one instruction that has
   measurably failed to land when stated as prose. A live tutorial run asked for uneven shots
   and returned a CV of 0.23 against its bank's 0.53, every shot between 1.2 and 2.9 seconds.
   State it as counts instead, from the vocabulary's own range:

   > At least two shots run under {short} seconds and at least one runs over {long} seconds.

   Take `{short}` and `{long}` from the format's measured shortest and longest banked shot,
   rounded to something a model can hit. A count is checkable; "make it uneven" is an opinion.

4. **The HANDOVER, stated plainly.** "You decide what each of the shots is, what order they come
   in, how long each one runs, where it happens, and how it is framed."

**What the prompt never contains:** a numbered shot list, a span, a per-shot framing, a per-shot
action, a Scene Breakdown, or any sentence beginning "shot 6". If a finished prompt tells the
model what shot 6 is, this engine has done the model's job with worse information and the prompt
is rebuilt.

**Dialogue is not assigned to shots either.** The transcript goes in as a block of lines in
order, and the pacing block tells the model to spread them across the full length and which
delivery mode the format allows. Which line lands on which shot is the model's decision, because
it is the one deciding what the shots are.

## V.3 Do NOT describe how a body moves

This engine used to paste a family of physical-realism instructions into every prompt: autofocus
breathing, contact shadows, real-time speed with its small pauses, grip changes, hair settling
under gravity, "add no gestures the beat does not call for."

**That block is gone and must not come back.** The video model renders a moving body better than
any written description of one, and the instructions were spending four hundred characters
telling it to do what it already does. Two live renders shipped without the block and neither
looked produced.

What replaced it is one line in block 1, `Authentic UGC, filmed on a phone. The phone is never in
frame.` That is the whole look note.

**The one thing the model does NOT infer is PERFORMANCE**, and that is why every prompt block now
carries a performance register. A prompt describing only physical facts, a person's height, hair,
skin and clothes, renders a mannequin: it was measured on a live tutorial render whose subject
never once smiled and stood motionless through the last fifth of the ad. Physical description
says what someone looks like. The performance register says who they are, and it is the
difference between a person and a shop dummy.

**Every SUBJECT block ENDS on an energy line.** The block describes height, hair, skin and
wardrobe, and physical facts never say who someone is. One short sentence in plain words, last
thing in the block: "She is warm and quick and alive, never flat: annoyed by the problem, excited
to show you what fixed it, hands moving while she talks." A SUBJECT block that stops at the
wardrobe has failed.

**Registers are written mode-neutral.** They never assume the subject is on camera speaking,
because the delivery line hands that choice to the model. "It shows on their face in any shot
their face is in" holds for a hands-only cutaway; "he smiles while he talks" quietly forces a
talking head.


## V.4 Audio, and the trap in the bank

**The banked Audio fields describe real ads, and most of those ads had music.** Ours never do.
Read that field for its DIEGETIC content, the room tone, the handling, the packaging, the
voice, and ignore every mention of a track, a bed, a beat or a mood.

**On-screen text is banned in the render for the same reason.** All 110 banked prompts ban text,
captions and watermarks outright, and generated text garbles into nonsense. Never write a caption,
a label, a day marker or a step number into the prompt. What the ad SHOULD carry as text is
recommended instead, with timecodes, in the delivery note the run engine writes.

Write the Audio field as the sound the scene physically makes and nothing else. No music, no
score, no trending sound, no library effect. Music is a post layer the user adds later over a
clean track. `generate_audio` stays on: a wordless ad is sound-carried, never silent.

## V.4a The pacing block, pasted verbatim into every render prompt

```
Say every line above, in order, once each, spread across the full length of the ad
so the delivery is unhurried and natural.

<the format's DELIVERY LINE goes here>

The spoken words should not feel rushed.
```

**No header above it.** The `TRANSCRIPT, 0:00 to 0:NN` heading on section 13 already labels the
lines; a second heading here reads as a new topic and pushes the pacing away from the words it
governs.

**The rushing guard is the last line and is fixed text.** A silent format has no delivery line
and no transcript, so it gets neither the block nor the guard.

**The last line is NOT generic and is never written by this engine.** It is copied from the
format's own shot-vocabulary file, which measured whether that format actually offers a choice.
Four of the eleven do not:

| Format | Banked on-camera : voiceover | The line says |
|---|---|---|
| Street interview | 122 : 0 | on camera only, there is no narrator |
| Green screen | 79 : 4 | on camera only, the empty plates carry no words |
| Unboxing | 0 : 16 | voiceover only, no speaking face ever |
| Expert | 26 : 2 | on camera, the speaker is in frame for every line |
| ASMR | 0 : 0 | nothing. This block is OMITTED entirely; nobody speaks |

The remaining six carry a real split in their banks and their line hands the choice to the model.
Offering a free choice to a format that has none is how a street interview acquires a narrator
and an unboxing grows a talking head.

Nothing in that block is adjusted per format or per run. It is fixed text and it is pasted whole
into every render prompt, after the transcript.

**Why it exists.** The generator's delivery rate is not the measured human rate the scripts are
written to, so it rushes the lines, finishes early, and fills the gap by repeating one. Saying
"once each, spread across the full length" fixes all three at once, and it is stated as what to
DO rather than as a list of prohibitions.

## V.4b The handover, pasted verbatim, second to last in every render prompt

```
YOU ARE THE DIRECTOR

You decide how long each shot runs and how the ad is structured.

The instructions above are there to tell you what a winning UGC <format> ad looks like. It is
your job to be the director and make a winning UGC <format> ad that feels authentic.
```

`<format>` is the format's own name, tutorial, testimonial, unboxing and so on. Nothing else in
the block changes, and it is always the final text in the prompt.

**Why it is this short.** An earlier version ran a thousand characters enumerating every decision
being handed over: shot assignment, order, duration, framing, focus, foreground, what he does
between the steps. It said nothing the two sentences above do not, and it spent a fifth of the
prompt saying it. The delegation lands because it is stated once and plainly.

## V.4c The ban line, the last text in every render prompt

```
No music. No subtitles, no captions, no on-screen text of any kind.
```

**No heading above it, and nothing appended to it.** Not watermarks, not logos, not stickers, not
app interfaces, not a list of transition effects. Four bans land; a list of twelve reads as noise
and dilutes the four that matter. The cutting instruction is NOT here: it lives in the block's
TIMING section beside the other timing instructions, which is where a model looks for it.

This is the final text in the prompt, after the director block.

## V.5 Length, 4,800 to 5,000 characters. This is a rule.

**Every finished render prompt lands between 4,800 and 5,000 characters.** Count it before the
gate. Outside that window the prompt is not finished.

The budget that makes it reachable:

```
PROMPT BLOCK        2,100 to 2,430     fixed per format, validated, never edited per run
output header         140 to   180     duration, aspect, pixels, shot count, audio
SUBJECT               250 to   520     THE FLEX
LOCATION              150 to   400     THE FLEX
PRODUCT               600 to   950     physical facts plus how it is handled
TRANSCRIPT            430 to   720     whatever the script engine wrote, about 5.2 chars a word
SOUND PLAN            550 to   750     silent formats only, in place of transcript and pacing
pacing block                  ~220     V.4a plus the format's delivery line
YOU ARE THE DIRECTOR          ~270     fixed text, V.4b
```

The prompt-block ceiling of 2,430 is not a taste call, it is the binding constraint. With the
longest transcript a format's word budget allows and SUBJECT plus LOCATION squeezed to their
floor of 400 combined, a block any larger cannot reach 5,000 from below.

**The fit step, run last.** Assemble the prompt, count the characters, then land the window by
adjusting SUBJECT and LOCATION and nothing else. They are the only blocks that carry DETAIL
rather than INSTRUCTIONS, so more of them adds ground truth about the person and the room, and
less of them costs nothing but specificity. With no anchor attached that detail is load-bearing,
which is why growing it is the honest direction to grow in.

**Never pad any other block, and never trim one.** Not the prompt block, which is validated. Not
the transcript, which is the approved script word for word. Not the product block, which is the
model's only description of the real object. Not the director block, which is fixed text. If
SUBJECT and LOCATION at their full range still cannot reach the window, something upstream is
wrong, a transcript far outside the format's word budget or a prompt block that failed
validation, and that is what gets fixed.

**Why a hard window rather than a guideline.** The previous rule said length was not a target and
nothing should be padded or trimmed to reach a number, while the self-check simultaneously asked
for 4,800 to 5,000. Two rules, opposite instructions, and prompts shipped anywhere from 3,700 to
8,700 characters depending on which one was read. One number now, in one place.


## V.6 The call

| | |
|---|---|
| Model | `seedance_2_5` on Path B, `bytedance/seedance-2-5` on Path C (fal.ai) |
| Mode | **`omni_reference`** whenever an anchor is attached. The default `t2v` refuses reference media and the render fails validation before it starts. |
| Reference | the reference stack, see V.6a |
| Resolution | `1080p` by default |
| Aspect | `9:16` |
| Duration | whole seconds, **30 maximum**; 31 or more is rejected |
| Audio | `generate_audio` true |

One render. No segmentation, no stitching, no assembly. The internal cuts live inside the prompt.

## V.6a The reference stack

Seedance 2.5 takes up to 30 images in `omni_reference`, and every one of them is free. Give the
model as much real ground truth as the ad needs, in this order:

1. **The approved anchor still.** Identity: who and what stays the same.
2. **The user's raw product photo.** Ground truth for the label. The anchor is already one
   generation removed from the real product, so the real photo is the only thing in the stack
   that has never been interpreted. Always attach it.
3. **In-use product photos, whenever the ad shows the product being USED.** If the ad opens it,
   applies it, pours it, wears it, assembles it or demonstrates it, the model needs to see the
   product in that state: the lid off, the pump depressed, the sachet torn, the garment worn,
   the texture on skin. A model that has only seen a sealed jar will invent what the open one
   looks like.

Ask for these at intake, name which states this format's ad will show, and say plainly that a
missing state is a state the model will guess at.

## V.7 The gates, and the spend law

Three stops, in this order. The first is free and is about whether the ad is right. The other two
are about money, and they are hard rules.

**GATE 1, THE PLAN. Free.**
The script, the shape of the ad and the anchor prompt, in ONE message, in that order:

1. **The spoken lines in plain form**, line by line. Or the sound plan, for a sound-carried
   format. Never buried inside a prompt; a user must never hunt for their own words.
2. **The shape of the ad**, in plain sentences rather than as a shot list: how many shots, what
   the hook will be doing, which of the format's shot types this product does and does not
   support, and which conditional rows were dropped. The user is approving an APPROACH, not a
   storyboard, because there is no storyboard: the model builds the shots.
3. **The anchor prompt** from the image engine, and one line on why that moment was chosen.

Then the plain-language note on the thinking, four or five sentences, no jargon: what the ad does
beat by beat, why it is shot this way for THIS product, where the product enters and why there,
and what the ten examples in the bank suggested. Explain the reasoning, never list parameters.

Then STOP. Nothing is generated until the user approves. Everything is free to change here, and
this is the last moment that is true. The full render prompt does NOT exist yet and is not shown:
it is assembled in phase 2 out of the parts approved right here.

**GATE 2, permission to render the anchor image. Costs money.**
Handled by the image engine, from the anchor prompt approved at gate 1. Ask, wait for an explicit
yes, then generate.

**GATE 3, permission to render the video. Costs money.**
Now assemble the full prompt in phase 2, from the approved script, the approved shape
and the approved anchor. Show it, show the anchor, name the exact price for the chosen duration
and resolution, and WAIT.

Phase 2 has no creative licence. If assembling the prompt reveals a real problem, a shot that
cannot be written, a span that does not tile, go BACK to the user with that one problem rather
than quietly redesigning what they approved.

> **THE SPEND LAW, binding on every format.** Nothing that costs the user money is ever
> generated without a clear, specific, immediately preceding yes. Not on silence, not on a maybe,
> not on an approval that was given for a different step, and never on an approval carried over
> from an earlier render in the same run. Every retry is a new spend and needs its own yes. The
> ask always names what is being made and what it costs, in one line, before it happens.

Measured on Path B at 9:16 for a 30-second ad: **1080p costs 270 credits, 720p costs 195, 480p
costs 75.** Default is one 1080p render. Offer 720p once as a cheaper first try for a user who
wants to see it before committing, and say what it saves. Never quote a price the agent did not
read back from the tool itself.

## V.7a Where the finished ad goes

```
05_UGC_Prompts/formats/<format>/<concept>/
    <concept>_v1.mp4          the render, versioned, never overwritten
    <concept>_v2.mp4          a rerun sits beside it, it does not replace it
    prompts/                  the video prompt and anchor prompt per version
    anchor/                   the approved still per version
    transcript.json
    manifest.json             per version: prompt, model, path, duration, resolution, spend
```

A rerun NEVER overwrites a previous render. Every one of those files was paid for, users
compare takes, and silently destroying a 270-credit file is destroying money already spent.

## V.8 Self-check

**Length and structure**
- the prompt is between 4,800 and 5,000 characters, counted, not estimated
- the PROMPT BLOCK was pasted verbatim from the format's own shot-vocabulary file, between its
  two fences, and nothing else from that file went in
- only conditional shot rows were dropped, and no sentence in the block was rewritten
- the fit step adjusted SUBJECT and LOCATION only
- the prompt carries no percentage, no CV, no "N of ten banked ads", and no sentence reporting a
  measurement rather than instructing the ad
- the V.4a pacing block is present after the transcript with the format's own DELIVERY LINE as
  its last line, and is omitted entirely for a format where nobody speaks
- the V.4b director block is the final text, verbatim, with the format's name in it

**Content**
- the prompt STATES a shot count and does NOT contain a shot list, a span, a per-shot framing or
  any sentence beginning "shot 6"
- every spoken line matches the approved transcript word for word, and each is in quotation marks
- no block restates the format definition, shot types, performance, rhythm or bans, because all
  five are inside the prompt block
- LOCATION states physical facts about the place, not a mood or a lighting design
- nothing describes how a body moves, per V.3
- no transition effect was requested anywhere
- swapping the product out would NOT leave a working ad
- nothing was copied, quoted or adapted from a bank example

**The call**
- `omni_reference`, 9:16, duration 30 or less
- the reference stack carries the raw product photo, every in-use state the ad shows, and the
  anchor when one exists
- the anchor spend and the video spend each got their own explicit yes
- the output is versioned and no previous render was overwritten
