# SA8 — Google Ads Optimisations (checklist ricorrente per tipo campagna)

**Agente:** SA8 (Analytics & Reporting)
**Output:** `output/reports/{YYYY-MM-DD}_google-optimisations/google_ads_optimisations_{account}.md`
**Tool:** Google Ads MCP (GAQL). MCC `5524890329`.
**Cadenza:** ricorrente. Le checklist sono cadenzate (Ogni 72h / Weekly / Monthly / 90 giorni).

---

## Knowledge base co-locata (in questa folder)
Checklist ufficiali Learnn per **tipo di campagna** (CSV, una riga = un task con frequenza + colonna TRUE/FALSE per cadenza):
- `Learnn Google Ads - Checklist Ottimizzazioni - Search.csv`
- `Learnn Google Ads - Checklist Ottimizzazioni - Shopping (1).csv`
- `Learnn Google Ads - Checklist Ottimizzazioni - Performance Max (1).csv`
- `Learnn Google Ads - Checklist Ottimizzazioni - Display (1).csv`
- `Learnn Google Ads - Checklist Ottimizzazioni - Demand Gen (1).csv`
- `Learnn Google Ads - Checklist Ottimizzazioni - Video (1).csv`
- `Learnn _ Google Ads Cheatsheet - Campaign Structure.csv` — **struttura campagne** (usata anche da SA4 per la campaign architecture)

Struttura CSV: colonne `Task | Frequency | Ogni 72h | Weekly | Monthly | 90 giorni | Note`. La cadenza attiva per ogni task è marcata `TRUE`.

---

## Scopo
Eseguire in modo disciplinato e ricorrente la checklist di ottimizzazioni **giusta per il tipo di campagna** dell'account, alla cadenza giusta. Niente ottimizzazioni a caso — processo ripetibile e tracciato.

## Procedura
1. **Identifica i tipi di campagna** presenti nell'account (GAQL `campaign.advertising_channel_type` / `...sub_type`): Search, Shopping, PMax, Display, Demand Gen, Video.
2. **Carica la checklist CSV corrispondente** a ogni tipo presente (da questa folder).
3. **Determina la cadenza** richiesta (72h / Weekly / Monthly / 90d) in base a quando è stata fatta l'ultima ottimizzazione (chiedi all'utente o default Weekly). Esegui solo i task marcati `TRUE` per quella cadenza.
4. Per ogni task: esegui la query GAQL pertinente, valuta contro la soglia indicata, decidi l'azione.
5. Compila il report: stato per task + finding (dato) + azione + impatto, prioritizzato con ICE.
6. **Non modificare l'account senza conferma** — produce raccomandazioni, l'esecuzione in piattaforma la fa l'utente (o un handoff dedicato).

## Output (struttura fissa, segue `31_reporting_template`)
```markdown
# Google Ads Optimisations — {account} — {tipo campagne} — {cadenza} — {periodo}

## Checklist eseguita (per tipo campagna)
| Tipo | # | Task | Cadenza | Stato | Finding (dato) | Azione | Impatto |

## Azioni prioritizzate (ICE)
| # | Azione | Tipo campagna | Impact | Confidence | Ease | ICE | Owner | Quando |

## Quick wins / Next Steps ➡️
```

## Regole critiche
- **Usa la checklist del tipo campagna corretto** — non applicare task Search a una PMax.
- **Rispetta la cadenza** (72h/Weekly/Monthly/90d) — esegui solo i task dovuti.
- **Dati GAQL reali**, costo in micros → € (÷ 1.000.000).
- **Non modificare l'account** senza conferma esplicita.
- **Prioritizza con ICE**. Handoff: copy/QS → SA7; landing → `29_landing_page`; struttura → SA4 (Campaign Structure cheatsheet).
