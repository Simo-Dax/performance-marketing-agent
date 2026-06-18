# Consistency and assembly: one person, one voice, product-only b-rolls, four distinct timelines

How the skill keeps every CHARACTER clip looking like the same person, sounding like the same voice, keeps the B-ROLLS product-only, then cuts everything into 4 genuinely different ads that each end on the CTA. Obeys `references/VERIFIED-backend-facts.md` and `references/generation-architecture.md`; if a number conflicts, those win. No clone step, no voice-ID step, no TTS, no separate spine, no force-muting.

---

## 1. Character consistency

### 1.1 The locked images are the identity method
The member uploads ONE face image and ONE body image. Those exact files, the same bytes, are attached on EVERY CHARACTER generation (the hooks and the body shots). Do not re-crop, re-compress, or re-export them between generations. Pick the two images once, freeze them, reuse the identical files. Reference-video chaining is NOT the identity method.

The product image is attached on character shots where the product is on screen, and is the ONLY reference on the product-only b-rolls.

### 1.2 Prompts: keep it simple, do NOT over-describe the character
Every prompt opens with: **"A realistic, authentic UGC ad."** For character shots, add: **"Keep the character consistent with the reference images."** That is it for the person — do NOT write a wardrobe/hair/lighting descriptor block; the reference images carry the look, and over-describing fights them.

Then give DETAILED per-scene VISUAL direction: the environment, camera framing and movement, the action beat by beat, the lighting, and the exact spoken line. End with "no on-screen text or captions." For a multi-scene generation, describe each scene with a hard cut between them and set only the total seconds.

### 1.3 B-rolls are product-only (no character)
A b-roll shows ONLY the product — held by an anonymous hand or standing on a surface — with a slow push-in or pan, and a voiceover. It attaches the **product image + the voice clip ONLY**; NO face, NO body. Do not put the character in a b-roll.

### 1.4 Optional quick QC
After clips return, eyeball the first frame of each character clip against the locked images for face match and wardrobe, and confirm the b-rolls show only the product. Re-roll any single clip that drifted, in isolation, from the same locked bytes.

---

## 2. Voice consistency (the locked model)

### 2.1 The same voice clip is the reference on EVERY generation
The member uploads ONE voice clip, max 15 seconds. It is attached as the voice reference on every generation: hooks, body shots, AND the product-only b-rolls (as the voiceover). Seedance speaks each shot's new words in a voice that matches it. Same reference every time → consistent voice automatically.

### 2.2 Audio is ON for every generation
Audio stays on for every clip, b-rolls included (the b-roll is a voiceover over the product). No silent clip unless a beat is deliberately wordless. The only limit: the reference clip is max 15s.

### 2.3 What we never do
No clone step, no voice-ID step, no TTS, no externally authored spine, no force-muting at assembly. Each clip carries its own consistent voice; assembly just keeps it.

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
- Derive each generation's integer seconds at the fast pace: `round(words / 3.5)`, plus 1 to 2s of action time on HOOKS only. Every generation must be 4 to 9s (under 10).
- Each body beat is its own generation (segment beats one at a time so the packer never merges one beat's first sentence onto the previous clip).
- It prints a table (words, seconds, wps) and flags any generation at 10s+ or outside ~2.4 to 4.0 wps. The member confirms BEFORE any generation spends credits.

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
- character.product_image is always present (b-rolls are product-only).
- body.shots: the reusable body beats, each ending in order with the CTA beat last.
- variants[].ordered_timeline: the per-ad cut. role is hook, body, or broll. **The last entry must be the CTA body beat.** b-rolls appear only in the middle. trim_out null means play to the clip's end.
- distinctness_fingerprint: hash of render-affecting axes (visual_hook + sorted broll_set + b-roll count + placement indices + ordered roles), unique per ad, enforced by build_manifest.py — which also enforces ends-on-CTA and no-b-roll-after-CTA.

---

## 6. The ffmpeg assembly (scripts/build_manifest.py then scripts/stitch.sh)

### 6.1 build_manifest.py (the planner)
Inputs: the segmenter output (body.shots), the rendered body clips, the 4 split hook clips, the 2 product-only b-rolls, the locked references, and the variant definitions. It fills body.shots with each clip path and seconds, builds each ad's ordered_timeline (hook, body beats, b-rolls at the ad's chosen MIDDLE points, CTA last), computes total_seconds and the fingerprint, and enforces: unique fingerprints; every ordered_timeline ends on the CTA; no b-roll after the CTA; the b-roll-count ladder (0/1/2/2) with V3/V4 differing in placement. It refuses a voice_track field.

### 6.2 stitch.sh (the muxer)
Reads one ad's ordered_timeline, scales/pads each clip to 1080x1920 at 30fps, concatenates KEEPING each clip's audio (~80ms seam crossfade, never mutes), two-pass loudness-normalizes to -14 LUFS. Output H.264 + AAC, 1080x1920, 30fps. Verifies the output has video + audio and the duration is within tolerance. Confirm each ad lands in 25 to 45 seconds.

### 6.3 The easy-to-edit output package
```
<project>/ugc-factory/<concept>/
  inputs/            face image, body image, product image, voice clip, docs
  hook-bank.md       the Step 1 hooks
  beat-sheet.md      the Step 2 body (ends on CTA) + the 2 b-roll lines
  variants.md        the Step 3 four-ad table (unique hooks + b-roll ladder)
  clips/             every raw clip (body beats, 4 hooks, 2 product-only b-rolls)
  assembly-manifest.json
  out/               variant_v1.mp4 ... variant_v4.mp4  (each 25-45s, ending on the CTA)
```
The raw clips are kept on purpose so a re-roll drops back in under the same name and a re-cut is just re-running stitch.sh.
