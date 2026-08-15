#!/usr/bin/env python3
"""
render_parallel.py - fire the whole approved batch of Seedance 2.0 generations in
PARALLEL via the Higgsfield CLI, IMAGE + VOICE-CUT ONLY (never a video reference).

ONLY run this AFTER an explicit human "go" for the batch (the COST gate lives in
SKILL.md; this script just executes). It:
  1. submits every generation WITHOUT --wait, capturing each job-id string,
  2. polls each job by id (renders can take >5 min; a --wait would falsely time out),
  3. downloads each completed result to gens/<gen_id>.mp4,
  4. retries any that FAILED or resolved to the poisoned _sfx audio variant, with a
     fresh unique voice cut (failed jobs cost nothing).

Each prompt is built from the locked template (match reference image, clone voice,
static camera, never-look-at-camera) + the generation's line(s). No --video, ever.

Usage: python3 render_parallel.py render_plan.json inputs_dir voice_cuts_dir gens_dir
"""
import glob, json, os, shutil, subprocess, sys, time

HB = os.path.expanduser("~/.local/bin/higgsfield")
if not os.path.exists(HB):
    HB = shutil.which("higgsfield") or HB

HEADER = (
    "Realistic candid podcast clip. Match the person and the setting exactly to the "
    "reference image — keep how they and the room look unchanged.\n\n"
    "VOICE: clone the voice, accent and tone from the attached voice reference; they "
    "speak only the scripted line(s) below in that voice (ignore the clip's words).\n\n"
    "STATIC locked camera — no move, pan, zoom or reframe; same fixed framing as the "
    "reference image.\n\n"
    "They NEVER look at the camera — gaze stays in the same direction they are already "
    "looking in the reference image (off toward their co-host), the whole time.\n\n"
    "Vertical 9:16. Subtle, natural emotion only.\n"
)


def build_prompt(lines):
    if len(lines) == 1:
        body = 'They say: "%s"\n' % lines[0]["line"]
    else:
        parts = []
        for j, ln in enumerate(lines):
            seg = 'Clip %d: "%s"' % (j + 1, ln["line"])
            if j < len(lines) - 1:
                seg += "\nHard cut."
            parts.append(seg)
        body = "\n".join(parts) + "\n"
    return HEADER + "\n" + body + "\nNo on-screen text or captions.\n"


def _resolve(inputs, rel):
    if not rel:
        return None
    if os.path.isabs(rel) and os.path.exists(rel):
        return rel
    cand = os.path.join(os.path.dirname(inputs.rstrip("/")), rel)
    if os.path.exists(cand):
        return cand
    b = os.path.join(inputs, os.path.basename(rel))
    return b if os.path.exists(b) else None


def host_image(plan, inputs, spk):
    img = _resolve(inputs, ((plan.get("hosts") or {}).get(spk) or {}).get("image"))
    if img:
        return img
    pool = [x for x in glob.glob(os.path.join(inputs, "*%s*" % spk))
            if x.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    return pool[0] if pool else None


def host_voice(plan, inputs, spk):
    v = _resolve(inputs, ((plan.get("hosts") or {}).get(spk) or {}).get("voice"))
    if v:
        return v
    pool = sum((glob.glob(os.path.join(inputs, "*" + e)) for e in (".mp3", ".wav", ".m4a")), [])
    return pool[0] if pool else None


def submit(prompt, image, audio, duration):
    r = subprocess.run([HB, "generate", "create", "seedance_2_0", "--prompt", prompt,
                        "--image", image, "--audio", audio, "--aspect_ratio", "9:16",
                        "--resolution", "1080p", "--duration", str(duration), "--json"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        if isinstance(d, list) and d and isinstance(d[0], str):  # no-wait => ["jobid"]
            return d[0]
        it = d[0] if isinstance(d, list) else d
        return it.get("id")
    except Exception:
        sys.stderr.write("submit error: %s\n" % (r.stderr or r.stdout)[:160])
        return None


def get(jid):
    r = subprocess.run([HB, "generate", "get", jid, "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        it = d[0] if isinstance(d, list) else d
        am = [m for m in (it.get("params", {}).get("medias") or []) if m.get("role") == "audio"]
        sfx = "_sfx" in (am[0]["data"]["url"] if am else "")
        return it.get("status"), it.get("result_url"), sfx
    except Exception:
        return "?", None, False


def recut(voicefile, outpath, salt):
    off = round(0.7 + salt * 0.9, 2)
    tempo = round(0.9 + salt * 0.045, 3)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(off), "-i", voicefile,
                    "-af", "atempo=%s,aresample=44100" % tempo, "-ar", "44100", "-ac", "1",
                    "-c:a", "pcm_s16le", outpath], capture_output=True)
    return outpath


def main():
    if len(sys.argv) < 5:
        sys.stderr.write("usage: render_parallel.py render_plan.json inputs voice_cuts gens\n")
        return 2
    plan_path, inputs, voice_cuts, gens_dir = sys.argv[1:5]
    os.makedirs(gens_dir, exist_ok=True)
    plan = json.load(open(plan_path, encoding="utf-8"))

    pending = {}
    for g in plan["generations"]:
        img = host_image(plan, inputs, g["speaker"])
        aud = os.path.join(voice_cuts, g["voice_cut"])
        if not img or not os.path.exists(aud):
            print("SKIP %s: missing image (%s) or voice cut (%s)" % (g["gen_id"], img, aud))
            continue
        jid = submit(build_prompt(g["lines"]), img, aud, g["duration"])
        print("submit %s -> %s" % (g["gen_id"], jid))
        if jid:
            pending[g["gen_id"]] = {"jid": jid, "gen": g, "img": img, "tries": 1}
        time.sleep(1)  # gentle stagger; stay under the workspace rate limit

    done = {}
    deadline = time.time() + 22 * 60
    while pending and time.time() < deadline:
        time.sleep(20)
        for gid in list(pending):
            st, url, sfx = get(pending[gid]["jid"])
            if st == "completed" and url and not sfx:
                out = os.path.join(gens_dir, gid + ".mp4")
                subprocess.run(["curl", "-sSL", url, "-o", out])
                print("DONE  %s -> %s" % (gid, out))
                done[gid] = out
                del pending[gid]
            elif st in ("failed", "cancelled") or (st == "completed" and sfx):
                ent = pending[gid]
                if ent["tries"] <= 2:
                    vf = host_voice(plan, inputs, ent["gen"]["speaker"])
                    aud = recut(vf, os.path.join(voice_cuts, ent["gen"]["voice_cut"]), ent["tries"])
                    jid = submit(build_prompt(ent["gen"]["lines"]), ent["img"], aud, ent["gen"]["duration"])
                    print("RETRY %s (was %s, sfx=%s) fresh voice -> %s" % (gid, st, sfx, jid))
                    pending[gid] = {"jid": jid, "gen": ent["gen"], "img": ent["img"], "tries": ent["tries"] + 1}
                else:
                    print("GIVE UP %s after %d tries" % (gid, ent["tries"]))
                    del pending[gid]

    if pending:
        print("STILL PENDING (timed out, recover via 'generate get'):", ", ".join(pending))
    print("\ncompleted %d/%d generations -> %s" % (len(done), len(plan["generations"]), gens_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
