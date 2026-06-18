# Meta (Facebook) Ads MCP — Operator Guide

> A complete, self-contained reference for operating the Meta/Facebook Ads MCP server.
> It documents **every tool**, what each does, the inputs it expects, the shape of the data
> you **should** get back on success, and the failure modes to expect.
> All IDs/values below are **generic placeholders** (e.g. `123456789`) — substitute real ones at runtime.
>
> Audience: an AI agent that will operate this MCP. Read §1 (Conventions) and §13 (Gotchas) before doing anything.

---

## 0. What this MCP is

There are **two server surfaces**:

1. **Meta Ads MCP** (the main, fully-functional server) — ~58 tools, all prefixed `ads_*`.
   Covers reporting, insights, datasets/pixels, creatives, audiences, campaign building, catalogs,
   the public Ad Library, and help articles. This is where 99% of work happens.
2. **`facebook-ads` OAuth server** — only 2 tools (`authenticate`, `complete_authentication`).
   Exposes nothing else until OAuth is completed. Used only to connect the account.

Tools fall into three behavioral classes — internalize this, it drives everything:

- **Config/identity reads** — return account structure regardless of spend (accounts, pages, datasets, catalogs).
- **Delivery-derived reads** — `ads_insights_*`, `ads_get_opportunity_score`, and the *metric* fields of
  `ads_get_ad_entities`. These return **empty / "no data"** until the account actually delivers ads.
  They are computed from spend; no spend → nothing to report. This is normal, not an error.
- **External reads** — `ads_library_search`, `ads_get_help_article`, `ads_get_field_context`.
  Independent of the account; always return data.
- **Writes** — create/update/activate/delete. See §13 for what is and isn't reversible via the MCP.

---

## 1. Global conventions (READ FIRST)

- **IDs are bare numeric strings.** Ad account IDs do **NOT** take an `act_` prefix here (pass `123456789`, not `act_123456789`). Entity IDs are digits only.
- **Money is in minor units (cents).** A `daily_budget` of `500` = $5.00. Always read `min_daily_budget_cents` from `ads_get_ad_accounts` first; budgets below the per-currency minimum are rejected.
- **Dates:** metric retrieval, metric filtering, and metric sorting require a time window. Provide **either**:
  - `date_preset`: `today, yesterday, this_month, last_month, this_quarter, last_3d, last_7d, last_14d, last_30d, last_90d, last_week_sun_sat, last_quarter, last_year, this_week_sun_today, this_year, maximum`, **or**
  - `time_range`: `{"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}`.
  - Never pass both. Without a time window, entity reads return **attributes only** (no metrics).
  - (The `ads_insights_*` tools use a slightly different preset enum — UPPERCASE, e.g. `LAST_7D`, `LIFETIME` — and `date_from`/`date_to` instead of `time_range`. Follow each tool's parameter spec.)
- **Levels:** `account`, `campaign`, `adset`, `ad`. Set the level to match the user's scope. When filtering/sorting and unsure, use `campaign`.
- **Field names & aliases — verify before querying.** Use `ads_get_field_context` to confirm a field exists and learn its type/operators/levels. Known aliases: `spend` → `amount_spent`; `roas` → `purchase_roas`. **`actions` is not a standalone field** — request specific actions like `actions:omni_purchase`, `actions:link_click`, `actions:lead`.
- **Pagination:** responses include `next_cursor` or `page_info.after_cursor`. To get the next page, pass that exact value back as `cursor`. **Never fabricate a cursor.**
- **Entities are created PAUSED.** `ads_create_campaign/ad_set/ad` always return `status: PAUSED`. Nothing delivers or spends until explicitly activated **and** a payment method exists.
- **CBO vs ABO budgeting** (mutually exclusive — pick one):
  - **CBO (recommended, default):** set `campaign_daily_budget` or `campaign_lifetime_budget` on `ads_create_campaign`. Do **not** set ad-set budgets; the campaign-level `bid_strategy` governs all ad sets.
  - **ABO:** leave campaign budgets unset, then set `daily_budget`/`lifetime_budget` (and bid strategy) on each `ads_create_ad_set`. The API rejects ad-set budgets under a CBO parent.
- **Batch/partial semantics (pixel tools):** the `ads_pixel_*` tools take `items: [...]`. By default the first item error aborts the whole call; pass `partial: true` to collect per-item errors and continue.
- **Read-before-write etiquette:** for destructive audience ops, list dependents first (`ads_get_custom_audience_adsets`) and warn. For metric fields, confirm names with `ads_get_field_context`.

---

## 2. Authentication (`facebook-ads` server)

### `authenticate`
- **Does:** starts the OAuth flow for the `facebook-ads` server.
- **Inputs:** none.
- **Returns:** an **authorization URL** (with `client_id`, requested scopes — typically `ads_management ads_read catalog_management business_management pages_show_list` — and a `localhost:<port>/callback` redirect). The human opens it and authorizes.
- **Notes:** read-only/no side effects; it just mints a URL. The server's real tools appear automatically once auth completes.

### `complete_authentication`
- **Does:** finishes the OAuth flow.
- **Inputs:** `callback_url` — the full `http://localhost:<port>/callback?code=...&state=...` URL from the browser address bar after authorizing.
- **Returns:** success/connection confirmation.
- **Notes:** must be called **after** `authenticate`; needs a real, fresh `code`/`state`. Cannot be exercised without an actual browser round-trip.

---

## 3. Account & identity (config reads — always populated)

### `ads_get_ad_accounts`
- **Does:** lists ad accounts the user can access. Start here to discover IDs.
- **Inputs:** `limit?` (default 50), `cursor?`.
- **Returns:** `ad_accounts: [{ ad_account_id, ad_account_name, business_id, business_name, is_ads_mcp_enabled, account_status, is_queryable, has_payment_method, currency, min_daily_budget_cents, is_ads_mcp_disabled_reason, not_queryable_reason }]`, plus `next_cursor`.
- **Notes:** If `is_ads_mcp_enabled` is false, do not use that account. If `is_queryable` is false, do **not** call `ads_get_ad_entities` for it — surface `not_queryable_reason`. `business_id/business_name` reflect the **owning** business only; empty string = no owning business. Check `has_payment_method` and `min_daily_budget_cents` before any campaign work.

### `ads_get_ad_account_pages`
- **Does:** Pages promoted under a specific ad account.
- **Inputs:** `ad_account_id` (required), `limit?`, `cursor?`.
- **Returns:** `pages: [{ page_id, page_name, leadgen_tos_accepted }]`, `next_cursor`.
- **Notes:** Use `leadgen_tos_accepted` to pre-filter Pages eligible for Lead Gen ads. May be empty even when the business owns Pages (this is account-scoped, not business-scoped).

### `ads_get_user_pages`
- **Does:** all Pages the user can advertise with (has `CREATE_ADS` on), across their businesses.
- **Inputs:** `limit?`, `cursor?`.
- **Returns:** `pages: [{ page_id, page_name }]`, `next_cursor`.

### `ads_get_pages_for_business`
- **Does:** Pages owned by a specific business.
- **Inputs:** `business_id` (required), `limit?`, `cursor?`.
- **Returns:** `pages: [{ page_id, page_name }]`, `next_cursor`.
- **Notes:** Often the most reliable way to find a usable `page_id` for creative building. Get `business_id` from `ads_get_ad_accounts`.

---

## 4. Reporting — `ads_get_ad_entities` (the workhorse)

### `ads_get_ad_entities`
- **Does:** the primary reporting tool. Returns account/campaign/adset/ad rows with **attributes** and/or **metrics**, with filtering, sorting, breakdowns, and time bucketing.
- **Inputs:**
  - `ad_account_id` (required), `fields` (required — always include `id` and `name` for entity rows).
  - `level`: `account|campaign|adset|ad`.
  - Time: `date_preset` **or** `time_range` (required for any metric/filter/sort on metrics).
  - `filtering`: `[{ field: "level.field_name", operator, value: [..] }]` (operators per `ads_get_field_context`).
  - `sort`: `"<metric>_ascending"` / `"<metric>_descending"`.
  - `breakdowns`: e.g. `age`, `gender`, `country`, `region`, `publisher_platform`, `platform_position`, `impression_device`, `device_platform`, `action_type`, `hourly_stats_aggregated_by_advertiser_time_zone`, etc.
  - `time_increment`: `1`–`90` (days), `monthly`, or `all_days`.
  - `limit`: up to 1000.
- **Returns:** `{ ad_entities: "[{ ...requested fields... }]", summary: { total_count } }` (the `ad_entities` value is a JSON string array). Metric currency fields come back human-formatted (e.g. `"$2.00 USD"`).
- **Common valid fields** (subset; verify with `ads_get_field_context`): `id, name, status, effective_status, objective, optimization_goal, bid_strategy, buying_type, daily_budget, lifetime_budget, campaign_id, adset_id, creative_id, created_time, start_time, stop_time, amount_spent, impressions, reach, frequency, clicks, ctr, cpc, cpm, cpp, conversions, cost_per_conversion, purchase_roas, results, cost_per_result, video_p25/50/75/95/100_watched_actions, actions:omni_purchase, actions:link_click, actions:lead`.
- **Notes / best practice:**
  - To get both top and bottom of a metric, call twice with opposite `sort` directions (the tool caps row count).
  - Don't request `actions`/`action_values` as standalone fields — use the `actions:<type>` form.
  - If a field is rejected, the error lists every supported field for that level — use it to self-correct.
  - **Empty result with no spend is expected**, not an error.

---

## 5. Insights, diagnostics & optimization (delivery-derived — empty until the account delivers)

> All take `ad_account_id` and optional `entity_ids` (scope to specific campaigns/adsets/ads of one type). On a no-spend account they return short "no data available" strings — that is the correct, expected response.

### `ads_insights_advertiser_context`
- **Does:** summarizes the advertiser's vertical & marketing-funnel context to inform optimization-goal choice.
- **Inputs:** `ad_account_id` (req), `entity_ids?`, `date_preset?`/`date_from?`+`date_to?`.
- **Returns (when populated):** `{ result: "Vertical: <vertical>; <funnel context...>" }`. Null vertical renders as `"Vertical: \N"`.

### `ads_insights_anomaly_signal`
- **Does:** flags unusual patterns — auction overlap, creative fatigue, narrow audience.
- **Inputs:** `ad_account_id` (req), `entity_ids?`.
- **Returns:** `{ result: "<observations / 'No anomaly signal issues found...'>" }`.
- **Notes:** present anomalies as *observations to investigate*, not confirmed causes; defer causal claims to `ads_get_opportunity_score`.

### `ads_insights_auction_ranking_benchmarks`
- **Does:** auction competitiveness — quality/engagement/conversion ranking and bid/quality levers.
- **Inputs:** `ad_account_id` (req), `entity_ids?`, date params.
- **Returns:** `{ result: "<ranking diagnosis / 'No auction ranking benchmarks data available...'>" }`.

### `ads_insights_industry_benchmark`
- **Does:** compares ad-set performance vs similar advertisers (by spend tier / optimization goal).
- **Inputs:** `ad_account_id` (req); optional `analysis_metric` (`CLICKS, COST_PER_LEAD, CPC, CPM, CPR, CTR, CVR, IMPRESSIONS, REACH, RESULT, ROAS, SPEND`), `conversation_intent`, `conversation_topic`, `cas_segment`, `optimization_goal_override`, `entity_ids?`, date params.
- **Returns:** `{ result: "<benchmark comparison / 'No industry benchmark data available...'>" }`.
- **Notes:** compare like-for-like (same optimization goal/conversion event). Focus on outcome metrics (cost per result) over surface metrics (CPM).

### `ads_insights_performance_trend`
- **Does:** time-series direction of CPC, CPM, CPR, ROAS, CTR, CVR.
- **Inputs:** `ad_account_id` (req); optional `analysis_metric`, `analysis_level` (`AD|ADSET`), `conversation_intent`, `conversation_topic`, `entity_ids?`.
- **Returns:** `{ result: "<trend narrative / 'No performance trend data available...'>" }`.

### `ads_get_opportunity_score`
- **Does:** account-level optimization score (0–100) + ranked, actionable recommendations (Meta best practices, errors, warnings).
- **Inputs:** `ad_account_id` (req).
- **Returns:** `{ recommendations: [{ recommendation_type, opportunity_score_lift, lift_estimate, ... }] }` (and an overall score when available). Empty `[]` on a bare account.
- **Notes:** score is **always account-level** — never attribute it to one campaign. Sort recommendations by `opportunity_score_lift` (call them "points"). Recommend proactively when the user asks "how do I improve?".

### `ads_get_errors`
- **Does:** delivery-blocking (hard-stop) errors for campaigns/adsets/ads.
- **Inputs:** `entity_ids` (required — campaign/adset/ad IDs), `limit?`.
- **Returns:** `{ errors: { <entity_id>: [ {error...} ] } }`; `{ "errors": "{}" }` when there are none.
- **Notes:** Pass **child entity IDs**. Passing only a bare ad-account ID can return `Invalid parameter`. Does **not** cover performance/pacing issues, account-level disable/restriction, or ad rejection — only hard delivery blockers.

---

## 6. Datasets / pixels / conversion tracking

### Reads

#### `ads_get_datasets`
- **Does:** lists datasets (pixels / apps) for a business or ad account.
- **Inputs:** exactly one of `business_id` or `ad_account_id`; `limit?`, `cursor?`.
- **Returns:** `datasets: [{ dataset_id, name, is_active, creation_time, last_fired_time, server_last_fired_time, business_id, data_use_setting, first_party_cookie_status }]`, `page_info{ has_next_page, total_count, after_cursor }`.
- **Notes:** `server_last_fired_time` at the Unix epoch means **server-side/CAPI has never fired**. The same dataset can appear more than once — de-duplicate by `dataset_id`.

#### `ads_get_dataset_details`
- **Inputs:** `dataset_id`.
- **Returns:** `{ metadata: {…same fields as list…}, openbridge: { dataset_id, gateway_status, gateway_status_detail } }`. `gateway_status: NOT_ONBOARDED` = CAPI Gateway not set up.

#### `ads_get_dataset_quality`
- **Does:** signal quality/health by channel (EMQ, match-key coverage, freshness).
- **Inputs:** `dataset_id`, `query_type?` (channels: `web, offline, crm, custom_attribution`).
- **Returns:** channel-keyed object, e.g. `{ web: [{ event_name, ...emq/coverage... }], offline: [...], crm: [...] }`. Low-volume web-only pixels may return just event names with no EMQ figures.

#### `ads_get_dataset_stats`
- **Does:** event volume over time (max 28-day lookback).
- **Inputs:** `dataset_id`; `aggregation?` (`event` default, or `device_type, event_source, url, host, event_total_counts`), `event_name?`, `event_source?` (`WEB_ONLY|SERVER_ONLY`), `start_time?`/`end_time?` (Unix-timestamp strings; default last 7 days).
- **Returns:** `{ dataset_id, start_time, end_time, aggregation, stats: [{ aggregation, timestamp, data: [{ value, count }] }] }`.
- **Notes:** flag events with zero volume that are used by active campaigns.

#### `ads_pixel_event_read`
- **Does:** lists/looks-up conversion **event rules** on a pixel.
- **Inputs:** `items: [{ pixel_id (req), event_rule_id?, event_type? }]`, `partial?`.
- **Returns:** `{ results: [{ success, error, events:[...] }] }` (or `event` for a single-ID lookup). Returned events do **not** include parameters — read those separately.

#### `ads_pixel_parameter_read`
- **Does:** lists/looks-up parameter **extractors** on a pixel.
- **Inputs:** `items: [{ pixel_id (req), parameter_id?, domain_uri?, event_type? }]`, `partial?`.
- **Returns:** `{ results: [{ success, error, parameters:[...] }] }`.

### Writes (pixel events & parameters)

> All batch-capable (`items: [...]`, `partial?`). Require `ads_management` or `business_management` scope.
> **Subject to the pixel's "data source category"** — some categories reject standard events or parameter types (you'll see *"This event type is not available for your data source category"*). This is an account/pixel property, not a usage error.

#### `ads_pixel_event_create`
- **Inputs:** `items:[{ pixel_id, event_type (one of the 17 standard events: Purchase, AddToCart, Lead, ViewContent, InitiateCheckout, AddPaymentInfo, CompleteRegistration, Search, AddToWishlist, Contact, CustomizeProduct, Donate, FindLocation, Schedule, StartTrial, SubmitApplication, Subscribe), rule_type (URL | TOKENIZED_BUTTON_TEXT), match_value, domain_uri, operator?, parameters?:[{parameter_type, extractor_type, extractor_config_json}] }]`.
- **Returns:** `{ results:[{ success, event / event_rule_id }] }`. Created events default to `status: INACTIVE`.
- **Notes:** `rule_type=URL` for page-load events (operator default CONTAINS); `rule_type=TOKENIZED_BUTTON_TEXT` for button clicks (operator default EQUALS; canonicalize button text: lowercase, drop punctuation and "to/the/a"). Embed `parameters` for atomic event+param creation.

#### `ads_pixel_event_update`
- **Does:** status-only (activate/deactivate).
- **Inputs:** `items:[{ event_rule_id, status: ACTIVE|INACTIVE }]`.
- **Returns:** `{ results:[{ success, event }] }`. Activating a freshly created event is the human checkpoint; verify it fires before relying on it.

#### `ads_pixel_event_delete`
- **Inputs:** `items:[{ event_rule_id }]`.
- **Returns:** `{ results:[{ success, event_rule_id }] }`.
- **Notes:** soft-delete (archived, reversible internally) for rules created via API/MCP; hard-delete for rules created in the Events Manager UI. **Linked parameters are NOT auto-deleted** — enumerate via `ads_pixel_parameter_read` and delete orphans explicitly.

#### `ads_pixel_parameter_create`
- **Inputs:** `items:[{ pixel_id, domain_uri, event_type, extractor_type (CSS | CONSTANT_VALUE), extractor_config_json?, event_rule_id? }]`.
- **Returns:** `{ results:[{ success, parameter }] }`.
- **Notes:** `CSS` reads `element.innerText` of the matched node (cannot read URL fragments, attributes, or JS state). `CONSTANT_VALUE` hardcodes a string (e.g. `{"parameter_type":"currency","value":"USD"}`). Link to an event via `event_rule_id` in nearly all cases.

#### `ads_pixel_parameter_update`
- **Inputs:** `items:[{ parameter_id, domain_uri?, event_type?, extractor_type?, extractor_config_json?, event_rule_id? }]` (omitted fields unchanged).
- **Returns:** `{ results:[{ success, parameter }] }`.

#### `ads_pixel_parameter_delete`
- **Inputs:** `items:[{ parameter_id }]`.
- **Returns:** `{ results:[{ success, parameter_id }] }`. Soft-delete; does not touch the linked event rule.

### `ads_get_customconversions`
- **Does:** lists custom conversions (rules built on pixel/offline events) for an ad account.
- **Inputs:** `ad_account_id` (req), `dataset_id?`, `limit?`, `cursor?`.
- **Returns:** paginated list of `{ id, name, rule, custom_event_type, ... }` (read-only; no metrics).
- **Notes:** may return a *"tool is new and is being gradually rolled out"* message on accounts where it isn't enabled yet — treat as "unavailable here," not a hard failure.

---

## 7. Creatives & assets

### `ads_get_creatives`
- **Does:** lists ad creatives, or fetches specific ones in full.
- **Inputs:** `ad_account_id` (req), `creative_ids?`, `fields?`, `limit?`, `cursor?`.
- **Returns:** `ad_creatives: [{ id, name, account_id, status, ... }]`.
  - **Partial-by-default:** a plain list returns only `id, name, account_id, status`. To get `body` (primary text), `title` (headline), `link_url`, `image_hash`, `image_url`, `video_id`, `thumbnail_url`, `call_to_action_type`, `object_story_id`, `effective_object_story_id`, `effective_instagram_media_id`, `product_set_id`, `child_attachments` — re-call with `creative_ids` or explicit `fields`. Never assume a field is empty because it was absent from a list.
  - Field-name mapping: `body` = "Primary text" in Ads Manager; `title` = "Headline".

### `ads_get_creative_ads`
- **Does:** which ads reference a given creative.
- **Inputs:** `creative_id` (req), `limit?`, `cursor?`.
- **Returns:** list of ad (adgroup) `{ id, name, ... }` + pagination.

### `ads_get_ad_images`
- **Does:** lists uploaded images.
- **Inputs:** `ad_account_id` (req), `hashes?`, `name?` (substring), `fields?`, `limit?`, `cursor?`.
- **Returns:** `ad_images: [{ hash, name, ... }]`. **Partial-by-default** (list = `hash, name`); request `status, width, height, original_width, original_height, url, url_128, permalink_url, created_time, updated_time` via `hashes`/`fields`. `hash` is what you pass to creative builders.

### `ads_get_ad_videos`
- **Does:** lists uploaded videos.
- **Inputs:** `ad_account_id` (req), `video_ids?`, `title?`, `fields?`, `limit?`, `cursor?`.
- **Returns:** `ad_videos: [{ id, title, ... }]`. **Partial-by-default** (list = `id, title`); request `description, length, created_time, updated_time, permalink_url, picture`. `id` is the video FBID for creative building.

### `ads_get_ad_preview`
- **Does:** renders a visual preview of an existing ad or creative for a placement.
- **Inputs:** `ad_format` (req — e.g. `DESKTOP_FEED_STANDARD, MOBILE_FEED_STANDARD, INSTAGRAM_STANDARD, INSTAGRAM_STORY, INSTAGRAM_REELS, RIGHT_COLUMN_STANDARD, MESSENGER_MOBILE_INBOX_MEDIA, THREADS_STREAM`), and **one of** `ad_id` or `creative_id`.
- **Returns:** `{ preview_html (iframe), preview_url (open in browser), <image content item>, creative details (body, headline, CTA) }`. Always surface `preview_url`.

### `ads_create_creative` (write)
- **Does:** creates an ad creative. Three formats: single-image, single-video, Advantage+ catalog carousel.
- **Inputs:** `ad_account_id`, `page_id` (always required inside the creative).
  - Image: + `link_url` + exactly one of `image_hash` (preferred) or `image_url`.
  - Video: + `video_id` + a thumbnail via `image_hash`/`image_url`; `link_url` optional.
  - Catalog carousel: + `product_set_id` + `link_url` (no image/video).
  - Optional: `message` (primary text), `headline`, `description`, `call_to_action_type` (default `LEARN_MORE`; pick the exact UPPER_CASE enum, e.g. `SHOP_NOW, SIGN_UP, BOOK_NOW`), `name`, `instagram_user_id` (omit → no Instagram delivery).
- **Returns (success):** `{ creative_id, ... }`.
- **Notes / important:** the canonical image field is **`image_hash`** (from `ads_get_ad_images`). There is **no image/video upload tool in this MCP** — assets must already exist as a hash/ID. Remote `image_url` fetching is unreliable and can fail with a generic *"An unknown error occurred."* Pre-upload assets via Ads Manager/Commerce Manager if you only have raw files.

---

## 8. Audiences

### Reads

#### `ads_get_ad_account_custom_audiences`
- **Inputs:** `ad_account_id` (req), `subtype_filter?` (`CUSTOM, WEBSITE, LOOKALIKE, APP, ENGAGEMENT, OFFLINE_CONVERSION`), `limit?` (default 25, max 100), `cursor?`.
- **Returns:** `audiences: [{ id, name, subtype, approximate_count/size, delivery_status, operation_status, time_created, time_updated, ... }]` + `next_cursor`. Highlight non-normal operation/delivery status.

#### `ads_get_custom_audience`
- **Inputs:** `custom_audience_id` (req).
- **Returns:** `{ id, name, subtype, size/approximate_count, delivery_status, operation_status (with code), time_created, time_updated, ... }`. If `operation_status` ≠ 200 or delivery is `INACTIVE/INVALID`, the audience can't be used for delivery.

#### `ads_get_custom_audience_adsets`
- **Inputs:** `custom_audience_id` (req), `limit?`.
- **Returns:** `{ adsets: [{ id, name }], total_count }`. **Call this before deleting** an audience — listed ad sets get auto-paused on delete.

### Writes

#### `ads_create_custom_audience`
- **Does:** creates a custom audience. Subtypes: `CUSTOM` (customer list/DFCA), `WEBSITE` (WCA), `ENGAGEMENT` (ECA).
- **Inputs:** `ad_account_id`, `name`, `subtype` (req).
  - `CUSTOM`: + `customer_file_source` (`USER_PROVIDED_ONLY|PARTNER_PROVIDED_ONLY|BOTH_USER_AND_PARTNER_PROVIDED`); created empty (add users next); `retention_days?` (1–180), `is_value_based?`.
  - `WEBSITE`: + `rule` (JSON-encoded **string**) with pixel `event_sources` and a `template` (`ALL_VISITORS`, `VISITORS_BY_URL`, `TOP_TIME_SPENDERS`); `prefill?`, `audience_labels?`.
  - `ENGAGEMENT`: + `rule` with `ig_business` event sources.
- **Returns (success):** `{ audience_id, ... }`.
- **Notes:** `CUSTOM` (customer-list) requires a **one-time Custom Audience ToS acceptance** in the UI, else `error_subcode 1870090` ("Custom audience terms not accepted"). LOOKALIKE/APP audiences are **not** creatable here. Example `WEBSITE` all-visitors rule:
  `{"inclusions":{"operator":"or","rules":[{"event_sources":[{"type":"pixel","id":"<PIXEL_ID>"}],"retention_seconds":2592000,"template":"ALL_VISITORS","filter":{"operator":"and","filters":[{"field":"url","operator":"i_contains","value":""}]}}]}}`

#### `ads_update_custom_audience`
- **Does:** updates audience **metadata** (name/description/rule/labels). Not users.
- **Inputs:** `custom_audience_id` (req) + ≥1 of `name, description, rule` (WCA only), `audience_labels`.
- **Returns:** `{ success, audience_id }`.

#### `ads_update_custom_audience_users`
- **Does:** adds/removes members of a **DFCA (customer-list)** audience.
- **Inputs:** `audience_id`, `schema` (e.g. `["EMAIL"]`, `["EMAIL","PHONE"]`, `["EXTERN_ID","EMAIL","LOOKALIKE_VALUE"]`), `data` (rows aligned to schema); `operation?` (`ADD` default / `REMOVE`), `customer_consent?`, `debug_identifier?`.
- **Returns:** `{ num_received, num_invalid_entries, session_id, ... }`.
- **Notes:** PII is accepted raw or pre-hashed — the server normalizes and SHA-256-hashes raw values before upload (EXTERN_ID/LOOKALIKE_VALUE pass through). Only works on `CUSTOM`/DFCA audiences. REMOVE can be rejected if it would drop an active audience below delivery thresholds.

#### `ads_delete_custom_audience`
- **Does:** permanently deletes a custom audience.
- **Inputs:** `custom_audience_id` (req).
- **Returns:** `{ success, ... }`.
- **Notes:** **PERMANENT.** First call `ads_get_custom_audience_adsets` and warn the user (those ad sets auto-pause). Delete child lookalikes first or it fails. One of the few truly deletable object types in this MCP.

---

## 9. Campaign construction & management (writes)

> Build top-down: campaign → ad set → ad. Everything is created PAUSED. Activate bottom objects only when ready; **all** levels must be ACTIVE *and* a payment method must exist for delivery.

### `ads_create_campaign`
- **Inputs:** `ad_account_id`, `campaign_name`, `objective`, `buying_type` (req).
  - `objective` must be ODAX: `OUTCOME_AWARENESS, OUTCOME_TRAFFIC, OUTCOME_ENGAGEMENT, OUTCOME_LEADS, OUTCOME_SALES, OUTCOME_APP_PROMOTION` (legacy objectives are rejected).
  - `buying_type`: `AUCTION` (default) or `RESERVED`.
  - `special_ad_categories` (default `"[]"`; use `["HOUSING"|"CREDIT"|"EMPLOYMENT"|...]` when applicable) and `special_ad_category_country?`.
  - CBO: `campaign_daily_budget` **or** `campaign_lifetime_budget` (cents) + optional `campaign_bid_strategy` (`LOWEST_COST_WITHOUT_CAP` default, `LOWEST_COST_WITH_BID_CAP`, `COST_CAP`, `LOWEST_COST_WITH_MIN_ROAS`).
  - Optional: `promoted_object` (required for some objectives), `campaign_spend_cap`, `campaign_start_time/stop_time`, etc.
- **Returns:** `{ campaign_id, status: "PAUSED", ads_manager_url, spec, valid_optimization_goals, recommended_optimization_goal }`.
- **Notes:** capture `valid_optimization_goals` — use only those when creating the ad set. After creating, it's good practice to check `ads_get_opportunity_score`.

### `ads_create_ad_set`
- **Inputs:** `ad_account_id`, `campaign_id`, `ad_set_name`, `billing_event` (`IMPRESSIONS|LINK_CLICKS|POST_ENGAGEMENT|VIDEO_VIEWS`), `optimization_goal`, `targeting` (req).
  - `targeting` (JSON string): minimum broad = `{"geo_locations":{"countries":["US"]}}`. **Never invent interest IDs** — omit interests or fetch real IDs first.
  - ABO only: `daily_budget`/`lifetime_budget` (+ `bid_strategy`, `bid_amount`/`bid_constraints` as required). Do **not** set these under a CBO parent.
  - `promoted_object` REQUIRED when `optimization_goal` ∈ `{OFFSITE_CONVERSIONS, VALUE, LEAD_GENERATION, QUALITY_LEAD, APP_INSTALLS, IN_APP_VALUE}` (e.g. `{"pixel_id":"123","custom_event_type":"PURCHASE"}`).
  - `destination_type` required for messaging/profile goals; `dsa_beneficiary`/`dsa_payor` required for EU geos.
- **`optimization_goal` by objective** (default first; values outside the list are rejected):
  - `OUTCOME_AWARENESS` → REACH, IMPRESSIONS, AD_RECALL_LIFT, THRUPLAY, TWO_SECOND_CONTINUOUS_VIDEO_VIEWS
  - `OUTCOME_TRAFFIC` → LINK_CLICKS, LANDING_PAGE_VIEWS, OFFSITE_CONVERSIONS, IMPRESSIONS, POST_ENGAGEMENT, REACH, CONVERSATIONS, THRUPLAY, VISIT_INSTAGRAM_PROFILE, PROFILE_VISIT, QUALITY_CALL, REMINDERS_SET
  - `OUTCOME_ENGAGEMENT` → THRUPLAY, POST_ENGAGEMENT, EVENT_RESPONSES, PAGE_LIKES, IMPRESSIONS, REACH, (2SEC/VIDEO_VIEWS), LINK_CLICKS, CONVERSATIONS, OFFSITE_CONVERSIONS, LANDING_PAGE_VIEWS, QUALITY_CALL
  - `OUTCOME_LEADS` → OFFSITE_CONVERSIONS, LEAD_GENERATION, QUALITY_LEAD, LANDING_PAGE_VIEWS, LINK_CLICKS, IMPRESSIONS, REACH, VALUE, CONVERSATIONS, QUALITY_CALL
  - `OUTCOME_SALES` → OFFSITE_CONVERSIONS, VALUE, LANDING_PAGE_VIEWS, IMPRESSIONS, POST_ENGAGEMENT, REACH, LINK_CLICKS, CONVERSATIONS
  - `OUTCOME_APP_PROMOTION` → APP_INSTALLS, OFFSITE_CONVERSIONS, IMPRESSIONS, LINK_CLICKS, REACH, VALUE, VIDEO_VIEWS
- **Returns:** `{ ad_set_id, status: "PAUSED", ads_manager_url, spec }`. Note Advantage+ Audience is auto-enabled (`targeting_automation.advantage_audience:1`); set it to 0 for a hard age cap.

### `ads_create_ad`
- **Inputs:** `ad_account_id`, `ad_set_id`, `ad_name`, `creative` (req).
  - `creative` (JSON string) must carry exactly one source: `{"creative_id":"..."}` (reuse), `{"object_story_id":"pageID_postID"}` (promote a post), or `{"object_story_spec":{...}}` (inline — must include `page_id`).
- **Returns (success):** `{ ad_id, status: "PAUSED", ... }`.
- **Notes:** ad creation hits **billing validation** — on an account with no funding source it fails with `"No Payment Method"` (subcode 1359188). Resolve by adding a payment method.

### `ads_update_entity`
- **Does:** edits an existing campaign/adset/ad (name, budget, status, targeting, schedule, etc.).
- **Inputs:** `ad_account_id` (must be the true owner), `entity_id`, `entity_type` (`campaign|ad_set|ad`), `fields` (JSON object; budgets in cents). Example `{"name":"New","daily_budget":5000}` or `{"status":"PAUSED"}`.
- **Returns:** `{ success, entity_id, entity_type, updated_fields, status_forced_to_paused, ads_manager_url }`.
- **Notes:** This is the pause/unpause tool (`status: PAUSED`/`ACTIVE`). **It does not hard-delete** — requesting `status: DELETED` is coerced to `PAUSED` (`status_forced_to_paused: true`). See §13.

### `ads_activate_entity`
- **Does:** flips PAUSED → ACTIVE (publishes).
- **Inputs:** `ad_account_id`, `entity_id`, `entity_type` (`campaign|ad_set|ad`).
- **Returns:** `{ ad_account_id, entity_id, entity_type, status: "ACTIVE", success }`.
- **Notes:** **starts spending** once all parent levels are ACTIVE and funding exists. Activating a parent does not activate children — activate each level. Get explicit user confirmation before calling.

---

## 10. Catalog / commerce

### Reads

#### `ads_catalog_get_catalogs`
- **Inputs:** `business_id?`, `name?`, `limit?` (max 100), `cursor?`.
- **Returns:** `catalogs: [{ catalog_id, name, vertical, business:{ business_id, name } }]`, `page_info`.
- **Notes:** requires `catalog_management`. Pass `business_id` to scope to one business.

#### `ads_catalog_get_details`
- **Inputs:** `catalog_id`; `feed_limit?`/`feed_cursor?` to include feeds.
- **Returns:** catalog metadata — name, vertical, `product_count`, `product_set_count`, business info, and (optional) a paginated `feeds` list.

#### `ads_catalog_get_diagnostics`
- **Inputs:** `catalog_id`, `severity?` (`MUST_FIX|OPPORTUNITY`), `limit?`.
- **Returns:** `diagnostics: [{ severity, type, affected_count, affected_channels, ... }]` (`[]` when healthy).
- **Notes:** `affected_channels` maps: `mini_shops`=FB/IG Shops, `da`=Dynamic Ads, `marketplace`=Marketplace, `ig_shopping`=IG Shopping, `whatsapp`=WhatsApp. Don't sum affected counts across issues (they overlap); don't overstate MUST_FIX scope when channels are limited.

#### `ads_catalog_get_product_sets`
- **Inputs:** `catalog_id`, `name?`, `product_set_id?`, `limit?`, `cursor?`.
- **Returns:** `product_sets: [{ product_set_id, catalog_id, name, product_count, product_set_type, visibility, creation_time, filter_rule }]`, `page_info`. To merely **count** sets, use `ads_catalog_get_details.product_set_count` instead of enumerating.

#### `ads_catalog_get_product_set_products`
- **Inputs:** `product_set_id`; filters (`availability, retailer_id, brand, category, condition, product_type, price_min, price_max`), `limit?`, `cursor?`.
- **Returns:** `products: [{ product_id, catalog_id, retailer_id, name, description, price, availability, image_url, ... }]`, `next_cursor`.

#### `ads_catalog_search_product`
- **Does:** the primary product list/search/count tool (use this, not the deprecated `ads_catalog_get_products`). Also the way to preview a filter before creating a product set.
- **Inputs:** `catalog_id`, `filter` (JSON-encoded rule — see Filter spec below); `limit?`, `cursor?`.
- **Returns:** `products: [{ product_id, catalog_id, retailer_id, name, description, price:{amount,currency}, sale_price, brand, category, color, condition, gender, material, pattern, size, availability, image_url, image_fetch_status, videos_fetch_status }]`, `page_info:{ has_next_page, total_count, after_cursor }`. Read `page_info.total_count` for "how many match".
- **Filter spec (commerce vertical):**
  - Leaf: `{<field>:{<op>:<value>}}`; compound: `{and|or:[...]}` / `{not:{...}}`.
  - Ops: `eq, neq, lt, lte, gt, gte, contains, not_contains, starts_with (category only), is_any, is_not_any`.
  - Fields incl.: `availability, brand, category, color, condition, currency, custom_label_0..4, gender, material, name, pattern, price_amount (integer = price×100), product_feed_id, product_item_id, product_type, retailer_id, sale_price_amount, size, tags, visibility`.
  - Value matching is case-insensitive; use `eq` (not `contains`) for enum fields.

#### `ads_catalog_get_product_details`
- **Inputs:** `product_id` (Meta numeric FBID only — NOT a retailer_id/SKU).
- **Returns:** `{ product_id, catalog_id, retailer_id, name, description, price:{amount,currency}, url, brand, condition, availability, image_url, image_fetch_status, videos_fetch_status }`.
- **Notes:** for alphanumeric SKUs, use `ads_catalog_search_product` with `{"retailer_id":{"eq":"SKU"}}` instead.

#### `ads_catalog_get_product_feed_details`
- **Inputs:** `feed_id`.
- **Returns:** feed name, schedule (replace/update), source type, product_count, latest upload-session status/errors.

#### `ads_catalog_get_feed_rules`
- **Inputs:** `feed_id`, `limit?`, `cursor?`.
- **Returns:** feed transformation rules: `mapping_rule, value_mapping_rule, letter_case_rule, fallback_rule, regex_replace_rule`.
- **Notes:** feeds exist only for feed-ingested catalogs; a catalog created from inline batch items has no feed (so `feed_id`-based tools won't apply).

#### `ads_catalog_get_products` — **DEPRECATED**
- Do not use. Route all listing/searching to `ads_catalog_search_product`; single-product lookup to `ads_catalog_get_product_details`.

### Writes

#### `ads_catalog_create`
- **Does:** creates a catalog and uploads products in one step.
- **Inputs:** `business_id`, `catalog_name` (req); `vertical?` (default `commerce`); exactly one data method: `feed_url` (+ `feed_name`, optional `schedule`, credentials), `feed_file_content`+`feed_file_name`, or inline `items:[{method:CREATE|UPDATE|DELETE, data:{id,title,description,price,availability,condition,link,image_link,brand,...}}]`; `update_only?`.
- **Returns:** `{ catalog_id, catalog_name, schedule_configured, warnings, upload_method, batch_handles }`.
- **Notes:** **First call `ads_catalog_get_catalogs`** — businesses should use one catalog; duplicates fragment signals. Newly-ingested products take a moment before `image_fetch_status` flips to `fetched`. **No catalog-delete tool exists in this MCP** (remove via Commerce Manager).

#### `ads_catalog_create_product_set`
- **Does:** creates a dynamic product set from a filter.
- **Inputs:** `catalog_id`, `title`, `filter` (same Filter spec as `ads_catalog_search_product`); `retailer_id?`.
- **Returns:** `{ product_set_id, catalog_id, name, product_count, product_set_type, visibility, creation_time, filter_rule }`.
- **Notes:** **preview the filter with `ads_catalog_search_product` first** and confirm with the user. No update/delete of sets via this MCP.

---

## 11. External data (no account delivery required)

### `ads_library_search`
- **Does:** searches Meta's public Ad Library (competitive/transparency research).
- **Inputs:** at least one of `search_terms`, `page_ids`, `countries` (ISO-2, e.g. `["US"]`); plus `ad_active_status?` (`ALL|ACTIVE|INACTIVE`), `ad_type?` (`ALL|POLITICAL_AND_ISSUE_ADS|HOUSING_ADS|EMPLOYMENT_ADS|CREDIT_ADS`), `limit?` (max 50).
- **Returns:** `{ estimated_total_count, ads: [{ id, page_id, page_name, ad_creative_link_title, ad_creation_time, ad_delivery_start_time, ad_snapshot_url, currency }] }`. Surface `ad_snapshot_url` for visual inspection and report `estimated_total_count` for scope.

### `ads_get_help_article`
- **Does:** retrieves official Meta help-center articles for advertising concepts/policies/how-tos.
- **Inputs:** `search_query` (a short, focused query).
- **Returns:** article text + canonical URL(s). **Always include the URL(s)** in any answer that uses the content. Don't use for account-specific metrics or billing/account-disable issues.

### `ads_get_field_context`
- **Does:** metadata catalog for reporting fields — type, supported levels, filterable/sortable, aliases, operators, enum values.
- **Inputs:** `field_names?` (omit/empty → returns the entire catalog).
- **Returns:** `{ fields: [{ name, description, type, levels, filterable, sortable, is_metric, aliases, supported_filter_operators, enum_values, example }], unknown_fields: [...] }`.
- **Notes:** call this whenever you're unsure a field exists or how to filter it, and to resolve aliases (`spend`→`amount_spent`, `roas`→`purchase_roas`). Names that don't resolve come back in `unknown_fields`.

---

## 12. Recommended workflows (playbooks)

**A. Orient on a new account**
1. `ads_get_ad_accounts` → pick a queryable, MCP-enabled account; note `currency`, `min_daily_budget_cents`, `has_payment_method`.
2. `ads_get_pages_for_business` / `ads_get_user_pages` → page IDs. `ads_get_datasets` → pixel IDs. `ads_catalog_get_catalogs` → catalogs.
3. Performance snapshot: `ads_get_ad_entities` (level=account, a `date_preset`, metric fields). If empty → no delivery yet.
4. Health: `ads_get_opportunity_score`, `ads_insights_anomaly_signal`, `ads_get_errors` (with child entity IDs).

**B. Diagnose performance**
1. `ads_get_ad_entities` at campaign→adset→ad with the metric(s) in question; sort both directions to find best/worst.
2. Add `breakdowns` (e.g. `publisher_platform`, `age`, `country`) to localize the issue.
3. `ads_insights_performance_trend` (trajectory), `ads_insights_industry_benchmark` (vs peers), `ads_insights_auction_ranking_benchmarks` (auction), `ads_get_opportunity_score` (fixes).

**C. Build a campaign end-to-end**
1. Confirm `page_id`; (if conversions) `pixel_id` from `ads_get_datasets`. Ensure assets exist (`ads_get_ad_images`/`ads_get_ad_videos`) since there's no upload tool.
2. `ads_create_campaign` (CBO budget; capture `valid_optimization_goals`).
3. `ads_create_ad_set` (valid `optimization_goal`; broad `targeting`; `promoted_object` for conversion goals).
4. `ads_create_creative` (with `image_hash`/`video_id`) → `ads_create_ad` (`creative_id`).
5. Review (`ads_get_ad_preview`), then `ads_activate_entity` per level **after** explicit confirmation.

**D. Set up conversion tracking**
1. `ads_get_datasets` → pixel. `ads_pixel_event_read`/`ads_pixel_parameter_read` to see what exists.
2. `ads_pixel_event_create` (URL or button rule, embed `parameters`) → `ads_pixel_event_update` to ACTIVE → verify it fires.

**E. Retargeting audience**
1. `ads_create_custom_audience` (WEBSITE from pixel, or CUSTOM after ToS) → for CUSTOM, `ads_update_custom_audience_users` (ADD).
2. Reference the audience ID in an ad set's `targeting`. Before deleting any audience, `ads_get_custom_audience_adsets` + warn.

**F. Competitive research** — `ads_library_search` (by competitor `page_ids` or `search_terms` + `countries`); open `ad_snapshot_url`s.

---

## 13. Known limitations & error catalog

**Reversibility (critical):**
- The MCP can **delete** only: custom audiences (`ads_delete_custom_audience`), pixel events (`ads_pixel_event_delete`), pixel parameters (`ads_pixel_parameter_delete`).
- It **cannot delete** campaigns, ad sets, ads, creatives, catalogs, or product sets. `ads_update_entity` with `status:DELETED` is **silently coerced to PAUSED** (`status_forced_to_paused:true`). To truly remove these, use Ads Manager (campaigns/adsets/ads) or Commerce Manager (catalogs). Plan test/cleanup accordingly.
- No image/video **upload** tool — creatives need a pre-existing `image_hash`/`video_id`.

**Account-state gates (expected errors, not bugs):**
- `No Payment Method` (subcode 1359188) on `ads_create_ad`/activation/delivery → add a funding source.
- `Custom audience terms not accepted` (subcode 1870090) on `CUSTOM` audience create → accept the one-time ToS in the UI; or use a `WEBSITE` audience instead.
- `This event type / Parameter type … is not available for your data source category` on pixel writes → the pixel's category restricts it; not all pixels accept all standard events/params.
- `ads_get_customconversions` may return a *"gradually rolling out"* message → unavailable on that account.
- `ads_insights_*` / `ads_get_opportunity_score` returning "no data"/`[]` → the account hasn't delivered; populate by running a campaign.

**Validation behavior:**
- Catalog/pixel tools reject placeholder IDs like `"0"` with `FBIDTypeError ("got zero")`. Audience/creative tools return a generic `Invalid parameter`.
- `ads_get_errors` needs **child entity IDs**; a bare ad-account ID can return `Invalid parameter`. Empty result is `{"errors":"{}"}`.
- `ads_get_ad_entities` rejects unknown fields and **echoes the full valid-field list** for that level in the error — use it to self-correct. `account_id`/`account_name` are not valid entity fields.
- Transient `500`/`INTERNAL ("try again later")` happen (e.g. brand-new catalog details, audience creation) — retry with backoff.

**Scoping rules:**
- `ads_get_datasets` accepts only one of `business_id`/`ad_account_id`.
- Partial-by-default listings (`ads_get_creatives`, `ads_get_ad_images`, `ads_get_ad_videos`) — re-query by ID/`fields` for anything beyond the 2–4 summary fields; don't assume omitted = empty.
- Currency metrics from `ads_get_ad_entities` are returned **pre-formatted** (e.g. `"$2.00 USD"`); budgets you send are **integer cents**.

**Permissions/scopes:** catalog tools need `catalog_management`; pixel writes need `ads_management` or `business_management`; reporting needs `ads_read`/`ads_management`.

---

## 14. Quick tool index (60 tools)

**Auth (2):** `authenticate`, `complete_authentication`
**Accounts/Pages (4):** `ads_get_ad_accounts`, `ads_get_ad_account_pages`, `ads_get_user_pages`, `ads_get_pages_for_business`
**Reporting (1):** `ads_get_ad_entities`
**Insights/diagnostics (7):** `ads_insights_advertiser_context`, `ads_insights_anomaly_signal`, `ads_insights_auction_ranking_benchmarks`, `ads_insights_industry_benchmark`, `ads_insights_performance_trend`, `ads_get_opportunity_score`, `ads_get_errors`
**Datasets/pixels (13):** `ads_get_datasets`, `ads_get_dataset_details`, `ads_get_dataset_quality`, `ads_get_dataset_stats`, `ads_pixel_event_read`, `ads_pixel_event_create`, `ads_pixel_event_update`, `ads_pixel_event_delete`, `ads_pixel_parameter_read`, `ads_pixel_parameter_create` (+`ads_pixel_parameter_update`, `ads_pixel_parameter_delete`), `ads_get_customconversions`
**Creatives/assets (6):** `ads_get_creatives`, `ads_get_creative_ads`, `ads_get_ad_images`, `ads_get_ad_videos`, `ads_get_ad_preview`, `ads_create_creative`
**Audiences (7):** `ads_get_ad_account_custom_audiences`, `ads_get_custom_audience`, `ads_get_custom_audience_adsets`, `ads_create_custom_audience`, `ads_update_custom_audience`, `ads_update_custom_audience_users`, `ads_delete_custom_audience`
**Campaign mgmt (5):** `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_update_entity`, `ads_activate_entity`
**Catalog (12):** `ads_catalog_get_catalogs`, `ads_catalog_get_details`, `ads_catalog_get_diagnostics`, `ads_catalog_get_product_sets`, `ads_catalog_get_product_set_products`, `ads_catalog_search_product`, `ads_catalog_get_product_details`, `ads_catalog_get_product_feed_details`, `ads_catalog_get_feed_rules`, `ads_catalog_get_products` (deprecated), `ads_catalog_create`, `ads_catalog_create_product_set`
**External (3):** `ads_library_search`, `ads_get_help_article`, `ads_get_field_context`

*End of guide.*
