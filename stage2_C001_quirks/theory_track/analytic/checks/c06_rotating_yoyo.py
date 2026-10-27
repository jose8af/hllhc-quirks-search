"""c06_rotating_yoyo.py -- E1: small targeted test of the accumulation step (NEAR_MISS_IMPULSE.md §5).

"Rotating yo-yo" model: the exact vacuum yo-yo in the pair rest frame, whose axis n_hat is rotated rigidly by
eta (§4-5 formula) toward E*_perp at every odd crossing (the crossings are where the string has zero length, so the
rotation is an exact zero mode there); boosted to the lab; hits at the 10 Phase-2 barrel radii; plane fit through
the origin -> Delta s_model.  Non-secular first-order offsets (b_odd, static polarisation) are NOT included.
Compared, event by event, with the exact causal NG string (T3_causal.run_causal, B = 3.8112 T, no material;
imported, not modified) on the same events (T3_propagator.sample_events, the T3 thickness sample).
Also prints, per event: gamma*, eps_perp, ln(l_max/b_odd), c_event = 1/(ln + K), number of odd crossings in the
tracker.
Usage: pixi run python analytic/checks/c06_rotating_yoyo.py [m] [lam1,lam2,...] [nev] [seed]
"""
import os, sys
import numpy as np
TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(TT, 'code'))
from T3_causal import run_causal  # noqa: E402
from T3_propagator import sample_events, plane_fit, REC_RADII, REC_ZMAX  # noqa: E402
from T2_propagator import sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T  # noqa: E402

B_CMS = 3.8112
# K(gamma*) of the exact NG string from c03 (max_boost 1e-4 where available; see c03 outputs)
K_TAB_G = np.array([1.0, 1.05, 1.28, 1.6, 2.0, 3.0])
K_TAB_K = np.array([3 * np.log(2) - 2, 0.056, -0.05, -0.18, -0.31, -0.58])


def K_of(g):
    return np.interp(g, K_TAB_G, K_TAB_K)


def G_of(g):
    rho = np.sqrt(g * g - 1); be = rho / g
    return 2 * (g - np.arcsinh(rho) / rho) / (rho * np.arctanh(be))


def boost(beta, t, x):
    """Lorentz boost of events (t, x[...,3]) from the frame moving with velocity beta (rest frame) to the lab."""
    b2 = beta @ beta; g = 1 / np.sqrt(1 - b2); bh = beta / np.sqrt(b2)
    xb = x @ bh
    tl = g * (t + x @ beta)
    xl = x + np.outer((g - 1) * xb + g * t * np.sqrt(b2), bh)
    return tl, xl


def pair_params(p1, p2, m, lam, B=B_CMS, q1=1.0):
    sig = sigma_from_lambda_keV(lam)
    E1 = np.hypot(m, np.linalg.norm(p1)); E2 = np.hypot(m, np.linalg.norm(p2))
    P = p1 + p2; E = E1 + E2; beta = P / E; b2 = beta @ beta; g = 1 / np.sqrt(1 - b2); bh = beta / np.sqrt(b2)
    # boost p1 to the rest frame
    p1s = p1 + ((g - 1) * (p1 @ bh) - g * np.sqrt(b2) * E1) * bh
    ps = np.linalg.norm(p1s); n = p1s / ps
    gs = np.hypot(m, ps) / m
    Bv = np.array([0, 0, B])
    qEs = q1 * EB_GEV_PER_CM_PER_T * g * np.cross(beta, Bv)        # force on quirk 1 in the rest frame (GeV/cm)
    Ep = qEs - (qEs @ n) * n
    eps_perp = np.linalg.norm(Ep) / sig
    eperp = Ep / np.linalg.norm(Ep)
    l0 = m / sig
    rho = np.sqrt(gs * gs - 1)
    bodd = 2 * eps_perp * l0 * (gs - np.arcsinh(rho) / rho)
    lmax = 2 * (gs - 1) * l0
    L = np.log(lmax / bodd)
    eta = eps_perp * G_of(gs) * (L + K_of(gs))
    return dict(sig=sig, beta=beta, g=g, n=n, ps=ps, gs=gs, eps_perp=eps_perp, eperp=eperp, l0=l0, bodd=bodd,
                lmax=lmax, L=L, eta=eta, E1s=np.hypot(m, ps))


def model_hits(p1, p2, m, lam, eta_scale=1.0, radii=REC_RADII[:10], zmax=REC_ZMAX[:10], rmax=120.0, npts=4000, q=1.0):
    pp = pair_params(p1, p2, m, lam, q1=q)
    sig, ps, E1s = pp['sig'], pp['ps'], pp['E1s']
    Th = 2 * ps / sig
    bT = np.hypot(pp['beta'][0], pp['beta'][1])
    tmax = 1.3 * rmax / bT / pp['g'] + Th
    nh = int(np.ceil(tmax / Th))
    ts = np.linspace(0, nh * Th, nh * npts + 1)
    h = np.floor(ts / Th).astype(int)
    u = ts - h * Th
    S = (E1s - np.sqrt(m * m + (ps - sig * u) ** 2)) / sig
    s1 = np.where(h % 2 == 0, S, -S)
    nodd = (h + 1) // 2                       # odd crossings at t* = Th, 3Th, ... -> count before t*
    Th_ = eta_scale * pp['eta'] * nodd
    nvec = np.outer(np.cos(Th_), pp['n']) + np.outer(np.sin(Th_), pp['eperp'])
    hits = []
    for k, sgn in ((0, 1.0), (1, -1.0)):
        x = sgn * s1[:, None] * nvec
        tl, xl = boost(pp['beta'], ts, x)
        r = np.hypot(xl[:, 0], xl[:, 1])
        for L, R in enumerate(radii):
            idx = np.where((r[:-1] - R) * (r[1:] - R) < 0)[0]
            for i in idx:
                f = (R - r[i]) / (r[i + 1] - r[i])
                X = xl[i] + f * (xl[i + 1] - xl[i])
                if abs(X[2]) < zmax[L]:
                    hits.append((k, L, *X))
    return np.array(hits), pp


def causal_hits(p1, p2, m, lam):
    r = run_causal(p1, p2, m, lam, B0=B_CMS, material=False)
    H = r['hits']
    return H[H[:, 1] < 10]


if __name__ == '__main__':
    m = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
    lams = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.0, 3.0]
    nev = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 2026
    rng = np.random.default_rng(seed)
    ev = sample_events(m, nev, rng=rng, eta_max=1.0)
    for lam in lams:
        print(f'\n# m={m:.0f} GeV, Lambda={lam} keV, B={B_CMS} T, no material; Delta s in um')
        print('# ev  gamma*  eps_perp   ln(lmax/b)  c_ev   eta[rad]   Ds_model  Ds_causal  ratio  Nhits(model,causal)')
        rat = []; cs = []
        for k, (p1, p2, info) in enumerate(ev):
            Hm, pp = model_hits(p1, p2, m, lam)
            H0, _ = model_hits(p1, p2, m, lam, eta_scale=0.0)
            Hc = causal_hits(p1, p2, m, lam)
            dm = plane_fit(Hm[:, 2:5])[0] if len(Hm) >= 4 else np.nan
            d0 = plane_fit(H0[:, 2:5])[0] if len(H0) >= 4 else np.nan
            dc = plane_fit(Hc[:, 3:6])[0] if len(Hc) >= 4 else np.nan
            c_ev = 1 / (pp['L'] + K_of(pp['gs']))
            rat.append(dm / dc); cs.append(c_ev)
            print(f'{k:4d}  {pp["gs"]:.3f}  {pp["eps_perp"]:.2e}  {pp["L"]:8.3f}  {c_ev:.4f}  {pp["eta"]:.2e}  '
                  f'{dm*1e4:8.3f}  {dc*1e4:8.3f}  {dm/dc:6.3f}  ({len(Hm)},{len(Hc)})  [vacuum model {d0*1e4:.1e}]', flush=True)
        rat = np.array(rat)
        print(f'# median ratio model/causal = {np.nanmedian(rat):.3f}, 16-84%: {np.nanpercentile(rat,16):.3f}-{np.nanpercentile(rat,84):.3f};'
              f' median c_event = {np.median(cs):.4f}')
