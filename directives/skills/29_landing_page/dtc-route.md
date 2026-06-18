# DTC Route, Section Order and Patterns

For ecommerce product landing pages from Meta paid traffic. Single primary CTA = Add to Cart or Buy Now.

## Section order (mandatory)

1. **Hero** (with embedded social proof)
2. **Problem agitation** (VOC pain quote)
3. **Product reveal or "The new way"** (mechanism in 1 to 2 sentences, then visual)
4. **Benefit grid** (3 to 6 outcome bullets from VOC)
5. **Social proof block** (testimonials with photos + UGC if available)
6. **Comparison table** (vs the alternative the customer was using)
7. **Detailed product info** (ingredients, specs, materials, transparency builds trust)
8. **Founder story** (why we built this, 3 to 5 sentences max)
9. **Stack of reviews** (5+ shorter reviews with star ratings)
10. **FAQ** (verbatim VOC questions)
11. **Guarantee block** (specific risk reversal)
12. **Final CTA** (matches hero CTA destination)
13. **Mobile sticky CTA bar** (visible after hero scroll, always present)
14. **Minimal footer** (3 lines max, copyright, privacy, terms)

## Hero composition

```
[Logo top left, no link]                    [Add to Cart button top right, mobile hidden]

[H1 left aligned, large, message match to ad]
[Subhead VOC outcome polished]

[Star rating + review count line, 4.8 from 1,847 reviews]

[Primary CTA button, Add to Cart, $XX]
[Secondary trust line, Free shipping over $50. 30 day returns.]

[Product hero image right side desktop, below text mobile]
```

## Primary CTA button rules

- Single verb intent, "Add to Cart", "Get the Kit", "Shop the Bundle", "Buy Now"
- Include price in button text if AOV is shown in the ad, "Add to Cart, $48"
- Color, `--brand-accent` if it has good contrast against `--brand-paper`, else `--brand-primary`
- Size, `px-8 py-4 text-lg` minimum on mobile
- Animation, subtle hover scale (1.02), no bounce, no pulse

## Mobile sticky CTA bar (required for DTC)

```html
<div class="fixed bottom-0 left-0 right-0 bg-[var(--brand-paper)] border-t border-[var(--brand-muted)]/20 p-3 md:hidden z-50 shadow-lg">
  <a href="#buy" class="block w-full text-center bg-[var(--brand-accent)] text-white py-4 rounded-md font-semibold">
    Add to Cart, $XX
  </a>
</div>
```

The bar appears after the user scrolls past the hero CTA. Hide via `md:hidden` on desktop where the page CTAs are always visible.

## Comparison table pattern

The comparison table is one of the highest leverage DTC blocks. It does the work of 10 benefit bullets.

```
                    [Your Brand]    [What They Were Using]
Ingredient quality  [specific]      [specific weakness]
Time to result      [specific]      [specific]
Price per use       [specific]      [specific]
Returns             [specific]      [specific or not offered]
Made where          [specific]      [specific or unknown]
```

Pull "what they were using" from VOC. Common patterns, "the drugstore version", "the prescription one", "the gummy ones", "the powdered version".

## FAQ block (DTC specific)

Top 6 questions, verbatim from VOC. The most common DTC FAQ patterns:

1. Does it actually work?
2. How long until I see results?
3. Are there side effects?
4. Can I cancel anytime? (if subscription)
5. What if it does not work for me?
6. How fast is shipping?

Answer in 1 to 3 sentences. Honest. Specific. No marketing speak.

## Guarantee block

Place between FAQ and final CTA. Specific risk reversal. Not "satisfaction guaranteed", that means nothing.

Patterns that work:

- "Try it for 60 days. If you don't feel sharper focus, email us and we refund every cent. Including the shipping back."
- "30 day money back. Keep the bottle. Just email mike@brand.com."
- "Use the full bag. If you don't love it, we send your money back. We eat the return shipping."

The specificity is the proof. Vague guarantees signal nothing.

## Trust element placement

| Element | Where | Why |
|---|---|---|
| Star rating + review count | Hero subhead area | Reduces hero CTA hesitation |
| Customer count | Trust line below hero CTA | Reinforces "many people bought this" |
| Press logos | Below hero (logo strip) OR omit | Only if real and recognizable to audience |
| UGC photo carousel | Mid page (after benefits) | Social proof through use, not testimony |
| Detailed reviews | Lower third (above guarantee) | For high consideration purchases |
| Trust badges (SSL, Norton) | NEVER on a branded Shopify page | They lower trust, not raise it |
| Money back guarantee | Just above final CTA | Reduces last second hesitation |

## Pixel events to wire (DTC)

Place these in the Meta Pixel scaffold. The base script is in `references/section-library.md`. Add the following per CTA click:

```html
<!-- On any primary CTA click, before navigation -->
<script>
  document.querySelectorAll('a[href^="REPLACE_WITH_CHECKOUT_URL"], a[href="#buy"]').forEach(el => {
    el.addEventListener('click', () => {
      if (typeof fbq !== 'undefined') fbq('track', 'InitiateCheckout');
    });
  });
</script>
```

If the page leads to a hosted Shopify checkout or Stripe Checkout, the real Purchase event fires from the checkout completion page, not the lander. The lander only fires PageView (auto) + InitiateCheckout (on CTA click).

## Hard rules for DTC route

1. Exactly 1 primary CTA destination (the Buy Now or Add to Cart action). All primary CTAs link to the same place.
2. Mobile sticky CTA bar mandatory.
3. Real product image required. No abstract graphics.
4. Comparison table required.
5. At least 3 testimonials with names and photos. If VOC does not have 3 with photos, use whatever is real and adjust the section.
6. Guarantee block must be specific (no "satisfaction guaranteed").
7. FAQ questions verbatim from VOC.
8. Price visible in primary CTA button when AOV is in the ad.
9. No countdown timers for evergreen offers (cold traffic does not buy fake urgency).
10. No Norton, McAfee, or SSL trust badges on a legitimate Shopify page.
