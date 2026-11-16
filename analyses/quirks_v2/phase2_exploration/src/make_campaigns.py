"""Write the runner campaign files of channel (i) (Phase 2, executor Rosalie, 2026-11-16).

Output: tools/runner/campaigns/<campaign>.json (runner schema, FEAS_C §2). Data land under data/phase2/<campaign>/.
Usage (light, stdlib only; on einstein with python3 -I is fine):
  python3 -I make_campaigns.py day0-pu1
  python3 -I make_campaigns.py day0-pu2 --sizes 1,2,4 [--name p2-a-day0-pu2]
  python3 -I make_campaigns.py c1-pu1 --per 20
  python3 -I make_campaigns.py c1-pu2 --per 5 --rss 3000
"""
import argparse
import json
import logging
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
REPO = QV2.parents[1]
CAMP_DIR = REPO / "tools" / "runner" / "campaigns"
PY = "$QV2/envs/tt/.pixi/envs/default/bin/python"
JOB = "$QV2/phase2_exploration/src/c1_pu_job.py"
PRELUDE = (". /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && "
           "export NUMBA_CACHE_DIR=$QV2_SCRATCH/cache/numba_s4 PYTHONPYCACHEPREFIX=$QV2_SCRATCH/cache/pyc "
           "QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH/cache/pythia_init PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 && ")
log = logging.getLogger("make_campaigns")


def pu_job(jid, stream, chunk, ev0, n, rho, roads, dump=0, premerge=None, kind="pu", sm_sample=None):
    cmd = (PRELUDE + f"{PY} {JOB} --id {jid} --stream {stream} --chunk {chunk} --ev0 {ev0} --n {n} "
           f"--rho {rho} --roads {roads} --dump {dump} --kind {kind}")
    outs = [f"{jid}.npz"]
    if premerge is not None:
        cmd += f" --premerge {premerge}"
        outs.append(f"{jid}.premerge.npz")
    if sm_sample:
        cmd += f" --sm-sample {sm_sample}"
    return dict(id=jid, shard=0, command=cmd, outputs=outs)


def write(name, jobs, tier, desc, hours, rss, regenerate=""):
    d = dict(campaign=name, tier=tier, data_prefix="phase2", description=desc, expected_hours=hours,
             regenerate=regenerate or "python3 -I phase2_exploration/src/make_campaigns.py (see description)",
             defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)
    CAMP_DIR.mkdir(parents=True, exist_ok=True)
    p = CAMP_DIR / f"{name}.json"
    p.write_text(json.dumps(d, indent=1) + "\n")
    log.info("wrote %s: %d jobs", p, len(jobs))


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("what")
    ap.add_argument("--sizes", default="1,2,4")
    ap.add_argument("--name", default=None)
    ap.add_argument("--per", type=int, default=20)
    ap.add_argument("--chunk0", type=int, default=0)
    ap.add_argument("--rss", type=float, default=None)
    ap.add_argument("--hours", type=float, default=None)
    a = ap.parse_args()
    if a.what == "day0-pu1":
        jobs = [pu_job("d0pu1-n5-a", "p2a.day0.pu1", 0, 0, 5, 1, 4, dump=5)]
        write(a.name or "p2-a-day0-pu1", jobs, "scratch",
              "day-0 timing: rho = 1, 4 roads, 5 events, frozen road 0.15 / T_seed 4, dumps on (as C1)",
              a.hours or 0.2, a.rss or 700)
    elif a.what == "day0-pu2":
        sizes = [int(x) for x in a.sizes.split(",")]
        jobs, ev0 = [], 0
        for k, n in enumerate(sizes):
            jobs.append(pu_job(f"d0pu2-n{n}", "p2a.day0.pu2", a.chunk0 + k, ev0, n, 2, 2,
                               dump=0, premerge=6))
            ev0 += n
        write(a.name or "p2-a-day0-pu2", jobs, "scratch",
              "day-0 rho = 2 memory and pre-merge storage (STR §4.5, COM B2-e): RSS vs events per job, one job alone "
              "on the node, pre-merge store N_IP2 >= 6 on", a.hours or 1.0, a.rss or 3600)
    elif a.what == "c1-pu1":
        per, n_tot = a.per, 4000
        jobs = [pu_job(f"c1pu1-{e0 // per:04d}", "c1.pu1", e0 // per, e0, min(per, n_tot - e0), 1, 4,
                       dump=min(per, n_tot - e0)) for e0 in range(0, n_tot, per)]
        write("p2-a-c1-pu1", jobs, "final",
              f"C1 (STR §4.1, §4.17 row 1): pile-up rho = 1, 4 roads, 4,000 events, {per} per job, stream c1.pu1, "
              "frozen v1 config (road 0.15, T_seed 4), hit dumps for every event (C2 T_seed, B2 occupancy development)",
              a.hours or 20.0, a.rss or 700)
    elif a.what == "c1-pu2":
        per, n_tot = a.per, 1000
        jobs = [pu_job(f"c1pu2-{e0 // per:04d}", "c1.pu2", e0 // per, e0, min(per, n_tot - e0), 2, 2,
                       dump=max(0, min(per, 200 - e0)), premerge=6) for e0 in range(0, n_tot, per)]
        write("p2-a-c1-pu2", jobs, "final",
              f"C1 (STR §4.1, §4.17 row 2): pile-up rho = 2, 2 roads, 1,000 events, {per} per job, stream c1.pu2, "
              "pre-merge store N_IP2 >= 6 on (B2 development), dumps for the first 200 events (C2 T_seed)",
              a.hours or 20.0, a.rss or 3000)
    elif a.what == "c1-s2":
        # C1 signal Stage 2 (orchestrator 2026-11-16 12:58): v1 TRG (pT_ME >= 100) and INC chunks at E 200 and E 500,
        # FSR off; a.per = LHE events per chunk; --sizes = chunk indices to add (top-ups use new indices, new seeds)
        s2 = "python3 -I /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/c1_s2_job.py"
        chunks = [int(x) for x in a.sizes.split(",")]
        jobs = []
        for proc in ("F_TRG", "F_INC"):
            for m in (200, 500):
                for c in chunks:
                    tag = f"c1s2-{proc[2:].lower()}-m{m}-c{c:02d}"
                    jobs.append(dict(id=tag, shard=0, command=f"{s2} c1gen {tag} {proc} {m} {a.per}",
                                     outputs=[f"{tag}.lhe.gz", f"{tag}.npz", f"{tag}.json", f"{tag}.aux.tar.gz"]))
        write(a.name or "p2-a-c1-s2", jobs, "final",
              f"C1 signal Stage 2 (STR §4.1, §4.17 row 6): v1 F_TRG (pT_ME >= 100 GeV) and F_INC, MLM 0-2j, CP5, "
              f"qCut 45, QED-FSR off, {a.per} LHE events per chunk, E 200 and E 500; stream c1.s2", a.hours or 2.0,
              a.rss or 1500)
    elif a.what == "c1-sm":
        per, n_tot = a.per, 2000
        jobs = [pu_job(f"c1sm-{e0 // per:04d}", "c1.sm", e0 // per, e0, min(per, n_tot - e0), 1, 1, kind="sm",
                       sm_sample="Znunu_j") for e0 in range(0, n_tot, per)]
        write("p2-a-c1-sm", jobs, "final",
              f"C1 (STR §4.1, §4.17 row 5): Z(nunu)+j hard scatter + PU 200 hit level, 1 MET road, 2,000 events, {per} "
              "per job, stream c1.sm, frozen v1 config", a.hours or 15.0, a.rss or 1000)
    elif a.what == "c1-cp0":
        cp = f"{PRELUDE}{PY} $QV2/phase2_exploration/src/c1_cp_job.py"
        sizes = {"dif": 50000, "ni22": 30000, "pvpair": 100000, "gamma": 100000, "v0": 100000}
        per = a.per
        jobs = []
        for topo, n in sizes.items():
            for ch, e0 in enumerate(range(0, n, per)):
                jid = f"c1cp0-{topo}-{ch:03d}"
                jobs.append(dict(id=jid, shard=0, outputs=[f"{jid}.npz"],
                                 command=f"{cp} --id {jid} --kind cp0 --topo {topo} --chunk {ch} --start {e0} "
                                         f"--n {min(per, n - e0)}"))
        write("p2-a-c1-cp0", jobs, "final",
              f"C1 (STR §4.1, §4.17 row 3): C'_0 no pile-up at v1 sizes for DIF, NI 22 mm, PV pair (f_pre) and the "
              f"gamma, V0 gun sources of C'_PU; {per} events per job; stream c1.c0", a.hours or 3.0, a.rss or 1500)
    elif a.what == "c1-s3in":
        # one job per mass from every done Stage-2 chunk (markers); a.name = campaign name (new name per top-up)
        mk = QV2 / "ledger" / "markers"
        outs = {}
        for camp in a.sizes.split(","):          # Stage-2 campaigns to use
            for p in sorted((mk / camp).glob("*/*.marker")):
                done = [json.loads(x) for x in p.read_text().splitlines() if '"done"' in x]
                if done:
                    for o in done[-1]["outputs"]:
                        outs[o["name"]] = o["path"]
        anapy = "$QV2/sim/.pixi/envs/ana/bin/python"
        jobs = []
        for m in (200, 500):
            sel = lambda kind, ext: sorted(v for k, v in outs.items() if k.startswith(f"c1s2-{kind}-m{m}-") and k.endswith(ext))  # noqa
            tn, tj, inn, ij = sel("trg", ".npz"), sel("trg", ".json"), sel("inc", ".npz"), sel("inc", ".json")
            jid = f"c1s3in-m{m}"
            jobs.append(dict(id=jid, shard=0, outputs=[f"F_m{m}_p2.npz", f"E-TRGS_m{m}.npz", f"c1_inputs_m{m}.json"],
                             command=PRELUDE + f"{anapy} $QV2/phase2_exploration/src/c1_s3_inputs.py {m} --trg "
                             f"{','.join(tn)} --trg-json {','.join(tj)} --inc {','.join(inn)} --inc-json {','.join(ij)}"))
        write(a.name or "p2-a-c1-s3in", jobs, "final", f"C1 signal: Stage-3 inputs from Stage-2 campaigns {a.sizes}",
              0.5, a.rss or 3000)
    elif a.what == "c1-s3":
        # a.sizes = "<input campaign>"; chunks: E200 100 events, E500 3 keV 40 events; 500 events covered per point
        src = QV2 / "ledger" / "markers" / a.sizes
        paths = {}
        for p in sorted(src.glob("*/*.marker")):
            done = [json.loads(x) for x in p.read_text().splitlines() if '"done"' in x]
            if done:
                for o in done[-1]["outputs"]:
                    paths[o["name"]] = o["path"]
        jobs = []
        nlist = {m: json.load(open(paths[f"c1_inputs_m{m}.json"]))["n_p2_list"] for m in (200, 500)}
        for m, lam, size in ((200, 1.5, 100), (200, 2.0, 100), (500, 3.0, 25)):
            if nlist[m] < 400:
                raise SystemExit(f"m = {m}: p2 list has {nlist[m]} events (< 400): top up Stage 2 first")
            for ch in range((nlist[m] + size - 1) // size):
                jid = f"c1s3-m{m}-l{lam:g}-c{ch:02d}".replace(".", "p")
                jobs.append(dict(id=jid, shard=0, outputs=[f"p2_F_m{m}_L{lam:g}_BM_c{ch:02d}.npz"],
                                 command=PRELUDE + f"{PY} $QV2/phase2_exploration/src/c1_s3_job.py --input "
                                 f"{paths[f'F_m{m}_p2.npz']} --m {m} --lam {lam:g} --chunk {ch} --size {size}"))
        write(a.name or "p2-a-c1-s3", jobs, "final", "C1 signal Stage 3 (v1 run_stage3.run_job, campaign p2 settings) at "
              "E200 1.5 and 2 keV and E500 3 keV; p2 lists (template + toy to the 200th |eta| < 2.5 event each)",
              a.hours or 4.0, a.rss or 800)
    elif a.what == "c1-sig":
        sg = f"{PRELUDE}{PY} $QV2/phase2_exploration/src/c1_sig_job.py"
        a2, a5 = [], []
        for ch in range((400 + a.per - 1) // a.per):              # a2 fast path, E 200, both Lambda, row-major
            jid = f"c1sig-a2-m200-c{ch:02d}"
            a2.append(dict(id=jid, shard=0, outputs=[f"{jid}.npz"],
                           command=f"{sg} --id {jid} --kind a2 --m 200 --lams 1.5,2 --chunk {ch} --size {a.per}"))
        for m, lam in ((500, 3.0), (200, 1.5), (200, 2.0)):     # full chain: E500 3 keV (v1 path) + the twins
            for ch in range((400 + a.per - 1) // a.per):
                jid = f"c1sig-a5-m{m}-l{lam:g}-c{ch:02d}".replace(".", "p")
                a5.append(dict(id=jid, shard=0, outputs=[f"{jid}.npz"],
                               command=f"{sg} --id {jid} --kind a5 --m {m} --lams {lam:g} --chunk {ch} --size {a.per}"))
        desc = ("C1 signal Stage 4 (STR §4.1, COM C1-d/e): v1 run_g1b.run_signal_job, frozen config; {}. SEALED CONTENT: "
                "outputs hold R07 and fallback bits; read only through c1_signal_compare.py (open: R04/R06 masked input)")
        write("p2-a-c1-siga2", a2, "final", desc.format("a2 fast path E200 x {1.5, 2} keV"), 6.0, a.rss or 1500)
        write("p2-a-c1-siga5", a5, "final", desc.format("a5 full chain E500 3 keV and twins E200 1.5 / 2 keV"), 10.0,
              a.rss or 1500)
    else:
        raise SystemExit(f"unknown campaign kind {a.what}")


if __name__ == "__main__":
    main()
