---
description: UGC Factory (Seedance 2.0, Andromeda) — da hook+script a 4 ad MP4 montati (25-45s), 4 hook unici + b-roll ladder, gen <10s, 2 gate (transcript+costo), 4 path. Skill nativa 25_ugc_prompt (SA6).
argument-hint: [niche / brief prodotto]
---

# /pm-ugc-video — UGC Factory (Seedance 2.0, Andromeda)

Esegui la skill nativa **`directives/skills/25_ugc_prompt/SKILL.md`** (SA6 — Asset Production). Reference in `references/` (generation-architecture **da leggere per primo**, andromeda-variation, scripting-frameworks, hook-library, seedance-2.0-limits, consistency-and-assembly, VERIFIED-backend-facts). Script in `scripts/` (segment_script.py, validate_payload.py, build_manifest.py, stitch.sh — richiede ffmpeg/ffprobe/jq).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/25_ugc_prompt/SKILL.md`. Leggi `references/generation-architecture.md` per primo.
2. Step 0.5: risolvi `$AILAB` (pwd) e `$SCRIPTS`; auto-discovery character in `11_Characters/`, prodotto in `_assets/`, VOC/Brand DNA.
3. Intake 4 asset (face, body, product+misura, voice ≤15s) + niche. Hook da `hook-library` + VOC (**no TikTok scraping**).
4. Script con framework → 4 ad Andromeda (4 hook unici + b-roll ladder 0/1/2/2, ognuno chiude su CTA).
5. 🚦 GATE TRANSCRIPT (Step 3.5) → 🚦 GATE COSTO/PACING (Step 4, pacing via `segment_script.py`, ogni gen <10s ~3.5wps). Ferma e attendi approvazione esplicita a entrambi.
6. Scelta path A/B/C/D. Genera, splitta hook reel, valida payload, monta con `build_manifest.py` + `stitch.sh`.
7. Output: `05_UGC_Prompts/factory/<slug>/` (4 MP4 in `out/`, clip in `clips/`, manifest).

Conferma il costo prima di qualsiasi generazione.
