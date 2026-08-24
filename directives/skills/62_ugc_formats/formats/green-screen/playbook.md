---
name: ugc-green-screen
description: "Build Green Screen Reaction footage, a creator talking to camera in a clean keyable environment so evidence can be composited behind them afterwards, rendered as a single 30-second-or-less Seedance 2.5 clip at 1080p 9:16. Trigger ONLY on /pm-ugc-green-screen or clearly Green Screen Reaction-specific language such as 'green screen ad', 'reacting to a screenshot', 'reaction to a review'. Generic UGC requests belong to /pm-ugc, which shows the format menu and routes; never claim a request that does not name this format. This skill produces the footage only: it never removes a background and never generates evidence. If the user names a different skill, command, plugin, or tool for the job, or is building or testing their own skill, do not trigger this skill; use what they named instead."
---

# Green Screen Reaction UGC ads

A creator reacting to external evidence. This skill renders ONLY the person, cleanly and keyably, and hands over a timed note about what belongs behind them.

Run the stages in order. Each engine owns its stage and nothing else.

| Stage | File |
|---|---|
| **What this format IS, read first** | `references/format-spec.md` |
| The run, folder to delivery | `../../../_shared/ugc_run_engine.md` |
| The words | `../../../_shared/ugc_script_engine.md` |
| The anchor still | `../../../_shared/ugc_image_engine.md` |
| The render prompt and the call | `../../../_shared/ugc_video_engine.md` |
| **How this format is SHOT, the measured assembly** | `references/shot-vocabulary.md` |
| The ten study pairs, this format only | `references/recreation-prompts/index.md` |
| What a format spec must define | `../../../_shared/ugc_format_contract.md` |

## The order

1. **Read `references/format-spec.md`.** Its facts block supplies every parameter the engines
   ask for. Never guess one, never borrow one from another format.
2. **Run the run engine from R.1.** Folder, homework, a proposal rather than an interview, the
   photo audit, the duration, the path.
3. **Script engine.** Speech is REQUIRED; a silent reaction is not a reaction. Every beat must
   play as complete footage on its own, because the background may not be there when it is
   watched.
4. **Video engine phase 1.** Read all ten pairs in this skill's own bank for HOW THIS FORMAT IS
   SHOT. Then set the shot COUNT from `shots_per_10s` times the duration, and decide which
   conditional shot-type rows this product supports. **Do NOT write a shot list.** The video
   model directs the ad; this skill teaches it the format by pasting that file's
   PROMPT BLOCK, and only the prompt block, into the render prompt.
5. **Image engine phase 1, I.1 to I.3.** Write the anchor prompt, no render yet. The anchor
   locks the CREATOR only. No evidence is generated, referenced as an image, or attached.
6. **GATE 1, THE PLAN. Free.** The script, the shape of the ad and the anchor prompt in ONE
   message, with the shot count stated. No shot list; the model builds the shots. The last
   moment anything is free.

7. **GATE 2, the anchor. Costs money.** Image engine I.4 to I.5 renders the prompt the user
   already approved.
8. **Video engine phase 2, then GATE 3.** Assemble the full render prompt from the approved
   script, shape and anchor, show it with the exact price, and render on an explicit
   yes.
9. **Deliver per R.8** into `05_UGC_Prompts/formats/green-screen/<concept>/`, including
   `post-production.md`.

## The laws, inherited by every run

**Audio on, music never.** Diegetic sound only. Music is added by the user afterwards.

**No text in the render.** The recommendation goes in `post-production.md`; the burn-in is the
user's editor.

**The spend law.** Nothing that costs money is generated without a clear, specific, immediately
preceding yes. Every retry is a new spend and needs its own.

**Bank isolation.** This skill reads only its own `references/recreation-prompts/`. Never another
format's, and never copied.

**One render.** Seedance 2.5, `omni_reference`, 1080p, 9:16, 4 to 30 seconds. No stitching, no
segmentation. The cuts live inside the one prompt.

## What makes this format itself

**The bank shows finished composites; you render only the person.** All ten banked ads describe
the screens and dashboards behind the creator, because that is what the finished ad contained.
Read those as what the user will composite later, never as prompt material. Never write a
background into the prompt: whatever you describe behind them gets rendered behind them, and the
footage stops being keyable.

**Centered, clean, keyable, and watchable as-is.** Gestures stay generic and body-centred: never point at a specific spot, because the thing being pointed at may not exist yet and may end up somewhere else. Never say 'as you can see here' over a frame with nothing in it. No screenshot, review card or chart is ever generated, in the render or as a reference.
