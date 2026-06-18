# SA5 — Competitor Ad Rebuild (Ingegneria Inversa)

**Agente:** SA5 (Creative Concepts)
**Output:** `08_Rebuilt_Competitor_Ads/rebuild-[YYYY-MM-DD].md` + immagini opzionali
**Modello default:** GPT Image 2 (`openai/gpt-image-2/edit`)

---

## Cosa produce

Trasforma un ad vincente del competitor in un prompt immagine completo per il proprio brand — con tutti i testi e swap visivi scritti esplicitamente. Opzionalmente: 5 variazioni persona.

---

## Input richiesti (chiedi tutto in un unico messaggio)

> "Per costruire il tuo prompt rebuild ho bisogno di:
>
> 1. **L'ad vincente del competitor** — carica/incolla l'immagine statica
> 2. **Il tuo documento Brand DNA** — incolla il testo o carica il file
> 3. **Il tuo documento VOC** — incolla il testo o carica il file
> 4. **Hai un'offerta o promozione specifica?** (sconto, bundle, trial, ecc. — se no: "nessuna offerta")
> 5. **Vuoi 5 variazioni per buyer persona?**"

Auto-discovery: controlla `01_VOC_Research/`, `02_Brand_DNA/`, `03_Ad_Spy/` per file esistenti e offrili al membro.

---

## Protezione cartella

```bash
mkdir -p "$TARGET/08_Rebuilt_Competitor_Ads/path_b_outputs" \
         "$TARGET/08_Rebuilt_Competitor_Ads/path_c_outputs" \
         "$TARGET/08_Rebuilt_Competitor_Ads/path_d_outputs" "$TARGET/_meta"
```

---

## FASE 1 — Analisi dell'ad competitor

Analizza l'immagine dell'ad competitor. Estrai:
- **Struttura e layout** (scheletro che va preservato nelle variazioni)
- **Meccanica di conversione** (il PERCHÉ funziona — DEVE essere onorato in ogni variazione)
- **Hook e awareness level** attuali (per poter scegliere quelli DIVERSI nelle variazioni)
- **Scena visiva e mondo colori** (per divergere consapevolmente)

Analisi completa interna. All'utente: "Ad analizzato. Costruisco il tuo prompt rebuild..."

---

## FASE 2 — Costruzione prompt rebuild

Costruisci il prompt immagine completo che il modello userà per rigenerare l'ad con il brand dell'utente.

**Regola numero uno:** TU scrivi le parole, non il modello immagine. Ogni elemento testuale deve avere il replacement copy scritto per esteso. MAI scrivere "sostituisci il titolo con qualcosa di rilevante" — scrivi il titolo effettivo.

**Regola conta parole:** Questa è la singola disciplina più importante. Conta le parole di ogni elemento nel competitor ad e rispettale:
- Titolo 4 parole → il tuo titolo è 4 parole (range: 3-5, mai di più)
- CTA 2 parole → il tuo CTA è 2 parole
- Body copy → stessa conta righe e parole approssimative
- Badge → stesso numero parole

Il word count è il blueprint visivo dell'ad. Violarlo = rompere l'ad.

**Ogni copy viene da:** Brand DNA (voce, posizionamento, dettagli prodotto) + VOC (linguaggio cliente, dolori, desideri). Zero copy generico inventato.

---

## FASE 3 — Variazioni persona (se richieste)

Genera 5 prompt completi standalone, uno per ogni buyer persona diversa dal VOC. Stessa struttura e gerarchia visiva dell'originale — cambia solo angolo copy, dolori e linguaggio cliente.

Formato ogni variazione:
```
VARIAZIONE 1 — [Nome/Descrizione Persona]
[Prompt completo]

VARIAZIONE 2 — [Nome/Descrizione Persona]
...
```

---

## Output format

1. **RIEPILOGO ANALISI AD** — 4-6 righe strategiche (tipo hook, layout, meccanica conversione, awareness level)
2. **IL PROMPT REBUILD** — completo, pronto da copiare nel modello immagine
3. **VARIAZIONI PERSONA** — solo se richieste, tutte e 5 complete

---

## Scelta modello e percorso generazione

```
Quale modello?
1. GPT Image 2 (raccomandato) — alta qualità, 4K
2. Nano Banana 2 — alternativa più economica

Come generare?
A. Manuale — copia il prompt nel modello web, carica reference + prodotto
B. Higgsfield MCP — via CLI (richiede subscription)
C. Fal.ai — pay per result (~$0.15 su GPT Image 2)
D. Playwright — guida automatica ChatGPT o AI Studio
```

### Percorso C — Fal.ai

1. Carica competitor ad con `mcp__fal-ai__upload_file`. Carica immagine prodotto. Cattura URLs come `$IMAGE_URLS`.
2. **GPT Image 2:** `model: "openai/gpt-image-2/edit"`, `image_urls: $IMAGE_URLS`, `image_size: {"width": 2880, "height": 2880}`, `quality: "high"`, **senza `safety_tolerance`**
3. **Nano Banana 2:** `model: "fal-ai/nano-banana-2"`, `thinking_level: "high"`, `enable_web_search: true`, `safety_tolerance: "4"`
4. Salva in `08_Rebuilt_Competitor_Ads/path_c_outputs/rebuild_N.png`

---

## Regole critiche

- **Mai cambiare path silenziosamente** — se il percorso scelto fallisce, chiedi: retry, switch to A, o abbandona
- **Mai addebitare crediti senza `yes` esplicito**
- **Il modello decide il copy** — TU scrivi il copy, il modello genera l'immagine
- **Regola word count è NON negoziabile**
- **Variazioni = stesso layout, copy diverso** — non ridisegnare, sostituire precisamente

---

## Validazione output

1. File `rebuild-[YYYY-MM-DD].md` esiste in `08_Rebuilt_Competitor_Ads/`
2. 1 prompt rebuild principale sempre presente
3. 5 variazioni presenti se (e solo se) richieste
4. Nessun placeholder (`[headline]`, `[CTA]`, `[Persona Name]`, `<TODO>`)
5. Ogni testo swap scritto esplicitamente
6. Word count corrisponde all'originale su ogni elemento
