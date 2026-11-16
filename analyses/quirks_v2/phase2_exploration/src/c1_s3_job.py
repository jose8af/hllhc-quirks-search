"""c1_s3_job.py -- one Stage-3 chunk of the C1 signal points through v1's sim/stage3/code/run_stage3.run_job
(channel (i), Rosalie, 2026-11-16).  Truth-level string propagation; no selection, no efficiency.

Job content as v1 make_jobs.py (campaign 'p2'): events = the template split up to its 200th |eta| < 2.5 event, then the
toy split likewise (p2_lists), cfg BM, luminous vertex, hmax 0.2, max_boost 1e-3 (Lambda <= 5 keV).  The event list is
cut into chunks of --size; this job runs chunk --chunk.  Kernel seeds are v1's blake2b("spin|m|row|lam|cfg").
Output in $QV2_OUT_DIR: p2_F_m<m>_L<lam>_BM_c<chunk>.npz (v1 Stage-3 output schema).
Run with the TT env:  envs/tt/.pixi/envs/default/bin/python c1_s3_job.py --input /nfs/.../F_m200_p2.npz --m 200 \
    --lam 1.5 --chunk 0 --size 100
"""
import argparse
import json
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
CODE = QV2 / "sim" / "stage3" / "code"
log = logging.getLogger("c1_s3_job")


def p2_lists(z):
    import numpy as np
    spl = z["tt_split"]; ins = z["in_eta25"]
    out = []
    for s in (0, 1):
        idx = np.where(spl == s)[0]
        c = np.cumsum(ins[idx])
        if c[-1] < 200:
            raise RuntimeError(f"only {c[-1]} split-{s} events in |eta| < 2.5 (need 200)")
        last = int(np.searchsorted(c, 200))
        out += idx[:last + 1].tolist()
    return out


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--lam", type=float, required=True)
    ap.add_argument("--chunk", type=int, required=True)
    ap.add_argument("--size", type=int, required=True)
    a = ap.parse_args()
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(CODE))
    import numpy as np
    import run_stage3 as R3
    inp = Path(a.input)
    with np.load(inp, allow_pickle=False) as z:
        ev_all = p2_lists(z)
    ev = ev_all[a.chunk * a.size:(a.chunk + 1) * a.size]
    if not ev:
        raise SystemExit("empty chunk")
    name = f"L{a.lam:g}_BM_c{a.chunk:02d}"
    job = dict(id=f"p2/F_m{a.m}/{name}", out=f"p2/F_m{a.m}/{name}.npz", campaign="p2", spin="F", m=a.m, lam=a.lam,
               cfg="BM", chunk=a.chunk, input=inp.name, ev=ev, max_boost=1e-3 if a.lam <= 5.0 else 1e-2, hmax=0.2,
               vertex="lumi", est_s=0.0)
    work = Path.cwd() / "s3out"
    log.info("Stage-3 job %s: %d events (of %d in the p2 lists)", job["id"], len(ev), len(ev_all))
    res = R3.run_job(job, str(inp.parent), str(work))
    log.info("done: %s", json.dumps(res, default=str))
    outd = Path(os.environ.get("QV2_OUT_DIR", "."))
    shutil.move(str(R3.out_path(work, job)), str(outd / f"p2_F_m{a.m}_{name}.npz"))


if __name__ == "__main__":
    main()
