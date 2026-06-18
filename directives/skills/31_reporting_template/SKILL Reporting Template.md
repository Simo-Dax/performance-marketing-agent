---
name: reporting-template
description: >
  Generate performance reports for paid advertising accounts (Google Ads, Meta Ads, or cross-channel).
  Use this skill whenever SA8 needs to produce a weekly, monthly, quarterly, or annual report.
  The template auto-adapts to business model (eCommerce / SaaS / LeadGen) and outputs a structured
  report with Executive Summary, Account Macro, Campaign Micro, Creative Performance, Insights + ICE Action Points, and Next Steps.
  Export format: Markdown (default) or single-file HTML email-ready.
---

# Reporting Template — SA8

Skill per SA8 (`/pm-report`). Genera report strutturati per Google Ads, Meta Ads, o cross-channel.

---

## Step 1 — Rilevamento contesto

Prima di scrivere il report, determina:

1. **Periodo**: weekly / monthly / quarterly / annual
2. **Canale**: Google Ads | Meta Ads | Cross-channel (entrambi + eventuali altri)
3. **Business model**: eCommerce | SaaS | LeadGen (leggi da `context/brand/business_profile.md`)
4. **Dati disponibili**: MCP live (Google Ads MCP attivo) | export CSV | entrambi

Se Meta Ads MCP non configurato → richiedi export CSV da Ads Manager prima di procedere.

---

## Step 2 — Struttura Report

Il report si divide in **macro** (account) e **micro** (campagna). Ogni sezione ha KPI diversi per business model.

---

### SEZIONE 0 — Header

```
# Report [Canale] — [Periodo] | [Brand]
Data generazione: YYYY-MM-DD
Periodo analizzato: YYYY-MM-DD → YYYY-MM-DD
Business model: [eCommerce | SaaS | LeadGen]
Generato da: SA8 Analytics & Reporting
```

---

### SEZIONE 1 — Executive Summary

3-5 bullet point. Massimo 2 righe ciascuno. Solo fatti + implicazione diretta.

Struttura bullet: `[Metrica] [valore] [vs periodo precedente] → [implicazione]`

Esempi:
- MER 4.2x (+0.6x MoM) → spend scalabile, mantenere allocazione attuale
- CPA Meta +34% → creative fatigue probabile su adset >14 giorni
- ROAS Google Search 5.8x, Performance Max 2.1x → riallocare budget da PMax a Search

**Tono**: diretto, zero fluff. L'umano legge questo per decidere se approfondire.

---

### SEZIONE 2 — Performance Macro (Account Level)

#### KPI per Business Model

**eCommerce**
| KPI | Valore | vs Periodo Prec. | Target | Status |
|-----|--------|-----------------|--------|--------|
| MER (Marketing Efficiency Ratio) | | Δ% | | 🟢/🟡/🔴 |
| Blended ROAS | | Δ% | | |
| Revenue totale attribuita | | Δ% | | |
| Ad Spend totale | | Δ% | | |
| ROAS per canale (Meta / Google) | | | | |
| CPA medio (acquisto) | | Δ% | | |
| NCAC (New Customer Acquisition Cost) | | Δ% | | |
| % New vs Returning customers | | | | |
| AOV medio | | Δ% | | |
| Impression share (Google) | | | | |

**SaaS**
| KPI | Valore | vs Periodo Prec. | Target | Status |
|-----|--------|-----------------|--------|--------|
| MER | | Δ% | | 🟢/🟡/🔴 |
| CPL (Cost per Lead) | | Δ% | | |
| CPA (trial / signup) | | Δ% | | |
| Lead volume | | Δ% | | |
| SQL conversion rate (se disponibile) | | | | |
| CAC (Customer Acquisition Cost) | | Δ% | | |
| LTV:CAC ratio | | | | |
| Ad Spend totale | | Δ% | | |
| Impression share (Google Search) | | | | |

**LeadGen**
| KPI | Valore | vs Periodo Prec. | Target | Status |
|-----|--------|-----------------|--------|--------|
| MER / ROI campagna | | Δ% | | 🟢/🟡/🔴 |
| CPL (Cost per Lead) | | Δ% | | |
| CPA (lead qualificato) | | Δ% | | |
| Lead volume totale | | Δ% | | |
| Lead quality score (se disponibile) | | | | |
| Conversion rate form | | Δ% | | |
| Ad Spend totale | | Δ% | | |
| Budget utilization % | | | | |

> **Legenda status**: 🟢 on target | 🟡 attenzione (±15% da target) | 🔴 fuori target (>15% da target)

---

### SEZIONE 3 — Performance Micro (Campaign Level)

Per ogni canale attivo, tabella campagna per campagna.

#### Google Ads — Campagne

| Campagna | Tipo | Spend | Conv. | CPA | ROAS | Impression Share | Status | Note |
|----------|------|-------|-------|-----|------|-----------------|--------|------|
| | Search | | | | | | 🟢/🟡/🔴 | |
| | PMax | | | | | | | |
| | Display | | | | | | | |

**Cosa guardare per tipo campagna:**
- **Search**: IS, Quality Score medio, top vs other impression %, search term anomalie
- **Performance Max**: asset group performance, audience signal match, search themes copertura
- **Display / YouTube**: view rate, completion rate, frequency (>4/week = saturation)

#### Meta Ads — Campagne

| Campagna | Obiettivo | Spend | Conv. | CPA | ROAS | CPM | CTR | Freq. | Status |
|----------|-----------|-------|-------|-----|------|-----|-----|-------|--------|
| | Conversions | | | | | | | | 🟢/🟡/🔴 |
| | TOF/Awareness | | | | | | | | |

**Soglie fatigue Meta:**
- Frequency >3 su campagne conversioni → probabile saturazione audience
- CTR calo >20% su adset attivi >14gg → creative fatigue
- CPM +30% MoM senza stagionalità → audience esaurita o asta competitiva

---

### SEZIONE 4 — Creative Performance

Solo top e bottom performer. Non elencare tutto.

#### Top 3 Creative (tutti i canali)

| ID/Nome | Canale | Formato | Spend | CPA | ROAS | CTR | Note |
|---------|--------|---------|-------|-----|------|-----|------|

#### Bottom 3 Creative (candidate a pause/refresh)

| ID/Nome | Canale | Formato | Spend | CPA | ROAS | Freq. | Motivo |
|---------|--------|---------|-------|-----|------|-------|--------|

**Segnali di fatigue obbligatori da rilevare:**
- Frequenza >3 (Meta)
- CTR <0.8% (Meta conversioni) | CTR <2% (Google Search)
- CPA deteriorato >25% vs baseline campagna
- ROAS <1.5x su adset >€500 spend

---

### SEZIONE 5 — Insights + Action Points (ICE)

Massimo 5 action point. Formato ICE (Impact/Confidence/Ease, ciascuno 1-5).

| # | Insight | Action | Impact | Confidence | Ease | ICE Score | Owner |
|---|---------|--------|--------|-----------|------|-----------|-------|
| 1 | | | /5 | /5 | /5 | = I×C×E | |
| 2 | | | | | | | |

**Ordina per ICE score decrescente.** Massimo 2 action point per canale.

Ogni insight deve avere:
- **Dato osservato** (cosa sta succedendo)
- **Ipotesi causa** (perché probabilmente)
- **Action proposta** (cosa fare)
- **KPI atteso** (come misuri il risultato)

---

### SEZIONE 6 — Next Steps

Checklist prioritizzata per la settimana/mese successivo.

```
IMMEDIATO (entro 48h):
- [ ] [azione urgente — es. pausa adset in fatigue]
- [ ] [azione urgente]

QUESTA SETTIMANA:
- [ ] [azione pianificata]
- [ ] [test da lanciare]

PROSSIMO PERIODO:
- [ ] [esperimento / budget review / creative refresh]
```

---

## Step 3 — Export

**Markdown (default):** salva in `output/reports/{YYYY-MM-DD}_{tipo}/`
- `google_ads_report.md` per Google
- `meta_ads_report.md` per Meta
- `executive_summary.md` per cross-channel o summary condivisa

**HTML email-ready (se richiesto):** genera single-file HTML con:
- Font: sistema (sans-serif stack)
- Colori status: verde #22c55e, giallo #eab308, rosso #ef4444
- Tabelle con border-collapse, header grigio scuro
- Section dividers chiari
- Footer con data generazione + "Generato da SA8 Performance Marketing Team"
- Inviabile via Gmail MCP (`mcp__claude_ai_Gmail__create_draft`)

---

## Regole editoriali report

1. **Zero fluff.** Ogni frase ha un dato o un'azione.
2. **Comparazione obbligatoria.** Ogni KPI va sempre affiancato al periodo precedente (Δ%).
3. **Target espliciti.** Se il target è nel brief o in `context/brand/financials/`, mostralo sempre.
4. **Status traffic-light.** 🟢/🟡/🔴 su ogni KPI principale — nessun numero senza giudizio.
5. **ICE reale.** Action point ordinati per priorità, non per canale.
6. **Lingua report**: uguale alla lingua del brief/brand (default italiano).

---

## Input richiesti

| Input | Fonte | Obbligatorio |
|-------|-------|-------------|
| Dati Google Ads | Google Ads MCP o export CSV | Sì (se canale attivo) |
| Dati Meta Ads | Meta Ads MCP o export CSV | Sì (se canale attivo) |
| Periodo analisi | Richiesta utente | Sì |
| Business model | `context/brand/business_profile.md` | Sì |
| Target KPI | `context/brand/financials/` o `context/campaign/brief.md` | Raccomandato |
| Benchmark settore | SA2 output o Lenny's Data MCP | Opzionale |

---

## Output

```
output/reports/{YYYY-MM-DD}_{weekly|monthly|quarterly|annual}/
├── google_ads_report.md       ← se canale Google attivo
├── meta_ads_report.md         ← se canale Meta attivo
└── executive_summary.md       ← sempre (cross-channel o single-channel summary)
```

Se export HTML richiesto: aggiunge `report.html` nella stessa folder.
