---
description: Ad collage editoriale voiceover-first: la voce racconta e ogni parola forte fa POP-IN dell'oggetto che nomina, misurato frame by frame e ri-tempato. Skill nativa 64_vox_ad (SA6).
argument-hint: [prodotto/angolo] — opzionale; la voce la incidi tu una volta e riporti il file
---

# /pm-vox-ad — VOX Ad (collage word-synced)

Esegui la skill nativa **`directives/skills/64_vox_ad/SKILL.md`** (SA6 — Asset Production).

Argomenti: $ARGUMENTS

## Cosa fare
1. Segui `SKILL.md`; la procedura integrale è in `references/procedure.md`. Leggi `vox-style.md` **prima** di scrivere qualunque prompt: il blocco di stile va incollato **byte-identico** in ogni keyframe — è quello l'ancora di consistenza, non un personaggio.
2. **LITERAL-FIRST.** La cosa che la voce nomina È l'immagine. Nessuna metafora astratta salvo richiesta. **È l'inverso di `59_pixar_ad`** (che è emotion-first) — non confonderli.
3. **Legge parola→oggetto:** ogni sostantivo forte, numero, brand e verbo incisivo prende il suo oggetto, che atterra su quella parola. **Una parola forte non mappata = validation failure.** Le parole deboli non prendono niente: è il ritmo.
4. **🚦 GATE 1 (Step 2.5) — transcript.** Le parole esatte che l'utente inciderà, **senza visual**. Approvale **prima** che spenda fatica sulla voce. Chiudi il turno e aspetta.
5. **🚦 GATE 2 (Step 4.5) — beat map + costo.** Beat map, lista keyframe, tabella per-clip span/generazione/scarto/costo, path. **Silenzio = rifiuto.** Poi: **ogni cambiamento dopo il gate annulla l'approvazione**, ogni re-roll vuole il suo sì.
6. **Step 6.5 è ciò che rende l'ad un VOX:** misura l'arrivo reale di ogni elemento frame by frame e ri-tempa in un solo filter graph ffmpeg, così ogni pop cade entro un quarto di secondo dalla parola. **Non dichiarare il sync riuscito senza aver girato la misurazione.**
7. Keyframe **sempre come image reference, mai come start image**. Camera bloccata. **Mai musica.** Barre cieche sulle card, mai lettering. Packaging del prodotto mai ridisegnato.

Richiede ffmpeg/ffprobe + whisper. Path A/B/C — **non esiste Path K**.

Output: `21_Vox_Ads/<concept>/`. A fine ad **offri le caption** (`/pm-captions`): il transcript è su disco, escono allineate parola per parola.
