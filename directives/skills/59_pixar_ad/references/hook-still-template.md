# Reference stills, the Pixar still template (mirrors the il sistema Studio)

This file generates the TWO reference images every Pixar ad run needs, using the prompt
template the il sistema app Studio uses for its Pixar style (helper/templates.mjs, style id
`pixar`, kept in sync by hand), extended with the cast-per-brand Character Bible from
`pixar-style.md`. The stills are cheap, approved by the member BEFORE any video credits
burn, and then drive the video generations:

1. **The HOOK STILL** (`$WORK/inputs/hook-still.png`): the cast Pixar hero in the hook
   scene's animated world (the hook ALWAYS contains the character). The hook video renders
   image-to-video FROM this still (its literal first frame), and every other
   character-visible scene attaches this SAME still as its IDENTITY image reference — it is
   the single source of character truth for the whole ad. A video clip is never used as a
   reference.
2. **The PRODUCT STILL** (`$WORK/inputs/product-still.png`): the member's product staged as
   a **polished Pixar-style 3D prop** inside the ad's world — real shape, label, logo, text
   and colors fully readable — generated WITH the real product photo attached as the
   generation reference. Every scene that displays the product attaches this still, so the
   product never renders from text description.

## The prompt template (7 sections, three locked, filled from the run)

Assemble each still prompt as these sections in this order. SCENE, ENVIRONMENT, COMPOSITION,
and LIGHTING are written per run; VISUAL STYLE, FORMAT, and NEGATIVE INSTRUCTIONS are LOCKED
and copied verbatim, never paraphrased.

```
SCENE: <one vivid sentence: the cast Character Bible from pixar-style.md VERBATIM
(including this scene's emotion/state), doing WHAT (the hook's opening beat), with the
emotion readable in the large expressive eyes and body language; name any Pixar witnesses
and what they do>

ENVIRONMENT: The scene takes place in <the hook scene's animated set with its concrete
props, materials, and light sources>. Include natural supporting details and props that fit,
while keeping the subject the clear focus.

COMPOSITION: Use a medium shot, positioning the character centered with strong separation
between foreground, subject, and background. Make the action immediately clear.

LIGHTING: <the scene's light from the storyboard; default: warm golden rim light plus a
soft key light, with subsurface scattering, controlled highlights, soft shadows, and gentle
atmospheric depth. The lighting should support a warm, energetic, premium mood.>

VISUAL STYLE: Cute Pixar style ultra detailed 3D animated render, smooth professional
textures, shallow depth of field, expressive but believable posing, cinematic and high end,
with a cohesive warm, vibrant color grade.

FORMAT: 9:16 vertical composition, high resolution, full frame image designed for a
cinematic social media advertisement.

NEGATIVE INSTRUCTIONS: No text, no captions, no watermark, no UI, no extra limbs, no
duplicated body parts, no warped or unreadable logo, no mixed art styles, no glossy plastic
over render, no distorted anatomy, no out of frame subject, no creepy uncanny face, no real
human being or photoreal person.
```

**For the PRODUCT STILL, append this section** (the Studio's Pixar product rule, verbatim)
and attach the member's real product photo as the generation reference image:

```
PRODUCT: Feature the uploaded product from the reference image, sitting in the scene as the
hero object. Render the product as a polished Pixar style 3D prop that matches the scene,
BUT keep its real shape, label, logo, text and colors fully readable and recognizable.
```

For the product still, SCENE describes the product as the subject (for example: the product
standing hero-lit on a warm kitchen counter, pin-sharp while the animated world blurs
behind it), ENVIRONMENT is a set drawn from the ad's world, and COMPOSITION becomes: Use a
hero shot, positioning the product centered with strong separation between foreground,
subject, and background. **When the product is software or an app, the "photo" is a
screenshot and the screen must reproduce THAT EXACT screenshot — same layout, same sections,
titles legible — never an invented interface.** A stack offer stages ALL its products
together in one still.

## Render settings

- Model: **Nano Banana 2** (the Studio's pick), 9:16, 2K.
- Path B, Higgsfield CLI: `higgsfield generate create nano_banana_2 --prompt "<assembled
  prompt>" --aspect_ratio 9:16 --resolution 2k` (add `--image "$WORK/inputs/<product
  photo>"` for the product still). Confirm the live cost with `higgsfield generate cost`
  first.
- Path C, fal.ai (gated by `fal-ai-prerun-check`): model `fal-ai/nano-banana-2`,
  `aspect_ratio "9:16"`, `resolution "2K"`, `output_format "png"`, `num_images 1`,
  `image_urls` carrying the uploaded product photo for the product still. Confirm cost with
  the fal-ai MCP `get_pricing` tool.
- Path A, manual: hand the member the assembled prompt for https://aistudio.google.com/
  (Nano Banana 2, 9:16), they drop the result into `$WORK/inputs/`.
  per generation.

Stills are paid renders: quote the cost and get an explicit yes before generating, same law
as every other spend in this skill.

## The approval loop (cheap, before any video)

Show the member each still and ask exactly one question per still:

- Hook still: "This is the character and world every scene will inherit. Happy with the
  hero, the emotion, the set, and the light? (yes / tell me what to change)"
- Product still: "This is your product staged in the ad's world, label intact. Happy?
  (yes / tell me what to change)"

Iterate on a no (adjust SCENE, ENVIRONMENT, or LIGHTING — never the locked sections) and
re-render until yes. Only after BOTH stills are approved does any video generation begin.
The approved hook still becomes the hook scene's image-to-video START IMAGE AND the
identity image reference attached to every other character-visible scene; the approved
product still becomes the attached image for every product scene. These two stills are the
only references in the whole build — never a video clip.

## Hard rules

| Rule | Detail |
|---|---|
| Locked sections are verbatim | The VISUAL STYLE block, FORMAT, NEGATIVE INSTRUCTIONS, and the PRODUCT rule are copied exactly as written here. Only SCENE, ENVIRONMENT, COMPOSITION, LIGHTING adapt per run. |
| The Bible never drifts | The cast Character Bible's wording is identical in the still prompt and in every later video prompt; only the bracketed emotion/state slot changes. |
| The product never renders from text | Any scene that displays the product uses the approved product still (generated WITH the real photo attached). The Pixar prop keeps the real shape, label, logo, text and colors fully readable. |
| App screens are exact | For software products the screen reproduces the exact uploaded screenshot layout, sections and titles, never an invented UI. |
| Stills before video | The hook video never renders before the hook still is approved. Product scenes never render before the product still is approved (the CTA always shows the product). |
| No text anywhere | Neither still contains any text besides the real product's own label. No banners with words, no invented UI, no labels. |
| Same spend law | Every still render gets a cost quote and an explicit yes. |
