---
description: Master setup del Performance Marketing Team. Verifica struttura cartelle, MCP, API key (Apify, Fal AI), e prepara il sistema per riprodurlo da zero. Idempotente.
---

# /pm-setup — Master Setup Performance Marketing Team

Setup one-command per riprodurre l'intero sistema agentico Performance Marketing Team su questa macchina. Walk-through completo senza far uscire l'utente da Claude Code.

## Hard rules
1. **Esegui ogni comando shell tu stesso via Bash.** Mai far aprire terminali. Eccezioni: approvare OAuth nel browser (l'utente clicca, tu aspetti), incollare un token quando lo chiedi, confermare azioni distruttive.
2. **Idempotente.** Ogni step completato scrive un marker in `~/.config/pm-agent/.state/step-N.done`. Su rerun, gli step completi vengono saltati con una riga: `step N già completo, skippo`.
3. **Lavoro indipendente in parallelo** via background process quando due step non dipendono l'uno dall'altro.
4. **Ogni messaggio d'errore finisce con un fix concreto.**
5. Niente em-dash.

## Step state dir
```
mkdir -p "$HOME/.config/pm-agent/.state"
```

## Step 1 — Verifica struttura progetto
Controlla che esistano nella root del progetto:
- `claude.md` (orchestrator), `ROADMAP.md`
- `agents/` con sa1-sa8
- `directives/skills/` con le skill 01-30
- `directives/skill_orchestrator.md`
- `context/brand/`, `context/campaign/`, `context/references/`
- `.claude/commands/` con i comandi `/pm-*`
- `output/`

Per ogni elemento mancante: elenca cosa manca con il fix. Non creare brand context fittizio.

## Step 2 — Verifica tool di sistema
Controlla in parallelo: `node` (20+), `python3` (3.12+), `gh` CLI, `ffmpeg`, Playwright Chromium. Per ogni mancante proponi l'installazione (Homebrew su macOS). Esegui tu l'install se l'utente conferma.

## Step 3 — Verifica MCP
Leggi `.mcp.json` (o config equivalente) e conferma che siano wired:
- Google Ads MCP (MCC `5524890329`) — `mcp__google-ads__*`
- SimilarWeb, Lenny's Data, Canva, Higgsfield, fal.ai, Apify, Gmail, Drive, Calendar, Slack, n8n, Playwright
Segnala quelli ⚠️ da configurare (es. Meta Ads MCP — solo claude.ai web).

## Step 4 — API key
Lancia (o verifica) in sequenza:
- `/pm-setup-apify` → Apify token (per `/pm-competitor-spy`, `/pm-ugc-analysis`)
- `/pm-setup-fal-ai` → Fal AI key (per generazione immagini/video)

## Step 5 — Verifica comandi /pm-*
Elenca i comandi in `.claude/commands/` e mappa ognuno alla sua skill nativa. Segnala comandi orfani (skill mancante) o skill senza comando.

## Step 6 — Riepilogo
Stampa una tabella: componente | stato (✅/⚠️/❌) | fix. Chiudi con: "Sistema pronto. Compila `context/campaign/brief.md` e lancia: 'Lancia pipeline performance marketing per [BRAND]'."

## Per riprodurre da zero su nuova macchina
Clona/copia la cartella progetto, apri Claude Code nella root, lancia `/pm-setup`. Gli step 1-6 ricostruiscono struttura, tool, MCP e key.
