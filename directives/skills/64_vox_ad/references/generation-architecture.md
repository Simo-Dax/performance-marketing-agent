# VOX generation architecture — the single source of truth

One diagram in words. Everything else in this skill hangs off these six facts.

1. **The voice is the master.** The user's ElevenLabs voiceover is recorded once,
   aligned with faster-whisper, and never altered. Every plan number (clip spans, beat
   targets, the film length) is derived from the REAL recorded audio, not the script.

2. **The keyframe is the contract.** Each clip has exactly one approved 2K still — the
   finished poster for that beat. The video model's job is to ASSEMBLE it: the clip
   starts on an empty background and its final frame must match the keyframe exactly.
   The keyframe is attached as an IMAGE REFERENCE. It is never a start image (that opens
   the clip on the finished poster), and no video is ever attached as a reference.

3. **Consistency is the style block, not a character.** A byte-identical collage style
   block plus a Brand-DNA-locked palette in every keyframe prompt is what makes five
   separately generated posters read as one ad. There is no recurring hero to anchor.

4. **Anchored pixels are never generated twice.** Real logos, the real product photo,
   and the brand logo ride as image references with a reproduce-exactly clause. The hero
   frame (product or glowing logo) is the only luminous thing in the film.

5. **Timing is measured, then manufactured.** Seedance obeys ORDER faithfully and
   compresses the BACK HALF of most clips (measured drift 0.5–1.3s early; occasionally a
   late element or a dead hold). So: prompts carry target timestamps, the sync step
   measures every element's true arrival frame-by-frame, and ONE ffmpeg filter graph
   retimes footage (stretch / compress / cut dead holds) until every element lands
   within 0.25s of its word. Clip foley is retimed with the inverse atempo so impacts
   stay on their objects. Re-rendering is never a timing tool.

6. **Assembly is one filter graph.** trim+setpts segments → concat → sfx at ~0.11 gain →
   untouched VO on top → loudnorm -16 LUFS → 24fps CFR. Concat demuxers and `-ss` before
   `-i` corrupt retimed timestamps; they are banned.

Order of operations: script → GATE 1 → voice in → align → beat map + waste table →
GATE 2 → keyframes (all approved) → clip 1 checkpoint → parallel wave → measure →
retime → verify (offset table) → deliver.
