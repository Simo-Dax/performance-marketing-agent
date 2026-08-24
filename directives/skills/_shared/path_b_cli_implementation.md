# Path B implementation, Higgsfield CLI

This reference is loaded by every Path B section in the generation skills (rebuild, multiplier, static, product-shot, character, and the UGC formats). The user-facing label in each skill is `Path B — Higgsfield CLI`. Path B runs through the official Higgsfield CLI (`@higgsfield/cli@^0.1` on npm), not the MCP server. The CLI authenticates with its own one-time device login in the user's browser; no MCP and no in-app OAuth is involved.

The CLI is the official Higgsfield CLI, MIT licensed, maintained by `*.@higgsfield.ai`. It exposes the same Higgsfield account, the same credits, and the same models as the MCP and the web UI.

---

## How each skill uses this file

Each skill's Path B section keeps its own:

1. Subset picker prompt (the skill knows how many prompts exist and what numbers are valid)
2. Output directory and filename pattern (e.g. `path_b_outputs/rebuild_<N>.png`)
3. Reference asset list (which local files to pass as `--image`)
4. Confirmation summary wording (skill-specific cost framing)
5. Manifest schema (per the skill's existing convention)

The skill calls into the steps below for the generic CLI workflow. Variable names in `{{double-braces}}` are filled in by the calling skill before the command runs.

---

## Step B.0, Ensure the CLI is installed

Check for the binary:

```
command -v higgsfield 2>/dev/null || command -v ~/.local/bin/higgsfield 2>/dev/null
```

If neither resolves, install with npm. Try the global install first, fall back to a user-prefix install if global is denied:

```
npm install -g @higgsfield/cli@^0.1 2>/dev/null || (mkdir -p ~/.local/lib/node_modules ~/.local/bin && npm config set prefix ~/.local && npm install -g @higgsfield/cli@^0.1)
```

After install, the binary is at one of:

- `/usr/local/bin/higgsfield` (global install on macOS or Linux)
- `~/.local/bin/higgsfield` (user-prefix fallback)
- `%APPDATA%\npm\higgsfield.cmd` (Windows global install, run via `where higgsfield`)

Resolve the working path once and reuse it:

```
HIGGS_BIN="$(command -v higgsfield 2>/dev/null || echo ~/.local/bin/higgsfield)"
```

Never run install with `sudo`. If npm denies global install without elevation, fall through to the user-prefix path.

If install fails entirely (no network, npm missing, Node missing), stop and tell the user:

> The Higgsfield CLI install failed. The CLI needs Node 20 or higher and npm reachable. Run `node --version` and `npm --version` to verify, then rerun this skill and pick Path B again. If you do not have Node installed, install it first.

---

## Step B.1, Ensure authentication

Check the auth state silently:

```
"$HIGGS_BIN" auth token >/dev/null 2>&1
```

If exit code is 0, the user is authenticated. Continue.

If exit code is non-zero, run device-flow login. The CLI prints a URL plus a one-time code, the user clicks Authorize in the browser, the CLI blocks until the browser flow completes. Run it in the background so Claude can surface the URL without holding the terminal:

```
"$HIGGS_BIN" auth login > /tmp/higgs-auth-$$.log 2>&1 &
LOGIN_PID=$!
```

Then poll the log file for the device URL and surface it to the user exactly as the CLI emits it:

> Open this URL in your browser and click Authorize:
>
> `<URL from /tmp/higgs-auth-*.log>`
>
> Code: `<code from log>`
>
> Reply `done` when the browser shows success.

Wait up to 5 minutes (300 s) for the background `auth login` to exit. If it exits with code 0, auth succeeded. If it times out or fails, kill the process and surface the error:

> Higgsfield login did not complete. Try again, or run `~/.local/bin/higgsfield auth login` in a separate terminal and re-run this skill.

Stop on failure. Do not retry silently.

---

## Step B.2, Workspace selection (if multiple)

If the user's Higgsfield account has more than one workspace, the CLI's `account status` may return ambiguous credit data until a workspace is set. Check:

```
"$HIGGS_BIN" workspace list --json
```

If the list contains more than one entry, ask the user:

> You have multiple Higgsfield workspaces: `<comma separated names>`. Which one should I use for this run? Reply with the name.

Then set it:

```
"$HIGGS_BIN" workspace set "<workspace-name>"
```

If only one workspace is returned, skip this step silently.

---

## Step B.3, Check credit balance

Run:

```
"$HIGGS_BIN" account status
```

Show the output verbatim to the user. The standard fields include current credit total, plan tier, and the workspace name. Capture the credit total for the cost gate.

---

## Step B.4, Dry-run cost per generation

Before the batch, run a single cost query for the picked model and aspect. This returns the per-generation credit cost without spending anything:

```
"$HIGGS_BIN" generate cost "{{MODEL_ID}}" \
  --prompt "cost-check" \
  --aspect_ratio "{{ASPECT}}" \
  --quality "{{QUALITY}}" \
  --resolution "{{RESOLUTION}}"
```

Variables filled by the calling skill:

- `{{MODEL_ID}}`: the CLI model id (see the Model ID mapping section below)
- `{{ASPECT}}`: `1:1`, `9:16`, `4:5`, `16:9`, `3:4`, depending on the skill
- `{{QUALITY}}`: usually `high` for GPT Image 2, omitted for Nano Banana 2 (CLI silently ignores it)
- `{{RESOLUTION}}`: `4k` for GPT Image 2, `2k` for Nano Banana 2 (the CLI accepts both lowercase)

Capture the returned per-generation cost. Multiply by the number of prompts the user picked in the subset step to get the total.

Tested reference: GPT Image 2 at `4k`, `9:16`, `quality=high`, with two `--image` references = 12 credits per generation.

---

## Step B.5, Confirmation gate

The calling skill prints its own confirmation summary, filling in real values from B.3 and B.4. Standard shape:

> About to generate `K` images via Higgsfield CLI using prompt numbers `<list>`.
> Per-generation cost: `<credits from B.4>` credits.
> Total: `<K times per-generation>` credits.
> Current balance: `<credits from B.3>`.
> Confirm `yes` to proceed.

Wait for explicit `yes` (case-insensitive). Any other response cancels the run. Acknowledge the cancellation and stop.

---

## Step B.6, Reference assets

The CLI auto-uploads local file paths passed via `--image`. There is no separate upload-and-confirm step. Collect the local file paths from the skill's intake (the user already provided them earlier), validate they exist on disk, and pass each one with a `--image` flag in the generate command.

Order matters for some models. As a general rule, pass references in the order the prompt expects them:

- Rebuild: competitor ad image first, user product image second
- Multiplier: winning ad image first, then 1 to 3 product images
- Static: product image only (optional)
- Product-shot: product image first, character `fullbody.png` second when applicable
- Character (headshot): no references (text-to-image)
- Character (full body): the headshot URL captured from the headshot generation
- UGC-prompt: character first if `$CHARACTER_REF` is set, then product, then voice clip

If a reference file is missing or unreadable, stop the run and report the path that failed. Do not silently skip.

---

## Step B.7, Generate each prompt

Write each prompt to a temp file first. Multi-paragraph prompts via shell args choke on quoting, especially when they include double quotes for dialogue:

```
PROMPT_FILE="/tmp/{{SKILL_SLUG}}-prompt-{{N}}-$$.txt"
cat > "$PROMPT_FILE" <<'PROMPT_EOF'
<the full prompt text, verbatim>
PROMPT_EOF
```

Then run the generate command:

```
"$HIGGS_BIN" generate create "{{MODEL_ID}}" \
  --prompt "$(cat "$PROMPT_FILE")" \
  --aspect_ratio "{{ASPECT}}" \
  --quality "{{QUALITY}}" \
  --resolution "{{RESOLUTION}}" \
  --image "<ref1_path>" \
  --image "<ref2_path>" \
  --wait \
  --wait-timeout 5m \
  --json \
  > "/tmp/{{SKILL_SLUG}}-result-{{N}}-$$.json" 2>&1
```

Notes:

- `--wait` blocks until the job completes. No separate polling step.
- `--wait-timeout 5m` is the upper bound. GPT Image 2 at 4K typically completes in 30 to 90 seconds.
- `--json` returns a JSON array with one entry per generated image. Required for parsing.
- Repeat `--image` once per reference. Omit if no references.
- For Nano Banana 2 the `--quality` flag is silently ignored by the CLI. Pass it anyway for consistency.
- For Seedance 2.0, the CLI accepts the same `generate create` interface. Pass `--duration "<n>"` as an integer. **Audio is automatic, there is NO `--generate_audio` flag for Seedance 2.0, do NOT pass it** (Seedance produces the audio on its own). The reference media flags are `--video`, `--image`, `--start-image`, `--end-image`, `--audio`. Verify the exact flag names against `higgsfield generate create --help` if unsure.

### Parallel batches for 5 or more jobs

For batches of 5 or more, run each generate command in the background to parallelize. Tested: 5 GPT Image 2 generations at 4K complete in roughly 90 seconds wall-clock when run in parallel, versus 5 minutes sequential.

Launch each generate command as a background shell process (`&`), capture each PID, and `wait` for all of them before the parse step. Do not exceed 8 parallel generations at once — Higgsfield rate-limits the API at the workspace tier.

For batches of 1 to 4, sequential is fine. Each generation costs the same regardless of order.

---

## Step B.8, Parse result and download

The `--json` output is a JSON array. Parse with `jq` if available, otherwise fall back to Python:

```
RESULT_FILE="/tmp/{{SKILL_SLUG}}-result-{{N}}-$$.json"

if command -v jq >/dev/null 2>&1; then
  JOB_ID="$(jq -r '.[0].id // empty' "$RESULT_FILE")"
  JOB_STATUS="$(jq -r '.[0].status // empty' "$RESULT_FILE")"
  RESULT_URL="$(jq -r '.[0].result_url // empty' "$RESULT_FILE")"
else
  JOB_ID="$(python3 -c "import json,sys; d=json.load(open('$RESULT_FILE')); print(d[0].get('id',''))")"
  JOB_STATUS="$(python3 -c "import json,sys; d=json.load(open('$RESULT_FILE')); print(d[0].get('status',''))")"
  RESULT_URL="$(python3 -c "import json,sys; d=json.load(open('$RESULT_FILE')); print(d[0].get('result_url',''))")"
fi
```

Why `jq` plus a Python fallback: `jq` is not on every user's machine (especially fresh Windows or WSL installs). Python 3 is a hard prereq of this agent, so the fallback is always available. Regex on JSON in shell breaks on the keys-quoted format the CLI emits — do not try to grep or sed the URL out.

If `JOB_STATUS` is anything other than `completed`, surface the error verbatim and continue with the remaining jobs in the batch. The CLI emits `failed`, `cancelled`, or `timeout` along with a human-readable reason.

Download the result image with curl:

```
curl -sSL "$RESULT_URL" -o "{{OUTPUT_DIR}}/{{OUTPUT_FILENAME}}"
```

Verify the download landed by checking the file size is over 50000 bytes (real generated images are several hundred KB minimum). If the file is smaller, the URL likely returned an error page rather than the image. Retry once, then report failure for that specific prompt and continue with the rest.

---

## Step B.9, Manifest

After the batch finishes (every requested prompt has either completed or failed), write a manifest at `{{OUTPUT_DIR}}/manifest.json`. Required fields:

```json
{
  "generated_via": "higgsfield-cli",
  "cli_version": "<from `higgsfield --version`>",
  "model_id": "{{MODEL_ID}}",
  "model_label": "<gpt-image-2 or nano-banana-2 or seedance-2.0>",
  "workspace": "<from B.2 if applicable>",
  "total_credits_spent": <integer, balance delta between B.3 and a fresh `account status` call after the batch>,
  "items": [
    {
      "prompt_number": <integer>,
      "prompt_text": "<verbatim prompt text>",
      "job_id": "<from B.8>",
      "status": "completed | failed | timeout",
      "output_path": "<absolute path or empty on failure>",
      "credits": <integer per-generation cost>,
      "failure_reason": "<verbatim error if failed, empty if completed>"
    }
  ]
}
```

The top-level `generated_via: "higgsfield-cli"` marks the output as Path B (CLI) for downstream tooling. The older `generated_via: "higgsfield-mcp"` value is no longer emitted; tooling that reads either value should treat both as Path B output.

---

## Model ID mapping

The Higgsfield CLI uses different model IDs than the MCP did. Mapping:

| Skill label       | MCP id (legacy)       | CLI id              | Notes |
|-------------------|-----------------------|---------------------|-------|
| GPT Image 2       | `gpt-image-2`         | `gpt_image_2`       | Default for all image skills. |
| Nano Banana 2     | `nano-banana-2`       | `nano_banana_flash` | Cheaper alternative. |
| Seedance 2.0      | `seedance-2`          | `seedance_2_0`      | Video (Clay Ad factory and the other Seedance 2.0 skills). VERIFIED id on CLI v0.1.40. `higgsfield model list` does NOT return any Seedance id, so do NOT verify it via model list, confirm with a cost call instead (`higgsfield generate cost seedance_2_0 --aspect_ratio 9:16 --resolution 1080p --duration 4`). |
| Seedance 2.0 Fast | `seedance-2-fast`     | `seedance_2_lite`   | Cheaper video variant. Same verification rule. |
| Seedance 2.5      | `seedance-2-5`        | `seedance_2_5`      | Video, ONE render up to 30s. VERIFIED id, schema and cost on the CLI 2026-08-18. Resolutions 480p/720p/1080p, aspect ratios include 9:16, `generate_audio` defaults true. Cost at 1080p is linear, 9 credits per second, so a 30s ad is 270 credits in a single render. Reference images require `mode omni_reference`, see the note below. |

If the calling skill captured `$MODEL` as `gpt-image-2`, substitute `gpt_image_2` for `{{MODEL_ID}}`. If `nano-banana-2`, substitute `nano_banana_flash`. For video (Seedance 2.0), substitute **`seedance_2_0`**, the verified Seedance 2.0 id, NOT `seedance_2_pro`.

To get the live list of available model ids at runtime, run:

```
"$HIGGS_BIN" model list --json | jq -r '.[].id'
```

If the picked id is not in the list, fall back to a fuzzy match (`grep -i gpt_image`, `grep -i nano_banana`) and use the closest match. Surface the chosen id to the user so they can override if the catalog has changed.

**Seedance caveat:** `model list` does NOT return any Seedance id (the `grep -i seedance` fallback finds nothing), so do NOT verify Seedance this way. The Seedance 2.0 id is **`seedance_2_0`**, confirm it directly with a cost call, `"$HIGGS_BIN" generate cost seedance_2_0 --aspect_ratio 9:16 --resolution 1080p --duration 4`, which returns the per-generation credit cost without spending.

**Seedance 2.5 attaches references differently from 2.0, and this is the one that bites.** On 2.0, `mode` is a QUALITY tier (`std` or `fast`) and reference images are accepted directly. On 2.5, `mode` is an INPUT mode (`t2v`, `omni_reference`, `video_edit`, `video_extension`) and the default `t2v` refuses reference media outright. Any skill that attaches an anchor still MUST pass `--mode omni_reference` or the render fails validation before it starts. Verified from `"$HIGGS_BIN" model get seedance_2_5` on 2026-08-18:

- `mode t2v` does not accept reference media at all
- `mode omni_reference` requires at least one reference item, and is the only mode that allows `start_image` and `end_image`
- at most 30 images, and at most 50 reference items in total
- `duration` is capped at 30; a request for 31 or more is rejected with `duration: Input should be less than or equal to 30`
- `resolution` is `480p`, `720p` or `1080p`; there is no 4k on this tier, unlike 2.0
- cost measured at 1080p 9:16: 45 credits at 5s, 135 at 15s, 270 at 30s, so 9 credits per second

Use `"$HIGGS_BIN" model get <id>` to read any model's live parameter schema and constraints; it costs nothing and it is the authoritative answer when this table and the CLI disagree.

---

## Output size to aspect ratio mapping

The CLI returns images at the model's native resolution for the picked aspect, not the `image_size` width and height that the fal.ai MCP accepts. Observed sizes for GPT Image 2 at 4K:

- `1:1` returns 2880 by 2880
- `9:16` returns 2160 by 3840
- `4:5` returns 2560 by 3200
- `16:9` returns 3840 by 2160
- `3:4` returns 2400 by 3200

These are the same dimensions the fal.ai Path C wiring requests, so downstream tooling (Meta uploaders, landing-page asset slots) treats Path B and Path C output as interchangeable.

For Nano Banana 2 at 2K the returned dimensions are roughly half of the GPT Image 2 4K sizes for the same aspect.

---

## Cross-platform notes

- **macOS / Linux**: the default install path is `/usr/local/bin/higgsfield`. User-prefix fallback lands at `~/.local/bin/higgsfield`. Both are detectable via `command -v higgsfield`.
- **Windows**: `npm install -g @higgsfield/cli@^0.1` installs to `%APPDATA%\npm\higgsfield.cmd`. The `command -v` check works under Git Bash and WSL. Under PowerShell, use `Get-Command higgsfield`. The user-prefix fallback uses `%APPDATA%\npm-userconfig` rather than `~/.local`, set via `npm config set prefix "$env:APPDATA\npm-userconfig"`.
- **WSL on Windows**: install at the WSL Linux side (Ubuntu / Debian). Do not call out to a Windows-side install from inside WSL, the file paths do not translate.

If the install path detection fails on Windows, fall back to running `where higgsfield` (cmd) or `Get-Command higgsfield | Select-Object -ExpandProperty Source` (PowerShell) and use that path explicitly.

---

## Hard rules across every skill that loads this reference

1. **Never auto-generate.** Every batch requires an explicit `yes` from the user after the B.5 confirmation summary.
2. **Always show the credit balance in B.3 and the per-generation cost in B.4** before the confirmation gate. The user must see real numbers, not estimates.
3. **Never charge Higgsfield credits without explicit `yes`.** Even a single test run.
4. **Save every output to disk** under the calling skill's `{{OUTPUT_DIR}}` (e.g. `path_b_outputs/`). The manifest is mandatory.
5. **Never silently switch paths.** If the CLI returns an error, ask whether to retry, switch to Path A (manual), or abandon. Do not auto-fall-back to Path C.
6. **The user-facing label is `Path B — Higgsfield CLI`.** The runtime IS the official Higgsfield CLI; menus and user-facing messages name it accurately (renamed from the legacy 'Higgsfield MCP' label in v2.25.0).

---

## Smoke test

A one-off smoke test script lives at `scripts/smoke-test-path-b.sh`. Run it after install or whenever the CLI version changes to confirm the binary is reachable, authentication is current, and the expected model IDs are in the catalog. The script exits 0 on success and prints which check failed otherwise.
