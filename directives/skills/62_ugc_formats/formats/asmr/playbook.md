---
name: ugc-asmr
description: "Build a sound-led ASMR or satisfying-demo UGC video ad, where the product's own textures and sounds carry the whole ad and nobody speaks, rendered as a single 25-second-or-less Seedance 2.5 clip at 1080p 9:16. Trigger ONLY on /pm-ugc-asmr or clearly ASMR-specific language such as 'asmr ad', 'satisfying demo', 'sound led product video', 'crunchy product sounds'. Generic UGC requests belong to /pm-ugc, which shows the format menu and routes; never claim a request that does not name this format. This format has no script at all, and narration disqualifies it. If the user names a different skill, command, plugin, or tool for the job, or is building or testing their own skill, do not trigger this skill; use what they named instead."
---

# ASMR and satisfying-demo UGC ads

The product's materials, motions and sounds ARE the ad. It removes the doubt "what is this
actually like to touch and hear", and it asks the viewer to trust their own senses. Nobody
speaks, nobody is introduced, nothing is argued.

Run the stages in order. Each engine owns its stage and nothing else.

| Stage | File |
|---|---|
| **What this format IS, read first** | `references/format-spec.md` |
| The run, folder to delivery | `../../../_shared/ugc_run_engine.md` |
| The sound plan, in place of a script | `../../../_shared/ugc_script_engine.md` |
| The anchor still | `../../../_shared/ugc_image_engine.md` |
| The render prompt and the call | `../../../_shared/ugc_video_engine.md` |
| **How this format is SHOT, the measured assembly** | `references/shot-vocabulary.md` |
| The ten study pairs, this format only | `references/recreation-prompts/index.md` |
| What a format spec must define | `../../../_shared/ugc_format_contract.md` |

## The order

1. **Read `references/format-spec.md`.** Give the brand-familiarity warning it carries, once,
   before building: ASMR measures negatively for brands the viewer does not already recognise.
   Say it plainly and continue if the user wants it.
2. **Run the run engine from R.1.** The photo audit matters more here than anywhere: this format
   lives on sensory states, and every state the ad shows needs a real photo behind it.
3. **Script engine.** `script_default` is `forbidden`, so U.2 sends you straight to U.3 and this
   skill produces a **sound plan** instead of a script: the ordered sounds the ad is built on,
   each tied to the beat that makes it and the action that produces it.
4. **Video engine phase 1.** Read all ten pairs in this skill's own bank for HOW THIS FORMAT IS
   SHOT. Then set the shot COUNT from `shots_per_10s` times the duration, and decide which
   conditional shot-type rows this product supports. **Do NOT write a shot list.** The video
   model directs the ad; this skill teaches it the format by pasting that file's
   PROMPT BLOCK, and only the prompt block, into the render prompt.
5. **Image engine phase 1, I.1 to I.3.** Write the anchor prompt, no render yet. The anchor
   locks the PRODUCT, not a person. No face is needed and none should be added.
6. **GATE 1, THE PLAN. Free.** The script, the shape of the ad and the anchor prompt in ONE
   message, with the shot count stated. No shot list; the model builds the shots. The last
   moment anything is free.

7. **GATE 2, the anchor. Costs money.** Image engine I.4 to I.5 renders the prompt the user
   already approved.
8. **Video engine phase 2, then GATE 3.** Assemble the full render prompt from the approved
   script, shape and anchor, show it with the exact price, and render on an explicit
   yes.
9. **Deliver per R.8** into `05_UGC_Prompts/formats/asmr/<concept>/`, including `post-production.md`.

## The laws, inherited by every run

**Audio on, music never.** Here that is not a restriction, it is the entire point: the product's
own sound is the content. `generate_audio` stays true. A wordless ad is sound-carried, never
silent.

**No text in the render.** The recommendation goes in `post-production.md`.

**The spend law.** Nothing that costs money without an immediately preceding yes.

**Bank isolation.** Own bank only, never copied.

**One render.** Seedance 2.5, `omni_reference`, 1080p, 9:16, 4 to 30 seconds.

## What makes this format itself

**The product is on screen as the source of every sound.** A sound with no visible cause is a
dubbed sound and fails the format.

**No narration, no whisper voiceover, no words.** The moment a voice explains what you are
hearing, the sound stops being the content and becomes a soundtrack. A concept that needs
explaining belongs in `/pm-ugc-tutorial` or `/pm-ugc-expert`.

**Macro or close framing throughout.** Nothing is satisfying at arm's length.

**There is no CTA in this ad, and that is correct.** No speech and no rendered text means the ad
ends on the product presented cleanly, and the call to action lives in the caption the user
writes when they post. Say so at handover rather than implying the video asks for something.
