"""Day-0 measurements of channel (i) (Phase 2, executor Rosalie, 2026-11-16): unit costs and rho = 2 memory/storage.

Reads only `done` markers of the given campaigns (ledger/markers/<campaign>/000/*.marker) and their pile-up-only
outputs (no signal): CPU, max RSS, wall per job (runner accounting = /usr/bin/time -v semantics, FEAS_C R1); per-event
chain stage times (`chain.timing`); per-trial finder times (`trials.times`); pre-merge store size per trial.
Also checks bit-identity of jobs that share a seed (pairs given with --pair a:b, v1-schema keys except meta/timing).
Writes phase2_exploration/outputs/day0_measurements.json (merged with what is there).

Run on a worker (imports numpy):  envs/tt/.pixi/envs/default/bin/python phase2_exploration/src/day0_summary.py \
    p2-a-day0-pu1 p2-a-day0-pu2b [--pair d0pu2b-n1:d0pu2-n1-nopm]
"""
import argparse
import json
import logging
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
MARKERS = QV2 / "ledger" / "markers"
OUT = HERE.parent / "outputs" / "day0_measurements.json"
log = logging.getLogger("day0_summary")
SKIP_KEYS = ("meta_json", "chain.timing", "trials.times", "trials.t_total")


def done_records(camp):
    recs = {}
    for p in sorted((MARKERS / camp).glob("*/*.marker")):
        last = None
        for line in p.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("status") == "done":
                last = d
        if last:
            recs[last["job_id"]] = last
    return recs


def job_summary(rec):
    s = dict(node=rec["node"], cpu_s=rec["cpu_s"], max_rss_mb=rec["max_rss_mb"], wall_s=rec["wall_s"],
             mem_limit_mb=rec.get("mem_limit_mb"), outputs={o["name"]: o["bytes"] for o in rec["outputs"]})
    for o in rec["outputs"]:
        if o["name"].endswith(".premerge.npz"):
            with np.load(o["path"], allow_pickle=False) as z:
                m = json.loads(str(z["meta_json"]))
            s["premerge"] = dict(n_trials=m["n_trials"], n_cand=m["n_cand"], n_hits=m["n_hits"], n_refs=m["n_refs"],
                                 bytes=o["bytes"], bytes_per_trial=o["bytes"] / max(1, m["n_trials"]),
                                 cand_per_trial=m["n_cand"] / max(1, m["n_trials"]), min_nip2=m["min_nip2"])
        elif o["name"].endswith(".npz"):
            with np.load(o["path"], allow_pickle=False) as z:
                meta = json.loads(str(z["meta_json"]))
                job = meta["job"]
                s.update(n_events=job["n_events"], rho=job["rho"], roads=job["roads"], seed=job["seed"],
                         finder_cfg=meta["finder_cfg"], v41_pass=meta.get("v41_pass"), t_chain_s=meta["t_chain_s"],
                         wall_s_tt=meta["wall_s"], cpu_s_tt=meta["cpu_s_tt"], main_bytes=o["bytes"])
                tc = list(z["chain.timing_cols"]) if "chain.timing_cols" in z.files else []
                if tc:
                    t = z["chain.timing"]
                    s["chain_timing_mean_s"] = {c: float(np.mean(t[:, i])) for i, c in enumerate(tc)}
                tt = z["trials.times"]
                cols = list(z["trials.times_cols"])
                s["trial_times_mean_s"] = {c: float(tt[:, i].mean()) for i, c in enumerate(cols)}
                s["trial_total_mean_s"] = float(z["trials.t_total"].mean())
                s["trial_total_sd_s"] = float(z["trials.t_total"].std(ddof=1)) if len(tt) > 1 else None
                s["n_trials"] = int(z["n_trials"])
            ev = s["n_events"]
            s["cpu_per_event_s"] = s["cpu_s"] / ev
            s["chain_per_crossing_s"] = s["t_chain_s"] / (ev * s["rho"])
    return s


def identical(path_a, path_b):
    diff = []
    with np.load(path_a, allow_pickle=False) as a, np.load(path_b, allow_pickle=False) as b:
        keys = sorted(set(a.files) | set(b.files))
        for k in keys:
            if k in SKIP_KEYS or k.startswith("trials.times") or k.endswith("timing_cols"):
                continue
            if k not in a.files or k not in b.files:
                diff.append(k)
            elif not np.array_equal(a[k], b[k], equal_nan=a[k].dtype.kind == "f"):
                diff.append(k)
        n = len(keys)
    return dict(n_keys=n, differing=diff, identical=not diff)


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("campaigns", nargs="+")
    ap.add_argument("--pair", action="append", default=[])
    a = ap.parse_args()
    res = json.loads(OUT.read_text()) if OUT.exists() else {}
    paths = {}
    for c in a.campaigns:
        recs = done_records(c)
        res.setdefault("campaigns", {})[c] = {j: job_summary(r) for j, r in recs.items()}
        for j, r in recs.items():
            for o in r["outputs"]:
                if o["name"] == f"{j}.npz":
                    paths[j] = o["path"]
        log.info("%s: %d done jobs", c, len(recs))
    for p in a.pair:
        x, y = p.split(":")
        res.setdefault("bit_identity", {})[p] = identical(paths[x], paths[y])
        log.info("pair %s: %s", p, res["bit_identity"][p])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.part")
    tmp.write_text(json.dumps(res, indent=1, default=str) + "\n")
    tmp.replace(OUT)
    log.info("wrote %s", OUT)


if __name__ == "__main__":
    main()
