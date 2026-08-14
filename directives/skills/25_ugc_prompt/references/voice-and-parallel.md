# Voice model + parallel rendering (UGC factory)

How the one uploaded voice clip becomes a consistent voice across every clip, why
naive batching FAILS SILENTLY on Higgsfield, and the unique-cut design that makes
the whole batch render in PARALLEL. Hard-won on the podcast factory; the physics
are identical here because both skills ride the same Seedance-2.0-with-audio-reference
backend.

## The voice model

- The member uploads ONE voice clip, max 15 seconds. Seedance is given a cut of that
  voice as the `audio` reference and speaks each generation's scripted words in that
  voice, with lip-sync (talking shots) or as voiceover (b-rolls), audio baked into the
  mp4. No TTS, no clone step, no separate track.
- Same source voice on every generation → the same voice across all clips automatically.

## The `_sfx` gotcha (why naive batching fails) — the big one

Higgsfield **fingerprints the SPEECH CONTENT** of an uploaded audio and lazily
transforms it into a processed `_sfx.wav` variant after its first use. Any later or
parallel generation that resolves to that transformed variant **fails SILENTLY** —
`status: failed`, empty error string, no credits charged.

Critically, the fingerprint is on the speech itself, so these all **collapse to the
same poisoned asset**:
- re-uploading the same file (including the CLI auto-uploading a local path per call),
- padding trailing silence or adding noise,
- an explicit fresh `upload create` id.

Symptom to check on any job: `params.medias[role=audio].data.url` ends in `_sfx.wav`
→ that job is doomed (or its audio silently degraded). Treat it as failed.

**This supersedes the old guidance "re-upload the voice fresh before each generation"
— re-uploading does NOT avoid the collision.** The old advice sometimes appeared to
work only because the first use of an upload is safe; the second render against the
same speech fingerprint is the one that dies.

## The fix: a unique voice cut per generation

Give every generation a genuinely different speech fingerprint of the SAME voice:

- `scripts/make_voice_cuts.py` re-cuts the member's clip once per generation with a
  **different trim offset + a slight tempo-shift** (`ffmpeg -ss <offset> -af
  "atempo=<f>"`, ~0.93–1.09, pitch preserved → the voice and timbre are unchanged,
  only the fingerprint differs). Output is clean mono 44.1 kHz `pcm_s16le` WAV,
  capped at 14.5s so a slow tempo never stretches past the 15s reference limit.
- Each generation passes its OWN cut as `--audio` (Path B) / the audio slot (Path A/D).
- With distinct fingerprints, the whole batch submits **in parallel** with no `_sfx`
  collision. Failed jobs cost nothing, so a retry with a fresh re-cut is free.

Operational notes:
- A re-cut that genuinely changes the speech (trim + tempo) reliably lands on a fresh,
  non-`_sfx` asset; tiny trailing-silence tweaks do NOT (they fingerprint-match).
- Tempo shifts inside ~0.93–1.09 with pitch preserved do not change how the cloned
  voice sounds in the render (proven in production on the podcast factory).
- **Path C (fal.ai) does not have this bug.** On fal you upload the ORIGINAL voice
  clip once and reuse the returned URL across every generation; the cuts are a
  Higgsfield-path (A/B/D) requirement. Payloads targeting fal set `"backend": "fal"`
  so the validator skips the voice_cut check.

## The parallel pattern (what `render_parallel.py` does)

1. Submit every generation WITHOUT `--wait`, capturing each job-id string (a
   `--wait` can falsely time out on >5-minute renders and return `[]` even though the
   job completes server-side; `generate create` without `--wait` returns a JSON array
   of bare id STRINGS — parse `result[0]`).
2. Poll each id with `generate get <id> --json` every ~20s (renders take ~3–6 min).
3. Download each completed `result_url` to `gens/<gen_id>.mp4`.
4. Retry only failures (including completed-but-`_sfx` jobs) with a FRESH voice cut —
   failed jobs cost nothing. Give up after 2 retries and name the survivor.
5. Recover a "lost" job (a timed-out wait) via `generate list --json` /
   `generate get <id>` — downloading a completed job is free.

Submit a few at a time (the script staggers 1s between submissions) — the workspace
rate-limits around 8 concurrent.

## render_plan.json (the batch contract)

Authored by the orchestrator from the approved pacing table, consumed by
`make_voice_cuts.py`, `render_parallel.py`, and `whisper_cut.py`:

```
{ "concept": "<slug>",
  "resolution": "1080p",
  "inputs": { "face": "inputs/face.png", "body": "inputs/body.png",
              "product": "inputs/product.png", "voice": "inputs/voice.mp3" },
  "generations": [
    { "gen_id": "hook_reel_A", "role": "hook_reel", "duration": 8,
      "voice_cut": "hook_reel_A.wav",
      "images": ["face", "body", "product"],
      "prompt_file": "prompts/hook_reel_A.txt",
      "lines": [ {"line": "<hook 1 exact spoken line>", "clip": "hook_1"},
                 {"line": "<hook 2 exact spoken line>", "clip": "hook_2"} ] },
    { "gen_id": "body_01", "role": "body", "duration": 5,
      "voice_cut": "body_01.wav", "images": ["face", "body"],
      "prompt_file": "prompts/body_01.txt",
      "lines": [ {"line": "<pain line>", "clip": "body_01"} ] },
    { "gen_id": "body_04", "role": "body", "duration": 5,
      "voice_cut": "body_04.wav", "images": ["face", "body", "product"],
      "prompt_file": "prompts/body_04.txt",
      "lines": [ {"line": "<CTA line>", "clip": "body_04", "tail": 0.6} ] },
    { "gen_id": "broll_A", "role": "broll", "duration": 4,
      "voice_cut": "broll_A.wav", "images": ["product"],
      "prompt_file": "prompts/broll_A.txt",
      "lines": [ {"line": "<bA voiceover line>", "clip": "broll_A"} ] }
  ] }
```

- `images` entries are keys into `inputs` ("face", "body", "product") or literal paths.
  Character generations list face + body (+ product when on screen); product-only
  b-rolls list product only. The voice never appears here — it rides as the audio cut.
- `lines[].clip` names the output clip `clips/<clip>.mp4` that `whisper_cut.py` writes.
  A hook reel has two lines → two clips; everything else has one.
- `lines[].tail` overrides the cut tail for that line (set ~0.6 on the CTA so the ad
  breathes at the end; everything else uses the default 0.20s).
- The hook-first checkpoint renders one generation alone:
  `python3 "$SCRIPTS/render_parallel.py" "$WORK/render_plan.json" "$WORK" "$WORK/voice_cuts" "$WORK/gens" hook_reel_A`.
