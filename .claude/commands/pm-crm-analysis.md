---
description: Analisi database clienti (Shopify/CRM/email export CSV) — struttura, data quality, list health, baseline metriche (repeat rate, AOV, Pareto), gap analysis. Prerequisito per RFM. Skill 43 (SA9).
argument-hint: [path export CSV clienti]
---

# /pm-crm-analysis — CRM Database Analysis (SA9)

Esegui la skill **`directives/skills/43_crm_database_analysis/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/43_crm_database_analysis/SKILL.md`.
2. Carica l'export clienti (da `$ARGUMENTS`, `context/campaign/data/` o `context/brand/financials/`). Se manca → richiedilo (colonne minime nella skill).
3. Esegui i 5 step: parsing/struttura → data quality → list health → baseline metriche → gap analysis.
4. Output: `intermediate/sa9_crm_analysis.md` — snapshot, data quality (🟢/🟡/🔴), list health, baseline (repeat rate, AOV, Pareto, distribuzione ordini), gap + quick win.
5. Passa la baseline a SA3 (LTV/repeat reali) e dichiara se il DB è pronto per `/pm-rfm`.
6. **PII:** dati reali cliente — non versionare/pubblicare, lavora in locale.
