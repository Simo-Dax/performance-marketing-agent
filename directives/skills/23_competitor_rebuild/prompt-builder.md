# Prompt Builder ,  Reference Image Prompt

The prompt produced by this guide is model-agnostic. It pastes cleanly into either GPT Image 2 (recommended default at high quality and 4K equivalent `image_size`) or Nano Banana 2 (the cheaper alternative). The prose below uses "the image model" to mean whichever of the two the member picks at the model picker step in `23_competitor_rebuild` (`/pm-competitor-rebuild`).

This guide tells you how to construct the rebuild prompt. The user will upload the competitor ad image as the reference image in the chosen model, alongside their product image. Your prompt is the text instruction that tells the image model what to change and what to keep.

---

## How Reference Image Prompts Work

The image model uses the uploaded reference image as a structural and compositional template. It reads your text prompt to understand what to modify. Your job is to:

1. Lock the layout ,  tell the image model to preserve the original composition
2. Specify every visual swap ,  product, colours, brand elements
3. Pre-write every text swap ,  give the image model the exact words to use
4. Never leave decisions to the image model ,  if you don't specify it, the image model will improvise

---

## Prompt Structure

Build the prompt in this exact order:

---

### SECTION 1 ,  REFERENCE INSTRUCTION

Open with a single sentence that tells the image model how to treat the uploaded image:

> "Use the uploaded image as the compositional reference. Preserve the exact layout, visual zones, text placement positions, and overall structure. Do not redesign ,  only replace the specific elements listed below."

---

### SECTION 2 ,  BRAND IDENTITY SWAPS

Pull from the Brand DNA document. List every brand-level visual change:

**Format:**
> "Replace the brand colour palette with: [primary colour hex], [secondary colour hex], [accent colour hex]. Apply these to backgrounds, text elements, and graphic shapes."
>
> "Replace any logo or brand name visible in the ad with: [brand name] in [brand font style if specified in Brand DNA, otherwise: clean sans-serif]."
>
> "Maintain the overall colour mood/temperature as [warm/cool/neutral] ,  shift the palette toward [brand palette description from Brand DNA]."

---

### SECTION 3 ,  PRODUCT IMAGE SWAP

The user is uploading their product image separately into the image model. Write the instruction:

> "Replace the product in the reference image with the second uploaded product image. Place the product in the same position and at the same scale as the original product in the reference. Maintain the same angle and orientation if possible. [Add any specific product context from Brand DNA ,  e.g. 'The product is a glass bottle with a gold cap' ,  so the image model renders it correctly.]"

If the original had a lifestyle context (product being held, product in a scene), specify:
> "Keep the [lifestyle element / background scene] from the reference image. Integrate the new product into this scene naturally."

---

### SECTION 4 ,  TEXT SWAPS

This is the most critical section. For every text element identified in the ad analysis, write the exact replacement.

#### THE WORD COUNT RULE (read this first, every time)

Every replacement copy element must match the original word count of that element as closely as possible. This is non-negotiable.

The acceptable tolerance is plus or minus 1 word maximum. A 4-word headline becomes a 3, 4, or 5 word headline. Never a 7-word headline. Never a 2-word headline. The same rule applies to the subheadline, the CTA, the badge, the callout, the body copy line count, and every other text element on the ad.

The reason: the original ad's visual balance, text block dimensions, and reading rhythm are part of why it converts. If you write a 9-word headline to replace a 4-word one, the ad's visual hierarchy collapses, the headline overflows its zone, and the new ad will not look or perform like the winning ad.

Before you write any replacement copy, look at the ad analysis and write down the exact word count of every text element. Then write copy that matches those word counts. If you cannot fit the customer language into the target word count, compress harder. Use shorter words. Cut filler. The word count is the constraint, not a suggestion.

**Format for each text element (always include the target word count in the prompt itself):**

> "HEADLINE: Replace the headline text with: '[YOUR EXACT HEADLINE HERE]' (target word count: [X words], matching the original).
> Keep the same font weight (bold), same font size relative to the image, same position ([top/centre/bottom], [left/centre/right]), same colour treatment ([white text / dark text / coloured text as in original])."

> "SUBHEADLINE: Replace the subheadline with: '[YOUR EXACT SUBHEADLINE HERE]' (target word count: [X words], matching the original).
> Same size, position, and colour as original."

> "BODY COPY: Replace the body text with: '[YOUR EXACT BODY COPY HERE]' (target line count: [X lines], target word count: approximately [X words], matching the original).
> Maintain the same approximate line count ([X lines]) and text block dimensions."

> "CTA: Replace the CTA text with: '[YOUR EXACT CTA HERE]' (target word count: [X words], matching the original).
> Keep the same button/text style, colour, and position."

> "BADGE/CALLOUT: Replace the badge text with: '[YOUR EXACT BADGE HERE]' (target word count: [X words], matching the original).
> Keep the same position and style."

**Rules for writing the replacement copy:**

- **Word count match is the first rule, every time.** Plus or minus 1 word maximum on every element. Verify each element by counting before you finalise.
- **Use verbatim customer language from the VOC document wherever possible.** Pull real phrases, not invented copy.
- **Align the hook mechanic to the original.** If the original used a bold result claim, your replacement uses a bold result claim, just for this brand's product. If it used a problem hook, yours uses a problem hook.
- **Match the tone.** Casual = casual. Clinical = clinical. Check the Brand DNA tone of voice.
- **For the headline:** Extract the single most powerful pain point or desire from the VOC document that matches the hook mechanic of the original. Compress it to the original word count, even if you have to cut adjectives or simplify phrasing.
- **For body copy:** Use the feature-to-benefit language and customer phrases from the VOC document. Match the line count and approximate word count of the original. Do not write generic ad copy.
- **For the CTA:** Match the original CTA type (discovery CTA like "Learn More" / commitment CTA like "Shop Now" / soft CTA like "See How"). Match the exact word count. Check the brand's preferred CTA language in the Brand DNA doc.

---

### SECTION 4b ,  CAMPAIGN OR OFFER LAYER (only if the user provided one)

If the user specified a campaign, discount, promotion, or specific offer, weave it into the ad as follows:

**If the original ad has a CTA button or badge**, this is the primary place to inject the offer:
> "CTA: Replace the CTA with: '[OFFER-DRIVEN CTA ,  e.g. "Get 20% Off", "Claim Free Trial", "Shop the Sale"]'. Keep the same button style, colour, and position."

**If the original ad has a badge, label, or callout element**, use it for the offer:
> "Badge/Label: Replace with: '[OFFER TEXT ,  e.g. "Limited Time", "20% Off This Week", "Free Shipping"]'. Keep the same position and style."

**If the offer changes the promise of the ad** (e.g. it's a launch deal that would affect the headline angle), reflect it in the headline:
> "Adjust the headline to incorporate the offer: '[HEADLINE WITH OFFER ANGLE ,  e.g. "Finally Clear Skin ,  Now 20% Off"]'. Match the original word count as closely as possible."

**If no offer was provided**, skip this section entirely. Do not add a generic offer or invent a promotion.

**Offer integration rules:**
- The offer must be real. Use exactly what the user described, not a paraphrase
- Do not force an offer into a placement that doesn't exist in the original ad's layout
- If the original ad has no badge/callout element, inject the offer into the CTA only
- The offer must still respect the word count rule. Match the word count of the element it replaces, plus or minus 1 word maximum

End the prompt with explicit keep-as-is instructions:

> "Keep the following elements exactly as they appear in the reference image:
> ,  Overall layout and compositional zones
> ,  Text placement positions and hierarchy
> ,  Background style and atmosphere [unless colour swap specified above]
> ,  Visual style and image treatment
> ,  Any graphic elements not listed above for replacement"

---

### SECTION 6 ,  QUALITY INSTRUCTION

Close with a single quality directive:

> "The output should look like a polished, production-ready static Meta ad. All text must be sharp, legible, and correctly spelled. Brand elements should feel cohesive and intentional."

---

## How to Source the Copy from the Documents

### From the Brand DNA document, extract:
- Brand name and product name
- Core product positioning statement
- Key product benefits (in brand's language)
- Brand visual identity (colours, font style, aesthetic)
- Tone of voice descriptors
- Any specific phrases or language the brand uses consistently

### From the VOC document, extract:
- The most emotionally resonant pain point matching the hook mechanic of the original ad
- The most powerful desire/dream outcome phrases
- Before/after language pairs
- High-intensity phrases from the Language Goldmine section
- Identity language that matches the audience level of the original ad
- The dominant awareness level ,  use language appropriate to it

### Matching hook mechanic to VOC section:
- Bold result / transformation hook → use After-State Visual Descriptions + Before/After pairs from VOC
- Problem-agitation hook → use top pain points + struggling moment language from JTBD section
- Curiosity gap hook → use "I wish" and unmet desire language from Language Goldmine
- Relatability hook → use identity language + situation descriptions from ICP section
- Social proof hook → use top testimonials from Social Proof Arsenal
- Direct offer hook → use Value Equation language ,  Dream Outcome + Time Delay

---

## Prompt Length and Format

The finished prompt should be 200, 400 words. Long enough to be precise, short enough to be processed cleanly by the image model.

Write in clear, direct instruction language. No bullet points inside the prompt itself ,  write it as flowing instructions that the image model reads as a directive. Avoid decorative language. Be surgical.

---

## Self-Check Before Finalising

Before outputting the prompt, verify:

- [ ] Every text element from the ad analysis has an exact replacement written. No placeholders.
- [ ] Replacement headline matches original word count (within 1 word). Counted and confirmed.
- [ ] Replacement subheadline matches original word count (within 1 word). Counted and confirmed.
- [ ] Replacement CTA matches original word count (within 1 word). Counted and confirmed.
- [ ] Replacement badge/callout (if present) matches original word count (within 1 word). Counted and confirmed.
- [ ] Body copy matches original line count and approximate word count (within 10 percent). Counted and confirmed.
- [ ] Every text element instruction in the prompt includes the target word count so the image model sees the constraint.
- [ ] All replacement copy is sourced from Brand DNA or VOC. No invented generic phrases.
- [ ] Product swap instruction references the user's uploaded product image
- [ ] Brand colour swaps reference specific values from the Brand DNA doc
- [ ] Preserve instruction lists everything that should stay unchanged
- [ ] Prompt reads as a complete, self-contained directive. User can copy-paste with zero edits.
