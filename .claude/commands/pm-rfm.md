---
description: Segmentazione clienti RFM (Recency/Frequency/Monetary) + lifecycle stage + churn risk — 11 segmenti standard con size, revenue, azione per segmento. Skill 44 (SA9). Richiede DB analizzato da /pm-crm-analysis.
argument-hint: [path export clienti se non già analizzato]
---

# /pm-rfm — RFM Segmentation (SA9)

Esegui la skill **`directives/skills/44_rfm_segmentation/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/44_rfm_segmentation/SKILL.md`.
2. Usa il DB clienti (idealmente già passato da `/pm-crm-analysis`). Se <200 clienti → terzili invece di quintili.
3. Scora R, F, M (1-5), assegna agli 11 segmenti standard (Champions → Lost), overlay lifecycle stage + churn risk.
4. Output: `intermediate/sa9_rfm_segments.md` — matrice segmenti (clienti, %, revenue, AOV, recency, azione), top opportunità per revenue potenziale, mappa lifecycle, churn risk, raccomandazioni per la strategia email.
5. Handoff: → `/pm-email-strategy` (azioni per segmento), SA4 (split budget retention), SA3 (LTV per segmento).
6. **Regola:** niente sconti ai Champions; win-back/incentivi solo dove servono (At Risk, Can't Lose Them).
