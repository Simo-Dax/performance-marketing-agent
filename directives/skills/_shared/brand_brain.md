# Brand Brain — the compiled brand memory

Some brands carry a curated, compiled memory at `$AILAB/_knowledge/`, written by the the agent desktop app. When it exists, it is the source of truth for what is on-brand: the user has approved rules into it, the app has distilled their feedback into it, and every file in it is regenerated from the brand's real folders on every build. Skills READ it; only the app writes it. Never create, edit, or delete anything under `_knowledge/`.

## The files

| File | What it is | When to read |
| --- | --- | --- |
| `context-pack.md` | The always-read core (~2k tokens): hard rules, forbidden phrasing, identity and voice, winning and losing angles, performance learnings, inventory, competitor patterns, offer, recorded feedback | ALWAYS, before any creative or strategic decision |
| `prompt-bank.json` | Recreation-grade prompts banked by /spy, ranked winners-first. Each entry: `{ id, brand, headline, tier, days_running, is_active, run_date, image, prompt }` — `prompt` is the full render-ready text, `image` is the source creative's path relative to `the agent/` | When picking reference ads for statics or rebuilds |
| `intel-pack.md` | Per-competitor intelligence: what they run, longest runners (the spend proxy), video hooks seen, paths to full teardowns | When strategy or concepting needs the competitive picture |
| `assets-index.md` | Reusable asset paths: user-uploaded product photos, Studio renders (labeled by their generation prompts), finished statics with concept joins, characters, assembled video ads | Before asking the user to upload or recreate ANYTHING |

## How to honor it

1. **Hard rules and forbidden phrasing are binding.** Not suggestions. If the pack says never say it, never say it — including close paraphrases.
2. **Recorded preferences and feedback steer output.** "Lean" preferences bend your defaults; feedback about past work must not be repeated.
3. **Winning angles are the starting bench; losing angles are benched.** Do not re-pitch a killed concept unless the user explicitly asks to retest it.
4. **"Taste vs data" entries are flagged conflicts** — the user's reaction disagrees with the performance data on the same ad. Surface the conflict to the user; never silently side with either.
5. **Inventory means don't recreate.** If the pack or `assets-index.md` lists it, use the existing file's path instead of generating or requesting it again.
6. **The prompt bank counts as a first-class reference source.** A banked recreation prompt is equivalent to a swipe-file teardown: design kept, identity swapped.
7. **The live user outranks the pack.** If the user's instruction in this session contradicts a pack rule, follow the user — and say in one line that the Brain disagrees, so they can update it deliberately.

If `_knowledge/` does not exist for this brand, skip all of this silently and continue — the brand simply has no compiled Brain yet.
