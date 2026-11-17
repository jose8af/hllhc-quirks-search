"""Unit tests of v2arith.core (stdlib unittest).  Run: python -m unittest v2arith.test_core (from src/)."""
import unittest

import numpy as np

from v2arith.core import (Factor, Term, b84, b84_analytic_single, chain, cprime_value, guarded, sm_value, srt_pu,
                          times_f1, trend_at)


class TestChain(unittest.TestCase):
    def test_counts(self):
        P, s, zb, _ = chain([Factor(N=81, M=500), Factor(N=2, M=81)])
        self.assertAlmostEqual(P, 81 / 500 * 2 / 81, places=15)
        self.assertAlmostEqual(s, np.hypot(1 / 9, 1 / np.sqrt(2)), places=15)
        self.assertFalse(zb)

    def test_one_zero_bound_largest_M(self):     # only the zero with the largest M enters, as 1.14/M, s_ln 1
        P, s, zb, used = chain([Factor(N=0, M=35), Factor(N=0, M=81), Factor(N=5, M=10)])
        self.assertTrue(zb)
        self.assertEqual(used[0], (1.0, 0.0))
        self.assertAlmostEqual(used[1][0], 1.14 / 81, places=15)
        self.assertAlmostEqual(P, 1.14 / 81 * 0.5, places=15)
        self.assertAlmostEqual(s, np.hypot(1.0, 1 / np.sqrt(5)), places=15)

    def test_fixed_and_given_width(self):
        P, s, _, _ = chain([Factor(value=1.2, s_ln=0.0), Factor(N=100, M=1000, s_ln=0.3)])
        self.assertAlmostEqual(P, 0.12, places=15)
        self.assertAlmostEqual(s, 0.3, places=15)            # max(0.3, 0.1)

    def test_values(self):          # v1 numbers: Z(nunu) R06 and C' DIF R06 (background.json / bsum_wp.json)
        self.assertAlmostEqual(sm_value(0.015950845922735858, 14.272389138981586, 1.4) / 956158.0564419407, 1, 12)
        self.assertAlmostEqual(cprime_value(0.004543582369836744, 40848447.93138061, 1.5945006834439603)
                               / 295936.5968327639, 1, 9)


class TestB84(unittest.TestCase):
    def test_single_term_closed_form(self):
        v, s = 1000.0, 0.7
        q, med, _ = b84([Term('a', v, {'stat': s})], nmc=400_000, seed=3)
        self.assertLess(abs(q / b84_analytic_single(v, s) - 1), 0.01)
        self.assertLess(abs(med / v - 1), 0.01)

    def test_shared_components_add_linearly(self):  # two terms with one shared width = one term of the summed value
        q2, _, _ = b84([Term('a', 1.0, {'normalisation': 0.5}), Term('b', 3.0, {'normalisation': 0.5})], 400_000, 5)
        self.assertLess(abs(q2 / (4.0 * np.exp(0.5)) - 1), 0.01)


class TestF1SrtTrend(unittest.TestCase):
    def test_guard(self):          # a second zero in a term that holds its bound enters as 1
        f = guarded(0, 46, 0.0, True)
        self.assertEqual((f.value, f.s_ln), (1.0, 0.0))
        self.assertEqual(guarded(0, 46, 0.0, False).N, 0)

    def test_times_f1(self):
        v, s, zb = times_f1(100.0, 0.3, False, dict(N=23, M=46, s_ln=0.0))
        self.assertAlmostEqual(v, 50.0, places=12)
        self.assertAlmostEqual(s, np.hypot(0.3, 1 / np.sqrt(23)), places=12)
        self.assertEqual(times_f1(100.0, 0.3, False, dict(N=3, M=5, s_ln=0.0)), (100.0, 0.3, False))   # M < 10: none

    def test_trend(self):
        tr = dict(significant=True, intercept_at_x0=1.85, slope=-0.36, direction='conservative')
        self.assertAlmostEqual(trend_at(tr, 9)[0], abs(1.85 - 3.24), places=12)
        self.assertEqual(trend_at(dict(significant=False), 9), (0.0, 1.0))
        s, f = trend_at(dict(significant=True, intercept_at_x0=0.1, slope=0.1, direction='anti-conservative'), 2)
        self.assertAlmostEqual(f, np.exp(0.3), places=12)

    def test_srt(self):            # both reachable: P(no BTL) = P - P(BTL); timing factors N/M
        esA = dict(P_per_trial=10.0, reachable_rho2=True, sigma_ln_components=dict(stat=0.1))
        esT = dict(P_per_trial=4.0, reachable_rho2=True, sigma_ln_components=dict(stat=0.2))
        srt = dict(P_late=dict(N=50, M=1000), P_oot=dict(N=20, M=10000), sigma_ln_PV=0.3, sigma_ln_sigma_t=0.4)
        (n1, v1, c1, _), (n2, v2, c2, _) = srt_pu(esT, esA, None, srt, 2.0)
        self.assertAlmostEqual(v1, 2.0 * 4.0 * 0.05, places=12)
        self.assertAlmostEqual(v2, 2.0 * 6.0 * 0.002, places=12)
        self.assertAlmostEqual(c1['stat'], np.hypot(0.2, 1 / np.sqrt(50)), places=12)
        self.assertEqual((c2['srt_pv'], c2['srt_sigt']), (0.3, 0.4))


if __name__ == '__main__':
    unittest.main()
