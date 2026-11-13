"""Summarise the Phase-1 runner validation (TEST ONLY) into outputs/feasibility/benchmarks_runner.json.

Inputs: test markers (outputs/feasibility/runner_ledger/markers), saved Argo workflow status JSON
(data/feasibility/runner/argo_status/*.json), pyhf benchmark outputs (data/feasibility/runner/feas-pyhf/000/).
Run:  tools/runner/.pixi/envs/default/bin/python analyses/quirks_v2/phase1_strategy/src/runner_feas/summarize_runner.py
"""
import datetime as dt
import glob
import json
import statistics as stats
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parents[1]
LEDGER = P1 / "outputs/feasibility/runner_ledger/markers"
OUT = P1 / "outputs/feasibility/benchmarks_runner.json"
DATA = Path("/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner")


def recs(campaign):
    out = {}
    for m in sorted((LEDGER / campaign).glob("*/*.marker")):
        out[m.stem] = [json.loads(ln) for ln in m.read_text().splitlines() if ln.strip()]
    return out


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def pods(campaign):
    res = []
    for f in sorted(DATA.glob(f"argo_status/jdochoa-qv2-{campaign}-*.json")):
        w = json.loads(Path(f).read_text())
        st = w["status"]
        for n in st["nodes"].values():
            if n["type"] == "Pod":
                res.append({"workflow": w["metadata"]["name"], "name": n["displayName"], "phase": n["phase"],
                            "start": ts(n["startedAt"]), "end": ts(n["finishedAt"]) if n.get("finishedAt") else None,
                            "message": n.get("message", "")})
        res.sort(key=lambda p: p["start"])
    wfs = []
    for f in sorted(DATA.glob(f"argo_status/jdochoa-qv2-{campaign}-*.json")):
        w = json.loads(Path(f).read_text())
        wfs.append({"name": w["metadata"]["name"], "created": ts(w["metadata"]["creationTimestamp"]),
                    "start": ts(w["status"]["startedAt"]), "end": ts(w["status"]["finishedAt"]),
                    "phase": w["status"]["phase"]})
    return res, wfs


def job_rows(campaign):
    rows = []
    for jid, rr in recs(campaign).items():
        starts = [r for r in rr if r["status"] == "started"]
        done = [r for r in rr if r["status"] == "done"]
        if not done:
            continue
        d, s = done[-1], starts[-1]
        rows.append({"job": jid, "node": d["node"], "mechanism": d["mechanism"], "cpu_s": d["cpu_s"],
                     "cmd_wall_s": d.get("cmd_wall_s", d["wall_s"]), "max_rss_mb": d["max_rss_mb"],
                     "startup_s": round(s["t_wrapper"] - s["t_proc_start"], 2) if s.get("t_proc_start") else None,
                     "pre_cmd_s": round(d["t_cmd_start"] - d["t_wrapper"], 2) if d.get("t_wrapper") else None,
                     "post_cmd_s": round(d["ts"] - d["t_cmd_end"], 2), "t_proc_start": s.get("t_proc_start"),
                     "t_marker_done": d["ts"], "attempts": len(starts), "cgroup_peak_mb": d.get("cgroup_peak_mb"),
                     "mem_guard": d.get("mem_guard")})
    return sorted(rows, key=lambda r: r["job"])


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(stats.mean(xs), 2) if xs else None


def sd(xs):
    xs = [x for x in xs if x is not None]
    return round(stats.stdev(xs), 2) if len(xs) > 1 else None


def cpu60(mech, t_launch=None, t_end=None):
    rows = job_rows(f"feas-cpu60-{mech}")
    res = {"jobs": rows, "cpu_s_mean": mean([r["cpu_s"] for r in rows]), "cpu_s_sd": sd([r["cpu_s"] for r in rows]),
           "cmd_wall_s_mean": mean([r["cmd_wall_s"] for r in rows]),
           "max_rss_mb_mean": mean([r["max_rss_mb"] for r in rows]),
           "wrapper_startup_s_mean": mean([r["startup_s"] for r in rows])}
    if mech == "argo":
        pp, wfs = pods("feas-cpu60-argo")
        res["pods"] = pp
        res["workflows"] = wfs
        w = wfs[0]
        # per-job slot overhead in a sequential (parallelism 1) workflow
        res["makespan_s"] = round(w["end"] - w["created"], 1)
        res["pod_minus_cmd_s"] = [round(p["end"] - p["start"] - r["cmd_wall_s"], 1) for p, r in zip(pp, rows)]
        res["pod_start_to_proc_start_s"] = [round(r["t_proc_start"] - p["start"], 1) for p, r in zip(pp, rows)]
        res["inter_pod_gap_s"] = [round(pp[i + 1]["start"] - pp[i]["end"], 1) for i in range(len(pp) - 1)]
        res["last_pod_end_to_wf_end_s"] = round(w["end"] - pp[-1]["end"], 1)
        res["submit_to_first_pod_s"] = round(pp[0]["start"] - w["created"], 1)
    else:
        if t_launch and t_end:
            res["makespan_s"] = round(t_end - t_launch, 1)
        res["proc_start_after_prev_done_s"] = [round(rows[i + 1]["t_proc_start"] - rows[i]["t_marker_done"], 1)
                                               for i in range(len(rows) - 1)]
    n = len(rows)
    if res.get("makespan_s"):
        res["overhead_per_job_s"] = round(res["makespan_s"] / n - res["cmd_wall_s_mean"], 1)
    return res


def main():
    out = {"label": "TEST ONLY — Phase-1 runner validation (session Boris, 2026-11-13); no physics",
           "node": "landau (i5-7500, 4 cores)", "generated": dt.datetime.now().isoformat(timespec="seconds")}
    times = {}
    f = DATA / "cpu60_driver_times.json"
    if f.exists():
        times = json.loads(f.read_text())
    out["cpu60"] = {"argo": cpu60("argo"), "ssh": cpu60("ssh", times.get("ssh_start"), times.get("ssh_end"))}
    for c in ("feas-acct-ssh", "feas-acct-argo", "feas-mini-ssh", "feas-mini-argo", "feas-mem-ssh",
              "feas-mem-argo"):
        rr = recs(c)
        if rr:
            out[c] = {"jobs": len(rr), "done": len(job_rows(c)),
                      "events": {j: [r["status"] for r in v] for j, v in rr.items()
                                 if [r["status"] for r in v] != ["started", "done"]},
                      "cpu_s_mean": mean([r["cpu_s"] for r in job_rows(c)]),
                      "max_rss_mb_max": max([r["max_rss_mb"] for r in job_rows(c)], default=None),
                      "wrapper_startup_s": [r["startup_s"] for r in job_rows(c)]}
            if c.startswith("feas-mem"):
                out[c]["last"] = {j: v[-1] for j, v in rr.items()}
    pyhf = {}
    for p in glob.glob(str(DATA / "feas-pyhf/000/*.json")):
        pyhf[Path(p).stem] = json.loads(Path(p).read_text())
    if pyhf:
        out["pyhf"] = {"outputs": pyhf, "jobs": job_rows("feas-pyhf")}
    OUT.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
