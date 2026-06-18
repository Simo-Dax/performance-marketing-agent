---
name: crm-database-analysis
description: >
  Analyze a customer database export (Shopify / CRM / email platform CSV) to assess structure, data quality,
  list health, and gaps before segmentation. Use when the user provides a customer/orders export and wants
  a database health check, list audit, or baseline for CRM/retention work. Also trigger on "analizza il database clienti",
  "audit lista email", "stato del CRM", "customer data analysis", "list health". Prerequisite for 44_rfm_segmentation.
---

# CRM Database Analysis — SA9

> **Agente:** SA9 (CRM/Lifecycle). Prima funzione del flusso CRM.
> **Output:** `intermediate/sa9_crm_analysis.md`
> **Prerequisito per:** `44_rfm_segmentation`.

Analizza un export del database clienti per capire **cosa c'è, quanto è pulito, e cosa manca** prima di segmentare o scrivere email. Garbage in = garbage out: questa skill è il gate qualità dei dati CRM.

---

## Input

**Fonte primaria — Klaviyo MCP (se configurato via `/pm-setup-klaviyo`):** leggi profili, liste, segmenti, metriche ed engagement live dall'account Klaviyo — niente export manuale. Preferisci questa fonte quando disponibile.

**Fallback — Export CSV/Excel** da una di queste fonti, in `context/campaign/data/` o `context/brand/financials/`:
- **Shopify:** Customers export (Customer name, email, orders count, total spent, accepts marketing, dates)
- **CRM generico:** contatti con storico ordini/interazioni
- **Email platform (Klaviyo/Mailchimp):** lista con engagement (open/click/last active)

### Colonne minime utili
| Colonna | Uso | Obbligatoria |
|---------|-----|-------------|
| email / customer_id | identità, dedup | Sì |
| first_order_date / created_at | recency, lifecycle | Sì per RFM |
| last_order_date | recency | Sì per RFM |
| orders_count / frequency | frequency RFM | Sì per RFM |
| total_spent / revenue | monetary RFM, LTV | Sì per RFM |
| accepts_marketing / consent | deliverability, base inviabile | Raccomandata |
| last_email_engagement | list health | Opzionale |
| country / city | geo, localizzazione | Opzionale |
| products / categories | cross-sell, affinità | Opzionale |

Se mancano le colonne RFM obbligatorie → segnalalo: la segmentazione completa non sarà possibile, solo l'audit lista.

---

## Processo

### Step 1 — Parsing & struttura
Leggi il file (Bash/Read). Conta righe, identifica le colonne, mappale allo schema sopra. Riporta: n. record totali, n. colonne, encoding, formato date.

### Step 2 — Data quality
| Check | Cosa misurare |
|-------|--------------|
| Email valide | % email con formato valido (regex), domini sospetti, role-based (info@, no-reply@) |
| Duplicati | % record duplicati per email/id |
| Campi mancanti | % null per ogni colonna chiave |
| Consenso marketing | % `accepts_marketing = true` → **base realmente inviabile** |
| Date coerenti | first_order ≤ last_order, niente date future |
| Outlier monetary | ordini/spesa anomali (refund, test order, B2B bulk) |

### Step 3 — List health (se dati engagement disponibili)
- % attivi (aperto/cliccato negli ultimi 90gg)
- % dormienti (90-180gg)
- % morti (>180gg senza engagement) → candidati sunset
- Rischio deliverability: lista con troppi morti danneggia la sender reputation

### Step 4 — Baseline metriche
Calcola (servono a SA3 e a `44`):
- Clienti totali / inviabili
- Repeat rate = clienti con ≥2 ordini / totale
- AOV medio = revenue totale / ordini totali
- Revenue per cliente medio (proxy LTV)
- % revenue da top 20% clienti (concentrazione Pareto)
- Distribuzione ordini per cliente (1 / 2 / 3+ ordini)

### Step 5 — Gap analysis
Cosa manca per fare retention seria:
- Segmenti non tracciati (es. nessun dato consenso, nessun engagement)
- Colonne mancanti per personalizzazione (prodotto, geo, compleanno)
- Automazioni assenti deducibili (nessun campo "welcomed", "last_campaign")
- Quick win di raccolta dati (es. aggiungere consenso, birthday, preferenze)

---

## Output — `intermediate/sa9_crm_analysis.md`

```markdown
# CRM Database Analysis — {Brand} — {Data}

## Snapshot
- Record totali: X
- Email valide: X (Y%)
- Base inviabile (consenso): X (Y%)
- Duplicati rimossi: X

## Data Quality
[Tabella check: metrica, valore, status 🟢/🟡/🔴]

## List Health
- Attivi (90gg): X% | Dormienti: X% | Morti (>180gg): X%
- Rischio deliverability: [basso/medio/alto] + raccomandazione

## Baseline Metriche (→ SA3 / 44_rfm)
- Clienti: X | Inviabili: X
- Repeat rate: X%
- AOV: €X | Revenue/cliente: €X
- Pareto: top 20% clienti = X% revenue
- Distribuzione ordini: 1 ordine X% · 2 ordini X% · 3+ ordini X%

## Gap Analysis
[Cosa manca + quick win di raccolta dati, prioritizzati]

## Pronto per RFM?
[Sì/No + quali colonne servono se No]
```

---

## Handoff
→ `44_rfm_segmentation` (se baseline OK) per la segmentazione.
→ Baseline metriche anche a **SA3** (LTV/repeat reali) e a `38_first_party_data_analysis` se serve il track qualitativo.

> **Privacy:** PII reale. Non versionare, non inviare a servizi esterni. Lavora sui dati in locale.
