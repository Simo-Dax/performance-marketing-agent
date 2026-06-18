# Advanced Copywriting — README

## Skill Disponibili

### 1. `meta-ads-copy/` — Meta Ads Copywriter
**Usa questa skill per**: scrivere copy Meta Ads (Facebook + Instagram) in italiano.
**Attiva quando**: l'utente chiede copy per Meta Ads, Facebook Ads, Instagram Ads, varianti di annunci, headline alternatives, funnel-based ad sets, o copy con framework PAS/AIDA/BAB/4Ps per paid social.

**Produce:**
- Full funnel set (9 ads: 3 varianti × 3 fasi Awareness/Consideration/Conversion)
- Single funnel stage (3 varianti per una fase specifica)
- Framework-based ads (PAS, AIDA, BAB, 4Ps)
- Behavioral principle ads (authority, social proof, scarcity, urgency)
- Angle-based ads (pain points, desires, USPs, FAQ, benefits, objections)
- Remarketing ads
- Headline alternatives (3 per ad)
- Meta Ads headlines (5 per slot)

**Reference files inclusi:** `references/copy-frameworks.md`, `references/headline-formulas.md`, `references/behavioral-principles.md`

---

### 2. `google-ads-copy/` — Google Ads RSA Generator
**Usa questa skill per**: scrivere copy Google Search Ads (RSA) in italiano o altra lingua.
**Attiva quando**: l'utente chiede copy per Google Ads, search ad text, RSA headlines o descriptions, o advertising copy per paid search.

**Produce (output strutturato RSA completo):**
- 15 Headline Standard (max 30 char): Keyword Focus (3), Benefits (5), USP (3), Desire (2), Bonus (1), Guarantee (1)
- 1 Headline Lunga (max 90 char)
- 4 Description (max 90 char): USP Focus (2), Scarcity & Urgency (2)
- Note per revisione A/B testing

---

### 3. `SKILL Advanced Copywriting.md` — Framework Copywriting Generale
**Usa questa skill per**: copy landing page, homepage, pricing page, feature page, sales page.
**Attiva quando**: l'utente chiede copy per pagine web (non ads).

**Formule**: AIDA, PAS, BAB, FAB, 4 U's.
**Template**: Hero, Social Proof, Features, How It Works, FAQ, Pricing, Final CTA.

---

## Routing Rapido

| Tipo di copy | Skill da usare |
|---|---|
| Meta Ads / Facebook / Instagram Ads | `meta-ads-copy/SKILL.md` |
| Google Search Ads / RSA | `google-ads-copy/SKILL.md` |
| Landing page / Homepage / Pricing | `SKILL Advanced Copywriting.md` |
| Headline optimization (qualsiasi) | `../02_headline_optimization.md` |
| QA finale copy | `../03_editing_selfcheck.md` |

---

## Integration

1. Ricevi strategia da SA3 (PM Strategist) — targeting, posizionamento, KPI
2. Ricevi angoli creativi da SA4 (Creative Concepts)
3. Attiva la skill appropriata in base al canale
4. Combina con `../09_marketing_psychology/` per leve psicologiche
5. Self-check finale con `../03_editing_selfcheck.md`
6. **Nota**: Entrambe le skill ads indicano di rivedere l'output con la skill "Humanizer" per eliminare linguaggio AI.
