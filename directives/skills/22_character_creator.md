# SA5 — Character Creator (Brand Cast)

**Agente:** SA5 (Creative Concepts)
**Output:** `11_Characters/<nome-personaggio>/headshot.png + fullbody.png`
**Modello default:** GPT Image 2 (`openai/gpt-image-2`) via fal.ai o Higgsfield

---

## Cosa produce

Per ogni personaggio: 2 immagini in coppia — headshot + full body — format 3:4.
- **Headshot:** ritratto studio frontale, flash diretto, sfondo grigio
- **Full body:** casting digital completo, face reference = headshot

Batch default: 5 personaggi per run. Range: 1-10 per batch.

---

## Step 0 — Protezione cartella + auto-discovery

```bash
PWD_ABS="$(pwd)"
TARGET="${PWD_ABS}"
# [blocco protezione standard]
mkdir -p "$TARGET/11_Characters" "$TARGET/_meta"
```

Auto-discovery: cerca Brand DNA in `02_Brand_DNA/`, personaggi esistenti in `11_Characters/`.

---

## Step 1 — Quanti personaggi?

> "Quanti personaggi vuoi creare? Default 5 per un cast completo, puoi scegliere da 1 a 10."

Cattura come `N`.

---

## Step 2 — Auto o manuale?

Solo se Brand DNA trovato:
> "Ho trovato il tuo Brand DNA. Come preferisci costruire il cast?
> 1. **Auto.** Leggo il Brand DNA e propongo N personaggi distinti che si adattano al brand.
> 2. **Manuale.** Compili tu i dettagli per ogni personaggio."

---

## Step 3 — Raccolta caratteristiche

**Se AUTO:** Leggi Brand DNA (target audience, voice adjectives, fotografia, regole visive). Genera N profili distinti e coesi — diversi per età, etnia, corporatura — presenta tutti in un unico messaggio, aspetta approvazione.

**Se MANUALE:** Per ogni personaggio, mostra questo form esatto:

```
Personaggio [I] di [N]:

IDENTITÀ
Età:
Genere:
Nazionalità:

VISO
Carnagione:
Mandibola:
Forma del viso:
Forma occhi:
Colore occhi:
Sopracciglia:
Naso:
Labbra:
Barba/peluria:
Lentiggini/dettagli pelle:
Zigomi:

CAPELLI
Colore:
Stile:

CORPORATURA
Altezza:
Tipo:

ABBIGLIAMENTO
Top:         (es. Hoodie bianco oversize)
Pantaloni:   (es. Jeans blu)
Scarpe:      (es. Air Force 1 bianchi)
Accessori:   (es. Catena d'oro, cappello nero)

LOOK
Tono:        (es. Grezzo e autentico, editoriale, street, luxury)
```

Campi abbigliamento vuoti → defaults: t-shirt bianca, jeans blu, sneakers bianche. Campi identità/viso/capelli vuoti = lasciare vuoti, non inventare.

---

## Step 4 — Naming

Chiedi N nomi (uno per personaggio, formato slug: lowercase, trattini). Valida che non collidano con cartelle esistenti in `11_Characters/`.

---

## Step 5 — Conferma batch + spec files

Mostra riepilogo cast. Crea per ogni personaggio:
- `$WORKDIR/11_Characters/<nome>/character-spec.json`
- `$WORKDIR/11_Characters/<nome>/characteristics.md`

---

## Step 6 — Scelta modello

> "Quale modello per il cast?
> 1. **GPT Image 2** (raccomandato). Alta qualità, 2400×3200 px (3:4). Il migliore disponibile.
> 2. **Nano Banana 2.** Alternativa più economica. Solo motivo: costo inferiore.

---

## Step 7 — Scelta percorso generazione

> "Come vuoi generare le immagini?
> **A.** Manuale — copia i prompt e incollali nel modello scelto
> **B.** Higgsfield MCP — via CLI Higgsfield (richiede subscription)
> **C.** Fal.ai pay-per-result — ~$0.30/personaggio su GPT Image 2
> **D.** Web UI via Playwright — guida automatica ChatGPT o AI Studio"

---

### Percorso B — Higgsfield CLI

Per ogni personaggio, in ordine STRETTO (headshot → full body):

**Headshot (text-to-image, senza reference):**
```bash
"$HIGGS_BIN" generate create gpt_image_2 \
  --prompt "$(cat /tmp/character-headshot-<nome>-$$.txt)" \
  --aspect_ratio "3:4" --quality "high" --resolution "4k" \
  --wait --wait-timeout 5m --json
```

**Full body (con headshot come reference):**
```bash
"$HIGGS_BIN" generate create gpt_image_2 \
  --prompt "$(cat /tmp/character-fullbody-<nome>-$$.txt)" \
  --aspect_ratio "3:4" --quality "high" --resolution "4k" \
  --image "$WORKDIR/11_Characters/<nome>/headshot.png" \
  --wait --wait-timeout 5m --json
```

Personaggi diversi possono girare in parallelo (max 5), ma dentro ogni personaggio l'ordine è fisso.

### Percorso C — Fal.ai

**Headshot GPT Image 2:**
- `model: "openai/gpt-image-2"`
- `image_size: {"width": 2400, "height": 3200}`
- `quality: "high"`, `num_images: 1`, `output_format: "png"`
- **NON passare `safety_tolerance`** — il modello GPT Image 2 la rifiuta

**Full body GPT Image 2 (con headshot come reference):**
- `model: "openai/gpt-image-2/edit"`
- `image_urls: [$HEADSHOT_URL]`
- Stessi parametri dimensione/qualità

**Nano Banana 2:**
- `model: "fal-ai/nano-banana-2"` / `"fal-ai/nano-banana-2/edit"`
- `aspect_ratio: "3:4"`, `resolution: "2K"`, `safety_tolerance: "4"`

---

## Prompt template — Headshot

```
Clean front facing studio portrait. Figure looking straight into the lens.

Character: {characteristics}

Clothing: {clothing}

Facial features: Clean natural skin, no makeup, no retouching. Natural skin texture, slightly visible pores, minimal freckling. Keep natural facial asymmetry. Groomed but natural brows and lashes.

Pose: Upright posture, head straight. Tight vertical headshot, from above head to chin. Eyes straight to camera. Neutral expression, no smile. Keep clothing out of frame.

Light: Direct on-camera flash. Every skin detail visible. Subtle specular highlights on T-zone. Minimal shadow, flat backdrop.

Camera: Full frame, 75-85mm, f/8. Sharp throughout. 3:4 vertical. 5750-5800K white balance. No grading.

Background: Clean pale grey, no texture.
```

## Prompt template — Full body

```
Full body studio shot. Face and full anatomical structure matched exactly to the reference image.

Character: {characteristics}

Facial reference: Maintain exact face consistency with reference. Matching throughout.

Pose: Full body visible, small gap top and bottom. Upright relaxed stance, arms at sides. Eyes straight to camera, neutral expression.

Clothing: {clothing}

Camera: Full frame, 75-85mm, f/8. Sharp head to feet. 3:4 vertical. 5750-5800K. No grading.

Background: Same pale grey as reference, no texture.
```

---

## Regole critiche

- **Headshot prima, full body dopo** — ordine fisso per ogni personaggio
- **Mai generare senza conferma esplicita** — ogni run richiede `yes`
- **Mai sovrascrivere senza consenso** — se cartella esiste già con immagini, chiedi
- **`openai/gpt-image-2/edit` NON accetta `safety_tolerance`** — ometti sempre
- **Spec files PRIMA della generazione** — `character-spec.json` e `characteristics.md` devono esistere prima di qualsiasi image call
