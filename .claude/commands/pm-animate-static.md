---
description: Trasforma una statica finita in un motion poster 3-8s — i layer si assemblano e l'ultimo frame È la statica originale. Niente musica, niente caption. Skill nativa 56_animate_static (SA6).
argument-hint: [path statica o "scegli"] [durata secondi]
---

# /pm-animate-static — Statica → Motion Poster

Esegui la skill nativa **`directives/skills/56_animate_static.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/56_animate_static.md`.
2. Auto-discovery statiche in `04_Static_Ads/`, `07_Multiplied_Ads/`, `08_Rebuilt_Competitor_Ads/` (o l'utente fornisce l'immagine). Una statica per run.
3. **Leggi davvero l'immagine** (tool Read) e inventaria i layer prima di scrivere il prompt.
4. UNA domanda (hai un'idea o vuoi 3 proposte?) → 3 concept di animazione → l'utente sceglie/modifica.
5. Scrivi il motion prompt con la regola non negoziabile: **l'ultimo frame È esattamente la statica originale**. Niente musica, niente caption, nessun elemento nuovo.
6. 🚦 Gate: durata (default 4s) + risoluzione (720p default) + **costo confermato** prima di renderizzare.
7. Percorsi: A manuale (gratis) · B Higgsfield · C fal.ai (`/pm-setup-fal-ai`). Serve un modello image-to-video con **start+end frame conditioning**.
8. Valida: estrai l'ultimo frame e confrontalo con la statica. Se non combacia → dillo e offri re-render.

Output: `16_Animated_Statics/animated-*.mp4` + il motion prompt `.txt` accanto.
