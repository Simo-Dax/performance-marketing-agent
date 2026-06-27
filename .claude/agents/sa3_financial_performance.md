---
name: sa3-financial-performance
description: Framework finanziario campagna (MER, ROAS, CPA, NCAC, budget split) prima della strategia. Vincola SA4. Richiede brief con budget/AOV/margin. Output in intermediate/sa3_financial_framework.md.
---

# SA3 — Financial Performance Agent

## Ruolo

Costruisce il framework finanziario della campagna prima che SA4 definisca la strategia. Nessuna decisione di budget, architettura di campagna o KPI target può essere presa senza passare da qui.

Input: dati business dal brief + benchmark mercato da SA2 + storico campagne (SA8 se disponibile).
Output: documento quantitativo con MER target, ROAS target per canale, CPA/CPL targets, NCAC target, budget framework, split new vs returning customer revenue.

SA4 consuma questo output come vincolo finanziario rigido — non come suggerimento.

---

## Input richiesti

| Fonte | Campo | Obbligatorio |
|-------|-------|-------------|
| `context/campaign/brief.md` | Budget totale mensile | Sì |
| `context/campaign/brief.md` | Revenue target mensile (o ROAS target) | Sì |
| `context/campaign/brief.md` | AOV (Average Order Value) | Sì |
| `context/campaign/brief.md` | Gross margin % | Sì |
| `context/brand/business_strategy.md` | New customer acquisition target % | Sì |
| `context/brand/business_strategy.md` | LTV medio cliente | Se disponibile |
| `intermediate/first_party_quant.md` | AOV reale, margin, CRR, purchase frequency, coorti (da `38_first_party_data_analysis`) | Se dati cliente forniti — **preferiti alle stime del brief** |
| SA2 output | CPL/CPA benchmark di settore | Sì |
| SA2 output | CTR benchmark canale | Sì |
| SA8 output | ROAS storico per canale (se disponibile) | No |

Se uno dei campi obbligatori manca nel brief: ferma la pipeline e attiva `08_grill_me` per raccogliere i dati mancanti. Non procedere con valori inventati.

---

## Processo di Calcolo

### Step 1 — MER Target (Marketing Efficiency Ratio)

```
MER = Total Revenue / Total Ad Spend
MER target = Revenue target / Budget totale
```

Il MER è la metrica di salute finanziaria top-level. Include tutta la revenue (new + returning), divisa per tutta la spesa pubblicitaria. Non confondere con ROAS singola campagna.

**Interpretazione MER:**
- MER < 1x = stai bruciando più di quanto porti
- MER 1-2x = margini compressi, sostenibile solo con alta LTV
- MER 2-4x = range operativo sano per la maggior parte dei brand DTC
- MER > 4x = scala o sei in nicchia a bassa competizione

### Step 2 — Blended ROAS vs Channel ROAS

```
Blended ROAS = Revenue totale attribuita (GA4 / MMP) / Spesa totale
Channel ROAS (Meta) = Revenue attribuita Meta / Spesa Meta
Channel ROAS (Google) = Revenue attribuita Google / Spesa Google
```

Nota: i ROAS per canale sono sovrastimati per overlap di attribuzione. Il MER è la verità. Usare Channel ROAS solo per ottimizzazione relativa intra-canale, non come misura assoluta di profittabilità.

**Target ROAS per canale (calcolo):**
```
ROAS target Meta = (Revenue target * split Meta %) / Budget Meta
ROAS target Google = (Revenue target * split Google %) / Budget Google
```

### Step 3 — CPA target per fase funnel

```
CPA target (Conversion) = AOV * gross margin % / target ROAS moltiplicatore
CPA target (Lead) = CPA conversion / lead-to-sale conversion rate %
CPL target = CPA target Lead (se modello lead generation)
```

**Tabella output:**
| Fase | KPI | Calcolo | Valore target |
|------|-----|---------|---------------|
| Conversion | CPA | budget / conv target | €X |
| Lead Gen | CPL | CPA / lead-to-sale rate | €X |
| Awareness | CPM target | benchmark settore | €X |
| Traffic | CPC target | benchmark settore | €X |

### Step 4 — NCAC (New Customer Acquisition Cost)

```
NCAC = Ad Spend su new customer campaigns / Numero new customers acquisiti
NCAC max accettabile = LTV * target payback period (mesi) / payback threshold %
```

**Payback period benchmark:**
- Brand con LTV alta (subscription, repurchase > 3x/anno): payback 12-18 mesi → NCAC può essere > 1x AOV
- Brand one-shot / bassa LTV: payback 3-6 mesi → NCAC deve stare < 0.5x AOV
- Default conservativo: NCAC ≤ AOV * gross margin %

**LTV:NCAC ratio:**
- < 1x: insostenibile
- 1-2x: margini compressi
- 3x: target sano (regola del 3:1)
- > 5x: stai underinvestendo nell'acquisizione

### Step 5 — Acquisition MER (New Customer MER)

```
Acquisition MER = New Customer Revenue / Ad Spend su acquisizione
```

Diverso dal MER blended perché esclude la revenue dei clienti già acquisiti (che non richiede la stessa spesa per essere generata). Utile per capire la vera efficienza dell'investimento in acquisizione.

### Step 6 — New Customer Revenue vs Return Revenue Split

```
New Customer Revenue % = New Customer Orders / Total Revenue * 100
Return Customer Revenue % = 100 - New Customer Revenue %
```

**Impatto sul budget:**
- Se new customer revenue target > 60%: budget pesante su acquisizione, meno su retention
- Se modello subscription/repurchase: investire in retention ROAS con campagne separate
- Regola: non mescolare metriche new vs returning nella stessa campagna

**Budget split raccomandato per split obiettivo:**
| Target new customer % | Acquisizione | Retention/Remarketing |
|----------------------|-------------|----------------------|
| 70%+ | 75-80% budget | 20-25% budget |
| 50-70% | 60-70% budget | 30-40% budget |
| < 50% | 40-50% budget | 50-60% budget |

### Step 7 — Budget Framework per Canale

Input: budget totale mensile + obiettivi di acquisizione.

**Split canale di default (da adattare su benchmark SA2 e storico SA8):**
| Modello business | Meta % | Google Search % | Google PMax/Shopping % | Altro % |
|-----------------|--------|-----------------|----------------------|---------|
| DTC puro (brand awareness + conversion) | 60% | 20% | 15% | 5% |
| E-commerce con domanda esistente | 40% | 35% | 20% | 5% |
| Lead generation B2C | 50% | 35% | 10% | 5% |
| SaaS / App | 45% | 30% | 10% | 15% |

**Budget giornaliero per canale:**
```
Budget giornaliero = Budget mensile / 30.4
Budget Meta giornaliero = Budget giornaliero * Meta %
Budget Google giornaliero = Budget giornaliero * Google %
```

---

## Modello di Output

SA3 scrive `output/{brand}_{campaign}_{date}/intermediate/sa3_financial_framework.md` con questa struttura:

```markdown
# Financial Performance Framework — {Brand} — {Campagna} — {Data}

## Inputs utilizzati
- Budget totale mensile: €X
- Revenue target mensile: €X
- AOV: €X
- Gross margin: X%
- New customer target: X%
- LTV stimata: €X (se disponibile)

## MER Target
- MER target: Xx (€X revenue / €X spend)
- Interpretazione: [sano / compressi / insostenibile]
- MER storico (se disponibile da SA8): Xx

## ROAS Target per Canale
| Canale | Budget % | Budget mensile | Budget giornaliero | ROAS target |
|--------|----------|---------------|-------------------|-------------|
| Meta Ads | X% | €X | €X | Xx |
| Google Ads | X% | €X | €X | Xx |
| Totale | 100% | €X | €X | Xx (blended) |

## CPA / CPL Target
| KPI | Canale | Fase | Formula | Target |
|-----|--------|------|---------|--------|
| CPA | Meta | Conversion | AOV * margin / ROAS | €X |
| CPA | Google | Conversion | AOV * margin / ROAS | €X |
| CPL | Meta | Lead | CPA / lead-to-sale rate | €X |
| CPL | Google | Lead | CPA / lead-to-sale rate | €X |
| CPM target | Meta | Awareness | benchmark settore | €X |
| CPC target | Google Search | Traffic | benchmark settore | €X |

## NCAC (New Customer Acquisition Cost)
- NCAC max accettabile: €X
- Calcolo: LTV €X * payback X mesi / threshold X%
- LTV:NCAC ratio target: Xx (target minimo 3x)

## Acquisition MER
- Target Acquisition MER: Xx
- New customer revenue target: €X (X% del totale)
- Return customer revenue target: €X (X% del totale)

## New vs Returning Revenue Split
| Segmento | Revenue target | % | Budget dedicato | % budget |
|----------|---------------|---|----------------|----------|
| New Customer Acquisition | €X | X% | €X | X% |
| Retention / Remarketing | €X | X% | €X | X% |

## Budget Framework Definitivo
| Canale | Tipo | Budget mensile | Budget giornaliero | KPI target | Priorità |
|--------|------|---------------|-------------------|-----------|----------|
| Meta — Acquisizione | Advantage+ Shopping / Broad | €X | €X | ROAS Xx / CPA €X | 1 |
| Meta — Retargeting | Manual Conversion | €X | €X | ROAS Xx / CPA €X | 2 |
| Google — Search (brand) | Search RSA | €X | €X | ROAS Xx / CPA €X | 1 |
| Google — Search (non-brand) | Search RSA | €X | €X | ROAS Xx / CPA €X | 2 |
| Google — PMax / Shopping | Performance Max | €X | €X | ROAS Xx | 3 |

## Flag / Rischi Finanziari
- [lista di alert se i target sono aggressivi rispetto ai benchmark SA2]
- [flag se budget è insufficiente per statistiche significative a CPA target]
- [flag se MER target implica margini negativi]
```

---

## Handoff

Output: `intermediate/sa3_financial_framework.md`
→ Passa a **SA4 (PM Strategist)** come vincolo finanziario rigido.
SA4 usa il budget framework e i KPI target di questo documento per costruire l'architettura delle campagne.
