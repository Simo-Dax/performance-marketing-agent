---
description: Parti da un video UGC che ti piace, misuralo shot-by-shot (curva di differenza, non a occhio) e ricostruiscilo col tuo prodotto e il tuo creator. Skill nativa 58_ugc_blueprint (SA6).
argument-hint: [file video locale ≤30s] — oppure allega il video e chiedi il teardown
---

# /pm-ugc-blueprint — UGC Blueprint (reference-driven)

Esegui la skill nativa **`directives/skills/58_ugc_blueprint/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `SKILL.md`. Reference: `gemini-teardown-prompt.md` (prompt locked Route A), `output-template.md` (template blueprint), `swap-and-render.md` (swap + vincoli render).
2. **Step 0.75 è obbligatorio:** offri SEMPRE le due route (A = modello video esterno veloce · B = analisi locale misurata) e **aspetta la scelta**. Mai avviare l'analisi locale senza chiedere.
3. **Route B misura, non guarda:** tagli dalla curva di differenza per-frame (mai `scdet` da solo), primo+medio frame di ogni shot guardati davvero, audio classificato con envelope a bande + whisper locale, lip-sync test per marcare TALKING ON CAMERA vs VOICEOVER.
4. **🚦 Gate 30s** subito dopo il probe: oltre i 30s il render non è possibile in una generazione — metti la scelta all'utente prima di analizzare.
5. Il blueprint è già un deliverable completo. **Offri la ricostruzione, non darla per scontata** (Step 8-12: hero anchor, personaggio dal Brand DNA, swap prompt, script riscritto dal VOC, render).
6. **Voce O musica, mai entrambe.** Niente render senza sì esplicito e costo mostrato. 720p è il tetto.

Richiede `ffmpeg`/`ffprobe`. Output: `17_UGC_Blueprints/<slug>/`.

**Le tre lane UGC:** `57_ugc_studio` (da format bank di winner) · `25_ugc_prompt` (fan-out Andromeda da uno script) · **`58` (da un video specifico che l'utente ha scelto)**. Per scrapare gli ad video di un competitor dalla Ad Library è invece `52_ad_spy_video`.
