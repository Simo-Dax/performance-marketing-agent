# The 34 Tells, Anti AI Slop Audit for Landing Pages

Adapted from awaken7050dev/anti-slop-ui (MIT) and combined with the anthropics/skills/frontend-design directives. Specialized for paid Meta ad landing pages.

## Critical wrapper rule

**Brand overrides aesthetic preference.** If Brand DNA explicitly declares Inter as the body font, use Inter. If Brand DNA specifies a purple gradient as the brand hero, use it. The 34 tells below apply ONLY to undeclared choices. Distinctive within the brand, not despite it.

When checking each tell below, ask, "Did the Brand DNA explicitly declare this choice?" If yes, the brand wins. If no, enforce the tell.

---

## Family 1, Visual Defaults (8 tells)

### Tell 1, Generic gradients

**Tell:** Purple to blue gradient hero. Pink to orange "vibrant" hero. Any rainbow gradient with no narrative.

**Fix:** Use solid brand color from `--brand-primary`. If gradient is required by Brand DNA, mix only 2 stops, use brand colors, and tilt the angle (35deg or 145deg, never 90deg or 180deg).

### Tell 2, Pill shaped everything

**Tell:** Every card has `rounded-full` or `rounded-3xl`. Every button is a pill. Every badge is a pill.

**Fix:** Pick ONE radius scale and stick to it. Default to `rounded-lg` (8px) for cards and `rounded-md` (6px) for buttons unless Brand DNA declares otherwise. Pills only for status badges and tags.

### Tell 3, Soft shadows on everything

**Tell:** Every card has `shadow-xl`. Every section has a soft drop shadow. Glassmorphism by default.

**Fix:** Use shadow purposefully. Hero CTA gets one shadow. Other elements use borders (`border-[var(--brand-muted)]/20`) for separation. Save heavy shadows for impression level 4 to 5.

### Tell 4, Component libraries shipped untouched

**Tell:** Default shadcn/ui card with default padding, default border, default header. Default Tailwind UI hero with no customization. Anything that looks like the marketing site of the library itself.

**Fix:** Override at least 3 design tokens per component, spacing, color, typography, or border treatment. The page must NOT look like it could be a shadcn demo.

### Tell 5, Decorative dashes and italic accents

**Tell:** Em dash decorated eyebrow labels with "FEATURES" framed by dashes. One word in the headline italicized for "emphasis" with no semantic reason.

**Fix:** Plain section markers (`01 / FEATURES` or just `FEATURES`). Italic only on quotes or genuinely italicized terms. No decorative punctuation. No em dashes anywhere.

### Tell 6, Abstract graphics instead of the product

**Tell:** Hero shows an orbital diagram, geometric shapes, or vague brand mark composition when the product is the actual selling point. The thing being sold is invisible.

**Fix:** Show the product. Lifestyle photo for DTC. Product screenshot for SaaS. Real face for service businesses. If no product image exists, use a high quality placeholder block with `REPLACE_WITH_PRODUCT_HERO_IMAGE` marker, not an abstract decoration.

### Tell 7, Generic stock photo heroes

**Tell:** Diverse people laughing in office stock photo. Hands on laptop stock. Lifestyle stock that has nothing to do with the brand.

**Fix:** Use the actual ad creative as the hero or a still derived from it. This auto creates message match. If no image is available, use a typographic hero with the H1 dominating the viewport.

### Tell 8, Purple, teal, or gradient text fills

**Tell:** Headline rendered with `bg-clip-text` gradient fill. Words gradient shaded to look "premium". Purple text on white.

**Fix:** Solid color text. Use `--brand-ink` for body and `--brand-primary` for accent words. Gradient text only if Brand DNA explicitly declares it.

---

## Family 2, Typography (8 tells)

### Tell 9, Inter on everything

**Tell:** Inter Variable as both display and body. No hierarchy beyond weight changes.

**Fix:** Two distinct font families (1 display + 1 body) from Brand DNA. If Brand DNA names only one font, pair it with a contrasting body font from the same foundry or Google Fonts (display, editorial serif paired with body, clean sans).

### Tell 10, Hero text breaks on mobile

**Tell:** H1 set in `text-7xl` desktop with no responsive scaling. On a 375px viewport the H1 wraps to 5 lines and feels cramped.

**Fix:** Use `clamp()` or Tailwind responsive prefixes, `text-4xl md:text-6xl lg:text-7xl`. Test the H1 at 375px, 768px, 1280px mentally before committing.

### Tell 11, Body type under 16px

**Tell:** `text-sm` (14px) or `text-xs` (12px) as body type. Hard to read on mobile.

**Fix:** Body type minimum 16px (`text-base`). 17px or 18px for premium feel. Smaller sizes only for legal text and metadata.

### Tell 12, Line height too tight on body

**Tell:** `leading-tight` or `leading-snug` on body paragraphs. Looks cramped.

**Fix:** Body paragraphs use `leading-relaxed` (1.625) or `leading-loose` for premium feel. Headings use `leading-tight` (1.25).

### Tell 13, All sentence case OR all title case

**Tell:** Every heading title cased like a corporate slide. Or every heading lowercased for "minimalist" feel when the brand is not minimalist.

**Fix:** Follow Brand DNA voice block. Default to sentence case for headings unless the brand is editorial or luxury. Punctuate H1 like a sentence (with a period or without, but consistently).

### Tell 14, Display fonts on every heading

**Tell:** H1, H2, H3, H4 all in the same display font. Visual rhythm collapses.

**Fix:** Display font on H1 and section H2s only. H3 and below in body font, weighted up to bold.

### Tell 15, No letter spacing on tiny caps

**Tell:** Eyebrow labels in `uppercase` with default `tracking-normal`. They look squished.

**Fix:** Uppercase eyebrows use `tracking-wider` or `tracking-widest` (0.05em to 0.1em). Add font weight 500 to 600.

### Tell 16, Same font weight throughout

**Tell:** Everything at `font-medium`. Or everything at `font-bold`. No contrast.

**Fix:** Use weight as hierarchy, H1 at 700 to 900, H2 at 700, H3 at 600, body at 400 to 500, eyebrow at 500 to 600. Three weight minimum across the page.

---

## Family 3, Layout (10 tells)

### Tell 17, Symmetric three card grid

**Tell:** Features section is always a 3 card grid with identical card heights and identical icon placement. Predictable.

**Fix:** Vary the grid, 4 column on desktop with one card spanning 2 columns. Or 2x2 asymmetric. Or list with horizontal scroll on mobile. Use the layout to imply hierarchy.

### Tell 18, Centered everything

**Tell:** Hero text centered. Section H2s centered. Body paragraphs centered. Reads like a slide deck, not a website.

**Fix:** Asymmetric is the default. Left aligned text with a right aligned image. Headlines may be left aligned even when buttons are centered. Centered only when the content genuinely commands it (a single CTA, a quote pull, a final close).

### Tell 19, Consumer app spacing on a dashboard

**Tell:** Big sections, big padding, big margins on a B2B SaaS page. The page feels like an iPhone app rather than a serious tool.

**Fix:** Match density to audience. Impression level 1 to 2 (data terminals, professional dashboards) use tight `py-8` to `py-12` sections. Level 4 to 5 (showcases) use generous `py-24` to `py-32`. Read the Brand DNA voice block.

### Tell 20, Motion that adds nothing

**Tell:** Every section fades in on scroll. Every card has a hover lift. Motion is performative not functional.

**Fix:** Motion only when it conveys meaning. Scroll reveal on the social proof block (because the testimonial matters). Hover state on the primary CTA only. No motion for motion's sake.

### Tell 21, 12 column grid bleed

**Tell:** Hero text spans full 12 column width. Lines run 120 characters long. Hard to read.

**Fix:** Body content max width 65 to 75 characters per line. Use `max-w-2xl` for hero subhead, `max-w-prose` for body sections. Containers (`max-w-7xl`) only on full bleed visual sections.

### Tell 22, Logo strip with no context

**Tell:** "As seen in" logo bar showing Forbes, Inc, TechCrunch when the brand was never in those publications. Or random partner logos for "trust".

**Fix:** Only include logos the brand has earned. If the brand has no notable press, replace with a customer count ("4,200 customers since 2022") or a star rating with review count.

### Tell 23, Nav with anchor links on a paid landing page

**Tell:** Top nav with Home, Features, Pricing, About, Contact links on a page that exists to convert one click from a Meta ad.

**Fix:** Hide the nav entirely or show only the logo (no link) and the primary CTA. No anchor links to other sections (the user scrolls). Definitely no off page links.

### Tell 24, Hamburger menu on a single page landing

**Tell:** Three line mobile menu icon on a one page landing. The menu opens to a single empty link.

**Fix:** No hamburger. Mobile nav shows logo + CTA only. If the page is genuinely multi section, use a sticky bottom CTA bar instead.

### Tell 25, Footer with 5 columns of empty links

**Tell:** "Resources, Company, Legal, Social, Support" footer columns with greyed out placeholder links because the brand does not have those pages yet.

**Fix:** Minimal footer, copyright, privacy link, terms link, support email. Three lines max. If the brand has real footer content, use it. No placeholders.

### Tell 26, No mobile sticky CTA

**Tell:** Long DTC landing page with the primary CTA visible only in the hero and the footer. Users scrolling through the middle have no path to convert.

**Fix:** Mobile sticky CTA bar at bottom of viewport, appearing after the user scrolls past the hero. Mandatory for DTC. Optional but recommended for lead gen.

---

## Family 4, Content Slop (8 tells)

### Tell 27, "Welcome to [Product]" hero

**Tell:** H1 reads "Welcome to BrandName" or "Introducing the future of X". Says nothing about what the product does.

**Fix:** H1 must contain at least one 3+ word phrase from the ad headline (message match rule). Must promise an outcome, not announce a product.

### Tell 28, Em dashes in every sentence

**Tell:** Body copy peppered with em dashes used as conversational pauses. The AI tell.

**Fix:** No em dashes as conversational pauses. No hyphens as pauses either. Use periods, commas, or colons. Em dashes acceptable only in genuine parenthetical asides, and even then prefer commas.

### Tell 29, Unverified marketing copy

**Tell:** "Trusted by 10,000+ customers" with no source. "5 star rated" with no review count. "Industry leading" with no benchmark.

**Fix:** Every number comes from Brand DNA or VOC. If a customer count exists, cite it with date. If a review count exists, link the source. If no number exists, write a different sentence.

### Tell 30, AI tell words and phrases

**Tell:** revolutionize, unlock, seamless, leverage, supercharge, game changer, harness, empower, elevate, transformative, in today's fast paced world, level up, paradigm shift, holistic, robust, scalable, synergistic.

**Fix:** Banlist enforced. Rewrite any sentence containing these words. Use Brand DNA voice block to find the brand's own words.

### Tell 31, Vague benefit bullets

**Tell:** "Save time", "Boost productivity", "Drive results", "Increase efficiency". Benefits with no specifics.

**Fix:** Concrete benefit copy from VOC. "Sharper focus by 10am" not "Better focus". "Cut your reporting time from 4 hours to 30 minutes" not "Save time on reports". Specifics from VOC, never invented numbers.

### Tell 32, Generic founder story

**Tell:** "Founded in 2021 with a mission to democratize X" template. Could apply to any brand. Says nothing real.

**Fix:** Use the Brand DNA origin story verbatim if it exists. If not, use one specific concrete fact (location, founding moment, named founder, year) and drop the rest.

### Tell 33, Placeholder testimonials

**Tell:** "This product changed my life! Best purchase ever. 10/10!" attributed to "Sarah J., Verified Buyer".

**Fix:** Pull whole verbatim quotes from VOC. Include the customer's real name, role, age, or city if available in VOC. Mix lengths (one short punchy, one longer story). If VOC has fewer than 3 testimonials of usable length, only use what is real.

### Tell 34, FAQ with invented questions

**Tell:** "Is this product good?" "How does it work?" "Why should I buy it?" Generic FAQ questions no real customer ever asked.

**Fix:** FAQ questions come VERBATIM from VOC. If VOC contains "Can I cancel anytime?" that is the FAQ question, not "What's your cancellation policy?". Use the customer's actual phrasing.

---

## Pre ship checklist

Before writing the file to disk, verify ALL 34 tells are resolved. Print a one line confirmation per family:

```
Family 1 (Visual Defaults): 8/8 clean
Family 2 (Typography): 8/8 clean
Family 3 (Layout): 10/10 clean
Family 4 (Content Slop): 8/8 clean
```

If any tell is unresolved, fix it before output. Do not ship with known tells.

## Impression level scale

From anti-slop-ui (MIT). Set the impression level early in Step 5 based on Brand DNA tone:

| Level | Name | Use For | Density | Motion | Color |
|---|---|---|---|---|---|
| 1 | INVISIBLE | Data terminal, info IS the product | Tight | None | Mono |
| 2 | RESTRAINED | Professional dashboard, B2B SaaS lead gen | Moderate | Minimal | 2 tones |
| 3 | BALANCED | Modern SaaS, mid AOV DTC | Standard | Subtle | 3 tones |
| 4 | EXPRESSIVE | Premium DTC, design forward consumer | Generous | Considered | Full palette |
| 5 | SPECTACULAR | Luxury, high AOV ($150+) DTC showcase | Lavish | Choreographed | Full palette + texture |

Pick the wrong level and the page mismatches the brand. A serious B2B SaaS at level 4 feels like a toy. A premium DTC at level 2 feels like a tax form.

For paid Meta ad traffic:

- DTC under $50 AOV, Level 3
- DTC $50 to $150 AOV, Level 3 to 4
- DTC over $150 AOV, Level 4 to 5
- Lead gen B2B, Level 2 to 3
- Lead gen consumer service, Level 3 to 4
