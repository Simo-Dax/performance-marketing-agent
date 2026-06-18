# START HERE — Checklist setup da zero

Tutto ciò che una persona deve fare per usare il Performance Marketing Team da zero. Segui in ordine.

---

## 1. Prerequisiti macchina (una tantum)
- [ ] **Claude Code** installato (CLI / desktop / IDE)
- [ ] **Node 20+**, **Python 3.12+**, **uv**, **ffmpeg**, **gh CLI** (per Higgsfield/Google Ads MCP)
- [ ] **Playwright Chromium** (per `21_brand_dna`): `npx playwright install chromium`
- [ ] (rapido) lancia `/pm-setup` — verifica struttura, tool, MCP, key in un colpo

## 2. Context Brand (`context/brand/`) — compila per il TUO brand-cliente
Sostituisci i template con i dati reali del brand:
- [ ] `about.md` — chi è il brand, prodotto, mercato (⚠️ file da creare se manca)
- [ ] `business_strategy.md` — modello business (eComm/SaaS/LeadGen), obiettivi, LTV, target new customer %
- [ ] `tone_of_voice.md` — voce + stile del brand (template da compilare)
- [ ] `anti_ai_writing_style.md` — regole anti-AI (già pronto, agnostico, opzionale ritocco)
- [ ] `brand_kit.md` — colori, font, logo (se esistente)
- [ ] `design_system.md` — design system (se esistente)
- [ ] `cro_principles.md` — principi CRO (se esistente)
- [ ] `preferences.md` — preferenze operative

## 3. Brief campagna (`context/campaign/`)
- [ ] `brief.md` — **obbligatori per SA3**: budget mensile, revenue target, AOV, gross margin %. + obiettivi, prodotto, timing
- [ ] `constraints.md` — vincoli (compliance, parole vietate, geo)

## 4. API Key & MCP
- [ ] **Fal AI** → `/pm-setup-fal-ai` (generazione immagini/video: statiche, UGC, product, character)
- [ ] **Apify** → `/pm-setup-apify` (competitor spy + UGC scraper TikTok)
- [ ] **Higgsfield** (opzionale) → MCP già in `.mcp.json`; CLI: `higgsfield auth login` al primo uso
- [ ] **Google Ads MCP** → già in `.mcp.json` (MCC `5524890329`); per altri account aggiorna developer token + login customer id
- [ ] **Meta Ads** → funziona solo in claude.ai web (OAuth). In Claude Code usa `/pm-handoff`

## 5. Reference opzionali (migliorano la qualità)
- [ ] `execution/prompts/` — popola la prompt library (reference/backup)
- [ ] `execution/checklists/google_ads_optimisations.md` — la TUA checklist ottimizzazioni Google (per `/pm-google-optimisations`)
- [ ] `context/references/ads|copy|landing-pages/` — esempi di riferimento

## 6. Avvio
- [ ] Crea cartella campagna: `output/{brand}_{campaign}_{date}/`
- [ ] **Apri Claude Code in quella cartella** (gli output finiscono lì, nelle sottocartelle numerate)
- [ ] Lancia: *"Lancia pipeline performance marketing per [BRAND]"*

---

## Flusso pipeline (cosa succede)
```
SA1∥SA2 (research) → 🚦GATE 1 insight → SA3 financial
   → SA4 [brand strategy 🚦GATE 2 → campaign architecture]
   → SA5 concept → SA7 copy → SA6 produzione → final/
SA8 (reporting/audit) = binario separato, on-demand
```

## Minimo indispensabile per partire
Se hai poco: **`business_strategy.md` + `brief.md` (budget/AOV/margin) + Fal key + Apify key**. Il resto si arricchisce strada facendo. Brand DNA, VOC, ToV li puoi generare con le skill (`/pm-brand-kit`, `/pm-dati-qualitativi`, `/pm-brand-strategy`).
