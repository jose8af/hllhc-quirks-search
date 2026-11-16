"""c1_cp_job.py -- one C' job of the C1 reproduction (channel (i), Rosalie, 2026-11-16).

Runs v1's acts.stage4.run_g1b.run_cp0_job / run_cppu_job unchanged (frozen configuration):
  cp0   C'_0, no pile-up: --topo {dif, ni22, pvpair, gamma, v0, ...}, events [ev0, ev0 + n)
  cppu  C'_PU, PU 200 overlay of preselected C'_0 events: slots [slot0, slot0 + n); --sources = the published C'_0
        outputs of the topology (all of them; v1 rule), symlinked into the job scratch so that v1's PROD-relative
        `needs` paths resolve.
Job seed = hash_seed("qv2|c1.cpu.<kind>|<topo>|<chunk>") (stream c1.c0 / c1.cpu of STR §4.17); v1's per-event trial seeds
hash_seed("stage4|Cp0trial|<topo>|<g>") are kept as v1 had them.  Output in $QV2_OUT_DIR: <id>.npz.
"""
import argparse
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger("c1_cp_job")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--kind", choices=["cp0", "cppu"], required=True)
    ap.add_argument("--topo", required=True)
    ap.add_argument("--chunk", type=int, required=True)
    ap.add_argument("--start", type=int, required=True, help="ev0 (cp0) or slot0 (cppu)")
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--sources", default="", help="cppu: comma list of published C'_0 files of this topology")
    a = ap.parse_args()
    work = Path.cwd() / "s4work"
    (work / "prod").mkdir(parents=True, exist_ok=True)
    os.environ["QV2_S4_DATA"] = str(work)
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)
    from acts.stage4 import run_stage4 as RS
    from acts.stage4 import run_g1b as G
    fz = RS.frozen_inputs()
    if fz is None or fz.get("wp_rule_sha256") != RS.sha256_file(RS.HERE / "WP_RULE.md"):
        raise SystemExit("frozen_inputs / WP_RULE.md mismatch")
    stream = "c1.c0" if a.kind == "cp0" else "c1.cpu"
    seed = RS.hash_seed(f"qv2|{stream}|{a.kind}|{a.topo}|{a.chunk}")
    job = dict(id=a.id, campaign="C1", sample=a.kind, kind=a.kind, topo=a.topo, chunk=a.chunk, n_events=a.n, roads=1,
               rho=1, seed=seed, dump_events=0, est_s=0.0, mem_gb=1.5, out=f"{a.id}.npz", requires="G1b",
               qv2_stream=stream)
    if a.kind == "cp0":
        job["ev0"] = a.start
    else:
        job["slot0"] = a.start
        srcd = work / "prod" / "src"
        srcd.mkdir()
        needs = []
        for p in a.sources.split(","):
            (srcd / Path(p).name).symlink_to(p)
            needs.append(f"src/{Path(p).name}")
        job["needs"] = needs
    log.info("C' job %s kind %s topo %s chunk %d start %d n %d seed %d", a.id, a.kind, a.topo, a.chunk, a.start, a.n,
             seed)
    res = G.run_job(job)
    log.info("finished: %s", {k: res.get(k) for k in ("wall", "t_chain", "n_trials", "bytes", "v41_pass")})
    outd = Path(os.environ.get("QV2_OUT_DIR", "."))
    shutil.move(str(RS.out_path(job)), str(outd / f"{a.id}.npz"))
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
