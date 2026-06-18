# Brand DNA Parsing

How to extract design tokens from a Brand DNA document produced by the `21_brand_dna` skill (`/pm-brand-kit`), and inject them into the landing page HTML.

## What to pull from Brand DNA

| Brand DNA field | What to extract | Where it lands in HTML |
|---|---|---|
| `colors.primary` | Hex code | `--brand-primary` CSS variable at `:root` |
| `colors.accent` | Hex code | `--brand-accent` CSS variable |
| `colors.text` or `colors.ink` | Hex code | `--brand-ink` CSS variable |
| `colors.background` or `colors.paper` | Hex code | `--brand-paper` CSS variable |
| `colors.muted` or `colors.subtle` | Hex code | `--brand-muted` CSS variable |
| `typography.display` | Font name | Google Fonts `<link>` + Tailwind arbitrary value |
| `typography.body` | Font name | Google Fonts `<link>` + Tailwind arbitrary value |
| `voice.tone` | Description | Top of file HTML comment + informs copy generation |
| `voice.avoid` | Word list | Added to banlist |
| `voice.use` | Word list | Preferred when generating copy |
| `positioning` | One liner | Informs hero subhead direction |
| `business_model` | `ecom` or `lead_gen` | Step 3 routing override |

## Brand DNA document format

The `21_brand_dna` skill produces HTML documents with these tokens visible inside structured sections. Parse them out. If the Brand DNA is provided as raw text or markdown, look for sections labeled:

- "Color palette" or "Brand colors"
- "Typography" or "Type system"
- "Voice and tone"
- "Positioning"
- "Business model"

If the file is HTML, the tokens are typically in `<dl>` definition lists, `<table>` rows, or hex codes inside `<code>` tags. Parse permissively, the goal is to surface the values, not enforce a schema.

If a required field is missing (primary color hex, display font, body font), refuse to proceed. Print which field is missing and ask the member to add it to the Brand DNA document, or re-run `/pm-brand-kit`.

## Confirmation step before parsing locks in

After extraction, print the parsed values back to the member in this format:

```
Parsed from Brand DNA:
  Colors: primary <#XXXXXX>, accent <#XXXXXX>, ink <#XXXXXX>, paper <#XXXXXX>, muted <#XXXXXX>
  Fonts: display <Name>, body <Name>
  Voice tone: <one line>
  Voice avoid list: <comma separated, or "none">
  Business model: <ecom / lead_gen / undeclared>
```

Ask one confirmation: "Looks right? Reply `yes` or what to fix." On `yes`, proceed. On any other response, accept the correction and reparse.

## Color token injection

Place tokens at the top of `<head>` inside a `<style>` block:

```html
<style>
  :root {
    --brand-primary: #1E40AF;
    --brand-accent: #F59E0B;
    --brand-ink: #0F172A;
    --brand-paper: #FAFAF7;
    --brand-muted: #94A3B8;
  }
</style>
```

Use the tokens via Tailwind arbitrary values throughout the page:

- `bg-[var(--brand-paper)]` for section backgrounds
- `text-[var(--brand-ink)]` for body text
- `text-[var(--brand-primary)]` for accent text
- `bg-[var(--brand-accent)]` for primary CTA buttons
- `border-[var(--brand-muted)]/20` for subtle dividers

Tailwind 3.4 Play CDN supports arbitrary values with CSS variables natively. No config extension required.

## Font token injection

Step 1, add Google Fonts `<link>` in `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DISPLAY_NAME:wght@600;700;800&family=BODY_NAME:wght@400;500;600&display=swap" rel="stylesheet">
```

Replace `DISPLAY_NAME` and `BODY_NAME` with the Brand DNA fonts, URL encoded with `+` for spaces.

Step 2, apply via Tailwind arbitrary values:

```html
<h1 class="font-['Display_Name'] text-5xl md:text-7xl font-bold">...</h1>
<p class="font-['Body_Name'] text-base leading-relaxed">...</p>
```

## Font fallback strategy

If Brand DNA names a font that Google Fonts does not serve, fall back in this order:

1. Look for the closest Google Fonts equivalent. "Proxima Nova" maps to "Mulish", "Calibre" maps to "Inter", "Brown" maps to "Manrope".
2. If no Google Fonts equivalent exists, use the system stack matching the font category:
   - Editorial serif, `Georgia, "Times New Roman", serif`
   - Modern sans, `system-ui, -apple-system, "Segoe UI", sans-serif`
   - Geometric sans, `Manrope, system-ui, sans-serif`
   - Monospace, `ui-monospace, "Courier New", monospace`
3. Log the substitution in a top of file HTML comment so the member sees it:

   ```html
   <!-- Font note, Brand DNA specified "Calibre" which is not on Google Fonts. Substituted Inter as closest match. Replace the <link> tag and font-['Inter'] classes if you license Calibre. -->
   ```

## Voice block application

The voice block from Brand DNA shapes copy generation. Apply it:

1. **Tone descriptor.** Set the writing tone for all copy. If voice says "direct, no jargon, second person, witty", every sentence reflects that.
2. **Avoid list.** Add to the global banlist. Default banlist plus brand banlist both enforced.
3. **Use list.** Bias copy generation toward these words. Not forced, but preferred when there is a natural fit.
4. **Sample sentences from Brand DNA.** If Brand DNA shows 3 example sentences, copy should sound like them.

## Brand override on anti AI slop rules

This is the critical wrapper rule for the 34 tells.

**The Brand DNA always overrides the 34 tells.** If Brand DNA explicitly declares:

- Inter as body font, use Inter even though Tell 9 flags it.
- Purple gradient as hero treatment, use it even though Tell 1 flags it.
- Centered hero alignment, use it even though Tell 18 prefers asymmetric.

The 34 tells apply ONLY to undeclared choices. The brand is the source of truth for declared choices.

**Implementation.** Before applying any tell from `references/34-tells.md`, check whether Brand DNA explicitly declared the choice. If yes, brand wins. If no, enforce the tell.

## Token limits

Maximum tokens on the page:

- 5 color tokens (primary, accent, ink, paper, muted)
- 2 font families (1 display + 1 body)
- 1 consistent spacing scale (Tailwind defaults, 4 / 8 / 16 / 24 / 32 / 48 / 64 / 96 / 128)

Going beyond these limits creates visual drift. Reject any Brand DNA that demands more without explicit declaration. If the brand legitimately has more (a premium luxury brand might have 7 colors), reduce to 5 by mapping non essential brand colors to existing tokens.

## Hard rules

1. Every color used on the page must come from one of the 5 tokens. No one off hex codes.
2. Every text element uses one of the 2 font families. No third font.
3. Spacing follows the Tailwind default scale. No arbitrary `mt-7` then `mt-11`.
4. If Brand DNA is missing a required token (primary color or any font), refuse to proceed and ask the member to add it.
5. If Brand DNA conflicts with a 34 tell, brand wins. Document the override in a top of file HTML comment.
