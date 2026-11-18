"""Unit tests of the clustered widths of c1_compare.py (fix agent Lisbet, 2026-11-18; REGRESSION_TICKET_SM.md §3).

SYNTHETIC clustered data only: no C'_PU input and no signal file is read.  The only real file read is the SM output on
record (c1_compare_sm_ignatius_2026-11-18.json), to check that the frozen-script path reproduces the recorded z.
Run on a worker (not einstein):  cd phase2_exploration/src && nice -n 19 <tt python> -B -m unittest -v test_c1_compare
"""
import json
import unittest
from pathlib import Path

import numpy as np

import c1_compare as CC

HERE = Path(__file__).resolve().parent


def sm_like(E, rng, p=0.42, k=0.7, theta=67.0):
    """Events with presel weight w in {0, 1} (P(w=1) = p) and n ~ Gamma(k, theta)-Poisson candidates (mean 47, sd ~57
    as the Z(nunu) R04 sample).  -> per-event x = w n, population mean and variance of x."""
    w = (rng.random(E) < p).astype(float)
    n = rng.poisson(rng.gamma(k, theta, E))
    mu_n = k * theta; en2 = k * theta + k * theta ** 2 + (k * theta) ** 2     # E[n^2] of the Gamma-Poisson
    return w * n, n, w, p * mu_n, p * en2 - (p * mu_n) ** 2


class TestEventBootstrap(unittest.TestCase):
    """SM family: the event bootstrap of ln(mean of w n) against the analytic clustered variance."""

    def test_against_analytic(self):
        rng = np.random.default_rng(1)
        E = 2000
        x, _, _, m, v = sm_like(E, rng)
        _, reps, nd = CC.cluster_boot_ln(x[:, None], np.ones(E), 4000, np.random.default_rng(2))
        s_boot = reps.std(0, ddof=1)[0]
        s_sample = np.sqrt(x.var(ddof=1) / E) / x.mean()     # analytic (delta method) with the sample variance
        s_pop = np.sqrt(v / E) / m                            # analytic with the population variance
        self.assertEqual(nd, 0)
        self.assertLess(abs(s_boot / s_sample - 1), 0.05)    # bootstrap MC error ~ 1/sqrt(2 x 4000) ~ 1 %
        self.assertLess(abs(s_boot / s_pop - 1), 0.15)       # sample-variance scatter (heavy tail) ~ 5 %
        s_poisson = 1 / np.sqrt(x.sum())                      # the frozen 1/sqrt(N) on candidates
        self.assertLess(s_poisson, s_boot / 5)               # underestimate: ~ 0.005 vs ~ 0.05 at this multiplicity

    def test_ensemble(self):
        """The bootstrap width equals the scatter of ln(mean) over independent samples; 1/sqrt(N) does not."""
        rng = np.random.default_rng(3)
        E = 500
        lm, sb, sp = [], [], []
        for i in range(300):
            x = sm_like(E, rng)[0]
            lm.append(np.log(x.mean()))
            if i < 30:
                sb.append(CC.cluster_boot_ln(x[:, None], np.ones(E), 400, rng)[1].std(ddof=1))
                sp.append(1 / np.sqrt(x.sum()))
        s_ens = np.std(lm, ddof=1)                            # its own relative error ~ 1/sqrt(2 x 299) ~ 4 %
        self.assertLess(abs(np.mean(sb) / s_ens - 1), 0.15)
        self.assertLess(np.mean(sp), s_ens / 4)


class TestClusterRatio(unittest.TestCase):
    """C'_PU family: ratio sum N / sum M over source clusters (several slots per source, counts correlated in a source)."""

    def make(self, rng, C_=600, m=2, k=0.8, theta=1.2):
        lam = rng.gamma(k, theta, C_)                         # source-level rate shared by its m re-overlays
        N = rng.poisson(lam[:, None] * np.ones(m)).sum(1).astype(float)
        M = np.full(C_, float(m))
        var_N = m * k * theta + m ** 2 * k * theta ** 2      # Var(N_c) = m E[lam] + m^2 Var(lam)
        s_pop = np.sqrt(var_N / C_) / (m * k * theta)
        return N, M, s_pop

    def test_against_analytic(self):
        rng = np.random.default_rng(4)
        N, M, s_pop = self.make(rng)
        _, reps, _ = CC.cluster_boot_ln(N[:, None], M, 4000, np.random.default_rng(5))
        R = N.sum() / M.sum()
        s_lin = np.sqrt(((N - R * M) ** 2).sum()) / N.sum()  # linearised ratio variance with the sample
        s_boot = reps.std(ddof=1)
        self.assertLess(abs(s_boot / s_lin - 1), 0.05)
        self.assertLess(abs(s_boot / s_pop - 1), 0.15)
        self.assertLess(1 / np.sqrt(N.sum()), s_boot)        # 1/sqrt(N) underestimates the clustered width
        self.assertGreater(s_boot * np.sqrt(N.sum()), 1.3)   # expected inflation sqrt(1 + m theta) = 1.83

    def test_variable_slots(self):
        """Unequal slots per source: the bootstrap still follows the linearised ratio variance."""
        rng = np.random.default_rng(6)
        C_ = 800
        m = rng.integers(1, 4, C_).astype(float)
        lam = rng.gamma(0.8, 1.2, C_)
        N = rng.poisson(lam * m).astype(float)
        _, reps, _ = CC.cluster_boot_ln(N[:, None], m, 4000, np.random.default_rng(7))
        R = N.sum() / m.sum()
        s_lin = np.sqrt(((N - R * m) ** 2).sum()) / N.sum()
        self.assertLess(abs(reps.std(ddof=1) / s_lin - 1), 0.05)

    def test_cppu_clusters(self):
        """cppu_clusters groups candidates and slots by SOURCE C'0 event across jobs (synthetic job dicts)."""
        from acts.stage4.analysis import common as C
        rng = np.random.default_rng(8)
        jobs, truthN, truthM = [], {}, {}
        for jn in range(3):
            n_ev = 20
            src = rng.integers(0, 15, n_ev)                   # sources re-used inside and across jobs
            tev = np.repeat(np.arange(n_ev), 2)               # 2 trials (slots) per event row
            nc = 50
            trial = rng.integers(0, len(tev), nc)
            att = rng.random(nc) < 0.7
            flags = np.zeros((nc, C.NR), bool)
            flags[:, 3] = rng.random(nc) < 0.6; flags[:, 4] = flags[:, 3] & (rng.random(nc) < 0.5)
            dc = {"trials.ev": tev, "cp.ev": np.stack([np.arange(n_ev), src], 1), "cp.ev_cols": "ev,src",
                  "cp.cand.attributed": att.astype(np.int8), "cp.cand.trial": trial,
                  "cp.cand.rungs": np.packbits(flags, axis=1)}
            jobs.append(dict(d_cp=dc))
            for s in src[tev]:
                truthM[s] = truthM.get(s, 0) + 1
            for i in np.where(att)[0]:
                s = src[tev[trial[i]]]
                truthN.setdefault(s, np.zeros(2))
                truthN[s] += flags[i, [3, 4]]
        N, M = CC.cppu_clusters(jobs, [3, 4])
        self.assertEqual(len(M), len(truthM))
        self.assertEqual(M.sum(), 3 * 40)
        ids = sorted(truthM)
        np.testing.assert_array_equal(M, [truthM[s] for s in ids])
        np.testing.assert_array_equal(N, [truthN.get(s, np.zeros(2)) for s in ids])


class TestJointFamily(unittest.TestCase):
    """Nested rungs (R05 subset of R04) on the same events: joint replicas carry the correlation."""

    def nested(self, rng, E):
        x4, n, w, _, _ = sm_like(E, rng)
        n5 = rng.binomial(n, 0.25)
        return np.stack([x4, w * n5], 1)

    def test_correlation(self):
        rng = np.random.default_rng(9)
        X = self.nested(rng, 2000)
        _, reps, _ = CC.cluster_boot_ln(X, np.ones(len(X)), 4000, np.random.default_rng(10))
        rho_b = np.corrcoef(reps, rowvar=False)[0, 1]
        rho_a = np.corrcoef(X, rowvar=False)[0, 1]            # correlation of the two means = per-event correlation
        self.assertGreater(rho_a, 0.8)
        self.assertLess(abs(rho_b - rho_a), 0.03)

    def test_coherence_width(self):
        """Family-mean width from the joint replicas equals the ensemble scatter of the family mean; the independent
        formula understates it.  v1 fixed (width 0), v1 values = the population means."""
        rng = np.random.default_rng(11)
        E = 500
        mus, s_joint, s_ind = [], [], []
        for i in range(300):
            X = self.nested(rng, E)
            d = np.log(X.mean(0))                             # ln(x2/x1) up to a constant per rung
            _, reps, _ = CC.cluster_boot_ln(X, np.ones(E), 300, rng)
            J = CC.joint_family(d, np.zeros(2), [([0, 1], reps)])
            mus.append(J["mean_ln_ratio"])
            if i < 40:
                s_joint.append(J["s"]); s_ind.append(J["s_independent"])
        s_ens = np.std(mus, ddof=1)
        self.assertLess(abs(np.mean(s_joint) / s_ens - 1), 0.15)
        self.assertLess(np.mean(s_ind), 0.85 * s_ens)

    def test_limits(self):
        """Independent groups and v1 width 0: the joint form reduces to the frozen independent form; chi2 -> sum z^2."""
        rng = np.random.default_rng(12)
        reps = [rng.normal(0, s, (200000, 1)) for s in (0.05, 0.1, 0.2)]
        d = np.array([0.02, -0.05, 0.1])
        J = CC.joint_family(d, np.zeros(3), [([0], reps[0]), ([1], reps[1]), ([2], reps[2])])
        sd = np.array([r.std(ddof=1) for r in reps])
        naive = CC.coherence_naive(list(zip(d, sd)))
        self.assertAlmostEqual(J["s"], naive["s"], places=12)
        self.assertAlmostEqual(J["z"], naive["z"], places=10)
        self.assertAlmostEqual(J["chi2_block"], float(((d / sd) ** 2).sum()), places=10)
        J0 = CC.joint_family(np.zeros(3), np.zeros(3), [([0], reps[0]), ([1], reps[1]), ([2], reps[2])])
        self.assertEqual(J0["chi2_block"], 0.0)               # chi2 -> 0 when v2 = v1 exactly


class TestEntries(unittest.TestCase):
    def test_v1_width_rule(self):
        f1 = dict(N=39032.5, M=2000, s_ln_used=1 / np.sqrt(39032.5))
        f2 = dict(N=40057.1, M=2000, s_ln_used=1 / np.sqrt(40057.1))
        e = CC.clustered_entry(f1, f2, 0.05, 0, "synthetic")
        self.assertAlmostEqual(e["v1_s_ln"], f1["s_ln_used"] * 0.05 / f2["s_ln_used"], places=14)
        d = np.log(f2["N"] / f1["N"])
        self.assertAlmostEqual(e["z"], d / np.hypot(e["v1_s_ln"], 0.05), places=12)
        self.assertAlmostEqual(e["v1_width_zero"]["z"], d / 0.05, places=12)
        self.assertAlmostEqual(e["mde_2sigma"], np.expm1(2 * np.hypot(e["v1_s_ln"], 0.05)), places=14)
        self.assertFalse(e["gross_check_only"])
        self.assertTrue(CC.clustered_entry(f1, f2, 0.3, 0, "synthetic")["gross_check_only"])   # expm1(2 x 0.42) > 0.5
        self.assertAlmostEqual(CC.v1_width_scaled(0.01, 0.05, 0.005), 0.1, places=15)          # limiting: ratio 1 -> same

    def test_frozen_script_reproduces_record(self):
        """The 1/sqrt(N) path (kept as 'frozen script') reproduces the SM verdict on record."""
        rec = json.loads((HERE.parent / "outputs" / "c1_compare_sm_ignatius_2026-11-18.json").read_text())
        for k, e in rec["entries"].items():
            r = CC.lr_entry(e["v1"], e["v1_s_ln"], e["v2"], e["v2_s_ln"], "x")
            self.assertAlmostEqual(r["z"], e["z"], places=12)
        fz = CC.coherence_naive([(np.log(e["v2"] / e["v1"]), np.hypot(e["v1_s_ln"], e["v2_s_ln"]))
                                 for e in rec["entries"].values()])
        self.assertAlmostEqual(fz["z"], rec["families"]["sm"]["z"], places=10)
        self.assertFalse(fz["coherent"])

    def test_rung_col(self):
        from acts.stage4.analysis import common as C
        self.assertEqual(CC.rung_col(f"HS cand P({C.RUNGS[3]}) direct (presel-weighted)"), 3)
        self.assertEqual(CC.rung_col(f"C'_PU attributed P({C.RUNGS[1]}) direct"), 1)


if __name__ == "__main__":
    unittest.main()
