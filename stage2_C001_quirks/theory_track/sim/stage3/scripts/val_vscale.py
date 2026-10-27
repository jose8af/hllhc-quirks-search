"""val_vscale.py -- Stage-3 validation V-scale (plan §3, §5): classical NG scaling identity (NEAR_MISS P-25).

An event at (sigma, qB, detector D) equals, scaled by lambda, the event at (lambda sigma, lambda qB, D/lambda).  With
lambda = 9: (Lambda = 1 keV, B0/9, detector x 9) must reproduce (3 keV, B0, D) with hits x -> x/9, up to the parts of
the algorithm that are not scaled (the step cap hmax = 0.2 cm and the bootstrap first_length = 1e-7 cm).
Kernel: T3_causal_s3 in legacy mode (barrel recorder; REC_RADII/REC_ZMAX, r_exit, z_exit and t_end all x 9 for the
1 keV run), B only (no material: material is not scale-free), max_boost 1e-2, 5 P1 events at E 500 GeV.
PASS (criterion of plan §5): hits matched by (quirk, layer, order) agree after x/9 to the hmax interpolation error;
operationally: identical hit counts per (quirk, layer) and max |dx| <= 5 um (the in-plane V3 criterion), plus the
thickness ratio Ds(1 keV, 9D)/9 / Ds(3 keV, D) within 1 %.
Output: sim/stage3/results/Vscale.json.  Run (theory_track/): pixi run python sim/stage3/scripts/val_vscale.py
"""
import json

import numpy as np

import s3common as C


def main():
    from T3_causal_s3 import run_causal_s3, REC_RADII, REC_ZMAX
    from s3_physics import plane_fit
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])
    sel = np.where(S['point'] == keys.index('p1/F_m500/L3_B'))[0][:5]
    out = []; ok_all = True
    for i in sel:
        p1, p2 = S['p_qp'][i], S['p_qm'][i]
        a = run_causal_s3(p1, p2, 500.0, 3.0, B0=C.B0, material=False, max_boost=1e-2, seed=1, legacy=True)
        P = p1 + p2; E = np.hypot(500, np.linalg.norm(p1)) + np.hypot(500, np.linalg.norm(p2))
        t_end = 1.3 * 118.0 / max(np.hypot(P[0], P[1]) / E, 0.02) + 50.0
        b = run_causal_s3(p1, p2, 500.0, 1.0, B0=C.B0 / 9, material=False, max_boost=1e-2, seed=1, legacy=True,
                          rec_radii=np.asarray(REC_RADII) * 9, rec_zmax=np.asarray(REC_ZMAX) * 9, r_exit=118.0 * 9,
                          z_exit=290.0 * 9, t_end=9 * t_end)
        ha, hb = a['hits'], b['hits'].copy()
        hb[:, 2:6] /= 9.0          # legacy columns: quirk, layer, t, x, y, z, beta, |p|, crossing count
        ka = {}; kb = {}
        for h, K in ((ha, ka), (hb, kb)):
            for row in h:
                K.setdefault((int(row[0]), int(row[1])), []).append(row[2:6])
        same_keys = {k: len(v) for k, v in ka.items()} == {k: len(v) for k, v in kb.items()}
        dmax = 0.0
        for k in ka:
            if k in kb:
                n = min(len(ka[k]), len(kb[k]))
                d = np.linalg.norm(np.array(ka[k])[:n, 1:4] - np.array(kb[k])[:n, 1:4], axis=1)
                dmax = max(dmax, float(d.max()) * 1e4)
        sa = plane_fit(ha[ha[:, 1] < 10][:, 3:6])[0]; sb = plane_fit(hb[hb[:, 1] < 10][:, 3:6])[0]
        ok = same_keys and dmax <= 5.0 and abs(sb / sa - 1) <= 0.01
        ok_all &= ok
        out.append(dict(row=int(S['row'][i]), n_hits=[len(ha), len(hb)], same_hit_counts=bool(same_keys), max_dx_um=dmax,
                        ds_ratio=float(sb / sa), status=[int(a['status']), int(b['status'])], nsteps=[int(a['nsteps']), int(b['nsteps'])],
                        PASS=bool(ok)))
        print(out[-1], flush=True)
    C.dump('Vscale.json', dict(events=out, PASS=bool(ok_all)))
    print('V-scale', 'PASS' if ok_all else 'FAIL')


if __name__ == '__main__':
    main()
