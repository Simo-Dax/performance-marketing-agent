# PIPELINE CONTRACTS — the four JSON files every studio script reads and writes

One order flows through four typed JSON contracts. Every script's argv and every
schema key is defined HERE and nowhere else; SKILL.md and the scripts defer to this
file. All paths inside contracts resolve relative to the ad's work folder (`$WORK`)
unless absolute.

```
render_plan.json   Step 5   authored by the orchestrator; the PROCUREMENT contract
cut_report.json    Step 8   written by whisper_cut.py; the measured truth per clip
edl.json           Step 5 (draft = the Gate 2 CUT MAP) + Step 9 (final); the EDIT decisions
manifest.json      Step 9   written by build_manifest.py; the resolved ASSEMBLY contract
```

---

## 1. render_plan.json — the procurement contract (one per AD)

Authored at Step 5 from the approved transcript + the format's bank shells. Voice
cuts, validation, dispatch, stills, compositing, and cutting all read this one file.

```json
{
  "ad_id": "deodorant_testimonial_A",
  "format": "testimonial",
  "close_type": "cta",
  "resolution": "1080p",
  "aspect_ratio": "9:16",
  "backend": "higgsfield",
  "wps": 3.7,
  "inputs": {
    "face":    "inputs/face.png",
    "body":    "inputs/body.png",
    "body_outfit2": "inputs/body_gym.png",
    "product": "inputs/product.png",
    "product_variant_coconut": "inputs/variant_coconut.png",
    "voice":   "inputs/voice.mp3",
    "screen_recording": "footage/app_capture.mov"
  },
  "entries": [ ]
}
```

- `format`: `testimonial | before-after | unboxing | direct-to-camera`.
- `close_type`: `cta | delight | display-loop | button` — the typed close the
  manifest enforces as the final beat.
- `backend`: `higgsfield | fal`. `fal` relaxes the per-gen voice-cut law (no `_sfx`
  dedup there — see voice-and-parallel.md).
- `wps`: the format band's approved words-per-second used at segmentation.
- `inputs`: every key is a stable handle; entries reference handles, never raw paths.
  EVERY shown product variant gets its own handle + real photo. A second outfit gets
  its own body handle. HANDLE NAMING IS LOAD-BEARING: the validator classifies
  handles by prefix — `face*`, `body*`, `product*` (e.g. `body_outfit2`,
  `product_variant_coconut`). A close_type other than the format default requires
  the plan-level flag `"close_type_explicit": true`.

### entries[] — four kinds

Every entry has `"kind": "gen" | "still" | "footage" | "composite"`.

**kind: "gen"** — one Seedance 2.0 generation.

```json
{
  "kind": "gen",
  "gen_id": "spine_car_A",
  "beat_type": "talking",
  "role": "spine",
  "duration": 8,
  "voice_cut": "spine_car_A.wav",
  "images": ["face", "body", "product"],
  "prompt_file": "prompts/spine_car_A.txt",
  "lines": [
    {"line": "If I smell this on someone at the bar it is over.", "clip": "t01"},
    {"line": "This is the only deodorant I repurchase.", "clip": "t02", "tail": 0.6}
  ],
  "sub_shots": [
    {"t": 0.0, "shot": "medium, sunglasses on, product at chest"},
    {"t": 3.0, "shot": "same seat same framing, sunglasses OFF, product to lens"}
  ],
  "is_identity_checkpoint": true
}
```

- `beat_type`: `talking | character_broll | product_only | green_screen` — drives
  validate_payload.py's attachment rules. `talking` lip-syncs; the b-roll types are
  VOICEOVER (never a talking head); `green_screen` is a chest-up talker for the
  app/green lane.
- `role`: `spine | hook | body | insert | close | checkpoint` — informational for
  the EDL; `spine` gens are slice candidates for non-adjacent reuse. The segmenter
  seeds middle gens as `body` (its neutral default); the orchestrator refines them
  to `spine`/`insert` when authoring the full plan at Step 5. Only `close` is
  enforced (the typed close must be the final base clip's gen).
- `duration`: INTEGER 4..9. Never anything else.
- `voice_cut`: this generation's OWN uniquely-fingerprinted WAV (Higgsfield paths).
  Omit only when `backend` is `"fal"` or the gen is silent (no `lines`).
- `lines[]`: the approved words this gen speaks, in order. `clip` names the cut
  output `clips/<clip>.mp4`. Optional `tail` (seconds after the last word;
  default 0.20, closes get ~0.6).
- `sub_shots[]`: THE PLANNED SUB-SHOT MAP — machine-readable, 1–3 items, `t` =
  expected internal hard-cut offset in seconds (first item always t 0.0). The
  validator checks the prompt actually carries this markup; whisper_cut.py
  reconciles scene-detected cuts against it. Silent gens NEED this map (plan-cut
  mode cuts on it) and each sub-shot then carries a `"clip"` name (silent gens
  have no `lines[]` to name clips): `{"t": 0.0, "shot": "...", "clip": "y01"}`.
- `is_identity_checkpoint`: exactly ONE gen per ad sets this true; it renders alone
  first and must contain the clean bare face frame.

**kind: "still"** — one 2K still-insert built FROM a real photo, optionally animated
motion-only.

```json
{
  "kind": "still",
  "still_id": "label_macro_coconut",
  "source_photo": "product_variant_coconut",
  "prompt_file": "prompts/still_label_macro_coconut.txt",
  "animate": "slow 4% push-in",
  "duration": 2
}
```

- `source_photo`: handle into `inputs` — the real photo the still is generated from.
- `animate`: motion-only image-to-video prompt, or `null` → cut in as a static still
  (Ken-Burns applied at composite time). `duration` = seconds needed on the timeline
  (the EDL may use less).

**kind: "footage"** — the member's real recording conformed in.

```json
{ "kind": "footage", "footage_id": "app_scroll", "source": "screen_recording" }
```

**kind: "composite"** — a green-screen/app-lane build (composite.sh output).

```json
{
  "kind": "composite",
  "composite_id": "gs_talker_1",
  "gen_id": "gs_gen_1",
  "footage_id": "app_scroll",
  "pattern": "matting"
}
```

- `pattern`: `chromakey | matting | pip | fullframe` (the GREEN GATE picks between
  chromakey/matting/pip after sampling the first render; `fullframe` = screen
  recording full-frame under VO, no keying).
- `gen_id` / `footage_id` reference sibling entries.

---

## 2. cut_report.json — whisper_cut.py's output (measured truth)

Written into the clips dir. One object per cut clip plus per-gen reconciliation.

```json
{
  "clips": [
    {
      "clip": "t01",
      "gen_id": "spine_car_A",
      "src_start": 0.0, "src_end": 4.28, "duration": 4.28,
      "match_ratio": 0.92,
      "words": [ {"w": "If", "start": 0.31, "end": 0.44}, ... ],
      "internal_cuts": [3.02]
    }
  ],
  "gens": [
    {
      "gen_id": "spine_car_A",
      "planned_sub_shots": [0.0, 3.0],
      "detected_cuts": [3.02],
      "reconcile": "OK",
      "notes": ""
    }
  ]
}
```

- `words[]`: word timestamps RELATIVE TO THE CLIP — the EDL anchors overlays on
  these. Silent clips have `words: []`.
- `internal_cuts`: scene-detected hard cuts inside the clip (clip-relative).
- `gens[].reconcile`: `OK` (every planned sub-shot found within ±0.5s) |
  `MISSING <t>` (a planned cut never rendered — rescue edit-side) | `EXTRA <t>`
  (an unplanned cut — inspect the frame grid). NEVER auto-re-render on a reconcile
  miss; timing is fixed in the edit. Gens without a `sub_shots` map get
  `planned_sub_shots: []` and reconcile `OK` unless detected cuts exist (then
  EXTRA, informational). Plan defects (a silent gen missing its map or clip names)
  do not abort the run: the report is still written for what was measured and the
  script exits 3.

---

## 3. edl.json — the edit decisions (one per AD)

Drafted at Step 5 (this IS the Gate 2 CUT MAP the member approves) and finalized at
Step 9 once real clip durations exist. Two rails.

```json
{
  "ad_id": "deodorant_testimonial_A",
  "format": "testimonial",
  "close_type": "cta",
  "base": [
    {"clip": "t01"},
    {"clip": "t02", "trim": [{"cut_dead_air_at": 2.1, "resume": 2.9}]},
    {"clip": "t03"}
  ],
  "overlays": [
    {
      "insert": "stills/label_macro_coconut.mp4",
      "anchor": {"clip": "t02", "word": "coconut", "occurrence": 1, "offset": 0.05},
      "duration": 1.0,
      "insert_in": 0.0
    },
    {
      "insert": "clips/broll_pour.mp4",
      "anchor": {"clip": "t03", "time": 1.4},
      "duration": 1.2,
      "insert_in": 0.6
    }
  ],
  "rhythm_targets": { "median_max": 3.2, "shot_max": 4.0, "close_exempt": true }
}
```

- `base[]` — THE AUDIO RAIL: ordered clips whose own audio + video form the spine of
  the timeline. Joins land at line boundaries (breath pauses). The same source gen
  may appear as multiple non-adjacent clips (spine slicing) but a `clip` id appears
  at most once. Optional `trim[]` = interior dead-air cuts (jump-cut manufacture) —
  both audio and video are cut there, legal at pauses only.
- `overlays[]` — THE VIDEO RAIL's punch-ins: `insert` video replaces the base
  PICTURE for `duration` seconds while base AUDIO continues. `anchor` targets a
  base clip either by `word` (+ `occurrence`, resolved against cut_report words,
  `offset` seconds after word onset) or by clip-relative `time`. `insert_in` = where
  in the insert file to start. Overlays must not cross a base-clip join, must not
  overlap each other, and must not cover the final close beat.
- `rhythm_targets`: from the format's bank RHYTHM CARD; stitch.sh QC enforces them.

---

## 4. manifest.json — build_manifest.py's output (resolved assembly)

All TIMES are absolute timeline seconds; file paths stay $WORK-relative (stitch.sh
resolves them against the manifest's directory). stitch.sh executes it verbatim,
no lookups.

```json
{
  "ad_id": "deodorant_testimonial_A",
  "close_type": "cta",
  "base": [
    {"file": "clips/t01.mp4", "duration": 4.28, "trims": []},
    {"file": "clips/t02.mp4", "duration": 5.10, "trims": [[2.1, 2.9]]}
  ],
  "overlays": [
    {"file": "stills/label_macro_coconut.mp4", "at": 6.93, "duration": 1.0, "insert_in": 0.0}
  ],
  "cut_points": [4.28, 6.93, 7.93, ...],
  "rhythm": {
    "targets": {"median_max": 3.2, "shot_max": 4.0, "close_exempt": true},
    "shots": [4.28, 2.65, 1.0, ...],
    "median": 2.65, "max_non_close": 3.9, "verdict": "PASS"
  },
  "audio": { "loudnorm": true, "target_lufs": -14 },
  "expected_total": 30.4
}
```

- `overlays[].at` is ABSOLUTE timeline seconds (build_manifest resolves word anchors
  via cut_report and sums prior base durations minus trims).
- `cut_points` / `rhythm.shots`: the deterministic cut list = base joins + interior
  trims + overlay in/out + reconciled internal cuts. Shot lengths derive from IT,
  not from scene detection. `verdict` must be PASS before stitch runs (stitch
  re-checks and refuses on FAIL). A rhythm FAIL still writes the manifest (verdict
  recorded, exit 0 — the refusal lives in stitch); STRUCTURAL failures (unresolvable
  anchor, overlay crossing a join or covering the close, wrong typed close, missing
  files) write nothing and exit 1.
- Silent ads set `"audio": {"loudnorm": false}` (SFX-only or none; never boost noise).
- build_manifest REFUSES to write a manifest whose final base clip does not trace
  to a render_plan entry with `role: "close"` (the typed close), or whose overlays
  violate the overlay rules above.

---

## 5. Script argv (canonical — SKILL.md copies these exactly)

```
python3 $SCRIPTS/segment_script.py   transcript.txt --format testimonial [--wps 3.7] --out render_plan.skeleton.json
python3 $SCRIPTS/validate_payload.py render_plan.json                      # whole plan, all kinds
python3 $SCRIPTS/make_voice_cuts.py  render_plan.json $WORK voice_cuts/
python3 $SCRIPTS/render_stills.py    render_plan.json $WORK stills/
python3 $SCRIPTS/render_parallel.py  render_plan.json $WORK voice_cuts/ gens/ [gen_id ...]
python3 $SCRIPTS/whisper_cut.py      render_plan.json gens/ clips/ [--lead 0.08] [--tail 0.20]
bash    $SCRIPTS/frame_check.sh      gens/ frames/
bash    $SCRIPTS/composite.sh        sample-green  gens/<id>.mp4
bash    $SCRIPTS/composite.sh        chromakey     gens/<id>.mp4 footage/<bg>.mp4 out.mp4 [0xRRGGBB] [0.10]
bash    $SCRIPTS/composite.sh        matting-key   matted.mp4    footage/<bg>.mp4 out.mp4
bash    $SCRIPTS/composite.sh        pip           gens/<id>.mp4 footage/<bg>.mp4 out.mp4
bash    $SCRIPTS/composite.sh        fullframe     footage/<src>.mov out.mp4
bash    $SCRIPTS/composite.sh        still         stills/<id>.png out.mp4 [seconds]
python3 $SCRIPTS/build_manifest.py   edl.json render_plan.json clips/cut_report.json --out manifest.json
bash    $SCRIPTS/stitch.sh           manifest.json out/<ad_id>.mp4
```

`$SCRIPTS` resolves per SKILL.md Step 0 (upward search for `directives/skills/57_ugc_studio/scripts`). All scripts:
stdlib + ffmpeg/ffprobe only, except whisper_cut.py (faster-whisper,
self-bootstrapping venv at `~/.cache/pm-agent/whisper-venv`). Exit 0 = pass,
non-zero = a printed, actionable failure. No script ever calls another skill's
folder — this skill is standalone.
