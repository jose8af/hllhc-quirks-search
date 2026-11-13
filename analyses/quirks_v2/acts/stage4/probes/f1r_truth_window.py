"""f1r_truth_window.py -- Stage-4 plan FIXER R1 probe (TT env): truth-level (Stage-3 hits, no PU, no smearing) geometry of the
F0 collection window and the per-crossing layer counts.  Extends data/acts_stage4/review_r1/r1_truth_window.py.

Per event (campaign p2, cfg BM, status 1, in_eta25, TEMPLATE half only, as the plan's acceptance studies; toys untouched):
true plane normal n (n_plane), pair axis n3 = (p_qp + p_qm) projected into the plane, n2 = n x n3, u = x - vtx.
  * wmax_IT     : max |u.n2| over TBPX hits; compared with ell_max/2 (the physics bound: each quirk stays within ell_max/2 of
                  the pair centre of mass, which moves along n3; ell_max is the closed-form maximal string length, cm)
  * f_W         : fraction of TBPX hits with |u.n2| < W, W in {50, 75, 100, 150} mm
  * nIT2c_W     : TBPX layers with >= 2 hits (= crossings, single-sensor layers) inside W
  * nOT2c_W     : barrel OT layers (TBPS L1-3, TB2S L1-3) with min(n_in, n_out) >= 2 inside W (crossings = in/out pairs)
  * nOT2h_W     : old definition (>= 2 hits on in+out together) for comparison
  * dw_old      : rms of u.n2 over all barrel hits inside |u.n2| < 50 mm (plan R0 definition)
  * dw_core     : 1.4826 x MAD of u.n2 over TBPX + TBPS hits inside W = 75 mm (robust core width, proposed diagnostic)
Run (theory_track):  pixi run python acts/stage4/probes/f1r_truth_window.py
Output: data/acts_stage4/fix_r1/f1r_truth_window.json
"""
import json
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
CAN = TT / 'data' / 'sim_stage3' / 'canon' / 'p2'
OUT = TT / 'data' / 'acts_stage4' / 'fix_r1'
OUT.mkdir(parents=True, exist_ok=True)
LAMS = [0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.85, 1, 2, 3, 5, 10]
POINTS = [('F_m200', LAMS), ('F_m500', LAMS), ('F_m1000', LAMS), ('F_m1500', LAMS), ('S_m500', LAMS)]
WS = [50.0, 75.0, 100.0, 150.0]
R_IT = 146.5


def lab(x):
    return f'{x:g}'


out = dict(note='template half, status 1, in_eta25; truth hits; see docstring', R_IT_mm=R_IT, W_mm=WS, points={})
for sp, lams in POINTS:
    for lam in lams:
        files = sorted((CAN / sp).glob(f'L{lab(lam)}_BM_c*.npz'))
        if not files:
            continue
        rows = []
        for f in files:
            z = np.load(f, allow_pickle=False)
            names = [str(k) for k in z['surf_names']]
            tbpx = {i: int(n[-1]) for i, n in enumerate(names) if n.startswith('TBPX_L')}
            stk = {}
            for i, n in enumerate(names):
                if n.startswith(('TBPS_L', 'TB2S_L')):
                    stk.setdefault(n[:7], {})['in' if n.endswith('_in') else 'out'] = i
            ps_ids = [i for i, n in enumerate(names) if n.startswith('TBPS_L')]
            barrel = [i for i, n in enumerate(names) if n.startswith(('TBPX', 'TBPS', 'TB2S'))]
            off = z['hit_offsets']
            for e in range(len(off) - 1):
                if int(z['status'][e]) != 1 or not bool(z['in_eta25'][e]) or int(z['tt_split'][e]) != 0:
                    continue
                n = np.array(z['n_plane'][e], float); n /= np.linalg.norm(n)
                P = np.array(z['p_qp'][e], float) + np.array(z['p_qm'][e], float)
                n3 = P - (P @ n) * n; n3 /= np.linalg.norm(n3)
                n2 = np.cross(n, n3)
                sl = slice(off[e], off[e + 1])
                s = z['h_surf'][sl]
                U = np.c_[z['h_x'][sl], z['h_y'][sl], z['h_z'][sl]] - np.array(z['vtx'][e][:3])[None, :]
                w = U @ n2
                it = np.isin(s, list(tbpx))
                row = [abs(float(z['eta'][e])), float(z['ell_max'][e]) * 10.0, float(np.max(np.abs(w[it]))) if it.any() else np.nan]
                for W in WS:
                    inw = np.abs(w) < W
                    f_w = float(np.mean(inw[it])) if it.any() else np.nan
                    nit = sum(1 for k in tbpx if np.sum((s == k) & inw) >= 2)
                    notc = sum(1 for L in stk.values() if min(np.sum((s == L['in']) & inw), np.sum((s == L['out']) & inw)) >= 2)
                    noth = sum(1 for L in stk.values() if np.sum(((s == L['in']) | (s == L['out'])) & inw) >= 2)
                    row += [f_w, nit, notc, noth]
                br = np.isin(s, barrel)
                in50 = np.abs(w) < 50.0
                dw_old = float(np.std(w[br & in50])) if np.sum(br & in50) > 2 else np.nan
                core = (it | np.isin(s, ps_ids)) & (np.abs(w) < 75.0)
                dw_core = float(1.4826 * np.median(np.abs(w[core] - np.median(w[core])))) if core.sum() > 2 else np.nan
                row += [dw_old, dw_core]
                rows.append(row)
        a = np.array(rows, float)

        def summ(m):
            b = a[m]
            if len(b) == 0:
                return None
            lh = b[:, 1] / 2.0
            d = dict(n=int(len(b)), frac_lmax_le_RIT=float(np.mean(b[:, 1] <= R_IT)),
                     median_lmax_mm=float(np.median(b[:, 1])), median_wmax_IT_mm=float(np.nanmedian(b[:, 2])),
                     frac_wmaxIT_le_1p1_half_lmax=float(np.nanmean(b[:, 2] <= 1.1 * lh)),
                     frac_wmaxIT_le_half_lmax_plus5mm=float(np.nanmean(b[:, 2] <= lh + 5.0)),
                     median_dw_old_mm=float(np.nanmedian(b[:, -2])), frac_dw_old_lt10=float(np.nanmean(b[:, -2] < 10.0)),
                     median_dw_core_mm=float(np.nanmedian(b[:, -1])))
            for j, W in enumerate(WS):
                c = 3 + 4 * j
                d[f'W{int(W)}'] = dict(median_f=float(np.nanmedian(b[:, c])), frac_nIT2_ge3=float(np.mean(b[:, c + 1] >= 3)),
                                       frac_nIT2_eq4=float(np.mean(b[:, c + 1] >= 4)),
                                       frac_nOT2cross_ge3=float(np.mean(b[:, c + 2] >= 3)),
                                       frac_nOT2cross_ge5=float(np.mean(b[:, c + 2] >= 5)),
                                       frac_nOT2hits_ge5=float(np.mean(b[:, c + 3] >= 5)),
                                       frac_IT3_OT3_cross=float(np.mean((b[:, c + 1] >= 3) & (b[:, c + 2] >= 3))),
                                       median_nL2cross=float(np.median(b[:, c + 1] + b[:, c + 2])))
            return d
        key = f'{sp}/L{lab(lam)}'
        out['points'][key] = dict(central_eta_lt1=summ(a[:, 0] < 1.0), all_eta25=summ(np.ones(len(a), bool)))
        c = out['points'][key]['central_eta_lt1']
        print(key, c['n'], 'lmax<=RIT', round(c['frac_lmax_le_RIT'], 2), 'wmax<=1.1lmax/2', round(c['frac_wmaxIT_le_1p1_half_lmax'], 2),
              ' IT3:', [round(c[f'W{int(W)}']['frac_nIT2_ge3'], 2) for W in WS],
              ' IT3&OT3:', [round(c[f'W{int(W)}']['frac_IT3_OT3_cross'], 2) for W in WS], 'dw_core', round(c['median_dw_core_mm'], 2), flush=True)
(OUT / 'f1r_truth_window.json').write_text(json.dumps(out, indent=1))
