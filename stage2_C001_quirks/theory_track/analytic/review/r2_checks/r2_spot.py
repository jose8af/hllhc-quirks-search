"""r2_spot.py -- [ABORTED, no output kept: the unmodified R1 conformal solver does not finish at 2 keV, weak B; superseded by r2_spot2.py (part S) and r2_spot3.py (parts O, C)] S1-R2 (round-2 reviewer) independent numerical spot checks of new v4 claims.

Part A ('outl'): the round-1 reviewer's 16 events (R1_conformal_ng.make_event, rng 2026, m = 500 GeV, gamma* = 1.28,
  pT = 300 GeV, Lambda = 1 keV) re-run with E2's causal kernel (nm_kernel, max_boost 1e-3, hmax 0.02 cm, the 10 barrel radii,
  no z cut = same hit set as the conformal solver).  Question: the conformal solver gave c_4 - c_E1 = +0.016/+0.032/+0.035
  for the three k_B = 8.4-12 events at 1 keV (r1_lab_c_out.txt), while E2's FIX1 says the k_B dependence of c is ABSENT at
  1 keV.  Does the causal kernel reproduce the conformal excess on these events?
Part B ('law'): headline law Delta_s_B ~ eps_B [ln(1/eps_B) + C] with C Lambda-independent, tested per event with the
  INDEPENDENT conformal solver (code/R1_conformal_ng.py, unmodified, N = 4096) and with the causal kernel, on the first NEV
  M3/T3-sample events (T3_propagator.sample_events(500, ., rng 777+500, eta_max 1)), at Lambda = 1 and 2 keV, B0 and B0/4:
  1/c(2 keV) - 1/c(1 keV) must equal ln 4 = 1.386 (c = (R(1/4)-1)/ln 4).  Also |q| = 2 <=> B -> 2 B0 exactly (only qB enters):
  Delta_s(2B0)/Delta_s(B0) at 1 keV vs E1's q[1 - ln q/(ln(1/eps_B) + C)] with the event's measured C.
Run (from TT): pixi run python analytic/review/r2_checks/r2_spot.py [NEV] > analytic/review/r2_checks/r2_spot_out.txt
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
for p in (os.path.join(TT, 'code'), os.path.join(TT, 'analytic', 'numerics'), os.path.join(TT, 'analytic', 'review', 'r1_checks')):
    sys.path.insert(0, p)
B0 = 3.8112
QB = 2.99792458e-3


def geom(p1, p2, m, lam, B=B0):
    """E1's per-event quantities (own implementation): eps_perp, gamma*, k_B = |B*perp|/|E*perp|, sin alpha, c_E1."""
    import R1_conformal_ng as R1
    sig = R1.sigma_keV(lam)
    E1 = np.hypot(m, np.linalg.norm(p1)); E2 = np.hypot(m, np.linalg.norm(p2))
    P = p1 + p2; E = E1 + E2
    beta = P / E; b2 = beta @ beta; g = 1 / np.sqrt(1 - b2); bh = beta / np.sqrt(b2)
    p1s = p1 + ((g - 1) * (p1 @ bh) - g * E1 * np.sqrt(b2)) * bh
    n = p1s / np.linalg.norm(p1s)
    gs = np.hypot(m, np.linalg.norm(p1s)) / m; rho = np.sqrt(gs * gs - 1)
    Bv = np.array([0, 0, B]); Es = g * np.cross(beta, Bv); Bs = g * Bv - (g - 1) * (Bv @ bh) * bh
    Ep = Es - (Es @ n) * n; Bp = Bs - (Bs @ n) * n
    eps = QB * np.linalg.norm(Ep) / sig
    l0 = m / sig; lmax = 2 * (gs - 1) * l0
    bodd = 2 * eps * l0 * (gs - np.arcsinh(rho) / rho)
    K = (3 * np.log(2) - 2) - 0.506 * np.log(gs) - 0.077 * np.log(gs) ** 2
    epsB = QB * B / sig
    cE = 1 / (np.log(lmax / bodd) + K)
    return dict(gs=gs, eps=eps, kB=np.linalg.norm(Bp) / np.linalg.norm(Ep), sa=np.linalg.norm(Ep) / np.linalg.norm(Es),
                cE=cE, CE=1 / cE - np.log(1 / epsB))


def ds_causal(p1, p2, m, lam, B, mb=1e-3, hm=0.02):
    from nm_kernel import run
    from nm_conformal import RADII
    from T3_propagator import plane_fit
    r = run(p1, p2, m, lam, B0=B, max_boost=mb, hmax_trk=hm, rec_radii=RADII, rec_zmax=np.full(10, 1e9), qcap=1 << 20)
    H = r['hits']; H = H[H[:, 1] < 10]
    return plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan


def ds_conf(p1, p2, m, lam, B, N=4096):
    import R1_conformal_ng as R1
    H, canon, nst = R1.run(p1, p2, m, lam, Bz=B, N=N)
    H = H[H[:, 1] < 10]
    return R1.plane_thickness(H[:, 3:6])[0] if len(H) >= 4 else np.nan


def job(a):
    kind, i, m, p1, p2 = a
    t0 = time.time()
    out = dict(kind=kind, i=i)
    if kind == 'outl':
        for f in (1.0, 0.25, 0.05):
            out[f'cau_{f}'] = ds_causal(p1, p2, m, 1.0, B0 * f)
        out['cau1e4_1.0'] = out['cau1e4_0.25'] = np.nan
        if i in (0, 3, 4, 13):
            for f in (1.0, 0.25):
                out[f'cau1e4_{f}'] = ds_causal(p1, p2, m, 1.0, B0 * f, mb=1e-4, hm=0.005)
    else:
        for lam, fs in ((1.0, (2.0, 1.0, 0.25)), (2.0, (1.0, 0.25))):
            for f in fs:
                out[f'conf_{lam}_{f}'] = ds_conf(p1, p2, m, lam, B0 * f)
                out[f'cau_{lam}_{f}'] = ds_causal(p1, p2, m, lam, B0 * f)
    out['cpu'] = time.time() - t0
    return out


if __name__ == '__main__':
    import R1_conformal_ng as R1
    from T3_propagator import sample_events
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    rng = np.random.default_rng(2026)
    outl = [R1.make_event(rng, 500.0) for _ in range(16)]
    evs = sample_events(500.0, nev, rng=np.random.default_rng(777 + 500), eta_max=1.0)
    tasks = [('outl', i, 500.0, p1, p2) for i, (p1, p2) in enumerate(outl)]
    tasks += [('law', i, 500.0, e[0], e[1]) for i, e in enumerate(evs)]
    t0 = time.time()
    with ProcessPoolExecutor(6, mp_context=mp.get_context('spawn')) as ex:
        rows = list(ex.map(job, tasks))
    # round-1 conformal values (r1_lab_c_out.txt, N = 4096): c_4 per event
    r1c4 = {}
    for line in open(os.path.join(TT, 'analytic', 'review', 'r1_checks', 'r1_lab_c_out.txt')):
        s = line.split()
        if len(s) > 10 and s[0].isdigit() and s[5] == '4096':
            r1c4[int(s[0])] = float(s[11])
    print('# Part A: round-1 events, 1 keV, causal (nm_kernel 1e-3; 1e-4 for 4 events) vs conformal c_4 (r1_lab_c_out, N=4096)')
    print('# ev  gamma*  kB     sin_a  c_E1    | c4_conf  c4_caus  c4_caus1e-4 | c20_caus | conf-E1  caus-E1')
    dA = []
    for r in [r for r in rows if r['kind'] == 'outl']:
        i = r['i']; p1, p2 = outl[i]; G = geom(p1, p2, 500.0, 1.0)
        c4 = (4 * r['cau_0.25'] / r['cau_1.0'] - 1) / np.log(4)
        c20 = (20 * r['cau_0.05'] / r['cau_1.0'] - 1) / np.log(20)
        c4v = (4 * r['cau1e4_0.25'] / r['cau1e4_1.0'] - 1) / np.log(4)
        print(f"{i:3d}  {G['gs']:.3f}  {G['kB']:6.2f}  {G['sa']:.3f}  {G['cE']:.4f} | {r1c4.get(i, np.nan):.4f}   {c4:.4f}   {c4v:.4f}     "
              f"| {c20:.4f}   | {r1c4.get(i, np.nan) - G['cE']:+.4f}  {c4 - G['cE']:+.4f}   ({r['cpu']:.0f}s)")
        dA.append((G['kB'], c4 - G['cE'], r1c4.get(i, np.nan) - G['cE']))
    dA = np.array(dA)
    for lo, hi in ((0, 6.5), (6.5, 99)):
        s = (dA[:, 0] >= lo) & (dA[:, 0] < hi)
        print(f'#  kB in [{lo},{hi}): n={s.sum()}  median caus-E1 = {np.median(dA[s, 1]):+.4f}  median conf-E1 = {np.median(dA[s, 2]):+.4f}')
    print()
    print('# Part B: M3/T3-sample events (500 GeV), c4 at 1 and 2 keV from conformal (N=4096) and causal (1e-3)')
    print('# ev gamma*  kB     c_E1(1keV) C_E1 | conf: c4(1) c4(2) D(1/c)  C(1)  | caus: c4(1) c4(2) D(1/c)  C(1) | q=2: conf caus pred(C_E1)')
    LB = []
    for r in [r for r in rows if r['kind'] == 'law']:
        i = r['i']; p1, p2 = evs[i][0], evs[i][1]; G = geom(p1, p2, 500.0, 1.0)
        epsB1 = QB * B0 / R1.sigma_keV(1.0)
        res = []
        for s in ('conf', 'cau'):
            c1 = (4 * r[f'{s}_1.0_0.25'] / r[f'{s}_1.0_1.0'] - 1) / np.log(4)
            c2 = (4 * r[f'{s}_2.0_0.25'] / r[f'{s}_2.0_1.0'] - 1) / np.log(4)
            q2 = r[f'{s}_1.0_2.0'] / r[f'{s}_1.0_1.0']
            res += [c1, c2, 1 / c2 - 1 / c1, 1 / c1 - np.log(1 / epsB1), q2]
        L = np.log(1 / epsB1)
        q2p = 2 * (1 - np.log(2) / (L + G['CE']))
        print(f"{i:3d} {G['gs']:.3f} {G['kB']:6.2f}  {G['cE']:.4f}  {G['CE']:+.3f} | {res[0]:.4f} {res[1]:.4f} {res[2]:+.3f} {res[3]:+.3f} | "
              f"{res[5]:.4f} {res[6]:.4f} {res[7]:+.3f} {res[8]:+.3f} | {res[4]:.3f} {res[9]:.3f} {q2p:.3f}  ({r['cpu']:.0f}s)")
        LB.append([G['kB'], G['CE']] + res + [q2p])
    LB = np.array(LB)
    ok = np.all(np.isfinite(LB), axis=1)
    LB = LB[ok]
    print(f'# n valid = {len(LB)};  ln 4 = {np.log(4):.3f}')
    for lab, j in (('conf', 2), ('caus', 2 + 5)):
        d = LB[:, j + 2]
        print(f'#  {lab}: median D(1/c) = {np.median(d):+.3f}, mean {d.mean():+.3f} +- {d.std(ddof=1) / np.sqrt(len(d)):.3f}; '
              f'median C(1keV) = {np.median(LB[:, j + 3]):+.3f} (E1 C_ev median {np.median(LB[:, 1]):+.3f}); '
              f'median c4(1) - c_E1 = {np.median(LB[:, j] - 1 / (np.log(1 / (QB * B0 / R1.sigma_keV(1.0))) + LB[:, 1])):+.4f}; '
              f'median q2 ratio = {np.median(LB[:, j + 4]):.3f} (pred {np.median(LB[:, -1]):.3f})')
    print(f'# wall {time.time() - t0:.0f}s, cpu {sum(r["cpu"] for r in rows):.0f}s')
