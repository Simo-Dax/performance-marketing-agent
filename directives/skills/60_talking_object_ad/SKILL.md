# SA6 — Talking Object Ad (dialogue-first, il cast vende l'ad)

**Agente:** SA6 (Asset Production)
**Output:** `19_Talking_Object_Ads/<slug>/` — un ad 9:16 montato + clip raw, storyboard, manifest
**Modello:** Seedance 2.0 — genera **voce e immagine insieme** (i personaggi parlano ON CAMERA); l'audio nativo delle clip **È** la colonna sonora finita
**Reference (leggi PRIMA `references/generation-architecture.md`):** `talking-object-style.md` (art direction, legge di design dei personaggi, casting vocale) · `talking-object-scripting.md` (formula del dialogo) · `scene-bank-ingredient-parade.md` (bank provato) · `casting-still-template.md` · `seedance-2.0-limits.md`
**Script:** `scripts/` (segment_scenes, validate_prompt, dialogue_check, build_manifest, frame_check, stitch_talking). Richiede `ffmpeg`/`ffprobe`.

---

## Il modello in un respiro

Il formato in cui **è il CAST a vendere**: il **problema del cliente personificato** si auto-sbeffeggia nell'hook, gli **eroi ingrediente/feature** si presentano in prima persona spiegando il proprio meccanismo, **il prodotto entra come la risposta assemblata**, e **il prodotto stesso chiede la vendita**.

**I personaggi PARLANO ON CAMERA.** Il modello genera voce e immagine insieme, quindi **non esiste nessun voiceover esterno** in questa skill: l'audio nativo delle clip è già l'audio finito.

> **Differenza da `59_pixar_ad`:** lì c'è un voiceover registrato dall'utente e i personaggi non parlano mai. Qui **non c'è voce esterna**: il dialogo è generato insieme al video. Sono due formati opposti, non varianti.

---

## REGOLE HARD (sovrascrivono qualsiasi cosa in conflitto)

1. **Dialogue-first.** Script e cast si approvano PRIMA di ogni prompt.
2. **I personaggi parlano on camera** — nessun voiceover esterno, mai. L'audio nativo delle clip è la traccia finale.
3. **La legge di casting** (`talking-object-style.md`) governa il design dei personaggi: il problema personificato, gli ingredienti/feature, il prodotto. Coerenti fra loro nel mondo.
4. **Il prodotto viene dalla sua foto reale** — forma, etichetta, logo, testo, colori fedeli. Mai inventato.
5. **Mai testo renderizzato** (niente caption/label): a parlare è il cast.
6. **Due 🚦 gate umani:** GATE 1 script + cast · GATE 2 storyboard + costo.
7. **Ogni generazione 4-9s interi**, una singola inquadratura continua per clip (il dialogo è "baked in").
8. **Niente render senza sì fresco**; ogni re-roll ne richiede uno nuovo.

---

## Step 0.5 — Cartella e script

```bash
WORKDIR="$PWD"
ROOT="$PWD"; while [ "$ROOT" != "/" ] && [ ! -d "$ROOT/directives/skills/60_talking_object_ad/scripts" ]; do ROOT="$(dirname "$ROOT")"; done
SCRIPTS="$ROOT/directives/skills/60_talking_object_ad/scripts"
mkdir -p "$WORKDIR/19_Talking_Object_Ads"
ls "$SCRIPTS"   # 6 script
```
**Auto-discovery:** `02_Brand_DNA/` (art direction, voce brand), `01_VOC_Research/` (il **dolore** da personificare, in parole reali del cliente), foto prodotto in `_assets/`.

## Step 0 — INTAKE
**Foto del prodotto** (etichetta leggibile, obbligatoria) · nicchia · gli **ingredienti/feature** che diventeranno personaggi · claim sanzionate · l'offerta se c'è una chiusura in offerta.

## Step 1 — IL CAST (legge di casting, non un template)
Definisci: **il problema personificato** (chi è, come si auto-sbeffeggia), **gli eroi ingrediente/feature** (uno per meccanismo reale, mai inventato), **il prodotto** come personaggio finale. Ognuno con design, voce e registro coerenti (`talking-object-style.md`). Il dolore personificato **viene dal VOC**, non dalla fantasia.

## Step 2 — SCRIPT (puro dialogo)
Scrivi **solo dialogo**, seguendo la formula in `talking-object-scripting.md`: hook auto-ironico del problema → presentazioni in prima persona coi meccanismi → il prodotto come risposta assemblata → **il prodotto chiede la vendita**. Voce naturale (`49_anti_ai_slop` + `anti_ai_writing_style.md`). Battute brevi: sono parlate on camera.

## Step 2.5 — 🚦 GATE 1: script + cast
Presenta il cast completo e **ogni battuta**. **FERMA IL TURNO** e aspetta approvazione.

## Step 3 — Casting still
Genera gli still di casting dei personaggi (`casting-still-template.md`) e falli approvare: sono l'àncora di identità di ogni clip.

## Step 4 — Storyboard
```bash
python3 "$SCRIPTS/segment_scenes.py" script.json --out storyboard.json
```
Riempi il bank PRIMARIO (`scene-bank-ingredient-parade.md` come struttura provata).

## Step 5 — Prompt (una inquadratura continua, dialogo baked in)
Un prompt per clip, **una sola inquadratura continua**, con la battuta esatta incorporata. Valida:
```bash
python3 "$SCRIPTS/validate_prompt.py" storyboard.json
python3 "$SCRIPTS/dialogue_check.py" storyboard.json    # le battute combaciano con lo script approvato
```
Exit non-zero = **non dispatchare**.

## Step 5.5 — 🚦 GATE 2: storyboard + costo
Storyboard completo + **costo esatto**. **FERMA IL TURNO**, sì esplicito.

## Step 6 — Generazione (hook checkpoint, poi ondate)
Renderizza **l'hook da solo** → l'utente approva design, voce e vibe del cast (tutto il resto eredita) → **sì fresco** → il resto a ondate parallele. Path A/B/C/D.

## Step 6.5 — VERIFICA parole E immagine (prima di montare)
```bash
bash "$SCRIPTS/frame_check.sh" <clip> <out.png>
```
Per ogni clip: **le parole pronunciate combaciano** con lo script approvato (ascolta/verifica, non dare per scontato) · il personaggio è on-model · **nessun testo renderizzato** · il prodotto è fedele alla foto · una sola inquadratura continua.

## Step 7 — Assembly
```bash
python3 "$SCRIPTS/build_manifest.py" storyboard.json --out manifest.json
bash "$SCRIPTS/stitch_talking.sh" manifest.json out/<slug>.mp4
```
Concatena in ordine di conversazione tenendo l'audio nativo di ogni clip, loudnorm −14 LUFS.

## Step 8 — Output + validazione
Pacchetto in `19_Talking_Object_Ads/<slug>/`. Stampa i **path assoluti**.
**Valida:** ogni battuta pronunciata = script approvato · cast on-model ovunque · nessun testo renderizzato · prodotto fedele · l'ad chiude sulla richiesta di vendita del prodotto.

## NEVER DO
Mai voiceover esterno (rompe il formato) · mai testo renderizzato · mai un ingrediente/meccanismo inventato · mai renderizzare senza sì esplicito · mai saltare i due gate · mai personaggi fuori dalla legge di casting.
