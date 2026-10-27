"""fix_a1_floor.py -- Stage-3 fix pass R1, critical A-1: discriminating evidence for the 3-5 keV c excess.
Reproduces in stage3 the critical reviewer's checks review/r1_checks/c_law.py (pooled arrays) and c_floor.py, on the stored
ds_barrel_um (the reviewer showed the SVD re-fit changes no pooled median beyond errors, review/r1_checks/c_law.out).

(1) Matched-(k_B, eps_perp(B0)) cells: median r/c_ev (r = c2 - c_ev) at Lambda = 1, 2, 3, 5 keV pooled over the 5 P1 points.
    The double-precision floor is a function of eps_perp per oscillation and is N-independent (Stage-1 FIX2, NUMERICS §13.1:
    B*-off Dc 0.0030/0.0038/0.0044 at s = 1/9, 1/3, 1); a cumulative effect grows with N_osc ~ Lambda^2 at fixed (k_B, eps).
(2) Partial Spearman correlations within one Lambda (r vs k_B | eps, r vs eps | k_B).
(3) Stage-1 floor-law allowance per k_B bin: CM-frame excess (0.5-1.3) u/eps^2 (u = 2.2e-16), full-event amplitude ~3.85x
    (NUMERICS §13.1 item 3), Dc at k_f = 2 ~ 1.06 * 3 delta(eps)/ln 2  -> floor Dc range per event (median over the bin),
    expressed as % of c (c ~ median c_ev of the bin).  This is an ESTIMATE (floor coefficient not demonstrated in Stage 1).
Output: results/FIX_A1_floor.json.  Run (theory_track/): pixi run python sim/stage3/scripts/fix_a1_floor.py
"""
import numpy as np
from scipy.stats import rankdata, spearmanr

import s3common as C

POINTS = ['F_m200', 'F_m500', 'F_m1000', 'F_m1500', 'S_m500']
KB = ((0, 2), (2, 4), (4, 6), (6, 10), (10, 1e9))
U = 2.2e-16
rng = np.random.default_rng(3)


def bmed(x, nb=400):
    if len(x) < 5:
        return None, None
    return float(np.median(x)), float(np.std([np.median(rng.choice(x, len(x))) for _ in range(nb)]))


def pooled(S, keys, lam):
    R, K, E, CE = [], [], [], []
    for pk in POINTS:
        def get(cfg):
            sel = S['point'] == keys.index(f'p1/{pk}/L{lam:g}_{cfg}')
            o = np.argsort(S['ev_index'][sel], kind='stable')
            return {c: S[c][sel][o] for c in ('ds_barrel_um', 'status', 'c_ev', 'k_B', 'eps_perp')}
        b, h = get('B'), get('B2')
        ok = (b['status'] == 1) & (h['status'] == 1) & (b['ds_barrel_um'] > 0)
        c2 = (2 * h['ds_barrel_um'] / b['ds_barrel_um'] - 1) / np.log(2)
        R += list(((c2 - b['c_ev']) / b['c_ev'])[ok]); K += list(b['k_B'][ok]); E += list(b['eps_perp'][ok]); CE += list(b['c_ev'][ok])
    return np.array(R), np.array(K), np.array(E), np.array(CE)


def main():
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])
    P = {lam: pooled(S, keys, lam) for lam in (1.0, 2.0, 3.0, 5.0)}
    ebins = [3e-7, 1e-6, 3e-6, 1e-5, 3e-5]
    matched = {}
    for kb in ((0, 4), (4, 10), (10, 1e9)):
        for e0, e1 in zip(ebins[:-1], ebins[1:]):
            cell = {}
            for lam, (r, k, e, _) in P.items():
                s = (k >= kb[0]) & (k < kb[1]) & (e >= e0) & (e < e1)
                m, er = bmed(r[s])
                cell[f'L{lam:g}'] = dict(n=int(s.sum()), median_rel_r=m, err=er)
            matched[f'kB[{kb[0]:g},{kb[1]:g}) eps[{e0:.0e},{e1:.0e})'] = cell
    partial = {}
    for lam in (3.0, 5.0):
        r, k, e, _ = P[lam]
        Rr, Kr, Er = (rankdata(x) for x in (r, np.log(k), np.log(e)))

        def res(y, x):
            A = np.c_[np.ones_like(x), x]
            return y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
        partial[f'L{lam:g}'] = dict(rho_r_kB=float(spearmanr(r, k)[0]), rho_r_eps=float(spearmanr(r, e)[0]),
                                    rho_kB_eps=float(spearmanr(k, e)[0]),
                                    partial_r_kB_given_eps=float(np.corrcoef(res(Rr, Er), res(Kr, Er))[0, 1]),
                                    partial_r_eps_given_kB=float(np.corrcoef(res(Rr, Kr), res(Er, Kr))[0, 1]))
    floor = {}
    for lam in (3.0, 5.0):
        r, k, e, ce = P[lam]
        floor[f'L{lam:g}'] = {}
        for a, b in KB:
            s = (k >= a) & (k < b)
            dc = lambda A: float(np.median(1.06 * 3 * A * U / e[s] ** 2 / np.log(2)))  # noqa: E731
            cm = float(np.median(ce[s]))
            m, er = bmed(r[s])
            floor[f'L{lam:g}'][f'kB[{a:g},{b:g})'] = dict(
                n=int(s.sum()), median_eps_perp=float(np.median(e[s])), median_c_ev=cm,
                floor_Dc_range=[dc(1.9), dc(5.0)], floor_rel_range=[dc(1.9) / cm, dc(5.0) / cm],
                measured_median_rel_r=m, err=er,
                floor_fraction_of_excess_range=([dc(1.9) / cm / m, dc(5.0) / cm / m] if m and m > 0 else None))
    out = dict(script='sim/stage3/scripts/fix_a1_floor.py', source='reproduces review/r1_checks/c_law.py + c_floor.py on stored ds_barrel_um',
               tags=dict(measured_cells='VERIFIED (measured; bootstrap errors)', floor_law='ESTIMATE (Stage-1 floor law, NUMERICS §13.1 item 3)',
                         attribution='ESTIMATE'),
               matched_kB_eps=matched, partial_spearman=partial, floor_law_by_kB=floor)
    C.dump('FIX_A1_floor.json', out)
    for k, v in matched.items():
        cells = []
        for L, x in v.items():
            val = '--' if x['median_rel_r'] is None else f"{100 * x['median_rel_r']:+.1f}+-{100 * x['err']:.1f}%"
            cells.append(f"{L}: n={x['n']} {val}")
        print(k, ' '.join(cells))
    print(partial)
    for L, v in floor.items():
        for kb, x in v.items():
            print(L, kb, f"eps {x['median_eps_perp']:.2e} floor {100*x['floor_rel_range'][0]:.1f}-{100*x['floor_rel_range'][1]:.1f} % of c, measured {100*x['measured_median_rel_r']:+.1f}+-{100*x['err']:.1f} %")


if __name__ == '__main__':
    main()
