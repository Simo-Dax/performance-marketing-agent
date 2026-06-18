---
name: carousel
description: When the user wants to design, optimize, or audit carousel/slider layouts for content display. Also use when the user mentions "carousel," "slider," "carousel layout," "testimonial carousel," "gallery carousel," "quote carousel," "image slider," "carosello," "slider immagini," or "carousel accessibility." For hero-area patterns, use hero-generator.
metadata:
  version: 1.1.0
---

# Components: Carousel Layout

> **Agente:** SA6 (Asset Production) / Post-SA7 (landing page) — componente layout.
> **Quando:** scelta e progettazione di layout carousel/slider per landing page, sezioni testimonial, logo strip, gallery.

Guida alla progettazione di layout carousel (slider) per la visualizzazione sequenziale di contenuti. I carousel mostrano uno o pochi elementi alla volta; l'utente avanza con swipe o click. Ideali quando lo spazio è limitato e più elementi devono ruotare — testimonial, citazioni, logo, highlight di gallery.

**Quando invocata:** al **primo uso**, se utile, apri con 1-2 frasi su cosa copre la skill e perché conta, poi fornisci l'output principale. Ai **usi successivi** o se l'utente chiede di saltare, vai diretto all'output.

## Quando usare un Carousel

| Usa carousel quando | Usa grid/list quando |
|-------------------|---------------------|
| **Spazio limitato** | Catalogo intero visibile |
| Un focus alla volta; rotazione desiderata | Browse, confronto di molti elementi |
| Testimonial, citazioni, logo, gallery in evidenza | Prodotti, template, indice blog |
| Above the fold; hero o highlight di sezione | Listing completo; discovery |

Vedi **grid** per display a gerarchia uguale; **list** per scan testuale; **masonry** per gallery ad altezza variabile.

## Carousel vs Grid vs List vs Masonry

| Layout | Struttura | Ideale per |
|--------|-----------|------------|
| **Grid** | Righe e colonne uguali; tutto visibile | Prodotti, template, feature |
| **List** | Colonna singola; impilata | Indice blog, doc, risultati ricerca |
| **Masonry** | Colonne; altezze variabili | Gallery stile Pinterest |
| **Carousel** | Slide; uno/pochi visibili; swipe/click | Testimonial, logo, elementi in evidenza |

## Best Practice

### Accessibilità

- **Navigazione da tastiera:** frecce per spostarsi; Enter/Spazio per attivare; focus visibile
- **Controllo utente:** non auto-avanzare troppo veloce; permetti la pausa; evita l'auto-avanzamento se `prefers-reduced-motion` è impostato
- **Annunci:** gli utenti screen reader devono sapere la slide corrente e il totale (es. "Slide 2 di 5")
- **Touch target:** ≥44×44px per i pulsanti prev/next su mobile

### Performance

- **Lazy load:** carica le slide fuori schermo on demand; evita di caricare tutte le immagini subito
- **Riserva lo spazio:** riserva spazio per le slide per evitare layout shift (CLS)

### SEO

- **Contenuto nel DOM:** tutto il contenuto del carousel deve essere nell'HTML iniziale al caricamento pagina. Google non simula i click; il contenuto caricato via AJAX al cambio slide non è scopribile. Stesso vincolo di **tab-accordion**.
- **Raccomandazione:** server-render di tutte le slide nell'HTML; usa CSS/JS solo per mostrare/nascondere. Vedi **rendering-strategies**.

## Casi d'uso

| Caso d'uso | Formato | Page Skill |
|----------|--------|------------|
| **Testimonial** | Carousel di citazioni; più testimonial | **testimonials-generator** |
| **Showcase / Gallery** | Elementi in evidenza; rotazione | **showcase-page-generator** |
| **Logo stampa** | Strip logo "As Seen In" o carousel citazioni | **press-coverage-page-generator** |
| **Community** | Carousel banner sotto l'hero | **community-forum** |

## Skill correlate

- **grid:** Grid per catalogo completo; quando il carousel è troppo restrittivo
- **list:** List per scan testuale
- **masonry:** Masonry per gallery ad altezza variabile
- **card:** Struttura card dentro le slide del carousel
- **29_landing_page:** Carousel come componente dentro la landing page Meta
- **testimonials-generator:** Carousel testimonial; testimonial come contenuto
- **rendering-strategies:** SSR, SSG; contenuto nell'HTML iniziale per i crawler
