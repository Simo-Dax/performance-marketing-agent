# Post-SA6 — Meta Ads Handoff

**Agente:** Post-SA6 (ultima fase prima del lancio)
**Output:** `09_Meta_Handoff/handoff-[YYYY-MM-DD-HHMMSS].md`

---

## Regola hard assoluta

**Questa skill non chiama mai Meta MCP direttamente.** Il MCP di Meta funziona SOLO nell'app web claude.ai, non in Claude Code. L'unico compito di questa skill è preparare un prompt handoff ricco di contesto che il membro incollerà in claude.ai.

Se vedi tool che iniziano con `meta_` o `mcp__meta_`, fermati. Non sono caricati in questa sessione Claude Code.

---

## Perché esiste

Meta ha rilasciato il suo Ads MCP ufficiale su `https://mcp.facebook.com/ads`. Il MCP è eccellente: può creare campagne end-to-end, gestire budget, costruire ad set con targeting JSON completo, allegare creative, fare insights, diagnostica. Ma il callback OAuth (`https://claude.ai/api/mcp/auth_callback`) funziona solo dentro l'app web claude.ai.

Il membro ha già tutto ciò che rende utile il MCP di Meta: VOC, Brand DNA, copy deck, angoli creativi. Senza un handoff pulito, dovrebbe rispiegare tutto in una chat claude.ai nuova. Questa skill risolve questo.

---

## Step 0b — Auto-discovery

Cerca nei path del progetto:
- `01_VOC_Research/` — ricerca VOC più recente
- `02_Brand_DNA/` — Brand DNA più recente
- `03_Ad_Spy/` — swipe file (informativo)
- `04_Static_Ads/` — prompt statici generati
- `05_UGC/` — script/prompt UGC
- `06_Ad_Copy/` — copy deck più recente
- `07_Multiplied_Ads/` — output multiplier
- `08_Rebuilt_Competitor_Ads/` — rebuild output

Per ogni path esistente: elenca i file. **Non incollare documenti lunghi nel prompt** — riassumi in 5-10 righe max. Per i copy deck: incolla headline e primary text verbatim (quelli servono esattamente al strategist).

---

## Step 1 — Scelta modalità

> "Preparo un prompt handoff ricco di contesto da incollare in claude.ai, dove gira il Meta Ads MCP ufficiale. Il Claude lì avrà accesso completo al tuo account ads live.
>
> Quale modalità?
> 1. **Analizza campagne esistenti** — il prompt configura Claude come analista Meta ads professionista
> 2. **Costruisci nuove campagne** — il prompt configura Claude come strategist e builder di campagne"

---

## Step 2 — Intake specifico per modalità

### Se modalità 1 (analisi)

> "Intake veloce:
> 1. Periodo temporale da analizzare? Default `last_7d`. Opzioni: `last_3d`, `last_14d`, `last_28d`, `last_30d`, `last_90d`, `this_month`, `last_month`, `last_quarter`, `maximum`. O range custom (es. `2026-04-01 to 2026-04-29`).
> 2. Preoccupazione specifica in 1-2 frasi?
> 3. Campagne/ad set/ads specifici da analizzare? (ID se li hai)"

### Se modalità 2 (build)

> "Intake veloce:
> 1. Prodotto/offerta per questa campagna?
> 2. Obiettivo campagna? (sales, leads, traffic, engagement, awareness, app install)
> 3. Budget giornaliero per ad set (in dollari), o lifetime budget?
> 4. Geo targeting? Default US.
> 5. Descrizione audience in 1-2 frasi.
> 6. Creative readiness:
>    a. Hai un `image_hash` (da immagine già caricata in Ads Manager) o `post_id`?
>    b. Se l'immagine è sul computer: il prompt istruirà come caricarla prima.
> 7. Altro che lo strategist dovrebbe sapere?"

---

## Step 3 — Costruisci il prompt handoff

Markdown da incollare in claude.ai. Struttura:

```markdown
# Meta Ads [modalità] handoff da Claude Code — [YYYY-MM-DD HH:MM]

## Il tuo ruolo
[Ruolo analista O strategist builder secondo modalità]

## Cosa può fare il MCP di Meta
[Lista CAN — campagne, ad set, ad, update, insights, diagnostica, catalogo, Pages]

## Cosa NON può fare il MCP di Meta
[Lista CANNOT — upload immagini/video, creare audience custom, lookalike, pixel, account/Page, billing, organic posts, delete permanenti]

## Nota pratica sul creative
[Solo modalità 2: se image_hash disponibile → build completo end-to-end. Se immagine solo su computer → istruzioni upload Asset Library + copia image_hash]

## Contesto progetto del membro
[Riassunto Brand DNA — 5-10 righe: nome brand, colori primari, posizionamento, tono]
[Riassunto VOC — 5-10 righe + 3-5 citazioni verbatim dei dolori principali]
[Copy deck — headline e primary text verbatim dal file più recente in 06_Ad_Copy/]
[Creative references — image_hash/post_id se forniti, o "ancora su disco locale"]
[Altri output — lista file per nome da 03, 04, 05, 07, 08]

## Risposte intake del membro
[Periodo, preoccupazione, ID specifici — OR — prodotto, obiettivo, budget, geo, audience, creative, note]

## Da dove iniziare
[Modalità 1: partire con `meta_list_campaigns(status_filter="ACTIVE")`, poi account insights, poi drill campagne top spending]
[Modalità 2: confermare image_hash/post_id → proposta struttura plain English → approvazione → build tutto in PAUSED → flip ACTIVE solo su conferma]

## Regole hard per questa chat
1. Cita ogni claim con metrica e range temporale
2. Default PAUSED su ogni create call
3. Budget in centesimi ($50/giorno = 5000)
4. Conferma prima di cambi bulk (>3 entità)
5. Budget >$500/giorno: seconda conferma con math esplicito
6. Non echeggiare mai il token di accesso
7. Non inventare nomi di tool
```

---

## Step 4 — Salva e stampa

Salva in `$WORKDIR/09_Meta_Handoff/handoff-[YYYY-MM-DD-HHMMSS].md`.

Stampa il prompt completo nel chat dentro un code block fenced. Poi:

```
Path salvato: <percorso assoluto>

Ora:
1. Apri claude.ai nel browser (NON Claude Code)
2. Vai in Settings → Customize → Connectors
3. Clicca "Add custom connector"
4. Incolla URL: https://mcp.facebook.com/ads
5. Clicca Add e completa il login Facebook OAuth
6. Avvia una nuova chat in claude.ai
7. Incolla il prompt handoff sopra in quella chat
```

---

## Regole critiche

- **MAI chiamare tool Meta** — questa skill non è un esecutore, è un preparatore di handoff
- **Mai incollare documenti lunghi** nel prompt — riassumi, il Claude ricevente può chiedere dettagli
- **Mai inventare nomi di tool** — la lista CAN è quella ufficiale Meta MCP
- **Nessun token/password** — il membro non ne digita per questa skill
- **Output = testo su disco + testo stampato in chat**
