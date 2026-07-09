---
description: Static ad da winner reali (rebrand) — ogni ad rebranda un ad vincente reale dalla reference bank (design tenuto, identità scambiata), prompt prosa unico, nessun template. Skill nativa 24_static_ads (SA6).
argument-hint: [pagina Facebook brand] [n. ad] [foto prodotto]
---

# /pm-statiche — Static Ads da Winner Reali (Rebrand)

Esegui la skill nativa **`directives/skills/24_static_ads/SKILL.md`** (SA6 — Asset Production). Reference: `references/format_families.md`, `references/winning_ad_science.md`, `references/rebrand_worked_example.md`, `../_shared/format_teardown_recreation.md`, `../_shared/adjacency_kill_pass.md`, `../_shared/angle_engine.md`.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/24_static_ads/SKILL.md`.
2. **Reference ads obbligatorie**: la skill scrapa gli ad live del brand + legge la reference bank bancata da `19_ad_spy` (`03_Ad_Spy/_scratch/format-*.json`). Zero fonti + scan competitor rifiutato = si ferma e indirizza a `/pm-competitor-spy`.
3. Ogni ad è il REBRAND di un ad vincente reale: design della fonte tenuto intero, solo identità scambiata (parole/marchi/prodotto/colori/numeri), 2-3 dettagli sibling shiftati. Deliverable = un blocco prosa per ad, mai zone/template/scaffold.
4. Batch plan (fonte+angolo per ogni ad, spread su famiglie di formato) approvato dall'utente PRIMA di scrivere qualunque prompt.
5. Aspect ratio segue la fonte di default; GPT Image 2 default (Nano Banana 2 solo per 4:5 vero insistito). Subset picker obbligatorio Path B/C/D.
6. Output: prompt in chat + copia `04_Static_Ads/static-ads-[YYYY-MM-DD].txt`. Niente HTML.

Conferma il costo crediti prima della generazione.
