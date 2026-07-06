# SA7 — Headline Bank (Headline Specialist)

**Agente:** SA7 (Ad Copywriter)
**Output:** `06_Ad_Copy/headline-bank-[angle-slug]-[YYYY-MM-DD].md`
**Reference:** `_shared/headline_frameworks.md`, `_shared/awareness_tension_funnel.md`, `_shared/creative_claims_compliance.md`, `_shared/creative_kill_floor_review.md`, `context/brand/anti_ai_writing_style.md`

Deliverable dedicato più profondo delle 5 headline dentro `28_meta_copy`: circa 20 headline platform, 8 hook on-image per statiche, 6 first-line per primary text — tutte framework-nominate, char-contate, awareness-taggate, evidence-grounded nel VOC, passate per il gate personal-attributes Meta. Gratis e solo testo.

---

## Step 0 — Cartella + auto-discovery

```bash
WORKDIR="$PWD"
mkdir -p "$WORKDIR/06_Ad_Copy"
```

Leggi: `01_VOC_Research/` (linguaggio goldmine, pain, desideri, obiezioni, distribuzione awareness, prove sanzionate), `context/brand/tone_of_voice.md`. Risolvi la nicchia (`_shared/niche_offer_types.md`). Controlla anche:
```bash
ls -t "$WORKDIR/14_Creative_Briefs/"angles-*.json 2>/dev/null | head -n 1
```
Documenti mancanti: procedi, marca la bank "provisional".

## Step 1 — Modalità di input, UNA domanda al massimo

| Modalità | Segnale | L'ancora |
|---|---|---|
| A — da un angolo descritto | l'utente descrive prodotto/angolo | la sua descrizione |
| B — da un creative | l'utente carica un'immagine ad | analizza come `28_meta_copy` Fase 1A; l'angolo del creative è l'ancora |
| C — da un angle bank | esiste `angles-*.json` approvato e l'utente nomina un id ("per l'angolo A03") | big idea/calibrazione/citazione di quella card, consumate verbatim, id tenuto nel filename |
| D — riff su un winner | l'utente incolla una headline performante | la meccanica strutturale del winner |

Niente fornito: fai UNA domanda che offra tutte le modalità (elenca gli id del bank come opzioni numerate se esiste). Proponi la calibrazione nello stesso messaggio (`_shared/awareness_tension_funnel.md` A.3), override in una parola. Chiedi anche, solo se non chiaro: placement destinazione (Facebook Feed, Instagram, TikTok, o misto — default misto, cambia la disciplina caratteri allo Step 2).

## Step 2 — Disciplina caratteri, deterministica, prima di scrivere

Carica `_shared/headline_frameworks.md`. Regole di conteggio:

1. Headline platform: hard max 40 caratteri. Flag SAFE-AT-27 su ogni riga (lunghezza truncation-safe Facebook Feed). ALMENO METÀ del bank deve essere ≤27.
2. Description non è il deliverable di questa skill — se richieste, indirizza a `28_meta_copy` (target 25, hard max 30).
3. First line: hook nei primi 125 caratteri visibili; scrivi nel range 60-110 come banda di lavoro.
4. Righe destinate a TikTok: devono reggere una caption a 4 righe, hook nella prima riga, niente link/@/hashtag nel testo.
5. Mediana storica headline vincenti: 5 parole. Quando una riga è lunga, taglia parole prima di tagliare significato.

Mostra il conteggio accanto a ogni riga, sempre. Una riga oltre il limite si riscrive prima di essere mostrata.

## Step 3 — Costruisci il bank

Carica `_shared/awareness_tension_funnel.md`, `context/brand/anti_ai_writing_style.md`, `_shared/creative_claims_compliance.md`. Genera 3 sezioni, ogni riga ancorata al linguaggio reale del cliente e a prove reali (o omesse):

**Sezione 1 — Headline platform.** Target 20 surfaced (genera ~30, il kill floor ne mangia circa un terzo).
- Almeno 8/20 righe guidano con le tattiche verificate a winner-rate più alto (offerta, annuncio sconto, price anchor, urgenza, novità, confessione) — taggale `leading`.
- Tutte le 9 famiglie framework rappresentate almeno una volta, + almeno 3 delle 5 formule direct-response. Nessuna famiglia più di 3 volte.
- Domanda/listicle/how-to/explainer ammesse ma taggate `weaker-default`, accoppiate a una riga `leading` sulla stessa idea (test forte-contro-debole deliberato).
- ZERO righe lifestyle vaghe o beneficio generico — riscrivi col meccanismo/prop/parole cliente verbatim prima che entrino nel bank.
- Ogni riga taggata: framework, conteggio char, SAFE-27 sì/no, fit awareness, rif evidenza se usa una claim.

**Sezione 2 — Hook on-image.** 8 righe per stare SULL'immagine statica (le statiche text-forward sono la famiglia asset vincente in assoluto — queste righe sono portanti, non decorazione). Corte, alto contrasto, frammenti ammessi, dal set meccaniche H.4, 3-8 parole ciascuna.

**Sezione 3 — First-line opener.** 6 righe di apertura primary text, ognuna su una forma diversa (`headline_frameworks.md` H.3), dentro la banda dello Step 2, che passa il test lettura-ad-alta-voce.

**Extra modalità D (riff ladder):** analisi strutturale del winner (meccanica, trigger, perché funziona, 3 righe), poi 3 scale di 3 variazioni ciascuna, ognuna cambiando ESATTAMENTE una variabile (verbo più forte, numero sourced aggiunto, riformulata come domanda, posta la scadenza, desiderio scambiato dal VOC). Le righe delle scale contano per la Sezione 1.

## Step 4 — Passaggio compliance, binario, su OGNI riga

1. **Gate personal-attributes (il rejection minefield).** Per ogni riga: assere o implica che il VIEWER ha un attributo listato (etnia, religione, credo, età, orientamento, disabilità, condizione medica/salute)? Meccaniche che fanno scattare la violazione: domanda diretta su salute ("Hai...?"), second-person legato ad attributo ("il tuo diabete"), "other" + sostantivo-attributo. Callout su interessi/comportamenti sono sicuri; età e salute no. Riscrivi silenziosamente prodotto-focused o community-focused (tabella in `headline_frameworks.md` H.1.7) prima che il bank sia mostrato.
2. **Gate prova** (`creative_claims_compliance.md` C.1): ogni numero traccia a VOC/Brand DNA/ad scrapati, o si omette.
3. **Gate nicchia** (C.2): linguaggio guadagni per brand info (mai livelli/range di reddito senza sostanziazione), claim salute a livello struttura-funzione per DTC.
4. **Postura clickbait:** niente forme clickbait information-withholding ("Non ci crederai...") né righe beg-for-engagement. Motivazione: rischio-demotion + craft debole — MAI "Meta lo vieta negli ad" (claim falsa).

## Step 5 — Self-review, kill floor

Carica `_shared/creative_kill_floor_review.md`. Ogni riga per D.2b pass/fail. Ordina ogni sezione best-first (densità di evidenza, verità del framework, distanza dall'ad-speak generico), UCCIDI il terzo più debole della Sezione 1 con ragioni in una riga. Poi il passaggio duplicati: nessuna coppia di righe superstiti può condividere lo stesso meccanismo + la stessa promessa riformulata — uccidi la più debole. All-pass innesca il secondo passaggio avversariale prima che il bank possa battere il floor.

## Step 6 — Presenta, itera, salva

Presenta in chat: la riga di calibrazione (modalità, angolo, awareness, funnel, nicchia, placement), le 3 sezioni ordinate coi tag, poi `Killed:` con ragioni. Chiedi una volta: "Vuoi spingere qualche riga? 'più tagliente la 3', 'più offer-led', 'versioni safe-27 di 5 e 9', o 'salva'."

Al salvataggio:
```
$WORKDIR/06_Ad_Copy/headline-bank-<angle-slug>-<YYYY-MM-DD>.md
```
Header con: modalità input, calibrazione, placement, documenti sorgente, id concept se deck-driven (anche nel filename: `headline-bank-A03-<data>.md`). Stampa il path assoluto.

## Regole hard

- **Un solo compito.** Headline, hook on-image, first line. Il pacchetto completo è `28_meta_copy`, gli script sono `55_video_script`, i concept sono `13_creative_concepts`/`53_ad_angles`.
- **Il gate personal-attributes è assoluto.** Una riga rifiutata da Meta può flaggare l'ad account; una riga che implica una condizione di salute o l'età non parte mai senza riscrittura.
- **Disciplina caratteri a due livelli sempre visibile.** 40 è il tetto, 27 il target, il conteggio si mostra.
- **Linguaggio VOC prima del linguaggio intelligente.** Le citazioni restano verbatim con riferimento.
- **Il bank è ordinato e tagliato.** Un bank non tagliato è una review fallita.
- **I concept da deck/angle bank si consumano verbatim** (modalità C), id tenuti joinabili.
