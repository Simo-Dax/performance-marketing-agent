---
name: ugc-unboxing
description: "Build an Unboxing UGC video ad, sealed package to reveal to first handling, rendered as a single 27-second-or-less Seedance 2.5 clip at 1080p 9:16. Trigger ONLY on /pm-ugc-unboxing or clearly Unboxing-specific language such as 'unboxing video', 'opening the package', 'first impressions unboxing'. Generic UGC requests belong to /pm-ugc, which shows the format menu and routes; never claim a request that does not name this format. If the user names a different skill, command, plugin, or tool for the job, or is building or testing their own skill, do not trigger this skill; use what they named instead."
---

# Unboxing UGC ads

The first physical encounter with the product. A curiosity loop: something is hidden, then it is not.

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
3. **Script engine.** Sound-carried by default: 8 of 10 banked ads carry no dialogue, and
   packaging sound is most of the sensory content.
4. **Video engine phase 1.** Read all ten pairs in this skill's own bank for HOW THIS FORMAT IS
   SHOT. Then set the shot COUNT from `shots_per_10s` times the duration, and decide which
   conditional shot-type rows this product supports. **Do NOT write a shot list.** The video
   model directs the ad; this skill teaches it the format by pasting that file's
   PROMPT BLOCK, and only the prompt block, into the render prompt.
5. **Image engine phase 1, I.1 to I.3.** Write the anchor prompt, no render yet. This format
   uses a PLATE SET, not one still: the container sealed, the container open, and one in-use
   plate per product the ad opens or uses. No speaking face appears in any of the ten banked
   ads.
6. **GATE 1, THE PLAN. Free.** The script, the shape of the ad and the anchor prompt in ONE
   message, with the shot count stated. No shot list; the model builds the shots. The last
   moment anything is free.

7. **GATE 2, the anchor. Costs money.** Image engine I.4 to I.5 renders the prompt the user
   already approved. The gate names how many plates and the cost of ALL of them, because a set
   costs more than a single still.
8. **Video engine phase 2, then GATE 3.** Assemble the full render prompt from the approved
   script, shape and anchor, show it with the exact price, and render on an explicit
   yes.
9. **Deliver per R.8** into `05_UGC_Prompts/formats/unboxing/<concept>/`, including
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

**The container is a box or a branded bag, and it usually holds several products.** Five of the ten
banked ads are multi-product hauls. Treat several as normal, not as an exception.

**The product is concealed until the reveal, and the reveal is the payoff.** Showing it in the hook collapses the entire loop.

**Quick front, quick handling, held reveal.** The arrival and the run through the products move
fast. The reveal beat itself gets the longest hold in the ad. Those are not in tension: everything
around the reveal moves so the reveal can be held. The photo audit matters more here than almost anywhere: the model needs to have seen the box open, or it invents what is inside.
