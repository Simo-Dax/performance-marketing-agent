---
description: Google Ads optimisations — esegue la checklist ricorrente per tipo campagna (Search/Shopping/PMax/Display/Demand Gen/Video) con report stato/azioni. Skill 37 (SA8).
argument-hint: [account] [cadenza: 72h|weekly|monthly|90d]
---

# /pm-google-optimisations — Google Ads Optimisations (SA8)

Esegui la skill **`directives/skills/37_google_ads_optimisations/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/37_google_ads_optimisations/SKILL.md`.
2. Identifica i tipi di campagna nell'account → carica la checklist CSV corrispondente (co-locata nella folder della skill: Search/Shopping/PMax/Display/Demand Gen/Video).
3. Determina la cadenza (72h/weekly/monthly/90d) → esegui solo i task marcati TRUE per quella cadenza.
4. Google Ads MCP (GAQL), MCC `5524890329`. Esegui ogni task, valuta contro soglia.
5. Output: `output/reports/{data}_google-optimisations/` — checklist eseguita per tipo + azioni ICE-prioritizzate.
6. NON modificare l'account senza conferma: produce raccomandazioni, non cambi diretti.
