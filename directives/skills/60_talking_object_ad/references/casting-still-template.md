# Casting stills — the Studio Talking Object template (tier 2 references)

This file generates the reference images a talking-object run needs — and ONLY the ones
the reference ladder demands. It uses the prompt template the il sistema app Studio uses
for its Talking Object style (helper/templates.mjs, style id `talking-object`, kept in
sync by hand).

## When a still is needed (the ladder decides — never generate stills by default)

| Scene contains | Still required | File |
|---|---|---|
| Generic character only (enzyme, root, leaf, personified problem) | **NONE** — tier 1 renders from the bible alone | — |
| A personified real product (full-cast mode: face built into the label) | **CASTING STILL**, generated WITH the real product photo attached | `$WORK/inputs/casting-still.png` |
| An un-personified real product (dignity mode, or a straight product beat) | **PRODUCT STILL**, generated WITH the real product photo attached | `$WORK/inputs/product-still.png` |

The CTA always shows the product, so every run with a product generates at least one of
the two. A stack/duo stages ALL its products together in ONE still (the duo is one
speaker). Tier-1 characters may OPTIONALLY get a cheap preview still if the member wants
to see a design before video — but that preview is for APPROVAL ONLY and is **never
attached to the video generation** (tier 1 renders reference-free; a needless reference
narrows the render).

## The prompt template (7 sections; three LOCKED, copied verbatim, never paraphrased)

```
SCENE: <one vivid sentence: the character bible from script.json VERBATIM — the product
as a cute Pixar-style talking character with a face built into its own body — doing its
signature business from the storyboard, personality readable in the big expressive eyes>

ENVIRONMENT: The scene takes place in <this character's own world from the script — its
concrete props, materials, and light sources>. Include natural supporting details and
props that fit, while keeping the subject the clear focus.

COMPOSITION: Use a hero shot, positioning the product character centered with strong
separation between foreground, subject, and background. Make the action immediately clear.

LIGHTING: <the scene's light from the storyboard; default: warm golden rim light plus a
soft key light, with subsurface scattering, controlled highlights, soft shadows, and
gentle atmospheric depth. The lighting should support a warm, energetic, premium mood.>

VISUAL STYLE: Cute Pixar style ultra detailed 3D animated render, smooth professional
textures, glossy realistic product surface, shallow depth of field, expressive but
believable posing, cinematic and high end, with a cohesive warm, vibrant color grade.

FORMAT: 9:16 vertical composition, high resolution, full frame image designed for a
cinematic social media advertisement.

NEGATIVE INSTRUCTIONS: No watermark, no UI, no extra limbs, no duplicated body parts, no
warped or unreadable label, no melted or distorted packaging, no mixed art styles, no out
of frame subject, no creepy uncanny face, no on-screen text, no captions, no real human
being or photoreal person.
```

**For the CASTING STILL (personified product), append this section** (the Studio's
Talking Object rule, adapted verbatim) and attach the member's real product photo as the
generation reference:

```
PRODUCT: Show the uploaded product from the reference image itself as a cute Pixar style
talking character with a face built into its own body, big expressive eyes, a visible
mouth, and tiny arms — <its signature moment from the storyboard>. Keep its real shape,
label and colors fully intact so it still reads as the real object.
```

**For the PRODUCT STILL (un-personified, dignity mode), append instead:**

```
PRODUCT: Feature the uploaded product from the reference image, sitting in the scene as
the hero object. Render the product as a polished Pixar style 3D prop that matches the
scene, BUT keep its real shape, label, logo, text and colors fully readable and
recognizable.
```

**When the product is software or an app**, the "photo" is a screenshot and the screen
must reproduce THAT EXACT screenshot — same layout, same sections, titles legible — never
an invented interface.

## Render settings

- Model: **Nano Banana 2** (the Studio's pick), 9:16, 2K.
- Path B, Higgsfield CLI: `higgsfield generate create nano_banana_2 --prompt "<assembled
  prompt>" --aspect_ratio 9:16 --resolution 2k --image "$WORK/inputs/<real product
  photo>"`. Confirm the live cost with `higgsfield generate cost` first.
- Path C, fal.ai (gated by `fal-ai-prerun-check`): model `fal-ai/nano-banana-2`,
  `aspect_ratio "9:16"`, `resolution "2K"`, `output_format "png"`, `num_images 1`,
  `image_urls` carrying the real product photo. Confirm cost with
  the fal-ai MCP `get_pricing` tool.
- Path A, manual: hand the member the assembled prompt for https://aistudio.google.com/
  (Nano Banana 2, 9:16) with the instruction to attach their real product photo; they
  drop the result into `$WORK/inputs/`.
  explicit confirmation per generation.

Stills are paid renders: quote the cost and get an explicit yes before generating.

## The approval loop (cheap, before any video)

- Casting still: "This is your product as a character — face in the label, label fully
  readable. This exact design appears in every product scene. Happy? (yes / tell me what
  to change)"
- Product still: "This is your product staged in the ad's world, label intact. Happy?
  (yes / tell me what to change)"

Iterate on a no (adjust SCENE, ENVIRONMENT, or LIGHTING — never the locked sections) and
re-render until yes. **No product scene renders before its still is approved.** The
approved still is then attached (`--image` / the image-reference slot) on every scene
that shows the product — including tier-3 scenes, alongside the voice_ref clip.

## Hard rules

| Rule | Detail |
|---|---|
| The ladder decides | No still for tier-1 characters (and an optional preview still is never attached to video); a still is mandatory the moment a real product is in frame. |
| Locked sections are verbatim | VISUAL STYLE, FORMAT, NEGATIVE INSTRUCTIONS, and the PRODUCT rules copy exactly as written here. Only SCENE, ENVIRONMENT, COMPOSITION, LIGHTING adapt per run. |
| The label is the face | On a casting still the eyes/mouth are built INTO the real label art and every word of the label stays legible — a warped label is an automatic re-roll. |
| The product never renders from text | Every still generates WITH the real photo attached; every product scene attaches the approved still. |
| App screens are exact | Software products reproduce the exact uploaded screenshot, never an invented UI. |
| Same spend law | Every still render gets a cost quote and an explicit yes. |
