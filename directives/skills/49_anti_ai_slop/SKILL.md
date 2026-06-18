---
name: anti-ai-slop
description: |
  Universal de-AI writing skill. Catches and rewrites the tells that expose
  AI-generated text — forbidden words ("delve", "crucial", "landscape", "tapestry",
  "Additionally"), forbidden patterns (rule of three, negative parallelism,
  em-dash overuse, Title Case headings, inline-header bullets, emoji headers,
  knowledge-cutoff disclaimers), and AI structure (Despite-its-X formula,
  "is/are" replaced by "serves as / represents"). Works on any medium: landing
  page copy, emails, DMs, LinkedIn posts, proposals, documentation, microcopy,
  CTAs, FAQ. The references in this folder are the canonical source — read them,
  then use your own judgment for the rewrite.

  TRIGGERS — Use this skill when the user says:
  - "de-ai this" / "de-ai-ify" / "remove the AI tells"
  - "make it sound human" / "humanize this copy" / "sound less AI"
  - "is this AI slop?" / "does this read like AI?"
  - "rewrite without AI words" / "scrub the AI from this"
  - "anti-ai" / "anti-slop" / "no slop"
  - "check this for AI tells" / "audit this copy"
  - Before publishing any external copy (LP, email, proposal, post) as a final gate
  - When another skill (design-ui, content, proposal, linkedin-hooks) is about to return copy
---

# anti-ai-slop

> **Integrazione Performance Marketing Team (skill 49).** Questa è la **gate finale anti-AI** per ogni copy esterno prodotto dal sistema (ad copy, email, landing, content). Le skill di copywriting (10, 11, 12, 28, 46, 02, 41, 34) e la QA copy (`03_editing_selfcheck`) la richiamano prima di consegnare.
> **Layer italiano:** la lista forbidden words/patterns qui sotto è EN. Per copy in **italiano**, applica in aggiunta `context/brand/anti_ai_writing_style.md` (regole anti-AI IT: "inoltre/fondamentale/approfondire", regola del tre, trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano: nessun tell EN **né** IT deve sopravvivere.
> **Script CLI** (`scripts/anti_ai_slop/`): `python3 -m anti_ai_slop.cli words <file>` (parole vietate), `dashes <file>` (em/en dash), `replace <file>` (riscrittura). Co-locati per la regola 6 di CLAUDE.md.

Two modes. Pick the matching one. Both pull from `references/` as the canonical
pattern list. You are the final judge — the references guide you, but the rewrite
is your call.

## Modes

| Mode | When | Output |
|---|---|---|
| 1. Audit | "is this AI?" / "what tells are in this?" | Annotated list of every tell, ranked by severity, with the exact word/phrase and the rule it breaks. No rewrite. |
| 2. Rewrite | "de-ai this" / "humanize this" | Clean rewrite that preserves meaning and length, removes every tell, returns the rewritten text plus a short diff log of what was changed and why. |

## References

| File | What it contains |
|---|---|
| `references/quick-scan-checklist.md` | Fast in-flight checklist — load for short copy (under 200 words) |
| `references/replacement-table.md` | Find/replace dictionary for the most common AI phrases |
| `references/by-medium.md` | Medium-specific rules: LP, email, DM, LinkedIn post, proposal, docs, microcopy |

## How to run

### Mode 1 — Audit
1. Load `references/quick-scan-checklist.md`.
2. For long copy, also load `references/replacement-table.md` and `references/by-medium.md`.
3. Read the input. For every tell found, output a row:
   `| line/excerpt | tell | rule broken | severity (high/med/low) |`
4. End with a one-line verdict: clean / minor / heavy slop.
5. Do not rewrite unless asked.

### Mode 2 — Rewrite
1. Load `references/quick-scan-checklist.md` and `references/replacement-table.md`.
2. Detect the medium from context (LP / email / DM / post / docs / microcopy).
   Load the matching section of `references/by-medium.md`.
3. Rewrite preserving:
   - Meaning (no new facts, no dropped facts)
   - Approximate length (within ±15%)
   - The author's voice if a style file is referenced (e.g., `walid-writing-style.md`)
4. Return:
   - The rewritten text
   - A short diff log: 5–10 bullet points listing what changed and which rule fired
   - A self-check confirming zero forbidden words remain

## The hard bans (apply to every output)

Forbidden words — never appear in the rewrite:
`Additionally` (opener) · `align with` · `crucial` · `delve` · `emphasizing` ·
`enduring` · `enhance` · `fostering` · `garner` · `highlight` (verb) ·
`interplay` · `intricate` · `intricacies` · `key` (adjective) · `landscape` ·
`pivotal` · `showcase` · `tapestry` · `testament` · `underscore` · `valuable` ·
`vibrant` · `serves as` · `stands as` · `It is worth noting` · `rich tapestry` ·
`evolving landscape` · `seamlessly` · `leverage` (as verb) · `empower` ·
`comprehensive` · `holistic` · `robust solution` · `cutting-edge` · `game-changer`

Forbidden patterns — never appear in the rewrite:
- Rule of three (three adjectives, three benefits, three phrases in a row)
- Negative parallelism: "not just X, but Y" / "not X, but Y"
- Em dashes — like this — (use commas, colons, or split the sentence)
- "Despite its X, Y faces challenges" formula
- Title Case in headings (sentence case only)
- Inline-header bullets: `• **Label:** description`
- Emoji in headings or section markers
- "Let's explore" / "Here is your" / "As we can see"
- Knowledge-cutoff disclaimers ("As of my last training update...")
- "is/are/has" replaced by "serves as / represents / marks / features / boasts"
- Bolding more than 2 words per paragraph for "emphasis"
- Synonym chains (calling the same person 4 different ways in a paragraph)
- "from X to Y" when X and Y don't form a real scale

## Self-check before returning (rewrite mode)

Run silently and confirm in the diff log:
- [ ] Zero forbidden words found via case-insensitive scan
- [ ] Zero em dashes
- [ ] Zero `Additionally` / `In conclusion` / `In summary` openers
- [ ] No paragraph has three parallel items in a row
- [ ] No heading is in Title Case
- [ ] No "not just X, but Y" pattern
- [ ] Length within ±15% of original
- [ ] All proper nouns and numbers preserved exactly

If any check fails, fix and re-check before returning.

## Chains into

- `design-ui` — applies anti-ai-slop to every headline, microcopy, CTA, FAQ generated
- `content` — applies before publishing LinkedIn posts
- `linkedin-hooks` — applies after hook generation
- `proposal` / `proposal-builder` — applies to every section of the proposal HTML
- `cold-dance` / `personalized-value-outreach` — applies to every DM
- `landing-page-copy` — applies to every section
- `de-ai-ify` — alias for Mode 2

## When NOT to apply

- Code, JSON, YAML, CLI commands — leave technical strings alone
- Direct quotes from external sources — preserve verbatim
- Legal copy where exact wording is required — flag, don't rewrite
- The user explicitly asks for "AI-style" or "formal corporate tone"
