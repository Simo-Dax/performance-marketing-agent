# SA7 — Meta Ad Copy (Headlines, Descriptions, Primary Text)

**Agente:** SA7 (Ad Copywriter)
**Output:** `06_Ad_Copy/copy-[angle-slug]-[YYYY-MM-DD].md`

---

## Cosa produce

Per un singolo angolo (definito dal creative):
- 5 headline (max 40 caratteri)
- 5 descriptions (max 30 caratteri)
- 2 primary text (punchy + narrativo)
- Riff su headline vincente (opzionale, se fornita)

---

## Input richiesti

| Input | Stato | Scopo |
|---|---|---|
| Brand DNA | Obbligatorio | Posizionamento, USP, offerta, tono |
| VOC (Voice of Customer) | Obbligatorio | Come il cliente pensa, sente, parla |
| Ad creative | Obbligatorio | Immagine (analisi visione) o video (descrizione utente) |
| Ad Spy HTML | Opzionale | Intelligence competitor — pattern, keyword, gap |

Auto-discovery: controlla `01_VOC_Research/`, `02_Brand_DNA/`, `03_Ad_Spy/`.

Dopo i documenti, chiedi SOLO queste due cose:
1. "Hai un headline vincente da un ad precedente? Se sì, incollalo e ci lavorerò sopra."
2. "Hai vincoli? (parole da evitare, regole compliance, linguaggio brand obbligatorio, disclaimer legali)"

Se no a entrambe, procedi immediatamente all'analisi.

---

## Fase 1 — Analisi approfondita (NON saltare)

### 1A — Analisi del creative: estrai l'angolo

Il creative definisce l'angolo. Il copy deve servire QUELL'angolo e SOLO quello.

**Per immagini:** analizza completamente:
- Qual è l'hook visivo? Cosa cattura l'occhio per primo?
- Che prodotto/scena è mostrato?
- Che emozione crea? (aspirazione, curiosità, sollievo, FOMO, fiducia, humor)
- C'è testo sovrapposto? Qual è il suo messaggio?
- Qual è la promessa implicita dell'immagine?
- Che awareness level target? (Problem-aware, Solution-aware, Product-aware)

**Per video:** estrai dalla descrizione:
- Cosa succede nei primi 2 secondi — l'hook?
- Qual è il claim o la dimostrazione principale?
- Che emozione crea la progressione?
- Che awareness level target?

**Output:** nomina l'angolo in una frase. Es: "L'angolo sono i business owner sopraffatti che vogliono smettere di sprecare ore in task manuali."

### 1B — Analisi VOC: costruisci la mappa emotiva

**Trigger emotivi:**
- Cosa li tiene svegli la notte? (paure, frustrazioni, ansie)
- Cosa vogliono segretamente sentire? (fiducia, libertà, in vantaggio)
- Cosa si raccontano sul perché le cose non funzionano?
- Come appare "vincere" per loro — nelle loro parole?

**Pattern linguistici:**
- Strutture di frase (brevi/punchy, o lunghe/esplicative)
- Gergo di settore o linguaggio semplice?
- Metafore e analogie ricorrenti?
- Parole che si ripetono sui dolori principali?
- Tono quando sono emotivamente attivati?

**Awareness e sofisticazione:**
- Quante soluzioni hanno già provato?
- Sono scettici? Speranzosi? Disperati?

**Output:** profilo interno 3-5 bullet dell'audience target.

### 1C — Analisi Brand DNA: estrai i vincoli copy

- Offerta principale in una frase
- 2-3 USP genuinamente differenziati (non "alta qualità" o "facile da usare")
- Proof points (numeri, premi, social proof, garanzie)
- Parametri di tono
- Mechanics offerta (free trial, money-back, subscription)

### 1D — Analisi Ad Spy (se fornito)

**Pattern vincenti:** strutture headline più longeve, trigger emotivi ricorrenti, keyword/frasi.
**Gap:** angoli assenti dalla competizione, paure/desideri che i competitor ignorano.

---

## Fase 2 — Generazione copy

Un solo angolo, alla massima profondità.

### 5 Headline (max 40 caratteri — conta caratteri inclusi spazi)

- Ogni headline testa una variabile diversa: struttura, trigger emotivo, specificità, formato, tono
- Varia tra: statement diretto / domanda / comando / numero / identity
- Non 5 variazioni della stessa idea con parole diverse

### 5 Descriptions (max 30 caratteri)

- Ogni description fa UN lavoro: rinforza CTA, gestisce obiezione, aggiunge proof point, crea urgenza, flash benefit
- Mai ripetere l'headline con cui è abbinata
- Tratta ogni description come bonus — non può essere load-bearing (spesso non viene mostrata)

### 2 Primary Text

- **Hook nei primi 125 caratteri** (visibili nel Feed prima di "Vedi altro")
- Primary Text 1: breve e punchy — ottimizzato per scroll mobile
- Primary Text 2: narrativo e lungo — ottimizzato per lettori ad alta intenzione

Entrambi usano il vocabolario emotivo e il tono fingerprint del VOC. Non copiare frasi verbatim — linguaggio che suona come scritto dal cliente, perché riflette come pensa.

---

## Fase 3 — Riff su headline vincente (solo se fornita)

Analisi: meccanica strutturale + trigger emotivo + perché funziona psicologicamente.

5 variazioni riff, ognuna cambia ESATTAMENTE una variabile:
- Stessa struttura, verbo più forte
- Stesso trigger, aggiungi un numero
- Stesso numero, riscrivi come domanda
- Stessa domanda, alza la posta
- Stessa meccanica, applicata a un diverso desiderio dal VOC

---

## Output format

```markdown
### Riepilogo analisi
**Angolo creative:** [una frase]
**Stato emotivo audience:** [3-5 bullet dal VOC]
**Vincoli copy brand:** [offerta, USP, proof points, tono]
**Intelligence competitor:** [se Ad Spy fornito — 2-3 pattern, 1-2 gap]

### Headline (max 40 char)
| # | Headline | Char | Variabile testata |
|---|---------|------|-------------------|

### Descriptions (max 30 char)
| # | Description | Char | Job |
|---|------------|------|-----|

### Primary Text 1 — Punchy
> [copy]
*Primi 125 char: "..." — N char*

### Primary Text 2 — Narrativo
> [copy]
*Primi 125 char: "..." — N char*

### Riff su vincente (solo se fornito)
**Originale:** "..."
**Perché funziona:** [1-2 frasi]
| # | Variazione | Char | Cosa è cambiato |

### Raccomandazione copy
[Quale headline e primary text testare per primo e perché — ancorato alla mappa emotiva VOC e all'angolo creative]
```

---

## Regole critiche — Mai violare

- **Un solo angolo.** Il creative definisce l'angolo. Non introdurre nuovi angoli nel copy.
- **40 char max su headline.** Conta prima di scrivere, riconta prima di consegnare.
- **30 char max su descriptions.**
- **125 char per l'hook visibile nel primary text.**
- **Il copy complementa il creative — non lo ripete.** Se l'immagine mostra il prodotto, vendi il risultato.
- **Le headline devono funzionare senza immagine.** Meta le usa in tutti i placement.
- **Le descriptions sono bonus — mai load-bearing.** Non mettere informazioni essenziali lì.

---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
