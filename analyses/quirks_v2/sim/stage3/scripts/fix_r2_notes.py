"""fix_r2_notes.py -- Stage-3 fix pass R2 (review C-3, C-6): two bookkeeping numbers from saved outputs; no production.

  C-3: error on the sep_IT log-log slope over 1-30 keV (P2.json sep_IT_handle).  The central slope is P2.json's
       (unchanged); the error propagates the per-Lambda bootstrap errors err_um stored in P2.json by 20 000 Gaussian toys in
       ln(sep_IT), each Lambda independent (the R2 reviewer's event-level bootstrap gives 0.025 / 0.032 / 0.020 for
       F_m1000 / F_m300 / S_m500, review/r2_checks/sepit_check.out).
  C-6: the P1 events whose c06 MG model Ds is 0 or missing (paired ratio measured/model not finite), with the same
       selection as p1_results.py (B config, status 1, finite Ds_B > 0), listed per cell.
Output: results/FIX_R2_notes.json.  Run (theory_track/): pixi run python sim/stage3/scripts/fix_r2_notes.py  (seconds)
"""
import json

import numpy as np

import s3common as C

LAMS = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]


def sep_slopes():
    H = json.load(open(C.RES / 'P2.json'))['sep_IT_handle']
    rng = np.random.default_rng(20261013)
    out = {}
    for k, v in H.items():
        if v['loglog_slope_1to30keV'] is None:
            continue
        sel = [i for i, l in enumerate(v['lam_keV']) if 1.0 <= l <= 30.0 and v['sep_IT_med_um'][i] and v['sep_IT_med_um'][i] > 0]
        x = np.log([v['lam_keV'][i] for i in sel]); y = np.log([v['sep_IT_med_um'][i] for i in sel])
        ey = np.array([v['err_um'][i] / v['sep_IT_med_um'][i] for i in sel])
        toys = y + rng.normal(size=(20000, len(y))) * ey
        A = np.vstack([x, np.ones_like(x)]).T
        sl = np.linalg.lstsq(A, toys.T, rcond=None)[0][0]
        out[k] = dict(slope=v['loglog_slope_1to30keV'], err=float(np.std(sl)), n_lambda=len(sel))
    return out


def c06_zero():
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys']); MG = np.load(C.SUMM / 'p1_model_mg.npz')
    out = []
    for spin, m in POINTS:
        for lam in LAMS:
            k = f'p1/{spin}_m{m}/L{lam:g}_B'
            if k not in keys:
                continue
            sel = S['point'] == keys.index(k)
            ok = (S['status'][sel] == 1) & np.isfinite(S['ds_barrel_um'][sel]) & (S['ds_barrel_um'][sel] > 0)
            rows = S['row'][sel][ok]; ds = S['ds_barrel_um'][sel][ok]; kb = S['k_B'][sel][ok]; ce = S['c_ev'][sel][ok]
            ms = (MG['point'] == f'{spin}_m{m}') & np.isclose(MG['lam'], lam)
            mp = dict(zip(MG['row'][ms].tolist(), MG['ds_model_um'][ms].tolist()))
            for r, d, kk, cc in zip(rows, ds, kb, ce):
                mod = mp.get(int(r), np.nan)
                if not np.isfinite(d / mod) if mod else True:
                    out.append(dict(cell=f'{spin}_m{m}/L{lam:g}', row=int(r), ds_B_um=float(d), model_um=(None if not np.isfinite(mod) else float(mod)),
                                    k_B=float(kk), c_ev=float(cc)))
    return out


def main():
    res = dict(sep_IT_slope_1to30keV=sep_slopes(), c06_model_zero_events=c06_zero())
    res['n_c06_model_zero'] = len(res['c06_model_zero_events'])
    C.dump('FIX_R2_notes.json', res)
    for k, v in res['sep_IT_slope_1to30keV'].items():
        print(f"{k} {v['slope']:.3f} +- {v['err']:.3f} (n={v['n_lambda']})")
    print('c06 model zero/missing:', res['n_c06_model_zero'])
    for e in res['c06_model_zero_events']:
        print('  ', e)


if __name__ == '__main__':
    main()
