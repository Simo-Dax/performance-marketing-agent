---
description: Brand DNA — estrae identità visiva (colori live via Playwright) e verbale del brand, produce documento HTML. Skill nativa 21_brand_dna (Pre-pipeline).
argument-hint: [nome brand] [URL sito]
---

# /pm-brand-kit — Brand DNA

Esegui la skill nativa **`directives/skills/21_brand_dna/SKILL.md`** (Pre-pipeline — setup brand).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/21_brand_dna/SKILL.md`.
2. Usa Playwright per estrarre i colori live dal CSS (3-5 pagine). Web search per tutto il resto.
3. I colori live sovrascrivono quelli trovati via web search.
4. Output: `02_Brand_DNA/brand-dna-[slug].html`.

Prerequisito per `/pm-statiche` e `/pm-buyer-persona`.
