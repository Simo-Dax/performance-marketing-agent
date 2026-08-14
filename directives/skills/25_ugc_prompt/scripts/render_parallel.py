#!/usr/bin/env python3
"""
render_parallel.py - fire an approved batch of Seedance 2.0 UGC generations in
PARALLEL via the Higgsfield CLI. Reference images + a UNIQUE voice cut per
generation, never a video reference.

ONLY run this AFTER an explicit human "go" for the batch (the COST gate lives in
SKILL.md; this script just executes). It:
  1. submits every generation WITHOUT --wait, capturing each job-id string
     (a --wait can falsely time out on >5 min renders),
  2. polls each job by id until completed/failed,
  3. downloads each completed result to gens/<gen_id>.mp4,
  4. retries any that FAILED or resolved to the poisoned _sfx audio variant,
     with a FRESH unique voice cut (failed jobs cost nothing).

Unlike the podcast variant, each UGC generation's prompt is authored per scene
by the orchestrator: the plan entry carries `prompt_file` (a text file under
$WORK) or an inline `prompt`. Attachments come from the entry's `images` list —
each item is a key into plan.inputs ("face", "body", "product") or a literal
path. The generation's `voice_cut` WAV rides as --audio.

Optionally render a subset (the hook-first checkpoint renders ONE generation):
  python3 render_parallel.py render_plan.json work_dir voice_cuts_dir gens_dir [gen_id ...]

With no gen_id arguments the whole plan renders.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HB = os.path.expanduser("~/.local/bin/higgsfield")
if not os.path.exists(HB):
    HB = shutil.which("higgsfield") or HB


def _dur(f):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "json", f], capture_output=True, text=True).stdout
        return float(json.loads(out)["format"]["duration"])
    except Exception:
        return 15.0


def _resolve(work, rel):
    if not rel:
        return None
    if os.path.isabs(rel) and os.path.exists(rel):
        return rel
    cand = os.path.join(work, rel)
    return cand if os.path.exists(cand) else None


def _prompt_of(work, g):
    if g.get("prompt"):
        return g["prompt"]
    pf = _resolve(work, g.get("prompt_file"))
    if pf:
        return open(pf, encoding="utf-8").read().strip()
    return None


def _images_of(plan, work, g):
    out = []
    inputs = plan.get("inputs") or {}
    for item in g.get("images") or []:
        p = _resolve(work, inputs.get(item)) or _resolve(work, item)
        if p:
            out.append(p)
        else:
            return None, item
    return out, None


def submit(prompt, images, audio, duration, resolution):
    cmd = [HB, "generate", "create", "seedance_2_0", "--prompt", prompt]
    for img in images:
        cmd += ["--image", img]
    cmd += ["--audio", audio, "--aspect_ratio", "9:16",
            "--resolution", resolution, "--duration", str(duration), "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        if isinstance(d, list) and d and isinstance(d[0], str):  # no-wait => ["jobid"]
            return d[0]
        it = d[0] if isinstance(d, list) else d
        return it.get("id")
    except Exception:
        sys.stderr.write("submit error: %s\n" % (r.stderr or r.stdout)[:200])
        return None


def get(jid):
    r = subprocess.run([HB, "generate", "get", jid, "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        it = d[0] if isinstance(d, list) else d
    except Exception:
        return "?", None, False
    sfx = False
    try:
        am = [m for m in (it.get("params", {}).get("medias") or []) if m.get("role") == "audio"]
        url = ((am[0].get("data") or {}).get("url") or "") if am else ""
        sfx = "_sfx" in url
    except Exception:
        pass  # a malformed media entry must not discard a real completed status
    return it.get("status"), it.get("result_url"), sfx


def recut(voicefile, outpath, gid, tries):
    """A FRESH fingerprint for a retry: unique per (generation, attempt) batch-wide.

    The offset/tempo fold in the gen_id, so two different generations retried the
    same number of times never produce byte-identical cuts (which would collide on
    the _sfx dedup all over again). Returns outpath, or None if ffmpeg failed (the
    old poisoned cut must never be resubmitted).
    """
    vd = _dur(voicefile)
    h = int(hashlib.sha256(gid.encode("utf-8")).hexdigest()[:8], 16)
    span = max(0.1, vd - 3.5)
    off = round((((h % 97) / 97.0) * span + tries * 0.9) % span, 2) if vd > 4.5 else 0.0
    tempo = round(0.93 + (((h % 13) * 0.013 + tries * 0.045) % 0.16), 3)
    rc = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(off), "-i", voicefile,
                         "-af", "atempo=%s,aresample=44100" % tempo, "-ar", "44100", "-ac", "1",
                         "-c:a", "pcm_s16le", "-t", "14.5", outpath],
                        capture_output=True).returncode
    if rc != 0 or not os.path.exists(outpath) or os.path.getsize(outpath) < 1000:
        return None
    return outpath


def main():
    if len(sys.argv) < 5:
        sys.stderr.write("usage: render_parallel.py render_plan.json work_dir voice_cuts_dir gens_dir [gen_id ...]\n")
        return 2
    plan_path, work, voice_cuts, gens_dir = sys.argv[1:5]
    only = set(sys.argv[5:])
    os.makedirs(gens_dir, exist_ok=True)
    plan = json.load(open(plan_path, encoding="utf-8"))
    resolution = plan.get("resolution", "1080p")
    voice_src = _resolve(work, (plan.get("inputs") or {}).get("voice"))

    gens = [g for g in plan["generations"] if not only or g["gen_id"] in only]
    if only and len(gens) != len(only):
        missing = only - {g["gen_id"] for g in gens}
        sys.stderr.write("unknown gen_id(s): %s\n" % ", ".join(sorted(missing)))
        return 2

    pending = {}
    for g in gens:
        prompt = _prompt_of(work, g)
        images, bad = _images_of(plan, work, g)
        aud = os.path.join(voice_cuts, g.get("voice_cut") or (g["gen_id"] + ".wav"))
        if not prompt or images is None or not os.path.exists(aud):
            print("SKIP %s: missing %s" % (g["gen_id"],
                  "prompt" if not prompt else ("image '%s'" % bad if images is None else "voice cut")))
            continue
        jid = submit(prompt, images, aud, g["duration"], resolution)
        print("submit %s -> %s" % (g["gen_id"], jid))
        if jid:
            pending[g["gen_id"]] = {"jid": jid, "gen": g, "images": images, "aud": aud, "tries": 1}
        time.sleep(1)  # gentle stagger; stay under the workspace rate limit

    done = {}
    deadline = time.time() + 22 * 60
    while pending and time.time() < deadline:
        time.sleep(20)
        for gid in list(pending):
            st, url, sfx = get(pending[gid]["jid"])
            if st == "completed" and url and not sfx:
                out = os.path.join(gens_dir, gid + ".mp4")
                rc = subprocess.run(["curl", "-sSL", url, "-o", out]).returncode
                if rc != 0 or not os.path.exists(out) or os.path.getsize(out) < 10000:
                    print("DOWNLOAD FAIL %s (job %s completed; recover free via "
                          "'higgsfield generate get %s' and re-download)"
                          % (gid, pending[gid]["jid"], pending[gid]["jid"]))
                    del pending[gid]
                    continue
                print("DONE  %s -> %s" % (gid, out))
                done[gid] = out
                del pending[gid]
            elif st in ("failed", "cancelled") or (st == "completed" and sfx):
                ent = pending[gid]
                if ent["tries"] <= 2 and voice_src:
                    aud = recut(voice_src, ent["aud"], gid, ent["tries"])
                    prompt = _prompt_of(work, ent["gen"])
                    jid = submit(prompt, ent["images"], aud, ent["gen"]["duration"],
                                 resolution) if aud else None
                    if not jid:
                        print("GIVE UP %s (recut or resubmit failed after %s, sfx=%s)"
                              % (gid, st, sfx))
                        del pending[gid]
                        continue
                    print("RETRY %s (was %s, sfx=%s) fresh voice cut -> %s" % (gid, st, sfx, jid))
                    pending[gid] = {"jid": jid, "gen": ent["gen"], "images": ent["images"],
                                    "aud": aud, "tries": ent["tries"] + 1}
                else:
                    print("GIVE UP %s after %d tries" % (gid, ent["tries"]))
                    del pending[gid]

    if pending:
        print("STILL PENDING (timed out, recover via 'higgsfield generate get <id>'):",
              ", ".join("%s=%s" % (k, v["jid"]) for k, v in pending.items()))
    print("\ncompleted %d/%d generations -> %s" % (len(done), len(gens), gens_dir))
    return 0 if len(done) == len(gens) else 1


if __name__ == "__main__":
    sys.exit(main())
