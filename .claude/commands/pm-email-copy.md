---
description: Copy email/newsletter — 5 subject A/B + 2 preview + body (hook→valore→proof→CTA) + 3 CTA microcopy, in tone of voice brand, anti-AI, per segmento RFM e obiettivo. Draft via Gmail MCP. Skill 46 (SA9).
argument-hint: [tipo email: welcome|abandoned-cart|win-back|newsletter|...] [segmento]
---

# /pm-email-copy — Email Creation (SA9)

Esegui la skill **`directives/skills/46_email_creation/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/46_email_creation/SKILL.md`.
2. Auto-discovery input: obiettivo/flow (da `sa9_email_strategy.md` o `$ARGUMENTS`), segmento (`sa9_rfm_segments.md`), `tone_of_voice.md` + `anti_ai_writing_style.md`, pain/desideri (`insight.md`).
3. Produci per ogni email: 5 subject A/B (max ~45char) + 2 preview text + body (hook→valore→proof→CTA singola) + 3 CTA microcopy.
4. Applica anti-AI rigoroso (no "In un mondo dove…", no em-dash a raffica, una idea per email, voce di persona del brand).
5. Output: blocco/file in `12_Email/{flow}_{nome}.md` con note invio (personalizzazione, esclusioni). Opzionale: draft reale via `mcp__claude_ai_Gmail__create_draft`.
6. QA: passa da `03_editing_selfcheck` (voice-editor brand) prima della consegna.
7. **Regola:** una email = un segmento + un obiettivo + una CTA. Se scrivi per "tutti" con 3 CTA → torna a `/pm-rfm` / `/pm-email-strategy`.
