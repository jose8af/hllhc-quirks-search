"""p1_timing.py -- Stage-3 probe 1: T3_causal cost and step convergence vs (m, Lambda, configuration, max_boost).

Events: Stage-2 stitched trigger samples (E, TRGS), selection pT(QQ) > 200 GeV, |eta_pair| < 2.5, template half,
deterministic unweighting (mg_events.iter_events(..., unweight=True)); the first NEV events (same events at every Lambda).
Propagator: code/T3_causal.run_causal (unmodified), defaults except the settings listed (qcap 2^18, max_steps 4e9).
Configurations:  V  = vacuum (B = 0, no material)          B  = 3.8112 T, no material (Delta s_B)
                 BM = 3.8112 T + full material (dE/dx, straggling, MS)   M = B = 0 + full material (MS floor)
                 BE = 3.8112 T + mean dE/dx only (deterministic; pairs across step sizes)
Settings: 'c' = max_boost 1e-2, hmax 0.2 cm (T3 production); 'f' = 1e-3, 0.2 cm; 'ff' = 1e-3, 0.02 cm (Stage-1 'fine').
Per job: data/sim_stage3/probes/p1/<tag>.npz with hits [quirk, layer, t, x, y, z, beta, p, count], status, nsteps,
maxq, wall time, and the per-event analytic parameters (gamma*, eps_perp, b_odd/l0, l_max, c_ev) from
analytic/checks/c06_rotating_yoyo.pair_params (read only).
Run (from theory_track/): nice pixi run python sim/stage3/probes/p1_timing.py [nworkers]
Analysis: sim/stage3/probes/p1_analyse.py.
"""
import os, sys, time
import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
RAW = os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p1'); os.makedirs(RAW, exist_ok=True)
B0 = 3.8112
CFG = {'V': dict(B0=0.0, material=False), 'B': dict(B0=B0, material=False),
       'BM': dict(B0=B0, material=True), 'M': dict(B0=0.0, material=True),
       'BE': dict(B0=B0, material=True, ms=False, strag=False)}
SET = {'c': (1e-2, 0.2), 'f': (1e-3, 0.2), 'ff': (1e-3, 0.02)}
MASSES = [200, 500, 1000, 1500]


def plan_jobs():
    J = []
    for m in MASSES:
        for lam in (0.3, 0.6, 1.0, 2.0, 3.0, 5.0):
            for i in range(16):
                for cfg in ('B', 'BM', 'M'):
                    J.append((m, lam, i, cfg, 'c'))
                for cfg in ('B', 'BM'):
                    J.append((m, lam, i, cfg, 'f'))
                if i < 8:
                    J.append((m, lam, i, 'B', 'ff'))
                    J.append((m, lam, i, 'V', 'c'))
                    if lam in (1.0, 3.0):
                        J.append((m, lam, i, 'BE', 'c')); J.append((m, lam, i, 'BE', 'f'))
        for i in range(8):
            for cfg in ('B', 'BM', 'M'):
                J.append((m, 10.0, i, cfg, 'c'))
            if i < 3:
                J.append((m, 10.0, i, 'B', 'f')); J.append((m, 10.0, i, 'BM', 'f'))
        for i in range(6):
            for cfg in ('B', 'BM', 'M'):
                J.append((m, 20.0, i, cfg, 'c'))
        for i in range(4):
            for cfg in ('B', 'BM'):
                J.append((m, 30.0, i, cfg, 'c'))
    # expected cost ~ Lambda^2.5 / max_boost x (material factor): run expensive first
    def cost(j):
        m, lam, i, cfg, s = j
        return lam ** 2.5 / SET[s][0] * (3.0 if cfg in ('BM', 'M') else 1.0) / (SET[s][1] / 0.2) ** 0.3
    return sorted(J, key=cost, reverse=True)


def job(args):
    m, lam, i, cfg, s = args
    tag = f"m{m}_L{lam:g}_e{i:02d}_{cfg}_{s}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, None
    sys.path.insert(0, os.path.join(TT, 'code')); sys.path.insert(0, os.path.join(TT, 'sim', 'scripts'))
    sys.path.insert(0, os.path.join(TT, 'analytic', 'checks'))
    import mg_events as mg
    from T3_causal import run_causal
    from c06_rotating_yoyo import pair_params, K_of
    ev = mg.iter_events(m, 'trig', 'F', eta_max=2.5, ptmin=200.0, split='template', unweight=True)
    for k, e in enumerate(ev):
        if k == i:
            p1, p2, info = e
            break
    mb, hm = SET[s]
    seed = 1000003 * m + 7919 * i + 17
    t0 = time.perf_counter()
    r = run_causal(p1, p2, float(m), lam, max_boost=mb, hmax_trk=hm, seed=seed, qcap=1 << 18,
                   max_steps=4_000_000_000, **CFG[cfg])
    dt = time.perf_counter() - t0
    pp = pair_params(p1, p2, float(m), lam)
    np.savez_compressed(fn, hits=r['hits'], status=r['status'], nsteps=r['nsteps'], maxq=r['maxq'], wall=dt,
                        X=r['X'], P=r['P'], eacc=r['eacc'], p1=p1, p2=p2, m=m, lam=lam, iev=i, cfg=cfg, setting=s,
                        max_boost=mb, hmax=hm, seed=seed, gstar=pp['gs'], eps_perp=pp['eps_perp'],
                        bodd_l0=pp['bodd'] / pp['l0'], lmax=pp['lmax'], c_ev=1.0 / (pp['L'] + K_of(pp['gs'])),
                        pt=info['pt'], eta=info['eta'], row=info['idx'])
    return tag, dt


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    nw = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    jobs = plan_jobs()
    print(f'{len(jobs)} jobs, {nw} workers', flush=True)
    t0 = time.time(); n = 0
    with ProcessPoolExecutor(nw) as ex:
        futs = [ex.submit(job, j) for j in jobs]
        for f in as_completed(futs):
            tag, dt = f.result(); n += 1
            if dt is not None and (dt > 20 or n % 200 == 0):
                print(f'[{n}/{len(jobs)}] {tag} {dt:.1f} s  (elapsed {time.time() - t0:.0f} s)', flush=True)
    print(f'done in {time.time() - t0:.0f} s', flush=True)
