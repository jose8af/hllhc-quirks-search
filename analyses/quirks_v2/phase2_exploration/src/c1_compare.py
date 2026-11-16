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


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--nboot", type=int, default=500)
    ap.add_argument("--pu1", default="p2-a-c1-pu1")
    ap.add_argument("--pu2", default="p2-a-c1-pu2")
    a = ap.parse_args()
    rng = np.random.default_rng(20261116)
    res = dict(n_declared=N_DECL, bonferroni_p=0.05 / N_DECL, entries={}, samples={}, families={})
    cols = [R[k] for k in ("R04", "R05", "R06", "R07", "R08", "R09")]
    f1 = done_outputs(a.pu1)
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
    f2 = done_outputs(a.pu2)
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
    # family coherence and global
    fam = {}
    for k, e in res["entries"].items():
        if e.get("test") == "log-ratio z":
            fam.setdefault(k.split(".")[0], []).append((np.log(e["v2"]) - np.log(e["v1"]), np.hypot(e["v1_s_ln"],
                                                                                                     e["v2_s_ln"])))
    for f, v in fam.items():
        d = np.array([x for x, _ in v]); s = np.array([x for _, x in v])
        w = 1 / s ** 2
        mu = float((w * d).sum() / w.sum()); smu = float(1 / np.sqrt(w.sum()))
        res["families"][f] = dict(n=len(v), mean_ln_ratio=mu, s=smu, z=mu / smu, coherent=bool(abs(mu / smu) < 3))
    zs = [e["z"] for e in res["entries"].values() if np.isfinite(e.get("z", np.nan))]
    res["individual_fail"] = [k for k, e in res["entries"].items() if e["p"] <= 0.05 / N_DECL]
    res["global_partial"] = dict(n_available=len(zs), sum_z2=float(np.sum(np.square(zs))),
                                 chi2_99_at_n_available=float(stats.chi2.ppf(0.99, max(1, len(zs)))),
                                 note="the global test of STR §4.1 uses all 41 quantities; partial value only")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.part")
    tmp.write_text(json.dumps(res, indent=1, default=str) + "\n")
    tmp.replace(OUT)
    for k, e in res["entries"].items():
        log.info("%-10s v1 %-12s v2 %-14s p %.3g", k, e["v1"], e["v2"] if isinstance(e["v2"], str) else f"{e['v2']:.5g}",
                 e["p"])
    log.info("families: %s", json.dumps(res["families"]))


if __name__ == "__main__":
    main()
