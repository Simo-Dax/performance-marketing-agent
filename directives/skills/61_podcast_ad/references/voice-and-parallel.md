# Voice model + parallel rendering (image + voice only)

The inverse of a video-chained approach: there is **NO video reference**. Each generation is anchored by the host's **reference image** (identity) + a **re-cut of the host's voice clip** (voice). That's it.

## The voice model
- The member uploads ONE voice clip (10–15s) per host. Seedance is given that voice as the `audio` reference and speaks the scripted line in it, with lip-sync and audio baked into the mp4. No TTS, no clone step, no separate track.
- Same host across many generations → same voice automatically (it's the same source clip).

## The `_sfx` gotcha (why naive parallel fails) — the big one
Higgsfield **fingerprints the SPEECH content** of an uploaded audio and lazily transforms it into a processed `_sfx.wav` variant after its first use. Any later/parallel generation that resolves to that transformed variant **fails SILENTLY** — `status: failed`, empty error string, no credits charged. Critically, the fingerprint is on the speech, so trailing-silence padding, added noise, re-upload, and even an explicit `upload create` id all **collapse to the same poisoned asset**. Symptom to check: `params.medias[role=audio].data.url` ends in `_sfx.wav` → that job is doomed.

## The fix that makes PARALLEL work: a unique voice cut per generation
Give every generation a genuinely different speech fingerprint of the SAME voice, so no two generations resolve to the same asset:
- Re-cut the host's voice with a **different trim window + a slight tempo-shift** per generation (`ffmpeg -ss <offset> -af "atempo=<f>"`, ~0.94–1.11, pitch preserved → the voice/timbre is unchanged, only the fingerprint differs).
- Encode clean: mono, 44.1 kHz, `pcm_s16le` WAV.
- Pass each generation its OWN cut as `--audio` (Path B) / `audio` (Path C).

With distinct fingerprints, all generations can be submitted **in parallel** with no `_sfx` collision. `scripts/make_voice_cuts.py` produces one unique cut per generation from `render_plan.json`.

Operational notes:
- A re-cut that genuinely changes the speech (trim + tempo) reliably lands on a fresh, non-`_sfx` asset; tiny trailing-silence tweaks do NOT (they fingerprint-match).
- Failed jobs cost nothing, so retrying a failed generation with a fresh cut is free.
- If a host needs many generations, that's fine — each just gets its own cut. There is no per-voice usage cap once cuts are unique.

## Why no video reference
Re-sending the locked image bytes is the identity anchor. A video reference is unnecessary here and adds failure surface; it is never used. (A reference video also competes with the audio reference and complicates the under-15s media limits.) Image + voice cut only.
