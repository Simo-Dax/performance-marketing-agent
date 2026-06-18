# Lead Gen Route, Section Order and Patterns

For lead capture, demo book, signup, and free consultation landing pages from Meta paid traffic. Single primary CTA = email capture or booking.

## Section order (mandatory)

1. **Hero** (with email capture or "Book a Demo" CTA)
2. **What you'll get** (value first framing of the lead magnet or call)
3. **Problem agitation** (VOC pain quote)
4. **Solution overview** (mechanism in 3 numbered steps)
5. **Social proof** (testimonials, customer logos, or case study numbers)
6. **Founder credibility** (why us, why now)
7. **FAQ** (verbatim VOC questions about the offer)
8. **Final CTA** (email or book a call, same destination as hero)
9. **Minimal footer** (3 lines max)

## Hero composition

Two layouts, pick based on the lead magnet type.

### Layout A, single field email capture (for guides, playbooks, free tools)

```
[Logo top left, no link]

[H1 left aligned, large, message match to ad]
[Subhead VOC outcome polished]

[Inline form, email input + "Get the [X]" button]
[Reassurance line, "Free. 60 seconds. No spam."]

[Right side, cover image of the lead magnet or a screenshot]
```

### Layout B, book a demo (for SaaS, services, consulting)

```
[Logo top left, no link]

[H1 left aligned, large, message match to ad]
[Subhead VOC outcome polished]

[Customer logos strip OR star rating + count]

[Primary CTA button, "Book Your Free Strategy Call"]
[Reassurance line, "30 min. Free. No sales pitch."]

[Right side, founder headshot or product screenshot]
```

## Primary CTA rules

- Value first verb, "Get the Playbook", "Book Your Strategy Call", "Send Me the Guide"
- Avoid, "Submit", "Sign Up", "Get Started" (generic)
- Color, `--brand-accent` for high contrast against the form
- For 2 step CTAs (button opens modal with form), use the button on hero and reveal the form on click. Cold traffic converts higher on 2 step than inline forms.

## Form field rules

**Single field forms outperform multi field forms for cold ad traffic by a wide margin.**

| Form type | Field count | When to use |
|---|---|---|
| Email only | 1 | Default for guides, playbooks, free tools, newsletters |
| Email + name | 2 | When personalization matters in the follow up |
| Email + phone + 1 qualifier | 3 | Service businesses, high ticket consulting |
| Multi step progressive | 4+ shown 1 per step | When more than 4 fields are required (Typeform style) |

Never put 5+ fields on a single form for cold ad traffic. Cobloom benchmark, 11 fields to 4 fields produced 160% lift. The next move (4 to 1) typically adds another 30 to 50%.

## "What you'll get" block

The highest leverage lead gen section after the hero. Tell the visitor exactly what they receive, when, and how. 3 to 5 bullets.

Pattern:

```
What's in the playbook:
- 12 pages of the exact framework we use with 8 figure brands
- 3 real client examples with screenshots (names changed)
- A Notion template you can copy
- 1 follow up email with the bonus tool

You'll get it in your inbox within 60 seconds.
```

Specifics matter. Page count, file format, real names. Vague descriptions ("comprehensive guide") signal low value.

## Mechanism in 3 steps

For lead gen, mechanism is usually about the process the lead will go through, not the product. 3 numbered steps. Brief.

Pattern:

```
1. Book your call (30 minutes, free)
2. We review your current setup (we send a Loom before the call)
3. You leave with a custom plan, action items, and a written follow up
```

The 3 steps reduce uncertainty about what happens after the click. Uncertainty is the #1 conversion killer in lead gen.

## Social proof patterns for lead gen

| Proof type | When to use | Format |
|---|---|---|
| Customer logos | B2B SaaS with recognizable customers | Logo strip below hero |
| Star rating + count | Any service business with reviews | Inline in hero |
| Specific case study numbers | High ticket consulting | "Helped Acme grow MRR 3.2x in 6 months" callout |
| Video testimonial | Premium service with willing customers | Embedded in social proof section |
| Customer count | Volume play | "Used by 2,400+ marketing teams" |
| Founder credibility | New brand without scale | "Built by [name], formerly at [company]" |

If the brand is too new for any of these, use the founder credibility play. Real human credibility beats fake scale claims.

## FAQ block (lead gen specific)

Top 5 questions, verbatim from VOC where possible. Common lead gen FAQ patterns:

1. Is this really free?
2. What happens after I submit my email?
3. Will I get spammed?
4. How long does the call take?
5. Who is this for, who is this not for?

Answer in 1 to 3 sentences. Be honest about what happens next (specifically, how many emails, how soon, what tone).

## Final CTA block

Same destination as the hero. Different framing.

Pattern for email capture:

```
[H2, Get the [thing] now]
[1 sentence summary of the value]
[Inline form, email + button, same as hero]
[Reassurance, Free. 60 seconds. Unsubscribe anytime.]
```

Pattern for demo book:

```
[H2, Ready to see if we're a fit?]
[1 sentence summary of what the call covers]
[Primary CTA button, Book Your Strategy Call]
[Reassurance, 30 min. Free. No pitch.]
```

## Pixel events to wire (lead gen)

Place these in the Meta Pixel scaffold. The base script is in `references/section-library.md`. Add the following per form or CTA:

```html
<!-- On form submit success, fire Lead event -->
<script>
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      if (typeof fbq !== 'undefined') fbq('track', 'Lead');
    });
  });
</script>
```

For demo book CTAs that link to a Calendly or SavvyCal URL, fire `Lead` on click (treat the click as the conversion).

## Hard rules for lead gen route

1. Exactly 1 primary CTA destination across the page.
2. Single field form by default. Justify any additional field.
3. Mobile form must be one tap to focus, large touch targets (48px+).
4. Reassurance line under every CTA (what happens after submit, how spam free, time commitment).
5. Founder credibility required if the brand is under 2 years old or under 10k customers.
6. No fake urgency timers on cold traffic.
7. FAQ questions verbatim from VOC.
8. "What you'll get" block required for any lead magnet (guide, playbook, template).
9. Mechanism in 3 steps required for any demo or call CTA.
10. Mobile sticky CTA bar optional but recommended for long pages.
