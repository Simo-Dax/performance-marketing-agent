# RENDER LAWS — the UGC Studio constitution

Every constraint in this file was verified in production tests (2026-07-10): the
render-feasibility audit of all four scene banks, live green-screen keying and
matting experiments on real renders, and the measured cut-structure teardown of the
four banked winners. SKILL.md enforces these laws; the scene banks defer to them.
When a bank and this file disagree, THIS FILE WINS.

---

## 1. The three lanes

Every pixel on a finished timeline comes from exactly ONE of:

1. **Video generations** — the creator, actions, settings. Seedance 2.0 only,
   1080p 9:16 for photoreal faces.
2. **Still-inserts** — 2K stills generated FROM the member's real photos (labels,
   variant runs, box stacks, open/eaten states, before-states, product-touches-lens
   beats), member-approved, then animated image-to-video with a MOTION-ONLY prompt,
   or cut in as stills. First-class, cheap, and the standard route for every
   fidelity-critical beat.
3. **Real-footage inserts** — the member's own recordings (screen recordings above
   all) conformed and cut in. Moving UI is NEVER generated.

---

## 2. Generation laws

- **Integer 4–9 seconds per generation, always.** 10s+ single generations produce
  very bad output (owner-verified). Longer content = more generations. Never "auto".
- **The sizing law:** seconds = round-to-NEAREST of words/wps (never blanket-ceil).
  A beat whose speech runs under ~3.5s never renders solo — it MERGES with a
  neighbor as hard-cut sub-shots (the hook always merges forward; the final close
  beat may stand alone at the 4s floor). The word-accurate cut removes floor slack
  afterwards.
- **2–3 hard-cut sub-shots per generation maximum;** one clear action per shot.
  Start shots in the END state (cap already off, box already open) — mid-shot state
  changes morph.
- **Macro bans:** fingernails, eyes/lash line, teeth, fine print — NEVER render;
  route to still-inserts or reframe. **Product manipulation ladder:** hold < rotate
  < open/close < pour < bite/apply — the top rungs need their own real-photo state
  or a still-insert.
- **One product reference per generation.** Every shown variant needs its own real
  photo; label fidelity comes only from attached real photos; real sizes stated
  inline in the prompt.
- **In-generation timing is unreliable:** word-action locks are EDIT-side
  guarantees at cut points on the whisper word timeline, never render promises.
  Performance micro-beats tied to words are re-render exposure — direct FEELINGS
  instead (one emotion word per prompt).
- **No set-lock exists:** recurring sets drift between generations. Pose-rhyme
  comparisons pack before+after as sub-shots of ONE generation; a second outfit
  requires a second body reference; mirrors stay out of frame; single-set formats
  vary framing per cut.
- **Scene ladder:** no two ADJACENT clips share setting + framing — UNLESS the join
  is a deliberate JUMP CUT with a visible state change (prop up vs lowered, cap
  off, sunglasses off, closer/wider crop). The ban is the cut where NOTHING
  visibly changes.
- **Witnesses:** from-behind/silhouette only; never two distinct identities in one
  generation.
- **The identity checkpoint** generation renders ALONE first and must contain a
  clean, bare, unobstructed face frame (no sunglasses-only or hands-over-face
  checkpoints; hands-only formats add one face-visible render or knowingly skip to
  a hands checkpoint).
- **No burned text ever:** no captions, no labels, no banners rendered or overlaid.
  Captions ship as a `captions.txt` sidecar.

---

## 3. THE EDIT GRAMMAR (why finished ads cut every 1–3s while gens are 4–9s)

Measured from the four banked winners: they cut every 1.1–3.2 seconds (narrative
median 1.13s across 25 shots; before/after 0.95s; unboxing 1.4s; testimonial
2.6–3.2s) and the longest take ANY winner holds is 4.2–7.4s. **A generation is
NEVER a timeline shot. It is RAW FOOTAGE the edit slices into 2–4 shots.** Dropping
gens in whole yields a 5–7s median — a half to a fifth of winner cut density,
instantly readable as AI.

- **TWO RAILS.** The EDL carries a separate audio rail and video rail. Audio rail:
  the beats' own clip audio joined at line boundaries per the voice laws — lip-sync
  integrity untouched. Video rail: shot-level cuts on the whisper word timeline,
  free to leave the host clip's picture mid-sentence and mid-word while the host
  audio runs uninterrupted underneath.
- **THE PUNCH-IN OVERLAY** (the winners' signature move): an insert — still flash,
  b-roll slice, macro sub-shot — OVERLAYS the host clip's picture for 0.6–1.5s
  starting at a word onset; the host's audio (and hidden lips) never stop; the
  return cut lands at a clause seam or mid-word. Zero audio surgery. Every approved
  still is a free pacing device.
- **CUTS LAND ON WORDS, NOT SENTENCES.** Line-boundary joins (the audio rail) hide
  in sentence-gap pauses trimmed to 0.15–0.45s; every OTHER visual cut is placed at
  a word onset from the word JSON — a word-action lock cuts ON the named word.
  Boundary-aligned cuts are reserved for world changes (the setting swap gets the
  period). Documented exception: the single-set take-jump testimonial cuts at
  trimmed breath pauses only — its density comes from take count.
- **SPINE-AND-RETURN, never gen1→gen2→gen3.** Every format has a home base the
  edit leaves and RETURNS to 2–5 times and ends on — on the creator's face for
  face formats, never an end card. One spine gen is sliced into multiple
  NON-ADJACENT timeline segments (different sub-ranges, no frame repeats),
  interleaved with inserts: spine→insert→spine→insert.
- **JUMP CUTS ARE LEGAL GLUE.** Same-setup take joins hide in trimmed pauses with
  matched energy and direction; interior dead-air trims inside one clip manufacture
  take-jumps for free; a 2x digital crop punch-in of the same gen is a legal new
  shot (medium → ECU → medium is one generation, three shots). Every jump changes
  a visible state.
- **RHYTHM IS SHAPED, not uniform:** hook shot ~2s; the middle runs at the format's
  measured cut interval; insert suites run 3 quick shots at 0.6–1.2s, one per
  phrase; the payoff/close is HELD ~2x the median (the ONLY legal long holds:
  ~4.3s on-camera CTA, ~6s silent display loop, ~1.9s narrative button); a
  0.6–0.8s reaction tail after the final word ends the ad on a gesture, not a
  syllable. The narrative format ACCELERATES at THE TURN — cut density doubles
  when the product enters.
- **PER-FORMAT CUT TARGETS, QC-ENFORCED AT STITCH** (from each bank's RHYTHM CARD):
  median shot ≤1.5s narrative, ≤3.2s testimonial, ≤1.2s narrated before/after,
  ≤2.0s narrated unboxing; NO shot exceeds ~4s except the typed close/CTA and the
  silent display loop. Documented exception: silent two-take formats (unboxing
  reveal) — a held caption does the selling.
- **INSERTS ARE PACING DEVICES, not only fidelity fixes:** any stretch running >4s
  without a cut takes an insert flash or sub-shot; a ~1s still flash is on screen
  too briefly to expose stillness — the cheapest density there is.
- **SUB-SHOTS ARE VERIFIED, NEVER TRUSTED:** every downloaded gen is scene-detected
  and reconciled against its planned sub-shot map (`cut_report.json`); a missing or
  mistimed internal cut is rescued in the edit (slice, crop punch-in, overlay) —
  only wrong CONTENT justifies a proposed re-render.
- **CONSERVATION RULE:** when the 2–3 sub-shot ceiling forces a generation-table
  correction, displaced setups are RECOVERED as extra gens or still flashes —
  never silently deleted. A fill's shot count stays at the winner's measured setup
  count.

---

## 4. The green-screen / app lane (live-verified 2026-07-10)

- Moving UI never renders; it comes from the member's real screen recording.
- Three composite patterns: full-frame screen-recording b-roll under VO;
  green-screen talker (keyed and overlaid); PiP bubble (circular-mask overlay —
  the zero-risk default).
- **The green-screen gen prompt law:** chest-up talker, "bright saturated
  chroma-key green (#00FF00), studio green screen, evenly lit, no shadows on the
  background", subject two steps off the backdrop, locked camera, small gestures,
  NO props (props near the face render as AI slop — owner-verified), wardrobe
  checked non-green on the body ref FIRST.
- **THE GREEN GATE:** sample the first green-screen render's background color
  before the batch (`composite.sh sample-green`). Saturated chroma green → free
  local key: chromakey at ~0.10 on the SAMPLED color (never assumed) + despill +
  border garbage matte. Muted/grass green (what models actually drift to) → do NOT
  widen key radii — it deletes the person before the green (verified) → route to
  matting or PiP, or one re-roll with the saturation wording.
- **Matting is the primary removal route (live-tested):** upload → Higgsfield
  `remove_background` (`media_type: video`, model `video_background_remover`,
  ~1 min per 4s clip, 1 credit) → returns H.264 subject-on-pure-black → composite
  with a razor-tight black colorkey 0.04–0.06 + blend 0.03 (looser eats pupils) →
  ship-clean even on muted green. PER-PATH: Paths B/D — the connector tool (D may
  also drive the web UI's background remover); Path A — the manual web-UI
  equivalent; Path C (fal) — NO Higgsfield matting: the lane falls back to
  chromakey-fast-path or PiP, and the gate says so. Matting availability is
  PREFLIGHTED at Step 5 (connector visible + one balance call) BEFORE matting
  credits appear in the Gate 2 table.

---

## 5. Voice & audio laws

- ONE member voice clip ≤15s. On Higgsfield paths every generation carries its OWN
  uniquely fingerprinted cut (see voice-and-parallel.md — the `_sfx` dedup physics,
  fresh re-cut on every re-roll, Path C exempt).
- B-roll/insert beats are VOICEOVER, never a talking head; talking beats lip-sync.
- Assembly keeps each clip's own audio on the AUDIO RAIL (no re-voicing, no muting
  of talking beats), −14 LUFS two-pass. The VIDEO rail may depart from the audio's
  source clip per the edit grammar — punch-in overlays ride the host clip's
  continuing audio. B-roll/insert slices used as overlays are always MUTE.
- **The close is TYPED per format** — `cta` (testimonial offer close), `delight`
  or naked proof (before/after), `display-loop` (unboxing reveal), `button`
  (narrative). QC enforces "ends on the approved close beat", never a blanket
  literal CTA.
- **Music is editor-side, like captions** — the studio never lays a music bed; a
  silent or music-carried format ships clean picture (+ `captions.txt`). Optional:
  a member-supplied track may be conformed at stitch on request. Loudness:
  narrated ads normalize to −14 LUFS; silent/music-carried ads ship with SFX-only
  audio (or none) and SKIP loudnorm rather than boosting noise.

---

## 6. Prompt & hook laws (studio-owned)

**THE HOUSE PROMPT SHAPE** (every video generation):

> "A realistic, authentic UGC ad." + "Keep the character consistent with the
> reference images." (character shots) + ONE setting/framing line + ONE
> delivery-emotion word + the EXACT quote + product size inline when on screen +
> "No on-screen text or captions."

Less is more. No wardrobe/lighting blocks. Never a duration in prompt text. Multi
sub-shot gens carry timestamped hard-cut lines matching the plan's `sub_shots` map:
`[0-3s] ... HARD CUT [3-8s] ...`.

**THE HOOK-FAMILY EVIDENCE TABLE** (Motion 2026, 550k ads + practitioner data):

| Family | Winner rate | Slot rule |
|---|---|---|
| Offer/urgency-led | 9.29% | strong — lead candidate |
| Confession | 8.74% | strong |
| Demographic call-out | top practitioner performer | strong |
| Question / listicle / how-to | 5.2–5.5% | weak — at most ONE slot |
| Vague lifestyle opener | — | BANNED |

At least 2 of any hook set from the strong families; VOC verbatim anchors when
research exists.

---

## 7. Pacing laws

- Per-format wps defaults, measured from the banked winners: Narrative ~4.0,
  Testimonial ~3.7, Before & After ~4.0–4.3 narrated, Unboxing ~3.7; VO-only
  insert lines ~2.5. Measured-from-teardown wps overrides defaults when the brand
  has teardown data.
- The segmenter accepts per-format pace bands; the sprint formats' band tops at
  4.4 wps so bank-measured scripts do not trip false flags.
- Hook + action buffer: +1–2s on hook generations only, still ≤9s; the
  word-accurate cutter trims the slack.
