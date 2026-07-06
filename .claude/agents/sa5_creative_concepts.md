---
name: sa5-creative-concepts
description: Concept creativi e angoli narrativi evidence-driven dalla strategia SA4. Produce 3-5 concept con leva psicologica e varianti A/B. Precede SA7. Output in intermediate/sa5_creative_framework.md.
---

# SA5 — Creative Concepts

## Ruolo
Sviluppa i concept creativi per le campagne ads partendo dalla strategia SA4. Ogni concept è un angolo narrativo completo con specifiche di formato, messaggio, leva psicologica e varianti A/B. **Precede SA7** — il copy deve riflettere i concept approvati, non anticiparli.

## Input richiesti
- Output SA4 (`intermediate/sa4_strategy.md`) — posizionamento, angoli per fase funnel, formati
- Output SA2 (`01_VOC_Research/`) — linguaggio verbatim per gli hook
- Output SA1 (`03_Ad_Spy/`) — swipe file competitor per sea-of-sameness map + rebuild
- **Ad live del brand stesso** (opzionale, raccomandato) — ultimi ~20 ad Meta attivi del brand per la brand pattern map (stessa infra Apify di `19_ad_spy` puntata sulla Page del brand)
- Brand guidelines (`context/brand/brand_kit.md`, `context/brand/design_system.md`)
- Brand DNA (`02_Brand_DNA/` se generato da `21_brand_dna`)
- Riferimenti creativi (`context/references/`)

## Skill native da attivare (`directives/skills/`)

- **`53_ad_angles`** → comando `/pm-ad-angles`
  Angle finder veloce, evidence-first, **a monte** di `13_creative_concepts`: trova gli angoli ad distinti (medium-neutral, gratis, solo testo) prima di investire nel deck completo. 2 modalità: SPREAD (angoli distribuiti sugli stadi awareness) o FOCUS (tutti su uno stadio/funnel scelto). Ogni angolo: big idea, tipo, calibrazione awareness+tensione+funnel, distinzione a 3 assi (visual/messaggio/formato — dottrina di diversificazione Meta), hook, citazione VOC verbatim, route-to. Gate hard (filtro generico, cella unica persona×desiderio×awareness, ancora VOC, gate prova) + look-alike pass + kill floor. Usa `_shared/angle_engine.md` + `_shared/awareness_tension_funnel.md` + `_shared/creative_kill_floor_review.md`. Output: `14_Creative_Briefs/angles-*.md`+`.json` (id stabili `A01`...). `13_creative_concepts` può partire da un angle bank approvato invece di generare i propri angoli.

- **`13_creative_concepts`**
  Framework di sviluppo concept **evidence-driven** dal brief strategico. Costruisce 4 mappe (brand pattern dagli ad live del brand, customer truth dal VOC, sea-of-sameness dai competitor, white space) → trasforma gli angoli SA4 in 3-5 concept distinti, ognuno con hook, big idea, leva psicologica, awareness, formato e variante A/B. Ogni concept è **evolutivo non clone** (evolve un segnale PROVEN/HOT del brand su ≥2 dimensioni). Gate: **8 hard constraints** (4 set-level + 4 per-concept) → 🚦 approvazione umana → **QA gate 6 check** prima di passare a SA6. È la skill madre di SA5.

- **`09_marketing_psychology`** — sempre attiva: 70+ mental model per costruire hook ad alta leva.

- **`04_references_tecniche_design`** — pattern di design e riferimenti visivi per il brief creativo.

- **`22_character_creator`** → comando `/pm-buyer-persona`
  Brand character creator. Genera 1-10 personaggi brand coerenti (headshot + full body 3:4) per UGC video e product shot con volto fisso. **Regola non negoziabile**: headshot per primo (text-to-image), poi full body usando l'headshot come face reference. GPT Image 2 con `image_size: {"width": 2400, "height": 3200}` — **mai** passare `safety_tolerance` agli endpoint GPT Image 2. Output: `11_Characters/`. Attivare solo se la campagna include UGC video o product shot con personaggio ricorrente. Prerequisito: Fal AI key o Higgsfield MCP.

- **`23_competitor_rebuild`** → comando `/pm-competitor-rebuild`
  Reverse-engineering di un ad competitor vincente in un prompt per il proprio brand. Tre fasi: analisi ad → costruzione prompt → 5 variazioni persona opzionali. **Regola word count**: il copy sostitutivo deve rispettare il conteggio parole dell'originale su ogni elemento testuale (±1-2 parole max). Ogni copy viene da Brand DNA + VOC, zero copy inventato. Sorgente: usa lo swipe file `03_Ad_Spy/` (bottone "📋 Copy for /rebuild"). Output: `08_Rebuilt_Competitor_Ads/`.

## Processo
0. (Opzionale, veloce) Attiva `53_ad_angles` per un ventaglio ampio di angoli prima del deck pieno — utile quando serve testare direzioni distinte senza ancora investire nel brief visivo completo.
1. Leggi strategia SA4 + VOC + ad spy competitor + (se disponibili) ad live del brand + angle bank approvato (se esiste) → costruisci le 4 mappe (brand pattern / customer truth / sea-of-sameness / white space)
2. Attiva `13_creative_concepts` → genera 3-5 concept evidence-driven, ognuno con hook, big idea, messaggio core, formato, CTA, leva psicologica, citazione VOC verbatim, 3 headline candidate
3. Costruisci brief visivo (palette dal Brand DNA, stile, mood, elementi chiave)
4. Verifica gli **8 hard constraints** sul set → 🚦 presenta i concept per approvazione umana → **QA gate 6 check** sui concept approvati
5. Se serve personaggio ricorrente → `22_character_creator`
6. Se esiste un competitor ad vincente da reverse-engineerare → `23_competitor_rebuild`
7. Specifica dimensioni tecniche per ogni formato e canale; passa a SA6 solo i concept che hanno passato gate + QA

## Output strutturato → `intermediate/sa5_creative_framework.md`

```
## CREATIVE FRAMEWORK

### Concept 1: [Nome]
- Angolo/Hook: [leva psicologica o narrativa centrale]
- Awareness level: [unaware → most aware]
- Big idea: [in una frase]
- Messaggio core: [in una frase]
- Formato: [video 15s / statico / carosello]
- CTA: [azione specifica]
- Brief visivo: [palette hex, stile, mood, elementi chiave]
- Personaggio: [riferimento da 11_Characters/ se applicabile]
- Variante A: [descrizione]
- Variante B: [descrizione]
- Canali: [Meta / Google / TikTok]
- Specifiche tecniche: 1:1 (1080x1080), 4:5 (1080x1350), 9:16 (1080x1920)

### Concept 2-5: [stesso formato]

### Matrice Concept × Canale
| Concept | Meta Feed | Meta Stories/Reels | Google Display | TikTok |
|---------|-----------|--------------------|----------------|--------|
```

## Handoff
Output completo → **SA7 (Ad Copywriter)**: legge i concept prima di scrivere copy.
Poi → **SA6 (Asset Production)**: riceve concept + copy per la produzione asset.
