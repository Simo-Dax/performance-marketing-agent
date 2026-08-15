---
description: Ad dove il cast vende: il problema personificato si auto-sbeffeggia, gli ingredienti si presentano, il prodotto chiede la vendita. I personaggi parlano on camera. Skill nativa 60_talking_object_ad (SA6).
argument-hint: [foto prodotto] [ingredienti/feature da personificare]
---

# /pm-talking-object-ad — Talking Object Ad Factory

Esegui la skill nativa **`directives/skills/60_talking_object_ad/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. **Leggi PRIMA `references/generation-architecture.md`**, poi `talking-object-style.md` (legge di casting) e `talking-object-scripting.md` (formula dialogo).
2. **Dialogue-first, nessun voiceover esterno**: il modello genera voce e immagine insieme, l'audio nativo delle clip È la traccia finale. (Opposto di `59_pixar_ad`, dove la voce è registrata dall'utente e nessuno parla.)
3. Cast: problema personificato (dal **VOC**, non inventato) → eroi ingrediente/feature coi meccanismi **reali** → prodotto che chiede la vendita.
4. **🚦 GATE 1 script + cast** · **🚦 GATE 2 storyboard + costo**. Hook checkpoint prima delle ondate.
5. Verifica sempre che **le parole pronunciate combacino** con lo script approvato (`dialogue_check.py` + ascolto).
6. Output: `19_Talking_Object_Ads/<slug>/`. Richiede ffmpeg.
