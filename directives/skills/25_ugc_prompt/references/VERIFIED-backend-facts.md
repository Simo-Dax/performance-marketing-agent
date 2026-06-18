# Seedance 2.0 facts + LOCKED model (read first, this overrides everything except generation-architecture.md on structure)

This is the single source of truth for backend facts. It is locked by the product owner. Do NOT reintroduce a 15s generation, an external voice spine, a TTS step, or character-present b-rolls. Build to THIS model exactly. For how generations assemble into the four ads, see `references/generation-architecture.md`.

## The inputs (uploaded once per skill run, reused on EVERY generation)
1. ONE face image of the character.
2. ONE body image of the character.
3. ONE product image. Used on every shot where the product is on screen AND on the product-only b-rolls.
4. ONE voice clip, max 15 seconds. The member creates this (e.g. on ElevenLabs). How they make it is NOT our concern.

## The voice model (LOCKED)
- The SAME voice clip is passed as the VOICE REFERENCE on EVERY generation: every hook, every body shot, and every product-only b-roll (as the voiceover).
- Seedance analyzes that clip and generates each shot's spoken line in a voice that sounds like the clip, saying the new words.
- Because the reference is identical on every generation, the voice stays consistent automatically. Nothing to "stitch", no separate track.
- AUDIO IS ENABLED ON EVERY GENERATION, b-rolls included (the b-roll voiceover uses the same clip).
- The only voice limit: the reference clip is max 15 seconds. The member's job.
- NEVER a clone step, a voice-ID step, a TTS step, an external spine, or force-muting at assembly.

## The character model (LOCKED)
- Re-send the SAME face image + body image bytes on every CHARACTER generation (+ the product image when the product is on screen). Identical bytes every time, never re-cropped. This is the identity anchor; not reference-video chaining.
- **B-ROLLS ARE PRODUCT-ONLY.** A b-roll carries the product image + the voice clip ONLY — NO face, NO body, NO character on screen. It shows just the product (held by an anonymous hand or standing on a surface) with a voiceover.

## Seedance 2.0 hard limits (the ONLY limits that matter)
- **UNDER 10 seconds PER generation.** Every generation is an integer 4 to 9 seconds. There is NO 15s generation in this factory. A longer ad is many short generations concatenated.
- duration is an explicit integer 4 to 9. Never auto, never 10+.
- Vertical 9:16 for UGC.
- **Resolution 1080p** (the default render resolution for this factory).
- Cost is per second, about **9 credits/sec at 1080p** (verified). Batching beats into one generation saves nothing. The leverage is reusing the body core and the b-roll pool, and fanning unique hooks.
- A generation may contain multiple SCENES described in the prompt (Seedance cuts them; there is no multi-shot parameter — you set only the total seconds). Multi-scene generations are split into clips afterward.
- Reference media attached: face + body + product on character shots; product + voice only on b-rolls; the voice clip on every generation.

## PACING is the make-or-break (HIGHEST PRIORITY) — and the rule is SLIGHTLY FAST
The thing that breaks the factory is getting a generation's length wrong relative to its words.
- Seedance STRETCHES the spoken line to fill the duration you request. So the duration you choose IS the talking speed. There is no clipping to protect against, and therefore no reason to leave "breath": a too-long duration just makes the delivery DRAG (slow, sluggish), and a too-short one rushes.
- Target a fast, punchy UGC pace: about **3.5 spoken words/sec**.
- The method (LOCKED): `requested_seconds = round(word_count / 3.5)`. Add 1 to 2 seconds ONLY for genuine on-screen ACTION (the hooks: a bottle dump, a slam, a toss). Add NOTHING to talking body shots or product-only b-rolls — the voiceover fills the time.
- Every generation must land UNDER 10 seconds. If content needs 10s or more, split it into more generations.
- Do NOT use a fill-ratio "breath buffer". That was the old, draggy model. The new model is a direct ~3.5 wps target.
- The skill SHOWS the member each generation's words, seconds, and resulting wps, and confirms every one is under 10s at ~3.5 wps BEFORE generating.

## Andromeda structure (LOCKED)
- BEFORE Andromeda (dead): one body, only the hook swapped, every variant otherwise identical. Do NOT do this.
- AFTER Andromeda (required): 4 ads that are genuinely DIFFERENT TIMELINES. Distinctness comes from **4 UNIQUE hooks (one per ad, different angle + different kind of visual action) + a B-ROLL-COUNT LADDER (0, 1, 2, 2)** of the 2 shared product-only b-rolls, inserted at spaced points. There is NO hook-length ladder; hooks are uniformly short.
- **EVERY AD ENDS ON THE CTA.** The body's last beat is the CTA; b-rolls are inserted only in the middle, never after the CTA. V3 and V4 both use both b-rolls but at different placements.

## Assembly (LOCKED)
- Each ad = concatenate its clips in order: hook, body beats, with b-rolls inserted at the ad's chosen MIDDLE points. The CTA body beat is always last.
- Every clip already contains its own consistent voice audio, so KEEP each clip's audio and concatenate. Do NOT force-mute. Do NOT lay a separate spine.
- Loudness-normalize the final cut to about -14 LUFS. Optional short picture crossfade at cuts.
- Output 9:16 1080p MP4 per ad, each 25 to 45 seconds, plus the raw clips so the member can re-cut.
