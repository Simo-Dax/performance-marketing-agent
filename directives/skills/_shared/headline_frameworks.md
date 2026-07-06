# Motore condiviso — Framework headline (libreria nominata + evidenze)

Riferimento condiviso usato da `54_headline_bank` e riusabile da `28_meta_copy`/SA7. 9 famiglie di framework + 5 formule direct-response, limiti carattere Meta, sub-libreria first-line per primary text. Ogni headline prodotta NOMINA il framework che usa, così si impara il mestiere e i reviewer possono verificare che la riga faccia davvero quello che il framework promette.

**Limiti hard (specifiche Meta, conta ogni carattere spazi inclusi), due tier:**
- Headline: 40 caratteri hard max; 27 caratteri è la lunghezza truncation-safe di Meta per Facebook Feed → preferisci ≤27 e mostra sempre il conteggio.
- Description: 30 caratteri hard max; 25 raccomandato.
- Hook visibile del primary text: i primi 125 caratteri devono portare l'hook (la guida Facebook stessa dà un range 50-150, più corto è più sicuro).
- Meta può troncare oltre le raccomandazioni a seconda di placement/device: nel dubbio, taglia parole.

Regola prova: eredita da `creative_claims_compliance.md` — ogni numero/conteggio/rating/endorsement in una headline traccia a VOC, Brand DNA o ad scrapati, altrimenti si omette o si sceglie un altro framework. Mai inventarne uno.

---

## H.1 — Le 9 famiglie di framework

Esempi = FORME da riempire col linguaggio VOC del brand, mai righe da riusare.

**1. Pattern Interrupt / Curiosity** — un loop aperto che il lettore deve risolvere. *"L'abitudine sotto la doccia che ti invecchia la pelle"*
**2. Direct Benefit** — il risultato, detto chiaro, nelle parole del cliente. *"Sonno profondo senza il torpore al mattino"*
**3. Enemy / Agitation** — nomina il nemico (ingrediente, vecchio modo, bugia di categoria) e schierati col lettore. *"Il tuo integratore è per lo più riempitivo"*
**4. Mechanism Reveal** — nomina COME funziona, idealmente con un termine proprietario o concreto. *"Spremuto a freddo, così gli enzimi sopravvivono"*
**5. Proof / Challenge** — un risultato reale sourced, o un test che il prodotto supera. *"12.000 recensioni a 5 stelle"* (solo se sourced)
**6. Specificity + Speed** — risultato esatto, finestra esatta. SOLO con fatti sourced. *"Pelle più morbida in 14 giorni o rimborsato"*
**7. Identity / Relatability** — chiama chi è il target, nel suo linguaggio identitario. *"Per i runner con le ginocchia a pezzi"*. **GATE POLICY (verificato):** Meta rifiuta ad che asseriscono/implicano attributi personali del VIEWER (etnia, religione, credo, età, orientamento, disabilità, condizioni mediche). Callout su interessi/comportamenti (runner, freelance) sono sicuri; callout su età/salute no ("Hai il diabete?" è un rejection documentato; "Nuovi trattamenti diabete disponibili" passa). Riscrivi ogni callout attributo-linked come prodotto-focused o community-focused.
**8. Contrarian / Hot Take** — [credenza comune] è sbagliata, ecco la verità opposta. *"Il cardio non è il modo più veloce per perdere grasso"*
**9. Simple + Direct** — prodotto, offerta, fine. Nessun device. Per traffico Product/Most-Aware il device è d'intralcio. *"La tote di ogni giorno. -20% questa settimana"* (solo promo reale)

## H.2 — Le 5 formule direct-response (famiglia KK)

- **KK1 Social Proof + Domanda:** "[numero sourced] hanno [risultato]. Ti stai perdendo qualcosa?"
- **KK2 Ti Hanno Mentito:** "Le bugie che [industria/autorità] ti racconta su [tema]". Pattern interrupt TOF forte; l'accusa punta sempre alla categoria, mai a un competitor nominato.
- **KK3 Minaccia + Soluzione:** "[risultato] in [tempo]" o "[perdita] ti costa [importo sourced]". Tempi e importi sourced o omessi.
- **KK4 Credibility Flip:** "Il [metodo/prodotto] che [gruppo credibile] giura di usare". Il gruppo deve essere reale e sourced.
- **KK5 Domanda:** "Stai facendo questi [n] errori di [categoria]?" **GATE POLICY:** mai puntare la domanda su un attributo personale ("Hai [condizione]?" è rejection documentato); interroga il mestiere o la categoria, mai salute/età/identità del viewer.

## H.3 — Sub-libreria first-line (apertura primary text)

I primi 125 caratteri del primary text sono la VERA headline su Meta; il feed tronca il resto dietro "Altro". Queste sono forme di apertura, distinte dalle headline on-image perché possono correre più lunghe e leggersi come una persona che parla:

1. Confessione: "Non ci credevo neanch'io, finché..."
2. Callout: "Se [comportamento specifico], questo è per te." (solo comportamento, mai condizione medica o età — il gate personal-attributes si applica anche qui)
3. Story cold-open: "Tre settimane fa, [scena concreta]..."
4. Stat shock (sourced): "[numero reale] di [gruppo] ha a che fare con [problema]."
5. Enemy opener: "Nessuno in [categoria] vuole dirlo ad alta voce:"
6. Domanda singola: una domanda tagliente, non tre impilate.
7. Mid-thought: "...ed è esattamente per questo che la mia [routine] è cambiata."
8. Objection-first: "Sì, costa più di [alternativa]. Ecco perché è proprio il punto."
9. Plain-truth: "[Prodotto] fa una cosa: [risultato]. Punto."

Ogni primary text nomina la sua forma di apertura come le headline nominano il framework. Le regole di cadenza vivono in `context/brand/anti_ai_writing_style.md` + `49_anti_ai_slop` (devono leggersi parlate, non scritte).

## H.4 — Set canonico di meccaniche hook

Una lista condivisa da ogni skill (hook on-image delle statiche, hook verbali UGC, hook dei deck). Quando serve "un hook diverso per variante", varia su queste meccaniche:

domanda, claim audace, pattern interrupt, confessione relazionabile, prova sociale, paura-di-perdere, aspirazione, agitazione del problema, offerta diretta, curiosity gap, identity callout, myth-break.

## H.5 — Guida di selezione per awareness

- Unaware e Problem-Aware: guida con Pattern Interrupt, Enemy/Agitation, Identity, Contrarian, KK2, KK5.
- Solution-Aware: Mechanism Reveal, Contrarian, KK4.
- Product-Aware: Proof/Challenge, Specificity+Speed, KK1, KK3.
- Most-Aware: Simple+Direct, offer-led.

## H.6 — Disciplina di output

- Nomina il framework accanto a ogni headline: `"Il tuo integratore è per lo più riempitivo" (Enemy/Agitation, 38 char)`.
- Mostra sempre il conteggio caratteri; oltre il limite si riscrive prima di mostrarla, mai segnata come "quasi ok".
- In un set standard (5 righe): nessuna famiglia più di 2 volte, almeno 3 famiglie rappresentate. Bank dedicate da 15+ righe (vedi `54_headline_bank`) seguono il proprio cap: tutte le 9 famiglie presenti, nessuna più di 3 volte.
- Il FILTRO GENERICO si applica a ogni riga: se la headline potrebbe girare per qualsiasi brand della categoria, riscrivila col meccanismo, il prop o il linguaggio verbatim di QUESTO brand.

## Evidenze verificate (canone 2026)

Dataset: Motion Creative Benchmarks 2026 — 550k+ ad, 6k+ inserzionisti, ~$1.3B spend Meta, finestra set-2025/gen-2026 (skewed BFCM, "winner" = proxy di allocazione spesa; default forte, non fisica).

- Tattiche hook/headline con winner rate più alto: offerta/urgenza/immediatezza-led. Offer-only 9,29%, Confessione 8,74%, contro Domanda 5,47%, Listicle 5,45%, How-to 5,47%, Explainer 5,24%.
- Dichiarazioni lifestyle vaghe e benefici generici appaiono spesso ma RARAMENTE tra i winner.
- Solo il 4-8% delle creative diventa winner in generale (3,8% micro account, ~8,2% enterprise) — il kill floor esiste perché la maggior parte delle righe perde.
- Testo ON-IMAGE: le statiche text-forward sono in cima alla classifica winner per famiglia di asset (hit rate ~4-12%). L'headline on-image non è decorazione, è la famiglia statica vincente.
- Mediana storica headline Facebook: 5 parole (studi descrittivi AdEspresso 37k/752k ad, non causali — trattali come craft, non legge).
- Gate personal-attributes (H.1.7): second person "tu/tua" NON è vietato, lo diventa solo se legato a un attributo listato. "other" + sostantivo-attributo fa scattare la violazione ("Meet other black singles" viola, "Meet black singles" passa).
- Clickbait/engagement bait: Meta li DEMOTE nelle sue Content Distribution Guidelines — ma quella definizione è documentata per la distribuzione ORGANICA, non come Ad Standard a pagamento. Non dire "Meta bans engagement bait in ads"; la postura corretta è: curiosità benvenuta, clickbait/beg-for-engagement evitati perché rischio-demotion + craft debole (e perché testano peggio in H.1).
- **Non citare mai:** nessuna soglia di similarità numerica attribuita a Meta, nessun dato causale CTR-per-stile-headline (solo winner-rate descrittivo), "regola del 20% di testo" (nessuna prova di penalità verificata in un senso o nell'altro).
