"""R1_conformal_ng.py -- INDEPENDENT Nambu-Goto solver for a quirk pair (massive endpoints) in a uniform B field,
written by the critical reviewer R1 to test the "causal string" numbers of T2/T3/T4 without reusing their code.

Formulation (textbook NG open string with massive endpoints, conformal gauge, endpoints at sigma = 0, pi):
    X(tau, sigma) = [A(tau + sigma) + B(tau - sigma)] / 2,   A', B' null 4-vectors.
At an endpoint with 4-velocity u (u.u = 1, metric +---), incoming null vector w and outgoing null vector o:
    dX/dtau = (u.w) u                      (endpoint world line, X' parallel to u)
    o       = 2 (u.w) u - w                (o null, (w + o)/2 = dX/dtau)
    m du/dtau = T (w - (u.w) u) + q kappa (u.w) (0, u_vec x B)     (string pull + Lorentz force)
Endpoint 1 (sigma = 0) absorbs A'(tau) and emits B'(tau); endpoint 2 (sigma = pi) absorbs B'(tau - pi) and emits
A'(tau + pi).  So each endpoint's incoming vector is the partner's outgoing vector emitted a conformal time pi
earlier:  w_k(tau) = o_{1-k}(tau - pi).  This is a delay ODE in the common conformal time tau, solved here with
classical RK4 (fixed step h = pi/N) and 4-point Lagrange interpolation of the delayed history.  It shares no code
and no discretisation with the Athena-type piecewise-null map (T2 CausalNullString, T3_causal.py), which applies
exact hyperbolic maps to a FIFO of finite null segments with alternating tracking.
Initial condition: a static straight string of length delta (default 1e-7 cm) along unit(v1 - v2), centred on the
origin; the endpoints start with the given lab momenta.  The bootstrap mismatch costs ~T*delta of energy.
Diagnostics: canonical momentum P_q1 + P_q2 + P_string - kappa sum q_i X_i x B (conserved exactly by NG + Lorentz).
Units: cm, GeV, c = 1; B in tesla.
Run: (from theory_track/) pixi run python code/R1_conformal_ng.py   -> self-tests + comparison table
"""
import os, sys, time
import numpy as np
from numba import njit

KAPPA = 2.99792458e-3          # GeV / (cm T)  (e c x 1 T)


def sigma_keV(lam):
    # sigma = Lambda^2 / (hbar c);  hbar c = 1.97327e-14 GeV cm
    return (lam * 1e-6) ** 2 / 1.9732698e-14


@njit(cache=True)
def _mdot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


@njit(cache=True)
def _rhs(u, w, T, m, q, Bz):
    uw = _mdot(u, w)
    du = (T / m) * (w - uw * u)
    # Lorentz: dp_vec/dtau = q kappa dX_vec/dtau x B, B = (0,0,Bz);  u_vec x B = (uy Bz, -ux Bz, 0)
    du[1] += q * KAPPA * uw * u[2] * Bz / m
    du[2] -= q * KAPPA * uw * u[1] * Bz / m
    dX = uw * u
    return du, dX


@njit(cache=True)
def _interp(hist, n0, x):
    """4-point Lagrange interpolation of hist (rows = grid index - n0 offset) at fractional index x (absolute)."""
    i = int(np.floor(x)) - 1
    if i < n0:
        i = n0
    t = x - i
    # nodes i, i+1, i+2, i+3 at t = 0,1,2,3
    l0 = -(t - 1) * (t - 2) * (t - 3) / 6.0
    l1 = t * (t - 2) * (t - 3) / 2.0
    l2 = -t * (t - 1) * (t - 3) / 2.0
    l3 = t * (t - 1) * (t - 2) / 6.0
    j = i - n0
    return l0 * hist[j] + l1 * hist[j + 1] + l2 * hist[j + 2] + l3 * hist[j + 3]


@njit(cache=True)
def _herm(X0, X1, D0, D1, s):
    h00 = 2 * s ** 3 - 3 * s ** 2 + 1; h10 = s ** 3 - 2 * s ** 2 + s
    h01 = -2 * s ** 3 + 3 * s ** 2; h11 = s ** 3 - s ** 2
    return h00 * X0 + h10 * D0 + h01 * X1 + h11 * D1


@njit(cache=True)
def solve(p1, p2, m, T, Bz, q1, q2, N, t_end, delta, max_steps, radii, max_hits, ncanon):
    """Delay-ODE RK4 in conformal time.  Ring buffer of outgoing vectors (length N + 8).  Hits at radius
    crossings are found in-loop with cubic Hermite interpolation in tau (positions + dX/dtau at both ends).
    Returns hits (n, 6) = [k, layer, t, x, y, z], canonical-momentum samples (ncanon, 4), steps."""
    h = np.pi / N
    RB = N + 8
    o = np.zeros((2, RB, 4))
    u = np.zeros((2, 4)); X = np.zeros((2, 4))
    for k in range(2):
        p = p1 if k == 0 else p2
        E = np.sqrt(m * m + p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
        u[k, 0] = E / m; u[k, 1:] = p / m
    v1 = u[0, 1:] / u[0, 0]; v2 = u[1, 1:] / u[1, 0]
    n = v2 - v1
    n = n / np.sqrt(n @ n)
    X[0, 1:] = -0.5 * delta * n; X[1, 1:] = 0.5 * delta * n
    c = delta / np.pi
    # absolute index a -> ring slot a % RB.  tau = 0 is absolute index N + 4; fill pre-history [0, N+4]
    a0 = N + 4
    for a in range(a0 + 1):
        o[1, a % RB, 0] = c; o[1, a % RB, 1:] = c * n      # o_2 history -> incoming w_1 = c(1, n)
        o[0, a % RB, 0] = c; o[0, a % RB, 1:] = -c * n     # o_1 history -> incoming w_2 = c(1, -n)
    hits = np.zeros((max_hits, 6)); nh = 0
    canon = np.zeros((ncanon, 4)); ic = 0
    qs = np.array([q1, q2])
    a = a0
    step = 0
    dXprev = np.zeros((2, 4))
    w0 = np.zeros((2, 4)); wh = np.zeros((2, 4)); w1 = np.zeros((2, 4))
    ku = np.zeros((4, 2, 4)); kX = np.zeros((4, 2, 4))
    canon_every = 200
    while step < max_steps:
        for k in range(2):
            j = 1 - k
            w0[k] = o[j, (a - N) % RB]
            w1[k] = o[j, (a - N + 1) % RB]
            # 4-point Lagrange at a - N + 0.5 using nodes a-N-1 .. a-N+2
            wh[k] = (-o[j, (a - N - 1) % RB] + 9 * o[j, (a - N) % RB] + 9 * o[j, (a - N + 1) % RB]
                     - o[j, (a - N + 2) % RB]) / 16.0
        for k in range(2):
            uw = _mdot(u[k], w0[k])
            o[k, a % RB] = 2 * uw * u[k] - w0[k]
            dXprev[k] = uw * u[k]
        if step % canon_every == 0 and ic < ncanon:
            Ps = np.zeros(4)
            for jj in range(a - N, a + 1):
                wgt = 0.5 if (jj == a - N or jj == a) else 1.0
                Ps += wgt * (o[0, jj % RB] + o[1, jj % RB])
            Ps *= 0.5 * T * h
            cm = Ps.copy()
            for k in range(2):
                cm += m * u[k]
                cm[1] -= qs[k] * KAPPA * X[k, 2] * Bz
                cm[2] += qs[k] * KAPPA * X[k, 1] * Bz
            canon[ic] = cm
            ic += 1
        uk = u.copy(); Xk = X.copy()
        for s in range(4):
            if s == 0:
                us = uk; ws = w0
            elif s == 1:
                us = uk + 0.5 * h * ku[0]; ws = wh
            elif s == 2:
                us = uk + 0.5 * h * ku[1]; ws = wh
            else:
                us = uk + h * ku[2]; ws = w1
            for k in range(2):
                du, dX = _rhs(us[k], ws[k], T, m, qs[k], Bz)
                ku[s, k] = du; kX[s, k] = dX
        u = uk + h / 6.0 * (ku[0] + 2 * ku[1] + 2 * ku[2] + ku[3])
        X = Xk + h / 6.0 * (kX[0] + 2 * kX[1] + 2 * kX[2] + kX[3])
        for k in range(2):
            u[k, 0] = np.sqrt(1.0 + u[k, 1] ** 2 + u[k, 2] ** 2 + u[k, 3] ** 2)
        # hits: radius crossings between Xk and X (Hermite with dX/dtau at both ends)
        for k in range(2):
            dXn = _mdot(u[k], w1[k]) * u[k]
            r0 = np.sqrt(Xk[k, 1] ** 2 + Xk[k, 2] ** 2); r1 = np.sqrt(X[k, 1] ** 2 + X[k, 2] ** 2)
            for L in range(radii.shape[0]):
                R = radii[L]
                if (r0 - R) * (r1 - R) < 0 and nh < max_hits:
                    lo = 0.0; hi = 1.0
                    for it in range(60):
                        mid = 0.5 * (lo + hi)
                        P = _herm(Xk[k], X[k], h * dXprev[k], h * dXn, mid)
                        rm = np.sqrt(P[1] ** 2 + P[2] ** 2)
                        if (r0 - R) * (rm - R) > 0:
                            lo = mid
                        else:
                            hi = mid
                    P = _herm(Xk[k], X[k], h * dXprev[k], h * dXn, 0.5 * (lo + hi))
                    hits[nh, 0] = k; hits[nh, 1] = L; hits[nh, 2:6] = P
                    nh += 1
        a += 1
        step += 1
        if X[0, 0] > t_end and X[1, 0] > t_end:
            break
        if np.sqrt(X[0, 1] ** 2 + X[0, 2] ** 2) > radii[-1] + 3 and np.sqrt(X[1, 1] ** 2 + X[1, 2] ** 2) > radii[-1] + 3:
            break
    return hits[:nh], canon[:ic], step


def _unused_hits_at_radii(rec, radii, zmax=None):
    """Radius crossings of each endpoint world line (cubic Hermite in tau using dX/dtau ~ finite differences)."""
    out = []
    for k in range(2):
        Xk = rec[:, k, 0:4]
        r = np.hypot(Xk[:, 1], Xk[:, 2])
        for iL, R in enumerate(radii):
            s = np.sign(r - R)
            idx = np.where(s[:-1] * s[1:] < 0)[0]
            for i in idx:
                # quadratic refinement with 3 points around the crossing
                i0 = max(i - 1, 0); i2 = min(i + 2, len(r) - 1)
                tt = np.arange(i0, i2 + 1).astype(float)
                rr = r[i0:i2 + 1]
                # find root of cubic interpolant of r(index) - R in [i, i+1]
                pc = np.polyfit(tt - i, rr - R, min(3, len(tt) - 1))
                roots = np.roots(pc)
                roots = roots[np.isreal(roots)].real
                roots = roots[(roots >= -1e-9) & (roots <= 1 + 1e-9)]
                f = roots[0] if len(roots) else (R - r[i]) / (r[i + 1] - r[i])
                pts = np.empty(4)
                for c in range(4):
                    pcc = np.polyfit(tt - i, Xk[i0:i2 + 1, c], min(3, len(tt) - 1))
                    pts[c] = np.polyval(pcc, f)
                if zmax is not None and abs(pts[3]) > zmax[iL]:
                    continue
                out.append((k, iL, pts[0], pts[1], pts[2], pts[3]))
    return np.array(out)


def plane_thickness(points):
    h = np.asarray(points, float)
    Tm = h.T @ h / (len(h) - 1)
    w, v = np.linalg.eigh(Tm)
    return np.sqrt(max(w[0], 0.0)), v[:, 0]


RADII = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3])


def run(p1, p2, m, lam, Bz=3.8, N=256, delta=1e-7, radii=None, max_steps=200_000_000, t_end=None):
    T = sigma_keV(lam)
    radii = RADII if radii is None else np.asarray(radii, float)
    P = p1 + p2
    E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    if t_end is None:
        t_end = 1.3 * radii[-1] / max(np.hypot(P[0], P[1]) / E, 1e-3) + 5
    hits, canon, nst = solve(np.asarray(p1, float), np.asarray(p2, float), float(m), T, float(Bz), 1.0, -1.0,
                             int(N), float(t_end), float(delta), int(max_steps), radii, 100000, 500000)
    return hits, canon, nst


def make_event(rng, m, gstar=1.28, pt=300.0):
    """Same kinematic recipe as T2's comparison events (fixed gamma*, pT), independent implementation."""
    M = 2 * m * gstar
    phi = rng.uniform(0, 2 * np.pi); y = rng.uniform(-0.8, 0.8)
    mT = np.hypot(M, pt)
    P = np.array([pt * np.cos(phi), pt * np.sin(phi), mT * np.sinh(y)]); E = mT * np.cosh(y)
    ps = m * np.sqrt(gstar ** 2 - 1)
    c = rng.uniform(-1, 1); ph = rng.uniform(0, 2 * np.pi); s = np.sqrt(1 - c * c)
    nn = np.array([s * np.cos(ph), s * np.sin(ph), c])
    b = P / E; g = E / M
    out = []
    for sgn in (1, -1):
        pv = sgn * ps * nn; e = np.hypot(m, ps)
        bp = b @ pv; b2 = b @ b
        out.append(pv + ((g - 1) * bp / b2 + g * e) * b)
    return out[0], out[1]


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    m = float(os.environ.get('R1_M', 500.0))
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
    lams = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['1', '2'])]
    nev = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    Ns = [int(x) for x in (sys.argv[4].split(',') if len(sys.argv) > 4 else ['128', '256'])]
    events = [make_event(rng, m) for _ in range(nev)]
    from T2_propagator import ExactPair
    from T3_causal import run_causal
    # --- self-test: vacuum hits vs exact closed form (T2 ExactPair used only as an external reference) ---
    p1, p2 = events[0]
    for lam in (1.0,):
        ex = ExactPair(p1, p2, m, m, sigma_keV(lam))
        tc = float(ex.crossing_spacing_lab()[1])
        H, canon, nst = run(p1, p2, m, lam, Bz=0.0, N=Ns[-1], radii=np.linspace(0.05, 3.0, 60), t_end=0.95 * tc)
        err = 0.0
        for hh in H:
            Xe = ex.lab_positions([hh[2]])[int(hh[0])][0]
            err = max(err, np.linalg.norm(Xe - hh[3:6]))
        print(f"[vacuum] Lambda={lam}: {len(H)} hits, max |hit - exact| = {err*1e4:.3g} um; "
              f"canonical P drift {np.abs(canon - canon[0]).max():.2e} GeV; steps {nst}", flush=True)
    for lam in lams:
        Nl = [int(x * max(1.0, lam) ** 2) for x in Ns]     # finer conformal step at larger Lambda (more crossings)
        for ie, (p1, p2) in enumerate(events):
            res = {}
            for N in Nl:
                tic = time.time()
                H, canon, nst = run(p1, p2, m, lam, Bz=3.8, N=N)
                res[N] = (H, np.abs(canon[-1, 1:] - canon[0, 1:]).max(), nst, time.time() - tic)
            rc = run_causal(p1, p2, m, lam, B0=3.8, material=False, rec_radii=RADII, rec_zmax=np.full(10, 1e9),
                            first_length=1e-7, max_boost=1e-3, hmax_trk=0.02)
            Hc = rc['hits']
            # match hits: same quirk, same layer, nearest lab time (|dt| < 0.02 cm/c)
            def match(H):
                A, Bm = [], []
                for hh in H:
                    cand = Hc[(Hc[:, 0] == hh[0]) & (Hc[:, 1] == hh[1])]
                    if len(cand) == 0:
                        continue
                    j = np.argmin(np.abs(cand[:, 2] - hh[2]))
                    if abs(cand[j, 2] - hh[2]) < 0.05:
                        A.append(hh[3:6]); Bm.append(cand[j, 3:6])
                return np.array(A), np.array(Bm)
            out = []
            for N in Nl:
                A, Bm = match(res[N][0])
                out.append(plane_thickness(A)[0] * 1e4)
            A, Bm = match(res[Nl[-1]][0])
            dc = plane_thickness(Bm)[0] * 1e4
            nrm = plane_thickness(A)[1]
            dv = Bm - A
            dperp = np.abs(dv @ nrm).max() * 1e4; dmax = np.linalg.norm(dv, axis=1).max() * 1e4
            ths = ' '.join(f"N={N}:{x:.3f}" for N, x in zip(Nl, out))
            print(f"Lambda={lam} ev{ie}: matched-hit thickness[um] conformal {ths} | causal port {dc:.3f} | "
                  f"ratio {out[-1]/dc:.4f} | hits {len(res[Nl[-1]][0])} vs {len(Hc)} ({len(A)} matched) | "
                  f"max|dhit| {dmax:.3g} um, max out-of-plane dhit {dperp:.3g} um | final canon drift "
                  f"{res[Nl[-1]][1]:.2e} GeV | steps {res[Nl[-1]][2]} ({res[Nl[-1]][3]:.0f}s)", flush=True)
