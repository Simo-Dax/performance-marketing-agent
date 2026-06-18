# Visual families e il render prompt template-structured

Questo file definisce le **5 visual families fisse** e la struttura di ogni render prompt. Lo Step 4 di `24_static_ads` carica questo file insieme a `40-templates.md` e scrive esattamente 5 prompt per concept approvato, uno per famiglia. Ogni prompt è costruito su un template chiamato per nome e mira a `$RENDER_MODEL` (GPT Image 2 di default; Nano Banana 2 solo per un 4:5 vero insistito).

Niente prompt edit-pass. Un render forte per variante. Se l'immagine va ritoccata, l'utente manda un follow-up normale nella conversazione col modello.

---

## Le 5 visual families

Ogni concept approvato riceve 5 render, uno per famiglia. Le famiglie **non** sono intercambiabili: ognuna persuade con un meccanismo diverso, quindi un set da 5 copre 5 leve di conversione distinte per la stessa idea.

### Family 1 — Product Hero
**Persuade con:** chiarezza e desiderio. Il prodotto è il focal point, presentato al massimo della sua attrattiva, con artigianalità massima e zero distrazione.
**Scena tipica:** superficie studio pulita o fondo a tinta brand, prodotto centrato o regola dei terzi, luce direzionale morbida, ombra intenzionale, palette brand.
**Cosa rende forte il render:** prodotto reso con **label fidelity assoluta** (ogni parola sul packaging combacia con la foto caricata), la luce rivela la qualità del materiale (matte vs gloss, texture, peso), la composizione sembra uno shooting editoriale, non un listing da marketplace.
**Da evitare:** superfici disordinate, mani/braccia in frame (quella è Family 5), decorazione astratta attorno al prodotto, colori brand sbagliati, geometria prodotto sfocata/deformata.

### Family 2 — Problem State
**Persuade con:** riconoscimento. Il viewer vede il proprio dolore reso visivamente in 1.5s e ferma lo scroll perché si riconosce.
**Scena tipica:** il cliente nel momento del dolore (non in agonia, nella versione quotidiana riconoscibile). Può essere una persona, un close-up del sintomo, o un ambiente che segnala il problema (scrivania incasinata, frigo mezzo vuoto, bagno poco illuminato).
**Cosa rende forte il render:** il dolore è abbastanza specifico che la persona target si riconosce subito, il visual evita horror medico o trigger di vergogna (performano peggio su traffico freddo), il framing lascia spazio all'headline overlay senza affollare il focal point.
**Da evitare:** energia "persona frustrata" da stock, distress finto, niente di giudicante verso il viewer, niente che richieda il prodotto visibile (il prodotto sta in Outcome State, non qui).

### Family 3 — Outcome State
**Persuade con:** aspirazione. Il viewer vede il "dopo", la sensazione desiderata, il "questo potrei essere io". Il prodotto è presente ma non focal point.
**Scena tipica:** il cliente post-prodotto, nel momento della vittoria. Una persona che vive il risultato (mattina più calma, focus al lavoro, sicuro allo specchio, energico all'aperto), o uno shot ambientale che segnala la vittoria senza mostrare la persona.
**Cosa rende forte il render:** il risultato è concreto e ancorato nel tempo (non "si sente bene" ma "sveglio alle 6", non "più energia" ma "focus netto entro le 10"), il prodotto è presente e identificabile ma secondario, la lettura emotiva è speranza/orgoglio/calma, non sorriso in posa.
**Da evitare:** staging finto "before/after", gioia da stock, prodotto fluttuante al centro (quella è Family 1), niente che implichi un risultato medico non claimabile legalmente.

### Family 4 — Proof or Mechanism
**Persuade con:** credibilità. Il viewer vede la prova che il prodotto funziona: dati, diagramma del meccanismo, breakdown ingredienti, comparativa, risultato visibile.
**Scena tipica:** stat callout attorno al prodotto, vista esplosa di ingredienti/componenti, side-by-side (noi vs alternativa), diagramma del meccanismo etichettato, immagine di risultato documentato.
**Cosa rende forte il render:** ogni numero/etichetta/ingrediente/elemento comparativo è **reale** (da VOC/Brand DNA/ad scrapati, mai inventato), il layout legge come informazione scannabile non come dato denso, il prodotto àncora la composizione senza essere coperto.
**Da evitare:** stat o studi fabbricati, finti "testato da [istituzione]", finte endorsement di dottori, finti before-after di lab, percentuali o citazioni di ricerca inventate. **FTC 2024 vieta tutto questo nei paid ads.**

### Family 5 — Identity or Social Proof
**Persuade con:** tribù e testimonianza. Il viewer vede una persona reale in cui si identifica, o altri clienti reali che confermano che il prodotto funziona.
**Scena tipica:** persona realistica che tiene/usa il prodotto (modalità Held di product-shot), selfie allo specchio UGC-style, review card screenshottata su foto lifestyle, layout testimonial cucito, commento Reddit/Instagram di un cliente su foto prodotto casual.
**Cosa rende forte il render:** la persona sembra un vero cliente di questo brand (non un modello stock, non un influencer generico), il copy testimonial viene da VOC reale (mai inventato), il layout legge come nativo della piattaforma che imita (un commento Instagram sembra un vero commento Instagram), l'identità brand resta intatta anche quando il formato è volutamente ruvido.
**Da evitare:** testimonial finti, attribuzioni review finte, foto di celebrity reali senza partnership, energia "gruppo diverso di persone sorridenti" da stock, UGC troppo patinato che sembra recitato.

---

## Il render prompt template-structured

Ogni prompt è costruito su un template per nome da `40-templates.md`. La famiglia è il **job di persuasione** che la variante deve fare; il template è la **struttura on-image concreta** che lo realizza. Costruisci ogni prompt in quest'ordine.

### 1. Seleziona il template per nome
Scegli il template (o template) che meglio serve l'angolo del concept e questa famiglia. **Mai per numero, sempre per nome**, qui e in ogni output. Pairing suggeriti (non vincolanti, usa giudizio):

- **Product Hero:** Headline · Hero Product Showcase + Stat Bar · Stat Surround / Callout Radial · Native / Ugly Post-It Note Style
- **Problem State:** Curiosity Gap + Scroll-Stopper Hook · Advertorial / Editorial Content Card · UGC + Viral Post Overlay
- **Outcome State:** Before & After (UGC Native) · Lifestyle Action + Product Colorway Array · Whiteboard Before / After + Product Hold
- **Proof or Mechanism:** Stat Surround / Callout Radial · Comparison Grid / Table · Us vs. Them Color Split · Feature Arrow Callout · Stat Callout
- **Identity or Social Proof:** Verified Review Card · Pull-Quote Review Card · Social Comment Screenshot + Product · Highlighted / Annotated Testimonial · UGC Lifestyle + Product + Review Card

### 2. Aggancia il prompt a un ad vincente reale del brand
Il template è un blueprint, non paint-by-numbers. Prima di scrivere, studia come appare un ad vincente *di questo brand specifico*: gli ad live scrapati, l'identità visiva Brand DNA (colori, type, logo, stile fotografico), e reference competitor/categoria (output spy in `03_Ad_Spy/` o ricerca di mercato). Adatta layout/palette/type/styling del template perché il risultato sia inequivocabilmente on-brand e spicchi nel feed. **Deviare dallo styling letterale del template è permesso e incoraggiato** quando rende l'ad più on-brand e meno generico. La bussola: ogni output deve sembrare **un vero ad fatto da un designer umano per questo brand**, non un template riempito.

### 3. Scrivi nella struttura del template
Ogni prompt porta:
- **Layout zonale.** Nomina cosa sta in ogni zona (top, center, bottom, o left/right), seguendo l'arrangiamento del template scelto.
- **Copy on-image tra virgolette.** Le parole esatte per ogni elemento testuale. Le headline vengono dalle 3 candidate del concept. Niente punto a fine headline. Niente testo CTA dentro l'immagine.
- **Spec fotografica e di luce.** Lente, angolo, sorgente luce, direzione, qualità, comportamento ombra. Anche un flatlay o un layout UI-chrome nomina il suo trattamento fotografico.
- **Formato UI-chrome se il template ne ha uno.** Review card, stat radial, comparison split, post-it, finto screenshot, comment card, masthead news — reso per sembrare nativo di ciò che imita.
- **Prop nominati.** I prop catalogati specifici da `$PROP_CATALOG` da featurare (uno, alcuni, o tutti). Mai "il prodotto" generico; nomina il prop ("il pouch kraft matte", "lo shaker in vetro e lo scoop bianco"). Solo prop presenti in `$PROP_CATALOG`.
- **La constraints line fissa** come riga finale.

Quando il template include uno slot stat/review/rating/stampa: riempilo solo con proof da VOC/Brand DNA/ad scrapati, oppure ometti lo slot. Il template è impalcatura, mai licenza per fabbricare proof.

### Constraints line (identica su ogni prompt, mai riscrivere)

```
Constraints: nessun punto a fine headline. Nessun bottone o testo CTA dentro l'immagine. Nessun AI-aesthetic tell (no gradienti viola-blu, no diagrammi orbitali, no forme geometriche fluttuanti, no finti riflessi di luce, no riempimenti arcobaleno over-saturi). Composizione mobile-first (soggetto e headline leggibili su crop da telefono). Ogni prop nominato reso con fedeltà assoluta alle immagini caricate (ogni parola, ogni carattere, colori esatti, materiale e forma corretti). Nessun rating fabbricato, nessun conteggio review fabbricato, nessun logo stampa fabbricato, nessun testimonial fabbricato. Render al formato scelto ($ASPECT_RATIO).
```

---

## Regole hard

1. Esattamente 5 varianti per concept. Una per famiglia. Mai più, mai meno.
2. Ogni variante è costruita su un template per nome e scritta nella sua struttura. **Mai citare un template per numero** in nessun output.
3. Template = blueprint, non paint-by-numbers. Aggancia ogni prompt a un ad vincente reale del brand e adatta lo styling. Deviare è permesso e incoraggiato.
4. La constraints line è identica su ogni variante. Mai riscriverla o accorciarla.
5. L'headline viene da una delle 3 candidate del concept. Varianti diverse dello stesso concept possono usare candidate diverse, ma ogni headline deve essere una di quelle che l'utente ha già visto.
6. Prop nominati per ad. Ogni variante nomina i prop catalogati specifici, con fedeltà assoluta alle foto. Mai "il prodotto" generico. Mai inventare un prop fuori da `$PROP_CATALOG`.
7. Nessun testo CTA dentro l'immagine. Le CTA vivono nel copy (skill SA7), non nel creativo.
8. Niente punto a fine headline. Le headline finiscono senza punteggiatura terminale. Punti interrogativi/esclamativi ammessi quando pertinenti.
9. Niente trattini come pausa di frase. Usa virgole, "e", o spezza la frase. Parole composte (pay-per-use) ok.
