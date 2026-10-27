"""T2_propagator.py -- vacuum quirk-pair propagator (theory track, investigator T2).

Purpose
-------
Reference implementation of the dynamics of two massive endpoints joined by a Nambu-Goto string
(tension sigma = Lambda^2, Lambda == sqrt(sigma)), with no external forces (vacuum), plus hooks so
that T3 can add B fields / matter.  Four independent descriptions are provided and cross-checked in
T2_test_propagator.py:

  1. ExactPair         -- exact closed-form solution.  In the pair CM frame the motion of a pair
                          produced at one point is exactly 1-D ("yo-yo"); the momentum of quirk 1
                          along the axis is a triangle wave of amplitude p* and period 4p*/sigma.
                          Lab-frame positions follow by an exact Lorentz transformation of the two
                          world lines (no simultaneity approximation is needed).
  2. li_analytic_lab   -- the lab-frame closed form of Li-Li-Pei-Zhang [2002.07503 Eq.II.4-II.8].
                          Shown here to be *exact* in vacuum (not an approximation).
  3. LabStraightString -- lab-frame ODE integrator of the Kang-Luty endpoint equation
                          [0805.4642 Eq.3.8] with s_hat = direction of the lab-SIMULTANEOUS
                          separation, adaptive DOP853 with crossing events.  Accepts an external
                          force callback fext(i, x, p, t) -> 3-vector [GeV/cm].
  4. CausalNullString  -- a Python port of the "string-vector queue" algorithm of the ATLAS Athena
                          package Simulation/G4Extensions/Quirks (InfracolorForce / HyperbolaStep,
                          read from gitlab.cern.ch/atlas/athena, main branch, 2026-10-07): the
                          string is a queue of null 4-vectors travelling between the endpoints;
                          each endpoint absorbs an incoming vector s_in and re-emits its reflection
                          s_out about (p + F s_in); dx = s_in + s_out, dp = F (s_in - s_out).
                          This is the exact Nambu-Goto dynamics for piecewise-null string data
                          (causal; no straight-string assumption).  Optional uniform E, B kicks
                          are applied exactly as in Athena (first-order splitting + mass-shell
                          renormalisation).

Units
-----
Lengths and times in cm (c = 1), momenta/energies/masses in GeV, string force sigma in GeV/cm.
Helper sigma_from_lambda_keV(L) converts Lambda [keV] -> sigma [GeV/cm]:
    sigma = (L*1e-6 GeV)^2 / (hbar c = 1.97327e-14 GeV cm) = 50.68 GeV/cm * (L/keV)^2.
Lorentz force: F = q v x B with q in units of e and B in tesla gives
    |F| [GeV/cm] = 2.99792e-3 * |q| * |v x B|[T].

How to run
----------
    pixi run python code/T2_propagator.py          # quick self-demo
    pixi run python code/T2_test_propagator.py     # unit tests (energy, period, cross-checks)
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HBARC_GEV_CM = 1.973269804e-14
C_CM_PER_NS = 29.9792458
EB_GEV_PER_CM_PER_T = 2.99792458e-3   # e * c * 1 T in GeV/cm


def sigma_from_lambda_keV(lam_keV: float) -> float:
    """String tension sigma = Lambda^2 in GeV/cm for Lambda in keV."""
    return (lam_keV * 1e-6) ** 2 / HBARC_GEV_CM


# ----------------------------------------------------------------------------------------------
# 1. Exact solution
# ----------------------------------------------------------------------------------------------
class ExactPair:
    """Exact vacuum solution for a pair produced at the origin at t = 0.

    Parameters
    ----------
    p1, p2 : lab 3-momenta [GeV] of the two quirks at production
    m1, m2 : masses [GeV]
    sigma  : string tension [GeV/cm]

    CM frame: total 4-momentum P = p1+p2 (string has zero energy at production).  Quirk 1 moves
    along +n (unit vector of its CM momentum).  With q(t*) = triangle wave (amplitude p*, period
    T* = 4 p*/sigma),
        x1*(t*) = sgn * (E1* - E1(q))/sigma * n,   x2*(t*) = -sgn * (E2* - E2(q))/sigma * n,
    sgn = +1 in the first half period, -1 in the second.  The centre of energy (quirks + string)
    stays at the origin.  Max separation  l_max = (M - m1 - m2)/sigma.
    """

    def __init__(self, p1, p2, m1, m2, sigma):
        self.m1, self.m2, self.sigma = float(m1), float(m2), float(sigma)
        p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
        E1 = np.sqrt(m1 ** 2 + p1 @ p1); E2 = np.sqrt(m2 ** 2 + p2 @ p2)
        self.P = p1 + p2; self.E = E1 + E2
        self.M = np.sqrt(self.E ** 2 - self.P @ self.P)
        self.beta = self.P / self.E
        b2 = self.beta @ self.beta
        self.gamma = 1.0 / np.sqrt(1.0 - b2)
        # CM momentum of quirk 1
        p1cm = self._boost_p(p1, E1, -self.beta)
        self.pstar = np.linalg.norm(p1cm)
        self.n = p1cm / self.pstar
        self.E1s = np.sqrt(m1 ** 2 + self.pstar ** 2)
        self.E2s = np.sqrt(m2 ** 2 + self.pstar ** 2)
        self.Tcm = 4.0 * self.pstar / self.sigma          # full CM period (return to same state)
        self.lmax = (self.M - m1 - m2) / self.sigma        # max CM separation
        bhat = self.beta / np.sqrt(b2) if b2 > 0 else np.array([0, 0, 1.0])
        self.cos_theta_star = float(self.n @ bhat) if b2 > 0 else 0.0
        self.bhat = bhat

    @staticmethod
    def _boost_p(p, E, beta):
        """Boost 4-momentum (E,p) by velocity beta (returns 3-momentum)."""
        b2 = beta @ beta
        if b2 == 0:
            return p.copy()
        g = 1 / np.sqrt(1 - b2)
        bp = beta @ p
        return p + ((g - 1) * bp / b2 + g * E) * beta

    # --- CM world lines -------------------------------------------------------------------
    def q_of_tcm(self, tc):
        """Signed momentum of quirk 1 along n (quirk 2 has -q), triangle wave."""
        tc = np.asarray(tc, float)
        ph = np.mod(tc, self.Tcm)
        half = self.Tcm / 2
        return np.where(ph < half, self.pstar - self.sigma * ph, -self.pstar + self.sigma * (ph - half))

    def x_cm(self, tc):
        """Scalar coordinates (along n) of quirks 1, 2 at CM time tc."""
        tc = np.asarray(tc, float)
        q = self.q_of_tcm(tc)
        ph = np.mod(tc, self.Tcm)
        sgn = np.where(ph < self.Tcm / 2, 1.0, -1.0)
        x1 = sgn * (self.E1s - np.sqrt(self.m1 ** 2 + q ** 2)) / self.sigma
        x2 = -sgn * (self.E2s - np.sqrt(self.m2 ** 2 + q ** 2)) / self.sigma
        return x1, x2

    def v_cm(self, tc):
        q = self.q_of_tcm(tc)
        return q / np.sqrt(self.m1 ** 2 + q ** 2), -q / np.sqrt(self.m2 ** 2 + q ** 2)

    # --- lab ------------------------------------------------------------------------------
    def _event_lab(self, tc, xs):
        """CM event (tc, xs*n) -> lab (t, x-vector)."""
        b = self.beta; g = self.gamma
        xv = np.multiply.outer(np.atleast_1d(xs), self.n)
        b2 = b @ b
        bx = xv @ b
        t = g * (np.atleast_1d(tc) + bx)
        if b2 > 0:
            x = xv + np.multiply.outer((g - 1) * bx / b2 + g * np.atleast_1d(tc), b)
        else:
            x = xv
        return t, x

    def lab_positions(self, t_lab):
        """Exact lab positions (N,3) of quirk 1 and quirk 2 at lab times t_lab (array, cm)."""
        t_lab = np.atleast_1d(np.asarray(t_lab, float))
        out = []
        bn = float(self.beta @ self.n)
        for k in (0, 1):
            pos = np.empty((len(t_lab), 3))
            for j, t in enumerate(t_lab):
                def f(tc):
                    xs = self.x_cm(tc)[k]
                    return self.gamma * (tc + bn * xs) - t
                lo = t / self.gamma - 2 * self.lmax - 1e-9 * (1 + abs(t))
                hi = t / self.gamma + 2 * self.lmax + 1e-9 * (1 + abs(t))
                tc = brentq(f, lo, hi, xtol=1e-14 * (1 + abs(t)), rtol=1e-14, maxiter=500)
                xs = self.x_cm(tc)[k]
                _, x = self._event_lab(tc, xs)
                pos[j] = x[0]
            out.append(pos)
        return out[0], out[1]

    # --- closed-form observables ----------------------------------------------------------
    def crossing_spacing_lab(self):
        """Lab distance and lab time between successive crossings (exact): 2p*(beta gamma)/sigma,
        2p* gamma/sigma.  (Crossings are CM events at the CM origin.)"""
        bg = self.gamma * np.linalg.norm(self.beta)
        return 2 * self.pstar * bg / self.sigma, 2 * self.pstar * self.gamma / self.sigma

    def lab_max_separation(self):
        """Exact maximum of the lab-SIMULTANEOUS separation (equal masses), and its component
        transverse to the pair velocity.  Derivation in the report (Sec. 2.3)."""
        assert abs(self.m1 - self.m2) < 1e-9 * self.m1
        m, s = self.m1, self.sigma
        b = np.linalg.norm(self.beta); c = self.cos_theta_star
        k = b * c
        gs = self.E1s / m
        # solve u = |k| (gamma* - sqrt(1+u^2))
        u = brentq(lambda u: u - abs(k) * (gs - np.sqrt(1 + u * u)), 0.0, gs + 1)
        dxs = 2 * m / s * (gs - np.sqrt(1 + u * u))     # CM-coordinate chord along lab slice
        full = dxs * np.sqrt(1 - k * k)
        transverse = dxs * np.sqrt(max(0.0, 1 - c * c))
        return full, transverse


# ----------------------------------------------------------------------------------------------
# 2. Li-Li-Pei-Zhang lab-frame closed form [2002.07503 Eq.II.4-II.8]
# ----------------------------------------------------------------------------------------------
def li_analytic_lab(p1, p2, m, sigma, t):
    """Positions of the two quirks at lab time t (array) from 2002.07503 Eq.II.4-II.7.

    e_x = unit(v1 - v2), e_y = unit(p1 - (p1.e_x) e_x); rho_i = p_i.e_x/m; h = p1.e_y/E1;
    l = sqrt(1-h^2) sigma t / (m (rho1 - rho2)).  Equal masses only (as in the paper).
    """
    p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
    E1 = np.sqrt(m * m + p1 @ p1); E2 = np.sqrt(m * m + p2 @ p2)
    ex = p1 / E1 - p2 / E2; ex /= np.linalg.norm(ex)
    ey = p1 - (p1 @ ex) * ex
    ney = np.linalg.norm(ey)
    ey = ey / ney if ney > 0 else np.cross(ex, [0, 0, 1.0]) / np.linalg.norm(np.cross(ex, [0, 0, 1.0]))
    r1, r2 = (p1 @ ex) / m, (p2 @ ex) / m
    h = (p1 @ ey) / E1
    t = np.atleast_1d(np.asarray(t, float))
    l = np.sqrt(1 - h * h) * sigma * t / (m * (r1 - r2))

    def ro1(l):
        return (m / sigma * (np.sqrt(1 + r1 ** 2) - np.sqrt(1 + (r1 - l * (r1 - r2)) ** 2)))[:, None] * ex \
            + (m / sigma * h * (r1 - r2) * l / np.sqrt(1 - h * h))[:, None] * ey

    def ro2(l):
        return (m / sigma * (np.sqrt(1 + (r2 - l * (r2 - r1)) ** 2) - np.sqrt(1 + r2 ** 2)))[:, None] * ex \
            + (m / sigma * h * (r1 - r2) * l / np.sqrt(1 - h * h))[:, None] * ey

    L = np.floor(l); lb = l - L
    one = np.ones_like(l)
    even = (np.mod(L, 2) == 0)[:, None]
    r1v = L[:, None] * ro1(one) + np.where(even, ro1(lb), ro2(lb))
    r2v = L[:, None] * ro2(one) + np.where(even, ro2(lb), ro1(lb))
    return r1v, r2v


# ----------------------------------------------------------------------------------------------
# 3. Lab-frame straight-string integrator (Kang-Luty endpoint equation)
# ----------------------------------------------------------------------------------------------
def kang_luty_force(v, shat, sigma):
    """String force on an endpoint [0805.4642 Eq.3.8]: shat = unit vector along the string at the
    endpoint pointing OUTWARD (from the partner towards this endpoint)."""
    vpar = v @ shat
    vperp = v - vpar * shat
    vp2 = vperp @ vperp
    root = np.sqrt(max(1.0 - vp2, 1e-300))
    return -sigma * (root * shat + vpar * vperp / root)


class LabStraightString:
    """Integrate both endpoints at common LAB time with s_hat = unit(x_i - x_j) (lab-simultaneous).

    In vacuum this is exact (the world sheet of the CM yo-yo is a flat timelike 2-plane, so every
    lab-time slice of it is a straight segment with a FIXED direction n_perp + n_par/gamma).
    With external forces it is the usual 'instantaneous straight string' approximation.

    fext(i, x, p, t) -> 3-vector force [GeV/cm] on quirk i (0 or 1); None for vacuum.
    """

    def __init__(self, m1, m2, sigma, fext=None, rtol=1e-11, atol_x=1e-13, atol_p=1e-10):
        self.m = (float(m1), float(m2)); self.sigma = float(sigma); self.fext = fext
        self.rtol = rtol
        self.atol = np.r_[np.full(3, atol_x), np.full(3, atol_p), np.full(3, atol_x), np.full(3, atol_p)]

    def _rhs(self, t, y, sref):
        x1, p1, x2, p2 = y[0:3], y[3:6], y[6:9], y[9:12]
        d = x1 - x2
        nd = np.linalg.norm(d)
        s1 = d / nd if nd > 1e-12 * (1 + abs(t)) else sref
        out = np.empty(12)
        for i, (x, p, s) in enumerate(((x1, p1, s1), (x2, p2, -s1))):
            E = np.sqrt(self.m[i] ** 2 + p @ p)
            v = p / E
            F = kang_luty_force(v, s, self.sigma)
            if self.fext is not None:
                F = F + self.fext(i, x, p, t)
            out[6 * i:6 * i + 3] = v
            out[6 * i + 3:6 * i + 6] = F
        return out

    def run(self, p1, p2, t_end, x1=(0, 0, 0), x2=(0, 0, 0), t0=0.0, max_step=np.inf, dense=True,
            max_segments=10 ** 6):
        """Integrate from t0 to t_end.  Returns dict with t (N), y (N,12), crossing times."""
        p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
        y = np.r_[np.asarray(x1, float), p1, np.asarray(x2, float), p2]
        v1 = p1 / np.sqrt(self.m[0] ** 2 + p1 @ p1); v2 = p2 / np.sqrt(self.m[1] ** 2 + p2 @ p2)
        d0 = y[0:3] - y[6:9]
        sref = d0 / np.linalg.norm(d0) if np.linalg.norm(d0) > 0 else (v1 - v2) / np.linalg.norm(v1 - v2)
        ts, ys, tcross = [np.array([t0])], [y[None, :]], []
        t = t0
        nseg = 0
        while t < t_end and nseg < max_segments:
            nseg += 1
            s_ref = sref.copy()

            def ev(tt, yy, s_ref=s_ref):
                return (yy[0:3] - yy[6:9]) @ s_ref
            ev.terminal = True; ev.direction = -1
            # avoid immediately re-triggering at the segment start (g = 0): nudge with free motion
            sol = solve_ivp(self._rhs, (t, t_end), y, method='DOP853', args=(s_ref,), rtol=self.rtol,
                            atol=self.atol, events=ev, max_step=max_step, dense_output=False,
                            first_step=None)
            ts.append(sol.t[1:]); ys.append(sol.y[:, 1:].T)
            y = sol.y[:, -1].copy(); t = sol.t[-1]
            if sol.status == 1 and len(sol.t_events[0]) > 0:
                tcross.append(t)
                sref = -sref
                # take one tiny free step past the crossing so that g starts positive
                h = 1e-9 * max(abs(t), 1e-6)
                y = y + h * self._rhs(t, y, sref)
                t = t + h
            elif sol.status != 0:
                raise RuntimeError(sol.message)
        return dict(t=np.concatenate(ts), y=np.concatenate(ys), tcross=np.array(tcross))


# ----------------------------------------------------------------------------------------------
# 4. Causal null-vector string (port of ATLAS Athena Quirks InfracolorForce/HyperbolaStep)
# ----------------------------------------------------------------------------------------------
def mdot(a, b):
    """Minkowski product, metric (+,-,-,-), 4-vectors stored as (t, x, y, z)."""
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


class CausalNullString:
    """Port of the Athena Quirks string-vector algorithm (vacuum + optional uniform E,B).

    Each quirk k keeps a FIFO of incoming null 4-vectors (length units).  Absorbing s_in:
        a = p + F s_in,  s_out = 2 (s_in.a) a / a^2 - s_in,
        dx = s_in + s_out,  dp = F (s_in - s_out),
    and s_out is appended to the partner's queue.  Steps are split so that the boost per step obeys
    exp(dy) - 1 <= 2 F s_in.p / m^2 limit (Athena: maxBoost = 1e-2, InfracolorForce::SetMaxBoost).
    The first string vector (Athena InfracolorForce::StartTracking) is
        s0 ~ u_partner - u_self (u_self.u_partner - sqrt((u_self.u_partner)^2 - 1)),  t(s0) = L0,
    and its consumed part is 'borrowed' from the partner's first emissions, as in Athena.
    External uniform fields (E in GeV/cm per unit charge, B in tesla) are applied after each step
    as in HyperbolaStep::Step (kick with chord dx, then mass-shell renormalisation).
    Tracking alternates: a quirk is stepped until its queue is empty (QuirkWatcher -> fSuspend).
    """

    def __init__(self, m, sigma, charges=(1.0, -1.0), Bfield=None, Efield=None, max_boost=1e-2,
                 first_length=1e-7, fext_kick=None):
        self.m = float(m); self.F = float(sigma)
        self.q = charges
        self.B = None if Bfield is None else np.asarray(Bfield, float)
        self.E = None if Efield is None else np.asarray(Efield, float)
        self.max_exp_y = np.sqrt((1 + max_boost) / (1 - max_boost))
        self.L0 = first_length
        self.fext_kick = fext_kick   # optional callable(k, x4, p4, dx4) -> dp4 (generic hook)

    def run(self, p1, p2, t_end, max_steps=5_000_000):
        m, F = self.m, self.F
        P = [np.r_[np.sqrt(m * m + np.dot(p, p)), p] for p in (np.asarray(p1, float), np.asarray(p2, float))]
        X = [np.zeros(4), np.zeros(4)]
        queues = [[], []]
        borrowed = [np.zeros(4), np.zeros(4)]
        # quirk 0 is tracked first and has no string yet (suspended); quirk 1 gets the first vector
        u0 = P[0] / m; u1 = P[1] / m
        dot = mdot(u1, u0)
        s0 = u0 - u1 * (dot - np.sqrt(dot * dot - 1))
        s0 = s0 * (self.L0 / s0[0])
        s0[0] = np.linalg.norm(s0[1:])             # make exactly null (Athena: set(vect, 0))
        queues[1].append(s0)
        first_step = [False, True]
        traj = [[X[0].copy()], [X[1].copy()]]
        mom = [[P[0].copy()], [P[1].copy()]]
        nsteps = 0
        k = 1
        while nsteps < max_steps:
            if min(X[0][0], X[1][0]) > t_end:
                break
            if not queues[k]:
                k = 1 - k
                if not queues[k]:
                    break
                continue
            # absorb vectors from queue k
            while queues[k] and nsteps < max_steps and X[k][0] <= t_end + 1e-12:
                s_in = queues[k][0]
                p = P[k]
                tmp = 2 * F * mdot(s_in, p) / (m * m)
                frac = 1.0
                if tmp > self.max_exp_y - 1:
                    frac = (self.max_exp_y - 1) / tmp
                s = s_in * frac
                a = p + F * s
                s_out = 2 * mdot(s, a) / mdot(a, a) * a - s
                dx = s + s_out
                Xn = X[k] + dx
                pn = p + F * (s - s_out)
                if self.B is not None or self.E is not None:
                    dt = dx[0]; dxv = dx[1:]
                    dpf = np.zeros(3); dEf = 0.0
                    if self.E is not None:
                        dpf += self.q[k] * self.E * dt
                        dEf += self.q[k] * (self.E @ dxv)
                    if self.B is not None:
                        dpf += self.q[k] * EB_GEV_PER_CM_PER_T * np.cross(dxv, self.B)
                    pn = pn + np.r_[dEf, dpf]
                if self.fext_kick is not None:
                    pn = pn + self.fext_kick(k, X[k], p, dx)
                pn = pn * (m / np.sqrt(mdot(pn, pn)))
                X[k] = Xn; P[k] = pn
                traj[k].append(Xn.copy()); mom[k].append(pn.copy())
                # pop / partial consumption
                if frac >= 1.0:
                    queues[k].pop(0)
                else:
                    queues[k][0] = s_in * (1 - frac)
                if first_step[k]:
                    borrowed[1 - k] = borrowed[1 - k] + s   # consumed part of the first vector
                    if frac >= 1.0:
                        first_step[k] = False
                # push s_out to partner, subtracting the borrowed first string if any
                j = 1 - k
                v = s_out
                if borrowed[j][0] > 0:
                    if borrowed[j][0] <= v[0]:
                        v = v * (1 - borrowed[j][0] / v[0])
                        borrowed[j] = np.zeros(4)
                    else:
                        borrowed[j] = borrowed[j] * (1 - v[0] / borrowed[j][0])
                        v = np.zeros(4)
                if v[0] > 0:
                    queues[j].append(v)
                nsteps += 1
            k = 1 - k
        return [np.array(traj[0]), np.array(traj[1])], [np.array(mom[0]), np.array(mom[1])]


def interp_track(traj4, t):
    """Linear interpolation of a 4-vector trajectory (N,4) at lab times t."""
    tt = traj4[:, 0]
    return np.stack([np.interp(t, tt, traj4[:, i]) for i in (1, 2, 3)], axis=-1)


# ----------------------------------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------------------------------
def plane_thickness(hits):
    """sqrt of the smallest eigenvalue of T_ij = sum h_i h_j/(N-1) (plane through the origin),
    [1708.02243; 2002.07503 Eq.C.1]."""
    h = np.asarray(hits, float)
    T = h.T @ h / (len(h) - 1)
    return np.sqrt(max(np.linalg.eigvalsh(T)[0], 0.0))


def radius_crossings(t, x, radii):
    """Linear-interpolated points where a trajectory x(t) (N,3) crosses cylinders r = radii."""
    r = np.hypot(x[:, 0], x[:, 1])
    hits = []
    for R in radii:
        s = np.sign(r - R)
        idx = np.where(s[:-1] * s[1:] < 0)[0]
        for i in idx:
            f = (R - r[i]) / (r[i + 1] - r[i])
            hits.append((R, t[i] + f * (t[i + 1] - t[i]), x[i] + f * (x[i + 1] - x[i])))
    return hits


if __name__ == '__main__':
    sig = sigma_from_lambda_keV(1.0)
    m = 500.0
    p1 = np.array([300.0, 50.0, 100.0]); p2 = np.array([-150.0, 120.0, 40.0])
    ex = ExactPair(p1, p2, m, m, sig)
    print(f'sigma(1 keV) = {sig:.4f} GeV/cm;  M = {ex.M:.2f} GeV, p* = {ex.pstar:.2f} GeV, '
          f'gamma_pair = {ex.gamma:.4f}')
    print(f'l_max(CM) = {ex.lmax:.4f} cm; CM period = {ex.Tcm:.4f} cm = {ex.Tcm / C_CM_PER_NS:.4f} ns')
    D, Dt = ex.crossing_spacing_lab()
    print(f'lab crossing spacing = {D:.4f} cm, every {Dt / C_CM_PER_NS:.4f} ns')
    print('lab max separation (full, transverse) =', ex.lab_max_separation())
