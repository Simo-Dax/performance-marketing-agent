---
description: Configura il Klaviyo MCP server per SA9 (CRM/email). Verifica uv, raccoglie la PRIVATE_API_KEY, aggiunge il blocco a .mcp.json e testa la connessione. Sicuro di default (READ_ONLY).
---

# /pm-setup-klaviyo — Setup Klaviyo MCP (SA9)

Collega il **Klaviyo MCP server** così SA9 può leggere profili/segmenti/metriche e (opzionale) creare draft email/flow. Server ufficiale: `uvx klaviyo-mcp-server@latest`, env `PRIVATE_API_KEY`. Snippet di riferimento in `.mcp.json.example (blocco klaviyo)`.

## Hard rules
1. Esegui tu i comandi shell via Bash. Non far aprire terminali all'utente.
2. Non echeggiare mai la key in chiaro nei log dopo averla salvata.
3. Non committare mai la key. Verifica che `.mcp.json` sia in `.gitignore` (o che la key non finisca versionata).
4. Idempotente: se il blocco `klaviyo` esiste già in `.mcp.json` e il test passa, dillo in una riga e fermati.
5. Default sicuro: prima connessione con `READ_ONLY=true` (solo lettura). L'utente sblocca la scrittura quando vuole.

## Step
1. **Prerequisito `uv`:** verifica `uv --version`. Se manca → installa (`curl -LsSf https://astral.sh/uv/install.sh | sh`) o segnala.
2. **Key:** chiedi all'utente la Klaviyo **Private API Key** (formato `pk_...`). Spiega dove crearla: Klaviyo → Settings → API Keys → Create Private API Key, con gli scope:
   - Full: Campaigns, Events, Images, Profiles, Segments, Subscriptions, Templates, Translations
   - Read: Accounts, Catalogs, Flows, List, Metrics, Tags
3. **Salva la key** in modo sicuro: `~/.config/pm-agent/klaviyo.env` (`mkdir -p`, poi `chmod 600`):
   ```
   KLAVIYO_PRIVATE_API_KEY=<pk_...>
   ```
4. **Aggiungi a `.mcp.json`:** inserisci dentro `mcpServers` il blocco da `.mcp.json.example (blocco klaviyo)`, sostituendo `<KLAVIYO_PRIVATE_API_KEY>` con la key reale e impostando `READ_ONLY` a `true` per la prima connessione. Preserva gli altri server esistenti (google-ads, higgsfield) — fai un merge, non un overwrite.
5. **Test:** dopo l'edit, la connessione MCP parte al prossimo avvio di Claude Code. Verifica che `uvx klaviyo-mcp-server@latest` si avvii senza errori di auth (puoi fare un dry-run con la env settata). Se ok → "Klaviyo MCP configurato (READ_ONLY). Riavvia Claude Code per attivare il server."
6. **Sblocco scrittura (opzionale):** quando l'utente vuole che SA9 crei draft/flow/template, imposta `READ_ONLY=false` in `.mcp.json`.

## Uso da SA9
- `43_crm_database_analysis` (`/pm-crm-analysis`): legge profili/liste/engagement live da Klaviyo invece dell'export CSV.
- `45_email_strategy` (`/pm-email-strategy`): legge flow esistenti + metriche → gap analysis automazioni.
- `46_email_creation` (`/pm-email-copy`): crea draft di campaign/template in Klaviyo (richiede `READ_ONLY=false`).

## Errore tipo
Auth fallita → "Private API Key non valida o scope insufficienti. Rigenerala in Klaviyo Settings → API Keys con gli scope richiesti e rilancia /pm-setup-klaviyo."
`uvx` non trovato → installa `uv` prima (vedi Step 1).
