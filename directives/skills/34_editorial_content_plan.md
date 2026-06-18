# Editorial & Content Plan — Piano Editoriale + Content Calendar

**Fase:** post-Strategy (dopo SA4 brand strategy + campaign architecture). Organico, complementare al paid.
**Input:** `intermediate/sa4_brand_strategy.md` + `intermediate/tone_of_voice_campaign.md` + `intermediate/insight.md` + `01_VOC_Research/`
**Output:** `output/{brand}_{campaign}_{date}/intermediate/editorial_plan.md` + `.../intermediate/content_calendar.md`. Vedi Convenzione Output in `claude.md`.
**Origine:** internalizzato da `editorial-planner` + parte content di `content-lp-writer` del Marketing Strategist (metodo Learnn fase 4).

---

## Cosa produce

Tre artefatti:
1. **Piano editoriale** — macrotemi + titoli mappati sui 5 stadi di awareness
2. **Content marketing plan** — contenuti per fase funnel (awareness/consideration/conversion)
3. **Content calendar** — calendarizzazione operativa pubblicabile

Materiale **grezzo ad alta densità di insight**, NON copy finale. Il tono finale lo dà `03_editing_selfcheck` (modalità brand-campagna).

---

## A) Piano Editoriale

```
### Macrotemi (2-5)
Per ogni macrotema:
- Angolo + perché conta per il target (leva emotiva o razionale dagli insight)
- 10 titoli di post

### Mappa awareness (5 stadi Eugene Schwartz)
| Titolo | Macrotema | Awareness stage | Formato consigliato |
|--------|-----------|-----------------|---------------------|
| ... | ... | Unaware / Problem-Aware / Solution-Aware / Product-Aware / Most-Aware | reel / carosello / post / story / long-form |
```

**Regole:**
- Niente titoli generici. Ogni titolo aggancia un **pain, desiderio, obiezione o USP reale** dagli insight.
- Segnala i macrotemi deboli invece di riempire per quota.
- Formato più adatto per stadio: Unaware → educativo/curiosità; Problem-Aware → agita il problema; Solution-Aware → confronto soluzioni; Product-Aware → demo/proof; Most-Aware → offerta.

## B) Content Marketing Plan (per funnel)

```
| Funnel stage | Obiettivo | Titolo | Focus strategico | Pain/Desiderio/USP agganciata | Formato |
|--------------|-----------|--------|------------------|-------------------------------|---------|
| Awareness | ... | ... | ... | ... | ... |
| Consideration | ... | ... | ... | ... | ... |
| Conversion | ... | ... | ... | ... | ... |
```
- Minimo **5 contenuti per fase** del funnel.
- Prioritizza contenuti informativi e utili; mostra come incorporare il prodotto nella vita del target; promuovi i valori del brand.

## C) Content Calendar (operativo)

```
| Settimana | Giorno | Canale | Macrotema | Titolo/Hook | Awareness | Formato | CTA | Stato |
|-----------|--------|--------|-----------|-------------|-----------|---------|-----|-------|
| W1 | Lun | IG | ... | ... | Problem-Aware | reel | ... | da produrre |
```
- Cadenza realistica (non riempire per riempire). Bilancia i 5 stadi di awareness e i macrotemi nel tempo.
- Allinea i picchi di contenuto a stagionalità/promo dalla strategia e ai trigger event.
- Collega, dove sensato, ai concept paid di SA5 (coerenza organico↔paid).

---

## Regole critiche

- Ogni titolo/contenuto ancora a un insight reale (pain/desiderio/obiezione/USP). Mai contenuto generico.
- Rispetta ToV, valori e **nemico del brand** da `tone_of_voice_campaign.md`.
- Materiale grezzo: il tono finale passa da `03_editing_selfcheck` (modalità brand-campagna), non da qui.
- Bilanciamento awareness: non tutto BOF/offerta. La maggior parte del contenuto organico è TOF/MOF (educa, agita, dimostra).

## Handoff
`editorial_plan.md` + `content_calendar.md` → produzione contenuti (SA6 per i visual, `03_editing_selfcheck` per il tono). Complementare al funnel paid di SA4.

---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
