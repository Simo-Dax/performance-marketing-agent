# SA6 — Pixar Ad (voiceover-first, formato progressione)

**Agente:** SA6 (Asset Production)
**Output:** `18_Pixar_Ads/<slug>/` — un ad 9:16 1080p montato + clip raw, storyboard, manifest
**Modello:** Seedance 2.0 (image-to-video, hook-anchored) — model-agnostic, vedi `execution/tools.md`
**Reference (leggi PRIMA `references/generation-architecture.md` — è la single source of truth):** `pixar-style.md` (art direction + Character Bible per brand) · `pixar-scripting.md` (selezione framework + regole beat) · `scene-bank-191xt.md` + `scene-bank-tutorial-trap.md` (2 ad vincenti bancati) · `hook-still-template.md` · `vo-and-audio.md` · `scripting-frameworks.md` · `seedance-2.0-limits.md`
**Script:** `scripts/` (align_vo, segment_scenes, validate_prompt, build_manifest, frame_check, last_frame, stitch_pixar). Richiede `ffmpeg`/`ffprobe` + faster-whisper.

---

## Il modello in un respiro

Il **formato progressione virale**: *"Cosa succede se ___? Giorno 1… Giorno 30…"* reso come mondo 3D animato in stile Pixar, premium e "carino".

Tu scrivi lo script (voiceover direct-response su UNO dei 12 framework DR, voce parlata naturale, 30-45s, che **chiude sulla CTA** col prodotto che entra come **LA SVOLTA**), l'utente lo registra **una volta** con la sua voce (es. ElevenLabs) e rimette l'audio qui. Da lì: allineamento della voce con whisper, storyboard delle scene sul timing reale della voce, prompt Seedance, montaggio in **un ad 9:16 finito**.

**L'eroe** è un personaggio 3D stile Pixar **castato dal cliente ideale del brand** (un Character Bible bloccato: occhi grandi espressivi, mai perturbante) che **vive** il percorso dentro un mondo interamente animato. I testimoni sono **ALTRI personaggi Pixar, MAI umani reali**. Il **prodotto** si renderizza come prop 3D Pixar dalla sua foto reale, con forma, etichetta, logo, testo e colori **leggibili e fedeli**.

**Consistenza:** l'hook si renderizza image-to-video da uno **still di riferimento approvato**; tutte le altre scene si ancorano al **Character Bible + lo STILL dell'hook** come image reference (**mai** un riferimento video-clip).

**Nessuna voce viene mai caricata al generatore, nessun personaggio fa lip-sync, e NESSUN testo viene mai renderizzato** — niente caption, niente etichette "Giorno 1", niente banner. **È il voiceover a portare ogni milestone.**

---

## REGOLE HARD (sovrascrivono qualsiasi cosa in conflitto)

1. **Voiceover-first.** Lo script si approva PRIMA che esista un prompt. La voce dell'utente è la spina temporale di tutto.
2. **Mai testo renderizzato.** Nessuna caption, nessun label di giorno, nessun banner. Il voiceover porta le milestone.
3. **Mai lip-sync.** I personaggi non parlano: recitano, reagiscono, vivono. La voce sta sopra.
4. **Testimoni = altri personaggi Pixar.** Mai un umano reale in scena.
5. **Il prodotto viene dalla sua foto reale**, ri-rese come prop Pixar mantenendo forma/etichetta/logo/testo/colori. Mai inventato.
6. **Identità via STILL, mai via clip.** Le scene si ancorano al Character Bible + still hook approvato.
7. **Due 🚦 gate umani obbligatori:** GATE 1 transcript (le parole si bloccano prima dei pixel) · GATE 2 storyboard + costo (prima di ogni credito).
8. **Ogni generazione è 4-9s interi.** Ad lunghi = più generazioni tagliate al parlato.
9. **Niente render senza un sì fresco.** Ogni re-roll ne richiede uno nuovo.

---

## Step 0.5 — Cartella, script, venv whisper

```bash
WORKDIR="$PWD"
ROOT="$PWD"; while [ "$ROOT" != "/" ] && [ ! -d "$ROOT/directives/skills/59_pixar_ad/scripts" ]; do ROOT="$(dirname "$ROOT")"; done
SCRIPTS="$ROOT/directives/skills/59_pixar_ad/scripts"
mkdir -p "$WORKDIR/18_Pixar_Ads"
ls "$SCRIPTS"   # 7 script
```
Il venv whisper vive in `~/.cache/pm-agent/whisper-venv` (condiviso con le altre skill video). Se manca, crealo con `uv venv` + `uv pip install faster-whisper` (mai col python dei Command Line Tools macOS: produce venv rotti).

**Auto-discovery:** `02_Brand_DNA/` (art direction, cliente ideale → casting), `01_VOC_Research/` (linguaggio, pain, desideri), `_assets/product-shots/` + foto prodotto, `15_Video_Scripts/` (script approvati da `55_video_script` che l'utente vuole rendere Pixar).

## Step 0 — INTAKE
Raccogli: **foto del prodotto** (etichetta leggibile, obbligatoria) · nicchia e claim sanzionate · l'offerta reale se c'è una chiusura in offerta · durata target (30-45s default) · se l'utente ha già uno script approvato.

## Step 1 — Framework + belief
Scegli **UN** framework dalla libreria DR (`references/scripting-frameworks.md` + `pixar-scripting.md`) adatto a nicchia e stadio di awareness, e **dichiara quale e perché**. Nomina la **belief** che l'ad deve installare.

## Step 2 — Script (solo il transcript del voiceover)
Scrivi le parole parlate: voce naturale (passa da `49_anti_ai_slop` + `context/brand/anti_ai_writing_style.md`), spina a progressione (giorno/settimana), il **prodotto entra come LA SVOLTA**, chiusura sulla CTA. Ancora il linguaggio al VOC.

## Step 2.5 — 🚦 GATE 1: approvazione transcript
Presenta le parole complete nell'ordine di riproduzione. **FERMA IL TURNO.** Le parole si bloccano prima che esista un prompt o una durata. Poi chiedi all'utente di registrarle e rimettere qui l'audio.

## Step 3 — Analisi audio (allinea la voce allo script)
```bash
python3 "$SCRIPTS/align_vo.py" <audio> <transcript> --out vo_timing.json
```
Ottieni i timestamp per parola: **è questa la spina temporale**, non una stima.

## Step 3.5 — Piano personaggio e mondo
Casta l'eroe **dal cliente ideale del Brand DNA** (cita da quale documento viene ogni tratto) e blocca il **Character Bible** (`references/pixar-style.md`). Definisci il mondo animato coerente.

## Step 4 — Storyboard
Mappa la voce sulle scene: **scena 1 = l'anchor dell'hook**, le altre in hard-cut da lì. Usa i due scene bank come riferimento di struttura provata.
```bash
python3 "$SCRIPTS/segment_scenes.py" vo_timing.json --out storyboard.json
```

## Step 5 — Prompt
Scrivi i prompt: hook anchor + tutte le altre identity-locked allo **STILL** dell'hook. Valida ognuno:
```bash
python3 "$SCRIPTS/validate_prompt.py" storyboard.json
```
Exit non-zero = **non dispatchare**.

## Step 5.5 — 🚦 GATE 2: storyboard + costo
Presenta lo storyboard completo e il **costo esatto**. **FERMA IL TURNO**, aspetta un sì esplicito.

## Step 6 — Generazione (prima l'hook, poi il resto in PARALLELO)
Renderizza **l'hook da solo**, fallo approvare (volto, mondo, vibe: tutto il resto eredita), poi **sì fresco** e lancia il resto in parallelo. Path A manuale / B Higgsfield CLI / C fal.ai (`/pm-setup-fal-ai`) / D Playwright.

## Step 6.5 — Frame check (prima di montare)
```bash
bash "$SCRIPTS/frame_check.sh" <clip> <out.png>
```
**LEGGI ogni contact sheet:** identità tenuta, azione renderizzata, **nessun testo**, prodotto a scala e etichetta credibili, nessun umano reale fra i testimoni.

## Step 7 — Assembly
```bash
python3 "$SCRIPTS/build_manifest.py" storyboard.json vo_timing.json --out manifest.json
bash "$SCRIPTS/stitch_pixar.sh" manifest.json out/<slug>.mp4
```
Il montaggio taglia sul parlato, la voce originale resta la traccia, loudnorm −14 LUFS.

## Step 8 — Output + validazione
Pacchetto in `18_Pixar_Ads/<slug>/`: `out/<slug>.mp4`, clip raw, `storyboard.json`, `vo_timing.json`, `manifest.json`, prompt. Stampa i **path assoluti**.

**Valida:** durata ≈ voce · nessun testo renderizzato · identità tenuta su ogni scena · prodotto fedele alla foto · l'ad chiude sulla CTA.

## NEVER DO
Mai testo/caption renderizzati · mai lip-sync · mai umani reali · mai un riferimento video-clip per l'identità (solo still) · mai renderizzare senza sì esplicito · mai inventare il prodotto o una claim non sanzionata · mai saltare i due gate.
