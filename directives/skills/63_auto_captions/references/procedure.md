---
name: auto-captions
description: "Burns the house-style captions onto any finished video, in the exact locked style: white Montserrat-style text with a soft drop shadow and no hard outline, sitting at 66% down the frame, mostly 2-3 words per card (1 or 4 only where they read better), always one row and never wrapped, no dots or commas anywhere, only the very first word of the video capitalised, and proper nouns like the agent kept intact and never split across cards. Two ways in: a user drops ANY video file and asks for captions, or a video skill offers captions on the ad it just finished. Works on the output of every ad skill (clay, pixar, skeleton, vox, podcast, animate-static, ugc-blueprint and all eleven UGC formats) and on plain uploaded videos from anywhere. When the ad's original script is on disk (transcript.json or timing.json) it FORCE-ALIGNS to it: whisper supplies the word timings, the script supplies the exact words, so the captions match the copy word-for-word instead of inheriting speech-recognition errors. Falls back to transcription alone when no script exists. Always writes a separate _captioned file and never overwrites the clean master. Trigger on /pm-captions, /captions, /subtitles, /add-captions, /caption, and natural language like add captions to this video, add subtitles, burn in captions, caption my ad, put subtitles on these videos, add capcut subtitles. If the user names a different skill, command, plugin, or tool for the job, or is building or testing their own skill, do not trigger this skill; use what they named instead."
---

# Auto Captions — the house caption style, applied to any video

Burns captions in the user's locked style onto a finished video. The style is not
adjustable per run: it was tuned on real footage and every value is fixed in
`references/caption-style.md`. **Read that file before changing anything.**

Two ways this runs, and they behave identically:

- **The user brings a video.** Any local file, from any source. It does not have to be
  something this agent made.
- **An ad skill hands one over.** Every video skill offers captions once its ad is
  assembled, and the user says yes or no. The ad's own script is on disk in that case,
  which is what makes the captions exact rather than merely good.

## The rules in one screen

- **Mostly 2-3 words** per card; 1 or 4 only where they genuinely read better
- **Always one row.** Never wraps — capped on rendered pixel width, not characters
- Split on real speech pauses and punctuation; **never end a card on a binding word**
  ("the", "than", "your", "if"...)
- **No dots, no commas** anywhere
- **Only the first word of the whole video is capitalised**
- **Proper nouns keep their capitals**; a brand name never splits across cards
- White, soft blurred drop shadow, **no hard outline**, 58px, baseline y=1275 (scaled by
  frame height for 4K and other sizes)

## Step 0. Resolve the scripts and the project folder

```
SCRIPTS="directives/skills/63_auto_captions/scripts"
echo "SCRIPTS=$SCRIPTS"
```

Captioned files land **next to the video they came from**, which for an ad this agent
built means inside that ad's own folder, beside the master. Only a video the user
brought in from outside needs a home of its own:

```
PWD_ABS="$(pwd)"
TARGET="${PWD_ABS}/the agent"
PROTECTED=0
case "$PWD_ABS" in
  "$HOME"|"$HOME/"|"/"|"/tmp"|"/tmp/"|"$HOME/Downloads"|"$HOME/Desktop") PROTECTED=1 ;;
esac
if [ "$PROTECTED" = "1" ] && [ ! -d "$TARGET" ]; then echo "PROTECTED:$PWD_ABS";
elif [ ! -f "$TARGET/_meta/folder-confirmed.flag" ] && [ ! -d "$TARGET" ]; then echo "FIRSTRUN:$TARGET";
else mkdir -p "$TARGET/_assets/captioned" "$TARGET/_meta"; echo "READY:$TARGET"; fi
```

## Step 1. Find the video(s) and the script

The user names the video, or points at a folder. For an ad the skills built, the video
is normally `<concept>/out/*.mp4`.

**Look for the ad's original script — this is the difference between good and exact.**
`autocaption.py` auto-discovers `transcript.json` / `timing.json` from the concept folder
(`./`, `../`, `../audio/`), so ad-skill output usually needs no wiring at all. Pass
`--script PATH` when it lives somewhere unusual, or when the user supplies the copy.

Why it matters: speech recognition is reliable about WHEN a word was said and only
approximate about WHICH word it was. Force-aligning uses whisper purely for timing and
takes every word from the script. On the user's own collection, transcription alone
produced "row ass" for ROAS in three ads, "cloud code" for Claude Code in three more, and
"minds" for "mines" in two. None of those existed in the scripts.

## Step 2. Dry-run first

```
python3 "$SCRIPTS/autocaption.py" <video> --dry-run
```

Prints every card with its timing and word count plus the audit, and renders nothing.
Read the cards against what the ad actually says. Cheap, fast, catches problems before a
long encode — a 4K minute-long ad takes a couple of minutes to burn.

## Step 3. Burn

```
python3 "$SCRIPTS/autocaption.py" <video> [<video> ...]
```

Writes `<name>_captioned.mp4` (into a sibling `out/` when one exists, else alongside) plus
`<name>.captions.json` holding the script, word timings, cards and audit. **The clean
master is never overwritten** — captions are always a separate deliverable, so the user
can A/B them.

Audio is stream-copied, so loudness and the mix are untouched. Video re-encodes at source
resolution: caption geometry scales off frame height, so 4K gets the same relative size
and position, not tiny text.

Useful flags: `--script PATH`, `--out DIR`, `--model medium|small.en|large-v3`,
`--no-align` (caption straight from the transcription even if a script exists).

## Step 4. Report the audit, honestly

Every run prints: card count, **% in the 2-3 band**, any two-row card, any punctuation,
and whether the captions **match the script word-for-word**. Report those numbers rather
than saying it looks right. Anything other than `two-row: none`, `punctuation: none` and
`script match: True` is a defect — investigate before handing it over.

Healthy looks like: ~90%+ in the 2-3 band, no two-row cards, exact script match.

If the run prints a `FONT:` line, the locked face was not available on that machine and
something else rendered. **Pass that line on to the user**; never let a substituted font
go out unmentioned.

## Step 5. Highest resolution wins

If several cuts of the same ad exist (a 1080 and a 4K master, or an upscale), caption the
**largest** one. Before trusting that an upscale is the same footage, sample 3-4 frames
against the original and compare — a mean pixel difference in the low single digits per
channel means it is genuinely the same cut and the timings will hold. A much larger number
means it is a different render and needs its own alignment.

## Iterating without re-transcribing

`<name>.captions.json` keeps the aligned word timings. After a change to
`caption_lib.py`, rebuild from that file instead of transcribing again — re-chunk, render
and composite. Transcription is the slow part; skipping it turns an hour into minutes.

## NEVER DO

- Never overwrite the clean master; captions are always a separate `_captioned` file.
- Never re-time or re-encode the audio — it is stream-copied.
- Never let a card wrap to a second row. That is a hard structural rule, not a preference.
- Never add dots or commas back, and never capitalise anything but the first word of the
  video and genuine proper nouns.
- Never split a brand name across two cards.
- Never claim the captions match the script without running the audit.
- Never silently swap the font or move the baseline; those values are user-locked, and a
  substitution is reported out loud.
- Never caption a video the user did not ask you to caption. This is always offered and
  never assumed.

## Files

- `references/caption-style.md` — the locked spec and the reasoning. Read first.
- `scripts/caption_lib.py` — the engine: chunker, styler, renderer, compositor.
- `scripts/autocaption.py` — the CLI: discover script, transcribe, align, burn, audit.

## Requirements

`ffmpeg` and `ffprobe` on PATH, Pillow, and faster-whisper. The script re-execs itself
into the shared whisper venv at `~/.cache/pm-agent/whisper-venv` automatically (the same
venv the video skills already build), and prints the one-line fix if it is missing.

**The font is resolved from a ladder, locked face first.** Avenir Next Heavy is the
Montserrat stand-in the style was tuned on and it is always tried first; a machine without
it falls through Montserrat, then the platform's bold face, and the run says which one it
used. Loading a single hardcoded macOS path is what this replaced, because it made the
whole skill a hard crash on Windows and Linux before it parsed an argument.

Captions are rendered as transparent PNGs with Pillow and composited with `overlay`, not
with `drawtext` or `subtitles`. That works on ffmpeg builds without libass or freetype,
and it gives exact control over the styling.
