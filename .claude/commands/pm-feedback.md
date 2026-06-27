---
description: Registra un feedback e lo applica come regola durevole al punto giusto (orchestrator/agente/skill) + log + memory. Layer di self-improvement.
argument-hint: ["testo del feedback"]
---

# /pm-feedback — Registra e applica feedback

Esegui la procedura **`directives/self_improvement.md`**.

Feedback: $ARGUMENTS

## Cosa fare
1. Leggi `directives/self_improvement.md`.
2. **Classifica** il feedback: tipo (correzione/conferma/preferenza), livello (procedurale/agentico/skill), target esatto (orchestrator / `.claude/agents/saN` / `skills/NN`), durata (one-off/durevole).
3. Se manca contesto (a quale agente/skill si riferisce), chiedi una sola domanda mirata.
4. **Proponi la modifica** concreta all'utente (quale file, quale regola). Attendi OK.
5. Su conferma:
   - Scrivi la regola nella sezione "## Feedback applicato" del file target (o aggiorna orchestrator/routing se procedurale).
   - Aggiungi una riga in cima a `directives/feedback_log.md`.
   - Salva un memory di progetto tipo `feedback` (con Why + How to apply).
6. Conferma cosa hai cambiato e dove.

## Regole
- Nessun feedback resta solo in chat. Sempre: file + log + memory.
- Azionabile, non vago. Reversibile se l'utente cambia idea.
