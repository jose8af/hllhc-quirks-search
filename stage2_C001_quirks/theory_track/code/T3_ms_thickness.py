"""T3_ms_thickness.py -- plane thickness of quirk-pair hits with and without multiple scattering (Q1).

For each (m_Q, Lambda) on the grid m in {200, 500, 1000} GeV x Lambda in {0.3, 1, 3, 10, 30} keV, sample LO DY+ISR
pairs from the T2 cache (pT(QQ) > 200 GeV, |eta_pair| < 1) and propagate each pair with the causal Nambu-Goto propagator T3_causal.run_causal (numba port of the
Athena/T2 algorithm; the lab straight-string kernel of T3_propagator is NOT used here, see T3_causal.py header) in four
configurations, same initial momenta:
   B      : uniform 3.8112 T, no material                     (B-field thickness only; the literature case)
   B+E    : 3.8 T + mean dE/dx + straggling, no MS
   B+M    : 3.8 T + full material (MS + dE/dx + straggling)   (realistic)
   M      : B = 0 + full material                              (MS-only thickness)
Hits: all crossings of the 10 barrel layers (IT r = 3.0/6.1/10.4/14.6 cm, |z| < 20 cm; OT 24.9..108.3 cm, |z| < 120 cm).
Thickness Delta_s = sqrt(min eigenvalue of T_ij = sum h_i h_j /(N-1)) for the plane through the origin
[1708.02243 Eq.11; 2002.07503 Eq.C.1]; also the max |n.h| and Delta_s from IT+PS hits only (CMS 3D points).
Material: T3_propagator.phase2_tracker(scale) (report Sec.2); scale = 1 nominal, 2 for the pessimistic variant.
Outputs: figures/T3_ms_thickness.npz (per-event table), printed summary tables, figures/T3_ms_thickness.png.
Run: pixi run python code/T3_ms_thickness.py [nev_low] [nev_high] [scale]     (default 300 120 1.0; ~20-40 min on 8 cores)
"""
import os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import plane_fit, sample_events, phase2_tracker
from T3_causal import run_causal

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
MASSES = [200.0, 500.0, 1000.0]
LAMS = [0.3, 1.0, 3.0, 10.0, 30.0]
CONFIGS = {'B': dict(B0=3.8112, material=False), 'B+E': dict(B0=3.8112, ms=False),
           'B+M': dict(B0=3.8112), 'M': dict(B0=0.0)}


def observables(hits):
    H = hits[hits[:, 1] < 10]
    if len(H) < 4:
        return np.nan, np.nan, np.nan, len(H)
    d, n = plane_fit(H[:, 3:6])
    res = np.abs(H[:, 3:6] @ n)
    sel = H[:, 1] < 7                                   # IT + PS (3D space points at CMS)
    d3 = plane_fit(H[sel, 3:6])[0] if sel.sum() >= 4 else np.nan
    return d, res.max(), d3, len(H)


def job(args):
    m, lam, k, p1, p2, scale, seed = args
    slabs = phase2_tracker(scale)
    out = []
    for name, cfg in CONFIGS.items():
        r = run_causal(p1, p2, m, lam, slabs=slabs, seed=seed, **cfg)
        out.append(observables(r['hits']))
    return (m, lam, k, out)


def summary(rows, scale=1.0):
    cols = list(CONFIGS)
    print('\nMedian (16-84 pct) plane thickness Delta_s [um], all 10 barrel layers, |eta_pair|<1, pT(QQ)>200 GeV, material x' + str(scale))
    print('| m_Q | Lambda [keV] | ' + ' | '.join(cols) + ' | f(Delta_s<100um) B | f B+M | Li formula 1.16um(m/100)(keV/L)^4 B |')
    print('|---|---|' + '---|' * len(cols) + '---|---|---|')
    for m in MASSES:
        for lam in LAMS:
            sel = (rows[:, 0] == m) & (rows[:, 1] == lam)
            cells = []
            for j, c in enumerate(cols):
                d = rows[sel, 6 + 4 * j] * 1e4
                d = d[np.isfinite(d)]
                q = np.percentile(d, [16, 50, 84])
                cells.append(f'{q[1]:.3g} ({q[0]:.2g}-{q[2]:.2g})')
            fB = np.mean(rows[sel, 6] * 1e4 < 100); fBM = np.mean(rows[sel, 6 + 8] * 1e4 < 100)
            li = 1.16 * (m / 100) * lam ** -4 * 3.8112
            print(f'| {m:.0f} | {lam:g} | ' + ' | '.join(cells) + f' | {fB:.2f} | {fBM:.2f} | {li:.3g} |')
    print('\nIT+PS-only thickness (3D points), median [um]: B vs B+M')
    for m in MASSES:
        print(m, [(lam, round(np.nanmedian(rows[(rows[:, 0] == m) & (rows[:, 1] == lam), 8]) * 1e4, 2),
                   round(np.nanmedian(rows[(rows[:, 0] == m) & (rows[:, 1] == lam), 8 + 8]) * 1e4, 2)) for lam in LAMS])
    print('\nmedian max |residual| [um]: B vs B+M')
    for m in MASSES:
        print(m, [(lam, round(np.nanmedian(rows[(rows[:, 0] == m) & (rows[:, 1] == lam), 7]) * 1e4, 1),
                   round(np.nanmedian(rows[(rows[:, 0] == m) & (rows[:, 1] == lam), 7 + 8]) * 1e4, 1)) for lam in LAMS])


if __name__ == '__main__':
    nlo = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    nhi = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    rng = np.random.default_rng(2026)
    tasks = []
    evinfo = {}
    for m in MASSES:
        ev = sample_events(m, nlo, rng=rng, eta_max=1.0)
        evinfo[m] = ev
        for lam in LAMS:
            n = nlo if lam <= 3 else (nhi if lam <= 10 else nhi // 2)
            for k in range(n):
                tasks.append((m, lam, k, ev[k][0], ev[k][1], scale, 1000 + k))
    tic = time.time()
    with Pool(8) as pool:
        res = pool.map(job, tasks, chunksize=4)
    print(f'{len(tasks)} jobs in {time.time()-tic:.0f} s', flush=True)
    rows = []
    for (m, lam, k, out) in res:
        info = evinfo[m][k][2]
        rows.append([m, lam, k, info['pt'], info['gstar'], info['eta']] + [v for o in out for v in o])
    rows = np.array(rows)
    tag = '' if scale == 1.0 else f'_x{scale:g}'
    np.save(os.path.join(FIG, f'T3_ms_thickness{tag}.npy'), rows)
    summary(rows, scale)
