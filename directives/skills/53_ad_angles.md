# SA5 — Ad Angles (Angle Finder)

**Agente:** SA5 (Creative Concepts)
**Output:** `14_Creative_Briefs/angles-[brand-slug]-[YYYY-MM-DD].md` + `.json`
**Reference:** `_shared/angle_engine.md`, `_shared/awareness_tension_funnel.md`, `_shared/niche_offer_types.md`, `_shared/creative_claims_compliance.md`, `_shared/creative_kill_floor_review.md`

Strumento veloce di strategia, evidence-first: trova gli ANGOLI ad prima ancora di scrivere headline, script o concept deck completi. Sta **a monte** di `13_creative_concepts` (che produce il deck completo con brief visivo) — usa questa skill quando serve un ventaglio ampio di battaglie distinte da testare, prima di investire nel deck pieno. Gratis e solo testo, al massimo 3 domande di intake.

---

## Step 0 — Cartella + auto-discovery

```bash
WORKDIR="$PWD"
mkdir -p "$WORKDIR/14_Creative_Briefs"
```

Leggi (auto-discovery, silenzioso, annuncia in una riga cosa trovi):
- `context/brand/business_profile.md` + `context/brand/tone_of_voice.md` (Brand DNA)
- `01_VOC_Research/` o `intermediate/insight.md` (VOC: pain, desideri, obiezioni, distribuzione awareness, linguaggio goldmine, prove sanzionate)
- `intermediate/sa1_competitor_landscape.md` + `03_Ad_Spy/` più recente (barra di differenziazione, opzionale)
- `04_Static_Ads/` o output SA6 esistenti (winner del brand stesso, opzionale)

Risolvi la nicchia (`_shared/niche_offer_types.md` N.2). Documenti mancanti: procedi comunque, marca il bank `"source": "provisional"` e raccomanda una volta `/pm-dati-qualitativi` + `/pm-brand-kit`. La skill funziona da sola coi soli documenti disponibili — nessun'altra skill deve girare prima.

## Step 1 — Micro-intake, UN messaggio, max 3 domande

1. **Offerta:** "Per cosa cerchiamo angoli?" (salta se il VOC nomina già l'offerta corrente)
2. **Modalità e target — il volante è dell'utente.** Proponi il default dalla distribuzione awareness del VOC, poi passa il controllo:

> Due modalità. SPREAD: distribuisco gli angoli sugli stadi awareness per un test slate diversificato (il tuo VOC skewa problem-aware, quindi peserei lì). FOCUS: ogni angolo punta a UN SOLO stadio o funnel step che scegli tu (es. "tutti problem-aware" o "tutti retargeting"). Quale preferisci? (default: spread)

Target FOCUS accettati (`_shared/awareness_tension_funnel.md`): uno dei 5 stadi awareness OPPURE un funnel stage (TOF/MOF/BOF). Un layer di tensione può essere nominato come vincolo aggiuntivo ("tutti gli angoli L4 identità").

3. **Conteggio:** default 8, accetta 5-12 (convenzione practitioner, non regola Meta).

"Default" o silenzio prende ogni proposta. Nessuna domanda sul medium: gli angoli sono medium-neutral.

## Step 2 — Genera

Carica `_shared/angle_engine.md`, `_shared/awareness_tension_funnel.md`, `_shared/creative_claims_compliance.md`. Costruisci le 4 mappe interne (G.2), poi genera conteggio+3 candidati con lo spread di angle type (G.3), passando questi vincoli a livello di set:

| Modalità | Vincoli a livello di set |
|---|---|
| SPREAD | copri almeno 3 dei 5 stadi awareness; almeno 2 layer di tensione; pesa lo stadio VOC dominante con ~1/3 del set; nessun angle type più di 2 volte |
| FOCUS | OGNI angolo sullo stadio scelto; distinzione dalle ALTRE dimensioni: almeno 4 angle type diversi, almeno 2 layer di tensione, nessuna coppia con stessa cella persona+desiderio |

Applica tutti i gate hard G.5 (filtro generico, check meccanismo, cella unica, ancora VOC, gate prova, match calibrazione) + le regole verificate: concept non copy variant, distinzione a 3 assi, gate risultati/testimonianze, gate guadagni coaching (vedi evidenze in `angle_engine.md`).

## Step 3 — La card dell'angolo (lean by design)

Ogni angolo surfaced è ESATTAMENTE questa card (le headline sono di `54_headline_bank`, il copy pieno di `28_meta_copy`/`13_creative_concepts`):

```
A<nn> <nome angolo>   [rank]
Tipo: <angle type da G.3>
Big idea: <1-2 frasi>
Calibrazione: <stadio awareness> | <layer tensione> | <funnel stage>
Distinto su: <mondo visivo> | <messaggio> | <formato: statica, video, entrambi>
Hook line: <una riga di apertura nel registro del cliente, meccanica nominata>
Il cliente dice: "<citazione VOC verbatim>" (voc:<rif>)
Perché funziona: <1-2 frasi, un segnale VOC + un gap white-space o segnale winner>
Route to: <13_creative_concepts per il deck pieno | 54_headline_bank | 55_video_script | 24_static_ads>
```

## Step 4 — Self-review, kill floor, look-alike pass

Carica `_shared/creative_kill_floor_review.md`, gira D.2a per ogni angolo. Poi il LOOK-ALIKE PASS: confronta ogni coppia di angoli superstiti e chiedi "produrrebbero ad che si somigliano o si sentono simili?" — forza la differenziazione o uccidi uno dei due, dichiarando quale asse era troppo vicino. Infine ordina best-first (G.7) e taglia fino al conteggio richiesto con ragioni in una riga.

## Step 5 — Presenta, itera, salva

Presenta in chat come testo semplice: una riga di calibrazione (modalità, target, nicchia, conteggio), le card ordinate, poi `Killed:` con le ragioni. Chiedi una volta:

> Approvi tutto, uccidi, o modifichi angolo per angolo ("approva tutto", "uccidi 3", "modifica 5: puntalo sull'odore invece"). O guida l'intero set: "rifocalizza su product-aware", "più angoli identity". Niente a valle consuma questo bank finché non lo approvi.

Le modifiche rigenerano solo gli angoli nominati attraverso gli stessi gate (max 2 cicli). All'approvazione, scrivi ENTRAMBI i file:

```
$WORKDIR/14_Creative_Briefs/angles-<brand-slug>-<YYYY-MM-DD>.md
$WORKDIR/14_Creative_Briefs/angles-<brand-slug>-<YYYY-MM-DD>.json
```

Sidecar JSON (valido, riparsalo prima di dichiarare fatto):

```json
{
  "schema_version": 1, "kind": "angle-bank",
  "brand": "<slug>", "created_at": "<ISO>",
  "mode": "spread | focus", "focus_target": "<stadio o funnel, null in spread>",
  "niche": "dtc | info | service", "offer": "<per cosa era questo run>",
  "count": 8, "approved": true, "approved_at": "<ISO>",
  "source": "docs | docs+spy | provisional",
  "angles": [ { "id": "A01", "rank": 1, "name": "", "angle_type": "", "big_idea": "",
    "awareness_stage": "", "tension_layer": "", "funnel_stage": "",
    "distinct_on": { "visual_world": "", "message": "", "format": "" },
    "hook_line": "", "hook_mechanic": "", "voc_quote": "", "voc_source_ref": "voc:S4",
    "route_to": "", "status": "approved | killed", "kill_reason": null } ]
}
```

Gli id (`A01`...) sono stabili, mai riusati in un bank; sono la chiave di join a valle. Suffisso `-2`/`-3` se il basename esiste; mai sovrascrivere un bank approvato. Stampa i path assoluti + riepilogo route: "Usa `13_creative_concepts` per il deck pieno partendo dagli id, `54_headline_bank` per una bank di headline, `55_video_script` per uno script — tutti accettano 'per l'angolo A03'."

## Come le altre skill consumano un angle bank

- **`13_creative_concepts`**: rileva il `angles-*.json` più recente approvato, offre di costruire il deck pieno PARTENDO dagli id scelti (salta la propria generazione di angoli; calibrazione e citazioni passano verbatim, id sorgente registrato su ogni concept).
- **`54_headline_bank`** e **`55_video_script`**: accettano "per l'angolo A03" come modalità di input; big idea, calibrazione e citazione della card sono l'ancora, consumate verbatim.
- **`24_static_ads`**: un angle bank approvato può seminare il suo slate di concept come farebbe un deck approvato.

## Regole hard

- **La card lean è l'intero deliverable.** Niente headline, niente primary text, niente script, niente render prompt. Route-to fa l'handoff.
- **L'utente possiede il volante.** SPREAD e FOCUS sono la sua scelta; una richiesta FOCUS non va mai ritrasformata in spread.
- **Concept, non copy variant.** La distinzione a 3 assi e il look-alike pass sono legge.
- **Gratis e solo testo.** Max 3 domande di intake, in un messaggio. Funziona da sola dai documenti.
- **Il bank è ordinato e tagliato.** Un bank non tagliato è una review fallita.
- **Gli id sono immutabili** una volta scritti.
