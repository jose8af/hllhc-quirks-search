"""c1_compare.py -- C1 comparison of v2 outputs with the tracked v1 values (channel (i), Rosalie, 2026-11-16).

Statistics fixed in STR §4.1 "Within statistical errors" (COM C1-a):
  counts >= 10: z = (ln x2 - ln x1) / sqrt(s1^2 + s2^2), s2 from the event bootstrap (trials of one event together);
  smaller counts: exact conditional binomial test of two Poisson counts with known exposures (two-sided);
  k/n efficiencies: Fisher exact (two-sided).  Individual pass p > 0.05/41; global sum z^2 < chi2_41 99th percentile;
  family coherence: inverse-variance mean of ln(x2/x1) per family, |z| < 3.  Power (2 sigma detectable shift) stated.
v1 values: STR §4.1 table (from D4 §5.2, D4 §2.3 and §3.1) with the v1 statistical widths quoted there.

Families implemented here (others are added as their samples finish; each prints "NOT YET" until then):
  pu1  rho = 1 groups per trial at R04, R05, R06 (mean of trials.n_grp), R07 count; R08, R09 zero counts
  pu2  rho = 2 <S_ded> per trial at R04, R05, R06
  clos T1 (R04) and T1w (R05) = (rho = 1 groups per trial) / (rho = 2 <S_ded> per trial)
BLINDING: this script reads no signal file in this version.  The signal open tier (R04 x 3, R06 at E 200 1.5 keV) and
the sealed branch are added in a separate function that reads only those columns (see the session log).
Output: phase2_exploration/outputs/c1_compare.json (atomic).  Run on a worker with the TT env python.

Families added by Ignatius (2026-11-18); every v2 number comes from v1's own analysis functions (QV2 copies, unchanged):
  clos.slope, clos.cfac  (i) closure trend slope (background.closure -> analyse_g3.trend_test, ladder R04-R14, points with
        >= 10 B1 counts) and the factorisation c-factor (analyse_g3.c_test -> c_max.c); B1 = pu1, B2 = pu2, nboot 1000,
        rng C.SEED as run_all.  slope: z = (b2 - b1)/sqrt(s1^2 + s2^2) with the joint event-bootstrap sigmas (a slope is
        not a ratio); in the family coherence it enters as ln(b2/b1) with s/|b|.  c: log-ratio z with the bootstrap s_c.
  cp0.<t> (ii) C'0 f_pre = n_pre / n_c0 for dif, ni22, pvpair (cprime_term's n_pre/n_c0; v1 background.json cprime);
        Fisher exact on the 2x2 table (STR: efficiencies k/n), signed z from p.
  cppu.<t>.<R> (iii) C'_PU attributed candidates per slot at R04, R05 (dif, gamma, v0) and R02 (pvpair): cprime_term's
        factor "C'_PU attributed P(R) direct" N/M and its bootstrap s_ln (clustered by source C'0 event); v1 per 500 slots.
  rates.<x> (iv) rates per preselected event (max over SM processes, normalise.build): dif, pvpair, gamma; N_trig total
        and N_trig(Z(nunu)); v2 from p2-a-c1-gen2 through v1 normalise.build.  Widths: N_trig and N_trig(Z) as v1
        (rel_stat); rates: v1 recorded none (sigma_ln = 0) -> ESTIMATE from the v2 run, s_ln = sqrt(D r / N_eff) / r
        (N_eff = sum_w^2/sum_w2 of the max process; D = 1 for dif-HS, 2 for gamma (photon pairs from pi0), 2 sqrt(2 r) + 1
        for PV pairs (pairs of a Poisson multiplicity); dif adds the min-bias term, rel 1/sqrt(objects) as gen_d123), the
        same width assumed for v1 (same generator, same sizes).  DECISION in experiment_log (2026-11-18, Ignatius).
  sm.<R> (v) Z(nunu) HS candidates per event (presel-weighted) at R04-R06: sm_term's factor "HS cand P(R) direct
        (presel-weighted)" N/M (STR's 19.52 / 4.51 / 0.0162) and s_ln; needs the smregen weights (p2-a-c1-smregen).
"""
import argparse
import json
import logging
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
MARK = QV2 / "ledger" / "markers"
OUT = HERE.parent / "outputs" / "c1_compare.json"
log = logging.getLogger("c1_compare")
N_DECL = 41
R = dict(R04=3, R05=4, R06=5, R07=6, R08=7, R09=8)      # column of acts/stage4/finder/production.RUNGS
V1 = {   # value, s_ln (v1 statistical width), source
    "pu1.R04": (171.55, 0.0056, "D4 §5.2 B1 (columns[3].B1_per_trial)"),
    "pu1.R05": (49.72, 0.0062, "D4 §5.2 B1"),
    "pu1.R06": (0.2470, 0.010, "D4 §5.2 B1 (s_ln ≈ 0.01 [E] there)"),
    "pu1.R07": (35, 48000, "D4 §2.3: 35 groups / 48,000 trials"),
    "pu1.R08": (0, 48000, "D4 §2.3: 0 / 48,000"),
    "pu1.R09": (0, 48000, "D4 §2.3: 0 / 48,000"),
    "pu2.R04": (114.36, 0.0077, "D4 §2.3 B2 <S_ded>/trial (s_ln boot)"),
    "pu2.R05": (30.96, 0.0079, "D4 §2.3"),
    "pu2.R06": (0.389, 0.0060, "D4 §2.3"),
    "clos.T1": (1.5001, 0.0097, "D4 §3.1 closure.T1 (s_ln = sqrt(0.0077^2 + 0.0056^2))"),
    "clos.T1w": (1.6061, 0.0100, "D4 §3.1 closure.T1w (s_ln = sqrt(0.0079^2 + 0.0062^2))"),
}


def done_outputs(camp, suffix=".npz", exclude=".premerge.npz"):
    paths = []
    for p in sorted((MARK / camp).glob("*/*.marker")):
        done = None
        for line in p.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("status") == "done":
                done = d
        if done:
            paths += [o["path"] for o in done["outputs"] if o["name"].endswith(suffix) and not o["name"].endswith(exclude)]
    return paths


def load_trials(paths, key, cols):
    """per-event sums of trials.<key>[:, cols] and trial counts per event (event = (file, ev))."""
    sums, ntr = [], []
    for p in paths:
        with np.load(p, allow_pickle=False) as z:
            x = z["trials." + key][:, cols].astype(np.float64)
            ev = z["trials.ev"]
        u, inv = np.unique(ev, return_inverse=True)
        s = np.zeros((len(u), len(cols)))
        np.add.at(s, inv, x)
        sums.append(s)
        ntr.append(np.bincount(inv, minlength=len(u)))
    return np.concatenate(sums), np.concatenate(ntr).astype(np.float64)


def boot_mean(sums, ntr, nboot, rng):
    n = len(ntr)
    mean = sums.sum(0) / ntr.sum()
    b = np.empty((nboot, sums.shape[1]))
    for i in range(nboot):
        k = rng.integers(0, n, n)
        b[i] = sums[k].sum(0) / ntr[k].sum()
    return mean, b


def z_entry(name, x2, s2, nboot_note=""):
    x1, s1, src = V1[name]
    z = (np.log(x2) - np.log(x1)) / np.hypot(s1, s2) if x2 > 0 else float("nan")
    p = 2 * stats.norm.sf(abs(z)) if np.isfinite(z) else float("nan")
    return dict(v1=x1, v1_s_ln=s1, v1_source=src, v2=float(x2), v2_s_ln=float(s2), z=float(z), p=float(p),
                mde_2sigma=float(np.expm1(2 * np.hypot(s1, s2))), test="log-ratio z", note=nboot_note)


def poisson_entry(name, k2, t2):
    k1, t1, src = V1[name]
    n = k1 + k2
    if n == 0:
        p = 1.0
    else:   # conditional binomial: k2 ~ Bin(n, t2 / (t1 + t2)) under equal rates
        p = float(stats.binomtest(int(k2), int(n), t2 / (t1 + t2)).pvalue)
    return dict(v1=f"{k1}/{t1}", v1_source=src, v2=f"{k2}/{t2:.0f}", p=p, z=float(stats.norm.isf(p / 2)) if p < 1 else 0.0,
                test="conditional binomial (Poisson counts, trial exposures)",
                gross_check_only=bool(n < 30))


import sys  # noqa: E402

sys.path.insert(0, str(QV2))
TT1 = Path("/home/users/jdochoa/hllhc-quirks-search/stage2_C001_quirks/theory_track")
V1BG = TT1 / "data/acts_stage4/analysis/C12FC_v1/background.json"
V1NORM = TT1 / "acts/stage4/analysis/inputs/normalisation.json"
DATA = Path("/nfs/cajuela/jdochoa/quirks_v2/data/phase2")


def signed_exact(name, p, sign, v1, v2, test, **kw):
    z = float(np.sign(sign) * stats.norm.isf(p / 2)) if p < 1 else 0.0
    return dict(v1=v1, v2=v2, p=float(p), z=z, test=test, v1_source=name, **kw)


def lr_entry(v1, s1, v2, s2, src, **kw):
    z = (np.log(v2) - np.log(v1)) / np.hypot(s1, s2) if (v1 > 0 and v2 > 0) else float("nan")
    p = 2 * stats.norm.sf(abs(z)) if np.isfinite(z) else float("nan")
    return dict(v1=float(v1), v1_s_ln=float(s1), v1_source=src, v2=float(v2), v2_s_ln=float(s2), z=float(z), p=float(p),
                mde_2sigma=float(np.expm1(2 * np.hypot(s1, s2))), test="log-ratio z", **kw)


def load_npz(p, keys=(), prefixes=()):
    with np.load(p, allow_pickle=False) as z:
        d = {k: z[k] for k in z.files if k in keys or any(k.startswith(x) for x in prefixes)}
        d["meta"] = json.loads(str(z["meta_json"]))
    return d


def fam_closure_extra(res, a, rng_seed):
    """(i) trend slope and c-factor with v1's functions on pu1 (B1) and pu2 (B2)."""
    from acts.stage4.analysis import background as BG
    from acts.stage4.analysis import common as C
    from acts.stage4.g3 import analyse_g3 as G3
    f1, f2 = done_outputs(a.pu1), done_outputs(a.pu2)
    if not (f1 and f2):
        return
    def jobs(paths, rho):
        out = []
        for p in paths:
            d = load_npz(p, keys=["job_id"] + ["trials." + k for k in BG.TR_KEYS] + (["cand." + k for k in ("tag", "trial",
                                                                                                          "rungs", "cross")]
                                                                                    if rho == 1 else []))
            tr = {k: d["trials." + k] for k in BG.TR_KEYS if "trials." + k in d}
            j = dict(tr=tr, job=d["meta"]["job"], job_id=str(d["job_id"]), meta=d["meta"], path=p)
            if rho == 1:   # c_test uses only loose F0 candidates: keep those (same mask as c_test, memory)
                F0 = np.unpackbits(d["cand.rungs"][:, :1], axis=1)[:, 0].astype(bool)
                m = ((d["cand.tag"] & 2) > 0) & F0
                j["cand"] = {k: d["cand." + k][m] for k in ("tag", "trial", "rungs", "cross")}
            out.append(j)
        return out
    b1, b2 = jobs(f1, 1), jobs(f2, 2)
    rng = np.random.default_rng(rng_seed)
    S = BG.PUSamples(b1, b2, a.nboot_v1, rng)
    cl = BG.closure(S, rng, a.nboot_v1)
    G3c = G3.c_test([dict(cand=d["cand"], tr=d["tr"]) for d in b1], rng)
    v1 = json.loads(V1BG.read_text())
    t1, t2 = v1["closure"]["trend"], cl["trend"]
    res["v2_closure_detail"] = dict(trend=t2, c_test={k: v for k, v in G3c.items()}, T1=cl["T1"].get("ratio"),
                                    T1w=cl["T1w"].get("ratio"), trials=dict(B1=int(S.n1()), B2=int(S.n2())))
    if t2.get("slope") is not None:
        b1_, s1 = t1["slope"], t1["s_slope_boot"]; b2_, s2 = t2["slope"], t2["s_slope_boot"]
        z = (b2_ - b1_) / np.hypot(s1, s2)
        res["entries"]["clos.slope"] = dict(v1=b1_, v1_s=s1, v2=b2_, v2_s=s2, z=float(z), p=float(2 * stats.norm.sf(abs(z))),
                                            test="difference z (joint event-bootstrap sigmas)",
                                            v1_points=[p["rung"] for p in t1["points"]],
                                            v2_points=[p["rung"] for p in t2["points"]],
                                            v1_source="v1 background.json closure.trend (slope, s_slope_boot)",
                                            coh=(float(np.log(b2_ / b1_)) if b1_ * b2_ > 0 else None,
                                                 float(np.hypot(s1 / abs(b1_), s2 / abs(b2_)))))
    else:
        res["entries"]["clos.slope"] = dict(v1=t1["slope"], v2=None, p=float("nan"), z=float("nan"),
                                            test="NOT TESTABLE", note=t2.get("note"))
    c1v, c2v = v1["c_test"]["c_max"], G3c.get("c_max")
    if c2v:
        res["entries"]["clos.cfac"] = lr_entry(c1v["c"], c1v["s_c"] / c1v["c"], c2v["c"], c2v["s_c"] / c2v["c"],
                                               "v1 background.json c_test.c_max (c, s_c)",
                                               v1_cell=dict(bin=c1v["bin"], layers=c1v["layers"]),
                                               v2_cell=dict(bin=c2v["bin"], layers=c2v["layers"]))
    _ = C


def cp_jobs(camp):
    out = []
    for p in done_outputs(camp):
        d = load_npz(p, keys=("job_id", "trials.ev", "cp.ev", "cp.ev_cols"), prefixes=("cp.cand.",))
        out.append(dict(job=d["meta"]["job"], meta=d["meta"], d_cp=d, tr={"ev": d.get("trials.ev", [])}, path=p))
    return out


def fam_cprime(res, a):
    """(ii) f_pre from C'0 and (iii) attributed C'_PU counts, both through v1 background.cprime_term."""
    from acts.stage4.analysis import background as BG
    from acts.stage4.analysis import common as C
    j0 = cp_jobs(a.cp0)
    if not j0:
        return
    jp = cp_jobs(a.cppua) + cp_jobs(a.cppub)
    cp = BG.cprime_term(j0, jp, {}, rng=np.random.default_rng(C.SEED), c_factor=1.0, spectra=None)
    v1 = json.loads(V1BG.read_text())["cprime"]
    res["samples"]["cp"] = {t: dict(n_c0=cp[t]["n_c0"], n_with_pu=cp[t]["n_with_pu"]) for t in cp}
    for t in ("dif", "ni22", "pvpair"):
        if t not in cp:
            continue
        k1, n1 = v1[t]["n_pre"], v1[t]["n_c0"]; k2, n2 = cp[t]["n_pre"], cp[t]["n_c0"]
        p = stats.fisher_exact([[k1, n1 - k1], [k2, n2 - k2]]).pvalue
        f1_, f2_ = k1 / n1, k2 / n2
        e = signed_exact(f"v1 background.json cprime.{t}.n_pre/n_c0", p, f2_ - f1_, f"{k1}/{n1}", f"{k2}/{n2}",
                         "Fisher exact (k/n)", v1_f=f1_, v2_f=f2_,
                         coh=(float(np.log(f2_ / f1_)), float(np.hypot(np.sqrt((1 - f1_) / k1), np.sqrt((1 - f2_) / k2)))))
        res["entries"][f"cp0.{t}"] = e
    want = {"dif": (3, 4), "gamma": (3, 4), "v0": (3, 4), "pvpair": (1,)}
    for t, cols in want.items():
        if t not in cp or cp[t]["n_with_pu"] == 0:
            continue
        for c in cols:
            def fac(row):
                fs = [f for f in row["factors"] if "attributed" in f["label"] and "direct" in f["label"]]
                return fs[0] if fs else None
            f1_, f2_ = fac(v1[t]["rows"][c]), fac(cp[t]["rows"][c])
            name = f"cppu.{t}.{C.RUNGS[c][:3]}"
            if f2_ is None:
                res["entries"][name] = dict(v1=f"{f1_['N']}/{f1_['M']}", v2=None, p=float("nan"), z=float("nan"),
                                            test="NOT TESTABLE (no direct v2 factor)",
                                            v2_factors=[f["label"] for f in cp[t]["rows"][c]["factors"]])
                continue
            if f2_["N"] >= 10 and f1_["N"] >= 10:
                res["entries"][name] = lr_entry(f1_["N"] / f1_["M"], f1_["s_ln_used"], f2_["N"] / f2_["M"],
                                                f2_["s_ln_used"], f"v1 background.json cprime.{t}.rows[{c}] attributed direct",
                                                v1_counts=f"{f1_['N']:.0f}/{f1_['M']:.0f}",
                                                v2_counts=f"{f2_['N']:.0f}/{f2_['M']:.0f}")
            else:
                pb = float(stats.binomtest(int(f2_["N"]), int(f1_["N"] + f2_["N"]), f2_["M"] / (f1_["M"] + f2_["M"])).pvalue)
                res["entries"][name] = signed_exact(f"v1 cprime.{t}", pb, f2_["N"] / f2_["M"] - f1_["N"] / f1_["M"],
                                                    f"{f1_['N']:.0f}/{f1_['M']:.0f}", f"{f2_['N']:.0f}/{f2_['M']:.0f}",
                                                    "conditional binomial")


def fam_rates(res, a):
    """(iv) rates and N_trig through v1 normalise.build on the merged c1-gen2 per-process JSONs."""
    paths = done_outputs(a.gen, suffix=".json", exclude=".none")
    if not paths:
        return
    from acts.stage4.analysis import normalise as NM
    gen = dict(processes={}, minbias=None)
    for p in paths:
        d = json.loads(Path(p).read_text())
        gen.setdefault("bins_pt", d["bins_pt"]); gen.setdefault("proxies", d["proxies"])
        if "minbias" in d:
            gen["minbias"] = d["minbias"]
        else:
            gen["processes"].update(d["processes"])
    need = set(NM.EXTRA_K) | {"Znunu_j", "Wtaunu_j", "Wtauhnu_j", "Wenu_j", "Wmunu_j", "ttbar_1l"}
    if gen["minbias"] is None or not need <= set(gen["processes"]):
        res["entries"]["rates.status"] = dict(v1=None, v2=None, p=float("nan"), z=float("nan"), test="NOT YET",
                                              note=f"have {sorted(gen['processes'])}, minbias {gen['minbias'] is not None}")
        return
    proc, ntot, rel, rates, _ = NM.build(gen)
    v1 = json.loads(V1NORM.read_text())
    res["v2_normalisation"] = dict(N_trig=ntot, rel_stat=rel, breakdown={k: v.get("N_trig") for k, v in proc.items()},
                                   rates={k: dict(value=v["value"], per_process=v["per_process"]) for k, v in rates.items()},
                                   processes={k: {x: gen["processes"][k][x] for x in ("n_acc", "sigma_MET200_pb",
                                                                                       "f_presel_weighted", "sum_w",
                                                                                       "sum_w2", "seconds")}
                                              for k in gen["processes"]},
                                   minbias_per_PU200=gen["minbias"]["per_PU200_event"])
    res["entries"]["rates.ntrig"] = lr_entry(v1["n_trig"]["value"], v1["n_trig"]["rel_stat"], ntot, rel,
                                             "v1 normalisation.json n_trig (value, rel_stat)")
    res["entries"]["rates.ntrig_Z"] = lr_entry(v1["sm_processes"]["Znunu_j"]["N_trig"], v1["sm_processes"]["Znunu_j"]["rel_stat"],
                                               proc["Znunu_j"]["N_trig"], proc["Znunu_j"]["rel_stat"],
                                               "v1 normalisation.json sm_processes.Znunu_j (N_trig, rel_stat)")
    mb = gen["minbias"]
    for t, D in (("dif", 1.0), ("pvpair", None), ("gamma", 2.0)):
        per = rates[t]["per_process"]; pmax = max(per, key=lambda k: per[k]); r = per[pmax]
        P = gen["processes"][pmax]
        neff = P["sum_w"] ** 2 / P["sum_w2"] if P["sum_w2"] > 0 else 1.0
        if t == "dif":
            rhs = (P["rates_per_presel_event"].get("dif") or 0.0)
            var = D * rhs / neff + (mb["per_PU200_event"]["dif"] * mb["rel_stat"]["dif"]) ** 2
        elif t == "pvpair":
            var = (2 * np.sqrt(2 * r) + 1) * r / neff
        else:
            var = D * r / neff
        s = float(np.sqrt(var) / r)
        v1r = v1["cprime_rates"][t]
        res["entries"][f"rates.{t}"] = lr_entry(v1r["value"], s, r, s, f"v1 normalisation.json cprime_rates.{t}.value "
                                                "(v1 width not recorded: v2 ESTIMATE used for both)",
                                                v1_max_process=max(v1r["per_process"], key=lambda k: v1r["per_process"][k]),
                                                v2_max_process=pmax, n_eff=neff, width_tag="ESTIMATE")


def fam_sm(res, a):
    """(v) Z(nunu) HS candidates per event through v1 background.sm_term with the smregen weights."""
    from acts.stage4.analysis import background as BG
    from acts.stage4.analysis import common as C
    rg = done_outputs(a.smregen, suffix=".json", exclude=".none")
    fs = done_outputs(a.sm)
    if not (rg and fs):
        return
    regen = {}
    for p in rg:
        regen.update({k: v for k, v in json.loads(Path(p).read_text()).items() if not k.startswith("_")})
    jobs = []
    for p in fs:
        d = load_npz(p, keys=["job_id"] + ["trials." + k for k in BG.TR_KEYS] + ["cand." + k for k in BG.B1_CAND_KEYS])
        job = dict(d["meta"]["job"]); job["sample"] = "C_" + job.get("sm_sample", "Znunu_j")   # SM_PSEUDO naming of v1
        jobs.append(dict(tr={k: d["trials." + k] for k in BG.TR_KEYS if "trials." + k in d},
                         cand={k: d["cand." + k] for k in BG.B1_CAND_KEYS if "cand." + k in d},
                         job=job, job_id=str(d["job_id"]), meta=d["meta"], path=p))
    sm = BG.sm_term(jobs, {"Znunu_j": dict(sigma_pb=1.0, K=1.0)}, 1.0, regen, rng=np.random.default_rng(C.SEED))
    if "_error" in sm:
        res["entries"]["sm.status"] = dict(v1=None, v2=None, p=float("nan"), z=float("nan"), test="REFUSED", note=sm["_error"])
        return
    v1 = json.loads(V1BG.read_text())["sm"]["Znunu_j"]
    res["samples"]["sm"] = dict(n_class_events=sm["Znunu_j"]["n_class_events"], f_presel=sm["Znunu_j"]["f_presel_class"],
                                regen_met_match=sum(r["n_met_match"] for r in regen.values()),
                                regen_n=sum(r["n"] for r in regen.values()),
                                n_hs_cand_R04_unweighted=sm["Znunu_j"]["n_hs_cand_R04"],
                                v1_n_hs_cand_R04_unweighted=v1["n_hs_cand_R04"], v1_f_presel=v1["f_presel_class"],
                                n_events_w_gt0=int(sum(1 for r in regen.values() for x in r["rows"] if x["w_presel"] > 0)))
    for c in (3, 4, 5):
        def fac(row):
            return [f for f in row["factors"] if f["label"].startswith("HS cand") and "direct" in f["label"]][0]
        f1_, f2_ = fac(v1["rows"][c]), fac(sm["Znunu_j"]["rows"][c])
        res["entries"][f"sm.{C.RUNGS[c][:3]}"] = lr_entry(f1_["N"] / f1_["M"], f1_["s_ln_used"], f2_["N"] / f2_["M"],
                                                          f2_["s_ln_used"], f"v1 background.json sm.Znunu_j.rows[{c}] HS cand direct",
                                                          v1_counts=f"{f1_['N']:.1f}/{f1_['M']:.0f}",
                                                          v2_counts=f"{f2_['N']:.1f}/{f2_['M']:.0f}")


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--nboot", type=int, default=500)
    ap.add_argument("--pu1", default="p2-a-c1-pu1")
    ap.add_argument("--pu2", default="p2-a-c1-pu2")
    ap.add_argument("--nboot-v1", type=int, default=1000, help="closure/trend/c-test bootstrap (run_all default)")
    ap.add_argument("--cp0", default="p2-a-c1-cp0")
    ap.add_argument("--cppua", default="p2-a-c1-cppua")
    ap.add_argument("--cppub", default="p2-a-c1-cppub")
    ap.add_argument("--gen", default="p2-a-c1-gen2")
    ap.add_argument("--sm", default="p2-a-c1-sm")
    ap.add_argument("--smregen", default="p2-a-c1-smregen")
    ap.add_argument("--families", default="pu,closure,cprime,rates,sm",
                    help="subset to run (pu = pu1/pu2/T1/T1w of Rosalie; closure = slope and c-factor)")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    fams = set(a.families.split(","))
    rng = np.random.default_rng(20261116)
    res = dict(n_declared=N_DECL, bonferroni_p=0.05 / N_DECL, entries={}, samples={}, families={})
    cols = [R[k] for k in ("R04", "R05", "R06", "R07", "R08", "R09")]
    f1 = done_outputs(a.pu1) if "pu" in fams else []
    g1 = None
    if f1:
        s, n = load_trials(f1, "n_grp", cols)
        m, b = boot_mean(s, n, a.nboot, rng)
        g1 = (s, n, m, b)
        res["samples"]["pu1"] = dict(campaign=a.pu1, files=len(f1), events=int(len(n)), trials=int(n.sum()))
        for i, r in enumerate(("R04", "R05", "R06")):
            res["entries"][f"pu1.{r}"] = z_entry(f"pu1.{r}", m[i], float(np.std(np.log(b[:, i]), ddof=1)))
        for i, r in ((3, "R07"), (4, "R08"), (5, "R09")):
            res["entries"][f"pu1.{r}"] = poisson_entry(f"pu1.{r}", int(round(s[:, i].sum())), float(n.sum()))
    f2 = done_outputs(a.pu2) if "pu" in fams else []
    if f2:
        s2, n2 = load_trials(f2, "S_ded", cols[:3])
        m2, b2 = boot_mean(s2, n2, a.nboot, rng)
        res["samples"]["pu2"] = dict(campaign=a.pu2, files=len(f2), events=int(len(n2)), trials=int(n2.sum()))
        for i, r in enumerate(("R04", "R05", "R06")):
            res["entries"][f"pu2.{r}"] = z_entry(f"pu2.{r}", m2[i], float(np.std(np.log(b2[:, i]), ddof=1)))
        if g1 is not None:
            for i, t in ((0, "T1"), (1, "T1w")):
                ratio = g1[2][i] / m2[i]
                sl = float(np.hypot(np.std(np.log(g1[3][:, i]), ddof=1), np.std(np.log(b2[:, i]), ddof=1)))
                res["entries"][f"clos.{t}"] = z_entry(f"clos.{t}", ratio, sl)
    if "closure" in fams:
        fam_closure_extra(res, a, 20261014)
    if "cprime" in fams:
        fam_cprime(res, a)
    if "rates" in fams:
        fam_rates(res, a)
    if "sm" in fams:
        fam_sm(res, a)
    # family coherence and global (family = first part of the entry name; pu1/pu2/clos as Rosalie, cp0, cppu, rates, sm)
    fam = {}
    for k, e in res["entries"].items():
        if e.get("test") == "log-ratio z":
            fam.setdefault(k.split(".")[0], []).append((np.log(e["v2"]) - np.log(e["v1"]), np.hypot(e["v1_s_ln"],
                                                                                                     e["v2_s_ln"])))
        elif e.get("coh") and e["coh"][0] is not None:
            fam.setdefault(k.split(".")[0], []).append(tuple(e["coh"]))
    for f, v in fam.items():
        d = np.array([x for x, _ in v]); s = np.array([x for _, x in v])
        w = 1 / s ** 2
        mu = float((w * d).sum() / w.sum()); smu = float(1 / np.sqrt(w.sum()))
        res["families"][f] = dict(n=len(v), mean_ln_ratio=mu, s=smu, z=mu / smu, coherent=bool(abs(mu / smu) < 3))
    zs = [e["z"] for e in res["entries"].values() if np.isfinite(e.get("z", np.nan))]
    res["individual_fail"] = [k for k, e in res["entries"].items() if e["p"] <= 0.05 / N_DECL]
    res["not_testable"] = [k for k, e in res["entries"].items() if not np.isfinite(e.get("p", np.nan))]
    res["global_partial"] = dict(n_available=len(zs), sum_z2=float(np.sum(np.square(zs))),
                                 chi2_99_at_n_available=float(stats.chi2.ppf(0.99, max(1, len(zs)))),
                                 note="the global test of STR §4.1 uses all 41 quantities; partial value only")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.part")
    tmp.write_text(json.dumps(res, indent=1, default=str) + "\n")
    tmp.replace(out)
    for k, e in res["entries"].items():
        v2 = e["v2"] if isinstance(e["v2"], str) or e["v2"] is None else f"{e['v2']:.5g}"
        log.info("%-16s v1 %-14s v2 %-14s z %+.2f p %.3g", k, e["v1"], v2, e.get("z", float("nan")), e["p"])
    log.info("families: %s", json.dumps(res["families"]))


if __name__ == "__main__":
    main()
