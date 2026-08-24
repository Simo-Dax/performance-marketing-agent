---
name: 64_vox_ad
description: Ad collage editoriale voiceover-first. La voce racconta, e ogni parola forte fa POP-IN dell'oggetto che nomina — misurato frame by frame e ri-tempato, non a occhio. Literal-first, l'opposto di 59_pixar_ad. SA6.
---

# 64 — VOX Ad (collage editoriale word-synced)

Un voiceover racconta, e **sullo schermo appare esattamente la cosa che la voce nomina**, nell'istante in cui la nomina. Ritagli di carta, texture halftone, ombre vere. Stile zine, non CGI.

**Output:** `21_Vox_Ads/<concept>/` — ad montato word-synced + clip raw + keyframe + beat map + report timing/arrivi + manifest.

---

## La legge centrale: LITERAL-FIRST

La voce dice *strumento* → entra uno strumento. Dice *recensione* → una card 5 stelle. Dice *legge* → una lente d'ingrandimento.

**È l'esatto inverso di `59_pixar_ad`.** Pixar dipinge l'emozione; qui **la cosa nominata È l'immagine**. Niente metafore astratte, salvo richiesta esplicita.

**Legge parola→oggetto:** ogni sostantivo forte, numero, nome di brand e verbo incisivo del transcript ha il **suo** oggetto, che atterra **su quella parola**. La beat map è una tabella: parole dette → oggetto → tempo target. **Una parola forte non mappata è un errore di validazione.** Le parole deboli ("di", "il", "quindi") non prendono niente — è quello il ritmo.

**Oggetti familiari soltanto:** cose che si riconoscono in mezzo secondo — loghi veri, card di feed, calendari, monete, fiamme, trofei, frecce, badge di notifica, cestini, lenti, bacheche con puntine, fumetti, persone ritagliate in halftone. **Ogni faccia di card porta barre cieche, mai lettering.**

**Il prodotto È l'oggetto.** Quando la voce nomina il prodotto appare **il prodotto**, mai un surrogato. Prodotto fisico = **sticker fotografico pixel-fedele** col bordo di carta strappato, generato allegando la **foto reale** come image reference: packaging **mai** ri-lettereggiato, ricolorato, ridisegnato o ri-composto. Entra alla svolta e possiede l'ultimo frame.

---

## Il modello in un respiro

- **Un voiceover continuo** (default ~25s, l'utente sceglie 10-40 all'intake). L'utente lo incide **una volta** (ElevenLabs o voce propria) e riporta il file. La voce viene **stesa sopra** in assembly e **non viene mai alterata**.
- **Il look è UN blocco di stile bloccato** — collage di carta tagliata a mano, bordi strappati, halftone, ombre vere, opaco, **NON CGI** — incollato **byte-identico** in ogni prompt di keyframe, con palette dai codici hex del Brand DNA. **È quel blocco, non un personaggio, l'ancora di consistenza** (`references/vox-style.md`).
- **Una clip per gruppo di frase.** I confini vengono dalla voce reale (allineamento faster-whisper).
- Ogni clip ha **un keyframe 2K approvato** (Nano Banana 2) e renderizza su Seedance 2.5 **da sfondo vuoto DENTRO quel keyframe**, 9:16 1080p, 4-9s interi.
- **Il keyframe si allega come IMAGE REFERENCE, mai come start image** — da start image la clip aprirebbe sul poster già finito.
- **Camera statica e bloccata in ogni clip.** L'energia sono i pop-in: rimbalzi, slam, timbri, tratti disegnati, schizzi di frammenti di carta. Ogni prompt video porta "Nothing moves position after it lands."
- **Generazione: clip 1 come checkpoint, poi tutte le altre in PARALLELO** — ogni clip dipende solo dal proprio keyframe, mai da un'altra clip.
- **MAI musica.** L'ad finito è il voiceover intatto più il foley di carta delle clip stesse, ri-tempato sotto.

## Il pezzo che rende VOX un VOX (Step 6.5)

Dopo il render la skill **misura l'arrivo reale di ogni elemento frame by frame** (`measure_pops.py`), poi **ri-tempa il footage in un unico filter graph ffmpeg** così ogni pop cade **entro un quarto di secondo** dalla parola detta.

Non si guarda a occhio e non si spera: si misura, si corregge, si verifica. Senza questo step è un collage carino, non un VOX.

---

## I due gate — fermate dure

| Gate | Cosa | Costo |
|---|---|---|
| **GATE 1 — TRANSCRIPT** (Step 2.5) | Le parole esatte che l'utente andrà a incidere. **Nessun visual.** Approvate **prima** che spenda fatica sulla voce. | Gratis |
| **GATE 2 — BEAT MAP + COSTO** (Step 4.5) | Beat map parola→oggetto, lista keyframe, tabella per-clip span/generazione/scarto/costo, e il path. | Prima di ogni spesa |

**Silenzio = rifiuto.** Chiudi il turno e aspetta.

> **LEGGE DELLA RI-APPROVAZIONE.** Qualsiasi cambiamento dopo GATE 2 — un oggetto, uno split di clip, una durata, il path — **annulla l'approvazione**. Ogni re-roll è una nuova spesa e vuole il suo sì.

---

## Procedura

Integrale in `references/procedure.md`. Sequenza: 0.5 setup → 0 intake → 1 angolo + palette lock → 2 script → **🚦GATE 1** → 3 analisi audio → 4 beat map → **🚦GATE 2** → 5 keyframe (wave A, tutti approvati prima di qualsiasi video) → 5.5 prompt clip → 6 generazione (clip 1, poi parallelo) → **6.5 sync misurato** → 7 delivery + checklist.

**Reference:** `vox-style.md` (blocco stile bloccato) · `vox-scripting.md` (scrittura a sostantivi concreti) · `generation-architecture.md` · `beat-bank-*.md` (banchi di beat da ad reali smontate).
**Script:** `align_vo.py` · `segment_beats.py` · `build_sync.py` · `measure_pops.py` · `validate_vox_prompt.py` · `frame_check.sh`.
**Motori condivisi:** `../_shared/brand_brain.md` · `voc_brand_reader.md` · `hook_anatomy.md` · `visual_invention.md` · `natural_voice.md` · `path_b_cli_implementation.md`.

**Path:** A (incolli tu) · B (Higgsfield CLI) · C (fal.ai). **Non esiste Path K** — KIE è mappato non cablato (`execution/kie_api_map.md`).

## MAI

- Mai generare senza un sì fresco ed esplicito — keyframe, clip 1, wave parallela, **ogni** re-roll
- Mai allegare un keyframe come start image, mai allegare un video come reference
- Mai musica
- Mai lettering sulle facce delle card: barre cieche
- Mai ri-lettereggiare o ridisegnare il packaging del prodotto
- Mai lasciare una parola forte senza oggetto mappato
- Mai muovere un elemento dopo che è atterrato
- Mai dichiarare il sync riuscito senza aver girato la misurazione

Richiede ffmpeg/ffprobe + whisper (venv condiviso `~/.cache/pm-agent/whisper-venv`).

A ad finita, **offri le caption** (`/pm-captions`): il transcript è su disco, quindi escono allineate parola per parola.
