"""R1 reviewer check of the P1 c-law claims (a)/(c) on the summary tables + SVD thickness (c_svd.npz)."""
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[4]
S = np.load(TT / 'data/sim_stage3/summary/events_p1.npz')
V = np.load(Path(__file__).with_name('c_svd.npz'))
keys = list(S['point_keys'])
svd = {(k, r): (a, b) for k, r, a, b in zip(V['key'], V['row'], V['ds_svd'], V['ds_st'])}
rng = np.random.default_rng(7)
POINTS = ['F_m200', 'F_m500', 'F_m1000', 'F_m1500', 'S_m500']
BINS = ((0, 2), (2, 4), (4, 6), (6, 10), (10, 1e9))


def get(pk, lam, cfg):
    k = f'p1/{pk}/L{lam:g}_{cfg}'
    sel = S['point'] == keys.index(k)
    o = np.argsort(S['ev_index'][sel], kind='stable')
    d = {c: S[c][sel][o] for c in ('row', 'ds_barrel_um', 'status', 'c_ev', 'k_B', 'gstar', 'bodd_l0', 'eps_perp', 'floor_flag')}
    d['svd'] = np.array([svd[(k, r)][0] for r in d['row']])
    return d


def bmed(x, nb=500):
    return np.median(x), np.std([np.median(rng.choice(x, len(x))) for _ in range(nb)])


print('== stored vs SVD thickness (all P1 B/B2) ==')
rel = (V['ds_st'] - V['ds_svd']) / V['ds_svd']; ok = np.isfinite(rel)
print('median |rel|', np.median(np.abs(rel[ok])), ' max |abs diff| um', np.nanmax(np.abs(V['ds_st'] - V['ds_svd'])),
      ' p99 abs diff', np.nanpercentile(np.abs(V['ds_st'] - V['ds_svd']), 99))
small = V['ds_svd'] < 0.2
print('events with ds_svd < 0.2 um:', small.sum(), ' median rel diff there', np.median(np.abs(rel[small & ok])) if small.any() else None)

for lam in (0.6, 1.0, 2.0, 3.0, 5.0):
    print(f'\n== Lambda {lam} keV ==')
    allr = []; allk = []; allrs = []; alle = []
    for pk in POINTS:
        b = get(pk, lam, 'B'); h = get(pk, lam, 'B2')
        ok = (b['status'] == 1) & (h['status'] == 1) & (b['ds_barrel_um'] > 0)
        c2 = (2 * h['ds_barrel_um'] / b['ds_barrel_um'] - 1) / np.log(2)
        c2s = (2 * h['svd'] / b['svd'] - 1) / np.log(2)
        ce = b['c_ev']; r = (c2 - ce)[ok]; rs = (c2s - ce)[ok]; cev = ce[ok]
        pop = np.median(c2[ok]) / np.median(cev) - 1; pops = np.median(c2s[ok]) / np.median(cev) - 1
        pm, pe = bmed(r / cev)
        # deterministic symmetric-scatter model: reflect r about its gamma*-bin median, pool both signs
        gb = np.digitize(b['gstar'][ok], [1.05, 1.15, 1.3, 1.6, 2.0]); r0 = r.copy()
        for g in np.unique(gb):
            r0[gb == g] -= np.median(r[gb == g])
        sym = np.median(np.r_[cev + r0, cev - r0]) / np.median(np.r_[cev, cev]) - 1
        # same but reflect about k_B-bin median (conditional on k_B, the relevant variable)
        kb = np.digitize(b['k_B'][ok], [2, 4, 6, 10]); r1 = r.copy()
        for g in np.unique(kb):
            r1[kb == g] -= np.median(r[kb == g])
        symk = np.median(np.r_[cev + r1, cev - r1]) / np.median(cev) - 1
        print(f'{pk:8s} pop {100*pop:+6.2f}% (svd {100*pops:+6.2f}%)  paired r/cev {100*pm:+6.2f}+-{100*pe:.2f}%  '
              f'sym(g*) {100*sym:+5.2f}%  sym(kB) {100*symk:+5.2f}%  f(kB>=6) {np.mean(b["k_B"][ok] >= 6):.2f}  '
              f'ds_B(B0) med {np.median(b["svd"][ok]):.3f} um')
        allr += list(r / cev); allk += list(b['k_B'][ok]); allrs += list(rs / cev); alle += list(b['eps_perp'][ok])
    allr = np.array(allr); allk = np.array(allk); allrs = np.array(allrs); alle = np.array(alle)
    print(' pooled median r/c_ev by k_B bin: stored | SVD')
    for a, bb in BINS:
        s = (allk >= a) & (allk < bb)
        m1, e1 = bmed(allr[s]); m2, e2 = bmed(allrs[s])
        print(f'   [{a:g},{bb:g}) n={s.sum():4d}  {100*m1:+6.1f}+-{100*e1:.1f}%  |  {100*m2:+6.1f}+-{100*e2:.1f}%   '
              f'median eps_perp {np.median(alle[s]):.2e}')
    np.savez(Path(__file__).with_name(f'pooled_L{lam:g}.npz'), r=allr, rs=allrs, kB=allk, eps=alle)
