---
name: 50_meta_analyze
description: Opera il Meta Ads MCP ufficiale direttamente dentro Claude Code per analizzare la performance live dell'account, STRETTAMENTE read-only — non crea, aggiorna, attiva o cancella mai nulla nell'ad account. Due modalità. Quick check = audit account single-pass veloce. Deep diagnosis = fan-out di investigator agent paralleli su slice di dati fisicamente isolate, un referee avversariale che prova a uccidere ogni teoria, e una diagnosi unica ranked con evidence-for, evidence-against, confidence e la singola azione più importante della settimana. SA8 (analytics/reporting), indipendente dalla pipeline creativa. Sostituisce la modalità "analisi" del vecchio 30_meta_handoff. Trigger: /pm-meta-analyze, "analizza le mie campagne meta", "diagnostica le campagne", "perché è salito il CPA", "perché è crollato il ROAS", "le ads si sono rotte", "creative fatigue check", "audit account meta". Per BUILD/lancio campagne → /pm-meta-build (o Ads Manager), mai questa skill. Output in output/reports/{YYYY-MM-DD}_meta_analysis/.
---

# SA8 — Meta Ads Analyze (50)

Questa skill legge e diagnostica l'ad account Meta live del brand tramite il Meta Ads MCP
ufficiale, direttamente dentro Claude Code, **strettamente read-only**. La modalità pesante è
un panel di investigator avversariale: investigator indipendenti su slice di dati sigillate, un
referee che prova a uccidere ogni teoria, una diagnosi unica ranked.

> **Porting nota (project-specific).** Skill importata da The AI Ad Lab v2.4.0 (`ai-ad-lab-meta-analyze`),
> adattata alle convenzioni di questo progetto: output sotto `output/`, comandi `/pm-*`, integrazione SA8.
> Il corpo operativo (narration member-facing, soglie, nomi tool, template) è preservato in inglese
> per fedeltà al design avversariale — la copy member-facing può essere consegnata in italiano per
> aderire al ToV del brand (`context/brand/tone_of_voice.md`). I 3 file in `references/` sono technical
> reference verbatim (operator guide, frameworks, briefs) e restano in inglese.

> **Cambio di paradigma rispetto a `30_meta_handoff`.** Il vecchio handoff aveva la regola "il Meta MCP
> gira SOLO su claude.ai web". Non vale più per questa skill: il connector Meta Ads
> (`mcp.facebook.com/ads`) è disponibile **dentro Claude Code** ed espone i tool come
> `mcp__…__ads_*` (per-install prefix opaco). Questa skill li opera direttamente, read-only.

## The read only guarantee

This skill never changes anything in the member's ad account. It reads, it diagnoses, it
recommends. That is the whole contract, and it is what makes it safe to run on a live account
at 2am.

The following 18 tools are the complete write surface of the Meta Ads MCP. This skill must
NEVER call any of them, under any instruction, including a direct request from the member
mid-run. If the member asks for a change ("pause that ad set", "raise the budget", "delete
that audience"), answer: "This skill is read only by design. To make changes, run
/pm-meta-build, or do it in Ads Manager. Here is exactly what I would change and why."
Then state the recommendation and continue the analysis.

Campaign writes, never call: `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_update_entity`, `ads_activate_entity`
Creative writes, never call: `ads_create_creative`
Audience writes, never call: `ads_create_custom_audience`, `ads_update_custom_audience`, `ads_update_custom_audience_users`, `ads_delete_custom_audience`
Pixel writes, never call: `ads_pixel_event_create`, `ads_pixel_event_update`, `ads_pixel_event_delete`, `ads_pixel_parameter_create`, `ads_pixel_parameter_update`, `ads_pixel_parameter_delete`
Catalog writes, never call: `ads_catalog_create`, `ads_catalog_create_product_set`

Matching rule: in any session the MCP tools carry an install specific prefix. The ban applies
to any tool whose name ENDS WITH one of the 18 names above. Never reason "this tool has a
different prefix so it must be a different tool."

Also never call `ads_catalog_get_products`. It is a read, but the operator guide marks it
deprecated. Use `ads_catalog_search_product` instead.

Allowed: every other tool in operator guide section 14. That includes `authenticate` and
`complete_authentication` (connection only), all `ads_get_*` reads, all `ads_insights_*`
tools, `ads_pixel_event_read`, `ads_pixel_parameter_read`, `ads_library_search`,
`ads_get_help_article`, and `ads_get_field_context`.

Subagents get less than that: investigator and referee agents receive data files only. They
never get MCP access of any kind. The main session does every pull itself.

## Reading the bundled references

Read `references/meta-ads-mcp-operator-guide.md` before your first MCP call. It is the single
source of truth for every tool name, parameter, convention, and limitation in this skill. For
deep diagnosis, also read `references/diagnostic-frameworks.md` before staging data and
`references/investigator-briefs.md` before fanning out investigators. All three files are
bundled inside this skill folder (`directives/skills/50_meta_analyze/references/`), so those
relative paths resolve from the skill folder.

## Step 0a, Resolve the project output folder

Outputs land under this project's `output/` tree, per the project output convention. The
canonical base is `output/reports/<YYYY-MM-DD>_meta_analysis/`. Run this Bash block first to
locate the project root (the folder containing `claude.md`) and seed the run folder:

```
# Walk up from pwd to find the project root (dir holding claude.md)
DIR="$(pwd)"; ROOT=""
while [ "$DIR" != "/" ]; do
  if [ -f "$DIR/claude.md" ] || [ -f "$DIR/CLAUDE.md" ]; then ROOT="$DIR"; break; fi
  DIR="$(dirname "$DIR")"
done
if [ -z "$ROOT" ]; then
  echo "NOROOT:$(pwd)"   # not inside the project; ask the member to open CC in the project (or campaign) folder
else
  TODAY="$(date +%Y-%m-%d)"
  BASE="$ROOT/output/reports/${TODAY}_meta_analysis"
  mkdir -p "$BASE"
  echo "READY:$BASE"
fi
```

- `NOROOT:<path>`, tell the member to reopen Claude Code in the project folder (or a campaign folder under it). Stop.
- `READY:<path>`, capture the path as `$BASE`. Continue silently. Run timestamps come from the system clock (`date +%Y-%m-%d-%H%M%S`).

Throughout this skill, wherever the upstream design referenced `14_Meta_Analysis/`, write to
`$BASE/` instead. Quick check artifact: `$BASE/quick-check-<stamp>.md`. Deep run folder:
`$BASE/deep-diagnosis-<stamp>/`.

## Step 0b, Auto-discover prior project context

Scan with ls, find, and Read (never Meta tools). Capture whatever exists, skip missing context
silently. Paths are relative to the project root `$ROOT` (and to the most recent campaign
folder `output/{brand}_{campaign}_{date}/` when one exists):

- `context/brand/business_profile.md` and `context/brand/tone_of_voice.md`: brand name, offer, ToV.
- Campaign folder `02_Brand_DNA/` and `01_VOC_Research/`, plus `intermediate/sa2_market_insights.md`: brand and offer context.
- `intermediate/sa7_copy_deck.md` and campaign `06_Ad_Copy/`: newest copy deck, context only in this skill.
- `09_Meta_Handoff/`: READ-ONLY legacy. Old intake answers occasionally carry account context. Nothing is ever written there.
- `15_Meta_Campaigns/`: build manifests from `/pm-meta-build` (when ported). The newest manifest auto-fills the case statement (optimized event, created entity ids, launch date) and lets the quick check call out the launched campaign by name. Skip silently if absent.

## Step 0c, Find the Meta Ads tools (never hardcode a server prefix)

Never hardcode or assume an MCP server prefix. Meta's connector installs under an opaque,
per-install ID, so the same tool can be named `mcp__<anything>__ads_get_ad_accounts` on
different machines (in this project it currently surfaces as `mcp__claude_ai_Meta_Ads_MCP__ads_*`,
but you MUST still resolve by suffix, never hardcode it). When this skill names a tool, the name
means "the tool whose name ends with this suffix". Never write a prefix into a file, a message,
or a tool call you compose from memory.

Resolve the connection state, in order:

1. **State A, tools already callable.** Scan the session's available tools for any name ending in `ads_get_ad_accounts`. Found: go to the smoke test.
2. **State B, tools deferred.** If a ToolSearch tool exists, load the Meta tools in bulk by suffix keywords, read-scoped: `+ads_get` (max_results 30), then `+ads_insights` (max_results 8), then `ads_pixel_event_read ads_pixel_parameter_read ads_library_search` (max_results 6). Loading a write tool schema in this skill is itself a Hard rules violation. Then go to the smoke test.
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
- `is_queryable: false`: exclude the account and send:

> Meta is not letting me read performance data from this account right now. Meta's stated reason: <not_queryable_reason>. This is an account state on Meta's side, not something broken on your machine.
> What I can still do here: check account structure, pages, pixels and their event volume, and run public Ad Library research. For performance analysis, resolve the reason above in Ads Manager first, then run me again.

- Exactly one usable account: do not ask, state it: "I will work in **<Account Name>** (ID <id>, currency <CUR>). It is the only ad account connected here." Several: numbered picker with name, ID, currency, and a recent-spend marker.
- Capture for the whole run: `ad_account_id` (bare digits, never `act_`), `currency`, `min_daily_budget_cents`, `has_payment_method`, `business_id`, `account_status`. Every money sentence uses `currency`; never print a dollar sign unless the currency is USD.

## Step 1, Route the request

If what the member actually wants is to build, launch, edit, pause, or activate a campaign,
stop here and run /pm-meta-build (when ported) or point them to Ads Manager; that route owns
every write to the ad account.

Break-language detection: if the triggering message contains break language ("CPA doubled",
"ROAS fell", "ads died", "stopped converting", "performance tanked" and similar), skip the
mode menu, send this, and fold their words into deep intake question 2:

> It sounds like something actually broke, not just a routine check. That is exactly what my
> deep diagnosis is for. Before I start it I will show you what it involves and what it costs,
> and you can still pick the lighter quick check instead.

Otherwise send the mode menu exactly:

> I can look at your Meta account two ways. Pick one.
>
> 1. **Quick check.** One pass over your live numbers. Top campaigns, what is up, what is down,
>    anything unusual, and the clearest next move. Takes a few minutes, runs right here, and
>    never changes anything in your account.
> 2. **Deep diagnosis.** For when something broke and you want the real reason before you touch
>    anything. I pull your data, seal it into separate evidence files, and send several
>    independent investigators at competing theories. Then a referee tries to kill every theory.
>    You get a ranked diagnosis with the evidence for and against each cause. Takes roughly 10
>    to 20 minutes and uses a lot more Claude usage than a normal chat.
>
> Reply 1 or 2. If nothing is on fire and you just want to know how things are going, 1 is the
> right call. If your cost per purchase jumped or ROAS fell off a cliff, pick 2.

## Step 2, Quick check (mode 1, the default)

Intake, one message:

> Two quick things, or just say go and I will use the defaults.
>
> 1. Time window. Default is the last 14 days compared with the 14 days before that. You can
>    also say last 7 days, last 30 days, last 90 days, this month, last month, or give exact
>    dates like 2026-05-01 to 2026-05-28.
> 2. Anything specific bothering you, or a full check? Default is a full check.

Author note, binding: member window words map only to `date_preset` values that exist in
operator guide section 1 (`last_7d`, `last_14d`, `last_30d`, `last_90d`, `this_month`,
`last_month`, `maximum`) or to a `time_range`. There is no `last_28d` preset. The comparison
window is always a second call with an explicit `time_range`. Never expose the words
date_preset or time_range to the member.

Pull list (about 10 to 12 calls, in order):
1. Field verification, once, per the rule in Step 5 below.
2. `ads_get_ad_entities` account level, totals for the chosen window, and again for the prior window (two explicit `time_range` calls).
3. Campaign level for the window, sort `amount_spent_descending`, limit 100.
4. Ad level for the window, twice: sort `cost_per_result_ascending` then `cost_per_result_descending`, limit 25 each (winners and losers, after confirming sortability in field context).
5. `ads_get_opportunity_score`, then `ads_insights_anomaly_signal`.
6. `ads_get_errors` with the child entity ids just pulled, never the bare account id.
7. `ads_get_datasets`, plus one `ads_get_dataset_stats` (`aggregation: "event"`, last 7 days) when the account optimizes to conversions.

Artifact: ONE file, `$BASE/quick-check-<YYYY-MM-DD-HHMMSS>.md`, using the
quick template in `references/diagnostic-frameworks.md` section 4.1. Print its summary in
chat. Every bullet cites metric, value, and window.

Endings. Healthy account: "Nothing here needs surgery. Sensible next move: keep feeding the
machine, /pm-statiche for fresh concepts or /pm-multiplier on your best ad." Suspected break:
"This looks like more than a wobble. Run me again and pick deep diagnosis, that is what it is
for."

## Step 3, Deep diagnosis intake and pre-pass

Intake, one message:

> Four things before the investigators go in. Defaults are fine for any of them, just answer
> what you know and say go.
>
> 1. When did it break? A date is perfect, "about two weeks ago" works too. Default: I find the
>    break point myself from your daily numbers.
> 2. What did you see, in one or two sentences? For example "cost per purchase roughly doubled"
>    or "ROAS went under 1 and stayed there". Default: I diagnose whatever the data shows.
> 3. Should I look at the whole account or specific campaigns? Default: the whole account,
>    starting with your biggest spenders.
> 4. Did anything change on your side around then? Price, offer, landing page, a big promo,
>    competitors acting up. Default: nothing you know of.

Question 3 is a LENS, not a fence: the pre-pass and all slices stay account-wide; named
campaigns get guaranteed ad-level coverage in slices A and C plus a dedicated report callout;
the case statement records "Member attention: <campaigns>" as testimony. Question 4 feeds
Investigator E verbatim and the case statement.

Pre-pass: if a date was given, confirm it against the data. Else pull `ads_get_ad_entities`
account level, `date_preset: "last_30d"` (extend to `"last_90d"` if the member says it is
older), `time_increment: 1`, with the verified primary metric set, and find the largest
sustained shift: the biggest 3-day-mean versus prior 3-day-mean delta in the primary cost
metric that persists at least 3 days. Confirm: "Your cost per purchase moved from about <X> to
about <Y> around <date> and stayed there. Is that the break you mean? (yes / no, it was
<date>)". The objective-aware metric mapping in frameworks section 6.2 applies (sales accounts
use purchase metrics, lead accounts use lead metrics).

No sustained shift above 25 percent persisting 3 or more days: "Nothing in the last 30 days
looks broken. The investigator panel is for when something real snapped. I will run the quick
check instead and flag anything worth watching."

Spend exists but zero conversions have EVER tracked: skip the panel, run the tracking-first
check (slice D's pulls, executed by the main session, findings reported directly), and say the
likely story is that tracking was never wired.

Window math: `before = D-14 .. D-1`, `after = D .. min(today, D+14)`, the full window W drives
the daily series. After side under 5 days: warn that confidence is limited.

## Step 4, Sufficiency gate and consent gate

The panel requires ALL of: 30 or more primary conversions in W, 1,000 or more link clicks in
W, 7 or more delivery days on EACH side of the break, 3 or more ads delivered (run the ad
count as a cheap pre-check first). On failure, send the degrade message with the actual
failing numbers filled in, then run the quick check:

> Deep diagnosis needs about two weeks of solid spending on each side of the break so the
> investigators can compare a real before with a real after. This account has <plain statement
> of the failing numbers, for example "9 purchases in the window and 4 days of delivery on the
> thin side">. Running the full panel on this little data would produce confident sounding
> guesses, and a confident guess is exactly what this skill exists to prevent. I am running the
> quick check instead, it sees everything that is actually visible here. Say stop if you would
> rather not.

Break 7 to 13 days old: run, cap all confidences MEDIUM, tell the member upfront. Break older
than about 24 days: run, warn that the Tracking seat sees at most 28 days back.

Consent gate, the ONE analyze gate. No agents are spawned before a yes:

> Before I start the deep diagnosis, here is exactly what happens.
>
> **What happens:** I make about 25 to 30 read-only pulls from your Meta account covering
> <since> to <until>. Nothing in your account changes, this skill cannot write. I seal the
> data into separate evidence files, then run 5 independent investigators in parallel, one per
> theory: creative fatigue, delivery and budget changes, traffic quality, tracking, and the
> outside world. A referee then tries to kill every theory against the complete dataset, and
> it may call up to two investigators back for one short follow-up.
> **Time:** usually 10 to 20 minutes. You can leave this chat open and come back.
> **Cost:** zero Meta spend, this never touches your ads. It does use a lot more Claude usage
> than a normal chat, roughly like running several chats at once. Worth it when something is
> genuinely broken, overkill for a routine look.
>
> Say **go** to start, or **quick** to drop down to the fast check instead.

## Step 5, Stage the evidence

Field verification, mandatory before any metric pull in either mode: call
`ads_get_field_context` once with the full candidate list from frameworks section 6.1. Drop
anything echoed in `unknown_fields` from every subsequent pull, resolve aliases to canonical
names, record the verified set in provenance.json, and self-correct silently from any later
field-rejection error (the error echoes the valid-field list), logging the substitution in
provenance. Every metric field in every pull goes through this. No special cases.

Then read `references/diagnostic-frameworks.md` section 6 and execute the deep pull plan
exactly: P1 through P13 plus P11b, E1 through E3, B1, and the oracle pack R1 through R3.
Apply the insights routing rule (section 6.3): the narrative oracles go to the referee pack
only, the benchmark numbers go to slice E, advertiser context goes to the case statement.

Build the run folder:

```
$BASE/deep-diagnosis-<YYYY-MM-DD-HHMMSS>/
  report.md                  (canonical artifact, written at the end)
  report.html                (rendered last, render failure never blocks)
  case.md                    (the case statement, template in investigator-briefs.md)
  provenance.json            (call ledger plus run state, schema in frameworks 6.7)
  staging/
    full/full-dataset.json   (the referee's universe, raw plus num pairs)
    slices/                  (five slice files per the contracts in frameworks 6.5)
  findings/                  (written by the main session as agents return)
```

Write case.md, the five slice files (compact encoding with the `_manifest` blinding header,
parsed numbers only, contracts and caps per frameworks 6.4 and 6.5), full-dataset.json, and
provenance.json (one entry per MCP call, updated as you go, `stage_completed` advanced after
each phase so an interrupted run can resume without re-pulling).

Narration before the pulls: "Pulling the evidence. Daily numbers around the break, placement
mix, pixel event volume, auction signals, and Meta's own anomaly flags. Bigger accounts can
take a couple of minutes here." Before slicing: "Sealing the data into separate evidence
files, one per investigator, so no investigator can peek at another's numbers."

## Step 6, Fan out the investigators

Launch five subagents with the standard Agent tool, in parallel. Each prompt is its full brief
assembled from `references/investigator-briefs.md`: the case statement prepended, the
hypothesis block inserted, the absolute path of its one slice file named. Investigators RETURN
findings as their final message; the MAIN session writes `findings/finding-<slice-name>.md`.
Subagents never write files and never call MCP or network tools; file IO stays in one place.

Isolation is three-layer: the briefs name exactly one path and forbid everything else; the
slices are field-filtered at write time so withheld values are physically absent; the referee
audits every finding's citations against that slice's `_manifest` and discards any claim that
relies on data the investigator could not have seen, naming the discard in the report.

Fan-out narration, exactly:

> Sending in the investigators.
>
> 1. The Creative Fatigue investigator, checking if your ads wore out.
> 2. The Delivery and Budget investigator, checking if a settings or spend change broke it.
> 3. The Traffic Quality investigator, checking if the clicks got worse.
> 4. The Tracking investigator, checking if your pixel stopped telling the truth.
> 5. The Outside World investigator, checking seasonality, your offer, and the auction.
>
> Each investigator works alone and only sees its own sealed slice. They know other
> specialists exist, but never who, and never what theory anyone else is chasing. This is the
> long part, usually 10 to 20 minutes. You can leave this chat open and come back.

Findings stay SEALED from the member until the referee finishes. As each agent returns, say
exactly: "The <name> investigator is back. I am holding every verdict until the referee has
attacked all of them, so no single story gets a head start."

## Step 7, The referee

Launch one referee subagent with the refuter brief from `references/investigator-briefs.md`
section 4. Inputs: case.md, the five findings verbatim, full-dataset.json (which embeds every
slice `_manifest` and the three oracle outputs), and the kill-criteria table. The main session
writes its output to `findings/refuter-verdicts.md`. Verdicts are KILLED, WOUNDED, SURVIVED,
or UNTESTED.

Narration: "All investigators are back. Sending in the referee now. Its only job is to try to
kill every theory with the full dataset, including the theories that sound convincing."

## Step 8, The supplementary round (conditional)

Fires only when: the top two theories are inseparable, OR everything came back KILLED or
UNTESTED, OR a verdict hinges on a named objection. The referee's provisional output may carry
up to 2 RECALL REQUESTS and up to 3 DATA REQUESTS (each naming the tool suffix, the
parameters, and the question it answers). The main session executes all pulls, appends to
full-dataset.json, and builds delta slices. Each recalled investigator is re-invoked once with
the recall brief (its original finding, the specific objection, the optional delta slice) and
returns DEFEND, CONCEDE, or AMEND with evidence. Then exactly ONE referee finalization pass
issues final verdicts.

Hard caps, repeated in Hard rules: max 2 recalls, max 3 data requests, 1 finalization, never a
second supplementary round under any instruction. Worst case 9 agent invocations per run, all
covered by the single upfront consent. Under time pressure this round is the first thing
dropped; if dropped, the report states that verdicts are first-pass.

Narration when it fires: "The referee wants a second look at <one or two> theories. Calling
<name> back for one follow-up, this is the panel arguing, which is exactly what it is for."

## Step 9, Synthesize and write the report

Narration: "Referee done. Writing your ranked diagnosis."

The main session applies the synthesis rubric in frameworks section 3: verdict class ranks
first (SURVIVED above WOUNDED above UNTESTED; KILLED never ranks, killed theories go to Ruled
out with their killing evidence), then confidence, then the tie-breaks. Cause-symptom pairs
render as one chain at the cause's rank with the symptom indented and "fix the cause; the
symptom resolves with it". The confidence caps fire mechanically with their stamps shown.

Write `report.md` from the template in frameworks section 4.2, including the data provenance
appendix rendered from provenance.json and the footer data note:

> A note on your data: the files in this run folder contain your real account performance
> data (entity names, spend, results). They exist only on this computer, inside your project
> folder. Nothing was uploaded anywhere by this skill, the only network calls were reads from
> Meta's own API. Everything in the run folder was kept so you can revisit the evidence.
> Delete the run folder whenever you like, the report stands alone. Say clean up the staging
> data and I will delete the working files and keep the report.

Render `report.html` last (same content, SURVIVED and RULED OUT chips, confidence as words,
single self-contained file; a render failure never blocks, note it in chat and move on). Print
the chat summary: the Read this first paragraph, the ranked list in one line each, the single
most important action.

Ending: the single most important action, then: "If the action is a change in your account,
/pm-meta-build can make it with the same confirm gates (when ported), or use the Ads Manager
link above. If it is creative refresh, /pm-statiche and /pm-multiplier are the tools." The
build pointer appears only when a recommended action is a Meta write.

## Progress narration contract

One line before every multi-call phase, present tense, plain words. Never a tool name, hash,
cursor, parameter name, or raw JSON in chat. Exceptions: the member's own entity names and
IDs, and a Meta error code once in parentheses after the plain-words explanation. Say
"referee" in member copy; "refuter" appears only in briefs and file contents. The deep-mode
time promise is "usually 10 to 20 minutes", everywhere, with no other duration ever stated.
Quick-check narration sequence: "Connecting to your Meta Ads tools." then "Pulling your last
14 days at campaign level, plus the 14 days before for comparison." (adjust the numbers to the
chosen window) then "Checking delivery health, anything Meta itself is flagging, and how your
auction position looks." then "Done pulling. Writing up what I found."

Transient errors, exactly: "Meta hiccuped on that request. Retrying in a few seconds, this is
normal and nothing is wrong on your side."

## Failure and degradation paths

- Every MCP pull retries on transient 500 or INTERNAL errors: 3 attempts, waits of 2, 5, and 15 seconds.
- An investigator whose primary pull fails after retries is dropped only if at least 4 seats remain. The empty seat is named in the report header and its theory listed UNTESTED with the reason. A failed Tracking pull is flagged loudly, tracking is the upstream invalidator.
- Delivery-derived tools returning "no data" strings are staged as-is, they are evidence of account youth, not errors. The investigator verdicts INSUFFICIENT DATA; the referee maps it to UNTESTED.
- An investigator returning malformed output (missing required sections) is re-invoked once, then marked UNTESTED.
- Truncation flags from pagination or slice caps surface in the report's provenance appendix.
- A non-queryable account uses the is_queryable wording from Step 0c and degrades to what is honestly possible.

## Output validation

Before declaring this skill complete, verify:

1. No banned tool was called: none of the 18 write tool names from the Read only guarantee appear among this session's tool calls, under any prefix. In deep mode, verify against provenance.json.
2. The report exists at the expected path (quick: `$BASE/quick-check-<stamp>.md`; deep: the run folder's `report.md`) and is non-empty.
3. Deep mode only: the consent question was asked and answered go before the first agent was spawned.
4. Deep mode only: every ranked theory carries all four parts: evidence FOR, evidence AGAINST, a confidence level, and a survived-the-referee flag.
5. Deep mode only: when two or more theories survive, the report pairs cause and symptom explicitly.
6. The "what I could not check from here" list is present and contains only things the MCP genuinely cannot see.
7. The single most important action this week is present, labeled as a recommendation, with the sentence "this skill changed nothing in your account" nearby. Any in-account action points to /pm-meta-build or Ads Manager.
8. Every performance claim in the report cites a metric and a time window.
9. Every slice file respects its blinding list: fields named in `excluded_by_design` never appear in its columns or rows, and the slices folder was KEPT.
10. No investigator seat is silently absent: any empty seat is named in the report header with its theory UNTESTED.
11. The data provenance appendix is present and renders provenance.json (calls, pages, truncation, self-corrections).
12. Deep mode: report.html exists, or its absence is noted in chat without blocking.
13. No token-like strings, OAuth codes, or callback URLs anywhere in any output file.
14. The data note appears in the report footer.
15. No placeholder strings remain (no unfilled angle brackets outside template explanations, no TODO, no lorem ipsum).

If validation fails:

1. Items 2, 4, 5, 6, 7, 8, 11, 14, 15: rebuild the report from the findings and verdict files on disk. Do not re-pull data and do not re-run agents to fix formatting.
2. Item 9 (a slice broke its blinding list): state it plainly, treat the affected finding as discarded, and rebuild the report without it.
3. Item 13: redact the file immediately, then state plainly what was written and that it was removed.
4. Item 1 or 3 failed: stop and tell the member exactly what happened in plain words, including what was called or spawned and why that broke this skill's contract. Do not soften it. These are promise breaks, not formatting problems.

## Hard rules

1. Read only, forever. Never call any of the 18 write tools listed in the Read only guarantee, no matter who asks. Change requests get a recommendation plus a pointer to /pm-meta-build or Ads Manager.
2. Investigator and referee agents never get MCP access. The main session pulls all data itself and hands each investigator only its own slice file. The referee additionally gets full-dataset.json and the findings.
3. No agent fan-out without the consent go. The quick check never spawns agents at all.
4. Never echo or store tokens, OAuth codes, or callback URLs. The connection preflight uses them once, in the moment, and never again.
5. Math runs on parsed numbers, never on Meta's formatted currency strings. Cite a metric and a window for every claim.
6. Pagination cursors are used exactly as returned, never fabricated.
7. If the account is not queryable, not MCP enabled, or too young or low spend for the panel, say so kindly, degrade to what is honestly possible, and never manufacture confidence from noise.
8. Anomaly signals are observations to investigate, not confirmed causes. The opportunity score is account-level, never attribute it to one campaign.
9. Never call `ads_catalog_get_products`. It is deprecated; use `ads_catalog_search_product`.
10. Supplementary round caps: max 2 recalls, max 3 data requests, one referee finalization, never a second round under any instruction.
11. Findings stay sealed from the member until the referee finishes.
12. Never record or print an MCP server prefix anywhere, suffixes only, including inside provenance.json.
13. The narrative insight oracles (anomaly signal, opportunity score, performance trend) go to the referee only, never to an investigator.
14. No em dashes, and no hyphens as sentence pauses, anywhere in skill output. Use commas, "and", or split sentences.
15. **(Project)** Output sotto `output/reports/{YYYY-MM-DD}_meta_analysis/` — mai fuori da `output/`. Anti-AI slop sulla copy member-facing italiana via `49_anti_ai_slop` + `context/brand/anti_ai_writing_style.md`.
