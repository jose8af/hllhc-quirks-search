"""c13_population.py -- E1 fix pass S1-R1: population properties needed by the reviews (constructive B4, B7, B8; critical B1).
On the T3 event sample (sample_events, |eta_pair| < 1, ISR, seed 2026, 150 events per mass) computes, per event:
  gamma*, kB = |B*_perp n| / |E*_perp n| (CM frame), sin alpha, f_N = |e_perp . N| (out-of-plane share of the rotation,
  N = unit(n x beta) in the CM), and the rotating-yo-yo Delta s_B (c06 model) at 1 keV.
Outputs: (1) fractions of events per gamma* bin and per kB bin, joint table; (2) per-gamma*-bin accuracy of the
rotating-yo-yo model vs the causal string, from the c06 event-by-event outputs; (3) angle dependence: median Ds/median(Ds)
vs f_N and vs sin alpha; (4) |q| = 2 (fermion) and scalar E~ (spin 'S' sample) population predictions (c, Ds) at 1 and 3 keV.
Run: pixi run python analytic/checks/c13_population.py > analytic/checks/c13_population_out.txt
"""
import os, sys, glob, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c06_rotating_yoyo import model_hits, pair_params, K_of, plane_fit, sample_events, B_CMS, EB_GEV_PER_CM_PER_T  # noqa

GB = [1.0, 1.1, 1.2, 1.35, 1.6, 2.0, 10.0]
KBB = [0, 2, 4, 6, 8, 12, 1e9]


def angles(p1, p2, m, lam, B=B_CMS):
    pp = pair_params(p1, p2, m, lam)
    beta = pp['beta']; g = pp['g']; bh = beta / np.linalg.norm(beta); n = pp['n']
    Bv = np.array([0, 0, B])
    Es = g * np.cross(beta, Bv)
    Bs = g * Bv - (g - 1) * (Bv @ bh) * bh
    Ep = Es - (Es @ n) * n; Bp = Bs - (Bs @ n) * n
    kB = np.linalg.norm(Bp) / np.linalg.norm(Ep)
    sina = np.linalg.norm(Ep) / np.linalg.norm(Es)
    N = np.cross(n, bh); N /= np.linalg.norm(N)
    fN = abs((Ep / np.linalg.norm(Ep)) @ N)
    return pp, kB, sina, fN


def binfrac(x, edges):
    h, _ = np.histogram(x, edges)
    return h / len(x)


if __name__ == '__main__':
    # (1) fractions
    print('## (1) event fractions (T3 sample, 150 events per mass)')
    allg, allk = {}, {}
    for m in (200.0, 500.0, 1000.0):
        ev = sample_events(m, 150, rng=np.random.default_rng(2026), eta_max=1.0)
        gs, ks = [], []
        for p1, p2, info in ev:
            pp, kB, sa, fN = angles(p1, p2, m, 1.0)
            gs.append(pp['gs']); ks.append(kB)
        allg[m] = np.array(gs); allk[m] = np.array(ks)
        print(f'm={m:.0f}: gamma* bins {GB[:-1]}+ : ' + ' '.join(f'{f:.3f}' for f in binfrac(allg[m], GB)) +
              f' | kB bins {KBB[:-1]}+ : ' + ' '.join(f'{f:.3f}' for f in binfrac(allk[m], KBB)) +
              f' | median kB {np.median(allk[m]):.2f}; f(kB>6) = {np.mean(allk[m] > 6):.3f}; f(kB>8) = {np.mean(allk[m] > 8):.3f}')
    # (2) per-gamma*-bin accuracy from c06 outputs
    print('\n## (2) rotating-yo-yo / causal Delta s per gamma* bin (c06 outputs, all masses and Lambda)')
    rows = []
    for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c06_rotating_yoyo_out_*.txt')):
        lam = None
        for line in open(f):
            mm = re.match(r'# m=(\d+) GeV, Lambda=([\d.]+) keV', line)
            if mm:
                lam = float(mm.group(2)); continue
            if line.strip() and not line.startswith('#'):
                tok = line.split()
                try:
                    rows.append((lam, float(tok[1]), float(tok[8])))
                except (ValueError, IndexError):
                    pass
    rows = np.array(rows)
    for lo, hi in zip(GB[:-1], GB[1:]):
        for lamsel, name in ((rows[:, 0] <= 3.0, '0.6-3 keV'), (rows[:, 0] > 3.0, '10 keV')):
            sel = lamsel & (rows[:, 1] >= lo) & (rows[:, 1] < hi)
            if sel.sum():
                r = rows[sel, 2]
                print(f'gamma* {lo}-{hi} ({name}): n={sel.sum():2d}  median ratio {np.median(r):.3f}  range {r.min():.3f}-{r.max():.3f}')
    # (3) angle dependence (model, 1 keV, 500 GeV)
    print('\n## (3) angle dependence, rotating-yo-yo Delta s at 1 keV, 500 GeV, 150 events')
    m = 500.0
    ev = sample_events(m, 150, rng=np.random.default_rng(2026), eta_max=1.0)
    ds, fNs, sas, kbs = [], [], [], []
    for p1, p2, info in ev:
        H, pp = model_hits(p1, p2, m, 1.0)
        _, kB, sa, fN = angles(p1, p2, m, 1.0)
        ds.append(plane_fit(H[:, 2:5])[0]); fNs.append(fN); sas.append(sa); kbs.append(kB)
    ds = np.array(ds); fNs = np.array(fNs); sas = np.array(sas); med = np.median(ds)
    for name, x, edges in (('f_N = |e_perp.N|', fNs, [0, 0.25, 0.5, 0.75, 0.9, 1.01]), ('sin alpha', sas, [0, 0.4, 0.6, 0.8, 0.9, 1.01])):
        print(name + ': ' + '; '.join(f'[{lo},{hi}): n={((x>=lo)&(x<hi)).sum()}, med Ds/med = {np.median(ds[(x>=lo)&(x<hi)])/med:.2f}'
                                     for lo, hi in zip(edges[:-1], edges[1:]) if ((x >= lo) & (x < hi)).sum()))
    print(f'correlation of Ds with f_N: Spearman-like rank corr = {np.corrcoef(np.argsort(np.argsort(ds)), np.argsort(np.argsort(fNs)))[0,1]:.2f}')
    # (4) |q| = 2 and scalar
    print('\n## (4) |q| = 2 (fermion E) and scalar E~ (spin S), m = 500 GeV, 150 events, B = 3.8112 T')
    for lam in (1.0, 3.0):
        for label, spin, q in (('fermion q=1', 'F', 1.0), ('fermion q=2', 'F', 2.0), ('scalar q=1', 'S', 1.0)):
            ev = sample_events(m, 150, rng=np.random.default_rng(2026), eta_max=1.0, spin=spin)
            ds, cs, gs = [], [], []
            for p1, p2, info in ev:
                H, pp = model_hits(p1, p2, m, lam, q=q)
                if len(H) < 4:
                    continue
                ds.append(plane_fit(H[:, 2:5])[0] * 1e4); cs.append(1 / (pp['L'] + K_of(pp['gs']))); gs.append(pp['gs'])
            print(f'Lambda={lam} {label}: median Ds = {np.median(ds):.3g} um, median c = {np.median(cs):.4f}, '
                  f'median gamma* = {np.median(gs):.3f}, f(gamma*>1.6) = {np.mean(np.array(gs)>1.6):.2f}', flush=True)
