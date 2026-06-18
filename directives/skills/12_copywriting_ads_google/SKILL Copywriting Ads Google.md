---
name: google-ads-copy
description: "Generate Google Ads search copy (headlines, long headline, descriptions) structured by strategic intent. Use this skill whenever the user asks to write Google Ads copy, create search ad text, generate RSA (Responsive Search Ads) headlines or descriptions, or needs ad copy for Google Ads campaigns. Also trigger when the user mentions \"ad copy\", \"search ads\", \"headline ads\", \"Google Ads text\", or wants to create advertising copy for paid search."
---

# Google Ads Search Copy Generator

Generate structured, publication-ready Google Ads search copy in the user's target language. The output follows Google Ads character limits and organizes copy by strategic intent (keyword focus, benefits, USP, desire, bonus, guarantees, scarcity).

## Input Requirements

Before generating copy, collect these variables from the user. If any are missing, ask for them before proceeding.

| Variable | Description | Required |
|---|---|---|
| `SEED_KEYWORD` | The primary keyword to include in at least 3 headlines | Yes |
| `PRODUCT_DESCRIPTION` | What the product/service is | Yes |
| `TARGET_AUDIENCE` | Who the ad is for | Yes |
| `PRODUCT_CATEGORY` | Category or industry | Yes |
| `TARGET_MARKET` | Geographic/language market | Yes |
| `USP` | Unique selling propositions (what makes it different) | Yes |
| `BENEFITS` | Key benefits for the customer | Yes |
| `DESIRES` | Emotional desires or aspirations of the target | Yes |
| `BONUS` | Any bonus, freebie, or added value | No |
| `GUARANTEES` | Money-back, satisfaction, or other guarantees | No |
| `LANGUAGE` | Output language (default: same as user's input) | No |

## Output Specification

Generate exactly this structure:

### HEADLINE STANDARD (15 headlines)
Each headline: min 20, max 30 characters (spaces included). Count characters carefully.

**Keyword Focus (3 headlines)**
Must contain the `SEED_KEYWORD` or a close variant. These headlines exist to boost ad relevance and Quality Score.

**Benefits Focus (5 headlines)**
Highlight concrete, tangible benefits. Avoid vague claims. Be specific: numbers, timeframes, outcomes.

**USP Focus (3 headlines)**
Communicate what makes this offer different from competitors. Differentiation, not features.

**Desire Focus (2 headlines)**
Tap into the emotional aspiration or end-state the target audience wants. Speak to the "after" state.

**Bonus Focus (1 headline)**
Highlight the bonus or added value. If no bonus was provided, use a compelling free-value angle.

**Guarantee Focus (1 headline)**
Communicate risk reversal. If no guarantee was provided, use a trust-building angle instead.

### HEADLINE LUNGA (1 headline)
Exactly 1 headline, max 90 characters (spaces included). This is for the long headline slot in RSA. It should be a complete, compelling value proposition.

### DESCRIZIONI (4 descriptions)
Each description: max 90 characters (spaces included).

**USP Focus (2 descriptions)**
Expand on the unique selling propositions with more detail than the short headlines allow.

**Scarcity & Urgency Focus (2 descriptions)**
Create urgency or scarcity. Use time pressure, limited availability, or exclusive access. Avoid fake urgency if no real constraint exists; in that case, use soft urgency (e.g., "non aspettare", "inizia oggi").

## Rules

1. **Character counting is critical.** Count every character including spaces. Double-check every line. If a headline exceeds 30 chars or a description exceeds 90 chars, it is invalid. When in doubt, err shorter.
2. **Include the SEED_KEYWORD in at least 3 headlines**, ideally in the Keyword Focus group, but it can appear elsewhere too.
3. **Write in the specified language.** Default to the user's input language. Italian market = Italian copy.
4. **No generic filler.** Every headline must convey a specific, concrete idea. Avoid empty phrases like "Scopri di più" or "Clicca qui" unless they serve a strategic purpose.
5. **Vary sentence structure.** Mix questions, imperatives, statements, and number-led headlines. Monotony kills CTR.
6. **Use title case or sentence case consistently** based on market norms (Italian typically uses sentence case).
7. **No trademark symbols, excessive punctuation, or all-caps** (violates Google Ads policy).
8. **Each headline must work independently.** RSA combines headlines randomly, so they should not depend on each other for meaning.

## Output Format

Present the output in a clean, scannable table format grouped by section. For each line, show the copy and the character count.

**Example format:**

#### Headline Standard — Keyword Focus
| # | Headline | Chars |
|---|----------|-------|
| 1 | Corsi SEO Professionali | 24 |
| 2 | Impara la SEO Oggi | 19 |
| 3 | SEO per il Tuo Business | 24 |

Repeat this table format for every group (Benefits, USP, Desire, Bonus, Guarantee, Long Headline, Descriptions).

After the tables, add a short "Note per la revisione" section with 2-3 practical suggestions for A/B testing or improving the copy based on the specific product context.

## Common Mistakes to Avoid

- Miscounting characters (especially with accented characters in Italian, which are 1 char each)
- Writing headlines that only make sense paired with another headline
- Using the same sentence structure in every headline
- Ignoring the emotional angle in favor of purely rational copy
- Writing descriptions that just repeat the headlines with more words


IMPORTANTE: Ricordati di rivedere il testo finale di ciò che produci alla luce della skill "Humanizer", per pulire al massimo il testo da linguaggio AI e renderlo più umano possibile
---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
