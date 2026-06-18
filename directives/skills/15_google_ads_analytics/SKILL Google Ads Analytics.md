---
name: google-ads-analytics
description: >
  Pull performance data from Google Ads via MCP and generate structured reports (weekly, monthly, quarterly, annual).
  Use this skill whenever SA7 needs to query Google Ads, build a performance report, analyze campaign results,
  spot anomalies, compare periods, or provide optimization recommendations for Google Ads accounts.
---

# Google Ads Analytics

Genera report di performance Google Ads usando GAQL via Google Ads MCP. Produce output strutturati con metriche core, analisi periodo su periodo e raccomandazioni azionabili.

---

## MCP Tools

- `mcp__google-ads__list_accessible_customers` — lista account accessibili dall'MCC
- `mcp__google-ads__search` — esegue query GAQL

**MCC default**: `5524890329` (Indie Growth MCC)

---

## Query GAQL Standard

### Performance campagna (periodo custom)
```gaql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.conversions_value,
  metrics.roas
FROM campaign
WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

### Performance ad group
```gaql
SELECT
  campaign.name,
  ad_group.id,
  ad_group.name,
  ad_group.status,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM ad_group
WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND ad_group.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

### Performance keyword + Quality Score
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr
FROM keyword_view
WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND ad_group_criterion.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

### RSA performance (responsive search ads)
```gaql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_ad.ad.id,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  ad_group_ad.ad_strength
FROM ad_group_ad
WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND ad_group_ad.status != 'REMOVED'
  AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
ORDER BY metrics.clicks DESC
LIMIT 50
```

### Impression share + competitività
```gaql
SELECT
  campaign.name,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_absolute_top_impression_share,
  metrics.search_top_impression_share,
  metrics.cost_micros,
  metrics.clicks,
  metrics.conversions
FROM campaign
WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND campaign.advertising_channel_type = 'SEARCH'
  AND campaign.status != 'REMOVED'
ORDER BY metrics.search_impression_share ASC
```

### Conversioni per tipo
```gaql
SELECT
  conversion_action.name,
  conversion_action.category,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion,
  metrics.all_conversions
FROM conversion_action
WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY metrics.conversions DESC
```

---

## Date Ranges

Sostituire `{start_date}` e `{end_date}` con formato `YYYY-MM-DD`.

| Tipo report | Start | End |
|-------------|-------|-----|
| Weekly (ultima settimana) | LAST_7_DAYS | — |
| Monthly (mese scorso) | primo giorno mese precedente | ultimo giorno mese precedente |
| Quarterly | primo giorno Q precedente | ultimo giorno Q precedente |
| Annual | `{anno}-01-01` | `{anno}-12-31` |

Per range relativi GAQL: `DURING LAST_7_DAYS`, `DURING LAST_30_DAYS`, `DURING LAST_MONTH` sono scorciatoie valide.

---

## Struttura Output Report

```markdown
# Google Ads Performance Report — {tipo} — {periodo}
Account: {account_name} ({customer_id})
Generato: {data_generazione}

## Executive Summary
- Spesa totale: {costo} ({delta_WoW/MoM/QoQ}%)
- Conversioni: {conv} ({delta}%)
- CPA medio: {cpa} ({delta}%)
- ROAS medio: {roas}x ({delta}%)

## Metriche Core
| Metrica | Periodo | Periodo precedente | Delta |
|---------|---------|-------------------|-------|
| Spesa | ... | ... | ...% |
| Impression | ... | ... | ...% |
| Click | ... | ... | ...% |
| CTR | ...% | ...% | ... pp |
| CPC medio | ... | ... | ...% |
| Conversioni | ... | ... | ...% |
| CPA | ... | ... | ...% |
| ROAS | ...x | ...x | ...% |

## Performance per Campagna
[tabella da query campagna]

## Top Performer
- Top 3 per ROAS: ...
- Top 3 per volume conversioni: ...

## Underperformer (da ottimizzare)
- Bottom 3 per ROAS: ...
- Campagne con IS < 50%: ...

## Anomalie Rilevate
[variazioni >20% WoW su metriche chiave]

## Quality Score
[keyword con QS < 6 = da ottimizzare]

## Raccomandazioni
1. ...
2. ...
3. ...
```

---

## Soglie di Alert

| Metrica | Soglia attenzione | Azione |
|---------|------------------|--------|
| ROAS | < 2x | Segnala + analisi cause |
| CPA | > 2x target | Segnala + proposta bid reduction |
| CTR Search | < 3% | Review copy RSA |
| CTR Display | < 0.5% | Review creative |
| Impression Share | < 50% | Aumenta budget o migliora QS |
| Quality Score | < 6 | Review landing page + keyword relevance |
| CPC anomalia | +30% WoW | Segnala competitività aumentata |

---

## Note Operative

- `cost_micros` in GAQL = costo in micro-unità valuta. Dividere per 1.000.000 per avere il valore reale.
- `roas` in GAQL = `conversions_value / cost`. Moltiplicare per 100 se si vuole percentuale.
- Se il sub-account ha valuta non EUR: specificare nel report la valuta dell'account.
- Per account MCC: eseguire la query su ogni sub-account separatamente o usare `login-customer-id` nel header MCP.
