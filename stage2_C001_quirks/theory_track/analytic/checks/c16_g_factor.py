"""c16_g_factor.py -- check for paper Appendix D (2026-10-17): the geometric factor g of the factorised thickness law.

Factorised estimate (paper App. D.8):  Delta s_B ~= g * f_N * eta * N_osc(R) * l_max/2,
  f_N = |e_perp . N|, N = unit(n x beta_cm), N_osc(R) = sigma R/(2 beta* p_T), R = outer barrel radius (108.3 cm).
Analytic "twist" estimate: the plane fit absorbs the mean tilt of a helicoid h = kappa u R, leaving
  g = (x_rms/l_max) * (sigma_R/R_out),  x_rms/l_max = sqrt(<x^2>)/l_max over a half period (0.73 NR),
  sigma_R = population standard deviation of the 10 layer radii.
Measured g: rotating-yo-yo model of c06 (exact vacuum yo-yo, axis stepped by eta at odd crossings, boosted, plane fit),
150 events per (m, Lambda) from the T3 sample, |eta_pair| < 1, B = 3.8112 T.
Run: pixi run python analytic/checks/c16_g_factor.py > analytic/checks/c16_g_factor_out.txt
"""
import os, sys
import numpy as np
TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(TT, 'analytic', 'checks')); sys.path.insert(0, os.path.join(TT, 'code'))
from c06_rotating_yoyo import model_hits  # noqa: E402
from T3_propagator import sample_events, plane_fit, REC_RADII  # noqa: E402

R = np.array(REC_RADII[:10])
print('layer radii [cm]:', R)
print(f'sigma_R/R_out = {R.std() / R[-1]:.4f}  (ddof=1: {R.std(ddof=1) / R[-1]:.4f})')
for g in (1.0001, 1.1, 1.23, 1.5, 2.0):
    rho = np.sqrt(g * g - 1); u = np.linspace(-rho, rho, 200001)
    xr = np.sqrt(np.mean(((g - np.sqrt(1 + u * u)) / (g - 1)) ** 2))
    print(f'gamma*={g}: x_rms/l_max = {xr:.4f};  g_twist = {xr * R.std() / R[-1]:.4f}')
for m in (200.0, 500.0, 1000.0):
    for lam in (1.0, 3.0):
        ev = sample_events(m, 150, rng=np.random.default_rng(2026), eta_max=1.0)
        gs = []
        for p1, p2, info in ev:
            Hm, pp = model_hits(p1, p2, m, lam)
            if len(Hm) < 4:
                continue
            ds = plane_fit(Hm[:, 2:5])[0]
            bh = pp['beta'] / np.linalg.norm(pp['beta']); N = np.cross(pp['n'], bh); N /= np.linalg.norm(N)
            fN = abs(pp['eperp'] @ N)
            pT = np.hypot(*(p1 + p2)[:2]); bs = pp['ps'] / pp['E1s']
            Nosc = pp['sig'] * R[-1] / (2 * bs * pT)
            gs.append(ds / (fN * pp['eta'] * Nosc * pp['lmax'] / 2))
        gs = np.array(gs)
        print(f'm={m:.0f} GeV, Lambda={lam} keV: n={len(gs)}, g median {np.median(gs):.3f}, '
              f'16-84% {np.percentile(gs, 16):.3f}-{np.percentile(gs, 84):.3f}', flush=True)
