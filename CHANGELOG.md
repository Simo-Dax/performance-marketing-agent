# CHANGELOG — Performance Marketing Team

Storia evolutiva del **sistema agentico** (non dei dati di campagna). Tiene traccia di skill aggiunte, cambi strutturali, decisioni architetturali.

> Ordine del sistema di "memoria":
> - **CHANGELOG.md** (questo) — evoluzione del sistema agentico
> - `directives/feedback_log.md` — feedback utente applicati (self-improvement)
> - `~/.claude/projects/.../memory/` — auto-memory cross-sessione (project/user/feedback/reference)
> - `ROADMAP.md` — task futuri

---

## 2026-05-31 (b)

### Google Ads (skill SA8)
- `35_google_ads_search_term_qs`, `36_google_ads_audit`, `37_google_ads_optimisations` (folder con checklist CSV per tipo campagna co-locate + Campaign Structure cheatsheet → anche SA4).
- Checklist ottimizzazioni dell'utente integrate in `37_google_ads_optimisations/`.

### First-party data analysis
- `38_first_party_data_analysis` (SA2): track quantitativo (→ SA3 baseline reale) + qualitativo (→ insight). Colma il gap "analyst" del metodo Learnn. Comando `/pm-data-analysis`. Dati cliente in `context/campaign/data/`.

### Pulizia struttura
- Comando `/pm-feedback` + self-improvement layer.
- Voce brand: `tone_of_voice.md` unico + `anti_ai_writing_style.md`; `writing_style.md` rimosso.
- Rimosso wrapper esterno dai path; Higgsfield MCP project-only.
- ROADMAP: packaging plugin/GitHub (standby) + reminder rimozione dati sensibili (Google Ads dev token in `.mcp.json`, Fal/Apify key).

## 2026-05-31

### Strategia & metodo
- Internalizzato il layer strategia dal progetto **Marketing Strategist** (metodo Learnn 4 fasi). Reference in `execution/strategy-method/`.
- `33_insight_synthesis` (7 dimensioni + GATE 1), `32_brand_strategy` (VP Bain/USP/ToV/offer + GATE 2), `34_editorial_content_plan`.
- **SA4 espanso a 2 fasi**: Brand Strategy → Campaign Architecture (+ sez. 11 ICE, sez. 12 experiment list).
- Filosofia human-in-the-loop: GATE 1 (insight), GATE 2 (strategia).

### Financial
- Integrati 10 calculators Learnn in `execution/calculators/` + `17_financial_performance/calculators_reference.md`.

### Reporting & Google Ads
- `31_reporting_template` (report SA8 fisso, business-model-aware).
- `35_google_ads_search_term_qs`, `36_google_ads_audit`, `37_google_ads_optimisations`.

### Dashboard
- `output/dashboard/competitor-ads/` — single-file, look&feel **Airbnb**, filtri awareness/funnel/competitor/tier. Alimentata da `19_ad_spy`.

### Self-improvement
- `directives/self_improvement.md` + `directives/feedback_log.md` + `/pm-feedback`. Auto-ottimizzazione a 3 livelli (procedurale/agentico/skill).

### Voce & contenuti brand
- `03_editing_selfcheck` reso agnostico (voice-editor brand-cliente).
- `context/brand/anti_ai_writing_style.md` (regole anti-AI agnostiche).
- Fusi `writing_style.md` + `tone_of_voice.md` → unico `tone_of_voice.md` (template per brand).

### Struttura & convenzioni
- **Rimosso il wrapper esterno** dai path output: le skill scrivono nelle sottocartelle numerate `01_*`-`11_*` direttamente sotto la cartella campagna.
- **Convenzione Output** autoritativa in `claude.md`: tutto sotto `output/`, `execution/` solo reference.
- Higgsfield MCP spostato da globale a project-only.
- Prompt library directive (`execution/prompts/`).

---

## 2026-05-30

- Internalizzate 13 skill produzione/research → native 18-30 (italiano), MCP propri (Apify/Fal/Playwright/Higgsfield).
- Create `13_creative_concepts`, `14_asset_production`.
- 17+ command `/pm-*` in `.claude/commands/`.
- Approfonditi SA1 (white-space) e SA2 (JTBD + Forces of Progress).

---

## Precedente (setup)
- 8 sub-agent SA1-SA8, orchestrator, skill 01-17, context/brand, MCP (Google Ads, Higgsfield, Apify, Fal, Playwright, Canva, SimilarWeb, Lenny's, Gmail, Drive, Calendar, Slack, n8n).
