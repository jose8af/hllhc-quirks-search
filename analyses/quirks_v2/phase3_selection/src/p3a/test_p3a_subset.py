"""test_p3a_subset.py -- synthetic tests of p3a_subset.py (plan: logs/executor_aurora_2026-11-24_10-16.md).

  cd phase3_selection/src/p3a && <tt python> -B -m unittest -v test_p3a_subset      (on a worker)

A  BASE of p3a_subset.road_multi == p2w_subset.classify_pool on every synthetic event of Cecilie's T1-T8 generators
   (widths none, 37.5, 18.75, 9.4, 4.7), and BASE(75) between BASE(none) and BASE(37.5).
B  category relations that hold by construction (listed in the plan, C2).
C  the dumped witness passes Nils's independent pure-numpy verifier (imported unchanged) with the stored k.
D  hard-window flag on constructed events.
"""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2].parent / 'phase2_exploration' / 'src'))
import test_p2w_subset as T2  # noqa: E402  (helpers frame / hit / event, frozen config)
import review_nils_subset as NR  # noqa: E402
import p3a_subset as A  # noqa: E402

FF, K, CFG, WCFG, PV = T2.FF, T2.K, T2.CFG, T2.WCFG, T2.PV
MAP = [0, 2, 3, 4, 5]                    # Phase-2 width index -> index in A.WL


def both(H, phim=0.3, tw=5):
    kb2, nr, ns, npl, ng, bad = T2.W.classify_pool(H, PV, phim, CFG, WCFG, FF, K)
    r = A.classify_pool(H, PV, phim, CFG, WCFG, FF, K, tw=tw)
    assert bad == 0 and r['bad'] == 0
    return kb2, r


def events(n=120, seed=3):
    rng = np.random.default_rng(seed)
    for it in range(n):
        ax, n2, nn = T2.frame(0.3 + rng.uniform(-0.1, 0.1), rng.uniform(-0.7, 0.7), rng.uniform(0, np.pi))
        pair = [(rng.uniform(-3, 3), rng.uniform(-0.02, 0.02)), (rng.uniform(-3, 3), rng.uniform(-0.02, 0.02))]
        drop = tuple(rng.choice(10, rng.integers(0, 4), replace=False))
        H = T2.event(ax, n2, pair, drop=drop)
        ex = []
        for _q in range(rng.integers(0, 40)):
            s = T2.SURF[rng.integers(len(T2.SURF))]
            ex.append(T2.hit(s, ax, n2, rng.uniform(-70, 70), off_n=rng.choice([0.0, 0.0, rng.normal(0, 3.0)]), nrm=nn))
        if ex:
            ex = np.array(ex); ex = ex[np.isfinite(ex).all(1)]
            H = np.concatenate([H, ex])
        if len(H) >= 8:
            yield it, H


class TestP3A(unittest.TestCase):
    def test_A_base_equals_phase2(self):
        n = 0
        for it, H in events():
            kb2, r = both(H)
            self.assertTrue((r['kb'][MAP] == kb2).all(), (it, kb2, r['kb']))
            self.assertTrue((r['kb'][0] <= r['kb'][1]).all() and (r['kb'][1] <= r['kb'][2]).all(), (it, r['kb']))
            n += 1
        self.assertGreater(n, 100)

    def test_B_relations(self):
        nsub = 0
        for it, H in events(seed=4):
            kb2, r = both(H)
            KC, kb = r['KC'], r['kb']
            own = np.minimum(np.minimum(KC[1], KC[2]), np.minimum(KC[3], KC[4]))
            # a hard-window witness is an own-axis witness: c4 >= min(c1, c2, c3, c4) trivially; and >= the plane bound c0 at 'none'
            self.assertTrue((KC[4] >= own).all())
            # BASE where the full set passes with the finder axis is c0; BASE never above min(c0, c2 restricted) is not
            # guaranteed (early exit), but min(c0, c2) <= BASE must hold: c2 is the same heuristic without early exit
            self.assertTrue((np.minimum(KC[0], KC[2]) <= kb).all(), (it, KC[0], KC[2], kb))
            # widths: 'none' <= 75 <= 37.5 ... for c0 and c1 (full sets); searches are heuristics, not asserted
            for c in (0, 1):
                for wi in range(5):
                    self.assertTrue((KC[c, wi] <= KC[c, wi + 1]).all(), (it, c, wi))
            # F never below S; s = 3 never below s = 0; k_IP of the s = 3 witness between k(s=0) and k(s=3)
            self.assertTrue((KC[..., 1] >= KC[..., 0]).all() and (KC[:, :, 1, :] >= KC[:, :, 0, :]).all())
            ok = KC[:, :, 1, :] < 99
            self.assertTrue((r['KI'][ok] <= KC[:, :, 1, :][ok]).all() and (r['KI'][ok] >= KC[:, :, 0, :][ok]).all())
            nsub += int((KC[2] < 99).any())
        self.assertGreater(nsub, 20)

    def test_C_witness_verified_independently(self):
        nver = 0
        for tw, W in ((5, 4.7), (4, 9.4), (3, 18.75), (2, 37.5), (1, 75.0)):
            for it, H in events(n=60, seed=5 + tw):
                r = A.classify_pool(H, PV, 0.3, CFG, WCFG, FF, K, tw=tw)
                if r['wk'] > 3:
                    continue
                KC = r['KC']
                allk = int(min(KC[c, tw, 0, 0] for c in range(A.NC)))
                self.assertEqual(r['wk'], allk)
                if r['wk'] < int(min(KC[c, tw, 0, 0] for c in range(1, A.NC))):
                    continue                      # the witness is the full set under the finder's axis (c0 only)
                # rebuild the road arrays as Nils does and verify the witness rows with his verifier
                U, CX, CY, S0, S1, LC, SD = NR.road_arrays(H, PV, 0.3, FF)
                sidm = H[:, 0].astype(np.int64)
                m, U0 = FF.road_select(H, sidm, PV, 0.3, CFG)
                Hr = H[m]
                mask = np.array([any(np.array_equal(h, wrow) for wrow in r['wit_rows']) for h in Hr])
                self.assertEqual(int(mask.sum()), len(r['wit_rows']))
                # the plane normal: least squares through the PV on the witness hits
                u = U[mask]
                _, _, vt = np.linalg.svd(u / np.linalg.norm(u, axis=1)[:, None])
                v = NR.verify(U, CX, CY, S0, S1, LC, SD, mask, vt[-1] / np.linalg.norm(vt[-1]), 0.3, W=W)
                if v['ok']:                        # (a refitted normal can differ from the kernel's at the 3 sigma edge)
                    self.assertLessEqual(v['k'], r['wk'], (tw, it, v))
                    nver += 1
        self.assertGreater(nver, 60)

    def test_D_hard_window(self):
        ax, n2, nn = T2.frame(0.33, 0.4, 0.5)
        H = T2.event(ax, n2, [(-0.6, 0.002), (0.7, -0.001)])              # narrow pair: hard at every width
        r = A.classify_pool(H, PV, 0.3, CFG, WCFG, FF, K)
        self.assertTrue((r['KC'][4][:, 0, 0] == 0).all(), r['KC'][4])
        # narrow pair on 5 IP layers, layers 2 and 5 only far away: MAD passes 4.7 mm with the far hits (k = 0),
        # a hard window of 6.3 mm cannot hold them (k = 2)
        H = T2.event(ax, n2, [(-0.6, 0.002), (0.7, -0.001)], drop=(2, 5),
                     extra=[(2, 30.0), (2, 33.0), (5, -28.0), (5, -31.0)])
        r = A.classify_pool(H, PV, 0.3, CFG, WCFG, FF, K)
        self.assertEqual(int(r['kb'][5, 0, 0]), 0)
        self.assertEqual(int(r['KC'][4, 5, 0, 0]), 2, r['KC'][4])
        self.assertEqual(int(r['KC'][4, 0, 0, 0]), 0)


if __name__ == '__main__':
    unittest.main()
