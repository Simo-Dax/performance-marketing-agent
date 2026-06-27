# Self-Improvement Layer — Auto-ottimizzazione del sistema

Sistema con cui agenti e skill **migliorano nel tempo** sulla base del feedback dell'utente. L'orchestrator lo legge a inizio sessione; ogni agente/skill lo consulta prima di eseguire.

> Principio: il sistema non è statico. Ogni volta che l'utente dice "questo va bene / questo non va bene", quel giudizio diventa una regola durevole applicata al punto giusto. Niente feedback va perso, niente resta solo nella chat.

---

## I 3 livelli di auto-ottimizzazione

### 1. Livello PROCEDURALE (orchestrator)
Riguarda **come scorre la pipeline**: ordine fasi, gate, handoff, quando attivare cosa.
- Trigger: feedback su flusso ("salta sempre X", "chiedimi conferma prima di Y", "non partire con Z senza W").
- Dove si applica: `claude.md` (ruolo orchestrator), `directives/skill_orchestrator.md` (routing), o un gate nuovo.
- Esempio: "voglio sempre validare gli insight prima del financial" → già implementato come GATE 1.

### 2. Livello AGENTICO (sub-agent SA1-SA9)
Riguarda **il comportamento di un agente** specifico: cosa enfatizza, cosa evita, quale taglio dà all'output.
- Trigger: feedback su un agente ("SA1 deve sempre includere lo spend stimato", "SA4 è troppo generico sui budget").
- Dove si applica: il file `.claude/agents/saN_*.md` → sezione **"## Feedback applicato"** in coda (regole durature apprese).
- Più i memory di progetto (vedi sotto).

### 3. Livello SKILL (singola skill 01-51)
Riguarda **l'output di una skill** specifica: formato, regole, default.
- Trigger: feedback su una skill ("le headline di 28 sono troppo lunghe", "la landing 29 deve sempre avere la sezione FAQ").
- Dove si applica: il file `directives/skills/NN_*.md` → sezione **"## Feedback applicato"** in coda.

---

## Procedura operativa

### Cattura del feedback
Due modi:
1. **Inline** — l'utente dà feedback durante una run. L'agente/orchestrator lo riconosce ("questo non va bene perché…") e lo processa.
2. **Esplicito** — l'utente lancia `/pm-feedback "[testo]"` per registrare un feedback mirato.

### Classificazione (sempre)
Per ogni feedback, classifica:
- **Tipo**: `correzione` (qualcosa è sbagliato) / `conferma` (qualcosa è giusto, da mantenere) / `preferenza` (gusto/stile)
- **Livello**: procedurale / agentico / skill
- **Target esatto**: quale file (orchestrator / `.claude/agents/saN` / `skills/NN`)
- **Durata**: one-off (solo questa run) o durevole (regola permanente)

### Applicazione
1. Se **durevole** → scrivi la regola nella sezione "## Feedback applicato" del file target (agente o skill), in forma azionabile e concisa. Per il livello procedurale → aggiorna orchestrator/routing.
2. Registra SEMPRE nel log `directives/feedback_log.md` (append-only): data, target, feedback, tipo, azione.
3. Salva anche come **memory di progetto** di tipo `feedback` (sistema memory in `~/.claude/projects/.../memory/`) con **Why** + **How to apply**, così sopravvive cross-sessione.
4. Conferma all'utente cosa hai cambiato e dove.

### Consultazione (prima di eseguire)
- L'orchestrator legge `feedback_log.md` + i memory `feedback` a inizio pipeline.
- Ogni agente/skill, prima di produrre output, controlla la propria sezione "## Feedback applicato".

---

## Sezione "## Feedback applicato" — formato standard

Da aggiungere in coda al file agente/skill quando arriva un feedback durevole:

```markdown
## Feedback applicato
- [YYYY-MM-DD] [correzione/conferma/preferenza] — [regola azionabile]. (fonte: feedback utente)
```

Esempio in `.claude/agents/sa4_pm_strategist.md`:
```markdown
## Feedback applicato
- [2026-06-02] correzione — ogni campagna deve sempre indicare bid strategy esplicita, non solo budget. (fonte: feedback utente)
```

---

## Regole critiche

- **Nessun feedback resta in chat.** Diventa sempre regola su file + log + memory.
- **Una regola, un punto.** Procedurale → orchestrator; agentico → file agente; skill → file skill. Mai duplicare.
- **Azionabile, non vago.** "Migliora il copy" non è una regola. "Headline max 30 char per questo brand" sì.
- **Reversibile.** Se l'utente cambia idea, rimuovi/aggiorna la regola e logga il cambiamento.
- **Conferma sempre** cosa hai modificato e dove, così l'utente sa che il feedback è stato recepito.
