"""T3_kick.py -- response of a quirk pair to a single transverse kick on one quirk (how the string shares an MS kick).

Causal NG propagator (T3_causal, kick hook), B = 0, no material.  One LO DY+ISR event (m_Q = 500 GeV, pT>200, |eta|<1);
quirk 0 receives dp = 10 MeV along the plane normal when it first crosses r = 3 cm (IT1; a typical MS kick there is
13.6 MeV sqrt(0.012)/beta ~ 5-10 MeV).  Output: out-of-plane displacement of the later hits of BOTH quirks vs r,
compared with
   CM model   : the total momentum turns by dp/|P_QQ|, so the guiding centre leaves the plane by (dp/|P|) x path;
   free quirk : a lone particle of momentum p_0 would leave it by (dp/p_0) x path.
Run: pixi run python code/T3_kick.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import sample_events, plane_fit, REC_RADII
from T3_causal import run_causal

if __name__ == '__main__':
    m = 500.0
    rng = np.random.default_rng(4)
    ev = sample_events(m, 6, rng=rng, eta_max=1.0)
    print('| event | Lambda | R [cm] | out-of-plane (both quirks) [um] | CM model [um] | free-quirk model [um] |')
    print('|---|---|---|---|---|---|')
    for ie, (p1, p2, info) in enumerate(ev[:3]):
        P = p1 + p2
        for lam in (0.3, 1.0, 3.0, 10.0):
            ref = run_causal(p1, p2, m, lam, B0=0.0, material=False)
            H0 = ref['hits'][ref['hits'][:, 1] < 10]
            _, nrm = plane_fit(H0[:, 3:6])
            dp = 0.010 * nrm
            r = run_causal(p1, p2, m, lam, B0=0.0, material=False, kick=(0, 3.0, dp))
            H = r['hits'][r['hits'][:, 1] < 10]
            for L in (4, 6, 9):
                sel = H[:, 1] == L
                if not sel.any():
                    continue
                off = H[sel, 3:6] @ nrm
                R = REC_RADII[L]
                path = (R - 3.0) * np.linalg.norm(P) / np.hypot(P[0], P[1])
                cm = 0.010 / np.linalg.norm(P) * path
                free = 0.010 / np.linalg.norm(p1) * path
                print(f'| {ie} | {lam} | {R} | {", ".join(f"{o*1e4:.1f}" for o in off)} | {cm*1e4:.1f} | {free*1e4:.1f} |')
