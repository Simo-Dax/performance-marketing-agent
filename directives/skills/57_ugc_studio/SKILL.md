# SA6 — UGC Studio (format-first, montaggio da editor vero)

**Agente:** SA6 (Asset Production)
**Output:** `05_UGC_Prompts/studio/<order-slug>/` — un sottofolder per ad (`out/<ad_id>.mp4` + tutto il pacchetto)
**Modello:** Seedance 2.0 (9:16, 1080p) — model-agnostic, vedi `execution/tools.md`
**Reference (leggile PRIMA di agire — vincono su questo file in caso di conflitto):**
`references/render-laws.md` (la costituzione: 3 lane, leggi di generazione, **EDIT GRAMMAR**, lane green-screen, voce/audio, hook, pacing) · `references/pipeline-contracts.md` (4 contratti JSON + argv canonico) · `references/voice-and-parallel.md` (fisica del dedup `_sfx`) · `references/variant-fanout.md` (1 script → fino a 4 timeline) · `references/scene-bank-{testimonial,before-after,unboxing,direct-to-camera}.md` (i 4 format bank: shell, verdetti, tabelle di generazione, rhythm card, liste di intake)
**Script:** `scripts/` (10: segment_script, validate_payload, make_voice_cuts, render_stills, render_parallel, frame_check, whisper_cut, composite, build_manifest, stitch). Richiede `ffmpeg`/`ffprobe`.

---

## Il modello in una riga

Il prodotto di questa skill è il suo **FORMAT BANK**: shell recreation-grade estratti da **ad UGC realmente vincenti**, con rhythm card misurate. Un ordine = scegli i formati, riempi gli shell con la verità del brand, generi clip da 4-9s, le **tagli come tagliano i winner** (l'edit grammar), assembli.

> **Perché è diverso da `25_ugc_prompt`.** La factory (25) genera 4 ad distinti da hook mining + script framework: parte dalla pagina bianca. Lo **studio (57) parte da formati provati** e ci mette dentro il brand. È lo stesso salto che `24_static_ads` ha fatto per le statiche (da template → rebrand di winner reali). **57 è il default per gli UGC video**; 25 resta l'alternativa quando serve il fan-out Andromeda a 4 varianti da uno script unico.

**Regole hard che non si piegano mai:**
1. Ogni generazione è di **4-9 secondi interi**. Una singola generazione da 10s+ è **vietata** (verificato: resa pessima). Ad più lunghi = più generazioni, affettate e interlacciate.
2. **Una generazione non è mai un'inquadratura della timeline** — è il montaggio che la affetta (`render-laws` §3).
3. Niente renderizza senza un **sì fresco** dell'utente sul batch prezzato. Ogni re-roll richiede un sì nuovo E un voice cut nuovo.
4. **Nessun testo reale viene mai renderizzato o impresso** — le caption escono come `captions.txt`.
5. Beat di prova e di etichetta si costruiscono dalle **foto REALI** dell'utente (still-insert), mai inventati. Niente foto → still-insert da ciò che esiste, oppure il beat si taglia.
6. La musica è lato editing. I formati silenziosi consegnano picture pulita.

---

## Step 0 — Cartella + risoluzione script + auto-discovery

```bash
WORKDIR="$PWD"
ORDER_SLUG="<slug-ordine>"
WORK="$WORKDIR/05_UGC_Prompts/studio/$ORDER_SLUG"
mkdir -p "$WORK"
# Risolvi $SCRIPTS cercando verso l'alto (stessa convenzione di 25_ugc_prompt)
ROOT="$PWD"; while [ "$ROOT" != "/" ] && [ ! -d "$ROOT/directives/skills/57_ugc_studio/scripts" ]; do ROOT="$(dirname "$ROOT")"; done
SCRIPTS="$ROOT/directives/skills/57_ugc_studio/scripts"
ls "$SCRIPTS"   # devono esserci 10 script
```

Un ordine = una cartella; ogni ad ha il suo sottofolder col nome `ad_id`. Scrivi SOLO sotto `studio/` — le altre sottocartelle di `05_UGC_Prompts/` appartengono a `25_ugc_prompt` e non si toccano mai.

**Auto-discovery** (riporta cosa hai trovato, chiedi solo ciò che manca):
```bash
ls -t "$WORKDIR/11_Characters/"* 2>/dev/null | head -5          # face/body reference
ls -t "$WORKDIR/02_Brand_DNA/"*.html "$WORKDIR/02_Brand_DNA/"*.md 2>/dev/null | head -2
ls -t "$WORKDIR/01_VOC_Research/"*.html "$WORKDIR/01_VOC_Research/"*.md 2>/dev/null | head -2
ls -t "$WORKDIR/15_Video_Scripts/"script-*.md 2>/dev/null | head -3   # script approvati da 55
ls -t "$WORKDIR/03_Ad_Spy/"*-video/video-teardown-*.json 2>/dev/null | head -2  # wps MISURATO da 52
```
I teardown di `52_ad_spy_video` con **wps misurato battono i default di formato** (stesso principio di `55_video_script`). Uno script approvato da `55_video_script` può essere l'input di questo studio.

---

## Step 1 — Intake (una volta per ordine)

- **UNA** face reference + **UNA** body reference (foto reale della persona/creator). Una body reference **per ogni outfit distinto** che comparirà — niente seconda ref, niente secondo outfit.
- **Foto prodotto**: l'eroe, più la sua foto reale per **ogni variante** che appare a schermo, più ogni faccia stampata del packaging per gli unboxing, più le foto stato-aperto/demo/consumato per i beat della manipulation ladder (vedi la lista di intake di ogni bank — quelle dei formati ordinati sono legge).
- **Dimensioni reali del prodotto** (vanno dichiarate inline nei prompt).
- **Voice clip ≤15s** — obbligatorio solo se l'ordine contiene ad narrati. Verifica con `ffprobe`; >15s = chiedi una clip più corta (o offri di tagliarla, l'utente approva).
- Nicchia, claim sanzionate, la **vera** storia di prova, l'offerta reale (se c'è una chiusura in offerta).
- Prodotti app/sito: screen recording + screenshot per la lane green-screen.

Foto mancante → quel beat diventa still-insert da ciò che esiste, oppure si taglia. **Mai inventato.**

---

## Step 2 — Scelta formato + ordine

Raccomanda fino a 3 formati da VOC, tipo prodotto e obiettivo funnel:
- **cold start** → Direct-to-Camera Narrative
- **trasformazione visibile** → Before & After
- **consideration / prova sociale** → Testimonial
- **offerta / lancio** → Unboxing

Presenta il menu dei 4 formati (job, durata, requisito volto — dagli header dei bank). L'utente ordina qualsiasi mix e quantità ("2 testimonial + 1 unboxing"). Opzionale per ordini Narrative/Testimonial: il **VARIANT FAN-OUT** (uno script → fino a 4 timeline distinte, `references/variant-fanout.md`).

---

## Step 3 — Script

Per ogni ad ordinato: riempi gli shell del formato (fill-or-synthesize; registra `source_shell` per scena; **mai copiare verbatim una sequenza sorgente**; claim/caption/brand sono slot da scambiare). Hook dalla tabella evidenze (`render-laws` §6): ≥2 hook da famiglie forti, ≤1 da famiglia debole, ancore VOC verbatim quando la ricerca esiste. Passaggio completo di voce naturale (`49_anti_ai_slop` + `context/brand/anti_ai_writing_style.md`). Punta alla banda wps del formato.

## Step 4 — 🚦 GATE 1: IL TRANSCRIPT

Presenta le **parole parlate complete** di ogni ad nell'ordine di riproduzione (+ il testo sidecar delle caption per i formati silenziosi). Prima fai il self-check silenzioso con kill floor (riscrivi ciò che fallisce **prima** di mostrarlo). **FERMA IL TURNO.** Le parole si bloccano prima che esista un solo prompt o una sola durata.

## Step 5 — Piano + 🚦 GATE 2: COSTO + CUT MAP

1. Segmenta: `python3 $SCRIPTS/segment_script.py transcript.txt --format <formato> --out render_plan.skeleton.json` (aggiungi `--wps <misurato>` quando esistono dati di teardown).
2. Scrivi `render_plan.json` per `pipeline-contracts.md` §1: handle degli input (prefissati `face*`, `body*`, `product*`), voci tipizzate, mappa `sub_shots` pianificata per ogni gen multi-shot, prompt nella HOUSE PROMPT SHAPE con markup `[0-Xs] ... HARD CUT [X-Ys]`, **esattamente un** `is_identity_checkpoint`, la voce di chiusura tipizzata per ultima (`role: "close"`), voci still per ogni beat con verdetto RED, voci footage/composite per la lane green.
3. Valida: `python3 $SCRIPTS/validate_payload.py render_plan.json` — deve **PASSARE**.
4. Voice cut: `python3 $SCRIPTS/make_voice_cuts.py render_plan.json "$WORK" voice_cuts/` (solo path Higgsfield; il Path C si salta da solo).
5. Bozza dell'EDL (`edl.json` per contracts §3) — **questa È la CUT MAP**: ordine base, posizioni degli overlay con ancore di parola, ritorni sulla spine, target di ritmo dalla rhythm card del bank.
6. **Preflight matting** (solo se è stata ordinata la lane green): Path B/D — conferma che il connettore Higgsfield sia raggiungibile e fai una chiamata di saldo; Path A — conferma che l'utente possa usare il background remover della web UI; Path C — matting **NON disponibile**, la lane ricade su chromakey/PiP e il piano lo dichiara. Mai prezzare un matting non confermato raggiungibile.
7. **Presenta il GATE 2** — una tabella per ad: ogni gen (id, secondi, unità di path), ogni still, crediti matting, il totale — **E la cut map** (numero di inquadrature, shot mediano/più lungo, posizioni degli insert, ritorni sulla spine) così l'utente approva **il ritmo che sta comprando**, non solo il prezzo. Scelta path A/B/C/D. **FERMA IL TURNO.**

> **LEGGE DI RI-APPROVAZIONE:** qualsiasi modifica al piano dopo il gate (un re-roll, una gen aggiunta, una durata cambiata) ri-presenta le righe di tabella interessate per un sì fresco.

## Step 6 — Prima le still

Tutte le still-insert renderizzano **economiche** e ottengono l'approvazione **PRIMA** di qualsiasi credito video:
1. `python3 $SCRIPTS/render_stills.py render_plan.json "$WORK" stills/` — scrive i prompt still 2K (dalle foto reali) + `stills/stills_plan.json` + la checklist.
2. Dispatcha ogni still sul path scelto (allega la foto sorgente come reference immagine). Salva come `stills/<still_id>.png`.
3. L'utente approva ogni still. Le still animate poi renderizzano image-to-video col prompt **SOLO-MOVIMENTO** (`prompts/still_<id>_motion.txt`); le still statiche si convertono al composite (`bash $SCRIPTS/composite.sh still stills/<id>.png stills/<id>.mp4 2`).
4. Ri-esegui `render_stills.py` per ribaltare gli stati a *rendered*.

## Step 7 — Generazione

**Prima l'identity checkpoint, DA SOLO:**
```
python3 $SCRIPTS/render_parallel.py render_plan.json "$WORK" voice_cuts/ gens/ <checkpoint_gen_id>
```
(Path A/D: dispatcha manualmente/via Playwright solo quella gen.) Fai il frame-check — deve contenere il **volto pulito, nudo, non ostruito**. L'utente approva volto/voce/vibe. **Sì fresco, poi il resto del batch in parallelo:**
```
python3 $SCRIPTS/render_parallel.py render_plan.json "$WORK" voice_cuts/ gens/
```
(submit-all → poll → download → retry automatico con voice cut fresco su fallimento o avvelenamento `_sfx`; i job falliti non costano).

**IL GREEN GATE** (primo render green-screen, prima del batch green):
`bash $SCRIPTS/composite.sh sample-green gens/<gs_gen>.mp4` → **SATURATED** → fast path chromakey; **MUTED** → matting (B/D, 1 credito/clip) o PiP — **MAI allargare i raggi di key**. Un re-roll con la formulazione sulla saturazione è lecito (sì fresco + cut fresco).

Ogni re-roll ovunque: sì fresco dell'utente + voice cut fresco (un fingerprint vecchio è bruciato, vedi `voice-and-parallel.md`) + **sposta prima il file rifiutato** (`mkdir -p gens/rejected && mv gens/<gen_id>.mp4 gens/rejected/`) — il dispatcher è idempotente e **salta** ogni gen il cui mp4 valido esiste già (è anche ciò che fa renderizzare una sola volta i body condivisi nel fan-out, e permette a un batch crashato di riprendere gratis).

## Step 8 — Taglio + verifica (gratis)

1. `bash $SCRIPTS/frame_check.sh gens/ frames/` — **LEGGI ogni contact sheet**: identità tenuta, azioni renderizzate, nessun testo, scala prodotto sensata, scene ladder che regge, uniformità del green (lane green).
2. `python3 $SCRIPTS/whisper_cut.py render_plan.json gens/ clips/` — clip accurate alla parola + `clips/cut_report.json`. Rivedi: match ratio (<75% = **ASCOLTA** prima di assemblare), colonna reconcile (sub-shot MISSING = recupero nel montaggio: affetta, punch-in in crop, o overlay — **mai** un re-render automatico).
3. I problemi di **timing** si risolvono nel montaggio. Solo il **contenuto** sbagliato (parole impastate, identità rotta, azione deformata) giustifica un re-render PROPOSTO — decide l'utente, sì fresco, cut fresco.

## Step 9 — Composite + assemblaggio

1. Lane green/app: `composite.sh chromakey|matting-key|pip|fullframe ...` secondo il routing del green gate (contracts §5 argv).
2. Finalizza `edl.json` sulle durate reali delle clip: slice della spine non adiacenti, overlay sugli onset di parola (ritorni a metà frase per l'edit grammar), trim interni per i jump cut, la chiusura tipizzata per ultima e **mai coperta**.
3. `python3 $SCRIPTS/build_manifest.py edl.json render_plan.json clips/cut_report.json --out manifest.json` — i fallimenti strutturali bloccano; un **FAIL di ritmo significa ri-montare** (aggiungi overlay/trim), mai falsare i target.
4. `bash $SCRIPTS/stitch.sh manifest.json out/<ad_id>.mp4` — **rifiuta** su FAIL di ritmo; conforma 1080x1920@30; loudnorm −14 LUFS sui narrati, saltato sui silenziosi.
5. **Verifica:** trascrivi l'ad NARRATO finito e diffalo contro il transcript approvato. Gli ad SILENZIOSI si verificano col frame-check contro il piano + `captions.txt`. Guarda le giunzioni a ogni overlay.

## Step 10 — Consegna

Pacchetto per ad sotto la cartella ordine: `out/<ad_id>.mp4`, `gens/`, `stills/`, `footage/`, `clips/` (+ `cut_report.json`), `frames/`, `prompts/`, `voice_cuts/`, `captions.txt` (formati silenziosi/caption), `render_plan.json`, `edl.json`, `manifest.json`, e la tabella di rendiconto finale (quotato vs speso, per unità di path).

Stampa i path **ASSOLUTI** di ogni deliverable. Ricorda all'utente: **il loop di montaggio è gratis** — ri-taglia, riordina, scambia overlay, stringi il pacing, zero crediti; costano solo le generazioni nuove. Offri il variant fan-out se ha ordinato un ad solo e converte.

---

## I quattro percorsi di generazione

- **Path A — incolla manuale:** stampa prompt + lista allegati + durata di ogni gen; l'utente incolla nella web UI (Seedance 2.0, 9:16, 1080p), allega immagini + **il voice cut WAV DI QUELLA GEN**, scarica in `gens/<gen_id>.mp4`.
- **Path B — Higgsfield CLI:** `render_parallel.py` guida `higgsfield generate` end-to-end (submit/poll/download/retry). Richiede la CLI autenticata.
- **Path C — fal.ai:** verifica prima la key (`/pm-setup-fal-ai`, hard gate). Imposta `"backend": "fal"` nel piano (i voice cut si saltano da soli; la voce unica si carica una volta — nessun bug `_sfx` su fal). **Niente matting Higgsfield su questo path** — la lane green va su chromakey/PiP.
- **Path D — Playwright web UI:** guida la web app con `mcp__playwright` (login → Seedance 2.0 → per gen: prompt, allegati, voice cut, durata → coda → download). Può guidare anche il background remover web per il matting.

Su ogni path: una gen = il **suo** voice cut con fingerprint unico (Higgsfield), il green gate prima dei batch green, integrity-check di ogni download (size + ffprobe).

---

## Regole critiche

| Regola | Dettaglio |
|---|---|
| **4-9s interi, mai 10s+** | Una generazione lunga rende male (verificato). Ad lunghi = più gen affettate. |
| **La gen non è l'inquadratura** | È il montaggio che affetta. L'ad finito taglia ogni 1-3s mentre le gen sono 4-9s: è l'edit grammar (`render-laws` §3) a farlo sembrare montato da un editor vero. |
| **Due gate umani** | GATE 1 parole (transcript), GATE 2 costo **+ cut map**. Più un sì fresco prima di ogni credito e a ogni re-roll. |
| **Mai testo renderizzato** | Le caption escono in `captions.txt`, mai impresse nel video. |
| **Prova solo da foto reali** | Beat di prova/etichetta da still-insert costruite sulle foto vere. Niente foto → still da ciò che c'è, o il beat si taglia. Mai inventare. |
| **Il ritmo è legge** | `stitch.sh` **rifiuta** una timeline che fallisce la rhythm card. Si ri-monta, non si falsano i target. |
| **Voice cut fresco a ogni re-roll** | Un fingerprint vecchio è bruciato (`voice-and-parallel.md`). |
| **Il montaggio è gratis** | Solo le generazioni costano. Ri-tagliare, riordinare, cambiare overlay: zero crediti. |
| **Non tocca `25_ugc_prompt`** | Scrive solo sotto `05_UGC_Prompts/studio/`. Le altre sottocartelle sono della factory. |
