"""val_vscale_s3.py -- Stage-3 fix pass R1 (constructive C-6): V-scale redone with the PRODUCTION (s3, all-roots) recorder.

Same identity and events as val_vscale.py (NEAR_MISS P-25; 5 P1 E 500 GeV events, B only, max_boost 1e-2 as in V-scale and
1e-3, the production setting for Lambda <= 5 keV): (3 keV, B0, D)
vs (1 keV, B0/9, 9 D) with hits x 1/9.  Here the kernel runs in production mode (legacy=False): the surfaces of
surfaces_s3.json (93 surfaces, every root of a chord recorded), vertex at the origin, z_exit 293 cm.  For the 1 keV run
every surface length, r_exit, z_exit and t_end are x 9 (a scaled copy of the surface table is installed as the kernel's
surface cache for that run only; material is off, so the slab tables do not matter).  hmax and first_length are not scaled.
Criterion (as V-scale): identical hit counts per (quirk, surface), max |dx| <= 5 um after x/9 for hits matched by
(quirk, surface, order), and Ds(T3V, 1 keV, 9D)/9 within 1 % of Ds(T3V, 3 keV, D).
Output: sim/stage3/results/Vscale_s3.json.  Run (theory_track/): pixi run python sim/stage3/scripts/val_vscale_s3.py
"""
import time

import numpy as np

import s3common as C


def main():
    import T3_causal_s3 as K
    from s3_physics import plane_fit
    S0 = K.load_surfaces()
    S9 = dict(S0); sf = S0['surf'].copy(); sf[:, 1:] *= 9.0; S9['surf'] = sf
    ic = np.where(sf[:, 0] < 0.5)[0]; idd = np.where(sf[:, 0] >= 0.5)[0]
    oc = np.argsort(sf[ic, 1], kind='stable'); od = np.argsort(sf[idd, 1], kind='stable')
    S9.update(cR=sf[ic, 1][oc].copy(), cI=ic[oc].astype(np.int64), dZ=sf[idd, 1][od].copy(), dI=idd[od].astype(np.int64))
    if len(S0['dslabs']):
        ds = S0['dslabs'].copy(); ds[:, :3] *= 9.0; S9['dslabs'] = ds
    t3v = np.where(np.array(S0['kinds']) == 'T3V')[0]
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])
    sel = np.where(S['point'] == keys.index('p1/F_m500/L3_B'))[0][:5]
    res = {}; t0 = time.process_time()
    for mb in (1e-2, 1e-3):
        out = []; ok_all = True
        for i in sel:
            p1, p2 = S['p_qp'][i], S['p_qm'][i]
            K._SURF = S0
            a = K.run_causal_s3(p1, p2, 500.0, 3.0, B0=C.B0, material=False, max_boost=mb, seed=1)
            P = p1 + p2; E = np.hypot(500, np.linalg.norm(p1)) + np.hypot(500, np.linalg.norm(p2))
            t_end = 1.3 * 118.0 / max(np.hypot(P[0], P[1]) / E, 0.02) + 50.0
            K._SURF = S9
            b = K.run_causal_s3(p1, p2, 500.0, 1.0, B0=C.B0 / 9, material=False, max_boost=mb, seed=1,
                                r_exit=118.0 * 9, z_exit=293.0 * 9, t_end=9 * t_end)
            K._SURF = S0
            ha, hb = a['hits'], b['hits'].copy()
            hb[:, 3:7] /= 9.0        # columns: quirk, surf, icross, t, x, y, z, px, py, pz, E, dl
            ka, kb = {}, {}
            for h, Kd in ((ha, ka), (hb, kb)):
                for row in h:
                    Kd.setdefault((int(row[0]), int(row[1])), []).append(row[3:7])
            same = {k: len(v) for k, v in ka.items()} == {k: len(v) for k, v in kb.items()}
            dmax = 0.0
            for k in ka:
                if k in kb:
                    n = min(len(ka[k]), len(kb[k]))
                    d = np.linalg.norm(np.array(ka[k])[:n, 1:4] - np.array(kb[k])[:n, 1:4], axis=1)
                    dmax = max(dmax, float(d.max()) * 1e4)
            sa = plane_fit(ha[np.isin(ha[:, 1], t3v)][:, 4:7], np.zeros(3))[0]
            sb = plane_fit(hb[np.isin(hb[:, 1], t3v)][:, 4:7], np.zeros(3))[0]
            ok = same and dmax <= 5.0 and abs(sb / sa - 1) <= 0.01
            ok_all &= ok
            out.append(dict(row=int(S['row'][i]), n_hits=[len(ha), len(hb)], same_hit_counts=bool(same), max_dx_um=dmax,
                            ds_ratio=float(sb / sa), status=[int(a['status']), int(b['status'])], PASS=bool(ok)))
            print(out[-1], flush=True)
        res[f'max_boost_{mb:g}'] = dict(events=out, PASS=bool(ok_all))
    C.dump('Vscale_s3.json', dict(recorder='production s3 (all roots, surfaces_s3.json)', **res,
                                  cpu_h=(time.process_time() - t0) / 3600))
    print({k: v['PASS'] for k, v in res.items()})


if __name__ == '__main__':
    main()
