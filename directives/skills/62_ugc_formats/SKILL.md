---
name: 62_ugc_formats
description: Porta d'ingresso agli 11 formati UGC video. Instrada verso il formato giusto e ne esegue la pipeline (piano → anchor → render). Ogni formato è costruito su 10 ad reali di quel formato, smontate shot by shot. SA6.
---

# 62 — UGC Formats (11 formati, una porta d'ingresso)

Undici formati UGC, undici comandi, un router. Ogni formato **toglie un dubbio diverso** e chiede allo spettatore di fidarsi di una cosa diversa. È per questo che sono undici e non uno — ed è anche il criterio con cui si instrada.

**Output:** `05_UGC_Prompts/formats/<formato>/<concept>/`

---

## Il principio che fa la differenza

Due modelli fanno l'ad, e sono bravi a cose **opposte**:

- **Il modello linguistico scrive cosa l'ad È**: chi c'è dentro, com'è la stanza, com'è fatto il prodotto fin dal carattere tipografico sull'etichetta, ogni parola che viene detta. Poi **si toglie di mezzo**.
- **Il modello video dirige.** Inquadrature, tagli, movimento.

Il modello linguistico **non scrive una shot list**, perché è pessimo a farlo — e una shot list scritta da un LLM è esattamente il motivo per cui la maggior parte delle ad AI sembra AI. Questo split è ciò che fa sembrare questi video *girati* invece che *generati*.

**Non violare questa divisione.** Se ti ritrovi a scrivere "shot 1: primo piano, shot 2: campo medio", stai sbagliando skill.

---

## Step 1 — Il formato è già ovvio?

Se l'utente ha nominato un formato o l'ha descritto in modo inequivocabile, **niente menu**. Dillo in una riga e passa la mano.

| Se dice | Vai a |
|---|---|
| unboxing, aprire la scatola, cosa c'è dentro | `/pm-ugc-unboxing` |
| testimonial, recensione cliente, recensione onesta | `/pm-ugc-testimonial` |
| prima e dopo, trasformazione, risultati nel tempo | `/pm-ugc-before-after` |
| problema soluzione, il mio prodotto risolve questo | `/pm-ugc-problem-solution` |
| tutorial, come si usa, insegnare | `/pm-ugc-tutorial` |
| esperto, dermatologo, perché funziona, la scienza | `/pm-ugc-expert` |
| interviste per strada, fermare gli sconosciuti | `/pm-ugc-street-interview` |
| ASMR, soddisfacente, il suono del prodotto | `/pm-ugc-asmr` |
| POV, skit, comico, divertente | `/pm-ugc-pov` |
| green screen, reagire a una recensione o screenshot | `/pm-ugc-green-screen` |
| founder story, perché ho iniziato | `/pm-ugc-founder-story` |

## Step 2 — Ha descritto un OBIETTIVO invece di un formato?

Succede spesso. Consiglia due o tre formati **per nome, col motivo**, poi mostra la lista completa così può scavalcarti. Instrada su cosa l'ad deve **FARE**:

| Vuole... | Formati |
|---|---|
| dimostrare che funziona | Before/After, Problem/Solution, Tutorial |
| farsi credere da uno sconosciuto | Testimonial, Street Interview, Expert |
| spiegare **perché** funziona | Expert, Tutorial |
| far venire voglia | Unboxing, ASMR |
| farsi guardare e condividere | POV Skit, Street Interview |
| costruire il brand invece di vendere un pezzo | Founder Story |
| usare una recensione/screenshot/press che ha già | Green Screen |

## Step 3 — Altrimenti mostra il menu

Raggruppato per **il dubbio che ogni formato toglie**, perché è quella la differenza vera.

**PROVA — lo spettatore dubita che funzioni**

| Formato | | Durata |
|---|---|---|
| `/pm-ugc-problem-solution` | Nomina un dolore, mostralo fallire, poi il prodotto che lo chiude. | 20-27s |
| `/pm-ugc-before-after` | Due stati della stessa cosa, confrontati onestamente. | 15-24s |
| `/pm-ugc-tutorial` | Insegna un risultato, step by step, col prodotto come strumento. | 22-30s |

**PERSONE — lo spettatore dubita della fonte**

| Formato | | Durata |
|---|---|---|
| `/pm-ugc-testimonial` | Un cliente vero dice cosa è cambiato, parole sue, in camera. | 20-30s |
| `/pm-ugc-expert` | Qualcuno competente spiega **perché** funziona, non *che* funziona. | 22-30s |
| `/pm-ugc-street-interview` | Sconosciuti in pubblico, risposte non copionate, nessun interesse in gioco. | 22-30s |
| `/pm-ugc-founder-story` | Il fondatore racconta perché questa cosa esiste. | 24-30s |

**DESIDERIO — lo spettatore deve volerlo**

| Formato | | Durata |
|---|---|---|
| `/pm-ugc-unboxing` | Da sigillato a rivelato, con la prima reazione come premio. | 18-27s |
| `/pm-ugc-asmr` | I suoni e le texture del prodotto reggono tutta l'ad. | 15-25s |
| `/pm-ugc-pov` | Situazione riconoscibile, giocata per una risata, risolta dal prodotto. | 15-25s |

**PROVA ESTERNA**

| Formato | | Durata |
|---|---|---|
| `/pm-ugc-green-screen` | Un creator che reagisce, girato pulito perché la cosa si aggiunga dopo. | 20-30s |

Chiedi quale, in una riga. Prendi la risposta e passa la mano.

---

## Dillo PRIMA che scelga, quando è vero

Ognuna di queste ferma un run a metà se la scopri dopo:

- **Testimonial, Expert e Street Interview richiedono la VOC.** Le parole vengono da linguaggio cliente reale, mai inventate. Senza VOC su file → prima `/pm-dati-qualitativi`.
- **Founder Story richiede una foto vera del fondatore.** Il fondatore non si genera mai.
- **Before/After ha un avviso di piattaforma** su dimagrimento, salute e beauty, dove Meta limita le immagini prima/dopo.
- **ASMR funziona meglio per brand già riconosciuti.** Misura negativamente per quelli sconosciuti. Va detto, non è un motivo per rifiutare.
- **Green Screen produce solo il girato.** Lo screenshot o la recensione li componi tu dopo, nel tuo editor.

---

## Eseguire un formato

1. Carica `formats/<formato>/playbook.md` — la procedura di quel formato.
2. Carica `formats/<formato>/format-spec.md` (cos'è, ordine dei beat, regole dure, failure mode) e `shot-vocabulary.md`.
3. Le 10 coppie di studio stanno in `formats/<formato>/recreation-prompts/` — `anchor/` (il fermo immagine) e `video/` (il movimento). Sono ad **reali** di quel formato, smontate. Usale come banco, non come template da copiare.
4. Motori condivisi: `../_shared/ugc_format_contract.md` · `ugc_script_engine.md` · `ugc_image_engine.md` · `ugc_video_engine.md` · `ugc_run_engine.md` · `natural_voice.md`.

## I tre gate — non negoziabili

| Gate | Cosa | Costo |
|---|---|---|
| **GATE 1 — IL PIANO** | Script riga per riga + forma dell'ad in frasi piane (**non** una shot list) + prompt dell'anchor. Poi FERMATI. | **Gratis** |
| **GATE 2 — ANCHOR** | Permesso di renderizzare il fermo immagine. | Costa |
| **GATE 3 — VIDEO** | Prompt assemblato + anchor approvato + prezzo esatto per durata e risoluzione. Poi aspetta. | Costa |

> **LEGGE DELLA SPESA.** Niente che costi viene generato senza un sì chiaro, specifico e **immediatamente precedente**. Non sul silenzio, non su un forse, non su un'approvazione data per un altro step, e mai su una riportata da un render precedente dello stesso run. **Ogni retry è una nuova spesa e vuole il suo sì.**

GATE 1 è gratis apposta: è l'ultimo momento in cui l'utente vede **tutto** invece di una fetta, e correggere non costa nulla.

## Regole di chiusura

- **Una ad per run.** Non batchare formati.
- **Render path:** Higgsfield (Path B) se loggato, altrimenti fal.ai (Path C), altrimenti Path A (consegni il prompt). **Non esiste Path K** — KIE è mappato non cablato (`execution/kie_api_map.md`).
- A ad finita, **offri le caption**: `63_auto_captions` (`/pm-captions`). Lo script dell'ad è su disco, quindi le caption escono allineate al copy parola per parola.
- Questo router **non scrive, non genera, non spende**. Se ti chiedono di fare l'ad direttamente, instrada e lascia lavorare la skill del formato.
