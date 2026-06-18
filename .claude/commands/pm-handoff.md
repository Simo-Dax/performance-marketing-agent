---
description: Meta Ads handoff — prepara un prompt context-rich da incollare in claude.ai web dove gira il Meta Ads MCP. Skill nativa 30_meta_handoff (Post-SA6).
argument-hint: [modalità: analisi|build]
---

# /pm-handoff — Meta Ads Handoff

Esegui la skill nativa **`directives/skills/30_meta_handoff.md`** (Post-SA6).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/30_meta_handoff.md`.
2. REGOLA HARD ASSOLUTA: questa skill NON chiama mai Meta MCP. Il MCP di Meta funziona solo in claude.ai web, non in Claude Code. Se vedi tool `meta_*` o `mcp__meta_*`, fermati.
3. Due modalità: analisi campagne esistenti o build nuove campagne.
4. Auto-discovery dei path progetto, riassumi (non incollare documenti lunghi).
5. Output: prompt markdown in `09_Meta_Handoff/` + stampa in chat + istruzioni per incollarlo in claude.ai.

Tutto PAUSED di default. Budget in centesimi.
