"""val_c5kev.py -- Stage-3 diagnostic of the P1 c excess at 5 keV (E8, 2026-10-13).  Is the large positive residual
r = c2 - c_ev of the high-k_B events at 5 keV a step effect, a round-off (precision-floor) effect, or physics?

Events: P1 E 1000 GeV, Lambda = 5 keV (B0 and B0/2 at max_boost 1e-3 in production): the 12 events with k_B >= 6 and the
largest r, plus 4 events with k_B < 2 (controls).  For each, B and B2 are rerun
  (i)  at max_boost 1e-4 (10x finer; step convergence), same seed rule;
  (ii) at 1e-3 with the initial momenta multiplied by (1 + 1e-14 N(0,1)) (2 replicas; the V3 floor-replica method).
c2 = (2 Ds(B0/2)/Ds(B0) - 1)/ln 2 on the 10 T3 barrel layers, as in production.  Production driver kernel, P1 settings
(|eta| < 1 rows, vertex at the origin, no material).  Reported (not gating): r at 1e-3 (production), at 1e-4, and the
replica spread of c2.  Output: sim/stage3/results/c5kev_diag.json.
Run (theory_track/): pixi run python sim/stage3/scripts/val_c5kev.py
"""
import json
import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import s3common as C


def ds_of(p1, p2, m, lam, B, mb, seed):
    from T3_causal_s3 import run_causal_s3, load_surfaces
    from s3_physics import plane_fit
    r = run_causal_s3(p1, p2, m, lam, B0=B, material=False, max_boost=mb, seed=seed)
    S = load_surfaces(); kinds = np.array(S['kinds'])
    h = r['hits']; L = h[:, 1].astype(int)
    sel = np.isin(L, np.where(kinds == 'T3V')[0])
    return plane_fit(h[sel, 4:7], np.zeros(3))[0] * 1e4, int(r['status'])


def job(a):
    import run_stage3 as R
    tag, row, p1, p2, m, lam, mb, eps = a
    t0 = time.process_time()
    rng = np.random.default_rng(int(row) * 7 + int(1e15 * eps) % 997)
    f1 = 1 + eps * rng.normal(size=3); f2 = 1 + eps * rng.normal(size=3)
    q1 = p1 * f1; q2 = p2 * f2
    out = {}
    for cfg, B in (('B', R.B0), ('B2', R.B0 / 2)):
        out[cfg] = ds_of(q1, q2, m, lam, B, mb, R.event_seed('F', m, row, lam, cfg))
    c2 = (2 * out['B2'][0] / out['B'][0] - 1) / np.log(2)
    return dict(tag=tag, row=int(row), mb=mb, eps=eps, ds_B=out['B'][0], ds_B2=out['B2'][0], c2=float(c2),
                status=[out['B'][1], out['B2'][1]], cpu_s=time.process_time() - t0)


def main():
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])

    def get(cfg):
        sel = S['point'] == keys.index(f'p1/F_m1000/L5_{cfg}')
        o = np.argsort(S['ev_index'][sel], kind='stable')
        return {c: S[c][sel][o] for c in ('row', 'ds_barrel_um', 'status', 'c_ev', 'k_B', 'p_qp', 'p_qm', 'gstar', 'bodd_l0')}
    b = get('B'); h = get('B2')
    ok = (b['status'] == 1) & (h['status'] == 1)
    c2 = (2 * h['ds_barrel_um'] / b['ds_barrel_um'] - 1) / np.log(2)
    r = c2 - b['c_ev']
    hi = np.where(ok & (b['k_B'] >= 6))[0]; hi = hi[np.argsort(-r[hi])][:12]
    lo = np.where(ok & (b['k_B'] < 2))[0][:4]
    tasks = []
    for tag, ids in (('kB>=6 top r', hi), ('kB<2 control', lo)):
        for i in ids:
            tasks.append((tag, b['row'][i], b['p_qp'][i], b['p_qm'][i], 1000.0, 5.0, 1e-4, 0.0))
            for rep in (1e-14, 2e-14):
                tasks.append((tag, b['row'][i], b['p_qp'][i], b['p_qm'][i], 1000.0, 5.0, 1e-3, rep))
    tasks.sort(key=lambda t: t[6])
    tic = time.time()
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        R = list(ex.map(job, tasks))
    ev = []
    for i in list(hi) + list(lo):
        rr = [x for x in R if x['row'] == int(b['row'][i])]
        fine = [x for x in rr if x['mb'] == 1e-4][0]
        reps = [x['c2'] for x in rr if x['mb'] == 1e-3]
        ev.append(dict(row=int(b['row'][i]), k_B=float(b['k_B'][i]), gstar=float(b['gstar'][i]), bodd_l0=float(b['bodd_l0'][i]),
                       c_ev=float(b['c_ev'][i]), c2_prod=float(c2[i]), r_prod=float(r[i]), c2_1e4=fine['c2'],
                       r_1e4=fine['c2'] - float(b['c_ev'][i]), c2_replicas=reps,
                       replica_spread=float(np.std([c2[i]] + reps)), dsB_prod=float(b['ds_barrel_um'][i]), dsB_1e4=fine['ds_B']))
    hi_ev = ev[:len(hi)]
    res = dict(point='E 1000 GeV, 5 keV, P1 (B, B2)', n_tasks=len(R), cpu_h=sum(x['cpu_s'] for x in R) / 3600, wall_s=time.time() - tic,
               summary=dict(median_r_prod_hi=float(np.median([e['r_prod'] for e in hi_ev])),
                            median_r_1e4_hi=float(np.median([e['r_1e4'] for e in hi_ev])),
                            median_abs_c2_change_1e4=float(np.median([abs(e['c2_1e4'] - e['c2_prod']) for e in ev])),
                            median_replica_spread_c2=float(np.median([e['replica_spread'] for e in ev])),
                            median_c_ev_hi=float(np.median([e['c_ev'] for e in hi_ev]))),
               events=ev)
    C.dump('c5kev_diag.json', res)
    print(json.dumps(res['summary'], indent=1), res['cpu_h'])
    for e in ev:
        print(f"  row {e['row']} kB {e['k_B']:.1f} g* {e['gstar']:.3f} c_ev {e['c_ev']:.4f} c2 prod {e['c2_prod']:.4f} 1e-4 {e['c2_1e4']:.4f} reps {np.round(e['c2_replicas'], 4)}")


if __name__ == '__main__':
    main()
