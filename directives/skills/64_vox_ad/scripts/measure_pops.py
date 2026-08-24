#!/usr/bin/env python3
"""Measure each element's real arrival time in a clip (or the finished film).

Usage: measure_pops.py <video.mp4> <checks.json> <out arrivals.json>

checks.json: {"fps": 24, "checks": [
  {"name": "meta logo", "word": "Andromeda", "target": 3.10,
   "x0": 0.10, "y0": 0.26, "x1": 0.90, "y1": 0.55,
   "window_start": 2.0, "window_end": 4.6, "frac": 0.45}, ...]}

Coordinates are normalized (0..1) over the frame. Arrival = first frame inside the
window whose region mean-brightness crosses lo + (hi - lo) * frac. Also reports
frame-difference dead holds (flatlines >= 0.7s) for the sync plan.

Pillow self-bootstraps into the shared venv (same one align_vo.py uses); frames are
extracted with ffmpeg at a reduced 90x160 grayscale, so a 25s film measures in seconds.
Exit 0 always when measurement ran; the offsets are data, not a pass/fail.
"""
import json, os, shutil, subprocess, sys, tempfile

VENV = os.path.expanduser("~/.cache/pm-agent/whisper-venv")

def ensure_pillow():
    try:
        import PIL  # noqa: F401
        return
    except ImportError:
        pass
    py = os.path.join(VENV, "bin", "python")
    if os.path.exists(py) and "MEASURE_POPS_BOOTSTRAPPED" not in os.environ:
        subprocess.run([py, "-m", "pip", "install", "-q", "pillow"], check=False)
        env = dict(os.environ, MEASURE_POPS_BOOTSTRAPPED="1")
        os.execve(py, [py] + sys.argv, env)
    print("measure_pops: Pillow unavailable and no venv to bootstrap into", file=sys.stderr)
    sys.exit(2)

def main():
    if len(sys.argv) != 4:
        print("usage: measure_pops.py <video> <checks.json> <out.json>", file=sys.stderr)
        sys.exit(2)
    ensure_pillow()
    from PIL import Image, ImageChops, ImageStat
    video, checks_path, out_path = sys.argv[1:4]
    cfg = json.load(open(checks_path))
    fps = int(cfg.get("fps", 24))
    W, H = 90, 160
    tmp = tempfile.mkdtemp(prefix="vox-pops-")
    try:
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video,
                            "-vf", f"fps={fps},scale={W}:{H}", "-pix_fmt", "gray",
                            os.path.join(tmp, "%05d.png")], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            sys.exit(1)
        frames = sorted(os.listdir(tmp))
        imgs = [Image.open(os.path.join(tmp, f)).convert("L") for f in frames]
        n = len(imgs)

        results = []
        for c in cfg["checks"]:
            box = (int(c["x0"] * W), int(c["y0"] * H), int(c["x1"] * W), int(c["y1"] * H))
            a = int(float(c.get("window_start", 0)) * fps)
            b = min(n, int(float(c.get("window_end", n / fps)) * fps))
            vals = [ImageStat.Stat(im.crop(box)).mean[0] for im in imgs[a:b]]
            arrival = None
            if vals:
                lo, hi = min(vals), max(vals)
                if hi - lo >= 2.5:
                    thr = lo + (hi - lo) * float(c.get("frac", 0.45))
                    for i, v in enumerate(vals):
                        if v >= thr:
                            arrival = round((a + i) / fps, 2)
                            break
            target = c.get("target")
            off = round(arrival - target, 2) if (arrival is not None and target is not None) else None
            results.append({"name": c["name"], "word": c.get("word", ""),
                            "target": target, "actual": arrival, "off": off})

        holds, prev, flat_start = [], None, None
        for i, im in enumerate(imgs):
            if prev is not None:
                d = ImageStat.Stat(ImageChops.difference(im, prev)).mean[0]
                if d < 0.5:
                    if flat_start is None:
                        flat_start = i - 1
                else:
                    if flat_start is not None and (i - flat_start) >= int(0.7 * fps):
                        holds.append({"start": round(flat_start / fps, 2),
                                      "end": round(i / fps, 2)})
                    flat_start = None
            prev = im
        if flat_start is not None and (n - flat_start) >= int(0.7 * fps):
            holds.append({"start": round(flat_start / fps, 2), "end": round(n / fps, 2)})

        json.dump({"video": video, "frames": n, "fps": fps,
                   "results": results, "dead_holds": holds}, open(out_path, "w"), indent=2)
        print(f"{'element':22s} {'word':18s} {'target':>7s} {'actual':>7s} {'off':>7s}")
        for r_ in results:
            t = f"{r_['target']:.2f}" if r_["target"] is not None else "-"
            a_ = f"{r_['actual']:.2f}" if r_["actual"] is not None else "MISS"
            o = f"{r_['off']:+.2f}" if r_["off"] is not None else "-"
            print(f"{r_['name'][:22]:22s} {r_['word'][:18]:18s} {t:>7s} {a_:>7s} {o:>7s}")
        if holds:
            print("dead holds: " + ", ".join(f"{h['start']}-{h['end']}s" for h in holds))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
