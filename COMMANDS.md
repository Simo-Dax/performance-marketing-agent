# COMMANDS — Riferimento completo `/pm-*`

Tutti i comandi del Performance Marketing Team. Vivono in `.claude/commands/`. Ognuno attiva una skill nativa in `directives/skills/`.

---

## Setup & sistema
| Comando | Cosa fa | Attiva |
|---------|---------|--------|
| `/pm-setup` | Master setup: verifica struttura, tool, MCP, API key. Idempotente. | — |
| `/pm-setup-apify` | Configura Apify API key (spy + UGC scraper) | — |
| `/pm-setup-fal-ai` | Configura Fal AI key (immagini/video) | — |
| `/pm-feedback "..."` | Registra feedback e lo applica come regola (orchestrator/agente/skill) + log + memory | `self_improvement.md` |

## Pre-pipeline & Research (SA1, SA2)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-brand-kit` | Brand DNA: colori live (Playwright) + voce brand → HTML | 21 / pre-pipeline |
| `/pm-dati-qualitativi` | VOC research: linguaggio verbatim clienti → HTML | 18 / SA2 |
| `/pm-competitor-spy` | Ad spy Meta: swipe file static ads ranked (Apify) | 19 / SA1 |
| `/pm-ugc-analysis` | UGC TikTok: 25 transcript virali (Apify) | 20 / SA1 |

## Strategia (33 → SA3 → SA4)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-insight` | Insight synthesis: 7 dimensioni + 🚦GATE 1 umano | 33 / ponte SA2→SA4 |
| `/pm-brand-strategy` | VP Bain + USP + ToV + offer design + trigger + 🚦GATE 2 | 32 / SA4 Fase 1 |
| `/pm-editorial` | Piano editoriale + content calendar (5 awareness) | 34 / post-SA4 |

> SA3 (financial) e SA4 Fase 2 (campaign architecture) girano dentro la pipeline, non hanno comando dedicato — partono con "Lancia pipeline…".

## Creative (SA5)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-buyer-persona` | 1-10 personaggi brand (headshot + full body 3:4) | 22 / SA5 |
| `/pm-competitor-rebuild` | Reverse-engineer ad competitor → prompt proprio brand | 23 / SA5 |

## Produzione (SA6)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-statiche` | 40 static ad prompts (GPT Image 2 / Nano Banana 2) | 24 / SA6 |
| `/pm-ugc-video` | 6 prompt video UGC → Seedance 2.0 | 25 / SA6 |
| `/pm-product-photo` | Product shot Studio/Held/Worn | 26 / SA6 |
| `/pm-multiplier` | 5-8 variazioni Andromeda-compliant da winner | 27 / SA6 |

## Copy (SA7)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-meta-copy` | 5 headline + 5 description + 2 primary text | 28 / SA7 |
| `/pm-google-ads-copy` | RSA: 15 headline + 4 description | 12 / SA7 |

## Post-produzione & Lancio
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-landing-page` | Landing HTML da ad Meta (VOC injection + anti-AI) | 29 / post-SA7 |
| `/pm-meta-build` | Lancio/gestione campagne Meta live (vedi SA8 sotto) | 51 / post-SA6 |
| `/pm-handoff` | ⚠️ DEPRECATO — prompt handoff Meta MCP claude.ai web (sostituito da 50/51) | 30 / post-SA6 |

## Analytics & Reporting (SA8)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-report` | Report performance (weekly/monthly/quarterly/annual), KPI business-model-aware | 31 / SA8 |
| `/pm-search-term` | Google Ads: search term + keyword + QS analyzer (ricorrente) | 35 / SA8 |
| `/pm-google-audit` | Google Ads: audit completo da zero (12 aree + roadmap ICE) | 36 / SA8 |
| `/pm-google-optimisations` | Google Ads: checklist ricorrente ottimizzazioni | 37 / SA8 |
| `/pm-meta-analyze` | Meta Ads: diagnosi **read-only live** (quick check o deep diagnosis con panel investigator + referee) | 50 / SA8 |
| `/pm-meta-build` | Meta Ads: **build/write** campagne live (tutto PAUSED, cerimonie budget/attivazione) + ogni modifica a esistenti | 51 / SA8 |

---

## Shortcut mentale (sequenza tipica nuova campagna)
```
/pm-brand-kit → /pm-dati-qualitativi → /pm-competitor-spy → /pm-ugc-analysis
→ /pm-insight (GATE 1) → [SA3 financial] → /pm-brand-strategy (GATE 2)
→ [SA4 campaign architecture] → /pm-buyer-persona → /pm-statiche /pm-ugc-video
→ /pm-meta-copy /pm-google-ads-copy → /pm-landing-page → /pm-meta-build (lancio) → /pm-meta-analyze (check ~7gg)
Reporting: /pm-report · /pm-search-term · /pm-google-audit · /pm-google-optimisations
```
