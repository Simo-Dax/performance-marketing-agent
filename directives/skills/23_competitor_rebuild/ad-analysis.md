# Ad Analysis Framework ,  Competitor Ad Breakdown

When you receive the competitor ad image, analyse every element below. Be precise and specific. This analysis feeds directly into the rebuild prompt ,  vague observations produce vague prompts.

---

## 1. LAYOUT & COMPOSITION

- **Format:** What are the approximate dimensions? Square (1:1), portrait (4:5 or 9:16), landscape (1.91:1)?
- **Visual zones:** How is the image divided? Describe the regions ,  e.g. "top 60% is product image, bottom 40% is text block on dark background"
- **Dominant focal point:** What does the eye land on first? Product? Face? Headline text?
- **Text placement:** Where does each text element sit? (top-left, centred, bottom overlay, beside product, etc.)
- **Negative space:** Is there deliberate empty space, and where?
- **Overall visual weight:** Is the design minimal/clean or dense/busy?

---

## 2. TEXT INVENTORY ,  CRITICAL, BE EXACT

For every piece of text visible in the ad, record the word count. Word counts feed directly into the rebuild prompt and dictate how the replacement copy must be written. Be precise. Count every word.

**HEADLINE (the largest/most prominent text):**
- Exact text (if legible) or approximate content
- Word count: [X words]
- Character count including spaces: [approximately X characters]
- Font weight: bold / semi-bold / regular
- Font size relative to image: large / medium / small
- Colour: [hex if determinable, or description]
- Position: [where on the image]
- All caps / title case / sentence case?

**SUBHEADLINE or SECONDARY TEXT (if present):**
- Exact text (if legible) or approximate content
- Word count: [X words]
- Character count including spaces: [approximately X characters]
- Font weight, size, colour, position (same breakdown as headline)
- All caps / title case / sentence case?

**BODY COPY (if present):**
- Exact text (if legible) or approximate content
- Word count: [X words]
- Line count: [X lines]
- Position and size relative to headline

**CTA / BUTTON TEXT (if present):**
- Exact text or close approximation
- Word count: [X words]
- Style: button / plain text / badge?
- Position

**BADGE, LABEL, or CALLOUT (if present, e.g. "New", "Sale", "As seen in..."):**
- Exact or approximate text
- Word count: [X words]
- Style and position

**OVERLAY TEXT or GRAPHIC TEXT (text integrated into the image, not just a text layer):**
- Describe any text that appears to be part of the visual scene
- Word count for each piece: [X words]

---

## 3. COPY STRATEGY ANALYSIS

- **Hook mechanic:** What type of hook does this ad use?
  - Curiosity gap ("You won't believe...")
  - Bold claim / specific result ("Lost 12kg in 8 weeks")
  - Pattern interrupt / contrarian ("Stop using X")
  - Relatability ("Every mum knows this feeling")
  - Social proof ("10,000 customers can't be wrong")
  - Problem-agitation ("Still struggling with X?")
  - Direct offer ("50% off today only")
  - Before/after ("From X to Y in Z days")

- **Awareness level targeted:** Which Schwartz stage does this ad speak to?
  - Unaware (no mention of problem or product ,  identity/lifestyle led)
  - Problem-Aware (names the pain, no solution yet)
  - Solution-Aware (category-level, no brand name)
  - Product-Aware (brand/product specific)
  - Most-Aware (direct offer, price, urgency)

- **Primary emotion activated:** What emotion does this ad trigger in the viewer? (frustration, desire, fear, curiosity, relief, aspiration, belonging, FOMO)

- **Tone:** Clinical / authoritative / warm / casual / humorous / urgent / aspirational?

- **What the copy promises:** In one sentence, what does this ad promise the viewer?

---

## 4. VISUAL & PRODUCT ELEMENTS

- **Product placement:** Is the product visible? How prominent? Centre stage, corner, held by person, lifestyle context, flat lay?
- **Background:** Solid colour, gradient, lifestyle scene, studio? Describe colour/mood.
- **Human element:** Is there a person in the ad? Face visible? What expression/body language?
- **Props or context objects:** What else appears in the image beyond the product?
- **Colour palette:** List the 2, 4 dominant colours. Describe the overall palette mood (warm/cool, bold/muted, dark/light).
- **Image style:** Photographic / illustrated / graphic design / collage / screenshot / mockup?
- **Social proof visual elements:** Any stars, review snippets, logos, certification badges?

---

## 5. WHAT MADE THIS AD WORK

Write 3, 5 bullet points on why this ad is likely performing. Consider:
- The specific hook and why it stops the scroll
- The clarity and simplicity of the promise
- The visual contrast or focal point that draws the eye
- The awareness level match to a cold audience
- Any trust signals present
- The format efficiency ,  how much it communicates in how little space

This is your strategic brief for the rebuild. The goal is to preserve these winning properties while substituting the brand, product, and copy.

---

## 6. SWAP REQUIREMENTS SUMMARY

List every element that needs to be changed for the rebuild, in priority order. Include the exact target word count for every text element. The word count is the most important constraint for the rebuild prompt.

1. **Headline** needs new copy [target: X words, X characters, same format]
2. **Subheadline** needs new copy [target: X words, same format]
3. **Body copy** needs new copy [target: X words, X lines]
4. **CTA** needs new copy [target: X words]
5. **Badge/Callout** needs new copy [target: X words] (if present)
6. **Product image** needs to be replaced with user's product
7. **Brand colours** needs to be replaced with [Brand DNA colours]
8. **Logo/brand name** needs to be replaced (if present)
9. **Background** keep as-is / adapt colour to brand palette
10. **Any other element** [describe]

Everything not on this list stays exactly as it is in the reference image.
