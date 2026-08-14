# Generation Architecture (read first — the single source of truth)

How generations, clips, and the four ads fit together. If any other file conflicts with this on structure, THIS file wins. If it conflicts on backend numbers, `references/VERIFIED-backend-facts.md` wins.

## Vocabulary (get this right or the whole thing breaks)

- **Scene** = one continuous moment: one hook, one body beat, or one product shot.
- **Generation** = one Seedance render / one API call. **Must be UNDER 10 seconds (integer 4 to 9).** A generation may contain ONE scene or SEVERAL scenes described in the prompt (Seedance cuts between them — there is no multi-shot parameter; you describe the scenes and set only the TOTAL seconds).
- **Clip** = a usable segment. Every generation is CUT WORD-ACCURATELY by `whisper_cut.py` after rendering: a single-scene generation becomes one clip trimmed to end ~0.2s after its last word; a multi-scene generation (a hook reel) is split at its LINE boundaries (word-aligned, never scene-detect-guessed) into multiple clips.
- **Ad / variant** = the final assembled video = a concatenation of clips, 25 to 45 seconds, ALWAYS ending on the CTA.

The pacing rule that drives all the seconds: **requested_seconds = round(words / 3.5)** (fast, punchy; use the MEASURED wps from the brand's spy-video teardowns instead of 3.5 when they exist on disk). The duration you request IS the talking speed — Seedance stretches the line to fill it, so never pad. Add seconds ONLY for genuine on-screen action (hooks). Then pack scenes into generations until just under 10s; the word-accurate cut trims whatever slack survives (which is also why the 4s floor is safe: a 3s line in a 4s render loses its dead tail at the cut).

## 1. HOOKS

- FOUR unique hooks, one per ad. Each = a short scene (~3 to 5s): a dramatic visual action + one spoken line (~8 to 13 words). Different ANGLE each (e.g. confession, contrarian, direct claim, curiosity) AND a different KIND of visual action.
- Hooks are short, so pack ~2 hooks into ONE generation (a "hook reel"), described as two scenes with a hard cut. 4 hooks → **2 hook reels**, each under 10s (e.g. ~7s and ~8s).
- Set only the reel's TOTAL seconds: round(sum of the two hook word-counts / 3.5) + ~1 to 2s for the visual actions, kept under 10.
- After rendering, `whisper_cut.py` SPLITS each reel at its line boundary (word-aligned) into the individual hook clips → 4 hook clips. The first hook keeps the reel's natural head so its visual action is never chopped.
- **HOOK REEL A RENDERS FIRST, ALONE (the identity checkpoint).** Show the member the reel and ask "happy with the face, the voice, and the vibe?" before anything else renders — the whole batch inherits this identity, so a mismatch caught here costs one reel, not the full spend. On yes, everything else renders in PARALLEL (unique voice cuts make that safe; see `references/voice-and-parallel.md`).

## 2. BODY (the shared core)

- The framework script as beats, one spoken thought each. Typical: pain → solution → proof → CTA. **The CTA is always the last beat.**
- Each beat ~5s at the fast pace. **Each body beat is its OWN generation** (single scene) — segment beats one at a time so the packer never merges one beat's opening sentence onto the previous clip. Typical = 4 body generations.
- **THE SCENE LADDER: every body beat gets a DIFFERENT everyday setting or framing** (e.g. kitchen-counter selfie → walking outside handheld → parked-car seat → couch or desk for the CTA). Adjacent body clips are separate takes of the same person; if they share a setting and framing they butt-cut as a glitchy jump. A visible scene change per beat reads as the native UGC multi-location style, keeps every cut re-hooking the viewer, and costs nothing. Never let two ADJACENT clips in any ad's timeline share the same setting + framing.
- A beat may itself be multi-shot (e.g. a wide then a close-up of the same line) if it still fits under 10s.
- Body clips are generated ONCE and reused, whole, in all 4 ads. No splitting needed (single scenes).

## 3. B-ROLLS

- **Voiceover, never a talking head. Product-focused.** A b-roll is carried by the voice clip as a voiceover; the character never talks to camera in one. It can, and by default should, feature the character: the character's own hands holding and filming the product (one hand holds, one hand films, face out of frame), OR the character using or demonstrating the product while the voiceover plays. A product-only b-roll (product held by an anonymous hand or standing on a surface, a slow push-in or pan) is also fine.
- Attachments follow the content. A **character b-roll** attaches the same locked **face + body bytes + the product image + the voice clip** (identical to a character shot with the product on screen; the prompt keeps the character off-mic, and for a hands-only b-roll keeps the face out of frame). A **product-only b-roll** attaches the **product image + the voice clip ONLY**, no face, no body.
- The pool is exactly **2 b-rolls (bA, bB)**, each a different product framing + line. Each is its own single-scene generation (~4 to 5s). Generated once, reused.

## 4. ASSEMBLY — the four ads (b-roll-count ladder, always end on CTA)

Same body, same 2-b-roll pool. Each ad gets its own unique hook and a different NUMBER of b-rolls inserted at spaced MIDDLE points. **The CTA body beat is always last; no b-roll ever sits after it.**

| Ad | Hook | B-rolls | Timeline (ends on CTA) |
|---|---|---|---|
| V1 | hook 1 | 0 | hook → pain → solution → proof → CTA |
| V2 | hook 2 | 1 | hook → bA → pain → solution → proof → CTA |
| V3 | hook 3 | 2 | hook → bA → pain → solution → bB → proof → CTA |
| V4 | hook 4 | 2 | hook → pain → bA → solution → proof → bB → CTA |

- V3 and V4 both use both b-rolls but at DIFFERENT placements (plus different hooks), so they are distinct timelines.
- Distinctness comes from UNIQUE HOOKS + the B-ROLL COUNT/PLACEMENT — not from hook length (there is no 4/6/8/10 ladder; hooks are uniformly short).

## 5. Length consequence (known and accepted)

With 2 b-rolls + uniformly short hooks + the always-end-on-CTA rule, ad lengths fall into THREE bands: V1 shortest (0 b-rolls), V2 (1), V3 ≈ V4 (2). So three of the four lengths differ; V3 and V4 match in length but read as different ads (different hook + different b-roll placement). All four land in 25 to 45s. If a member ever wants all four lengths distinct, the only levers are varying a hook's length or giving one ad an extra body beat — otherwise this is the structure.

## 6. Generation count (typical)

**8 generations**: 2 hook reels + 4 body beats + 2 b-rolls. After the word-accurate cut (which splits the 2 hook reels) → **10 clips** (4 hooks + 4 body + 2 b-rolls). Every generation is under 10s.

## 7. The division algorithm (for ANY script)

1. Write content: 4 unique short hooks, the body beats (ending on CTA), the 2 b-roll lines (each product-only or character, voiceover).
2. Size each scene: `seconds = round(words / 3.5)` (or the measured wps); add 1 to 2s on HOOKS only for the visual action; add nothing to talking body shots or b-rolls.
3. Pack scenes into generations, each STRICTLY under 10s: hooks → reels of ~2; body → ~1 beat per gen; b-rolls → 1 per gen. Author `render_plan.json` and run `make_voice_cuts.py` (one unique voice cut per generation).
4. Render hook reel A ALONE → the member approves the identity → render everything else in PARALLEL (`render_parallel.py`).
5. CUT + VERIFY: `whisper_cut.py` splits the reels at their line boundaries and trims every clip word-accurately (~0.2s tail, ~0.6s on the CTA), printing the per-line match ratio; `frame_check.sh` contact sheets confirm the content. All free.
6. Assemble 4 ads = unique hook + shared body + 0/1/2/2 b-rolls inserted at spaced MIDDLE points → every ad ends on the CTA, all four land in 25 to 45s. Verify each by transcribing it back.

## Worked example (the canonical reference run)

8 generations, all under 10s, at the fast ~3.5 wps pace:
- Hook reel A 8s (renders FIRST, alone — the identity checkpoint) → whisper-cut → hook_1 + hook_2
- Hook reel B 9s → whisper-cut → hook_3 + hook_4
- body_01 pain 6s · body_02 solution 5s · body_03 proof 4s · body_04 CTA 5s (each its OWN generation, each a DIFFERENT setting per the scene ladder)
- broll_A 4s · broll_B 4s (product-only or character, voiceover)

→ 10 word-accurately cut clips → 4 ads, b-rolls inserted BETWEEN whole body beats:
V1 hook_1 + body (~24s) · V2 hook_2 + bA + body (~28s) · V3 hook_3 + bA + body_01–02 + bB + body_03–04 (~32s) · V4 hook_4 + body_01 + bA + body_02–03 + bB + body_04 (~31s). Body beats always play WHOLE and in order; only the b-roll insertion points differ. All 1080p, ~-14 LUFS, every one ending on the CTA.
