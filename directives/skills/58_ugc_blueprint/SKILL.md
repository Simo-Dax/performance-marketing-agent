# SA6 — UGC Blueprint (parti da un video che ti piace, misuralo, ricostruiscilo tuo)

**Agente:** SA6 (Asset Production)
**Input:** un file video UGC locale (≤30s) che l'utente vuole usare come riferimento strutturale
**Output:** `17_UGC_Blueprints/<slug>/` — blueprint shot-by-shot + (opzionale) prompt di ricostruzione + render
**Modello:** Seedance 2.5 (**720p è il tetto attuale**, max 30s per generazione) — model-agnostic, vedi `execution/tools.md`
**Reference:** `references/gemini-teardown-prompt.md` (prompt locked per la Route A) · `references/output-template.md` (template blueprint) · `references/swap-and-render.md` (swap prompt + vincoli render)

La **terza lane** della famiglia UGC, quella **reference-driven**:
- `62_ugc_formats` costruisce da **11 formati**, ognuno con il suo banco di ad reali
- `25_ugc_prompt` fa il **fan-out Andromeda** da uno script
- `58_ugc_blueprint` (questa) parte da **UN video specifico che l'utente ha già scelto** e ne solleva la struttura

> **Cosa trasferisce: la STRUTTURA, mai il girato.** Numero di inquadrature, durate, ritmo dei tagli, inquadrature e dove cade il parlato. **Non** un frame dell'originale, non la sua persona, non le sue stanze, non il suo prodotto, non il suo audio.

> **Non è `52_ad_spy_video`.** Quella scrapa gli ad video di un competitor dalla Meta Ad Library (intelligence su molti ad). Questa parte da **un file locale** che l'utente ti dà, e arriva fino al render del **suo** ad.

Il blueprint da solo è un deliverable completo. **Offri la ricostruzione, non darla per scontata.**

---

## Step 0 — Chiedi il video

Se l'utente ha già allegato un video, salta allo Step 0.5. Altrimenti chiedi e **aspetta**:

> Dammi il video UGC di cui vuoi seguire la struttura — un ad o un post organico, qualsiasi cosa il cui impianto vuoi che il tuo abbia. **Un file locale, non un link.**
>
> **Tienilo sotto i 30 secondi**: è il massimo che il modello renderizza in una generazione, quindi un riferimento più lungo non può essere ricostruito come video singolo.
>
> Ti dico esattamente com'è fatto: ogni taglio e quanto dura, cosa c'è in ogni inquadratura, e se l'audio è musica, un voiceover o qualcuno che parla in camera. Poi, se vuoi, lo ricostruiamo col tuo prodotto e il tuo creator.

Accetta qualsiasi video locale. Non commentare cosa rende buono un riferimento se non te lo chiede — l'ha scelto perché per lui funziona.

## Step 0.5 — Cartella

```bash
WORKDIR="$PWD"
mkdir -p "$WORKDIR/17_UGC_Blueprints"
```
I file di lavoro vanno in una **scratch dir temporanea**, mai nel progetto. Solo il blueprint finito atterra in `17_UGC_Blueprints/<slug>/`.

## Step 0.75 — Offri le DUE route, e aspetta

Ci sono due modi per ottenere il blueprint. **Offri sempre entrambi e lascia scegliere.** Mai avviare l'analisi locale senza chiedere: è lenta, e metà delle volte l'utente preferisce quella veloce.

Manda esattamente questo, riempiendo il blocco con il contenuto di `references/gemini-teardown-prompt.md` **verbatim e per intero**:

> Due modi per analizzarlo. Scegli tu:
>
> **A — Con un modello video esterno (un paio di minuti).** Apri il tuo modello video preferito (es. Gemini), carica il video, incolla il prompt qui sotto, poi rimettimi qui la sua risposta. È veloce perché è un modello nato per il video.
>
> **B — Lo faccio io qui (più lento, ma MISURATO).** Trovo ogni taglio da una curva di differenza per-frame, guardo ogni inquadratura, trascrivo in locale e faccio un test di lip-sync su ogni shot. È più accurato che guardarlo — ma non sono un modello video specializzato, quindi ci vuole un po'.
>
> Stesso template in entrambi i casi, ed entrambi proseguono nella ricostruzione.
>
> ```
> [incolla qui il prompt completo da references/gemini-teardown-prompt.md]
> ```

Poi **fermati e aspetta.**

- **Sceglie A** → attendi che incolli l'output. Esegui i 4 check di validazione in `references/gemini-teardown-prompt.md`, riporta quali sono passati, salva, poi vai allo **Step 8**. Salta gli Step 1-7.
- **Sceglie B** → prosegui allo Step 1.
- **Non gli importa** → consiglia A per velocità, B quando l'ad è a taglio rapido o il conteggio delle inquadrature deve essere esatto.

Dichiara il trade onestamente: **la Route B misura, la Route A osserva.** Su un ad a taglio rapido un modello video può restituire 12 shot dove la curva di differenza ne trova 21, e ogni miss è un jump cut dentro un'inquadratura invariata.

---

## Step 1 — Probe

```bash
ffprobe -v error -show_entries format=duration \
  -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,channels,sample_rate \
  -of default=noprint_wrappers=1 "$V"
```
Registra durata, risoluzione, fps, e **se esiste una traccia audio**. Un video senza traccia audio non è "musica silenziosa": non ha traccia, e l'output deve dirlo.

**🚦 Gate 30 secondi.** Il modello renderizza **max 30s per generazione**. Controlla la durata ORA, prima di ogni analisi:
- **Sotto 30s** → prosegui, non dire nulla.
- **Sopra 30s** → fermati e metti la scelta all'utente: (a) **tagliare il riferimento** ai 30s che contano (di solito hook→CTA) e fare il teardown solo su quello; (b) **ritempare proporzionalmente** scalando tutte le durate per `30/durata` (preserva il ritmo, funziona fino a ~35s prima che il parlato debba perdere parole); (c) **fare comunque il teardown completo** come documento e ricostruire solo una parte.

Mai proseguire in silenzio oltre i 30s: un prompt il cui ultimo timestamp supera i 30s **non renderizza**, e il fallimento arriva dopo che il costo è stato approvato.

## Step 2 — Trova i tagli dalla curva di differenza

**Non usare `scdet` da solo.** La sua soglia è un pavimento cieco: i jump cut dentro un'inquadratura invariata scendono sotto e vengono persi, e il movimento veloce sale e inventa tagli inesistenti. Spazzare la soglia non risolve.

Prendi **tutta la curva**:
```bash
ffmpeg -hide_banner -nostats -i "$V" \
  -vf "select='gte(scene,0)',metadata=print:file=$D/scene.txt" -f null -
```
Poi ordina gli score e **cerca il GAP**: i tagli veri si raggruppano in alto e c'è un salto visibile fino al rumore di fondo. Esempi misurati: ad talking-head 32s → 8 tagli, range 0.177-0.617, rumore 0.055 (gap 3.2x); ad fast-cut 20s → 13 tagli, gap 2.2x.

Ignora gli score che cadono 1-2 frame dopo un taglio confermato: è la nuova inquadratura che si assesta, non un secondo taglio.

**Quando non c'è gap → cerca una griglia a battuta.** Alcuni ad sono montati su un intervallo musicale fisso e non producono **nessun gap**: gli score decadono in modo liscio. Prima di dichiarare irrisolto, testa la periodicità: se i tempi candidati sono quasi-multipli di un numero, quello è il grid dell'edit — allora valuta **ogni posizione della griglia** invece di sogliare. Misurato su un ad beauty da 22.7s: tutti e 30 i candidati su griglia 0.7s, i tagli on-grid 0.168-0.593, le due posizioni non-taglio 0.030 e 0.003 (gap 5.6x che il ranking grezzo nascondeva). Le posizioni saltate sono inquadrature di durata doppia, non errori.

Solo se **entrambi** i test falliscono, riporta i tagli marginali come irrisolti invece di inventare confini.

## Step 3 — Verifica ogni taglio debole
Ogni taglio nel terzo inferiore del cluster va verificato. **La finestra di score locale è il test; i frame sono solo una sanity check dopo.**

## Step 4 — Guarda ogni inquadratura
Estrai il **primo e il medio frame** di ogni shot e **guardali davvero**. Registra: cosa c'è in scena, inquadratura, tipo di shot, se la camera si muove (il dato dello Step 2 già risponde), prodotto presente e leggibilità dell'etichetta. Conta qui i **product beat** (servono allo Step 9).

## Step 5 — Classifica l'audio
1. **Trascrizione locale prima** (faster-whisper).
2. **L'envelope a bande è il vero discriminante** fra musica e parlato.
3. **Guarda la bocca** per il lip-sync.

Se l'audio è **solo musica**, dillo. Se qualcuno parla, **trascrivi verbatim**.

## Step 6 — Assegna il parlato agli shot, marca on-camera vs voiceover
Assegna ogni parola allo shot su cui cade (in codice, con `bisect`, **mai a occhio**) e marca ogni shot **TALKING ON CAMERA** o **VOICEOVER** col test di lip-sync contro i gap audio.

## Step 7 — Scrivi il breakdown
Compila il template di `references/output-template.md`. **Non aggiungere sezioni**: niente blocchi Set/Location, niente Camera globale, niente campo Music — gli sfondi si descrivono dentro lo shot che li usa, la camera vive sulla riga `Shot Type`.

---

# RICOSTRUZIONE (opzionale — offrila, non darla per scontata)

## Step 8 — Estrai l'hero anchor dall'apertura
**Il video serve anche in Route A** (un modello esterno restituisce testo, l'anchor è un frame reale).

L'anchor è **un frame dal primo product beat**, dove il prodotto è tenuto e leggibile. Spesso è il primo frame, e va benissimo — parti da lì e verificalo. Cerca nel **primo terzo**, solo negli shot che contengono il prodotto, ed estrai i candidati:
```bash
ffmpeg -y -loglevel error -i "$V" -vf "select='eq(n\,$N)',scale=240:427" -vsync 0 -frames:v 1 "$D/a$N.png"
```
Scegli il frame dove: l'etichetta è **più perpendicolare all'obiettivo** e a fuoco · nessun motion blur sul prodotto · volto non ostruito (o deliberatamente dietro il prodotto) · **nessuna caption sovrapposta**. Ri-esporta a **piena risoluzione**, mostralo e fatti approvare. Se ogni frame d'apertura ha testo impresso, dillo e offri il product beat pulito successivo.

## Step 9 — Il personaggio dal Brand DNA, poi l'intake
**Non chiedere chi è il creator prima di aver guardato.** Il brand ha già risposto. Leggi `02_Brand_DNA/*` e `01_VOC_Research/*` e **proponi** un personaggio (età, capelli, corporatura, incarnato, registro di abbigliamento) dal cliente ideale dichiarato, **citando da quale documento viene ogni tratto**. Se entrambe le cartelle sono vuote, dillo chiaramente, proponi dal profilo demografico del video di riferimento e segnala che `/pm-brand-kit` lo fonderebbe correttamente.

Poi l'intake in **un messaggio**, e aspetta:
> 1. **Una foto di OGNI prodotto nell'ad.** Questo ne ha [N], ognuna con l'etichetta leggibile. Non posso descrivere un'etichetta e farla esistere: il testo stampato sopravvive solo se il modello lo vede.
> 2. **Il personaggio.** Dal tuo Brand DNA proporrei: [proposta]. Va bene o lo cambi?
> 3. **La stanza.** Il riferimento è girato in [categoria letta dall'anchor], quindi la tua sarà una [categoria] **diversa** — mai la loro stanza. Preferenze?
> 4. **Voce o musica?** Il render porta l'una o l'altra, **mai entrambe**.

La domanda 3 non chiede permesso: **la stanza si ricostruisce sempre**. Riusare il set del riferimento è riusare il suo girato, ed è l'unica cosa che questa skill non fa mai.

## Step 10 — Scrivi il prompt di swap
Template completo in `references/swap-and-render.md` §3. Anchor come immagine 1, foto prodotto come immagine 2. Riempi 4 slot: **personaggio**, **categoria di sfondo** (dall'anchor), **nuova stanza** della stessa categoria, **direzione della luce**. Tutto il resto del template è fisso e non si riformula.

**La stanza si sostituisce sempre, mai si tiene**: stessa specie di spazio, istanza diversa. Una camera da letto semplice diventa **un'altra** camera da letto semplice. E poiché la stanza cambia, **cambia la luce**: scrivila esplicitamente. Mai riportare "stessa illuminazione"/"stesso sfondo" — contraddice la sostituzione e il modello risponde incollando il soggetto sulla stanza nuova non illuminato, che legge come un ritaglio.

## Step 10.5 — Una foto prodotto copre davvero ogni beat?
Chiediti questo **prima** di spendere. Cammina la lista shot e scrivi ogni **vista del prodotto** che l'ad richiede: tappo che si toglie → prodotto aperto + tappo come oggetto separato · pump/contagocce/spray in scena → l'applicatore stesso, stappato, di fronte · prodotto capovolto che eroga → base/ugello + texture e colore · etichetta posteriore letta → retro e fianchi · sostanza su pelle/mano → texture e colore reali. Se le foto già presenti rispondono a tutte, **dillo e vai avanti** — non chiedere immagini che non ti servono.

## Step 11 — Scrivi il prompt di render
Riscrivi il prompt dello Step 7 per il personaggio e il prodotto dell'utente. **Numero di shot, timing, inquadrature, ritmo dei tagli e split on-camera/voiceover NON cambiano mai** — quella struttura è la cosa che vale ed è ciò che è stato misurato. Scrivi i blocchi Subject e Props per descrivere **lo still swappato approvato**, non il riferimento.

**Quando il prodotto nuovo funziona diversamente, cambiano le righe di azione.** Leggi ogni riga d'azione che tocca il prodotto e chiediti se il prodotto dell'utente può fisicamente farlo (gocce→stick = si passa direttamente; pump→spray = nebulizzazione, che dura 2-3 frame e vuole il suo shot). Due regole: **mai aggiungere o togliere shot** per adattare un meccanismo (assorbilo nei beat esistenti, il conteggio e il ritmo SONO la struttura) e **mai lasciare dialogo che descrive un meccanismo che l'immagine non mostra più**.

**🔒 Legge audio: voce O musica, mai entrambe.** Chiedere a un generatore un voiceover su un letto musicale dà un mix fangoso non separabile, e la musica è proprio la parte che vorresti cambiare. Voce scelta → solo voce + room tone, zero musica nel prompt (la traccia si mette dopo in editing, dove controlli livello e timing). Musica scelta → nessun voiceover, riga audio `Solo musica ambient. Nessun voiceover, nessun parlato.` **Vale anche quando il riferimento ha entrambe.**

Altri vincoli in `references/swap-and-render.md` §4: **720p è il tetto attuale**, il prompt sta fra 4.800 e 5.000 caratteri, le azioni fisiche discrete vogliono il loro shot o vengono perse.

## Step 11.5 — Solleva la tecnica di scrittura, riscrivi le parole per il brand
**Se il riferimento non ha parlato, salta e dillo.** Non inventare un voiceover per un ad che non ce l'aveva.

Altrimenti: le parole del riferimento sono dell'altro brand. **La tecnica** è ciò che si trasferisce.
1. **Nomina la tecnica**: funzioni dei beat e loro ordine (hook, scoperta, meccanismo, beneficio, lifestyle, pre-empt obiezione, prova, CTA) · **meccanismo dell'hook** (curiosità, prova sociale, domanda, claim, reveal) · stadio di awareness e punto di vista · **il passo** (parole/durata, riportato in wpm) · dove le frasi si rompono contro i tagli.
2. **Scrivi la loro** da `01_VOC_Research/*` e `02_Brand_DNA/*`, stessa tecnica nello stesso ordine, col linguaggio del brand. **Cita quale pain/desiderio VOC risponde a ogni beat.** Se le cartelle sono vuote, dillo e offri `/pm-dati-qualitativi` o `/pm-brand-kit` prima.

**Regole della riscrittura:** **mai portare una claim** (ingredienti, numeri di performance, premi, "clinicamente provato", menzioni stampa appartengono all'altro brand e sono molto probabilmente false per questo) · **allinea il budget parole alle durate misurate** e dichiara il numero in entrambi i modi ("il riferimento era 124 parole a 248 wpm; il tuo è 83 a 166") · **ri-distribuisci le parole sugli shot in codice**, mai a occhio · **tieni lo split on-camera/voiceover** misurato · **fai atterrare il significato sull'immagine giusta**.

Poi consegna: "Ecco il prompt completo col nuovo script. Cambia qualsiasi riga — mandami la riscrittura e ridistribuisco sulle inquadrature così i timing reggono." Se riscrive una riga, **ri-esegui la distribuzione**, non incollare le sue parole nei vecchi slot.

## Step 12 — Offri il path di render
Presenta la scelta col costo attaccato: **lo renderizza lui** (gli dai prompt + anchor + foto prodotto, zero spesa qui) oppure **Path B** (Higgsfield CLI) / **Path C** (fal.ai, serve `/pm-setup-fal-ai`) / **Path D** (Playwright). Leggi il saldo, quota il numero, **aspetta un sì esplicito. Un preventivo non è un'approvazione.**

---

## Regole hard

| Regola | Dettaglio |
|---|---|
| **Offri sempre le due route e aspetta** | Mai avviare l'analisi locale senza chiedere. Incolla il prompt locked per intero, mai parafrasato. |
| **Mai inventare un transcript** | Niente whisper locale = gli slot dialogo restano vuoti e dici perché. Uno script plausibile è peggio di un vuoto. |
| **Mai descrivere uno shot non visto** | |
| **Il nome del file non è una prova** | Identifica il prodotto dai frame. |
| **Riporta il conteggio che hai MISURATO** | Anche quando contraddice l'aspettativa dell'utente. Se il suo tool trovava 6 shot e la curva ne mostra 9, di' 9 e nomina i due tagli persi. |
| **Separa misurato da inferito** | In tutto ciò che riporti. |
| **Non aggiungere sezioni al template** | Niente Set/Location, niente Camera globale, niente campo Music. |
| **Ogni prodotto nell'ad vuole la SUA foto** | Mai far partire un render con un prodotto che il modello ha solo sentito descrivere. |
| **Voce O musica, mai entrambe** | La musica si mette dopo in editing. Vale anche se il riferimento aveva entrambe. |
| **Niente render senza un sì esplicito** | E l'utente vede prima il costo. |
| **720p è il tetto attuale** | Mai promettere 1080p o 4K. |
| **La struttura si trasferisce, il girato MAI** | Non un frame del riferimento, non la sua persona, non le sue stanze, non il suo prodotto, non il suo audio. |

## Trappole shell

- `tile` vuole `-frames:v 1` per un singolo foglio; per **più** fogli da una sequenza numerata usa `ffmpeg -start_number 1 -i "$D/s%02d.png" -vf "tile=8x2" "$D/GRID_%d.png"`.
- Estrai i frame di confronto con `select='eq(n,N)'`, **mai** `-ss` prima di `-i`.
- zsh non fa word-splitting sulle variabili non quotate: `set -- $PAIR` dentro un loop fallisce in silenzio. Usa liste esplicite.
- `rm -f inesistente*` aborta lo script sotto zsh. Proteggi o togli.
- Tagliare con `-t` + `-c copy` sfora di qualche frame. Usa `-frames:v N` quando il taglio deve essere esatto al frame.
