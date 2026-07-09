# Performance Marketing Team — Roadmap

Ultimo aggiornamento: 2026-06-02

---

## STATO ATTUALE — COMPLETATO

- [x] `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `~/.claude/settings.json`
- [x] `claude.md` — orchestrator agnostico, mappa struttura, tabella MCP + skills
- [x] `.claude/agents/` — file sub-agent nativi (sa1–sa9) con frontmatter + ruolo, input, output, tool, handoff
- [x] `context/brand/` — file brand: `business_profile.md` (unifica about + business_strategy), `tone_of_voice.md`, `anti_ai_writing_style.md`, `brand_kit.md`, `design_system.md`, `preferences.md`
- [x] `context/brand/financials/` — cartella dati finanziari brand con README (SA3)
- [x] `context/campaign/brief.md` — template brief (opzionale, solo campagne specifiche)
- [x] `context/campaign/constraints.md` — template vincoli campagna
- [x] `context/references/ads|copy|landing-pages` — organizzato; `cro_principles.md` in `landing-pages/`
- [x] `directives/skill_orchestrator.md` — routing skill → sub-agent + flusso + Gate 0 aggiornato
- [x] `directives/skills/` — 46 skill (01–46) complete
- [x] `.claude/agents/` — 9 sub-agent (sa1–sa9): sa9_crm_lifecycle.md aggiunto (CRM/retention/email)
- [x] `31_reporting_template` — creata: struttura report SA8, KPI business-model-aware (eComm/SaaS/LeadGen), macro+micro, ICE action points, export HTML email
- [x] `39_marketing_ideas` / `40_seo_audit` / `41_seo_content_optimizer` / `42_carousel` — importate da kostja94/marketing-skills + plugin, tradotte IT (cartelle con references/scripts)
- [x] `google-search-console` — skill globale installata in `~/.claude/skills/` (alimenta 40_seo_audit)
- [x] `execution/tools.md` + sottocartelle `scripts/|workflows/|prompts/|calculators/`
- [x] `execution/calculators/` — template struttura agnostici per SA3 (budget planning, CVO forecast, break-even) e SA4 (experiment framework, ICE prioritization) — blank, mai aggiornati
- [x] `output/README.md` — naming convention + struttura per campagna
- [x] MCP attivi: Canva, SimilarWeb, n8n, Gmail, Google Drive, Google Calendar, Slack, Lenny's Data
- [x] Higgsfield MCP — CLI + wrapper Python + configurato in `.mcp.json`
- [x] Google Ads MCP — ADC credentials, MCC 5524890329, 11 sub-account verificati
- [x] Apify + Fal AI key configurate
- [x] 17 command file `/pm-*` in `.claude/commands/`

---

## COMPLETATO IN QUESTA SESSIONE (2026-05-31)

### ✅ SA9 — Agente CRM / Retention / Lifecycle
Terzo pilastro (canale owned) costruito. Aggiunge CRM/retention/email a paid+organico.
- **Agent:** `.claude/agents/sa9_crm_lifecycle.md`
- **4 skill:** `43_crm_database_analysis` (analisi DB, list health, baseline) · `44_rfm_segmentation` (RFM + lifecycle + churn, 11 segmenti) · `45_email_strategy` (calendario + automazioni ICE + KPI, business-model-aware) · `46_email_creation` (copy email per segmento, anti-AI, draft Gmail MCP)
- **4 comandi:** `/pm-crm-analysis` → `/pm-rfm` → `/pm-email-strategy` → `/pm-email-copy`
- **Output:** `intermediate/sa9_*.md` + copy in `12_Email/`
- **Integrazioni:** → SA3 (LTV reale) · → SA4 (split acquisition/retention) · → SA8 (KPI email). Input da `38_first_party_data_analysis` + `33_insight_synthesis`.
- **MCP Klaviyo (basi pronte):** `/pm-setup-klaviyo` + snippet `.mcp.klaviyo.example.json` + `.gitignore` rinforzato (`.mcp.json`, `financials/`, `data.json` esclusi). Fonte CRM primaria quando configurata (fallback CSV). **TODO utente:** lanciare `/pm-setup-klaviyo` con la Private API Key (`pk_...`, scope nella skill). `uv` richiesto.

### ✅ Dashboard Performance — Live Data (n8n + HTML)
- **Dashboard:** `output/dashboard/performance/index.html` — single-file Airbnb, KPI macro business-model-aware + sparkline + tabelle Google/Meta + alert automatici. Legge `data.json`, fallback SAMPLE.
- **Schema:** `output/dashboard/performance/data.sample.json` (commentato)
- **n8n:** `execution/workflows/performance_dashboard_n8n.json` — Schedule → Shopify+Google+Meta (HTTP) → Code (calcola MER/ROAS/NCAC/split) → Write data.json. Importabile, credenziali da configurare.
- **README:** `output/dashboard/performance/README.md` — token-zero sui refresh; SA8 legge `data.json` on-demand per il report (`31_reporting_template`).
- **TODO utente:** configurare credenziali n8n (Shopify Admin API, Google Ads OAuth+dev-token, Meta Marketing API) + inserire i `*_target` da `context/brand/financials/` nel Code node.

---

## TASK APERTI — PRIORITÀ 1

### 1. Calculators finanziari — dati reali SA3

**Cosa**: fornire i dati reali del brand dentro `context/brand/financials/` perché SA3 abbia baseline numerica vera.

**Come**: compila `context/brand/financials/financials.md` con:
- AOV medio, gross margin %, COGS
- LTV (12 mesi + lifetime), repeat rate
- NCAC storico, payback period attuale
- MER storico (ultimi 3 mesi), ROAS per canale
- Budget mensile attuale, split Meta/Google

**Calcolatori Google Sheet (opzionale ma raccomandato):**
Fornisci in formato **CSV** (logica formule) + **1 screenshot** (layout visivo):
- Budget Planning → `context/brand/financials/calculators/budget_planning.csv`
- CVO Forecast → `context/brand/financials/calculators/cvo_forecast.csv`
- Break Even / Net Profit → `context/brand/financials/calculators/break_even.csv`
- KPI Overview → schema per SA8 dashboard performance
- Performance Tracker → schema per SA8 dashboard performance

> `execution/calculators/` mantiene i template blank agnostici (struttura output SA3/SA4).
> `context/brand/financials/calculators/` riceve i CSV reali con la tua logica specifica.

**Stato:** in attesa dei file dall'utente.

---

### 2. Dashboard Competitor Ads (esterna)

**Cosa**: dashboard HTML separata per vedere e filtrare le ads dei competitor da Meta Ad Library.
**Alimentata da**: `data.json` generato da `19_ad_spy` (`/pm-competitor-spy`)
**Path**: `output/dashboard/competitor-ads/index.html` (già nel piano)

**Funzionalità:**
- Filtri: awareness stage (5 Schwartz) + funnel (TOF/MOF/BOF) + competitor + tier
- Visualizzazione ad: immagine/video + copy + metriche stimate
- Export swipe file

**Stato:** da costruire — dopo dashboard performance (stesso pattern HTML+JSON).

---

## TASK APERTI — PRIORITÀ 2

### Meta Ads MCP
**Server ufficiale**: `mcp.facebook.com/ads`
**Cosa sblocca**: SA1 (analisi ads competitor), SA7 (lancio campagne), SA8 (reporting Meta live)
**Setup**:
1. Crea Meta App su developers.facebook.com
2. Abilita Marketing API
3. Genera Access Token con scope: `ads_management`, `ads_read`
4. Aggiungi in `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "meta-ads": {
      "url": "https://mcp.facebook.com/ads",
      "headers": { "Authorization": "Bearer {ACCESS_TOKEN}" }
    }
  }
}
```
**Note**: OAuth Meta non supportato in Claude Code — solo claude.ai web. Per SA8 Meta fino alla configurazione: usa export CSV da Ads Manager.
**Stato:** in attesa credenziali Meta.

### Packaging plugin/GitHub — Distribuzione a pagamento (STANDBY)

Obiettivo: versione templatizzabile, vendibile, auto-aggiornabile via plugin GitHub. Substack/Polar gestisce il pagamento → accesso automatico al repo privato. Disdetta → si perdono gli update (non l'ultima versione scaricata — limite intrinseco).

**Verità da tenere a mente:**
- L'abbonamento blocca gli *update*, non revoca ciò che hanno già scaricato.
- Le skill sono markdown in chiaro: non si offuscano. Il moat è il sistema + update + onboarding, non il segreto.
- Dipendenze esterne (MCP/API) = attrito setup per l'acquirente.

**Architettura plugin (1 repo = 1 marketplace = N plugin):**
```
pm-team-plugins/
├── .claude-plugin/marketplace.json   ← elenca full + 4 moduli
├── plugins/{pm-full,pm-crm,pm-paid,pm-strategy,pm-landing}/
├── INSTALL.md · LICENSE (proprietaria, vieta redistribuzione)
```
Install: `/plugin marketplace add user/pm-team-plugins` → `/plugin install pm-crm`.

**Paywall → accesso GitHub (dalla migliore):**
1. **Polar.sh** — tier con "GitHub repo access" nativo (invita/rimuove auto).
2. **Gumroad/Lemon Squeezy + GitHub Action** — webhook acquisto → API add collaborator.
3. **Substack + n8n → GitHub API** — tieni Substack se l'audience è lì (n8n già disponibile).

---

### ⭐ Task 4 — Pulizia dati personali / templatizzazione (PREREQUISITO di tutto)

Scrub di 9 file + path hardcoded.

**Segreti (già gitignored, aggiungi `.example`):**
- `.mcp.json` → crea `.mcp.json.example` con placeholder. Contiene **Google Ads dev token reale + MCC 5524890329** → se mai condiviso, **ruota il token**.
- Path `/Users/simonedassereto/...` in `.mcp.json` (google-ads project, higgsfield server) → templatizza con `${HOME}`/placeholder + istruzioni `/pm-setup`.

**Dati personali da templatizzare (blank template):**
- `context/brand/business_profile.md` → bio/Substack/email → template vuoto.
- `5524890329` (MCC) hardcoded in: `sa8`, `skill_orchestrator`, `35/36/37`, `15_google_ads_analytics`, `CLAUDE.md` → `<YOUR_MCC_ID>` + leggi da config.
- `sdassereto@gmail.com` + riferimenti Substack in skill/CLAUDE → scrub.
- `memory/` (`.claude/projects/.../memory/`) → personale, **non** spedire.
- `output/` → già gitignored.

**Procedura sicura:** branch `template` → scrub → `git filter-repo` per cancellare i segreti dalla *history* (non basta l'ultimo commit). Se mai stato git → parti pulito da zero.

---

### ⭐ Task 5 — I 4 sub-agenti (core condiviso + 4 bundle)

Ogni bundle = core + le sue skill.

**🔵 Core condiviso (in ogni plugin):** `context/brand/*` (template) · `09_marketing_psychology` · `03_editing_selfcheck` · `anti_ai_writing_style` · `08_grill_me` · `/pm-setup` · `/pm-feedback`

**🟢 pm-crm:** SA9 + `43-46` + `/pm-crm-analysis` `/pm-rfm` `/pm-email-strategy` `/pm-email-copy` + `/pm-setup-klaviyo` + `38_first_party_data_analysis`

**🔴 pm-paid:** SA1,SA3,SA5,SA6,SA7,SA8 + `17-30` (spy/voc/static/ugc/copy/multiplier/handoff/reporting) + `35-37` Google + dashboard performance + n8n workflow

**🟡 pm-strategy:** SA1,SA2,SA3,SA4 + `17_financial` `32_brand_strategy` `33_insight` `34_editorial` `13_creative_concepts` + calculators

**🟣 pm-landing:** `29_landing_page` `01_landing_brief` `05/06/07_frontend` `42_carousel` `21_brand_dna` `18_voc` + `cro_principles`

**Overlap (VOC, brand-dna, ecc.):** (a) duplica nei bundle che le usano, oppure (b) plugin `pm-base` come dipendenza. Per semplicità di vendita → **duplica** (ogni bundle autosufficiente).

---

### ⭐ Task 6 — Onboarding = make-or-break

5 servizi da configurare (Google Ads, Klaviyo, Apify, Fal, Higgsfield). Un `/pm-setup` eccellente + **video** + **lista account/costi** è il vero prodotto percepito. Senza onboarding fluido, il prodotto non si percepisce come tale.

---

### ✅ Task 7 — Dipendenze plugin esterno → RIMOSSE (Path B fatto)

Eliminata ogni dipendenza da plugin di terzi. **Zero riferimenti residui** nel sistema (skill/agenti/doc).
- **3 MCP propri aggiunti** a `.mcp.json`: `apify` (`@apify/actors-mcp-server`), `fal-ai` (`fal-ai-mcp-server`), `playwright` (`@playwright/mcp`). Più i preesistenti `google-ads`, `higgsfield`. Tutti via npx/uv, indipendenti.
- **Tool-name riscritti** nelle skill: `mcp__plugin_*` → `mcp__apify` / `mcp__fal-ai` / `mcp__playwright` / `mcp__higgsfield`.
- **Key migrate** in `~/.config/pm-agent/` (`apify.env`, `fal.env`) + in `.mcp.json` — non più dentro i pluginConfigs del plugin.
- **Comandi-plugin sostituiti** con i `/pm-*` nativi (setup-apify, brand-kit, handoff, ecc.).
- **install.sh del plugin cancellato** (era il loro bootstrap installer).
- **`.mcp.json.example`** consolidato (6 server, placeholder, `${HOME}`) per la distribuzione.
- **`.gitignore`** rinforzato: `.mcp.json`, `.claude/settings.local.json` (token+path personali), `financials/`, `data.json`, `.playwright-mcp/`.

**Resta da fare (acquirente):** configurare le proprie key via `/pm-setup-apify`, `/pm-setup-fal-ai`, `/pm-setup-klaviyo`. Playwright non richiede key.

---

### ⭐ Task 8 — Esecuzione autonoma: `/goal` (ora) + `/schedule` routine (post-GitHub)

Due leve di automazione di Claude Code, complementari a n8n.

**A) `/goal` — disponibile ORA, locale, in-sessione** (CLI ≥ v2.1.139, workspace trusted, hooks attivi).
Imposta una condizione di completamento → Claude lavora a turni finché un evaluator (Haiku) la verifica. **⚠️ Salta i GATE umani** → usare SOLO su task meccanici con end-state verificabile, MAI sulla pipeline gated SA1→SA4. Combina con **auto mode** per run batch non presidiati. L'evaluator giudica solo ciò che è nel transcript → la skill deve *stampare la prova*.

Goal-recipe da usare/testare (solo task senza gate umano):
- `/goal report SA8 Google+Meta generato con tutte le sezioni di 31_reporting_template, salvato in output/reports/` → `/pm-report`
- `/goal la landing page HTML passa il 34-point anti-AI audit con zero fail, audit stampato` → `29_landing_page`
- `/goal 6 email (welcome+abandoned+winback) scritte, ognuna passata da 03_editing_selfcheck` → `46_email_creation`
- `/goal ogni skill 01-46 ha frontmatter valido + output path dichiarato, grep stampato` → QA sistema
- (idea libreria: salvare le recipe collaudate in `execution/goal_recipes.md`)

**B) `/schedule` — routine cloud, dopo packaging GitHub.** Girano su cloud Anthropic, clonano un repo GitHub, usano connector/`.mcp.json` committato. Richiedono Pro/Max/Team/Enterprise + Claude Code on the web.
**Prerequisiti (vedi Task 4-7):** (1) repo su GitHub privato; (2) MCP cloud-friendly nel `.mcp.json` committato — `apify`/`fal-ai`/`playwright`/`klaviyo` via npx/uvx OK col setup script; **`google-ads` e `higgsfield` (server Python in `~/.claude/mcp-servers/`) NON girano nel cloud** senza bundlarli nel repo o esporli come connector claude.ai; (3) key come env del routine environment.
Routine candidate (output = report/PR):
- Report performance settimanale (`/pm-report`) — schedule lun 9:00
- Monitor search-term/QS Google daily (`/pm-search-term`)
- Audit Google mensile (`/pm-google-audit`)
- Refresh competitor spy settimanale (`/pm-competitor-spy`)
- RFM/CRM refresh mensile (`/pm-rfm`)

**Divisione del lavoro:** n8n = movimento dati dashboard (token-zero) · `/goal` = batch produzione/QA locali ora · routine `/schedule` = report/audit ricorrenti cloud dopo GitHub · `/loop` = polling a intervallo in sessione aperta.
**Stato:** `/goal` usabile da subito; routine bloccate finché il repo non è su GitHub (Task 4).

---

### ⚠️ SICUREZZA — Prima di pubblicare/condividere
- `.mcp.json` → Google Ads developer token reale + MCC → placeholder in `.example`, ruota il token se esposto
- Fal AI / Apify / Klaviyo key → mai committate (stanno in `~/.config/pm-agent/` + `.mcp.json` gitignored)
- Account Google Ads, email, MCC, nomi cliente → ripulire da CLAUDE.md/agenti/skill
- `.gitignore` copre già: `output/`, `data.json`, `context/brand/financials/`, `.mcp.json`, `.playwright-mcp/` ✓ (versiona `.mcp.*.example.json`)
- LICENSE proprietaria (non MIT) che vieta redistribuzione
- Opzionale: watermark per-acquirente (buyer ID in commento) per tracciare leak

---

## TASK APERTI — PRIORITÀ 3

### Test End-to-End Pipeline Creativa
**Prerequisiti**: brand context compilato + `context/brand/financials/financials.md` compilato + brief campagna specifico
**Steps**:
1. Compila `context/brand/business_profile.md` per brand reale
2. Compila `context/brand/financials/financials.md`
3. Compila `context/campaign/brief.md`
4. Crea `output/{brand}_{campaign}_{date}/` e apri Claude Code in quella folder
5. Lancia: "Esegui pipeline performance marketing per [BRAND]"
6. Valida gate: GATE 1 (insight SA1+SA2) → GATE 2 (brand strategy SA4)
7. Verifica output in `final/`

### Test SA8 Google Ads Report
**Prerequisiti**: account con dati (Google Ads MCP attivo)
**Steps**:
1. Lancia: "Genera report settimanale Google Ads per tutti gli account MCC"
2. Verifica output in `output/reports/{data}_weekly/`

---

## ORDINE ESECUZIONE CONSIGLIATO

```
Fatto (sessioni 2026-05-31 / 06-01):
✅ SA9 CRM/Lifecycle (agent + skill 43-46 + comandi)
✅ Dashboard Performance (HTML + schema + workflow n8n)
✅ Skill 39-42 (marketing-ideas, seo-audit, seo-content-optimizer, carousel) + /pm-seo-*, /pm-carousel
✅ Basi MCP Klaviyo (/pm-setup-klaviyo + .mcp.json.example)
✅ MCP propri apify/fal-ai/playwright; zero dipendenze da plugin esterni
✅ .gitignore rinforzato + .mcp.json.example consolidato

Subito (locale, nessun prerequisito):
1. Usa /goal per batch produzione/QA (vedi Task 8 — goal-recipe). Mai sui GATE.

Quando hai i dati / le credenziali:
2. Configura n8n: credenziali Shopify/Google/Meta nel workflow performance_dashboard → attiva
3. Compila context/brand/financials/financials.md (sblocca SA3) + *_target nel Code node n8n
4. Fornisci CSV calcolatori Google Sheet → context/brand/financials/calculators/
5. Fornisci export clienti → testa SA9 (/pm-crm-analysis → /pm-rfm → /pm-email-strategy → /pm-email-copy)

Packaging (sblocca le routine cloud):
6. Scrub/template (Task 4) → push repo GitHub privato → marketplace.json + 5 plugin (Task 5)
7. Routine /schedule per SA8 ricorrente (Task 8B) — dopo GitHub

Da costruire / setup pendenti:
8. Dashboard Competitor Ads esterna (stessa architettura HTML+JSON, dati da 19_ad_spy)
9. Meta Ads MCP (credenziali Meta richieste)

Test finali:
10. Test pipeline end-to-end con brand reale (valida GATE 1 + GATE 2)
11. Test SA8 report + dashboard performance con dati reali
12. Verifica i 3 nuovi MCP (apify/fal-ai/playwright) si connettano dopo restart
```

---

## FONTI / RIFERIMENTI

- Meta Ads MCP ufficiale: https://mcp.directory/blog/meta-ads-cli-mcp
- Google Ads MCP: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- Meta Ads Library: https://www.facebook.com/ads/library
- Google Ads Transparency Center: https://adstransparency.google.com
- Community Meta MCP: https://github.com/pipeboard-co/meta-ads-mcp
- Community Google Ads MCP: https://github.com/cohnen/mcp-google-ads
