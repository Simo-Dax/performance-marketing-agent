#!/usr/bin/env python3
"""Build the finished VOX ad in ONE ffmpeg filter graph: retime, mix, loudnorm.

Usage: build_sync.py <sync-plan.json> <out.mp4>

sync-plan.json:
{ "clips": ["clips/clip_01.mp4", ...],        // indexed 0..n-1
  "vo": "audio/voiceover.mp3",
  "segments": [                                // film order
    {"src": 0, "start": 0.0,  "end": 1.708, "speed": 1.0},
    {"src": 0, "start": 1.708,"end": 2.458, "speed": 1.856},  // >1 stretches (slower)
    ...
  ],
  "sfx_gain": 0.11, "lufs": -16, "fps": 24 }

speed multiplies PTS: 1.856 stretches a 0.75s slice to 1.39s; 0.80 compresses. The
slice's own foley is retimed with the inverse atempo (chained when outside 0.5..2.0).
Assembly law: never a concat demuxer, never -ss before -i — this graph IS the assembly.
"""
import json, shlex, subprocess, sys

def atempo_chain(factor):
    # ffmpeg atempo accepts 0.5..2.0 per instance; chain to cover the rest.
    chain = []
    f = factor
    while f < 0.5 or f > 2.0:
        step = 0.5 if f < 0.5 else 2.0
        chain.append(f"atempo={step}")
        f /= step
    chain.append(f"atempo={f:.5f}")
    return ",".join(chain)

def main():
    if len(sys.argv) != 3:
        print("usage: build_sync.py <sync-plan.json> <out.mp4>", file=sys.stderr)
        sys.exit(2)
    plan = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    clips = plan["clips"]
    vo_idx = len(clips)
    fps = int(plan.get("fps", 24))
    sfx_gain = float(plan.get("sfx_gain", 0.11))
    lufs = float(plan.get("lufs", -16))

    f, labels = [], []
    for i, s in enumerate(plan["segments"]):
        src, a, b = int(s["src"]), float(s["start"]), float(s["end"])
        sp = float(s.get("speed", 1.0))
        if b <= a:
            print(f"segment {i}: end must be after start", file=sys.stderr)
            sys.exit(3)
        f.append(f"[{src}:v]trim=start={a}:end={b},setpts={sp}*(PTS-STARTPTS)[v{i}]")
        af = f",{atempo_chain(1.0 / sp)}" if abs(sp - 1.0) > 1e-6 else ""
        f.append(f"[{src}:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS{af},aresample=48000[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    n = len(plan["segments"])
    f.append("".join(labels) + f"concat=n={n}:v=1:a=1[vv][sfx]")
    f.append(f"[sfx]volume={sfx_gain}[sfxq]")
    f.append(f"[{vo_idx}:a]aresample=48000[vo]")
    f.append("[sfxq][vo]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mx]")
    f.append(f"[mx]loudnorm=I={lufs}:TP=-1.5:LRA=11[aout]")

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for c in clips:
        cmd += ["-i", c]
    cmd += ["-i", plan["vo"], "-filter_complex", ";".join(f),
            "-map", "[vv]", "-map", "[aout]", "-r", str(fps), "-fps_mode", "cfr",
            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", out]
    print("RUN:", " ".join(shlex.quote(x) for x in cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(r.returncode)
    probe = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v",
                            "-show_entries", "stream=nb_read_frames",
                            "-show_entries", "format=duration",
                            "-of", "default=nk=1:nw=1", out],
                           capture_output=True, text=True)
    print("built:", out, probe.stdout.replace("\n", " ").strip())

if __name__ == "__main__":
    main()
