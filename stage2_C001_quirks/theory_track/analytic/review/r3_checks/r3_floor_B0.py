"""S1-R3: how much of E2's direct-B0 Delta_c(2) at 5-13 keV (FIX2 N2) is the double-precision floor?
Floor model from r3_floor_test: relative excess of Delta_s at field eps_perp, delta = A u/eps^2 (capped at 0.18), with
A = 0.76 (M2b, CM frame, gamma* = 1.3, max_boost 1e-3) and A = 2.9 (= 3.8 x 0.76, fitted to E2's pure-E*perp lab runs at 3 keV).
Predicted Delta_c(2) = R(1/2) [delta(eps/2) - delta(eps)]/ln 2 per event, compared with the measured per-event Delta_c(2).
Run from TT: pixi run python analytic/review/r3_checks/r3_floor_B0.py"""
import os, sys, numpy as np
from scipy.stats import spearmanr
TT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(TT, 'analytic', 'numerics')); sys.path.insert(0, os.path.join(TT, 'code'))
import FIX2_analysis as X
u = np.finfo(float).eps
delta = lambda e, A: np.minimum(A * u / e ** 2, 0.18)
for m, lams in ((500.0, (5.0, 7.0, 10.0, 13.0)), (1000.0, (5.0, 7.0, 10.0))):
    for lam in lams:
        S = X.load_kind('b0', m, lam); ids = sorted(S); K = X.evkin(m, lam, ids)
        cE = np.array([K[i]['c_E1'] for i in ids]); eps = np.array([K[i]['eps'] for i in ids])
        kB = np.array([K[i]['kB_perp'] for i in ids])
        d = np.array([X.cvec(S[i])[0] for i in ids]) - cE
        line = f"m={m:g} L={lam:g} n={len(ids)} eps(B0/2) median {np.median(eps/2):.1e}: meas Delta_c(2) median {np.median(d):+.4f} (k_B<5: {np.median(d[kB<5]):+.4f})"
        for A in (0.76, 2.9):
            p = (1 + cE * np.log(2)) * (delta(eps / 2, A) - delta(eps, A)) / np.log(2)
            line += f" | A={A}: floor pred median {np.median(p):+.4f} (k_B<5 {np.median(p[kB<5]):+.4f}), meas-pred {np.median(d-p):+.4f}, rho {spearmanr(p, d).correlation:+.2f}"
        print(line)
