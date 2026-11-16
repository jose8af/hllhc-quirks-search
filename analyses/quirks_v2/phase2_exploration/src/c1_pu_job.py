"""One Stage-4 pile-up job of the v2 C1 reproduction (Phase 2, channel (i), executor Rosalie, 2026-11-16).

Runs v1's `acts.stage4.run_stage4.run_pu_job` unchanged in logic, with the operative frozen configuration of
`acts/stage4/frozen_inputs.json` (road = delta95 = 0.15, T_seed = 4; STR §4.1), a v2 seed stream
(job seed = v1 `hash_seed("qv2|<stream>|<chunk>")`, STR §4.17) and its output in the runner's `$QV2_OUT_DIR`:

  <job_id>.npz            v1 Stage-4 output schema (trials.*, cand.*, hit.*, btl, dump.*, chain.*, meta_json)
  <job_id>.premerge.npz   (optional) pre-merge candidate store (STR §4.5 (a)): one zip entry per trial and key,
                          written trial by trial (keys "t<trial>/<name>"), so memory does not grow with the events

Run inside a runner job (`tools/runner`), from any directory:
  envs/tt/.pixi/envs/default/bin/python phase2_exploration/src/c1_pu_job.py --id ID --stream c1.pu1 --chunk K \
      --ev0 E0 --n N --rho 1 --roads 4 [--dump N] [--premerge 6] [--kind sm --sm-sample Znunu_j]
"""
import argparse
import hashlib
import json
import logging
import os
import shutil
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger("c1_pu_job")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class PremergeWriter:
    """Streams each trial's pre-merge arrays into one zip of .npy entries (readable with numpy.load)."""

    def __init__(self, path, min_nip2):
        import numpy as np
        self.np = np
        self.path = Path(path)
        self.min_nip2 = int(min_nip2)
        self.zf = zipfile.ZipFile(self.path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        self.n_trials = 0
        self.n_cand = 0
        self.n_hits = 0
        self.n_refs = 0

    def write(self, ti, pre):
        for k, v in pre.items():
            with self.zf.open(f"t{ti}/{k}.npy", "w", force_zip64=True) as f:
                self.np.lib.format.write_array(f, self.np.asanyarray(v), allow_pickle=False)
        self.n_trials += 1
        self.n_cand += len(pre["idx"])
        self.n_hits += len(pre["h_sid"])
        self.n_refs += len(pre["ref"])

    def close(self, meta):
        with self.zf.open("meta_json.npy", "w") as f:
            self.np.lib.format.write_array(f, self.np.array(json.dumps(meta, default=str)), allow_pickle=False)
        self.zf.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--id", required=True)
    ap.add_argument("--stream", required=True, help="seed stream name of STR §4.17, e.g. c1.pu1")
    ap.add_argument("--chunk", type=int, required=True)
    ap.add_argument("--ev0", type=int, required=True)
    ap.add_argument("--n", type=int, required=True, help="events in this job")
    ap.add_argument("--rho", type=int, default=1)
    ap.add_argument("--roads", type=int, default=4)
    ap.add_argument("--dump", type=int, default=0, help="number of events whose chain output is dumped (S6 dumps)")
    ap.add_argument("--premerge", type=int, default=None, help="store pre-merge candidates with N_IP2 >= this")
    ap.add_argument("--kind", default="pu", choices=["pu", "sm"])
    ap.add_argument("--sm-sample", default=None)
    a = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    out_dir = Path(os.environ.get("QV2_OUT_DIR", "."))
    work = Path.cwd() / "s4work"
    os.environ["QV2_S4_DATA"] = str(work)                       # run_stage4 writes PROD = work/prod/<out>
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)                                               # v1 convention: run from the TT (= QV2) root

    from acts.stage4 import run_stage4 as RS

    fz = RS.frozen_inputs()
    if fz is None:
        raise SystemExit("frozen_inputs.json missing or not frozen")
    if fz.get("wp_rule_sha256") != RS.sha256_file(RS.HERE / "WP_RULE.md"):
        raise SystemExit("WP_RULE.md sha256 differs from frozen_inputs.json -> refusing (v1 freeze rule)")

    seed = RS.hash_seed(f"qv2|{a.stream}|{a.chunk}")
    job = dict(id=a.id, campaign="C1", sample=a.stream, kind=a.kind, chunk=a.chunk, ev0=a.ev0, n_events=a.n,
               roads=a.roads, rho=a.rho, seed=seed, dump_events=a.dump, est_s=0.0, mem_gb=0.0,
               out=f"{a.id}.npz", requires="pu-chain", qv2_stream=a.stream)
    if a.kind == "sm":
        job["sm_sample"] = a.sm_sample
    log.info("job %s stream %s chunk %d ev0 %d n %d rho %d roads %d seed %d dump %d premerge %s",
             a.id, a.stream, a.chunk, a.ev0, a.n, a.rho, a.roads, seed, a.dump, a.premerge)
    (work / "prod").mkdir(parents=True, exist_ok=True)
    pw = None
    if a.premerge is not None:
        pw = PremergeWriter(work / f"{a.id}.premerge.npz", a.premerge)
    t0 = time.time()
    res = RS.run_pu_job(job, allow_interim=False, premerge=pw)
    log.info("run_pu_job done in %.1f s: %s", time.time() - t0, json.dumps(res, default=str))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(RS.out_path(job)), str(out_dir / f"{a.id}.npz"))
    if pw is not None:
        meta = dict(job=job, min_nip2=pw.min_nip2, n_trials=pw.n_trials, n_cand=pw.n_cand, n_hits=pw.n_hits,
                    n_refs=pw.n_refs, created_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        pw.close(meta)
        log.info("premerge: %s", json.dumps(meta, default=str))
        shutil.move(str(pw.path), str(out_dir / f"{a.id}.premerge.npz"))
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
