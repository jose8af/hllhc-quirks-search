"""Truth-level prediction of the no-PU high-Lambda losses in the barrel fiducial (|eta_pair| < 1):
 f_merge_any : >= 1 of the 10 IP surfaces (TBPX L1-4, TBPS L1-3 in/out) has its nearest quirk-1/quirk-2 hit pair inside
               one pitch in BOTH coordinates (U-5 b rule: IT 25 x 100 um, PS 100 um x 1.467 mm) -> N_IP2 < 7 without PU
 f_seed_degen: every cross-quirk (a in TBPX L4, b in TBPX L3) pair has sin(angle(PV->a, PV->b)) < 1e-3 (seeds_fast cut)
 also the median truth IT pair separation (the Stage-3 'merging edge' variable)."""
import sys, json
import numpy as np
from acts.stage4.code import s4sig as S
from acts.stage4.analysis import common as C
spin, m = sys.argv[1], int(sys.argv[2]); lams = [float(x) for x in sys.argv[3].split(',')]
PITCH = {'IT': (0.025, 0.100), 'PS': (0.100, 1.467)}
IP = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4'] + [f'TBPS_L{k}_{s}' for k in (1, 2, 3) for s in ('in', 'out')]
IPI = [S.NAME.index(n) for n in IP]
out = {}
for lam in lams:
    P = S.Point(S.point_key(spin, m, lam))
    rows = P.rows(template=False, counting=False, status1=True)
    fm = []; fs = []; sep_med = []; fm_it = []; n = 0
    for r in rows:
        h, ev = P.event(r)
        if abs(ev['eta']) >= 1: continue
        n += 1
        sid = h['h_surf'].astype(int); q = h['h_quirk'].astype(int)
        x, y, z = h['h_x'], h['h_y'], h['h_z']; vt = ev['vtx']
        merged_any = False; merged_it = False; seps = []
        for s_, nm in zip(IPI, IP):
            a = np.where((sid == s_) & (q == 0))[0]; b = np.where((sid == s_) & (q == 1))[0]
            if not len(a) or not len(b): continue
            R = S.RAD[s_]
            ua = R * np.arctan2(y[a], x[a]); ub = R * np.arctan2(y[b], x[b])
            du = np.abs(ua[:, None] - ub[None, :]); dv = np.abs(z[a][:, None] - z[b][None, :])
            pu, pv = PITCH['IT' if nm.startswith('TBPX') else 'PS']
            if np.any((du < pu) & (dv < pv)):
                merged_any = True; merged_it |= nm.startswith('TBPX')
            if nm.startswith('TBPX'):
                seps.append(np.min(np.hypot(du, dv)))
        A = np.where((sid == S.NAME.index('TBPX_L4')))[0]; B = np.where((sid == S.NAME.index('TBPX_L3')))[0]
        degen = True
        for i in A:
            for j in B:
                if q[i] == q[j]: continue
                ua = np.array([x[i], y[i], z[i]]) - vt[:3]; ub = np.array([x[j], y[j], z[j]]) - vt[:3]
                sn = np.linalg.norm(np.cross(ua, ub)) / (np.linalg.norm(ua) * np.linalg.norm(ub))
                if sn >= 1e-3: degen = False
        fm.append(merged_any); fm_it.append(merged_it); fs.append(degen)
        if seps: sep_med.append(np.median(seps))
    out[lam] = dict(n=n, f_merge_any=float(np.mean(fm)), f_merge_IT=float(np.mean(fm_it)), f_seed_degen=float(np.mean(fs)),
                    f_either=float(np.mean(np.array(fm) | np.array(fs))), median_sep_IT_mm=float(np.median(sep_med)),
                    f_sepIT_lt_100um=float(np.mean(np.array(sep_med) < 0.1)))
    print(f'L={lam:g}', {k: round(v, 3) for k, v in out[lam].items()})
json.dump(out, open(C.TT / 'data/acts_stage4/investigation' / f'truth_degeneracy_{spin}{m}.json', 'w'), indent=1)
