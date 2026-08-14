# Seedance 2.0 facts + LOCKED model (read first, this overrides everything except generation-architecture.md on structure)

This is the single source of truth for backend facts. It is locked by the product owner. Do NOT reintroduce a 15s generation, an external voice spine, or a TTS step. Build to THIS model exactly. B-rolls are voiceover clips that may be product-only or feature the character (see the character model below). For how generations assemble into the four ads, see `references/generation-architecture.md`.

## The inputs (uploaded once per skill run, reused on EVERY generation)
1. ONE face image of the character.
2. ONE body image of the character.
3. ONE product image. Used on every shot where the product is on screen AND on every b-roll.
4. ONE voice clip, max 15 seconds. The member creates this (e.g. on ElevenLabs). How they make it is NOT our concern.

## The voice model (LOCKED)
- The SAME voice is the reference on EVERY generation: every hook, every body shot, and every b-roll (as the voiceover). Seedance analyzes it and generates each shot's spoken line in a voice that sounds like the clip, saying the new words.
- **On Higgsfield paths (A/B/D), each generation carries its OWN uniquely-fingerprinted CUT of that voice** (`make_voice_cuts.py`: a distinct trim offset + slight tempo-shift, pitch preserved — the voice is unchanged, only the speech fingerprint differs). This is NOT optional: Higgsfield fingerprints the speech content and lazily poisons a reused audio into a `_sfx.wav` variant that makes later generations FAIL SILENTLY. Re-uploading the same clip does NOT avoid it — the fingerprint is on the speech. See `references/voice-and-parallel.md`. On Path C (fal) the bug does not exist; upload the original clip once and reuse its URL.
- Because every cut is the same voice, the voice stays consistent automatically. Nothing to "stitch", no separate track.
- Unique cuts also make the batch PARALLEL-SAFE: submit every generation at once (`render_parallel.py`), poll by job id, retry failures with a fresh cut for free.
- AUDIO IS ENABLED ON EVERY GENERATION, b-rolls included (the b-roll voiceover uses the same voice).
- The only voice limit: the reference is max 15 seconds (cuts are capped at 14.5s). The member's job.
- NEVER a clone step, a voice-ID step, a TTS step, an external spine, or force-muting at assembly.

## The character model (LOCKED)
- Re-send the SAME face image + body image bytes on every CHARACTER generation (+ the product image when the product is on screen). Identical bytes every time, never re-cropped. This is the identity anchor; not reference-video chaining.
- **B-ROLLS ARE VOICEOVER, NEVER A TALKING HEAD.** A b-roll is a product-focused clip carried by the voiceover, never the character talking to camera. It can, and by default should, feature the character: the character's own hands holding and filming the product (face out of frame), or the character using or demonstrating the product under the voiceover. A CHARACTER b-roll carries the same face + body bytes + the product image + the voice clip. A PRODUCT-ONLY b-roll (product held by an anonymous hand or standing on a surface) carries the product image + the voice clip ONLY, no face, no body. Either way the words are voiceover, never lip-synced dialogue.

## Seedance 2.0 hard limits (the ONLY limits that matter)
- **UNDER 10 seconds PER generation.** Every generation is an integer 4 to 9 seconds. There is NO 15s generation in this factory. A longer ad is many short generations concatenated.
- duration is an explicit integer 4 to 9. Never auto, never 10+.
- Vertical 9:16 for UGC.
- **Resolution 1080p** (the default render resolution for this factory).
- Cost is per second, about **9 credits/sec at 1080p** (verified). Batching beats into one generation saves nothing. The leverage is reusing the body core and the b-roll pool, and fanning unique hooks.
- A generation may contain multiple SCENES described in the prompt (Seedance cuts them; there is no multi-shot parameter — you set only the total seconds). Multi-scene generations are split into clips afterward.
- Reference media attached: face + body + product on character shots and character b-rolls; product + voice only on product-only b-rolls; the voice clip on every generation.

## PACING is the make-or-break (HIGHEST PRIORITY) — and the rule is SLIGHTLY FAST
The thing that breaks the factory is getting a generation's length wrong relative to its words.
- Seedance STRETCHES the spoken line to fill the duration you request. So the duration you choose IS the talking speed. There is no clipping to protect against, and therefore no reason to leave "breath": a too-long duration just makes the delivery DRAG (slow, sluggish), and a too-short one rushes.
- Target a fast, punchy UGC pace: about **3.5 spoken words/sec**.
- The method (LOCKED): `requested_seconds = round(word_count / 3.5)`. Add 1 to 2 seconds ONLY for genuine on-screen ACTION (the hooks: a bottle dump, a slam, a toss). Add NOTHING to talking body shots or b-rolls — the voiceover fills the time.
- Every generation must land UNDER 10 seconds. If content needs 10s or more, split it into more generations.
- Do NOT use a fill-ratio "breath buffer". That was the old, draggy model. The new model is a direct ~3.5 wps target.
- The skill SHOWS the member each generation's words, seconds, and resulting wps, and confirms every one is under 10s at ~3.5 wps BEFORE generating.

## Andromeda structure (LOCKED)
- BEFORE Andromeda (dead): one body, only the hook swapped, every variant otherwise identical. Do NOT do this.
- AFTER Andromeda (required): 4 ads that are genuinely DIFFERENT TIMELINES. Distinctness comes from **4 UNIQUE hooks (one per ad, different angle + different kind of visual action) + a B-ROLL-COUNT LADDER (0, 1, 2, 2)** of the 2 shared b-rolls, inserted at spaced points. There is NO hook-length ladder; hooks are uniformly short.
- **EVERY AD ENDS ON THE CTA.** The body's last beat is the CTA; b-rolls are inserted only in the middle, never after the CTA. V3 and V4 both use both b-rolls but at different placements.

## Cutting + verification (LOCKED, all free — no credits)
- After the renders land, every generation is CUT WORD-ACCURATELY with faster-whisper (`whisper_cut.py`): the known script lines are aligned to the recognized words, each line becomes one clip ending ~0.2s after its last word (the CTA gets ~0.6s so the ad breathes). This kills dead tails and drag, and it is how hook reels are split into their hook clips (word-aligned, not scene-detect-guessed). The FIRST line of a generation keeps the clip's natural head so a hook's visual action is never chopped.
- The same pass prints a per-line MATCH RATIO (recognized words vs the script). A low ratio means Seedance garbled the line — LISTEN before assembly; only genuinely wrong words justify proposing a re-render (the member's call, fresh yes).
- Every clip is FRAME-CHECKED (`frame_check.sh` contact sheets) before stitching: character on-model, hook action rendered, b-roll has no talking face, no text in frame, product at believable scale. Fix by re-cutting to the good footage when possible; a re-render costs credits and needs its own fresh yes.

## Assembly (LOCKED)
- Each ad = concatenate its (already word-accurately cut) clips in order: hook, body beats, with b-rolls inserted at the ad's chosen MIDDLE points. The CTA body beat is always last.
- Every clip already contains its own consistent voice audio, so KEEP each clip's audio and concatenate. Do NOT force-mute. Do NOT lay a separate spine.
- Loudness-normalize the final cut to about -14 LUFS. Optional short picture crossfade at cuts.
- Output 9:16 1080p MP4 per ad, each 25 to 45 seconds, plus the raw clips so the member can re-cut.
- VERIFY each finished ad by transcribing it and reading back the recognized line order against the approved transcript.
