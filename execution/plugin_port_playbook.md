# Playbook — Portare aggiornamenti da un plugin esterno alle skill native

Procedura ripetibile per quando un plugin di terze parti (installato **solo come reference locale**, mai come dipendenza runtime) rilascia aggiornamenti utili. Due fasi: **estrazione** (leggere cosa è cambiato nel plugin) e **ricostruzione** (riscrivere l'equivalente dentro la nostra struttura sub-agent/skill). **Nessun riferimento al plugin sorgente deve finire nei file del repo** — né nel nome, né nel testo, né nei commenti.

---

## Fase 1 — Estrazione dalla cartella plugin

1. **Localizza il clone locale del plugin.**
   ```bash
   find ~/.claude/plugins/marketplaces -maxdepth 1 -type d
   ```
   Ogni plugin di terze parti installato come marketplace ha un clone git in `~/.claude/plugins/marketplaces/<nome-plugin>/`.

2. **Verifica la versione installata vs upstream.**
   ```bash
   cd ~/.claude/plugins/marketplaces/<nome-plugin>
   cat .claude-plugin/plugin.json | grep version   # versione locale
   git fetch origin --tags                         # scarica gli aggiornamenti senza toccare il working tree
   git log --oneline origin/main -30                # changelog upstream
   ```
   Il fetch NON modifica il checkout locale (nessun checkout/reset) — sicuro da eseguire sempre.

3. **Identifica i commit/tag rilevanti** per l'area che ti interessa (es. "spy", "copy", "static"):
   ```bash
   git log --oneline origin/main -- skills/<area-correlata>
   ```

4. **Leggi il contenuto a quel punto della storia SENZA checkout** (il clone potrebbe essere condiviso da altri progetti — mai `git checkout`/`git reset --hard` su di esso):
   ```bash
   git ls-tree -r --name-only origin/main -- skills/ | grep -i <area>
   git show origin/main:skills/<skill-name>/SKILL.md > /tmp/latest-<skill>.md
   git diff <vecchio-tag> origin/main -- skills/<area>   # per vedere solo cosa è cambiato
   ```

5. **Leggi il file estratto per intero** (non solo il diff) — capisci: cosa fa, quali tool/MCP/servizi esterni usa, quale schema di output produce, quali sono le regole hard (mai fare X, sempre fare Y).

---

## Fase 2 — Ricostruzione nella nostra struttura

6. **Mappa la funzione al sub-agente corretto** (SA1-SA9) e decidi il numero di skill nativa: prossimo numero libero in `directives/skills/` (`ls directives/skills/ | sort -t_ -k1 -n | tail`).

7. **Riscrivi da zero in italiano**, seguendo lo stile e le sezioni delle skill native esistenti (Step 0 prerequisiti → Step 0.5 protezione cartella → Step N raccolta input → ... → Step finale riepilogo). Non tradurre riga-per-riga: adatta.

8. **Sostituisci ogni dipendenza specifica del plugin con l'infrastruttura nostra:**
   - Path di config/token → i nostri (`~/.config/pm-agent/*.env`, non i percorsi del plugin)
   - Tool locali pesanti (venv Python, install one-off) → preferisci un MCP già configurato nel progetto (fal.ai, Higgsfield, Apify) se copre lo stesso bisogno — meno dipendenze da installare, coerente con l'architettura "MCP propri"
   - Nomi comandi/skill del plugin → convenzione nostra (`/pm-*`, `NN_nome_skill`)
   - Cartelle output del plugin → le nostre (`03_Ad_Spy/`, `intermediate/`, ecc. — vedi convenzione output in `claude.md`)

9. **Elimina ogni riferimento testuale al plugin sorgente**: nome del plugin, nome dell'autore, URL del repository, nomi di skill/comandi con il prefisso del plugin. Il file risultante deve leggersi come se fosse sempre stato nostro. Grep di verifica prima di salvare:
   ```bash
   grep -rniE "<nome-plugin>|<nome-autore>" directives/ .claude/ claude.md
   ```
   Deve restituire zero risultati nei file nuovi/modificati.

10. **Aggiorna tutti i punti di aggancio** (non basta il file della skill):
    - `.claude/agents/saN_*.md` — aggiungi la skill alla sezione "Skill native da attivare" + eventuali FASE/tool list rilevanti
    - `claude.md` — sezione "Skills Disponibili" (riga descrittiva) + mappa cartelle output se serve una sottocartella nuova
    - `directives/skill_orchestrator.md` — tabella skill, tabella comandi, checklist "internalizzate"
    - `.claude/commands/pm-*.md` — nuovo comando wrapper se la skill è invocabile standalone
    - comandi di setup (`pm-setup-*.md`) se la skill introduce una nuova dipendenza da credenziale

11. **Verifica di coerenza incrociata**: se la nuova skill è "sorella" di una esistente (stesso dominio, media diverso — es. static vs video), controlla che entrambe usino lo stesso Design System/HTML palette/convenzioni, non due stili diversi per caso.

12. **Registra il port in memoria** (non nel repo): aggiorna il file di memoria dedicato ai port upstream con — cosa è stato portato, quali adattamenti sono stati fatti rispetto all'originale (e perché), cosa resta da valutare, il tag/commit upstream raggiunto dal fetch. Questo tiene la provenance fuori dal repo ma recuperabile per port futuri.

---

## Regola di fondo

Il plugin di terze parti è **solo materiale di lettura** per capire una funzionalità. Il codice/testo che finisce nel repo è sempre riscritto, mai copiato verbatim con branding del plugin, e mai dipendente a runtime dal plugin stesso (niente `.mcp.json` che punta a server del plugin, niente import di suoi script). Se un blocco di codice è meccanico e privo di branding (es. uno script Python di puro parsing JSON), può essere adattato quasi 1:1 — ma va comunque passato attraverso i punti 8-9 sopra.
