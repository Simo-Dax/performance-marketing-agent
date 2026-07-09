# Winning Ad Science — il layer di evidenza verificata per i render prompt

Traduce eye-tracking research, dati piattaforma Meta, scienza della percezione visiva e dataset di creative testing nel layer di evidenza dietro ogni render prompt. Step 6 di `24_static_ads` carica questo file insieme a `format_families.md`. Step 4 (motore angoli) può consultare la Sezione 7 (Scroll Stop) per la meccanica del messaggio.

**Come vincola, dipende dalla mossa:** su un REBRAND il design della fonte si tiene intero perché ha già vinto nel feed reale, quindi un conflitto con una regola qui è UNA riga onesta di warning, mai una riscrittura. Su una SYNTHESIS queste regole sono legge e il glance test (Sezione 10) è un gate hard.

Filosofia in una riga: la STRUTTURA è provata, la SCENA è libera. Ogni regola dichiara il vincolo E la libertà che lascia, così mille ad possono seguire la stessa scienza e sembrare comunque mille ad diversi.

**Label di evidenza:** VERIFIED-STRONG (fonti platform-primary o peer-reviewed, accordo multiplo) · VERIFIED-MODERATE (uno studio credibile o un dataset ampio, con caveat dichiarati) · WEAK (dato practitioner direzionale, mai citato come scienza) · HEURISTIC (nessuna evidenza trovata in un senso o nell'altro — giudizio di mestiere, utile ma mai research-backed) · MYTH (la ricerca lo confuta — mai codificarlo).

**Ordine di autorità nello scrivere ogni prompt:** su REBRAND: 1) il design tenuto della ricreazione sorgente, 2) il messaggio dell'angolo assegnato, 3) il Winning Ad Visual DNA + `$PRODUCT_DNA` (lato identità dello swap), 4) questo file, solo warn. Su SYNTHESIS: 1) l'angolo assegnato, 2) il Visual DNA, 3) `$PRODUCT_DNA`, 4) il linguaggio di pattern della bank, 5) le regole di questo file come floor hard. Quando una regola qui confligge coi winner provati del brand, vincono i winner e si nota la tensione.

---

## Sezione 1 — La realtà dell'attenzione per cui ogni prompt è disegnato

1. Le persone passano in media 1,7s su un contenuto feed mobile, 2,5s desktop (VERIFIED-STRONG, fonte Meta primaria). Mobile è il caso maggioritario: disegna per la finestra 1,7s.
2. Il contenuto feed mobile è richiamabile a un tasso statisticamente significativo dopo solo 0,25s di esposizione (VERIFIED-STRONG). La prima fissazione fa lavoro reale.
3. L'eye tracking su Instagram trova l'attenzione concentrata sulla porzione immagine più che sul testo circostante (VERIFIED-MODERATE, n=100). L'immagine è l'ad; la caption è un attore di supporto.
4. La creative è il singolo driver più grande degli outcome di vendita ad-driven: 49% delle vendite incrementali (NCS 2023) vs 11% targeting, 14% reach; Nielsen via Meta indica 56% del ROI vendite di una campagna. Mai dire che la creative batte "targeting, budget e placement combinati" — budget e placement non sono quantificati.
5. I segnali di rilevamento visivo core emergono entro ~150ms di esposizione (VERIFIED-MODERATE, un bound ERP per rilevamento binario rapido, non piena comprensione della scena). Il soggetto deve essere riconoscibile a colpo d'occhio.

Conseguenza di design: ogni ad deve comunicare la sua unica idea a uno sconosciuto in meno di 2 secondi, a scala thumbnail su telefono.

## Sezione 2 — Layout zonale e posizionamento testo

**2.1, un solo focal point dominante (VERIFIED-MODERATE).** Ogni prompt nomina esattamente un elemento che possiede la prima fissazione: prodotto, volto, headline, o device di prova. Tutto il resto visibilmente subordinato. Mai due eroi in competizione. *Libertà: quale elemento è l'eroe.*

**2.2, l'headline vive dentro le prime due fissazioni (HEURISTIC, su base saliency verificata).** Lo stack classico (headline top, prodotto/scena centro, prova bottom) segue l'ordine di scan naturale — default, non legge. *Libertà: qualunque arrangiamento che tenga l'headline dentro le prime due fissazioni; i formati native-post possono centrare il testo come uno screenshot.*

**2.3, rispetta le safe zone del placement (VERIFIED-STRONG per 9:16, WEAK per feed).** 9:16 Stories/Reels: Meta raccomanda percentualmente il top 14%, il bottom 35%, 6% per lato, liberi da testo/loghi/elementi critici (su 1080x1920 ≈270px top, ≈670px bottom — la zona bottom è molto più grande di quanto la maggior parte delle spec practitioner ammetta). 4:5/3:4 feed: Meta non pubblica una spec di crop feed — l'euristica practitioner è un quadrato centrato ~950x950 su canvas 1080 di larghezza, mai citato come regola piattaforma.

**2.4, clutter vs struttura (VERIFIED-MODERATE, Pieters/Wedel/Batra 2010).** Clutter visivo non strutturato danneggia l'attenzione al brand; una composizione ricca ma ordinata la aumenta. Ordinato vince, disordinato perde. Spazio negativo generoso si legge come posizionamento premium/qualità (VERIFIED-MODERATE, Pracejus 2006 — associazione percettiva, non un boost di prominenza provato).

**2.5, i pattern di lettura Z ed F non si applicano alle image ad (MYTH per immagini).** Usa la logica di fissazione: eroe primo, headline secondo, prova terzo.

**2.6, i ruoli degli elementi (VERIFIED-MODERATE, Pieters/Wedel 2004).** Il pictorial cattura attenzione INDIPENDENTEMENTE dalla sua dimensione (punto di ingresso); il testo cattura attenzione in proporzione diretta alla sua superficie; l'elemento brand è il più forte hub di TRASFERIMENTO attenzione nonostante la sua piccola dimensione. Non scambiare mai i ruoli.

**2.7, prima fissazione al centro schermo (VERIFIED-MODERATE, Tatler 2007).** Le prime fissazioni atterrano al centro del frame a prescindere da dove sta il contenuto saliente. Eroe al centro ottico per default; un eroe off-center è una scelta deliberata che deve guadagnarsi la posizione con contrasto forte.

## Sezione 3 — Copy on-image

**3.1, un messaggio per ad (VERIFIED-MODERATE, fluidità di processamento).** L'immagine comunica esattamente un'idea; benefici extra vivono nel primary text.

**3.2, lunghezza headline 4-8 parole (HEURISTIC, nessuna evidenza per una banda specifica).** Tenuta perché entra nella finestra 1,7s. I formati text-native (advertorial, finto post) sono esenti.

**3.3, tieni magro il testo on-image (storia VERIFIED-MODERATE, meccanismo attuale MYTH).** Meta ha smesso di penalizzare le immagini text-heavy in asta/delivery attorno a settembre 2020. NESSUN favoritismo di delivery verificato oggi verso creative low-text — il testo magro resta lo standard per la fisica dell'attenzione (Sezione 1), non per una penalità di delivery. Standard di lavoro: headline + al massimo una riga di supporto + un testo device di prova.

**3.4, l'headline deve funzionare senza la caption (WEAK).** La maggioranza degli utenti non tocca mai "Altro" per espandere il primary text troncato — quindi l'headline on-image comunica da sola. Correzione da eye-tracking (VERIFIED-MODERATE, Rayner): il folklore "nessuno legge il testo ad" è impreciso — i viewer nello studio hanno speso PIÙ tempo/fissazioni sul testo ad che sull'immagine, moderato dal loro obiettivo (scroller casuali entrano dall'immagine, shopper coinvolti leggono davvero).

**3.5, la specificità batte la vaghezza (VERIFIED-MODERATE per numeri precisi).** Numeri dispari precisi ("2.147 recensioni") si leggono più research-based di numeri tondi ("2.000+"). Ogni numero traccia comunque a VOC/Brand DNA/ad scrapati.

**3.6, formattazione prezzo (VERIFIED-MODERATE, entrambi gli effetti condizionali).** Congruenza font sale-price (Coulter/Coulter 2005): in un layout comparativo, il prezzo scontato in font fisicamente PIÙ PICCOLO del prezzo barrato — effetto di confronto, mai uno shrink-the-price standalone. Finali left-digit (Thomas/Morwitz 2005): i finali in 9 si leggono più economici SOLO quando cambiano la cifra a sinistra ($30→$29,99 funziona; $35,99 non prova nulla).

## Sezione 4 — Tipografia

**4.1, floor di leggibilità mobile (HEURISTIC).** Headline principale ~5-10% dell'altezza immagine per riga, nessun testo sotto ~3%. Il vero test è 9.2 (sopravvivenza thumbnail).

**4.2, massimo 3 livelli di gerarchia testo (VERIFIED-MODERATE, carico cognitivo).** Headline, riga di supporto, micro testo — ogni livello visibilmente distinto.

**4.3, peso e case (CORRETTO da evidenza peer-reviewed).** Nessun vantaggio di velocità del bold su regular/medium — solo i pesi LIGHT sottoperformano significativamente. All-caps: risultati contrastanti, nessuna soglia di conteggio parole in nessuna fonte — riservalo a headline corte come scelta di mestiere. Il disfluency claim (font difficili da leggere aiutano la memoria) non ha retto la replicazione indipendente — mai scambiare leggibilità per una storia di memoria. Serif vs sans-serif: nessuna differenza di leggibilità praticamente significativa su schermo — scegli su base brand.

## Sezione 5 — Colore e contrasto

**5.1, i floor di contrasto sono standard reali (VERIFIED-STRONG, W3C).** Testo-su-sfondo rispetta le ancore WCAG: 4,5:1 per testo di supporto, 3:1 per headline grande (18pt, o 14pt bold+). Nessuna fonte lega il contrasto direttamente a metriche di performance ad — non affermarlo.

**5.2, contrasto contro l'ambiente feed (meccanismo VERIFIED-MODERATE).** Il feed è perlopiù card bianche e fotografia. Solo UNA differenza di feature forte spicca pre-attentivamente (Treisman/Gelade 1980) — differenzia l'eroe su un asse forte, non tre timidi. Dentro la palette: saturazione più alta alza arousal/energia, luminosità più alta alza piacevolezza (Valdez/Mehrabian 1994).

**5.3, le mappature colore-emozione fisse sono un MYTH (VERIFIED-STRONG debunk).** Rosso non significa universalmente urgenza, blu non significa universalmente fiducia — dipende da contesto/cultura/categoria.

**5.4, coerenza brand tra ad (VERIFIED-MODERATE, direzionale).** Ehrenberg-Bass: l'incoerenza in colori/font/loghi è nemica della costruzione di asset distintivi. Devia deliberatamente per formati native/ugly e dillo nel prompt.

## Sezione 6 — Volti, umani e sguardo

**6.1, i volti sono tra i più forti magneti di attenzione (VERIFIED-STRONG, con il superlativo corretto).** Fissazione su volti >80% probabilità nelle prime due fissazioni, ma il TESTO è comparabile in salienza (volti 16,6x, testo 11,1x vs regioni size-matched) — un volto non è automaticamente più forte di una headline bold.

**6.2, gestisci il vampire effect (VERIFIED-MODERATE per celebrity/volti molto attraenti).** L'attenzione bloccata su volti celebrity/attraenti riduce misurabilmente il riconoscimento brand. Disciplina comunque: ogni volto in frame dichiara una direzione di sguardo, il prodotto resta competitivo in dimensione/contrasto.

**6.3, la direzione dello sguardo è un volante (VERIFIED-MODERATE, il lever creativo meglio supportato in questo file).** Sguardo distolto verso prodotto/headline: aumenta attenzione/memoria per testo e prodotto, alza il riconoscimento brand (default per ad prodotto). Sguardo diretto in camera: supporta credibilità spokesperson per appeal informativi — MAI affermare che alza l'arousal (non supportato); uno studio sul campo trova lo sguardo distolto vincere su CTR e purchase likelihood. Il meccanismo è il gaze cueing riflesso (Friesen/Kingstone 1998): il viewer sposta l'attenzione dove guarda un volto raffigurato anche sapendo che non predice nulla. Ogni prompt con una persona dichiara la direzione dello sguardo, senza eccezioni.

**6.4, le mani lavorano tramite il tocco, non la presenza (VERIFIED-MODERATE).** Una mano visibile vicino al prodotto non fa nulla — deve TOCCARLO. Il contatto mano-prodotto aumenta la proprietà psicologica percepita per vicarious touch (solo la percezione di ownership è verificata, non lift di conversione). Quando un prompt include una mano, afferra/tiene/tocca, mai fluttua accanto.

## Sezione 7 — Meccaniche di scroll-stop e la manopola del polish

**7.1, il polish stilizzato segnala "questo è un ad" (VERIFIED-MODERATE, meccanismo corretto).** Visual altamente stilizzati aumentano la probabilità che gli utenti classifichino un post come sponsorizzato via riconoscimento euristico veloce — NON filtraggio preattentivo letterale. Il gap di performance è più piccolo del folklore: creative native-style a circa 1,3-1,5x il CTR di equivalenti polished su traffico freddo, non 2-4x. La manopola del polish resta: i formati native si impegnano pienamente nell'imperfezione, i formati hero pienamente nella craft, un ad polished che finge casual è il perdente documentato di mezzo.

**7.2, il pattern interrupt via contrasto col feed, non casualità (meccanismo VERIFIED-MODERATE).** Interrupt legali: scala inaspettata, un primo piano scomodo ma relazionabile, un campo colore piatto e forte, un oggetto fuori posto, formati platform-native grezzi. Il meccanismo di memoria verificato è l'isolation effect (Von Restorff): UN item diverso in un contesto altrimenti omogeneo si ricorda meglio.

**7.3, i curiosity gap servono un payoff (HEURISTIC).** Un post troncato o un risultato parzialmente nascosto ferma lo scroll quando il viewer sente la risposta a un tap di distanza. Mai una troncatura finta senza senso.

**7.4, retorica visiva (VERIFIED-MODERATE, due risultati separati).** Figure retoriche (metafora, gioco di parole, antitesi, giustapposizione) aumentano elaborazione e gradimento SENZA danneggiare la comprensione — ma i benefici della metafora collassano oltre un punto di complessità concettuale.

**7.5, il tradeoff dell'umorismo (VERIFIED-MODERATE, Eisend 2009).** L'umorismo alza attenzione, atteggiamento verso l'ad, atteggiamento brand E intenzione d'acquisto (il folklore "l'umorismo non vende" è sbagliato). Il suo unico costo documentato: riduce la credibilità della fonte — usalo liberamente per identity/lifestyle/native, evitalo quando il concept persuade via autorità/credenziali esperte.

## Sezione 8 — Elementi di prova

**8.1, i device di prova devono sembrare nativi ed essere reali (HEURISTIC su grammatica visiva, LEGGE HARD su sourcing via il gate FTC esistente).** Render di card recensione/star row/screenshot commenti fedeli pixel a ciò che imitano. Ogni numero/nome resta sourced o lo slot si omette.

**8.2, un device di prova per ad (VERIFIED-MODERATE, carico cognitivo).** Una card recensione O una stat O un confronto, salvo strutture esplicitamente costruite come trust stack.

**8.3, framing prima/dopo (HEURISTIC sulla forza, LEGGE HARD sulla compliance).** Quando usato, lo stato "dopo" è l'eroe e la coppia deve passare le policy su attributi personali e risultati non realistici + il gate di compliance esistente.

## Sezione 8b — Leve di messaggio ed emozione

1. **La paura ha bisogno di un corrimano (VERIFIED-MODERATE, Tannenbaum 2015, d=0,29).** Appeal basati su paura/problema funzionano in modo affidabile, e i contenuti di efficacia li AMPLIFICANO: accoppia ogni minaccia/agitazione con un'azione/soluzione esplicita e fattibile. Non codificare il folklore inverso — gli appeal alla paura non fanno backfire senza contenuto di efficacia, sono solo più deboli.
2. **Nessun frame di default (VERIFIED-MODERATE, meta-analisi O'Keefe/Jensen).** La differenza persuasiva media tra framing gain e loss è vicina a zero — scegli il frame che si adatta all'offerta, mai come regola di performance.
3. **Emotion-led per il lungo periodo (WEAK, databank practitioner).** Binet/Field: le campagne emotion-led associano a effetti business di lungo termine più forti — un prior soft per concept TOF freddi di brand-building, mai una legge per-ad.
4. **La creatività correla con l'efficacia, solo qualitativamente (WEAK su qualunque numero).** L'originalità da sola è insufficiente.

## Sezione 9 — Formato e frame

**9.1, il portrait verticale massimizza il real estate feed (VERIFIED su geometria).** A larghezza feed fissa, 4:5 rende ~25% più alto di 1:1; Meta raccomanda 4:5 per Facebook Feed. 3:4 non è una raccomandazione feed Meta confermata — esiste perché GPT Image 2 non renderizza un vero 4:5.

**9.2, disegna prima per il thumbnail (VERIFIED-STRONG come conseguenza della Sezione 1).** Prima di finalizzare qualunque prompt, immagina l'immagine a 150px di larghezza. Se eroe e headline sopravvivono, l'ad funziona.

## Sezione 10 — Il glance test

Tre domande di self-check. Su prompt SYNTHESIS gira prima dell'output e ogni fallimento significa riscrittura. Su REBRAND gira come sanity look: un ad che ha girato nel feed reale ha già passato il vero glance test — un fallimento qui è una riga di warning all'utente, mai una riscrittura.

1. **TEST THUMBNAIL:** a 150px di larghezza, l'elemento eroe è identificabile e l'headline leggibile? (Sezioni 2, 4)
2. **TEST SCONOSCIUTO:** uno sconosciuto che vede questo per 1,7s se ne va con l'unico messaggio inteso, senza leggere la caption? (Sezioni 1, 3)
3. **TEST FEED:** scrollando oltre 20 post organici, questo frame differisce visibilmente dal feed attorno, in un modo che serve l'angolo? (Sezioni 5, 7)

## Sezione 11 — Divieti hard per prompt SYNTHESIS

Vincolano ogni prompt sintetizzato (insieme ai divieti standard su AI-aesthetic tell e prova fabbricata). Su un rebrand sono diagnostiche per la riga di warning, mai edit al design tenuto:

1. Nessun testo che fallisce le ancore WCAG (4,5:1 supporto, 3:1 headline grande).
2. Non più di un messaggio per immagine, non più di 3 livelli di gerarchia testo.
3. Nessun secondo focal point in competizione.
4. Nessun volto senza direzione di sguardo specificata.
5. Nessun testo/dettaglio prodotto critico dentro le zone overlay 9:16 (top 14%, bottom 35%, lati 6%).
6. Nessun ad polished che finge casual — scegli un lato della manopola polish per concept.
7. Nessuna scelta colore giustificata da color psychology.
8. Nessun peso font light/thin su testo glance-critical.
9. Nessuna mano che fluttua vicino al prodotto — una mano renderizzata tocca, afferra, tiene.
10. Nessuna energia da stock photo — niente composizioni gruppo sorridenti generiche, niente perfezione watermark-style.

## Sezione 12 — Cosa resta libero, per sempre

Così gli ad non convergono mai verso l'omologazione: scena, ambientazione, persone, palette dentro i vincoli di contrasto, typeface dentro i vincoli di leggibilità, scelta della fonte strutturale, stile fotografico, meccanica dell'interrupt, scelta del device di prova, posizione della manopola polish, ogni parola del copy. La scienza vincola la struttura. Il Visual DNA vincola l'identità. Il Product DNA vincola come il prodotto stesso è mostrato. Tutto il resto è la superficie creativa, ed è enorme.

## Sezione 13 — Cosa non dire mai (folklore rifiutato)

1. "Le image post hanno una finestra di decisione di 2,5s al massimo" — mobile è 1,7s, il recall registra da 0,25s.
2. "La creative batte targeting, budget e placement combinati" — budget e placement non sono quantificati.
3. "Il delivery system Meta favorisce le creative low-text" — le penalità sono finite nel 2020.
4. "La maggior parte dei viewer non legge mai il primary text" — solo la non-espansione di "Altro" è misurata.
5. "Il bold si legge più veloce del regular a colpo d'occhio" — rifiutato, solo i pesi light sottoperformano.
6. "L'all-caps funziona fino a 5 parole" — nessuna soglia ha una fonte.
7. "Il basso contrasto è un killer di performance ad documentato" — documentato solo per leggibilità e fiducia.
8. Qualsiasi mappatura colore-emozione fissa — mito confermato.
9. "Un volto è IL magnete di attenzione più forte" — le regioni testo sono comparabili in salienza.
10. "Lo sguardo diretto alza l'arousal" — non supportato; lo sguardo distolto ha vinto il test sul campo.
11. "I feed filtrano gli ad polished pre-attentivamente" — il meccanismo verificato è classificazione euristica.
12. "Le creative native tirano 2-4x il CTR delle polished" — i dati mostrano ~1,3-1,5x.
13. "Qualsiasi mano visibile aggiunge un beneficio di tocco umano" — inerte senza contatto col prodotto.
14. "Le foto stile-UGC si leggono più autentiche delle studio" — la catena di autenticità non ha retto la verifica.
15. "Font difficili da leggere migliorano la memoria" — replicazione indipendente fallita, mai scambiare leggibilità per questo.
16. "Gli appeal alla paura fanno backfire senza uno statement di efficacia" — restano positivi in modo affidabile senza; l'efficacia amplifica.
17. "Il framing gain (o loss) supera affidabilmente l'altro" — differenza media vicina a zero.
18. "Il serif (o sans-serif) è più leggibile a schermo" — nessuna differenza praticamente significativa.
19. "Lo spazio bianco aumenta la prominenza visiva, per ricerca" — solo l'associazione con percezione premium è evidenziata.

## Sezione 14 — Ledger dei gap, onestamente sconosciuto

Domande a cui la ricerca non ha potuto rispondere. Trattale come aperte, usa giudizio di mestiere, mai implicare che esista evidenza: angolo camera prodotto ottimale per statiche; quanto del frame il prodotto dovrebbe occupare; quando aggiungere un logo standalone se il pack già lo porta; leve di appetite cue per statiche food; quando mani/persone aiutano nelle immagini STATICHE specificamente; floor di dimensione tipo/conteggio parole headline on-image (tenuti come euristiche); se la complessità di design migliora l'ATTITUDE (solo effetti di attenzione sono evidenziati); se il gaze cueing si traduce in conversione (il meccanismo è evidenza da tempo di reazione in lab).

---

## Come la skill usa questo file

Step 6 di `24_static_ads` carica questo file insieme a `format_families.md`. L'ordine di autorità è in cima al file. Su prompt synthesis il glance test (Sezione 10) e i divieti hard (Sezione 11) sono legge. Su rebrand girano solo come warn: la nota di tensione scientifica emerge come una riga onesta, il design tenuto spedisce invariato salvo richiesta dell'utente.
