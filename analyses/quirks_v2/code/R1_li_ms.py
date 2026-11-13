"""R1_li_ms.py -- reviewer R1: does the LITERAL Li et al. straight-string integrator (CM-simultaneous, Eq.III.6-9)
also produce the "fake mm thickness" with multiple-scattering kicks that T3 found with T2's lab-simultaneous labSS?

Model: B = 0, thin scatterers at the T3 Phase-2 slab radii with T3's x/X0 values (beam pipe, 4 TBPX, IT service
cylinder, 3 PS, 3 2S), Highland theta0 = 13.6 MeV/(beta p) sqrt(x/X0/cos a) [1 + 0.038 ln(x/X0/cos a /beta^2)]
applied as two independent Gaussian angles when a quirk crosses a slab radius (inside its |z| half-length).
Integrator: R1_li_literal (explicit Euler, CM-simultaneous step condition Eq.III.7, s_hat Eq.III.8-9) with step
eps = frac x (Li bound Eq.III.10).  Reference: T3_causal (causal NG + T3's continuous MS, no dE/dx), different random
numbers, so only medians over events are compared.
Run: pixi run python code/R1_li_ms.py [nev] [lambdas] [frac]
"""
import os, sys
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from R1_li_literal import _kl, sigma_keV, li_step, plane_thickness, RADII  # noqa: E402

SLAB_R = np.array([2.2, 3.0, 6.1, 10.4, 14.6, 19.0, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3])
SLAB_X = np.array([0.0023, 0.012, 0.012, 0.012, 0.012, 0.010, 0.025, 0.025, 0.025, 0.018, 0.018, 0.018])
SLAB_Z = np.array([300.0, 20, 20, 20, 20, 120, 120, 120, 120, 120, 120, 120])


@njit(cache=True)
def li_ms_run(p1, p2, m, sig, eps, t_end, radii, s0, seed):
    np.random.seed(seed)
    t = np.zeros(2); r = np.zeros((2, 3)); p = np.zeros((2, 3))
    p[0] = p1; p[1] = p2
    hits = np.zeros((20000, 6)); nh = 0
    nstep = 0
    while min(t[0], t[1]) < t_end and nstep < 2_000_000_000:
        E = np.sqrt(m * m + (p * p).sum(axis=1))
        v = p / E.reshape(2, 1)
        beta = (p[0] + p[1]) / (E[0] + E[1])
        rs1 = (r[0] - r[1]) - (t[0] - t[1]) * v[0]
        rs2 = (r[1] - r[0]) - (t[1] - t[0]) * v[1]
        n1 = np.sqrt(rs1 @ rs1); n2 = np.sqrt(rs2 @ rs2)
        s1 = rs1 / n1 if n1 > 1e-14 else s0
        s2 = rs2 / n2 if n2 > 1e-14 else -s0
        F = np.zeros((2, 3))
        F[0] = _kl(v[0], s1, sig); F[1] = _kl(v[1], s2, sig)
        Et = E[0] + E[1]
        d = r[0] - r[1]
        c1 = 1 - v[0] @ beta - d @ (F[0] - (v[0] @ F[0]) * beta) / Et
        c2 = 1 - v[1] @ beta + d @ (F[1] - (v[1] @ F[1]) * beta) / Et
        if c1 >= c2:
            e1 = eps * c2 / c1; e2 = eps
        else:
            e1 = eps; e2 = eps * c1 / c2
        es = (e1, e2)
        for i in range(2):
            rn = r[i] + v[i] * es[i]
            r0 = np.sqrt(r[i, 0] ** 2 + r[i, 1] ** 2); r1 = np.sqrt(rn[0] ** 2 + rn[1] ** 2)
            pn = p[i] + F[i] * es[i]
            for L in range(SLAB_R.shape[0]):
                R = SLAB_R[L]
                if (r0 - R) * (r1 - R) < 0:
                    f = (R - r0) / (r1 - r0)
                    pos = r[i] + f * (rn - r[i])
                    if abs(pos[2]) < SLAB_Z[L]:
                        for LL in range(radii.shape[0]):
                            if radii[LL] == R and nh < hits.shape[0]:
                                hits[nh, 0] = i; hits[nh, 1] = LL; hits[nh, 2] = t[i] + f * es[i]
                                hits[nh, 3:6] = pos; nh += 1
                        # thin-scatterer MS kick
                        pm = np.sqrt(pn @ pn); Ei = np.sqrt(m * m + pm * pm); b = pm / Ei
                        rhat = np.array([pos[0], pos[1], 0.0]) / np.sqrt(pos[0] ** 2 + pos[1] ** 2)
                        cosa = abs(pn @ rhat) / pm
                        if cosa < 0.05:
                            cosa = 0.05
                        x = SLAB_X[L] / cosa
                        th0 = 13.6e-3 / (b * pm) * np.sqrt(x) * max(1.0 + 0.038 * np.log(x / b ** 2), 0.5)
                        u = pn / pm
                        a = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
                        e1v = np.cross(u, a); e1v /= np.sqrt(e1v @ e1v); e2v = np.cross(u, e1v)
                        g1 = th0 * np.random.normal(); g2 = th0 * np.random.normal()
                        un = u + g1 * e1v + g2 * e2v
                        pn = pm * un / np.sqrt(un @ un)
            r[i] = rn; p[i] = pn; t[i] += es[i]
        nstep += 1
        if np.sqrt(r[0, 0] ** 2 + r[0, 1] ** 2) > radii[-1] + 3 and np.sqrt(r[1, 0] ** 2 + r[1, 1] ** 2) > radii[-1] + 3:
            break
    return hits[:nh], nstep


if __name__ == '__main__':
    from R1_conformal_ng import make_event
    from T3_causal import run_causal
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    lams = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['3'])]
    frac = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
    m = 500.0
    rng = np.random.default_rng(23)
    events = [make_event(rng, m) for _ in range(nev)]
    for lam in lams:
        dl, dc, dl0 = [], [], []
        for ie, (p1, p2) in enumerate(events):
            P = p1 + p2; Et = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
            t_end = 1.3 * RADII[-1] / max(np.hypot(P[0], P[1]) / Et, 1e-3) + 5
            s0 = p1 / np.hypot(m, np.linalg.norm(p1)) - p2 / np.hypot(m, np.linalg.norm(p2)); s0 /= np.linalg.norm(s0)
            H, ns = li_ms_run(p1, p2, m, sigma_keV(lam), li_step(m, lam) * frac, t_end, RADII, s0, 1000 + ie)
            dl.append(plane_thickness(H[:, 3:6]) * 1e4)
            rc = run_causal(p1, p2, m, lam, B0=0.0, material=True, ms=True, eloss=False, strag=False,
                            rec_radii=RADII, rec_zmax=np.array([20.0] * 4 + [120.0] * 6), seed=2000 + ie)
            dc.append(plane_thickness(rc['hits'][:, 3:6]) * 1e4)
            print(f"Lambda={lam} ev{ie}: Li-literal+MS (eps x{frac:g}) {dl[-1]:.3g} um [{len(H)} hits, {ns} steps] | "
                  f"causal+MS {dc[-1]:.3g} um [{len(rc['hits'])}]", flush=True)
        print(f"Lambda={lam} MEDIAN: Li-literal+MS {np.median(dl):.3g} um (16-84: {np.percentile(dl,16):.3g}-"
              f"{np.percentile(dl,84):.3g}) | causal+MS {np.median(dc):.3g} um ({np.percentile(dc,16):.3g}-"
              f"{np.percentile(dc,84):.3g})", flush=True)
