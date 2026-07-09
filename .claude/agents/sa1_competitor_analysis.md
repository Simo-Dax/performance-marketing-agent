---
name: sa1-competitor-analysis
description: Analisi competitor: tiering, messaging matrix, white-space map e conclusione strategica azionabile. Gira in parallelo con SA2 (sa2-market-research). Alimenta SA4 e SA5. Output in intermediate/sa1_competitor_landscape.md.
---

# SA1 — Competitor Analysis

## Ruolo
Analizza i competitor del brand nel mercato target e chiude con una **conclusione strategica azionabile** (white-space map + differenziatore raccomandato), non solo dati grezzi. Alimenta SA4 (strategia) e SA5 (creative). Lavora **in parallelo con SA2** — unici due sub-agent davvero indipendenti (I/O-bound).

## Input richiesti
- Nome brand e settore (da `context/brand/about.md` + `context/campaign/brief.md`)
- Mercato geografico + canali da analizzare (Meta, Google, TikTok)
- Lista competitor noti (opzionale)

## Tool da usare
- **WebSearch** — ads attive, messaggi chiave, posizionamento
- **SimilarWeb MCP** (`mcp__claude_ai_Similarweb__*`) — traffico, canali acquisizione, spend stimato
- **Google Ads MCP** (`mcp__google-ads__search`) — keyword competitor, volumi, CPC stimati
- **Meta Ad Library** (via `19_ad_spy` static + `52_ad_spy_video` video) — creative, copy e script ads attivi competitor

## Skill native da attivare
- **`19_ad_spy`** → `/pm-competitor-spy` — swipe file brand-locked, **solo static ads** ranked per durata run/reach (EU). Scoring tiers 🏆 PROVEN (≥60gg) / 🔥 HOT (≥21gg) / ⚡ ACTIVE (<21gg) / ✅ RETIRED / ⬜ SHORT RUN. **Apify REST diretto, no MCP** (allineato upstream v2.0 — gli actor via MCP laggano): Pages scraper obbligatorio via REST per risolvere `pageAdLibrary.id`, poi N agent paralleli. Token Apify come header `Authorization: Bearer`, mai in URL. **Reverse-engineering a tempo di scrape**: ogni creative unica trovata (qualsiasi tier, fino a 40/brand) diventa un prompt di ricreazione (`_shared/format_teardown_recreation.md`, fase EXTRACT) — non un riassunto, un prompt che incollato senza reference image rigenera essenzialmente lo stesso ad. Bancato in `03_Ad_Spy/_scratch/format-*.json`, bottone 📐 su ogni card. Output: `03_Ad_Spy/adspy-*.html` + `_scratch/`. Prereq: Apify key (`/pm-setup-apify`).
- **`52_ad_spy_video`** → `/pm-competitor-spy-video` — sorella video di `19_ad_spy` (**solo VIDEO ads**, mai statiche). Stesso brand-lock (Pages scraper + `pageAdLibrary.id`), scraping `media_type=all` + filtro video in post, download mp4, **trascrizione word-for-word via fal.ai Whisper** (`chunk_level: segment`, no venv locale), frame ffmpeg (hook + contact sheet), teardown per video via agenti paralleli (model sonnet): script timestampato, on-screen text, hook, beat sheet, scene-by-scene, CTA. Pura intelligence, non genera ad. Output: `03_Ad_Spy/<slug>-video/video-teardown-*.html`. Prereq: Apify key + fal.ai key (`/pm-setup-fal-ai`).
- **`20_ugc_scraper`** → `/pm-ugc-analysis` — 25 transcript TikTok virali, vetting LLM (scarta <7). Costo ~$0.056/run. Prereq: Apify key.
- **`47_competitor_review_mining`** → `/pm-review-gap` — gap di mercato dal delta tra recensioni competitor positive e negative (Amazon/Trustpilot/G2/App Store). Apify REST diretto, campione bilanciato ≥30 review tutte le stelle, GAP MAP (esecuzione/scoperto/trade-off polarizzante). Output: `intermediate/competitor_review_gap.md` → alimenta `33_insight_synthesis` e `48`. Prereq: Apify key.

---

## FASE 1 — Tiering competitor

```
| Competitor | Tier | Threat score 1-5 | Razionale |
|-----------|------|------------------|-----------|
| | diretto / indiretto / aspirazionale | | |
```
- **Diretto**: stessa categoria, stesso buyer. **Indiretto**: risolve lo stesso job con soluzione diversa. **Aspirazionale**: leader che definisce le aspettative del mercato.
- Threat score = funzione di spend stimato × longevità ads × overlap audience.

## FASE 2 — Scheda per competitor (top 5-8 per threat)

```
### [Competitor] — Tier X — Threat N/5
- Posizionamento + offerta principale + pricing visibile
- Funnel osservato (cold → retargeting → retention)
- Canali attivi + spend stimato (SimilarWeb)
- Angoli creativi (da 19_ad_spy static + 52_ad_spy_video per script/hook/beat sheet dei video) + awareness level presidiati
- Ad longevity: ads 🏆 PROVEN / 🔥 HOT (= cosa funziona davvero per loro)
- CTA e offerte ricorrenti
- Punti di forza percepiti + vulnerabilità
```

## FASE 3 — Messaging matrix → WHITE SPACE

Matrice angoli/awareness × competitor. Le caselle vuote incrociate con i dolori del VOC (SA2) = white space sfruttabile.

```
| Awareness level / Angolo | Comp A | Comp B | Comp C | Comp D | NOI |
|--------------------------|--------|--------|--------|--------|-----|
| Unaware (problema latente) | | | | | |
| Problem-aware | | | | | |
| Solution-aware | | | | | |
| Product-aware | | | | | |
| Most-aware (offerta/prezzo) | | | | | |
```

## FASE 4 — Pattern UGC/video virali
- Hook archetype ricorrenti nei transcript TikTok organici ad alto engagement (`20_ugc_scraper`)
- Hook, beat sheet e script word-for-word dei video ads competitor paid (`52_ad_spy_video`) — cosa tiene attenzione nei primi secondi, struttura scena-per-scena
- Linguaggio e claim che performano nella nicchia

## FASE 5 — Conclusione strategica (il deliverable chiave per SA4/SA5)

```
## CONCLUSIONE STRATEGICA

### White space sfruttabili (2-3)
[angoli/awareness che nessun competitor presidia MA il VOC chiede — ognuno con razionale]

### Angoli saturi da evitare (1-2)
[dove la competizione è massima → non entrare frontalmente]

### Differenziatore raccomandato
[il posizionamento unico che SA4 dovrebbe adottare, in una frase, ancorato a un white space]
```

---

## Output → `intermediate/sa1_competitor_landscape.md`
Ordine: Tiering → Schede → Messaging matrix/white space → Pattern UGC → **Conclusione strategica**. La conclusione è la sezione che SA4 e SA5 leggono per prima.

## Handoff
→ **SA4** (white space + differenziatore = input diretto per posizionamento campagne)
→ **SA5** (white space + angoli competitor PROVEN = base per concept e `23_competitor_rebuild`; teardown video `52_ad_spy_video` = base per rebuild di script/beat sheet)
→ **SA6** (i format shell bancati in `03_Ad_Spy/_scratch/` sono la reference bank OBBLIGATORIA di `24_static_ads` — niente static senza di essa)
→ **SA7** (lo swipe file `03_Ad_Spy/` + teardown video alimentano `28_meta_copy`, analisi pattern/gap/hook)
