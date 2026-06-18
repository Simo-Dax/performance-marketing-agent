# Performance Dashboard — Live Data

Dashboard HTML single-file che aggrega **Shopify + Google Ads + Meta Ads** in una vista unica (macro account + micro campagna). Stesso pattern della competitor-ads dashboard: legge `data.json` client-side, **zero token Claude per ogni refresh**.

```
output/dashboard/performance/
├── index.html          ← dashboard (apri nel browser)
├── data.json           ← dati live (generato da n8n) — NON committare
└── data.sample.json    ← schema di riferimento + dati demo
```

---

## Architettura (token-free sui refresh)

```
n8n workflow (scheduled, autonomo)
  → Shopify API + Google Ads API + Meta Ads API
  → calcola MER / blended ROAS / NCAC / split
  → scrive output/dashboard/performance/data.json

index.html (statico)
  → fetch('data.json') client-side, fallback su SAMPLE incorporato
  → KPI card + sparkline + tabelle campagne + alert automatici
  → zero Claude, zero token

SA8 (Claude, on-demand)
  → legge data.json SOLO quando chiedi analisi/report
  → produce report con ICE action points (skill 31_reporting_template)
```

---

## Cosa mostra

**Macro (account):** card KPI adattate al `business_model` (eComm: MER, Blended ROAS, Revenue, Spend, NCAC, %New, AOV · SaaS: CAC, LTV:CAC, CPL · LeadGen: CPL, Lead, CPA). Ogni card ha delta vs periodo precedente + barra vs target.

**Trend:** sparkline revenue (area) vs spend (linea tratteggiata), dati giornalieri Shopify.

**Alert automatici** (client-side, niente AI): MER vs target, frequency Meta >3 (creative fatigue), ROAS <2 su spend alto.

**Micro (campagne):** tabella Google (per tipo: Search/PMax/Shopping + Impression Share) e tabella Meta (CPM, CTR, Frequency) con status traffic-light.

---

## Setup

### 1. Prima esecuzione (demo)
Apri `index.html` nel browser → parte coi dati `SAMPLE` incorporati (nessun `data.json` richiesto).

### 2. Collega n8n
1. Importa `execution/workflows/performance_dashboard_n8n.json` nella tua istanza n8n
2. Configura le credenziali: Shopify Admin API, Google Ads API, Meta Marketing API (vedi note nel workflow)
3. Imposta lo schedule (default: ogni mattina 06:00)
4. Il nodo finale scrive `data.json` in questa cartella (o via FTP/Drive/webhook secondo il tuo setup)

### 3. Refresh
n8n aggiorna `data.json` da solo. La dashboard mostra sempre l'ultimo dato al reload. Nessun intervento Claude.

---

## Schema dati

Vedi `data.sample.json` (commentato). Campi chiave:
- `business_model`: `"eCommerce"` | `"SaaS"` | `"LeadGen"` → cambia le card KPI
- `calculated.*` + `*_prev` (periodo precedente, per i delta) + `*_target` (da `context/brand/financials/`)
- `shopify.daily[]`: serie giornaliera per la sparkline
- `google_ads.campaigns[]` / `meta_ads.campaigns[]`: righe tabella, `status` ∈ `g|w|b`

---

## Note
- `data.json` contiene dati reali del cliente → **in `.gitignore`**, non pubblicare.
- Dashboard 100% offline-capable: nessuna dipendenza esterna a runtime (solo Google Fonts via CDN, degrada a system font).
- Per il report narrativo con insight e action point → SA8 `/pm-report` (legge questo `data.json`).
