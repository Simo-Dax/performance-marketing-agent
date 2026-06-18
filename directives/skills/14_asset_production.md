# SA6 — Asset Production Router

**Agente:** SA6 (Asset Production)
**Input:** `intermediate/sa5_creative_framework.md` + `intermediate/sa7_copy_deck.md` + `02_Brand_DNA/` + `11_Characters/`
**Output:** `final/assets/` + manifest produzione
**Ruolo della skill:** **router**, non esecutore. Decide *cosa* produrre e instrada alla skill specializzata.

---

## Perché questa skill esiste

SA6 non genera immagini di tasca propria. La produzione effettiva vive in 4 skill specializzate, ognuna ottimizzata per un tipo di asset e per il modello AI migliore per quel tipo. `14_asset_production` è il livello di **decisione e instradamento**: legge i concept SA5, capisce per ognuno se serve una statica, un video, uno shot prodotto o la moltiplicazione di un winner, e chiama la skill giusta con gli input giusti.

Tenere il routing separato dall'esecuzione evita che SA6 reinventi prompt già perfezionati nelle skill 24-27 e garantisce coerenza modello/formato.

---

## Le 4 skill esecutrici

| Se il concept è… | Skill | Comando | Modello | Output |
|------------------|-------|---------|---------|--------|
| Statica / ad image da zero | `24_static_ads` | `/pm-statiche` | GPT Image 2 / Nano Banana 2 | `04_Static_Ads/` |
| Video UGC (hook + parlato) | `25_ugc_prompt` | `/pm-ugc-video` | Seedance 2.0 | `05_UGC_Prompts/` |
| Shot prodotto (studio/held/worn) | `26_product_shot` | `/pm-product-photo` | GPT Image 2 / Nano Banana 2 | `_assets/product-shots/` |
| Scalare un ad vincente esistente | `27_multiplier` | `/pm-multiplier` | GPT Image 2 / Nano Banana 2 | `07_Multiplied_Ads/` |

---

## Step 0 — Auto-discovery input

Leggi:
- `intermediate/sa5_creative_framework.md` — **obbligatorio**: contiene per ogni concept il campo "Skill di produzione SA6" già compilato da SA5
- `intermediate/sa7_copy_deck.md` — copy approvato da incorporare on-image / nel dialogo
- `02_Brand_DNA/` — palette, font, tono visivo
- `11_Characters/` — personaggi salvati (per UGC video e product shot worn/held)
- `context/brand/brand_kit.md`, `design_system.md`

Se manca SA5 → ferma, richiedi l'esecuzione di SA5.
Se un concept richiede un personaggio ma `11_Characters/` è vuoto → segnala e proponi `22_character_creator` (`/pm-buyer-persona`) prima di procedere.

---

## Step 1 — Decision tree di routing

Per **ogni** concept in `sa5_creative_framework.md`:

```
1. Il concept ha "Formato primario" = video / UGC?
   → SÌ → 25_ugc_prompt
   → NO → continua

2. Il concept è centrato sul prodotto fisico (packshot, in mano, indossato)?
   → SÌ → 26_product_shot (scegli modalità: studio / held / worn)
   → NO → continua

3. Esiste già un ad VINCENTE da scalare (da SA8 o da campagna live)?
   → SÌ → 27_multiplier (5-8 varianti Andromeda-compliant)
   → NO → continua

4. Default → 24_static_ads (statica ad image da concept + VOC + Brand DNA)
```

SA5 ha già scritto il routing suggerito nel campo "Skill di produzione SA6". Usalo come default; sovrascrivi solo se il copy SA7 o un input nuovo lo richiedono — e in quel caso **annuncia l'override** prima di procedere.

---

## Step 2 — Costruisci il piano di produzione (mostra PRIMA di generare)

Tabella riepilogo da confermare con l'utente:

| Concept | Tipo asset | Skill | Formati richiesti | Personaggio | Copy on-image |
|---------|-----------|-------|-------------------|-------------|---------------|
| 1 | statica | 24 | 1:1, 4:5, 9:16 | – | da SA7 var.A |
| 2 | UGC video | 25 | 9:16 | char_01 | dialogo |
| 3 | product shot | 26 worn | 4:5 | char_02 | – |

**Mostra la tabella e aspetta conferma** prima di generare (le skill esecutrici addebitano crediti AI).

---

## Step 3 — Esecuzione (parallelizzabile)

Le 4 skill esecutrici sono **indipendenti tra loro**. Per più concept di tipo diverso → lancia in parallelo con `run_in_background` (es. statiche del concept 1 mentre gira il video del concept 2).

Per ogni skill passa gli input richiesti:
- **24_static_ads**: Brand DNA + VOC + angolo concept → 40 prompt (subset picker per generazione)
- **25_ugc_prompt**: script/angolo + personaggio da `11_Characters/` + VOC → 6 prompt Seedance
- **26_product_shot**: foto prodotto + personaggio (se worn/held) + modalità
- **27_multiplier**: ad vincente + 1-3 foto prodotto + Brand DNA + VOC → tabella strategia (conferma) → prompt

---

## Step 4 — Finishing e formati

Dopo la generazione AI:
1. **Canva MCP** (`mcp__canva__*`) per finishing: testo on-image dal copy SA7, logo, applicazione brand kit, export multi-formato
2. Verifica copertura formati per canale (1:1, 4:5, 9:16, 1.91:1 secondo SA4)
3. Naming convention: `{brand}_{campagna}_{concept}_{formato}_{variante}`
4. Upload Google Drive con struttura per concept/ad set

---

## Output → `final/assets/` + manifest

```
## ASSET PRODOTTI — {Brand} {Campagna} {Data}

### Concept 1: [Nome] — tipo: statica — skill: 24_static_ads
- [ ] 1:1 — var A / var B
- [ ] 4:5 — var A / var B
- [ ] 9:16 — var A / var B
- Copy applicato: [da sa7_copy_deck]
- Link Drive: [url]

### Concept 2: [Nome] — tipo: UGC video — skill: 25_ugc_prompt
- [ ] 9:16 — 6 prompt / N render
- Personaggio: char_01
- Link Drive: [url]

### Manifest
| File | Concept | Formato | Skill | Modello | Stato |
```

---

## Regole critiche

- **SA6 instrada, non reinventa** — i prompt vivono nelle skill 24-27, non qui
- **Mostra il piano prima di generare** — conferma utente obbligatoria (costo crediti AI)
- **Mai switch silenzioso di skill** — se cambi il routing suggerito da SA5, annuncialo
- **Personaggio prima del video** — UGC/worn/held richiedono `11_Characters/` popolato
- **Copy da SA7, non inventato** — il testo on-image viene dal copy deck approvato
- **Formati per canale da SA4** — non produrre formati non richiesti dalla strategia

## Handoff
Asset + manifest → **Orchestrator** (`final/assets/`).
Se landing → `29_landing_page` (`/pm-landing-page`). Per lancio → `30_meta_handoff` (`/pm-handoff`).
