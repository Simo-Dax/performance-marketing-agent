---
description: Genera report performance (weekly/monthly/quarterly/annual) per Google/Meta/blended con struttura fissa, KPI business-model-aware, insights + action points + next steps. SA8.
argument-hint: [weekly|monthly|quarterly|annual] [google|meta|entrambi]
---

# /pm-report — Performance Report (SA8)

Genera un report seguendo la struttura fissa di **`directives/skills/31_reporting_template.md`** (SA8).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/31_reporting_template.md` per la struttura e il look & feel.
2. Determina periodo (weekly/monthly/quarterly/annual) e canale (Google/Meta/entrambi). Se non specificati, chiedi.
3. Determina il business model da `context/brand/business_strategy.md` → seleziona il set KPI giusto (eCommerce / SaaS / Lead Gen).
4. Pull dati:
   - Google → `15_google_ads_analytics` (GAQL, MCC `5524890329`)
   - Meta → `16_meta_ads_analytics` (se MCP non configurato → chiedi export CSV o usa `/pm-handoff`)
5. Calcola delta periodo su periodo, RAG status, anomalie, creative fatigue.
6. Produci SEMPRE: KPI Scorecard → Insights 💡 → Action Points 🎯 (ICE-scored) → Next Steps ➡️.
7. Output: `output/reports/{YYYY-MM-DD}_{tipo}/` — `executive_summary.md` (+ `.html` per email se richiesto) + report per canale.

## Email (opzionale)
Se richiesto invio: Gmail MCP → crea **bozza** con HTML inline. Mai invio diretto senza conferma esplicita.
