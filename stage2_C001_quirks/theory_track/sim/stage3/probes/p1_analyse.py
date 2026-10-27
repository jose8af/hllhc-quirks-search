"""p1_analyse.py -- analysis of Stage-3 probe 1 (p1_timing.py): cost model and step convergence.

Reads data/sim_stage3/probes/p1/*.npz.  Writes data/sim_stage3/probes/p1_summary.json and prints tables:
 (1) cost per event [s, 1 core of this M-series Mac, nice 10, 7 workers busy] per (m, Lambda, cfg, setting): mean, median,
     p90, max; nsteps; status counts; hits per event;
 (2) cost model fit: t = a(cfg, setting) * Lambda^p (mean over events, all masses), and the mass dependence;
 (3) convergence: settings c (1e-2, 0.2 cm) vs f (1e-3, 0.2 cm) vs ff (1e-3, 0.02 cm) for the deterministic configs B, BE:
     Delta s (10 barrel layers, plane through the origin) ratio, and hit displacements matched by (quirk, layer, crossing
     count), split into out-of-plane (along the reference plane normal) and in-plane parts; BM (stochastic): medians only;
 (4) floor indicator: fraction of events with b_odd/l0 < 1e-7 and the c-vs-f Delta s_B change for them.
Run: pixi run python sim/stage3/probes/p1_analyse.py
"""
import glob, json, os, sys
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(TT, 'code'))
from T3_propagator import plane_fit  # noqa: E402

RAW = os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p1')
D = {}
for fn in glob.glob(os.path.join(RAW, '*.npz')):
    z = np.load(fn)
    key = (int(z['m']), float(z['lam']), int(z['iev']), str(z['cfg']), str(z['setting']))
    D[key] = {k: z[k] for k in ('hits', 'status', 'nsteps', 'maxq', 'wall', 'gstar', 'bodd_l0', 'eps_perp', 'c_ev', 'eta', 'pt')}
print(f'{len(D)} job files')


def ds_barrel(h):
    H = h[h[:, 1] < 10]
    if len(H) < 4:
        return np.nan, None
    d, n = plane_fit(H[:, 3:6])
    return d, n


# (1) cost table
G = defaultdict(list)
for (m, lam, i, cfg, s), v in D.items():
    G[(m, lam, cfg, s)].append(v)
cost = {}
print('\n(1) cost per event [s]: m lam cfg set | n mean median p90 max | nsteps_med | status | hits_med')
for key in sorted(G):
    L = G[key]
    t = np.array([float(v['wall']) for v in L]); ns = np.array([int(v['nsteps']) for v in L])
    st = np.bincount(np.array([int(v['status']) for v in L]), minlength=6).tolist()
    nh = np.median([len(v['hits']) for v in L])
    cost['%d_%g_%s_%s' % key] = dict(n=len(L), mean=float(t.mean()), median=float(np.median(t)), p90=float(np.percentile(t, 90)),
                                     max=float(t.max()), nsteps_med=float(np.median(ns)), ns_per_step=float(t.sum() / ns.sum() * 1e9),
                                     status=st, hits_med=float(nh))
    print('%5d %5g %3s %2s | %3d %8.3f %8.3f %8.3f %8.3f | %.3g | %s | %d' % (*key, len(L), t.mean(), np.median(t),
          np.percentile(t, 90), t.max(), np.median(ns), st, nh))

# (2) cost model: mean time vs Lambda per (cfg, setting), pooled over masses (only complete-ish groups)
model = {}
print('\n(2) fit mean t = a * Lambda^p (pooled over masses), per cfg/setting; and per-mass means at 3 keV and 10 keV')
for cfg in ('V', 'B', 'BM', 'M', 'BE'):
    for s in ('c', 'f', 'ff'):
        pts = [(lam, np.mean([float(v['wall']) for v in G[(m, lam, cfg, s)]])) for (m, lam, c2, s2) in G
               if c2 == cfg and s2 == s and lam >= 1.0]
        if len(pts) < 3:
            continue
        x = np.log([p[0] for p in pts]); y = np.log([p[1] for p in pts])
        p, lna = np.polyfit(x, y, 1)
        model[f'{cfg}_{s}'] = dict(a=float(np.exp(lna)), p=float(p), npts=len(pts))
        print(f'  {cfg:3s} {s:2s}: a = {np.exp(lna):.4g} s, p = {p:.2f} ({len(pts)} points)')
for lam in (3.0, 10.0, 20.0, 30.0):
    for cfg in ('B', 'BM', 'M'):
        row = [np.mean([float(v['wall']) for v in G[(m, lam, cfg, 'c')]]) if (m, lam, cfg, 'c') in G else np.nan for m in (200, 500, 1000, 1500)]
        print(f'  per-mass mean, {lam:g} keV {cfg:3s} c: ' + ' '.join(f'{r:8.2f}' for r in row))

# (3) convergence for deterministic configs
print('\n(3) convergence (deterministic configs): ratio Delta s(test)/Delta s(ref); hit displacement [um] (median of per-event max)')
conv = {}
for cfg in ('B', 'BE'):
    for test, ref in (('c', 'f'), ('f', 'ff'), ('c', 'ff')):
        for m in (200, 500, 1000, 1500):
            for lam in (0.3, 0.6, 1.0, 2.0, 3.0, 5.0, 10.0):
                rr, dout, din, nmis = [], [], [], 0
                for i in range(16):
                    a = D.get((m, lam, i, cfg, test)); b = D.get((m, lam, i, cfg, ref))
                    if a is None or b is None:
                        continue
                    da, _ = ds_barrel(a['hits']); db, nb = ds_barrel(b['hits'])
                    if not (np.isfinite(da) and np.isfinite(db)) or db == 0:
                        continue
                    rr.append(da / db)
                    ka = {(int(h[0]), int(h[1]), int(h[8])): h[3:6] for h in a['hits'] if h[1] < 10}
                    kb = {(int(h[0]), int(h[1]), int(h[8])): h[3:6] for h in b['hits'] if h[1] < 10}
                    common = set(ka) & set(kb)
                    nmis += len(set(ka) ^ set(kb))
                    if common:
                        dv = np.array([ka[k] - kb[k] for k in common])
                        o = np.abs(dv @ nb); ip = np.linalg.norm(dv - np.outer(dv @ nb, nb), axis=1)
                        dout.append(o.max() * 1e4); din.append(ip.max() * 1e4)
                if rr:
                    k = f'{cfg}_{test}vs{ref}_m{m}_L{lam:g}'
                    conv[k] = dict(n=len(rr), ds_ratio_med=float(np.median(rr)), ds_ratio_p16=float(np.percentile(rr, 16)),
                                   ds_ratio_p84=float(np.percentile(rr, 84)), out_um_med=float(np.median(dout)) if dout else None,
                                   out_um_max=float(np.max(dout)) if dout else None, in_um_med=float(np.median(din)) if din else None,
                                   in_um_max=float(np.max(din)) if din else None, unmatched_hits=nmis)
                    print(f'  {k:28s} n={len(rr):2d} ratio {np.median(rr):.4f} ({np.percentile(rr, 16):.4f}-{np.percentile(rr, 84):.4f}) '
                          f'out {conv[k]["out_um_med"]} / max {conv[k]["out_um_max"]}  in {conv[k]["in_um_med"]} / max {conv[k]["in_um_max"]} unmatched {nmis}')

# BM medians c vs f (stochastic)
print('\n    BM (stochastic) median Delta s [um], c vs f, and M c:')
bm = {}
for m in (200, 500, 1000, 1500):
    for lam in (0.3, 0.6, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0):
        row = {}
        for cfg, s in (('BM', 'c'), ('BM', 'f'), ('M', 'c'), ('B', 'c'), ('B', 'f')):
            v = [ds_barrel(D[(m, lam, i, cfg, s)]['hits'])[0] for i in range(16) if (m, lam, i, cfg, s) in D]
            v = [x for x in v if np.isfinite(x)]
            row[f'{cfg}_{s}'] = (float(np.median(v) * 1e4), len(v)) if v else None
        bm[f'm{m}_L{lam:g}'] = row
        print(f'  m{m} L{lam:g}: ' + '  '.join(f'{k} {v[0]:.3g}({v[1]})' for k, v in row.items() if v))

# (4) floor indicator
print('\n(4) floor: fraction of events with b_odd/l0 < 1e-7 (B, c) and median |Ds_c/Ds_f - 1| for them vs the others')
floor = {}
for m in (200, 500, 1000, 1500):
    for lam in (3.0, 5.0, 10.0, 20.0, 30.0):
        b = [D[(m, lam, i, 'B', 'c')] for i in range(16) if (m, lam, i, 'B', 'c') in D]
        if not b:
            continue
        fl = np.array([float(v['bodd_l0']) < 1e-7 for v in b])
        floor[f'm{m}_L{lam:g}'] = {"n": len(b), "f_below_1e-7": float(fl.mean())}
        print(f'  m{m} L{lam:g}: n={len(b)} f(b_odd/l0<1e-7) = {fl.mean():.2f}')

json.dump(dict(cost=cost, model=model, convergence=conv, ds_medians=bm, floor=floor),
          open(os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p1_summary.json'), 'w'), indent=1)
