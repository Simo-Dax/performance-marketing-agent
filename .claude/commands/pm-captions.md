---
description: Brucia le caption in stile locked su un video finito. Se lo script dell'ad è su disco fa force-align, così le caption sono il copy esatto invece della trascrizione. Skill nativa 63_auto_captions (SA6).
argument-hint: [file video] — uno o più; funziona anche su video non prodotti da noi
---

# /pm-captions — Auto Captions

Esegui la skill nativa **`directives/skills/63_auto_captions/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi `references/caption-style.md` **prima** di toccare qualunque valore: lo stile è bloccato, non è regolabile per run.
2. **Dry-run sempre per primo** — `python3 directives/skills/63_auto_captions/scripts/autocaption.py <video> --dry-run`. Stampa le card e l'audit senza renderizzare. Leggile contro quello che l'ad dice davvero.
3. Poi brucia. Scrive `<nome>_captioned.mp4`: **il master pulito non si sovrascrive mai**.
4. **Riporta l'audit coi numeri**, non a sensazione: % nella banda 2-3, card a due righe, punteggiatura, script match. Qualsiasi cosa diversa da `two-row: none` / `punctuation: none` / `script match: True` è un difetto — indaga prima di consegnare.
5. Se compare una riga `FONT:`, il font bloccato non c'era e ha renderizzato altro: **passa quella riga all'utente**, mai in silenzio.
6. Più cut della stessa ad → caption sul **più grande**.

## Da sapere
- **Force-align:** con lo script su disco (`transcript.json`/`timing.json`, auto-scoperti) whisper serve solo per i tempi e le parole vengono dallo script. Senza script, ripiega sulla trascrizione e lo dice.
- **Brand-agnostic:** nessun brand è cablato. Per le maiuscole giuste e per non spezzare il nome su due card, crea `context/brand/caption_vocab.json` (`brand_names` / `proper_nouns` / `fixes`).
- **Mai captionare un video che l'utente non ha chiesto di captionare.** Si offre, non si assume.

Richiede `ffmpeg`/`ffprobe`, Pillow, faster-whisper (venv condiviso `~/.cache/pm-agent/whisper-venv`).
