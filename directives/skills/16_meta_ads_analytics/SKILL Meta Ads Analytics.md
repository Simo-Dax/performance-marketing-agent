---
name: meta-ads-analytics
description: >
  Pull performance data from Meta Ads (Facebook/Instagram) via Meta Ads MCP and generate structured reports
  (weekly, monthly, quarterly, annual). Use this skill whenever SA7 needs to query Meta Ads, build a
  performance report, analyze campaign results, spot creative fatigue, compare periods, or provide
  optimization recommendations for Meta Ads accounts.
  NOTE: Requires Meta Ads MCP configured with OAuth (mcp.facebook.com/ads). Until configured, work
  with manually exported data provided by the user.
---

# Meta Ads Analytics

Genera report di performance Meta Ads (Facebook + Instagram) usando il Meta Ads MCP. Produce output strutturati con metriche core, analisi creativa, audience insights e raccomandazioni azionabili.

---

## MCP Status

⚠️ **Meta Ads MCP richiede configurazione OAuth** (`mcp.facebook.com/ads`).
- Disponibile solo su claude.ai web (non Claude Code) per OAuth Meta
- Alternativa fino a configurazione: usa `/pm-handoff` per preparare il handoff prompt, o chiedi all'utente di fornire export CSV da Meta Ads Manager

---

## Metriche Chiave Meta Ads

| Metrica | Descrizione |
|---------|-------------|
| Reach | Persone uniche raggiunte |
| Impressions | Visualizzazioni totali (include frequenza) |
| Frequenza | Impressions / Reach — indicatore creative fatigue |
| CPM | Costo per 1.000 impression |
| CPC | Costo per click (link click) |
| CTR (link) | Link clicks / Impressions — esclude click su like/commenti |
| ROAS | Purchase value / Spesa |
| CPA | Spesa / Conversioni (purchase, lead, etc.) |
| Hook Rate | Video: % che guardano i primi 3 secondi |
| Hold Rate | Video: % che guardano il 25%, 50%, 75%, 100% |
| Conversion Rate | Acquisti / Click sul link |

---

## Struttura Campagne Meta (per analisi)

```
Account
└── Campagna (obiettivo: conversions, traffic, awareness, reach, etc.)
    └── Ad Set (audience, placement, budget, schedule)
        └── Ad (creative: immagine/video + copy + CTA)
```

Report deve analizzare ogni livello.

---

## Query API Meta Ads (per riferimento quando MCP disponibile)

### Campagne — performance periodo
```
GET /{account_id}/campaigns?
  fields=id,name,status,objective,
         insights.fields(spend,impressions,clicks,ctr,cpm,cpc,reach,frequency,
                         actions,action_values,roas,cost_per_action_type,
                         cost_per_unique_click,unique_clicks,unique_ctr)
  &time_range={"since":"{start_date}","until":"{end_date}"}
  &level=campaign
```

### Ad Set — performance + audience
```
GET /{account_id}/adsets?
  fields=id,name,status,targeting,daily_budget,lifetime_budget,
         insights.fields(spend,impressions,clicks,ctr,cpm,cpc,reach,frequency,
                         actions,action_values,cost_per_action_type,roas)
  &time_range={"since":"{start_date}","until":"{end_date}"}
```

### Ad — performance creativo
```
GET /{account_id}/ads?
  fields=id,name,status,creative{title,body,image_url,video_id},
         insights.fields(spend,impressions,clicks,ctr,cpm,cpc,reach,frequency,
                         actions,action_values,roas,
                         video_p25_watched_actions,video_p50_watched_actions,
                         video_p75_watched_actions,video_p100_watched_actions,
                         video_thruplay_watched_actions)
  &time_range={"since":"{start_date}","until":"{end_date}"}
```

---

## Creative Fatigue Detection

**Segnali di fatigue:**
- Frequenza > 3 in 7 giorni (cold audience)
- Frequenza > 5 in 7 giorni (warm/retargeting)
- CTR calo >20% WoW su stesso creative
- CPM aumento >30% WoW senza variazioni audience
- Hook Rate video < 25% (problema nei primi 3 secondi)
- Hold Rate 50% < 20% (contenuto non abbastanza coinvolgente)

**Azione consigliata:**
- Fatigue lieve: duplica ad set con nuova audience simile
- Fatigue severa: refresh creative — attiva SA4 + SA5 per nuovi asset

---

## Struttura Output Report

```markdown
# Meta Ads Performance Report — {tipo} — {periodo}
Account: {account_name} ({account_id})
Generato: {data_generazione}

## Executive Summary
- Spesa totale: {spesa} ({delta}%)
- Reach: {reach} persone
- Conversioni: {conv} ({delta}%)
- CPA: {cpa} ({delta}%)
- ROAS: {roas}x ({delta}%)
- Frequenza media: {freq}x (alert se > 3)

## Metriche Core
| Metrica | Periodo | Periodo precedente | Delta |
|---------|---------|-------------------|-------|
| Spesa | | | |
| Reach | | | |
| Impressions | | | |
| Frequenza | | | |
| CPM | | | |
| CPC | | | |
| CTR (link) | | | |
| Conversioni | | | |
| CPA | | | |
| ROAS | | | |

## Performance per Campagna
[tabella per campagna: spesa, reach, frequenza, conversioni, CPA, ROAS]

## Performance per Ad Set
[tabella top 5 + bottom 3 per ROAS]

## Creative Analysis
[tabella per ad: creative, spesa, CTR, frequenza, ROAS, hook rate se video]

### Top Creative (per ROAS)
1. ...
2. ...
3. ...

### Creative con Fatigue
[lista ad con frequenza > 3 o CTR decay > 20%]

## Audience Insights
- Segmenti top performer per CPA
- Overlap potenziale audience (se rilevabile)

## Anomalie Rilevate
[variazioni >20% su metriche chiave]

## Raccomandazioni
1. ...
2. ...
3. ...

## Prossime Azioni Creative (se fatigue rilevata)
- [ ] Brief nuovi creative per campagna X: attivare SA4 + SA5
- [ ] Refresh copy per ad set Y: attivare SA6
```

---

## Soglie di Alert

| Metrica | Soglia attenzione | Azione |
|---------|------------------|--------|
| ROAS | < 2x | Analisi cause + revisione audience |
| CPA | > 2x target | Review bid + audience |
| CTR link | < 1% (feed) / < 0.5% (stories) | Refresh creative |
| CPM | +30% WoW | Competitività aumentata o audience satura |
| Frequenza | > 3 (cold) / > 5 (warm) | Creative refresh urgente |
| Hook Rate | < 25% | Revisione primi 3 secondi video |
| Conversion Rate | < 1% | Review landing page (attiva `01_landing_brief`) |

---

## Note Operative

- **Pixel**: verificare che il Meta Pixel sia attivo e che stia tracciando correttamente le conversioni priority (Purchase, Lead, etc.) prima di fare analisi.
- **Attribution window**: default Meta = 7-day click + 1-day view. Specificare nel report quale window è usata.
- **Valuta**: gli account sub avranno valute diverse (EUR, AUD, USD). Normalizzare in EUR per confronti cross-account se necessario.
- **Lookalike vs Interest vs Retargeting**: distinguere nel report perché hanno benchmark CPA/ROAS molto diversi.
- **iOS 14+ impact**: modeled conversions per iOS; segnalare se il dato risulta sotto-rappresentato.

---

## Workflow SA7 quando Meta Ads MCP non è disponibile

1. Chiedi all'utente: "Puoi esportare i dati da Meta Ads Manager per il periodo {X}? Export in CSV da Ads Manager → Report → Customize Columns."
2. Carica il CSV come file nell'interfaccia Claude.
3. Analizza i dati del CSV con questo framework di metriche.
4. Genera il report in `output/reports/{data}/meta_ads_report.md`.
