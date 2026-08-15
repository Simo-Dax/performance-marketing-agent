# Cutting & assembly — word-accurate, single-shot, −14 LUFS

This stage is pure EDITING — it runs on already-rendered clips and spends NO credits. The member can iterate here endlessly.

## faster-whisper (auto-provisioned)
`whisper_cut.py` needs faster-whisper in a venv so it never touches system Python. It self-bootstraps into a durable, namespaced cache venv (not `/tmp`, so the model isn't re-downloaded every reboot); the exact commands (also a manual fallback):
```
python3 -m venv ~/.cache/pm-agent/whisper-venv
~/.cache/pm-agent/whisper-venv/bin/pip install -q faster-whisper
~/.cache/pm-agent/whisper-venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('small.en', device='cpu', compute_type='int8')"
```
Use `small.en` (good word timing on clean podcast audio).

## Cutting each generation into per-line clips
For each generation mp4 (which contains its 1–N scripted lines):
1. Transcribe with **word timestamps**.
2. **Align the KNOWN script lines to the recognized words** with `difflib.SequenceMatcher` over normalized tokens. This gives each line a real `[start, end]` even when whisper mis-hears a middle word (it anchors on matched words). Do NOT split by silence/gaps — a dramatic in-line pause cuts in the wrong place, and a robust transcription drops quiet words.
3. For each line, cut a clip:
   - **start** = `first_word_start − 0.08` (small lead so the onset isn't clipped), clamped ≥ previous clip end and ≥ 0. Starting on the first word also **drops any front "peep"** (a tiny startup tick some generations place before speech).
   - **end** = `last_word_end + 0.20` (the house rule — snappy but the word rings out), clamped ≤ the next line's start − 0.05 (never bleed into the next line) and ≤ the generation duration.
4. **Verify single-shot:** scene-detect the output clip (`select='gt(scene,0.3)'`). If a cut is found inside it, the clip contains two shots — flag it (and cap before the cut). With per-line cutting this is rare, but always check.

## Front "peep" / startup artifact
Some generations begin with a faint high tick before the first word. Because the clip starts on `first_word_start − 0.08`, anything earlier is dropped. If a tick still sits right at the start, analyze the first ~0.6s envelope (10 ms RMS windows) to find where speech actually begins and start there, optionally with a ~0.03s audio fade-in.

## No freeze-holds
Do not pad a clip by cloning/holding its last frame for "breathing room" — it reads as a static stutter and the member rejected it. Breathing room comes from real footage: either the natural 0.2s tail, or re-rendering that line with a trailing beat in the prompt (a NEW gated render).

## Assembly (stitch_podcast.sh)
- Concatenate the per-turn clips in **conversation (turn) order**.
- Conform each to 1080x1920 @ 30fps, SAR 1.
- **Keep each clip's own baked audio** and concat straight — never mute, never lay a separate spine.
- Two-pass loudness-normalize the final mix to **−14 LUFS**.
- QC: output must have a video AND an audio stream, and a duration within tolerance of the summed clips.

## Avoid two same-speaker takes back-to-back
If the timeline would place two of one host's separate takes adjacently, they jump-cut (the host changes pose between takes). Fix at the script stage (alternate speakers, or write the two points as one continuous turn → one clip). If it slips through, drop one beat or re-render the pair as a single continuous generation.

## Verify the whole ad
After stitching, transcribe the final mp4 and print the recognized line order. It should match the approved transcript top to bottom — proof the conversation flows and nothing dropped or reordered.
