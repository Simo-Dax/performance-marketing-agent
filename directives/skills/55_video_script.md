# SA6 — Video Script Studio

**Agente:** SA6 (Asset Production)
**Output:** `15_Video_Scripts/script-[slug]-[formato]-[secondi]s-[YYYY-MM-DD].md`
**Reference:** `_shared/script_frameworks.md`, `_shared/awareness_tension_funnel.md`, `_shared/niche_offer_types.md`, `_shared/creative_claims_compliance.md`, `_shared/creative_kill_floor_review.md`, `context/brand/anti_ai_writing_style.md`

Studio di script video universale: qualsiasi formato (UGC a camera, solo voiceover, dialogo a due, founder talking-head, VSL lungo), qualsiasi nicchia. L'utente decide la lunghezza (preset 10s-90s+ o secondi custom), la skill converte in un budget di parole esatto così lo script entra davvero nel tempo. Gratis e solo testo — **non produce video**, produce lo script finito.

> **Relazione con `25_ugc_prompt`:** quella skill scrive già i propri script internamente (Step 3, hook+framework) prima di esplodere in 4 ad — non richiede questa skill come prerequisito. Usa `55_video_script` quando: (a) serve un formato che `25_ugc_prompt` non copre (voiceover-only, dialogo a due, founder, VSL lungo — production path da consegnare a un creator umano), (b) serve un deliverable-script veloce senza passare dai gate della factory, (c) l'utente vuole partire da uno script già approvato invece di farne scrivere uno nuovo a `25_ugc_prompt`.

---

## Step 0 — Cartella + auto-discovery

```bash
WORKDIR="$PWD"
mkdir -p "$WORKDIR/15_Video_Scripts"
```

Leggi: `01_VOC_Research/` (pain, desideri, obiezioni, awareness, linguaggio goldmine, prove sanzionate), `context/brand/tone_of_voice.md`. Risolvi la nicchia (`_shared/niche_offer_types.md`). Controlla anche:
```bash
ls -t "$WORKDIR/14_Creative_Briefs/"angles-*.json 2>/dev/null | head -n 1
ls -d "$WORKDIR/03_Ad_Spy/"*-video 2>/dev/null | head -n 1
```
Un angle bank approvato abilita lo scripting concept-driven (nomina l'id come ancora allo Step 1, big idea/calibrazione/citazione consumate verbatim). Una cartella teardown `03_Ad_Spy/<slug>-video/` (da `52_ad_spy_video`) sblocca l'upgrade di pacing misurato (Step 2) ed evidenza sui winner (Step 4).

## Step 1 — Intake, UN messaggio

Rileva cosa l'utente ha già dato. Chiedi SOLO i pezzi mancanti, tutti in un messaggio:

1. **Soggetto** (salta se già dato): "Di cosa parla lo script? Descrivi il prodotto/angolo, nomina un id da angle bank, o di' 'rispondi ai loro ad' per scriptare contro i teardown competitor."
2. **Formato**:

| # | Formato | Cos'è | Consumer a valle |
|---|---|---|---|
| 1 | UGC a camera | un creator che parla a camera, b-roll di cutaway | `25_ugc_prompt`, o un creator umano |
| 2 | Solo voiceover | VO continuo su scene, nessuno speaker in camera | animazione/claymation, montaggio b-roll |
| 3 | Dialogo a due | due persone in conversazione, turni alternati | produzione podcast/dialogo |
| 4 | Founder talking-head | il founder parla con calma a camera, story-led | ripresa umana |
| 5 | VSL lungo | arco direct-response per coaching/high-ticket | ad webinar/VSL |

3. **Lunghezza, LA SCEGLIE L'UTENTE.** Offri i preset, accetta QUALSIASI secondi custom:

> Quanto deve durare? 10s (Stories/reminder), 15s (hook-test feed), 30s (lo standard, mio default), 45-60s (story/meccanismo pesante), 90s+ (VSL). O scrivi un numero di secondi qualsiasi.

Proponi un default: retargeting/product-aware → 10-15s, UGC standard → 30s, problem-unaware/meccanismo pesante → 45-60s, VSL coaching → 90s+.
4. **CTA** (proponi il default di nicchia da `_shared/niche_offer_types.md`).
5. **Conteggio:** quanti script (default 1, max 4; script multipli devono prendere angoli diversi, mai lo stesso script due volte).

"Default" o silenzio prende ogni default proposto. Calibra awareness/tensione/funnel via `_shared/awareness_tension_funnel.md` (proponi i default derivati, override in una parola).

## Step 2 — LA MATEMATICA, prima di scrivere una riga

Deterministico. Calcola e MOSTRA il budget prima di scrivere:

1. **Scegli wps** (parole al secondo), in quest'ordine di priorità:

| Priorità | Fonte | Valori |
|---|---|---|
| 1 | MISURATO dai teardown `03_Ad_Spy/<slug>-video/` se esistono: prendi i 3 ad top con voiceover (scarta i music-only), dividi parole totali per secondi parlati totali, di' "misurato X wps dai winner della tua nicchia" | quello che dicono i dati |
| 2 | Costanti di produzione (`_shared/script_frameworks.md`) | UGC/founder/two-host ~3,5; voiceover-only ~2,5; founder ~2,8-3,0; VSL ~2,9 (mirror da talking-head) |

2. **Budget parole** = secondi × wps. Esempio: 30s UGC = 30×3,5 = 105 parole. Tolleranza ±10%. Uno script 30s con 160 parole è un FALLIMENTO anche se le parole sono buone.
3. **Budget hook** = 3×wps parole (~10 per UGC). La value proposition deve essere leggibile dentro quelle parole.
4. **Allocazione per beat** (split default del budget):

| Lunghezza | Hook | Body | Mid-beat | Body profondo/prova | CTA |
|---|---|---|---|---|---|
| 10-15s | 25% | 45% | — | — | 30% |
| 30s | 12% | 45% | — (no mid-CTA sotto 20s) | 28% | 15% |
| 45-60s | 10% | 35% | mid-hook/pattern reset a metà | 40% | 15% |
| 90s+ | 8% | 52% (arco hook-story-offer) | pattern reset ogni 12-15s | 30% (prova impilata metà-fine) | 10% |

5. Ceiling segmento: se lo script alimenta una factory AI (`25_ugc_prompt`), nessuna presa continua supera i 9 secondi di parlato — scrivi micro-pause naturali o punti di taglio almeno a quella frequenza.

## Step 3 — Scegli il framework

Carica `_shared/script_frameworks.md` col mode giusto (`self-voice` per formati 1/4, `external-VO` per 2, `two-speaker-turns` per 3; VSL 90s+ usa hook-story-offer) e il wps dello Step 2. Scegli UN framework dalla tabella di selezione (angolo problem/pain → PAS o SIMPLE; contrarian → DISRUPT; meccanismo → CURE o CROWD; founder → FOUNDER o PROVE; comparison → SHOW; social proof → CROWD; native/anti-ad → PURE o UGLY).

Hook-story-offer (VSL): HOOK (chi è + la promessa), STORY (la valle del prima, il momento di scoperta, il meccanismo nominato), PROOF (risultati sourced con contesto tipicità), OFFER (cosa ottengono, risk reversal se reale), CTA (un'azione). Pattern reset ogni 12-15s.

## Step 4 — Scrivi prima gli hook, 3 varianti per script

1. Tre varianti, ognuna da una famiglia DIVERSA (`_shared/script_frameworks.md` evidenze):
   - **Offerta/urgenza/immediatezza-led** (famiglia top verificata): il valore o la novità concreta nella prima riga.
   - **Confessione:** un'ammissione in prima persona.
   - **Demographic call-out:** nomina l'audience.
2. Domanda/listicle/how-to/explainer sono default PIÙ DEBOLI — usane uno solo come quarta variante chiaramente etichettata, mai come lead.
3. HARD-FLAG e riscrivi ogni apertura lifestyle/beneficio vaga.
4. Ogni hook: value proposition leggibile entro il secondo 3, payoff entro il secondo 6, il primo shot porta motion/visual device (mai un volto statico che si assesta). Un dispositivo hook visivo per variante (reveal, focus rack, testo su schermo, ecc. — libreria in `script_frameworks.md` E.2 evidenze).
5. Ancora il linguaggio hook al linguaggio goldmine VOC. Se esistono teardown spy-video, controlla gli hook verbatim dei top ad e differenziati, mai copiare.

## Step 5 — Scrivi il body, beat per beat

Scrivi sull'allocazione dello Step 2, beat del framework dello Step 3, tre tracce parallele: **VO/dialogo** (parole esatte, frasi naturali parlate, contrazioni, registro brand — dialogo a due: turni alternati, 6-9 parole a battuta, mai due prese consecutive stesso speaker), **testo on-screen** (2,5-3 parole/sec massimo, stile keyword non frasi complete), **b-roll/shot** (una direzione concreta per beat — per VO-only è il seme dello storyboard, per UGC marca dove mani/prodotto portano la riga).

Regole: una CTA, lo script FINISCE su di essa. Mid-CTA solo in script 30s+, mai una richiesta dura. Un open loop aperto nell'hook deve risolversi nel body profondo di script 45s+. I beat non sono MAI etichettati nello script finale.

## Step 6 — Passaggio compliance (binario)

Carica `_shared/creative_claims_compliance.md`. Ogni riga: gate prova (C.1), gate nicchia + guadagni (C.2 — per script coaching/info: NESSUN livello/range di reddito implicito senza sostanziazione scritta + contesto tipico; niente b-roll lifestyle-flex che implica reddito), gate salute per ingeribili/topici DTC (struttura-funzione), niente urgenza finta (C.3).

## Step 7 — Passaggio voce naturale

Applica `context/brand/anti_ai_writing_style.md` / `49_anti_ai_slop` sulla traccia VO: niente one-liner impilati, niente ritmo a lista parallela, niente aperture bannate, leggi ogni riga ad alta voce mentalmente, riscrivi ciò che non diresti a un amico al tavolo di cucina. Passaggio silenzioso, mai annunciato.

## Step 8 — Self-review, kill floor

Carica `_shared/creative_kill_floor_review.md` D.2c + checklist: budget entro ±10%, hook timing (value prop entro 3×wps parole, payoff entro 6s), famiglia hook lead da quelle ammesse, framework davvero seguito, CTA singola e coerente, nessuna presa oltre 9s se factory-bound, compliance verde, voce che regge la lettura ad alta voce, evidenza VOC sull'hook/claim centrale, script multipli distinti per angolo e famiglia hook (non solo parole), filtro generico (con brand cambiato lo script non deve poter girare per chiunque nella categoria).

Ordina le 3 varianti hook best-first, UCCIDI la più debole con una ragione. Script che fallisce un check → riscritto prima che l'utente lo veda, max 2 cicli, poi presenta col problema residuo dichiarato onestamente.

## Step 9 — Presenta, itera, salva

Presenta in chat: riga di calibrazione (formato, lunghezza, wps usato+fonte, framework, awareness, funnel, CTA), poi per script: i 3 hook ordinati con dispositivo visivo e nota di kill, la tabella beat (Tempo | VO | On-screen | Shot), conteggio parole vs budget. Chiedi una volta: "Vuoi spingere qualcosa? 'hook 2 più tagliente', 'pacing più lento', 'portalo a 45s' (ricalcolo e riscrivo), o 'salva'."

Al salvataggio, un file per script:
```
$WORKDIR/15_Video_Scripts/script-<slug>-<formato>-<secondi>s-<YYYY-MM-DD>.md
```
Header con: formato, secondi, wps+fonte, framework, calibrazione, nicchia, documenti sorgente, id concept se deck-driven (anche nel filename: `script-A05-ugc-30s-<data>.md`). Stampa i path assoluti e la riga di routing: "Script formato 1/2 entrano diretti in `/pm-ugc-video` (`25_ugc_prompt`, li troverà), o consegna il file a un creator."

## Regole hard

- **La matematica è legge.** Mai presentare uno script il cui conteggio parole sfora il budget. Ricalcola o taglia, mai sperare.
- **L'utente possiede la lunghezza.** Qualsiasi secondi digiti è valido; la skill adatta la struttura, non lo forza mai su un preset.
- **Gratis e solo testo.** Nessun rendering, nessun path di generazione — quello è `25_ugc_prompt` o un creator umano.
- **Un solo compito.** Solo script finiti. Le headline sono `54_headline_bank`, i concept sono `53_ad_angles`/`13_creative_concepts`.
- **Gate guadagni assoluto** per script coaching/info. Nel dubbio, linguaggio di trasformazione, mai cifre.
