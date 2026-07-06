# Motore condiviso — Angle engine (generatore di concept medium-neutral)

Riferimento condiviso usato da `53_ad_angles`, riusabile da `13_creative_concepts` (SA5) per il layer di ideazione veloce a monte del concept deck completo. Trasforma l'evidenza brand in ANGOLI ad distinti e pronti al render — medium-neutral (statiche, UGC video, qualunque formato), eseguibile anche SENZA dati Ad Spy live.

Chi chiama passa i propri vincoli a livello di set come variabili. I vincoli specifici della skill chiamante restano nella skill, mai in questo file.

---

## G.1 — Input

Assemblati da: `context/brand/business_profile.md` + `context/brand/tone_of_voice.md` (Brand DNA), `01_VOC_Research/` o `intermediate/insight.md` (VOC — pain, desideri, obiezioni, distribuzione awareness, linguaggio goldmine, prove sanzionate), `niche_offer_types.md` (nicchia + offerta), `awareness_tension_funnel.md` (calibrazione default). Opzionali: swipe/teardown competitor più recente in `03_Ad_Spy/` (barra di differenziazione), i propri winner scrapati del brand se esistono, `intermediate/sa1_competitor_landscape.md` (white space SA1).

## G.2 — Le quattro mappe interne (mai mostrate)

Prima di generare un solo angolo, costruisci:

- **Mappa verità cliente.** I 3-5 territori di dolore/desiderio principali con citazioni verbatim, lo stadio awareness dominante, l'obiezione più grande, il linguaggio identitario che i clienti usano su se stessi.
- **Mappa pattern brand.** Cosa il brand gira già e cosa vince (quando esistono dati winner). Cosa non ha mai provato.
- **Mappa mare della somiglianza.** I 3-5 angoli che ogni brand nella categoria usa, i formati clichè, le claim che i clienti hanno imparato a ignorare (fonte: white space SA1 + VOC).
- **Mappa white space.** Angoli e meccanismi di prova che il brand non usa, la categoria non usa, e il VOC dice che ai clienti importa davvero.

## G.3 — Lo spread di angle type

Genera candidati su TIPI di angolo genuinamente diversi. Mai riempire un set con cinque sapori della stessa idea:

| Tipo angolo | La mossa |
|---|---|
| Problem-agitation | Rispecchia il dolore nelle parole del cliente, twist, allevia |
| Trasformazione prima-dopo | Il cambio di stato, mostrato o raccontato |
| Rivelazione ingrediente/meccanismo | PERCHÉ funziona, la cosa che i competitor non spiegano |
| Prova sociale | Numeri reali, recensioni reali, volti reali (solo sourced) |
| Confronto noi-vs-loro | Il vecchio modo contro questo modo, nominato o no |
| Storia founder/origin | La ragione umana per cui questo esiste |
| Identity callout | "Per chi..." appartenenza e auto-immagine |
| Contrarian/myth-break | La credenza di categoria che è sbagliata |
| Quick win/timeline | Risultato specifico in finestra specifica (solo fatti sourced) |
| Offer-led | L'offerta stessa, per traffico warm/hot |

Per nicchia `info`, stesso spread con transformation/insider-secret/proof pesati di più (vedi `niche_offer_types.md` N.4).

## G.4 — Il contratto a 10 campi del concept

Ogni angolo emesso dal motore è un concept completo in questa forma esatta:

```
CONCEPT <n>: <nome concept>
Big idea: <1-2 frasi>
Angle type: <uno dello spread sopra>
Awareness stage: <unaware | problem-aware | solution-aware | product-aware | most-aware>
Tension layer: <L1..L5, da awareness_tension_funnel.md>
Hook: <la logica dello scroll-stop, poi la riga di apertura>
Target persona: <chi esattamente, una riga>
VOC quote: "<citazione cliente verbatim>" (voc:<rif sezione>)
Direzione visiva: <1-3 frasi, scena concreta, da linguaggio sensoriale VOC + identità visiva brand>
Headline candidate: <3-5, ognuna nominata col suo framework da headline_frameworks.md>
Perché dovrebbe funzionare: <2-3 frasi che citano almeno un segnale VOC + un gap white-space o segnale winner>
```

## G.5 — I gate hard (girano su ogni candidato)

1. **FILTRO GENERICO.** Questo concept potrebbe girare per qualsiasi brand della categoria col logo cambiato? Se sì, kill. Il fix è sempre la specificità: il meccanismo di QUESTO brand, le parole verbatim di QUESTO cliente, i prop nominati di QUESTO prodotto.
2. **CHECK MECCANISMO.** Se la differenziazione del brand è vaga e il concept ci si appoggia, fermati e deriva il meccanismo da Brand DNA + VOC (feature-to-benefit). Se non è genuinamente derivabile, fai UNA domanda all'utente: "Cosa rende il tuo prodotto davvero diverso? Senza questo l'ad suona come tutti gli altri." Non spedire un buco a forma di meccanismo.
3. **CELLA UNICA.** Ogni concept nel set occupa una cella unica Persona × Desiderio × Awareness. Due concept possono condividere una dimensione, mai tutte e tre. Inoltre, per la dottrina di diversificazione di Meta (verificata): ad che "si somigliano o si sentono simili" vengono raggruppati come varianti della stessa creative con learning in pool, quindi la vera distinzione è simultanea su visual, messaggio E formato — non solo copy variant. Meta non pubblica soglie numeriche di similarità né un conteggio minimo di concept: non presentarli mai come dottrina.
4. **ANCORA VOC.** Ogni concept porta una citazione verbatim reale col suo riferimento fonte. Niente citazione, niente concept.
5. **GATE PROVA.** Ogni numero/conteggio/rating/testimonianza nel concept traccia a VOC, Brand DNA o ad scrapati, o lo slot si omette (regole complete in `creative_claims_compliance.md`).
6. **MATCH CALIBRAZIONE.** Profondità hook e CTA coerenti con lo stadio awareness e il funnel stage dichiarati (`awareness_tension_funnel.md` A.5).

Candidati che falliscono ottengono una riscrittura, poi vengono scartati silenziosamente. Genera candidati extra finché il conteggio richiesto non passa tutti i gate.

## G.6 — Spread a livello di set (default, chi chiama può sovrascrivere)

- Copri almeno 3 dei 5 stadi awareness nel set.
- Almeno 2 layer di tensione diversi.
- Nessun angle type usato più di due volte.
- Quando il set alimenta le statiche: almeno un concept native/ugly e almeno un concept social-proof.

## G.7 — Ranking

Ordina il set emesso dal migliore al peggiore per: forza dell'evidenza VOC, distanza dal mare della somiglianza, fit con l'obiettivo dichiarato del run, e (quando esistono learning) vicinanza al territorio winner provato. I concept più deboli del set sono i primi candidati al kill sotto `creative_kill_floor_review.md`.

## Evidenze verificate (canone 2026) — la dottrina di diversificazione Meta

Fonte: Meta for Business, "Demystifying creative diversification" (2025-12-16) + Meta Blueprint Performance 5.

1. **L'iterazione non è diversificazione.** Meta distingue ufficialmente l'ITERAZIONE creativa (stesso visual, testo/CTA diverso) dalla DIVERSIFICAZIONE (concept creativi distintamente diversi). Un angolo è un CONCEPT, mai una copy variant.
2. **I look-alike vengono raggruppati.** Il sistema di delivery di Meta tratta gli ad che "si somigliano o si sentono simili" come varianti della stessa creative, con learning e ottimizzazione in pool. Un set di angoli quasi-duplicati è un'illusione — il motore forza la differenziazione o uccide i look-alike. Usa il linguaggio di Meta: "raggruppati come varianti della stessa creative" — mai terminologia tipo "Entity ID" (non esiste nel materiale ufficiale Meta, è folklore da community).
3. **La distinzione è a tre assi.** Meta lega la diversificazione a essere distinti simultaneamente su visual, messaggio E formato, non un asse singolo.
4. **Nessun numero esiste.** Meta non pubblica soglie di similarità (non 40% o 60%), né un conteggio minimo di concept. Qualsiasi default di batch-size in questa skill è convenzione, mai attribuito a Meta.
5. **Un leva su cinque.** Diversificazione creativa e semplificazione account sono 2 di 5 leve co-equali nel framework Performance 5 di Meta (con automazione, qualità dati, validazione risultati) — mai promettere che lo spread di angoli da solo salvi un account strutturalmente rotto.

**Gate risultati/testimonianze (FTC, vincolante):** una testimonianza a risultato specifico implica tipicità — genera dollari/kg/giorni-a-risultato SOLO se il risultato è sostanziato come rappresentativo (VOC), altrimenti rigenera su meccanismo/processo/identità. "Risultati non tipici" NON è una patch di compliance valida (la normativa la giudica esplicitamente insufficiente). Per nicchia `info`: angoli income-outcome solo con sostanziazione scritta fornita dall'utente, altrimenti framing di trasformazione.

**Da non citare mai:** soglie numeriche di similarità o conteggio minimo concept attribuiti a Meta; "le claim di guadagno nel coaching violano il Business Opportunity Rule" (la norma è proposta, non finalizzata); "risultati non tipici" come disclaimer sufficiente.
