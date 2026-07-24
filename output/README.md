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

## Struttura interna per ogni campagna (mappa completa skill→cartella)

Questa è la mappa autoritativa dettagliata (CLAUDE.md ne tiene una versione compatta per il routing rapido).

```
{brand}_{campagna}_{data}/
├── 01_VOC_Research/            ← 18_voc_research (/pm-dati-qualitativi)
├── 02_Brand_DNA/              ← 21_brand_dna (/pm-brand-kit)
├── 03_Ad_Spy/ (+ data.json)   ← 19_ad_spy (/pm-competitor-spy) + 52_ad_spy_video (/pm-competitor-spy-video, sottocartella <slug>-video/)
│   └── _scratch/format-*.json ← prompt di ricreazione bancati da 19, consumati da 24_static_ads
├── 04_Static_Ads/             ← 24_static_ads (/pm-statiche)
├── 05_UGC_Prompts/            ← 25_ugc_prompt (/pm-ugc-video)
├── 06_Ad_Copy/                ← 28_meta_copy (/pm-meta-copy) + 54_headline_bank (/pm-headlines)
├── 07_Multiplied_Ads/         ← 27_multiplier (/pm-multiplier)
├── 08_Rebuilt_Competitor_Ads/ ← 23_competitor_rebuild (/pm-competitor-rebuild)
├── 09_Meta_Handoff/           ← 30_meta_handoff (DEPRECATA)
├── 10_Landing_Pages/          ← 29_landing_page (/pm-landing-page)
├── 11_Characters/             ← 22_character_creator (/pm-buyer-persona)
├── 12_Email/                  ← 46_email_creation (/pm-email-copy)
├── 13_Meta_Campaigns/         ← 51_meta_build (/pm-meta-build): plan.md + build-manifest.json + manifest.md
├── 14_Creative_Briefs/ (+ .json) ← 53_ad_angles (/pm-ad-angles): angle bank id-stabili (A01...)
├── 15_Video_Scripts/          ← 55_video_script (/pm-video-script)
├── _assets/product-shots/     ← 26_product_shot (/pm-product-photo)
├── intermediate/              ← output TESTUALI dei SA (handoff interni)
│   ├── insight.md             ← 33_insight_synthesis (/pm-insight)
│   ├── sa1_competitor_landscape.md ← SA1
│   ├── sa2_market_insights.md ← SA2
│   ├── sa3_financial_framework.md ← SA3
│   ├── sa4_brand_strategy.md + tone_of_voice_campaign.md ← 32_brand_strategy
│   ├── sa4_strategy.md        ← SA4 Fase 2 (media plan)
│   ├── sa5_creative_framework.md ← SA5
│   ├── sa7_copy_deck.md       ← SA7
│   ├── sa9_crm_analysis.md / sa9_rfm_segments.md / sa9_email_strategy.md ← SA9 (43/44/45)
│   └── editorial_plan.md + content_calendar.md ← 34_editorial_content_plan
└── final/                     ← deliverable pronti al lancio
    ├── media_plan.md           ← budget allocation + KPI per canale
    ├── ad_copy.md              ← copy Meta + Google pronti al lancio
    ├── creative_framework.md   ← concept approvati + brief visivo
    └── assets/                 ← file immagine/video prodotti da SA6
        └── {brand}_{campagna}_{concept}_{formato}_{variante}.png
```

**Fuori dalla cartella campagna:** `output/reports/{data}_{tipo}/` (SA8: report, meta_analysis, meta_campaigns) · `output/dashboard/` (competitor-ads + performance, alimentate da data.json).

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
