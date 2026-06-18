# Prompt Library — Reference / Backup

Libreria di prompt riutilizzabili. **Reference e backup** per la scrittura: quando una skill o un agente deve scrivere un prompt (immagini, video, copy, ricerca) e serve un punto di partenza collaudato, cerca qui prima di inventare da zero.

## Come si usa
- Ogni file `.md` qui è un prompt o un set di prompt per uno scopo (es. `image_prompts.md`, `voc_research_prompts.md`, `strategy_prompts.md`).
- Agenti/skill: **consultare questa cartella come fallback/reference**, non sostituisce le istruzioni della skill ma le supporta.
- Direttiva: vedi `claude.md` → "Prompt Library".

## Organizzazione suggerita
```
prompts/
├── image/          ← prompt GPT Image 2 / Nano Banana 2 (static, product shot)
├── video/          ← prompt Seedance 2.0 (UGC)
├── research/       ← prompt ricerca VOC / market / competitor
├── copy/           ← prompt copywriting per piattaforma
└── strategy/       ← prompt insight / brand strategy / offer design
```

> Popola questa libreria man mano. È reference, non obbligo: le skill funzionano anche se vuota, ma con la libreria piena la qualità e la coerenza migliorano.
