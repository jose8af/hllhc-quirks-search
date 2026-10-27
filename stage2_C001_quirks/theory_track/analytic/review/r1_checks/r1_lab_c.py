"""r1_lab_c.py -- S1-R1: end-to-end spot check of E1's per-event c_ev = 1/[ln(l_max/b_odd) + K(gamma*)] against the
lab-frame B response of the INDEPENDENT conformal solver code/R1_conformal_ng.py (unmodified, imported), m = 500 GeV,
Lambda = 1 keV, B0 = 3.8112 T and B0/4, events from R1.make_event (gamma* = 1.28, pT = 300 GeV; |y| < 0.8).
E1's formula is implemented here from the note (own code): eps_perp = q|E*_perp|/sigma with E* = gamma_cm beta_cm x B in the
pure-boost pair rest frame, perp to n = CM direction of quirk 1; b_odd = 2 eps_perp l0 [g - asinh(rho)/rho];
K(g) = (3 ln2 - 2) - 0.506 ln g - 0.077 ln^2 g.  Measured c_4 = (R(1/4) - 1)/ln 4, R = 4 Ds(B0/4)/Ds(B0).
Run: pixi run python analytic/review/r1_checks/r1_lab_c.py > analytic/review/r1_checks/r1_lab_c_out.txt
"""
import os, sys, time
import numpy as np

TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(TT, 'code'))
import R1_conformal_ng as R1  # noqa: E402

M, LAM, B0 = 500.0, 1.0, 3.8112
QB = 2.99792458e-3       # GeV/cm per T, unit charge


def c_E1(p1, p2, m=M, lam=LAM, B=B0):
    sig = R1.sigma_keV(lam)
    E1 = np.hypot(m, np.linalg.norm(p1)); E2 = np.hypot(m, np.linalg.norm(p2))
    P = p1 + p2; E = E1 + E2
    beta = P / E; b2 = beta @ beta; g = 1 / np.sqrt(1 - b2); bh = beta / np.sqrt(b2)
    p1s = p1 + ((g - 1) * (p1 @ bh) - g * E1 * np.sqrt(b2)) * bh       # pure boost to the pair rest frame
    n = p1s / np.linalg.norm(p1s)
    gs = np.hypot(m, np.linalg.norm(p1s)) / m
    rho = np.sqrt(gs * gs - 1)
    Es = QB * B * g * np.cross(beta, [0, 0, 1.0])                     # q E* [GeV/cm]
    Eperp = Es - (Es @ n) * n
    eps = np.linalg.norm(Eperp) / sig
    l0 = m / sig; lmax = 2 * (gs - 1) * l0
    bodd = 2 * eps * l0 * (gs - np.arcsinh(rho) / rho)
    K = (3 * np.log(2) - 2) - 0.506 * np.log(gs) - 0.077 * np.log(gs) ** 2
    return 1 / (np.log(lmax / bodd) + K), gs, eps


def ds(p1, p2, B, N):
    H, canon, nst = R1.run(p1, p2, M, LAM, Bz=B, N=N)
    H = H[H[:, 1] < 10]
    return R1.plane_thickness(H[:, 3:6])[0] if len(H) >= 4 else np.nan, len(H)


if __name__ == '__main__':
    rng = np.random.default_rng(2026)
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print(f'# R1 conformal solver (unmodified), m={M}, Lambda={LAM} keV, B0={B0} T; E1 c_ev from own implementation')
    print('# ev  gamma*  eps_perp   c_E1     | N    Ds(B0)[um]  Ds(B0/4)[um]  nhits  R(1/4)   c_4 meas  meas-E1')
    rows = []
    for ie in range(nev):
        p1, p2 = R1.make_event(rng, M)
        cE, gs, eps = c_E1(p1, p2)
        for N in (1024, 4096):
            tic = time.time()
            d0, n0 = ds(p1, p2, B0, N); d4, n4 = ds(p1, p2, B0 / 4, N)
            R = 4 * d4 / d0; c4 = (R - 1) / np.log(4)
            print(f'{ie:3d}  {gs:.3f}  {eps:.3e}  {cE:.4f}   | {N:4d}  {d0 * 1e4:9.3f}  {d4 * 1e4:9.3f}   {n0:3d}/{n4:3d}  {R:.4f}   {c4:.4f}'
                  f'   {c4 - cE:+.4f}   ({time.time() - tic:.0f}s)', flush=True)
            if N == 4096:
                rows.append((cE, c4))
    a = np.array(rows)
    d = a[:, 1] - a[:, 0]
    print(f'# N=4096: median c_E1 = {np.median(a[:, 0]):.4f}, median c_4 = {np.median(a[:, 1]):.4f}, '
          f'median(meas - E1) = {np.median(d):+.4f}, mean = {d.mean():+.4f} +- {d.std(ddof=1) / np.sqrt(len(d)):.4f} (n={len(d)})')


def geometry(p1, p2, m=M, B=B0):
    """sin(alpha) = |E*perp|/|E*| and kB = |B*perp n| / |E*perp| (q|B*perp|/sigma in units of eps_perp)."""
    E1 = np.hypot(m, np.linalg.norm(p1)); E2 = np.hypot(m, np.linalg.norm(p2))
    P = p1 + p2; E = E1 + E2
    beta = P / E; b2 = beta @ beta; g = 1 / np.sqrt(1 - b2); bh = beta / np.sqrt(b2)
    p1s = p1 + ((g - 1) * (p1 @ bh) - g * E1 * np.sqrt(b2)) * bh
    n = p1s / np.linalg.norm(p1s)
    Bv = np.array([0, 0, B]); Es = g * np.cross(beta, Bv); Bs = g * Bv - (g - 1) * (Bv @ bh) * bh
    Ep = Es - (Es @ n) * n; Bp = Bs - (Bs @ n) * n
    return np.linalg.norm(Ep) / np.linalg.norm(Es), np.linalg.norm(Bp) / np.linalg.norm(Ep), g * np.sqrt(b2)


if __name__ == '__main__' and os.environ.get('R1_GEOM'):
    rng = np.random.default_rng(2026)
    print('# geometry of the same events: ev, sin(alpha), kB = |B*perp|/|E*perp|, gamma_cm beta_cm')
    for ie in range(int(sys.argv[1]) if len(sys.argv) > 1 else 16):
        p1, p2 = R1.make_event(rng, M)
        sa, kB, gb = geometry(p1, p2)
        print(f'{ie:3d}  sin(alpha) = {sa:.3f}  kB = {kB:6.2f}  gamma_cm beta_cm = {gb:.3f}')
