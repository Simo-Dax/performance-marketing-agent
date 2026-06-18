# Diagnostic frameworks, ai-ad-lab-meta-analyze

This file holds the deep-diagnosis methodology: the signature and kill-criteria tables, the
confidence rubric and ranking rules, the report templates, the worked example, and the full
data-staging spec (pull plan, slice contracts, encoding, provenance). The main session reads
this file before staging data and applies it exactly. Angle-bracket placeholders inside
template blocks are filled at run time, they are part of the templates by design.

---

## 1. The signature table (how each theory shapes the data)

| Signal | Creative Fatigue | Delivery and Budget | Traffic Quality | Tracking | Outside World |
|---|---|---|---|---|---|
| Onset shape | gradual, per-creative | sharp step on one date | follows a delivery event, or gradual | cliff in event volume on one date | gradual or calendar-aligned |
| Frequency | rising | any | any | unchanged | unchanged |
| CTR | falling on fatigued ads | stable, may jump | stable or rising (cheap clicks can click) | unchanged | stable |
| CPM | drifting up (quality penalty) | step with the budget or bid event | down if delivery broadened | unchanged | up account-wide, structure stable |
| Click to cart | stable | collapses after broadening | collapses | cart events vanish from the pixel side | stable |
| Pixel event volume | normal | normal | normal upstream, weaker intents downstream | broken, stepped, one channel silent, or pixel steady while ads-reported conversions collapse | normal |
| Scope | one or few creatives | whole campaign or account at once | the broadened slice of traffic | everything optimizing on the broken event | whole account, and peers too |
| Industry benchmark | peers unaffected | peers unaffected | peers unaffected | peers unaffected | peers also degraded |

## 2. The kill-criteria table (binding, also printed in the referee brief)

| Theory | KILLED if all of these hold |
|---|---|
| Creative Fatigue | Frequency flat (under 10 percent rise) AND CTR stable or rising; OR all creatives stepped on one date; OR new creatives decay identically at launch |
| Delivery and Budget | No spend step, budget footprint, bid change, or entity birth or pause within 3 days either side of the break; CPM smooth; the errors check empty |
| Traffic Quality | Placement and demographic mix stable (no segment moves 10 share points) AND click-to-cart AND cart-to-purchase rates stable through the break |
| Tracking | Optimized-event volume steady through the break, stable vs the upstream reference event, both channels firing in their usual ratio, no rules deactivated, EMQ stable, AND ads-reported conversions did not diverge from pixel-side event volume through the break |
| Outside World | CPM and CPC flat or falling; auction benchmarks stable; peers steady while the account fell; no reported offer or site change; no seasonal match |

## 3. Synthesis rubric

Ranking rules, applied in order:
1. Verdict class: SURVIVED ranks above WOUNDED ranks above UNTESTED. KILLED never ranks; killed theories go to a "Ruled out" section with their killing evidence. That section is half the member value: "your gut theory is dead, here is why".
2. Within class: confidence level.
3. Tie-break: mechanism completeness, meaning the theory explains timing AND magnitude AND scope of the break.
4. Tie-break: fewest assumed unobserved events.
5. Cause-symptom pairs render as ONE chain ranked at the cause's position, with the symptom indented beneath it and the line "fix the cause; the symptom resolves with it".

Canonical cause-symptom chains the referee tests and the synthesis renders:
- A delivery change causes a traffic-quality collapse (a budget or bid event precedes the mix or conversion-rate shift by 0 to 2 days).
- A tracking break causes apparent delivery chaos (optimization starved of events).
- External auction pressure causes delivery instability (CPM inflation forces pacing changes).
- Fatigue causes delivery drift (a quality ranking penalty raises CPM and spend reallocates).
The rule: the cause must precede or co-date the symptom, and a mechanism must be stated.

Confidence levels, operational:
- HIGH: survived refutation AND at least 2 independent confirming signals from different slices AND timing aligns within 2 days AND magnitude plausibly accounts for the break.
- MEDIUM: survived or wounded with one strong signal; or timing loose (within a week); or magnitude explains only part of the break.
- LOW: not killed but circumstantial only.

Caps, applied mechanically with the stamp shown in the report:
- If Tracking is WOUNDED or SURVIVED, every conversion-dependent theory caps at MEDIUM with the stamp "capped: measured on possibly corrupted data".
- If the after-side window is under 14 days, all confidences cap at MEDIUM and the report says why.

The single most important action this week: exactly one. It must name the entity (name and ID),
the specific change, the expected effect, the verification signal, and when to check it
("compare cost per purchase for the 5 days after the change against the 5 days before"). When
the diagnosis exonerates a creative the member suspected, the action block includes an explicit
guard: "Do NOT pause <ad name>. The panel cleared it: <one line of evidence>." That guard is
the reason this method exists.

## 4. Report templates

### 4.1 Quick check (the file and the chat summary share this skeleton)

```
# Quick check: <Account Name>, <window> vs <previous window>

## The one thing to do this week
<one action, one paragraph, with entity names>

## What is working
<3 to 6 bullets, every bullet cites metric, value, and window>

## What is off
<3 to 6 bullets, same citation rule, each with a one line "what I would do">

## Meta's own flags
<opportunity score recommendations and anomaly observations in plain words, "none" is fine>

## What I could not see from here
<short list with where to look manually>

Run /ai-ad-lab:meta-analyze again and pick deep diagnosis if one of these looks like a real
break rather than a wobble.
```

### 4.2 Deep diagnosis report.md (canonical layout)

```
# Why <Account Name> broke: ranked diagnosis

Run <date>. Window: <since> to <until>. Break date: <date> (<member-stated | detected>).
Spend in window: <X CUR>. Investigators: <N seated>/<5>. Referee pass: complete<, plus one follow-up round | , first-pass verdicts>.
<If any seat was empty: "Empty seat: <name>, <reason>, its theory is listed UNTESTED.">

## Read this first
<The break in one line: "<metric> moved from <before> to <after> around <date> and persisted.">
<One short plain-words paragraph: most likely cause, confidence, and the single most important
action this week. A member who reads nothing else gets the answer here.>

## Ranked diagnosis

### 1. <Plain-words theory name>   MOST LIKELY CAUSE
- **What happened:** <2 to 4 plain sentences>
- **Confidence:** High / Medium / Low  <plus the cap stamp when it fired>
- **Survived the referee:** Yes. <The strongest attack against it and why the attack failed.>
- **Cause or symptom:** Cause. <If a lower-ranked theory is its symptom, name it.>
- **Evidence for:**
  - <metric, value(s), exact date range>   (every bullet cites all three)
- **Evidence against:**
  - <same discipline; "none found" allowed but the referee must have looked>
- **What would change this:** <specific data or event>
   <indented symptom line when paired: "Symptom of this cause: <theory>, fix the cause and this resolves.">

### 2. <theory>   <SECONDARY | SYMPTOM OF #1 | WOUNDED | UNTESTED>
<same block; UNTESTED blocks state what data was missing>

## Ruled out
- <Theory>: KILLED. <killing evidence: metric, value, dates>
<Dead theories stay in the report. Seeing WHY fatigue was ruled out is what stops the member
from killing a winning creative anyway.>

## What the panel argued about
<Only when the supplementary round fired: each objection, the recalled investigator's
DEFEND/CONCEDE/AMEND response, and what the referee concluded.>

## Cause and symptom map
<e.g. "The budget change on <date> (cause) widened delivery into cheaper, lower intent
placements, which produced the click to purchase collapse (symptom). Fix the cause and the
symptom resolves. Do not treat the symptom separately.">

## The single most important action this week
<Exactly one action: entity name and ID, the specific change, the expected effect, the
verification signal, and when to check.>
<When the action is a change in the account: "I can make this change for you through
/ai-ad-lab:meta-build, with the same confirm before anything happens, or do it in Ads Manager
here: <ads_manager_url>.">
Do not: <guard lines when applicable, e.g. "Do NOT pause <ad name>. The panel cleared it:
<one line of evidence>.">
This skill changed nothing in your account.

## Watch after you act
<2 to 3 signals and the date to re-check; offer to re-run analyze then.>

## What I could not check from here
<Only what the MCP genuinely cannot see, each with where to look: landing page changes and
site speed, checkout and site conversion config beyond pixel events, GA or Shopify conversion
truth, consent or CMP changes, competitor promos beyond Ad Library visibility, organic, email,
and SMS demand shifts, Ads Manager change history (edits were inferred from spend and CPM
steps, confirm in Account history), ad rejection and account restriction status, billing
history. Pixel volume, placement mix, auction pressure, and delivery errors were checked live
and never belong on this list.>

## Appendix: the numbers
<Before and after table for the key metrics, parsed values with the account currency stated.>

## Appendix: data provenance
<Rendered from provenance.json: one row per call (tool suffix, level, window, rows, pages,
truncated, self-corrections), the verified field list, dropped fields, slice row counts,
any isolation-breach discards, whether the supplementary round fired.>

<Footer: the data note plus the one-line cleanup offer, wording in the SKILL.>
```

HTML version: same content as report.md, ranked cards with a green SURVIVED chip and a red
RULED OUT chip, confidence shown as words not percentages, brand-neutral styling, one single
self-contained file, no external assets. Rendered last; a render failure never blocks the run.

## 5. Worked example (illustrative, from the member-submitted case, not a benchmark)

An account where cost per purchase nearly tripled mid-month. The operator's gut said creative
fatigue, because the hero ad had been running longest. The data said otherwise. Everything
stepped overnight on a single date:

| Signal | Before | After |
|---|---|---|
| Daily spend | ~198 | ~399 |
| CPM | 17.75 | 11.89 |
| Link CTR | 1.59% | 1.65% |
| Frequency | ~1.55 | ~1.78 |
| Click to add-to-cart | 16.2% | 4.4% |
| ROAS | 2.30 | 1.10 |

The referee killed the fatigue theory cleanly. Fatigue needs rising frequency and falling CTR,
but here CTR went UP for all three creatives, CPC dropped 35 percent, frequency barely moved,
and all three broke on the exact same overnight cliff. Fatigue decays creative by creative, it
does not hit a whole account at once.

The real cause: a budget change that doubled daily spend, which broadened delivery into
cheaper, lower-intent inventory (CPM down 33 percent). Those diluted clicks died at the first
on-site step, click-to-cart collapsed from 16.2 to 4.4 percent while everything downstream of
the cart stayed healthy. The fix was a one-line budget rollback, not a reshoot. It saved a
creative the operator was about to kill. Read it as the canonical cause-and-symptom chain: the
delivery change was the cause, the traffic-quality collapse was its symptom.

---

## 6. Data-staging spec

### 6.1 Field verification candidate list (one ads_get_field_context call, before any metric pull)

```
["spend","amount_spent","impressions","reach","frequency","clicks","ctr","cpc","cpm",
 "purchase_roas","results","cost_per_result","cost_per_conversion",
 "actions:omni_purchase","actions:link_click","actions:lead",
 "actions:omni_add_to_cart","actions:omni_initiated_checkout","action_values:omni_purchase",
 "video_p25_watched_actions","video_p50_watched_actions","video_p75_watched_actions",
 "video_p95_watched_actions","video_p100_watched_actions",
 "objective","optimization_goal","bid_strategy","daily_budget","lifetime_budget",
 "created_time","start_time","stop_time","status","effective_status",
 "creative_id","adset_id","campaign_id"]
```

Rules: anything echoed in `unknown_fields` is dropped from every subsequent pull (revenue falls
back to roas times spend). Resolve aliases per the response (`spend` to `amount_spent`, `roas`
to `purchase_roas`) and use canonical names in `fields`, `filtering`, and `sort`. Record the
verified set in provenance.json. Backstop: if a later call still rejects a field, the error
echoes the full valid-field list for that level; self-correct silently from it and log the
substitution in provenance, never showing the raw error. One uniform rule: EVERY metric field
in EVERY pull goes through this verification, video watch fields and cart and checkout actions
included. No special cases.

### 6.2 Deep-mode pull plan

Defaults for every `ads_get_ad_entities` call: `ad_account_id`; `fields` always includes `id`
and `name` for entity rows; `time_range: {"since","until"}` with explicit dates (lowercase
presets belong to this tool only; the `ads_insights_*` tools use UPPERCASE presets or
`date_from` and `date_to`); daily series use `time_increment: 1`; `limit: 1000`; follow
`next_cursor` or `page_info.after_cursor` by passing the exact value back, stop after 5 pages
and set `truncated: true` in provenance.

Objective-aware mapping applied everywhere "purchase" appears: OUTCOME_SALES uses
`actions:omni_purchase`, `purchase_roas`, `cost_per_conversion`; OUTCOME_LEADS uses
`actions:lead`, `cost_per_result`. Detected from the campaign attribute pull.

| # | Pull | Level | Time | Fields (post-verification) | Notes |
|---|---|---|---|---|---|
| P1 | Account daily series | account | W, daily | amount_spent, impressions, reach, frequency, clicks, ctr, cpc, cpm, purchase_roas, actions:omni_purchase, actions:link_click, verified funnel actions | Backbone of slices C, E, and D's ads-reported series |
| P2a | Ad totals, top | ad | W | id, name, adset_id, campaign_id, created_time, impressions, reach, frequency, ctr, cpc, clicks, actions:omni_purchase, purchase_roas, amount_spent | sort `impressions_descending`, limit 100 |
| P2b | Ad totals, bottom | ad | W | same | sort `impressions_ascending`, limit 100, only if `summary.total_count` > 100 (both-direction rule) |
| P3 | Ad daily series | ad | W, daily | date plus the P2 metric set minus created_time | Scope: ads covering ~90 percent of window impressions, cap 30, via `filtering: [{"field":"ad.id","operator":<from field context, typically IN>,"value":[ids]}]`. Row estimate = ads x days; over 1000, split W into sub-windows and concatenate |
| P4a/P4b | Adset before / after | adset | before; after | id, name, campaign_id, optimization_goal, bid_strategy, daily_budget, lifetime_budget, amount_spent, impressions, cpm, reach | Structural before and after comparison for slice B |
| P5 | Campaign attributes | campaign | none | id, name, status, effective_status, objective, buying_type, bid_strategy, daily_budget, lifetime_budget, created_time, start_time, stop_time | No time window means attributes only |
| P5b | Campaign daily | campaign | W, daily | amount_spent, impressions, reach, cpm | Slice B spend and CPM series |
| P6 | Ad attributes | ad | none | id, name, status, effective_status, created_time, creative_id, adset_id, campaign_id | days_live computed at staging |
| P7a/P7b | Placement before / after | campaign | before; after | impressions, clicks, ctr, cpm, actions:omni_purchase | `breakdowns: ["publisher_platform","platform_position"]`; mix table built at staging; goes to slice C |
| P8a/P8b | Demographics before / after | account | before; after | same as P7 | `breakdowns: ["age","gender"]`; goes to slice C; optional third pair `["country"]` only when geo expansion is suspected from intake |
| P9 | Datasets | n/a | n/a | n/a | `ads_get_datasets(ad_account_id)`; de-duplicate by `dataset_id`; record `is_active`, `last_fired_time`, `server_last_fired_time` (epoch value means CAPI has never fired) |
| P10 | Dataset stats | n/a | last 28d max | n/a | Per active dataset, three pull groups: the optimized event with `event_source: "WEB_ONLY"` and again `"SERVER_ONLY"`; an upstream reference event (ViewContent or PageView) for ratio analysis; one `aggregation: "event_total_counts"` baseline. `start_time` and `end_time` as Unix-timestamp strings from max(W.start, today minus 28d). Break older than about 24 days: the slice header and the report note the truncation |
| P11 | Dataset quality | n/a | n/a | n/a | `ads_get_dataset_quality(dataset_id, query_type: "web")`; low-volume pixels may return event names with no EMQ figures, which is normal |
| P11b | Dataset details | n/a | n/a | n/a | `ads_get_dataset_details(dataset_id)`; `gateway_status: NOT_ONBOARDED` is a finding, not an error |
| P12 | Pixel event rules | n/a | n/a | n/a | `ads_pixel_event_read(items:[{pixel_id}])`; INACTIVE Purchase rules on a sales account are a smoking gun |
| P13 | Custom conversions | n/a | n/a | n/a | `ads_get_customconversions(ad_account_id)`; a "gradually rolling out" message means unavailable here, log and continue |
| E1 | Auction benchmarks | n/a | W | n/a | `ads_insights_auction_ranking_benchmarks(ad_account_id, date params)`; slice E |
| E2 | Industry benchmark | n/a | W | n/a | `ads_insights_industry_benchmark(ad_account_id, analysis_metric: "CPM")` and a second pull with `"CPR"`; like-for-like note; slice E |
| E3 | Ad Library | n/a | n/a | n/a | `ads_library_search` ONLY if the member named competitors: `page_ids` or `search_terms` plus `countries`; report `estimated_total_count` and delivery-start clustering near the break; slice E |
| B1 | Delivery errors | n/a | n/a | n/a | `ads_get_errors(entity_ids: all campaign, adset, and ad ids from P5, P4, P2)`; child ids only; `{"errors":"{}"}` is itself evidence; slice B and the referee pack |
| R1 to R3 | Oracle pack | n/a | W | n/a | `ads_insights_advertiser_context` (feeds case.md); `ads_insights_anomaly_signal` (verbatim, with the observations-not-causes caveat attached); `ads_insights_performance_trend(analysis_level: "ADSET", analysis_metric per the broken metric)`; `ads_get_opportunity_score`. REFEREE PACK ONLY except advertiser_context |

On a young or no-spend account every `ads_insights_*` tool and the opportunity score
legitimately return "no data" strings or empty lists; stage those strings as-is, they are
evidence of account youth, not failures.

### 6.3 Insights routing rule (binding)

- Referee-only narrative oracles: `ads_insights_anomaly_signal`, `ads_get_opportunity_score`, `ads_insights_performance_trend`. They ship pre-baked diagnosis strings; handing them to an investigator is institutionalized anchoring. They land only inside full-dataset.json.
- Investigator E instruments: `ads_insights_auction_ranking_benchmarks`, `ads_insights_industry_benchmark` (comparative numbers, not narratives), plus `ads_library_search` results when present.
- Case statement: `ads_insights_advertiser_context` (vertical and funnel framing; a null vertical renders "Vertical: \N", keep as-is).

### 6.4 Slice encoding and the _manifest blinding header

Every slice file: `{"_manifest": {...}, "columns": [...], "rows": [[...]]}` plus named
sub-tables where a slice carries more than one table (for example `"placement_mix":
{columns, rows_before, rows_after}`). Values are parsed plain numbers; the main session strips
Meta's formatted currency strings at staging time; investigators never parse formatted strings.
full-dataset.json keeps raw and num pairs for display fidelity.

`_manifest` header schema (mandatory, the blinding declaration):

```json
{
  "investigator": "creative-fatigue",
  "built_at": "<ISO timestamp>",
  "window": {"since": "...", "until": "...", "break_date": "..."},
  "level": "ad",
  "currency": "USD",
  "tool_calls": ["P3", "P6"],
  "fields_included": ["..."],
  "excluded_by_design": ["amount_spent", "budgets", "cpm", "purchases", "roas", "..."],
  "rows": 812,
  "truncated": false,
  "note": "This file intentionally contains only the fields listed. Do not infer values for fields not present."
}
```

### 6.5 Slice contracts (contains and deliberately withheld)

| Slice file | Contains | Deliberately withheld |
|---|---|---|
| slice-creative-fatigue.json | per-ad daily: date, ad_id, ad_name, days_live (from created_time), impressions, reach, frequency, ctr, cpc, clicks; verified video watch fields when video ads exist | amount_spent, all budgets, cpm, ALL conversion fields, placement and demographic mixes, entity structure beyond ids, pixel data |
| slice-delivery-and-budget.json | campaign and adset daily spend, impressions, reach, cpm (P5b, P4); full attribute inventories incl. budgets, bid_strategy, optimization_goal, created, start, and stop times, status (P5, P4, P6 attributes); the adset before and after table; the B1 errors result (empty is evidence) | ctr, cpc, frequency, conversions, roas, placement and demographic mixes, pixel data. The brief carries the honesty note: no change-history log exists, label inferred edits "inferred edit" |
| slice-traffic-quality.json | account daily: date, impressions, clicks, ctr, cpc, cpm, link clicks, conversion counts, verified cart and checkout actions; precomputed daily funnel rates (click to cart, cart to checkout, checkout to purchase, whichever resolved); the placement mix before and after table (P7); the demographic mix before and after table (P8) | amount_spent, budgets, bid strategy, purchase_roas and revenue, entity inventory and created_times, frequency, days_live, pixel data |
| slice-tracking.json | per-day pixel event counts by event name with the web vs server split (P10); EMQ and quality summary (P11); gateway_status (P11b); event rule inventory and statuses (P12); custom conversions list or the unavailable marker (P13); dataset last-fired times (P9); PLUS exactly one ads-side series, date and ads_reported_conversions for the primary event from P1; the break date and the optimized event name | ALL other ads performance data: no spend, no ROAS, no CPA, no CTR, no clicks, no budgets, no entity structure |
| slice-outside-world.json | account daily: date, impressions, reach, cpm, cpc (the cost environment from P1); auction ranking benchmarks verbatim (E1); industry benchmark results verbatim (E2); Ad Library results when present (E3); the member's intake question 4 answers verbatim; the break date with the calendar-inference labeling rule | amount_spent, budgets, entity structure, conversion counts, roas, ctr, frequency, placement and demographic mixes, pixel data |

Caps: 300 KB or 3000 rows per slice (aggregate ad level up to adset level and record it in the
_manifest and the report); 10000 rows for full-dataset.json; truncation keeps the most recent
days first and sets `truncated: true`.

### 6.6 full-dataset.json (the referee's universe)

Everything above, un-blinded, plus: a campaign-level daily pull with the complete metric set
(amount_spent, impressions, reach, frequency, clicks, ctr, cpc, cpm, actions:link_click, the
primary conversion action, purchase_roas, cost_per_conversion, results, cost_per_result, plus
resolved cart and checkout actions), the three oracle outputs verbatim, and a copy of every
slice _manifest so the referee knows exactly what each investigator could and could not see.
Values stored as raw and num pairs.

### 6.7 provenance.json schema (call ledger plus run state)

```json
{
  "run_id": "deep-diagnosis-2026-06-11-141503",
  "mode": "deep",
  "ad_account_id": "123456789",
  "currency": "USD",
  "window": {"since": "...", "until": "...", "break_date": "...", "break_source": "member-stated|detected"},
  "stage_completed": "fanout",
  "verified_fields": ["..."],
  "dropped_fields": ["..."],
  "calls": [
    {"seq": 1, "tool_suffix": "ads_get_ad_accounts", "level": null, "time_params": null,
     "fields_or_breakdowns": null, "row_count": 2, "pages_followed": 1, "truncated": false,
     "self_corrections": []}
  ],
  "slices": [{"file": "slice-creative-fatigue.json", "rows": 812, "truncated": false}],
  "agents": [{"role": "investigator:creative-fatigue", "invoked_at": "...", "returned": true,
              "discarded_for_isolation_breach": false}],
  "supplementary_round": {"fired": false, "recalls": [], "data_requests": []}
}
```

No prefixes are ever recorded, suffixes only. `stage_completed` lets an interrupted deep run
resume without re-pulling. The report's data provenance appendix renders the calls table (tool
suffix, level, window, rows, pages, truncated, self-corrections) plus the verified and dropped
field lists.

### 6.8 Sufficiency thresholds (the deep-mode gate)

| Requirement | Threshold |
|---|---|
| Primary conversions in the window W | 30 or more |
| Link clicks in W | 1,000 or more |
| Delivery days on EACH side of the break | 7 or more |
| Ads that delivered in W | 3 or more (cheap pre-check, run first) |

ALL are required for the panel. The thresholds are currency-free on purpose. Failing any:
degrade to the quick check with the degrade wording in the SKILL. Special routes: break 7 to
13 days old, run with all confidences capped MEDIUM and say so; break older than about 24
days, run with the warning that the Tracking seat sees at most 28 days back; spend exists but
zero conversions have EVER tracked, skip the panel and run the tracking-first check.

### 6.9 Window math

`before = D-14 .. D-1`, `after = D .. min(today, D+14)`, where D is the confirmed break date.
The full window W spans both sides and drives every daily series. If the after side has under
5 days, warn the member that confidence is limited. Break-point detection when no date was
given: largest sustained shift, meaning the biggest 3-day-mean versus prior 3-day-mean delta
in the primary cost metric that persists at least 3 days; below a 25 percent sustained shift,
nothing looks broken and the skill offers the quick check instead.
