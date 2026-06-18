# SA8 — Google Ads Audit (account analizzato da zero)

**Agente:** SA8 (Analytics & Reporting)
**Output:** `output/reports/{YYYY-MM-DD}_google-audit/google_ads_audit_{account}.md`
**Tool:** Google Ads MCP (GAQL). MCC `5524890329`.
**Quando:** onboarding nuovo account o audit periodico (mensile/trimestrale). Documento strutturato, completo, prioritizzato.

---

## Scopo
Audit completo di un account Google Ads analizzato da zero: cosa funziona, cosa è rotto, cosa manca, cosa ottimizzare — in un documento professionale consegnabile al cliente.

---

## Le 12 aree dell'audit (coprire tutte)

### 1. Struttura account
Campagne, ad group, naming convention, granularità. GAQL: `campaign`, `ad_group`. Red flag: ad group con troppe keyword, campagne mescolate brand/non-brand, naming caotico.

### 2. Conversion tracking
Conversion actions attive, dedup, valore conversione, primary vs secondary. GAQL: `conversion_action`. **Red flag critico**: nessuna conversione tracciata, doppio conteggio, conversioni "Enhanced" non attive.

### 3. Budget & bidding
Bid strategy per campagna, budget vs spend effettivo, lost IS (budget). GAQL: `campaign.bidding_strategy_type`, `metrics.search_budget_lost_impression_share`. Red flag: Maximize Conversions senza tCPA su account maturo, budget limited su campagne profittevoli.

### 4. Keyword & match type
Distribuzione match type, keyword duplicate, conflitti. Broad senza tCPA/tROAS = pericolo. GAQL: `keyword_view`.

### 5. Negative keywords
Liste negative presenti? Shared? Copertura sprechi. Red flag: nessuna negative list, sprechi evidenti nei search term.

### 6. Search terms & sprechi
(vedi `35_google_ads_search_term_qs`) — quota spend su term irrilevanti.

### 7. Ad copy & RSA
Numero RSA per ad group (min 2-3), Ad Strength, pin, asset. GAQL: `ad_group_ad`. Red flag: 1 sola RSA, Ad Strength "Poor", headline non pertinenti.

### 8. Assets / Extensions
Sitelink, callout, structured snippet, image, call, lead form. GAQL: `asset`, `campaign_asset`. Red flag: extension mancanti (lasciano CTR/spazio a terra).

### 9. Quality Score
Distribuzione QS, componenti deboli (vedi `35`).

### 10. Audiences & signals
Observation/targeting, remarketing list, customer match, PMax audience signals. Red flag: nessun remarketing, nessun customer list sync.

### 11. Performance Max
Asset group quality, brand exclusion, search themes, cannibalizzazione Search. Red flag: PMax che cannibalizza brand search, asset group unico generico.

### 12. Geo / Schedule / Device
Geo targeting (presence vs interest), ad schedule, device bid. Red flag: targeting "presence OR interest" (spreco), nessun ad schedule su account con pattern orari.

---

## Output — struttura documento audit

```markdown
# Google Ads Audit — {account} — {data}

## Executive Summary
- Salute account: 🟢/🟡/🔴 + voto /100
- 3 problemi più gravi (impatto € stimato)
- 3 opportunità più grandi

## Scorecard (12 aree)
| Area | Stato 🟢🟡🔴 | Findings chiave | Priorità |
|------|-------------|-----------------|----------|
[una riga per ognuna delle 12 aree]

## Findings dettagliati (per area)
[per ogni area: cosa ho trovato (con dati GAQL), perché è un problema, impatto, fix]

## Roadmap di ottimizzazione (ICE-scored)
| # | Azione | Area | Impact | Confidence | Ease | ICE | Owner | Quando |
[ordinata per ICE desc — cosa fare prima]

## Quick wins (questa settimana)
[3-5 azioni ad alto ICE eseguibili subito]
```

## Regole critiche
- **Tutto basato su dati GAQL reali** — ogni finding cita la metrica/query. Mai audit a sensazione.
- **Quantifica l'impatto** dove possibile (€ sprecati/mese, IS perso, conversioni mancate).
- **Prioritizza con ICE** — un audit senza priorità è una lista inutile.
- **Linguaggio cliente-ready** — passa da `03_editing_selfcheck` se il documento va al cliente.
- Costo in micros → € (÷ 1.000.000).
