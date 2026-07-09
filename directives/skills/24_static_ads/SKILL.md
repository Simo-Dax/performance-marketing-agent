# SA6 — Static Ads da Winner Reali (Rebrand)

**Agente:** SA6 (Asset Production)
**Input:** reference bank obbligatoria (format shell bancati da `19_ad_spy` e/o dai winner live del brand) + Brand DNA + VOC + foto prodotto
**Output:** prompt in chat (un blocco prosa per ad) + copia su disco `04_Static_Ads/static-ads-[YYYY-MM-DD].txt`
**Modello default:** GPT Image 2 (`openai/gpt-image-2/edit`) al ratio nativo di ogni ad sorgente. Nano Banana 2 solo per 4:5 vero insistito.
**Reference:** `references/format_families.md` (13 famiglie verificate, vocabolario di classificazione, mai template) · `references/winning_ad_science.md` (evidenze — warn su rebrand, legge su synthesis) · `references/rebrand_worked_example.md` (coppia PRIMA/DOPO da studiare prima di scrivere) · `../_shared/format_teardown_recreation.md` (F-EXTRACT/F-TRANSFORM, gate R1-R6) · `../_shared/adjacency_kill_pass.md` (gate K1-K3) · `../_shared/angle_engine.md` (motore angoli, fallback Step 4)

---

## Cambio di filosofia (rebrand model)

Questa skill **non riempie più template**. L'utente ordina un numero qualsiasi di ad. **Ogni ad è il REBRAND di un winner reale dalla reference bank**: l'intero design della fonte si tiene di proposito, solo l'identità si scambia (parole, marchi, prodotto, colori, numeri), 2-3 dettagli shiftati così è un sibling, non un gemello. Il deliverable per ad è **UN BLOCCO PROSA**, esattamente come il prompt di ricreazione bancato da cui viene — nessuna zona, nessun template di layout, nessuno scaffold di output, nessun paragrafo di constraints appiccicato. Il prompt è il prompt.

**Legge Andromeda:** Meta raggruppa creative look-alike e le pool come un solo ad in delivery — quindi di default N ad = N ad sorgente strutturalmente DIVERSI, distribuiti su famiglie di formato diverse. L'utente può ordinare esplicitamente variazioni di uno stesso stile (stesso design tenuto, messaggio diverso ogni volta); la skill lo permette con una nota onesta che quelle variazioni si raggruppano come un cluster e Meta sceglie il messaggio vincente tra loro. Spread di default, ripetizione solo se richiesta.

**Reference ads obbligatorie.** Questa skill non scrive mai prompt senza ad di riferimento reali: ad live del brand stesso (scrapati) o ricreazioni bancate dal competitor (`19_ad_spy`). Zero fonti + scan competitor rifiutato = il run si ferma con instradamento a `/pm-competitor-spy`.

L'utente interagisce a: intake, approvazione batch plan, scelta path, ogni gate di spesa. Tutto il resto gira silenziosamente.

---

## Step 0 — Cartella + token Apify

```bash
WORKDIR="$PWD"
mkdir -p "$WORKDIR/04_Static_Ads/_scratch" "$WORKDIR/04_Static_Ads/path_b_outputs" "$WORKDIR/04_Static_Ads/path_c_outputs" "$WORKDIR/04_Static_Ads/path_d_outputs"
[ -f ~/.config/pm-agent/apify.env ] && . ~/.config/pm-agent/apify.env
TOKEN="${APIFY_TOKEN:-}"
```
Se `TOKEN` vuoto e serve scrapare (Step 2) → chiedi `/pm-setup-apify`. Se la reference bank basta già (Step 2 salta lo scrape), non serve fermarsi qui.

---

## Step 1 — Intake

Auto-discovery prima di chiedere:
```bash
ls -t "$WORKDIR/01_VOC_Research/"*.html "$WORKDIR/01_VOC_Research/"*.md 2>/dev/null | head -n 1
ls -t "$WORKDIR/02_Brand_DNA/"*.html "$WORKDIR/02_Brand_DNA/"*.md 2>/dev/null | head -n 1
ls -t "$WORKDIR/14_Creative_Briefs/"angles-*.json 2>/dev/null | head -n 1
```
Chiedi solo ciò che non è derivabile:
1. **Brand Facebook Page URL o Page ID** — per scrapare gli ad live del brand.
2. **Foto prodotto** — 1+ immagini reference (+ logo se esiste).
3. **Quanti ad vuoi?** Qualsiasi numero — prima dirò quanto è profonda la reference bank.
4. **Brief opzionale** — obiettivo campagna, offerta corrente, geo, price point, un ratio richiesto (solo se i placement lo impongono, altrimenti ogni ad renderizza al ratio nativo della sua fonte — il default raccomandato). "skip" se nessuno di questi conta per questo run.

Se esiste un **angle bank approvato** (`14_Creative_Briefs/angles-*.json`), offri una volta: i suoi angoli diventano il pool per questo run e lo Step 4 salta la generazione interna. Porta l'id di ogni angolo (`A03`) fino agli header ad e ai nomi file.

Cattura: `$BRAND_DNA`, `$VOC`, `$PAGE_INPUT`, `$PRODUCT_IMAGES`, `$BRAND_LOGO` (vuoto se assente — mai inventare un allegato), `$AD_COUNT`, `$FORCED_RATIO` (vuoto = ratio nativo per ad), `$BRIEF`.

---

## Step 1a — Catalogo prop + Product DNA

Ispeziona visivamente ogni immagine prodotto caricata, cataloga gli asset fisici reali (pouch, bottiglia, scatola, screenshot, ecc.) con nome breve + testo etichetta + dettagli visivi leggibili → `$PROP_CATALOG`. Mai inventare un prop non presente nelle foto. Nota anche: la faccia migliore del prodotto, la leggibilità del pack, dove vive il logo → `$PRODUCT_DNA`.

Uso condizionale allo Step 6: quando la fonte mostra un prodotto, il prop scambiato è nominato da `$PROP_CATALOG` per `$PRODUCT_DNA`. Quando la fonte non mostra prodotto (una lettera, uno screenshot Notes, una card di testo), non si forza nessun prop dentro.

---

## Step 1b — Aspect ratio + renderer

Il ratio segue di default la fonte (Step 6). GPT Image 2 è il renderer default per ogni ratio supportato. Non produce un 4:5 vero (il portrait più vicino è 3:4):
- Se `$FORCED_RATIO` = 4:5 vero: "GPT Image 2 non produce un 4:5 vero, il più vicino è 3:4 (quasi identico nel feed Meta). Va bene 3:4, o serve un 4:5 vero?"
- Accetta 3:4 → `$RENDER_MODEL = gpt-image-2`. Insiste su 4:5 vero → `$RENDER_MODEL = nano-banana-2` solo per quel batch (mai opzione generale).

---

## Step 2 — Scrape ad live del brand

Stesso actor/pattern di `19_ad_spy` Step 2C+4 (Pages scraper REST per risolvere `pageAdLibrary.id`, poi `curious_coder~facebook-ads-library-scraper` con `count=20`, `active_status=active`, `search_type=page`, `view_all_page_id={PAGE_ID}`, `scrapeAdDetails:true`; filtro solo statiche in post). Avvisa: "Scrapo i tuoi ad statici live dal Meta Ad Library. 60-180 secondi."

### Ramo zero-ad (il mandato reference-ads)

Questa skill non scrive mai prompt senza ad di riferimento. Se lo scrape torna zero (dopo il filtro statiche), controlla prima i fallback:
```bash
ls -t "$WORKDIR/03_Ad_Spy/_scratch/"format-*.json 2>/dev/null | head -n 3
ls -t "$WORKDIR/03_Ad_Spy/"adspy-*.html 2>/dev/null | head -n 3
```
Se esistono ricreazioni bancate o swipe file → "Nessun ad live sulla tua pagina; costruisco dalle tue reference competitor bancate." e continua. Se ENTRAMBI sono vuoti, ferma e chiedi solo questo:

> Non trovo ad statici live per questo brand, né reference competitor su disco. Questo workflow costruisce ogni ad da reference reali, quindi ne serve una delle due. Vuoi che scrapi 1-3 competitor ora? Dammi nomi brand o URL Facebook, separati da virgola. O rispondi "stop" ed esegui prima `/pm-competitor-spy`.

Risposta con competitor → rilancia lo scrape (via `19_ad_spy` logic) per ciascuno (max 3), tagga ogni ad `source_brand`. Risposta "stop" (o non una lista) → **fermati**: "Serve reference reali per costruire. Esegui `/pm-competitor-spy` su uno o due competitor, poi rilancia questa skill." Hard gate, non una preferenza. Mai auto-ricercare competitor: l'utente li conosce meglio di una web search.

---

## Step 3 — Normalizza, score, scratch file

Per ogni ad: calcola `days_active`, `variant_count`, `scoring_tier` (stesse soglie di `19_ad_spy` Step 4), deriva `angle`/`hook_style`/`copy_length` dal copy. Scrivi `$WORKDIR/04_Static_Ads/_scratch/brand-ads-$(date -u +%Y%m%d).json` (sovrascrivi quello di oggi; i file più vecchi restano come loop di apprendimento delle run precedenti).

---

## Step 3b — Guarda i winner e bancali

Mandatorio quando esistono ad attivi. **Guarda davvero le creative.** Scarica le top 10-20 immagini primarie (ranked PROVEN/HOT/ACTIVE, run più lunghi e più varianti prima) in `$WORKDIR/04_Static_Ads/_scratch/creatives/<ad_archive_id>.jpg`, leggi ogni file col tool Read.

**Costruisci `$AD_ANALYSIS` (Winning Ad Visual DNA)**: layout/composizione condivisi dai winner, palette reale, tipografia/text-overlay, stile fotografico, device di prova, framing dell'hook, presentazione prodotto, + una riga trasferibile per ad sul perché funziona. Merge nello scratch file di oggi sotto `"visual_dna"`. `$AD_ANALYSIS` governa il lato IDENTITÀ di ogni rebrand (quali colori brand su quali ruoli, la voce del copy sostitutivo, come il prodotto appare nelle zone scambiate), mai il lato design — quello viene dall'ad sorgente.

**Banca i winner del brand come ricreazioni.** Dedup per headline+body normalizzati, prendi i top 3 unique per tier, salta quelli già bancati a `schema_version: 2`. Carica `../_shared/format_teardown_recreation.md`, esegui F-EXTRACT (F.2-F.6) su ognuno dal jpg locale già scaricato. Persisti in `$WORKDIR/03_Ad_Spy/_scratch/` con `created_by_skill: "24_static_ads"`. **Regola attribuzione:** `source.slug` = il tag `source_brand` di quell'ad, mai il brand dell'utente in blocco. Ad entrati dal ramo zero-ad competitor bancano come ricreazioni COMPETITOR (gate R pieni allo Step 6); solo ad scrapati dalla pagina propria dell'utente bancano col proprio slug.

---

## Step 4 — Pool di angoli

Se il run è stato seedato da un angle bank approvato (Step 1), salta questo step — gli angoli seedati sono il pool.

Altrimenti, assembla in memoria: `$BRAND_DNA`, `$VOC`, il set ad normalizzato con tag/tier, `$AD_ANALYSIS`, `$PROP_CATALOG`+`$PRODUCT_DNA`, `$BRIEF`, storia delle run precedenti (fino a 5 `brand-ads-*.json` scratch più recenti, oggi escluso). Carica `../_shared/angle_engine.md` e genera **6-10 angoli** (usa lo spread G.3, i gate hard G.5, il contratto G.4 semplificato: ogni angolo porta message/awareness/citazione VOC/proof disponibile/segnale su cui si appoggia — **nessuna direzione visiva**, il visual viene sempre dagli ad sorgente in questa skill, dargliene una lo romperebbe). Avvisa: "Costruisco il pool di angoli da Brand DNA, VOC, e i tuoi ad live. 45-90 secondi."

Applica silenziosamente i gate su ogni angolo prima che entri nel piano (da `../_shared/creative_claims_compliance.md`): C.1 (citazione VOC verbatim), C.1 (prova solo sourced), C.3 (niente urgenza finta). Un angolo che fallisce si fixa o si scarta prima che l'utente veda il piano, mai dopo.

---

## Step 5 — Il batch plan (l'unica approvazione che conta)

**Conta la bank.** Glob `$WORKDIR/03_Ad_Spy/_scratch/format-*.json`. Fonti usabili = artefatti `schema_version: 2` (`fidelity: "recreation"`); uno shell legacy `schema_version: 1` viene ri-torn-down a recreation grade prima di essere scelto ("Aggiorno un teardown vecchio a recreation grade, circa un minuto"). Leggi anche `competitors.json` se presente. `$BANK_DEPTH` = ricreazioni usabili strutturalmente distinte (dedup creative quasi-identiche), nota lo spread di famiglia formato via `classification.format_family_hint` di ogni artefatto.

**Riporta la capacità onestamente, prima di costruire qualunque cosa:**

> La tua reference bank ha `<BANK_DEPTH>` design vincenti distinti su `<F>` famiglie di formato. Hai ordinato `<AD_COUNT>` ad.

- `$AD_COUNT` ≤ `$BANK_DEPTH` → continua.
- `$AD_COUNT` > `$BANK_DEPTH` → l'utente sceglie, niente accade silenziosamente: esegui `/pm-competitor-spy` su più competitor per approfondire la bank (opzione migliore), abbassa il conteggio, ordina variazioni degli stili più forti, o approva esplicitamente l'overflow come ad SYNTHESIS etichettati (Sezione S).

**Accoppia fonti e angoli.** Scegli i `$AD_COUNT` migliori ad sorgente: tier provati prima, poi spread sulle famiglie di formato che la bank permette (l'asse Andromeda). Accoppia ogni fonte con l'angolo che serve meglio. Quando esistono ricreazioni del brand stesso, preferiscine almeno una: evolvere il proprio winner è la mossa a percentuale più alta.

**Presenta il piano come menu:**

> IL PIANO, `<AD_COUNT>` ad dalla tua bank:
> AD 1: F-<id> (<brand>, <famiglia o nome formato>, <tier> <giorni>g) porta ANGOLO <n>: <nome angolo>
> AD 2: ...
> Spread batch: `<AD_COUNT>` ad su `<K>` cluster strutturali. [se K < AD_COUNT: "I <n> ad stile <nome> si raggruppano come una creative in delivery; Meta sceglie il messaggio vincente tra loro."]
> Rispondi "vai" per costruire tutto, o modifica prima: "cambia fonte ad 2", "cambia angolo ad 2", "togli ad 3", "fai 3 dell'ad 1" (variazioni di quello stile, ognuna con angolo diverso), "aggiungi un ad".

**Variazioni.** Quando l'utente ordina N di uno stile: quella fonte produce N ad, stesso design tenuto, ognuno con un angolo DIVERSO dal pool e i propri 2-3 sibling shift. Due ad con stesso design E stesso messaggio sarebbero un vero duplicato — resta vietato. Le variazioni ordinate sono esenti dalla regola una-fonte-un-ad (K-2), la ripetizione silenziosa fallisce comunque.

Loop finché l'utente non dice "vai".

---

## Step 6 — Scrivi i prompt (il rebrand)

Studia `references/rebrand_worked_example.md` PRIMA di scrivere qualunque cosa — è una coppia PRIMA/DOPO reale, la coppia è l'istruzione.

Per ogni ad nel piano approvato:

1. **Leggi la fonte.** Apri il JSON di ricreazione, prendi il suo `condensed_prompt` VERBATIM come bozza.
2. **Scambia solo l'identità.** Le loro parole quotate diventano il messaggio dell'utente per l'angolo assegnato a quest'ad, stesso lavoro argomentativo, lunghezza simile. Il loro brand/prodotto/marchi diventano quelli dell'utente (file ATTACHED quando esistono su disco, descritti in testo quando no — l'immagine dell'ad competitor non si allega mai a niente). I loro colori diventano quelli brand o sostituzioni a contrasto uguale. I loro numeri diventano numeri reali sourced dell'utente (scala R4 quando non esiste un numero reale: citazione VOC allo stesso peso visivo, claim non-numerica, o lascia recedere lo slot).
3. **Shifta 2-3 dettagli sibling** così è un sibling, non un gemello (un'istanza di device, un elemento specchiato/riproporzionato, lunghezza lista, carattere della scrittura a mano).
4. **Ogni parola che non hai appena toccato resta parola per parola.** Quella restrizione è il mestiere. Non decomporre in zone, non ristrutturare, non appendere un paragrafo di constraints, non inserire una headline da fuori lo swap.
5. **Gestisci il ratio.** Default: l'ad renderizza al ratio nativo della fonte, dichiarato nell'header. Se `$FORCED_RATIO` è settato e diverso: tieni il design descritto intero e appendi una frase: "Imposta l'intera card descritta sopra, invariata, centrata su un canvas `<FORCED_RATIO>` il cui sfondo continua lo stesso fondo; non riarrangiare nessun elemento." Mai re-layoutare un design per un ratio.
6. **Prodotti/prop, condizionale.** Quando la fonte mostra un prodotto, il prop scambiato è nominato da `$PROP_CATALOG` per `$PRODUCT_DNA`. Quando la fonte non mostra prodotto, non forzarne nessuno.
7. **Giudica contro l'obiettivo.** Metti il prompt finito accanto alla sua fonte: stessa razza di ad vincente, brand diverso, magari migliore, e qualunque cosa rendeva la fonte nativa nel feed sopravvive intatta (se il winner sembrava una nota scritta a mano da una persona, il render pure — renderlo più "designed" è un fallimento). I gate girano silenziosamente dietro questo flusso: R1-R6 da `../_shared/format_teardown_recreation.md` + l'adjacency pass K1-K3 da `../_shared/adjacency_kill_pass.md` (le fonti del brand stesso usano le relazioni sopra: saltano R3, tengono R4/R6). I floor di `references/winning_ad_science.md` sono LEGGE per gli ad synthesis e un WARN in una riga per i rebrand — la fonte ha già vinto nel feed reale, mai riscrivere il suo design per soddisfare una regola da laboratorio, nota solo la tensione se esiste.

Per variazioni ordinate: ripeti 1-7 sulla stessa fonte con l'angolo e i sibling shift propri della variazione.

### Sezione S — SYNTHESIS: solo overflow approvato dall'utente

Mai silenziosa. Esiste per un solo caso: l'utente ha ordinato più ad di quanti la bank ne possa servire e ha esplicitamente approvato synthesis etichettata per l'overflow nel batch plan.

1. **Leggi l'intera bank** (proprie e competitor): raccogli il linguaggio di pattern (architetture zona ricorrenti, grammatica device, discipline colore-ruolo, sistemi tipografici, pattern di enfasi).
2. **Scansiona `references/format_families.md`** (13 famiglie verificate), scegli una famiglia che il batch non ha ancora usato, adatta all'angolo e allo stadio awareness di quest'ad.
3. **Scrivi un prompt ORIGINALE.** Una combinazione nuova che non esiste in nessuna singola ricreazione, un blocco prosa nella stessa voce delle ricreazioni bancate, stilizzato da Visual DNA del brand + `$PRODUCT_DNA`. I floor scientifici e il glance test in `winning_ad_science.md` sono LEGGE qui, non warning.
4. **Check del travestimento.** Se la struttura sintetizzata riproduce la mappa zone E il device set di una ricreazione, è un rebrand travestito: riclassificalo come rebrand di quella ricreazione e gira i gate R.
5. **Etichetta.** `synthesized (famiglia: <nome>, ispirato da F-<id>, F-<id>, ...)`. Ogni F-<id> citato deve esistere nella bank.

---

## Step 7 — Consegna

Stampa ogni ad direttamente in chat. Formato per ad, nessun altro:

```
AD <n> di <totale>, rebrand di F-<id> (fonte: <brand>, <nome formato>, <tier> <giorni>g), angolo: <nome angolo>
Render: <ratio> su <modello>. Allega: <nomi file, o "nessuno">.

<il blocco prosa completo del render prompt, esattamente come lo incollerebbe uno sconosciuto>
```

Variazioni aggiungono `, variazione <k> di <m>` dopo il numero ad. Gli ad synthesis etichettano `synthesized (famiglia: <nome>, ispirato da F-<id>, F-<id>)` invece del label rebrand.

Dopo l'ultimo ad, salva lo stesso contenuto in `$WORKDIR/04_Static_Ads/static-ads-<YYYY-MM-DD>.txt` e registra `source_format` (o `source_format_inspiration`) di ogni ad nel JSON scratch di oggi. **Niente HTML.** Testo semplice in chat è il deliverable.

---

## Step 8 — Scelta del path

> I tuoi `<totale>` prompt sono pronti. Come vuoi generare le immagini?
> **A. Incolla manuale.** Gratis. Copia il prompt di un blocco AD nella tua sessione del modello immagine, allega i file che l'header nomina, genera.
> **B. Higgsfield MCP.** Meglio con subscription Higgsfield. OAuth one-time al primo uso.
> **C. Fal.ai a consumo.** Nessuna subscription. ~$0.15/immagine high quality.
> **D. Automazione web via Playwright.** Guido io il browser, incollo ogni prompt, alleg i file, clicco Genera, con conferma a ogni step.
> Scrivi A, B, C, o D. O "fatto" per fermarti qui coi prompt in chat.

Attendi una scelta esplicita. Un solo path per volta. Se "fatto", conferma e fermati.

Nomi file: `ad_<NN>.png`, variazioni `ad_<NN>_v<K>.png`, run seedati prefissano l'id (`A03_ad_02.png`).

### Path A — Incolla manuale
GPT Image 2 default: apri il modello immagine, nuova chat, modello GPT Image 2, quality high. Incolla un blocco AD alla volta, allega i file che l'header nomina, ratio dall'header, genera, salva alla dimensione più grande. Batch 4:5 vero → Nano Banana 2 (AI Studio, modello Gemini Flash Image) invece.

### Path B — Higgsfield CLI
Stessa infra di `25_ugc_prompt`/`27_multiplier` per il pattern CLI: `{{SKILL_SLUG}}: static`, `{{MODEL_ID}}: gpt_image_2` (o `nano_banana_flash` per 4:5 vero), `{{ASPECT}}`: ratio header di ogni ad, `{{QUALITY}}: high`, `{{RESOLUTION}}: 4k` (GPT Image 2) / `2k` (Nano Banana 2), `{{OUTPUT_DIR}}: 04_Static_Ads/path_b_outputs`. **Subset picker obbligatorio** prima della conferma spesa ("genera ad 1, ad 3" o "tutti"). Costo/credito citato prima di procedere, solo su `yes` esplicito. 5+ ad → `run_in_background` parallelo (tetto testato 8).

### Path C — Fal.ai diretto
1. `mcp__fal-ai__upload_file` per ogni file allegato → URL per ad.
2. Subset picker, stesse parole di Path B.
3. Costo: ~$0.15/immagine GPT Image 2 high (Nano Banana 2: chiama `mcp__fal-ai__get_pricing`). Moltiplica per il conteggio scelto, attendi "yes".
4. Per ad: `mcp__fal-ai__run_model`. **GPT Image 2**: `model: "openai/gpt-image-2/edit"`, `prompt`: il blocco prosa completo, `image_urls`: i file allegati di quell'ad, `image_size` dalla tabella sotto, `quality: "high"`, `output_format: "png"`, `num_images: 1`. **Mai `safety_tolerance`** — l'endpoint la rifiuta. **Nano Banana 2** (solo batch 4:5 vero): `model: "fal-ai/nano-banana-2"`, `aspect_ratio: "4:5"`, `resolution: "2K"`, `thinking_level: "high"`, `enable_web_search: true`, `safety_tolerance: "4"`, `output_format: "png"`, `num_images: 1`.

| ratio | `image_size` |
|---|---|
| `1:1` | `{"width": 2880, "height": 2880}` |
| `9:16` | `{"width": 2160, "height": 3840}` |
| `16:9` | `{"width": 3840, "height": 2160}` |
| `3:4` | `{"width": 2400, "height": 3200}` |
| `4:3` | `{"width": 3200, "height": 2400}` |
| `2:3` | `{"width": 2160, "height": 3240}` |
| `3:2` | `{"width": 3240, "height": 2160}` |
| altro | calcola width/height del ratio, lato lungo ≤3840, totale ≤8.294.400px, arrotonda a pari |

Report ogni 5: "5 di N fatti. Continuo? (yes/stop)". Salva in `04_Static_Ads/path_c_outputs/` + `manifest.json`.

### Path D — Playwright
Mai auto-upload media (serve "yes upload" per ogni file), mai cliccare Genera senza "yes go", un ad alla volta. Apri il renderer (ChatGPT per GPT Image 2, AI Studio per Nano Banana 2), seleziona modello+quality high+ratio dell'ad, per ad: annuncia, incolla il prompt, chiedi sull'allegare i file, conferma Genera, salva in `04_Static_Ads/path_d_outputs/`. Manifest finale nella stessa cartella.

---

## Validazione output

1. Ogni ad nel deliverable è UN blocco prosa sotto header corretto. Nessun prompt contiene numerazione zone, righe scaffold `Layout:`, label di campo template, o un paragrafo constraints appiccicato — se ne trovi uno, ricostruisci dalla ricreazione sorgente, mai una patch.
2. Ogni F-<id> citato risolve a un file reale in `$WORKDIR/03_Ad_Spy/_scratch/` (verifica con glob; un id non risolvibile è un fallimento, mai inventarne uno).
3. Swap completo: nessun nome brand/prodotto competitor, nessuna stringa dal `verbatim_text_ledger` di nessuna fonte sopravvive in nessun prompt (ri-diff meccanico, K-3). Le fonti del brand stesso sono esenti dal requisito di swap parole, mai dai numeri sourced.
4. Ogni numero/rating/conteggio/menzione stampa in ogni prompt è sourced da VOC/Brand DNA/ad scrapati, o ha seguito la scala R4.
5. L'utente ha approvato il batch plan prima che qualunque prompt fosse scritto, i conteggi sono stati onorati, la riga di spread (ad vs cluster strutturali) è stata mostrata.
6. Allegati corretti: quando una fonte mostra un marchio e `$BRAND_LOGO` esiste, la riga Allega dell'header lo porta; l'immagine dell'ad competitor non si allega mai a niente.
7. La copia su disco `04_Static_Ads/static-ads-<YYYY-MM-DD>.txt` esiste e combacia con l'output chat, lo scratch JSON di oggi registra il `source_format` di ogni ad.
8. Se un path è girato, la cartella output ha le immagini attese + un manifest.

Su fallimento: fix SOLO meccanico (un campo header mancante si riempie; una stringa del registro superstite significa rifare lo swap di quell'ad dalla ricreazione sorgente). MAI riscrivere un prompt in una struttura diversa per soddisfare un check.

---

## Regole hard

| Regola | Dettaglio |
|---|---|
| Il prompt è il prompt | Un blocco prosa che si legge esattamente come la ricreazione bancata da cui viene. Nessuna zona, nessun template, nessuno scaffold, nessun paragrafo constraints, mai. |
| N ad, N fonti, di default | Spread su famiglie di formato, tier provati prima. Ripetizione di uno stile solo se ordinata esplicitamente, con la nota cluster in una riga. |
| Rebrand, mai copia dell'identità | L'intero design della fonte si tiene; parole/marchi/prodotto/numeri/colori della fonte non si tengono mai (le fonti del brand stesso possono tenere/evolvere il proprio copy). Le fonti competitor girano R1-R6 + K1-K3. |
| Reference ads obbligatorie | Ad live propri, ricreazioni bancate da `19_ad_spy`, o un teardown da swipe. Zero fonti + scan competitor rifiutato = il run si ferma con instradamento a `/pm-competitor-spy`. |
| Synthesis è solo opt-in | Solo quando l'utente ha esplicitamente approvato l'overflow oltre la profondità della bank, etichettato, Sezione S. Mai un fallback silenzioso. |
| Il ratio segue la fonte | Ogni ad renderizza al ratio nativo della sua fonte salvo forzatura utente; un ratio forzato tiene il design intero su un fondo esteso, mai un re-layout. |
| La scienza avvisa sui rebrand, fa legge sulla synthesis | La fonte ha già vinto nel feed reale. Su un rebrand un conflitto coi floor scientifici è una riga onesta all'utente, non una riscrittura. Su una synthesis i floor e il glance test sono legge. |
| Gli angoli non portano visual | Il motore produce messaggi, stadi, citazioni VOC, prove. Il design viene solo dagli ad sorgente. |
| La storia delle run precedenti è il loop di apprendimento | Ogni run scrive `_scratch/brand-ads-<YYYYMMDD>.json`; le run future leggono fino alle 5 più recenti. |
| Niente trattini lunghi come pause di frase | Virgole, "e", o frasi separate. |
| `openai/gpt-image-2` rifiuta `safety_tolerance` | Il wiring Path C deve ometterlo. |
