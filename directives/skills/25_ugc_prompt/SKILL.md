# SA6 — UGC Factory (Seedance 2.0, Andromeda)

**Agente:** SA6 (Asset Production)
**Output:** `05_UGC_Prompts/factory/<concept-slug>/` — 4 ad MP4 (25-45s), clip raw, manifest
**Modello:** Seedance 2.0, 9:16, 1080p, audio ON
**Reference:** `references/` (generation-architecture, andromeda-variation, scripting-frameworks, hook-library, seedance-2.0-limits, consistency-and-assembly, VERIFIED-backend-facts)
**Script:** `scripts/` (segment_script.py, validate_payload.py, build_manifest.py, stitch.sh)

---

## Cambio di filosofia (v2 — Factory)

Questa skill **non produce più 6 prompt da incollare a mano**. È una **factory end-to-end**: estrae hook → scrive uno script con framework → lo fa esplodere in **4 ad UGC genuinamente distinti** (modello Andromeda) → genera le clip → le monta in **4 video MP4 finiti** (25-45s, ognuno di lunghezza diversa, **ognuno che chiude sulla CTA**), più un pacchetto raw facile da editare.

**Leggi tutto questo file prima di iniziare.** Poi: Step 0.5 (cartella + auto-discovery) → Step 0-7 in ordine. **Leggi `references/generation-architecture.md` per primo** — è la single source of truth su come generazioni/clip/4-ad si incastrano.

Due **hard stop** obbligatori:
- **GATE TRANSCRIPT (Step 3.5):** l'umano approva esattamente cosa si dice nei 4 ad PRIMA che si scriva un prompt o una durata.
- **GATE COSTO/PACING (Step 4):** l'umano approva la tabella di pacing e il costo PRIMA di renderizzare una sola clip.

Termina il turno a ogni gate e attendi approvazione umana esplicita.

> **Nota architettura:** la factory NON scrapa TikTok. Gli hook vengono dalla `hook-library` + VOC. Il tuo `20_ugc_scraper` (SA1) resta separato come research/swipe-file, indipendente da questa skill.

## Il modello in un respiro

- INPUT caricati una volta, riusati su ogni generazione: UNA face image, UN body image, UN product image, UN voice clip (max 15s).
- Lo STESSO voice clip cavalca ogni generazione come VOICE REFERENCE (anche i b-roll product-only, come voiceover). Audio ON su ogni clip. Niente TTS, niente clone, niente spine separato.
- Gli STESSI byte face+body su ogni generazione CHARACTER (+ product image quando il prodotto è in scena). Byte identici, mai ri-croppati. È l'àncora di identità.
- **I B-ROLL SONO PRODUCT-ONLY** — solo il prodotto (mano anonima o su superficie) + voiceover. NO character.
- **OGNI GENERAZIONE È SOTTO 10s** (intero 4-9), 9:16 verticale, 1080p. Niente generazione 15s. Gli ad lunghi sono molte generazioni corte concatenate.
- Una generazione può contenere UNA o PIÙ scene descritte nel prompt (Seedance taglia, niente parametro multi-shot: descrivi le scene, setti solo i secondi TOTALI). Le multi-scena si splittano ai tagli dopo.
- **OGNI AD ASSEMBLATO CHIUDE SULLA CTA.** I b-roll si inseriscono solo in mezzo, mai dopo la CTA.

Il craft non negoziabile è il **PACING**, regola FAST AND PUNCHY (~3.5 parole/sec). Seedance allunga la battuta per riempire la durata richiesta → la durata scelta È la velocità di parlato. Non paddare.

**Gotcha Higgsfield (Path B/D):** ri-carica la media FRESCA e usala subito. Il voice clip in particolare: Higgsfield trasforma pigramente l'audio in un `_sfx.wav` dopo il primo uso e le generazioni successive che lo risolvono FALLISCONO con errore vuoto. Ri-carica il voice fresco prima di ogni generazione (su Path B la CLI auto-uploada il path locale a ogni chiamata → sidesteppa). Su Path C (fal) uploadi una volta e riusi l'URL.

---

## Step 0.5 — Cartella output + auto-discovery (PRIMA di tutto)

Gli output vanno nella cartella dove Claude Code è aperto (la campaign folder = `$AILAB`). Risolvi `$AILAB` e gli script:

```bash
AILAB="$PWD"
# Risolvi la root del progetto (cerca verso l'alto directives/skills/25_ugc_prompt/scripts)
ROOT="$PWD"; while [ "$ROOT" != "/" ] && [ ! -d "$ROOT/directives/skills/25_ugc_prompt/scripts" ]; do ROOT="$(dirname "$ROOT")"; done
SCRIPTS="$ROOT/directives/skills/25_ugc_prompt/scripts"
mkdir -p "$AILAB/05_UGC_Prompts/factory"
echo "AILAB=$AILAB"; echo "SCRIPTS=$SCRIPTS"
```

Una volta nominato il concept (Step 2): `WORK="$AILAB/05_UGC_Prompts/factory/<concept-slug>"` e `mkdir -p "$WORK/clips" "$WORK/out" "$WORK/inputs"`. Ogni file intermedio, clip raw e ad finale va sotto `$WORK`.

### Auto-discovery asset salvati
Riusa ciò che è già nel progetto prima di chiedere upload:
- **Character (face+body):** scansiona `11_Characters/` (creati da `22_character_creator`). Se esistono, offri: face = `11_Characters/<name>/headshot.png`, body = `11_Characters/<name>/fullbody.png`. Stesso volto su tutti e 4 gli ad = forma giusta per paid. Se l'utente ne sceglie uno, non chiedere upload separato.
- **Product image:** scansiona `_assets/product-shots/` e `_assets/product-images/`. Offri il più recente; override possibile.
- **VOC + Brand DNA:** `ls -t "01_VOC_Research/"*.{html,md}` e `"02_Brand_DNA/"*.{html,md}` (head -1). Se trovati, usali per affinare hook e script.

Se `11_Characters/` è vuoto, nota che lanciare `22_character_creator` (`/pm-buyer-persona`) prima dà lo stesso volto a ogni ad, poi continua con upload face+body se l'utente preferisce.

---

## Step 0 — INTAKE

Raccogli (spiega ogni input in una riga). Non partire senza i 4 asset richiesti. Se lo Step 0.5 ha già trovato character/product/VOC/Brand DNA, usali e chiedi solo il mancante (sempre il voice clip; la misura prodotto se non leggibile dall'immagine).

| Input | Obbl. | Scopo |
|---|---|---|
| Face image | Sì | Àncora volto, byte-identica su ogni gen character. Auto da `11_Characters/<name>/headshot.png`. |
| Body image | Sì | Àncora corpo+wardrobe, byte-identica su ogni gen character. Auto da `fullbody.png`. |
| Product image | Sì | Il prodotto. Su ogni product shot E sui b-roll product-only. Auto da `_assets/`. |
| Misura prodotto | Sì | Dimensione reale (es. "pouch 360g, ~19cm", "bottiglia 50ml"). Va in OGNI prompt che mostra il prodotto, per scala credibile. Leggi dall'etichetta; se illeggibile, CHIEDI. Mai inventare. |
| Voice clip ≤15s | Sì | Voice reference su ogni gen (b-roll voiceover incluso) → voce consistente. L'utente lo registra (es. ElevenLabs). |
| Niche | Sì | Per chi è e cos'è il prodotto, 1-2 frasi. |
| VOC / Brand DNA | Opz. | Linguaggio cliente + regole brand. Auto-discovery. |

Check prima di proseguire: voice ≤15s (se più lungo, rimanda — trim è compito dell'utente); face/body puliti frontali; product image presente; misura prodotto reale (letta o fornita). **NON scrapare TikTok per gli hook.**

---

## Step 1 — HOOK MINING (verbale)

Pesca candidate hook da `references/hook-library.md`, bias verso niche + VOC. **No scraping.**
- 8-12 linee hook parlate, punchy, prima persona UGC, corte, non slogan.
- Servono esattamente **4 hook DISTINTI, uno per ad**, ognuno un ANGOLO diverso (confessione, contrarian, claim diretto, curiosità), non solo riformulati. Gli hook NON si condividono tra ad.
- Corti: ~8-13 parole (rendono in ~3-5s). La lunghezza hook non è una leva di distinzione → non laddizzarli.

---

## Step 2 — SCRIPT FIRST

Scrivi lo script prima di pensare ai secondi. Scegli UN framework da `references/scripting-frameworks.md` adatto a niche + awareness, e dichiara quale e perché.
- BODY come beat sheet: beat ordinati, ognuno un pensiero parlato completo, UGC naturale. Body tipico = 4 beat: pain, solution, proof, CTA.
- **Il body DEVE CHIUDERE sul beat CTA.**
- Il body è il core condiviso che tutti e 4 gli ad riusano. Scrivilo una volta, bene.
- Scrivi le 2 linee voiceover B-ROLL product-only (corte, focus prodotto). Il pool b-roll è esattamente 2 clip (bA, bB), riusate.
- Linee parlabili: niente phrasing da ad scritto, niente trattini come separatori, ritmo parlato reale.

Nomina il concept → crea `$WORK` e copia i 4 asset in `$WORK/inputs/`. **Niente durate ancora** (è lo Step 4).

---

## Step 3 — ANDROMEDA VARIATION

Trasforma un body in 4 ad che sono TIMELINE genuinamente DIVERSE (`references/andromeda-variation.md` + `generation-architecture.md`).

PRIMA (NO): un body, solo l'hook swappato, resto identico = consolidato e throttlato.
DOPO (SÌ): distinzione e lunghezze diverse da **4 hook UNICI + un B-ROLL-COUNT LADDER (0, 1, 2, 2)**. Ogni ad ha il suo hook e un numero diverso dei 2 b-roll condivisi, inseriti in punti spaziati, e **ogni ad chiude sulla CTA**:

| Ad | Hook | B-roll | Timeline (chiude sempre su CTA) | Banda lunghezza |
|---|---|---|---|---|
| V1 | hook 1 | 0 | hook → pain → solution → proof → CTA | più corto |
| V2 | hook 2 | 1 | hook → bA → pain → solution → proof → CTA | + ~un b-roll |
| V3 | hook 3 | 2 | hook → bA → pain → solution → bB → proof → CTA | + due b-roll |
| V4 | hook 4 | 2 | hook → pain → bA → solution → proof → bB → CTA | + due b-roll, piazzati diversamente |

Regole: 4 hook unici (angolo verbale E tipo di azione visiva diversi); i 2 b-roll sono PRODUCT-ONLY, inseriti solo in MEZZO, mai dopo la CTA; V3 e V4 usano entrambi i b-roll ma a placement DIVERSI; fingerprint di distinzione = hash stabile degli assi che impattano il render. `build_manifest.py` impone fingerprint unici, che ogni ad chiuda su CTA, e che nessun b-roll stia dopo la CTA. Niente hook-length ladder.

Produci una tabella variazioni (hook verbale, hook visivo, count+placement b-roll per ad). Conferma 4 distinti e 4 che chiudono su CTA.

---

## Step 3.5 — 🚦 GATE TRANSCRIPT (hard stop: parole PRIMA dei prompt)

Prima di scrivere un solo prompt o assegnare un secondo, mostra all'utente ESATTAMENTE COSA SI DICE in ognuno dei 4 ad, in ordine, e ottieni approvazione esplicita delle parole.

Per ogni ad V1-V4 stampa il transcript completo in ordine di play, ogni linea etichettata col ruolo:
```
V1  (hook → pain → solution → proof → CTA)
  [HOOK]  <hook 1>
  [BODY]  <pain>
  [BODY]  <solution>
  [BODY]  <proof>
  [CTA]   <CTA>
V2  (hook → bA → pain → solution → proof → CTA)
  [HOOK]  <hook 2>
  [BROLL] <bA>
  ...
```
È il momento per fixare wording, tagliare slop, cambiare un hook — finché è solo testo e costa zero. Poi **STOP, termina il turno.** Non scrivere prompt né durate né lanciare il segmenter. Attendi approvazione (gli edit si applicano e si ri-mostrano fino all'ok). Solo DOPO l'ok → Step 4. Prompt e durate sono DERIVATI dalle parole approvate.

---

## Step 4 — PACING + SEGMENTAZIONE (make-or-break, hard gate)

PREREQUISITO: transcript Step 3.5 approvato. Ora misuri le parole APPROVATE per decidere quanti secondi per generazione. Leggi `references/seedance-2.0-limits.md`.

METODO (locked): Seedance ALLUNGA la battuta per riempire la durata → la durata È la velocità. Target FAST/PUNCHY ~3.5 wps: `requested_seconds = round(word_count / 3.5)`. Aggiungi secondi SOLO per azione on-screen reale (gli hook: un dump, uno slam, ~1-2s). Nulla ai body shot parlati o ai b-roll. **Ogni generazione SOTTO 10s (intero 4-9).** Se serve ≥10s, splitta in più generazioni.

Autora `beat_sheet.json` per il body sotto `$WORK`, poi gira il segmenter **un beat alla volta** (così il packer greedy non incolla la prima frase di un beat sul precedente — es. il "Try the Welcome Kit." della CTA non deve finire sulla proof clip). Lo script RICHIEDE due argomenti file posizionali, mai bare:

```bash
python3 "$SCRIPTS/segment_script.py" "$WORK/body_beats.json" "$WORK/body_shots.json"
echo "exit=$?"
```

Restituisce per generazione: vo_text, word_count, requested_seconds, pace (wps). Usa i numeri VERBATIM. CONTROLLA L'EXIT CODE: non-zero = generazione mal-pacing (fuori ~2.4-4.0 wps) o ≥10s → STOP, ri-splitta/riscrivi, ri-gira. Ogni run deve tornare exit=0. Fai lo stesso per hook (reel beat sheet) e b-roll.

### 🚦 GATE COSTO/PACING (hard stop)
Le parole sono già approvate (3.5). Questo gate è su secondi e spesa. Presenta 5 cose in chat:
1. Framework scelto + recap script approvati (body che chiude su CTA, 4 hook, 2 b-roll).
2. Tabella variazioni (4 hook unici, ladder 0/1/2/2, tutti chiudono su CTA).
3. Tabella pacing completa dal tool (ogni gen <10s, ~3.5 wps).
4. Il path generazione scelto (A/B/C/D — Step 4.5). Sceglilo ora per il preview costo nell'unità giusta.
5. PREVIEW COSTO: secondi totali generati = somma di ogni generazione (hook reel + body shot + 2 b-roll). Path B/D → crediti Higgsfield (~9 crediti/sec a 1080p, conferma il costo/sec live). Path C → dollari (prezzo/sec fal, confermato a runtime). Path A → nessun costo automazione.

Poi **STOP, termina il turno.** Non chiamare alcun tool di generazione nello stesso turno del gate. Genera solo se l'utente risponde in un turno SUCCESSIVO con approvazione esplicita. Tuo giudizio/silenzio = RIFIUTO.

Tabella pacing:
| gen_id | role | words | seconds | wps | status |
|---|---|---|---|---|---|

---

## Step 4.5 — Scelta path generazione (A / B / C / D)

PREREQUISITO: gate Step 4 approvato. Frame:

> Tutte le generazioni sono prezzate e approvate. Quattro modi di renderizzarle:
>
> **(A) Manuale su Higgsfield.** Gratis. Ti do ogni prompt con durata/attachment/audio esatti. Incolli in Higgsfield (Seedance 2.0, 1080p, 9:16), generi, droppi le clip in `clips/`. Poi splitto gli hook reel e monto i 4 ad.
> **(B) Higgsfield CLI.** Se hai subscription. Genero ogni clip chiamando Higgsfield. Primo uso installa la CLI + device login. Mostro il saldo crediti e attendo `yes` esplicito prima di spendere.
> **(C) fal.ai pay-per-result.** Senza subscription. Renderizzo su `bytedance/seedance-2.0/reference-to-video`, billing a secondo in dollari. Richiede Fal AI key (`/pm-setup-fal-ai`).
> **(D) Web UI via Playwright.** Guido la UI Higgsfield, con ok esplicito a ogni upload e generate.
>
> Quale path, A, B, C o D?

### Path B — Higgsfield CLI
Variabili skill-specific: `{{SKILL_SLUG}}`=`ugc-factory`; `{{MODEL_ID}}`=`seedance_2_pro` (Seedance 2.0; `seedance_2_lite` per test fast — verifica l'id live con `higgsfield model list` se la CLI lo rifiuta); `{{ASPECT}}`=`9:16`; `{{RESOLUTION}}`=`1080p`; `{{QUALITY}}` omesso (Seedance lo ignora); `{{OUTPUT_DIR}}`=`$WORK/clips`; `{{OUTPUT_FILENAME}}` = `hook_reel_A.mp4`, `hook_reel_B.mp4`, `body_01..04.mp4`, `broll_A.mp4`, `broll_B.mp4`.
- Durata = intero 4-9 dalla tabella approvata (NON `--duration "15"`). `--duration "<n>"`.
- `--generate_audio "true"` su ogni gen, b-roll inclusi.
- Reference come flag `--image` separati. Gen character (hook, body) → face + body (+ product quando in scena). B-roll product-only → solo product. Voice clip su ogni gen.
- Passa il voice fresco a ogni chiamata (la CLI auto-uploada → sidesteppa il bug `_sfx.wav`).
- Dopo i 2 hook reel, SPLITTA ognuno al taglio in 4 hook clip con ffmpeg prima dell'assembly.

### Path C — fal.ai
Gate first: verifica Fal AI key (`/pm-setup-fal-ai` se manca). Poi:
- Conferma `mcp__fal-ai__*` visibili. Se no nonostante la key, ricarica Claude Code (Cmd+Q) per far prendere la key all'MCP.
- Modello: `bytedance/seedance-2.0/reference-to-video`. Verifica lo shape input con `mcp__fal-ai__get_model_schema` prima della prima chiamata.
- Upload media con `mcp__fal-ai__upload_file`, UN yes esplicito per file. Se è stato scelto un character salvato, uploada `headshot.png` (face) + `fullbody.png` (body) una volta e riusa gli URL. Idem product image e voice.
- Per gen: referenzia la media uploadata per schema, `resolution: "1080p"`, `aspect_ratio: "9:16"`, `duration: "<n>"` (intero 4-9), `generate_audio: true`. Gen character → face+body (+product se in scena)+voice; b-roll product-only → solo product+voice.
- Max 12 reference file per chiamata; voice + eventuale reference video combinati < 15s.
- Conferma costo/gen (`mcp__fal-ai__get_pricing`), poi `mcp__fal-ai__run_model` (sync, video singoli) o `submit_job`+`check_job` (batch). Scarica ogni clip in `$WORK/clips/<name>.mp4`.
- Splitta gli hook reel in 4 hook clip prima dell'assembly.

### Path D — Playwright su higgsfield.ai
Guida `https://higgsfield.ai/ai/video`. Conferma sign-in (stop se appare login), seleziona Seedance 2.0 a 1080p 9:16, incolla ogni prompt, setta la durata intera dalla tabella, attacca i file (yes esplicito per file, mai auto-upload), abilita audio, click generate solo su yes esplicito, scarica in `$WORK/clips/`. Onora il gotcha voice (ri-upload fresco per gen). Splitta i reel come gli altri path.

### Path A — manuale
Dai all'utente ogni prompt con durata, aspect (9:16), resolution (1080p), audio (on), lista attachment esatta. Genera su Higgsfield, droppa le clip in `$WORK/clips/` coi nomi attesi. Poi splitti i reel e giri l'assembly. Unico path senza costo automazione.

### Never-do (ogni path)
Mai generare/click/chiamare modello senza `yes` esplicito per quel batch · mai uploadare file non approvato per nome/path · mai procedere su B se CLI non installata/autenticata, o su C se Fal key non c'è · mai switch silenzioso di path su errore (chiedi retry / fallback Path A / stop) · mai cambiare billing o gen extra non richieste.

---

## Step 5 — GENERAZIONE

Leggi `references/generation-architecture.md` e `consistency-and-assembly.md`. Questo step costruisce e valida prompt+payload; il dispatch reale gira sul path scelto (4.5). Ordine render e riuso:

1. **HOOK come REEL, poi split.** Hook corti → impacchetta ~2 hook in UNA generazione ("hook reel") descritta come 2 scene con taglio netto, secondi totali = somma. 4 hook → 2 reel (ognuno <10s). Dopo render, SPLITTA ogni reel al taglio (rileva il cambio scena con ffmpeg, poi taglia) → 4 hook clip, una per ad.
2. **BODY, un beat per generazione, generato UNA volta, riusato intero.** Ogni beat = sua generazione. Salva `body_01.mp4` (pain), `body_02` (solution), `body_03` (proof), `body_04` (CTA) in `$WORK/clips`. Ogni ad riusa questi file; mai rigenerare un body beat per ad.
3. **B-ROLL, 2 generazioni product-only, generate UNA volta, riusate.** `broll_A.mp4`, `broll_B.mp4`.

COSTRUZIONE PROMPT (ogni prompt), LESS IS MORE. Corti: la scena in una riga + la citazione ESATTA. Lascia che reference images + voice portino il resto.
- Apri con: **"A realistic, authentic UGC ad."** + per gli shot character **"Keep the character consistent with the reference images."** NIENTE blocco wardrobe/hair/lighting, niente pila di aggettivi.
- Body/talking: una riga di scena ("A man in a kitchen, handheld selfie video") + la citazione esatta. Nient'altro.
- Hook: nomina l'hook visivo in poche parole dirette (il dump, lo slam, il lift) + citazione esatta.
- **Quando il prodotto è in scena, dichiara la sua misura reale inline** (es. "a sealed AG1 pouch (360 g, ~19 cm tall)"). Mai inventarla.
- Chiudi con "No on-screen text or captions."
- **MAI scrivere una durata o secondi-per-scena nel testo del prompt.** La durata si setta SOLO dal parametro durata della generazione.
- Multi-scena: descrivi ogni scena ("Scene 1 ... hard cut ... Scene 2 ...") e setta solo i secondi totali.

Attachment per gen: character (hook, body) → stessi byte face+body+voice (+product se in scena); b-roll product-only → solo product+voice. Settaggi: audio ON ogni gen; durata intero 4-9 (mai 10+, mai auto) dalla tabella approvata; 9:16; 1080p.

Costruisci un `payload.json` per generazione sotto `$WORK` e validalo prima di inviare. Per i b-roll product-only setta `"product_only": true`:
```bash
python3 "$SCRIPTS/validate_payload.py" "$WORK/payload_body_01.json"
```
Exit non-zero = NON dispatchare. Dopo ogni render, assert `returned_duration == requested_duration`. Salva ogni clip raw in `$WORK/clips`. Splitta gli hook reel in 4 prima dell'assembly.

---

## Step 6 — ASSEMBLY

Costruisci il manifest, poi monta ogni ad. `stitch.sh` gira UNA VOLTA PER AD:
```bash
python3 "$SCRIPTS/build_manifest.py" "$WORK/spec.json" "$WORK/assembly-manifest.json"
mkdir -p "$WORK/out"
for V in v1 v2 v3 v4; do bash "$SCRIPTS/stitch.sh" "$WORK/assembly-manifest.json" "$V" "$WORK/out/variant_${V}.mp4"; done
```
(`stitch.sh` richiede `ffmpeg`, `ffprobe`, `jq` su PATH.)

Regole assembly (`references/consistency-and-assembly.md`): ogni ad = concatena le clip in ordine — hook, body beat, coi b-roll inseriti ai punti MEZZO scelti. **Il body beat CTA è sempre ultimo, niente dopo.** Ladder b-roll 0/1/2/2, V3 e V4 piazzano i loro 2 b-roll diversamente. Ogni clip porta già il suo audio voce consistente → TIENI l'audio e concatena, NON force-mute, NON spine voce separato. Loudness-normalizza a ~-14 LUFS. Crossfade picture-only corto opzionale ai tagli. Output ogni ad 9:16 1080p MP4, 25-45s.

Il manifest è il contratto (schema dettagliato in `references/consistency-and-assembly.md` e nell'header di `build_manifest.py`). `build_manifest.py` impone fingerprint unici, che ogni timeline chiuda sul CTA, e che nessun b-roll stia dopo la CTA.

---

## Step 7 — OUTPUT + VALIDAZIONE

Consegna il pacchetto sotto `$WORK` (`05_UGC_Prompts/factory/<concept-slug>/`): 4 ad MP4 in `out/` (variant_v1..v4, 9:16 1080p, ~-14 LUFS, ognuno 25-45s di banda diversa); clip raw in `clips/` (body beat condivisi, 4 hook, 2 b-roll); `assembly-manifest.json`, tabella pacing approvata, tabella variazioni, asset input in `inputs/`. Stampa i path assoluti.

Validazione finale (conferma ogni riga):
- [ ] Deliverable sotto `05_UGC_Prompts/factory/<slug>/`: 4 ad in `out/`, clip in `clips/`, `assembly-manifest.json`.
- [ ] 4 asset: face, body, product, voice (≤15s).
- [ ] Stessi byte face+body su ogni gen CHARACTER, mai ri-croppati.
- [ ] Stesso voice reference su ogni gen (b-roll inclusi come voiceover).
- [ ] B-roll PRODUCT-ONLY (no face/body); audio su ogni clip.
- [ ] Ogni gen 4-9s (SOTTO 10), returned==requested per tutte. Nessuna ≥10s.
- [ ] Ogni gen ~3.5 wps (segmenter exit=0).
- [ ] Ogni body beat generato una volta e riusato sui 4 ad; b-roll pool generato una volta.
- [ ] 4 hook UNICI, uno per ad; ladder b-roll 0/1/2/2.
- [ ] OGNI ad chiude su CTA; nessun b-roll dopo la CTA.
- [ ] 4 distinctness_fingerprint unici; V3 e V4 piazzano i b-roll diversamente.
- [ ] Ogni ad 25-45s; i 4 non tutti uguali. Niente clip force-muted; niente spine voce separato.
- [ ] Cut finali 9:16 1080p, ~-14 LUFS, audio continuo.

---

## NEVER DO (regole critiche)

- Mai una generazione ≥10s. Sempre intero 4-9. Contenuto lungo = più generazioni corte concatenate.
- Mai durata auto. Mai paddare per "respiro" (Seedance riempie parlando più lento → trascina). Target ~3.5 wps.
- Mai scrivere durata/secondi nel testo del prompt. Durata solo dal parametro.
- Mai over-scrivere un prompt. Less is more: scena corta + citazione esatta; reference images + voice portano il resto.
- Mai riempire copy di slop ("honestly", "like", "literally", "basically", "genuinely") per fare word count.
- Mai un character in un b-roll. B-roll product-only + voiceover.
- Mai chiudere un ad su un b-roll. Ogni ad chiude sul body beat CTA.
- Mai force-mute una clip né spine voce separato. Ogni clip tiene il suo audio.
- Mai riusare un hook tra ad. 4 ad, 4 hook unici. Mai laddizzare le lunghezze hook.
- Mai rigenerare un body beat o b-roll per ad. Generati una volta, riusati.
- Mai scrapare TikTok per gli hook. Usa hook-library + VOC.
- Mai descrizione fisica lunga del character nel prompt. Di' "keep the character consistent with the reference images". Mai reference-video chaining per l'identità, mai ri-croppare face/body tra gen.
- Mai scrivere output fuori dall'albero `05_UGC_Prompts/factory/`, mai girare gli script con path bare (risolvi `$SCRIPTS`, Step 0.5).
- Mai generare prima del gate Step 4.

---

## Reference + script

- `references/generation-architecture.md` — single source of truth generazioni/clip/split/assembly 4-ad. **LEGGI PER PRIMO.**
- `references/VERIFIED-backend-facts.md` — spec backend locked.
- `references/scripting-frameworks.md` — i framework, scegline uno (Step 2).
- `references/hook-library.md` — hook verbali + visivi, mina in Step 1 e 3 (no scraping).
- `references/seedance-2.0-limits.md` — limiti Seedance 2.0 + motore fast-pace.
- `references/andromeda-variation.md` — modello distinzione 4-ad (hook unici + b-roll ladder, ends-on-CTA).
- `references/consistency-and-assembly.md` — identità, b-roll product-only, audio, regole assembly.
- `scripts/segment_script.py` — pacing+segmentazione ~3.5 wps, gen sub-10s (Step 4).
- `scripts/validate_payload.py` — validazione payload per-gen, sub-10s, b-roll product-only (Step 5).
- `scripts/build_manifest.py` — scrive assembly-manifest.json, impone hook unici + ladder + ends-on-CTA (Step 6).
- `scripts/stitch.sh` — concatena tenendo l'audio, -14 LUFS, crossfade picture opzionale (Step 6).
