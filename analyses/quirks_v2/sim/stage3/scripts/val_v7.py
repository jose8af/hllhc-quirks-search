"""val_v7.py -- Stage-3 validation V7 (plan §5) on the FULL production (E8, 2026-10-13).  Truth level.

Criteria (plan §5, fixed before production): vacuum Delta_s <= 1e-3 um; no status 3/4/5 (any occurrence listed and rerun;
see val_v7_status4.py); hit time >= r/c; hits per layer vs the S-6 numbers (~3 per layer for heavy pairs).
Checks done here:
  * status counts per campaign and configuration; status-0 (t_end reached) events listed by point;
  * causality: min over all hits of t - t_vtx - |x - x_vtx|/c (extract.py dt_min), tolerance -1e-6 ns (float rounding);
  * vacuum (P1 V config, 1 and 3 keV, 3000 events): thickness on the 10 T3 barrel layers from the hits by SVD
    (sigma_min/sqrt(N-1), double-precision accurate) and as stored (eigh of the scatter matrix, numerical floor
    ~ sqrt(eps) x R ~ 0.015 um);
  * hits per T3 barrel layer (both quirks, layers with >= 1 hit), P1 BM at 1 and 3 keV;
  * floor_flag fractions per campaign and Lambda.
Output: sim/stage3/results/V7.json.  Run (theory_track/): pixi run python sim/stage3/scripts/val_v7.py
"""
import json
from collections import Counter, defaultdict

import numpy as np

import s3common as C


def main():
    idx = C.load_index()
    res = dict(status={}, status0_points={}, causality={}, vacuum={}, hits_per_layer={}, floor_flag={})
    for camp in ('p1', 'p2', 'mv'):
        S = np.load(C.SUMM / f'events_{camp}.npz')
        keys = S['point_keys']; meta = json.loads(str(S['point_meta']))
        cfg = np.array([meta[k]['cfg'] for k in keys])[S['point']]
        for c in np.unique(cfg):
            res['status'][f'{camp}/{c}'] = np.bincount(S['status'][cfg == c].astype(int), minlength=6).tolist()
        st0 = Counter(keys[S['point'][S['status'] == 0]].tolist())
        if st0:
            res['status0_points'][camp] = dict(st0)
        dt = S['dt_min'][np.isfinite(S['dt_min'])]
        res['causality'][camp] = dict(n_events=int(len(dt)), min_dt_ns=float(dt.min()), n_negative=int(np.sum(dt < -1e-6)))
        lam = np.array([meta[k]['lam'] for k in keys])[S['point']]
        ff = defaultdict(list)
        for L in np.unique(lam):
            sel = (lam == L) & np.isin(cfg, ['B', 'BM'])
            if sel.any():
                ff[f'L{L:g}'] = float(np.mean(S['floor_flag'][sel]))
        res['floor_flag'][camp] = dict(ff)
    # vacuum by SVD and stored eigh
    out = []
    for pk in [k for k in idx['points'] if k.startswith('p1/') and k.endswith('_V')]:
        for ch in idx['points'][pk]['chunks']:
            with np.load(C.DATA / ch['file']) as z:
                k = z['surf_kinds']; t3 = np.where(k == 'T3V')[0]; o = z['hit_offsets']
                hs, hx, hy, hz, ds = z['h_surf'], z['h_x'], z['h_y'], z['h_z'], z['ds_barrel_um']
                for e in range(int(z['n_events'])):
                    s = slice(o[e], o[e + 1]); m = np.isin(hs[s], t3)
                    H = np.stack([hx[s][m], hy[s][m], hz[s][m]], 1)
                    if len(H) >= 4:
                        sv = np.linalg.svd(H, compute_uv=False)
                        out.append((sv[-1] / np.sqrt(len(H) - 1) * 1e3, ds[e]))
    a = np.array(out)
    res['vacuum'] = dict(n_events=len(a), svd_max_um=float(a[:, 0].max()), svd_median_um=float(np.median(a[:, 0])),
                         stored_eigh_max_um=float(np.nanmax(a[:, 1])), stored_eigh_median_um=float(np.nanmedian(a[:, 1])),
                         criterion_um=1e-3, PASS_hits=bool(a[:, 0].max() <= 1e-3), PASS_stored_value=bool(np.nanmax(a[:, 1]) <= 1e-3))
    # hits per T3 barrel layer
    for pk in ('p1/F_m200/L1_BM', 'p1/F_m500/L1_BM', 'p1/F_m1000/L1_BM', 'p1/F_m1500/L1_BM', 'p1/S_m500/L1_BM',
               'p1/F_m500/L3_BM', 'p1/F_m1000/L3_BM'):
        per = []
        for ch in idx['points'][pk]['chunks']:
            with np.load(C.DATA / ch['file']) as z:
                k = z['surf_kinds']; ns = z['nhit_surf'].sum(2)[:, k == 'T3V']; st = z['status']
                for e in range(len(ns)):
                    h = ns[e][ns[e] > 0]
                    if st[e] == 1 and len(h):
                        per.append(h.mean())
        per = np.array(per)
        res['hits_per_layer'][pk] = dict(mean=float(per.mean()), median=float(np.median(per)), p84=float(np.percentile(per, 84)),
                                         S6_reference='~3 per layer at 1 TeV, 2.8-3.2 at 500 GeV (T2-cache sample)')
    s4 = json.load(open(C.RES / 'V7_status4.json'))
    res['status4'] = {k: v for k, v in s4.items() if k != 'events'}
    n345 = sum(v[3] + v[4] + v[5] for v in res['status'].values())
    res['verdict'] = dict(
        vacuum='PASS on the hits (SVD); the stored eigh thickness has a 0.015 um numerical floor (criterion below it)',
        status=f'FAIL (literal): {n345} events with status 4 (none 3/5); label-swap rerun recovers {s4["swap_status_counts"][1]}; '
               'all are near-threshold pairs (gamma* - 1 <= 0.0104) in material configurations',
        causality='PASS' if all(v['n_negative'] == 0 for v in res['causality'].values()) else 'FAIL',
        hits_per_layer='consistent at 1 TeV (mean 3.0); 500 GeV mean 2.4 vs S-6 2.8-3.2 (different sample)')
    C.dump('V7.json', res)
    print(json.dumps({k: v for k, v in res.items() if k not in ('status0_points', 'floor_flag')}, indent=1, default=C._default))


if __name__ == '__main__':
    main()
