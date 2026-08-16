# KIE AI — Mappa API (gateway di render alternativo)

**Stato: MAPPATO, NON CABLATO.** Nessuna skill chiama KIE oggi. Questo file esiste perché il giorno in cui vorrai attivarlo la mappatura c'è già: metti la key, segui la tabella "punti di innesto", fatto. Finché non lo attivi, non costa nulla e non tocca nulla.

**Perché REST diretto e non un MCP:** KIE non pubblica un server MCP proprio. Esistono MCP di terzi che lo wrappano, ma introdurrebbero una dipendenza esterna — contro la regola dell'agente (zero dipendenze da plugin/server di terzi). Il pattern è quindi lo stesso di Apify: **key in un env file nostro + chiamate REST con `curl`** dai nostri script.

---

## 1. Contratto API (verificato su docs.kie.ai, 2026-08-16)

**Base URL:** `https://api.kie.ai`
**Auth:** header `Authorization: Bearer $KIE_API_KEY` su ogni chiamata. **Mai la key in URL o query string.**
**Key:** si genera su https://kie.ai → API Key Management.

### 1.1 Credito (gratis — è il gate di spesa)

```
GET https://api.kie.ai/api/v1/chat/credit
```

```json
{ "code": 200, "msg": "success", "data": 100 }
```

`data` = crediti residui. Chiamata gratuita: **leggila e mostrala all'utente PRIMA di ogni `createTask`**, mai spendere senza un sì esplicito.

### 1.2 Creare un task (spende crediti)

```
POST https://api.kie.ai/api/v1/jobs/createTask
Content-Type: application/json
Authorization: Bearer $KIE_API_KEY
```

Body:
```json
{
  "model": "<model-id>",
  "input": { "...": "campi specifici del modello" },
  "callBackUrl": "opzionale — noi non lo usiamo, facciamo polling"
}
```

Risposta:
```json
{ "code": 200, "msg": "success", "data": { "taskId": "..." } }
```

> ⚠️ **`input` cambia da modello a modello.** La forma esatta va letta sulla pagina del modello su docs.kie.ai al momento del cablaggio — non assumerla. Stessa disciplina che usiamo con fal.ai (`mcp__fal-ai__find` prima di chiamare).

### 1.3 Stato e risultato (polling)

```
GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=<taskId>
```

```json
{
  "code": 200, "msg": "success",
  "data": {
    "taskId": "...", "model": "...", "state": "...",
    "resultJson": "<stringa JSON>",
    "failCode": "...", "failMsg": "...",
    "progress": 0, "costTime": 0, "creditsConsumed": 0
  }
}
```

`state` ∈ `waiting` · `queuing` · `generating` · `success` · `fail`. Polling finché `success` o `fail`.

`resultJson` è una **stringa JSON** (va parsata due volte):
- media: `{"resultUrls": ["https://..."]}`
- Seedance 2 con frame: `{"resultUrls": [...], "firstFrameUrl": [...], "lastFrameUrl": [...]}`
- testo: `{"resultObject": {}}`

### 1.4 Scadenze — la regola che ti frega se la ignori

- URL dentro `resultJson`: **~24 ore**.
- URL restituiti da `POST /api/v1/common/download-url` (body `{"url": "..."}`): **20 minuti**.

**Scarica sempre subito con `curl` dentro la cartella campagna.** Un asset non scaricato è un asset perso e ripagato.

---

## 2. Setup della key

`/pm-setup-kie` → scrive `~/.config/pm-agent/kie.env` (`chmod 600`):

```
KIE_API_KEY=<key>
```

Gli script la leggono come Apify:

```bash
[ -f ~/.config/pm-agent/kie.env ] && . ~/.config/pm-agent/kie.env
KEY="${KIE_API_KEY:-}"
[ -z "$KEY" ] && { echo "KIE key mancante — lancia /pm-setup-kie"; exit 1; }
```

**KIE non va in `.mcp.json`**: non è un server MCP, è REST. In `.mcp.json.example` c'è solo una nota che lo dice.

---

## 3. Punti di innesto (se un giorno attivi KIE)

KIE diventerebbe un **Path aggiuntivo**, mai un rimpiazzo: le skill restano model-agnostic e i path esistenti non si toccano.

| Skill | Cosa genererebbe via KIE |
|---|---|
| `24_static_ads` | statiche (GPT Image 2 / Nano Banana) |
| `25_ugc_prompt` · `57_ugc_studio` · `58_ugc_blueprint` | clip UGC (Seedance) |
| `26_product_shot` | product shot |
| `27_multiplier` | varianti |
| `56_animate_static` | image-to-video da statica |
| `59` · `60` · `61` | clip dei formati creativi |

Ordine di lavoro per il cablaggio:
1. Key via `/pm-setup-kie` + verifica su `/chat/credit`.
2. Sulla pagina del modello, leggi lo schema `input` reale.
3. Uno script condiviso in `execution/scripts/` (create → poll → download), non uno per skill.
4. Aggiungi il Path nelle skill sopra, **dietro il gate credito**.
5. Testa su UNA generazione reale prima di dichiararlo funzionante.

**Vale la pena solo se il risparmio è reale sui tuoi volumi.** Oggi il Path C (fal.ai) copre già "pay-per-render senza abbonamento".

---

Fonti: [Common API Quickstart](https://docs.kie.ai/common-api/quickstart) · [Get Task Details](https://docs.kie.ai/market/common/get-task-detail)
