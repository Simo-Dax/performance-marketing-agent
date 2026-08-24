# COMMANDS — Riferimento completo `/pm-*`

Tutti i comandi del Performance Marketing Team. Vivono in `.claude/commands/`. Ognuno attiva una skill nativa in `directives/skills/`.

---

## Setup & sistema
| Comando | Cosa fa | Attiva |
|---------|---------|--------|
| `/pm-setup` | Master setup: verifica struttura, tool, MCP, API key. Idempotente. | — |
| `/pm-setup-apify` | Configura Apify API key (spy + UGC scraper) | — |
| `/pm-setup-fal-ai` | Configura Fal AI key (immagini/video) | — |
| `/pm-setup-kie` | Configura KIE AI key (render alternativo, REST). Opzionale: mappato in `execution/kie_api_map.md`, non cablato nelle skill | — |
| `/pm-feedback "..."` | Registra feedback e lo applica come regola (orchestrator/agente/skill) + log + memory | `self_improvement.md` |

## Pre-pipeline & Research (SA1, SA2)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-brand-kit` | Brand DNA: colori live (Playwright) + voce brand → HTML | 21 / pre-pipeline |
| `/pm-dati-qualitativi` | VOC research → HTML + Fase 3 opzionale Foundation Pack (avatar/offer brief/6 beliefs) | 18 / SA2 |
| `/pm-competitor-spy` | Ad spy Meta static: swipe file ranked + prompt di ricreazione per ogni creative (Apify) | 19 / SA1 |
| `/pm-competitor-spy-video` | Ad spy Meta video: teardown per video (script/hook/beat sheet, Apify + fal.ai) | 52 / SA1 |
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
| `/pm-ad-angles` | Angle finder evidence-driven (SPREAD/FOCUS), a monte del deck | 53 / SA5 |
| `/pm-buyer-persona` | 1-10 personaggi brand (headshot + full body 3:4) | 22 / SA5 |
| `/pm-competitor-rebuild` | Reverse-engineer un singolo ad competitor → prompt proprio brand (ad-hoc) | 23 / SA5 |

## Produzione (SA6)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-statiche` | Static ad da winner reali: rebrand della reference bank (design tenuto, identità scambiata) | 24 / SA6 |
| `/pm-video-script` | Video script studio universale (qualsiasi formato/lunghezza), solo testo | 55 / SA6 |
| `/pm-animate-static` | Statica finita → motion poster 3-8s (ultimo frame = la statica) | 56 / SA6 |
| `/pm-ugc` | **Porta d'ingresso UGC (default)**: menu 11 formati, instrada sul dubbio da togliere. Non spende | 62 / SA6 |
| `/pm-ugc-problem-solution` | Nomina un dolore, mostralo fallire, poi il prodotto che lo chiude (20-27s) | 62 / SA6 |
| `/pm-ugc-testimonial` | Cliente vero, parole sue, in camera (20-30s). Richiede VOC | 62 / SA6 |
| `/pm-ugc-before-after` | Due stati confrontati sotto condizioni identiche (15-24s). Avviso piattaforma | 62 / SA6 |
| `/pm-ugc-tutorial` | Insegna UN risultato step by step (22-30s) | 62 / SA6 |
| `/pm-ugc-unboxing` | Da sigillato a rivelato, la reazione è il payoff (18-27s) | 62 / SA6 |
| `/pm-ugc-street-interview` | Sconosciuti in pubblico, risposte non copionate (22-30s). Richiede VOC | 62 / SA6 |
| `/pm-ugc-asmr` | Suoni e texture reggono l'ad (15-25s). Render più affidabile del set | 62 / SA6 |
| `/pm-ugc-expert` | Spiega **perché** funziona, non che funziona (22-30s). Richiede VOC | 62 / SA6 |
| `/pm-ugc-pov` | Skit riconoscibile, risata prima del prodotto (15-25s) | 62 / SA6 |
| `/pm-ugc-green-screen` | Creator che reagisce, girato pulito da comporre dopo (20-30s) | 62 / SA6 |
| `/pm-ugc-founder-story` | Il fondatore racconta perché esiste (24-30s). Richiede foto vera | 62 / SA6 |
| `/pm-captions` | Brucia caption stile locked su qualsiasi video; force-align sullo script se c'è | 63 / SA6 |
| `/pm-ugc-studio` | UGC Studio (lane precedente): format bank → ad 9:16, edit grammar | 57 / SA6 |
| `/pm-ugc-blueprint` | Da un video UGC che ti piace: teardown misurato + ricostruzione col tuo prodotto | 58 / SA6 |
| `/pm-ugc-video` | UGC factory (lane precedente): 4 ad MP4 fan-out Andromeda, render parallelo + taglio word-accurate | 25 / SA6 |
| `/pm-pixar-ad` | Ad Pixar 3D voiceover-first, formato progressione "Giorno 1… Giorno 30…" | 59 / SA6 |
| `/pm-talking-object-ad` | Ad dove il cast parla: problema personificato → ingredienti → il prodotto chiede la vendita | 60 / SA6 |
| `/pm-podcast-ad` | Finto podcast a due host (2 volti + 2 voci → 9:16 montato) | 61 / SA6 |
| `/pm-product-photo` | Product shot Studio/Held/Worn | 26 / SA6 |
| `/pm-multiplier` | 5-8 variazioni Andromeda-compliant da winner | 27 / SA6 |

## Copy (SA7)
| Comando | Cosa fa | Skill / Agente |
|---------|---------|----------------|
| `/pm-headlines` | Headline bank dedicata (~20 headline + 8 hook on-image + 6 first-line) | 54 / SA7 |
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
