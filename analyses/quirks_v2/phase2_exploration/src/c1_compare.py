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

Width fix (fix agent Lisbet, 2026-11-18; REGRESSION_TICKET_SM.md, advisor ruling in LOG.md 2026-11-18 12:29):
  The s_ln_used of a v1 "direct" factor is 1/sqrt(N) on CANDIDATES (background.Term.evaluate l.205), which ignores that
  candidates come in clusters (~47 per SM event; several per C'_PU source event).  sm.<R> and cppu.<t>.<R> now take
  the v2 width from a cluster bootstrap of ln(sum N / sum M) (SM: per event, x_e = w_presel x n_cand, events without a
  candidate included; C'_PU: per source C'0 event, slots as denominator), all rungs of a sample from the same resamples.
  v1 width (per-cluster counts lost): primary = v1 1/sqrt(N) x (v2 bootstrap / v2 1/sqrt(N)); alternative = 0, both
  reported.  Family coherence and the global chi2 use the joint replicas (joint_family).  The SM 1/sqrt(N) path is kept
  only as res["frozen_script"] (the FAIL on record); C'_PU has no 1/sqrt(N) verdict.  C'_PU entries with N < 10 keep the
  frozen conditional binomial, flagged.  SM verdicts with the fixed width are amendment E4 (pending the user's approval).
  Unit tests: test_c1_compare.py (synthetic clustered data).

Joint replicas for pu1, pu2, clos (executor Mattias, 2026-11-19; orchestrator decision LOG.md 2026-11-18 12:37 (b)):
  the family coherence of pu1 (R04-R06), pu2 (R04-R06) and clos (T1, T1w, slope, c-factor) is computed by joint_family
  on ONE set of paired event resamples of pu1 and pu2 (PUSamples bi1/bi2, the resamples of the v1 trend width), so
  nested rungs and shared events keep their correlation (pu_joint).  Individual entries unchanged.  The frozen
  independent-entry coherence is kept as families[f]["frozen_script_independent"].  Tests: TestPUJoint.
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
    mde = float(np.expm1(2 * np.hypot(s1, s2)))      # 2 sigma power: the shift of ln x detectable at 2 sigma (STR §4.1 item 4)
    return dict(v1=float(v1), v1_s_ln=float(s1), v1_source=src, v2=float(v2), v2_s_ln=float(s2), z=float(z), p=float(p),
                mde_2sigma=mde, gross_check_only=bool(mde > 0.5), test="log-ratio z", **kw)


# ---------------------------------------------------------------------------------------------------------------------
# Clustered widths (fix agent Lisbet, 2026-11-18; REGRESSION_TICKET_SM.md §3, advisor ruling LOG.md 2026-11-18 12:29).
# Quantities counted per candidate (SM HS candidates per event, C'_PU attributed candidates per slot) are ratios
# sum_c N_c / sum_c M_c over clusters c (SM: the event; C'_PU: the source C'0 event).  Their width is the cluster
# bootstrap of ln(sum N / sum M); all rungs of one sample use the SAME resamples (joint replicas), so the nested rungs
# keep their correlation in the family coherence and in the global chi2.  v1 per-cluster counts are lost: the v1 width
# is v1's own 1/sqrt(N) times the v2 ratio (bootstrap / Poisson) of the same entry (primary), and 0 (strict bound).
# ---------------------------------------------------------------------------------------------------------------------
V1W_PRIMARY = "v1 1/sqrt(N) x (v2 cluster-bootstrap s_ln / v2 1/sqrt(N)) of the same entry [ESTIMATE]"
V1W_ZERO = "v1 width = 0 (strict bound)"


def cluster_boot_ln(N, M, nboot, rng, chunk=100):
    """Joint cluster bootstrap of ln(sum N / sum M).  N: (C, K) per-cluster numerators (K rungs), M: (C,) denominators.
    -> (estimate (K,), replicas (nboot', K) of ln ratio, n_dropped).  Replicas with a zero numerator in any column are
    dropped (jointly) and counted."""
    N = np.asarray(N, float).reshape(len(N), -1); M = np.asarray(M, float)
    C_ = len(M)
    est = N.sum(0) / M.sum()
    reps = np.empty((nboot, N.shape[1]))
    done = 0
    while done < nboot:
        k = min(chunk, nboot - done)
        idx = rng.integers(0, C_, size=(k, C_))
        W = np.zeros((k, C_))
        np.add.at(W, (np.repeat(np.arange(k), C_), idx.ravel()), 1.0)    # multiplicity of every cluster per replica
        with np.errstate(divide="ignore"):
            reps[done:done + k] = np.log((W @ N) / (W @ M)[:, None])
        done += k
    ok = np.all(np.isfinite(reps), axis=1)
    return est, reps[ok], int((~ok).sum())


def v1_width_scaled(s1_poisson, s2_boot, s2_poisson):
    """Primary v1 width rule: v1's 1/sqrt(N) scaled by the v2 clustering inflation of the same entry."""
    return float(s1_poisson * s2_boot / s2_poisson)


def clustered_entry(f1_, f2_, s2_boot, n_drop, src, **kw):
    """Log-ratio z with the cluster-bootstrap v2 width and both v1-width choices (primary: scaled; alternative: 0)."""
    s1p, s2p = f1_["s_ln_used"], f2_["s_ln_used"]                  # 1/sqrt(N) of v1 Term.evaluate (Poisson on candidates)
    x1, x2 = f1_["N"] / f1_["M"], f2_["N"] / f2_["M"]
    s1 = v1_width_scaled(s1p, s2_boot, s2p)
    e = lr_entry(x1, s1, x2, s2_boot, src, v1_width_rule=V1W_PRIMARY, v2_width="cluster bootstrap (joint replicas)",
                 v1_s_ln_poisson=float(s1p), v2_s_ln_poisson=float(s2p), inflation_v2=float(s2_boot / s2p),
                 n_boot_dropped=n_drop, **kw)
    z0 = lr_entry(x1, 0.0, x2, s2_boot, src)
    e["v1_width_zero"] = {k: z0[k] for k in ("v1_s_ln", "z", "p", "mde_2sigma", "gross_check_only")}
    e["v1_width_zero"]["v1_width_rule"] = V1W_ZERO
    return e


def joint_family(d, s1, reps_by_group):
    """Family coherence and decorrelated chi2 with the joint replicas.
    d: ln(x2/x1) per entry (K,); s1: v1 widths (K,); reps_by_group: list of (entry indices, replicas (B, k)) of
    independent samples.  Covariance: v2 from the replicas (zero between groups); v1 = D1 rho_v2 D1 (v1 rungs are nested
    on v1's events the same way; ESTIMATE).  Coherence: the frozen form (inverse-variance mean with the diagonal
    weights), its variance w'Sw/(sum w)^2 with the full covariance.  chi2 block: d' S^-1 d (chi2 with K dof)."""
    d = np.asarray(d, float); s1 = np.asarray(s1, float); K = len(d)
    S2 = np.zeros((K, K))
    for idx, r in reps_by_group:
        S2[np.ix_(idx, idx)] = np.atleast_2d(np.cov(r, rowvar=False, ddof=1))
    sd2 = np.sqrt(np.diag(S2))
    rho = S2 / np.outer(sd2, sd2)
    S = S2 + rho * np.outer(s1, s1)
    w = 1.0 / np.diag(S)
    mu = float(w @ d / w.sum()); smu = float(np.sqrt(w @ S @ w) / w.sum())
    chi2 = float(d @ np.linalg.solve(S, d))
    return dict(n=K, mean_ln_ratio=mu, s=smu, z=mu / smu, coherent=bool(abs(mu / smu) < 3), chi2_block=chi2,
                chi2_block_ndof=K, chi2_block_p=float(stats.chi2.sf(chi2, K)), correlation_v2=rho.round(4).tolist(),
                s_independent=float(1 / np.sqrt(w.sum())),
                method="joint replicas: diagonal inverse-variance weights, full covariance (v2 bootstrap + v1 scaled with "
                       "the v2 correlation)")


def coherence_naive(v):
    """Frozen-script family coherence (entries treated as independent)."""
    d = np.array([x for x, _ in v]); s = np.array([x for _, x in v])
    w = 1 / s ** 2
    mu = float((w * d).sum() / w.sum()); smu = float(1 / np.sqrt(w.sum()))
    return dict(n=len(v), mean_ln_ratio=mu, s=smu, z=mu / smu, coherent=bool(abs(mu / smu) < 3))


# ---------------------------------------------------------------------------------------------------------------------
# Joint replicas for the PU-derived families pu1, pu2, clos (executor Mattias, 2026-11-19; orchestrator decision LOG.md
# 2026-11-18 12:37 (b), made before the full read).  pu1.R04-R06 (nested rungs, same trials), pu2.R04-R06 (nested),
# clos.T1/T1w (= pu1/pu2 at R04/R05), clos.slope (v1 trend_test on the ln ratios at its points) and clos.cfac (v1
# c_test at the c_max cell, pu1 events) are all functions of the same pu1 and pu2 events.  The frozen script treated the
# entries of a family as independent in its coherence.  Here every entry is recomputed on ONE set of event resamples
# (pu1 row b paired with pu2 row b), so the family coherence (joint_family) carries the correlations.  The individual
# entries (values, widths, z, p) are NOT changed; the nominal values are recomputed from the per-event arrays and must
# reproduce the entries (checked).
# ---------------------------------------------------------------------------------------------------------------------
PU_JOINT_NAMES = ["pu1.R04", "pu1.R05", "pu1.R06", "pu2.R04", "pu2.R05", "pu2.R06", "clos.T1", "clos.T1w"]


def _counts(I, E):
    """(B, E) resample indices -> (B, E) multiplicities."""
    W = np.zeros((len(I), E))
    for b, row in enumerate(I):
        W[b] = np.bincount(row, minlength=E)
    return W


def pu_joint_stats(W1, W2, g1, n1, s2, n2, trend=None, cfac=None):
    """ln of the PU-derived C1 quantities for event multiplicities W1 (B, E1) of pu1 and W2 (B, E2) of pu2.
    g1 (E1, 3): pu1 per-event group sums at R04-R06, n1 (E1,): trials per event; s2 (E2, 3), n2 (E2,): pu2 S_ded sums.
    trend: dict(O (E1, k), P (E2, k), x (k,), w (k,)) = the points of v1 trend_test with its fixed weights; cfac:
    dict(n (E1,), J (E1,), S (E1, m)) = the c_max cell of v1 c_test.  -> (B, K) columns PU_JOINT_NAMES [+ clos.slope as
    ln|b|] [+ clos.cfac as ln c]."""
    m1 = (W1 @ g1) / (W1 @ n1)[:, None]
    m2 = (W2 @ s2) / (W2 @ n2)[:, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        cols = [np.log(m1), np.log(m2), np.log(m1[:, :2] / m2[:, :2])]
        if trend is not None:
            x, w = np.asarray(trend["x"], float), np.asarray(trend["w"], float)
            xm = np.sum(w * x) / np.sum(w)
            Y = np.log(((W1 @ trend["O"]) / (W1 @ n1)[:, None]) / ((W2 @ trend["P"]) / (W2 @ n2)[:, None]))
            b = np.sum(w * (x - xm) * Y, axis=1) / np.sum(w * (x - xm) ** 2)
            cols.append(np.log(np.abs(b))[:, None])
        if cfac is not None:
            Nb = W1 @ cfac["n"]
            c = (W1 @ cfac["J"]) / Nb / np.prod((W1 @ cfac["S"]) / Nb[:, None], axis=1)
            cols.append(np.log(c)[:, None])
    return np.concatenate(cols, axis=1)


def pu_joint_reps(g1, n1, s2, n2, I1, I2, trend=None, cfac=None, chunk=100):
    """Nominal (K,) and joint replicas (B', K) of pu_joint_stats over the paired resamples I1 (B, E1), I2 (B, E2);
    replicas with a non-finite column are dropped jointly (as trend_test drops O or P <= 0) and counted."""
    E1, E2 = len(n1), len(n2)
    nom = pu_joint_stats(np.ones((1, E1)), np.ones((1, E2)), g1, n1, s2, n2, trend, cfac)[0]
    reps = np.concatenate([pu_joint_stats(_counts(I1[i:i + chunk], E1), _counts(I2[i:i + chunk], E2), g1, n1, s2, n2,
                                          trend, cfac) for i in range(0, len(I1), chunk)])
    ok = np.all(np.isfinite(reps), axis=1)
    return nom, reps[ok], int((~ok).sum())


def cfac_event_arrays(jobs, cell):
    """Per-event arrays of v1 analyse_g3.c_test (same construction: loose F0 candidates with tag & 2, road-hit tercile
    bins over all trials, events numbered per job in np.unique order) for one cell dict(bin, layers).
    -> dict(n, J, S), number of events."""
    X, B, EV = [], [], []
    evn = 0
    q = np.quantile(np.concatenate([d["tr"]["n_road"] for d in jobs]), [1 / 3, 2 / 3])
    for d in jobs:
        c = d["cand"]
        F0 = np.unpackbits(c["rungs"][:, :1], axis=1)[:, 0].astype(bool)
        m = ((c["tag"] & 2) > 0) & F0
        X.append(c["cross"][m] >= 2)
        B.append(np.digitize(d["tr"]["n_road"][c["trial"][m]], q))
        ue, inv = np.unique(d["tr"]["ev"], return_inverse=True)
        EV.append(inv[c["trial"][m]] + evn); evn += len(ue)
    X = np.concatenate(X); B = np.concatenate(B); EV = np.concatenate(EV)
    mb = B == cell["bin"]
    Xe, Ee, L = X[mb], EV[mb], list(cell["layers"])
    return dict(n=np.bincount(Ee, minlength=evn).astype(float),
                J=np.bincount(Ee, weights=np.all(Xe[:, L], axis=1), minlength=evn),
                S=np.stack([np.bincount(Ee, weights=Xe[:, l], minlength=evn) for l in L], 1)), evn


def pu_joint(res):
    """Register the joint families pu1, pu2, clos (coherence with joint replicas) from the context left by the pu and
    closure families.  With the closure context: PUSamples resamples (bi1, bi2: the resamples of the slope width) for
    all entries; without it: the paired rows of the pu bootstrap (pu1, pu2, T1, T1w only)."""
    ctx = res.pop("_pu_ctx", {})
    E = res["entries"]
    if not all(n in E for n in PU_JOINT_NAMES):
        return
    if "S" in ctx:
        S = ctx["S"]
        g1, n1 = S.nobs_ev[:, 3:6], S.ntr1_ev
        s2, n2 = S.s2_ev[:, 3:6], S.ntr2_ev
        I1, I2 = S.bi1, S.bi2
        src = "PUSamples event resamples bi1/bi2 (nboot_v1, the resamples of the v1 trend width)"
    else:
        g1, n1, s2, n2 = ctx["g1"], ctx["n1"], ctx["s2"], ctx["n2"]
        I1, I2 = ctx["I1"], ctx["I2"]
        src = "pu bootstrap resamples (pu1 row b paired with pu2 row b)"
    names = list(PU_JOINT_NAMES)
    trend = cfac = None
    if "trend" in ctx and "clos.slope" in E and E["clos.slope"].get("v2") is not None:
        trend = ctx["trend"]; names.append("clos.slope")
    if "cfac" in ctx and "clos.cfac" in E:
        cfac = ctx["cfac"]; names.append("clos.cfac")
    nom, reps, ndrop = pu_joint_reps(g1, n1, s2, n2, I1, I2, trend, cfac)
    for j, n in enumerate(names):                   # the per-event arrays must reproduce every entry
        v2 = E[n]["v2"]
        if not np.isclose(np.exp(nom[j]), abs(v2), rtol=1e-9):
            raise RuntimeError(f"joint PU arrays do not reproduce {n}: {np.exp(nom[j])} vs {v2}")
    d, s1 = [], []
    for n in names:
        e = E[n]
        if n == "clos.slope":
            d.append(e["coh"][0]); s1.append(e["v1_s"] / abs(e["v1"]))
        else:
            d.append(float(np.log(e["v2"] / e["v1"]))); s1.append(e["v1_s_ln"])
        e["joint_family"] = n.split(".")[0]
    groups = {}
    for j, n in enumerate(names):
        groups.setdefault(n.split(".")[0], []).append(j)
    J = res.setdefault("_joint", {})
    for f, idx in groups.items():
        J[f] = dict(names=[names[j] for j in idx], groups=[(list(range(len(idx))), reps[:, idx])], clustered=False,
                    d=[d[j] for j in idx], s1=[s1[j] for j in idx], replicas_source=src, n_boot=int(len(reps)),
                    n_boot_dropped=ndrop)


def rung_col(label):
    """Ladder column of a 'P(Rxx_...) direct' factor label."""
    from acts.stage4.analysis import common as C
    name = label.split("P(", 1)[1].split(")", 1)[0]
    return C.RUNGS.index(name)


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
    # context for the joint replicas of pu1/pu2/clos (pu_joint): the same resamples as the trend width
    ctx = res.setdefault("_pu_ctx", {})
    ctx["S"] = S
    if t2.get("slope") is not None:
        pts = t2["points"]
        pc = [p["col"] for p in pts]
        ctx["trend"] = dict(O=S.nobs_ev[:, pc], P=S.s2_ev[:, pc], x=[p["x"] for p in pts],
                            w=[1 / p["sig"] ** 2 for p in pts])
    if c2v:
        cf, evn = cfac_event_arrays([dict(cand=d["cand"], tr=d["tr"]) for d in b1], c2v)
        if evn != S.E1:
            raise RuntimeError(f"c_test events {evn} != PUSamples B1 events {S.E1}")
        ctx["cfac"] = cf
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
    by_t = {}
    for d in jp:
        by_t.setdefault(d["job"]["topo"], []).append(d)
    names, groups, k0 = [], [], 0
    for t, cols in want.items():
        if t not in cp or cp[t]["n_with_pu"] == 0:
            continue
        def fac(row):
            fs = [f for f in row["factors"] if "attributed" in f["label"] and "direct" in f["label"]]
            return fs[0] if fs else None
        lr_cols = []
        for c in cols:
            f1_, f2_ = fac(v1[t]["rows"][c]), fac(cp[t]["rows"][c])
            name = f"cppu.{t}.{C.RUNGS[c][:3]}"
            if f2_ is None:
                res["entries"][name] = dict(v1=f"{f1_['N']}/{f1_['M']}", v2=None, p=float("nan"), z=float("nan"),
                                            test="NOT TESTABLE (no direct v2 factor)",
                                            v2_factors=[f["label"] for f in cp[t]["rows"][c]["factors"]])
                continue
            if f2_["N"] >= 10 and f1_["N"] >= 10:
                if "C'_PU attributed" not in f2_["label"]:     # low-gun branch (depth from C'0): no clustering defined here
                    res["entries"][name] = dict(v1=f"{f1_['N']}/{f1_['M']}", v2=f"{f2_['N']}/{f2_['M']}", p=float("nan"),
                                                z=float("nan"), test="NOT TESTABLE (v2 factor from C'0, low gun count)",
                                                v2_factor=f2_["label"])
                    continue
                lr_cols.append((c, name, f1_, f2_))
            else:
                # N < 10 branch FROZEN (advisor ruling 2026-11-18): exact test on the candidate counts as written
                pb = float(stats.binomtest(int(f2_["N"]), int(f1_["N"] + f2_["N"]), f2_["M"] / (f1_["M"] + f2_["M"])).pvalue)
                mde = float(np.expm1(2 * np.sqrt(1 / max(f1_["N"], 1) + 1 / max(f2_["N"], 1))))
                res["entries"][name] = signed_exact(f"v1 cprime.{t}", pb, f2_["N"] / f2_["M"] - f1_["N"] / f1_["M"],
                                                    f"{f1_['N']:.0f}/{f1_['M']:.0f}", f"{f2_['N']:.0f}/{f2_['M']:.0f}",
                                                    "conditional binomial",
                                                    frozen_branch_flag="N < 10: conditional binomial on candidate counts "
                                                    "treated as Poisson (not clustered); branch frozen by the advisor ruling "
                                                    "2026-11-18, FLAG: clustered counts make this test anti-conservative",
                                                    mde_2sigma=mde, mde_tag="ESTIMATE (Poisson, unclustered)",
                                                    gross_check_only=bool(mde > 0.5))
        if not lr_cols:
            continue
        Ncl, Mcl = cppu_clusters(by_t[t], [rung_col(f2_["label"]) for _, _, _, f2_ in lr_cols])
        for j, (c, name, f1_, f2_) in enumerate(lr_cols):     # consistency with v1's own cprime_term
            if not (np.isclose(Ncl[:, j].sum(), f2_["N"], rtol=1e-9) and np.isclose(Mcl.sum(), f2_["M"], rtol=1e-9)):
                raise RuntimeError(f"C'_PU clusters do not reproduce cprime_term for {name}: {Ncl[:, j].sum()} vs "
                                   f"{f2_['N']}, {Mcl.sum()} vs {f2_['M']}")
        est, reps, ndrop = cluster_boot_ln(Ncl, Mcl, a.nboot_cl, np.random.default_rng([C.SEED, 11, len(groups)]))
        s2b = reps.std(0, ddof=1)
        for j, (c, name, f1_, f2_) in enumerate(lr_cols):
            res["entries"][name] = clustered_entry(f1_, f2_, float(s2b[j]), ndrop,
                                                   f"v1 background.json cprime.{t}.rows[{c}] attributed direct",
                                                   v1_counts=f"{f1_['N']:.0f}/{f1_['M']:.0f}",
                                                   v2_counts=f"{f2_['N']:.0f}/{f2_['M']:.0f}", n_clusters=int(len(Mcl)),
                                                   n_boot=int(len(reps)), joint_family="cppu",
                                                   v2_factor_rung=C.RUNGS[rung_col(f2_["label"])],
                                                   v1_factor_rung=C.RUNGS[rung_col(f1_["label"])],
                                                   criterion="clustered width committed before reading (advisor ruling "
                                                             "2026-11-18); no 1/sqrt(N) verdict")
            names.append(name)
        groups.append((list(range(k0, k0 + len(lr_cols))), reps)); k0 += len(lr_cols)
    if names:
        res.setdefault("_joint", {})["cppu"] = dict(names=names, groups=groups)


def cppu_clusters(js, cols):
    """Per-cluster attributed-candidate counts at the given rung columns and slots per cluster for one topology's C'_PU
    jobs, with the clusters of cprime_term.recs (B-7): source C'0 event (cp.ev[:, 1]) when cp.ev_cols has 'src', else
    the trial.  -> N (C, len(cols)), M (C,).  Denominator: one slot per trial (cprime_term's n_with)."""
    from acts.stage4.analysis import common as C
    cn, cm = [], []                                   # (cluster id, rung flags) of candidates; cluster id of slots
    for jn, d in enumerate(js):
        dc = d["d_cp"]
        tev = np.asarray(dc.get("trials.ev", []), np.int64)
        src = "cp.ev" in dc and "src" in str(dc.get("cp.ev_cols", "")) and dc["cp.ev"].shape[1] >= 2
        cm.append(dc["cp.ev"][tev, 1].astype(np.int64) if src else np.arange(len(tev), dtype=np.int64) + 10_000_000 * jn)
        cc = {k[8:]: dc[k] for k in dc if isinstance(k, str) and k.startswith("cp.cand.")}
        if not cc or "attributed" not in cc:
            continue
        a = cc["attributed"].astype(bool)
        tr = np.asarray(cc["trial"])[a].astype(np.int64)
        cid = dc["cp.ev"][tev[tr], 1].astype(np.int64) if src else tr + 10_000_000 * jn
        cn.append((cid, C.rung_flags(cc["rungs"])[a][:, cols]))
    ids = np.unique(np.concatenate(cm + [x for x, _ in cn]))
    M = np.bincount(np.searchsorted(ids, np.concatenate(cm)), minlength=len(ids)).astype(float)
    N = np.zeros((len(ids), len(cols)))
    for cid, Fa in cn:
        ii = np.searchsorted(ids, cid)
        for j in range(len(cols)):
            N[:, j] += np.bincount(ii[Fa[:, j]], minlength=len(ids))
    return N, M


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
    def fac(row):
        return [f for f in row["factors"] if f["label"].startswith("HS cand") and "direct" in f["label"]][0]
    cols = (3, 4, 5)
    F1 = [fac(v1["rows"][c]) for c in cols]; F2 = [fac(sm["Znunu_j"]["rows"][c]) for c in cols]
    names = [f"sm.{C.RUNGS[c][:3]}" for c in cols]
    # frozen script (as run by Ignatius 2026-11-18): s_ln = 1/sqrt(weighted candidate count) on both sides; kept to
    # reproduce the FAIL on record (STR §4.1 item 5); NOT used for any verdict of the amended criterion (E4, pending)
    fz = {}
    for n, c, f1_, f2_ in zip(names, cols, F1, F2):
        fz[n] = lr_entry(f1_["N"] / f1_["M"], f1_["s_ln_used"], f2_["N"] / f2_["M"], f2_["s_ln_used"],
                         f"v1 background.json sm.Znunu_j.rows[{c}] HS cand direct",
                         v1_counts=f"{f1_['N']:.1f}/{f1_['M']:.0f}", v2_counts=f"{f2_['N']:.1f}/{f2_['M']:.0f}")
    res["frozen_script"] = dict(
        label="frozen script: SM widths 1/sqrt(weighted candidate count) (c1_compare.py as run 2026-11-18, Ignatius); "
              "verdict on record",
        entries=fz, families=dict(sm=coherence_naive([(np.log(e["v2"] / e["v1"]), np.hypot(e["v1_s_ln"], e["v2_s_ln"]))
                                                      for e in fz.values()])),
        individual_fail=[k for k, e in fz.items() if e["p"] <= 0.05 / N_DECL],
        sum_z2=float(sum(e["z"] ** 2 for e in fz.values())))
    # corrected: per-event x_e = w_presel(e) x n_cand(e, R) over ALL class events (events without a candidate = 0),
    # the same candidate mask as sm_term (l.712: tag & 1, n_hs_band >= 1, rung flag), event bootstrap, joint replicas
    X = []
    for d in jobs:
        if d["job"]["sample"] != "C_Znunu_j":
            continue
        rows = regen[d["job_id"]]["rows"]
        wev = np.array([r["w_presel"] for r in rows], float)
        cnd = d["cand"]
        m = ((cnd["tag"] & 1) > 0) & (cnd["n_hs_band"] >= 1)
        ie = (d["tr"]["ev"][cnd["trial"]] - int(d["job"].get("ev0", 0))).astype(np.int64)
        if m.any() and (ie[m].min() < 0 or ie[m].max() >= len(rows)):
            raise RuntimeError(f"SM event index outside the regen rows in {d['job_id']}")
        Fr = C.rung_flags(cnd["rungs"])
        x = np.zeros((len(rows), len(cols)))
        for j, c in enumerate(cols):
            k = m & Fr[:, c]
            x[:, j] = np.bincount(ie[k], weights=wev[ie[k]], minlength=len(rows))
        X.append(x)
    X = np.concatenate(X)
    for j, (c, f2_) in enumerate(zip(cols, F2)):     # consistency with v1's own sm_term (same N, M, same deep rung)
        if rung_col(f2_["label"]) != c or not np.isclose(X[:, j].sum(), f2_["N"], rtol=1e-9) or len(X) != f2_["M"]:
            raise RuntimeError(f"per-event SM arrays do not reproduce sm_term at {C.RUNGS[c]}: "
                               f"{X[:, j].sum()} vs {f2_['N']}, {len(X)} vs {f2_['M']}, {f2_['label']}")
    est, reps, ndrop = cluster_boot_ln(X, np.ones(len(X)), a.nboot_cl, np.random.default_rng([C.SEED, 5]))
    s2b = reps.std(0, ddof=1)
    for j, (n, c, f1_, f2_) in enumerate(zip(names, cols, F1, F2)):
        res["entries"][n] = clustered_entry(f1_, f2_, float(s2b[j]), ndrop,
                                            f"v1 background.json sm.Znunu_j.rows[{c}] HS cand direct",
                                            v1_counts=f"{f1_['N']:.1f}/{f1_['M']:.0f}",
                                            v2_counts=f"{f2_['N']:.1f}/{f2_['M']:.0f}", n_events=int(len(X)),
                                            n_boot=int(len(reps)), joint_family="sm",
                                            criterion="amendment E4 (pending the user's approval, after the result)")
    res.setdefault("_joint", {})["sm"] = dict(names=names, groups=[(list(range(len(cols))), reps)])


CLOSURE_SEED = 20261014     # frozen closure-family seed (verdict on record); --closure-seed changes it for diagnostics


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--nboot", type=int, default=500)
    ap.add_argument("--pu1", default="p2-a-c1-pu1")
    ap.add_argument("--pu2", default="p2-a-c1-pu2")
    ap.add_argument("--nboot-v1", type=int, default=1000, help="closure/trend/c-test bootstrap (run_all default)")
    ap.add_argument("--nboot-cl", type=int, default=2000, help="cluster bootstrap replicas (SM events, C'_PU sources)")
    ap.add_argument("--cp0", default="p2-a-c1-cp0")
    ap.add_argument("--cppua", default="p2-a-c1-cppua")
    ap.add_argument("--cppub", default="p2-a-c1-cppub")
    ap.add_argument("--gen", default="p2-a-c1-gen2")
    ap.add_argument("--sm", default="p2-a-c1-sm")
    ap.add_argument("--smregen", default="p2-a-c1-smregen")
    ap.add_argument("--families", default="pu,closure,cprime,rates,sm",
                    help="subset to run (pu = pu1/pu2/T1/T1w of Rosalie; closure = slope and c-factor)")
    ap.add_argument("--closure-seed", type=int, default=CLOSURE_SEED,
                    help="rng seed of the closure family (PUSamples, trend, c-test); default = the frozen seed. Other "
                         "values: DIAGNOSTIC seed scan only (advisor ruling LOG.md 2026-11-19 10:28), never a verdict")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)
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
            jr = np.random.default_rng([20261116, 1])      # fallback resamples for pu_joint (no closure context)
            res["_pu_ctx"] = dict(g1=s[:, :3], n1=n, s2=s2, n2=n2, I1=jr.integers(0, len(n), (a.nboot, len(n))),
                                  I2=jr.integers(0, len(n2), (a.nboot, len(n2))))
    if "closure" in fams:
        fam_closure_extra(res, a, a.closure_seed)
        if a.closure_seed != CLOSURE_SEED:
            res["closure_seed"] = dict(seed=a.closure_seed, frozen_seed=CLOSURE_SEED,
                                       label="DIAGNOSTIC seed scan; the frozen verdict uses frozen_seed")
    if "cprime" in fams:
        fam_cprime(res, a)
    if "rates" in fams:
        fam_rates(res, a)
    if "sm" in fams:
        fam_sm(res, a)
    pu_joint(res)
    # family coherence and global (family = first part of the entry name; pu1/pu2/clos as Rosalie, cp0, cppu, rates, sm)
    fam = {}
    for k, e in res["entries"].items():
        if e.get("joint_family") in ("sm", "cppu"):
            continue                       # clustered families (sm, cppu): joint replicas only (no 1/sqrt(N) form)
        if e.get("test") == "log-ratio z":
            fam.setdefault(k.split(".")[0], []).append((np.log(e["v2"]) - np.log(e["v1"]), np.hypot(e["v1_s_ln"],
                                                                                                     e["v2_s_ln"])))
        elif e.get("coh") and e["coh"][0] is not None:
            fam.setdefault(k.split(".")[0], []).append(tuple(e["coh"]))
    for f, v in fam.items():
        res["families"][f] = coherence_naive(v)
    joint = res.pop("_joint", {})
    block = {}                             # entry names replaced in the global sum by their family's d' S^-1 d
    for f, J in joint.items():
        es = [res["entries"][n] for n in J["names"]]
        if J.get("clustered", True):       # sm, cppu (54610b6): v1 width primary (scaled) and 0
            d = [np.log(e["v2"] / e["v1"]) for e in es]
            res["families"][f] = joint_family(d, [e["v1_s_ln"] for e in es], J["groups"])
            res["families"][f]["v1_width_rule"] = V1W_PRIMARY
            res["families"][f]["v1_width_zero"] = joint_family(d, np.zeros(len(d)), J["groups"])
        else:                              # pu1, pu2, clos (pu_joint): v1 widths as recorded by v1
            naive = res["families"].get(f)
            res["families"][f] = joint_family(J["d"], J["s1"], J["groups"])
            res["families"][f].update(v1_width_rule="v1 widths as recorded (STR §4.1 table / background.json); v1 "
                                                    "correlation = v2's (ESTIMATE)",
                                      replicas_source=J["replicas_source"], n_boot=J["n_boot"],
                                      n_boot_dropped=J["n_boot_dropped"],
                                      frozen_script_independent=naive,
                                      criterion="joint-replica coherence (orchestrator decision LOG 2026-11-18 12:37 (b), "
                                                "committed before the full read); frozen script form kept as "
                                                "frozen_script_independent")
        res["families"][f]["entries"] = J["names"]
        block.update({n: f for n in J["names"]})
    zs = [e["z"] for k, e in res["entries"].items() if k not in block and np.isfinite(e.get("z", np.nan))]
    zall = [e["z"] for e in res["entries"].values() if np.isfinite(e.get("z", np.nan))]
    s_blk = sum(res["families"][f]["chi2_block"] for f in joint)
    s_blk0 = sum(res["families"][f].get("v1_width_zero", res["families"][f])["chi2_block"] for f in joint)
    res["individual_fail"] = [k for k, e in res["entries"].items() if e["p"] <= 0.05 / N_DECL]
    res["individual_fail_v1_width_zero"] = [k for k, e in res["entries"].items()
                                            if e.get("v1_width_zero", e)["p"] <= 0.05 / N_DECL]
    res["not_testable"] = [k for k, e in res["entries"].items() if not np.isfinite(e.get("p", np.nan))]
    n_av = len(zs) + len(block)
    res["global_partial"] = dict(n_available=n_av, sum_z2=float(np.sum(np.square(zs)) + s_blk),
                                 sum_z2_v1_width_zero=float(np.sum(np.square(zs)) + s_blk0),
                                 sum_z2_naive=float(np.sum(np.square(zall))),
                                 chi2_99_at_n_available=float(stats.chi2.ppf(0.99, max(1, n_av))),
                                 note="the global test of STR §4.1 uses all 41 quantities; partial value only. sum_z2: "
                                      "families " + (",".join(joint) or "none") + " enter as d' S^-1 d with the joint "
                                      "replicas (same dof); sum_z2_naive treats every entry as independent (frozen "
                                      "form). The pu1/pu2/clos blocks are decorrelated within each family only: "
                                      "clos.T1/T1w are functions of pu1/pu2 (cross-family correlation not removed)")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.part")
    tmp.write_text(json.dumps(res, indent=1, default=str) + "\n")
    tmp.replace(out)
    for k, e in res["entries"].items():
        v2 = e["v2"] if isinstance(e["v2"], str) or e["v2"] is None else f"{e['v2']:.5g}"
        log.info("%-16s v1 %-14s v2 %-14s z %+.2f p %.3g", k, e["v1"], v2, e.get("z", float("nan")), e["p"])
    log.info("families: %s", json.dumps({f: {k: v for k, v in x.items() if k in ("n", "z", "coherent", "chi2_block")}
                                         for f, x in res["families"].items()}))
    if "frozen_script" in res:
        log.info("frozen script (SM, 1/sqrt(N)): %s", json.dumps({k: round(e["z"], 3) for k, e in
                                                                  res["frozen_script"]["entries"].items()}))


if __name__ == "__main__":
    main()
