# Prompt Builder ,  Reference Image Prompts for Variations

The prompts produced by this guide are model-agnostic. They paste cleanly into either GPT Image 2 (recommended default at high quality and 4K equivalent `image_size`) or Nano Banana 2 (the cheaper alternative). The prose below uses "the image model" to mean whichever of the two the member picks at the model picker step in `27_multiplier` (`/pm-multiplier`).

This guide tells you how to construct each variation's prompt. The user will upload their winning ad image as the brand and quality reference in the chosen model, alongside their 1 to 3 product images. Your prompt is the text instruction that tells the image model what to generate.

This is different from a rebuild prompt. In a rebuild, the reference image is a layout template to clone. In a multiply variation, the reference image is a brand and quality benchmark, and the prompt deliberately diverges from it visually while preserving the conversion mechanic.

---

## How Reference Image Prompts Work in Multiply 2.0

The image model uses the uploaded images in two roles:

1. **The winning ad image** is the brand identity, aesthetic quality, and structural skeleton reference. It tells the image model what brand world this lives in and what production quality bar to hit.

2. **The product images** are the source of truth for the product. The image model must render the product accurately from these images, not improvise from the winning ad's product depiction.

Your text prompt is what tells the image model to:
- Honor the brand and quality of the winning ad reference
- Render the product from the product images
- Use the variation's NEW visual scene, color world, and copy
- Preserve the structural skeleton (layout zones, text hierarchy)
- Preserve the conversion mechanic element (testimonial / claim / demo / lifestyle / etc.)

---

## Prompt Structure

Build each variation's prompt in this exact order.

---

### SECTION 1 ,  REFERENCE INSTRUCTION

Open with a single sentence that tells the image model how to treat the uploaded images:

> "Use the first uploaded image as the brand identity and production quality reference. Match the brand colors, typography style, and overall production polish. Use the additional uploaded image(s) as the source of truth for the product itself. Do not clone the layout or scene of the reference ad. Build a new ad as specified below, preserving the structural skeleton and conversion mechanic but with a genuinely different visual scene."

---

### SECTION 2 ,  STRUCTURAL SKELETON (preserved from original)

Lock the structural pattern extracted in Phase 1. Example:

> "Maintain this layout structure: [describe the structural skeleton from the analysis, e.g. 'top 60% is product on lifestyle background, bottom 40% is dark text block with white headline, logo bottom right']. Keep the same text hierarchy and proportional relationships."

This stays consistent across every variation.

---

### SECTION 3 ,  VISUAL SCENE (unique per variation)

This is where each variation diverges. Be specific about:

- **Setting/environment:** Exact location and context. Example: "a sun-drenched kitchen with marble countertops and herbs in small terracotta pots near the window"
- **Lighting:** Specific quality and direction. Example: "warm morning light from a window left of frame, golden tone, soft shadows"
- **Color world:** Dominant palette. Example: "warm whites, sage green, terracotta, no cool tones"
- **Surface/props:** What the product sits on or is surrounded by
- **Camera treatment:** Distance, angle, depth of field where relevant. Example: "shot on 35mm at f/2.0, slight depth of field"
- **Human element:** Person present? If yes, describe demographic, body language, expression. If no, state "no human in frame"

This section is the core of Andromeda variation. Every variation must read clearly different here.

---

### SECTION 4 ,  PRODUCT INTEGRATION

Tell the image model how to render the product in this variation:

> "Render the product from the uploaded product image(s). Place it in the scene as follows: [hero on the surface / held by the person / in mid-use / flatlay among complementary objects / etc.]. The product should be [scale relative to frame] and [angle/orientation]. Maintain accurate product details from the uploaded product image(s). Lighting on the product should match the scene's overall lighting (warm/cool/clinical/etc.)."

The product positioning style can vary across variations (one variation hero, another in-use, another hand-held) as long as the structural skeleton from Section 2 is preserved.

---

### SECTION 5 ,  CONVERSION MECHANIC ELEMENT (preserved from original)

Every variation must contain the structural element the original ad's conversion mechanic depends on. Reference the analysis. Example phrasings:

For testimonial-led originals:
> "Include a testimonial element: a short customer quote of [target word count] words rendered in [white/dark] text overlay, attributed to '[Name], [Credential]'. Five filled [brand color] stars beside or below the quote."

For claim-led originals:
> "Include a specific claim element: a bold falsifiable result rendered as the headline focal point. Example structure: '[NUMBER]% [OUTCOME]' or '[RESULT] in [TIMEFRAME]'."

For lifestyle-led originals:
> "Lead with the lifestyle moment. The product is part of the scene, not the hero. The viewer should feel the moment first, see the product second."

For demo-led originals:
> "Show the product in use or with its mechanism visible. The viewer must understand how it works from the image alone."

Adapt the language to match the original's specific mechanic.

---

### SECTION 6 ,  TEXT SWAPS

For every text element, write the exact replacement copy.

**Word count guidance:** Use the original ad's word counts as a reference for visual balance. Match where possible (within plus or minus 2 words on headlines, plus or minus 1 word on CTAs and badges). Do not lock copy length so tightly that you sacrifice the angle. The whole point is variation.

**Format for each text element:**

> "HEADLINE: '[YOUR EXACT HEADLINE HERE]' (target word count: [X words], original was [Y words]).
> Render as [bold sans-serif / matching the brand typography from the reference image]. Position: [top / center / bottom], [left / center / right]. Color: [white / dark / brand color]."

> "SUBHEADLINE: '[YOUR EXACT SUBHEADLINE HERE]' (target word count: [X words]).
> Smaller than headline, same color treatment unless the variation calls for contrast."

> "BODY COPY: '[YOUR EXACT BODY COPY HERE]' (target line count: [X lines], target word count: approximately [X words]).
> Maintain the same approximate text block dimensions as the original."

> "CTA: '[YOUR EXACT CTA HERE]' (target word count: [X words]).
> [Button style / plain text / badge style], [position]."

> "BADGE/CALLOUT: '[YOUR EXACT BADGE HERE]' (target word count: [X words], if the variation includes one)."

**Rules for writing the replacement copy:**

- **Use verbatim customer language from the VOC document wherever possible.** Pull real phrases from the Language Goldmine, not invented copy.
- **Match this variation's hook mechanic, not the original's.** Each variation has a different hook. Write copy that lives inside that hook's logic.
- **Match this variation's awareness level.** A Problem-Aware variation does not name the product. A Most-Aware variation can lead with price or urgency.
- **Match the brand's tone.** Casual stays casual. Clinical stays clinical. Check the Brand DNA.
- **Never repeat a headline or key phrase across two variations.** Every variation's hero copy must be distinct.

---

### SECTION 6b ,  CAMPAIGN OR OFFER LAYER (if the user provided one)

If the user said "all variations" include the offer in every prompt. If "mix", include in roughly half (the variations targeting Most-Aware, Product-Aware, or Solution-Aware audiences).

**If the variation includes an offer:**

If there is a CTA, the offer goes in the CTA:
> "CTA: '[OFFER-DRIVEN CTA, e.g. Get 20% Off / Claim Free Trial / Shop the Sale]'."

If there is a badge or callout slot:
> "Badge: '[OFFER TEXT, e.g. Limited Time / 20% Off This Week / Free Shipping]'."

If the offer changes the headline angle:
> "Headline: '[HEADLINE WITH OFFER ANGLE, e.g. Finally Clear Skin, Now 20% Off]'."

**Offer integration rules:**
- The offer must be real, use exactly what the user described
- Do not force an offer into a placement that doesn't exist in the structural skeleton
- The offer must respect the word count guidance (plus or minus 1 word on the element it sits in)

---

### SECTION 7 ,  BRAND IDENTITY LOCK

Every variation must stay on-brand. Reference the Brand DNA:

> "Brand colors: [primary hex], [secondary hex], [accent hex]. Apply these to text, graphic elements, and any color-coded zones. Brand logo: place [bottom right / bottom center / position from analysis] in [white / brand color]. Typography style: match the reference image's typography family (sans-serif, weight, character). Overall production quality: match the polish of the reference image."

This section is identical across every variation.

---

### SECTION 8 ,  QUALITY INSTRUCTION

Close with a single quality directive:

> "The output should look like a polished, production-ready static Meta ad. All text must be sharp, legible, and correctly spelled. Product details must match the uploaded product image accurately. The scene should feel intentional, not stock or generic. The ad should look distinctly different from the reference ad in scene, color world, and composition while still feeling unmistakably from the same brand."

---

## Prompt Length and Format

Each finished prompt should be 250 to 450 words. Long enough to be precise, short enough to be processed cleanly by the image model.

Write in clear, direct instruction language. No bullet points inside the prompt itself. Write it as flowing instructions that the image model reads as a directive. Avoid decorative language. Be surgical.

---

## How to Source the Copy from the Documents

### From the Brand DNA document, extract:
- Brand name and product name
- Core product positioning statement
- Key product benefits (in brand's language)
- Brand visual identity (colors, font style, aesthetic)
- Tone of voice descriptors
- Any specific phrases or language the brand uses consistently

### From the VOC document, extract:
- The most emotionally resonant pain point matching THIS variation's hook mechanic
- The most powerful desire/dream outcome phrases for this variation's angle
- Before/after language pairs (especially for transformation hooks)
- High-intensity phrases from the Language Goldmine
- Identity language matching this variation's awareness level
- For testimonial-style variations: real quotes from the Social Proof Arsenal

### Matching hook mechanic to VOC section:
- Bold result / transformation hook → After-State Visual Descriptions and Before/After pairs
- Problem-agitation hook → top pain points and struggling moment language
- Curiosity gap hook → "I wish" and unmet desire language
- Relatability hook → identity language and situation descriptions
- Social proof hook → top testimonials from Social Proof Arsenal
- Direct offer hook → Value Equation language, Dream Outcome plus Time Delay
- Aspiration hook → identity-led desire language and future-self phrases

---

## Self-Check Before Finalising Each Variation Prompt

Before outputting each variation's prompt, verify:

- [ ] The reference instruction in Section 1 tells the image model to use the winning ad image as brand and quality reference, not as layout to clone
- [ ] The product is rendered from the user's uploaded product image, not from the reference ad
- [ ] The structural skeleton from the original is preserved
- [ ] The conversion mechanic element is preserved (testimonial / claim / demo / lifestyle / etc.)
- [ ] The visual scene is genuinely different from the original AND from every other variation
- [ ] The color world is genuinely different from the original AND from every other variation
- [ ] All text elements have exact replacement copy written, no placeholders
- [ ] Headline word count is within plus or minus 2 words of the original
- [ ] CTA word count is within plus or minus 1 word of the original
- [ ] All replacement copy is sourced from Brand DNA or VOC, no generic phrases
- [ ] The hook mechanic for this variation is distinct from every other variation
- [ ] The awareness level for this variation is appropriate for the hook
- [ ] If an offer was specified for this variation, it's integrated cleanly
- [ ] The prompt reads as a complete, self-contained directive, user can copy-paste with zero edits

---

## Self-Check Across All Variations (run before final output)

After writing all prompts, audit the full set:

- [ ] Every variation uses a different visual scene from every other variation AND from the original
- [ ] Every variation uses a different color world from every other variation AND from the original
- [ ] Every variation uses a different hook mechanic from every other variation
- [ ] Awareness levels are spread across at least 3 stages
- [ ] No two variations share the same headline or hero phrase
- [ ] Every variation honors the original's conversion mechanic
- [ ] All variations stay on-brand per the Brand DNA
- [ ] If "mix" was specified for the offer, the offer appears in roughly half the variations, weighted toward higher awareness levels

If any check fails, revise before delivering the final output to the user.
