# Podcast Ad — Locked Rules (read first)

These are the rules that make the outcome good. They are brand-agnostic — they encode HOW to make any two-host AI podcast ad land, not what any specific ad says.

## Process (the cardinal rules)
1. **NEVER render without an explicit human "go" for that exact batch.** Silence, your own judgement, or re-printing a table is NOT approval. A new or changed render is a NEW batch needing its OWN go.
2. **Two hard gates:** the TRANSCRIPT gate (member approves the exact words before anything renders) and the COST gate (member approves the spend before any render).
3. **Editing is free; rendering costs.** Always exhaust the free edit loop (re-cut + re-stitch existing clips) before spending credits. Only genuinely NEW spoken content triggers a render.
4. **Verify the final cut by transcribing it** and reading the recognized line order back against the approved transcript.

## Inputs
- The member uploads **one reference image + one voice clip (10–15s) per host**. The skill NEVER generates faces, voices, or studios.
- Don't have them yet? `your-inputs.md` shows how to make both — host images from a real podcast still, voice clips recorded / borrowed / generated in ElevenLabs.

## Visual rules (into every generation prompt)
- **Never look at the camera.** Each host's gaze stays in the direction they are already looking in their reference image, toward the co-host.
- **Mirror eyelines.** Left-seat host looks screen-right; right-seat host looks screen-left — so cuts make the two gazes "meet" and read as one conversation. (Determined from the uploaded images; if both look the same way, warn the member.)
- **Static locked camera** — no pan, zoom, or reframe drift. Same fixed framing as the reference image.
- **Subtle emotion per line** — small, real micro-expressions, never exaggerated; a slightly different shade per beat.
- **No video reference, ever.** Identity comes from the re-sent image bytes only.
- Prompt is short: the reference image carries the look. Scene line + exact quote + "no on-screen text." Do not re-describe the person's anatomy.

## Script rules
- **Natural spoken dialogue** — how people actually talk (fillers, reactions, half-thoughts). NEVER clipped ad-copy fragments (e.g. "One command. The whole funnel. Done." is banned — nobody talks like that).
- **Fast + short** — ~6–9 words per beat (~2 seconds), ~3.5–4 words/sec. Benchmark: a real fast-cut podcast runs a visual cut every ~2–2.5s, median beat ~1.8s / ~8 words.
- **Structure:** open on a **curiosity hook** (a question), deliver value props through the **skeptic's short questions**, optional **meta/proof** beat, close on a **CTA button** (a confident closing line).
- **Default dynamic:** insider vs. skeptic — the skeptic's doubts let the insider land each value prop; it carries any topic.
- **Alternate speakers.** Never end up with two of one host's separate takes back-to-back (jarring position jump between takes). If a host must make two points, write them as ONE turn (one continuous clip) — do not split them into two adjacent clips.
- **Acronyms/garbled words:** spell acronyms so the model says the letters (write `A.I` → "A-I"). If the model mangles a specific word in a test render, swap the word for a synonym.

## Cutting rules
- **Cut each clip to end ~0.2s after the last spoken word**, found from faster-whisper word timestamps. Small ~0.08s lead before the first word so the onset isn't clipped.
- **Find cut points by aligning the KNOWN script lines to the recognized words** (difflib), NOT by silence/gap detection — a dramatic in-line pause (e.g. "Honestly?…") makes gap-based splitting cut in the wrong place.
- **Trim the front startup artifact** (a tiny "peep"/tick some generations put before the first word) by starting on the real audio onset.
- **No freeze-holds for breathing room** — they look static and the member rejected them. Breathing comes from real footage (render a trailing beat) or simply the 0.2s tail.
- **Verify every clip is a single shot** (scene-detect) — no two-shots-in-one-clip, no overlap.

## Length
- Default ad **~30s** — write ~13–16 short turns / ~110–130 words at ~3.5–4 wps. 9:16, 1080p, −14 LUFS. After assembly, confirm the ad lands ~25–35s; if it runs long, cut a beat.
- **2–3 lines (shots) per generation** — never a lone 1-line generation (a trailing single is merged up to 3).
