# SA6 — Animate Static (statica → motion poster)

**Agente:** SA6 (Asset Production)
**Input:** una statica finita (da `04_Static_Ads/`, `07_Multiplied_Ads/`, `08_Rebuilt_Competitor_Ads/`, o un'immagine qualsiasi fornita dall'utente)
**Output:** `16_Animated_Statics/animated-[slug]-[YYYY-MM-DD].mp4` + il motion prompt `.txt` accanto
**Modello default:** Seedance 2.0 **image-to-video con la statica come PRIMO frame** (start image) — model-agnostic, vedi "best model available" in `execution/tools.md`
**Durata:** 3-8 secondi (default **4**) · **1080p default** (un motion poster si giudica su quanto atterra nitido il testo), 720p per risparmiare · **ratio = quello della statica**

Trasforma **una** statica finita in un **motion poster**: i layer della statica entrano in scena uno alla volta (headline che slamma, prodotto che compare, badge che atterrano) e **l'ultimo frame È esattamente la statica originale**. L'ad che si assembla da solo.

**Comportamenti provati su cui è costruita la ricetta:**
- Le sequenze di beat vengono obbedite con precisione (alternanze sinistra/destra, reveal dall'alto al basso).
- **Il testo display sopravvive perfettamente QUANDO il prompt lo pinna.** Il testo non pinnato viene ri-renderizzato e deriva.
- I numeri sopravvivono quando il prompt elenca **valori e lati esatti**. Mai lasciare le stat al caso.
- **Il micro-testo da packaging si ammorbidisce o si scioglie a QUALSIASI risoluzione.** È una proprietà del modello, non del prompt. **Avvisa, non promettere** (nemmeno il 1080p lo salva).
- I frame intermedi possono ballare; **è l'ultimo frame che atterra.** Blocca la camera, pretendi il match finale, e **giudica la clip dal suo atterraggio**.

> **Cos'è e cosa NON è.** È un layer di *animazione* sopra un asset già approvato — non genera un ad nuovo, non cambia il design, non aggiunge scene o storytelling. Se serve un video vero (parlato, UGC, script) → `25_ugc_prompt` o `55_video_script`. Se la statica non esiste ancora → prima `24_static_ads`.

---

## Regole non negoziabili

1. **La statica è l'unica fonte di verità.** Ogni parola, numero, logo ed elemento nella clip esiste già nell'immagine. Mai copy nuovo, claim nuove, badge nuovi o layout nuovo. **Mai "migliorare" l'ad.**
2. **L'ultimo frame deve combaciare col riferimento.** Ogni prompt chiude pretendendo che la clip si assesti nella composizione esatta della statica e **tenga**.
3. **Legge del testo pinnato.** Ogni headline, wordmark, CTA e stringa badge visibile va elencata **VERBATIM** nel blocco **HOLD/TEXT INTEGRITY**, con l'istruzione che resta pin-sharp e identica: mai ri-digitata, ri-spaziata, ri-letterata, spostata, sfumata o ri-illuminata (salvo che l'arrivo di quell'elemento SIA un beat approvato, e allora è pinnata da quando atterra).
4. **Legge dell'integrità numerica.** Se ci sono statistiche, prezzi, percentuali, rating o conteggi, il prompt elenca i **valori esatti E le loro posizioni/lati**, con l'istruzione che non vengono mai alterati, scambiati, ri-digitati o inventati.
5. **Camera bloccata.** Niente pan, zoom, riquadratura o movimento di camera per tutta la durata. **Solo movimento degli elementi.**
6. **Onestà sul micro-testo.** Se la statica si regge su body copy da packaging, **dillo PRIMA di spendere**: quel tipo si ammorbidirà a qualsiasi risoluzione, il display invece è sicuro. Lascia decidere con questo fatto sul tavolo.
7. **Una clip, 3-8s, default 4.** La durata segue i beat: **massimo ~2 beat al secondo**, 6-8 beat per 4s. Più beat = **raggruppa elementi in beat condivisi**, mai comprimere il ritmo.
8. **Il ratio della sorgente è il ratio dell'output.** Genera al ratio più vicino supportato (9:16, 1:1, 16:9, 4:3, 3:4); se non c'è match esatto, dillo e indica quale usi.
9. **Risoluzione: 1080p default**, 720p per risparmiare. Nessuna delle due risolve il micro-testo.
10. **Audio: mai musica.** Il modello aggiunge un letto musicale se non glielo vieti: chiudi ogni prompt con la formula no-music **più foley diegetico leggero sui beat** (pop, whoosh, tonfi, tap). **Mai voiceover.**
11. **Linguaggio positivo nei prompt** (dichiara cosa C'È in scena), con esattamente **due zone di negazione ammesse**: la riga Audio e il blocco HOLD/TEXT INTEGRITY.
12. **🚦 Gate costo prima di ogni render.** Qualsiasi cambio dopo l'approvazione (durata, risoluzione, concept, path) **la annulla**: ri-presenta e ri-approva.
13. **Scarica subito i risultati.** Un clip pagato e non scaricato è denaro perso.
14. **Questa skill non chiede mai documenti di ricerca** e non si blocca sulla loro assenza.

---

## Step 0 — Cartella + input

```bash
WORKDIR="$PWD"
mkdir -p "$WORKDIR/16_Animated_Statics"
```

Auto-discovery delle statiche disponibili (mostra le più recenti, l'utente sceglie):
```bash
ls -t "$WORKDIR/04_Static_Ads/"*.png "$WORKDIR/04_Static_Ads/path_"*"_outputs/"*.png 2>/dev/null | head -n 10
ls -t "$WORKDIR/07_Multiplied_Ads/"*.png "$WORKDIR/08_Rebuilt_Competitor_Ads/"*.png 2>/dev/null | head -n 10
```
Se l'utente fornisce direttamente un'immagine, usa quella. **Una statica per run** — questa skill anima un ad alla volta.

Se non trovi nessuna statica e l'utente non ne fornisce una → fermati: "Serve una statica finita da animare. Genera prima con `/pm-statiche`, o dammi l'immagine."

---

## Step 1 — Inventario dei layer (guarda davvero l'immagine)

**Leggi l'immagine col tool Read prima di scrivere qualsiasi cosa.** Poi inventaria OGNI elemento visivo distinto, perché l'animazione si costruisce su questi:

| Layer tipo | Cosa registrare |
|---|---|
| Sfondo | colore/texture/gradiente, se è una scena o un fondo piatto |
| Prodotto | cosa è, dove sta (posizione %), scala, orientamento |
| Headline | testo **verbatim**, posizione, peso/dimensione relativa |
| Sub-headline / body | testo verbatim, posizione |
| Badge / sticker / pill | testo verbatim, forma, posizione |
| Stat / numeri / prova | valore verbatim, posizione |
| CTA | testo verbatim, forma, posizione |
| Device grafici | frecce, cerchi disegnati, linee, annotazioni, ombre |
| Logo / marchio | posizione, dimensione |

Registra per ogni layer: **cosa è, dove sta (in percentuale), quanto pesa visivamente**. Questo inventario è la base del prompt di movimento — un layer non inventariato non può essere animato.

**Regola:** l'inventario descrive SOLO ciò che è realmente nell'immagine. Non aggiungere elementi che non ci sono (è animazione, non ridisegno).

---

## Step 2 — UNA domanda all'utente

> Hai già in mente come dovrebbe muoversi, o vuoi che ti proponga delle idee? (descrivi / proponi)

- **Descrive** → usa la sua idea come base del concept (Step 3 salta la generazione delle 3 pitch, ma passa comunque dalla struttura beat-by-beat).
- **Proponi** (o silenzio) → Step 3 completo.

---

## Step 3 — Tre concept di animazione (l'utente sceglie)

Genera **3 concept genuinamente diversi** per come l'ad si assembla. Diversi nell'**ordine di entrata** e nella **logica di movimento**, non solo nell'easing. Esempi di direzioni (non esaustivi, adatta ai layer reali):

- **Build gerarchico** — entra prima il fondo, poi il prodotto, poi headline, poi badge/CTA: l'occhio segue la gerarchia di lettura.
- **Hook-first** — la headline slamma per prima su fondo nudo, poi tutto il resto si costruisce intorno a lei.
- **Reveal del prodotto** — il prodotto entra per ultimo come punchline, tutto il resto lo "aspetta".
- **Snap sincronizzato** — pochi elementi entrano insieme a scatti ritmici, stile poster kinetico.

Presenta così (compatto, niente muri di testo):

```
CONCEPT 1: <nome>
Logica: <in una riga, perché quest'ordine>
Sequenza: <layer A entra a 0.0s> → <layer B a 0.6s> → ... → frame finale = la statica
```

Chiedi: "Quale? Puoi anche modificarlo (es. 'concept 2 ma il badge entra per ultimo')."

**Non procedere senza la scelta dell'utente.**

---

## Step 4 — Scrivi il motion prompt

Il prompt di movimento ha **una regola non negoziabile**:

> **L'ULTIMO FRAME DEVE ESSERE ESATTAMENTE LA STATICA ORIGINALE.** Nessun elemento spostato, ricolorato, riscritto o aggiunto rispetto all'immagine di partenza. Il video "atterra" sul design approvato.

Struttura del prompt (prosa, non zone/scaffold — coerente col resto delle nostre skill di produzione):

1. **Dichiarazione di partenza:** l'immagine allegata è il **primo frame** E la composizione di destinazione su cui la clip deve assestarsi.
2. **Beat sheet dei layer:** per ogni layer, *quando* entra (secondo), *come* entra (slide da quale direzione, scale-up, fade, snap, pop) e *dove atterra* (la sua posizione nella statica).
3. **Regole di chiusura:** l'ultimo ~0.5s è statico sul design completo (il "landing"), niente movimento residuo, niente overshoot che sposta i layer dalla loro posizione finale.
4. **Blocco HOLD/TEXT INTEGRITY:** ogni stringa **verbatim** + ogni valore numerico **col suo lato**, pin-sharp e immutabili (regole 3-4).
5. **Camera lock** esplicito (regola 5).
6. **Riga Audio:** formula no-music + foley diegetico sui beat, mai voiceover (regola 10).
7. **Divieti** (solo nelle due zone ammesse dalla regola 11): niente musica, niente caption generate, niente testo nuovo, niente elementi assenti dalla statica, niente cambio palette o crop.

**Timing:** distribuisci gli ingressi sul budget durata scelto lasciando l'ultimo mezzo secondo di "riposo" sul frame finale. Con 4s (default): ingressi tra 0.0s e ~3.4s, poi statico.

Mostra il prompt completo all'utente **prima** di renderizzare.

---

## Step 5 — Parametri + 🚦 gate costo

Chiedi (proponendo i default):
1. **Durata:** 3-8s (default **4** — il punto dolce: abbastanza per costruire, abbastanza corto da non annoiare).
2. **Risoluzione:** 720p default · **1080p** se la statica ha molto testo fine (più nitido, costa di più).

Poi **🚦 gate obbligatorio**: mostra il costo stimato della generazione e attendi un `sì` esplicito. **Mai renderizzare senza conferma.**

---

## Step 6 — Genera (4 percorsi)

> **Contratto tecnico comune:** image-to-video con la statica come **letterale PRIMO frame** (start image). L'atterraggio sul design non viene da un end-frame conditioning ma **dal prompt**, che pretende esplicitamente che la composizione si assesti sulla statica e tenga (regola 2). Audio generato dal modello secondo la riga Audio del prompt: **non caricare mai audio**.

Chiedi quale percorso:

> **A. Manuale.** Gratis. Ti do il prompt: lo incolli nel tool video che preferisci (Higgsfield, Kling, Runway), alleghi la statica, generi, e mi rimetti la clip.
> **B. Higgsfield.** Meglio con abbonamento Higgsfield. Genero io direttamente.
> **C. fal.ai.** Pay-per-video, nessun abbonamento. Serve `/pm-setup-fal-ai`.

**Path C (fal.ai) — parametri:**
1. `mcp__fal-ai__upload` della statica → URL.
2. `mcp__fal-ai__generate` sull'endpoint image-to-video della famiglia Seedance 2.0, `input_data`: `prompt` (il motion prompt), la statica nello slot **primo-frame/image** (verifica model id e nomi campo con `mcp__fal-ai__find` prima di chiamare, gli schemi cambiano), durata e risoluzione approvate.
3. Poll con `mcp__fal-ai__result`, scarica l'mp4.

**Path B (Higgsfield CLI):** la statica va su `--start-image "<path>"` così diventa il primo frame letterale; `--aspect_ratio`, `--resolution`, `--duration` (intero). **L'audio è automatico, non c'è un flag audio.** Conferma la tariffa live prima della riga di costo del gate.

**Verifica modello prima di generare:** skill **model-agnostic**. Se esiste un image-to-video migliore (`mcp__fal-ai__search` categoria `image-to-video`), preferiscilo dicendolo — principio "best model available" (`execution/tools.md`).

---

## Step 7 — Consegna + validazione

Salva:
```
16_Animated_Statics/animated-[slug]-[YYYY-MM-DD].mp4
16_Animated_Statics/animated-[slug]-[YYYY-MM-DD].txt   ← il motion prompt completo, per ri-renderizzare o ritoccare
```

**Validazione prima di dichiarare fatto:**
1. Il file mp4 esiste e non è vuoto.
2. La durata è quella richiesta (±0.5s).
3. **L'ultimo frame combacia con la statica originale.** Estrailo e confrontalo:
   ```bash
   ffmpeg -y -sseof -0.1 -i "<video>" -frames:v 1 "/tmp/lastframe.jpg" 2>/dev/null
   ```
   Leggi `/tmp/lastframe.jpg` col tool Read e confrontalo con la statica di partenza. Se il frame finale ha testo diverso, elementi spostati, o palette cambiata → **è il fallimento tipico di questa skill**: dillo onestamente all'utente e offri un re-render con il vincolo di end-frame rinforzato nel prompt. Non spacciare per riuscito un video che atterra su un design diverso.
4. Il `.txt` col prompt esiste accanto al video.

Riepilogo finale: path del video + path del prompt + una riga su cosa fare dopo ("ritocca il prompt e ri-renderizza, oppure caricalo come variante video dell'ad statica — stesso messaggio, formato diverso").

---

## Regole hard

| Regola | Dettaglio |
|---|---|
| **L'ultimo frame è la statica** | È il senso della skill. Un video che atterra su un design diverso è fallito, va rigenerato o riportato onestamente come fallito. |
| **Anima, non ridisegnare** | Nessun elemento nuovo, nessun testo nuovo, nessun cambio di palette/crop. Solo i layer che esistono già nella statica. |
| **Guarda l'immagine** | Inventario layer col tool Read prima di scrivere il prompt. Mai animare da una descrizione a memoria. |
| **Niente musica, niente caption** | Output pulito: solo movimento. L'audio e i sottotitoli sono decisioni di editing successive. |
| **Una statica per run** | Per animare più ad, run separate (o chiedi conferma esplicita per un batch e applica comunque il gate costo per ognuno). |
| **🚦 Gate costo sempre** | Concept approvato + prompt mostrato + costo confermato PRIMA di ogni render. Mai addebitare senza `sì`. |
| **Model-agnostic** | Il default è un default, non un vincolo: serve un image-to-video che accetti una start image. Preferisci il migliore disponibile e dillo. |
