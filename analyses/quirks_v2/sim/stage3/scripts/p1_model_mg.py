"""p1_model_mg.py -- the analytic predictions RE-DERIVED on the MadGraph P1 events (E8, 2026-10-13).

For every P1 event (same rows as the production P1 B runs: |eta_pair| < 1, vertex at the origin, 300 events at
Lambda <= 5 keV, 200 at 7-10 keV) and Lambda in {0.45, 0.6, 1, 2, 3, 5, 7, 10} keV, evaluate the E1 rotating-yo-yo model
(analytic/checks/c06_rotating_yoyo.model_hits, imported read-only; npts as in c07: 4000 for Lambda <= 3 keV, else 600) at
B = 3.8112 T, and the plane thickness on the 10 T3 barrel radii (c06.plane_fit), i.e. exactly the c07 procedure that
produced predictions.json's model medians, but on the MG events instead of the T3-cache sample.
Output: data/sim_stage3/summary/p1_model_mg.npz (point key, Lambda, row, ds_model_um).  No re-propagation (model only).
Run (theory_track/): pixi run python sim/stage3/scripts/p1_model_mg.py
"""
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import s3common as C

LAMS = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]


def job(a):
    sys.path.append(str(C.TT / 'analytic' / 'checks')); sys.path.append(str(C.TT / 'code'))
    from c06_rotating_yoyo import model_hits, plane_fit
    spin, m, lam, rows, P1, P2 = a
    out = []
    for r, p1, p2 in zip(rows, P1, P2):
        H, pp = model_hits(p1, p2, m, lam, npts=(4000 if lam <= 3 else 600))
        out.append(plane_fit(H[:, 2:5])[0] * 1e4 if len(H) >= 4 else np.nan)
    return spin, m, lam, rows, out


def main():
    S = np.load(C.SUMM / 'events_p1.npz')
    keys = S['point_keys']
    tasks = []
    for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)):
        for lam in LAMS:
            # events of the P1 point at this Lambda (any configuration carries the same rows; use M, run at every Lambda)
            k = list(keys).index(f'p1/{spin}_m{m}/L{lam:g}_M')
            sel = S['point'] == k
            rows = S['row'][sel]; P1 = S['p_qp'][sel]; P2 = S['p_qm'][sel]
            for c in range(0, len(rows), 25):
                tasks.append((spin, float(m), lam, rows[c:c + 25], P1[c:c + 25], P2[c:c + 25]))
    tasks.sort(key=lambda t: -t[2])
    tic = time.time()
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        R = list(ex.map(job, tasks))
    pk, lam_, row_, ds_ = [], [], [], []
    for spin, m, lam, rows, out in R:
        pk += [f'{spin}_m{int(m)}'] * len(rows); lam_ += [lam] * len(rows); row_ += list(rows); ds_ += out
    np.savez_compressed(C.SUMM / 'p1_model_mg.npz', point=np.array(pk), lam=np.array(lam_), row=np.array(row_),
                        ds_model_um=np.array(ds_), note=np.array(__doc__))
    print(f'{len(ds_)} model events in {time.time() - tic:.0f} s')


if __name__ == '__main__':
    main()
