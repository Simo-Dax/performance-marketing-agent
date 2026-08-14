---
description: UGC Studio format-first — ordini un mix di formati provati (testimonial/before-after/unboxing/direct-to-camera), lo studio scrive, renderizza, taglia con edit grammar e assembla ad 9:16 finiti. Skill nativa 57_ugc_studio (SA6). Default per gli UGC video.
argument-hint: [mix formati es. "2 testimonial + 1 unboxing"] [foto face/body/prodotto] [voice clip ≤15s]
---

# /pm-ugc-studio — UGC Studio (format-first)

Esegui la skill nativa **`directives/skills/57_ugc_studio/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. **Leggi PRIMA le law file** (vincono su tutto in caso di conflitto): `references/render-laws.md` (edit grammar, leggi di generazione, lane, pacing), `references/pipeline-contracts.md` (contratti JSON + argv), poi il/i `references/scene-bank-*.md` dei formati ordinati.
2. Segui integralmente `SKILL.md` Step 0→10. Output sotto `05_UGC_Prompts/studio/<order-slug>/`.
3. **Regole non negoziabili:** generazioni 4-9s interi (mai 10s+) · la gen non è un'inquadratura, il montaggio la affetta · nessun testo renderizzato (caption in `captions.txt`) · prova solo da foto reali.
4. **Due 🚦 gate umani:** GATE 1 = transcript (le parole si bloccano prima dei prompt) · GATE 2 = costo **+ cut map** (l'utente approva il ritmo, non solo il prezzo). Più un sì fresco prima di ogni credito e a ogni re-roll.
5. Percorsi: A manuale / B Higgsfield CLI / C fal.ai (`/pm-setup-fal-ai` prima) / D Playwright.
6. Richiede `ffmpeg`/`ffprobe`. Gli script stanno in `directives/skills/57_ugc_studio/scripts/` (risolti cercando verso l'alto dalla pwd).

**Rapporto con `/pm-ugc-video` (`25_ugc_prompt`):** questo studio è il **default** per gli UGC video (parte da formati provati). La factory `25` resta l'alternativa per il fan-out Andromeda a 4 varianti da uno script unico. Le due non si toccano: 57 scrive solo sotto `studio/`.
