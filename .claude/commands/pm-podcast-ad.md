---
description: Ad finto-podcast a due host: carichi 2 volti + 2 voci, la skill scrive, renderizza in parallelo e monta un 9:16 che legge come una clip vera. Skill nativa 61_podcast_ad (SA6).
argument-hint: [2 immagini host] [2 voice clip 10-15s] [prodotto]
---

# /pm-podcast-ad — Podcast Ad Factory

Esegui la skill nativa **`directives/skills/61_podcast_ad/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. **Leggi `references/backend-higgsfield.md` e `voice-and-parallel.md` prima del primo render** — sono il motivo per cui il parallelo funziona.
2. Input: **1 immagine + 1 voice clip (10-15s) per host**. La skill non genera volti né voci: consuma gli upload. I volti possono venire da `11_Characters/`.
3. Ogni battuta = una generazione singola-speaker 4-9s, ancorata ai **byte dell'immagine** + un **ri-taglio con fingerprint unico** della voce. **Nessun riferimento video, mai.**
4. **🚦 GATE transcript** (parole prima dei pixel) · **🚦 GATE costo** (mai renderizzare senza un "vai" esplicito).
5. Dopo i render è tutto **montaggio gratis**: taglio word-accurate con whisper, ~0.2s dopo l'ultima parola, concat in ordine di conversazione, −14 LUFS.
6. Sguardi **specchiati**, nessun host guarda in camera. Output: `20_Podcast_Ads/<slug>/`. Richiede ffmpeg + faster-whisper.
