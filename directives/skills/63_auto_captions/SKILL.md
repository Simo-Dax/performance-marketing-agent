---
name: 63_auto_captions
description: Brucia caption in stile locked su qualsiasi video finito. Se lo script dell'ad è su disco fa force-align (whisper dà i tempi, lo script dà le parole) così le caption sono il copy esatto. Scrive sempre un file _captioned separato. SA6.
---

# 63 — Auto Captions

Brucia le caption su un video **finito**, in uno stile bloccato. Funziona sull'output di ogni skill video (25, 56, 57, 58, 59, 60, 61, 62) **e** su qualsiasi video caricato da fuori.

**Lo stile non è regolabile per run.** I valori sono fissi in `references/caption-style.md` — tarati su footage vero. Leggi quel file prima di toccare qualunque cosa.

**Output:** `<nome>_captioned.mp4` accanto al video sorgente (o in `out/` se esiste). **Il master pulito non viene mai sovrascritto.**

---

## Le regole in una schermata

- **2-3 parole per card**; 1 o 4 solo dove si leggono davvero meglio
- **Sempre una riga.** Mai a capo — il cap è sui **pixel renderizzati**, non sui caratteri
- Taglia sulle pause vere e sulla punteggiatura; **mai chiudere una card su una parola legante** ("the", "than", "your", "if"…)
- **Niente punti, niente virgole.** Da nessuna parte
- **Maiuscola solo sulla primissima parola del video**
- I **nomi propri tengono le maiuscole** e non si spezzano mai su due card
- Bianco, ombra sfocata morbida, **nessun contorno duro**, 58px, baseline y=1275 (scalata sull'altezza frame per 4K e altri formati)

## Il pezzo che conta: il force-align

Il riconoscimento vocale è **affidabile su QUANDO** una parola è stata detta e solo **approssimativo su QUALE** parola fosse.

Quando lo script originale è su disco (`transcript.json` / `timing.json`, auto-scoperti da `./`, `../`, `../audio/`), la skill **allinea**: whisper serve solo per i tempi, ogni parola viene dallo script. Risultato: le caption sono il copy esatto invece di ereditare gli errori di trascrizione.

Su una raccolta reale, la sola trascrizione produceva "row ass" al posto di ROAS in tre ad e "cloud code" per Claude Code in altre tre. Nessuna di quelle stringhe esisteva negli script.

Senza script su disco → ripiega sulla sola trascrizione, e lo dice.

## Vocabolario di brand (nostro, non upstream)

Questo agente è **brand-agnostic**: nessun nome di brand è cablato nel motore. Per far sì che il nome del cliente esca con le maiuscole giuste e non si spezzi mai su due card, crea `context/brand/caption_vocab.json`:

```json
{
  "brand_names":  ["Acme Coffee Co"],
  "proper_nouns": ["Nespresso", "Arabica"],
  "fixes":        {"acme coffee": "Acme Coffee"}
}
```

Viene caricato in automatico se esiste (oppure `--brand-vocab PATH`). File assente = non è un errore: resta la lista generica (AI, ROAS, ChatGPT, Canva, Meta, DNA…).

---

## Procedura

Dettaglio completo in `references/procedure.md`. In sintesi:

```bash
SCRIPTS="directives/skills/63_auto_captions/scripts"
```

**1. Dry-run sempre per primo.**
```bash
python3 "$SCRIPTS/autocaption.py" <video> --dry-run
```
Stampa ogni card con timing e conteggio parole, più l'audit. Non renderizza nulla. Leggi le card contro quello che l'ad dice davvero — costa niente e intercetta i problemi prima di un encode lungo (un 4K da un minuto ci mette un paio di minuti a bruciare).

**2. Brucia.**
```bash
python3 "$SCRIPTS/autocaption.py" <video> [<video> ...]
```
Scrive `<nome>_captioned.mp4` + `<nome>.captions.json` (script, word timing, card, audit). L'audio è **stream-copiato**: loudness e mix restano intatti.

**3. Riporta l'audit con i numeri, non a sensazione.**
Ogni run stampa: numero di card, **% nella banda 2-3**, eventuali card a due righe, eventuale punteggiatura, e se le caption **combaciano con lo script parola per parola**.

Sano = ~90%+ nella banda 2-3, zero card a due righe, script match esatto. Qualsiasi cosa diversa da `two-row: none`, `punctuation: none`, `script match: True` **è un difetto**: indaga prima di consegnare.

Se compare una riga `FONT:`, il font bloccato non era disponibile su questa macchina e ha renderizzato altro. **Passa quella riga all'utente** — un font sostituito non esce mai in silenzio.

**4. Vince la risoluzione più alta.** Se esistono più cut della stessa ad (1080 e 4K, o un upscale), caption sul **più grande**. Prima di fidarti che l'upscale sia lo stesso footage, campiona 3-4 frame e confronta: differenza media in unità basse per canale = stesso cut, i timing tengono. Molto più alta = render diverso, vuole il suo allineamento.

**Iterare senza ri-trascrivere:** `<nome>.captions.json` conserva i word timing. Dopo una modifica a `caption_lib.py`, ricostruisci da lì invece di ri-trascrivere. La trascrizione è la parte lenta.

---

## MAI

- Mai sovrascrivere il master pulito — le caption sono sempre un file `_captioned` separato
- Mai ri-timare o ri-encodare l'audio: è stream-copiato
- Mai lasciare che una card vada a capo. È una regola strutturale dura, non una preferenza
- Mai rimettere punti o virgole, mai maiuscole oltre la prima parola del video e i nomi propri veri
- Mai spezzare il nome di un brand su due card
- Mai dichiarare che le caption combaciano con lo script senza aver girato l'audit
- Mai sostituire il font o spostare la baseline in silenzio: quei valori sono bloccati, e una sostituzione si dichiara ad alta voce
- **Mai mettere le caption su un video che l'utente non ha chiesto di captionare.** Si offre sempre, non si assume mai

## Requisiti

`ffmpeg` e `ffprobe` nel PATH, Pillow, faster-whisper. Lo script si ri-esegue da solo nel venv whisper condiviso `~/.cache/pm-agent/whisper-venv` (lo stesso che costruiscono già le skill video) e stampa il fix in una riga se manca.
