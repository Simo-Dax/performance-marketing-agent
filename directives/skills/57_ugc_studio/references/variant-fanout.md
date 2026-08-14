# VARIANT FAN-OUT — one approved script, up to 4 distinct timelines (UGC Studio)

Batch feature for **Narrative and Testimonial** orders: fan one approved script
into up to 4 ads that Meta's creative retrieval treats as 4 DISTINCT entities.
Near-duplicate timelines get pooled as variations of one creative and throttled —
so distinctness is **three-axis**: a different VISUAL WORLD (what the opening
shows), a different MESSAGE (what the hook claims), and a different FORMAT feel
(how the timeline cuts). Swapping only the opening line fails all three.

## Lever 1 — four unique hooks (the evidence-weighted families)

One hook per variant, drawn from the render-laws §6 table:

- **At least 2** of the set from the strong families (offer/urgency-led 9.29%,
  confession 8.74%, demographic call-out).
- **At most 1** from the weak family (question / listicle / how-to, 5.2–5.5%).
- Vague lifestyle openers: banned, zero slots.
- Every hook performs a **different VISUAL action** (slam-down, armful-dump,
  product-to-lens, call-out to camera…) — a different action KIND, not four
  near-identical camera moves. The visual axis is what the retrieval model
  actually sees first.
- VOC verbatim anchors the hook line whenever research exists.

Each hook is its own `kind: "gen"` entry with `role: "hook"` (merged forward per
the sizing law), so the four variants open on four different generations.

## Lever 2 — the insert ladder over a SHARED BODY

All variants ride ONE shared body: the same spine + close gens, rendered once.
What differs per variant is the **insert suite density and placement** — how the
shared spine gets punched into:

| Rung | Overlay punch-ins | Overlay anchor positions | Base-rail insert beat |
|---|---|---|---|
| 1 | 1 | early (first spine clip) | none |
| 2 | 2 | early + mid | none |
| 3 | 3 | mid-weighted suite | one VO insert beat |
| 4 | 3 | late-weighted suite, different anchors than rung 3 | one VO insert beat, different slot |

- Overlays replace the base PICTURE while base audio runs (pipeline-contracts §3),
  so overlay count changes **cut density, not runtime** — the four timelines cut
  differently through their whole middle, not just open differently.
- Runtime spread comes from the base rail: hooks of different word counts, the
  higher rungs' base-rail insert beat, and per-variant interior `trim[]` choices.
  **Every variant lands on a different total length** (spread inside the format's
  band) — same-length twins read as one creative.
- Overlay positions differ per variant even at equal counts: different `anchor`
  words/times, different insert files or different `insert_in` offsets into the
  same insert. Rungs 3 and 4 share density but never placement.

## The close and the exit

Every variant ends on its format's **typed close** (`close_type`: testimonial →
`cta`, narrative → `button`): the final base clip traces to a `role: "close"` gen,
overlays never cover it, and build_manifest refuses anything else.

## The DISTINCTNESS FINGERPRINT

Each variant's fingerprint is the tuple **`hook_family/insert_count/length`**
(e.g. `confession/3/27.4`). The orchestrator asserts before dispatch:

1. All four fingerprints unique.
2. **No two variants share hook family + insert ladder rung** — if two hooks come
   from the same strong family (legal), those variants MUST sit on different rungs.
3. All four lengths differ.

A collision is fixed by moving a variant to a different rung, re-anchoring its
overlays, or swapping its hook family — never by shipping the twin.

## Contract mapping

- **ONE render_plan.json per variant ad** (`ad_id` e.g. `brand_testimonial_A` …
  `_D`). Each plan lists its own hook gen + its rung's insert entries (`kind:
  "gen"` inserts, `kind: "still"` flashes) PLUS the full shared body.
- **Shared body gens carry the SAME `gen_id`, `prompt_file`, and `voice_cut` in
  every plan and are rendered ONCE** — the dispatcher skips any gen whose
  `gens/<gen_id>.mp4` already exists, so the shared spine costs one render, not
  four (and its one voice-cut fingerprint is used exactly once, per
  voice-and-parallel.md). A shared-gen re-roll gets a fresh recut and the new file
  flows into ALL variants.
- The shared spine's first gen is the ONE `is_identity_checkpoint` in every plan:
  it renders alone, the member approves the identity once, then all four variants'
  remaining gens fan out in parallel.
- Shared gens are whisper-cut once; their clips (and `cut_report.json` words) are
  reused by every variant's edit.
- **Four edl.json files**, one per variant: same shared clips in `base[]`, but a
  different hook clip, different `overlays[]` (count + anchors, per rung),
  different `trim[]` choices, and the format's `rhythm_targets` enforced on each
  at stitch. Same raw footage, four genuinely different edits — which is the whole
  feature.
