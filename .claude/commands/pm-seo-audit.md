---
description: Audit SEO tecnico + on-page + content quality — framework 5 priorità, findings Issue/Impact/Evidence/Fix/Priority, action plan ICE. Script seo_checker.py per check on-page automatici. Skill 40 (SA8/organico).
argument-hint: [url o dominio] [scope: full|technical|on-page|content]
---

# /pm-seo-audit — SEO Audit (SA8 / organico)

Esegui la skill **`directives/skills/40_seo_audit/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/40_seo_audit/SKILL.md`.
2. Valutazione iniziale: tipo di sito (da `context/brand/business_profile.md`), business goal SEO, keyword prioritarie, scope.
3. Applica il framework 5 priorità: Crawlability & Indexation → Fondamenta Tecniche → On-Page → Content Quality → Authority & Link (vedi `references/seo-audit-reference.md`).
4. Per check on-page automatici su un URL: lancia `python3 directives/skills/40_seo_audit/scripts/seo_checker.py --url <URL>` (title, meta, heading, alt, link ratio, word count, viewport → score 0-100).
5. Se serve leggere dati reali di performance/indicizzazione → usa la skill globale `google-search-console`.
6. Output: `output/reports/{data}_seo-audit/` — Executive Summary (3-5 bullet) + findings SEO Tecnica/On-Page/Content (formato Issue/Impact/Evidence/Fix/Priority) + Action Plan prioritizzato (Critico/Alto/Quick Win) + mappa keyword cannibalization.
7. Quick win sempre separate dalle raccomandazioni ad alto effort. Niente raccomandazioni senza evidenza. Se cliente-ready → passa da `03_editing_selfcheck`.
