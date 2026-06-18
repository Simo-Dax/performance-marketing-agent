---
name: financial-performance
description: >
  Build the financial performance framework for a paid advertising campaign.
  Use this skill whenever SA3a needs to calculate MER targets, ROAS targets per channel,
  CPA/CPL targets, NCAC (New Customer Acquisition Cost), Acquisition MER, budget splits,
  or New vs Returning Customer revenue targets. Also use when brief inputs are available
  and financial modeling must precede strategy definition.
---

# Financial Performance Framework

Questo documento è la skill di supporto per SA3a. Definisce le formule, le soglie, i benchmark e i template di calcolo per costruire il financial framework prima della strategia.

---

## KPI Glossario

| KPI | Formula | Uso |
|-----|---------|-----|
| **MER** (Marketing Efficiency Ratio) | Total Revenue / Total Ad Spend | Salute finanziaria top-level, indipendente dall'attribuzione |
| **Blended ROAS** | Revenue attribuita totale / Spesa totale | Proxy MER con attribuzione piattaforma — sempre inferiore al MER reale |
| **Channel ROAS** | Revenue attribuita canale / Spesa canale | Ottimizzazione relativa intra-canale, non assoluta |
| **CPA** (Cost Per Acquisition) | Ad Spend / Conversioni | Costo per singola conversione (acquisto, iscrizione, lead qualificato) |
| **CPL** (Cost Per Lead) | Ad Spend / Lead generati | Solo modelli lead generation |
| **NCAC** (New Customer Acquisition Cost) | Spesa acquisizione / New customers | Costo per portare un cliente nuovo — da confrontare con LTV |
| **Acquisition MER** | New Customer Revenue / Spesa acquisizione | MER depurato dalla revenue retention — misura vera efficienza acquisizione |
| **LTV:NCAC** | Customer LTV / NCAC | Ratio di sostenibilità: target minimo 3:1 |
| **Payback Period** | NCAC / (AOV * gross margin%) | Mesi per recuperare il costo di acquisizione |
| **Gross Margin %** | (Revenue - COGS) / Revenue * 100 | Margine lordo — limite superiore del CPA sostenibile |

---

## Formule Core

### MER Target
```
MER target = Revenue target mensile / Budget ad spend mensile
```
Esempio: revenue target €100.000, budget €20.000 → MER target = 5x

### CPA Max Sostenibile (senza LTV)
```
CPA max = AOV * Gross Margin % / 1
```
Con MER target:
```
CPA target = AOV / MER target
```
Esempio: AOV €80, MER target 4x → CPA target = €20

### NCAC Max (con payback period)
```
NCAC max = LTV * (payback period mesi / 12) * gross margin %
```
Esempio: LTV €240, payback 6 mesi, margin 50% → NCAC max = 240 * 0.5 * 0.5 = €60

### ROAS target per canale
```
ROAS target canale = (Revenue target * split canale %) / Budget canale
```
Esempio: revenue target €100k, Meta split 60% (€60k target), budget Meta €12k → ROAS Meta = 5x

### CPL da CPA (lead gen)
```
CPL target = CPA target * lead-to-sale conversion rate
```
Esempio: CPA target €30, lead-to-sale rate 20% → CPL max = €30 * 0.20 = €6

### Acquisition MER
```
Acquisition MER = (New Customer Revenue) / (Spesa campagne acquisizione)
```
New Customer Revenue = Total Revenue * new customer revenue %

---

## Benchmark di Settore (default — sovrascrivere con dati SA2)

### CPA / ROAS benchmark per verticale
| Verticale | ROAS medio Meta | ROAS medio Google | CPA medio | CPM Meta | CPC Google Search |
|-----------|----------------|------------------|-----------|----------|------------------|
| Fashion / Apparel | 2-3x | 3-5x | €15-30 | €8-15 | €0.50-1.50 |
| Health & Beauty | 2-4x | 3-6x | €20-40 | €10-18 | €0.80-2.00 |
| Food & Beverage | 2-3x | 2-4x | €25-50 | €8-12 | €0.60-1.50 |
| SaaS / Software | 3-6x | 4-8x | €30-80 | €12-20 | €2-10 |
| Lead Gen B2C | — | — | €5-25 CPL | €10-15 | €1-4 |
| Home & Lifestyle | 2-4x | 3-5x | €20-45 | €8-14 | €0.70-2.00 |
| Wellness / Fitness | 2-4x | 3-5x | €20-40 | €9-16 | €1-3 |

Fonte baseline: Lenny's Data MCP per benchmark aggiornati. Sovrascrivere sempre con dati reali da SA7 se disponibili.

### MER benchmark per fase business
| Fase | MER tipico | Note |
|------|-----------|------|
| Early stage (< 6 mesi) | 1.5-2.5x | Budget basso, ottimizzazione in corso |
| Growth stage | 3-5x | Volume + efficienza |
| Mature / Scale | 4-8x | Brand equity aiuta |
| Subscription | 1-3x | NCAC elevato accettabile per LTV |

---

## Regole Finanziarie da Rispettare

1. **CPA max assoluto** = AOV * gross margin % (sopra questo livello ogni vendita è in perdita)
2. **Budget minimo statisticamente significativo** = CPA target * 50 conversioni / mese (sotto questo livello l'algoritmo non ottimizza)
3. **NCAC non > 3x CPA target** (se NCAC è 3x CPA stai pagando troppo per clienti nuovi rispetto a ciò che valgono nel breve)
4. **MER blended non confondere con Channel ROAS**: il MER è sempre l'unica verità finanziaria
5. **Budget minimo per canale per far girare l'algoritmo**:
   - Meta Advantage+: min €20-30/giorno per campagna
   - Meta Manual: min €10-15/giorno per ad set
   - Google PMax: min €15-25/giorno per campagna
   - Google Search: min €5-10/giorno per gruppo di annunci
6. **Non ottimizzare sul Channel ROAS** se il MER è fuori target — il problema è strutturale, non di singola campagna

---

## Red Flag Finanziari

Segnala all'orchestrator e blocca la pipeline se:

| Condizione | Red Flag | Azione |
|-----------|----------|--------|
| Budget totale < CPA target * 30 | Budget insufficiente per dati statistici | Aumenta budget o allunga periodo |
| MER target > 10x | Target irrealistico per la maggior parte dei brand | Rivedere obiettivi con cliente |
| NCAC target < CPL target | Impossibile: costo acquisizione < costo lead | Errore nel brief |
| Gross margin < 30% | Margini compressi — poco spazio per CPA | Rivedere pricing o scala solo su brand |
| LTV non definita ma payback > 6 mesi | Rischio: se LTV è bassa, stai bruciando | Raccogliere dati LTV prima di procedere |

---

## Output Template Rapido

Per ogni campagna nel budget framework, SA3a deve specificare:

```
Campagna: [nome]
Canale: Meta / Google
Tipo: Advantage+ / Manual / Search / PMax / Shopping / Display
Obiettivo: Conversione / Lead / Traffico / Awareness / Reach
Budget mensile: €X
Budget giornaliero: €X
ROAS target: Xx
CPA target: €X
CPL target (se lead gen): €X
New vs Returning: Acquisizione / Retention / Misto
KPI primario: ROAS / CPA / CPL / CPM / Reach
KPI secondari: CTR / CVR / Frequenza / IS%
```
