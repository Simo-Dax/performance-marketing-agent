# Voiceover & Audio Model — Pixar Ad Factory

The Pixar Ad is **voiceover-first**. The member writes the script, voices it ONCE in
ElevenLabs, and drops the file back in. The voice is the master clock and the master audio —
identical to the Clay Ad Factory's model.

## The audio model

- **The ElevenLabs VO is the only voice**, laid over the whole picture once at full level.
  The generator is never given a voice clip or voice reference, and no clip ever contains
  spoken dialogue or lip-sync — no witness and no character ever mouths a word.
- **Clips are silent or carry ambient real-world SFX only** (gym clatter, street hum, bar
  murmur, room tone — the photoreal world's foley). If a scene's `sfx` is true and the
  generator produced ambience, `stitch_pixar.sh` keeps it **ducked under** the VO
  (sidechain compression keyed off the VO, plus a low static floor) so the narration always
  sits on top. Set `keep_sfx:false` in `spec.json` for a fully silent picture under the VO.
- **No captions and no overlay text of any kind, ever.** The finished ad ships completely
  clean; the VO speaks every milestone ("Day fifteen: ...") and the offer. The stitcher has
  no caption path at all. Background music is an editor-side choice AFTER delivery, never
  part of this pipeline.
- The final mix is loudness-normalized to about **-14 LUFS**.

## ElevenLabs hand-off (Gate 1)

After the member approves the transcript, give them TWO things:

1. **The full transcript** as one copy-pasteable block (one beat per line for natural pauses).
2. **A quick voice design** for ElevenLabs Voice Design — one or two lines describing the
   voice: gender, age, energy/pace, tone, accent — drawn from the brand voice and audience.
   The format's native narrator is **calm, dramatic, documentary-style** — measured pace,
   quiet intensity that lets the escalation do the work. Example: "Male, mid 30s, calm and
   dramatic documentary narrator, low quiet intensity, measured pace with weight on the day
   counts, neutral American accent — never salesy, never hyped."

The transcript is a **second-person journal ("you") or a third-person case study ("a man /
he")** — the voice mode chosen in Step 2 — never first person. The CTA line may address
"you" directly in either mode.

Then the instruction:

> Create this voice in ElevenLabs Voice Design, render the transcript as ONE continuous
> voiceover (one voice, no music or SFX baked in), export MP3/WAV, and drop it into
> `18_Pixar_Ads/<concept>/audio/`. Tell me when it's in.

The voiceover is written to run **30–45 seconds**. One continuous render (not per-line) is
the default — it gives the most natural delivery, and `align_vo.py` recovers the per-line
timing.

## faster-whisper setup (auto-provisioned, shared with the clay skill)

Step 3 of the skill auto-creates this venv on first run (idempotent, lazy) — it is the SAME
voice-alignment engine the clay skill uses, so members who ran a clay ad already have it:

```
VENV="$HOME/.cache/la skill claymation/venv"
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install -U pip wheel faster-whisper
"$VENV/bin/python" -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8')"
```

`align_vo.py` self-bootstraps: if the interpreter running it can't import `faster_whisper`,
it re-execs through `$CLAY_AD_VENV` (env override) or the path above. If neither exists, it
falls back to the proportional method and says so.

## How alignment works

1. `ffprobe` gives the VO's exact total duration.
2. faster-whisper transcribes the VO with **word timestamps**.
3. The KNOWN script (transcript.json, which we wrote) is token-aligned onto the recognized
   word stream (difflib), so each script line gets a real `[start, end]`.
4. Output `timing.json`:

```
{ "audio_file":"audio/vo.mp3", "total_seconds": 38.2, "method":"whisper-aligned",
  "lines":[ {"id":"l01","role":"hook","vo":"...","start":0.0,"end":4.1,"dur":4.1,"word_count":16}, ... ] }
```

`method` is `whisper-aligned` (high confidence) or `proportional` (fallback: the total
duration split across lines by word count — exact total, approximate per-line; flag it).

## Picture-lock (round to nearest, fit the picture to the voice)

The voice defines how long each scene is on screen. Seedance renders only integer 4–9s
clips, so:

- `requested_seconds = clamp(round_half_up(span), 4, 9)` — **ROUND TO NEAREST: ≥.5 up,
  <.5 down (4.42s → 4s, 6.62s → 7s), never blanket-ceil** — rounded-up tails are wasted
  credits.
- At stitch, each clip is trimmed to its exact `span` (`trim_out - trim_in = span`); a
  round-down generation that runs a hair short (at most ~0.5s) is **freeze-held** — the
  stitcher clones its last frame out to the exact span — so the picture locks to the audio
  with no drift or gaps.
- **THE VOICE IS UNTOUCHABLE.** The VO file is never trimmed, silence-cut, stretched, or
  sped up to fit the picture; sync is always reconciled on the picture side. Dead space in
  the voice is an editing concern, never a re-voice.
- A scene whose span reaches 10s is split into more scenes (cut at a clean word boundary
  using the word timestamps); a single line can be ONE clip for any span up to just under
  10s. **THE MERGE LAW: a span under 3.5s (it would round below the 4s floor) never
  renders solo — merge its line with an adjacent line into ONE generation carrying both
  beats as hard-cut sub-shots** (`segment_scenes.py` hard-fails otherwise; the
  last-position CTA is the only exception, rendering at the 4s floor with a warning).
  **The hook line ALWAYS merges with the adjacent next line** — scene 1 opens on the
  hook's continuous 1–2s beat, then hard-cuts into the merged line's beats; a hook scene
  covering only the hook line is a structural error.
- The scene spans sum to ≈ the VO total; the final video is padded/trimmed to the exact VO
  length, which is the master.
