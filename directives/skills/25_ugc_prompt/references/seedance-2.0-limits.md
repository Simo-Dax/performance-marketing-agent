# Seedance 2.0 limits and the fast-pace engine

Seedance 2.0 only. If a number here conflicts with `references/VERIFIED-backend-facts.md`, that file wins. For structure, `references/generation-architecture.md` wins.

## 1. Hard per-generation limits

| Limit | Value | Why it matters |
|---|---|---|
| Max duration | UNDER 10 seconds (integer 4 to 9) | Every generation is short; a longer ad is many short generations concatenated. There is NO 15s generation. |
| Duration values | integer 4 to 9 | Always request an explicit integer 4 to 9. Never auto, never 10+. |
| Aspect ratio | 9:16 vertical | The factory outputs 1080x1920. |
| Resolution | 1080p (default) | About 9 credits/sec. |
| Audio | enabled on EVERY generation | Native voice from the attached voice reference, in that voice, saying the shot's words. The product-only b-rolls get the voiceover too. |
| Scenes per generation | one OR several (described in the prompt) | No multi-shot parameter. Describe the scenes, set only the TOTAL seconds; Seedance cuts. Multi-scene gens are split into clips after. |
| Reference media | face + body + product on character shots; product + voice ONLY on b-rolls | Same bytes every time. B-rolls never carry the character. |
| Cost | about 9 credits/sec at 1080p | Per second, so batching saves nothing. Leverage = reuse body + b-roll pool, fan unique hooks. |

There is no separate voice track, no clone step, no TTS, no spine, and no force-muting anywhere.

## 2. THE FAST-PACE ENGINE (the make-or-break)

The single most important fact: **Seedance STRETCHES the spoken line to fill the duration you request.** The duration you choose IS the talking speed.
- Request too MANY seconds for the words and Seedance talks slowly to fill it — the delivery DRAGS (slow, sluggish, dead-feeling). This is the failure mode, not clipping.
- Request too FEW and it rushes / skips.
- So you do NOT leave a "breath buffer". You target the speaking pace you want directly.

### The rule

```
requested_seconds = round(word_count / WPS)      WPS = 3.5 (fast, punchy UGC)
action_buffer     = +1 to +2 seconds, HOOKS ONLY (for the on-screen action: dump / slam / toss)
generation_seconds = requested_seconds + action_buffer    (must be 4..9, UNDER 10)
```

- Talking body shots and product-only b-rolls get NO action buffer — the voiceover fills the slow product motion.
- Target band: about **2.4 to 4.0 effective wps**. Below ~2.4 it drags; above ~4.0 it rushes.
- EVERY generation must be UNDER 10 seconds. If a chunk needs 10s or more at 3.5 wps (more than ~31 words), SPLIT it into more generations.

### Worked examples (WPS 3.5)

| Line / scene | words | round(words/3.5) | + action | generation | wps | verdict |
|---|---|---|---|---|---|---|
| body beat "My counter used to be a row of supplement bottles, and I never knew which ones did anything." | 18 | 5 | 0 | 5s | 3.6 | OK (talking) |
| body beat "AG1 is one scoop with over seventy ingredients, so it replaced that whole shelf." | 14 | 4 | 0 | 4s | 3.5 | OK |
| hook reel: two ~11-word hooks, with a bottle-dump and a slam | 22 | 6 | +1 to +2 | 7 to 8s | ~3.5 speech | OK (action eats the extra) |
| product b-roll "One scoop, once a day. That is the entire routine." | 10 | 3→4 | 0 | 4s | 2.5 | OK (clamped to 4s floor) |
| 31-word block | 31 | 9 | 0 | 9s | 3.4 | OK, at the ceiling |
| 35-word block | 35 | 10 | — | — | — | TOO LONG (>=10s); split into two generations |

## 3. Segmentation so every generation is under 10 seconds

A framework body runs 20 to 30 seconds total, far more than one generation, so it is split — but now the cap is UNDER 10s, not 15s.
- Split ONLY at sentence / beat boundaries; a generation never starts or ends mid-thought.
- Each body beat is its OWN generation (segment beats one at a time so the packer never merges one beat's first sentence onto the previous clip).
- Each generation independently lands at ~3.5 wps and UNDER 10s.
- Hooks are short, so ~2 hooks share one generation (a reel) that is still under 10s; the reel is split into clips after.
- `scripts/segment_script.py` enforces all of this: it derives seconds at 3.5 wps, flags any generation that hits 10s or whose pace falls outside ~2.4 to 4.0 wps, and refuses to drop content.

## 4. Cost note

Billing is per second at ~9 credits/sec (1080p). No saving from cramming. The real leverage is structural: render the body core ONCE and reuse it, render the 2 b-rolls ONCE and reuse them, and fan 4 unique short hooks (rendered as 2 reels).
