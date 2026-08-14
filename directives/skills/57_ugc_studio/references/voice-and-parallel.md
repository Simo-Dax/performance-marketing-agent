# VOICE CUTS & PARALLEL RENDERING — UGC Studio

How one member voice clip (≤15s) becomes a consistent voice across every
generation, why naive batching fails SILENTLY on Higgsfield, and the unique-cut
design that makes a whole render_plan submit in PARALLEL. Every claim here is
production-verified physics of the Seedance-2.0-with-audio-reference backend.

## The voice model

- The member uploads ONE voice clip, max 15 seconds. Seedance receives a cut of
  that voice as the audio reference and speaks each generation's `lines[]` in that
  voice — lip-synced on `beat_type: "talking"` gens, voiceover on the b-roll types —
  with audio baked into the mp4. No TTS, no clone step, no separate track.
- Same source voice on every generation → the same voice across all clips for free.

## The `_sfx` dedup physics (why naive batching fails)

Higgsfield **fingerprints the SPEECH CONTENT** of an uploaded audio and lazily
transforms it into a processed `_sfx.wav` variant after its first use. Any later or
parallel generation that resolves to that transformed variant **fails SILENTLY** —
`status: failed`, empty error string, no credits charged — or completes with
silently degraded audio.

Because the fingerprint is on the speech itself, these all **collapse to the same
poisoned asset**:
- re-uploading the same file (including a CLI auto-uploading a local path per call),
- padding trailing silence or adding noise,
- an explicit fresh `upload create` id.

So "re-upload the voice fresh before each generation" is a trap: the FIRST use of
any upload is safe, which makes the advice look right exactly once — the second
render against the same speech fingerprint is the one that dies.

**Detection** — on any job, inspect the audio media URL:
`params.medias[role=audio].data.url` ending in `_sfx.wav` means that job rode the
poisoned variant. Treat it as failed **even when `status` is `completed`** — a
completed-but-`_sfx` job is a retry, never a download.

## The fix: one uniquely-fingerprinted cut per generation

Give every generation a genuinely different speech fingerprint of the SAME voice.
`make_voice_cuts.py` reads render_plan.json and, for each `entries[]` object with
`kind: "gen"` that carries a `voice_cut`, re-cuts `inputs.voice` with a distinct
**trim offset + tempo-shift**:

    ffmpeg -ss <offset> -i voice -af "atempo=<f>,aresample=44100" \
           -ar 44100 -ac 1 -c:a pcm_s16le -t 14.5 voice_cuts/<gen_id>.wav

- `atempo` 0.93–1.09, **pitch preserved** — the voice and timbre are unchanged in
  the render (production-proven); only the fingerprint differs.
- Output: clean mono 44.1 kHz `pcm_s16le` WAV.
- **Capped at 14.5s** so a slow tempo never stretches past the 15s reference limit
  (a full 15s clip at atempo 0.93 runs 16.1s — over the limit).
- A recut must genuinely change the speech (trim + tempo). Trailing-silence tweaks
  or noise beds do NOT — they fingerprint-match the spent asset.

Each generation passes its OWN `voice_cut` WAV as the audio reference (`--audio`
on the CLI path, the audio slot on manual/web paths). Silent gens (no `lines[]`)
carry no `voice_cut` and no audio reference at all.

## Why unique cuts make full parallel submission safe

With distinct fingerprints there is nothing shared for the dedup to collide on, so
the whole plan submits at once. `render_parallel.py`:

1. Submits every generation WITHOUT `--wait`, capturing each job-id string (a
   `--wait` can falsely time out on >5-minute renders and return `[]` even though
   the job completes server-side; no-wait submits return `["<jobid>"]` — parse
   element 0). Stagger ~1s between submissions to stay under the workspace rate
   limit. A gen whose valid `gens/<gen_id>.mp4` already exists is SKIPPED, not
   resubmitted (idempotent dispatch — fan-out shared bodies render once; a re-roll
   starts by moving the old file aside).
2. Polls each id (`generate get <id> --json`) every ~20s; renders take ~3–6 min.
3. Downloads each completed `result_url` to `gens/<gen_id>.mp4`.
4. Retries failures — including completed-but-`_sfx` jobs — with a FRESH recut.
   Failed jobs cost nothing, so retries are free. Give up after 2 retries and name
   the survivor.
5. Recovers a "lost" job (timed-out wait) via `generate list` / `generate get` —
   downloading an already-completed job is free.

The one serial exception is by design: the plan's `is_identity_checkpoint` gen
renders ALONE first (pass its `gen_id` as the argv subset) so an identity mismatch
costs one gen, not the batch. On approval, everything else fans out in parallel.

## The fresh-recut law: a used fingerprint is SPENT

Every submission consumes its cut's fingerprint. ANY resubmission — dedup retry,
content re-roll, member-requested re-render, a re-render days later — gets a fresh
recut first. Never resubmit an already-used WAV; it is the `_sfx` collision again,
one render delayed.

**The retry salt.** A retry's offset/tempo fold in **hash(gen_id) + attempt
number**, so the new cut is unique per (generation, attempt) BATCH-WIDE: two
different generations each retried once must not derive byte-identical cuts from
the same arithmetic (identical bytes = identical fingerprint = the same collision
reborn). And if the recut's ffmpeg fails, the retry is abandoned — the old
poisoned cut must never ride again as a fallback.

## The Path C (fal) exemption

fal.ai has **no dedup bug**: the ORIGINAL voice clip uploads once and the returned
URL is reused across every generation. Plans with `"backend": "fal"` therefore omit
`voice_cut` on their gens (the validator relaxes the check, per pipeline-contracts
§1) — cuts are a Higgsfield-path requirement only. The fresh-recut law does not
apply on fal either; re-rolls reuse the same uploaded URL.

## Contract touchpoints (pipeline-contracts.md is authoritative)

- `render_plan.json` → `inputs.voice` (the one source clip), and per `kind: "gen"`
  entry: `gen_id`, `voice_cut`, `lines[]`, `duration`, `images`, `prompt_file`,
  `is_identity_checkpoint`, plus plan-level `backend` and `resolution`.
- Canonical argv:
  `python3 $SCRIPTS/make_voice_cuts.py render_plan.json $WORK voice_cuts/`
  `python3 $SCRIPTS/render_parallel.py render_plan.json $WORK voice_cuts/ gens/ [gen_id ...]`
