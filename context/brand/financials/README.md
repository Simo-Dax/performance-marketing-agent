# Financial Data — Brand Baseline

Metti qui i dati finanziari **reali del brand** per alimentare SA3 (`17_financial_performance`).

SA3 legge questa cartella **prima** di fare calcoli. Se vuota, usa solo i valori del brief (meno preciso).

---

## Cosa inserire

### `financials.md` — dati baseline brand
Crea questo file con i valori reali. Formato suggerito:

```markdown
# [Brand] — Financial Baseline

## Unit Economics
- AOV medio: €___
- Gross margin %: ___% 
- COGS medio per ordine: €___
- Shipping + fulfillment medio: €___

## Customer Metrics
- LTV (12 mesi): €___
- LTV (lifetime): €___
- Repeat purchase rate: ___%
- Average orders/customer/year: ___
- Churn rate mensile (SaaS): ___%

## Acquisition Benchmarks (storici)
- NCAC medio (ultimi 3 mesi): €___
- NCAC target: €___
- LTV:NCAC ratio attuale: ___:1
- Payback period attuale: ___ mesi

## Performance Storica
- MER medio (ultimi 3 mesi): ___x
- MER target: ___x
- ROAS Google Search (medio): ___x
- ROAS Meta (medio): ___x
- CPA medio (acquisto): €___
- CPA target: €___
- % new customers su revenue totale: ___%

## Budget & Split
- Budget mensile attuale: €___
- Split Meta / Google / altri: ___% / ___% / ___%
```

### `calculators/` (opzionale)
Quando fornisci i CSV dei calcolatori Google Sheet:
- Inseriscili qui come `calculator_[nome].csv`
- Aggiungi uno screenshot del layout come `calculator_[nome].png`
- SA3 li usa per replicare la tua logica di calcolo

---

## Come SA3 usa questi dati

1. Legge `financials.md` come baseline (valori storici reali)
2. Incrocia con `context/campaign/brief.md` (target campagna specifica)
3. Calcola: MER target, CPA max sostenibile, NCAC max, ROAS target per canale, budget split ottimale
4. Produce `intermediate/sa3_financial_framework.md` con il framework finanziario della campagna

> Nota: questa cartella contiene dati sensibili del cliente. Non versionare/pubblicare (vedi `.gitignore`).
