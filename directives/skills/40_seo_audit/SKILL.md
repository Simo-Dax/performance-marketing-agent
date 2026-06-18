---
name: "seo-audit"
description: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," "audit SEO," "SEO tecnica," or "SEO health check." For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema-markup.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---

# SEO Audit

> **Agente:** SA8 (Analytics & Reporting) — area organica/SEO, affianca `36_google_ads_audit`.
> **Output:** report di audit SEO cliente-ready in `output/reports/{YYYY-MM-DD}_seo-audit/`.
> **Tool correlati:** skill globale `google-search-console`, `41_seo_content_optimizer`.

Sei un esperto di search engine optimization. L'obiettivo è identificare i problemi SEO e fornire raccomandazioni azionabili per migliorare la performance di ricerca organica.

## Valutazione Iniziale

**Controlla prima il contesto di marketing del prodotto:**
Se esiste `context/brand/business_profile.md` (o `.claude/product-marketing-context.md`), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche del task.

Prima dell'audit, comprendi:

1. **Contesto del Sito**
   - Che tipo di sito? (SaaS, e-commerce, blog, ecc.)
   - Qual è il business goal primario per la SEO?
   - Quali keyword/topic sono prioritari?

2. **Stato Attuale**
   - Problemi o preoccupazioni note?
   - Livello di traffico organico attuale?
   - Cambiamenti o migrazioni recenti?

3. **Scope**
   - Audit completo del sito o pagine specifiche?
   - Tecnico + on-page, o un'area di focus singola?
   - Accesso a Search Console / analytics?

---

## Framework di Audit
→ Vedi `references/seo-audit-reference.md` per i dettagli.
→ Script opzionale: `scripts/seo_checker.py` esegue check automatici on-page (title, meta, heading, alt, ecc.) su un URL.

## Formato Output

### Struttura del Report di Audit

**Executive Summary**
- Valutazione generale dello stato di salute
- Top 3-5 problemi prioritari
- Quick win identificate

**Findings SEO Tecnica**
Per ogni problema:
- **Issue:** cosa non va
- **Impact:** impatto SEO (Alto/Medio/Basso)
- **Evidence:** come l'hai trovato
- **Fix:** raccomandazione specifica
- **Priority:** 1-5 o Alta/Media/Bassa

**Findings SEO On-Page**
Stesso formato di sopra

**Findings sui Contenuti**
Stesso formato di sopra

**Action Plan Prioritizzato**
1. Fix critici (bloccano indicizzazione/ranking)
2. Miglioramenti ad alto impatto
3. Quick win (facili, beneficio immediato)
4. Raccomandazioni a lungo termine

---

## Tool Referenziati

**Tool Gratuiti**
- Google Search Console (essenziale)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test
- Mobile-Friendly Test
- Schema Validator

**Tool a Pagamento** (se disponibili)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Domande Specifiche del Task

1. Quali pagine/keyword contano di più?
2. Hai accesso a Search Console?
3. Cambiamenti o migrazioni recenti?
4. Chi sono i tuoi top competitor organici?
5. Qual è il baseline attuale di traffico organico?

---

## Skill Correlate

- **41_seo_content_optimizer** — QUANDO: l'utente vuole ottimizzare un singolo contenuto/articolo per la ricerca dopo che l'audit ha identificato gap. QUANDO NO: non per la diagnosi tecnica generale del sito.
- **google-search-console** (globale) — QUANDO: serve leggere dati reali di performance, indicizzazione, query. QUANDO NO: per problemi puramente di crawl che non richiedono dati GSC.
- **29_landing_page** — QUANDO: l'audit rivela problemi sulle landing page prodotte. QUANDO NO: per audit tecnico crawl/indexation.
- **34_editorial_content_plan** — QUANDO: l'audit rivela contenuti thin, gap di keyword o mancanza di autorità topica che richiedono un piano editoriale. QUANDO NO: quando il problema è puramente tecnico (robots.txt, redirect, velocità).

---

## Comunicazione

Tutto l'output di audit segue lo **standard di qualità SEO Audit**:
- Apri con l'executive summary (massimo 3-5 bullet)
- I findings usano il formato Issue / Impact / Evidence / Fix / Priority in modo consistente
- L'Action Plan Prioritizzato è sempre la sezione finale del deliverable
- Evita gergo senza spiegazione; scrivi per un lettore tecnicamente consapevole ma non specialista SEO
- Le quick win sono indicate esplicitamente e tenute separate dalle raccomandazioni ad alto effort
- Non presentare mai raccomandazioni senza evidenza o rationale

---

## Trigger Proattivi

Fai emergere automaticamente raccomandazioni di seo-audit quando:

1. **Calo di traffico citato** — l'utente dice che il traffico organico è calato o i ranking sono scesi; inquadra subito lo scope di un audit.
2. **Migrazione o redesign del sito** — l'utente menziona un cambio URL, switch di piattaforma o redesign pianificato o recente; segnala i bisogni di audit pre/post-migrazione.
3. **"Perché la mia pagina non si posiziona?"** — qualsiasi frustrazione sul ranking attiva la checklist on-page + intent prima dei fattori esterni.
4. **Discussione di content strategy** — quando la skill di content plan è attiva ed emergono gap di keyword, suggerisci proattivamente un audit SEO per validare l'opportunità.
5. **Nuovo sito o lancio prodotto** — l'utente prepara un lancio; raccomanda proattivamente una checklist SEO tecnica pre-lancio dal framework di audit.

---

## Output Artifact

| Artifact | Formato | Descrizione |
|----------|--------|-------------|
| Executive Summary | Bullet markdown | Top 3-5 problemi + quick win, adatto alla condivisione con gli stakeholder |
| Findings SEO Tecnica | Tabella strutturata | Issue / Impact / Evidence / Fix / Priority per finding |
| Findings SEO On-Page | Tabella strutturata | Stesso formato, focalizzato su contenuto e metadata |
| Action Plan Prioritizzato | Lista numerata | Ordinato per impatto × effort, raggruppato in Critico / Alto / Quick Win |
| Mappa Keyword Cannibalization | Tabella | Pagine in competizione per la stessa keyword con azioni canonical o redirect raccomandate |
