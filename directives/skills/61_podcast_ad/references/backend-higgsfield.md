# Seedance 2.0 via the Higgsfield CLI — how to make it actually work

Hard-won facts. Build to these exactly; they are why generation is reliable here.

## Model + params
- Model id: **`seedance_2_0`** (verified on the CLI; NOT `seedance_2_pro`). `higgsfield model list` does NOT return any Seedance id, so do NOT verify it that way — confirm with a free cost call: `higgsfield generate cost seedance_2_0 --prompt cost-check --aspect_ratio 9:16 --resolution 1080p --duration 4`.
- `--aspect_ratio 9:16`, `--resolution 1080p`, `--duration <integer 4..9>` (UNDER 10s; never `auto`).
- Audio is automatic — there is **no `--generate_audio` flag** for Seedance; do not pass one.
- Media flags: attach `--image <host image>` and `--audio <unique voice cut>`. **Never `--video`.** Local paths are auto-uploaded by the CLI.
- Cost ≈ **9 credits/sec at 1080p** (≈4.5 at 720p). Billing is per second, so batching saves nothing per second — the leverage is parallel wall-clock and reusing the uploads.

## Submitting + the two CLI gotchas
1. **`generate create --wait` can falsely time out.** Renders sometimes take >5 minutes; a `--wait --wait-timeout 5m` returns an empty `[]` even though the job completes server-side. So either bump `--wait-timeout` to 20m, or — better for parallel — submit WITHOUT `--wait` and poll by job id.
2. **`generate create` WITHOUT `--wait` returns a JSON array of bare job-id STRINGS**, e.g. `["b3025b74-..."]` — parse `result[0]` as the id (it is NOT an object with an `.id` field). With `--wait` (or via `generate get`) you get the full job object.

## The robust parallel pattern (what `render_parallel.py` does)
1. Submit every generation WITHOUT `--wait`; capture each job id (`result[0]`). Submit a few at a time (≤8 concurrent — the workspace rate-limits) but do not block on each.
2. Poll each job id with `generate get <id> --json` until `status` is `completed` (grab `result_url`) or `failed`/`cancelled`. Renders take ~3–6 min; poll every ~20s, up to ~20 min.
3. Download each `result_url` with `curl -sSL`.
4. **Retry only failed ones** — a `failed` job (often the `_sfx` audio collision) costs nothing. Re-cut that generation's voice to a fresh fingerprint and resubmit.
5. Always check `params.medias[role=audio].data.url`: if it contains `_sfx`, that audio resolved to the poisoned variant — treat as failed and retry with a fresh cut.

## Recovering a "lost" job
If a `--wait` timed out (empty result) but the job actually finished, find it with `generate list --json` (sort by `created_at` desc) or `generate get <id>` and download its `result_url`. Confirm it's the right job by matching a distinctive word in `params.prompt`. **Downloading a completed job is free** (no new render).

## Auth / balance
- `higgsfield auth token` (exit 0 = logged in); else `higgsfield auth login` (device flow, surface the URL + code).
- `higgsfield account status` shows the credit balance — show it at the COST gate. Never charge credits without an explicit `go`.
