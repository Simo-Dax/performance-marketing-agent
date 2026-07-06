# Motore condiviso — Framework di script (video parlato + primary text)

Riferimento condiviso usato da `55_video_script` (e riusabile da `25_ugc_prompt` in futuro). Scheletro direct-response, 12 framework video nominati, matematica del pacing. Serve SIA script video parlati SIA primary text scritto per Meta, selezionati con un parametro `mode` obbligatorio.

## S.0 — Parametri OBBLIGATORI, fermati se assenti

Chi chiama questo modulo deve passare ENTRAMBI. Se manca uno, FERMATI e chiedilo prima di scrivere una riga. Mai assumere un default.

- `mode`: uno tra `self-voice` (UGC/founder a camera) | `external-VO` (voiceover continuo, no dialogo) | `two-speaker-turns` (dialogo a due) | `static-primary-text` (copy scritto)
- `wps` (parole al secondo, solo modalità parlate): vedi tabella costanti in `55_video_script.md` Step 2.

Perché il fermo conta: uno script scritto al wps sbagliato rompe silenziosamente il budget di lunghezza della skill di produzione a valle (uno script 30s scritto a 3,5 wps quando la produzione pensa a 2,5 wps porta il 40% di parole in più del dovuto).

---

## S.1 — Lo scheletro universale (tutte le modalità)

La struttura interna è sempre le stesse 5 beat. I beat non sono MAI etichettati nell'output; chi legge/ascolta vive solo il flusso.

1. **Hook.** La prima riga (parlato: i primi 3 secondi; scritto: dentro i primi 125 caratteri). Parla direttamente alla persona target al suo stadio awareness e layer di tensione. Meccanica da `headline_frameworks.md` H.4.
2. **Body.** Uno di tre motori, calibrato sull'awareness (`awareness_tension_funnel.md`):
   - agitazione (Problem-Aware): rispecchia il dolore, twist, allevia
   - meccanismo (Solution-Aware): perché questo funziona quando gli altri no
   - storia (Unaware o identity play): una narrazione concreta che atterra il problema
3. **Mid-CTA.** Un puntatore naturale incorporato, mai una richiesta dura ("è lì che ho trovato...", "è nel link sotto"). Saltalo del tutto sotto i 20 secondi.
4. **Body più profondo.** Prova, un'obiezione risolta nelle parole del cliente (VOC), o la conseguenza del non agire. Solo prova sourced.
5. **CTA finale.** Una richiesta, coerente con funnel stage e tipo offerta (`awareness_tension_funnel.md` A.4). Ogni ad parlato FINISCE sulla CTA.

## S.2 — I 12 framework video nominati (modalità parlate)

Scegli UNO per script; i beat dello scheletro si mappano sull'ordine di beat del framework.

| Framework | Forma | Migliore per |
|---|---|---|
| C.R.O.W.D. | Chiama il movimento, Rigetta il vecchio modo, Onboarda il nuovo, Sventola la prova, Dirigi | energia da effetto gregge, momentum esperto/crowd |
| D.I.S.R.U.P.T. | Declassifica, fallimento di Industria, Soluzione, Rinforza, Sorpassa, Prova, Trigger | angoli contrarian, bugia di categoria |
| C.U.R.E. | Curiosity hook a lista, sCopri i fallimenti, Rimedio, Evidenza, Coinvolgi | listicle "errori che stai facendo" |
| F.O.U.N.D.E.R. | Presenta il founder, forza avversaria, sblocca l'idea, Numeri, Destino, Coinvolgi | storie origin |
| S.I.M.P.L.E. | Stato di fuga, Identifica il dolore, Minima soluzione, Prova, Lifestyle win, Escape CTA | risultato-senza-lo-sforzo-temuto |
| P.U.R.E. | Problema scoperto, caos non filtrato, Evidenza reale, libertà Effortless | scoperta organica-nativa grezza |
| P.A.S. | Pain, Agitate, Solution | il classico, funziona sempre |
| U.G.L.Y. | Non rifinito, Grezzo, Snello, Urla-all'azione (applicato a qualunque struttura) | scroll-stopper deliberatamente anti-lucido |
| P.R.O.V.E. | Problema, Reframe credibilità, Objection nominata, Vittoria, Espandi | il founder smonta gli scettici |
| S.H.O.W. | Setta la sfida, testa a testa, Outcome e perché, Win e CTA | confronto e demo |
| Triple G | Goal, Gap, Gains | aspirazione con reveal del pezzo mancante |
| T.E.A.S.E. | Tease, Engage, Advantage, Satisfy, Encourage | loop di curiosità per la retention |

Selezione per angle type (`53_ad_angles`): angoli problem-agitation → PAS o SIMPLE; contrarian → DISRUPT; founder → FOUNDER o PROVE; comparison → SHOW; social proof → CROWD; native/ugly → PURE o UGLY.

## S.3 — Matematica del pacing (modalità parlate)

- `secondi = round(parole / wps)` per riga e per segmento. Le parole scritte sono il budget: il generatore video allunga o affretta il parlato per riempire la clip, quindi le parole devono entrare nei secondi PRIMA di renderizzare.
- Ogni segmento generato resta sotto i 10 secondi (soglia di generazione delle skill video); il segmentatore della skill consumatrice possiede gli split esatti.
- L'hook atterra nei primi 3 secondi di audio.
- `two-speaker-turns`: turni alternati corti, ~6-9 parole a battuta, mai due prese consecutive dallo stesso speaker.
- `external-VO`: uno script VO continuo, beat di scena marcati per lo storyboard, nessun dialogo.
- `self-voice`: prima persona a camera, beat b-roll marcati dove mani/prodotto portano la riga.

## S.4 — Modalità static-primary-text

Primary text scritto per Meta. Spedito in DUE lunghezze calibrate per concept, e la coppia è un asse di diversità deliberato (due ad genuinamente diversi, non uno tagliato):

- **Short punch.** L'hook È l'ad: 1-3 frasi, tutto il vitale dentro i 125 caratteri visibili, una CTA. Default per Product-Aware e Most-Aware.
- **Story length.** 100-400 parole sullo scheletro completo. Default per Unaware e Problem-Aware, dove il traffico freddo ha bisogno dell'arco di fiducia.

Le 5 forme per story length (scegli per angle type):
1. **Story + Trasformazione:** lotta relazionabile, agitazione, il momento di svolta, il risultato, CTA.
2. **Contrarian:** rottura di una credenza, perché il modo comune fallisce, l'alternativa, prova sourced, CTA.
3. **Quick Win Promise:** risultato specifico, finestra specifica (solo sourced), obiezioni rimosse, prova, CTA.
4. **Identity Shift:** dolore identitario attuale, identità desiderata, il gap, il ponte, prova, CTA.
5. **Problem Agitation:** problema relazionabile, approfondiscilo, conta il costo, la soluzione, prova, CTA.

Ogni primary text apre con una forma first-line nominata (`headline_frameworks.md` H.3) e rispetta la cadenza naturale (`context/brand/anti_ai_writing_style.md` / `49_anti_ai_slop`). I beat non sono mai etichettati nell'output.

## S.5 — Self-check prima di restituire uno script

- mode e wps impostati esplicitamente (S.0)
- hook entro 3 secondi o 125 caratteri
- una CTA, coerente col funnel stage, e (parlato) lo script FINISCE su di essa
- il conteggio parole entra nel budget secondi al wps dato
- nessuna etichetta beat trapelata nell'output
- si legge ad alta voce come una persona (test in `context/brand/anti_ai_writing_style.md`)

## Evidenze verificate (canone 2026)

- **Hook verbale (Motion 2026, 550k+ ad):** offer-only 9,29% winner rate, confessione 8,74%, contro domanda 5,47%, listicle 5,45%, how-to 5,47%, explainer 5,24%. Default: offerta/urgenza-led, confessione, demographic call-out. Domanda/listicle/how-to/explainer ammessi ma flaggati più deboli. Lifestyle vago hard-flag e riscritto.
- **Timing piattaforma (Meta/TikTok ufficiale, alta confidenza):** brand + messaggio chiave nei primi 3 secondi, motion/visual accattivante nel primissimo frame; hook payoff entro il secondo 6.
- **Durata:** <15s è il best-performer su Instagram feed (verificato), <10s su Stories. Oltre, sono convenzioni di produzione non scienza verificata di retention: ~30s standard UGC 5-beat; 45-60s con mid-hook/pattern-reset ogni 12-15s; 90s+ (VSL) hook-story-offer con prova impilata metà-fine.
- **Costanti wps (case interne, misurate su produzione reale — non winner-data pubblici):** self-voice/two-host ~3,5 wps; external-VO (claymation/animazione) ~2,5 wps (pacing editoriale più lento); founder talking-head ~2,8-3,0 wps.
- **UPGRADE DI MISURA:** quando esistono teardown in `03_Ad_Spy/<slug>-video/` (da `52_ad_spy_video`), calcola il wps REALE dei winner della nicchia dai loro transcript timestampati e preferiscilo alla costante di casa, dicendo quale hai usato — è un vantaggio misurato per-brand.
- On-screen text: satura a 2,5-3 parole/secondo di lettura (mai la cifra 5-10 wps, implausibile contro le norme dei sottotitoli).
- **Gate guadagni (coaching/info, FTC):** claim di guadagno ingannevoli sono GIÀ illegali sotto FTC Act Section 5. Mai stato/implicato un livello di reddito senza sostanziazione scritta + contesto risultato tipico; niente immagini lifestyle-flex che implicano reddito. Vedi `creative_claims_compliance.md` C.2.
- **Non citare mai:** nessun "calo del 37% di performance hook dopo 7 giorni" (non verificato, cita solo rotazione su frequenza osservata); nessun wps "benchmark" da blog generico (solo costanti di casa + misura da spy-video).
