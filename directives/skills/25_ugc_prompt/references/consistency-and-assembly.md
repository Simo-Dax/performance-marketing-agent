# Consistency and assembly: one person, one voice, voiceover b-rolls, four distinct timelines

How the skill keeps every CHARACTER clip looking like the same person, sounding like the same voice, keeps the B-ROLLS as voiceover (product-only or character, never a talking head), then cuts everything into 4 genuinely different ads that each end on the CTA. Obeys `references/VERIFIED-backend-facts.md` and `references/generation-architecture.md`; if a number conflicts, those win. No clone step, no voice-ID step, no TTS, no separate spine, no force-muting.

---

## 1. Character consistency

### 1.1 The locked images are the identity method
The member uploads ONE face image and ONE body image. Those exact files, the same bytes, are attached on EVERY CHARACTER generation (the hooks and the body shots). Do not re-crop, re-compress, or re-export them between generations. Pick the two images once, freeze them, reuse the identical files. Reference-video chaining is NOT the identity method.

The product image is attached on character shots where the product is on screen, and on every b-roll. A character b-roll also carries the locked face + body bytes; a product-only b-roll carries the product image as its only image reference.

### 1.2 Prompts: keep it simple, do NOT over-describe anything
Every prompt opens with: **"A realistic, authentic UGC ad."** For character shots, add: **"Keep the character consistent with the reference images."** That is it for the person — do NOT write a wardrobe/hair/lighting descriptor block; the reference images carry the look, and over-describing fights them.

The scene direction is LESS IS MORE, matching SKILL.md Step 5 exactly: ONE short line naming the setting and framing (the beat's rung on the scene ladder, e.g. "walking down a sidewalk, handheld selfie video"), ONE emotion word for the delivery ("delivery: fed up" / "relieved" / "confident"), and the EXACT spoken quote. Hooks add a few direct words for the visual action. Nothing else — no lighting paragraphs, no beat-by-beat choreography for a talking shot; over-writing fights the model. End with "No on-screen text or captions." For a multi-scene generation (a hook reel), describe each scene with a hard cut between them and set only the total seconds.

### 1.3 B-rolls are voiceover (product-only or character)
A b-roll is a product-focused clip carried by the voiceover; the character never talks to camera in one. By default it features the character: either the character's own hands holding and filming the product (one hand holds, one hand films, face out of frame), or the character using or demonstrating the product while the voiceover plays. A product-only b-roll (product held by an anonymous hand or standing on a surface, with a slow push-in or pan) is also fine. A character b-roll attaches the same locked face + body bytes + the product image + the voice clip (the prompt keeps the character off-mic, and for a hands-only b-roll keeps the face out of frame). A product-only b-roll attaches the product image + the voice clip ONLY, no face, no body.

### 1.4 MANDATORY verification (cut check + frame check, both free)
Never declare a batch good because the renders returned. Two checks run on every generation BEFORE assembly, and both are free:

1. **The word check** rides the `whisper_cut.py` pass: it prints each line's match ratio (recognized words vs the script). A low ratio (<75%) means Seedance garbled or swapped words — LISTEN to that clip. Only genuinely wrong words justify proposing a re-render, which is the member's call with its own fresh yes.
2. **The frame check** (`frame_check.sh` per clip → read every contact sheet): character on-model against the locked face/body images (face, wardrobe), the hook's visual action actually rendered, each b-roll is a voiceover with NO talking face (character b-roll: the character matches the locked images; product-only: only the product in frame), no generated text in any frame, and the product at a believable scale. A content miss is fixed by re-cutting to the good footage when possible; a re-render needs its own fresh explicit yes.

---

## 2. Voice consistency (the locked model)

### 2.1 One voice, one unique cut per generation
The member uploads ONE voice clip, max 15 seconds. On Higgsfield paths (A/B/D) each generation attaches its OWN uniquely-fingerprinted cut of it (`make_voice_cuts.py`; see `references/voice-and-parallel.md` for the `_sfx` dedup bug that makes this mandatory and for why re-uploading the same file does not work). On Path C (fal) the original clip uploads once and its URL is reused. Either way it rides every generation: hooks, body shots, AND the b-rolls (as the voiceover). Seedance speaks each shot's new words in a voice that matches it. Same voice every time → consistent voice automatically, and unique fingerprints → the whole batch renders in parallel safely.

### 2.2 Audio is ON for every generation
Audio stays on for every clip, b-rolls included (the b-roll is a voiceover over the product). No silent clip unless a beat is deliberately wordless. The only limit: the reference clip is max 15s (cuts capped at 14.5s).

### 2.3 What we never do
No clone step, no voice-ID step, no TTS, no externally authored spine, no force-muting at assembly. Each clip carries its own consistent voice; assembly just keeps it. And never one shared voice file across a parallel batch on Higgsfield — that is the `_sfx` silent-failure trap.

---

## 3. Always-on audio at assembly

1. Keep every clip's own audio and concatenate. Do not mute.
2. No separate spine. There is no voice_track field. build_manifest.py refuses to emit or accept one.
3. Smooth the seam, do not duck the voice: stitch.sh applies a very short equal-power audio crossfade (~80ms, AUDIO_SEAM_MS) at each cut to remove clicks and tonal steps. Not a spine; far below a spoken word.
4. Optional short PICTURE-only crossfade (xfade), independent of the audio seam.
5. Normalize the final cut to about -14 LUFS (two-pass loudnorm) so all 4 ads match.

---

## 4. The segmenter (scripts/segment_script.py)

The body runs longer than one generation, so it is split — every generation UNDER 10 seconds.
- Concatenate each beat's vo_line into the spoken script; split only at sentence/beat boundaries (never mid-thought).
- Derive each generation's integer seconds at the fast pace: `round(words / 3.5)` — or pass `--wps <measured>` when the brand's spy-video teardowns give a real number — plus 1 to 2s of action time on HOOKS only. Every generation must be 4 to 9s (under 10).
- Each body beat is its own generation (segment beats one at a time so the packer never merges one beat's first sentence onto the previous clip).
- It prints a table (words, seconds, wps) and flags any generation at 10s+ or outside ~2.4 to 4.0 wps. The member confirms BEFORE any generation spends credits.

---

## 4.5 The cutter (scripts/whisper_cut.py) — word-accurate, all free

After the renders land, every generation is cut BEFORE assembly. faster-whisper transcribes each mp4 with word timestamps, the KNOWN script lines are aligned to the recognized words (difflib — robust to a mis-heard middle word, never silence-guessing), and each line becomes one clip:

- The FIRST line of a generation keeps the clip's natural head (starts at 0.0) so a hook's visual action is never chopped; later lines in a reel start ~0.08s before their first word — the word-accurate reel split.
- Every line ends ~0.20s after its LAST word — snappy, the word rings out, no dead tail. The CTA line gets ~0.6s (set per-line in render_plan.json) so the ad breathes at the end.
- A clip never bleeds into the next line (bounded at next_start − 0.05).
- Internal scene cuts are detected and PRINTED, never auto-truncated — a UGC hook may legally contain a deliberate hard cut (a before/after).
- The pass prints each line's MATCH RATIO; low ratios get listened to before assembly (see 1.4).

This is why floor-padded generations are safe (a 3s line in a 4s render loses its dead tail) and why the ads feel cut by an editor instead of stitched from whole renders. Re-running the cutter or the stitcher costs nothing — always exhaust the free edit loop before any re-render.

---

## 5. The assembly manifest (assembly-manifest.json)

The single contract. No voice_track field; each clip keeps its own audio. Every ad's ordered_timeline ENDS on the CTA body beat.

```json
{
  "concept": "string", "niche": "string", "date": "YYYY-MM-DD",
  "fps": 30, "resolution": "1080x1920", "media_type": "video",
  "framework": "string", "voice_ref_clip": "path",
  "character": { "face_image": "path", "body_image": "path", "product_image": "path" },
  "body": { "shots": [ { "shot_id": "string", "clip": "path", "words": "string", "word_count": 0, "seconds": 0 } ] },
  "variants": [
    {
      "variant_id": "string",
      "verbal_hook": "string", "visual_hook": "string", "hook_clip": "path",
      "broll_set": ["path"],
      "ordered_timeline": [ { "role": "hook|body|broll", "clip": "path", "trim_in": 0, "trim_out": null } ],
      "total_seconds": 0, "distinctness_fingerprint": "string"
    }
  ]
}
```

Field notes:
- character.product_image is always present (every b-roll shows the product).
- body.shots: the reusable body beats, each ending in order with the CTA beat last.
- variants[].ordered_timeline: the per-ad cut. role is hook, body, or broll. **The last entry must be the CTA body beat.** b-rolls appear only in the middle. trim_out null means play to the clip's end.
- distinctness_fingerprint: hash of render-affecting axes (visual_hook + sorted broll_set + b-roll count + placement indices + ordered roles), unique per ad, enforced by build_manifest.py — which also enforces ends-on-CTA and no-b-roll-after-CTA.

---

## 6. The ffmpeg assembly (scripts/build_manifest.py then scripts/stitch.sh)

### 6.1 build_manifest.py (the planner)
Inputs: the segmenter output (body.shots), the rendered body clips, the 4 split hook clips, the 2 b-rolls, the locked references, and the variant definitions. It fills body.shots with each clip path and seconds, builds each ad's ordered_timeline (hook, body beats, b-rolls at the ad's chosen MIDDLE points, CTA last), computes total_seconds and the fingerprint, and HARD-enforces: unique fingerprints; every ordered_timeline ends on the CTA; no b-roll after the CTA. It refuses a voice_track field. The b-roll-count ladder and V3-vs-V4 placement difference are only WARNED about (the fingerprint includes the visual hook, so differing hooks alone keep fingerprints unique) — the orchestrator checks both by hand and treats any ladder warning as a failure.

### 6.2 stitch.sh (the muxer)
Reads one ad's ordered_timeline, scales/pads each clip to 1080x1920 at 30fps, concatenates KEEPING each clip's audio (~80ms seam crossfade, never mutes), two-pass loudness-normalizes to -14 LUFS. Output H.264 + AAC, 1080x1920, 30fps. Verifies the output has video + audio and the duration is within tolerance. Confirm each ad lands in 25 to 45 seconds.

### 6.3 Verify the finished ads
After stitching, transcribe each variant (the whisper engine is already provisioned) and read back the recognized line order against that ad's approved transcript — proof the timeline plays hook → beats → CTA with nothing dropped, reordered, or garbled. This is the last check before delivery and it is free.

### 6.4 The easy-to-edit output package
```
<campagna>/05_UGC_Prompts/factory/<concept-slug>/
  inputs/            face image, body image, product image, voice clip, docs
  hook-bank.md       the Step 1 hooks
  beat-sheet.md      the Step 2 body (ends on CTA) + the 2 b-roll lines
  variants.md        the Step 3 four-ad table (unique hooks + b-roll ladder)
  render_plan.json   the batch contract (generations, images, voice cuts, lines)
  prompts/           one prompt file per generation
  voice_cuts/        one uniquely-fingerprinted voice WAV per generation
  gens/              the raw generations as rendered (uncut)
  clips/             the word-accurately CUT clips (4 hooks, body beats, 2 b-rolls)
  assembly-manifest.json
  out/               variant_v1.mp4 ... variant_v4.mp4  (each 25-45s, ending on the CTA)
```
The raw generations AND the cut clips are both kept on purpose: a re-roll drops back into `gens/` under the same name, a re-cut is just re-running whisper_cut.py, and a re-order is just re-running stitch.sh — the whole edit loop after rendering is free.
