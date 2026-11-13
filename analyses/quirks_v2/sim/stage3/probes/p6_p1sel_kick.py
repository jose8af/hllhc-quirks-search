"""p6_p1sel_kick.py -- Stage-3 probe 6: (a) cost on the P1 selection (|eta_pair| < 1); (b) why B+M is 5-10x costlier than
B at high Lambda, and whether max_boost 1e-2 is converged when the pair carries angular momentum.

(a) E 500/1000 GeV, |eta_pair| < 1, both halves, unweighted, first 6 events: B at max_boost 1e-3 (P1 Delta s_B setting)
    at 1/3/5/7/10 keV and B/2 at 3/5 keV; BM at 1e-2 at 1/3/5/10 keV.
(b) Configuration BK = B0, no material, ONE deterministic kick of 3 MeV (a typical single-layer Highland kick,
    13.6 MeV x sqrt(0.012)/beta) perpendicular to quirk 0's momentum in the transverse plane, applied when quirk 0 first
    crosses r = 3.0 cm (T3_causal's kick option; code unmodified).  It gives the pair a deterministic J != 0, as MS does.
    Cost of BK vs B vs BM at 10/20 keV (1e-2), and hit convergence BK 1e-2 vs 1e-3 at 3 and 10 keV (3 events).
Output: data/sim_stage3/probes/p6/*.npz, p6_summary.json.  Run: nice pixi run python sim/stage3/probes/p6_p1sel_kick.py [nw]
"""
import glob, json, os, sys, time
import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
RAW = os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p6'); os.makedirs(RAW, exist_ok=True)
B0 = 3.8112


def jobs():
    J = []
    for m in (500, 1000):
        for i in range(6):
            for lam in (1.0, 3.0, 5.0, 7.0, 10.0):
                J.append((m, lam, i, 'B', 1e-3))
            for lam in (3.0, 5.0):
                J.append((m, lam, i, 'B2', 1e-3))
            for lam in (1.0, 3.0, 5.0, 10.0):
                J.append((m, lam, i, 'BM', 1e-2))
            for lam in (10.0, 20.0):
                J.append((m, lam, i, 'BK', 1e-2)); J.append((m, lam, i, 'B', 1e-2))
            J.append((m, 20.0, i, 'BM', 1e-2))
            J.append((m, 3.0, i, 'BK', 1e-2)); J.append((m, 3.0, i, 'BK', 1e-3))
            if i < 3:
                J.append((m, 10.0, i, 'BK', 1e-3))
    return sorted(J, key=lambda j: j[1] ** 2.5 / j[4] * (4 if j[3] in ('BM', 'BK') else 1), reverse=True)


def job(a):
    m, lam, i, cfg, mb = a
    fn = os.path.join(RAW, f'm{m}_L{lam:g}_e{i}_{cfg}_mb{mb:g}.npz')
    if os.path.exists(fn):
        return
    sys.path.insert(0, os.path.join(TT, 'code')); sys.path.insert(0, os.path.join(TT, 'sim', 'scripts'))
    import mg_events as mg
    from T3_causal import run_causal
    for k, e in enumerate(mg.iter_events(m, 'trig', 'F', eta_max=1.0, ptmin=200.0, unweight=True)):
        if k == i:
            p1, p2, info = e
            break
    kw = dict(B0=B0, material=False)
    if cfg == 'B2':
        kw['B0'] = B0 / 2
    elif cfg == 'BM':
        kw = dict(B0=B0, material=True)
    elif cfg == 'BK':
        u = np.cross(p1, [0.0, 0.0, 1.0]); u /= np.linalg.norm(u)
        kw['kick'] = (0, 3.0, 3e-3 * u)
    t0 = time.perf_counter()
    r = run_causal(p1, p2, float(m), lam, max_boost=mb, seed=1000003 * m + 7919 * i + 17, qcap=1 << 18,
                   max_steps=8_000_000_000, **kw)
    np.savez_compressed(fn, hits=r['hits'], status=r['status'], nsteps=r['nsteps'], wall=time.perf_counter() - t0)


def analyse():
    sys.path.insert(0, os.path.join(TT, 'code'))
    from T3_propagator import plane_fit
    L = {}
    for fn in glob.glob(os.path.join(RAW, '*.npz')):
        b = os.path.basename(fn)[:-4].split('_')
        L[(int(b[0][1:]), float(b[1][1:]), int(b[2][1:]), b[3], float(b[4][2:]))] = np.load(fn)
    out = {'cost': {}, 'conv': {}}
    keys = sorted({(k[0], k[1], k[3], k[4]) for k in L})
    for (m, lam, cfg, mb) in keys:
        t = [float(L[(m, lam, i, cfg, mb)]['wall']) for i in range(6) if (m, lam, i, cfg, mb) in L]
        ns = [int(L[(m, lam, i, cfg, mb)]['nsteps']) for i in range(6) if (m, lam, i, cfg, mb) in L]
        st = [int(L[(m, lam, i, cfg, mb)]['status']) for i in range(6) if (m, lam, i, cfg, mb) in L]
        out['cost'][f'm{m}_L{lam:g}_{cfg}_{mb:g}'] = dict(n=len(t), mean=float(np.mean(t)), max=float(np.max(t)),
                                                         nsteps_med=float(np.median(ns)), status=st)
        print(f'cost m{m} L{lam:g} {cfg} {mb:g}: n={len(t)} mean {np.mean(t):.2f} s max {np.max(t):.2f} nsteps {np.median(ns):.3g} status {st}')
    for m in (500, 1000):
        for lam in (3.0, 10.0):
            o, ip, un, r = [], [], 0, []
            for i in range(6):
                a = L.get((m, lam, i, 'BK', 1e-2)); b = L.get((m, lam, i, 'BK', 1e-3))
                if a is None or b is None:
                    continue
                ha = a['hits'][a['hits'][:, 1] < 10]; hb = b['hits'][b['hits'][:, 1] < 10]
                da, _ = plane_fit(ha[:, 3:6]); db, n = plane_fit(hb[:, 3:6]); r.append(da / db)
                ka = {(int(h[0]), int(h[1]), int(h[8])): h[3:6] for h in ha}
                kb = {(int(h[0]), int(h[1]), int(h[8])): h[3:6] for h in hb}
                com = set(ka) & set(kb); un += len(set(ka) ^ set(kb))
                dv = np.array([ka[k] - kb[k] for k in com])
                o.append(float(np.abs(dv @ n).max() * 1e4)); ip.append(float(np.linalg.norm(dv - np.outer(dv @ n, n), axis=1).max() * 1e4))
            if o:
                out['conv'][f'BK_m{m}_L{lam:g}'] = dict(n=len(o), ds_ratio=[round(x, 4) for x in r], out_um_max=o, in_um_max=ip, unmatched=un)
                print(f'conv BK 1e-2 vs 1e-3 m{m} L{lam:g}:', out['conv'][f'BK_m{m}_L{lam:g}'])
    # P1 c from B and B2 at 1e-3
    for m in (500, 1000):
        for lam in (3.0, 5.0):
            cs = []
            for i in range(6):
                a = L.get((m, lam, i, 'B', 1e-3)); b = L.get((m, lam, i, 'B2', 1e-3))
                if a is None or b is None:
                    continue
                da = plane_fit(a['hits'][a['hits'][:, 1] < 10][:, 3:6])[0]; db = plane_fit(b['hits'][b['hits'][:, 1] < 10][:, 3:6])[0]
                cs.append((2 * db / da - 1) / np.log(2))   # R(1/2) = 1 + c ln 2 (NEAR_MISS §5.3)
            if cs:
                print(f'c(k_f=2) per event m{m} L{lam:g}: {np.round(cs, 4)}')
    json.dump(out, open(os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p6_summary.json'), 'w'), indent=1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'analyse':
        analyse(); sys.exit()
    mp.set_start_method('spawn', force=True)
    nw = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    with ProcessPoolExecutor(nw) as ex:
        list(ex.map(job, jobs()))
    analyse()
