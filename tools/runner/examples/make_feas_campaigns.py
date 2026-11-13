"""Write the Phase-1 runner validation campaigns (TEST ONLY) to tools/runner/examples/feas/.

Outputs land under data/feasibility/runner/<campaign>/<shard>/; markers in the test ledger
analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/markers (not the production ledger).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "feas"
PY = "/home/users/jdochoa/hllhc-quirks-search/tools/runner/.pixi/envs/default/bin/python"
PAY = "/home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/payload.py"
LEDGER = "analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/markers"
CPU60_MIB = 27000  # ~60 s of sha256 on landau (460 MiB/s measured, 2000 MiB in 4.34 s)
MINI_MIB = 4600    # ~10 s
PYHF = "/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase1_strategy/src/pyhf_bench"


def camp(name, jobs, **kw):
    d = {"campaign": name, "tier": "test", "data_prefix": "feasibility/runner", "ledger": LEDGER,
         "description": "Phase-1 runner validation (TEST ONLY, no physics)", "defaults": {"max_rss_mb": 100}}
    d.update(kw)
    d["jobs"] = jobs
    (OUT / f"{name}.json").write_text(json.dumps(d, indent=1) + "\n")


def payload(args):
    return f"{PY} {PAY} {args}"


def main():
    OUT.mkdir(exist_ok=True)
    for mech in ("argo", "ssh"):
        camp(f"feas-cpu60-{mech}", [{"id": f"cpu60-{mech}-r{i}", "outputs": [f"cpu60-{mech}-r{i}.dat"],
                                     "command": payload(f"--hash-mib {CPU60_MIB} --pad-kib 1024 --out cpu60-{mech}-r{i}.dat")}
                                    for i in (1, 2, 3)])
        camp(f"feas-mini-{mech}", [{"id": f"mini-{mech}-{i:03d}", "shard": i // 12,
                                    "outputs": [f"mini-{mech}-{i:03d}.dat"],
                                    "command": payload(f"--hash-mib {MINI_MIB} --pad-kib 1024 --out mini-{mech}-{i:03d}.dat")}
                                   for i in range(24)])
        camp(f"feas-mem-{mech}", [{"id": f"mem-{mech}", "max_rss_mb": 133.34, "outputs": [f"mem-{mech}.dat"],
                                   "command": payload(f"--mem-mib 400 --out mem-{mech}.dat")}])
        camp(f"feas-acct-{mech}", [{"id": f"acct-{mech}", "max_rss_mb": 400, "outputs": [f"acct-{mech}.dat"],
                                    "command": "(ls -l /usr/bin/time || echo NO_USR_BIN_TIME; command -v python3 || echo NO_PYTHON3; "
                                               "cat /proc/self/cgroup; nice) && "
                                               + payload(f"--mem-mib 300 --hold 0 --hash-mib 4000 --out acct-{mech}.dat")}])
    camp("feas-pyhf", [{"id": f"pyhf-{part}", "max_rss_mb": 1500, "outputs": [f"pyhf-{part}.json"],
                        "command": f"cd {PYHF} && .pixi/envs/default/bin/python bench_pyhf.py --part {part} "
                                   f"--out $QV2_OUT_DIR/pyhf-{part}.json"}
                       for part in ("fit", "toys")])


if __name__ == "__main__":
    main()
