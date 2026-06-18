# Output — Naming Convention & Struttura

## Naming cartelle campagna

```
{brand}_{campagna}_{YYYY-MM-DD}/
```

Esempi:
```
IndieProductivity_LeadGen_2026-06-01/
NomeBrand_Retargeting_2026-07-15/
```

## Struttura interna per ogni campagna

```
{brand}_{campagna}_{data}/
├── intermediate/               ← output sub-agent (handoff interni)
│   ├── sa1_competitor.md
│   ├── sa2_market_research.md
│   ├── sa3_strategy.md
│   └── sa4_creative_concepts.md
└── final/                      ← deliverable pronti al lancio
    ├── media_plan.md            ← budget allocation + KPI per canale
    ├── ad_copy.md               ← copy Meta + Google pronti al lancio
    ├── creative_framework.md    ← concept approvati + brief visivo
    └── assets/                  ← file immagine/video prodotti da SA5
        ├── {brand}_{campagna}_{concept}_{formato}_{variante}.png
        └── ...
```

## Naming asset

```
{brand}_{campagna}_{concept}_{formato}_{variante}.{ext}
```

Esempi:
```
IndieProductivity_LeadGen_Concept1_1x1_A.png
IndieProductivity_LeadGen_Concept1_9x16_B.mp4
NomeBrand_Promo_Concept2_4x5_A.png
```

## Formati standard

| Codice | Dimensioni | Canale |
|--------|-----------|--------|
| 1x1 | 1080×1080 | Meta Feed, Google Display |
| 4x5 | 1080×1350 | Meta Feed |
| 9x16 | 1080×1920 | Stories, Reels, TikTok |
| 191x1 | 1200×628 | Google Display, Meta Link |
