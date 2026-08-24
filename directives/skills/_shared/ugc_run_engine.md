# UGC run engine, start to finish

Every UGC format skill loads this first. It owns the run: where the work goes, what is
discovered, what is asked, which path renders, when the user is stopped, and what is handed
over. The three stage engines it calls own only their own stage.

```
run engine  ->  script engine   (the words, or the sound plan)
            ->  video engine    (the shot COUNT and the format's shot types)
            ->  image engine    (the ANCHOR PROMPT, phase 1)
            ->  THE PLAN, all three together              GATE 1, free
            ->  image engine    (render the anchor)        GATE 2, costs money
            ->  video engine    (the full render prompt, phase 2)
            ->  video engine    (the render)               GATE 3, costs money
            ->  delivery

The user sees the whole creative idea at GATE 1, while every part of it is still free to
change: the words, the shots and the still, in one message. The 5,000-character render prompt is
assembled LAST, out of parts that were already approved, because nobody can usefully review a
script by reading it buried inside a technical description of forty camera moves.
```

The format spec beats this engine on anything it declares. This engine beats nothing.

---

## R.1 Resolve the project folder

```
PWD_ABS="$(pwd)"
TARGET="${PWD_ABS}/the agent"
PROTECTED=0
case "$PWD_ABS" in
  "$HOME"|"$HOME/"|"/"|"/tmp"|"/tmp/"|"$HOME/Downloads"|"$HOME/Desktop") PROTECTED=1 ;;
esac
if [ "$PROTECTED" = "1" ] && [ ! -d "$TARGET" ]; then
  echo "PROTECTED:$PWD_ABS"
elif [ ! -f "$TARGET/_meta/folder-confirmed.flag" ] && [ ! -d "$TARGET" ]; then
  echo "FIRSTRUN:$TARGET"
else
  mkdir -p "$TARGET/05_UGC" "$TARGET/_meta"
  echo "READY:$TARGET"
fi
```

`PROTECTED`: refuse, tell the user to open in a brand subfolder, stop. `FIRSTRUN`: confirm the
path once, write the flag. `READY`: continue silently as `$AILAB`.

## R.2 Do the homework, then propose. Do not interview.

Read what is on disk BEFORE asking anything:

- VOC and Brand DNA, per `voc-brand-reader.md`, plus the Foundation Pack when present
- the compiled brand memory, per `brand-brain.md`, when `_knowledge/context-pack.md` exists
- saved characters in `11_Characters/`
- product photos in `_assets/product-images/`, `_assets/product-shots/`, `02_Brand_DNA/`
- previous runs of this format in `05_UGC/<format>/`, so the same angle is not made twice

Then come back with a PROPOSAL, not a questionnaire: the product, the angle and why that angle,
the duration, and the length of the script. One short paragraph. The user corrects whatever is
wrong, and correcting costs nothing because gate 1 has not happened yet.

Ask a question only where the answer cannot be found or reasonably inferred, and ask it in ONE
message alongside the proposal, never as a separate round.

If a `voc-required` format finds no VOC document, STOP and route the user to `/voc`. Do not
invent a customer.

## R.3 The photo audit, before anything is written

Work out which product STATES this ad will show, then name them all in one message:

> This ad opens the jar and shows the cream on skin. I need: the sealed jar, the jar open, and
> the product on skin. I have the sealed jar. Send the other two.

Then STOP until they arrive. A state the model has never seen is a state it invents, and an
invented product interior is instantly obvious and unusable in a render the user paid for.

Ask once, up front, with the full list. Never discover a missing photo halfway through.

## R.4 Duration

The format spec's band is the DEFAULT, not a rule. **The user owns the length.** Any duration
they ask for is honoured, and the word budget recalculates from the format's wps rather than
arguing them back into the band.

The one hard limit is the renderer: **Seedance accepts 4 to 30 seconds**. Outside that, say so
plainly and offer the nearest valid value.

## R.5 Pick the render path, state it, allow the override

Detect what the user has configured and choose. Do not present a menu.

| Found | Use |
|---|---|
| Higgsfield CLI logged in | Path B |
| fal.ai key configured | Path C |
| nothing configured | Path A, hand over the prompt for the user to paste |

> There is no Path K in this agent. KIE AI is mapped but not wired --- see
> `execution/kie_api_map.md`. Do not attempt to route a render through it.

Say which in one line with the override visible: `Rendering through Higgsfield. Say "use fal"
to switch.` When more than one is available, prefer the order above unless the user has said
otherwise in this project before.

## R.6 The gates

**GATE 1, THE PLAN. Free.** One message, three things, in this order:

1. **The script**, in plain form, line by line. Or the sound plan, for a sound-carried format.
2. **The shape of the ad**, in plain sentences: how many shots, what the hook will be doing, and
   which of this format's shot types the product supports. NOT a shot list, because there is no
   shot list. The video model directs the ad; the prompt teaches it the format.
3. **The anchor prompt**: what the still will lock, and why that moment was chosen.

Then a short plain-language note on the thinking, four or five sentences, no jargon. Then STOP.
Nothing is generated until the user approves. This is the last moment when everything is free,
and it is deliberately the moment when the user can see EVERYTHING rather than one slice.

Corrections here cost nothing. A user who moves a beat, cuts a line, adds a shot or changes
who is in the anchor is doing it before a single credit has been spent, which is the entire
reason the plan is presented whole instead of in three separate rounds.

**GATE 2, permission to render the anchor. Costs money.** Handled by the image engine, using the
anchor prompt the user already approved at GATE 1.

**GATE 3, permission to render the video. Costs money.** The assembled render prompt, the
approved anchor, the exact price for the chosen duration and resolution, then wait.

> **THE SPEND LAW.** Nothing that costs money is generated without a clear, specific,
> immediately preceding yes. Not on silence, not on a maybe, not on an approval given for a
> different step, and never on one carried over from an earlier render in the same run. Every
> retry is a new spend and needs its own yes.

## R.7 One ad per run

One prompt, one anchor, one render. A user who wants four ads runs it four times, and each one
gets its own three gates. Batching is deliberately not offered until output quality is proven,
because batching an unproven pipeline multiplies a mistake by four.

## R.8 Delivery

```
05_UGC_Prompts/formats/<format>/<concept>/
    <concept>_v1.mp4          versioned, NEVER overwritten by a rerun
    anchor/                   the approved still per version
    prompts/                  video prompt and anchor prompt per version
    transcript.json
    post-production.md        what to add after the render, see below
    manifest.json             per version: prompt, model, path, duration, resolution, spend
```

### post-production.md, the handover note

The render deliberately contains **no music and no on-screen text**. Both are added afterwards by
the user, and this file tells them exactly what to add and when:

1. **On-screen text.** A timed recommendation: the line, the timecode it appears, and why.
   Elapsed-time markers for a transformation, step numbers for a tutorial, the hook restated for
   sound-off viewing. Recommend it properly, do not just note that text is missing.
2. **Music.** Whether this ad wants a bed at all, and what kind if so. Some formats are better
   dry, and this file says which.
3. **Format extras.** Anything the format spec calls for. A green-screen ad names what belongs
   behind the creator and at what timecode.

**Text is never rendered into the video.** All 110 banked prompts ban on-screen text, captions
and watermarks outright, and generated text garbles. The recommendation is the deliverable; the
burn-in is the user's editor, or the caption offer below.

### Offer captions

Once the file is delivered, ask once, then respect the answer:

> Want captions burned on? I'll add them in your locked house style, mostly 2-3 words a card,
> and keep this clean master untouched as a separate file.

On yes, run the `auto-captions` skill on the delivered `<concept>_v1.mp4`. It
force-aligns to the `transcript.json` sitting beside it, so the captions carry the exact spoken
lines rather than whisper's guess at them. On no, deliver as is.

**A silent format has nothing to caption.** When the ad carries no dialogue, say so instead of
offering: the on-screen text recommendation in `post-production.md` is the deliverable there, and
it is a different job from spoken captions.

Never caption without asking, and never replace the clean master.

## R.9 Output validation

- the file exists, is non-empty, and is the duration that was approved
- the render carries no music, no burned-in text and no watermark
- the anchor used is saved beside it
- `post-production.md` names every add-on with its timecode
- the manifest records the real spend, read back from the tool, never estimated
- no previous version was overwritten
