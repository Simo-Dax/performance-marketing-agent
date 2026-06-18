---
description: Layout component carousel/slider per landing page — quando usarlo vs grid/list/masonry, accessibilità (keyboard, screen reader, touch target), performance (lazy load, CLS), SEO (contenuto nel DOM). Skill 42 (SA6/Post-SA7).
argument-hint: [caso d'uso: testimonial|gallery|logo|featured]
---

# /pm-carousel — Carousel Layout (SA6 / Post-SA7)

Esegui la skill **`directives/skills/42_carousel/SKILL.md`**.

Argomenti: $ARGUMENTS

## Cosa fare
1. Leggi e segui `directives/skills/42_carousel/SKILL.md`.
2. Verifica prima se il carousel è la scelta giusta: spazio limitato + un focus alla volta + rotazione (testimonial, citazioni, logo, gallery). Se serve confronto/browse di molti elementi → suggerisci grid/list/masonry.
3. Applica le best practice obbligatorie:
   - **Accessibilità:** navigazione tastiera, controllo utente (pausa, no auto-advance se `prefers-reduced-motion`), annunci slide ("Slide 2 di 5"), touch target ≥44×44px.
   - **Performance:** lazy load slide off-screen, riserva spazio (evita CLS).
   - **SEO:** tutto il contenuto nel DOM al load (Google non simula click) → server-render le slide, CSS/JS solo per mostrare/nascondere.
4. Se il carousel è dentro una landing page → coordina con `29_landing_page` (`/pm-landing-page`).
5. Output: componente carousel (HTML/CSS/JS) integrato nella landing, conforme ai vincoli accessibilità + SEO.
