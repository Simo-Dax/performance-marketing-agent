# Swap and render — turning a teardown into the member's own ad

The teardown describes someone else's video. This turns it into the member's, in three
moves: pull anchor frames out of the original, swap the character and product inside those
frames, then render the video from the swapped stills.

---

## 1. Pull the hero anchor

**One anchor, from the opening product beat.** Not one per shot and not one per look: a
single frame is the source of truth the whole rebuild is generated from, and the render
holds continuity from it. Step 8 in `../SKILL.md` owns the full procedure; this is the
summary.

The opening product beat is the first place the product is held up and readable, and in a
UGC ad that is **often the first frame** — these ads usually open with the product already
in hand. Start at frame 0 and take it when it passes the checks. Position never disqualifies
a frame; failing a check does.

Pick the frame that does all of this at once:

- The product's label or wordmark is squarest to the lens and in focus.
- No motion blur on the product.
- The character's face is unobstructed, or deliberately behind the product if that is the
  shot's design.
- **No overlaid caption sits across it.** Openings are where burned-in text lives, so prefer
  a clean frame a few tenths later over one with text baked in.

Extract candidates by frame number and look at them, then re-export the chosen frame at
**full resolution**:

```
ffmpeg -y -loglevel error -i "$V" -vf "select='eq(n\,$N)'" -vsync 0 -frames:v 1 "$D/anchor.png"
```

If every opening frame carries a caption, say so and offer the cleanest later product beat
instead. Show the member the anchor and get approval before going further. They approve the
frame, not you.

---

## 2. Collect the member's assets

Ask for, and wait for:

1. **Every brand product that appears in the ad.** One clear photo per product, label
   readable. If the ad features three products, three photos. Seedance renders a product it
   has been shown; it invents a product it has only been told about.
2. **The character direction** — who replaces the person on screen. Age, hair, build,
   anything they care about. If they have no preference, propose one and let them confirm.

**Why every product needs a photo, stated plainly if the member pushes back:** printed
label text does not survive a text description. Measured on this brand's own render, a
wordmark described in words came back as "FAL" in one shot and something closer to "AAL" in
another — wrong, and inconsistent between shots of the same video. The reference image is
the fix, and there is no prompt wording that substitutes for it.

---

## 3. The swap prompt

One per anchor frame. Attach the anchor as image 1 and the product photo as image 2. With
several products, attach the anchor plus each product photo and number them in the prompt.

**The background is always replaced, and always with the same KIND of space.** There is one
template and no "keep the room" option. The reference's actual room is its footage, and
footage never transfers — only structure does. A simple home bedroom becomes a *different*
simple home bedroom; a bathroom becomes a different bathroom; a plain studio backdrop
becomes a different plain backdrop.

First classify what the anchor is actually shot in, then write a different instance of that
same category:

| Reference reads as | Replace with |
|---|---|
| Simple home bedroom, bed in shot | A different simple home bedroom, different bed, wall, art |
| Bathroom, tile and counter | A different bathroom, different tile, fittings, counter |
| Kitchen | A different kitchen, different cabinets and worktop |
| Living room / sofa | A different living room, different sofa and layout |
| Plain wall or studio backdrop | A different plain wall in a different colour |
| Car interior | A different car interior |
| Outdoors | A different outdoor spot of the same type |

Match the register too, not just the room type: a lived-in phone-shot bedroom must not
become a styled magazine interior. Same everyday feel, different room.

```
Image 1 is a frame from an existing video. Image 2 is the product.

Swap the product in Image 1 for the product in Image 2, matching its shape, cap, label,
colour and printed text exactly. The printed text must read exactly as it does in Image 2.

Swap the person for a completely different woman, [CHARACTER DIRECTION], who looks nothing
like the person in Image 1: different face, different hair, different build.

Keep the camera identical: same framing, same crop, same lens feel, same camera height and
angle, same pose and hand position.

Replace the room with a DIFFERENT [BACKGROUND CATEGORY]. It must read as the same kind of
everyday space, but it is not the same room: [NEW ROOM DESCRIPTION]. Different furniture,
different wall, different layout and different objects from Image 1. Do not reproduce the
room in Image 1.

Light the subject to match that room: [LIGHT DIRECTION AND QUALITY]. Shadows on the face,
hand and product must fall consistently with that light, and the colour grade must match
the new room, not Image 1.

Ignore anything overlaid on Image 1: captions, on-screen text, watermarks, and any pause or
play button. None of it appears in the output. The output carries no text of any kind
except the printed text on the product itself.
```

Fill `[CHARACTER DIRECTION]` from the Brand DNA proposal the member approved.
`[BACKGROUND CATEGORY]` from the table above. `[NEW ROOM DESCRIPTION]` and
`[LIGHT DIRECTION AND QUALITY]` you write — concrete and specific, three or four details
each. Change nothing else.

**Never write "same background", "same lighting" or "same shadows" in this prompt.** Those
clauses contradict the room replacement, and the model resolves the contradiction by
compositing the subject onto the new room without relighting — which reads instantly as a
cut-out. The camera is held; the room and its light are rebuilt.

The "ignore the overlay" line is not optional. Anchors pulled from a paused player carry a
pause glyph and progress bar, and an image model will happily paint them back in.

**Renderer for the swap:** GPT Image 2 image-to-image. Proven on this brand — it reproduced
a tight brand ligature correctly across a five-still chain with no identity drift. Available on
Path C (fal.ai, `openai/gpt-image-2/edit`) and Path B (Higgsfield).

Generate the swaps, show them, and get approval before any video spends anything.

---

## 4. The Seedance 2.5 render prompt

Take the filled recreation prompt from the teardown and change only the Subject and Props
blocks to the member's character and products. Shot list, timings, framings and audio line
stay exactly as measured — that structure is the thing worth keeping.

### Facts that constrain the prompt

- **A voice or music, never both.** A generated voiceover sitting on a generated music bed
  is a mix the member cannot unpick afterwards, and the music is the part they would want
  to change. Voice chosen means the audio line is the voice with room tone and no music
  anywhere in the prompt. Music chosen means no voiceover and no talking at all. Either
  way the member lays their own track on afterwards in an editor, where they control level,
  timing, and swapping it out. **This holds even when the reference video has both** — the
  blueprint records what the reference did, the render prompt still picks one.
- **720p is the ceiling right now.** Seedance 2.5 currently renders 720p only; higher
  resolutions up to 4K are expected later. Never promise the member 1080p or 4K today, and
  never put a resolution in the prompt that the model cannot deliver.
- **The render prompt runs 4,800 to 5,000 characters, and never over 5,000.** That is the
  house band, not a model limit: Seedance 2.5 itself accetta molto di piu (alcuni transport
  arrivano a 30.000), but a teardown that lands in this band carries every shot,
  every label and every line of dialogue without padding, and that is what renders
  faithfully. An earlier note here claimed a 4,000 character cap; that number was wrong and
  is retired. Count before submitting, because cost endpoints do not validate length and a
  quote can succeed while the render still fails.
- **References only engage in `omni_reference` mode.** The default text-to-video mode
  accepts reference media and silently ignores it, which looks like a bad model and is
  actually a dropped input. If references are attached, the mode is `omni_reference`.
- **Up to 50 reference items**, bound by @-tag in the prompt text.
- **There is no per-shot reference binding.** A reference applies to the whole generation.
  You cannot say "use image 3 only for shot 5."

### Attach, in this order

1. The approved swapped still — the character and their world.
2. One image per brand product.

Then tag them in the prompt text the way the shot list needs.

### What this model does and does not honour

Measured by auditing a 12-shot render against its own prompt:

- Shot count, durations and cut positions are held tightly — 12 asked, 12 delivered, mean
  cut drift 0.15s, worst 0.38s, two cuts frame-exact.
- Framing is honoured on every shot.
- **Discrete physical events get dropped.** A spray, a cap going on, a lid flipping: the
  model renders the pose and skips the event. Give any such action its own shot with
  nothing else in it, or expect it missing.
- **Requested fps is ignored.** 60fps asked, 24fps delivered.

---

## 5. Offer the render path

Never render without an explicit go. Present the choice plainly, with the cost the member
is agreeing to:

- **Render it yourself** — hand over the prompt, the swapped still, the product images and
  the settings. Nothing is spent here.
- **Path B, Higgsfield CLI** — load `../../_shared/path-b-cli-implementation.md`. Read the
  member's balance and quote the cost before submitting.
- **Path C, fal.ai** — pay per result, gated by the `/pm-setup-fal-ai` skill. Run that
  first, always.
- **Path D, Playwright** — guida la web UI del renderer con `mcp__playwright`, un render per
  volta con conferma esplicita.

Quote the number, wait for the yes, then render. A quote is not approval.
