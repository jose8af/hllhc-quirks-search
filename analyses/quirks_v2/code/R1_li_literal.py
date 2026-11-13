"""R1_li_literal.py -- reviewer R1: a LITERAL implementation of the Li-Li-Pei-Zhang quirk integrator
[1911.02223 Eq.III.1-III.10 = 2002.07503 Eq.II.1-II.3 and VIII.1-VIII.4], to test whether T2's `LabStraightString`
("labSS", converged DOP853 with s_hat along the LAB-simultaneous separation) is a faithful stand-in for what Li et al.
actually ran.

Li et al. algorithm, as written in the papers:
  * explicit Euler, each quirk with its own time step eps_i;
  * the two quirks are kept CM-simultaneous, t1 - t2 = beta.(r1 - r2), beta = (P1+P2)/(E1+E2)  [Eq.III.6], by choosing
    eps_1/eps_2 from Eq.III.7;
  * s_hat_i = unit vectors of r_s1 = (r1 - r2) - (t1 - t2) v1,  r_s2 = (r2 - r1) - (t2 - t1) v2  [Eq.III.8-9];
  * string force = Kang-Luty endpoint force with lab v_i and s_hat_i [Eq.III.2]; F_ext = q v x B [Eq.III.3];
  * step bound eps < 1e-4 ns (m_Q/100 GeV)(keV/Lambda)^2  [Eq.III.10]; we run at that bound ("Li step") and at 1/10 and 1/100.
No dE/dx (B-only comparison, as in T2 Sec.5.1).  Hits: crossings of the 10 Phase-2 barrel radii (linear interpolation
inside an Euler step).  Compared, on the same events, with the causal port (T3_causal, used only as the reference
being tested elsewhere) and with T2's labSS.
Run (from theory_track/): pixi run python code/R1_li_literal.py [seed] [lambdas] [nev]
"""
import os, sys, time
import numpy as np
from numba import njit

KAPPA = 2.99792458e-3
RADII = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3])


@njit(cache=True)
def _kl(v, s, sig):
    vpar = v @ s
    vperp = v - vpar * s
    vp2 = vperp @ vperp
    root = np.sqrt(max(1.0 - vp2, 1e-300))
    return -sig * (root * s + vpar * vperp / root)


@njit(cache=True)
def li_run(p1, p2, m, sig, Bz, eps, t_end, radii, s0):
    t = np.zeros(2); r = np.zeros((2, 3)); p = np.zeros((2, 3))
    p[0] = p1; p[1] = p2
    q = np.array([1.0, -1.0])
    hits = np.zeros((20000, 6)); nh = 0
    nstep = 0
    while min(t[0], t[1]) < t_end and nstep < 2_000_000_000:
        E = np.sqrt(m * m + (p * p).sum(axis=1))
        v = p / E.reshape(2, 1)
        beta = (p[0] + p[1]) / (E[0] + E[1])
        # s_hat (outward) from Eq.III.8-9
        rs1 = (r[0] - r[1]) - (t[0] - t[1]) * v[0]
        rs2 = (r[1] - r[0]) - (t[1] - t[0]) * v[1]
        n1 = np.sqrt(rs1 @ rs1); n2 = np.sqrt(rs2 @ rs2)
        s1 = rs1 / n1 if n1 > 1e-14 else s0
        s2 = rs2 / n2 if n2 > 1e-14 else -s0
        F = np.zeros((2, 3))
        for i in range(2):
            si = s1 if i == 0 else s2
            F[i] = _kl(v[i], si, sig)
            # q v x B, B = (0,0,Bz)
            F[i, 0] += q[i] * KAPPA * v[i, 1] * Bz
            F[i, 1] -= q[i] * KAPPA * v[i, 0] * Bz
        Et = E[0] + E[1]
        d = r[0] - r[1]
        c1 = 1 - v[0] @ beta - d @ (F[0] - (v[0] @ F[0]) * beta) / Et
        c2 = 1 - v[1] @ beta + d @ (F[1] - (v[1] @ F[1]) * beta) / Et
        # eps1 c1 = eps2 c2, max(eps1, eps2) = eps
        if c1 >= c2:
            e1 = eps * c2 / c1; e2 = eps
        else:
            e1 = eps; e2 = eps * c1 / c2
        es = (e1, e2)
        for i in range(2):
            rn = r[i] + v[i] * es[i]
            r0 = np.sqrt(r[i, 0] ** 2 + r[i, 1] ** 2); r1 = np.sqrt(rn[0] ** 2 + rn[1] ** 2)
            for L in range(radii.shape[0]):
                R = radii[L]
                if (r0 - R) * (r1 - R) < 0 and nh < hits.shape[0]:
                    f = (R - r0) / (r1 - r0)
                    hits[nh, 0] = i; hits[nh, 1] = L; hits[nh, 2] = t[i] + f * es[i]
                    hits[nh, 3:6] = r[i] + f * (rn - r[i]); nh += 1
            r[i] = rn
            p[i] = p[i] + F[i] * es[i]
            t[i] += es[i]
        nstep += 1
        if np.sqrt(r[0, 0] ** 2 + r[0, 1] ** 2) > radii[-1] + 3 and np.sqrt(r[1, 0] ** 2 + r[1, 1] ** 2) > radii[-1] + 3:
            break
    return hits[:nh], nstep


def sigma_keV(lam):
    return (lam * 1e-6) ** 2 / 1.9732698e-14


def plane_thickness(points):
    h = np.asarray(points, float)
    Tm = h.T @ h / (len(h) - 1)
    return np.sqrt(max(np.linalg.eigvalsh(Tm)[0], 0.0))


def li_step(m, lam):
    return 1e-4 * 29.9792458 * (m / 100.0) / lam ** 2     # cm (c = 1)


def run_li(p1, p2, m, lam, Bz=3.8, frac=1.0):
    P = p1 + p2
    E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    t_end = 1.3 * RADII[-1] / max(np.hypot(P[0], P[1]) / E, 1e-3) + 5
    s0 = (p1 / np.hypot(m, np.linalg.norm(p1)) - p2 / np.hypot(m, np.linalg.norm(p2)))
    s0 = s0 / np.linalg.norm(s0)
    return li_run(np.asarray(p1, float), np.asarray(p2, float), float(m), sigma_keV(lam), float(Bz),
                  li_step(m, lam) * frac, float(t_end), RADII, s0)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from R1_conformal_ng import make_event
    from T3_causal import run_causal
    from T2_propagator import LabStraightString, EB_GEV_PER_CM_PER_T, radius_crossings
    m = 500.0
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
    lams = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['1', '2', '3'])]
    nev = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    events = [make_event(rng, m) for _ in range(nev)]
    fracs = [float(x) for x in (sys.argv[4].split(',') if len(sys.argv) > 4 else ['1', '0.1', '0.01', '0.001'])]
    do_lab = len(sys.argv) > 5 and sys.argv[5] == 'lab'

    def match_dmax(H, Hc):
        dm = 0.0; n = 0
        for hh in H:
            cand = Hc[(Hc[:, 0] == hh[0]) & (Hc[:, 1] == hh[1])]
            if len(cand) == 0:
                continue
            j = np.argmin(np.abs(cand[:, 2] - hh[2]))
            dm = max(dm, np.linalg.norm(cand[j, 3:6] - hh[3:6])); n += 1
        return dm, n
    for lam in lams:
        for ie, (p1, p2) in enumerate(events):
            rc = run_causal(p1, p2, m, lam, B0=3.8, material=False, rec_radii=RADII, rec_zmax=np.full(10, 1e9),
                            first_length=1e-7, max_boost=1e-3, hmax_trk=0.02)
            Hc = rc['hits']
            dc = plane_thickness(Hc[:, 3:6])
            row = [f"Lambda={lam} ev{ie}: causal {dc*1e4:.3g} um [{len(Hc)}]"]
            for frac in fracs:
                H, ns = run_li(p1, p2, m, lam, frac=frac)
                dm, n = match_dmax(H, Hc)
                row.append(f"Li(x{frac:g}) {plane_thickness(H[:, 3:6])*1e4:.3g} um [{len(H)}; max|dhit| {dm*1e4:.3g} um]")
            if do_lab:
                sig = sigma_keV(lam); Bv = np.array([0, 0, 3.8]); Q = (1.0, -1.0)

                def fext(i, x, p, t):
                    E = np.sqrt(m * m + p @ p)
                    return Q[i] * EB_GEV_PER_CM_PER_T * np.cross(p / E, Bv)
                P = p1 + p2; Et = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
                t_end = 1.3 * RADII[-1] / max(np.hypot(P[0], P[1]) / Et, 1e-3) + 5
                sol = LabStraightString(m, m, sig, fext=fext, rtol=1e-10).run(p1, p2, t_end)
                y = sol['y']; hh = []
                for kq, (a, b) in enumerate(((0, 3), (6, 9))):
                    hh += [(kq, RADII.tolist().index(h[0]), h[1], *h[2]) for h in radius_crossings(sol['t'], y[:, a:b], RADII)]
                hh = np.array(hh, float)
                dm, n = match_dmax(hh, Hc)
                row.append(f"T2 labSS {plane_thickness(hh[:, 3:6])*1e4:.3g} um [max|dhit| {dm*1e4:.3g} um]")
            print(' | '.join(row), flush=True)
