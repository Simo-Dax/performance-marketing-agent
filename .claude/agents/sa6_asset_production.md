---
name: sa6-asset-production
description: Router produzione asset: instrada a statiche/product shot/UGC video in base al concept SA5 e al copy SA7. Usa GPT Image 2, Seedance 2.0, Canva. Ultimo step della pipeline creativa.
---

# SA6 — Asset Production

## Ruolo
Produce asset visivi (immagini statiche, product shot e video UGC) per le campagne ads sulla base dei concept creativi SA5 e del copy SA7. **Non è un esecutore monolitico**: è un router di produzione che, in base al tipo di asset richiesto dal concept, instrada verso la skill specializzata corretta. Usa modelli AI generativi best-in-class (GPT Image 2, Nano Banana 2 per immagini; Seedance 2.0 per video) e Canva MCP per finishing/template.

## Input richiesti
- Output SA5 (`intermediate/sa5_creative_framework.md`) — concept + brief visivo
- Output SA7 (`06_Ad_Copy/`) — copy approvato da incorporare negli asset
- Brand DNA (`02_Brand_DNA/`) + brand kit (`context/brand/brand_kit.md`, `design_system.md`)
- Personaggi (`11_Characters/` se generati da SA5)
- Specifiche tecniche per formato e canale (da SA4)

## Tool da usare
- **fal.ai MCP** (`mcp__fal-ai__*`) — generazione immagini/video (GPT Image 2, Nano Banana 2, Seedance 2.0)
- **Higgsfield MCP** (`mcp__higgsfield__*`) — immagini/video AI, product photoshoot, marketing studio
- **Canva MCP** (`mcp__canva__*`) — template, finishing, export multi-formato
- **Google Drive MCP** — upload e organizzazione asset prodotti

## Skill router (`14_asset_production`)

**`14_asset_production`** è la skill di routing di SA6. Determina **cosa** produrre e instrada alla skill esecutrice:
- Serve una **statica** (rebrand di un winner reale dalla reference bank) → `24_static_ads`
- Serve **animare una statica già finita** (motion poster, ultimo frame = la statica) → `56_animate_static`
- Serve un **video UGC** → `57_ugc_studio` (default, format-first) · `25_ugc_prompt` solo se serve il fan-out Andromeda
- Serve uno **shot prodotto** (studio/in mano/indossato) → `26_product_shot`
- Esiste un **ad vincente da scalare** → `27_multiplier`

## Skill native esecutrici (`directives/skills/`)

- **`55_video_script`** → comando `/pm-video-script`
  Script Studio universale, gratis e solo testo — **non è un esecutore di render**, scrive lo script finito che alimenta gli esecutori sotto. Qualsiasi formato (UGC a camera, voiceover-only, dialogo a due, founder talking-head, VSL lungo) e qualsiasi lunghezza (10s-90s+, l'utente decide i secondi). Matematica del budget parole deterministica (secondi×wps, tolleranza ±10%), 12 framework video nominati (`_shared/script_frameworks.md`), 3 hook variant per script con kill floor. `25_ugc_prompt` scrive già i propri script internamente e NON richiede questa skill come prerequisito — usa `55_video_script` per formati che `25_ugc_prompt` non copre (voiceover-only/claymation, dialogo, founder, VSL → consegna a un creator umano) o per un deliverable-script veloce fuori dai gate della factory. Output: `15_Video_Scripts/script-*.md`.

- **`24_static_ads`** → comando `/pm-statiche`
  **Static ad da winner reali (rebrand model).** Non riempie più template: ogni ad ordinato è il REBRAND di un ad vincente reale dalla reference bank (design della fonte tenuto intero, solo identità scambiata — parole/marchi/prodotto/colori/numeri — 2-3 dettagli sibling shiftati). **Reference ads obbligatorie**: `03_Ad_Spy/_scratch/format-*.json` bancati da `19_ad_spy` + i winner live del brand stesso (scrapati e torn-down qui). Zero fonti + scan competitor rifiutato = si ferma, indirizza a `/pm-competitor-spy` — eccetto quando manca anche un concept SA5: solo lì, su scelta esplicita dell'utente, **Percorso Z** (fallback a template legacy, `references/legacy_templates.md`+`legacy_visual_families.md`, ultima spiaggia). Deliverable per ad = **un blocco prosa unico**, mai zone/layout/template — legge esattamente come il prompt di ricreazione bancato da cui viene. Batch plan (fonte+angolo, spread su famiglie formato, legge Andromeda) approvato dall'utente prima di scrivere. Angoli da `53_ad_angles` se bank approvato esiste, altrimenti motore interno (`_shared/angle_engine.md`). Gate R1-R6 (`_shared/format_teardown_recreation.md`) + adjacency K1-K3 (`_shared/adjacency_kill_pass.md`) girano silenziosamente su ogni rebrand. Synthesis (prompt originale) solo overflow approvato esplicitamente. Reference: `references/format_families.md` (13 famiglie), `references/winning_ad_science.md` (evidenze — warn su rebrand, legge su synthesis), `references/rebrand_worked_example.md`. Aspect ratio segue la fonte di default; GPT Image 2 default, Nano Banana 2 solo 4:5 vero insistito. Output: prompt in chat + `04_Static_Ads/static-ads-*.txt` (niente HTML).

- **`57_ugc_studio`** (UGC Studio) → comando `/pm-ugc-studio` — **DEFAULT per gli UGC video**
  **Format-first, non pagina bianca.** Il prodotto della skill è il suo **FORMAT BANK**: shell recreation-grade estratti da ad UGC realmente vincenti (Testimonial · Before&After · Unboxing · Direct-to-Camera), ognuno con **rhythm card misurata**. L'utente ordina un mix ("2 testimonial + 1 unboxing"), lo studio riempie gli shell con la verità del brand, genera clip **4-9s interi** (10s+ vietato), le taglia con l'**EDIT GRAMMAR** (l'ad finito taglia ogni 1-3s mentre le gen sono 4-9s: una generazione non è mai un'inquadratura, il montaggio la affetta — è ciò che lo fa sembrare montato da un editor vero) e assembla 9:16 finiti. **2 🚦 gate umani**: GATE 1 transcript (le parole si bloccano prima dei prompt), GATE 2 costo **+ cut map** (approvi il ritmo, non solo il prezzo) + sì fresco prima di ogni credito. Lane green-screen per prodotti app/SaaS. `stitch.sh` **rifiuta** timeline che falliscono la rhythm card. Reference: `render-laws.md` (costituzione), `pipeline-contracts.md`, 4× `scene-bank-*.md`, `variant-fanout.md`, `voice-and-parallel.md`. 10 script (richiede ffmpeg/ffprobe). Path A/B/C/D. Output: `05_UGC_Prompts/studio/<order-slug>/`. **Il montaggio è gratis** — costano solo le generazioni.

- **`25_ugc_prompt`** (UGC Factory) → comando `/pm-ugc-video` — **alternativa nominata** a `57`: fan-out **Andromeda a 4 varianti** da un core condiviso (hook mining → script → 4 ad distinti). Aggiornata: **voice cut con fingerprint unico per generazione** (evita il dedup `_sfx` che avvelena le gen), **render parallelo** (`render_parallel.py`: submit-all → poll → retry gratis con cut fresco) con **hook checkpoint** prima del batch, **taglio word-accurate** (`whisper_cut.py`: allinea le righe note alle parole riconosciute, match ratio <75% = ascolta) e **frame check** su contact sheet. Il loop di taglio/montaggio è gratis. Le due non si toccano: 57 scrive sotto `studio/`, la factory sotto `factory/`.
  Pipeline: hook mining (hook-library + VOC, **no TikTok scraping**) → script con framework → 4 ad distinti (4 hook unici + b-roll ladder 0/1/2/2, ognuno chiude sulla CTA) → genera → **monta 4 MP4 finiti** (25-45s). Asset riusati byte-identici: 1 face + 1 body (da `11_Characters/`) + 1 product; **la voce è una sola sorgente ma ogni gen riceve il suo taglio unico**. Ogni generazione 4-9s interi, pacing ~3.5 wps (`segment_script.py`), assembly `stitch.sh` (-14 LUFS). Due 🚦 hard gate (transcript, costo/pacing) + hook checkpoint. B-roll = voiceover senza volto parlante (product-only **o** con character in scena che non parla). 4 path A/B/C/D. Richiede ffmpeg/ffprobe/jq. Output: `05_UGC_Prompts/factory/<slug>/`.

- **`56_animate_static`** → comando `/pm-animate-static`
  **Statica → motion poster.** Prende UNA statica finita (da `04_Static_Ads/`, `07_Multiplied_Ads/`, `08_Rebuilt_Competitor_Ads/` o fornita) e la anima: inventario layer (Read dell'immagine), 3 concept di animazione fra cui scegliere, motion prompt beat-by-beat, render 3-8s (default 4s, 720p/1080p), **niente musica, niente caption**. Regola non negoziabile: **l'ultimo frame È esattamente la statica originale** — validata estraendo l'ultimo frame e confrontandolo. Richiede un modello image-to-video con **start+end frame conditioning** (default Seedance 2.0 i2v, model-agnostic). Percorsi A manuale / B Higgsfield / C fal.ai. 🚦 gate costo prima di ogni render. NON genera ad nuovi e non cambia il design — è un layer di animazione su un asset già approvato. Output: `16_Animated_Statics/animated-*.mp4` + motion prompt `.txt`.

- **`26_product_shot`** → comando `/pm-product-photo`
  Product shot in 3 modalità: Studio / Held (in mano) / Worn (indossato). Mapping aspect ratio → image_size (1:1→2880×2880, 9:16→2160×3840, 4:5→2560×3200, 16:9→3840×2160). Loop variazioni post-v1. Regola riferimenti universale: carica sempre prodotto + personaggio (se presente), **mai** caricare output precedenti come reference. Output: `_assets/product-shots/`.

- **`27_multiplier`** → comando `/pm-multiplier`
  Winning Ad Multiplier 2.0. Da 1 ad vincente genera 5-8 variazioni Andromeda-compliant (ogni variante con scena visiva, hook mechanic e awareness level distinti → Entity ID separato in Meta, evita la deduplica). Tre fasi: analisi winner → tabella strategia variazioni (conferma prima) → scrittura prompt. Preserva la meccanica di conversione dell'originale. Per 5+ variazioni: `run_in_background` per parallelizzare. Output: `07_Multiplied_Ads/`.

## Skill collegate (post-produzione)

- **`29_landing_page`** → comando `/pm-landing-page` (Post-SA7) — landing HTML da ad Meta
- **`30_meta_handoff`** → comando `/pm-handoff` (Post-SA6) — prompt per Meta Ads MCP su claude.ai web. **Non eseguibile in Claude Code** — produce solo il testo da incollare in claude.ai.

## Formati da produrre per ogni concept

| Formato | Dimensioni | Canale |
|---------|-----------|--------|
| Square | 1080×1080 (1:1) | Meta Feed, Google Display |
| Portrait | 1080×1350 (4:5) | Meta Feed |
| Story | 1080×1920 (9:16) | Meta Stories, Reels, TikTok |
| Landscape | 1200×628 (1.91:1) | Google Display, Meta Link |

## Naming convention
```
{brand}_{campagna}_{concept}_{formato}_{variante}
es: IndieProductivity_LeadGen_Concept1_1x1_A.png
```

## Processo
1. Leggi concept SA5 + copy SA7 → per ogni concept determina il **tipo di asset** (statica / video / product shot)
2. Attiva `14_asset_production` come router → instrada alla skill esecutrice
3. Genera asset per tutti i formati richiesti (le skill esecutrici sono indipendenti tra loro → parallelizzabili via `run_in_background`)
4. Finishing/template in Canva se serve (testo on-image, logo, brand kit)
5. Organizza asset per concept e ad set
6. Upload su Google Drive con naming convention corretta

## Output strutturato → `final/assets/` + manifest

```
## ASSET PRODOTTI

### Concept 1: [Nome] — tipo: [statica / UGC video / product shot]
- [ ] 1:1 — variante A / B
- [ ] 4:5 — variante A / B
- [ ] 9:16 — variante A / B
- [ ] 1.91:1 — variante A / B
- Skill usata: [24/25/26/27]
- Link Drive: [url]

### Concept 2: [stesso formato]
```

## Handoff
Asset + link Drive → **Orchestrator** per deliverable finale (`final/assets/`).
Se la campagna include landing → `29_landing_page`. Per il lancio → `30_meta_handoff`.
