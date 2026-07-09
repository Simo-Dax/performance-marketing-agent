# Motore condiviso — Adjacency Pass (consapevolezza ad live)

Ultimo gate tra un rebrand ribrandizzato e un renderer, usato da `24_static_ads` (Step 6, dopo che i gate R di `format_teardown_recreation.md` passano). I gate R provano che l'identità è scambiata completamente col design intatto; questo pass gestisce l'unica cosa che i gate R non possono: l'ad sorgente, o i suoi simili, potrebbero essere LIVE nello stesso feed in cui il brand sta per entrare.

Nel modello di ricreazione (il design si tiene di proposito), questo pass non uccide più un rebrand per assomigliare alla sua fonte — è il punto. Restano tre compiti: rendere INFORMATA la scelta del brand quando la fonte è live nel suo mercato, evitare che un batch si appoggi due volte sulla stessa fonte, e ri-eseguire la scansione a livello di parola per ultima.

## K.1 — Quando gira

Una volta per ricreazione, per brand target, per run, su ogni render la cui fonte strutturale è una ricreazione bancata. `19_ad_spy` non lo esegue MAI: non ha brand target e non renderizza mai.

## K.2 — Contro cosa verifica

Assembla il set di confronto prima di giudicare:

1. L'intero swipe set ATTIVO del competitor sorgente: ogni ad nel `adspy-<slug>-*.html` più recente per quel brand.
2. Ogni ALTRO competitor spiato nel progetto: per ogni brand in `competitors.json`, gli ad attivi dello swipe più recente.
3. Gli ALTRI ad dello stesso run: quali ad sorgente questo batch ha già usato, e quali ripetizioni sono state dichiarate come variazioni ordinate dall'utente.

## K.3 — I gate

- **K-1, Adjacency informata (WARN, una volta per run, mai un kill silenzioso).** Quando l'ad sorgente del rebrand è attualmente ATTIVO (o un sibling attivo condivide il suo design) e il brand vende allo stesso pubblico, dillo chiaramente prima di renderizzare, un messaggio per l'intero batch: "Attenzione: <n> di queste build condividono il design con ad che <competitor> sta girando ADESSO (<id>). La tua versione porta le tue parole, brand e colori, ma il layout gemello starà nello stesso feed. Renderizzo come previsto, o li scambio con un ad sorgente ritirato?" Procedi solo su decisione dell'utente. Quando l'ad sorgente è ritirato o i pubblici non si sovrappongono, nessun messaggio.
- **K-2, Ripetizione fonte nel batch (HARD, con un'esenzione).** Entro un run, nessun ad sorgente serve da base rebrand per più di un ad, ECCETTO le variazioni ordinate dall'utente dichiarate nel batch plan: condividono la fonte deliberatamente, ognuna con un angolo diverso e i propri sibling shift, con l'utente informato che si raggruppano come un cluster Andromeda. La ripetizione SILENZIOSA fallisce comunque.
- **K-3, Ri-diff verbatim (HARD, meccanico).** Ri-esegui R3 (la scansione del registro da `format_teardown_recreation.md`) come ultimissimo check, perché le revisioni richieste dall'utente possono reintrodurre una frase della fonte.

## K.4 — Regole hard

| Regola | Dettaglio |
|---|---|
| Gira per uso, mai per ricreazione | La clearance appartiene a un brand, un rebrand, un run. Registra l'esito negli artefatti di chi consuma, mai dentro il file di teardown. |
| L'intero set attivo è la barra | Il check adjacency informata copre ogni ad live nel set di confronto, non solo la riga sorgente. |
| Avvisa, non veta | Condividere il design di un ad live è la scelta dell'utente, una volta, con i fatti davanti. |
| Le parole restano hard | K-3 non ha override utente. Una frase della fonte in un render del brand non spedisce mai. |
| Ricade, mai forza | Una ripetizione K-2 costa a un ad la sua fonte, non il run. Una ricreazione diversa è sempre disponibile, o l'utente dichiara la ripetizione come variazione ordinata. |
| Niente trattini lunghi ovunque | In chat o nei file. |
