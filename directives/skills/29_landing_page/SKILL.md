# Post-SA7 — Landing Page Generator (Meta Ad → HTML)

**Agente:** Post-SA7 (eseguito dopo copy e creative)
**Output:** `10_Landing_Pages/landing-page-[YYYY-MM-DD-HHMMSS].html`
**Dipende da:** VOC (`01_VOC_Research/`) + Brand DNA (`02_Brand_DNA/`) — obbligatori
**Reference co-locate (consultare):** `section-library.md` (libreria sezioni), `conversion-patterns.md`, `34-tells.md` (anti-AI slop audit), `dtc-route.md` / `leadgen-route.md` (struttura per business model), `voc-injection-map.md` (dove iniettare il VOC), `brand-dna-parsing.md`.

---

## Regola hard

Questa skill produce UN solo artefatto: un file HTML self-contained salvato in `10_Landing_Pages/`. Non chiama Meta MCP, non deploya, non pusha su Shopify o Cloudflare. Il deploy spetta al membro.

---

## Perché questa skill esiste

Benchmark Imprint LA: lander dedicati convertono ~15% su traffico Meta vs 1-2% per homepage. Ogni altra slot sulla pagina ha una regola hardcoded sul tipo di contenuto: H1 = echo dell'headline dell'ad, subheadline = outcome cliente, problem agitation = citazione verbatim cliente con attribution, FAQ = parole esatte del cliente (mai riscrittura marketer).

---

## Step 0a — Protezione cartella

```bash
mkdir -p "$TARGET/10_Landing_Pages" "$TARGET/_meta"
```

## Step 0b — Auto-discovery input

Cerca:
- `01_VOC_Research/` — VOC più recente (HTML o markdown) — **obbligatorio**
- `02_Brand_DNA/` — Brand DNA più recente — **obbligatorio**
- `04_Static_Ads/`, `07_Multiplied_Ads/`, `08_Rebuilt_Competitor_Ads/` — ad outputs (opzionale)
- `06_Ad_Copy/` — copy deck più recente (opzionale, fallback per headline se ad non ha testo leggibile)

Se VOC o Brand DNA MANCANTI → rifiuta:
- Nessun VOC → "Esegui prima la skill `18_voc_research`"
- Nessun Brand DNA → "Esegui prima la skill `21_brand_dna`"

Non inventare mai input mancanti.

---

## Step 1 — Intake ad creative

> "Costruirò la landing page dai tuoi VOC e Brand DNA in questa cartella. Ho ancora bisogno del creative dell'ad. Tre opzioni:
> 1. Incolla/carica l'immagine dell'ad Meta vincente
> 2. Indica un file da `04_Static_Ads/`, `07_Multiplied_Ads/` o `08_Rebuilt_Competitor_Ads/`
> 3. Descrivi l'ad in 2-3 frasi se non hai l'immagine
>
> Opzionali:
> a. URL target del CTA principale
> b. Average Order Value (DTC) o valore della lead"

---

## Step 2 — Analisi creative

Estrai e mostra al membro per conferma:

```
Headline Ad (verbatim): "..."
Soggetto Visivo Dominante: <persona / prodotto / scena lifestyle / solo testo>
Color Story: <3-5 hex dall'immagine o "non applicabile">
Promessa/Hook: <frase singola>
Awareness Level: <unaware / problem aware / solution aware / product aware / most aware>
Intent Traffico Probabile: <impulso DTC / DTC considerato / lead capture / demo>
Prezzo nell'Ad: <sì con anchor $XX, o no>
```

Chiedi conferma. L'**headline verbatim** è il campo più importante — il rule H1 message match dipende da essa.

---

## Step 3 — Routing DTC vs Lead Gen

Priorità:
1. Brand DNA dichiara esplicitamente `business_model`
2. Ad contiene prezzo/packshot/"Shop Now"/"Add to Cart" → DTC
3. Ad contiene "Book a demo", "Free consultation", "Sign up" → lead gen
4. Chiedi: "È un acquisto prodotto (DTC) o lead capture/booking (lead gen)?"

Annuncia routing per consentire override.

---

## Step 4 — Copy con VOC injection

Genera il copy slot per slot seguendo la mappa injection:

**Regole hard:**
- **H1 message match — non negoziabile:** H1 deve contenere almeno una frase di 3+ parole dall'headline dell'ad verbatim
- **Livello lettura:** target sotto la 7a elementare (dati Unbounce 2024: 5a-7a elementare = 12.9% conversione vs 2.1% professionale)
- **Budget parole:** 250-725 parole totali (hard ceiling 800)
- **Frasi vietate:** revolutionize, unlock, seamless, leverage, supercharge, game changer, harness, empower, elevate, transformative, paradigm shift, holistic, robust, scalable, synergistic + qualsiasi frase dalla voice.avoid del Brand DNA
- **Zero numeri inventati:** ogni customer count, recensione, star rating o testimonial viene da VOC o Brand DNA. Se un numero non è in nessuno dei due documenti, scrivi la sezione senza di esso

---

## Step 5 — Design con brand tokens

Estrai dal Brand DNA le CSS custom properties:

```css
:root {
  --brand-primary: <dal Brand DNA>;
  --brand-accent: <dal Brand DNA>;
  --brand-ink: <dal Brand DNA>;
  --brand-paper: <dal Brand DNA>;
  --brand-muted: <dal Brand DNA>;
}
```

Importa font dal Brand DNA via Google Fonts. Applica con Tailwind.

---

## Step 6 — Assembly HTML e self-audit

Il file deve contenere, in ordine:
1. DOCTYPE, html con `lang` e `scroll-smooth`, head, body
2. Tailwind Play CDN in head
3. Google Fonts preconnect + stylesheet in head
4. CSS custom properties `:root` con 5 brand tokens
5. Open Graph tags, Twitter card, viewport, favicon
6. Meta Pixel scaffold con `REPLACE_WITH_YOUR_PIXEL_ID`, PageView on load
7. Sezioni nel corretto ordine (DTC o lead gen route)
8. FAQ JSON-LD schema (se sezione FAQ inclusa)
9. Mobile sticky CTA bar (obbligatorio DTC, opzionale lead gen)
10. Footer minimale (copyright, privacy, terms, contact)
11. Marker `<!-- ====== EDIT: <SLOT> ====== -->` su ogni blocco editabile
12. Placeholder `REPLACE_WITH_*` per tutti i valori da sostituire
13. 5 blocchi A/B variant commentati al fondo

**Pre-ship audit obbligatorio prima di scrivere il file:**
```
Pre-ship audit:
  H1 message match (frase 3+ parole dall'headline ad): PASS / FAIL
  Livello lettura sotto 7a elementare: PASS / FAIL
  Word count 250-725: <N> ... PASS / FAIL
  Frasi vietate: NESSUNA / <lista>
  Esattamente 1 CTA destination: PASS / FAIL
  Brand tokens (5): PASS / FAIL
  2 famiglie font (1 display + 1 body): PASS / FAIL
  Mobile sticky CTA (DTC): PASS / FAIL
  Meta Pixel placeholder: PASS / FAIL
  Nessun image ref rotto: PASS / FAIL
  Nessun link nav esterno off-page: PASS / FAIL
  Nessun lorem ipsum: PASS / FAIL
```

Se qualcosa è FAIL → fix in memoria prima di scrivere. Non consegnare con tell noti.

---

## Step 7 — Istruzioni deployment

```
Fatto. Salvato in: <path assoluto>

Prossimi passi:
1. Preview locale — apri il file .html in qualsiasi browser. Nessun build step.
2. Deploy — trascina su Cloudflare Pages, Netlify Drop, o carica come pagina custom in Shopify/Webflow/Framer.
3. Sostituisci placeholder — cerca `REPLACE_WITH_` per trovare ogni punto da completare.
4. A/B test — scorri al fondo per i 5 blocchi variant commentati.
5. Produzione — questo file usa Tailwind Play CDN. Per spesa >$50/giorno, sostituisci con un foglio stile precompilato.
```

---

## Regole critiche

- **Mai scrivere fuori da `$AILAB/10_Landing_Pages/`**
- **Mai procedere senza VOC e Brand DNA**
- **Zero numeri/testimonial inventati**
- **Un solo CTA destination**
- **H1 DEVE echeggiare l'headline dell'ad (3+ parole verbatim)**
- **34 anti-AI slop tells risolti prima del write**
- **Mai deployare** — il file va su disco, il deploy spetta al membro

---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
