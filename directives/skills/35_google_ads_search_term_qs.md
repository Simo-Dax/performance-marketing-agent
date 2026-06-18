# SA8 — Google Ads: Search Term & Keyword & Quality Score Analyzer

**Agente:** SA8 (Analytics & Reporting)
**Output:** `output/reports/{YYYY-MM-DD}_search-term-qs/google_search_term_qs_report.md`
**Tool:** Google Ads MCP (`mcp__google-ads__search` GAQL, `mcp__google-ads__list_accessible_customers`). MCC `5524890329`.
**Cadenza:** ricorrente (settimanale/bisettimanale) — report sempre aggiornato di come performa l'account e cosa tenere sotto controllo.

---

## Scopo
Tre analisi in un report:
1. **Search Term analysis** — dove va lo spend, sprechi, nuove opportunità keyword, candidati negative.
2. **Keyword performance** — top/bottom keyword, match type, copertura.
3. **Quality Score** — QS basso, componenti deboli, fix concreti.

---

## Step 1 — Periodo e account
Chiedi: periodo (default `LAST_30_DAYS`), account/i (default tutti i sub-account MCC). Per ogni customer, esegui le query sotto.

## Step 2 — Search Term analysis (GAQL)
```sql
SELECT search_term_view.search_term, segments.keyword.info.match_type,
       metrics.impressions, metrics.clicks, metrics.cost_micros,
       metrics.conversions, metrics.conversions_value, metrics.ctr
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```
Estrai:
- **Spreco** — search term con costo alto e **0 conversioni** (candidati negative keyword). Soglia: costo > 2× CPA target senza conv.
- **Nuove opportunità** — search term con conversioni MA non ancora keyword esplicita → aggiungere come keyword.
- **Intent mismatch** — term irrilevanti rispetto al business (brand confusion, off-topic).
- **N-gram analysis** — parole ricorrenti nei term che sprecano (per negative a tema).

## Step 3 — Keyword performance (GAQL)
```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
       metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions,
       metrics.conversions_value, metrics.average_cpc, metrics.ctr,
       metrics.search_impression_share
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```
Estrai: top 10 per conversioni/ROAS, bottom (alto spend basso ritorno → pausa/bid down), distribuzione match type, keyword con impression share basso (<60% → budget/bid limited).

## Step 4 — Quality Score (GAQL)
```sql
SELECT ad_group_criterion.keyword.text,
       ad_group_criterion.quality_info.quality_score,
       ad_group_criterion.quality_info.creative_quality_score,
       ad_group_criterion.quality_info.post_click_quality_score,
       ad_group_criterion.quality_info.search_predicted_ctr,
       metrics.impressions, metrics.cost_micros
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```
Per ogni keyword con **QS < 7** e spend significativo, diagnostica il componente debole:
- `search_predicted_ctr` BELOW_AVERAGE → ad copy poco rilevante / poca varietà RSA → brief a SA7
- `creative_quality_score` (Ad Relevance) BELOW_AVERAGE → keyword non nel copy/headline → aggiungere
- `post_click_quality_score` (Landing Page Exp) BELOW_AVERAGE → landing lenta/non pertinente → fix LP (29_landing_page)

## Step 5 — Report (struttura fissa, segue `31_reporting_template`)
```markdown
# Google Ads — Search Term & QS Report — {account} — {periodo}

## 1. Executive Summary
- 🟢/🟡/🔴 [3-5 bullet: spend sprecato, QS medio, opportunità top]

## 2. Search Term — Sprechi (candidati negative)
| Search term | Match | Costo | Conv | Azione |
(+ blocco negative keyword pronto da incollare)

## 3. Search Term — Nuove opportunità keyword
| Search term | Conv | ROAS | Match consigliato |

## 4. Keyword Performance
| Keyword | Match | Costo | Conv | ROAS | IS% | Azione |

## 5. Quality Score — keyword da fixare
| Keyword | QS | Componente debole | Fix | Owner |

## 6. Insights 💡 / Action Points 🎯 (ICE) / Next Steps ➡️
```

## Regole critiche
- **Solo numeri reali da GAQL.** Mai inventare metriche.
- **Costo in micros**: dividere per 1.000.000 per avere €.
- **Ogni raccomandazione azionabile** + owner + collegata a fase funnel.
- **Negative keyword**: fornisci sempre il blocco pronto da incollare (1 per riga, con match type consigliato).
- Handoff: QS basso lato copy → SA7; lato landing → `29_landing_page`; sprechi → applicare negative.
