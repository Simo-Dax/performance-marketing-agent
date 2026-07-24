# Performance Marketing Team — Orchestrator

Sistema multi-agent per performance marketing end-to-end: dal brief brand agli asset pronti al lancio. Agnostico rispetto al brand — il contesto specifico è in `context/brand/` e `context/campaign/`.

> **Cataloghi di dettaglio (caricati SOLO quando servono, non ogni turno):** routing skill→agente in `directives/skill_orchestrator.md` · elenco comandi `/pm-*` in `COMMANDS.md` · MCP/tool in `execution/tools.md` · mappa output completa in `output/README.md` · automazione in `ROADMAP.md` (Task 8). Questo file è l'indice operativo: leggi i cataloghi quando devi instradare a qualcosa di specifico.

---

## Regole base (valgono per ogni task)

1. **Non assumere. Non nascondere la confusione. Esplicita i tradeoff.** Se manca contesto o ci sono più strade, dillo e mostra le alternative — non indovinare in silenzio.
2. **Codice minimo che risolve il problema. Niente speculativo.** Nessuna astrazione/opzione/feature "per il futuro" non richiesta.
3. **Tocca solo ciò che devi. Pulisci solo il tuo casino.** Niente refactor collaterali; rimuovi solo file/temp che hai creato tu.
4. **Definisci i criteri di successo. Loop finché non sono verificati.** Dichiara cosa significa "fatto", poi prova/verifica — niente "dovrebbe funzionare".

---

## Architettura

```
ORCHESTRATOR (questo file)
├── sa1_competitor_analysis   ← spy static+video, ugc-scraper, review-gap, SimilarWeb
├── sa2_market_research       ← VOC, JTBD, Lenny's Data, first-party data
├── sa3_financial_performance ← MER/ROAS/CPA/NCAC/budget (da brief + SA2)
├── sa4_pm_strategist         ← strategia + segment-pain + campaign architecture (da SA1+SA2+SA3)
├── sa5_creative_concepts     ← ad-angles, concept, character, rebuild (da SA4)
├── sa6_asset_production      ← video-script, static, ugc, product-shot, multiplier (da SA5+SA7)
├── sa7_ad_copywriter         ← headline-bank, meta/google copy (da SA4+SA5)
├── sa8_analytics_reporting   ← Google/Meta Ads report + meta_analyze (read) + meta_build (write)
└── sa9_crm_lifecycle         ← CRM/RFM/email lifecycle (canale owned, indipendente)
```

**Flusso pipeline creativa:** SA1∥SA2 → [47 review-gap + 48 segment-pain] → Insight (🚦GATE 1) → SA3 → SA4 [Brand Strategy 🚦GATE 2 → Campaign Architecture] → SA5 → SA7 → SA6 → consolidation.

- SA1∥SA2 sono gli **unici in parallelo** (davvero indipendenti). Tutto il resto è sequenziale.
- **GATE umani** stanno sull'orchestrator, fra una Task e l'altra: 🚦GATE 1 = insight validati (`33`), 🚦GATE 2 = strategia validata (`32`). I subagent non si fermano da soli.
- **SA8 e SA9 sono binari indipendenti**, invocati on-demand fuori dalla pipeline.
- Filosofia human-in-the-loop: l'AI accelera dato ed esecuzione; l'umano valida insight e strategia.

---

## Come si invocano gli agenti

I 9 sub-agent vivono in `.claude/agents/saN_*.md` come **subagent nativi** (frontmatter `name` + `description`, corpo SOP).

1. **Via Task tool**, `subagent_type` = il `name` del frontmatter (`sa1-competitor-analysis` … `sa9-crm-lifecycle`). Mai letti inline nel contesto dell'orchestrator.
2. **Contesto isolato:** ogni agente gira in una sua finestra e ritorna solo il deliverable.
3. **Parallelo = stesso messaggio:** SA1+SA2 = due Task in un messaggio. Il resto = un Task per volta.
4. **Handoff via file:** gli agenti si passano il lavoro scrivendo/leggendo `intermediate/*.md`, non via contesto condiviso.

> **Agente vs skill vs command:** un **subagent** (`.claude/agents/`) è un *ruolo* che orchestra skill. Una **skill** (`directives/skills/NN_*`) è una *procedura*. Un **command** `/pm-*` (`.claude/commands/`) lancia una skill.

---

## Runbook Orchestrator

0. **Self-improvement:** a inizio sessione leggi `directives/self_improvement.md` + `directives/feedback_log.md` + memory `feedback`. Applica le regole. Feedback utente in-run → `/pm-feedback`.
0.5. **🚦 Context Completeness Gate:** verifica `context/brand/` (`business_profile.md`, `tone_of_voice.md`) + `context/brand/financials/` (per SA3) + (per campagna specifica) `context/campaign/brief.md` con budget/revenue/AOV/margin. Campi critici mancanti → ferma, elenca, attiva `08_grill_me`. Garbage in = garbage out.
1. Leggi `context/campaign/brief.md` (obbligatorio solo per campagne specifiche; senza, gira in modalità strategia/ricerca senza SA3) + brand context da `context/brand/`.
2. **SA1 + SA2 in parallelo** (due Task, stesso messaggio). Per strategia/posizionamento: anche `47_competitor_review_mining` + `48_segment_pain_prioritization` → alimentano l'insight.
3. `33_insight_synthesis` → `intermediate/insight.md` → **🚦GATE 1** (ferma, mostra le 7 dimensioni, attendi OK umano).
4. **SA3** (`sa3-financial-performance`) → `intermediate/sa3_financial_framework.md`.
5. **SA4 Fase 1** (`sa4-pm-strategist`, esegue `32_brand_strategy`) → `sa4_brand_strategy.md` + `tone_of_voice_campaign.md` → **🚦GATE 2** (attendi OK umano). Opzionale `34_editorial_content_plan`.
6. **SA4 Fase 2** (stesso agente, Campaign Architecture) → `intermediate/sa4_strategy.md`.
7. **SA5** (`sa5-creative-concepts`) con output SA4.
8. **SA7** (`sa7-ad-copywriter`) con SA4+SA5 (dopo SA5 — il copy segue i concept).
9. **SA6** (`sa6-asset-production`) con SA5+SA7.
10. Consolida in `output/{brand}_{campaign}_{date}/final/`.

> Routing skill→agente: `directives/skill_orchestrator.md`. SA8/SA9 si invocano on-demand fuori da questa sequenza.

---

## Struttura & Convenzione Output

```
/
├── CLAUDE.md · ROADMAP.md · COMMANDS.md
├── .claude/agents/       ← 9 subagent nativi
├── .claude/commands/     ← command /pm-*
├── context/
│   ├── brand/            ← business_profile, tone_of_voice, anti_ai_writing_style, brand_kit, design_system, preferences, financials/
│   ├── campaign/         ← brief.md, constraints.md, data/ (solo campagna specifica)
│   └── references/       ← ads/, copy/, landing-pages/ (+ cro_principles.md)
├── directives/
│   ├── skill_orchestrator.md   ← routing skill→agente
│   └── skills/           ← tutte le skill (NN_*) + _shared/ (motori riusati)
├── execution/            ← reference/tooling agnostico: tools.md, calculators/, strategy-method/, scripts/, workflows/, prompts/
└── output/               ← OUTPUT per-brand (vedi mappa sotto)
```

**Mappa output** (dove ogni skill salva — dettaglio completo in `output/README.md`):

```
output/
├── {brand}_{campaign}_{date}/       ← working dir campagna (apri CC qui = pwd)
│   ├── 01_VOC_Research/  ← 18 · 02_Brand_DNA/ ← 21 · 03_Ad_Spy/ ← 19+52 (+_scratch/format-*.json)
│   ├── 04_Static_Ads/ ← 24 · 05_UGC_Prompts/ ← 25 · 06_Ad_Copy/ ← 28+54 · 07_Multiplied_Ads/ ← 27
│   ├── 08_Rebuilt_Competitor_Ads/ ← 23 · 09_Meta_Handoff/ ← 30 · 10_Landing_Pages/ ← 29
│   ├── 11_Characters/ ← 22 · 12_Email/ ← 46 · 13_Meta_Campaigns/ ← 51 · 14_Creative_Briefs/ ← 53 · 15_Video_Scripts/ ← 55
│   ├── _assets/product-shots/ ← 26
│   ├── intermediate/    ← output TESTUALI dei SA (insight, sa1..sa9, strategy, copy deck)
│   └── final/           ← deliverable compilati (media_plan, ad_copy, creative_framework, assets/)
├── reports/{data}_{tipo}/    ← SA8 (report, meta_analysis, meta_campaigns)
└── dashboard/                ← competitor-ads + performance (alimentate da data.json)
```

**Regole output (obbligatorie):**
1. Ogni skill dichiara esplicitamente il suo output path.
2. Testo fra SA → `intermediate/`. Asset/HTML → sottocartelle `NN_*/`. Deliverable finali → `final/`. Report SA8 → `output/reports/`.
3. `execution/` è solo reference/tooling agnostico: **mai** output di campagna.
4. Naming campagna: `{brand}_{campaign}_{date}`.
5. Script di UNA skill → co-locati in `directives/skills/<skill>/scripts/` (unità portabile self-contained). `execution/scripts/` solo per script cross-skill.
6. Le skill scrivono nella cartella dove CC è aperto (`pwd`). Il CLAUDE.md root si carica anche da una sottocartella.

---

## MCP disponibili

Dettaglio + prefissi in `execution/tools.md`. In sintesi:

- **Ads:** Meta Ads MCP (SA1 spy, SA8, `50_meta_analyze` read / `51_meta_build` write) · Google Ads MCP (SA1/SA4/SA8, MCC 5524890329).
- **Produzione:** Canva · Higgsfield (SA6 immagini/video/product) · Apify + fal.ai (spy, ugc, whisper — via `.mcp.json`).
- **Research:** SimilarWeb (SA1) · Lenny's Data (SA2).
- **Ops:** Gmail · Google Drive · Calendar · Slack · n8n. Klaviyo ⚠️ da configurare (SA9, `/pm-setup-klaviyo`).

Setup key: `/pm-setup-apify`, `/pm-setup-fal-ai`, `/pm-setup-klaviyo`.

---

## Skill — indice per agente

Elenco completo con trigger/dipendenze in `directives/skill_orchestrator.md`; comandi in `COMMANDS.md`. Ogni skill NN vive in `directives/skills/NN_*` con la sua SOP dettagliata (caricata solo quando invocata).

| SA / Fase | Skill (num) |
|---|---|
| **SA1** Competitor | 19 ad_spy (spy static + reverse-eng) · 52 ad_spy_video · 20 ugc_scraper · 47 review_mining |
| **SA2** Research | 18 voc_research · 38 first_party_data · 09 marketing_psychology |
| **SA3** Financial | 17 financial_performance |
| **SA4** Strategy | 32 brand_strategy (GATE 2) · 48 segment_pain · 34 editorial_plan · 39 marketing_ideas |
| **33** Ponte | 33 insight_synthesis (GATE 1) |
| **SA5** Creative | 53 ad_angles · 13 creative_concepts · 22 character_creator · 23 competitor_rebuild |
| **SA6** Production | 55 video_script · 24 static_ads (rebrand) · 25 ugc_prompt · 26 product_shot · 27 multiplier · 14 asset_router · 42 carousel |
| **SA7** Copy | 54 headline_bank · 28 meta_copy · 12 google_copy · 11/10/02/03 copy support · 49 anti_ai_slop · 41 seo_content |
| **SA8** Analytics | 15 google_analytics · 16 meta_analytics · 31 report_template · 35 search_term · 36 google_audit · 37 google_optim · 40 seo_audit · 50 meta_analyze · 51 meta_build |
| **SA9** CRM | 43 crm_analysis · 44 rfm · 45 email_strategy · 46 email_creation |
| Pre-pipeline | 21 brand_dna · 08 grill_me · 01 landing_brief · 29 landing_page · 04-07 design/frontend |

**Note chiave:**
- `_shared/` = motori riusati da 53/54/55 (angle_engine, awareness_tension_funnel, niche_offer_types, headline_frameworks, script_frameworks, creative_claims_compliance, creative_kill_floor_review, format_teardown_recreation, adjacency_kill_pass). Non invocabili direttamente.
- **`30_meta_handoff` DEPRECATA** → sostituita da `50_meta_analyze` (read) + `51_meta_build` (write).
- **Skill globali CC** (in `~/.claude/skills/`): marketing-psychology, copywriting, copy-editing, marketing-ideas, higgsfield-* (generate/product/marketplace/soul-id), google-search-console.
- Zero dipendenze da plugin di terzi: i servizi (Apify, fal.ai, Playwright, Higgsfield) girano come MCP propri.

---

## Avvio sessione

**Pipeline campagna:** compila `context/campaign/brief.md` → verifica `context/brand/` → crea `output/{brand}_{campaign}_{date}/` → apri CC in quella folder → "Lancia pipeline performance marketing per [BRAND]".

**SA8 (report, indipendente):** "Genera report [weekly|monthly|quarterly|annual] per [Google|Meta|entrambi]" → output in `output/reports/`.

**SA9 (CRM, indipendente):** export clienti in `context/campaign/data/` → `/pm-crm-analysis` → `/pm-rfm` → 🚦 valida segmenti → `/pm-email-strategy` → `/pm-email-copy`.

---

## Esecuzione autonoma

Quattro leve (dettaglio in ROADMAP Task 8):
- **`/goal <condizione>`** — locale, a turni finché un evaluator verifica. **⚠️ Salta i GATE umani** → solo task meccanici con end-state verificabile, MAI la pipeline gated. La skill deve *stampare la prova*.
- **`/schedule`** — routine cloud (cron/API/GitHub). Ideale per SA8 ricorrente. Richiede repo GitHub + Claude Code web.
- **n8n** — movimento dati dashboard, token-zero (Shopify+Google+Meta → `data.json`).
- **`/loop`** — ripeti un prompt a intervallo in sessione aperta.

Regola: report ricorrenti → routine · batch produzione → `/goal` · dati dashboard → n8n.
