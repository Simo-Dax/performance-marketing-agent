# SA6 — Static Ads (Render Prompts evidence-driven)

**Agente:** SA6 (Asset Production)
**Input:** concept approvati da SA5 (`intermediate/sa5_creative_framework.md`) + Brand DNA + VOC + foto prodotto
**Output:** `04_Static_Ads/static-concepts-[YYYY-MM-DD].md` (testo) + immagini opzionali
**Modello default:** GPT Image 2 (`openai/gpt-image-2`) per ogni ratio. Nano Banana 2 solo per 4:5 vero insistito.
**Reference:** `visual-families.md` (le 5 famiglie + struttura prompt) · `40-templates.md` (libreria template per nome)

---

## Cambio di filosofia (v2)

Questa skill **non riempie più 40 template alla cieca**. Riceve i **concept approvati da SA5** e, per ogni concept, scrive **5 render prompt** — uno per ognuna delle 5 visual families. Ogni prompt è costruito su un **template chiamato per nome** (dalla libreria `40-templates.md`), ma il template è un **blueprint, non paint-by-numbers**: prima di scrivere si studia un ad vincente reale del brand e si **devia dallo styling letterale** del template per ottenere un risultato che sembra fatto da un designer umano, non un template riempito.

> Regola-bussola: ogni output deve sembrare **un vero ad creato da un designer per questo brand**, non un template compilato.

Se SA5 non ha girato (skill usata standalone), la skill può ancora lavorare da Brand DNA + VOC + foto prodotto, ma i "concept" vanno almeno abbozzati con le 4 mappe di SA5 prima dei render prompt.

---

## Step 0 — Auto-discovery input

```bash
ls -t "$WORKDIR/intermediate/sa5_creative_framework.md" 2>/dev/null | head -n 1
ls -t "$WORKDIR/01_VOC_Research/"*.html "$WORKDIR/01_VOC_Research/"*.md 2>/dev/null | head -n 1
ls -t "$WORKDIR/02_Brand_DNA/"*.html "$WORKDIR/02_Brand_DNA/"*.md 2>/dev/null | head -n 1
```

Cattura:
- `$CONCEPTS` — i concept approvati da SA5 (con: nome, big idea, awareness, hook, persona, citazione VOC, visual direction, 3 headline candidate, perché funziona)
- `$BRAND_DNA`, `$VOC` (testo)
- `$BRAND_ADS` — ad live del brand da `03_Ad_Spy/` se presenti (per il grounding "ad vincente reale")

---

## Step 1 — Intake (2 cose mancanti)

Chiedi solo ciò che non è derivabile:

1. **Foto prodotto** — 1+ immagini reference del prodotto.
2. **Aspect ratio** — formato finale dell'ad: `4:5`, `1:1`, `9:16`, o Altro (es. `16:9`, `3:4`).

---

## Step 1a — Catalogo prop prodotto (`$PROP_CATALOG`)

Subito dopo aver ricevuto le foto, **ispeziona visivamente ogni immagine** e cataloga gli **asset fisici reali** che mostra. Leggi cosa c'è davvero nelle foto, non una descrizione generica. Asset tipici: pouch stand-up, shaker in vetro, scoop in plastica, scatola retail, capsule/gummies sfuse, barattolo con coperchio, bustina, flacone con contagocce, blister, tubo, barretta nel wrapper.

Per ogni asset distinto registra: **nome concreto breve** + testo dell'etichetta + dettagli visivi leggibili (colore, materiale, finitura, parole esatte sul packaging). Esempio:

- pouch stand-up, kraft matte, fronte recita "[testo etichetta esatto]"
- shaker in vetro trasparente con tappo in acciaio
- scoop bianco in plastica
- capsule sfuse marrone cioccolato

`$PROP_CATALOG` è il **menu dei prop reali disponibili**. Lo Step 4 sceglie quali featurare in ogni ad (uno, alcuni, o tutti) in base ad angolo e template. **Mai inventare un prop che non è nelle foto.** Se è stato caricato un solo asset, il catalogo ha una voce e ogni ad usa quella.

---

## Step 1b — Aspect ratio + renderer (`$ASPECT_RATIO`, `$RENDER_MODEL`)

GPT Image 2 è il **default** e la scelta raccomandata. Regge ogni ratio supportato (1:1, 9:16, 4:3, 3:4, 16:9, 3:2, 2:3). Per tutti questi → `$RENDER_MODEL = gpt-image-2`.

GPT Image 2 **non** produce un 4:5 vero. Il suo portrait più vicino è 3:4:
- Se l'utente sceglie 4:5: "GPT Image 2 non produce un 4:5 vero. Il portrait più vicino è 3:4, che nel feed Meta legge quasi identico. Consiglio 3:4 su GPT Image 2. Va bene 3:4, o ti serve un 4:5 vero?"
- Se accetta 3:4 (o non insiste): `$ASPECT_RATIO = 3:4`, `$RENDER_MODEL = gpt-image-2`.
- Solo se insiste su 4:5 vero e rifiuta 3:4: `$ASPECT_RATIO = 4:5`, `$RENDER_MODEL = nano-banana-2` (solo per questa run).

Nano Banana 2 **non** è un'opzione generale o co-equa. È un fallback stretto per il 4:5 vero insistito. Per ogni altro ratio il renderer è GPT Image 2, punto.

---

## Step 2 — Le 5 visual families

Carica `visual-families.md`. Ogni concept approvato riceve **5 render**, uno per famiglia. Le famiglie non sono intercambiabili: ognuna persuade con un meccanismo diverso, quindi un set da 5 copre 5 leve di conversione distinte per la stessa idea.

1. **Product Hero** — chiarezza e desiderio. Prodotto focal point, label fidelity assoluta, luce che rivela il materiale.
2. **Problem State** — riconoscimento. Il cliente vede il proprio dolore in 1.5s. Niente prodotto in frame.
3. **Outcome State** — aspirazione. Il "dopo" concreto e ancorato nel tempo. Prodotto presente ma secondario.
4. **Proof or Mechanism** — credibilità. Stat/diagramma/comparativa/ingredienti. Ogni numero reale.
5. **Identity or Social Proof** — tribù e testimonianza. Persona reale o review nativa. Copy testimonial dal VOC reale.

Dettaglio completo (cosa rende forte ogni render, cosa evitare) in `visual-families.md`.

---

## Step 3 — Selezione template per nome

Per ogni variante, scegli dalla libreria `40-templates.md` il **template per nome** (mai per numero, né qui né in output) che meglio serve l'angolo del concept e il job della famiglia. Pairing suggeriti (non vincolanti, usa giudizio):

- **Product Hero:** Headline · Hero Product Showcase + Stat Bar · Stat Surround / Callout Radial · Native / Ugly Post-It Note Style
- **Problem State:** Curiosity Gap + Scroll-Stopper Hook · Advertorial / Editorial Content Card · UGC + Viral Post Overlay
- **Outcome State:** Before & After (UGC Native) · Lifestyle Action + Product Colorway Array · Whiteboard Before / After + Product Hold
- **Proof or Mechanism:** Stat Surround / Callout Radial · Comparison Grid / Table · Us vs. Them Color Split · Feature Arrow Callout · Stat Callout
- **Identity or Social Proof:** Verified Review Card · Pull-Quote Review Card · Social Comment Screenshot + Product · Highlighted / Annotated Testimonial · UGC Lifestyle + Product + Review Card

---

## Step 4 — Scrittura dei 5 render prompt per concept

Per ogni concept approvato, scrivi 5 prompt in quest'ordine di lavoro:

1. **Seleziona il template per nome** (Step 3).
2. **Aggancia il prompt a un ad vincente reale del brand.** Il template è un blueprint. Prima di scrivere, studia come appare un ad vincente *di questo brand specifico*: ad live scrapati (`03_Ad_Spy/` / `$BRAND_ADS`), identità visiva Brand DNA (colori, type, logo, stile fotografico), reference competitor/categoria. Adatta layout/palette/type/styling del template perché il risultato sia inequivocabilmente on-brand e spicchi nel feed. **Deviare dallo styling letterale del template è permesso e incoraggiato** quando rende l'ad più on-brand e meno generico.
3. **Scrivi nel formato strutturale del template:** layout zonale esplicito (top/center/bottom o left/right, nominando cosa sta in ogni zona) · il copy on-image esatto **tra virgolette** per ogni elemento testuale · spec fotografica e di luce (lente, angolo, direzione e qualità della luce) · il formato UI-chrome che il template richiede (review card, stat radial, comparison split, post-it, screenshot finto, comment card, masthead news…).
4. **Nomina i prop specifici.** Ogni prompt nomina quali prop da `$PROP_CATALOG` featurare (uno, alcuni, o tutti). Sostituisci ogni "il prodotto" generico con il callout specifico ("il pouch kraft matte", "lo shaker in vetro e lo scoop bianco"). Solo prop presenti in `$PROP_CATALOG`.
5. **Headline dalle candidate del concept.** Ogni headline usata deve essere una delle 3 candidate che SA5 ha già prodotto per quel concept. Varianti diverse dello stesso concept possono usare candidate diverse.

Quando un template prevede uno stat / conteggio review / rating / slot stampa: riempilo **solo** con proof da VOC/Brand DNA/ad scrapati. Se non esiste un numero reale, **ometti lo slot** invece di inventarlo. Il template è impalcatura strutturale, mai licenza per fabbricare social proof.

Un solo render forte per variante (no prompt edit-pass). Render a `$ASPECT_RATIO`.

---

## Step 5 — Output finale (testo)

Stampa ogni concept con i suoi 5 prompt. Layout esatto:

```
CONCEPT APPROVATO 1: <nome concept>

VARIANTE 1.1, Product Hero, template: <nome template>
Layout: <layout zonale, cosa in ogni zona, con il copy on-image tra virgolette>
Soggetto e prop: <i prop catalogati specifici featurati, per nome>
Fotografia: <lente, angolo, direzione e qualità luce, stile e medium>
Mood e colore: <lettura emotiva e palette brand>
Testo: <l'headline tra virgolette, una delle candidate, con posizione e peso>
Constraints: <la constraints line fissa>

VARIANTE 1.2, Problem State, template: <nome template>
<stessa struttura>

VARIANTE 1.3, Outcome State, template: <nome template>
VARIANTE 1.4, Proof or Mechanism, template: <nome template>
VARIANTE 1.5, Identity or Social Proof, template: <nome template>

---
CONCEPT APPROVATO 2: <nome concept>
<stessa struttura, 5 varianti>
```

Salva copia su disco: `04_Static_Ads/static-concepts-[YYYY-MM-DD].md`.

### Constraints line (identica su ogni variante, mai riscrivere/accorciare)

```
Constraints: nessun punto a fine headline. Nessun bottone o testo CTA dentro l'immagine. Nessun AI-aesthetic tell (no gradienti viola-blu, no diagrammi orbitali, no forme geometriche fluttuanti, no finti riflessi di luce, no riempimenti arcobaleno over-saturi). Composizione mobile-first (soggetto e headline leggibili su crop da telefono). Ogni prop nominato reso con fedeltà assoluta alle immagini caricate (ogni parola, ogni carattere, colori esatti, materiale e forma corretti). Nessun rating fabbricato, nessun conteggio review fabbricato, nessun logo stampa fabbricato, nessun testimonial fabbricato. Render al formato scelto ($ASPECT_RATIO).
```

---

## Percorsi generazione

```
A. Manuale — copia i prompt, incolla nel modello web ($RENDER_MODEL), allega foto prodotto
B. Higgsfield CLI — richiede subscription
C. Fal.ai — ~$0.15/img GPT Image 2 high+4K
D. Playwright — guida automatica ChatGPT (GPT Image 2) o AI Studio (Nano Banana 2)
```

**Subset picker obbligatorio (Path B/C/D)** — mai generare tutto in automatico:
> "Ho <N> concept e <N×5> varianti pronte. Quali genero? Rispondi con coppie concept.variante separate da virgola (es. '1.1, 1.3, 2.4'), o 'tutto concept 1', o 'tutti'."

### Path C — Fal.ai (parametri)

1. `mcp__fal-ai__upload_file` per ogni foto → `$PRODUCT_URLS`.
2. Per ogni coppia, branch su `$RENDER_MODEL`:

**GPT Image 2 (default):** `model: "openai/gpt-image-2/edit"`, `image_urls: $PRODUCT_URLS`, `image_size` dalla tabella, `quality: "high"`, `output_format: "png"`, `num_images: 1`. **NON passare `safety_tolerance`.**

| `$ASPECT_RATIO` | `image_size` |
|---|---|
| `1:1` | `{"width": 2880, "height": 2880}` |
| `9:16` | `{"width": 2160, "height": 3840}` |
| `16:9` | `{"width": 3840, "height": 2160}` |
| `3:4` | `{"width": 2400, "height": 3200}` |
| `4:3` | `{"width": 3200, "height": 2400}` |
| `2:3` | `{"width": 2160, "height": 3240}` |
| `3:2` | `{"width": 3240, "height": 2160}` |
| altro | calcola width/height del ratio, lato lungo ≤3840, totale ≤8.294.400 px, arrotonda a pari |

**Nano Banana 2 (solo 4:5 vero insistito):** `model: "fal-ai/nano-banana-2"`, `aspect_ratio: "4:5"`, `resolution: "4K"`, `thinking_level: "high"`, `enable_web_search: true`, `safety_tolerance: "4"`, `output_format: "png"`, `num_images: 1`, `image_urls: $PRODUCT_URLS`.

Report ogni 5: "5 di N completati. Continuo? (yes/stop)". Manifest in `04_Static_Ads/path_c_outputs/manifest.json`.

### Path D — Playwright (regole hard)
1. Mai caricare media automaticamente — ogni upload richiede `yes`.
2. Mai cliccare Genera senza conferma — `yes go` per ogni variante.
3. Una variante alla volta.

---

## Regole critiche

- **5 varianti per concept** — esattamente 5, una per famiglia. Mai più, mai meno.
- **Template per nome, mai per numero** — in skill e in output. I numeri in `40-templates.md` sono solo navigazione umana.
- **Template = blueprint, non paint-by-numbers** — studia un ad vincente reale del brand e adatta lo styling. Deviare è permesso e incoraggiato.
- **Prop nominati per ad** — mai "il prodotto" generico, solo prop reali da `$PROP_CATALOG`.
- **Headline solo dalle candidate del concept** — quelle che SA5 ha già prodotto.
- **No proof fabbricato** — stat/review/rating/stampa solo se sourced, altrimenti slot omesso.
- **No punto a fine headline · no CTA dentro l'immagine.**
- **GPT Image 2 default** — Nano Banana 2 solo per 4:5 vero insistito.
- **Mai switch silenzioso di percorso · mai addebitare crediti senza `yes`.**
- **Salva ogni output su disco** in `04_Static_Ads/path_X_outputs/`.

---

## Validazione output

1. Output testo: ogni concept con tutte e 5 le varianti nel formato template-structured.
2. Copia su disco `04_Static_Ads/static-concepts-[YYYY-MM-DD].md` esiste e non è vuota.
3. Ogni prompt: nome template + layout zonale + copy on-image tra virgolette + spec fotografica + constraints line.
4. Ogni variante nomina prop specifici da `$PROP_CATALOG`, mai "il prodotto".
5. Ogni headline è una delle 3 candidate del concept.
6. Nessun placeholder residuo (`<TODO>`, `[BRACKETS]`, lorem ipsum).
7. Nessun template citato per numero. Solo per nome.
8. Ogni constraints line render a `$ASPECT_RATIO`.
