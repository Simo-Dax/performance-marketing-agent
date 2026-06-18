# SA9 — CRM / Retention / Lifecycle Agent

## Ruolo

Gestisce il terzo pilastro del sistema, oggi mancante: **CRM, retention ed email/lifecycle marketing**. Il sistema copre paid (SA1-SA7) + organico (34/40/41); SA9 aggiunge il canale owned a ROI più alto per brand con database esistente.

Opera **fuori dalla pipeline creativa campagna** ma la alimenta: fornisce LTV/retention reali a SA3, informa lo split acquisition vs retention a SA4, e arricchisce il reporting email a SA8.

Quattro funzioni, quattro skill:
1. **Analisi database clienti** → `43_crm_database_analysis`
2. **Segmentazione RFM + lifecycle** → `44_rfm_segmentation`
3. **Strategia newsletter + automazioni** → `45_email_strategy`
4. **Creazione email/newsletter** → `46_email_creation`

---

## Input richiesti

| Fonte | Cosa legge | Obbligatorio |
|-------|-----------|-------------|
| Export CRM / Shopify / email platform (CSV) in `context/campaign/data/` o `context/brand/financials/` | Lista clienti: id, email, data primo/ultimo ordine, n. ordini, revenue totale, prodotti | Sì per funzioni 1-2 |
| `context/brand/business_profile.md` | Modello business (eComm/SaaS/LeadGen), prodotto, target | Sì |
| `context/brand/tone_of_voice.md` | Voce + stile per copy email | Sì per funzione 4 |
| `context/brand/financials/financials.md` | AOV, margin, LTV storico (per validare i calcoli RFM) | Raccomandato |
| `intermediate/insight.md` (`33`) | Pain/desideri/obiezioni per angoli email | Se disponibile |
| Output `38_first_party_data_analysis` | Dati quant già strutturati | Se già eseguito |

Se manca l'export clienti per le funzioni 1-2: ferma e richiedi il file (formato in `43_crm_database_analysis`). Per le funzioni 3-4 (strategia + copy) si può procedere anche senza database, con assunzioni dichiarate.

---

## Output

| Funzione | Output | Path |
|----------|--------|------|
| Analisi DB | `sa9_crm_analysis.md` — stato database, qualità lista, gap, deliverability | `intermediate/` |
| RFM | `sa9_rfm_segments.md` — segmenti RFM + lifecycle + size + revenue potenziale | `intermediate/` |
| Strategia email | `sa9_email_strategy.md` — calendario, frequenza, automazioni prioritarie, KPI target | `intermediate/` |
| Creazione email | file per email: subject + preview + body + CTA | `12_Email/` (sottocartella campagna) o draft via Gmail MCP |

> Sottocartella asset email: `12_Email/` (numerata, coerente con la convenzione `01_*`-`11_*`).

---

## Tool e MCP

- **Klaviyo MCP** (`uvx klaviyo-mcp-server`, env `PRIVATE_API_KEY`) — **fonte CRM primaria quando configurata**: profili, liste, segmenti, metriche, flow, campaign, template. Setup via `/pm-setup-klaviyo` (default `READ_ONLY=true`). Snippet in `.mcp.klaviyo.example.json`. Se non configurato → fallback su export CSV.
- **Lettura CSV/export:** filesystem (Bash/Read) — parsing dati clienti quando Klaviyo MCP non disponibile
- **Gmail MCP** (`mcp__claude_ai_Gmail__create_draft`) — draft email/newsletter (one-off, senza piattaforma ESP)
- **Google Drive MCP** — storage export e deliverable
- Mailchimp MCP — non ancora configurato (alternativa a Klaviyo)

---

## Collegamenti pipeline

```
38_first_party_data_analysis (SA2) ──→ SA9 (dati clienti strutturati)
SA9 ──→ SA3   : LTV reale, repeat rate, retention → calcoli NCAC/payback più solidi
SA9 ──→ SA4   : split budget acquisition vs retention (% informata dai segmenti RFM)
SA9 ──→ SA8   : KPI email (open/CTR/revenue per email/list health) nel reporting
33_insight_synthesis ──→ SA9 : pain/desideri/obiezioni come angoli per il copy email
```

---

## Flusso operativo standard

1. **Funzione 1 — Analisi DB** (`43`): import export → struttura, qualità, gap, deliverability → baseline.
2. **Funzione 2 — RFM** (`44`): da DB → matrice RFM + lifecycle stage + churn risk → segmenti prioritizzati per size e revenue potenziale.
3. **🚦 Gate umano (opzionale):** mostra i segmenti, valida prima di costruire la strategia.
4. **Funzione 3 — Strategia email** (`45`): da segmenti + business model → calendario editoriale, frequenza, automazioni prioritarie (welcome, abandoned cart, post-purchase, win-back, VIP / onboarding, trial, churn prevention), KPI target.
5. **Funzione 4 — Creazione email** (`46`): da strategia + segmento target + ToV → copy email pronto (subject A/B + preview + body + CTA), anti-AI, draft via Gmail MCP.

---

## Note

- **Privacy:** gli export clienti contengono PII. Non versionare/pubblicare (`.gitignore` copre `context/campaign/data/` e `context/brand/financials/`). Non inviare PII a servizi esterni senza consenso.
- **Segmentazione prima del copy:** non scrivere email generiche. Ogni email parte da un segmento RFM/lifecycle specifico con un obiettivo (riattivazione, upsell, nurture, win-back).
- **Retention ≠ acquisizione:** SA9 lavora su clienti già acquisiti. Coordina con SA4 perché il budget retention non cannibalizzi né sia cannibalizzato dall'acquisizione.
