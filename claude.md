# Performance Marketing Team — Orchestrator

Sistema multi-agent per performance marketing end-to-end: dal brief brand agli asset pronti al lancio.
Agnostico rispetto al brand — il contesto specifico è in `context/brand/` e `context/campaign/`.

---

## Regole base (valgono per ogni task)

1. **Non assumere. Non nascondere la confusione. Esplicita i tradeoff.** Se manca contesto o ci sono più strade, dillo e mostra le alternative — non indovinare in silenzio.
2. **Codice minimo che risolve il problema. Niente speculativo.** Nessuna astrazione, opzione o feature "per il futuro" non richiesta.
3. **Tocca solo ciò che devi. Pulisci solo il tuo casino.** Niente refactor collaterali; rimuovi file/temp che hai creato tu, non quelli altrui.
4. **Definisci i criteri di successo. Loop finché non sono verificati.** Dichiara cosa significa "fatto", poi prova/verifica fino a soddisfarlo — niente "dovrebbe funzionare".

---

## Architettura

```
ORCHESTRATOR (questo file)
├── .claude/agents/sa1_competitor_analysis.md   ← WebSearch + SimilarWeb MCP + spy + ugc-scraper
├── .claude/agents/sa2_market_research.md       ← WebSearch + Lenny's Data MCP + voc
├── .claude/agents/sa3_financial_performance.md ← MER / ROAS / CPA / NCAC / budget framework (alimentato da brief + SA2)
├── .claude/agents/sa4_pm_strategist.md         ← strategia: job→pain-non-risolto→desiderio→segmento(contesto+trigger)→posizionamento→nemico+POV (47 review-gap + 48 segment-pain) + campaign architecture Meta+Google (alimentato da SA1+SA2+SA3)
├── .claude/agents/sa5_creative_concepts.md     ← alimentato da SA4 + ad-angles + character + rebuild
├── .claude/agents/sa6_asset_production.md      ← alimentato da SA5 + video-script + static + ugc-prompt + product-shot + multiplier
├── .claude/agents/sa7_ad_copywriter.md         ← alimentato da SA4 + SA5 + headline-bank + copy
├── .claude/agents/sa8_analytics_reporting.md   ← Google Ads MCP + Meta Ads MCP + 15_google_ads_analytics + 16_meta_ads_analytics + 50_meta_analyze (diagnosi read-only) + 51_meta_build (build/write live)
└── .claude/agents/sa9_crm_lifecycle.md         ← CRM/retention/email: 43_crm + 44_rfm + 45_email_strategy + 46_email_creation (canale owned, indipendente)
```

Flusso pipeline creativa: SA1∥SA2 → **[47 review-gap + 48 segment-pain]** → **Insight (🚦GATE 1)** → **SA3** → **SA4 [Brand Strategy 🚦GATE 2 → Campaign Architecture]** → SA5 → SA7 → SA6 → consolidation.

> SA1 e SA2 sono gli unici in parallelo (davvero indipendenti, I/O-bound).
> **Insight Synthesis** (`33`) unisce SA1+SA2 in 7 dimensioni → 🚦GATE 1 (l'umano valida gli insight).
> SA3 (Financial) corre dopo gli insight e prima di SA4: framework finanziario che vincola la strategia.
> **SA4 lavora in 2 fasi:** Brand Strategy (`32`: VP Bain/USP/ToV/offer → 🚦GATE 2) poi Campaign Architecture.
> SA7 dipende da SA5 — il copy deve riflettere la direzione creativa, non precederla.
> SA8 è indipendente dalla pipeline creativa — opera su base ricorrente per reporting e audit. **`50_meta_analyze`** opera il Meta Ads MCP **read-only direttamente in Claude Code** per diagnosi live on-demand: quick check o deep diagnosis (panel investigator avversariale + referee). Sostituisce la modalità "analisi" del vecchio `30_meta_handoff`. Per BUILD/lancio campagne → **`51_meta_build`** (`/pm-meta-build`), l'unica superficie di write sull'account: campaign+ad set+creative+ad tutto PAUSED, cerimonie di conferma su budget/attivazione (un sì per livello, >500/gg = digita il totale). Insieme `50`+`51` sostituiscono `30_meta_handoff`.
> SA9 è indipendente dalla pipeline creativa — gestisce CRM/retention/email (canale owned). Alimenta SA3 (LTV reale), SA4 (split acquisition vs retention), SA8 (KPI email).
> **Filosofia human-in-the-loop:** l'AI accelera dato ed esecuzione; l'umano valida insight (GATE 1) e strategia (GATE 2).

---

## Agenti — dove vivono, come sono organizzati, come si invocano

I 9 sub-agent vivono in **`.claude/agents/`** come **subagent nativi di Claude Code** (NON più nella vecchia `agents/` a root). Ogni file `saN_*.md` ha:
- **frontmatter** YAML in cima: `name` (kebab-case, es. `sa1-competitor-analysis`) + `description` (quando invocarlo + dipendenze + output path);
- **corpo SOP**: ruolo, input richiesti, tool, fasi di lavoro, output, handoff.

**Regole di invocazione (obbligatorie per l'orchestratore):**
1. **Si invocano via Task tool**, con `subagent_type` = il `name` del frontmatter (es. `sa1-competitor-analysis` … `sa9-crm-lifecycle`). NON si leggono inline nel contesto dell'orchestratore.
2. **Contesto isolato**: ogni agente gira in una sua finestra e ritorna **solo il deliverable**. Il ragionamento grezzo resta nel suo contesto.
3. **Parallelo vs sequenziale**: SA1∥SA2 = due Task **nello stesso messaggio** (parallelo vero). Tutto il resto della pipeline = un Task per volta, in sequenza. SA8 e SA9 = binari indipendenti, on-demand.
4. **Handoff via file**: gli agenti si passano il lavoro scrivendo/leggendo `intermediate/*.md` (memoria condivisa su disco), non via contesto condiviso.
5. **Gate umani**: GATE 1 (insight) e GATE 2 (strategia) restano sull'orchestratore, **fra** una invocazione e l'altra — i subagent non si fermano da soli per validazione umana.

> **Agenti vs skill vs command:** un **subagent** (`.claude/agents/`) è un *ruolo* che orchestra una o più skill. Una **skill** (`directives/skills/NN_*`) è una *procedura* eseguibile. Un **command** `/pm-*` (`.claude/commands/`) è la scorciatoia che lancia una skill. I command puntano alle skill, non ai subagent.

---

## Ruolo Orchestrator

0. **Self-improvement:** a inizio sessione legge `directives/self_improvement.md` + `directives/feedback_log.md` + i memory `feedback`. Applica le regole apprese. Durante la run, ogni feedback utente ("va bene / non va bene") viene catturato e processato via la procedura di self-improvement (comando `/pm-feedback`).
0.5. **🚦 Context Completeness Gate:** verifica `context/brand/` (`business_profile.md`, `tone_of_voice.md` compilato) + `context/brand/financials/` (se disponibile, alimenta SA3) + `context/campaign/data/` (opzionale). Se si lancia una campagna specifica, verifica anche `context/campaign/brief.md` (budget, revenue target, AOV, margin — obbligatori per SA3). Se campi critici mancano → ferma, elenca, attiva `08_grill_me`. Garbage in = garbage out. Dettaglio in `skill_orchestrator.md` (Fase 0).
1. Legge brief da `context/campaign/brief.md` — **obbligatorio solo per campagne specifiche**; se non presente, la pipeline può girare in modalità strategia/ricerca senza SA3. Se presente ma incompleto, attiva `directives/skills/08_grill_me`
2. Legge brand context da `context/brand/`
3. Avvia SA1 + SA2 **in parallelo** via Task tool — due chiamate `Task(subagent_type: "sa1-competitor-analysis")` + `Task(subagent_type: "sa2-market-research")` nello **stesso messaggio** (unica fase parallela — davvero indipendenti). Gli step successivi = un Task per volta, in sequenza.
3.5. (Per strategia/posizionamento) Avvia **`47_competitor_review_mining`** (gap recensioni competitor) e **`48_segment_pain_prioritization`** (pain matrix + segmenti per contesto/trigger) → alimentano l'insight
4. Avvia **`33_insight_synthesis`** → `intermediate/insight.md` → **🚦GATE 1**: ferma, mostra le 7 dimensioni, attende OK umano
5. Avvia **SA3** via `Task(subagent_type: "sa3-financial-performance")` con brief + insight validati → `intermediate/sa3_financial_framework.md`
6. Avvia **SA4 Fase 1** via `Task(subagent_type: "sa4-pm-strategist")` (esegue `32_brand_strategy`) → `sa4_brand_strategy.md` + `tone_of_voice_campaign.md` → **🚦GATE 2**: attende OK umano. (opzionale `34_editorial_content_plan`)
7. Avvia **SA4 Fase 2** (stesso agente `sa4-pm-strategist`, Campaign Architecture) → `intermediate/sa4_strategy.md` (con ICE prioritization + experiment list)
8. Avvia **SA5** via `Task(subagent_type: "sa5-creative-concepts")` con output SA4
9. Avvia **SA7** via `Task(subagent_type: "sa7-ad-copywriter")` con output SA4 + SA5 (sequenziale dopo SA5 — il copy segue i concept)
10. Avvia **SA6** via `Task(subagent_type: "sa6-asset-production")` con output SA5 + SA7
11. Consolida tutto in `output/{brand}_{campaign}_{date}/final/`

> **Nota invocazione:** ogni SA gira via **Task tool** in contesto isolato — legge i suoi input dai file `intermediate/*.md` e ci scrive l'output (handoff su disco, non via contesto condiviso). I 🚦GATE (1 insight, 2 strategia) restano qui sull'orchestrator, **fra** una Task e l'altra: i subagent non si fermano da soli per la validazione umana. SA8 (`sa8-analytics-reporting`) e SA9 (`sa9-crm-lifecycle`) si invocano on-demand, fuori da questa sequenza.

Per routing skill → sub-agent: leggi `directives/skill_orchestrator.md`.

---

## Struttura Progetto

```
/
├── claude.md                        ← questo file (orchestrator)
├── ROADMAP.md                       ← task e stato setup
│
├── .claude/agents/                  ← sub-agent nativi (frontmatter name/description + SOP ruolo/input/output/tool), invocabili via Task
│
├── context/
│   ├── brand/                       ← brand context (agnostico, si sostituisce per ogni brand)
│   │   ├── business_profile.md      ← chi è il brand, modello business, target clienti (unifica about + business_strategy)
│   │   ├── tone_of_voice.md          ← voce+stile brand (unico file, ex writing_style fuso qui)
│   │   ├── anti_ai_writing_style.md  ← regole anti-AI agnostiche
│   │   ├── brand_kit.md / design_system.md
│   │   ├── preferences.md
│   │   └── financials/              ← dati finanziari brand (margin %, LTV, AOV storico, MER storico, NCAC) → SA3
│   ├── campaign/                    ← brief e vincoli della campagna corrente (solo quando si lancia una campagna specifica)
│   │   ├── brief.md                 ← COMPILARE solo per campagne specifiche (non obbligatorio per ricerca/strategia standalone)
│   │   └── constraints.md
│   └── references/
│       ├── ads/                     ← esempio ads competitor o reference
│       ├── copy/                    ← reference copy
│       └── landing-pages/           ← reference landing page + cro_principles.md (principi CRO usati da 29_landing_page)
│
├── directives/
│   ├── skill_orchestrator.md        ← routing: quando usare quale skill
│   └── skills/                      ← tutte le skill disponibili
│
├── execution/                       ← REFERENCE/tooling agnostico (non cambia per brand)
│   ├── tools.md                     ← tool e MCP disponibili
│   ├── calculators/                 ← 10 calculators Learnn (CSV + screenshots/) — TEMPLATE/reference SA3
│   ├── strategy-method/             ← metodo Learnn + SOP (reference layer strategia)
│   ├── scripts/
│   ├── workflows/                   ← n8n workflow JSON
│   └── prompts/
│
└── output/                          ← OUTPUT per-brand (dati reali, generati dalla pipeline)
    ├── dashboard/competitor-ads/    ← dashboard competitor (Airbnb style), alimentata da data.json di 19_ad_spy
    ├── reports/                     ← output SA8 (analytics + reporting — indipendente da campagne)
    │   └── {YYYY-MM-DD}_{weekly|monthly|quarterly|annual}/
    │       ├── google_ads_report.md
    │       ├── meta_ads_report.md
    │       └── executive_summary.md
    └── {brand}_{campaign}_{date}/   ← working dir campagna (apri CC qui = pwd)
        ├── 01_VOC_Research/         ← /pm-dati-qualitativi (SA2)
        ├── 02_Brand_DNA/            ← /pm-brand-kit (pre-pipeline)
        ├── 03_Ad_Spy/              ← /pm-competitor-spy (SA1, static) + /pm-competitor-spy-video (SA1, video, sottocartella <slug>-video/)
        ├── 04_Static_Ads/          ← /pm-statiche (SA6)
        ├── 05_UGC_Prompts/         ← /pm-ugc-video (SA6)
        ├── 06_Ad_Copy/             ← /pm-meta-copy (SA7)
        ├── 07_Multiplied_Ads/      ← /pm-multiplier (SA6)
        ├── 08_Rebuilt_Competitor_Ads/ ← /pm-competitor-rebuild (SA5)
        ├── 09_Meta_Handoff/        ← /pm-handoff (post-SA6)
        ├── 10_Landing_Pages/       ← /pm-landing-page (post-SA7)
        ├── 11_Characters/          ← /pm-buyer-persona (SA5)
        ├── 12_Email/               ← /pm-email-copy (SA9)
        ├── 14_Creative_Briefs/     ← /pm-ad-angles (SA5)
        ├── 15_Video_Scripts/       ← /pm-video-script (SA6)
        ├── _assets/product-shots/  ← /pm-product-photo (SA6)
        ├── intermediate/           ← output SA testuali per handoff (insight, strategy, copy deck)
        └── final/                  ← deliverable compilati pronti al lancio
```

> **Convenzione cartelle:** le skill scrivono nella cartella dove Claude Code è aperto (`pwd`).
> **Campagna specifica (pipeline completa):** crea `output/{brand}_{campaign}_{date}/` e apri Claude Code in quella folder. Le sottocartelle numerate `01_*`-`15_*` vengono create lì dentro (13_Meta_Campaigns = `51_meta_build`; 14_Creative_Briefs = `53_ad_angles`; 15_Video_Scripts = `55_video_script`). **Skill standalone** (es. `/pm-google-audit`, `/pm-report`, `/pm-dati-qualitativi` isolato): non serve creare la folder campagna — gli output vanno nel path appropriato (`output/reports/` per SA8, o nella folder corrente). Nessun wrapper esterno: tutto rimane dentro `output/`.

---

## ⭐ Convenzione Output — DOVE finiscono gli output (REGOLA OBBLIGATORIA per ogni skill)

**Ogni output di ogni skill va salvato sotto `output/`, in modo ordinato e prevedibile.** Nessun output sparso altrove. Questa è la mappa autoritativa — ogni skill DEVE dichiarare il suo path di output e rispettare questa struttura:

```
output/
├── {brand}_{campaign}_{date}/            ← TUTTI gli output di una campagna
│   ├── 01_VOC_Research/                  ← 18_voc_research (/pm-dati-qualitativi)
│   ├── 02_Brand_DNA/                     ← 21_brand_dna (/pm-brand-kit)
│   ├── 03_Ad_Spy/ (+ data.json)          ← 19_ad_spy (/pm-competitor-spy) + 52_ad_spy_video (/pm-competitor-spy-video, sottocartella <slug>-video/)
│   ├── 04_Static_Ads/                    ← 24_static_ads (/pm-statiche)
│   ├── 05_UGC_Prompts/                   ← 25_ugc_prompt (/pm-ugc-video)
│   ├── 06_Ad_Copy/                       ← 28_meta_copy (/pm-meta-copy) + 54_headline_bank (/pm-headlines)
│   ├── 07_Multiplied_Ads/                ← 27_multiplier (/pm-multiplier)
│   ├── 08_Rebuilt_Competitor_Ads/        ← 23_competitor_rebuild (/pm-competitor-rebuild)
│   ├── 09_Meta_Handoff/                  ← 30_meta_handoff (/pm-handoff)
│   ├── 10_Landing_Pages/                 ← 29_landing_page (/pm-landing-page)
│   ├── 11_Characters/                    ← 22_character_creator (/pm-buyer-persona)
│   ├── 12_Email/                         ← 46_email_creation (/pm-email-copy)
│   ├── 13_Meta_Campaigns/                ← 51_meta_build (/pm-meta-build): plan.md + build-manifest.json + manifest.md per run
│   ├── 14_Creative_Briefs/ (+ .json)     ← 53_ad_angles (/pm-ad-angles): angle bank id-stabili (A01...)
│   ├── 15_Video_Scripts/                 ← 55_video_script (/pm-video-script)
│   ├── _assets/product-shots/            ← 26_product_shot (/pm-product-photo)
│   ├── intermediate/                     ← output TESTUALI dei SA (handoff fra agenti)
│   │   ├── insight.md                    ← 33_insight_synthesis (/pm-insight)
│   │   ├── sa9_crm_analysis.md           ← 43 · sa9_rfm_segments.md ← 44 · sa9_email_strategy.md ← 45 (SA9)
│   │   ├── sa1_competitor_landscape.md   ← SA1
│   │   ├── sa2_market_insights.md        ← SA2
│   │   ├── sa3_financial_framework.md    ← SA3 (numeri reali del brand)
│   │   ├── sa4_brand_strategy.md         ← 32_brand_strategy (/pm-brand-strategy)
│   │   ├── tone_of_voice_campaign.md     ← 32_brand_strategy
│   │   ├── sa4_strategy.md               ← SA4 Fase 2 (media plan campagne)
│   │   ├── sa5_creative_framework.md     ← SA5
│   │   ├── sa7_copy_deck.md              ← SA7
│   │   ├── editorial_plan.md             ← 34_editorial_content_plan (/pm-editorial)
│   │   └── content_calendar.md           ← 34_editorial_content_plan
│   └── final/                            ← deliverable compilati pronti al lancio
│       ├── media_plan.md / ad_copy.md / creative_framework.md / assets/
├── reports/{YYYY-MM-DD}_{tipo}/          ← SA8 (/pm-report) — indipendente da campagna
│                                          ├ {YYYY-MM-DD}_meta_analysis/ ← 50_meta_analyze (/pm-meta-analyze): quick-check-<stamp>.md o deep-diagnosis-<stamp>/
│                                          └ {YYYY-MM-DD}_meta_campaigns/ ← 51_meta_build standalone (se non in campaign dir)
└── dashboard/competitor-ads/             ← dashboard competitor (data.json da 19_ad_spy)
```

**Regole:**
1. Ogni skill **dichiara esplicitamente** il suo output path (relativo a `output/{brand}_{campaign}_{date}/`).
2. Output testuali fra SA → `intermediate/`. Asset visivi/HTML → sottocartelle numerate `NN_*/`. Deliverable finali → `final/`.
3. Report SA8 → `output/reports/`. Dashboard → `output/dashboard/`.
4. `execution/` è solo **reference/tooling agnostico** (calculators, metodo, workflow): NON ci finiscono output di campagna.
5. Naming campagna: `{brand}_{campaign}_{date}` (es. `acme_summer-launch_2026-06-01`).
6. **Script delle skill — convenzione co-locazione:** uno script (`.py`/`.sh`) usato da UNA skill vive **co-locato** in `directives/skills/<skill>/scripts/` (es. `25_ugc_prompt/scripts/`, `40_seo_audit/scripts/`). Così la cartella skill è l'unità portabile self-contained: copiandola arrivano SKILL.md + `references/` + `scripts/` insieme. `execution/scripts/` è riservato **solo** a script cross-skill o davvero agnostici (al brand e alla singola skill). Le skill risolvono il path script cercando verso l'alto `directives/skills/<skill>/scripts` dalla pwd.

---

## Prompt Library (reference/backup)

Quando una skill o un agente deve scrivere un prompt (immagini, video, copy, ricerca) e serve un punto di partenza collaudato, **consulta `execution/prompts/` come reference/backup** prima di inventare da zero. È una libreria opzionale ma raccomandata: le skill funzionano anche se vuota, con la libreria piena migliorano coerenza e qualità. Struttura in `execution/prompts/README.md`.

---

## MCP Disponibili

### Ads Platforms
| MCP | Status | Uso |
|-----|--------|-----|
| Meta Ads MCP (`mcp.facebook.com/ads`) | ✅ Disponibile in Claude Code (connector, prefix per-install `mcp__…__ads_*`) | SA1 (analisi competitor ads via `ads_library_search`), SA8 reporting + **`50_meta_analyze` diagnosi read-only live** (quick/deep, mai write). I write (`ads_create/update/activate/delete`) sono di **`51_meta_build`** (`/pm-meta-build`): tiered loading, tutto PAUSED, cerimonie di conferma |
| Google Ads MCP | ✅ Attivo | SA1 (analisi keyword), SA4 (targeting), SA8 (reporting) — MCC: 5524890329 Indie Growth MCC |

### Produzione Asset
| MCP | Status | Uso |
|-----|--------|-----|
| Canva MCP | ✅ Attivo | SA6 (asset statici + video) |
| Higgsfield MCP | ✅ Attivo | SA6 (immagini AI, video, product photo, marketing studio) |

### Research & Data
| MCP | Status | Uso |
|-----|--------|-----|
| SimilarWeb MCP | ✅ Attivo | SA1 (traffico competitor) |
| Lenny's Data MCP | ✅ Attivo | SA2 (benchmark, case study) |

### Operations
| MCP | Status | Uso |
|-----|--------|-----|
| Gmail MCP | ✅ Attivo | Delivery report a cliente |
| Google Drive MCP | ✅ Attivo | Storage asset e deliverable |
| Google Calendar MCP | ✅ Attivo | Scheduling sessioni |
| Slack MCP | ✅ Attivo | Notifiche team |
| n8n MCP | ✅ Attivo | Automazione workflow |
| Klaviyo MCP | ⚠️ Da configurare | SA9 (CRM/email): profili, segmenti, metriche, flow, draft campaign/template. Setup `/pm-setup-klaviyo` (`uvx klaviyo-mcp-server`, env `PRIVATE_API_KEY`). Snippet `.mcp.klaviyo.example.json` |

---

## Skills Disponibili

### Skills Custom (in `directives/skills/`)
- `01_landing_brief` — ✅ Landing page brief
- `02_headline_optimization` — ✅ Headline optimization
- `03_editing_selfcheck` — ✅ QA copy
- `04_references_tecniche_design` — ✅ Design patterns
- `05_frontend_design` — ✅ Frontend design
- `06_web_artifacts` — ✅ React/Tailwind components
- `07_vercel_guidelines` — ✅ QA produzione
- `08_grill_me` — ✅ Requirements gathering
- `09_marketing_psychology` — ✅ 70+ mental models
- `10_advanced_copywriting` — ✅ Advanced copy framework
- `11_copywriting_ads_meta` — ✅ Meta Ads copy (primary text, headline, description per funnel stage)
- `12_copywriting_ads_google` — ✅ Google RSA copy (15 headline + 4 description)
- `13_creative_concepts` — ✅ Framework concept evidence-driven (SA5): 4 mappe (brand pattern/customer truth/sea-of-sameness/white space), 3-5 concept evolutivi-non-clone, 8 hard constraints + 🚦gate umano + QA gate 6 check, routing produzione
- `14_asset_production` — ✅ Router produzione (SA6): decide statica/video/product e instrada a 24/25/26/27
- `15_google_ads_analytics` — ✅ Report performance Google Ads — query GAQL + template report (SA8)
- `16_meta_ads_analytics` — ✅ Report performance Meta Ads — metriche, creative fatigue, template report (SA8)
- `17_financial_performance` — ✅ KPI framework: MER, ROAS, CPA, NCAC, Acquisition MER, budget split, red flag finanziari (SA3)
- `18_voc_research` — ✅ VOC Research — linguaggio verbatim clienti, 2 fasi: ricerca web + HTML (SA2)
- `19_ad_spy` — ✅ Ad Spy 2.0 — swipe file competitor Meta, brand-locked, solo static, **Apify REST diretto (no MCP)**. **Reverse-engineering a tempo di scrape**: ogni creative unica (qualsiasi tier, ≤40/brand) diventa un prompt di ricreazione via `_shared/format_teardown_recreation.md` (non un riassunto — incollato senza reference image rigenera essenzialmente lo stesso ad), bancato in `_scratch/format-*.json`, bottone 📐 su ogni card, consumato direttamente da `24_static_ads` come reference bank. (SA1)
- `20_ugc_scraper` — ✅ UGC Scraper 2.0 — 25 transcript TikTok virali, vetting LLM rilevanza (SA1)
- `21_brand_dna` — ✅ Brand DNA Playwright 3.0 — colori live CSS + web search, HTML (Pre-pipeline)
- `22_character_creator` — ✅ Character Creator — 1-10 personaggi headshot+fullbody 3:4, GPT Image 2 (SA5)
- `23_competitor_rebuild` — ✅ Competitor Ad Rebuild — ingegneria inversa + prompt rebuild + variazioni persona (SA5)
- `24_static_ads` — ✅ Static Ads da winner reali — rebrand model (SA6): niente template, ogni ad è il REBRAND di un ad vincente reale dalla reference bank (`19_ad_spy` + winner live del brand), design tenuto intero, solo identità scambiata (parole/marchi/prodotto/colori/numeri) via `_shared/format_teardown_recreation.md` + `_shared/adjacency_kill_pass.md`, deliverable = un blocco prosa per ad (mai zone/scaffold). Reference ads obbligatorie (hard gate). Batch plan approvato dall'utente prima di scrivere. Angoli da `53_ad_angles` o motore interno. Synthesis solo overflow approvato. Ratio segue la fonte, GPT Image 2 default, percorsi A/B/C/D
- `25_ugc_prompt` — ✅ UGC Factory (Seedance 2.0, Andromeda) — da hook+script a **4 ad MP4 montati** (25-45s): 4 hook unici + b-roll ladder 0/1/2/2 ends-on-CTA, gen <10s, pacing 3.5wps + assembly via script python/bash, 2 🚦gate (transcript+costo), 4 path A/B/C/D, no TikTok scraping (SA6)
- `26_product_shot` — ✅ Product Shot — Studio/Held/Worn, loop variazioni post-v1 (SA6)
- `27_multiplier` — ✅ Winning Ad Multiplier 2.0 — 5-8 variazioni Andromeda-compliant (SA6)
- `28_meta_copy` — ✅ Meta Ad Copy — 5 headline + 5 description + 2 primary text, analisi VOC approfondita (SA7)
- `29_landing_page` — ✅ Landing Page HTML — Tailwind + VOC injection + 34 anti-AI slop audit (Post-SA7)
- `30_meta_handoff` — ⚠️ DEPRECATA — Meta Ads Handoff (prompt da incollare in claude.ai web, 2 modalità). Superata da `50_meta_analyze` (analisi) + `51_meta_build` (build): il Meta MCP gira ora direttamente in Claude Code, niente più handoff manuale. Mantenuta solo come fallback storico
- `31_reporting_template` — ✅ Template report SA8 — struttura fissa, KPI business-model-aware (eComm/SaaS/LeadGen), Insights + Action Points ICE + Next Steps, export HTML email → `/pm-report`
- `32_brand_strategy` — ✅ Brand Strategy (SA4 Fase 1): Value Proposition piramide Bain, USP, ToV+nemico, benefici, offer design (10+10+10), bonus, garanzie, trigger event — 🚦GATE 2 → `/pm-brand-strategy`
- `33_insight_synthesis` — ✅ Insight Synthesis: 7 dimensioni (Job, Alternative, Categoria, Key Segment, Pain, Desideri, Obiezioni) con fonte, ponte SA2→SA4 — 🚦GATE 1 → `/pm-insight`
- `34_editorial_content_plan` — ✅ Piano editoriale + content calendar, 5 awareness stage, content plan per funnel (post-SA4) → `/pm-editorial`
- `35_google_ads_search_term_qs` — ✅ Search Term & Keyword & Quality Score analyzer (SA8) → `/pm-search-term`
- `36_google_ads_audit` — ✅ Audit account Google da zero, 12 aree + roadmap ICE (SA8) → `/pm-google-audit`
- `37_google_ads_optimisations` — ✅ Checklist ottimizzazioni per tipo campagna (folder con CSV co-locati) (SA8) → `/pm-google-optimisations`
- `38_first_party_data_analysis` — ✅ Analisi dati first-party cliente: track quant (→SA3) + qual (→insight) (SA2) → `/pm-data-analysis`
- `39_marketing_ideas` — ✅ Libreria 139 idee di marketing per categoria + matrice effort/impact, trigger proattivi (SA4 — ispirazione strategica). Tradotta IT. (invocabile via skill globale `marketing-ideas` o leggendo la skill)
- `40_seo_audit` — ✅ Audit SEO tecnico + on-page + content quality, framework 5 priorità, script `seo_checker.py` (SA8 — area organica). Tradotta IT. → `/pm-seo-audit`
- `41_seo_content_optimizer` — ✅ Ottimizzazione SEO di un singolo contenuto da URL: keyword research (9 tipi) + slug + heading + meta + alt + internal linking, preserva la voce autore (SA7/organico). Tradotta IT. → `/pm-seo-content`
- `42_carousel` — ✅ Layout component carousel/slider per landing page: accessibilità, performance, SEO (contenuto nel DOM) (SA6/Post-SA7). Tradotta IT. → `/pm-carousel`
- `43_crm_database_analysis` — ✅ Analisi database clienti (Shopify/CRM/email export): struttura, data quality, list health, baseline metriche, gap analysis (SA9). Prerequisito RFM → `/pm-crm-analysis`
- `44_rfm_segmentation` — ✅ Segmentazione RFM (Recency/Frequency/Monetary) + lifecycle + churn risk: 11 segmenti con size/revenue/azione (SA9) → `/pm-rfm`
- `45_email_strategy` — ✅ Strategia email: calendario, frequenza, automazioni prioritarie ICE, KPI target, roadmap 90gg, business-model-aware (SA9) → `/pm-email-strategy`
- `46_email_creation` — ✅ Copy email/newsletter: 5 subject A/B + preview + body (hook→valore→proof→CTA) + CTA, anti-AI, per segmento, draft Gmail MCP (SA9) → `/pm-email-copy`
- `47_competitor_review_mining` — ✅ Gap di mercato dal delta recensioni competitor positive vs negative (gap esecuzione/scoperto/trade-off polarizzante), Apify REST, alimenta insight+segmentazione (SA1/SA2→SA4) → `/pm-review-gap`
- `48_segment_pain_prioritization` — ✅ Segmentazione acquisition: pain matrix frequency×frustration vs alternative, matrice attributi×pain, segmenti per contesto+trigger, prioritizzazione 3 fattori (profittabilità/accesso/TAM) (SA4) → `/pm-segments`
- `49_anti_ai_slop` — ✅ Gate finale anti-AI per ogni copy esterno: forbidden words/patterns EN (delve/crucial/landscape/rule-of-three/em-dash/negative-parallelism…) + script CLI `words`/`dashes`/`replace`. Layer IT via `context/brand/anti_ai_writing_style.md`. Richiamata da tutte le skill copy (10,11,12,28,46,02,41,34,03,29). Importata da github.com/walidboulanouar/anti-ai-slop → `/pm-de-ai`
- `50_meta_analyze` — ✅ Meta Ads diagnosi **read-only live** dentro Claude Code (Meta Ads MCP, suffix-resolved, mai write). 2 modalità: quick check (audit single-pass ~10-12 pull) o deep diagnosis (5 investigator paralleli su slice isolate + referee avversariale → diagnosi ranked con evidence-for/against, confidence, singola azione settimanale; 🚦 consent gate). 3 reference verbatim EN (operator guide 60 tool, frameworks, briefs). Output in `output/reports/{data}_meta_analysis/`. Sostituisce la modalità analisi di `30`. (SA8) → `/pm-meta-analyze`
- `51_meta_build` — ✅ Meta Ads **build/write** dentro Claude Code: UNICA superficie di write sull'account. Costruisce campagne complete (campaign+ad set+creative+ad) + ogni modifica a esistenti (pause/budget/targeting/audience/customer list/attivazione). Tutto **PAUSED**; tiered tool loading (create solo post-piano, activate solo in cerimonia); 🚦 Gate 1 piano + cerimonia attivazione bottom-up (un sì/livello, >500/gg = digita totale); gate special-ad-categories + DSA EU + fine print irreversibilità; validator subagent del piano; manifest before/after ogni write (resume/adopt-by-name). 3 reference verbatim EN (operator guide, build-chain-spec, validation-checklist). Output in `output/{brand}_{campaign}_{date}/13_Meta_Campaigns/` o `output/reports/{data}_meta_campaigns/`. Sostituisce la modalità build di `30`. (SA8/post-SA6) → `/pm-meta-build`
- `52_ad_spy_video` — ✅ Ad Spy Video — sorella video di `19_ad_spy` (quella copre solo static). Stesso brand-lock (Pages scraper + `pageAdLibrary.id`), scraping `media_type=all` + filtro post a video, download mp4, **trascrizione word-for-word via fal.ai Whisper** (`chunk_level: segment`, niente venv locale), frame ffmpeg (hook + contact sheet), teardown per video via agenti paralleli model sonnet (script timestampato, on-screen text, hook, beat sheet, scene-by-scene, CTA). Pura intelligence, mai genera ad. Output: `03_Ad_Spy/<slug>-video/video-teardown-*.html`. Prereq: Apify key + fal.ai key. (SA1) → `/pm-competitor-spy-video`
- `53_ad_angles` — ✅ Angle Finder evidence-driven, **a monte** di `13_creative_concepts`: angoli ad medium-neutral, gratis e solo testo, 2 modalità (SPREAD sugli stadi awareness / FOCUS su uno scelto), distinzione a 3 assi (dottrina diversificazione Meta), gate hard + look-alike pass + kill floor, id stabili `A01...` consumati da `13`/`54`/`55`. Reference condivise in `_shared/` (`angle_engine.md`, `awareness_tension_funnel.md`, `niche_offer_types.md`, `creative_claims_compliance.md`, `creative_kill_floor_review.md`). Output: `14_Creative_Briefs/angles-*.md`+`.json`. (SA5) → `/pm-ad-angles`
- `54_headline_bank` — ✅ Headline Bank, deliverable dedicato più profondo delle 5 headline di `28_meta_copy`: ~20 headline platform + 8 hook on-image + 6 first-line, framework-nominate (9 famiglie + 5 formule DR, `_shared/headline_frameworks.md`), char-discipline a due livelli (27 safe/40 hard), gate personal-attributes Meta, kill floor. 4 modalità input incl. angle bank `53`. Output: `06_Ad_Copy/headline-bank-*.md`. (SA7) → `/pm-headlines`
- `55_video_script` — ✅ Video Script Studio universale (qualsiasi formato/lunghezza), gratis e solo testo: matematica del budget parole deterministica, 12 framework video nominati (`_shared/script_frameworks.md`), 3 hook variant + kill floor, upgrade di pacing misurato da `52_ad_spy_video` quando disponibile. Non richiesto da `25_ugc_prompt` (che scrive già i propri script) — copre i formati che quella non produce (voiceover-only, dialogo, founder, VSL) o un deliverable-script rapido. Output: `15_Video_Scripts/script-*.md`. (SA6) → `/pm-video-script`

> **Reference condivise (`directives/skills/_shared/`):** motori riusati da più skill creative (53/54/55, e riusabili da 13/28 in futuro): `angle_engine.md`, `awareness_tension_funnel.md`, `niche_offer_types.md`, `headline_frameworks.md`, `script_frameworks.md`, `creative_claims_compliance.md`, `creative_kill_floor_review.md`. Non sono skill invocabili direttamente, solo reference caricate dalle skill che le citano.

> **Skill SEO/supporto (39-42):** importate da `kostja94/marketing-skills` + plugin esterni, tradotte in italiano (corpo IT, termini tecnici SEO in EN). Pacchetti come cartelle con `references/` e `scripts/`. La skill globale `google-search-console` è installata in `~/.claude/skills/` (alimenta `40_seo_audit`).

> **Layer strategia internalizzato** dal progetto Marketing Strategist (corso Learnn, metodo 4 fasi: dato→insight→strategia→esecuzione). Reference completa in `execution/strategy-method/`. `03_editing_selfcheck` potenziato dual-mode (personal Simone + brand-campagna voice-editor). Human-in-the-loop: GATE 1 insight, GATE 2 strategia.
> **Dashboard competitor ads:** `output/dashboard/competitor-ads/index.html` — single-file, **look&feel Airbnb**, filtri awareness (5 Schwartz) + funnel (TOF/MOF/BOF) + competitor + tier. Alimentata da `data.json` di `19_ad_spy`.
> **Dashboard performance:** `output/dashboard/performance/index.html` — single-file, look&feel Airbnb, KPI macro (MER/ROAS/NCAC business-model-aware) + sparkline + tabelle campagne Google/Meta + alert automatici. Alimentata da `data.json` generato dal workflow n8n `execution/workflows/performance_dashboard_n8n.json` (Shopify+Google+Meta). **Token-zero sui refresh** — SA8 legge `data.json` solo on-demand per i report. Dettaglio in `output/dashboard/performance/README.md`.

> **Nota:** le funzioni un tempo coperte da plugin esterni (ad spy static+video, UGC scraper, brand DNA, character, rebuild, static, ugc-prompt, product-shot, multiplier, copy, landing-page, meta-handoff, angle finder, headline bank, video script) sono **internalizzate** nelle skill native `18`-`30` + `52`-`55` (comandi `/pm-*`). Nessuna dipendenza da plugin di terzi: i servizi (Apify, Fal.ai, Playwright, Higgsfield) girano come **MCP propri** configurati in `.mcp.json` (vedi `.mcp.json.example`). Setup: `/pm-setup-apify`, `/pm-setup-fal-ai`, `/pm-setup-klaviyo`. `53`/`54`/`55` sono gratis e solo testo, nessuna key richiesta.

### Skills Claude Code (globali)
- `marketing-psychology` — attiva sempre per SA2, SA5, SA7
- `copywriting` — QA e supporto SA7
- `copy-editing` — QA finale copy
- `marketing-ideas` — ispirazione strategica SA4
- `higgsfield-generate` — generazione immagini/video AI (SA6)
- `higgsfield-product-photoshoot` — foto prodotto brand-quality (SA6)
- `higgsfield-marketplace-cards` — immagini listing marketplace (SA6)
- `higgsfield-soul-id` — Soul ID training per consistenza personaggio (SA6)

---

## Avvio Sessione

1. Compila `context/campaign/brief.md`
2. Verifica `context/brand/` sia aggiornato per il brand corretto
3. Crea la folder campagna: `output/{brand}_{campaign}_{date}/`
4. **Apri Claude Code nella folder campagna** (`output/{brand}_{campaign}_{date}/`) — gli output finiscono nelle sottocartelle numerate lì
5. Avvia: "Lancia pipeline performance marketing per [BRAND]"

> Il CLAUDE.md del progetto root viene caricato automaticamente da Claude Code anche quando apri una sottocartella — non serve copiarlo.

### Avvio SA8 (Analytics & Reporting — indipendente dalla pipeline)
1. Avvia: "Genera report [weekly|monthly|quarterly|annual] per [Google Ads|Meta Ads|entrambi]"
2. SA8 legge account da `context/brand/` e MCC da `.mcp.json`
3. Output in `output/reports/{data}_{tipo}/`

### Avvio SA9 (CRM / Retention / Lifecycle — indipendente dalla pipeline)
1. Fornisci l'export clienti (Shopify/CRM/email) in `context/campaign/data/` o `context/brand/financials/`
2. `/pm-crm-analysis` → `/pm-rfm` → 🚦 valida segmenti → `/pm-email-strategy` → `/pm-email-copy`
3. Output testuali in `intermediate/sa9_*.md`; copy email in `12_Email/`
4. SA9 alimenta SA3 (LTV reale), SA4 (split retention), SA8 (KPI email)

---

## Deliverable Finale

```
output/{brand}_{campaign}_{date}/
├── 01_VOC_Research/voc-*.html        ← asset/HTML nelle sottocartelle numerate
├── 03_Ad_Spy/adspy-*.html
├── 06_Ad_Copy/copy-*.html
├── ... (02, 04, 05, 07-11, _assets)
├── intermediate/                     ← output SA testuali
│   ├── sa1_competitor_landscape.md
│   ├── sa2_market_insights.md
│   ├── sa4_strategy.md
│   ├── sa5_creative_framework.md
│   └── sa7_copy_deck.md
└── final/                            ← deliverable compilati pronti al lancio
    ├── media_plan.md                 → strategia canali + budget allocation + KPI
    ├── ad_copy.md                    → copy Meta + Google pronti al lancio
    ├── creative_framework.md         → concept approvati + brief visivo
    └── assets/                       → file immagine/video con naming convention
```

Struttura dettagliata in `output/README.md`.

---

## Esecuzione Autonoma — `/goal`, `/schedule`, n8n, `/loop`

Quattro leve, non sovrapposte:

- **`/goal <condizione>`** — locale, in-sessione. Claude lavora a turni finché un evaluator verifica la condizione. **⚠️ Salta i GATE umani** → usare SOLO su task meccanici con end-state verificabile (batch produzione/QA), MAI sulla pipeline gated SA1→SA4. L'evaluator legge solo il transcript → la skill deve *stampare la prova*. Combina con auto mode per run non presidiati. Disponibile ora. Goal-recipe in ROADMAP Task 8A.
- **`/schedule`** — routine cloud Anthropic (cron/API/GitHub event). Richiede repo GitHub + Pro/Max/Team/Ent + Claude Code on the web. Ideale per **SA8 ricorrente** (report/audit). Bloccato finché il repo non è su GitHub (packaging). `google-ads`/`higgsfield` (MCP Python locali) non girano nel cloud senza bundling. Dettaglio ROADMAP Task 8B.
- **n8n** (`execution/workflows/performance_dashboard_n8n.json`) — movimento dati dashboard, **token-zero**. Shopify+Google+Meta → `data.json`.
- **`/loop`** — ripeti un prompt a intervallo dentro una sessione aperta (locale).

Regola: report/audit ricorrenti → routine (post-GitHub) · batch produzione locale → `/goal` · dati dashboard → n8n.
