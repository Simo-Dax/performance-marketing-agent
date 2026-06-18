---
name: rfm-segmentation
description: >
  Segment a customer database using RFM (Recency, Frequency, Monetary) plus lifecycle stage and churn risk.
  Use when the user wants customer segments, an RFM matrix, a segmentation strategy, or to prioritize retention
  efforts by segment value. Also trigger on "segmentazione clienti", "matrice RFM", "segmenti", "RFM analysis",
  "lifecycle stage", "churn risk". Requires a customer export already analyzed by 43_crm_database_analysis.
---

# RFM Segmentation — SA9

> **Agente:** SA9 (CRM/Lifecycle). Seconda funzione del flusso CRM.
> **Input:** database clienti (post `43_crm_database_analysis`).
> **Output:** `intermediate/sa9_rfm_segments.md`
> **Alimenta:** `45_email_strategy` (azioni per segmento), SA4 (split budget), SA3 (LTV per segmento).

Segmenta il database con **RFM + lifecycle stage + churn risk**. Ogni segmento esce con size, revenue, e azione raccomandata — pronto per la strategia email.

---

## Metodo RFM

Tre dimensioni, ognuna in score 1-5 (5 = migliore):

| Dimensione | Cosa misura | Come scorare |
|-----------|-------------|-------------|
| **Recency (R)** | giorni dall'ultimo ordine | quintili: 5 = più recente, 1 = più vecchio |
| **Frequency (F)** | n. ordini totali | quintili: 5 = più ordini, 1 = un ordine |
| **Monetary (M)** | revenue totale cliente | quintili: 5 = più speso, 1 = meno speso |

**Scoring per quintili:** ordina i clienti per ogni dimensione, dividi in 5 fasce uguali (20% ciascuna), assegna 1-5. Score RFM = concatenazione (es. `5-4-5`) o somma (3-15).

> Se il dataset è piccolo (<200 clienti) usa terzili (1-3) invece dei quintili per evitare fasce vuote.

---

## 11 Segmenti standard (da score R-F-M)

| Segmento | Regola (R,F,M) | Significato | Azione |
|----------|---------------|-------------|--------|
| **Champions** | R 4-5, F 4-5, M 4-5 | comprano spesso, di recente, spendono tanto | VIP, early access, referral, no sconti |
| **Loyal** | R 3-5, F 3-5, M 3-4 | regolari, buon valore | upsell, cross-sell, loyalty |
| **Potential Loyalist** | R 4-5, F 2-3, M 2-3 | recenti, pochi ordini | nurture verso il 2°/3° ordine |
| **New Customers** | R 5, F 1, M 1-2 | primo ordine recente | welcome series, onboarding prodotto |
| **Promising** | R 4, F 1, M 1 | recenti, spesa bassa | educazione valore, incentivo soft |
| **Need Attention** | R 3, F 3, M 3 | sopra media ma in calo | offerta limitata, reminder |
| **About to Sleep** | R 2-3, F 1-2, M 1-2 | recency in calo | riattivazione, "ci manchi" |
| **At Risk** | R 1-2, F 2-5, M 2-5 | spendevano, spariti | win-back forte, sondaggio |
| **Can't Lose Them** | R 1, F 4-5, M 4-5 | ex big spender persi | win-back premium, contatto personale |
| **Hibernating** | R 1-2, F 1-2, M 1-2 | bassi su tutto, vecchi | last-chance, poi sunset |
| **Lost** | R 1, F 1, M 1 | inattivi totali | sunset / esclusione invii |

---

## Lifecycle Stage (overlay)

Sopra l'RFM, mappa lo stage del ciclo di vita (utile per le automazioni):
```
Prospect → New Customer (1 ordine) → Active Repeat (2+) → Loyal/VIP → At Risk → Churned → Reactivated
```

## Churn Risk (se dati sufficienti)

Stima il rischio di abbandono:
- **Alto:** recency oltre 2× il purchase cycle medio del segmento + frequency in calo
- **Medio:** recency 1-2× il cycle medio
- **Basso:** dentro il cycle medio atteso

`Purchase cycle medio = media giorni tra ordini consecutivi` (per chi ha ≥2 ordini).

---

## Output — `intermediate/sa9_rfm_segments.md`

```markdown
# RFM Segmentation — {Brand} — {Data}

## Metodo
- Scoring: quintili (1-5) | terzili se <200 clienti
- Clienti segmentati: X | Purchase cycle medio: X giorni

## Matrice Segmenti
| Segmento | Clienti | % base | Revenue | % revenue | AOV seg. | Recency media | Azione |
|----------|--------:|-------:|--------:|----------:|---------:|--------------:|--------|
| Champions | X | X% | €X | X% | €X | Xgg | VIP/referral |
| ... | | | | | | | |

## Top opportunità (per revenue potenziale)
1. [Segmento] — X clienti, €Y revenue potenziale recuperabile — azione
2. ...

## Mappa Lifecycle
[distribuzione clienti per stage: prospect/new/active/loyal/at-risk/churned]

## Churn Risk
- Alto rischio: X clienti (€Y revenue a rischio) → priorità win-back
- Medio: X | Basso: X

## Raccomandazioni per la strategia email (→ 45)
- Automazioni prioritarie deducibili dai segmenti
- Segmenti più redditizi su cui concentrare gli invii
```

---

## Handoff
→ `45_email_strategy`: ogni segmento prioritizzato diventa un trigger di automazione o un flusso editoriale.
→ **SA4:** la dimensione dei segmenti retention informa lo split budget acquisition vs retention.
→ **SA3:** LTV e revenue per segmento per i calcoli NCAC/payback.

> Niente sconti ai Champions (margine bruciato su chi già compra). Sconti/win-back solo dove servono (At Risk, Can't Lose Them, About to Sleep).
