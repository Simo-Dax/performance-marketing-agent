---
name: ugc-testimonial
description: "Build a Testimonial UGC video ad, one customer speaking to camera about their own experience, rendered as a single 30-second-or-less Seedance 2.5 clip at 1080p 9:16. Trigger ONLY on /pm-ugc-testimonial or clearly testimonial-specific language such as 'testimonial video', 'customer review ad', 'honest review ad', 'someone talking about my product'. Generic UGC requests belong to /pm-ugc, which shows the format menu and routes; never claim a request that does not name this format. Requires a VOC document: the spoken lines come from real customer language and are never invented. If the user names a different skill, command, plugin, or tool for the job, or is building or testing their own skill, do not trigger this skill; use what they named instead."
---

# Testimonial UGC ads

One person tells the viewer what changed for them. This format removes the doubt "did this work
for someone like me", and it asks the viewer to trust a peer's lived experience. Nothing is
proven on screen; someone is believed.

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
2. **Run the run engine from R.1.** Folder, then homework, then a proposal rather than an
   interview, then the photo audit, then the duration, then the path.
3. **Script engine, U.0 to U.10.** The words come from the VOC. This format is `voc-required`:
   with no VOC document on file, stop and route to `/voc`. Do not write a customer from
   imagination. The words do not get their own approval round; they are approved at GATE 1 as
   part of THE PLAN.
4. **Video engine phase 1.** Read all ten pairs in this skill's own bank for HOW THIS FORMAT IS
   SHOT. Then set the shot COUNT from `shots_per_10s` times the duration, and decide which
   conditional shot-type rows this product supports. **Do NOT write a shot list.** The video
   model directs the ad; this skill teaches it the format by pasting that file's
   PROMPT BLOCK, and only the prompt block, into the render prompt.
5. **Image engine phase 1, I.1 to I.3.** Write the anchor prompt, no render yet. The anchor
   locks the speaker and the product together.
6. **GATE 1, THE PLAN. Free.** The script, the shape of the ad and the anchor prompt in ONE
   message, with the shot count stated. No shot list; the model builds the shots. The last
   moment anything is free.

7. **GATE 2, the anchor. Costs money.** Image engine I.4 to I.5 renders the prompt the user
   already approved.
8. **Video engine phase 2, then GATE 3.** Assemble the full render prompt from the approved
   script, shape and anchor, show it with the exact price, and render on an explicit
   yes.
9. **Deliver per R.8** into `05_UGC_Prompts/formats/testimonial/<concept>/`, including
   `post-production.md`.

## The laws, inherited by every run

**Audio on, music never.** Every render carries diegetic sound only: the voice, the room tone,
the handling. Music is added by the user afterwards.

**No text in the render.** The recommendation goes in `post-production.md`; the burn-in is the
user's editor.

**The spend law.** Nothing that costs money is generated without a clear, specific, immediately
preceding yes. Every retry is a new spend and needs its own.

**Bank isolation.** This skill reads only its own `references/recreation-prompts/`. Never another
format's, and never copied.

**One render.** Seedance 2.5, `omni_reference`, 1080p, 9:16, 4 to 30 seconds. No stitching, no
segmentation. The cuts live inside the one prompt.

## What makes this format itself

The **Specific beat** carries the ad: one concrete detail only a real user would say. Without it
this is an endorsement, and viewers discount endorsements automatically. If time is short, cut
the Verdict, never the Specific.

The product does not appear before the Turn. The speaker never claims expertise or a credential;
a speaker who cites one belongs in `/pm-ugc-expert`. Polish is the enemy: a testimonial that sounds
produced triggers the reflex that recognises an ad, and the trust goes with it.
