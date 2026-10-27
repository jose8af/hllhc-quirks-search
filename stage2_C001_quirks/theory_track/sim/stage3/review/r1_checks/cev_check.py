"""R1: stored c_ev vs c06 pair_params (c = 1/(L + K(g*)), L = ln(lmax/bodd)) on 40 events at 3 points."""
import sys, numpy as np
from pathlib import Path
TT = Path(__file__).resolve().parents[4]; sys.path += [str(TT/'analytic/checks'), str(TT/'code')]
from c06_rotating_yoyo import pair_params, K_of
S = np.load(TT/'data/sim_stage3/summary/events_p1.npz'); keys = list(S['point_keys'])
for k in ('p1/F_m1000/L5_B', 'p1/F_m200/L1_B', 'p1/S_m500/L3_B'):
    sel = np.where(S['point'] == keys.index(k))[0][:40]
    m = float(k.split('_m')[1].split('/')[0]); lam = float(k.split('/L')[1].split('_')[0])
    d = []; dk = []
    for i in sel:
        pp = pair_params(S['p_qp'][i], S['p_qm'][i], m, lam)
        c = 1.0 / (pp['L'] + K_of(pp['gs'])); d.append(c / S['c_ev'][i] - 1); dk.append(pp['gs'] / S['gstar'][i] - 1)
    print(k, 'max|rel| c_ev:', np.max(np.abs(d)), ' max|rel| g*:', np.max(np.abs(dk)))
