"""T2_transverse_linear.py -- independent check of the transverse (out-of-plane) response of the quirk
string: exact LINEARISED Nambu-Goto dynamics around the vacuum yo-yo, solved by characteristics, compared
with (a) the causal null-vector string (Athena port, T2_propagator.CausalNullString) and (b) the
instantaneous straight-string integrator (T2_propagator.LabStraightString).  Theory track, T2.

Physics (pair CM frame, background = exact 1-D yo-yo along x):
  * the background world sheet is flat, so a small transverse displacement y(t,x) of the string obeys
    y_tt = y_xx (c = 1) between the endpoints:  y = f(t-x) + g(t+x);
  * linearising the Kang-Luty endpoint equation [0805.4642 Eq.3.8] at the right endpoint
    (outward +x, background velocity v, incoming right-mover a = f'(t-x_R), outgoing left-mover
    b = g'(t+x_R)) gives, with P = gamma m dY/dt the transverse endpoint momentum,
        dP/dt = -sigma P/(gamma m) + 2 sigma (1-v) a + F_ext,
        b = (P/(gamma m) - a (1-v)) / (1+v);
    the left endpoint is the mirror image (v -> -v, f <-> g).
  * an instantaneous straight string would instead give dP/dt = -sigma (Y_R - Y_L)/(x_R - x_L) * (...),
    i.e. it neglects the finite propagation time of the transverse signal along the string.
Test: pair at rest (p2 = -p1 along x), opposite charges in a uniform transverse field E_z (force +-qE),
i.e. the CM-frame electric field that a moving pair sees in a magnetic field [2002.07503 Eq.II.16].
Run:  pixi run python code/T2_transverse_linear.py   -> table + figures/T2_transverse_check.png
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import ExactPair, CausalNullString, LabStraightString, interp_track, sigma_from_lambda_keV


def linear_transverse(m, pstar, sigma, Fext, t_end, nstep=200000):
    """Fext(i, t) -> transverse force on quirk i (i=0: starts as right endpoint).  Returns t, Z (2, N).
    Midpoint (RK2) time stepping; waves stored on preallocated monotone grids (queries are monotone)."""
    ex = ExactPair(np.array([pstar, 0, 0.]), np.array([-pstar, 0, 0.]), m, m, sigma)
    half = ex.Tcm / 2
    dt = t_end / nstep
    # precompute background on the half-step grid
    tg = np.arange(2 * nstep + 2) * (dt / 2)
    xg1, xg2 = ex.x_cm(tg); vg1, vg2 = ex.v_cm(tg)
    xg = np.stack([xg1, xg2]); vg = np.stack([vg1, vg2])
    N = 2 * nstep + 10
    W = np.zeros(N); FW = np.zeros(N); nW = 1          # right-movers f'(w)
    U = np.zeros(N); GU = np.zeros(N); nU = 1          # left-movers g'(u)
    P = np.zeros(2); Z = np.zeros(2)
    ts, Zs = [0.0], [Z.copy()]

    def interp(X, Y, n, q):
        if n == 1 or q <= X[0]:
            return 0.0
        if q >= X[n - 1]:
            return Y[n - 1]
        j = np.searchsorted(X[:n], q)
        f = (q - X[j - 1]) / (X[j] - X[j - 1])
        return Y[j - 1] + f * (Y[j] - Y[j - 1])

    def rhs(ig, P):
        tt = tg[ig]
        k = int(np.floor(tt / half))
        R = 0 if k % 2 == 0 else 1
        dP = np.zeros(2); vel = np.zeros(2); emit = []
        for i, sgn in ((R, 1), (1 - R, -1)):
            v = vg[i, ig]; x = xg[i, ig]
            vt = sgn * v
            g = 1 / np.sqrt(1 - v * v)
            a = interp(W, FW, nW, tt - x) if sgn > 0 else interp(U, GU, nU, tt + x)
            vel[i] = P[i] / (g * m)
            dP[i] = -sigma * vel[i] + 2 * sigma * (1 - vt) * a + Fext(i, tt)
            emit.append((sgn, (vel[i] - a * (1 - vt)) / (1 + vt), tt + sgn * x))
        return dP, vel, emit

    for n in range(nstep):
        dP1, _, _ = rhs(2 * n, P)
        dP2, vel2, _ = rhs(2 * n + 1, P + 0.5 * dt * dP1)
        P = P + dt * dP2; Z = Z + dt * vel2
        _, _, emit = rhs(2 * n + 2, P)
        for sgn, b, arg in emit:
            if sgn > 0:
                if arg > U[nU - 1]:
                    U[nU] = arg; GU[nU] = b; nU += 1
            else:
                if arg > W[nW - 1]:
                    W[nW] = arg; FW[nW] = b; nW += 1
        if n % 50 == 0:
            ts.append(tg[2 * n + 2]); Zs.append(Z.copy())
    return np.array(ts), np.array(Zs).T, ex


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    m = 500.0
    sig = sigma_from_lambda_keV(1.0)
    rows = []
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for j, gs in enumerate((1.05, 1.3)):
        pstar = m * np.sqrt(gs ** 2 - 1)
        E0 = 1e-4 * sig                              # transverse force q E = 1e-4 sigma
        ex = ExactPair(np.array([pstar, 0, 0.]), np.array([-pstar, 0, 0.]), m, m, sig)
        t_end = 3 * ex.Tcm
        tl, Zl, _ = linear_transverse(m, pstar, sig, lambda i, t: E0 if i == 0 else -E0, t_end, nstep=150000)
        cs = CausalNullString(m, sig, charges=(1.0, -1.0), Efield=np.array([0, 0, E0]), max_boost=2e-3, first_length=1e-9)
        traj, _ = cs.run(np.array([pstar, 0, 0.]), np.array([-pstar, 0, 0.]), t_end)
        Zc = np.array([interp_track(traj[k], tl)[:, 2] for k in (0, 1)])
        ss = LabStraightString(m, m, sig, fext=lambda i, x, p, t: np.array([0, 0, E0 if i == 0 else -E0]), rtol=1e-11)
        sol = ss.run(np.array([pstar, 0, 0.]), np.array([-pstar, 0, 0.]), t_end)
        Zs = np.array([np.interp(tl, sol['t'], sol['y'][:, 2]), np.interp(tl, sol['t'], sol['y'][:, 8])])
        rel = lambda Z: Z[0] - Z[1]
        sc = np.max(np.abs(rel(Zl)))
        e_c = np.max(np.abs(rel(Zc) - rel(Zl))) / sc
        e_s = np.max(np.abs(rel(Zs) - rel(Zl))) / sc
        rows.append((gs, sc * 1e4, e_c, e_s, np.max(np.abs(rel(Zs))) / sc))
        ax = axes[j]
        ax.plot(tl / ex.Tcm, rel(Zl) * 1e4, 'k-', lw=2, label='linearised exact NG (characteristics)')
        ax.plot(tl / ex.Tcm, rel(Zc) * 1e4, 'C1--', label='causal null-vector string (Athena port)')
        ax.plot(tl / ex.Tcm, rel(Zs) * 1e4, 'C0:', lw=2, label='instantaneous straight string')
        ax.set_xlabel('t / T (full CM period)'); ax.set_ylabel('z₁ − z₂ [µm]')
        ax.set_title(f'm=500 GeV, Λ=1 keV, γ*={gs}, transverse force 10⁻⁴σ')
        ax.grid(alpha=0.3); ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'T2_transverse_check.png'), dpi=130)
    print('| γ* | max|z1-z2| linear NG [µm] | causal vs linear (max rel. dev.) | straight vs linear (max rel. dev.) | straight/linear amplitude |')
    print('|---|---|---|---|---|')
    for r in rows:
        print('| %.2f | %.3g | %.2g | %.2g | %.2f |' % r)
