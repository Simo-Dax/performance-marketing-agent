# SA6 — Animate Static (statica → motion poster)

**Agente:** SA6 (Asset Production)
**Input:** una statica finita (da `04_Static_Ads/`, `07_Multiplied_Ads/`, `08_Rebuilt_Competitor_Ads/`, o un'immagine qualsiasi fornita dall'utente)
**Output:** `16_Animated_Statics/animated-[slug]-[YYYY-MM-DD].mp4` + il motion prompt `.txt` accanto
**Modello default:** Seedance 2.0 image-to-video (`bytedance/seedance-2.0/image-to-video`) con **start+end frame** — model-agnostic, vedi principio "best model available" in `execution/tools.md`
**Durata:** 3-8 secondi (default **4**) · **niente musica, niente caption** · 720p default, 1080p per testo più nitido

Trasforma **una** statica finita in un **motion poster**: i layer della statica entrano in scena uno alla volta (headline che slamma, prodotto che compare, badge che atterrano) e **l'ultimo frame È esattamente la statica originale**. L'ad che si assembla da solo.

> **Cos'è e cosa NON è.** È un layer di *animazione* sopra un asset già approvato — non genera un ad nuovo, non cambia il design, non aggiunge scene o storytelling. Se serve un video vero (parlato, UGC, script) → `25_ugc_prompt` o `55_video_script`. Se la statica non esiste ancora → prima `24_static_ads`.

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

1. **Dichiarazione di partenza:** che l'immagine allegata è il frame finale di destinazione e va riprodotta fedelmente.
2. **Beat sheet dei layer:** per ogni layer, *quando* entra (secondo), *come* entra (slide da quale direzione, scale-up, fade, snap, pop) e *dove atterra* (la sua posizione nella statica).
3. **Regole di chiusura:** l'ultimo ~0.5s è statico sul design completo (il "landing"), niente movimento residuo, niente overshoot che sposta i layer dalla loro posizione finale.
4. **Divieti espliciti:** niente musica, niente caption/sottotitoli generati, niente nuovo testo, niente elementi non presenti nella statica, niente cambio di palette o crop.

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

> **Contratto tecnico comune:** si usa un modello **image-to-video con start+end frame conditioning**, passando la statica **sia come primo sia come ultimo frame** (o come frame finale, a seconda dell'endpoint) — è ciò che garantisce l'atterraggio esatto sul design. Se il modello scelto non supporta l'end-frame, dillo all'utente: senza quel controllo il frame finale non sarà fedele e la skill perde il suo punto.

Chiedi quale percorso:

> **A. Manuale.** Gratis. Ti do il prompt: lo incolli nel tool video che preferisci (Higgsfield, Kling, Runway), alleghi la statica, generi, e mi rimetti la clip.
> **B. Higgsfield.** Meglio con abbonamento Higgsfield. Genero io direttamente.
> **C. fal.ai.** Pay-per-video, nessun abbonamento. Serve `/pm-setup-fal-ai`.

**Path C (fal.ai) — parametri:**
1. `mcp__fal-ai__upload` della statica → URL.
2. `mcp__fal-ai__generate` con `app_id: "bytedance/seedance-2.0/image-to-video"`, `input_data`: `prompt` (il motion prompt), l'immagine come **start frame** e come **end frame** (nomi campo secondo lo schema corrente dell'endpoint — verificalo con `mcp__fal-ai__find` prima di chiamare, gli schemi cambiano), durata e risoluzione scelte, **audio disabilitato** se il modello lo espone.
3. Poll con `mcp__fal-ai__result`, scarica l'mp4.

**Path B (Higgsfield):** stesso prompt e stessa logica start/end frame tramite il suo image-to-video.

**Verifica modello prima di generare:** questa skill è **model-agnostic**. Controlla se esiste un modello migliore per il caso (`mcp__fal-ai__search` categoria `image-to-video`, cerca il supporto start/end frame) e preferiscilo, dicendolo all'utente — principio "best model available" (`execution/tools.md`).

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
| **Model-agnostic** | Il modello di default è un default, non un vincolo: serve start+end frame conditioning. Preferisci il migliore disponibile e dillo. |
