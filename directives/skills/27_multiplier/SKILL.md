# SA6 — Winning Ad Multiplier 2.0 (Variazioni Andromeda-Compliant)

**Agente:** SA6 (Asset Production)
**Output:** `07_Multiplied_Ads/variations-[YYYY-MM-DD].md` + immagini opzionali
**Modello default:** GPT Image 2

---

## Perché questa skill esiste

L'algoritmo Andromeda di Meta raggruppa ad con embedding visivi simili nello stesso Entity ID e mostra solo uno di essi nell'asta. Se generi 8 ad che condividono la stessa scena, palette colori e composizione (anche con copy diverso), Andromeda li tratta come un unico ad e sopprime gli altri 7.

Per ottenere 8 ticket d'asta invece di 1, ogni ad deve essere genuinamente diverso sia nell'angolo strategico SIA nel mondo visivo.

---

## Input richiesti (tutto in un unico messaggio)

> "Per moltiplicare il tuo ad vincente ho bisogno di:
>
> 1. **Il tuo ad vincente** — carica/incolla l'immagine statica
> 2. **Le tue immagini prodotto** — 1-3 foto
> 3. **Il tuo documento VOC**
> 4. **Il tuo documento Brand DNA**
> 5. **Quante variazioni?** (5-8)
> 6. **Hai un'offerta specifica?** (sconto, bundle, ecc. — se no: "nessuna offerta")
> 7. **L'offerta va in ogni variazione o solo alcune?** ("all variations" o "mix")"

Auto-discovery: controlla `01_VOC_Research/` e `02_Brand_DNA/`.

---

## FASE 1 — Analisi dell'ad vincente

Analizza l'immagine dell'ad. Estrai:
- **Scheletro strutturale** (pattern layout da preservare)
- **Meccanica di conversione** (il PERCHÉ funziona — OBBLIGATORIO in ogni variazione)
- **Hook, awareness level, angolo attuali** (per scegliere quelli DIVERSI)
- **Scena visiva e mondo colori** (per divergere consapevolmente)

All'utente: "Ad vincente analizzato. Costruisco la strategia variazioni..."

---

## FASE 2 — Strategia variazioni (mostrare PRIMA dei prompt)

Costruisci una tabella con una riga per variazione:

| N | Angolo copy | Hook mechanic | Awareness | Registro emotivo | Scena visiva | Mondo colori | Differenziatore vs originale |
|---|---|---|---|---|---|---|---|

**Regole:**
- Nessun angolo copy, hook mechanic, awareness level O scena visiva in comune tra variazioni
- Ogni variazione deve essere genuinamente diversa — stessa scena + copy diverso = stesso Entity ID Andromeda
- Meccanica di conversione preservata in tutte (se l'originale vince per un claim boldness → ogni variazione ha un claim forte)

**Mostra la tabella e aspetta conferma** prima di scrivere i prompt.

---

## FASE 3 — Prompt variazioni (dopo conferma)

Scrivi tutti i prompt, modello-agnostici (funzionano con GPT Image 2 e Nano Banana 2).

Formato ogni variazione:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VARIAZIONE N — [Nome angolo]
Awareness Level: [livello]
Hook: [meccanica]
Emozione: [registro]
Scena Visiva: [breve descrizione]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Prompt completo]
```

**Regole copy:**
- Guida word count (non lock rigido) — usa word count originale come riferimento per equilibrio visivo (±2 parole su titoli, ±1 su CTA e badge)
- Tutto il copy viene da Brand DNA + VOC — zero copy generico inventato
- Le immagini prodotto portano il prodotto — ogni prompt istruisce il modello a rendere il prodotto dalle immagini caricate

---

## Output format

1. **RIEPILOGO AD VINCENTE** — 4-6 righe strategiche
2. **TABELLA STRATEGIA** — mostrare e aspettare conferma
3. **PROMPT VARIAZIONI** — solo dopo conferma, numerati e etichettati

---

## Scelta modello e percorso

Stesso pattern A/B/C/D delle altre skill.

### Percorso B — Higgsfield CLI

Subset picker: "Quali variazioni (1-N) vuoi generare? Es. '1, 3, 5' o 'all'."

Per 5+ variazioni: usa `run_in_background` per parallelizzare (~90s wall-clock vs minuti sequenziale).

Output: `variation_<N>.png` in `07_Multiplied_Ads/path_b_outputs/`.

### Percorso C — Fal.ai

1. Carica ad vincente + 1-3 immagini prodotto. Cattura come `$IMAGE_URLS`.
2. Per ogni variazione:

**GPT Image 2:**
```json
{
  "model": "openai/gpt-image-2/edit",
  "image_urls": "$IMAGE_URLS",
  "image_size": {"width": 2880, "height": 2880},
  "quality": "high",
  "output_format": "png",
  "num_images": 1
}
```
**Senza `safety_tolerance`.**

**Nano Banana 2:**
```json
{
  "model": "fal-ai/nano-banana-2",
  "resolution": "4K",
  "thinking_level": "high",
  "enable_web_search": true,
  "safety_tolerance": "4",
  "output_format": "png",
  "num_images": 1
}
```

Report ogni 3 variazioni. Salva manifest in `07_Multiplied_Ads/path_c_outputs/manifest.json`.

---

## Regole critiche

- **Variazione visiva obbligatoria** — scena e mondo colori diversi per ogni variazione
- **Preserva la meccanica di conversione** in tutte le variazioni
- **Nessuna variazione semanticamente identica** — se due dicono la stessa cosa allo stesso pubblico nello stesso contesto, Andromeda le raggruppa
- **Mostra la strategia prima** — mai scrivere i prompt finché l'utente non ha confermato la tabella
- **Le immagini prodotto portano il prodotto** — il modello non ri-crea da immaginazione
- **Mai switch silenzioso percorso**
- **Mai addebitare crediti senza `yes` esplicito**

---

## Validazione output

1. Documento variazioni > 8.000 byte
2. N variazioni esatte (5-8 come richiesto)
3. Tabella strategia con 8 colonne per ogni riga
4. Ogni variazione: hook, awareness level E scena visiva distinti da tutte le altre
5. Nessun placeholder
