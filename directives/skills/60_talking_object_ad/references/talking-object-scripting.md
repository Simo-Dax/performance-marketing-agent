# Talking-Object Scripting — the cast carries the ad

The talking-object script is DIALOGUE, not narration: every line is spoken ON CAMERA by a
character whose mouth animates with the words. You are not writing a voiceover — you are
writing a tiny ensemble comedy that sells. This doc is the Step 1–2 craft. The quality bar
is the primary bank (`scene-bank-ingredient-parade.md`) — its recovered script is the
swipe file; match its rhythm exactly.

## The format formula (from the primary bank)

```
1. VILLAIN HOOK      the customer's problem personified, self-roasts        1 line,  ~15 words
2. HERO PARADE       2–4 ingredients/features, each: "Hi, I'm ___..."       1 line each, 15–25 words
3. PRODUCT REVEAL    the product(s) as the assembled answer                 1 line,  ~20 words
4. CTA               the product asks for the sale, points at the link      1 line,  ≤16 words
```

Total: **5–8 speaking scenes, 30–60 seconds** (the flagship runs 54s with 7 scenes; the
Alpha Serum secondary source runs 32s). Fewer heroes is always better than compressed
heroes — cut a character, never cram two mechanisms into one speaker.

## LAW 1 — Every word is character speech

There is no detached narrator by default. Villain, heroes, and product all speak in first
person. If a bridge line genuinely needs a narrator (rare), confine ALL narrator lines to
ONE single clip — Seedance casts the narrator voice fresh per generation, so a narrator
spread across clips comes back as a different voice every time. (A recurring CHARACTER
solves this with a video reference; a disembodied narrator has no character to reference.)

## LAW 2 — The dialogue formula (the chorus)

Every ingredient/feature hero speaks the same sentence skeleton — the repetition is the
format's rhythm:

> **"Hi, I'm [INGREDIENT]. I may help [MECHANISM VERB] [THE BAD THING], so you can stop
> [PAIN] and start [DESIRE]. With diet and exercise."**

The three load-bearing pieces:

1. **"I may help"** — the compliance hedge INSIDE the character's voice. It reads as
   humility, not legalese. Never "I will", "I fix", "I cure", "I guarantee". Mandatory on
   every regulated claim (body composition, hormones, fat loss, health outcomes, income).
2. **"so you can stop ___ and start ___"** — pain and desire in one breath, concrete and
   daily-life sized ("stop crashing at 3pm and actually have energy for your family") —
   never clinical, never spec-sheet.
3. **The compliance close ("with diet and exercise" / "with proper diet and exercise")** —
   attached to every REGULATED claim, omitted on unregulated ones (the flagship's energy
   line has no close and breathes better for it). Hedge where regulators watch; breathe
   where they don't.

Vary the greeting so the chorus never goes stale: "Hi" → "What's up" → "Hey" → no greeting
at all (straight to "I'm ___") — the flagship uses all four across four heroes.

## LAW 3 — The villain hook

The opener is the customer's PROBLEM personified, self-roasting, sharing the viewer's
grief:

> **"Hey, I'm your [PROBLEM]. Remember when you [HAD THE GOOD THING]? Yeah… me too."**

- `[PROBLEM]` in the customer's own words (from VOC): muscle loss, the 3pm crash,
  thinning hair, the cluttered inbox. The PROBLEM — not the competitor product (that's
  the Alpha Serum secondary mode: the old-way product introduces itself and roasts its
  own flaws; both hooks are legal, the problem-villain is the primary).
- Keep the **"Yeah… me too"** beat — the shared grief IS the hook.
- 12–16 words, deadpan-sad delivery. The villain speaks once and is never seen again.

## LAW 4 — Line length is clip length (~2.8 words per second)

Dialogue clips are sized from the words: the flagship averages **2.8 words/second
including acting pauses**. Seedance renders 4–9 second clips, so:

- **A line runs 11–25 words.** Under ~11 words → the clip pads with silent acting
  business (legal and charming — a beat of business before/after the line); over 25
  words → the line MUST be trimmed or split into two scenes (and a split makes the
  speaker RECURRING: its second scene carries the first clip as a video reference, in a
  new environment — the reference ladder, tier 3). `segment_scenes.py` enforces this.
- Never pack a line to the 25-word ceiling by default — 15–22 words is the sweet spot.

## LAW 5 — The product reveal and the CTA

- **Reveal:** the product(s) enter as the assembled answer, on a pedestal from the
  customer's aspiration world (45 LB plates, a cutting board, a desk riser). A duo/stack
  gets an element pair with tension ("a steel and fire stack"). The line ties the parade
  to the offer: mechanism verbs return, now winning. First-person plural when the
  products speak ("Together, we're...") — hold whatever attribution you pick through the
  CTA.
- **CTA:** the product asks for the sale ITSELF and physically points down at the link:
  > **"If you want to get us [OFFER], you can just click the link below."**
  Sixteen words or fewer — the flagship's is exactly 16, and the offer token ("70%")
  counts as a word. First person ("get us" / "get me"). The offer may ALSO render as
  in-scene 3D text in this clip only (the style doc's one text exception). Nothing
  follows the CTA.

## Voice casting (written at script time, locked per character)

Each character's `voice` field is 4–7 words locking age, texture, and energy — written
into the script, approved at Gate 1, pasted verbatim into every dialogue block:

| Character | Voice casting |
|---|---|
| Villain (muscle loss) | small, deflated, apologetic, deadpan-sad |
| Brawler hero | warm, cocky, confident, mid-30s male |
| Knight hero | low, assured, knightly, calm |
| Sweetheart hero | bright, kind, light, smiling |
| Ember hero | low, smoldering, deliberate |
| Product duo | deep, unified, proud |

## Beat-writing rules

- **Present tense, short punchy sentences.** The line must sound SPOKEN, not written —
  read it aloud once before locking it.
- **One claim per character.** The character IS the claim; a second claim needs a second
  character.
- **Every claim names its prop.** When you write "stress hormones that block your natural
  testosterone", the storyboard needs red orbs the character can punch. If you can't name
  the prop while writing the line, rewrite the line.
- **Specificity = believability.** "crashing at 3pm", "stubborn belly fat", "the last
  enzyme" beat vague claims.
- **No corporate voice.** Banned: "revolutionary", "seamless", "leverage", "solution",
  "game-changer", "unlock", "elevate". Characters talk like people.
- Honor the brand voice rules from the Brand DNA (banned words, tone) and pull the pain
  and desire slots from VOC verbatim where possible — Gate 1 names which line carries the
  VOC anchor.

## The swipe file (the primary bank's recovered script — the voice bar)

- **Villain:** "Hey, I'm your muscle loss. Remember when you used to be strong? Yeah… me
  too."
- **Brawler:** "Hi, I'm ashwagandha. I may help reduce stress hormones that block your
  natural testosterone, so you can stop feeling drained and start feeling like yourself
  again. With diet and exercise."
- **Sweetheart:** "Hi, I'm enXtra. I may help give you sustained energy all day, so you
  can stop crashing at 3pm and actually have energy for your family."
- **Ember:** "I'm Coleus Forskohlii. I may help your body burn stored fat for energy, so
  that stubborn belly fat can finally start coming off. With diet and exercise."
- **Product duo:** "Together with a steel and fire stack designed to help you reclaim
  your masculine energy while torching the fat that's stealing it. When combined with
  diet and exercise."
- **CTA:** "If you want to get us for 70% off, you can just click the link below."

## Non-supplement translation (the formula is product-agnostic)

| Product | Villain | Heroes (personality) | Prop |
|---|---|---|---|
| SaaS time-tracker | "your Sunday-night invoicing panic" (crumpled receipt) | auto-capture (sweetheart, a gauge fills), one-click invoices (brawler punching paper stacks) | receipts as a landscape |
| Skincare | "your 6-week breakout" (sad clogged pore) | salicylic acid (knight slashing sebum blobs), niacinamide (sweetheart, redness gauge cools) | pore tunnel world |
| Coffee brand | "your 3pm crash" (deflated battery) | slow-roast beans (ember), l-theanine (sweetheart) | a battery that fills |

When presenting the script, state the mode (full-cast / dignity), name each character's
personality in one word, and name the prop for every claim.
