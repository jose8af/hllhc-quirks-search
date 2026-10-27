"""r2_kB_confound.py -- S1-R2: re-analysis of E2's raw per-event data (no new runs).

(1) Is the 3 keV weak-field excess Delta c(1/20) = c(1/20) - c_E1 driven by k_B (the B* hypothesis of NEAR_MISS v4 §9.3) or
    by the size of the field-driven miss distance b_odd/l_max (proximity to the double-precision floor, small eps_perp)?
    In the lab, k_B ~ sin(n,z)/(beta_T sin alpha): large k_B <=> small sin alpha <=> small eps_perp <=> small b_odd.
    Rank correlations and partial rank correlations; 2D split.  Data: FU fine (max_boost 1e-3) 3 keV runs (E2), M3 events.
(2) Scale-free comparison: same events at 1 keV, f = 1/80 (b_odd/l_max 2.25x larger than 3 keV, f = 1/20): is there a
    k_B-dependent excess at 1 keV, f = 1/80?  Data: M3 prod_B 1 keV (f = 1/80 available).
(3) |q| = 2 <=> B -> 2 B exactly.  Per-event Delta_s(2 B0)/Delta_s(B0) at 1 keV from M3 prod_B (E2's f = 2 point) vs
    E1's per-event 2 [1 - c_E1 ln 2].
Uses E2's loaders/kinematics (FIX1_analysis.kin2, FU_analysis.fu_load) for reading only.
Run (from TT): pixi run python analytic/review/r2_checks/r2_kB_confound.py > analytic/review/r2_checks/r2_kB_confound_out.txt
"""
import os, sys, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(TT, 'analytic', 'numerics')); sys.path.insert(0, os.path.join(TT, 'code'))
import FIX1_analysis as X  # noqa: E402
import FU_analysis as F    # noqa: E402

D = os.path.join(TT, 'data', 'stage1_numerics')


def rank(a):
    return np.argsort(np.argsort(a)).astype(float)


def spear(a, b):
    return np.corrcoef(rank(a), rank(b))[0, 1]


def pspear(a, b, z):
    """partial Spearman of a, b controlling z (linear on ranks)."""
    ra, rb, rz = rank(a), rank(b), rank(z)
    ea = ra - np.polyval(np.polyfit(rz, ra, 1), rz); eb = rb - np.polyval(np.polyfit(rz, rb, 1), rz)
    return np.corrcoef(ea, eb)[0, 1]


def m3B(m, lam):
    out = {}
    for f in glob.glob(os.path.join(D, 'M3', f"m{m:g}_L{lam:g}_e*_prod_B.npz")):
        z = np.load(f)
        if np.all(z['status'] == 1):
            out[int(z['iev'])] = (dict(zip([float(x) for x in z['fracs']], z['ds'])), z['p1'], z['p2'])
    return out


def boot_med(x, n=1000, seed=1):
    r = np.random.default_rng(seed); x = np.asarray(x)
    return np.median(x), np.std([np.median(r.choice(x, len(x))) for _ in range(n)])


if __name__ == '__main__':
    for m in (500.0, 1000.0):
        m3_3 = m3B(m, 3.0); fu = F.fu_load(m, 3.0, 'fine'); m3_1 = m3B(m, 1.0)
        rows = []
        for i, ds in fu.items():
            if i not in m3_3 or i not in m3_1 or not np.all(np.isfinite(ds)):
                continue
            _, p1, p2 = m3_3[i]
            k3 = X.kin2(p1, p2, m, 3.0); k1 = X.kin2(p1, p2, m, 1.0)
            d20 = (ds[3] * 20 / ds[0] - 1) / np.log(20) - k3['c_E1']
            d1 = m3_1[i][0]
            c80 = (d1[0.0125] * 80 / d1[1.0] - 1) / np.log(80); c20_1 = (d1[0.05] * 20 / d1[1.0] - 1) / np.log(20)
            q2 = d1[2.0] / d1[1.0]
            rows.append(dict(i=i, d20=d20, kB=k3['kB_perp'], kBt=k3['kB'], sa=k3['sin_alpha'], g=k3['gstar'],
                             bl3=k3['b_over_lmax'] / 20, bl1=k1['b_over_lmax'] / 80, d80_1=c80 - k1['c_E1'],
                             d20_1=c20_1 - k1['c_E1'], q2=q2, q2p=2 * (1 - k1['c_E1'] * np.log(2)), cE1=k1['c_E1']))
        R = {k: np.array([r[k] for r in rows]) for k in rows[0]}
        n = len(rows)
        print(f'=== m = {m:.0f} GeV: {n} events (3 keV FU fine 1e-3 & M3 prod 1 keV)')
        print('(1) 3 keV, Delta c(1/20): Spearman with k_B(perp) %.2f, k_B(tot) %.2f, sin alpha %.2f, b_odd/l_max(B0/20) %.2f, gamma* %.2f'
              % (spear(R['d20'], R['kB']), spear(R['d20'], R['kBt']), spear(R['d20'], R['sa']), spear(R['d20'], R['bl3']), spear(R['d20'], R['g'])))
        print('    Spearman k_B(perp) vs b_odd/l_max: %.2f; vs sin alpha: %.2f' % (spear(R['kB'], R['bl3']), spear(R['kB'], R['sa'])))
        print('    partial: d20 vs k_B | b/l_max = %+.2f ;  d20 vs b/l_max | k_B = %+.2f ;  d20 vs k_B | sin alpha = %+.2f ; d20 vs sin alpha | k_B = %+.2f'
              % (pspear(R['d20'], R['kB'], R['bl3']), pspear(R['d20'], R['bl3'], R['kB']), pspear(R['d20'], R['kB'], R['sa']), pspear(R['d20'], R['sa'], R['kB'])))
        bm = np.median(R['bl3'])
        print(f'    2D medians of Delta c(1/20) [n] (b/l_max at B0/20 split at its median {bm:.2e}):')
        for klo, khi in ((0, 5), (5, 1e9)):
            s = []
            for lo, hi in ((0, bm), (bm, 1)):
                sel = (R['kB'] >= klo) & (R['kB'] < khi) & (R['bl3'] >= lo) & (R['bl3'] < hi)
                if sel.sum() >= 3:
                    v, e = boot_med(R['d20'][sel]); s.append(f'{"small" if lo == 0 else "large"} b: {v:+.4f} +- {e:.4f} [{sel.sum()}]')
                else:
                    s.append(f'{"small" if lo == 0 else "large"} b: n={sel.sum()}')
            print(f'      k_B in [{klo},{khi:g}): ' + ';  '.join(s))
        print('(2) 1 keV, same events: Delta c(1/80) (b/l_max 2.25x the 3 keV f=1/20 value) and Delta c(1/20):')
        for klo, khi in ((0, 5), (5, 10), (10, 1e9)):
            sel = (R['kB'] >= klo) & (R['kB'] < khi)
            if sel.sum() >= 3:
                v80, e80 = boot_med(R['d80_1'][sel]); v20, e20 = boot_med(R['d20_1'][sel]); v3, e3 = boot_med(R['d20'][sel])
                print(f'      k_B in [{klo},{khi:g}) n={sel.sum():3d}: 1 keV Dc(1/80) = {v80:+.4f} +- {e80:.4f}; 1 keV Dc(1/20) = {v20:+.4f} +- {e20:.4f}'
                      f';  3 keV Dc(1/20) = {v3:+.4f} +- {e3:.4f}')
        sel = R['bl1'] < np.quantile(R['bl1'], 0.25)
        v, e = boot_med(R['d80_1'][sel])
        print(f'      1 keV f=1/80, lowest-b quartile (b/l_max < {np.quantile(R["bl1"], 0.25):.1e}): Dc = {v:+.4f} +- {e:.4f} [{sel.sum()}]; '
              f'3 keV f=1/20 events with b/l_max in the same range: n = {((R["bl3"] >= R["bl1"][sel].min()) & (R["bl3"] < np.quantile(R["bl1"], 0.25))).sum()}, '
              f'Dc = {np.median(R["d20"][(R["bl3"] >= R["bl1"][sel].min()) & (R["bl3"] < np.quantile(R["bl1"], 0.25))]):+.4f}')
        rq = R['q2'] / R['q2p']
        v, e = boot_med(rq)
        print(f'(3) |q| = 2 <=> 2 B0 (1 keV, E2 M3 f = 2): per-event Ds(2B0)/Ds(B0) median {np.median(R["q2"]):.3f} '
              f'(16-84 % {np.quantile(R["q2"], 0.16):.3f}-{np.quantile(R["q2"], 0.84):.3f}); E1 2[1 - c_E1 ln2] median {np.median(R["q2p"]):.3f}; '
              f'ratio meas/pred median {v:.4f} +- {e:.4f}')
        print()
