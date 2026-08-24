---
description: Before/After UGC video ad (15-24s). Due stati della stessa cosa, confrontati sotto condizioni identiche. Skill nativa 62_ugc_formats (SA6).
argument-hint: [prodotto/concept] — opzionale, altrimenti parte dal Brand DNA e dalla VOC
---

# /pm-ugc-before-after — Before/After

Esegui la skill nativa **`directives/skills/62_ugc_formats/SKILL.md`** (SA6 — Asset Production), formato **before-after**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Carica il playbook del formato: `directives/skills/62_ugc_formats/formats/before-after/playbook.md`, più `format-spec.md` e `shot-vocabulary.md` della stessa cartella.
2. Le 10 coppie di studio stanno in `formats/before-after/recreation-prompts/` — `anchor/` (fermo immagine) e `video/` (movimento). Sono ad **reali** di questo formato, smontate shot by shot. Banco di studio, non template da copiare.
3. Motori condivisi: `directives/skills/_shared/ugc_format_contract.md` · `ugc_script_engine.md` · `ugc_image_engine.md` · `ugc_video_engine.md` · `ugc_run_engine.md` · `natural_voice.md`.
4. **Lo split dei due modelli è la regola centrale:** l'LLM scrive cosa l'ad È (chi, la stanza, il prodotto fino al carattere sull'etichetta, ogni parola detta) e poi si toglie di mezzo. Il **modello video dirige**. **Non scrivere una shot list** — è esattamente ciò che fa sembrare AI le ad AI.
5. **Specifico di questo formato:** **Avviso piattaforma:** su dimagrimento, salute e beauty Meta limita le immagini prima/dopo. Dillo prima di produrre. Condizioni identiche o il confronto è disonesto.

## I tre gate
| Gate | Cosa | Costo |
|---|---|---|
| **1 — IL PIANO** | Script riga per riga + forma dell'ad in frasi piane (non una shot list) + prompt dell'anchor. Poi FERMATI. | Gratis |
| **2 — ANCHOR** | Permesso di renderizzare il fermo immagine. | Costa |
| **3 — VIDEO** | Prompt assemblato + anchor approvato + prezzo esatto. Poi aspetta. | Costa |

**Legge della spesa:** niente che costi si genera senza un sì chiaro, specifico e immediatamente precedente. Ogni retry è una nuova spesa e vuole il suo sì.

## Chiusura
Una ad per run. Render: Higgsfield (Path B), altrimenti fal.ai (Path C), altrimenti Path A (consegni il prompt). **Non esiste Path K.**

A ad finita **offri le caption** (`/pm-captions`): lo script è su disco, quindi escono allineate al copy parola per parola.

Output: `05_UGC_Prompts/formats/before-after/<concept>/`
