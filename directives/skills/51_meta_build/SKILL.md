---
name: 51_meta_build
description: Opera il Meta Ads MCP ufficiale direttamente dentro Claude Code per COSTRUIRE campagne complete nell'ad account live del brand — campaign + ad set + creative + ad, con audience di retargeting opzionali. Tutto creato PAUSED. I budget sono quotati nella valuta dell'account, convertiti in centesimi interi, ed entrambi i numeri confermati prima di ogni call. Totali sopra 500/giorno richiedono di digitare il numero per confermare, e nulla si attiva senza un sì esplicito per livello (ad → ad set → campaign = spend switch). È anche la sede di OGNI write su campagne esistenti: pause, budget change, targeting update, audience, customer list, attivazione. SA8/post-SA6. Sostituisce la modalità "build" del vecchio 30_meta_handoff. Trigger: /pm-meta-build, "costruisci una campagna", "lancia una campagna", "pubblica/attiva la campagna", "metti in pausa", "cambia il budget", "aggiorna il targeting", "crea un'audience", "carica la customer list". Per SOLA analisi/diagnosi → /pm-meta-analyze (read-only). Risolve i tool Meta per suffisso (`…ads_*`), mai hardcoda il prefix. Usa i copy deck da 06_Ad_Copy verbatim. Creatives via image_hash/video_id/object_story_id dall'account (il MCP non carica file). Output in output/{brand}_{campaign}_{date}/13_Meta_Campaigns/.
---

# SA8 — Meta Ads Build (51)

Questa skill è l'**UNICA superficie di write** sull'ad account Meta live del brand. Costruisce
campagne complete tramite il Meta Ads MCP ufficiale, dentro Claude Code, ed esegue ogni
modifica successiva alle campagne esistenti. Tutto creato PAUSED; l'attivazione è una cerimonia
separata con le sue conferme. Se il membro vuole solo guardare la performance o diagnosticare
un problema, usa /pm-meta-analyze, che è read-only by design.

> **Porting nota (project-specific).** Skill importata da The AI Ad Lab v2.4.0 (`ai-ad-lab-meta-build`),
> adattata: output sotto `output/`, comandi `/pm-*`, integrazione SA8. Il corpo operativo
> (cerimonie di sicurezza, narration member-facing, soglie) è preservato in inglese per fedeltà al
> design di sicurezza — la copy member-facing può essere consegnata in italiano (ToV brand). I 3 file
> in `references/` sono technical reference verbatim. La copy nel creative arriva VERBATIM dai deck
> `06_Ad_Copy/` (SA7).

> **Cambio di paradigma rispetto a `30_meta_handoff`.** Il vecchio handoff generava prompt da
> incollare in claude.ai web ("Meta MCP solo lì"). Non vale più: il connector Meta Ads
> (`mcp.facebook.com/ads`) è disponibile dentro Claude Code (`mcp__…__ads_*`, prefix per-install).
> Questa skill opera i write direttamente, con le cerimonie di conferma qui sotto.

## Scope and the loading discipline

Build owns all 18 write tools of the Meta Ads MCP plus the discovery reads. Tools load in
tiers, by stable suffix, never by prefix:

- Tier 1, at preflight: discovery reads only (`+ads_get` keyword load, max_results 30).
- Tier 2, only AFTER the member approves the written plan: `+ads_create` (max_results 10) plus `ads_update_entity ads_update_custom_audience_users` (max_results 4).
- Tier 3, only when the activation ceremony begins: `ads_activate_entity` (max_results 2).
- Rare paths, loaded only when the member explicitly requests that path: `ads_delete_custom_audience` (audience deletion) and `+ads_pixel` (pixel rule work). The loading event is part of the audit trail.

Emergency rule: at any moment, in any step, if the member says stop, pause, wait, or expresses
doubt about live spend, pause first and discuss second: call `ads_update_entity` with
`{"status":"PAUSED"}` on the campaign (pausing the campaign stops all delivery under it),
confirm it is paused, then talk.

Never call `ads_catalog_get_products`. It is deprecated; use `ads_catalog_search_product`.

## Reading the bundled references

Read `references/meta-ads-mcp-operator-guide.md` before your first MCP call. It is the single
source of truth for every tool name, parameter, convention, and limitation in this skill. Read
`references/build-chain-spec.md` before the create chain and for every update flow, and
`references/build-validation-checklist.md` at the validation step. All three files are bundled
inside this skill folder (`directives/skills/51_meta_build/references/`), so those relative
paths resolve from the skill folder.

## Step 0a, Resolve the project output folder

Output sotto `output/`. Convenzione: quando Claude Code è aperto in una **campaign working dir**
(`output/{brand}_{campaign}_{date}/`), il piano e i manifest vanno in `13_Meta_Campaigns/` lì
dentro. Altrimenti (run standalone dalla root progetto) vanno in
`output/reports/<YYYY-MM-DD>_meta_campaigns/`. Run this Bash block first:

```
PWD_ABS="$(pwd)"
case "$PWD_ABS" in
  */output/*/*|*/output/*)
    # CC opened inside a campaign working dir under output/
    BASE="$PWD_ABS/13_Meta_Campaigns" ;;
  *)
    # walk up to the project root (dir holding claude.md), route to reports/
    DIR="$PWD_ABS"; ROOT=""
    while [ "$DIR" != "/" ]; do
      if [ -f "$DIR/claude.md" ] || [ -f "$DIR/CLAUDE.md" ]; then ROOT="$DIR"; break; fi
      DIR="$(dirname "$DIR")"
    done
    if [ -z "$ROOT" ]; then echo "NOROOT:$PWD_ABS"; else
      BASE="$ROOT/output/reports/$(date +%Y-%m-%d)_meta_campaigns"
    fi ;;
esac
if [ -n "${BASE:-}" ]; then mkdir -p "$BASE"; echo "READY:$BASE"; fi
```

- `NOROOT:<path>`, tell the member to reopen Claude Code in the project folder (or a campaign folder under `output/`). Stop.
- `READY:<path>`, capture the path as `$BASE`. Continue silently. Run timestamps come from the system clock (`date +%Y-%m-%d-%H%M%S`). Each build run gets its own subfolder `$BASE/<YYYY-MM-DD-HHMMSS>-<slug>/` per the chain spec.

## Step 0b, Auto-discover context and detect unfinished builds

Scan with ls, find, and Read (never Meta tools). Paths relative to the campaign folder and project root:

- Campaign `06_Ad_Copy/` and `intermediate/sa7_copy_deck.md`: newest copy deck (headlines, primary texts, descriptions for Step 4).
- Campaign `02_Brand_DNA/` and `context/brand/business_profile.md` + `context/brand/tone_of_voice.md`: brand name powers the naming convention and DSA defaults.
- Campaign `01_VOC_Research/` and `intermediate/sa2_market_insights.md`: VOC context.
- `output/reports/<date>_meta_analysis/`: the newest analyze report from `/pm-meta-analyze`. When the member arrives from a diagnosis, pre-fill the intent from its recommended action and say so.

Resume detection: scan `$BASE/*/build-manifest.json` for any manifest with `next_step` not
equal to "complete". When found, send:

> I found an unfinished campaign build from <date>: the campaign "<name>" exists (paused, id
> <id>), and the run stopped at <step> with this error: <last_error in one line>. Nothing in
> that run can spend, everything was created paused.
>
> Want me to: resume from where it stopped (resume), re-check what exists on Meta's side first
> (check), or archive that run and start fresh (fresh)? Fresh pauses and renames anything the
> old run created with the zz_archived_ prefix.

The resume, check, and fresh mechanics are in `references/build-chain-spec.md` section 7.

## Step 0c, Find the Meta Ads tools (never hardcode a server prefix)

Never hardcode or assume an MCP server prefix. Meta's connector installs under an opaque,
per-install ID, so the same tool can be named `mcp__<anything>__ads_get_ad_accounts` on
different machines (in this project it currently surfaces as `mcp__claude_ai_Meta_Ads_MCP__ads_*`,
but you MUST resolve by suffix, never hardcode it). Identify every Meta tool by its stable
suffix only. Never write a prefix into a file, a message, or a tool call you compose from
memory.

Resolve the connection state, in order:

1. **State A, tools already callable.** Scan the session's available tools for any name ending in `ads_get_ad_accounts`. Found: go to the smoke test.
2. **State B, tools deferred.** If a ToolSearch tool exists, load tier 1 only: `+ads_get` (max_results 30). Later tiers load at their own steps per the loading discipline. Then go to the smoke test.
3. **State C, only the auth server present.** If no `ads_*` tools were found but tools ending in `authenticate` and `complete_authentication` exist (the facebook-ads server, operator guide section 2): call `authenticate` (no inputs), then send exactly:

> Your Meta connection needs a one-time login.
> 1. Open this link in your browser: <url>
> 2. Log in with the Facebook profile that has access to your ad account and click Allow.
> 3. Your browser will land on a page whose address starts with http://localhost. Copy that ENTIRE address from the address bar and paste it back here. It is safe to paste in this chat, I use it once to finish the connection and never show it again.

Call `complete_authentication` with `callback_url` set to the pasted URL. Never echo any part
of the pasted URL back. Re-run detection from state 1 (the tools may appear deferred, so the
ToolSearch pass runs again). Still nothing: "The connection succeeded but the tools have not
appeared in this session yet. Close this session, reopen it in the same folder, and run me
again. The connection is saved."

4. **State D, nothing present.** Send exactly:

> I could not find Meta's Ads tools in this session, which means the connector is not installed yet. One-time setup, about two minutes:
> 1. Open your Claude settings and find the Connectors section (on some versions it is under Settings then Connectors, on others under Settings then Extensions).
> 2. Choose to add a custom connector and paste this URL: https://mcp.facebook.com/ads
> 3. Complete the Facebook login when it asks. Sign in with the account that has access to your ad account.
> 4. Close this session, reopen it in this same folder, and run me again. Your project files are all saved, we pick up exactly where we left off.
> If you get stuck, run /pm-setup or ask the team.

Stop the skill after State D. Never guess at tools that are not present.

### The smoke test (always runs once tools are callable)

Call `ads_get_ad_accounts` with `limit: 25`.

- Auth or permission error: treat as State C if the auth server exists, else State D.
- Zero accounts: "Your Facebook login works, but it has no ad accounts attached. You may have logged in with a personal profile instead of the one connected to your Business Manager. Reconnect with the right profile, or check your access in Business settings."
- Filter to `is_ads_mcp_enabled: true`. For an ineligible account say: "This ad account is not enabled for Meta's MCP connection. Meta's stated reason: <is_ads_mcp_disabled_reason>. I will not use this account." and offer the other accounts when they exist.
- `is_queryable: false`: warn that creation may work but verification reads will fail, and recommend resolving `not_queryable_reason` first.
- Exactly one usable account: do not ask, state it: "I will work in **<Account Name>** (ID <id>, currency <CUR>). It is the only ad account connected here." Several: numbered picker with name, ID, currency, and a recent-spend marker.
- Capture for the whole run: `ad_account_id` (bare digits, never `act_`), `currency`, `min_daily_budget_cents`, `has_payment_method`, `business_id`, `account_status`. Every money sentence uses `currency`; never print a dollar sign unless the currency is USD.

Payment fork, surfaced HERE, never as a raw create error later. When `has_payment_method` is
false, send:

> One thing before we design anything. Your ad account has no payment method on file, and Meta
> blocks the final ad creation step without one (their error is "No Payment Method", code
> 1359188). Nothing is wrong with our setup, it is just how Meta works.
>
> Two ways forward:
> 1. Add a card now: open Ads Manager, Billing and payments, add a payment method, then tell me done and we continue.
> 2. Keep building anyway: I can create the campaign and ad set now, save the full plan, and we add the ad itself after you add a card. Nothing is lost either way.
>
> Which one?

## Step 1, Route: new campaign or change something existing

If the trigger or the member's words name an existing-entity action (pause, budget change,
targeting update, activate an existing campaign, audience work, customer list upload), route
to the update flows step below. Otherwise continue to intake. One line each, no menu when the
intent is clear.

## Step 2, Intake

Send one numbered message:

> Quick intake before I build anything. Answer what you know, say "default" for any item, and
> remember nothing goes live until you explicitly turn it on at the end. Everything is created
> paused.
>
> 1. What product or offer is this campaign for?
> 2. What is the goal? Sales, leads, traffic, engagement, awareness, or app installs. Default is sales.
> 3. Daily budget, for example 50.00 a day in your account currency. You can also give a lifetime budget with an end date instead, I need the end date to do the daily math. I will confirm the exact numbers with you again before anything is created.
> 4. Which countries should the ads run in? Default is US only.
> 5. Who is the customer, in one or two sentences? After this intake I will also show you any saved audiences already in your account, and I can build a website retargeting audience from your pixel if you want one. Default is broad targeting, which is what Meta currently rewards.
> 6. One legal question Meta requires for every campaign. Do your ads relate to any of these: housing (selling or renting property, real estate services), credit (loans, credit cards, financing, buy now pay later), or employment (job listings, recruiting)? Answer none, or name the ones that apply. Why this matters, in plain words: Meta legally requires these ad types to be declared, and declaring switches off some targeting options. Declaring when you did not need to costs a little reach. Failing to declare when you should can get the ad rejected or the account restricted, which is far worse. When in doubt, declare. And if your ads touch politics, elections, or social issues, stop here and set those up directly in Ads Manager, this skill does not handle that category.
> 7. Anything else I should know? Offers, deadlines, things you never want said. Default is nothing.

Binding notes:
- Question 6 maps none to the empty special ad categories list, and declared answers ONLY to the guide's enum values (HOUSING, CREDIT, EMPLOYMENT), never invented values, with one follow-up for the special ad category country, defaulting to the question 4 geo. A politics answer routes out of the skill, never into an enum. Never print parameter names to the member.
- Lifetime budgeting without an end date is refused: the over-500 math needs an effective daily spend.
- DSA is NOT asked here. It is a conditional follow-up at plan time when geo includes any EU-27 country (the mechanical ISO list is in build-chain-spec.md section 6), and it is re-asked whenever a later edit adds EU geo:

> Your targeting includes <countries>, which are in the EU. EU law (the Digital Services Act)
> requires two names on every ad there: who benefits from the ad and who pays for it. For most
> members both are simply the business name. I will set both to "<brand name>" unless you give
> me different names. Reply ok, or give me the beneficiary and payor names to use.

- Creative is deliberately NOT in the intake. It is its own step, because asking well requires live account data.

## Step 3, Discovery

- Page: `ads_get_ad_account_pages` first (it carries `leadgen_tos_accepted`); if empty, `ads_get_pages_for_business`; then `ads_get_user_pages`. One page: state it and continue. Several: numbered picker, "Which Facebook Page should the ad run from?". None anywhere: stop; Pages cannot be created here, the member connects one in Business settings.
- Pixel, only when the goal resolves to a conversion optimization: `ads_get_datasets`, de-duplicate by `dataset_id`, prefer `is_active` with a recent `last_fired_time`. Member wording: "I found your pixel, <name>, last active <date>." Stale beyond 7 days: warn in one line and continue, that is analyze territory, never block the build. `server_last_fired_time` at the epoch is informational.
- Audiences, when intake question 5 mentioned retargeting or an audience: `ads_get_ad_account_custom_audiences` with limit 100. Present only audiences with normal `delivery_status` and `operation_status`, flag the rest unusable. Offer WEBSITE creation from the pixel (the guide section 8 all-visitors rule shape with the real pixel id), retention confirmed with the member, default 30 days. CUSTOM (customer list) only on request, with the terms recovery in build-chain-spec.md section 3. LOOKALIKE and APP audiences are not creatable here; say so plainly and suggest creating lookalikes in Ads Manager from a seed this skill can build.

## Step 4, Creative and copy resolution

Ask: "Where does your ad image or video live right now? 1. Already uploaded to Meta's ad
library. 2. It is a published post on your Page. 3. Only on this computer."

Run the matching flow from `references/build-chain-spec.md` section 2. The member experience
rules: never ask for a hash cold, always show a named, numbered picker built from the
account's library:

> Here are the most recent images in your ad account's library:
>
> 1. summer-hero-v2.png, uploaded May 28
> 2. ugc-still-03.jpg, uploaded May 25
> 3. founder-story.png, uploaded May 12
>
> Reply with a number, or tell me the name of the file you expect to see and I will search for
> it. If your image only exists on your computer, say "not uploaded yet" and I will walk you
> through the one minute upload.

After any pick, re-query for the thumbnail link and show it so the member visually confirms
THE image before it goes into an ad. The "not uploaded yet" walk and the promote-a-post path
are in the chain spec. Hard line: never `image_url` for image creatives. Videos also resolve a
thumbnail.

Copy: present the newest deck from `06_Ad_Copy/` (o `intermediate/sa7_copy_deck.md`) as a
numbered menu; chosen headline, primary text, and description go VERBATIM into the creative;
the call to action defaults to SHOP_NOW for sales, SIGN_UP for leads, LEARN_MORE otherwise,
member can override. No deck:

> I looked in your project folder and there is no copy deck in 06_Ad_Copy yet. Three options:
>
> 1. Run /pm-meta-copy first. It writes headlines and primary text from your Brand DNA and VOC, takes a few minutes, and gives this campaign its best shot. I recommend this one<add only when Brand DNA or VOC exist: ", your Brand DNA and VOC are already done so it will be fast">.
> 2. Type your own headline and primary text right here and I will use them word for word.
> 3. Build the campaign and ad set now and attach the ad once you have copy.
>
> Reply 1, 2, or 3.

Instagram identity, asked once here: "Should this ad also run under your Instagram account
identity? If yes, paste your Instagram account ID (Page settings, linked accounts). If you
skip this, the ad runs without Instagram delivery."

## Step 5, The plan and Gate 1

Assemble the full plan and send ONE message containing, in order:

> Here is the plan in plain words. Nothing has been created yet.
>
> Campaign: <campaign name>. Objective <objective in plain words>. Budget <X.XX> <CUR> per day at the campaign level, sent to Meta as <cents> cents.
> Ad set: <ad set name>. Audience: <plain language audience description>. Optimization goal: <goal in plain words>. Geo: <countries>.
> Ad: <ad name>. Creative: <image name or post reference>. Headline: <headline>. Primary text starts: "<first line>".
> Special ad categories: <none declared | declared: HOUSING / CREDIT / EMPLOYMENT>.
> <If EU geo> DSA names: beneficiary <name>, payor <name>.
>
> Budget check. You said <X.XX> <CUR> per day. Meta's API takes budgets in integer cents, so I will send <cents>. Both numbers together: <X.XX> <CUR> equals <cents> cents. Your account currency is <CUR> and this account's minimum daily budget is <min> (<min_cents> cents).
>
> The honest fine print about undo, before anything is created: Meta's connection cannot delete campaigns, ad sets, ads, or creatives, not even ones we create by mistake, asking for deletion just flips the thing back to paused. Cleanup here means pause it (paused things never spend or bill) and rename it with the prefix zz_archived_ so it sinks to the bottom of your lists; true deletion happens only by hand in Ads Manager. Three things CAN be permanently deleted here: custom audiences (forever, and deleting one auto pauses any ad sets using it, so I always list those and ask first), and pixel event rules and parameters, which Meta archives when they were created through this connection.
>
> Everything will be created PAUSED. Paused things never spend a cent. Activation is a separate step with its own confirmations. Reply **build** to create it paused, **change** to adjust something, or **stop**.

A budget below the account minimum is caught here, before any call: "Quick check on the
amount. Meta's minimum daily budget on this account is <min> (<min_cents> cents, currency
<CUR>), and your <Y.YY> is below it, so Meta would reject the call. Want to use the minimum
<min>, or pick another amount?"

On build: save the message verbatim plus a timestamp as `plan.md` in the run folder, record
the budget confirmation in the manifest, and continue.

## Step 6, Validate the plan

Narrate one line: "Double checking the plan against Meta's rules before I create anything."

Launch ONE validator subagent with the brief in `references/build-validation-checklist.md`
section 2: inputs are the approved plan, the checklist verbatim, and the relevant guide
sections (1, 7, 8, 9, 12C, 13). It has no MCP access and is advisory. Output: PASS, or a
numbered issue list. On issues: fix them with the member (a material change re-opens Gate 1),
then re-validate. Record the result in build-manifest.json as `validator_pass`. When the Agent
tool is unavailable, walk the same checklist inline, line by line, and record the result the
same way. The optimization goal versus `valid_optimization_goals` check runs after the
campaign create, by the main session, because the list only exists in the create response.

## Step 7, The create chain

Load tier 2 now. Execute the chain in `references/build-chain-spec.md` section 1, step by
step: campaign, goal enforcement, ad set, creative, ad, verification read-back, post-create
health. The manifest is written intent-before and id-after EVERY write call. Narrate each
step:

> Creating the campaign, paused.
> Campaign created and paused. 1 of 3 levels done.
> Creating the ad set inside it, paused.
> Ad set created and paused. 2 of 3 levels done.
> Creating the ad with your creative and copy, paused.
> Ad created and paused. 3 of 3. Nothing is live and nothing has spent.

Error handling throughout: the catalog in build-chain-spec.md section 3. Transient errors
retry 3 times with 2, 5, and 15 second waits, with adopt-by-name between attempts on any
ambiguous create failure (chain spec section 7). After the third failure, park with the
manifest and the catalog's member-facing line. The transient narration line: "Meta hiccuped on
that request. Retrying in a few seconds, this is normal and nothing is wrong on your side."

## Step 8, Preview and the ceremony entry

Call `ads_get_ad_preview` with the ad id and the MOBILE_FEED_STANDARD format; always surface
`preview_url`. Offer INSTAGRAM_STANDARD and INSTAGRAM_STORY when Instagram delivery is on.
Then send:

> Your ad exists, fully assembled and PAUSED. Before we talk about turning anything on, look
> at it with your own eyes.
>
> Preview link: <preview_url>
>
> Open it and check the image, the headline, the text, and the link. Reply looks good to move
> to activation, change to fix something, or done to leave everything paused and finish here.
> Leaving it paused is a completely normal way to end, many members review in Ads Manager
> first and activate later.

"done" routes to the not-yet ending in Step 10. This message is the entry to the activation
sequence, not an extra gate.

## Step 9, The activation ceremony

Load tier 3 now. Bottom-up, one yes per level:

> Time to go live. Activation works level by level, and nothing delivers until all three
> levels are active and a payment method is on file. We go bottom up so the final yes is the
> one that starts spend.
>
> Step 1 of 3: activate the AD "<ad name>" (id <ad_id>)? It cannot spend yet, its ad set and
> campaign are still paused. Reply yes or skip.

On yes, call `ads_activate_entity` with entity type ad, report the returned status, then:

> Step 2 of 3: activate the AD SET "<ad set name>" (id <ad_set_id>)? Still no spend, the
> campaign above it is paused. Reply yes or skip.

On yes, activate, report. If the total planned daily spend exceeds 500 major units of the
account currency, run the typed-number double confirm NOW, before the final message. CBO
shape:

> This plan is above 500 <CUR> per day, so I need one extra confirmation, and I will spell the
> math out.
>
> Your campaign level budget is <Y.YY> <CUR> per day. That is one number for the whole
> campaign, and left untouched it is about <Y times 7> per week and about <Y times 30> per 30
> days.
>
> To confirm this budget, type the daily total in plain numbers: <Y.YY>. Anything else cancels
> activation and everything stays paused.

ABO shape replaces the middle paragraph with: "<X.XX> <CUR> per day times <N> ad sets equals
<Y.YY> <CUR> per day in total. Left untouched, that is about <Y times 7> per week and about
<Y times 30> per 30 days." Record the typed string in the manifest. Then:

> Step 3 of 3, the spend switch: activate the CAMPAIGN "<campaign name>" (id <campaign_id>)?
> The moment you say yes, Meta begins spending <X.XX> <CUR> per day. Pausing later is instant
> and safe, but money spent is spent. Reply yes to go live, or not yet to leave it paused.

A skip or not-yet at any level stops cleanly with everything above it still PAUSED. Partial
activation is a valid end state, recorded in the manifest, and the wrap-up says what is live
and what is not. One yes equals one level: never activate an entity without an explicit
confirmation naming that exact entity, with level, name, and id echoed in the question. A yes
for the ad is not a yes for the ad set. "Activate everything" still runs level by level with
each result shown.

## Step 10, Done

- Write or refresh both manifests per `references/build-chain-spec.md` section 4: `build-manifest.json` (machine state) and `manifest.md` (member record), in the run folder next to `plan.md`.
- Print the click-through list of every `ads_manager_url`.
- Confirm `ads_get_errors` is clean on the created ids.
- Learning-phase note: fetch it live via `ads_get_help_article` ("ad set learning phase") and quote the specifics with the article's canonical URL. If the fetch fails, the hedged framing stands alone: "expect about a week of unstable results while Meta's learning phase settles; do not edit budget, audience, or creative during it."
- Activated ending: "It is live. Meta usually reviews new ads within a few hours, you do not need to do anything. Your manifest with every link is saved at <path>. See you in about 7 days for the first quick check with /pm-meta-analyze."
- Not-yet ending: "Good, leaving it paused. The manifest at <path> has the checklist. When you are ready, come back and say activate my campaign and we finish in under a minute."

## Changing existing campaigns (the update flows)

Build performs surgical updates on entities it did not create: pause, budget change, targeting
update, activation of existing entities, audience create, update, and delete, customer list
upload, and pixel event and parameter work. The per-action ceremony table is in
`references/build-chain-spec.md` section 5. Binding conditions:

- Identical ceremonies: every budget change gets the full budget echo (stated amount, computed cents, currency, account minimum); the over-500 typed confirm computes against the NEW total daily spend of the affected structure, not the delta.
- The bulk guard: changing more than 3 entities in one request requires listing them all and one explicit confirmation of the list.
- Unpausing an existing campaign IS an activation and gets the full ceremony.
- DSA is re-asked when an edit adds any EU-27 country to geo.
- Audience deletion is the strictest ceremony: list dependent ad sets first via `ads_get_custom_audience_adsets`, state that deletion is permanent and auto-pauses those ad sets, and require the member to type the audience name exactly. A yes is not enough for a permanent delete. Child lookalikes block deletion; route to Ads Manager.
- Pixel writes carry the data-source-category gate wording and the reminder that deleting an event rule does not auto-delete its linked parameters.
- Customer lists: PII passes straight through to Meta (it normalizes and hashes server side); store only the row counts and the audience id. Never copy the list, or any single row of it, into the manifest, the chat, or any file.
- DELETED coercion guard: if `ads_update_entity` returns `status_forced_to_paused: true`, say exactly what happened, Meta paused it instead of deleting, and never report a coerced pause as a deletion.
- Archive convention: pause plus rename with the `zz_archived_<date>_<original name>` prefix, recorded in the manifest, never described as deletion.

## Failure and recovery

The manifest is the recovery state. Rules:

1. Write the manifest before and after every write call. Before: record what is about to be attempted (level and exact name). After success: record the returned id, status, and ads_manager_url. The manifest on disk must never lag behind reality by more than one call.
2. Never re-create what the manifest already has. If the campaign id is set, the campaign create is never called again in this run. Resume always continues at `next_step`.
3. After an ambiguous failure (timeout or transient 500 on a create), do not retry blind. Adopt-by-name first: list recent entities at that level with attributes only, look for the exact name from the intent record, and adopt the found id into the manifest. The failure may have succeeded on Meta's side, and a blind retry mints a duplicate that can never be deleted.
4. Transient 500 or INTERNAL: retry the same call up to 3 times with waits of about 2, 5, and 15 seconds. After the third failure, stop, save the manifest with the error, and tell the member it is safe to come back later, nothing needs to be redone.
5. Everything in the manifest was created PAUSED, so an interrupted run cannot spend. Say that out loud whenever a run stops early.

Specific recoveries (full catalog in build-chain-spec.md section 3): the payment block
(1359188) parks the chain and retries only the failed call on "done"; the audience terms block
(1870090) offers the website-audience fast unblock; an FBIDTypeError means a placeholder id
leaked, re-resolve from the manifest and never ask the member for raw IDs. Cleanup guidance is
honest: nothing campaign-shaped hard-deletes, leftovers stay PAUSED and harmless, true removal
happens in Ads Manager.

Mid-build failure message:

> Something failed at the <level> step, so I stopped. Here is the state: <mini table of what
> exists, all paused>. Nothing is spending and nothing here can break anything. Your manifest
> at <path> is the recovery map. Say **resume** to retry from where it stopped, or **leave
> it** to keep what exists paused for later.

## Output validation

Before declaring this skill complete, verify:

1. The manifest exists at `$BASE/<run-folder>/build-manifest.json`, parses as JSON, and lists every entity created this run with id, status at create, and ads_manager_url.
2. Every entity in the manifest was created PAUSED (`status_at_create: "PAUSED"` on each).
3. Every `ads_activate_entity` call this session has a matching entry in `activations` recording the member's explicit yes for that exact entity, with level, name, and id having been echoed in the question.
4. Every budget that was sent has a `budget_confirmations` entry where the stated amount and the sent cents are mutually consistent (stated times 100 equals cents) and `confirmed: true`.
5. If the total planned daily spend exceeded 500 account currency units and anything was activated, `over_500_confirmation` records the typed daily total matching the plan.
6. The special ad categories question was asked and the answer is recorded in the manifest, including the explicit none case as the empty list.
7. If geo includes any EU country, the DSA beneficiary and payor are non-empty and were sent on the ad set.
8. The irreversibility fine print was shown inside the Gate 1 plan message, before the first create call.
9. The creative carries exactly one source (`creative_id`, or `object_story_id`, or `object_story_spec`), and any image creative used `image_hash`, never `image_url`.
10. `promoted_object` is present whenever the optimization goal required it, and the ad set's optimization goal is one of the campaign's returned `valid_optimization_goals`.
11. `validator_pass` is recorded in the manifest (PASS, or the numbered issues and their resolutions).
12. `manifest.md` exists next to build-manifest.json and its status line matches reality.
13. No customer PII appears in the manifest or any output file, only counts and ids.
14. No token-like strings, OAuth codes, or callback URLs anywhere in any output file.
15. The wrap-up message states the final status of all three levels (active or paused), the daily budget in the stated amount and cents, the ads_manager_url links, the learning-phase note, and points at /pm-meta-analyze in about 7 days.
16. No placeholder strings remain.

If validation fails:

1. Documentation items (1, 6, 7 recording, 11, 12, 15, 16): fix the manifest or the message from session memory. Never re-run a write call to repair a document.
2. Item 2 or 3 failed because something was activated without its recorded yes: pause that entity immediately via `ads_update_entity`, then tell the member exactly what was active, for how long, and that it is now paused. Do not soften it.
3. Item 9 or 10 failed on an already created entity: the entity is paused (everything is), explain the spec problem, offer to fix via `ads_update_entity` or archive via the zz_archived_ convention and rebuild that level correctly.
4. Item 13 or 14: redact the file immediately and tell the member what was written and that it was removed.

## Hard rules

1. Everything is created PAUSED, always. There is no flag, request, or shortcut that changes this.
2. One yes equals one level. Never call `ads_activate_entity` without an explicit member confirmation naming that exact entity, level, name, and id. Activation order is ad, then ad set, then campaign, so the last yes is the spend switch. Activating a parent never activates children; never claim a campaign is live unless all three levels were individually activated.
3. Budgets: the amount stated in account currency, the cents computed, both echoed with the currency and the account minimum, before any create that carries a budget. Above 500 account currency units per day total, the member must type the daily total to proceed, with the multiplication and the 7 day and 30 day projections spelled out.
4. The special ad categories question is mandatory on every run. The DSA beneficiary and payor questions are mandatory whenever geo includes the EU.
5. The irreversibility fine print comes before the first create call, inside the plan message. Never describe pause plus rename as deletion. If Meta coerces DELETED to PAUSED, say exactly that.
6. Permanent deletes (custom audiences only, the one true permanent delete this skill names to members) require listing dependent ad sets first and a typed name confirmation. Pixel event and parameter deletes require an explicit yes and the reminder that linked parameters are not auto deleted; rules created through this connection are archived by Meta, rules created in Events Manager delete for good.
7. The manifest is written before and after every write call. Never re-create an entity whose id is already in the manifest. After an ambiguous failure, adopt-by-name before any retry. Transient errors get 3 retries with 2, 5, and 15 second waits, then a clean stop with resume instructions.
8. Creatives: `image_hash` or `video_id` or `object_story_id` only, exactly one source, never `image_url` for an image creative, never an invented interest id, never an optimization goal outside the campaign's `valid_optimization_goals`.
9. Bulk guard: changing more than 3 existing entities in one request requires listing them all and a single explicit confirmation of the list.
10. Stop means pause. Any doubt after activation: pause the campaign first, discuss second.
11. Never echo or store tokens, OAuth codes, any part of a pasted callback URL, or any row of a customer list. Counts and ids only.
12. Tiered loading: never load `ads_activate_entity` before the activation ceremony, and never load the create tools before the member approves the plan.
13. Apply the entity naming convention (`<Brand> | <Product> | <Objective word> | <YYYY-MM-DD>`) unless the member overrides it; adopt-by-name recovery depends on it.
14. Never call `ads_catalog_get_products`. It is deprecated; use `ads_catalog_search_product`.
15. No em dashes, and no hyphens as sentence pauses, anywhere in skill output. Use commas, "and", or split sentences.
16. **(Project)** Output sotto `output/{brand}_{campaign}_{date}/13_Meta_Campaigns/` (campaign dir) o `output/reports/{date}_meta_campaigns/` (standalone) — mai fuori da `output/`. Copy nel creative VERBATIM dai deck SA7; copy member-facing italiana passa per `49_anti_ai_slop`.
