# SA6 — Podcast Ad (due host realistici, 9:16)

**Agente:** SA6 (Asset Production)
**Output:** `20_Podcast_Ads/<slug>/` — un ad 9:16 montato + clip raw, transcript, manifest
**Modello:** Seedance 2.0 (immagine + voce, lip-sync e audio inclusi)
**Reference:** `podcast-rules.md` · `backend-higgsfield.md` + `voice-and-parallel.md` (**leggile prima del primo render**: sono il motivo per cui il parallelo funziona) · `cutting-and-assembly.md` · `your-inputs.md`
**Script:** `scripts/` (segment_turns, validate_payload, make_voice_cuts, render_parallel, whisper_cut, build_manifest, stitch_podcast). Richiede `ffmpeg`/`ffprobe` + faster-whisper.

---

## Il modello in un respiro

Due host dall'aspetto reale siedono in uno studio e parlano **fra loro** di un brand/prodotto; la camera stacca su chi parla. **L'utente carica due volti e due voci — tutto il resto lo fa la skill**: scrive lo script, renderizza ogni battuta in parallelo, poi taglia e monta un 9:16 finito che si legge come una clip di podcast vera.

- **INPUT caricati una volta:** **UNA immagine di riferimento + UNA voice clip (10-15s) per host** (due host = due immagini, due voci). La skill **non genera** volti o voci: consuma gli upload.
- Ogni battuta = **UNA generazione singola-speaker** (9:16, 1080p, 4-9s interi). L'identità è **i byte dell'immagine dell'host** (ri-inviati byte-identici); la voce è un **ri-taglio della sua voice clip** passato come riferimento audio. **Nessun input video su nessuna generazione, mai.**
- Per renderizzare **in parallelo in sicurezza**, ogni generazione riceve un **ri-taglio con fingerprint unico** della voce dell'host (piccolo trim + tempo-shift, pitch preservato). **È l'intero motivo per cui il parallelo funziona** — vedi `voice-and-parallel.md` (il gotcha del dedup `_sfx`).
- Dopo i render, **tutto è montaggio (gratis, zero crediti)**: whisper trova i timing esatti per parola, ogni clip si taglia **~0.2s dopo l'ultima parola**, si rimuove il "peep" iniziale, si verifica che ogni clip sia a inquadratura singola, si concatena in ordine di conversazione, loudnorm −14 LUFS.
- I due host **specchiano gli sguardi** (host di sinistra guarda a destra, host di destra guarda a sinistra) così gli stacchi leggono come una conversazione vera. **Nessun host guarda mai in camera.**

---

## REGOLE HARD

1. **Mai renderizzare senza un "vai" umano esplicito** (gate costo, Step 3).
2. **Ogni clip è ancorata da un'IMMAGINE caricata + una VOCE caricata. Nessun riferimento video, mai.**
3. **Voice cut con fingerprint unico per generazione** — un fingerprint speso è bruciato: ogni re-roll vuole un taglio fresco.
4. **Nessun host guarda in camera**, sguardi specchiati fra i due.
5. **Il montaggio è gratis**: esaurisci il loop di taglio prima di ogni re-render.

---

## Step 0.5 — Cartella e script

```bash
WORKDIR="$PWD"
ROOT="$PWD"; while [ "$ROOT" != "/" ] && [ ! -d "$ROOT/directives/skills/61_podcast_ad/scripts" ]; do ROOT="$(dirname "$ROOT")"; done
SCRIPTS="$ROOT/directives/skills/61_podcast_ad/scripts"
mkdir -p "$WORKDIR/20_Podcast_Ads"
ls "$SCRIPTS"   # 7 script
```
Venv whisper in `~/.cache/pm-agent/whisper-venv`. **Auto-discovery:** `11_Characters/` (volti già generati da `22_character_creator` usabili come host), `01_VOC_Research/` + `02_Brand_DNA/` (linguaggio e regole brand), foto prodotto.

## Step 0 — INTAKE
Per **ogni** host: **1 immagine di riferimento** (frontale pulita) + **1 voice clip 10-15s**. Più: nicchia, prodotto, claim sanzionate, offerta, durata target. Verifica le voci con `ffprobe` (10-15s); se più lunghe, chiedi un taglio.

## Step 1 — SCRIPT (dialogo a due, solo parole)
Scrivi la conversazione: battute **brevi e alternate** (6-9 parole per turno, mai due prese consecutive dello stesso host), linguaggio dal VOC, voce naturale (`49_anti_ai_slop`). Deve leggersi come due persone che parlano, non come un annuncio recitato.

## Step 1.5 — 🚦 GATE TRANSCRIPT (hard stop: parole prima dei pixel)
Presenta ogni battuta in ordine di riproduzione. **FERMA IL TURNO.**

## Step 2 — Segmenta e costruisci il render plan
```bash
python3 "$SCRIPTS/segment_turns.py" transcript.txt --out render_plan.json
python3 "$SCRIPTS/validate_payload.py" render_plan.json     # deve PASSARE
python3 "$SCRIPTS/make_voice_cuts.py" render_plan.json "$WORK" voice_cuts/
```

## Step 3 — 🚦 GATE COSTO (hard stop)
Tabella: ogni generazione (id, host, secondi, unità di path) + **totale**. **Mai renderizzare senza un "vai" esplicito.**

## Step 4 — Scelta path (A / B / C)
**A** manuale · **B** Higgsfield CLI (`render_parallel.py` guida submit/poll/download/retry) · **C** fal.ai (`/pm-setup-fal-ai` prima; la voce si carica una volta, nessun bug `_sfx`).

## Step 5 — GENERAZIONE (parallela, solo immagine + voce)
```bash
python3 "$SCRIPTS/render_parallel.py" render_plan.json "$WORK" voice_cuts/ gens/
```
Submit-all → poll → download → **retry gratis con voice cut fresco** su fallimento o avvelenamento `_sfx`. Nessun input video su nessuna generazione.

## Step 6 — TAGLIO (word-accurate, gratis)
```bash
python3 "$SCRIPTS/whisper_cut.py" render_plan.json gens/ clips/
```
Timing per parola, ogni clip finisce ~0.2s dopo l'ultima parola, "peep" iniziale rimosso. Verifica il **match ratio**: sotto il 75% → **ascolta** quella clip prima di montare.

## Step 7 — ASSEMBLY (+ loop di montaggio gratis)
```bash
python3 "$SCRIPTS/build_manifest.py" clips/ render_plan.json --out manifest.json
bash "$SCRIPTS/stitch_podcast.sh" manifest.json out/<slug>.mp4
```
Concatena in ordine di conversazione, 9:16 1080p, loudnorm −14 LUFS. **Ri-tagliare e ri-montare non costa nulla**: esaurisci questo loop prima di proporre un re-render.

## Step 8 — Output + validazione
Pacchetto in `20_Podcast_Ads/<slug>/`. Stampa i **path assoluti**.
**Valida:** ogni clip a inquadratura singola · sguardi specchiati, nessuno in camera · le parole combaciano col transcript approvato · nessuna clip finisce troncata a metà parola · loudness normalizzata.

## NEVER DO
Mai un riferimento video su una generazione · mai riusare lo stesso voice cut su due generazioni · mai renderizzare senza "vai" esplicito · mai far guardare un host in camera · mai proporre un re-render prima di aver esaurito il montaggio (che è gratis).
