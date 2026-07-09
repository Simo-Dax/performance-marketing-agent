# SA5 — Creative Concepts Framework

**Agente:** SA5 (Creative Concepts)
**Input:** `intermediate/sa4_strategy.md` + `01_VOC_Research/` + `03_Ad_Spy/` + `02_Brand_DNA/` + `context/brand/`
**Output:** `intermediate/sa5_creative_framework.md`
**Skill collegate:** `09_marketing_psychology`, `04_references_tecniche_design`, `22_character_creator`, `23_competitor_rebuild`

---

## Cosa produce

Da `sa4_strategy.md` produce **3-5 concept creativi distinti**, ognuno è un angolo completo e indipendente: hook visivo + big idea + leva psicologica + awareness level + formato + CTA + brief visivo + 2 varianti A/B + matrice canale.

Un "concept" non è un'immagine. È un **sistema di persuasione**: un modo specifico di far percepire al cliente il problema o il desiderio, ancorato a una verità del VOC e a una leva psicologica nominata.

---

## Regola di fondo: un concept = un angolo = un'idea testabile

Ogni concept deve poter vincere o perdere **da solo**. Se due concept dicono la stessa cosa allo stesso pubblico con la stessa leva, sono lo stesso concept con due immagini — non due test. Diversità obbligatoria su almeno **tre** di questi assi:
- Awareness level (unaware / problem-aware / solution-aware / product-aware / most-aware)
- Leva psicologica (vedi `09_marketing_psychology`)
- Formato (statico / UGC video / carosello / demo)
- Angolo di entrata (problema / desiderio / obiezione / identità / status quo)

## Filosofia: evidence-driven, evolutivo non clone

I concept non si inventano: si **estraggono dall'evidenza**. Quattro fonti, quattro mappe (Step 1):
1. **Brand pattern map** — cosa il brand sta già usando e cosa funziona (dai suoi ad live, taggati per tier).
2. **Customer truth map** — dolori/desideri/obiezioni ad alta intensità, in parole verbatim (dal VOC).
3. **Sea-of-sameness map** — gli angoli che TUTTI in categoria usano e che il cliente ha imparato a ignorare (dall'ad spy competitor).
4. **White space map** — angoli che il brand non usa, la categoria non usa, ma il VOC dice che contano → i concept più forti.

Ogni concept è **evolutivo**: prende un elemento vincente (hook/angolo/visual) di un ad PROVEN/HOT del brand e lo fa evolvere (diversa awareness, diverso meccanismo di proof, diversa scena), **non lo clona**. Per i cloni con nuovo copy esiste `27_multiplier`.

---

## Step 0 — Auto-discovery input

Cerca e leggi:
- `intermediate/sa4_strategy.md` — **obbligatorio**: angoli per fase funnel, messaggi core, formati per canale
- `01_VOC_Research/` — **obbligatorio**: linguaggio verbatim, dolori, desideri
- `02_Brand_DNA/` — colori, tono, USP (se presente)
- `03_Ad_Spy/` — swipe file competitor (per gap e rebuild)
- `03_Ad_Spy/` o scrape on-demand — **ad live del brand stesso** (opzionale ma raccomandato): gli ultimi ~20 ad Meta attivi del brand, per la brand pattern map. Stessa infra Apify di `19_ad_spy` puntata sulla Page del brand invece che sui competitor. Se non disponibile, la pattern map si costruisce dai reference in `context/references/ads/` o si dichiara assente.
- `context/brand/brand_kit.md`, `design_system.md`, `tone_of_voice.md`
- `context/references/ads/` — reference visive

Se manca SA4 → ferma, richiedi l'esecuzione di SA4.
Se manca VOC → ferma, richiedi `18_voc_research`. I concept senza VOC sono invenzioni.

---

## Step 1 — Estrai la materia prima (NON saltare)

### 1A — Dalla strategia SA4
- Quanti e quali angoli ha definito SA4 per ogni fase funnel?
- Qual è la UVP per paid advertising (diversa dalla UVP brand)?
- Quali formati richiede ogni canale/fase?

### 1B — Dal VOC: costruisci la mappa persuasiva
Per ogni dolore/desiderio principale estrai:
- **Frase verbatim** del cliente (parole esatte, con fonte)
- **Awareness level** implicito
- **Obiezione dominante** ("perché non ha ancora comprato")
- **Trasformazione desiderata** ("come appare vincere, nelle sue parole")

### 1C — Sea-of-sameness map (dall'Ad Spy competitor)
- Quali angoli usano già i competitor (da NON ripetere identici)
- Quali formati visivi e meccanismi di proof sono cliché in categoria
- Quale linguaggio marketing il cliente ha imparato a ignorare

### 1D — Brand pattern map (dagli ad live del brand stesso)
Se disponibili gli ad live del brand (input opzionale Step 0), taggali e scorali:
- **Scoring tier:** PROVEN (`attivo` e `≥60 giorni`), HOT (`attivo` e `≥21 giorni`), ACTIVE (`attivo` e `<21 giorni`), RETIRED (`non attivo` e `≥60 giorni`), SHORT_RUN (`non attivo` e `<60 giorni`).
- **Tag per ad:** angolo, formato visivo, hook style, lunghezza copy.
- Cosa hanno in comune i vincenti (PROVEN/HOT)? Cosa il brand ha provato e ritirato? Quali assi (awareness, formato, proof) sono **assenti**?
- Questa mappa alimenta il constraint "evolutivo non clone": ogni concept deve evolvere un segnale PROVEN/HOT, non duplicarlo.

Se gli ad del brand non sono disponibili: dichiaralo esplicitamente. I concept lavorano allora su VOC + white space + sea-of-sameness, segnalando che manca il layer "brand ad signal".

### 1E — White space map (sintesi)
Incrocia le tre mappe sopra: gli angoli/hook/formati/proof che il brand NON usa, la categoria NON usa, e il VOC dice che il cliente vuole → **white space** = i concept più forti.

---

## Step 2 — Genera i concept (3-5)

Per ogni concept compila la scheda completa. Costruisci ogni concept partendo da **un'intersezione VOC × leva psicologica × white space**.

```
### Concept N: [Nome memorabile]

**Angolo di entrata:** [problema / desiderio / obiezione / identità / status quo]
**Awareness level:** [unaware → most-aware]
**Leva psicologica:** [nome esatto da 09_marketing_psychology — es. loss aversion, social proof, curiosity gap]
**Verità VOC ancorante:** "[citazione verbatim dal VOC]" — fonte
**Big idea:** [la singola idea che rende il concept memorabile, in una frase]
**Hook visivo:** [cosa cattura l'occhio nei primi 0.5s — descrizione concreta]
**Messaggio core:** [in una frase, ciò che il concept fa percepire]
**CTA:** [azione specifica]

**Brief visivo:**
- Palette: [hex dal Brand DNA]
- Stile: [fotografico / illustrato / UGC raw / studio / lifestyle]
- Mood: [aggettivi]
- Elementi chiave: [cosa deve esserci nel frame]
- Personaggio: [riferimento da 11_Characters/ se applicabile, o "nessuno"]

**Formato primario:** [statico 1:1 / 4:5 / UGC video 9:16 / carosello / product shot]
**Skill di produzione SA6:** [24_static_ads / 25_ugc_prompt / 26_product_shot / 27_multiplier]

**Variante A:** [descrizione — cosa cambia sull'esecuzione, stesso angolo]
**Variante B:** [descrizione — seconda esecuzione testabile, stesso angolo]

**Canali:** [Meta Feed / Stories-Reels / Google Display / TikTok]
**Fase funnel:** [awareness / consideration / conversion / retention]
**Specifiche tecniche:** 1:1 (1080×1080), 4:5 (1080×1350), 9:16 (1080×1920)
```

---

## Step 3 — Gli 8 hard constraints (gate obbligatorio)

Prima di consegnare, il set di concept deve passare **8 vincoli**. 4 a livello di set (tutto il set insieme), 4 per ogni singolo concept. Un set che non li rispetta si rifonde, non si consegna.

### Constraint a livello di SET (tutti e 4)
1. **Copertura awareness:** il set copre **≥3 dei 5 stadi Schwartz** (unaware, problem-aware, solution-aware, product-aware, most-aware).
2. **Ugly/native:** **≥1 concept** che sembra un vero post social o screenshot, non un ad patinato.
3. **Social proof:** **≥1 concept** testimonial/review/rating-led.
4. **No overlap totale:** nessuna coppia di concept condivide *angolo* **+** *awareness* **+** *meccanismo di proof* tutti e tre. Possono condividerne uno o due, mai tutti e tre. (= la vecchia matrice diversità, irrigidita.)

### Constraint PER CONCEPT (tutti e 4)
5. **VOC verbatim:** cita ≥1 frase verbatim dal VOC, esatta, nel campo "Verità VOC ancorante". Niente parafrasi.
6. **Brand signal o white space:** il "perché funziona" aggancia ≥1 segnale specifico (elemento vincente di un ad PROVEN/HOT del brand) **oppure** ≥1 white space specifico supportato dal VOC. Niente "perché rispecchia il brand" generico.
7. **No fake proof (FTC 2024):** ogni numero clienti, conteggio review, rating, testimonial, menzione stampa o endorsement deve venire da VOC/Brand DNA/ad scrapati, o si omette. Zero proof fabbricato.
8. **Evolutivo non clone:** prende un hook/angolo/visual da un ad PROVEN/HOT e ne cambia ≥2 dimensioni (awareness, hook, famiglia visiva, proof, persona, scena). Un concept che duplica 5/6 dimensioni è un clone → va a `27_multiplier`, non qui.

### Matrici di verifica
| Concept | Awareness | Leva psicologica | Angolo entrata | Meccanismo proof |
|---------|-----------|------------------|----------------|------------------|
| 1 | | | | |

| Concept | Meta Feed | Meta Stories/Reels | Google Display | TikTok |
|---------|-----------|--------------------|----------------|--------|
| 1 | ✓/– | | | |

---

## Step 3b — 🚦 Gate concept (approvazione umana)

Presenta i concept come testo pulito (le schede Step 2). L'umano fa **approve / reject / edit** per concept. Gli edit rifondono il singolo concept e lo ri-sottopongono. Solo i concept approvati proseguono.

> Filosofia human-in-the-loop: SA5 propone concept evidence-driven, l'umano decide cosa entra in produzione.

---

## Step 3c — QA gate (6 check silenziosi sui concept approvati)

Ogni concept approvato (anche dopo edit) passa 6 check **prima** di andare a SA6. Passano in silenzio; falliscono con un messaggio a una riga → l'umano rivede o droppa.

1. **VOC evidence** — la citazione VOC compare verbatim nel documento VOC (match case-insensitive, whitespace-normalizzato). Parafrasi = fail.
2. **Brand signal / white space** — il "perché funziona" punta a un segnale concreto (es. "layout testimonial dell'ad PROVEN attivo da 87gg") o a un gap concreto (es. "0 concept problem-aware negli ultimi 20 ad, ma 38% del VOC è problem-aware"). Generico = fail.
3. **FTC compliance** — nessun dato/review/rating/stampa/endorsement non sourced. Inventato = fail.
4. **Producibilità visiva** — soggetto concreto (prodotto/persona/scena reale, non "il senso di libertà"), prodotto renderizzabile dalle foto reali, niente che richieda capacità che GPT Image 2 non regge bene (tipografia di paragrafi lunghi, screenshot pixel-perfect di app reali, layout comic multi-frame), niente identità reali (celebrity/founder) senza ok Brand DNA.
5. **No fake urgency** — niente "limited time"/"only X left"/countdown se non c'è una deadline reale nel brief/Brand DNA.
6. **Evolutivo non clone** — differisce da ogni ad esistente del brand su ≥2 dimensioni. 1 sola dimensione → fail (è multiplier).

Solo i concept che passano tutti e 6 vanno a SA6.

---

## Step 4 — Routing produzione

Per ogni concept indica esplicitamente quale skill SA6 lo produrrà, così SA6 sa già cosa instradare:
- Statica → **`24_static_ads`** (`/pm-statiche`). Nota: `24_static_ads` è **rebrand di winner reali** — prende il design da un ad vincente reale della reference bank, non dalla direzione visiva del concept. Del concept usa **l'angolo/messaggio/citazione VOC** (che seedano il pool angoli); la direzione visiva del concept è ignorata di proposito (il design vince già nel feed reale). Un concept può quindi passare a 24 come seed angolo, non come brief visivo.
- Video UGC con hook → **`25_ugc_prompt`** (`/pm-ugc-video`)
- Shot prodotto (studio/in mano/indossato) → **`26_product_shot`** (`/pm-product-photo`)
- Scalare un winner esistente → **`27_multiplier`** (`/pm-multiplier`)
- Reverse-engineer competitor ad → **`23_competitor_rebuild`** (in SA5 stessa)

Se un concept richiede un personaggio ricorrente (UGC con volto fisso, product shot "worn/held") → attiva **`22_character_creator`** (`/pm-buyer-persona`) **prima** di passare a SA6.

---

## Output format finale → `intermediate/sa5_creative_framework.md`

```markdown
# Creative Framework — {Brand} — {Campagna} — {Data}

## Sintesi strategica
[2-3 righe: quale UVP, quale audience, quali leve dominanti emerse da VOC + gap competitor]

## Concept (3-5)
[le schede complete dallo Step 2]

## Matrice di diversità
[tabella Step 3]

## Matrice concept × canale
[tabella Step 3]

## Routing produzione SA6
[concept → skill esecutrice]

## Personaggi richiesti
[lista personaggi da generare con 22_character_creator, o "nessuno"]
```

---

## Regole critiche

- **Mai inventare la verità VOC** — ogni concept ancora a una citazione verbatim reale. Se non c'è nel VOC, il concept non parte. (Constraint 5)
- **Evidence-driven, non a sentimento** — i concept escono dalle 4 mappe (brand pattern / customer truth / sea-of-sameness / white space), non dall'intuizione.
- **Evolutivo non clone** — ogni concept evolve un segnale PROVEN/HOT del brand su ≥2 dimensioni. I cloni con nuovo copy vanno a `27_multiplier`. (Constraint 8)
- **Gli 8 hard constraints sono un gate, non un suggerimento** — un set che non li passa si rifonde.
- **No fake proof (FTC 2024)** — zero numeri/review/rating/stampa fabbricati. Sourced o omessi. (Constraint 7)
- **Mai due concept gemelli** — no overlap su angolo+awareness+proof tutti e tre. (Constraint 4)
- **Ogni concept nomina la leva psicologica** — niente "fa scena". Il meccanismo va dichiarato.
- **Il brief visivo usa colori dal Brand DNA** — niente palette inventate.
- **Routing esplicito** — ogni concept dice già a SA6 quale skill lo produce.
- **Gate umano + QA gate prima di SA6** — solo concept approvati e che passano i 6 check entrano in produzione.
- **SA7 segue, non precede** — i concept sono completi prima che SA7 scriva una riga di copy.

## Handoff
Output completo → **SA7** (copy per ogni concept) → poi **SA6** (produzione asset).
