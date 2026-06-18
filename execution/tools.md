# Tools & MCP — mappati ai ruoli degli agenti

Riferimento di quali tool/MCP/skill usa ogni sub-agent. Per il routing skill→agente vedi `directives/skill_orchestrator.md`.

---

## MCP per agente

| Agente | MCP / Tool | Uso |
|--------|-----------|-----|
| **SA1** Competitor | Apify (`mcp__apify`), SimilarWeb (`mcp__claude_ai_Similarweb`), Google Ads (`mcp__google-ads`), WebSearch | Ad spy Meta, UGC TikTok, traffico/spend competitor, keyword |
| **SA2** Market | Lenny's Data (`mcp__claude_ai_Lenny_s_Data_MCP`), WebSearch, Playwright | VOC, benchmark, ricerca mercato, JTBD |
| **SA3** Financial | — (usa `execution/calculators/`) | MER/break-even/unit economics (no MCP, calcolo) |
| **SA4** Strategist | Google Ads (targeting), WebSearch | Brand strategy + campaign architecture |
| **SA5** Creative | fal.ai (`mcp__fal-ai`), Higgsfield (`mcp__higgsfield`) | Character creator, rebuild |
| **SA6** Production | fal.ai, Higgsfield, Canva (`mcp__canva`), Google Drive | Statiche (GPT Image 2 / Nano Banana 2), UGC video (Seedance 2.0), product shot, finishing |
| **SA7** Copy | — (usa VOC + Brand DNA + skill) | Meta/Google copy |
| **SA8** Analytics | Google Ads (`mcp__google-ads__search` GAQL), Meta Ads (`mcp.facebook.com/ads`, solo web), Gmail (`mcp__claude_ai_Gmail`) | Report, audit, search-term/QS, ottimizzazioni, delivery email |
| **Orchestrator/Ops** | Slack, Google Calendar, n8n (`mcp__claude_ai_n8n`) | Notifiche, scheduling, automazione |

> **Meta Ads MCP**: funziona solo in claude.ai web (OAuth). In Claude Code usa `30_meta_handoff` (`/pm-handoff`) o export CSV.
> **Higgsfield MCP**: configurato **solo in questo progetto** (`.mcp.json`), non globale. Server in `~/.claude/mcp-servers/higgsfield/`.
> **Google Ads MCP**: MCC `5524890329`, config in `.mcp.json` (developer token + login customer id).

---

## Modelli AI generativi (SA5/SA6)

| Modello | Endpoint | Uso | Nota |
|---------|----------|-----|------|
| GPT Image 2 | `openai/gpt-image-2` / `.../edit` (fal.ai) | Immagini/design/testo, statiche, product shot, character | **Mai** `safety_tolerance` |
| Nano Banana 2 | `fal-ai/nano-banana-2` / `.../edit` | Alternativa economica immagini | accetta `safety_tolerance: "4"` |
| Seedance 2.0 | `bytedance/seedance-2.0/reference-to-video` | UGC video (9:16, 1080p, 15s, audio) | via Higgsfield CLI o fal.ai |
| Higgsfield CLI | `@higgsfield/cli` | generate/product-photoshoot/soul-id | device login al primo uso |

API key: `/pm-setup-fal-ai` (fal.ai), `/pm-setup-apify` (Apify).

> ⭐ **Principio "best model available" (immagini E video):** i modelli sopra sono i **default attuali**, non vincoli. Usa sempre il **migliore disponibile al momento** per qualità e consistenza. Se esce un modello superiore (immagini: nuovi GPT Image / Nano Banana / Flux; video: Veo 3/4, Kling, ecc.) accessibile via Higgsfield MCP o fal.ai, **preferiscilo** — annunciandolo all'utente e adattando i parametri. Verifica i modelli disponibili con `mcp__higgsfield__list_models` o `mcp__fal-ai__search_models`. Le skill 24/25/26/27 sono scritte model-agnostic: cambia solo l'endpoint/parametri, non la struttura del prompt.

---

## Skill Claude Code globali (supporto)

- `marketing-psychology` — 70+ mental model (SA2, SA5, SA7)
- `marketing-ideas` — 139 idee crescita (SA4)
- `copywriting` / `copy-editing` — supporto QA copy (SA7)
- `higgsfield-generate` / `-product-photoshoot` / `-marketplace-cards` / `-soul-id` — generazione (SA6)

---

## Reference / tooling (in `execution/`)

- `calculators/` — 10 calculators finanziari Learnn (SA3)
- `strategy-method/` — metodo Learnn 4 fasi + SOP (SA4)
- `prompts/` — prompt library reference/backup
- `scripts/` — script utilità
- `workflows/` — n8n workflow JSON

> Checklist Google Ads ottimizzazioni: **co-locate** nella folder della skill `directives/skills/37_google_ads_optimisations/` (CSV per tipo campagna), non in execution.
