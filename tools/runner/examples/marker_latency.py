"""TEST ONLY: marker-write latency on /home/users (NFS, sync export) with N concurrent writers.

Each writer owns one marker file and performs K events spaced by a random 0-1 s pause (like jobs that start and
finish), timing each event: method `append` (runner: O_APPEND + fsync) or `rewrite` (read, write .part, fsync,
rename). Writers are sleep-dominated (negligible CPU). Usage:
    python marker_latency.py --writers 12 --events 10 --method append --dir DIR --out result.json
"""
import argparse
import json
import os
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qv2run import markers  # noqa: E402
from qv2run.fsops import write_atomic  # noqa: E402


def rewrite(path, rec):
    lines = []
    try:
        lines = Path(path).read_text().splitlines()
    except FileNotFoundError:
        pass
    lines.append(json.dumps(rec))
    write_atomic(path, "\n".join(lines) + "\n")


def writer(path, events, method, seed):
    rnd = random.Random(seed)
    lat = []
    for i in range(events):
        time.sleep(rnd.uniform(0, 1))
        rec = {"job_id": Path(path).stem, "status": "started" if i % 2 == 0 else "done", "i": i,
               "outputs": [{"name": "x.dat", "sha256": "0" * 64, "bytes": 123}]}
        t0 = time.perf_counter()
        if method == "append":
            markers.append(path, rec)
        else:
            rewrite(path, rec)
        lat.append(time.perf_counter() - t0)
    return lat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--writers", type=int, default=12)
    ap.add_argument("--events", type=int, default=10)
    ap.add_argument("--method", choices=("append", "rewrite"), default="append")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--child", default=None)
    a = ap.parse_args()
    if a.child:
        lat = writer(a.child, a.events, a.method, hash(a.child) & 0xFFFF)
        sys.stdout.write(json.dumps(lat) + "\n")
        return 0
    d = Path(a.dir) / f"{a.method}-w{a.writers}"
    d.mkdir(parents=True, exist_ok=True)
    procs = [subprocess.Popen([sys.executable, __file__, "--events", str(a.events), "--method", a.method,
                               "--dir", a.dir, "--child", str(d / f"job{i:03d}.marker")], stdout=subprocess.PIPE,
                              text=True) for i in range(a.writers)]
    lat = []
    for p in procs:
        out, _ = p.communicate()
        lat += json.loads(out)
    lat.sort()
    q = lambda f: round(lat[min(len(lat) - 1, int(f * len(lat)))] * 1000, 1)  # noqa: E731
    res = {"host": os.uname().nodename, "writers": a.writers, "events_per_writer": a.events, "method": a.method,
           "n": len(lat), "median_ms": round(statistics.median(lat) * 1000, 1), "p90_ms": q(0.9), "p99_ms": q(0.99),
           "max_ms": round(lat[-1] * 1000, 1), "mean_ms": round(statistics.mean(lat) * 1000, 1),
           "t": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    sys.stdout.write(json.dumps(res) + "\n")
    if a.out:
        with open(a.out, "a") as f:
            f.write(json.dumps(res) + "\n")
    for m in d.glob("*.marker"):
        m.unlink()
    d.rmdir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
