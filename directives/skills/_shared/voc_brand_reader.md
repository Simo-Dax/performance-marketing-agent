# VOC + Brand DNA reader, the canonical doc-intake contract

This shared module defines how any skill discovers and extracts data from the brand's existing research documents, so every consumer parses the SAME fields the SAME way and the user is never re-asked for something the docs already contain. Load it whenever a skill needs brand or customer intelligence from disk.

The rule this module enforces: **documents first, questions last.** A skill may only ask the user for what genuinely cannot be derived from the docs below.

---

## R.1 Discovery, newest file per source

All paths are relative to `$AILAB` (the resolved `the agent/` project folder). Run these and keep the newest hit per source:

```
ls -t "$AILAB/01_VOC_Research/voc-"*.html "$AILAB/01_VOC_Research/"*.md 2>/dev/null | head -n 1
ls -t "$AILAB/01_VOC_Research/foundation-"*.html 2>/dev/null | head -n 1
ls -t "$AILAB/02_Brand_DNA/"*.html "$AILAB/02_Brand_DNA/"*.md 2>/dev/null | head -n 1
ls -t "$AILAB/03_Ad_Spy/"*.html 2>/dev/null | head -n 1
ls -t "$AILAB/16_Creative_Briefs/"brief-*.json 2>/dev/null | head -n 1
cat "$AILAB/_meta/learnings.json" 2>/dev/null
cat "$AILAB/03_Ad_Spy/competitors.json" 2>/dev/null
```

The `voc-` prefix on the first glob matters: the Foundation Pack (`foundation-*.html`, see R.9) lives in the same folder and is usually newer, so a bare `*.html` glob would grab the wrong document as "the VOC doc".

Also read the brand's `$AILAB/CLAUDE.md` if present (brand rules, forbidden words, offers). It is normally auto-loaded by Claude Code, but confirm its rules are in context before writing anything.

Announce what was found in ONE line, for example: "Using voc-glowserum.html, foundation-glowserum.html, brand-dna-glowserum.html, and your latest ad spy swipe from this project folder." Never dump file contents at the user.

## R.1b The source ladder (first-party outranks public)

Not all customer language is equally true. When the VOC document (or the user directly) carries material from more than one source tier, the tiers rank:

1. **The user's own first-party material**: sales or support call transcripts, support tickets and chat logs, the brand's own store or product reviews, survey answers. This is the customer talking TO this brand about THIS product.
2. **Public third-party reviews of the product itself** (marketplace listings, app stores).
3. **Public forums and social** (Reddit, groups, comments): the category talking, not necessarily this brand's buyer.

A tier 1 quote outranks a tier 3 quote saying something similar, so when the doc marks its sources, hooks and headlines prefer the highest tier available. Consumers never DEMAND tier 1: when only public research exists, work with it exactly as before, silently. The ladder decides preference when both exist, nothing else.

## R.2 Reading the docs

The VOC and Brand DNA deliverables are self-contained HTML. To extract text, strip tags (script and style blocks first, then all tags) and read the remaining text. Section headings survive stripping, so navigate by the section names below, not by visual position. Verbatim customer quotes inside the VOC doc carry their tags (emotional intensity, awareness level, JTBD force) as adjacent badge text; keep a quote and its tags together.

## R.3 The VOC extraction map

The VOC document has 16 sections. Pull each primitive from its home section:

| Primitive | VOC section | What to take |
|---|---|---|
| Offer, product, price | S3 Product and Brand Snapshot | product name, price point, offer mechanics if stated |
| Pains | S4 Pain Points | the 3 to 5 highest-intensity pain territories, each with 1 or 2 verbatim quotes |
| Desires | S5 Desires | the 3 to 5 strongest desire clusters, each with verbatim quotes |
| Objections | S6 Objections | every distinct objection, with its strongest verbatim quote |
| JTBD forces | S7 Jobs To Be Done | push, pull, habit, anxiety forces |
| Awareness distribution | S8 Awareness Deep Dive | the percentage split across the 5 stages and the dominant stage |
| Lead with pain or desire | S9 Emotional Territory Map | whether pain or desire language dominates, and the top emotional territories |
| Visual and sensory bank | S10 Visual and Sensory Language | concrete imagery words for render prompts |
| Competitive context | S11 Competitive Landscape | the sea-of-sameness notes and competitor-tagged quotes |
| Feature to benefit | S12 Feature-to-Benefit table | each feature with its customer-language benefit |
| Language goldmine | S13 Language and Messaging Goldmine | the customer's exact recurring words and phrases |
| Real proof | S14 Social Proof Arsenal | every REAL number, count, rating, or quotable testimonial. This is the ONLY sanctioned source of proof numbers besides Brand DNA and scraped ads |
| Value equation | S15 Value Equation | dream outcome, likelihood, time delay, effort |

When citing a quote downstream, record a source ref alongside it in the form `voc:S4` (section) or `voc:S4 "first six words..."` so a reviewer can verify the quote is real. Quotes are used VERBATIM, never paraphrased.

## R.4 The Brand DNA extraction map

From the newest Brand DNA doc pull:

- Brand voice: the tone adjectives and voice description
- Visual identity: brand colors (hex values from the live sampling), typography notes, image style modifiers
- Positioning: the one-line positioning and the named differentiators
- Banned list: any forbidden words, claims, or styles (merge with the brand CLAUDE.md banlist; CLAUDE.md wins on conflict)
- Offer facts: guarantees, shipping claims, founding story facts usable as proof

## R.5 Ad spy and winning-ads context (optional layer)

If `03_Ad_Spy/` has a swipe file or teardown, extract: the angles and hooks competitors lean on (the bar to differentiate FROM), any reach or longevity signals, and the visual formats saturating the category. If `04_Static_Ads/_scratch/brand-ads-*.json` exists (written by the static skill), the newest file holds the brand's own normalized live ads with scoring tiers (PROVEN, HOT, ACTIVE) and a `visual_dna` key. Treat PROVEN and HOT ads as the brand's current winners.

## R.6 Learnings file (the feedback loop)

If `$AILAB/_meta/learnings.json` exists, read it. Shape:

```
{ "updated_at": "...", "winners": [ { "concept_id": "C03", "angle": "...", "framework": "...", "awareness_stage": "...", "evidence": "..." } ], "losers": [ ... ], "notes": "..." }
```

Winners bias generation TOWARD their angle territory and framework family. Losers are territory to avoid or consciously reframe. Say so in one line when applied: "Your last cycle's winner was the ingredient-mechanism angle, weighting toward that territory."

## R.7 What can NEVER be derived (the only allowed questions)

The docs do not contain the user's intent for THIS run. These are the only intake questions a doc-driven skill should ask, and they should be asked in ONE message:

1. The specific offer or promo to push right now (only if VOC S3 has no current offer)
2. Funnel stage or awareness override (always PROPOSE a default derived from the S8 distribution, ask for confirmation, never ask open-ended)
3. The desired action (CTA)
4. Target medium or format, when the skill supports more than one

## R.8 Missing-doc fallback

- VOC missing: tell the user the output will be much stronger with `/pm-dati-qualitativi`, offer to continue in a reduced mode that asks 3 short questions (top customer pain in their words, main desired outcome, biggest objection), and label the output "provisional, run /pm-dati-qualitativi for the evidence-backed version".
- Brand DNA missing: same pattern with `/brand-dna`; ask brand voice in 3 adjectives plus any banned words.
- Both missing: recommend running them first (they can run in parallel), but honor an explicit "just do it" with the reduced intake and the provisional label.

## R.9 The Foundation Pack strategy layer

`foundation-*.html` (built by /pm-dati-qualitativi Phase 3) is one document with three parts: the Customer Avatar Sheet, the Offer Brief, and the Necessary Purchase Beliefs. When it exists it OUTRANKS improvisation on strategy: **the Foundation Pack decides WHAT to say, the VOC document decides HOW to say it.** Verbatim customer language always comes from the VOC doc, never rewritten from the foundation doc.

Pull and apply:

- **Avatar (Part 1):** who this piece talks to. Identity, top pain clusters, fears, emotional drivers. Target this person, not a generic buyer.
- **Offer Brief (Part 2):** the recommended category position, big idea, named problem mechanism (UMP) and solution mechanism (UMS), claims-that-land vs claims-that-get-mocked, the objection bank with strategic responses, and the headline bank as a style reference (generate against the same strategy, never copy its headlines blindly).
- **Purchase Beliefs (Part 3):** the ladder of at most 6 "I believe that..." statements. Every ad, script, or page targets ONE primary belief; record which one in the deliverable's notes or sidecar (for example `"belief": 2`).
- Any **[ASSUMPTION - VALIDATE]** badge marks an unverified input: never turn an assumption into a public claim.

Foundation Pack missing: work exactly as before from VOC + Brand DNA alone, and at most once mention that /pm-dati-qualitativi can build it from the existing research.
