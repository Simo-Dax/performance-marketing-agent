---
description: Render prompt statici evidence-driven — 5 visual families per concept SA5, template per nome usato come blueprint, prop catalog, aspect ratio + GPT Image 2 default. Skill nativa 24_static_ads (SA6).
argument-hint: [aspect ratio] [foto prodotto]
---

# /pm-statiche — Static Render Prompts (evidence-driven)

Esegui la skill nativa **`directives/skills/24_static_ads/SKILL.md`** (SA6 — Asset Production). Usa i reference `visual-families.md` (5 famiglie + struttura prompt) e `40-templates.md` (libreria template per nome).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/24_static_ads/SKILL.md` + `visual-families.md` + libreria `40-templates.md`.
2. Auto-discovery dei concept approvati SA5 (`intermediate/sa5_creative_framework.md`), VOC (`01_VOC_Research/`) e Brand DNA (`02_Brand_DNA/`). Se mancano i concept, indirizza a SA5 (`/pm-insight` → pipeline); se manca VOC/Brand DNA, a `/pm-dati-qualitativi` e `/pm-brand-kit`.
3. Per ogni concept approvato: cataloga i prop dalle foto prodotto, poi scrivi **5 render prompt** (uno per visual family) costruiti su template per nome usati come **blueprint** (studia un ad vincente reale del brand, devia dallo styling letterale).
4. Aspect ratio in intake; GPT Image 2 default per ogni ratio (Nano Banana 2 solo per 4:5 vero insistito). Subset picker obbligatorio Path B/C/D. Report progresso ogni 5 generazioni su Path C.
5. Output testo + `04_Static_Ads/static-concepts-[YYYY-MM-DD].md`.

Conferma il costo crediti prima della generazione.
