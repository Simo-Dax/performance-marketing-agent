# Seedance 2.0 limits & knobs — for the Talking-Object Ad Factory

The locked facts this skill renders against. When a backend rejects a value, verify the
live schema (`higgsfield model list` on Path B, the fal-ai MCP `get_model_schema` tool on Path
C) before improvising.

## Per-generation limits

- **Duration:** an explicit integer **4 to 9 seconds**. Every generation is UNDER 10s.
  Sized from the line's word count (`clamp(round(words/2.8), 4, 9)`); a >25-word line
  cannot fit and is a script bug.
- **Aspect:** vertical **9:16**. **Resolution:** **1080p**.
- **Audio: NATIVE AND LOAD-BEARING.** Seedance generates the clip's audio automatically
  (the Higgsfield CLI has NO `--generate_audio` flag) — and in THIS skill that audio is
  the ad's actual soundtrack: the character speaks the prompt's DIALOGUE line in the
  prompt's described voice, mouth loosely synced. Verified working "very well"
  (member-confirmed). Two consequences:
  - The dialogue and voice descriptions in the prompt are PRODUCTION AUDIO — word-exact
    lines, locked voice castings.
  - Every rendered dialogue clip is whisper-verified (`dialogue_check.py`); a flubbed
    line is a re-render, because the audio is baked into the pixels.
- **The voice is cast fresh on every generation.** Same prompt, same voice description —
  a DIFFERENT take of the voice each render. Within one clip the voice is consistent;
  across clips it is not. This is the physical fact behind the reference ladder's tier 3.
- **Reference inputs (verified CLI media flags: `--image`, `--start-image`, `--video`;
  `--audio` is NEVER used):**
  - **Tier 1** (generic one-off speaker): NO reference flags at all. Text-to-video from
    the bible. (Member-locked; proven by the enzyme test.)
  - **Tier 2** (real product in frame): the approved casting/product still as an
    **`--image`** reference. The label must read in every frame.
  - **Tier 3** (recurring speaker): the speaker's approved wave-1 clip via **`--video`**
    — THE ONE LEGAL VIDEO-REFERENCE USE IN THE PLUGIN FAMILY, carrying the character's
    face AND voice into the new clip. The prompt must command a brand-new environment
    and angle so the reference carries the character, never the scene. Expect the model
    to pull composition toward the reference — fight it in the prompt ("do NOT copy the
    reference's environment, framing, or camera").
  - `--start-image` is NOT used in this skill (there is no approved-still-as-first-frame
    model here; the hook is tier 1, text-to-video).

## One scene = one shot

Dialogue clips hold **ONE continuous shot** — the character's performance is the footage;
no internal hard cuts, no sub-shot montage (that grammar belongs to the VO-first
factories). Movement comes from the acting business, the prop payoff, and one slow camera
move. Timestamped beats inside the prompt are required; the clip's TOTAL duration is
never written in the prompt text (the duration field sets it).

## Pricing

- **Higgsfield (Path B):** about **9 credits/sec** at 1080p — 36 (4s), 45 (5s), 54
  (6s), 31.5 (7s). Confirm the live rate at runtime.
- **fal (Path C):** billed per second in dollars; confirm with the fal-ai MCP `get_pricing` tool.
- **Path A (manual):** no automation cost.

Total ≈ (sum of `requested_seconds`) × rate, **plus the re-render contingency**: dialogue
clips occasionally flub words and only a re-render fixes them — Gate 2 quotes a ~+30%
contingency line so a flub is never a surprise spend. Wave-2 scenes render after their
voice_ref clip is approved (they can't join the parallel batch).

## Higgsfield gotcha (Path B)

Upload media FRESH and use it immediately; verify a render truly succeeded by the credit
balance dropping and a real downloadable MP4, not by the call returning. The CLI
auto-uploads local files each call. There is no voice upload in this skill (the voice
comes from the prompt), so the UGC factory's stale-voice bug cannot apply.

## Trim reminder

After render, `dialogue_check.py` reports where the speech actually ends
(`speech_end`); set `trim_out = speech_end + 0.3–0.6s` (never past the clip, never
cutting a word) so dead tail air never pads the ad. The stitcher trims video+audio
together — the performance stays intact.
