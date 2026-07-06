# SA1 — Ad Spy 2.0 (Competitor Intelligence)

**Agente:** SA1 (Competitor Analysis)
**Output:** `03_Ad_Spy/adspy-[brand]-[YYYYMMDD].html` + `competitors.json`
**Prerequisiti:** Apify API key configurata

---

## Tre modalità di input

| Input | Esempio | Modalità |
|---|---|---|
| Brand singolo | `Huel`, `facebook.com/huel` | brand mode → 1 swipe file |
| Lista brand | `Huel, Soylent, Ka'Chava` | list mode → N swipe file in parallelo |
| Nicchia/keyword | `protein powder`, `DTC skincare` | niche mode → ricerca 10 competitor → N swipe file |

---

## Step 0 — Token Apify (REST diretto, no MCP)

Questa skill scrapa il Meta Ad Library via **Apify REST API diretta** (allineato all'upstream v2.0: niente MCP — gli actor via MCP laggano). **Non chiamare alcun `mcp__apify__*`.**

```bash
# Token Apify dalla config locale (scritta da /pm-setup-apify), fallback su env
[ -f ~/.config/pm-agent/apify.env ] && . ~/.config/pm-agent/apify.env
TOKEN="${APIFY_TOKEN:-}"
```

Se `TOKEN` vuoto → chiedi di eseguire `/pm-setup-apify` e fermati. Token SEMPRE come header `Authorization: Bearer`, **mai in URL**. Non procedere senza token.

---

## Step 0.5 — Protezione cartella

```bash
PWD_ABS="$(pwd)"
TARGET="${PWD_ABS}"
PROTECTED=0
case "$PWD_ABS" in
  "$HOME"|"$HOME/"|"/"|"/tmp"|"/tmp/"|"$HOME/Downloads"|"$HOME/Desktop")
    PROTECTED=1 ;;
esac
if [ "$PROTECTED" = "1" ] && [ ! -d "$TARGET" ]; then
  echo "PROTECTED:$PWD_ABS"
elif [ ! -f "$TARGET/_meta/folder-confirmed.flag" ] && [ ! -d "$TARGET" ]; then
  echo "FIRSTRUN:$TARGET"
else
  mkdir -p "$TARGET/03_Ad_Spy" "$TARGET/_meta"
  echo "READY:$TARGET"
fi
```

Cattura il path risolto come `$WORKDIR`.

---

## Step 1 — Raccolta input

Chiedi:
1. **Cosa si vuole spiare?** (brand/lista/nicchia)
2. **Paese?** (default: US)
3. **Ads per brand?** (default: 30, max: 100)

**Nota disponibilità dati reach:** Meta pubblica reach solo per mercati EU/UK/BR. Per US/CA/AU il segnale principale è la durata di pubblicazione. Informa l'utente prima di iniziare.

---

## Step 2 — Risoluzione Page ID (OBBLIGATORIO per ogni brand)

Questo step non si salta mai. Ogni brand passa per il Pages scraper per ottenere il vero `pageAdLibrary.id`.

**2A — Modalità nicchia:** ricerca i top N competitor via subagent:
```
Ricerca i top {N} brand competitor nella nicchia "{nicchia}".
Restituisci SOLO array JSON: [{"name": "...", "fb_url": "https://facebook.com/..."}].
Verifica che ogni fb_url punti alla pagina ufficiale del brand.
```

**2B — Costruisci lista URL Facebook:**
```json
[{"url": "https://www.facebook.com/{slug}/"}]
```

**2C — Chiama Pages scraper Apify (REST diretto, no MCP):**
Il Facebook Pages scraper è **obbligatorio** per ogni brand: risolve il vero `pageAdLibrary.id` prima di scrapare gli ad, così i risultati sono garantiti dal brand esatto. Chiamata via REST (`apify~facebook-pages-scraper`), token in header `Authorization: Bearer`, mai in URL:
```bash
curl -sS -X POST "https://api.apify.com/v2/acts/apify~facebook-pages-scraper/run-sync-get-dataset-items?timeout=120" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://www.facebook.com/{slug}/"}]}'
```
(`${TOKEN}` risolto allo Step 0.) Non usare `mcp__apify__*`. Il Page ID da usare nello Step 4 è `pageAdLibrary.id` (campo nidificato, **diverso** dal `pageId` FB). Se uno slug torna errore "content isn't available" (pagina con slug sbagliato/ristretto), ritenta con slug alternativi (es. `7shifts` → `7shiftsinc`) prima di scartarlo.

---

## Step 3 — Validazione brand-lock

| Condizione | Verdetto | Azione |
|---|---|---|
| `error: not_available` | HARD FAIL | Pagina ristretta, chiedi URL diretto Ad Library |
| `error: no_items` | HARD FAIL | Slug inesistente |
| `categories` vuoto E `pageAdLibrary.id` assente | HARD FAIL | È un profilo personale, non una Page |
| `pageAdLibrary.id` presente + `categories` include "Page" | PASS | Procedi |
| `pageAdLibrary.id` presente MA title non corrisponde al brand | SOFT WARN | Chiedi conferma utente |

Salva brand validati in `$WORKDIR/03_Ad_Spy/competitors.json`.

---

## Step 4 — Dispatch agenti paralleli

**Actor:** `curious_coder~facebook-ads-library-scraper` (REST `run-sync-get-dataset-items`). **Un brand per chiamata** — `count` è un cap **globale** dell'actor: passare più URL in una sola run esaurisce il count sul primo brand. Quindi una chiamata curl per brand, lanciate in parallelo (`run_in_background`).

1. **Scraping** — URL brand-locked: `view_all_page_id={PAGE_ID}` (= il `pageAdLibrary.id` dallo Step 2C, mai bare slug). **NON mettere `media_type=image` nell'URL** → azzera i risultati (`ADS_NOT_FOUND`); il filtro statiche si fa in post (punto 3). Usa `active_status=all` (poi `is_active` distingue attivi/ritirati nello scoring).
```bash
curl -sS -X POST "https://api.apify.com/v2/acts/curious_coder~facebook-ads-library-scraper/run-sync-get-dataset-items?timeout=300" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  -d '{"urls":[{"url":"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={COUNTRY}&search_type=page&view_all_page_id={PAGE_ID}"}],"count":{COUNT},"scrapeAdDetails":true}'
```
Campi utili per ad: `page_name`, `ad_archive_id`, `is_active`, `start_date`/`end_date` (unix), `collation_count` (= n_variants), `reach_estimate` (eu_reach, spesso null fuori EU), `publisher_platform`, `snapshot.{title,body.text,cta_text,display_format,images[].resized_image_url,cards[],videos}`.

2. **Controllo contaminazione** — verifica che tutti gli ads abbiano lo stesso `page_name`

3. **Filtro solo immagini statiche** — scarta gli ad con `snapshot.videos` o `display_format=VIDEO`. **DCO** (`display_format=DCO`): l'immagine sta in `snapshot.cards[].resized_image_url` (non in `images[]`); fallback `cards[].video_preview_image_url`. Tieni gli ad con almeno un'immagine statica.

4. **Scoring** (per mercati non EU/UK/BR — basato su durata, `reach_available=false`):
   - 🏆 PROVEN WINNER: `is_active=true` AND `days_running >= 60`
   - 🔥 HOT RUNNER: `is_active=true` AND `days_running >= 21`
   - ⚡ ACTIVE AD: `is_active=true` AND `days_running < 21`
   - ✅ RETIRED WINNER: `is_active=false` AND `days_running >= 60`
   - ⬜ SHORT RUN: `is_active=false` AND `days_running < 60`

   **Per mercati EU/UK/BR** (`aaa_info.eu_total_reach`/`uk_total_reach`/`br_total_reach` popolato su almeno un ad → `reach_available=true`): scoring blended reach + durata, così un lancio nuovo ad alto reach e un vecchio slow-burner emergono entrambi:
   - 🏆 PROVEN WINNER: `is_active=true` AND (`reach >= 100000` OR `days_running >= 60`)
   - 🔥 HOT RUNNER: `is_active=true` AND (`reach >= 25000` OR `days_running >= 21`)
   - ⚡ ACTIVE AD: `is_active=true` AND `reach < 25000` AND `days_running < 21`
   - ✅ RETIRED WINNER: `is_active=false` AND (`reach >= 100000` OR `days_running >= 60`)
   - ⬜ SHORT RUN: `is_active=false` AND `reach < 100000` AND `days_running < 60`

   Dentro ogni tier, ordina per reach desc poi days_running desc. **Non fabbricare mai reach** — se `aaa_info` è null anche in un run `reach_available=true` (capita ad-per-ad), tratta quell'ad come i mercati non-EU (solo durata) e non stimare/interpolare dai fratelli.

   Nella card HTML di ogni ad EU/UK/BR con `aaa_info` popolato, aggiungi un blocco "🎯 Audience & Reach": reach formattato con separatore migliaia + regione (`"1.240.000 (EU)"`), fascia età dominante e skew di genere da `age_country_gender_reach_breakdown[]`, top country. Quando `reach_available=false` per l'intero brand, mostra un banner in testa allo swipe file: *"Meta non pubblica reach/impression per ads commerciali fuori da EU/UK/Brasile. Il segnale winner più forte per questo brand è la durata di pubblicazione + stato attivo."* — mai ometterlo, evita che l'utente pensi che lo scrape sia fallito.

5. **Analisi** — per ogni 🏆/🔥/⚡: 2-3 frasi su hook, awareness level, perché funziona

6. **Download immagini base64:**
```bash
curl -s -L --max-time 10 \
  -H "User-Agent: Mozilla/5.0..." \
  -H "Referer: https://www.facebook.com/" \
  "<URL>" | base64
```

7. **Build HTML** — **stesso Design System chiaro navy/slate di `18_voc_research`/`52_ad_spy_video`** (non più dark theme — allinea i 3 deliverable HTML come stessa famiglia prodotto):
   - CSS variabili: `--bg:#FFFFFF; --surface-light:#F4F6FA; --surface-mid:#E8EDF5; --navy:#162441; --slate:#8A9BBC; --body:#2C3E50; --green:#1A6B3C (winner/reach); --blue:#1A5276 (link/info); --amber:#8B6914 (disclaimer)`. Font: system sans-serif stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`).
   - Header navy pieno (`--navy` bg, testo bianco): brand + kicker + sub-riga con conteggio ads/winner + reach totale (o "reach n/a" se `reach_available=false`, vedi Step 4.4).
   - Barra filtri sticky, sfondo bianco, bordo `--surface-mid`: filtro per tier badge, per formato, per stato attivo/ritirato.
   - Card grid su sfondo bianco, ogni card `--surface-light` bg, bordo 1px `--surface-mid`, badge tier in alto (colori: PROVEN/RETIRED = `--green`, HOT = `--amber`, ACTIVE = `--blue`, SHORT = `--slate`), immagine statica inline base64, copy sotto (headline/body/CTA), blocco Audience & Reach quando disponibile (Step 4).
   - Banner disclaimer reach (Step 4) quando `reach_available=false`, in testa alla pagina, `--amber` come da Step 4.
   - Self-contained: zero `<link>`/`<script src>` esterni, tutto CSS inline + immagini base64.

8. **Salva** in `$WORKDIR/03_Ad_Spy/adspy-{SLUG}-{YYYYMMDD}.html`

---

## Step 5 — Riepilogo aggregato

```
✅ Ad Spy 2.0 Completato

Brand verificati e processati:
  🏆 Ka'Chava   → 28 ads, 12 winner → adspy-kachava-{data}.html
  🏆 Huel       → 18 ads, 7 winner  → adspy-huel-{data}.html

Non brand-lockati:
  ❌ Brand X — pagina ristretta. Vuoi riprovare? Incolla l'URL Ad Library.

Prossimo step: Apri un 🏆 → clicca "📋 Copy for /pm-competitor-rebuild" → esegui skill 23_competitor_rebuild
```

---

## Step 6 — Export dati per Competitor Ads Dashboard

Oltre allo swipe file HTML, emetti `data.json` per la dashboard esterna (`output/dashboard/competitor-ads/`).

Per ogni ad nello swipe file, classifica via LLM (analizzando creative + copy):
- **`awareness_stage`** — uno dei 5 stadi Eugene Schwartz: `Unaware` / `Problem-Aware` / `Solution-Aware` / `Product-Aware` / `Most-Aware`
- **`funnel_stage`** — `TOF` (awareness/educazione) / `MOF` (consideration/proof) / `BOF` (offerta/prezzo/urgency)

Mappa il badge scoring al campo `tier`: PROVEN / HOT / ACTIVE / RETIRED / SHORT.

Estrai i KPI realmente disponibili da Meta Ad Library (ads commerciali): `days_active`, `eu_reach` (se presente, altrimenti `null`), `n_variants`, `first_seen`, `platforms`, `format`, `ad_library_url`. **NON** inventare impressions/spend/CTR — non esistono per ads commerciali.

Scrivi `$WORKDIR/03_Ad_Spy/data.json` seguendo lo schema in `output/dashboard/competitor-ads/data.sample.json`. L'utente copia questo file in `output/dashboard/competitor-ads/data.json` e apre `index.html` (o lo deploya su Netlify/Cloudflare/Vercel).

---

## Regole critiche

- **Pages scraper obbligatorio** per ogni brand, nessuna eccezione
- **Mai token Apify in URL** — sempre `Authorization: Bearer` header
- **Solo immagini statiche** — scarta tutto con video
- **`scrapeAdDetails: true` obbligatorio** — senza, i dati sono incompleti
- **Controllo contaminazione in ogni agente** — mix di page_name = fallimento, nessuno swipe file
- **Dispatch parallelo in UN SOLO messaggio**
