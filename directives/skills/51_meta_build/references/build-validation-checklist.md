# Build validation checklist, ai-ad-lab-meta-build

This checklist is the entire rubric for the pre-create plan validation (SKILL Step 6). It is
walked once per build, after the member approves the plan and before the first create call.
Preferred mechanism: one validator subagent with the brief in section 2. Fallback: the main
session walks the same list inline, line by line. Either way, the result is recorded in
build-manifest.json as `validator_pass` (true, or the numbered issues and their resolutions).
The checklist is the rubric; improvised judgment beyond it is out of scope.

## 1. The checklist

Each line is checkable with a PASS criterion. Guide references are to
`references/meta-ads-mcp-operator-guide.md`.

1. Objective is ODAX: one of the six OUTCOME_* values (guide section 9). PASS when the plan's objective is in that list and no legacy name appears anywhere.
2. CBO xor ABO: a campaign budget OR ad set budgets, never both (guide section 1). PASS when exactly one budget mode carries values.
3. Budget is integer cents and at or above `min_daily_budget_cents` from the account record (guide section 1). PASS when sent cents is an integer and meets the minimum.
4. Lifetime budgets carry an end date and a computed effective daily spend (lifetime divided by scheduled days). PASS when daily math exists or the budget is daily.
5. `promoted_object` is present whenever the optimization goal requires it (guide section 9 lists the goals), shaped with `pixel_id` and `custom_event_type`. PASS when present and shaped, or the goal does not require it.
6. Targeting carries `geo_locations` with the member's countries (guide section 9 floor shape). PASS when present.
7. No invented interest IDs: every interest ID in the plan was pasted by the member or absent. PASS when none exist or provenance is the member.
8. DSA beneficiary and payor are present when geo includes any EU-27 country (list in build-chain-spec.md section 6; guide section 9). PASS when both are set or no EU country is targeted.
9. Special ad categories were answered: an explicit none maps to the empty list, declared categories map only to the guide's enum values, and `special_ad_category_country` is set when declared (guide section 9). PASS when the manifest records the answer.
10. Exactly one creative source: `creative_id`, or `object_story_id`, or `object_story_spec` with `page_id` (guide section 9). Image creatives use `image_hash`, never `image_url` (guide section 7). PASS when one source exists and no image creative uses a URL.
11. `page_id` is confirmed from discovery, not assumed (guide section 3). PASS when the plan's page came from a discovery call this run.
12. Copy fits Meta's lengths and is verbatim from the deck or the member's own typed words. PASS when no silent rewriting happened.
13. Money math is consistent: the stated amount times 100 equals the sent cents, and the currency is the account currency. PASS when the multiplication checks out.
14. The naming convention is applied or the member overrode it knowingly (build-chain-spec.md section 7). PASS either way, FAIL only when names are missing or duplicated within the plan.
15. No placeholder values remain in the plan (empty ids, sample names, unfilled brackets). PASS when every value is real.

NOTE line, printed at the end of every validation: the ad set's `optimization_goal` versus the
campaign's `valid_optimization_goals` is enforced by the main session AFTER the campaign
create, not here, because that list only exists in the create response (guide section 9).

## 2. The validator subagent brief (template)

```
You are a fresh-context plan reviewer for a Meta ads campaign build. You did not write this
plan, and that is the point: review it with no attachment to it. You have no MCP access and
need none. You are advisory; the member's approval already happened and the main session
decides what to do with your findings.

THE APPROVED PLAN
<the full plan message verbatim, plus the structured plan record>

YOUR RUBRIC
<the checklist from section 1, verbatim>

REFERENCE EXCERPTS
<the relevant operator guide passages for sections 1, 7, 8, 9, 12C, and 13>

RULES
1. The checklist is your entire rubric. Do not invent additional requirements and do not
   waive listed ones.
2. Check every line. Cite the checklist line number and the guide section for every issue.
3. Numbers are checked by recomputing them, not by trusting the plan's arithmetic.

RETURN FORMAT
Return as your final message either the single word PASS, or a numbered issue list where each
issue carries: the checklist line number, what is wrong, the guide section that says so, and
the smallest fix.
```

## 3. The inline fallback

When the Agent tool is unavailable in the session, the main session walks the section 1 list
inline, line by line, recording the same PASS or numbered-issues result in the manifest the
same way. The narration line and the member experience do not change.
