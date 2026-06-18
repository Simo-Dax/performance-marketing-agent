---
description: Anti-AI slop gate — audit o rewrite di copy per rimuovere i tell da testo AI (forbidden words/patterns EN + layer IT). Skill 49 importata. Gate finale prima di pubblicare copy.
argument-hint: [testo o path file] [audit|rewrite]
---

# /pm-de-ai — Anti-AI Slop Gate (skill 49)

Esegui la skill nativa **`directives/skills/49_anti_ai_slop/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/49_anti_ai_slop/SKILL.md` (modalità Audit o Rewrite).
2. Carica i reference canonici (`references/quick-scan-checklist.md`, `replacement-table.md`, `by-medium.md`).
3. Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` + tone of voice brand.
4. Check automatici opzionali via CLI (da `49_anti_ai_slop/scripts/`):
   - `python3 -m anti_ai_slop.cli words <file>` — parole vietate
   - `python3 -m anti_ai_slop.cli dashes <file>` — em/en dash
   - `python3 -m anti_ai_slop.cli replace <file>` — riscrittura forbidden phrases
5. Audit → tabella tell (excerpt | tell | regola | severity) + verdetto. Rewrite → testo pulito + diff log + self-check (zero forbidden words EN/IT, lunghezza ±15%, nomi propri/numeri preservati).
