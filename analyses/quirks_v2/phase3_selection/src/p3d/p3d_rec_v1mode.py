"""p3d_rec_v1mode.py -- the refined toy recipe (PREREG draft steps 3-6) on the v1-mode workspace.  Gorm, 2026-11-24.
Uses the Phase-2 validated v1-mode fitter of p2f_t1.py (imported, not edited): pyhf fits on the jax backend at SLSQP
tolerance 1e-10 with closed-form starts, every toy's q~ checked against the exact one-dimensional profile (FLO §2,
§4).  Same seeds and pseudo-data as T1-b (p2f_t1.ensembles), so the grid points of replica i reproduce Flora's.
  <out> <seed> [ntoys=1000] [budget_s=1500]
"""
import json
import logging
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'phase2_exploration', 'src'))

import numpy as np  # noqa: E402

import p2f_t1 as f  # noqa: E402
import p3d_toys as pt  # noqa: E402

log = logging.getLogger('p3d_rec_v1mode')
MU_A = 828.7069115492852            # T1-b asymptotic root (FLO l.18; p2-c-t1f-diag-ref command)


def main(out, seed, ntoys=1000, budget=1500.0):
    t0 = time.time()
    f.CONF['tol'] = 1e-10
    f.set_backend('jax')
    inp = f.v1_inputs('limits'); truth = f.V1Truth(inp)
    ws, model = f.v1_model(inp)
    fit = f.Fitter(model, truth)
    pts = []

    def ev(mu):
        r = f.ensembles(fit, truth, mu, ntoys, seed)
        rec = dict(mu=float(mu), qb=r['b']['q'], qsb=r['sb']['q'], b=dict(dropped=r['b']['dropped']),
                   sb=dict(dropped=r['sb']['dropped']), max_abs_dq=[r['b']['max_abs_dq'], r['sb']['max_abs_dq']],
                   ntoys=ntoys, cpu_s_per_unit=r['loop_cpu_s_per_1000_plus_1000'])
        pts.append(rec)
    for g in pt.GRID:
        ev(MU_A * g)
    status = {}
    while time.time() - t0 < budget and len(pts) < 40:
        nxt = None
        for rule in ('ecdf', 'npmedian'):
            s = pt.limit_status([(r['mu'], pt.counts_of(r, 0.5, rule)) for r in pts]); status[rule] = s
            if s['status'] != 'ok' and s.get('next') and nxt is None:
                nxt = s['next']
        if nxt is None:
            break
        ev(nxt)
    res = dict(mode='rec_v1mode', seed=seed, ntoys=ntoys, mu_a=MU_A, points=pts, status={})
    for rule in ('ecdf', 'npmedian'):
        cs = [(r['mu'], pt.counts_of(r, 0.5, rule)) for r in pts]
        s = pt.limit_status(cs)
        s['frozen_grid_value'] = pt.limit_frozen(cs[:len(pt.GRID)])
        s['variants'] = {e: pt.limit_status(cs, empty=e).get('mu95') for e in ('k1139', 'k05')}
        res['status'][f'0.5|{rule}'] = s
    res['complete'] = all(s['status'] == 'ok' for s in res['status'].values())
    pt.dump(out, res)
    log.info('rec seed %d: %s', seed, {k: (v['status'], v.get('mu95'), v.get('frozen_grid_value'))
                                       for k, v in res['status'].items()})


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[0], int(a[1]), int(a[2]) if len(a) > 2 else 1000, float(a[3]) if len(a) > 3 else 1500.0)
