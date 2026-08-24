# The house caption style (user-locked)

Every value here was set by the user on real footage. Do not "improve" them.
`scripts/caption_lib.py` is the implementation; this file is the contract.

## Typography and placement

| Setting | Value | Why |
|---|---|---|
| Font | **Montserrat** requested. Currently renders in **Avenir Next Heavy** (`/System/Library/Fonts/Avenir Next.ttc`, face index 8) because Montserrat is not installed. Closest geometric-sans match available. | The one open item. Swap `FONT_PATH` / `FONT_INDEX` when Montserrat lands. |
| Size | **58px** at 1080x1920, scaled by frame height for other resolutions | Calibrated so a 3-4 word card spans ~38% of frame width, matching the user's reference frame |
| Colour | white `#FFFFFF` | |
| Edge | **soft blurred drop shadow** — offset (0,+5), blur 7, alpha 170 — plus a 2px hairline dark edge | A hard black stroke was explicitly rejected. The shadow is what makes it read as the reference. |
| Position | baseline **y=1275** at 1080x1920 (~66% down) | Moved up from 1432, then back down from 1250. This is the settled value: clears faces in close-ups, clears the TikTok/Instagram bottom UI band. |
| Rows | **ALWAYS one.** Never wraps. | Enforced on rendered pixel width (<= 88% of frame width), not character count — character limits are unreliable because glyph widths differ. |

## Word rules

- **Mostly 2-3 words per card.** 1 or 4 are allowed only where they genuinely read
  better. On the user's 13-ad collection this lands at ~92% in the 2-3 band.
- Split on **real speech pauses** (>=0.20s) and on punctuation in the transcript.
- **Never end a card on a word that binds to the next one** — "the", "than", "your",
  "if", "inside"... See `BIND` in caption_lib.
- **No dots and no commas anywhere.** Not just trailing — stripped throughout.
- **Only the very first word of the whole video is capitalised.** Everything after it
  is lowercase.
- **Proper nouns keep their capitals**: AI, Claude Code, ROAS, ChatGPT,
  Canva, IKEA, Meta, Brand DNA, Russian. Extend `PROPER` as brands appear.
- **Multi-word names never split across cards.** "Claude Code" and any brand name are
  atomic; "the agent" additionally gets its own card.
- Abbreviations survive the no-dots rule: `a.m.` renders "am", not "a m".
- Contractions are captioned as spoken: "would've", never "would have".

## How the split is chosen

Not greedy. Each phrase is partitioned by a dynamic-programming search that minimises

    (cards outside 2-3 words) x 1.0  +  (cards ending on a binding word) x 2.0

subject to the hard one-row width limit. Weighting the binding penalty higher is what
makes it reach for a 1- or 4-word card only when the alternative would break a phrase
in the middle.

## Correctness

Speech recognition is reliable about WHEN a word was said and only approximate about
WHICH word it was. Whenever the real script exists, force-align: whisper supplies the
timings, the script supplies the words. On this collection that turned "ROAS" into
"row ass" in three ads, "Claude Code" into "cloud code" in three more, and "mines"
into "minds" in two — every one of them an ASR artifact the script never contained.

Always run the audit and report it: card count, % in the 2-3 band, any two-row card,
any punctuation, and whether the captions match the script word-for-word.

## Output contract

- Writes `<name>_captioned.mp4`; **never overwrites the clean master.**
- Writes `<name>.captions.json` beside it (script, word timings, cards, audit).
- Audio is stream-copied, so loudness and mix are untouched.
- Video re-encodes h264 CRF 18 at source resolution.
