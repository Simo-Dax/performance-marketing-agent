# Persona Variations ,  5 Buyer Persona Rebuild Prompts

When the user requests persona variations, generate 5 complete reference image prompts. The prompts are model-agnostic, they work with either GPT Image 2 (recommended default) or Nano Banana 2 (the cheaper alternative). Each variation targets a distinct buyer persona sourced from the VOC document.

---

## What Changes Across Variations

**Stays identical in every variation:**
- The full layout and compositional structure of the original ad
- Visual zones, text placement positions, hierarchy
- Product image swap (same instruction in every prompt)
- Brand colour and identity swaps (same in every prompt)
- Campaign or offer layer ,  if the user provided an offer, it appears identically in all 5 variations
- Image style and treatment
- Preserve instructions

**Changes in every variation:**
- The headline ,  different angle, different pain point or desire, different emotional trigger
- The subheadline ,  supports the new headline angle
- The body copy ,  different customer language matching the persona
- The CTA ,  can vary slightly if the persona is at a different awareness level
- The hook mechanic ,  different variations can use different hook types

---

## How to Identify the 5 Personas

Pull the personas directly from the VOC document. Look for:

1. **The Awareness Level dimension** ,  different stages of Schwartz awareness found in the data. One persona may be problem-aware, another solution-aware, another most-aware.

2. **The Pain Point dimension** ,  the VOC will surface 6, 10 distinct pain points. Select the 3, 5 highest-frequency, highest-intensity ones as persona anchors.

3. **The Identity dimension** ,  the ICP section and identity language in the Language Goldmine will reveal different self-descriptions. "Busy parent," "fitness beginner," "professional wanting more energy" etc. are persona anchors.

4. **The Desire dimension** ,  different dream outcomes found in the desires section. One persona wants to feel confident, another wants to save time, another wants to impress others.

5. **The JTBD dimension** ,  functional job vs. emotional job vs. social job buyers are meaningfully different personas even for the same product.

If the VOC doesn't contain 5 clearly distinct personas, construct them from combinations of the above dimensions. Always ground each in actual VOC language.

---

## Persona Label Format

Label each variation clearly before the prompt:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VARIATION 1 ,  [Short persona description]
Awareness Level: [Unaware / Problem-Aware / Solution-Aware / Product-Aware / Most-Aware]
Hook Mechanic: [type]
Primary Emotion Activated: [emotion]
VOC Source: [quote or section this persona is based on]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Full prompt here]
```

The persona description should be a short, specific label ,  not a generic demographic. Good: "Exhausted mum who's tried everything" / "First-time buyer with price anxiety" / "Already knows the category, needs a reason to switch." Bad: "Female, 25, 45, interested in wellness."

---

## Writing the 5 Variation Prompts

Each prompt follows the same structure as the main rebuild prompt from `references/prompt-builder.md`:

1. Reference instruction (identical across all 5)
2. Brand identity swaps (identical across all 5)
3. Product image swap (identical across all 5)
4. Text swaps ,  THIS IS WHERE VARIATIONS DIVERGE
5. Preserve instructions (identical across all 5)
6. Quality instruction (identical across all 5)

Only Section 4 (text swaps) changes. Everything else copies from the base prompt.

---

## Writing the Copy for Each Variation

For each persona, follow this process:

**Step 1 ,  Identify the persona's dominant emotional state**
What are they feeling right now? Frustrated? Hopeful? Sceptical? Desperate? Aspirational? This determines the emotional register of the copy.

**Step 2 ,  Pick the hook mechanic that matches**
- Frustrated / stuck → Problem-agitation hook
- Hopeful / motivated → Aspiration / transformation hook
- Sceptical → Skeptic-to-believer / social proof hook
- Desperate / urgent → Fear/loss hook
- Aspirational → Identity / desire hook
- Ready to buy → Direct offer / bold claim hook

**Step 3 ,  Pull the exact customer language from VOC**
Go to the specific section of the VOC that matches this persona:
- Pain point personas → Sections 4 (Pain Points) and 13 (Language Goldmine ,  problem language)
- Desire personas → Sections 5 (Desires) and 13 (Language Goldmine ,  solution language)
- Identity personas → Section 2 (ICP) and Section 13 (identity language)
- Awareness-level personas → Section 8 (Awareness Level Deep Dive)
- Sceptic personas → Section 14 (Social Proof Arsenal ,  Skeptic-to-Believer quotes)

**Step 4 ,  Write the headline**
Match the original word count exactly (plus or minus 1 word maximum). This applies in every single variation. Use customer language from VOC. Compress the persona's core emotion/desire/pain into the headline's exact structure. If you cannot fit the language into the target word count, compress harder. Do not exceed the budget.

**Step 5 ,  Write supporting copy**
Subheadline, body copy, CTA, and badge all match the original word counts (plus or minus 1 word maximum). The word count discipline applies to every text element in every variation, not just the headline. Maintain the VOC language register. Do not shift tone between elements.

**Step 6 ,  Adjust CTA if awareness level differs**
- Unaware / Problem-Aware: soft CTA: "See How It Works" / "Learn More" / "Discover"
- Solution-Aware: medium CTA: "See [Brand Name]" / "Find Out More"
- Product-Aware / Most-Aware: direct CTA: "Shop Now" / "Get Yours" / "Claim Offer"

The CTA wording can shift by awareness level, but the word count must still match the original CTA's word count. If the original CTA is 2 words, every variation's CTA is 2 words.

---

## Quality Check for Variations

Before outputting all 5 variations, verify:

- [ ] All 5 personas are meaningfully distinct. Different emotional register, different angle, different hook mechanic.
- [ ] Every persona label cites a specific VOC source
- [ ] Every headline matches the original word count (within 1 word). Counted and confirmed for all 5.
- [ ] Every subheadline matches the original word count (within 1 word). Counted and confirmed for all 5.
- [ ] Every CTA matches the original word count (within 1 word). Counted and confirmed for all 5.
- [ ] Every badge/callout (if present) matches the original word count (within 1 word). Counted and confirmed for all 5.
- [ ] All body copy matches the original line count and approximate word count. Counted and confirmed for all 5.
- [ ] All copy is grounded in VOC language. No two variations use the same phrases.
- [ ] Each prompt is fully self-contained. No cross-references to other variations.
- [ ] CTAs vary appropriately by awareness level but still respect the word count rule.
- [ ] The brand identity and layout sections are identical across all 5
