"""M3_thickness.py -- E2 measurement M3: truth-level B-only plane thickness scans with bootstrap uncertainties.

Events: T2 LO DY+ISR kinematics cache (T3_propagator.sample_events, pT(QQ) > 200 GeV, |eta_pair| < 1), the same NEV events
for every Lambda / B at a given m (seed 777 + m).  NOTE: Stage 3 will redo this on MadGraph samples.
Propagator: nm_kernel.run (= T3_causal B-only, bit-identical hits), uniform B, no material.
Lambda scan: m = 200, 500, 1000 GeV x Lambda = 0.45, 0.6, 1, 2, 3, 5, 10 keV at B0 = 3.8112 T.
B scan: f = B/B0 in {0, 1/1000, 1/80, 1/20, 1/4, 1/2, 1, 2} at Lambda = 1, 3 keV, m = 500, 1000 GeV (f = 0 = vacuum
reference for hit displacements).
Settings: 'prod' max_boost 1e-2, hmax 0.2 cm (T3 production); 'fine' 1e-3, 0.02 cm on the first NFINE events (M4).
Per event and f: Delta_s (plane through the origin, all hits on the 10 barrel layers, T3 definition), hits
[quirk, layer, t, x, y, z, beta, p, count], vacuum crossing spacing (lab time) and number of crossings inside r = 108.3 cm.
Output: data/stage1_numerics/M3/<tag>.npz (one per event; skipped if present).  Analysis: M3_analysis.py.
Run: pixi run python analytic/numerics/M3_thickness.py [prod|fine|all] [NEV] [NFINE]
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'M3'); os.makedirs(RAW, exist_ok=True)
MASSES = [200.0, 500.0, 1000.0]
LAMS = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 10.0]
FRACS = [0.0, 1e-3, 1 / 80, 1 / 20, 1 / 4, 1 / 2, 1.0, 2.0]
B0 = 3.8112


def job(args):
    m, lam, iev, p1, p2, info, setting, fracs = args
    tag = f"m{m:g}_L{lam:g}_e{iev:03d}_{setting}_{'B' if len(fracs) > 1 else 'L'}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 0.0
    from nm_kernel import run
    from T2_propagator import ExactPair, sigma_from_lambda_keV
    from T3_propagator import plane_fit
    sig = sigma_from_lambda_keV(lam)
    ex = ExactPair(p1, p2, m, m, sig)
    D, Dt = ex.crossing_spacing_lab()
    bT = np.hypot(*ex.beta[:2])
    ncross_in = int(np.floor(108.3 / max(bT * Dt, 1e-12)))
    mb, hm = (1e-2, 0.2) if setting == 'prod' else (1e-3, 0.02)
    t0 = time.time()
    out = dict(m=m, lam=lam, iev=iev, fracs=np.array(fracs), Dt=Dt, ncross_in=ncross_in, gstar=info['gstar'],
               pt=info['pt'], eta=info['eta'], cstar=ex.cos_theta_star, lmax=ex.lmax, p1=p1, p2=p2)
    ds = []; nh = []; st = []
    for j, f in enumerate(fracs):
        r = run(p1, p2, m, lam, B0=B0 * f, max_boost=mb, hmax_trk=hm, max_steps=4_000_000_000)
        H = r['hits']; H = H[H[:, 1] < 10]
        out[f'hits{j}'] = H
        ds.append(plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan); nh.append(len(H)); st.append(r['status'])
    out.update(ds=np.array(ds), nh=np.array(nh), status=np.array(st), cpu=time.time() - t0)
    np.savez(fn, **out)
    return tag, time.time() - t0


def build(which, nev, nfine):
    from T3_propagator import sample_events
    tasks = []
    for m in MASSES:
        evs = sample_events(m, nev, rng=np.random.default_rng(777 + int(m)), eta_max=1.0)
        for lam in LAMS:
            bscan = (m in (500.0, 1000.0)) and lam in (1.0, 3.0)
            fr = FRACS if bscan else [1.0]
            for i, (p1, p2, info) in enumerate(evs):
                info = {k: float(v) for k, v in info.items()}
                if which in ('prod', 'all'):
                    tasks.append((m, lam, i, p1, p2, info, 'prod', fr))
                if which in ('fine', 'all') and i < nfine and (m == 500.0 or bscan):
                    tasks.append((m, lam, i, p1, p2, info, 'fine', fr))
    return tasks


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    nev = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    nfine = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    tasks = build(which, nev, nfine)
    tasks.sort(key=lambda a: -(a[1] ** 2 * len(a[7]) * (10 if a[6] == 'fine' else 1)))
    tic = time.time(); cpu = 0.0
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        for i, (tag, dt) in enumerate(ex.map(job, tasks, chunksize=2)):
            cpu += dt
            if i % 200 == 0:
                print(f"[{i+1}/{len(tasks)}] {tag} {dt:.1f}s (wall {time.time()-tic:.0f}s, cpu {cpu:.0f}s)", flush=True)
    print(f"M3 {which}: {len(tasks)} jobs, wall {time.time()-tic:.0f} s, job cpu {cpu:.0f} s", flush=True)
