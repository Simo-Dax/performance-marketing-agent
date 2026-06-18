---
name: email-creation
description: >
  Write email/newsletter copy: subject lines (A/B), preview text, body, and CTA — in brand tone of voice, anti-AI,
  for a specific RFM segment and automation/broadcast goal. Use when the user wants to write an email, newsletter,
  email copy, automation flow copy, or a campaign email. Also trigger on "scrivi email", "copy email", "newsletter",
  "email per [segmento]", "welcome email", "win-back email", "abandoned cart email", "email copy". Can draft via Gmail MCP.
---

# Email Creation — SA9

> **Agente:** SA9 (CRM/Lifecycle). Quarta funzione del flusso CRM.
> **Input:** strategia email (`45`) + segmento target (`44`) + `tone_of_voice.md` + `anti_ai_writing_style.md` + insight (`33`).
> **Output:** file copy email in `12_Email/` (sottocartella campagna) o draft via Gmail MCP.

Scrive **copy email pronto** per uno specifico segmento e obiettivo: subject A/B + preview + body + CTA. Voce del brand, anti-AI. Non scrive email generiche: ogni email parte da un segmento e un goal.

---

## Input minimi (auto-discovery)

| Input | Fonte | Se manca |
|-------|-------|----------|
| Obiettivo email + flow | `45_email_strategy` o richiesta utente | chiedi |
| Segmento target | `44_rfm_segments` | assumi "tutti gli inviabili" e dichiaralo |
| Tone of voice | `context/brand/tone_of_voice.md` | usa neutro brand-safe e segnala |
| Regole anti-AI | `context/brand/anti_ai_writing_style.md` | applica le agnostiche |
| Pain/desideri/obiezioni | `intermediate/insight.md` (`33`) | usa il prodotto/offerta dal brief |
| Offerta/prodotto | brief / `business_profile.md` | chiedi |

---

## Anatomia email (struttura output)

Per ogni email produci:

### 1. Subject line — 5 varianti A/B
- Max ~45 caratteri (mobile-safe), front-load la parola chiave
- Mix di leve: curiosità, beneficio, urgenza, personalizzazione, domanda
- Niente clickbait che il body non mantiene → danneggia trust + deliverability
- Evita spam trigger (TUTTO MAIUSCOLO, "GRATIS!!!", troppi emoji)

### 2. Preview text (preheader) — 2 varianti
- 35-90 caratteri, completa il subject (non ripeterlo)
- È il secondo hook nell'inbox

### 3. Body
Struttura per tipo, sempre **hook → valore → proof → CTA singola**:
- **Hook:** prima riga = continua il subject, aggancia in 1 frase. Niente "Spero che questa email ti trovi bene".
- **Valore/storia:** corpo centrale, ToV del brand, una sola idea per email
- **Proof:** recensione, dato, social proof (verbatim VOC se disponibile)
- **CTA:** una sola, chiara, sopra e sotto la piega. Bottone + link testuale.

### 4. CTA copy
3 varianti di microcopy bottone (azione + beneficio, non "Clicca qui").

---

## Copy per tipo di email (linee guida rapide)

| Tipo | Hook | Focus | CTA |
|------|------|-------|-----|
| **Welcome** | benvenuto + cosa aspettarsi | brand story, primo valore | scopri / primo acquisto |
| **Abandoned cart** | "hai lasciato qualcosa" | rimuovi attrito, urgenza soft, no sconto subito | completa ordine |
| **Post-purchase** | conferma + cosa succede ora | onboarding prodotto, recensione | usa / recensisci |
| **Win-back** | "ci manchi" + novità | ragione per tornare, eventuale incentivo | torna / riscatta |
| **VIP** | riconoscimento status | reward esclusivo, early access | accedi / referral |
| **Newsletter** | hook editoriale | valore (70%), una idea | leggi / approfondisci |
| **SaaS onboarding** | next step chiaro | activation, un'azione | completa setup |

---

## Anti-AI (obbligatorio)

Applica `anti_ai_writing_style.md`. In più, per email:
- Niente "In un mondo dove…", "Immagina di…", "Non è solo X, è Y"
- Niente em-dash a raffica, niente liste di tre aggettivi
- Frasi brevi, ritmo parlato, leggibile a voce
- Una sola idea per email — non impacchettare 4 messaggi
- Scrivi come una persona del brand a un cliente, non come un'azienda a una lista

---

## Output

Per ogni email, un blocco markdown (o file in `12_Email/{flow}_{nome}.md`):

```markdown
# Email — {Flow} — {Segmento} — {Obiettivo}

**Segmento:** [...] | **Trigger/Invio:** [...] | **KPI atteso:** [...]

## Subject (A/B — 5)
1. ...  (X char)
...

## Preview text (2)
1. ...

## Body
[testo completo, formattato]

## CTA (3 varianti microcopy)
1. ...

## Note invio
- Personalizzazione: [first_name, prodotto, ...]
- Segmento di esclusione: [...]
```

### Draft reale (opzionale)
- **Klaviyo MCP** (se configurato via `/pm-setup-klaviyo` con `READ_ONLY=false`): crea direttamente campaign/template in Klaviyo con il copy prodotto. Fonte preferita per brand su Klaviyo.
- **Gmail MCP** (`mcp__claude_ai_Gmail__create_draft`): draft one-off con subject scelto + body, quando non c'è ESP collegato.
- **Mailchimp/altri ESP:** esporta il copy formattato (MCP non ancora configurato).

---

## Handoff
→ QA copy: passa da `03_editing_selfcheck` (modalità voice-editor brand) prima della consegna.
→ Metti i risultati di invio (open/CTR/revenue) a disposizione di **SA8** per il reporting email.

> Una email = un segmento + un obiettivo + una CTA. Se stai scrivendo per "tutti" con 3 CTA, fermati e torna a `44`/`45`.

---

## 🧹 Anti-AI gate (`49_anti_ai_slop`) — OBBLIGATORIO prima di consegnare il copy
Ogni testo prodotto da questa skill passa la gate **`49_anti_ai_slop`** prima dell'handoff:
- Rimuovi forbidden words/patterns EN (canonico in `directives/skills/49_anti_ai_slop/references/`).
- Per copy in **italiano**: applica ANCHE `context/brand/anti_ai_writing_style.md` (regola del tre, "inoltre/fondamentale/approfondire", trattino lungo come pausa, ecc.) + il tone of voice del brand. I due layer si sommano.
- Check rapido via CLI: `python3 -m anti_ai_slop.cli words <file>` e `dashes <file>` (da `49_anti_ai_slop/scripts/`).
- Regola: nessun tell EN **né** IT deve sopravvivere nel copy finale.
