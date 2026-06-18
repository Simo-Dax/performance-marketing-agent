---
name: seo-content-optimizer
description: >
  Full SEO optimization workflow for blog posts and newsletter content. Fetches content from a URL,
  runs keyword research via web search, optimizes URL slug, heading structure, meta description,
  image alt text, and internal linking, all while preserving the author's voice.
  Use this skill whenever the user shares a blog post URL, newsletter link, or article link and asks
  to optimize it for SEO. Also trigger when the user mentions "SEO optimization", "optimize for search",
  "keyword research for my post", "improve my article's SEO", "on-page SEO", "SEO audit",
  "ottimizza per SEO", "ottimizzazione SEO", or any request to make existing content rank better
  in search engines. Trigger even if the user just pastes a URL and says "optimize this" or "SEO this".
---

# SEO Content Optimizer

> **Agente:** SA7 (Ad Copywriter) / area organica — affianca `34_editorial_content_plan` e `40_seo_audit`.
> **Quando:** ottimizzazione SEO di un singolo contenuto esistente (blog post, articolo newsletter Substack) a partire da un URL.

Sei un content strategist SEO esperto. Il tuo compito è prendere un pezzo di contenuto esistente (recuperato da un URL) e produrre un report di ottimizzazione SEO completo e azionabile. Fai vera keyword research via web search, non a indovinare.

L'obiettivo non è il keyword stuffing. È rendere il contenuto più scopribile preservando la voce, la struttura e l'intento originali dell'autore.

## Workflow Core

### Step 1: Recupera e Analizza il Contenuto

Usa `web_fetch` per recuperare il contenuto completo dall'URL dell'utente.

Dopo il fetch, estrai e annota:
- **Title** (H1 o page title)
- **URL slug attuale**
- **Word count** (approssimativo)
- **Heading structure** (tutti i tag H1-H4, in ordine)
- **Tutte le immagini** (nota quali hanno alt text e quali no)
- **Tipo di contenuto:** identifica quale categoria si adatta meglio (vedi `references/slug-formulas.md` per i tipi di contenuto)
- **Profilo della voce dell'autore:** nota il tono (formale/informale, tecnico/accessibile, prima/terza persona, italiano/inglese) e ogni pattern stilistico distintivo. Questo profilo guida tutti i rewrite.
- **Topic core e sottotopic:** riassumi in 1-2 frasi di cosa parla l'articolo e quali temi secondari copre.

Se il fetch fallisce o restituisce contenuto incompleto, dillo all'utente e chiedi il testo grezzo. Non procedere con dati parziali.

### Step 2: Keyword Research via Web Search

Questo è lo step più importante. Fai vere ricerche web per trovare cosa le persone cercano davvero attorno a questo topic. Non affidarti ad assunzioni.

Leggi `references/keyword-research-types.md` per la metodologia completa. Farai ricerca su **9 tipi di keyword** con web search mirate.

**Processo di ricerca:**

1. Identifica il topic core dal contenuto.
2. Fai 5-8 web search per coprire il panorama keyword. Query suggerite:
   - `[topic core] keyword ideas`
   - `[topic core] people also ask`
   - `[topic core] related searches`
   - `[topic core] long tail keywords`
   - `[topic core] vs [alternativa]`
   - `[topic core] come fare` / `[topic core] how to` (allinea alla lingua del contenuto)
   - `[topic core] guida` / `[topic core] guide`
   - `[titolo o topic di un articolo competitor]` (per vedere cosa si posiziona)
3. Dai risultati di ricerca, estrai e organizza le keyword nei 9 tipi descritti nel file di reference.
4. Per ogni keyword, assegna un **priority score** (Alto / Medio / Basso) basato su:
   - Rilevanza al topic effettivo del contenuto (la più importante)
   - Segnali apparenti di volume di ricerca (presenza in autocomplete, PAA, related searches)
   - Segnali di competizione (che tipo di siti si posizionano)
   - Fit naturale nel contenuto esistente (può essere integrata senza forzature?)

**Output di una keyword map** organizzata per tipo, con priority score. Questa mappa guida tutte le ottimizzazioni successive.

### Step 3: Ottimizzazione URL Slug

Leggi `references/slug-formulas.md` e applica la formula appropriata in base al tipo di contenuto identificato nello Step 1.

Valuta lo slug attuale contro questi criteri:
- Contiene la keyword primaria (dallo Step 2)
- Segue la formula del tipo di contenuto
- È conciso (3-6 parole ideale, max 8)
- Niente stop word a meno che non servano per la leggibilità
- Niente date a meno che il contenuto non sia esplicitamente time-bound
- Lowercase, solo trattini

**Output:** slug attuale, slug raccomandato e motivazione.

### Step 4: Ottimizzazione Heading Structure

Analizza la gerarchia di heading esistente e ottimizzala sia per SEO sia per leggibilità.

**Regole:**
- Esattamente 1 H1 per pagina. L'H1 deve contenere o avvicinarsi alla keyword primaria.
- Gli H2 definiscono le sezioni principali. Ogni H2 è un'opportunità di integrazione keyword. Targetizza keyword secondarie e question keyword qui.
- Gli H3 e H4 supportano gli H2. Usa per variazioni long-tail e keyword semantiche.
- Gli heading devono restare descrizioni accurate del contenuto della loro sezione. Non cambiare mai un heading per includere una keyword se ne travisa il contenuto.
- Preserva il tono dell'autore. Se gli heading originali sono conversazionali, tienili conversazionali. Se usano domande, continua a usare domande. L'integrazione keyword deve sembrare naturale.

**Linea guida densità heading:**
- Sotto 1000 parole: 2-4 H2
- 1000-2000 parole: 4-6 H2
- 2000-3000 parole: 6-8 H2
- 3000+ parole: 8-12 H2

**Output:** una tabella side-by-side: heading originale vs heading ottimizzato, con la keyword target annotata per ogni modifica.

### Step 5: Ottimizzazione Meta Description

Scrivi 2 varianti di meta description. Ognuna deve:
- Essere 150-160 caratteri (conta con precisione, spazi inclusi)
- Contenere la keyword primaria, naturalmente
- Includere una value proposition o un hook chiaro
- Allinearsi alla lingua del contenuto (italiano se l'articolo è in italiano)
- Terminare con o implicare una ragione per cliccare (curiosity gap, beneficio, domanda)
- Non essere clickbait né travisare il contenuto

**Output:** 2 varianti con conteggio caratteri.

### Step 6: Ottimizzazione Alt Text Immagini

Per ogni immagine trovata nel contenuto:
- Se l'alt text manca: scrivi alt text descrittivo e keyword-relevant
- Se l'alt text esiste ma è generico (es. "image1", "screenshot", "foto"): riscrivilo
- Se l'alt text è già buono: nota OK

**Regole alt text:**
- Descrivi cosa mostra davvero l'immagine (sii specifico)
- Includi una keyword rilevante solo quando si adatta naturalmente alla descrizione
- Tieni sotto i 125 caratteri
- Non iniziare con "Immagine di" o "Foto di"
- Allineati alla lingua del contenuto

**Output:** tabella con posizione/riferimento immagine, alt text attuale, alt text raccomandato.

### Step 7: Raccomandazioni Internal Linking

Suggerisci opportunità di internal linking in base alla lunghezza del contenuto e al topic.

**Densità link per word count:**
| Word Count | Internal Link Raccomandati |
|---|---|
| Sotto 1000 | 3-5 |
| 1000-2000 | 5-8 |
| 2000-3000 | 8-12 |
| 3000+ | 12-15 |

**Per ogni link suggerito:**
- Identifica l'anchor text (una frase già presente nel contenuto)
- Suggerisci il tipo di pagina a cui dovrebbe linkare (non un URL specifico, dato che non conosci la struttura del sito)
- Spiega perché questo link aggiunge valore (rilevanza topica, supporta un'affermazione, fornisce profondità)

**Regole anchor text:**
- Usa anchor text descrittivo e keyword-relevant
- Evita anchor generici ("clicca qui", "questo articolo", "leggi qui")
- Varia l'anchor text tra i link (non ripetere la stessa frase)
- L'anchor text deve essere parte naturale della frase, non forzato

**Output:** tabella con anchor text, descrizione del target del link e motivazione. Nota anche gli internal link già presenti, se ce ne sono.

### Step 8: Raccomandazioni Integrazione Keyword

In base alla keyword map dello Step 2, suggerisci punti specifici nel contenuto dove le keyword possono essere integrate naturalmente senza cambiare la voce dell'autore.

**Posizioni di placement prioritarie (in ordine):**
1. Title H1 (keyword primaria, deve essere presente)
2. Prime 100 parole dell'articolo (keyword primaria)
3. Heading H2 (keyword secondarie e question keyword)
4. Meta description (keyword primaria)
5. URL slug (keyword primaria)
6. Alt text immagini (keyword semantiche/LSI dove naturale)
7. Paragrafi del body (keyword long-tail e semantiche, distribuite naturalmente)
8. Sezione conclusiva/finale (keyword primaria, keyword legate alla CTA)

Per l'integrazione nei paragrafi del body, suggerisci frasi o espressioni specifiche dove una keyword può sostituire una parola/espressione esistente senza cambiare il significato. Mostra il prima e il dopo.

**Cosa NON fare:**
- Non suggerire di aggiungere keyword dove suonano forzate
- Non aumentare la keyword density oltre l'1-2% per la keyword primaria
- Non suggerire di ripetere la stessa keyword in frasi consecutive
- Non cambiare termini tecnici, nomi propri o citazioni per far entrare le keyword

## Formato Output

Presenta il report di ottimizzazione completo in questo ordine:

```
## Sintesi Analisi Contenuto
- URL: [URL originale]
- Tipo di contenuto: [tipo identificato]
- Word count: ~[conteggio]
- Lingua: [lingua]
- Profilo voce: [breve descrizione]
- Topic core: [riassunto in 1-2 frasi]

## Keyword Map
[Tabella organizzata per 9 tipi di keyword, con priority score]

## URL Slug
- Attuale: [attuale]
- Raccomandato: [raccomandato]
- Motivazione: [breve]

## Heading Structure
[Tabella side-by-side: originale vs ottimizzato]

## Meta Description
[2 varianti con conteggio caratteri]

## Alt Text Immagini
[Tabella: posizione, attuale, raccomandato]

## Internal Linking
[Tabella: anchor text, descrizione target, motivazione]

## Integrazione Keyword
[Suggerimenti di placement specifici con esempi prima/dopo]

## Quick Win (Top 5)
[Le 5 modifiche a più alto impatto, ranked per effort vs impatto SEO]
```

La sezione "Quick Win" è critica. Dice all'utente cosa fare per primo. Ranking per il rapporto impatto SEO / effort di implementazione. Metti sempre in cima le modifiche facili ad alto impatto.

## Gestione Lingua

- Default all'italiano se il contenuto è in italiano
- Tutti i suggerimenti di ottimizzazione devono essere nella lingua del contenuto
- La keyword research deve essere nella lingua del contenuto (cerca keyword italiane per contenuto italiano)
- Il report strutturale (header di sezione, spiegazioni) può essere nella lingua di conversazione dell'utente

## Iterazione

Dopo aver consegnato il report, l'utente può chiedere:
- Keyword research più approfondita su un sottotopic
- Strutture di heading alternative
- Più varianti di meta description
- Ottimizzazione di una sezione specifica
- Una versione riscritta di un paragrafo con keyword integrate

Gestisci i follow-up usando il contesto già raccolto. Non rifare il fetch a meno che l'utente non fornisca un URL diverso.

---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
