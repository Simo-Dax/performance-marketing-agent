# seo-audit reference

> Terminologia tecnica SEO mantenuta in inglese (standard di settore); descrizioni e istruzioni in italiano.

## Framework di Audit

### Ordine di Priorità
1. **Crawlability & Indexation** (Google riesce a trovarlo e indicizzarlo?)
2. **Fondamenta Tecniche** (il sito è veloce e funzionale?)
3. **On-Page Optimization** (il contenuto è ottimizzato?)
4. **Qualità del Contenuto** (merita di posizionarsi?)
5. **Authority & Link** (ha credibilità?)

---

## Audit SEO Tecnica

### Crawlability

**Robots.txt**
- Controlla blocchi non intenzionali
- Verifica che le pagine importanti siano permesse
- Controlla il riferimento alla sitemap

**XML Sitemap**
- Esiste ed è accessibile
- Inviata a Search Console
- Contiene solo URL canonical e indicizzabili
- Aggiornata regolarmente
- Formattazione corretta

**Site Architecture**
- Pagine importanti entro 3 click dalla homepage
- Gerarchia logica
- Struttura di internal linking
- Nessuna orphan page

**Problemi di Crawl Budget** (per siti grandi)
- URL parametrizzati sotto controllo
- Faceted navigation gestita correttamente
- Infinite scroll con fallback di paginazione
- Session ID non negli URL

### Indexation

**Index Status**
- Check `site:domain.com`
- Coverage report di Search Console
- Confronta indicizzate vs attese

**Problemi di Indexation**
- Tag noindex su pagine importanti
- Canonical che puntano nella direzione sbagliata
- Catene/loop di redirect
- Soft 404
- Contenuto duplicato senza canonical

**Canonicalization**
- Tutte le pagine hanno tag canonical
- Canonical self-referencing su pagine uniche
- Canonical HTTP → HTTPS
- Coerenza www vs non-www
- Coerenza trailing slash

### Site Speed & Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Fattori di Velocità**
- Tempo di risposta server (TTFB)
- Ottimizzazione immagini
- Esecuzione JavaScript
- Delivery CSS
- Header di caching
- Uso di CDN
- Caricamento font

**Tool**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Report Core Web Vitals di Search Console

### Mobile-Friendliness

- Design responsive (non sito m. separato)
- Dimensioni dei tap target
- Viewport configurato
- Nessuno scroll orizzontale
- Stesso contenuto del desktop
- Pronto per mobile-first indexing

### Sicurezza & HTTPS

- HTTPS su tutto il sito
- Certificato SSL valido
- Nessun mixed content
- Redirect HTTP → HTTPS
- Header HSTS (bonus)

### Struttura URL

- URL leggibili e descrittivi
- Keyword negli URL dove naturale
- Struttura coerente
- Nessun parametro non necessario
- Lowercase e separati da trattini

---

## Audit SEO On-Page

### Title Tag

**Controlla:**
- Title unici per ogni pagina
- Keyword primaria vicino all'inizio
- 50-60 caratteri (visibili in SERP)
- Convincenti e cliccabili
- Posizionamento del brand name (in fondo, di solito)

**Problemi comuni:**
- Title duplicati
- Troppo lunghi (troncati)
- Troppo corti (opportunità sprecata)
- Keyword stuffing
- Mancanti del tutto

### Meta Description

**Controlla:**
- Description uniche per pagina
- 150-160 caratteri
- Include la keyword primaria
- Value proposition chiara
- Call to action

**Problemi comuni:**
- Description duplicate
- Spazzatura auto-generata
- Troppo lunghe/corte
- Nessuna ragione convincente per cliccare

### Heading Structure

**Controlla:**
- Un H1 per pagina
- H1 contiene la keyword primaria
- Gerarchia logica (H1 → H2 → H3)
- Gli heading descrivono il contenuto
- Non solo per lo styling

**Problemi comuni:**
- Più H1
- Salto di livelli (H1 → H3)
- Heading usati solo per styling
- Nessun H1 sulla pagina

### Ottimizzazione Contenuto

**Contenuto Pagina Principale**
- Keyword nelle prime 100 parole
- Keyword correlate usate naturalmente
- Profondità/lunghezza sufficiente per il topic
- Risponde al search intent
- Migliore dei competitor

**Problemi di Thin Content**
- Pagine con poco contenuto unico
- Pagine tag/categoria senza valore
- Doorway page
- Contenuto duplicato o quasi-duplicato

### Ottimizzazione Immagini

**Controlla:**
- Nomi file descrittivi
- Alt text su tutte le immagini
- L'alt text descrive l'immagine
- File compressi
- Formati moderni (WebP)
- Lazy loading implementato
- Immagini responsive

### Internal Linking

**Controlla:**
- Pagine importanti ben linkate
- Anchor text descrittivo
- Relazioni di link logiche
- Nessun internal link rotto
- Numero di link ragionevole per pagina

**Problemi comuni:**
- Orphan page (nessun internal link)
- Anchor text sovra-ottimizzato
- Pagine importanti sepolte
- Link eccessivi in footer/sidebar

### Keyword Targeting

**Per Pagina**
- Target di keyword primaria chiaro
- Title, H1, URL allineati
- Il contenuto soddisfa il search intent
- Non in competizione con altre pagine (cannibalization)

**A Livello di Sito**
- Documento di keyword mapping
- Nessun gap importante nella copertura
- Nessuna keyword cannibalization
- Cluster topici logici

---

## Valutazione Qualità del Contenuto

### Segnali E-E-A-T

**Experience**
- Esperienza diretta dimostrata
- Insight/dati originali
- Esempi reali e case study

**Expertise**
- Credenziali dell'autore visibili
- Informazione accurata e dettagliata
- Affermazioni con fonti corrette

**Authoritativeness**
- Riconosciuto nel settore
- Citato da altri
- Credenziali di settore

**Trustworthiness**
- Informazione accurata
- Trasparente sul business
- Informazioni di contatto disponibili
- Privacy policy, termini
- Sito sicuro (HTTPS)

### Profondità del Contenuto

- Copertura completa del topic
- Risponde alle domande di follow-up
- Migliore dei competitor top-ranking
- Aggiornato e attuale

### Segnali di Engagement Utente

- Tempo sulla pagina
- Bounce rate nel contesto
- Pagine per sessione
- Visite di ritorno

---

## Problemi Comuni per Tipo di Sito

### Siti SaaS/Prodotto
- Le pagine prodotto mancano di profondità di contenuto
- Blog non integrato con le pagine prodotto
- Mancano pagine comparison/alternative
- Pagine feature thin di contenuto
- Nessun contenuto glossary/educativo

### E-commerce
- Pagine categoria thin
- Descrizioni prodotto duplicate
- Schema prodotto mancante
- Faceted navigation che crea duplicati
- Pagine out-of-stock gestite male

### Siti Content/Blog
- Contenuto datato non aggiornato
- Keyword cannibalization
- Nessun clustering topico
- Internal linking scarso
- Pagine autore mancanti

### Business Locale
- NAP incoerente
- Schema local mancante
- Nessuna ottimizzazione Google Business Profile
- Pagine località mancanti
- Nessun contenuto locale

---
