"""c2_verdicts.py -- channel (i), Ignatius 2026-11-18: verdicts of C2-b (V4-4 reproducibility) and C2-c (T_seed 4 -> 2).

C2-b (STR §4.2 row V4-4; COM C2-b): 20 production-type rho = 1 jobs (c2v44-NN, stream c2.v44) run twice on landau
(-a, -b), once on maxwell (-c), plus two jobs with other seeds (c2v44x-00/01, stream c2.v44x).  Criteria: outputs
bit-identical on the same node; cross-node identity reported (with the CPU models); different seeds give different
outputs; all seeds recorded.  Comparison: day0_summary.identical() (every npz key except meta_json and timing keys);
'job_id' is expected to differ (it is the job name) and is listed separately.  Seeds: meta_json job.seed, compared too.

C2-c (STR §4.2 row T_seed; COM C2-c; deviation D-i-4: regeneration from the same job seeds with T_seed = 2): pairs
c2ts2-pu1-NNNN <-> c1pu1-NNNN (0000-0024, rho = 1, 20 events x 4 roads) and c2ts2-pu2-NNNN <-> c1pu2-NNNN (0000-0039,
rho = 2, 5 events x 2 roads).  Pairing check: chain.evstats identical, trials.ev identical, trials.pv equal.
Metric (v1 acts/stage4/g3/analyse_g3.py tseed_test, 'pass_frac'): per trial, g = n_grp (n_pass where n_grp < 0), a
trial passes a rung if g > 0.  Family statistic (one per family and density, STR: 'per-trial pass fraction of each rung
family (counting R04, width R05-R06, chi2, 2S)'): the fraction of trials that pass at least one rung of the family;
families: counting = R04; width = R05, R06; chi2 = R09-R11; 2S = R12-R14 (v1 FAM, rungs as in STR / Rosalie's plan).
z = (f_T2 - f_T4) / sd of the paired event bootstrap of the difference (2,000 replicas, events = (job, ev)).
Criterion: |z| < 2.73 for all 8 tests (Bonferroni, family-wise 4.9 %).  The v1 per-rung table (R01-R14, pass_frac and
mean_grp, paired z) is reported as a diagnostic.
Usage (worker, TT env):  python c2_verdicts.py <out.json>
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from day0_summary import identical  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("c2")
QV2 = HERE.parents[1]
D = Path("/nfs/cajuela/jdochoa/quirks_v2/data/phase2")
FAMS = {"counting": [3], "width": [4, 5], "chi2": [8, 9, 10], "2S": [11, 12, 13]}
ZMAX = 2.73
NBOOT = 2000
SEED = 20261118


def path(camp, job):
    mk = QV2 / "ledger" / "markers" / camp / "000" / f"{job}.marker"
    assert mk.exists() and '"done"' in mk.read_text(), f"no done marker {camp}/{job}"
    return D / camp / "000" / f"{job}.npz"


def meta(p):
    with np.load(p, allow_pickle=False) as z:
        return json.loads(str(z["meta_json"]))


def c2b():
    rows = []
    for i in range(20):
        a, b, c = (path(f"p2-a-c2-v44{s}", f"c2v44-{i:02d}-{s}") for s in "abc")
        ab, ac = identical(a, b), identical(a, c)
        sa, sb, sc = (meta(p)["job"]["seed"] for p in (a, b, c))
        rows.append(dict(job=f"c2v44-{i:02d}", seed_a=sa, seed_b=sb, seed_c=sc,
                         ab_differing=ab["differing"], ac_differing=ac["differing"], n_keys=ab["n_keys"]))
    xs = []
    for i in range(2):
        x, a = path("p2-a-c2-v44c", f"c2v44x-{i:02d}"), path("p2-a-c2-v44a", f"c2v44-{i:02d}-a")
        r = identical(x, a)
        xs.append(dict(job=f"c2v44x-{i:02d}", vs=f"c2v44-{i:02d}-a", seed_x=meta(x)["job"]["seed"],
                       seed_ref=meta(a)["job"]["seed"], differing=r["differing"], n_keys=r["n_keys"]))
    same_node = all(set(r["ab_differing"]) <= {"job_id"} and r["seed_a"] == r["seed_b"] for r in rows)
    cross = all(set(r["ac_differing"]) <= {"job_id"} and r["seed_a"] == r["seed_c"] for r in rows)
    differ = all(x["seed_x"] != x["seed_ref"] and any(k.startswith(("trials.", "cand.", "chain.")) for k in x["differing"])
                 for x in xs)
    seeds = all(r["seed_a"] is not None for r in rows) and all(x["seed_x"] is not None for x in xs)
    v = dict(same_node_bit_identical=same_node, cross_node_identical=cross, different_seeds_differ=differ,
             seeds_recorded=seeds, verdict="PASS" if (same_node and differ and seeds) else "FAIL", pairs=rows,
             other_seed=xs)
    log.info("C2-b: same node %s, cross node %s, other seeds differ %s, seeds %s -> %s", same_node, cross, differ, seeds,
             v["verdict"])
    return v


TK = ("ev", "pv", "n_grp", "n_pass")


def load_tr(p):
    with np.load(p, allow_pickle=False) as z:
        m = json.loads(str(z["meta_json"]))
        return {k: z["trials." + k] for k in TK}, z["chain.evstats"], m


def c2c(rng):
    out = {}
    for dens, camp_t2, camp_t4, pre2, pre4, nj in (("rho1", "p2-a-c2-tseed1", "p2-a-c1-pu1", "c2ts2-pu1", "c1pu1", 25),
                                                     ("rho2", "p2-a-c2-tseed2", "p2-a-c1-pu2", "c2ts2-pu2", "c1pu2", 40)):
        G4, G2, EV = [], [], []
        evn = 0; checks = []
        for j in range(nj):
            t2, es2, m2 = load_tr(path(camp_t2, f"{pre2}-{j:04d}"))
            t4, es4, m4 = load_tr(path(camp_t4, f"{pre4}-{j:04d}"))
            ck = dict(job=j, evstats_identical=bool(np.array_equal(es2, es4)),
                      ev_identical=bool(np.array_equal(t2["ev"], t4["ev"])),
                      pv_equal=bool(np.array_equal(t2["pv"], t4["pv"])), pv_allclose=bool(np.allclose(t2["pv"], t4["pv"])),
                      tseed_2=m2["finder_cfg"].get("tseed"), tseed_4=m4["finder_cfg"].get("tseed"),
                      seed_equal=m2["job"]["seed"] == m4["job"]["seed"])
            checks.append(ck)
            G4.append(np.where(t4["n_grp"] < 0, t4["n_pass"], t4["n_grp"]))
            G2.append(np.where(t2["n_grp"] < 0, t2["n_pass"], t2["n_grp"]))
            ue, inv = np.unique(t4["ev"], return_inverse=True)
            EV.append(inv + evn); evn += len(ue)
        G4 = np.concatenate(G4).astype(float); G2 = np.concatenate(G2).astype(float); EV = np.concatenate(EV)
        en = np.bincount(EV, minlength=evn).astype(float)
        bi = rng.integers(0, evn, size=(NBOOT, evn))

        def paired(a4, a2):
            e4 = np.bincount(EV, weights=a4, minlength=evn); e2 = np.bincount(EV, weights=a2, minlength=evn)
            m4, m2 = e4.sum() / en.sum(), e2.sum() / en.sum()
            nb = en[bi].sum(1)
            b4 = e4[bi].sum(1) / nb; b2 = e2[bi].sum(1) / nb
            sd = float(np.std(b2 - b4, ddof=1))
            z = (m2 - m4) / sd if sd > 0 else (0.0 if m2 == m4 else float("inf"))
            sdu = float(np.hypot(np.std(b4, ddof=1), np.std(b2, ddof=1)))
            return dict(f_T4=float(m4), f_T2=float(m2), rel=float(m2 / m4 - 1) if m4 > 0 else None, sd_paired=sd,
                        z_paired=float(z), sd_unpaired=sdu, n_trials_pass_T4=int(a4.sum()), n_trials_pass_T2=int(a2.sum()))
        fam = {}
        for f, cols in FAMS.items():
            r = paired((G4[:, cols] > 0).any(1).astype(float), (G2[:, cols] > 0).any(1).astype(float))
            r.update(rungs=[f"R{c + 1:02d}" for c in cols], pass_=bool(abs(r["z_paired"]) < ZMAX))
            fam[f] = r
            log.info("C2-c %s %-8s f4 %.5f f2 %.5f z %+.2f", dens, f, r["f_T4"], r["f_T2"], r["z_paired"])
        diag = []
        for c in range(14):
            diag.append(dict(rung=f"R{c + 1:02d}", pass_frac=paired((G4[:, c] > 0).astype(float), (G2[:, c] > 0).astype(float)),
                             mean_grp=paired(G4[:, c], G2[:, c])))
        pair_ok = all(c["evstats_identical"] and c["ev_identical"] and c["pv_allclose"] and c["seed_equal"]
                      and c["tseed_2"] == 2 and c["tseed_4"] == 4 for c in checks)
        out[dens] = dict(n_trials=int(len(EV)), n_events=int(evn), pairing_ok=pair_ok,
                         pairing_failures=[c for c in checks if not (c["evstats_identical"] and c["ev_identical"]
                                                                       and c["pv_allclose"] and c["seed_equal"])],
                         pv_bit_equal_all=all(c["pv_equal"] for c in checks), families=fam, per_rung_diag=diag)
    tests = [(d, f, out[d]["families"][f]["z_paired"]) for d in out for f in FAMS]
    out["n_tests"] = len(tests)
    out["n_fail"] = sum(abs(z) >= ZMAX for _, _, z in tests)
    out["verdict"] = "PASS" if out["n_fail"] == 0 and all(out[d]["pairing_ok"] for d in ("rho1", "rho2")) else "FAIL"
    return out


def main(dst):
    rng = np.random.default_rng(SEED)
    res = dict(definition=__doc__, C2b=c2b(), C2c=c2c(rng))
    Path(dst).write_text(json.dumps(res, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    log.info("C2-b %s; C2-c %s (%d of %d tests fail)", res["C2b"]["verdict"], res["C2c"]["verdict"], res["C2c"]["n_fail"],
             res["C2c"]["n_tests"])


if __name__ == "__main__":
    main(sys.argv[1])
