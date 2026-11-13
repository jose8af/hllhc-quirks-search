"""extract.py -- Stage-3 per-event summary tables (E8, 2026-10-13); plan §4.3 "derived observables" (observables.py
role).  One pass over the canonical production (STAGE3_INDEX.json), no re-propagation.

Output: data/sim_stage3/summary/events_<campaign>.npz (campaign p1, p2, mv, xover_mac, xover_pc) with one row per
(event, configuration) and the point keys; read by p1_results.py, p2_results.py, validation_post.py.

Per event, copied from the production files: provenance (row, ev_index, tt_split, in_eta25), pair kinematics (pt, eta,
M, cstar, gstar, x), closed-form truth (ell_max [cm], N_osc_vac, eps_B, eps_perp, bodd_l0, k_B, c_ev, C_ev, floor_flag),
thickness (ds_barrel_um, ds_all_um, ds_itps_um, res_max_um), status, nsteps, swapped, cpu_s, eacc, the tilt weights.

Derived from the hits (definitions; units mm, ns; "tracker" = kinds IT, PS, 2S; T3V virtual layers excluded):
  n_trk[q]        tracker hits of quirk q (stacked OT sensors counted separately); n_IT, n_PS, n_2S, n_BTL, n_ETL
  n_surf_hit      tracker surfaces with >= 1 hit (either quirk); hits_per_surf = n_trk.sum()/n_surf_hit
  max_cross       maximum number of crossings of one tracker surface by one quirk
  n_rev[q]        lab-frame "turn-arounds" seen in the time-ordered tracker hit sequence of quirk q: number of sign
                  changes of the outward flag (cylinder: p.r_xy > 0; disc: p_z z > 0).  0 for both quirks = the pattern
                  is two outgoing arcs (no visible oscillation).  A hit-level oscillation indicator, not N_osc itself.
  dt_min          min over all hits of t - t_vtx - |x - x_vtx|/c [ns] (must be >= 0: V7 causality)
  dt_trk_max      max of the same delay over tracker hits; dt_BTL (max over BTL hits, NaN if none)
  sep_IT_um       pair separation on the IT (TBPX, TFPX, TEPX): for each IT surface hit by both quirks, the symmetric
                  max-min distance between the hits of q0 and q1 (Hausdorff distance, um); median over those surfaces
                  (NaN if no IT surface has hits of both quirks).  Merged pair: sep_IT_um < 100 (IT long pitch) / 25 um.
  sep_IT_max_um   max over the same surfaces
Run (theory_track/): pixi run python sim/stage3/scripts/extract.py
"""
import json
from multiprocessing import Pool

import numpy as np

import s3common as C

COPY = ('row', 'ev_index', 'tt_split', 'in_eta25', 'pt', 'eta', 'M', 'cstar', 'gstar', 'x', 'ell_max', 'N_osc_vac', 'eps_B',
        'eps_perp', 'bodd_l0', 'k_B', 'c_ev', 'C_ev', 'floor_flag', 'ds_barrel_um', 'ds_all_um', 'ds_itps_um',
        'res_max_um', 'status', 'nsteps', 'swapped', 'cpu_s', 'w_lmax_up', 'w_lmax_dn', 'w_qed', 'w_qed_19', 'w_orig', 'seed')
DERIVED = ('n_trk0', 'n_trk1', 'n_IT', 'n_PS', 'n_2S', 'n_BTL', 'n_ETL', 'n_surf_hit', 'hits_per_surf', 'max_cross',
           'n_rev0', 'n_rev1', 'dt_min', 'dt_trk_max', 'dt_BTL', 'sep_IT_um', 'sep_IT_max_um', 'eacc_GeV')


def hausdorff(a, b):
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1))
    return max(d.min(1).max(), d.min(0).max())


def do_file(args):
    path, pkey = args
    with np.load(C.DATA / path, allow_pickle=False) as z:
        n = int(z['n_events'])
        out = {k: z[k] for k in COPY}
        kinds = z['surf_kinds']; st = z['surf_table']
        offs = z['hit_offsets']
        hq = z['h_quirk']; hs = z['h_surf'].astype(int); ht = z['h_t']; hx = z['h_x']; hy = z['h_y']; hz = z['h_z']
        hpx = z['h_px']; hpy = z['h_py']; hpz = z['h_pz']
        vtx = z['vtx']; nsurf = z['nhit_surf'].astype(int); eacc = z['eacc']
        p_qp = z['p_qp']; p_qm = z['p_qm']
    trk = np.isin(kinds, ['IT', 'PS', '2S']); isIT = kinds == 'IT'; isBTL = kinds == 'BTL'
    cyl = st[:, 0] < 0.5
    D = {k: np.full(n, np.nan) for k in DERIVED}
    ns_trk = nsurf[:, trk, :]
    D['n_trk0'] = ns_trk[:, :, 0].sum(1); D['n_trk1'] = ns_trk[:, :, 1].sum(1)
    for nm, kd in (('n_IT', 'IT'), ('n_PS', 'PS'), ('n_2S', '2S'), ('n_BTL', 'BTL'), ('n_ETL', 'ETL')):
        D[nm] = nsurf[:, kinds == kd, :].sum((1, 2))
    D['n_surf_hit'] = (ns_trk.sum(2) > 0).sum(1)
    D['hits_per_surf'] = ns_trk.sum((1, 2)) / np.maximum(D['n_surf_hit'], 1)
    D['max_cross'] = ns_trk.max((1, 2)) if ns_trk.shape[1] else 0
    D['eacc_GeV'] = eacc.sum(1)
    for i in range(n):
        a, b = offs[i], offs[i + 1]
        if b == a:
            continue
        q = hq[a:b]; s = hs[a:b]; t = ht[a:b]
        X = np.stack([hx[a:b], hy[a:b], hz[a:b]], 1)
        Pm = np.stack([hpx[a:b], hpy[a:b], hpz[a:b]], 1)
        v = vtx[i]
        dt = t - v[3] - np.linalg.norm(X - v[:3], axis=1) / C.C_MM_PER_NS
        D['dt_min'][i] = dt.min()
        tk = trk[s]
        if tk.any():
            D['dt_trk_max'][i] = dt[tk].max()
        bt = isBTL[s]
        if bt.any():
            D['dt_BTL'][i] = dt[bt].max()
        # outward flag and turn-arounds per quirk (time ordered tracker hits)
        rel = X - v[:3]
        out_flag = np.where(cyl[s], (Pm[:, 0] * X[:, 0] + Pm[:, 1] * X[:, 1]) > 0, Pm[:, 2] * rel[:, 2] > 0)
        for qq in (0, 1):
            sel = tk & (q == qq)
            if sel.sum() >= 2:
                o = out_flag[sel][np.argsort(t[sel], kind='stable')]
                D[f'n_rev{qq}'][i] = int(np.sum(o[1:] != o[:-1]))
            else:
                D[f'n_rev{qq}'][i] = 0
        # pair separation on IT surfaces
        seps = []
        for sid in np.unique(s[isIT[s]]):
            m0 = (s == sid) & (q == 0); m1 = (s == sid) & (q == 1)
            if m0.any() and m1.any():
                seps.append(hausdorff(X[m0], X[m1]) * 1000.0)
        if seps:
            D['sep_IT_um'][i] = float(np.median(seps)); D['sep_IT_max_um'][i] = float(np.max(seps))
    out.update(D)
    out['p_qp'] = p_qp; out['p_qm'] = p_qm
    out['pkey'] = np.array([pkey] * n)
    return out


def main():
    idx = C.load_index()
    groups = {}
    for key, P in idx['points'].items():
        camp = P['campaign'] if not key.startswith('xover/') else f"xover_{key.split('/')[1]}"
        for ch in P['chunks']:
            groups.setdefault(camp, []).append((ch['file'], key))
    with Pool(7) as pool:
        for camp, tasks in groups.items():
            res = pool.map(do_file, tasks, chunksize=4)
            keys = sorted({k for _, k in tasks})
            kid = {k: i for i, k in enumerate(keys)}
            cols = {}
            for k in res[0]:
                if k == 'pkey':
                    continue
                cols[k] = np.concatenate([r[k] for r in res])
            pk = np.concatenate([r['pkey'] for r in res])
            cols['point'] = np.array([kid[k] for k in pk], np.int32)
            meta = {k: dict(spin=idx['points'][k]['spin'], m=idx['points'][k]['m'], lam=idx['points'][k]['lam_keV'],
                            cfg=idx['points'][k]['cfg'], max_boost=idx['points'][k]['max_boost'],
                            campaign=idx['points'][k]['campaign']) for k in keys}
            np.savez_compressed(C.SUMM / f'events_{camp}.npz', point_keys=np.array(keys), point_meta=np.array(json.dumps(meta)),
                                **cols)
            print(camp, len(tasks), 'files', len(cols['row']), 'events', len(keys), 'points', flush=True)


if __name__ == '__main__':
    main()
