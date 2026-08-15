# Output template — locked

Fill the bracketed slots. Add no sections. Timestamps in tenths, zero-padded seconds,
en-dash, every shot starting exactly where the previous one ended.

---

```
Overall Style & Aesthetics:

* Subject: [The person. Hair, skin, eyes, nails. Base outfit, then any layers added for
  other locations, so one line covers a wardrobe that changes across the video. Omit this
  block entirely if no person appears.]
* Props: [Every object that appears, product first. Label text spelled out in full,
  exactly as it reads on screen.]
* Lighting & Vibe: [Setting, light quality, aspect ratio, cut pace.]
* Audio: [see the three audio cases below]

Scene Breakdown

0:00–0:0X.X
Shot Type: [framing / angle / static or the specific move]
Action: [what happens, one beat]
Dialogue: [see below]

0:0X.X–0:0Y.Y
Shot Type:
Action:
Dialogue:

[...one per shot...]
```

---

## The three audio cases

These describe **the reference video**, so all three are legitimate observations and a
reference may well carry a voice over a music bed. The member's own **render prompt** is
different: it carries a voice or music, never both, and the music goes on afterwards in an
editor. Record what the reference did; write the render with one.

**Music only** — a bed runs, nobody speaks:

```
* Audio: Ambient music only. No voiceover, no talking.
```
Every shot then carries `Dialogue: (None)`.

**No audio stream at all** — ffprobe shows no audio index:

```
* Audio: Silent. No audio track.
```
Every shot carries `Dialogue: (None)`. Never call this music.

**Speech present** — transcript exists, so every shot is marked:

```
* Audio: One [woman's/man's] voice throughout. [Music bed / no music, room tone only.]
```
Then per shot, one of:

```
Dialogue (On-Camera):
"[verbatim words that land in this shot]"
```
```
Dialogue (Voiceover):
"[verbatim words that land in this shot]"
```
```
Dialogue (Voiceover):
(Continues over the shot)
```

The `(Continues over the shot)` form is for a sentence that started in an earlier shot and
runs past the cut. Use it rather than `(None)`, which would claim silence that is not there.

When the 5,000-character ceiling binds (Step 7), **`Dialogue (VO):` is the sanctioned short
form** of `Dialogue (Voiceover):`. It is the only abbreviation this template allows, and on
a 22-shot speaking video it recovers 154 characters of pure repetition. `Dialogue
(On-Camera):` is never shortened, because the distinction it carries is the whole point of
the marking.

---

## Definitions the marking depends on

**Voiceover** — the subject's mouth is not moving to speak, or she is not in frame at all,
and the voice continues over the shot.

**On camera** — the subject is visibly speaking and the lips are in sync with the words.

The distinction is decided by the lip-sync test in Step 6, never by the presence of audio.
A shot with a voice over it is not on-camera speech until the mouth is checked.

---

## Worked references in the member's project

Two filled examples exist under `21_Custom_Ads/`:

- `reference-sauvage-elixir/recreation-prompt.txt` — speech ad, 9 shots in 32s, mixes
  on-camera and voiceover, jump cuts inside one framing.
- `reference-armani-power-of-you/recreation-prompt.txt` — music-only ad, 14 shots in 20s,
  every `Dialogue` line `(None)`.
