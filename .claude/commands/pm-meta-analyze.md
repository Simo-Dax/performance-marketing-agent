---
description: Meta Ads analyze — opera il Meta Ads MCP read-only dentro Claude Code. Due modalità: quick check (audit single-pass) o deep diagnosis (panel investigator avversariale + referee → diagnosi ranked). Skill nativa 50_meta_analyze (SA8). Per BUILD/lancio → /pm-meta-build o Ads Manager.
argument-hint: [quick|deep] [finestra: last_14d|last_30d|date range]
---

# /pm-meta-analyze — Meta Ads Analyze (SA8)

Esegui la skill nativa **`directives/skills/50_meta_analyze/SKILL.md`** (SA8, indipendente dalla pipeline).

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/50_meta_analyze/SKILL.md`.
2. **READ-ONLY HARD RULE:** non chiamare MAI nessuno dei 18 write tool Meta (`ads_create_*`, `ads_update_*`, `ads_activate_*`, `ads_delete_*`, pixel/catalog write). Su richiesta di modifica → consiglia e rimanda a `/pm-meta-build` o Ads Manager. Continua l'analisi.
3. Risolvi i tool Meta per **suffisso** (`…ads_*`), mai hardcodare il prefix (qui appare come `mcp__claude_ai_Meta_Ads_MCP__ads_*`, ma resta install-specific). Se i tool sono deferred → caricali via ToolSearch (State B). Se assente il connector → istruzioni setup `mcp.facebook.com/ads` (State D).
4. Prima di ogni MCP call leggi `references/meta-ads-mcp-operator-guide.md`. Per deep: anche `references/diagnostic-frameworks.md` (prima dello staging) e `references/investigator-briefs.md` (prima del fan-out).
5. **Quick check:** ~10-12 pull, file unico. **Deep diagnosis:** 🚦 consent gate obbligatorio prima di spawnare agent; 5 investigator paralleli su slice isolate + referee; diagnosi ranked con evidence-for/against, confidence, singola azione settimanale.
6. Output: `output/reports/{YYYY-MM-DD}_meta_analysis/` — `quick-check-<stamp>.md` oppure `deep-diagnosis-<stamp>/report.md` (+ `.html`).
7. Copy member-facing in italiano → passa per `/pm-de-ai` (49_anti_ai_slop) + `context/brand/anti_ai_writing_style.md`.
