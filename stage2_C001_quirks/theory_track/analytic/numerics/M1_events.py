"""M1_events.py -- E2 measurement M1: per-crossing diagnostics on full events (B = 3.8112 T uniform, no material).

Events: T2 LO DY+ISR kinematics cache (T3_propagator.sample_events, pT(QQ) > 200 GeV, |eta_pair| < 1), the same events
for every Lambda at a given m (seed 4242 + m).  Grid: m = 200, 500, 1000 GeV x Lambda = 0.6, 1, 2, 3, 5, 10 keV.
Settings: 'prod' = causal max_boost 1e-2, hmax 0.2 cm (T3 production), NEV events per point;
          'fine' = causal max_boost 1e-3, hmax 0.02 cm, first NFINE events (convergence, M4);
          'conf256'/'conf1024' = conformal solver N = 256/1024 on the first NCONF events at m = 500, Lambda <= 3 keV.
Per crossing (nm_crossings.analyse): b, b components (eN = plane normal, eP), cos(b, E*_perp), gamma*, v, l_before,
axis tilts dA_N/dA_P (turning point to turning point), TP-to-TP string / total impulse, r_lab, log-law fit of the
string impulse profile (kappa, kappa0).  eps_perp = q|E*_perp|/sigma per crossing.
Output: data/stage1_numerics/M1/<tag>.npz (one per event; skipped if present).  Merge: M1_analysis.py.
Run: pixi run python analytic/numerics/M1_events.py [prod|fine|conf|all] [NEV]
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'M1'); os.makedirs(RAW, exist_ok=True)
MASSES = [200.0, 500.0, 1000.0]
LAMS = [0.6, 1.0, 2.0, 3.0, 5.0, 10.0]
NEV_HIGH = 60      # production events at Lambda >= 5 keV (CPU); 100 at Lambda <= 3 keV (m = 200, 10 keV ran 100)
KEYS = ('k', 'parity', 'b', 'bN', 'bP', 'gamma1', 'vrel', 'l_before', 'dA_N', 'dA_P', 'dPiTP_N', 'dPiTP_P',
        'dJTP_N', 'dJTP_P', 'aN', 'aP', 'r_lab', 'flag', 'cos_b_E', 't', 'v1', 'E_perp', 'l_after')
B0 = 3.8112


def job(args):
    m, lam, iev, p1, p2, info, setting = args
    tag = f"m{m:g}_L{lam:g}_e{iev:03d}_{setting}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 'skip', 0.0
    from nm_kernel import run
    import nm_conformal as NC
    from nm_crossings import analyse, table, fit_profile
    from T2_propagator import ExactPair, sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T
    sig = sigma_from_lambda_keV(lam)
    ex = ExactPair(p1, p2, m, m, sig)
    Th = 2 * ex.pstar / sig
    P0 = np.r_[ex.E, ex.P]
    pi = (np.r_[np.hypot(m, np.linalg.norm(p1)), p1], np.r_[np.hypot(m, np.linalg.norm(p2)), p2])
    Es = ex.gamma * np.cross(ex.beta, [0, 0, B0]) * EB_GEV_PER_CM_PER_T
    t0 = time.time()
    valid = True
    if setting in ('prod', 'fine', 'vfine'):
        mb, hm = {'prod': (1e-2, 0.2), 'fine': (1e-3, 0.02), 'vfine': (1e-4, 0.005)}[setting]
        r = run(p1, p2, m, lam, B0=B0, rec=True, rec_dt=Th * ex.gamma / 60, rec_dlog=0.08, rec_near=6.0,
                max_rec=12_000_000, max_steps=4_000_000_000, max_boost=mb, hmax_trk=hm, qcap=1 << 21)
        res = analyse(r['rec'][0], r['rec'][1], 'causal', P0, m, sig, ex.n, Estar=Es, Th=Th, p_init=pi)
    else:
        N = int(setting[4:])
        r = NC.run(p1, p2, m, sigma=sig, Bz=B0, N=N, rec=True, rec_dt=Th * ex.gamma / 60, rec_dlog=0.08,
                   rec_near=6.0, max_rec=12_000_000)
        R0, R1 = r['rec']
        valid = bool(r['status'] != 7 and len(R0) > 10 and np.all(np.diff(R0[:, 1]) > 0) and np.all(np.diff(R1[:, 1]) > 0))
        res = analyse(R0, R1, 'conf', P0, m, sig, ex.n, Estar=Es, Th=Th, p_init=pi, h_conf=np.pi / N) if valid else None
    tk = time.time() - t0
    if res is None or len(res['crossings']) == 0:
        np.savez(fn, valid=False, T=np.zeros((0, len(KEYS))), keys=np.array(KEYS), status=r['status'])
        return tag, 'invalid/empty', tk
    T, _ = table(res, KEYS)
    fits = np.array([fit_profile(c, sig, Th) for c in res['crossings']])
    prof = np.array([c['profile'] for c in res['crossings'][:12]])
    np.savez(fn, valid=valid, T=T, keys=np.array(KEYS), fits=fits, prof=prof, m=m, lam=lam, sig=sig, Th=Th,
             gstar=info['gstar'], pt=info['pt'], eta=info['eta'], cstar=ex.cos_theta_star, lmax=ex.lmax,
             gamma_pair=ex.gamma, beta_pair=np.linalg.norm(ex.beta), Estar=np.linalg.norm(Es), nsteps=r['nsteps'],
             status=r['status'], cpu=time.time() - t0, p1=p1, p2=p2)
    return tag, f"{len(T)} crossings", time.time() - t0


def build_tasks(which, nev, nfine=20, nconf=6):
    from T3_propagator import sample_events
    tasks = []
    for m in MASSES:
        evs = sample_events(m, nev, rng=np.random.default_rng(4242 + int(m)), eta_max=1.0)
        for lam in LAMS:
            for i, (p1, p2, info) in enumerate(evs):
                info = {k: float(v) for k, v in info.items()}
                if which in ('prod', 'all') and (lam < 5.0 or i < NEV_HIGH or m == 200.0 and lam == 10.0):
                    tasks.append((m, lam, i, p1, p2, info, 'prod'))
                if which in ('fine', 'all') and i < nfine:
                    tasks.append((m, lam, i, p1, p2, info, 'fine'))
                if which in ('conf', 'all') and i < nconf and m == 500.0 and lam <= 3.0:
                    tasks.append((m, lam, i, p1, p2, info, 'conf256'))
                    tasks.append((m, lam, i, p1, p2, info, 'conf1024'))
    return tasks


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    nev = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    tasks = build_tasks(which, nev)
    # heavy jobs first for load balance
    tasks.sort(key=lambda a: -(a[1] ** 2 * (10 if a[6] == 'fine' else 1) * (30 if a[6].startswith('conf') else 1)))
    tic = time.time(); cpu = 0.0
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        for i, (tag, msg, dt) in enumerate(ex.map(job, tasks, chunksize=1)):
            cpu += dt
            if i % 50 == 0 or dt > 60:
                print(f"[{i+1}/{len(tasks)}] {tag}: {msg} {dt:.1f}s (wall {time.time()-tic:.0f}s, cpu {cpu:.0f}s)", flush=True)
    print(f"M1 {which}: {len(tasks)} jobs, wall {time.time()-tic:.0f} s, job cpu {cpu:.0f} s", flush=True)
