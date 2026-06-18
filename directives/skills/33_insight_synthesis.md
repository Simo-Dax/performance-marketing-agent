# Insight Synthesis — 7 Dimensioni (+ Gate Umano)

**Fase:** ponte tra Research (SA1+SA2) e Strategy (SA4). Gira dopo SA1∥SA2, prima di SA3/SA4.
**Input:** `intermediate/sa1_competitor_landscape.md` + `intermediate/sa2_market_insights.md` + `01_VOC_Research/` + `context/brand/`
**Output:** `output/{brand}_{campaign}_{date}/intermediate/insight.md` (con sezione finale di validazione umana obbligatoria). Vedi Convenzione Output in `claude.md`.
**Origine:** internalizzato da `insight-synthesizer` del Marketing Strategist (metodo Learnn fase 2). Reference: `execution/strategy-method/`.

---

## Filosofia (non negoziabile)

Questo è il punto in cui il sistema rischia di produrre **plausibilità invece di verità**. L'AI accelera dato (fase 1) ed esecuzione (fase 4); il **giudizio su insight (fase 2) e strategia (fase 3) è umano**. Questa skill produce una **BOZZA** che l'umano valida prima che la pipeline prosegua verso strategia e budget.

→ Dopo l'output, **GATE 1**: l'orchestrator si ferma, mostra il riepilogo, chiede conferma. Non si procede senza OK esplicito.

---

## Cosa produce

Sintesi dei tre livelli di analisi (quantitativa, qualitativa, ricerca macro) nelle **7 dimensioni di insight strategico**, ognuna con la **fonte citata**.

I tre livelli nel nostro sistema:
- **Quantitativo** → `first_party_quant.md` (da `38_first_party_data_analysis`, dati reali cliente) + benchmark SA2 + storico SA8 + financial SA3
- **Qualitativo** → VOC (`18_voc_research`) + `first_party_qual.md` (da `38`, recensioni/ticket/survey propri) + ad spy (`19_ad_spy`) + UGC (`20_ugc_scraper`) + **gap recensioni competitor (`47_competitor_review_mining`)**
- **Macro** → ricerca di mercato SA2 + competitor landscape SA1
- **Pain & segmento** → **`48_segment_pain_prioritization`** (pain matrix frequency×frustration, matrice attributi×pain, segmenti per contesto+trigger, prioritizzazione) — alimenta dim 4 e 5

---

## Le 7 dimensioni (UNA ALLA VOLTA, in quest'ordine)

> **L'ordine è il metodo, non una formalità.** Si parte SEMPRE dal Job (dim 1): è il job che definisce chi sono le alternative, quali pain contano, quali desideri muovono l'acquisto. Saltare il job = costruire strategia su sabbia. Catena: **Job → Alternative → Pain non risolto dalle alternative → come lo soddisfiamo parlando ai desideri**.

```
## INSIGHT — 7 Dimensioni

### 1. Job to be done (SEMPRE PER PRIMO)
Funzionale E emotivo: non solo "cosa fa il prodotto" ma "che lavoro emotivo gli affida il cliente".
Il job viene prima di tutto: definisce il perimetro delle alternative e quali pain sono rilevanti.
[ancorato a JTBD + Forces of Progress di SA2]
Fonte: [quantitativa / qualitativa / macro]

### 2. Alternative
Soluzioni dirette e indirette, inclusi i fai-da-te. + overview competitor con gap sfruttabili (da SA1 white space + `47_competitor_review_mining`).
Per ogni alternativa: cosa risolve bene (table stakes) e cosa NON risolve (dove vive il pain non soddisfatto, dim 5).
Fonte: [...]

### 3. Categoria
Come è strutturata la categoria, sotto-segmenti.
Fonte: [...]

### 4. Key Segment (decisione critica)
Il segmento NON è una demografica: è **contesto + trigger** in cui un pain diventa azione (da `48_segment_pain_prioritization`).
Valuta early adopter (nicchia, alta propensione, alta profittabilità) vs target scalabile (volume), prioritizzando sui 3 fattori macro (fatturato/profittabilità, accesso, crescita/TAM).
Pesa profittabilità contro scalabilità. **Raccomanda un segmento prioritario motivando con contesto, trigger e i 3 fattori.**
Fonte: [`48` + ...]

### 5. Pain point del segmento prioritario (NON risolto dalle alternative)
Dai dolori VOC verbatim, scorati su frequency × frustration (da `48`) e **incrociati con dim 2**: il pain che conta è quello ad alta frequenza+frustrazione che le alternative NON risolvono (white space) o risolvono male (sweet spot). Un pain già ben coperto dai competitor è table stakes, non leva.
Fonte: [`48` + `47` + VOC ...]

### 6. Desideri (come soddisfiamo il pain)
Dai desideri VOC + Pull forces. Qui si costruisce il ponte: **per ogni pain prioritario (dim 5), come la nostra soluzione lo soddisfa parlando al desiderio sottostante** (non alla feature). È il seme della Value Proposition (`32`).
Fonte: [...]

### 7. Obiezioni
Dalle anxiety forces + recensioni negative (proprie e competitor da `47`).
Fonte: [...]
```

Ogni dimensione chiude con una **"logica strategica"** (non descrittiva): dove ci possiamo spostare a livello di posizionamento.

---

## Regole ferree

- Per OGNI insight indica la **fonte** (quantitativa / qualitativa / macro). Se non supportato dai dati → marcalo **"ipotesi da validare"**.
- **Vietato essere generico**: niente insight che varrebbero per qualsiasi brand. Se vale per chiunque, non è un insight.
- **Niente invenzioni.** Se i dati non bastano per una dimensione, dillo esplicitamente.
- Distingui sempre dato del brand da dato dei competitor.

---

## Output + GATE 1

Scrivi `intermediate/insight.md`. Termina SEMPRE con:

```
## ⚠️ DA VALIDARE DALL'UMANO

Le 3-5 decisioni più importanti e incerte che richiedono il tuo giudizio di mercato:
1. [es. Key Segment: early adopter X vs target scalabile Y — quale prioritizziamo?]
2. ...
```

Poi l'orchestrator mostra il riepilogo delle 7 dimensioni e chiede:
> "Confermi questi insight o vuoi correggere/scartare qualcosa prima di costruire la strategia?"

Applica le correzioni umane riscrivendo il file. **Procedi a SA3/SA4 solo dopo OK esplicito.**

---

## Handoff
`intermediate/insight.md` (validato) → **SA3** (i pain/segment informano i target finanziari) e **SA4 / `32_brand_strategy`** (la VP e l'offerta discendono da questi insight). Niente strategia senza insight validati.
