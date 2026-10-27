"""M4_conformal_thickness.py -- E2 (M4): solver independence of the M3 thickness and of its response per unit B.

The first NEV M3 events (m = 500 GeV, Lambda = 1 and 2 keV, same kinematics as M3_thickness.py, seed 777 + m) are re-run
with the conformal-gauge solver (nm_conformal = R1 formulation) at N = 1024 and 4096 for B = B0 x {1, 1/4, 1/20} and
compared with the causal kernel at max_boost 1e-3, hmax 0.02 cm: event-by-event Delta_s ratio and event-level response
R_ev(k) = Delta_s(B0/k) k / Delta_s(B0).  Hit sets: the 10 barrel radii, no z limit for both solvers (the conformal solver
has no z acceptance), so Delta_s here differs slightly from M3 for events with hits beyond |z| = 20/120 cm.
Output: results/M4_conformal_thickness.json.  Run: pixi run python analytic/numerics/M4_conformal_thickness.py [NEV]
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
B0 = 3.8112
KS = [1.0, 4.0, 20.0]


def job(args):
    i, lam, p1, p2 = args
    import nm_conformal as NC
    from nm_kernel import run
    from T3_propagator import plane_fit
    out = dict(i=i, lam=lam)
    t0 = time.time()
    for k in KS:
        r = run(p1, p2, 500.0, lam, B0=B0 / k, max_boost=1e-3, hmax_trk=0.02, rec_radii=NC.RADII, rec_zmax=np.full(10, 1e9))
        out[f'causal_k{k:g}'] = plane_fit(r['hits'][:, 3:6])[0]
        for N in (1024, 4096):
            rc = NC.run(p1, p2, 500.0, lam, Bz=B0 / k, N=N)
            ok = rc['status'] != 7
            out[f'conf{N}_k{k:g}'] = plane_fit(rc['hits'][:, 3:6])[0] if ok and len(rc['hits']) >= 4 else np.nan
    out['cpu'] = time.time() - t0
    return out


if __name__ == '__main__':
    from T3_propagator import sample_events
    from nm_stats import dump, boot
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    evs = sample_events(500.0, nev, rng=np.random.default_rng(777 + 500), eta_max=1.0)
    tasks = [(i, lam, p1, p2) for lam in (1.0, 2.0) for i, (p1, p2, _) in enumerate(evs)]
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        rows = list(ex.map(job, tasks))
    res = dict(description=__doc__, nev=nev, cpu_seconds=float(sum(r['cpu'] for r in rows)))
    for lam in (1.0, 2.0):
        R = [r for r in rows if r['lam'] == lam]
        ent = {}
        for N in (1024, 4096):
            for k in KS:
                rat = np.array([r[f'conf{N}_k{k:g}'] / r[f'causal_k{k:g}'] for r in R])
                rat = rat[np.isfinite(rat)]
                ent[f'conf{N}_over_causal_k{k:g}'] = dict(median=float(np.median(rat)), min=float(rat.min()),
                                                         max=float(rat.max()), n=int(len(rat)))
            for k in KS[1:]:
                for s in ('causal', f'conf{N}'):
                    rr = np.array([r[f'{s}_k{k:g}'] * k / r[f'{s}_k1'] for r in R]); rr = rr[np.isfinite(rr)]
                    ent[f'R_ev_{s}_k{k:g}'] = dict(zip(('median', 'err'), boot(np.median, rr)[:2]))
        res[f'L{lam:g}'] = ent
        print(f"Lambda={lam}: " + ' | '.join(f"{k}: {v['median']:.4f} [{v.get('min', np.nan):.4f},{v.get('max', np.nan):.4f}]" if 'min' in v else f"{k}: {v['median']:.4f}±{v['err']:.4f}" for k, v in ent.items()))
    dump(res, os.path.join(HERE, 'results', 'M4_conformal_thickness.json'))
    print(f"cpu {res['cpu_seconds']:.0f} s")
