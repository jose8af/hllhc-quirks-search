"""FIX1_runs.py -- E2 fix pass 1 (reviews S1-R1): new runs only; earlier results are not modified.

 vfine40 : A1(b) 3 keV, m = 500/1000 GeV, M3 events 0-39 (seed 777 + m), f = B/B0 in {1, 1/2, 1/4, 1/20}, causal max_boost 1e-4,
           hmax 0.005 cm, string-queue cap raised to 2^21 (the FU 1e-4 runs overflowed the default 2^16 in 45 % of cases).
 rep     : A1 / critical C4: 3 keV, 500 GeV, events 0-9, max_boost 1e-3; initial 3-momenta perturbed by relative 1e-14, 1e-10, 1e-8
           (3 replicas each) + unperturbed: is the excess deterministic? does the replica spread scale with the perturbation?
 li2     : B6(i): Li (nm_li, R1 equations) vs causal (max_boost 1e-3, hmax 0.02) thickness at gamma* = 2, Lambda = 1 keV, m = 500 GeV,
           pT = 300 GeV (R1/R2 recipe, R1_conformal_ng.make_event), 30 events (seed 2027), B = 3.8 T; Li at 1e-3 of the printed
           step for all, 3e-4 for the first 10 (convergence).  Hits: the 10 barrel radii, no z cut, both integrators.
 t3ev    : B6(ii): T3's own event list (T3_ms_thickness.py: rng 2026, sample_events(m, 60) for m = 200, 500, 1000 in turn),
           B only, production settings, Lambda = 1, 3 (60 events) and 10 keV (24) -> per-event comparison with
           figures/T3_ms_thickness.npy and population comparison with the M3 sample.
 M1 extra: B6(iii): M1_events.job 'fine' for events 20-59 at Lambda = 0.6, 1, 2 keV (all masses) and 'vfine' (1e-4) for
           events 0-9 at Lambda = 1 keV (all masses) -> step dependence of the low-gamma* residual.
Outputs: data/stage1_numerics/FIX1/<tag>.npz and data/stage1_numerics/M1/ (M1 extra), one per job, skipped if present.
Run: pixi run python analytic/numerics/FIX1_runs.py
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'FIX1'); os.makedirs(RAW, exist_ok=True)
B0 = 3.8112
FR = [1.0, 0.5, 0.25, 0.05]


def job(args):
    kind = args[0]
    tag = '_'.join(str(a) for a in args[1:] if not isinstance(a, (np.ndarray, dict, list, tuple)))
    tag = f"{kind}_{tag}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 0.0
    from nm_kernel import run
    from T3_propagator import plane_fit
    t0 = time.time()
    if kind in ('vfine40', 'rep'):
        _, m, iev, delta, j, p1, p2 = args
        p1 = np.array(p1, float); p2 = np.array(p2, float)
        if delta > 0:
            rng = np.random.default_rng(int(1e6 * j) + iev + int(-np.log10(delta)) * 1000)
            p1 = p1 * (1 + delta * rng.standard_normal(3)); p2 = p2 * (1 + delta * rng.standard_normal(3))
        mb, hm = (1e-4, 0.005) if kind == 'vfine40' else (1e-3, 0.02)
        ds, st = [], []
        for f in FR:
            r = run(p1, p2, m, 3.0, B0=B0 * f, max_boost=mb, hmax_trk=hm, max_steps=8_000_000_000, qcap=1 << 21)
            H = r['hits']; H = H[H[:, 1] < 10]
            ds.append(plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan); st.append(r['status'])
        np.savez(fn, ds=np.array(ds), fr=np.array(FR), status=np.array(st), cpu=time.time() - t0)
    elif kind == 'li2':
        _, iev, frac, p1, p2 = args
        import nm_li
        from nm_conformal import RADII
        H, ns = nm_li.run_li(p1, p2, 500.0, 1.0, Bz=3.8, frac=frac) if frac > 0 else (None, 0)
        if frac > 0:
            np.savez(fn, ds=plane_fit(H[:, 3:6])[0], nh=len(H), cpu=time.time() - t0)
        else:
            r = run(p1, p2, 500.0, 1.0, B0=3.8, max_boost=1e-3, hmax_trk=0.02, rec_radii=RADII, rec_zmax=np.full(10, 1e9))
            np.savez(fn, ds=plane_fit(r['hits'][:, 3:6])[0], nh=len(r['hits']), status=r['status'], cpu=time.time() - t0)
    elif kind == 't3ev':
        _, m, lam, iev, p1, p2 = args
        r = run(p1, p2, m, lam, B0=B0)
        H = r['hits']; H = H[H[:, 1] < 10]
        np.savez(fn, ds=plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan, status=r['status'], cpu=time.time() - t0)
    return tag, time.time() - t0


if __name__ == '__main__':
    from T3_propagator import sample_events
    from R1_conformal_ng import make_event
    import M1_events as M1
    tasks = []
    for m in (500.0, 1000.0):
        evs = sample_events(m, 120, rng=np.random.default_rng(777 + int(m)), eta_max=1.0)
        for i in range(40):
            tasks.append(('vfine40', m, i, 0.0, 0, evs[i][0], evs[i][1]))
        if m == 500.0:
            for i in range(10):
                tasks.append(('rep', m, i, 0.0, 0, evs[i][0], evs[i][1]))
                for d in (1e-14, 1e-10, 1e-8):
                    for j in (1, 2, 3):
                        tasks.append(('rep', m, i, d, j, evs[i][0], evs[i][1]))
    rng = np.random.default_rng(2027)
    li_ev = [make_event(rng, 500.0, gstar=2.0, pt=300.0) for _ in range(30)]
    for i, (p1, p2) in enumerate(li_ev):
        tasks.append(('li2', i, 0.0, p1, p2))
        tasks.append(('li2', i, 1e-3, p1, p2))
        if i < 10:
            tasks.append(('li2', i, 3e-4, p1, p2))
    rng = np.random.default_rng(2026)
    for m in (200.0, 500.0, 1000.0):
        ev = sample_events(m, 60, rng=rng, eta_max=1.0)
        for lam, n in ((1.0, 60), (3.0, 60), (10.0, 24)):
            for k in range(n):
                tasks.append(('t3ev', m, lam, k, ev[k][0], ev[k][1]))
    m1 = []
    for t in M1.build_tasks('fine', 100, nfine=60):
        if t[2] >= 20 and t[1] in (0.6, 1.0, 2.0):
            m1.append(t)
    for t in M1.build_tasks('fine', 100, nfine=10):
        if t[1] == 1.0:
            m1.append(t[:6] + ('vfine',))
    tasks.sort(key=lambda a: -(100 if a[0] == 'vfine40' else 10 if a[0] == 'li2' and a[2] == 3e-4 else 1))
    tic = time.time(); cpu = 0.0
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        futs = [ex.submit(job, t) for t in tasks] + [ex.submit(M1.job, t) for t in m1]
        for i, fu in enumerate(futs):
            r = fu.result()
            cpu += r[-1] if isinstance(r[-1], float) else 0.0
            if i % 100 == 0:
                print(f"[{i+1}/{len(futs)}] {r[0]} (wall {time.time()-tic:.0f}s, cpu {cpu:.0f}s)", flush=True)
    print(f"FIX1 runs done: {len(futs)} jobs, wall {time.time()-tic:.0f} s, cpu {cpu:.0f} s", flush=True)
