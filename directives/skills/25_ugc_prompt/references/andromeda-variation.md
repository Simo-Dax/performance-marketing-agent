# Andromeda Variation

How to turn ONE re-cut body into 4 UGC ads that Meta's Andromeda treats as 4 distinct ads, not near-duplicates. For the full structure see `references/generation-architecture.md`.

## 1. Why the old way is dead

The BEFORE-Andromeda playbook was: build one body, swap only the hook, ship 4. Andromeda's creative retrieval collapses near-duplicate timelines into one entity and throttles the duplicates, so that playbook burns budget.

The AFTER-Andromeda requirement: each ad is a genuinely DIFFERENT TIMELINE. In this factory the difference comes from **4 UNIQUE hooks + a B-ROLL-COUNT LADDER**, and **every ad ends on the CTA**. There is NO hook-length ladder anymore.

## 2. The distinctness levers

### Lever 1 — four UNIQUE hooks (one per ad)
- A different spoken hook line per ad, each a different ANGLE (e.g. confession, contrarian, direct claim, curiosity). Never reuse a hook across ads.
- A different KIND of dramatic visual action in the first 1 to 2 seconds (an action, not a talking head). Pull from the visual archetypes in `references/hook-library.md`. Use different kinds, not two near-identical camera moves.
- Hooks are uniformly SHORT (~3 to 5s, ~8 to 13 words). Hook length is NOT a distinctness lever and is not laddered.

### Lever 2 — the b-roll-count ladder (0, 1, 2, 2)
- The b-roll pool is exactly **2 product-only clips (bA, bB)** — no character, voiceover only (see `references/consistency-and-assembly.md`).
- Each ad uses a different NUMBER of them, inserted at spaced points: V1 uses 0, V2 uses 1, V3 uses 2, V4 uses 2.
- B-rolls are inserted only in the MIDDLE of the timeline (after the hook or between body beats) — NEVER after the CTA.
- V3 and V4 both use both b-rolls but at DIFFERENT placements, so they read as different timelines even at the same length.

### The default 4-ad matrix (every ad ends on the CTA)

| Ad | Verbal hook (example, short) | Visual action | B-rolls | Timeline |
|---|---|---|---|---|
| V1 | "Okay, I literally owned like thirty supplement bottles." | dumps an armful of unbranded bottles | 0 | hook → pain → solution → proof → CTA |
| V2 | "Stop buying ten supplements that just cancel each other out." | slams the product down | 1 | hook → bA → pain → solution → proof → CTA |
| V3 | "This one pouch replaced every supplement I used to take." | lifts the product to the lens | 2 | hook → bA → pain → solution → bB → proof → CTA |
| V4 | "I finally threw out my entire cabinet of supplements." | tosses a cabinet of bottles into a bin | 2 | hook → pain → bA → solution → proof → bB → CTA |

## 3. The distinctness fingerprint

Every ad gets a fingerprint = a stable hash of RENDER-AFFECTING axes ONLY: visual_hook (the opening action) + sorted b-roll set + b-roll COUNT + b-roll placement indices + ordered roles in the timeline. The free-text verbal hook is NOT in the hash (it varies by construction).

`scripts/build_manifest.py` computes the fingerprint and enforces:
- All 4 fingerprints unique (it names colliders so you change a placement or a visual hook).
- **Every ad's ordered_timeline ENDS ON THE CTA body beat** — it rejects any timeline that does not, and any b-roll placed after the CTA.
- V3 and V4 (same b-roll count) must differ in b-roll PLACEMENT.

Because the four hooks are unique and the b-roll count/placement differs, the four timelines are genuinely distinct — they read as four different creators, which is what Andromeda needs.

## 4. Length (known and accepted)

With 2 b-rolls + uniformly short hooks + the always-end-on-CTA rule, lengths fall into THREE bands: V1 shortest (0 b-rolls), V2 (1), V3 ≈ V4 (2). Three of the four differ; V3 and V4 match in length but are distinct timelines. All four land in 25 to 45 seconds. (To force all four lengths distinct, vary one hook's length or give one ad an extra body beat — otherwise this is the structure.)

## 5. Scaling past 4

To make more than 4 distinct ads, do NOT pile more hooks or b-rolls onto the same body. Run 2 to 3 different frameworks for the same product as independent ad families, each producing its own 4 ads. Reuse the locked character, body, and voice clip across all of them.

## 6. Spoken versus on-screen text

On-screen text (added by the member in editing, not by Seedance) must never be a verbatim copy of the spoken hook. Use it to carry a second message, a stat or a contrast.
