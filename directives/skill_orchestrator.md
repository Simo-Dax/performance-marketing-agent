# Skill Orchestrator — Performance Marketing Team

Questo file definisce il routing delle skill: quando attivarle, in quale fase del flusso, e con quale priorità. L'orchestrator lo legge prima di delegare ai sub-agent.

> **⭐ Convenzione Output:** ogni skill salva i suoi output sotto `output/` secondo la mappa autoritativa in `claude.md` (sezione "Convenzione Output"). Output testuali fra SA → `intermediate/`, asset/HTML → sottocartelle numerate `NN_*/` sotto la cartella campagna, deliverable finali → `final/`, report → `output/reports/`, dashboard → `output/dashboard/`. `execution/` = solo reference, mai output di campagna. Quando deleghi a un sub-agent/skill, ricordagli il path di output esatto.

---

## Mappa Skill → Sub-Agent

### Skill Native (in `directives/skills/`)

| Skill | Sub-Agent | Fase | Trigger |
|-------|-----------|------|---------|
| `17_financial_performance` | SA3 | Financial | Calcolo MER/ROAS/CPA/NCAC targets + budget framework — sempre prima di SA4 |
| `09_marketing_psychology` | SA2, SA5, SA7 | Research + Creative | Sempre attiva per insight comportamentali |
| `53_ad_angles` | SA5 | Creative | Angle finder veloce evidence-driven, a monte di `13_creative_concepts` — angoli medium-neutral, SPREAD/FOCUS, gratis e solo testo. Input: VOC + Brand DNA (+ Ad Spy opzionale). Output id-stabili `A01...`. |
| `13_creative_concepts` | SA5 | Creative | Sviluppo concept da brief strategico |
| `11_copywriting_ads_meta` | SA7 | Creative | Copy Meta Ads (primary text, headline, description) |
| `12_copywriting_ads_google` | SA7 | Creative | Copy Google RSA (15 headline, 4 description) |
| `10_advanced_copywriting` | SA7 | Creative | Copy complesso, funnel multi-step |
| `14_asset_production` | SA6 | Production | Brief per asset visivi statici e video |
| `15_google_ads_analytics` | SA8 | Analytics | Report performance Google Ads — weekly/monthly/quarterly/annual |
| `16_meta_ads_analytics` | SA8 | Analytics | Report performance Meta Ads — weekly/monthly/quarterly/annual |
| `01_landing_brief` | SA4 / Orchestrator | Strategy | Se la campagna include landing page da costruire |
| `02_headline_optimization` | SA7 | Creative | Ottimizzazione headline dopo prima draft |
| `03_editing_selfcheck` | SA7 / Orchestrator | QA | Self-check prima di ogni delivery |
| `05_frontend_design` | SA6 | Production | Solo se richiesta produzione landing page |
| `06_web_artifacts` | SA6 | Production | Solo se richiesta produzione componenti React |
| `07_vercel_guidelines` | SA6 | QA | Audit qualità landing page prodotta |
| `08_grill_me` | Orchestrator | Brief | Quando il brief iniziale è incompleto o ambiguo |
| `04_references_tecniche_design` | SA5, SA6 | Creative | Riferimento design pattern per visual |
| `39_marketing_ideas` | SA4 | Strategy | Libreria 139 idee marketing per categoria — ispirazione/selezione tattiche cross-channel |
| `40_seo_audit` | SA8 | Analytics (organico) | Audit SEO tecnico + on-page + content, framework 5 priorità + script `seo_checker.py` |
| `41_seo_content_optimizer` | SA7 | Creative (organico) | Ottimizzazione SEO singolo contenuto da URL: keyword research 9 tipi + slug + heading + meta + internal linking |
| `42_carousel` | SA6 / Post-SA7 | Production | Layout component carousel/slider per landing page (accessibilità, performance, SEO DOM) |
| `43_crm_database_analysis` | SA9 | CRM | Analisi DB clienti: struttura, quality, list health, baseline, gap. Prerequisito RFM |
| `44_rfm_segmentation` | SA9 | CRM | Segmentazione RFM + lifecycle + churn risk, 11 segmenti con azione |
| `45_email_strategy` | SA9 | CRM | Calendario + frequenza + automazioni ICE + KPI email, business-model-aware |
| `46_email_creation` | SA9 | CRM | Copy email per segmento: subject A/B + body + CTA, anti-AI |

### Skill produzione/research — internalizzate (in `directives/skills/`, numerazione 18-30)

| Skill | Sub-Agent | Fase | Trigger |
|-------|-----------|------|---------|
| `18_voc_research` | SA2 | Research | VOC research — linguaggio verbatim clienti da review/community. Input: URL prodotto + nome prodotto. Output HTML. Richiede web search. |
| `19_ad_spy` | SA1 | Research | Ad spy competitor Meta — swipe file HTML con static ads. Input: brand/lista/nicchia, paese, n. ads. Richiede Apify. |
| `52_ad_spy_video` | SA1 | Research | Ad spy competitor Meta — sorella video di `19_ad_spy` (solo VIDEO ads). Teardown per video: script timestampato (fal.ai Whisper), on-screen text, hook, beat sheet, CTA. Input: brand/lista/nicchia, paese, n. video. Richiede Apify + fal.ai. |
| `20_ugc_scraper` | SA1 | Research | Scraping TikTok UGC virali — 25 transcript per swipe file. Input: VOC + nicchia. Richiede Apify. Costo ~$0.056/run. |
| `21_brand_dna` | Pre-pipeline | Setup | Brand DNA HTML — colori live via Playwright + web search. Input: nome brand + URL. Prerequisito per static e character. |
| `22_character_creator` | SA5 | Creative | Brand character creator — 1-10 personaggi (headshot + full body). Input: Brand DNA opzionale. Modello: GPT Image 2 o Nano Banana 2. |
| `23_competitor_rebuild` | SA5 | Creative | Competitor ad rebuild — trasforma ad competitor in prompt per proprio brand + 5 variazioni persona opzionali. Input: ad competitor + Brand DNA + VOC. |
| `55_video_script` | SA6 | Production | Video Script Studio universale, gratis e solo testo — script finito per qualsiasi formato/lunghezza (10s-90s+), matematica budget parole deterministica, 12 framework nominati, non richiesto da `25_ugc_prompt`. |
| `24_static_ads` | SA6 | Production | 40 static ad prompts — da Brand DNA + VOC. Input: brand URL + nome prodotto. Modello: GPT Image 2 o Nano Banana 2. |
| `25_ugc_prompt` | SA6 | Production | UGC video prompts → Seedance 2.0 (Higgsfield o fal.ai). Input: script UGC + VOC + Brand DNA. 6 prompt con hook archetype diversi. |
| `26_product_shot` | SA6 | Production | Product shot (Studio/Held/Worn). Input: immagine prodotto. Opzionale: personaggio da `22_character_creator`. |
| `27_multiplier` | SA6 | Production | Moltiplicatore winner — 5-8 variazioni Andromeda-compliant da ad vincente. Input: ad vincente + 1-3 img prodotto + Brand DNA + VOC. |
| `54_headline_bank` | SA7 | Creative | Headline bank dedicata, più profonda di `28_meta_copy` — ~20 headline + 8 hook on-image + 6 first-line, framework-nominate, char-discipline 27/40, gate personal-attributes Meta. Input: angolo/creative/angle-bank/riff. |
| `28_meta_copy` | SA7 | Creative | Meta ad copy — 5 headline (40char) + 5 description (30char) + 2 primary text. Input: Brand DNA + VOC + creative. Alias nativo di `11_copywriting_ads_meta`. |
| `29_landing_page` | Post-SA7 | Production | Landing page HTML single-file da ad Meta (Tailwind + VOC injection). Input: ad creative + Brand DNA + VOC. Anti-AI slop 34-point audit. |
| `30_meta_handoff` | Post-SA6 | Lancio | Prompt handoff per Meta Ads MCP su claude.ai web. Due modalità: analisi campagne esistenti o build nuove campagne. |

---

## Flusso Standard Performance Marketing

### Fase 0 — 🚦 Context Completeness Gate (prima di tutto)
Prima di avviare la pipeline, l'orchestrator verifica che il contesto sia sufficiente. **Garbage in = garbage out.** Controlla:
- `context/brand/`: `business_profile.md` (chi è il brand, modello business, target clienti), `tone_of_voice.md` compilato (non template), `brand_kit.md`/`design_system.md` se disponibili
- `context/brand/financials/`: dati finanziari brand (margin %, LTV, AOV storico, MER storico, NCAC) — **opzionale ma critico per SA3**; se assente SA3 usa solo i valori del brief
- `context/campaign/brief.md`: **obbligatorio solo per campagne specifiche** — budget mensile, revenue target, AOV, gross margin % + obiettivo, prodotto, timing. Per ricerca/strategia standalone il brief non è necessario.
- `context/campaign/data/`: dati first-party (opzionale ma raccomandato → `38_first_party_data_analysis`)

Esito gate:
- **Campi critici mancanti** → ferma, elenca cosa manca, attiva `08_grill_me` per raccoglierli. Non procedere con valori inventati.
- **Context parziale ma sufficiente** → procedi segnalando cosa manca e cosa verrà generato (es. Brand DNA via `21_brand_dna`, VOC via `18_voc_research`).
- **Context completo** → procedi.

> Lo stesso gate vale per le singole skill: ognuna verifica i propri input (auto-discovery) e si ferma se mancano prerequisiti obbligatori (es. `29_landing_page` richiede VOC + Brand DNA).

### Fase 1 — Brief Collection
- Orchestrator legge `context/campaign/brief.md`
- Se brief incompleto → attiva `08_grill_me`
- Legge `context/brand/` per brand context
- Legge `context/references/` per materiale di riferimento

### Fase 2 — Research (SA1 + SA2 in parallelo)
- SA1: WebSearch + SimilarWeb MCP + **`19_ad_spy`** (competitor ad intelligence, static) + **`52_ad_spy_video`** (competitor ad intelligence, video teardown) + **`20_ugc_scraper`** (TikTok UGC viral)
- SA2: WebSearch + Lenny's Data MCP + `09_marketing_psychology` + **`18_voc_research`** (VOC verbatim) + JTBD/Forces of Progress

### Fase 2.5 — Insight Synthesis (🚦 GATE 1 umano)
- Attiva **`33_insight_synthesis`**: unifica SA1+SA2 nelle 7 dimensioni (Job, Alternative, Categoria, Key Segment, Pain, Desideri, Obiezioni), ognuna con fonte citata
- Output: `intermediate/insight.md` con sezione "⚠️ DA VALIDARE DALL'UMANO"
- **🚦 GATE 1**: l'orchestrator si ferma, mostra il riepilogo, chiede conferma. **Non procedere senza OK esplicito dell'umano.** L'AI accelera dato ed esecuzione; insight e strategia li valida l'umano.

### Fase 2b — Financial Modeling (SA3)
- Input: `context/campaign/brief.md` (se disponibile) + output SA2 (benchmark) + `intermediate/insight.md` + `context/brand/business_profile.md` + `context/brand/financials/` (se disponibile)
- Attiva `17_financial_performance` (+ 10 calculators Learnn in `execution/calculators/`) per KPI, break-even, red flag
- Output: `intermediate/sa3_financial_framework.md` — MER, ROAS, CPA, NCAC, budget framework, new vs returning split
- Se dati mancanti nel brief (AOV, margin, revenue target): attiva `08_grill_me` e blocca pipeline

### Fase 3 — Strategy (SA4 — DUE FASI)
- **Fase 1 — Brand Strategy**: attiva **`32_brand_strategy`** da `intermediate/insight.md` validato → VP (piramide Bain), USP, ToV+nemico, benefici, offer design (10+10+10), bonus, garanzie, trigger event
  - Output: `intermediate/sa4_brand_strategy.md` + `intermediate/tone_of_voice_campaign.md`
  - **🚦 GATE 2**: mostra VP/USP/ToV/offerta/trigger, ricorda i punti DA DECIDERE DALL'UMANO (valori, purpose, mission), chiedi OK
  - Opzionale: **`34_editorial_content_plan`** per piano editoriale organico
- **Fase 2 — Campaign Architecture**: input strategia + SA3 financial → architettura campagne Meta+Google, targeting, budget, KPI, **ICE prioritization** (sez. 11) + **experiment list** (sez. 12)
  - Se campagna include landing page → attiva `01_landing_brief`
  - Output: `intermediate/sa4_strategy.md`

### Fase 2a — Setup Brand (Pre-pipeline, prima della ricerca se brand non ha DNA)
- Orchestrator: attiva **`21_brand_dna`** per estrarre identità visiva e verbale del brand
- Output: `02_Brand_DNA/brand-dna-[brand-slug].html` — prerequisito per `24_static_ads` e `22_character_creator`

### Fase 4 — Creative (SA5 → SA7 sequenziale)
- SA5: (opzionale, veloce) **`53_ad_angles`** per un ventaglio ampio di angoli prima del deck pieno — poi attiva `13_creative_concepts` + `04_references_tecniche_design` + `09_marketing_psychology`
  - **`22_character_creator`** — se la campagna include UGC video o product shot con personaggio fisso
  - **`23_competitor_rebuild`** — se esiste un competitor ad da reverse-engineerare
- SA7: alimentato da output SA5 — (opzionale) **`54_headline_bank`** per esplorare un ventaglio ampio di headline — poi attiva `11_copywriting_ads_meta` + **`28_meta_copy`** + `12_copywriting_ads_google` + `10_advanced_copywriting` + `09_marketing_psychology`
- SA7 NON parte prima del completamento di SA5: il copy deve riflettere i concept approvati

### Fase 5 — Production (SA6)
- Input: output SA5 + SA7 + brand kit
- Attiva `14_asset_production`
- **`55_video_script`** — script finito per formati non coperti da `25_ugc_prompt` (voiceover-only, dialogo, founder, VSL) o deliverable-script rapido
- **`24_static_ads`** — 40 prompt statici (GPT Image 2 o Nano Banana 2)
- **`25_ugc_prompt`** — 6 prompt video Seedance 2.0 (se campagna include UGC)
- **`26_product_shot`** — product shot Studio/Held/Worn (se necessario)
- **`27_multiplier`** — 5-8 variazioni Andromeda-compliant (se esiste un ad vincente da moltiplicare)
- Tool: Canva MCP + Higgsfield MCP + fal.ai MCP
- Se landing page: attiva **`29_landing_page`** + `05_frontend_design` o `06_web_artifacts` + `07_vercel_guidelines`

### Fase 6 — QA & Delivery
- SA7 attiva `03_editing_selfcheck` sul copy
- SA6 verifica naming convention e formati
- Orchestrator consolida tutto in `output/{brand}_{campaign}_{date}/final/`
- **`30_meta_handoff`** — genera prompt handoff per Meta Ads MCP su claude.ai web (modalità: analisi o build campagne)

---

## Flusso Analytics & Reporting (SA8 — indipendente dalla pipeline)

SA8 opera separatamente. Trigger: richiesta esplicita di report o audit periodico.

### Fase A — Setup
- Determina periodo (weekly/monthly/quarterly/annual) e canale (Google/Meta/entrambi)
- Carica account da `context/brand/` e `.mcp.json`

### Fase B — Pull dati Google Ads
- Attiva `15_google_ads_analytics` per query GAQL appropriate
- Interroga Google Ads MCP (`mcp__google-ads__search`)
- Periodo default: account MCC `5524890329`, tutti i sub-account

### Fase C — Pull dati Meta Ads
- Attiva `16_meta_ads_analytics` per template query
- Interroga Meta Ads MCP (se configurato) — altrimenti richiede export CSV all'utente

### Fase D — Analisi e Report
- Calcola delta periodo su periodo
- Identifica anomalie e creative fatigue
- Genera report in `output/reports/{YYYY-MM-DD}_{tipo}/`

### Fase E — Handoff opzionale
- Se anomalie critiche o fatigue creativa rilevata: passa brief a Orchestrator per attivare SA5+SA6 (refresh creative)

> **Dashboard performance (live):** `output/dashboard/performance/index.html` legge `data.json` generato da n8n (`execution/workflows/performance_dashboard_n8n.json` — Shopify+Google+Meta). Token-zero sui refresh. SA8 legge `data.json` on-demand per il report narrativo (`31_reporting_template`).

---

## Flusso CRM / Lifecycle (SA9 — indipendente dalla pipeline)

SA9 gestisce il canale owned (email/retention). Trigger: export clienti disponibile o richiesta esplicita.

### Fase 1 — Analisi DB (`43`)
- Input: export clienti (Shopify/CRM/email) in `context/campaign/data/` o `context/brand/financials/`
- Output: `intermediate/sa9_crm_analysis.md` — quality, list health, baseline. Se manca l'export → richiedilo.

### Fase 2 — RFM (`44`)
- Da DB → 11 segmenti RFM + lifecycle + churn risk → `intermediate/sa9_rfm_segments.md`
- 🚦 Gate umano opzionale: valida i segmenti prima della strategia.

### Fase 3 — Strategia email (`45`)
- Da segmenti + business model → automazioni ICE + calendario + KPI → `intermediate/sa9_email_strategy.md`

### Fase 4 — Creazione email (`46`)
- Da strategia + segmento + ToV → copy email (subject A/B + body + CTA) → `12_Email/` o draft Gmail MCP. QA via `03_editing_selfcheck`.

### Collegamenti
- SA9 → SA3 (LTV/repeat reali) · SA9 → SA4 (split acquisition vs retention) · SA9 → SA8 (KPI email nel reporting)
- `38_first_party_data_analysis` e `33_insight_synthesis` alimentano SA9 (dati + angoli copy)

---

## Skill — Status

### Native (create in questa sessione)
- [x] `11_copywriting_ads_meta` — Meta Ads copy
- [x] `12_copywriting_ads_google` — Google RSA copy → `/pm-google-ads-copy`
- [x] `13_creative_concepts` — framework concept (SA5)
- [x] `53_ad_angles` — angle finder veloce, a monte di 13 (SA5)
- [x] `54_headline_bank` — headline bank dedicata (SA7)
- [x] `55_video_script` — script studio universale (SA6)
- [x] `14_asset_production` — router produzione (SA6) → instrada a 24/25/26/27
- [x] `15_google_ads_analytics` — report Google Ads
- [x] `16_meta_ads_analytics` — report Meta Ads
- [x] `17_financial_performance` — MER/ROAS/CPA framework

### Produzione/Research — internalizzate (skill native 18-30, +52)
- [x] `18_voc_research` — VOC Research (SA2)
- [x] `19_ad_spy` — Ad Spy 2.0, static (SA1)
- [x] `52_ad_spy_video` — Ad Spy Video, teardown video competitor (SA1)
- [x] `20_ugc_scraper` — UGC Scraper 2.0 (SA1)
- [x] `21_brand_dna` — Brand DNA Playwright 3.0 (Pre-pipeline)
- [x] `22_character_creator` — Character Creator (SA5)
- [x] `23_competitor_rebuild` — Competitor Ad Rebuild (SA5)
- [x] `24_static_ads` — 40 Static Ad Prompts (SA6)
- [x] `25_ugc_prompt` — UGC Prompt Generator Seedance 2.0 (SA6)
- [x] `26_product_shot` — Product Shot Generator (SA6)
- [x] `27_multiplier` — Winning Ad Multiplier 2.0 (SA6)
- [x] `28_meta_copy` — Meta Ad Copy (SA7)
- [x] `29_landing_page` — Landing Page Generator (Post-SA7)
- [x] `30_meta_handoff` — Meta Ads Handoff (Post-SA6)

### Strategia + Reporting (internalizzate da Marketing Strategist + Learnn)
- [x] `31_reporting_template` — struttura fissa report SA8, KPI business-model-aware, export HTML email (SA8) → `/pm-report`
- [x] `32_brand_strategy` — VP Bain + USP + ToV + offer design + bonus/garanzie + trigger (SA4 Fase 1, 🚦GATE 2) → `/pm-brand-strategy`
- [x] `33_insight_synthesis` — 7 dimensioni + gate umano (ponte SA2→SA4, 🚦GATE 1) → `/pm-insight`
- [x] `34_editorial_content_plan` — piano editoriale + content calendar, 5 awareness (post-SA4) → `/pm-editorial`
- [x] `03_editing_selfcheck` — potenziato dual-mode: personal (Simone) + brand-campagna (voice-editor: anti-AI + ToV brand)

### SEO / Supporto (importate da kostja94/marketing-skills + plugin, tradotte IT)
- [x] `39_marketing_ideas` — 139 idee marketing per categoria (SA4)
- [x] `40_seo_audit` — audit SEO tecnico/on-page/content + `seo_checker.py` (SA8)
- [x] `41_seo_content_optimizer` — ottimizzazione SEO contenuto da URL (SA7/organico)
- [x] `42_carousel` — layout component carousel per landing (SA6/Post-SA7)
- [x] `google-search-console` (globale `~/.claude/skills/`) — analisi dati GSC, alimenta `40_seo_audit`

### CRM / Lifecycle (SA9 — create in questa sessione)
- [x] `43_crm_database_analysis` — analisi DB clienti (SA9)
- [x] `44_rfm_segmentation` — segmentazione RFM + lifecycle + churn (SA9)
- [x] `45_email_strategy` — strategia email + automazioni ICE (SA9)
- [x] `46_email_creation` — copy email per segmento, anti-AI (SA9)

> Layer strategia internalizzato dal progetto **Marketing Strategist** (corso Learnn, metodo 4 fasi). Reference completa in `execution/strategy-method/`. Filosofia human-in-the-loop: l'AI accelera dato (fase 1) ed esecuzione (fase 4); l'**umano valida insight (GATE 1) e strategia (GATE 2)**.

Vedi `ROADMAP.md` per status e priorità.

---

## Comandi `/pm-*` (in `.claude/commands/`)

Ogni skill produzione è invocabile come slash-command nativo. Tabella di mapping:

| Comando | Skill | Agente |
|---------|-------|--------|
| `/pm-dati-qualitativi` | `18_voc_research` | SA2 |
| `/pm-competitor-spy` | `19_ad_spy` | SA1 |
| `/pm-competitor-spy-video` | `52_ad_spy_video` | SA1 |
| `/pm-ugc-analysis` | `20_ugc_scraper` | SA1 |
| `/pm-brand-kit` | `21_brand_dna` | Pre-pipeline |
| `/pm-buyer-persona` | `22_character_creator` | SA5 |
| `/pm-competitor-rebuild` | `23_competitor_rebuild` | SA5 |
| `/pm-ad-angles` | `53_ad_angles` | SA5 |
| `/pm-statiche` | `24_static_ads` | SA6 |
| `/pm-video-script` | `55_video_script` | SA6 |
| `/pm-ugc-video` | `25_ugc_prompt` | SA6 |
| `/pm-product-photo` | `26_product_shot` | SA6 |
| `/pm-multiplier` | `27_multiplier` | SA6 |
| `/pm-headlines` | `54_headline_bank` | SA7 |
| `/pm-meta-copy` | `28_meta_copy` | SA7 |
| `/pm-google-ads-copy` | `12_copywriting_ads_google` | SA7 |
| `/pm-landing-page` | `29_landing_page` | Post-SA7 |
| `/pm-handoff` | `30_meta_handoff` | Post-SA6 |
| `/pm-report` | `31_reporting_template` | SA8 |
| `/pm-insight` | `33_insight_synthesis` | Ponte SA2→SA4 (🚦GATE 1) |
| `/pm-brand-strategy` | `32_brand_strategy` | SA4 Fase 1 (🚦GATE 2) |
| `/pm-editorial` | `34_editorial_content_plan` | Post-SA4 (organico) |
| `/pm-data-analysis` | `38_first_party_data_analysis` | SA2 (quant→SA3, qual→insight) |
| `/pm-search-term` | `35_google_ads_search_term_qs` | SA8 |
| `/pm-google-audit` | `36_google_ads_audit` | SA8 |
| `/pm-google-optimisations` | `37_google_ads_optimisations` | SA8 |
| `/pm-seo-audit` | `40_seo_audit` | SA8 (organico) |
| `/pm-seo-content` | `41_seo_content_optimizer` | SA7 (organico) |
| `/pm-carousel` | `42_carousel` | SA6 / Post-SA7 |
| `/pm-crm-analysis` | `43_crm_database_analysis` | SA9 |
| `/pm-rfm` | `44_rfm_segmentation` | SA9 |
| `/pm-email-strategy` | `45_email_strategy` | SA9 |
| `/pm-email-copy` | `46_email_creation` | SA9 |
| `/pm-feedback` | `self_improvement` | self-improvement |
| `/pm-setup` | master setup sistema | — |
| `/pm-setup-apify` | config Apify key | — |
| `/pm-setup-fal-ai` | config Fal AI key | — |

---

## Quando NON usare una skill

- **`05_frontend_design` / `06_web_artifacts`**: solo se la campagna richiede produzione landing page, NON per ogni campagna ads
- **`07_vercel_guidelines`**: solo post-produzione landing page, non su copy o asset
- **`08_grill_me`**: solo se brief è genuinamente incompleto — non usare come routine per ogni campagna
