---
description: Configura la KIE AI API key (gateway di render alternativo, pay-per-render). Opzionale — nessuna skill lo richiede oggi.
---

# /pm-setup-kie — Configura KIE AI API Key

Configura la key di KIE AI, gateway che espone gli stessi modelli (Nano Banana, GPT Image 2, Seedance) di fal.ai, spesso a costo minore.

**Dillo subito all'utente:** oggi **nessuna skill usa KIE**. Questo comando serve solo a preparare la key. Il contratto API e i punti di innesto sono in `execution/kie_api_map.md`; il cablaggio nelle skill è un lavoro separato da chiedere esplicitamente.

## Hard rules
1. Esegui ogni comando shell tu stesso via Bash. Non far aprire terminali all'utente.
2. Non echeggiare mai la key in chiaro dopo averla salvata.
3. Key **sempre** in header `Authorization: Bearer`, **mai** in URL o query string.
4. Idempotente: se la key esiste già e `/chat/credit` risponde, dillo in una riga e fermati.

## Step
1. Chiedi la key. Si genera su https://kie.ai → API Key Management.
2. Salva in `~/.config/pm-agent/kie.env` (`mkdir -p` sulla dir):
   ```
   KIE_API_KEY=<key>
   ```
   poi `chmod 600` sul file.
3. **Non** toccare `.mcp.json`: KIE non è un server MCP, si usa via REST.
4. Verifica con la chiamata gratuita del credito:
   ```
   GET https://api.kie.ai/api/v1/chat/credit
   ```
   Attesa: `{"code":200,"msg":"success","data":<crediti>}`.
5. Conferma in una riga, riportando i crediti residui: "KIE key configurata e verificata — N crediti."

## Errore tipo
Verifica fallita → "Key non valida o scaduta. Rigenerala su kie.ai (API Key Management) e rilancia `/pm-setup-kie`."
