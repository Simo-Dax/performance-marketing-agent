# 03 — Voice Editor & Self-Check (brand-cliente)

## Obiettivo
Passaggio finale obbligatorio su **ogni asset testuale**: elimina le tracce di scrittura AI-generated e allinea il copy alla **Tone of Voice del brand-cliente**. Agnostico rispetto al brand — si adatta a qualsiasi cliente leggendo i suoi file di voce.

## Quando si usa
**Dopo ogni draft di copy di campagna** — ad copy (SA7), landing page, piano editoriale, content plan. Obbligatorio, non opzionale. Tutto il copy passa da qui prima della delivery.

## Input
- Il draft appena scritto
- `context/brand/anti_ai_writing_style.md` — regole anti-AI agnostiche (confronto riga per riga)
- `intermediate/tone_of_voice_campaign.md` (da `32_brand_strategy`) **oppure** `context/brand/tone_of_voice.md` — ToV specifica del brand-cliente
- Brand DNA (`02_Brand_DNA/`) se presente — per `voice.avoid` e vocabolario

---

## Processo di revisione

### Pass 1 — Detector AI-speak
Applica integralmente `context/brand/anti_ai_writing_style.md`: frasi vietate, vocabolario gonfio, pattern strutturali (ritmo a metronomo, rule-of-three meccanica, parallelismi negativi, em-dash, paragrafi riassuntivi, conclusioni che riformulano l'intro). Cerca e riscrivi ogni occorrenza.

### Pass 2 — Allineamento alla ToV del brand-cliente
Confronta punto per punto con la ToV del brand (`tone_of_voice_campaign.md` o `tone_of_voice.md`):

| Check | Domanda | Se NO → |
|-------|---------|---------|
| Personalità | Suona come il brand, non generico? | Riscrivi con la personalità definita |
| Point of view | Riflette il sistema di credenze del brand? | Aggancia al POV |
| Nemico del brand | Combatte il nemico giusto (non colpevolizza il cliente)? | Riorienta verso il nemico esterno |
| Vocabolario | Usa il vocabolario core del brand? | Sostituisci con i termini del brand |
| Diretto | Va al punto nelle prime 2 righe? | Riscrivi l'hook |
| Specifico | Numeri, nomi, dettagli concreti? | Aggiungi concretezza |
| Azione | Il lettore sa cosa fare dopo? | Aggiungi CTA/takeaway |
| No hype | Niente da "guru"/pitch infoprodotto? | Elimina o riformula |
| Paragrafi | Qualche paragrafo > 4 righe? | Spezza |
| Frasi | Qualche frase > 25 parole? | Spezza |

### Pass 3 — Vincoli del brand
- Nessuna parola/claim dalla `voice.avoid` del Brand DNA / ToV.
- **Terminologia tecnica non tradotta** (ROAS, CPA, MER, CTR, AOV, hook rate).
- Non cambiare la **sostanza strategica**, solo forma e tono.

### Pass 4 — Ritmo e leggibilità
- Leggi ad alta voce (mentalmente). Dove inciampi, riscrivi.
- Alternanza: frase lunga → corta → domanda → affermazione.
- Grassetti con parsimonia (1-2 per paragrafo max). Emoji max 2-3 se il brand le usa.

---

## Output

Modifica il draft direttamente e segnala:

```
## Voice edit completato — Brand: [nome]

### Modifiche apportate:
- [X] Rimossa AI-speak: "[originale]" → "[corretto]"
- [X] Allineato al nemico del brand in sezione [N]
- [X] Sostituito vocabolario generico con termini brand
- [X] Spezzato paragrafo/frase lunghi

### Punteggio allineamento ToV: [X]/10
- [cosa funziona, cosa migliorare rispetto alla ToV del brand]
```

## Regole

1. **Non opzionale.** Ogni copy passa da qui prima di essere presentato.
2. **Agnostico.** Allinea SEMPRE alla ToV del brand-cliente corrente, mai a una voce personale fissa.
3. **Preferisci tagliare che aggiungere.** Più corto e autentico batte lungo e generico.
4. **Non cambiare la sostanza strategica** — solo forma e tono.
5. **Test finale:** se non puoi dire con certezza se l'ha scritto un umano esperto del brand o un AI, non è pronto.

---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
