---
description: Meta Ads build — costruisce/lancia campagne complete (campaign+ad set+creative+ad) e fa OGNI write su campagne esistenti (pause, budget, targeting, audience, customer list, attivazione) via Meta Ads MCP in Claude Code. Tutto PAUSED, cerimonie di conferma per budget/attivazione. Skill nativa 51_meta_build (SA8). Per sola diagnosi → /pm-meta-analyze.
argument-hint: [build | pause | budget | targeting | activate | audience]
---

# /pm-meta-build — Meta Ads Build (SA8 / post-SA6)

Esegui la skill nativa **`directives/skills/51_meta_build/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui integralmente `directives/skills/51_meta_build/SKILL.md`. Questa è l'**unica** skill che fa write sull'ad account Meta.
2. **HARD RULE — tutto creato PAUSED.** Nessuna scorciatoia. L'attivazione è una cerimonia separata: un sì esplicito per livello, ordine ad → ad set → campaign (l'ultimo sì = spend switch). Sopra 500/giorno → il membro digita il totale per confermare.
3. **Budget:** importo in valuta account + centesimi computati, entrambi confermati prima di ogni create con budget. Sotto il minimo account → blocca e ri-chiedi.
4. **Tiered tool loading:** Tier 1 (`+ads_get`) al preflight; Tier 2 (`+ads_create`, `ads_update_entity`, `ads_update_custom_audience_users`) SOLO dopo approvazione piano (Gate 1); Tier 3 (`ads_activate_entity`) SOLO all'inizio della cerimonia di attivazione. Risolvi per suffisso, mai hardcodare il prefix.
5. **Stop = pause.** Se il membro esita dopo l'attivazione → metti in pausa la campaign prima, poi discuti.
6. **Gate obbligatori:** special ad categories (ogni run), DSA beneficiary/payor (se geo include EU-27), fine print irreversibilità (dentro il piano, prima del primo create). Audience delete = cerimonia più stretta (typed name).
7. **Creative/copy:** image_hash/video_id/object_story_id dall'account (no upload via MCP). Copy VERBATIM dai deck `06_Ad_Copy/` (o `intermediate/sa7_copy_deck.md`); nessun deck → offri `/pm-meta-copy`.
8. Output: `output/{brand}_{campaign}_{date}/13_Meta_Campaigns/<run>/` (campaign dir) o `output/reports/{data}_meta_campaigns/<run>/` (standalone) — `plan.md` + `build-manifest.json` (machine) + `manifest.md` (member). Mai PII customer nei file.
9. Post-lancio → check a ~7 giorni con `/pm-meta-analyze`.
