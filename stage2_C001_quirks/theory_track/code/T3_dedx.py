"""T3_dedx.py -- ionisation deposited per silicon sensor by a quirk pair, incl. the internal motion (Q6).

For each event (LO DY+ISR, pT(QQ) > 200 GeV, |eta| < 1, fermion E; T2 cache) and Lambda, the exact vacuum world lines
(T2 ExactPair) are integrated through a silicon sensor of thickness w at radius R:
    E_dep = sum_quirks  int S_Si(beta_i(t)) |v_i(t)| dt  over the time quirk i is inside R - w/2 < r < R + w/2,
with S = mean Bethe (no density effect; T3_propagator.stopping_power).  Compared with
    MIP   : 3.88 MeV/cm x w / sin(theta_pair)  (mean, Si, PDG minimum ~1.66 MeV cm2/g, UNVERIFIED round number),
    HSCP  : one charge at the pair-CM velocity crossing the same sensor.
Sensors: IT w = 150 um at R = 3.0 / 14.6 cm; OT w = 290 um at R = 52.3 cm (thicknesses UNVERIFIED).
Mean dE/dx is used (the most probable value is ~30% lower for thin Si); ratios are what matter.
Run: pixi run python code/T3_dedx.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import ExactPair, sigma_from_lambda_keV
from T3_propagator import stopping_power, sample_events, MAT

ZA_RHO = MAT[1, 0] * MAT[1, 3]; I_SI = MAT[1, 1]
MIP = 1.664e-3 * 2.329   # GeV/cm, mean at minimum (PDG Si, recalled)


def deposit(ex, R, w, nper=4000):
    bT = np.hypot(ex.beta[0], ex.beta[1])
    # lab-time window when the CM is within R +- (w/2 + lmax)
    t0 = (R - w / 2 - 1.2 * ex.lmax) / bT; t1 = (R + w / 2 + 1.2 * ex.lmax) / bT
    tc0 = max(t0 / ex.gamma - 2 * ex.lmax, 0); tc1 = t1 / ex.gamma + 2 * ex.lmax
    n = int(min(2e6, max(2e4, nper * (tc1 - tc0) / ex.Tcm)))
    tc = np.linspace(tc0, tc1, n)
    x1, x2 = ex.x_cm(tc)
    Ed = 0.0
    for xs in (x1, x2):
        t, X = ex._event_lab(tc, xs)
        r = np.hypot(X[:, 0], X[:, 1])
        inside = (np.abs(r - R) < w / 2)
        dX = np.diff(X, axis=0); dt = np.diff(t)
        v = np.linalg.norm(dX, axis=1) / dt
        mid = inside[:-1] & inside[1:]
        if mid.any():
            S = np.array([stopping_power(b, 1.0, ZA_RHO, I_SI) for b in v[mid]])
            Ed += np.sum(S * np.linalg.norm(dX[mid], axis=1))
    sinth = bT / np.linalg.norm(ex.beta)
    bcm = np.linalg.norm(ex.beta)
    hscp = stopping_power(bcm, 1.0, ZA_RHO, I_SI) * w / sinth
    return Ed, MIP * w / sinth, hscp


if __name__ == '__main__':
    rng = np.random.default_rng(11)
    print('Deposit per sensor in units of a MIP crossing the same sensor at the same angle: median (16-84%)')
    print('| m_Q | Lambda [keV] | sensor | pair E_dep / MIP | single HSCP at beta_cm / MIP | pair / (2 x HSCP) |')
    print('|---|---|---|---|---|---|')
    for m in (500.0, 1000.0):
        ev = sample_events(m, 150, rng=rng, eta_max=1.0)
        for lam in (3.0, 10.0, 30.0, 100.0):
            sig = sigma_from_lambda_keV(lam)
            for (R, w, name) in ((3.0, 0.015, 'IT1 150um'), (52.3, 0.029, 'PS3 290um')):
                rat, hs, rr = [], [], []
                for (p1, p2, info) in ev[:80]:
                    ex = ExactPair(p1, p2, m, m, sig)
                    E, mip, h = deposit(ex, R, w)
                    rat.append(E / mip); hs.append(h / mip); rr.append(E / (2 * h))
                q = lambda a: np.percentile(a, [16, 50, 84])
                a, b, c = q(rat), q(hs), q(rr)
                print(f'| {m:.0f} | {lam:g} | {name} | {a[1]:.1f} ({a[0]:.1f}-{a[2]:.1f}) | {b[1]:.1f} ({b[0]:.1f}-{b[2]:.1f}) | '
                      f'{c[1]:.2f} ({c[0]:.2f}-{c[2]:.2f}) |', flush=True)
