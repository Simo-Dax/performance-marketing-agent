# Seedance 2.0 limits & knobs — for the Pixar Ad Factory

The locked facts this skill renders against. When a backend rejects a value, verify the
live schema (`higgsfield model list` on Path B, the fal-ai MCP `get_model_schema` tool on Path C)
before improvising.

## Per-generation limits

- **Duration:** an explicit integer **4 to 9 seconds**. Every generation is UNDER 10s.
  Never auto, never 10+. Longer content = more, shorter scenes concatenated.
- **Aspect:** vertical **9:16**.
- **Resolution:** **1080p** (the default; the CLI accepts `480p`, `720p`, `1080p` — the
  verified `--resolution` values).
- **Reference inputs (verified CLI media flags: `--image`, `--start-image`,
  `--end-image`; `--video` and `--audio` are NEVER used in this skill):**
  - The **HOOK STILL** (`inputs/hook-still.png`) is attached to every non-hook
    character-visible scene as an **`--image` reference** — an IDENTITY anchor only; the
    prompt says "study the reference and lock the character exactly, but build a
    brand-new scene, do NOT copy its pose, framing or set." **A video clip is NEVER
    attached as a reference (member hard rule)** — a video ref drags its scene and
    composition onto the new shot.
  - The **product still** (`inputs/product-still.png`, the REAL product staged photoreal in
    the ad's world, generated from the real photo and approved in Step 3.5) is attached to
    the **CTA** scene, and any earlier product reveal, as a second **`--image`** reference
    (alongside the hook still). The product is never re-stylized.
  - The **hook itself** is ALWAYS image-to-video, seeded from the approved hook still
    (`inputs/hook-still.png`, generated and approved in Step 3.5) via **`--start-image`**,
    which makes the still the clip's literal first frame. Never text-to-video, and never
    plain `--image` for the hook seed.
- **Audio:** real-world ambience/foley only, **generated automatically** (the Higgsfield CLI
  has NO `--generate_audio` flag — Seedance produces the audio on its own). **No voice clip
  is ever uploaded.** Generated audio never contains music or dialogue because the prompt
  forbids them and no voice reference is attached.

## Multi-scene generations

A single generation can describe several hard-cut shots (Seedance cuts between them; there
is no multi-shot parameter — you describe the shots in the prompt and set only the TOTAL
seconds). For every NON-HOOK clip this is the **standard, not the exception**: each clip is
a fast-cut sequence of **2–3 sub-shots, a brand-new camera angle ~every 3 seconds** (the
banked winners average ~2.4s), with angle+scale tracked across the WHOLE ad so nothing
repeats. The **hook BEAT** is the opening 1–2s of scene 1 as **ONE single continuous
shot — never a flash montage** (member hard rule); the same generation then hard-cuts
into the merged adjacent line's beats (the hook line never renders solo). The whole clip
still maps to **ONE voiceover span** — do NOT split the sub-shots into separate clips;
keep them as one generation trimmed to that VO span.

Multi-beat generations are also how the **MERGE LAW** is satisfied: a VO line whose span
is under 3.5s never renders as its own clip (a 2.6s beat inside a forced 4s floor render
wastes a third of the spend) — its line merges with an adjacent line into ONE generation
that carries both beats as hard-cut sub-shots (the hook line always; the last-position
CTA is the only exception).

## Pricing

- **Higgsfield (Path B):** about **9 credits/sec** at 1080p — verified: 36 (4s), 45
  (5s), 54 (6s), 31.5 (7s). Confirm the live rate at runtime; show the member the credit
  balance and the dry-run cost before spending.
- **fal (Path C):** billed **per second in dollars**; confirm with
  the fal-ai MCP `get_pricing` tool before the first render.
- **Path A (manual):** no automation cost.

Total cost ≈ (sum of every scene's `requested_seconds`) × the path's per-second rate. Gate 2
presents the exact per-clip table (span, generation, per-scene cost, totals) before anything
renders, and re-presents it after ANY plan change.

## Higgsfield gotcha (Path B)

Upload media FRESH and use it immediately; verify a render truly succeeded by the credit
balance dropping and a real downloadable MP4, not by the call returning. On Path B the CLI
auto-uploads the local file each call, which sidesteps stale-upload failures. (There is no
voice clip here, so the UGC factory's stale-voice bug does not apply.)

## Picture-lock reminder

Choose `duration = clamp(round_half_up(span), 4, 9)` — round to NEAREST (≥.5 up, <.5 down,
e.g. 4.42s → 4s, 6.62s → 7s), never blanket-ceil — and trim to the exact voiceover span at
stitch (a round-down shortfall is freeze-held by the stitcher; the VO is never altered). Do
not write the duration into the prompt text — the duration is set only by the generation
call's parameter.
