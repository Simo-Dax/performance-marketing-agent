---
name: email-strategy
description: >
  Build an email/newsletter strategy: editorial calendar, send frequency, priority automations (flows), and email KPI targets,
  adapted to business model (eCommerce / SaaS / LeadGen) and to RFM segments. Use when the user wants an email marketing strategy,
  newsletter plan, automation/flow strategy, lifecycle email plan, or retention plan. Also trigger on "strategia email",
  "piano newsletter", "automazioni email", "flussi email", "email marketing strategy", "retention strategy".
---

# Email Strategy — SA9

> **Agente:** SA9 (CRM/Lifecycle). Terza funzione del flusso CRM.
> **Input:** segmenti RFM (`44`) + `business_profile.md` + insight (`33` se disponibile).
> **Output:** `intermediate/sa9_email_strategy.md`
> **Alimenta:** `46_email_creation` (brief per ogni email) + SA8 (KPI email nel reporting).

Definisce **calendario editoriale + frequenza + automazioni prioritarie + KPI target**, adattati al business model e ai segmenti RFM. Strategia, non copy: il copy è `46`.

---

## Step 0 — Stato attuale (se Klaviyo MCP configurato)

Se il Klaviyo MCP è attivo (`/pm-setup-klaviyo`): leggi i **flow esistenti** + le **metriche** dell'account (open/click/revenue per flow) prima di proporre. La strategia diventa gap analysis sul reale: quali automazioni mancano, quali sottoperformano, quali segmenti non ricevono nulla. Senza Klaviyo MCP → procedi da assunzioni dichiarate + benchmark.

## Step 1 — Frame business model

| Modello | Focus email | Metrica nord |
|---------|------------|-------------|
| **eCommerce** | repeat purchase, AOV, win-back | Revenue per email / per recipient |
| **SaaS** | activation, retention, expansion, churn prevention | Activation rate / NRR |
| **LeadGen** | nurture, qualification, sales handoff | Lead-to-SQL / reply rate |

---

## Step 2 — Automazioni prioritarie (flows) per modello

Le automazioni (trigger-based) battono le campagne broadcast su revenue/email. Prioritizza per ICE.

### eCommerce
| Flow | Trigger | Obiettivo | Segmento RFM tipico |
|------|---------|-----------|--------------------|
| **Welcome series** (3-4 email) | iscrizione / 1° contatto | educare brand, 1° acquisto | Prospect / Promising |
| **Abandoned cart** (2-3) | carrello non concluso | recuperare acquisto | tutti |
| **Browse abandonment** (1-2) | visita prodotto senza acquisto | nurture intent | New / Promising |
| **Post-purchase** (2-3) | ordine completato | onboarding prodotto, recensione, cross-sell | New Customer |
| **Replenishment** | X giorni post-acquisto (consumabili) | riacquisto ciclico | Active Repeat |
| **Win-back** (2-3) | inattività > purchase cycle | riattivare | At Risk / About to Sleep |
| **VIP** | ingresso in Champions | reward, early access, referral | Champions / Loyal |
| **Sunset** | morti > 180gg | ultima chance poi rimozione | Lost / Hibernating |

### SaaS
Onboarding/activation series · trial nurture · trial-ending · feature adoption · upgrade/expansion · dunning (failed payment) · churn prevention (low usage) · reactivation.

### LeadGen
Lead nurture (educativo) · qualification (progressive profiling) · case study/proof · sales handoff (SQL) · re-engagement lead freddi.

---

## Step 3 — Calendario broadcast (newsletter)

Oltre alle automazioni, il ritmo editoriale:
- **Frequenza:** parti da quella sostenibile del brand (`business_profile.md`; per Simone: newsletter bisettimanale). Non superare la soglia di fatica → monitora unsubscribe + spam rate.
- **Mix contenuto:** regola ~ 70% valore (educativo/storia/insight) / 20% soft promo / 10% hard promo. Adatta al modello.
- **Mappatura awareness:** allinea i temi ai 5 stadi (coordina con `34_editorial_content_plan` se esiste un piano organico).
- **Segmentazione invii:** non inviare tutto a tutti. Champions ≠ At Risk ≠ New. Definisci quali broadcast vanno a quali segmenti.

---

## Step 4 — KPI target email

| KPI | Formula | Benchmark indicativo* |
|-----|---------|----------------------|
| Open rate | aperture / inviate (consegnate) | 25-40% (post Apple MPP, indicativo) |
| CTR | click / inviate | 2-5% |
| CTOR | click / aperture | 10-20% |
| Conversion rate | acquisti / click | dipende dal flow |
| Revenue per email | revenue / email inviate | benchmark interno |
| Revenue per recipient | revenue flow / destinatari | benchmark interno |
| List growth rate | (nuovi - persi) / lista | > 0 mensile |
| Unsubscribe rate | unsub / inviate | < 0.5% |
| Spam complaint | complaint / inviate | < 0.1% (oltre = problema deliverability) |

*Benchmark indicativi: usa sempre lo storico del brand come riferimento primario (da `43` / piattaforma email).

---

## Output — `intermediate/sa9_email_strategy.md`

```markdown
# Email Strategy — {Brand} — {Data}

## Frame
- Business model: [eComm/SaaS/LeadGen] | Metrica nord: [...]
- Base inviabile: X | Segmenti chiave (da 44): [...]

## Automazioni prioritarie (ICE)
| # | Flow | Trigger | Segmento | Impact | Confidence | Ease | ICE | Stato attuale |
|---|------|---------|----------|-------:|-----------:|-----:|----:|--------------|
| 1 | Welcome | ... | ... | | | | | assente/da migliorare |

## Calendario broadcast
- Frequenza: [...] | Mix: 70/20/10
- Tema per settimana/mese + segmento destinatario

## KPI target
[Tabella KPI con target basati su storico brand]

## Roadmap 90 giorni
- Mese 1: [automazioni quick win]
- Mese 2: [...]
- Mese 3: [...]
```

---

## Handoff
→ `46_email_creation`: ogni automazione/broadcast prioritizzato diventa un brief per il copy.
→ **SA8:** i KPI target entrano nel reporting email (sezione email in `31_reporting_template`).
→ **SA4:** la strategia retention informa lo split budget vs acquisizione.

> Automazioni prima dei broadcast: hanno il ROI/email più alto. Costruisci welcome + abandoned cart + post-purchase + win-back prima di ottimizzare le newsletter.
