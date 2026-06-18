# Build chain spec, 51_meta_build (ex ai-ad-lab-meta-build)

Operational methodology for the create chain, creative resolution, error recovery, manifests,
update flows, and resume. Drift rule, binding on this file: no parameter or enum tables are
restated here; every tool fact cites the operator guide
(`references/meta-ads-mcp-operator-guide.md`) by section number, and the guide always wins on
tool facts. Angle-bracket placeholders inside template blocks are filled at run time.

---

## 1. The create chain (guide sections 9 and 12C)

Manifest discipline binds every step: write the intent record BEFORE the call, write the
returned id, status, and ads_manager_url AFTER success (schema in section 4).

1. **Campaign.** `ads_create_campaign` per guide section 9. Objective mapping from intake
   words, ODAX only (guide section 9 lists the six values): sales to OUTCOME_SALES, leads to
   OUTCOME_LEADS, traffic to OUTCOME_TRAFFIC, engagement to OUTCOME_ENGAGEMENT, awareness to
   OUTCOME_AWARENESS, app installs to OUTCOME_APP_PROMOTION. Never emit a legacy objective
   name. `buying_type` AUCTION. CBO is the default: the budget lives on the campaign and never
   on the ad set; ABO only on explicit member request, in which case the campaign carries no
   budget and each ad set does (guide section 1, CBO and ABO are mutually exclusive).
   `campaign_bid_strategy` defaults to LOWEST_COST_WITHOUT_CAP (guide section 9).
   `special_ad_categories` from intake, `special_ad_category_country` when declared. Naming per
   section 7 below. Capture: `campaign_id`, `status` (must read PAUSED), `ads_manager_url`,
   `valid_optimization_goals`, `recommended_optimization_goal`.
2. **Post-create goal enforcement.** The ad set's `optimization_goal` MUST be in the captured
   `valid_optimization_goals`. Default to `recommended_optimization_goal` when present, else
   the guide's first-listed default for the objective (guide section 9 table). The member may
   pick an alternative only from the valid list. This check cannot run pre-create because the
   list only exists in the campaign create response (guide section 9).
3. **Ad set.** `ads_create_ad_set` per guide section 9. `billing_event` IMPRESSIONS.
   `promoted_object` is REQUIRED for the conversion goals the guide enumerates in section 9
   (sales: pixel_id plus custom_event_type PURCHASE; website leads: same shape with LEAD).
   `destination_type` when a messaging or profile goal is chosen. Targeting floor:
   `{"geo_locations":{"countries":[...]}}` with the member's countries. NEVER invent interest
   IDs; no interest-search tool exists (guide section 9), so the three audience options are
   broad default, an existing audience id from discovery, or IDs the member pastes from Ads
   Manager. Advantage+ audience is auto-enabled; a demanded hard age cap sets
   `targeting_automation.advantage_audience` to 0 with the why stated (guide section 9). Age,
   gender, and the audience-reference key beyond the guide's documented floor follow the
   loaded tool's own runtime parameter documentation, which outranks memory. DSA beneficiary
   and payor when geo includes any EU-27 country (list in section 6; guide section 9 requires
   the fields for EU geos). Capture: `ad_set_id`, `status`, `ads_manager_url`.
4. **Creative.** Per the decision tree in section 2: `ads_create_creative` (guide section 7),
   capturing `creative_id`. The promote-a-post path skips this step entirely.
5. **Ad.** `ads_create_ad` per guide section 9 with `creative` carrying exactly one source:
   `{"creative_id":"..."}` or `{"object_story_id":"<pageID_postID>"}`. Billing validation
   fires here on accounts without a payment method (guide section 13, subcode 1359188; the
   recovery is in section 3). Capture: `ad_id`, `status`.
6. **Verification read-back.** `ads_get_ad_entities` per level, attributes only (no time
   window, guide section 1), filtered to the created ids, confirming everything reads PAUSED
   with the intended settings.
7. **Post-create health.** `ads_get_errors` with the three created ids (child ids only, guide
   section 5), and `ads_get_opportunity_score` (the guide recommends it after creating, guide
   section 9).

## 2. Creative resolution decision tree (guide section 7)

Ask first: "Where does your ad image or video live right now? 1. Already uploaded to Meta's
ad library. 2. It is a published post on your Page. 3. Only on this computer."

**Flow 1, existing upload.** `ads_get_ad_images` returns hash and name only by default (guide
section 7, partial-by-default). Show a named, numbered picker, newest first when dates are
available. If the member knows the filename, narrow with the name substring parameter. After
the pick, re-query by `hashes` with explicit fields for dates plus `url_128` or
`permalink_url` and show the thumbnail link so the member visually confirms THE image before
it goes into an ad. Multiple name matches: newest created_time wins, member confirms. Videos:
same pattern with `ads_get_ad_videos` (title search, then re-query by `video_ids` with
explicit fields). A video creative ALSO requires a thumbnail (guide section 7): prefer an
`image_hash`; the video's `picture` URL as an `image_url` fallback carries the guide's
unreliability warning. Image creatives never use `image_url`, hard line.

**Flow 2, promote a post.** Explain the shape once: "I need the post's ID in the form
pageID_postID. Open the post on your Page, the numbers are in the URL, or paste the post URL
here and I will extract them." Build `ads_create_ad` directly with
`creative: {"object_story_id":"<pageID_postID>"}`, skipping `ads_create_creative` (guide
section 9). Copy deck fields do not apply on this path, the post IS the creative; say so.

**Flow 3, manual upload, then rediscover.** No upload tool exists in this MCP (guide sections
7 and 13); never pretend otherwise. Say: "Meta does not let me upload files directly, so this
one step is yours, it takes about a minute. Open Ads Manager, find the media or asset library,
and upload your image there. When it is done, tell me the exact file name and I will find it
in your account and carry on." Then run Flow 1 with the name substring. Zero matches: wait 30
seconds and retry once (asset indexing can lag), then ask the member to confirm the spelling.

**Copy deck integration.** Present the newest deck from `06_Ad_Copy/` as a numbered
menu of headlines, primary texts, and descriptions. Chosen values go VERBATIM into
`ads_create_creative`: the guide's mapping is `message` for Primary text, `headline` (title)
for Headline, `description` for description (guide section 7). `call_to_action_type` defaults:
SHOP_NOW for sales, SIGN_UP for leads, LEARN_MORE otherwise; the member can override with any
value from the guide's documented enum (guide section 7).

**Instagram identity, asked once here:** "Should this ad also run under your Instagram account
identity? If yes, paste your Instagram account ID (Page settings, linked accounts). If you
skip this, the ad runs without Instagram delivery." An omitted `instagram_user_id` means no
Instagram delivery (guide section 7); surface it, never silently default it.

## 3. Error-to-recovery catalog (guide section 13)

Error codes appear in member copy once, in parentheses, after the plain-words explanation.

| Signal | Member-facing recovery | Skill behavior |
|---|---|---|
| No Payment Method on ad create or activation (subcode 1359188) | "Meta blocked this because the ad account has no payment method (their code 1359188). Open Ads Manager, Billing and payments, add a card, then tell me done." | Park the chain at the manifest; retry ONLY the failed call on "done". The preflight fork (SKILL Step 0c) already warned, so this should rarely surprise. |
| Custom audience terms not accepted (subcode 1870090) | "Customer list audiences need a one-time terms acceptance Meta only shows in the browser (their code 1870090). Open Ads Manager, Audiences, start creating a Customer list audience, accept the terms screen, then tell me done. Or say website audience and I build a site-visitors audience from your pixel instead, no acceptance needed." | Offer the WEBSITE subtype path immediately, it is usually the faster unblock (guide section 8). |
| Field rejected on a read | nothing shown | Self-correct silently from the echoed valid-field list (guide section 13) and log the substitution. |
| Transient 500 or INTERNAL try again later | nothing shown unless final: "Meta's side is having a moment. Your progress is saved in the manifest, run me again in a few minutes and I resume where we stopped." | Retry up to 3 times with 2, 5, and 15 second waits. On any ambiguous CREATE failure, run adopt-by-name (section 7) between attempts. After the third failure, park with the manifest. |
| FBIDTypeError got zero, or generic Invalid parameter on placeholder-looking ids | nothing shown | Internal guard: a placeholder id leaked into a call. Re-resolve the id from the manifest or re-run discovery. Never ask the member for raw FBIDs the skill can fetch. |
| Event type or parameter type not available for your data source category (pixel writes) | "Your pixel's category does not allow that event type. This is a property of the pixel, not a mistake. We can pick another event or skip it." | Not retried (guide section 6). |
| Gradually rolling out on custom conversions | nothing shown | Mark unavailable, continue (guide section 6). |
| is_queryable false | surface `not_queryable_reason` plainly | Creation may work; warn that verification reads will fail. |
| Empty metrics on a young account | "No delivery data yet, which is normal for a new or paused account." | Expected state, not an error (guide section 0). |

## 4. Manifest schemas

### 4.1 build-manifest.json (machine manifest, the recovery state)

Path: `$BASE/<YYYY-MM-DD-HHMMSS>-<slug>/build-manifest.json`, slug from the
product or campaign name, lowercased and hyphenated. Written intent-before and id-after every
write call; `next_step` drives resume; "complete" is the terminal value.

```json
{
  "run_id": "2026-06-11-142233-glowserum",
  "created_by": "51_meta_build",
  "ad_account_id": "123456789",
  "currency": "USD",
  "min_daily_budget_cents": 100,
  "plan_approved_at": "2026-06-11T14:25:10Z",
  "validator_pass": true,
  "plan": {
    "objective": "OUTCOME_SALES",
    "buying_type": "AUCTION",
    "budget_mode": "CBO",
    "stated_amount_per_day": "40.00",
    "sent_cents_per_day": 4000,
    "special_ad_categories": [],
    "special_ad_category_country": null,
    "dsa": { "beneficiary": null, "payor": null },
    "geo_countries": ["US"],
    "optimization_goal": "OFFSITE_CONVERSIONS",
    "promoted_object": { "pixel_id": "123456789", "custom_event_type": "PURCHASE" },
    "creative_source": { "type": "image_hash", "value": "abc123", "page_id": "123456789" }
  },
  "entities": {
    "campaign": { "id": "120210000000000", "name": "Acme | Glow Serum | Sales | 2026-06-11", "status_at_create": "PAUSED", "ads_manager_url": "https://...", "created_at": "..." },
    "ad_sets": [ { "id": null, "name": "Acme | Glow Serum | Broad US | 2026-06-11", "attempted_at": "...", "last_error": "transient 500 after 3 retries", "ads_manager_url": null } ],
    "creatives": [],
    "ads": []
  },
  "audiences_created": [],
  "valid_optimization_goals": ["OFFSITE_CONVERSIONS", "VALUE", "LANDING_PAGE_VIEWS"],
  "budget_confirmations": [
    { "stated_amount": "40.00", "sent_cents": 4000, "currency": "USD", "confirmed": true, "at": "..." }
  ],
  "over_500_confirmation": null,
  "activations": [],
  "archive_actions": [],
  "next_step": "create_ad_set",
  "last_error": { "step": "create_ad_set", "message": "...", "at": "..." }
}
```

Notes: `validator_pass` is true or `{issues: [...], resolved_at}`. Every created entity
carries its `ads_manager_url`. Each `activations` entry records `{entity_type, entity_id,
name_echoed, confirmed_at, status_returned}`. `over_500_confirmation` records the typed daily
total string when that gate fired. `archive_actions` records any zz_archived_ renames.

### 4.2 manifest.md (member manifest)

```
# Campaign manifest: <campaign name>

Built <date time> in <Account Name> (<account id>), currency <CUR>.
Overall status: ALL PAUSED, NOTHING SPENDING   (update this line on every change)

## What exists
| Level | Name | ID | Status | Open in Ads Manager |
| Campaign | <name> | <id> | PAUSED | <ads_manager_url> |
| Ad set | <name> | <id> | PAUSED | <ads_manager_url> |
| Ad | <name> | <id> | PAUSED | <preview or manager link> |

## Money
Daily budget <X.XX> <CUR>, stored at Meta as <N> cents. You confirmed both numbers at <time>.
While paused this spends nothing.

## Targeting and goal
<plain words: goal, countries, audience choice, special category answer, EU names if given>

## Creative and copy
Image: <file name> (already in your account's library). Copy deck: <file path or "typed in
chat">. Preview: <preview_url>

## Activation checklist, in order
[ ] 1. Open the preview link and look at the ad one last time.
[ ] 2. Payment method: <"on file" / "MISSING, add one in Ads Manager billing or nothing will
       ever deliver">.
[ ] 3. Say "activate my campaign" in this chat, or flip each level on in Ads Manager yourself.
[ ] 4. After it goes live, leave it alone through the learning phase (below).

## What to expect after launch
Expect about a week of unstable results while Meta's learning phase settles. Do not edit
budget, audience, or creative during it, big edits restart the learning. <Insert the
specifics quoted from Meta's own help article, with its link, when the live fetch succeeded.>
Check in after about 7 days: open this project and run /pm-meta-analyze, quick check.
Only reach for the deep diagnosis if something still looks genuinely broken after learning
ends.

## If this build was interrupted
The table above is the source of truth for what exists. Campaigns, ad sets, and ads cannot be
hard deleted through this connection, so an unfinished structure is safe, it just sits paused.
Run /pm-meta-build again in this folder and it will offer to finish from this manifest
instead of starting over.
```

## 5. Update flows (writes to existing entities)

Build owns every write to the ad account, including entities it did not create. Per-action
ceremony table:

| Action | Tools (guide section) | Ceremony |
|---|---|---|
| Pause | `ads_update_entity` status PAUSED (section 9) | One confirmation naming the entity. Pausing is the safe direction; on an emergency stop, pause first and discuss second. |
| Unpause an existing campaign | `ads_activate_entity` (section 9) | This IS an activation. Full activation ceremony, bottom-up state check, over-500 math on the NEW total. |
| Budget change | `ads_update_entity` with budget cents (section 9) | Full budget echo (stated amount, computed cents, currency, account minimum). The over-500 typed confirm computes against the NEW total daily spend of the affected structure, not the delta. |
| Targeting update | `ads_update_entity` (section 9) | Echo the change in plain words. Re-ask DSA when the edit adds any EU-27 country. |
| Audience create | `ads_create_custom_audience` (section 8) | WEBSITE from the pixel with the guide's all-visitors rule shape and a member-confirmed retention (default 30 days). CUSTOM only on request, with the 1870090 recovery. LOOKALIKE and APP are not creatable here, say so and point at Ads Manager with a seed this skill can build. |
| Customer list upload | `ads_update_custom_audience_users` (section 8) | PII passes straight through to Meta; store only counts (`num_received`, `num_invalid_entries`) and the audience id. Never copy a row anywhere. |
| Audience delete | `ads_delete_custom_audience` (section 8) | The strictest ceremony: list dependent ad sets via `ads_get_custom_audience_adsets` first, state the permanence and the auto-pausing, require the member to TYPE THE AUDIENCE NAME exactly. Child lookalikes block deletion; surface plainly and route to Ads Manager. |
| Pixel event or parameter work | `ads_pixel_event_*`, `ads_pixel_parameter_*` (section 6) | Explicit yes per write. Carry the data-source-category gate wording from section 3 and remind that deleting an event rule does not auto-delete its linked parameters (guide section 6). |

Bulk guard: changing more than 3 entities in one request requires listing them all and one
explicit confirmation of the list.

DELETED coercion guard: if `ads_update_entity` returns `status_forced_to_paused: true`, tell
the member exactly what happened: "Meta does not allow deletion through this connection, so it
paused the entity instead. It will not spend, and you can delete it by hand in Ads Manager if
you want it gone." Never report a coerced pause as a successful deletion.

Archive convention: to retire an entity, one `ads_update_entity` call setting
`{"status":"PAUSED","name":"zz_archived_<date>_<original name>"}`. Record the rename in the
manifest under `archive_actions`. Never describe this as deletion; say archived and paused.

## 6. The EU-27 ISO-2 list (mechanical DSA trigger)

AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE

DSA beneficiary and payor are required whenever ad set geo includes any of these (guide
section 9). The check is mechanical against this list, never from memory.

## 7. Entity naming convention and the resume protocol

Naming convention, member can override: `<Brand> | <Product> | <Objective word> | <YYYY-MM-DD>`
for the campaign; descendants substitute their own descriptor for the objective word (for
example "Broad US"). The convention exists for member recognition in Ads Manager AND because
adopt-by-name recovery depends on exact, unique names.

Adopt-by-name (mandatory between retry attempts on any ambiguous create failure): a timeout or
transient 500 on a create may have succeeded on Meta's side, and a blind retry mints a
duplicate that nothing can hard-delete. Before any create retry: list recent entities at that
level with attributes only (`ads_get_ad_entities`, fields id, name, created_time, no time
window), look for the exact name from the manifest's intent record, and if found, adopt that
id into the manifest and continue the chain instead of retrying.

Resume protocol: at skill start, scan `$BASE/*/build-manifest.json` for
`next_step != "complete"` and offer resume, check, or fresh. On resume: verify every stored id
still exists with attribute-only reads (`ads_get_ad_entities` per level, `ads_get_creatives`
with creative_ids), reconcile the manifest against reality, then continue at `next_step`. On
check: report what exists on Meta's side versus the manifest, then re-offer. On fresh: run the
archive convention over the old run's entities, then start a new run folder. Never re-create
an entity whose id the manifest already holds.
