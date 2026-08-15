---
description: Ad in stile Pixar 3D, voiceover-first, formato progressione "Giorno 1… Giorno 30…". Eroe castato dal Brand DNA, nessun testo renderizzato. Skill nativa 59_pixar_ad (SA6).
argument-hint: [foto prodotto] [durata 30-45s] [script approvato opzionale]
---

# /pm-pixar-ad — Pixar Ad Factory

Esegui la skill nativa **`directives/skills/59_pixar_ad/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. **Leggi PRIMA `references/generation-architecture.md`** (single source of truth), poi `pixar-style.md` e `pixar-scripting.md`.
2. Voiceover-first: scrivi lo script → **🚦 GATE 1 transcript** → l'utente lo registra e rimette l'audio → allineamento whisper → storyboard sul timing reale.
3. Eroe castato **dal cliente ideale del Brand DNA** (Character Bible bloccato). Testimoni = altri personaggi Pixar, **mai umani reali**. Prodotto come prop 3D dalla **foto reale**.
4. **Mai testo renderizzato** (niente caption/label giorno), **mai lip-sync**: è il voiceover a portare le milestone.
5. Identità via **STILL** dell'hook, mai via clip video. **🚦 GATE 2 storyboard + costo** prima di ogni credito.
6. Output: `18_Pixar_Ads/<slug>/`. Richiede ffmpeg + faster-whisper.
