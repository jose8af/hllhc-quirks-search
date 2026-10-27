"""R1 reviewer check: is the 3-5 keV c excess per-oscillation (floor-like: a function of eps_perp only, N-independent)
or cumulative (grows with N_osc ~ Lambda^2 at fixed eps_perp, k_B)?  Uses pooled_L*.npz from c_law.py.
Also: Stage-1 floor law (NEAR_MISS §9.3: CM excess (0.5-1.3) u/eps^2, full-event amplitude ~3.85x CM) -> predicted
floor Dc per event at k_f = 2:  Dc ~ R (delta(eps/2) - delta(eps))/ln 2 = 1.06 * 3 delta(eps)/ln 2."""
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

H = Path(__file__).parent
rng = np.random.default_rng(3)
P = {lam: np.load(H / f'pooled_L{lam:g}.npz') for lam in (1, 2, 3, 5)}
u = 2.2e-16


def bmed(x, nb=400):
    if len(x) < 5:
        return np.nan, np.nan
    return np.median(x), np.std([np.median(rng.choice(x, len(x))) for _ in range(nb)])


print('matched (eps_perp at B0, k_B) cells: median r/c_ev [%] at each Lambda')
ebins = [3e-7, 1e-6, 3e-6, 1e-5, 3e-5]
for kb in ((0, 4), (4, 10), (10, 1e9)):
    for e0, e1 in zip(ebins[:-1], ebins[1:]):
        line = f'k_B [{kb[0]:g},{kb[1]:g}) eps [{e0:.0e},{e1:.0e}):'
        for lam, d in P.items():
            s = (d['kB'] >= kb[0]) & (d['kB'] < kb[1]) & (d['eps'] >= e0) & (d['eps'] < e1)
            m, e = bmed(d['r'][s])
            line += f'  {lam:g}keV n={s.sum():3d} {100*m:+6.1f}+-{100*e:4.1f}' if s.sum() >= 5 else f'  {lam:g}keV n={s.sum():3d}   --   '
        print(line)

print('\npartial Spearman at 5 keV and 3 keV (r/c_ev vs k_B | eps, vs eps | k_B)')
for lam in (3, 5):
    d = P[lam]; r, k, e = d['r'], np.log(d['kB']), np.log(d['eps'])
    from scipy.stats import rankdata
    R, K, E = (rankdata(x) for x in (r, k, e))
    def res(y, x):
        A = np.c_[np.ones_like(x), x]; return y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    print(f' {lam} keV: rho(r,kB)={spearmanr(r,k)[0]:+.2f} rho(r,eps)={spearmanr(r,e)[0]:+.2f} rho(kB,eps)={spearmanr(k,e)[0]:+.2f}'
          f'  partial(r,kB|eps)={np.corrcoef(res(R,E),res(K,E))[0,1]:+.2f}  partial(r,eps|kB)={np.corrcoef(res(R,K),res(E,K))[0,1]:+.2f}')

print('\nStage-1 floor law, predicted Dc/c (c ~ 0.072 at 5 keV) per k_B bin, A_full = 3.85*(0.5..1.3):')
for lam in (3, 5):
    d = P[lam]
    for a, b in ((0, 2), (2, 4), (4, 6), (6, 10), (10, 1e9)):
        s = (d['kB'] >= a) & (d['kB'] < b); eps = d['eps'][s]
        dc = lambda A: np.median(1.06 * 3 * A * u / eps ** 2 / np.log(2))  # noqa: E731
        print(f'  {lam} keV k_B [{a:g},{b:g}): median eps {np.median(eps):.2e}  floor Dc {dc(1.9):.4f}..{dc(5.0):.4f}'
              f'  (~{100*dc(1.9)/0.072:.1f}..{100*dc(5.0)/0.072:.1f} % of c)  measured median r/c {100*np.median(d["r"][s]):+.1f} %')
