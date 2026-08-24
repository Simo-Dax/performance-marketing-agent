---
description: Menu degli 11 formati UGC video. Instrada al formato giusto in base al dubbio che l'ad deve togliere. Non scrive, non genera, non spende. Skill nativa 62_ugc_formats (SA6).
argument-hint: [formato o obiettivo] — es. "unboxing", oppure "devo dimostrare che funziona"
---

# /pm-ugc — Porta d'ingresso UGC (11 formati)

Esegui la skill nativa **`directives/skills/62_ugc_formats/SKILL.md`** (SA6 — Asset Production), **modalità router**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Segui `SKILL.md` Step 1→3. **Se il formato è già ovvio dalla richiesta, niente menu**: dillo in una riga e passa la mano al comando del formato.
2. Se ha descritto un **obiettivo** invece di un formato, consiglia 2-3 formati per nome col motivo, poi mostra la lista completa così può scavalcarti.
3. **Dì le precondizioni PRIMA che scelga**, quando valgono — ognuna ferma un run a metà se la scopre dopo:
   - Testimonial / Expert / Street Interview → **richiedono la VOC**
   - Founder Story → **richiede una foto vera del fondatore**
   - Before/After → **avviso piattaforma** su dimagrimento, salute, beauty
   - ASMR → funziona meglio su brand già riconosciuti
   - Green Screen → produce **solo il girato**, la composizione la fai tu
4. **Questo router non scrive, non genera, non spende.** Se ti chiedono di fare l'ad direttamente, instrada e lascia lavorare la skill del formato.

## I formati, per dubbio che tolgono

**Prova** — dubita che funzioni: `/pm-ugc-problem-solution` · `/pm-ugc-before-after` · `/pm-ugc-tutorial`
**Persone** — dubita della fonte: `/pm-ugc-testimonial` · `/pm-ugc-expert` · `/pm-ugc-street-interview` · `/pm-ugc-founder-story`
**Desiderio** — deve volerlo: `/pm-ugc-unboxing` · `/pm-ugc-asmr` · `/pm-ugc-pov`
**Prova esterna**: `/pm-ugc-green-screen`

Da dove partire: **Problem/Solution** o **Testimonial** funzionano per quasi ogni prodotto. Per vedere la pipeline girare pulita, **ASMR** è il render più affidabile del set.

**Le altre lane UGC:** `58_ugc_blueprint` (`/pm-ugc-blueprint`, parte da un video reference che hai scelto) · `25_ugc_prompt` (`/pm-ugc-video`, fan-out a 4 ad distinte dallo stesso script).
