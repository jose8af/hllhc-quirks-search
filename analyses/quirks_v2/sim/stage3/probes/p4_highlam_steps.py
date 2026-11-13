"""p4_highlam_steps.py -- Stage-3 probe 4: can the high-Lambda (10-40 keV) B+M production use a coarser max_boost?

Deterministic configuration BE (3.8112 T + mean dE/dx, no straggling, no MS) so that runs at different step settings are
paired event by event.  max_boost 3e-2 and 1e-2 at 10/20/30/40 keV, plus 1e-3 at 10 keV as the reference there.
Observables: hit positions matched by (quirk, layer, crossing count) on the 10 barrel layers, split into out-of-plane
(along the plane normal of the reference) and in-plane parts; number of unmatched hits; the CPU time.  Plus the cost of
40 keV BM at 1e-2 (stochastic, timing only).
Events: E 500 and 1500 GeV TRGS, |eta_pair| < 2.5, template, unweighted, first 4 events.  Kernel: code/T3_causal (unmodified).
Run: nice pixi run python sim/stage3/probes/p4_highlam_steps.py [nworkers]  -> data/sim_stage3/probes/p4/*.npz, p4_summary.json
"""
import json, os, sys, time, glob
import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
RAW = os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p4'); os.makedirs(RAW, exist_ok=True)
B0 = 3.8112


def jobs():
    J = []
    for m in (500, 1500):
        for i in range(4):
            for lam in (10.0, 20.0, 30.0, 40.0):
                for mb in (3e-2, 1e-2):
                    J.append((m, lam, i, 'BE', mb))
            J.append((m, 10.0, i, 'BE', 1e-3))
            J.append((m, 40.0, i, 'BM', 1e-2))
    return sorted(J, key=lambda j: j[1] ** 2.5 / j[4], reverse=True)


def job(a):
    m, lam, i, cfg, mb = a
    fn = os.path.join(RAW, f'm{m}_L{lam:g}_e{i}_{cfg}_mb{mb:g}.npz')
    if os.path.exists(fn):
        return
    sys.path.insert(0, os.path.join(TT, 'code')); sys.path.insert(0, os.path.join(TT, 'sim', 'scripts'))
    import mg_events as mg
    from T3_causal import run_causal
    for k, e in enumerate(mg.iter_events(m, 'trig', 'F', eta_max=2.5, ptmin=200.0, split='template', unweight=True)):
        if k == i:
            p1, p2, info = e
            break
    kw = dict(B0=B0, material=True, ms=False, strag=False) if cfg == 'BE' else dict(B0=B0, material=True)
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
    out = {}
    for m in (500, 1500):
        for lam in (10.0, 20.0, 30.0, 40.0):
            for test, ref in ((3e-2, 1e-2), (1e-2, 1e-3), (3e-2, 1e-3)):
                o, ip, un, tt, tr = [], [], 0, [], []
                for i in range(4):
                    a = L.get((m, lam, i, 'BE', test)); b = L.get((m, lam, i, 'BE', ref))
                    if a is None or b is None:
                        continue
                    ha = a['hits'][a['hits'][:, 1] < 10]; hb = b['hits'][b['hits'][:, 1] < 10]
                    _, n = plane_fit(hb[:, 3:6])
                    ka = {(int(h[0]), int(h[1]), int(h[8])): h[3:6] for h in ha}
                    kb = {(int(h[0]), int(h[1]), int(h[8])): h[3:6] for h in hb}
                    com = set(ka) & set(kb); un += len(set(ka) ^ set(kb))
                    dv = np.array([ka[k] - kb[k] for k in com])
                    o.append(np.abs(dv @ n).max() * 1e4); ip.append(np.linalg.norm(dv - np.outer(dv @ n, n), axis=1).max() * 1e4)
                    tt.append(float(a['wall'])); tr.append(float(b['wall']))
                if o:
                    k = f'm{m}_L{lam:g}_{test:g}vs{ref:g}'
                    out[k] = dict(n=len(o), out_um_max=[round(x, 3) for x in o], in_um_max=[round(x, 3) for x in ip],
                                  unmatched=un, t_test=float(np.mean(tt)), t_ref=float(np.mean(tr)))
                    print(k, out[k], flush=True)
            bm = [float(L[(m, lam, i, 'BM', 1e-2)]['wall']) for i in range(4) if (m, lam, i, 'BM', 1e-2) in L]
            if bm:
                out[f'm{m}_L{lam:g}_BM_1e-2_time'] = bm; print(m, lam, 'BM 1e-2 times', bm)
    json.dump(out, open(os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p4_summary.json'), 'w'), indent=1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'analyse':
        analyse(); sys.exit()
    mp.set_start_method('spawn', force=True)
    nw = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    with ProcessPoolExecutor(nw) as ex:
        list(ex.map(job, jobs()))
    analyse()
