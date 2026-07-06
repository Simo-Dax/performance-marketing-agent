# Motore condiviso — Review binario con kill floor

Riferimento condiviso usato da `53_ad_angles`, `54_headline_bank`, `55_video_script` come self-review prima di presentare l'output. Definisce come un output creativo viene GIUDICATO prima di essere consegnato: un obiettivo di run in una riga, una rubrica binaria (pass/fail, mai punteggi), e 4 regole strutturali che rendono impossibile l'approvazione pigra.

Premessa: chiedere a un reviewer di "essere critico" non funziona, perché l'accondiscendenza è la via a minor sforzo. Ogni meccanismo qui rimuove una mossa facile invece di chiedere al modello di resisterle. Approvare deve costare più sforzo che rifiutare.

---

## D.1 — L'obiettivo del run (tutto si misura contro una frase)

Prima di ogni valutazione, scrivi l'obiettivo in una riga:

```
[volume] [tipo asset] per [brand] targeting [funnel stage + awareness] intorno a [offerta/momento], ottimizzando per [la cosa che conta di più in questo run]
```

Esempio: "8 concept per Brand X, TOF freddo, skew problem-aware, offerta lancio primavera, ottimizzando per diversità di retrieval."

Regole: l'obiettivo si scrive una volta e non cambia silenziosamente a metà run. Ogni verdetto lo cita ("fallisce l'obiettivo: duplica la cella-desiderio del concept 3"). Se la richiesta è troppo vaga per scrivere questa riga, fai UNA domanda prima; giudicare contro un obiettivo indovinato produce nonsense sicuro di sé.

## D.2 — La rubrica binaria

Ogni check è pass o fail. Un fail su un check hard uccide o rimanda l'item. Nessun punteggio 1-10 (i punteggi driftano verso i sette, e i sette passano tutti).

### D.2a — Check per angolo/concept (per ogni angle)

| # | Check | Se fallisce |
|---|---|---|
| 1 | FILTRO GENERICO: potrebbe girare per qualsiasi brand della categoria col logo cambiato? | kill |
| 2 | CELLA UNICA: occupa una cella Persona × Desiderio × Awareness che nessun altro angolo nel set occupa | kill |
| 3 | ANCORA VOC: porta una citazione cliente verbatim con riferimento fonte che regge (verifica meccanicamente: cerca la citazione nel testo sorgente, normalizzata negli spazi; non trovata = fail) | kill |
| 4 | DISTINZIONE AL RENDER: produrrebbe un ad visibilmente diverso da tutti gli altri a dimensione thumbnail | kill |
| 5 | MATCH AWARENESS: la profondità del messaggio si adatta allo stadio dichiarato (niente lezioni sul meccanismo su most-aware, niente offerte nude su unaware) | rimanda per ricalibrazione |
| 6 | COMPLIANCE: passa i gate di nicchia in `creative_claims_compliance.md` (C.1, C.2, C.3) | kill, con l'alternativa compliant proposta |

### D.2b — Check per headline/copy (per riga o blocco)

| # | Check | Se fallisce |
|---|---|---|
| 1 | FRAMEWORK NOMINATO e VERO: la riga nomina il suo framework E fa davvero quello che promette | revise |
| 2 | LIMITI CARATTERE: headline ≤40, description ≤30, hook nei primi 125 del primary text | hard fail, riscrivi |
| 3 | SLOT PROVE: ogni numero traccia per C.1 | kill la riga |
| 4 | TEST PRIMA RIGA: la riga di apertura ferma lo scroll SENZA l'immagine | revise |
| 5 | VOCE NATURALE: passa il test lettura-ad-alta-voce, nessuna costruzione bandita (cita la frase violante) | revise |
| 6 | FIT OBIETTIVO: serve il funnel stage e l'offerta del run (una riga TOF brillante in un run BOF fallisce) | revise |

### D.2c — Check per script (per ogni script)

1. Scheletro seguito internamente, i beat mai etichettati nell'output.
2. `mode` e `wps` seguono l'ordine di priorità della skill target: MISURATO dai teardown spy-video quando esistono, altrimenti la costante della modalità.
3. Hook entro i primi 3 secondi di audio parlato.
4. Ogni riga regge se detta ad alta voce da una persona reale.
5. CTA presente, singola, coerente col funnel stage, script che finisce su di essa.

## D.3 — Le 4 regole strutturali

**1. Prova o fallisce.** Un verdetto di pass deve citare la sua prova inline: il rif VOC, il nome del framework, le coordinate della cella, il conteggio caratteri. "Il concept 4 passa" è un verdetto invalido e va rifatto. Quando approvare costa una citazione, l'approvazione pigra smette di essere la mossa economica.

**2. Ranking forzato con kill floor.** Ogni review classifica tutti gli item dal migliore al peggiore e nomina il più debole con ragioni specifiche e una direzione di sostituzione proposta, anche quando tutto tecnicamente passa. Kill floor per tipo asset: i deck/bank uccidono il terzo più debole (scala proporzionalmente), i blocchi copy e gli script prendono almeno un revise-o-kill per batch. **REGOLA ALL-PASS:** una review che approva tutto conta come review fallita e scatena ESATTAMENTE un secondo passaggio avversariale ("un media buyer esperto ne taglierebbe due prima di spendere un euro; trovali e di' perché"). Se il secondo passaggio conferma che il set è forte, approva CON una giustificazione scritta del perché ha battuto il kill floor, mostrata all'utente.

**3. Occhi freschi.** Il passaggio di valutazione gira in un contesto pulito contenente SOLO: l'obiettivo del run, questa rubrica, l'output sotto review, le regole hard del brand (banlist, compliance), il deck approvato (per congruenza), e la barra competitor. Non contiene mai la conversazione di pianificazione o il ragionamento del generatore. Framing: stai revisionando la submission di un'agenzia esterna prima che il cliente paghi i render.

**4. Rifiuta con una direzione, o non rifiutare.** Ogni kill/revise arriva con una direzione di sostituzione proposta, instradata verso la skill che l'ha prodotto. "Uccidi il concept 6" è invalido. "Uccidi il concept 6: duplica la cella-desiderio price-anxiety del concept 2. Sostituisci con l'obiezione sui tempi di spedizione non affrontata dal VOC, angolata come rivelazione del meccanismo sul fulfillment" è valido.

## D.4 — Il loop di revisione (limitato)

1. Instrada la nota di correzione (1-3 righe, citando il check fallito e la direzione) di nuovo verso la skill produttrice.
2. Ri-revisiona solo gli item cambiati. I pass invariati non si ridiscutono.
3. Massimo due cicli di revisione per item. Ancora fallito dopo due: escalation all'utente con l'item, i check falliti, la miglior proposta di sostituzione. Mai spedire silenziosamente un item fallito.
4. Il reviewer NON riscrive mai il contenuto creativo. Nel momento in cui il reviewer riscrive una headline diventa un secondo autore senza gate. Solo fix meccanici (naming file, posizionamento cartella); i cambi creativi tornano sempre alla skill produttrice.

## D.5 — Il verdetto visibile

Riporta all'utente: la riga obiettivo, il ranking, cosa è stato ucciso e perché, cosa è stato rivisto, e le citazioni di prova per ciò che è stato spedito. Le decisioni di kill visibili sono dove la strategia diventa tangibile.

## D.6 — Fallimenti ricorrenti

Se lo stesso check fallisce ripetutamente sulla stessa skill in run successivi, non è rumore ma un segnale a monte: cattura il pattern via il meccanismo di self-improvement già esistente nel progetto (`/pm-feedback`, `directives/feedback_log.md`), non con un log nuovo. Il reviewer non modifica mai questo file o le skill che lo consumano — solo l'utente, tramite feedback esplicito.
