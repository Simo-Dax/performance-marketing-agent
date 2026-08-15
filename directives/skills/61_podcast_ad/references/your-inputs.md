# Making your inputs (host images + voice clips)

For each host you upload **one portrait image + one 10–15s voice clip**. The skill never generates faces or voices — you bring them. (Both are also covered in a video tutorial in the community.)

Two hosts = **two images + two voice clips**.

## 1. Host reference images

1. **Find a real podcast still.** Go to **Pinterest** (best for clean stills) — or TikTok, YouTube, Instagram, whatever — and search "podcast," "podcast setup," "2 host podcast."
2. **Pick a two-host shot** — both hosts in a studio, sitting across from each other.
3. **Screenshot each host separately** — one frame for the left host, one frame for the right host. These are *scene references*, not your finals.
   - ⚠️ **Pick frames where each host looks toward the other** — left host looking screen-right, right host looking screen-left. The skill mirrors these eyelines so the cut reads as one conversation. If both look the same way, the gazes won't meet.
4. **Generate each host image from its screenshot** in an image model — GPT Image 2 recommended. Tell it to keep the **same scene and setting** as the screenshot, with your host in frame.
5. **The character is yours** — yourself, a teammate, an invented person, anyone. Swap the person, restyle wardrobe, change whatever you want.
6. **Brand it if you want** — add your logo, a branded mug, your colors to the set. Totally optional.
7. **Lighting will drift.** The model won't copy the screenshot's lighting exactly — expect it to come out a little different. If matching lighting matters to you, say so explicitly in the prompt.
8. **Make the two hosts share one studio: generate host 1 first, then feed host 1's *generated* image back in as a reference for host 2** — and prompt "same room, same lighting, same setting." That shared reference is what keeps both hosts looking like they're in one studio.

## 2. Host voice clips

You upload **one voice clip per host — 10–15 seconds.** The model clones the **voice and accent** from it for every line that host speaks — this is what keeps the voice consistent across the whole ad. The actual words in the clip don't matter (your scripted lines will be different); only the voice does.

Where the voice can come from:

1. **Your own voice** — just record yourself talking for 10–15 seconds.
2. **Someone else's voice** — any clean clip of a real person's voice.
3. **A generated voice** — make one in **ElevenLabs** (or any AI text-to-speech model) and use that. (Also taught in the community.)

Keep it clean:

- ⚠️ **One voice only** — no music, no background noise, no second person talking. A clean clip clones far better.
- **Talk naturally** — normal podcast pace and energy; the clone matches tone and accent.

---

**Result:** two images + two voice clips (one of each per host) — everything you upload at intake.
