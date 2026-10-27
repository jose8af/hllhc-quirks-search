"""R1_Blinearity.py -- reviewer R1: independent test of the claimed non-linear (B ln B) response of the exact string
(synthesis T-3, T4 G-T4-4) with the R1 conformal-gauge NG solver (no Athena-type code involved).
Metric (as T4/S): for hits after the first crossing, Q68|d(B) - k d(B/k)| / Q68|d(B)|, d = hit - vacuum hit
(vacuum hits from the exact closed form, T2 ExactPair, used only as an analytic reference), plus the per-unit-B
response ratio |d(B/k)| k / |d(B)| (median).  m = 500 GeV, Lambda = 1 keV.
Run: pixi run python code/R1_Blinearity.py [nev] [N] [k]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from R1_conformal_ng import run, make_event, sigma_keV, RADII
from T2_propagator import ExactPair

nev = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
ks = [float(x) for x in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['20'])]
lam = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
m = 500.0
rng = np.random.default_rng(11)
events = [make_event(rng, m) for _ in range(nev)]


def vac_hits(p1, p2):
    ex = ExactPair(p1, p2, m, m, sigma_keV(lam))
    P = p1 + p2; E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    t = np.linspace(0, 1.3 * RADII[-1] / (np.hypot(P[0], P[1]) / E) + 5, 400001)
    X = ex.lab_positions(t)
    out = []
    for k in range(2):
        r = np.hypot(X[k][:, 0], X[k][:, 1])
        for L, R in enumerate(RADII):
            idx = np.where((r[:-1] - R) * (r[1:] - R) < 0)[0]
            for i in idx:
                f = (R - r[i]) / (r[i + 1] - r[i])
                out.append((k, L, t[i] + f * (t[i + 1] - t[i]), *(X[k][i] + f * (X[k][i + 1] - X[k][i]))))
    return np.array(out), float(ex.crossing_spacing_lab()[1])


def match(H, V):
    D = []
    for h in H:
        c = V[(V[:, 0] == h[0]) & (V[:, 1] == h[1])]
        if len(c) == 0:
            continue
        j = np.argmin(np.abs(c[:, 2] - h[2]))
        D.append((h[0], h[1], h[2], *(h[3:6] - c[j, 3:6])))
    return np.array(D)


for ie, (p1, p2) in enumerate(events):
    V, tc = vac_hits(p1, p2)
    Hb, _, _ = run(p1, p2, m, lam, Bz=3.8, N=N)
    Db = match(Hb, V)
    for k in ks:
        Hk, _, _ = run(p1, p2, m, lam, Bz=3.8 / k, N=N)
        Dk = match(Hk, V)
        rows = []
        for d in Db:
            c = Dk[(Dk[:, 0] == d[0]) & (Dk[:, 1] == d[1])]
            if len(c) == 0:
                continue
            j = np.argmin(np.abs(c[:, 2] - d[2]))
            rows.append((d[2] > tc, np.linalg.norm(d[3:6]), np.linalg.norm(d[3:6] - k * c[j, 3:6]),
                         k * np.linalg.norm(c[j, 3:6])))
        rows = np.array(rows)
        pre = rows[rows[:, 0] == 0]; post = rows[rows[:, 0] == 1]
        def met(a):
            return np.quantile(a[:, 2], 0.68) / np.quantile(a[:, 1], 0.68) if len(a) else np.nan
        print(f"ev{ie} k={k:g}: pre-first-crossing hits {len(pre)}: nonlin {met(pre):.4f}; "
              f"post: {len(post)} hits, nonlin metric {met(post):.3f}, median response ratio "
              f"k|d(B/k)|/|d(B)| = {np.median(post[:,3]/post[:,1]):.3f}; median |d(B)| {np.median(post[:,1])*1e4:.1f} um",
              flush=True)
