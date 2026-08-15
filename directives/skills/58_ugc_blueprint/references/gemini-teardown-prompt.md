# Route A — the locked Gemini teardown prompt

Paste the fenced block below to the member **verbatim and in full**, inside a code
block, so they can copy it in one click. Never paraphrase it, never shorten it, and
never rewrite the rules — every rule in it exists because a teardown failed without it.

Gemini watches the video; it cannot run a frame-difference curve. The counting
discipline in Rule 1 is what compensates. Expect it to under-count cuts on jump-cut
edits and verify the result (see "Validate what comes back", below).

Send them here: **https://gemini.google.com** — upload the video, paste the prompt,
paste the answer back into this chat.

---

```
You are reverse-engineering a video ad into a shot-by-shot recreation prompt.
I have attached the video. Study it, then output ONE prompt in the exact locked
template at the bottom. Output nothing else — no preamble, no commentary.

═══════════════════════════════════════════════════════
RULE 0 — MEASURE, NEVER INFER
═══════════════════════════════════════════════════════
Every line you write must come from something you actually saw or heard in
the video. Do not fill gaps with what an ad of this kind usually does.

The filename is NOT evidence. Scraper sites name files from unrelated SEO
copy — a file called "easy meal prep recipes" turned out to be a skincare ad.
Identify the product from the frames only. Never let the filename influence
a single word of your output.

If something is genuinely unreadable or unclear, say so explicitly. Never
guess, and never silently omit it.

═══════════════════════════════════════════════════════
RULE 1 — COUNT EVERY SINGLE CUT
═══════════════════════════════════════════════════════
Do not skim the video and describe the beats you remember. Step through it
and find every hard cut.

Do not assume a cut rate. First establish what kind of edit this is: count
the cuts in the first 10 seconds, then extrapolate and verify against the
rest.

Whatever the pace, the failure mode is the same: JUMP CUTS INSIDE ONE
UNCHANGED FRAMING are the ones that get missed. Locked camera, fixed
background, the subject's pose snapping between adjacent frames. Watch the
hands, head angle and hair — if they jump discontinuously, that is a cut,
even though the shot "looks the same".

Sanity-check both directions. If your shots average over 3 seconds, look
again for jump cuts you skipped. If you found a cut roughly every 0.3s
across the whole video, check you are not calling fast motion a cut.

Do not merge several short shots into one entry because they share a
subject. Shots of 0.3–0.7 seconds are normal and each gets its own block.
Report the count you actually observe, even if it feels high. If the video
is genuinely one continuous take, say so and output one shot.

State the total shot count in the Lighting & Vibe line.

═══════════════════════════════════════════════════════
RULE 2 — CAMERA MOVES
═══════════════════════════════════════════════════════
Decide static vs moving from the BACKGROUND, every time. If the background
is fixed, the shot is static no matter how much the subject moves — a
subject leaning toward the lens is not a push-in. Only write a pan, tilt,
push, whip or handheld drift if you can see the background actually travel.

═══════════════════════════════════════════════════════
RULE 3 — AUDIO
═══════════════════════════════════════════════════════
Classify the audio into exactly one of three cases:

  • Speech present  → "One [woman's/man's] voice throughout. [Music bed /
                       no music, room tone only.]"
  • Music only      → "Ambient music only. No voiceover, no talking."
  • No audio track  → "Silent. No audio track." (never call this music)

If anyone speaks, transcribe VERBATIM. Exact words, exact contractions,
including filler and false starts. Do not clean it up, paraphrase or
summarise. If you cannot make out a word, write [unclear] rather than
inventing one.

Pay special attention to brand and product names — these are the words most
often misheard. Cross-check every brand name you transcribe against the text
printed on the product itself, and make them agree.

═══════════════════════════════════════════════════════
RULE 4 — SPLIT THE DIALOGUE ACROSS THE CUTS
═══════════════════════════════════════════════════════
In this format the voice runs CONTINUOUSLY while the picture jump-cuts
underneath it. Sentences therefore do NOT line up with shots — most shots
begin and end mid-sentence.

Do not assign one tidy sentence per shot. Work out which words actually land
inside each shot's time window and quote only those, even when that means a
shot's dialogue is a fragment like "asking" or "and this product." or
"moisturizer and".

A shot whose dialogue is one word is normal and correct.

Never write "(None)" for a shot that has speech running over it.

═══════════════════════════════════════════════════════
RULE 5 — ON-CAMERA vs VOICEOVER
═══════════════════════════════════════════════════════
Mark every shot with speech as ONE of these:

  Dialogue (On-Camera):  the subject is visibly speaking, lips in sync
  Dialogue (Voiceover):  lips are not moving, or she is not in frame,
                         and the voice continues over the shot

Decide this by LOOKING AT THE MOUTH in that specific shot — never by whether
audio is present. Audio runs over the whole ad; that proves nothing.

Do not assume a ratio. Some ads are entirely on-camera, some entirely
voiceover, most mix. Judge every shot independently by its own mouth.

These ads routinely cut B-roll (hands, product macro, texture, posed beauty
shots) into a continuous take. Those inserts carry the voice as VOICEOVER
even though the speech never stops.

Be careful: a closed mouth during a /m/, /b/ or /p/ sound is correct
lip-sync, not evidence of voiceover. Check several frames across the shot
before deciding.

═══════════════════════════════════════════════════════
RULE 6 — PRINTED TEXT ON OBJECTS: CAPTURE IT IN FULL
═══════════════════════════════════════════════════════
Spell out ALL text physically printed on the product, exactly as it reads on
screen, in the Props line. Use the frame where the label is squarest to the
lens and zoom in. Printed text does not survive a vague description, so it
must be captured literally.

If the label is genuinely illegible even zoomed, write that explicitly.
Never invent label copy and never quietly leave it out.

If more than one product appears, describe each separately, and say clearly
if a substance appears with no container ever shown.

═══════════════════════════════════════════════════════
RULE 7 — OVERLAID TEXT: IGNORE IT COMPLETELY
═══════════════════════════════════════════════════════
Anything composited ON TOP of the picture is invisible to you. Do not
describe it, do not transcribe it, do not give it timestamps, and never put
it in an Action line.

That means: burned-in captions and subtitles, typed-on or sticker text,
emoji, watermarks, corner logos, platform handles and UI, pause and play
buttons, progress bars and scrubbers, countdown timers, "link in bio"
graphics.

Describe only what was physically in front of the camera. The distinction is
simple: text printed on an object in the scene is real and goes in Props
(Rule 6); text laid over the picture in an editor does not exist.

The recreated video must contain NO on-screen text of any kind, so the
Lighting & Vibe line must always end with this sentence, verbatim:

  No on-screen text, captions, subtitles, emoji or watermarks anywhere; the
  only text is what is physically printed on the product.

═══════════════════════════════════════════════════════
OUTPUT TEMPLATE — reproduce this structure exactly
═══════════════════════════════════════════════════════
Add no sections. No "Set", no "Location", no global "Camera" line, no
"Music" field, no on-screen-text field. Backgrounds go inside the shot that
uses them; camera goes on the Shot Type line.

Overall Style & Aesthetics:

* Subject: [Person: age, hair, eyes, skin, nails. Base outfit, then any
  layers or props added later with the timestamp they appear. Omit this
  block entirely if no person appears.]
* Props: [Every object, product first. Full printed label text spelled out.]
* Lighting & Vibe: [Setting, light quality, aspect ratio, resolution, total
  shot count, average shot length, static or moving — then the mandatory
  no-text sentence from Rule 7.]
* Audio: [one of the three cases from Rule 3]

Scene Breakdown

0:00–0:0X.X
Shot Type: [framing / angle / static or the specific move]
Action: [what physically happens in this shot, one beat, concrete]
Dialogue (On-Camera or Voiceover): "[verbatim words landing in this shot]"

[...one block per shot, one for EVERY cut you found...]

FORMATTING
• Timestamps in tenths, zero-padded seconds, en-dash: 0:04.7–0:06.1
• Every shot starts exactly where the previous one ended — no gaps, no
  overlaps. Verify this before you output.
• The last timestamp must equal the video's true duration.
• Action lines: concrete physical description. What the hands do, where the
  subject looks, what the product does. Not mood, not vibe adjectives.

At the very end, on its own line, print:
CHARACTER COUNT: [exact character count of everything above]

Target 4,800–5,000 characters. Never exceed 5,000. If you are over,
compress by shortening the Action prose — never by merging shots, never by
cutting dialogue, and never by dropping printed label text.
```

---

## Validate what comes back

Never save a pasted teardown without these four checks. Say plainly which passed
and which did not; do not quietly repair it.

1. **Duration.** `ffprobe` the file. The last timestamp must equal the real
   duration. If it is short, shots are missing.
2. **Continuity.** Every shot must start exactly where the previous one ended. Gaps
   or overlaps mean invented timings.
3. **Shot count against the pace.** Divide duration by shot count. An average over
   ~2.5s on a fast-cut social ad means missed jump cuts. Measured case: Gemini
   returned 12 shots on a video that has 21, all nine misses being jump cuts inside
   one unchanged framing.
4. **Dialogue split.** If every shot carries a neat complete sentence, Rule 4 was
   ignored — in this format sentences run across cuts and most shots start
   mid-sentence.

If checks 3 or 4 fail, offer the member the local route for the affected section,
or ask Gemini again pointing at the specific rule it broke.

Then save it to `17_UGC_Blueprints/<slug>/recreation-prompt.txt`, write
`17_UGC_Blueprints/<slug>/method-notes.md` recording that it came from Route A plus
which checks passed, and go to Step 8.
