# SA6 — Product Shot Generator

**Agente:** SA6 (Asset Production)
**Output:** `_assets/product-shots/<output-name>/<output-name>_v1.png` (auto-increment v1, v2, v3...)
**Modello default:** GPT Image 2 (`openai/gpt-image-2/edit`)

---

## Tre modalità in un'unica skill

| Modalità | Descrizione |
|---|---|
| **Studio** | Prodotto su sfondo piatto. Nessuna persona. |
| **Held** | Prodotto tenuto in mano. Mani/braccia visibili. |
| **Worn/Used** | Prodotto indossato (abbigliamento) o usato attivamente (skincare, drink) |

**Regola reference universale:** ogni generazione carica le stesse reference — immagine prodotto + (per Held/Worn con personaggio salvato) `fullbody.png`. Mai caricare output precedenti come reference.

---

## Step 0a — Protezione cartella

```bash
mkdir -p "$TARGET/_assets/product-images" "$TARGET/_assets/product-shots" "$TARGET/_meta"
```

## Step 0b — Auto-discovery contesto progetto

```bash
ls "$WORKDIR/11_Characters/" 2>/dev/null
ls -t "$WORKDIR/02_Brand_DNA/"*.html 2>/dev/null | head -n 1
ls "$WORKDIR/_assets/product-shots/" 2>/dev/null
```

Informa in una riga: "Contesto: Brand DNA trovato, 3 personaggi disponibili (sofia, kai, marcus)."

---

## Step 1 — Selezione immagine prodotto

Cerca in `$WORKDIR/_assets/product-images/*.{png,jpg,jpeg,webp}`. Se trovate, mostra come lista numerata. Se non trovate:
> "Copia la tua immagine prodotto in `$WORKDIR/_assets/product-images/`. Filename minuscolo con trattini (es. `pynk-can-pink.jpg`). Dimmi quando è pronta."

Cattura path come `$SRC_IMG`.

---

## Step 2 — Scelta modalità

> "Che tipo di shot vuoi?
> 1. **Studio.** Prodotto su sfondo piatto. Nessuna persona.
> 2. **Held.** Prodotto tenuto in mano.
> 3. **Worn/Used.** Prodotto indossato o usato attivamente."

---

## Step 3 — Fonte persona (solo Held e Worn)

Se personaggi esistono:
> "Chi è nello shot?
> 1. **Usa personaggio salvato** (raccomandato). Disponibili: <lista>. Migliore per coerenza del volto.
> 2. **Persona random.** Descrivi in una riga.
> 3. **Skip.** Il modello improvvisa."

Se nessun personaggio: suggerisci di crearne uno prima (skill `22_character_creator`). Offri random o skip.

Per random: "Descrivi la persona in una riga (es. `donna sulla trentina, mediterranea, unghie curate`)."

---

## Step 4 — Interazione (solo Worn)

> "Qual è l'interazione? (es. `indossa la maglietta`, `applica il siero sul viso con la punta delle dita alla guancia`, `beve dal barattolo, avvicinato alle labbra`)"

---

## Step 5 — Background/scena

Studio: "Che sfondo? Default bianco pulito. Es. `beige morbido`, `verde salvia pallido`, `nero opaco`."

Held/Worn:
- **A. Sfondo piatto:** colore o superficie (es. `beige seamless pallido`)
- **B. Scena lifestyle:** ambiente reale in una riga (es. `cucina mattutina luminosa, bancone in marmo`)

---

## Step 6 — Aspect ratio

`1:1` square (default), `9:16` vertical, `4:5` portrait, `16:9` horizontal.

---

## Step 7 — Modello

GPT Image 2 (raccomandato) o Nano Banana 2 (solo se si vuole ridurre i costi).

---

## Step 8 — Conferma + spec file

Mostra riepilogo. Crea `$WORKDIR/_assets/product-shots/<output-name>/product-shot-spec.json`.

---

## Percorsi generazione

Stesso pattern A/B/C/D delle altre skill. Path B via Higgsfield CLI, Path C via fal.ai.

### Percorso C — Fal.ai

Carica `$SRC_IMG`. Se personaggio salvato, carica anche `fullbody.png`. Costruisci `image_urls`.

**GPT Image 2 — dimensioni per aspect ratio (max edge 3840px, max totale 8.294.400px, multipli di 16):**
- `1:1` → `{"width": 2880, "height": 2880}`
- `9:16` → `{"width": 2160, "height": 3840}`
- `4:5` → `{"width": 2560, "height": 3200}`
- `16:9` → `{"width": 3840, "height": 2160}`

`model: "openai/gpt-image-2/edit"`, **senza `safety_tolerance`**.

**Nano Banana 2:** `model: "fal-ai/nano-banana-2/edit"`, `safety_tolerance: "4"`, `resolution: "2K"`.

---

## Prompt templates

### Studio
```
The reference image defines every detail of the product. Reproduce it without alteration. Every colour, surface, text element, and proportion must match exactly. Reproduce all text as written.

Light: single soft overhead source. Even coverage, no hard shadows.
Background: <background>. Flat solid colour, no gradient, no texture.
Product centred and upright. No hands, no props.
Format: <orientation> framing for <aspect> output.
```

### Held
```
[Stessa apertura prodotto di Studio]

<person_block>

Person holds product naturally, label fully readable. Natural hand-to-product interaction.
Scene: <background>.
Light: Natural even daylight, no harsh shadows. Clean neutral colour grade.
Camera: 50mm equivalent, f/2.8, natural eye level.
Format: <orientation> framing for <aspect> output.
```

### Worn/Used
```
[Stessa apertura prodotto di Studio]

<person_block>

Interaction: <interaction>. Natural, unforced. Product fully visible, label readable.
Scene: <background>.
Light: Natural even daylight, no harsh shadows.
Camera: 50mm equivalent, f/2.8, sharp focus on interaction zone.
Format: <orientation> framing for <aspect> output.
```

**Sostituzione `<person_block>`:**
- Personaggio salvato: `"The person in the shot must exactly match the second reference image. Maintain face consistency, skin tone, hair, features, body proportions. Characteristics: <person_description>."`
- Random: `"The person is <person_description>."`
- Skip: `"A person is in the shot."`

---

## Step 11 — Loop post-v1

Dopo ogni generazione:
> "Salvato in: `<path>_vN.png`. Cosa vuoi fare?
> 1. Angolo diverso
> 2. Cambia personaggio (solo Held/Worn)
> 3. Cambia sfondo/scena
> 4. Aggiusta interazione (solo Worn)
> 5. Rigenera (stesso prompt, risultato diverso)
> 6. Fatto"

Ogni variazione: aggiorna spec file, riusa stesso percorso `$PATH_CHOICE`, auto-increment versione.

---

## Regole critiche

- **Una immagine per call Fal** — variazioni dal loop post-v1
- **Mai generare automaticamente** — ogni run richiede `yes` esplicito
- **Mai sovrascrivere** — auto-increment `_v1`, `_v2`, `_v3`
- **Regola reference universale:** prodotto sempre. Personaggio se impostato. Mai caricare output precedenti.
- **`openai/gpt-image-2/edit` NON accetta `safety_tolerance`**
