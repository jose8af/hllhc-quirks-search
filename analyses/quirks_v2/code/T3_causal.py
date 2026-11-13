"""T3_causal.py -- numba port of the causal (null-vector) Nambu-Goto quirk-string propagator, with B field and
material (theory track, investigator T3).

Why: T2 (`T2_string_methods_B.py`, figures/T2_string_methods_B.png) showed that the lab-simultaneous straight-string
force (Kang-Luty with s_hat = unit(x1 - x2) at equal lab time; = T2 LabStraightString = the numba kernel in
T3_propagator.py) is exact in vacuum but violates momentum conservation as soon as an external force acts
(drift of the canonical momentum by 0.2-7 GeV over the tracker), which inflates the plane thickness to
20-1000 um at any Lambda.  T3 confirmed it independently: with material kicks and B = 0 it produces a spurious
thickness that grows with the number of crossings.  The causal algorithm of the ATLAS Athena package
Simulation/G4Extensions/Quirks (InfracolorForce / HyperbolaStep; Python port T2_propagator.CausalNullString)
is exact Nambu-Goto dynamics for piecewise-null string data, so arbitrary endpoint kicks are propagated along
the string causally.  This file is a line-by-line numba port of T2's CausalNullString (same first-string
construction, borrowing, max-boost splitting, B kick = first-order chord kick + mass-shell renormalisation),
with three additions:
  * a step-length limit (string-vector time component <= hmax) so that hits can be linearly interpolated;
  * material (mean dE/dx, Bohr straggling, Highland MS) applied to an endpoint after each of its steps, with
    path = |dx| and the same material model as T3_propagator (Phase-2 tracker slabs + Evans-Luty outer CMS);
  * radius-crossing hit recording and stop/exit conditions.
Units: cm, GeV (c = 1).  Run the checks: pixi run python code/T3_causal.py
"""
import os, sys, time
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T, CausalNullString, ExactPair, interp_track  # noqa
from T3_propagator import (material_at, bfield, stopping_power, MAT, phase2_tracker, cms_outer_regions,   # noqa
                           DUMMY_GRID, REC_RADII, REC_ZMAX, plane_fit, sample_events)


@njit(cache=True, inline='always')
def mdot(a0, a1, a2, a3, b0, b1, b2, b3):
    return a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3


@njit(cache=True)
def _material_kick(P, X, k, m, q, dsx, slabs, regions, mat, do_eloss, do_strag, do_ms, eacc):
    """Apply energy loss / MS to 4-momentum P[k] for a path dsx at the endpoint position X[k]."""
    px = P[k, 1]; py = P[k, 2]; pz = P[k, 3]
    p = np.sqrt(px * px + py * py + pz * pz)
    if p <= 0.0 or dsx <= 0.0:
        return
    E = np.sqrt(m * m + p * p)
    beta = p / E
    za_rho, I, X0, xlay, reg = material_at(X[k, 1], X[k, 2], X[k, 3], slabs, regions, mat)
    if za_rho <= 0.0:
        return
    q2 = q * q
    if do_eloss:
        dE = stopping_power(beta, q2, za_rho, I) * dsx
        if do_strag:
            g2 = 1.0 / (1.0 - beta * beta)
            var = 0.1569e-6 * za_rho * dsx * q2 * (1.0 - 0.5 * beta * beta) * g2
            dE += np.sqrt(var) * np.random.normal()
            if dE < 0.0:
                dE = 0.0
        eacc[k] += dE
        Ek = E - m - dE
        if Ek <= 1e-9 * m:
            Ek = 1e-9 * m
        pn = np.sqrt((Ek + m) ** 2 - m * m)
        f = pn / p
        px *= f; py *= f; pz *= f; p = pn
        E = Ek + m; beta = p / E
    if do_ms and X0 < 1e29:
        xr = xlay / (beta * beta) * q2
        if xr < 1e-4:
            xr = 1e-4
        flog = 1.0 + 0.038 * np.log(xr)
        if flog < 0.5:
            flog = 0.5
        th0 = 13.6e-3 / (beta * p) * abs(q) * np.sqrt(dsx / X0) * flog
        t1 = th0 * np.random.normal(); t2 = th0 * np.random.normal()
        ux = px / p; uy = py / p; uz = pz / p
        if abs(ux) < 0.9:
            ax, ay, az = 1.0, 0.0, 0.0
        else:
            ax, ay, az = 0.0, 1.0, 0.0
        e1x = uy * az - uz * ay; e1y = uz * ax - ux * az; e1z = ux * ay - uy * ax
        n1 = np.sqrt(e1x * e1x + e1y * e1y + e1z * e1z)
        e1x /= n1; e1y /= n1; e1z /= n1
        e2x = uy * e1z - uz * e1y; e2y = uz * e1x - ux * e1z; e2z = ux * e1y - uy * e1x
        th = np.sqrt(t1 * t1 + t2 * t2)
        if th > 0:
            c = np.cos(th); s = np.sin(th) / th
            px = p * (c * ux + s * (t1 * e1x + t2 * e2x))
            py = p * (c * uy + s * (t1 * e1y + t2 * e2y))
            pz = p * (c * uz + s * (t1 * e1z + t2 * e2z))
    P[k, 0] = np.sqrt(m * m + px * px + py * py + pz * pz)
    P[k, 1] = px; P[k, 2] = py; P[k, 3] = pz


@njit(cache=True)
def causal_propagate(p1, p2, m, F, q1, q2, bmode, B0, bgrid, rgrid, zgrid, slabs, regions, mat,
                     rec_radii, rec_zmax, do_eloss, do_strag, do_ms, t_end, r_exit, z_exit, beta_stop,
                     max_boost, hmax_trk, hmax_out, first_length, seed, max_hits, max_steps, qcap,
                     kick_k, kick_R, kick_dp):
    """Returns (status, hits[n,9], X[2,4], P[2,4], eacc[2], nsteps, max_queue).
    kick_k >= 0: apply a deterministic 3-momentum kick kick_dp to quirk kick_k when it first crosses r = kick_R
    (for the kick-response study; use with material off)."""
    if seed >= 0:
        np.random.seed(seed)
    maxexpy = np.sqrt((1 + max_boost) / (1 - max_boost))
    P = np.zeros((2, 4)); X = np.zeros((2, 4))
    P[0, 1:] = p1; P[1, 1:] = p2
    P[0, 0] = np.sqrt(m * m + p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    P[1, 0] = np.sqrt(m * m + p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2)
    qs = np.array([q1, q2])
    Q = np.zeros((2, qcap, 4))
    head = np.zeros(2, np.int64); cnt = np.zeros(2, np.int64)
    borrowed = np.zeros((2, 4))
    first_step = np.array([False, True])
    # first string vector (Athena InfracolorForce::StartTracking)
    u0 = P[0] / m; u1 = P[1] / m
    dot = mdot(u1[0], u1[1], u1[2], u1[3], u0[0], u0[1], u0[2], u0[3])
    s0 = u0 - u1 * (dot - np.sqrt(dot * dot - 1))
    s0 = s0 * (first_length / s0[0])
    s0[0] = np.sqrt(s0[1] ** 2 + s0[2] ** 2 + s0[3] ** 2)
    Q[1, 0] = s0; cnt[1] = 1
    hits = np.zeros((max_hits, 9)); nh = 0
    ncnt = np.zeros((2, rec_radii.shape[0]))
    eacc = np.zeros(2)
    kicked = False
    nsteps = 0; maxq = 1
    status = 0
    k = 1
    nalt = 0
    s = np.zeros(4); a = np.zeros(4); sout = np.zeros(4); dx = np.zeros(4); pn = np.zeros(4)
    while True:
        if nsteps >= max_steps:
            status = 3
            break
        if X[0, 0] > t_end and X[1, 0] > t_end:
            status = 0
            break
        if cnt[k] == 0:
            k = 1 - k
            if cnt[k] == 0:
                status = 4
                break
            continue
        while cnt[k] > 0 and nsteps < max_steps and X[k, 0] <= t_end:
            hidx = head[k] % qcap
            sin = Q[k, hidx]
            p = P[k]
            tmp = 2 * F * mdot(sin[0], sin[1], sin[2], sin[3], p[0], p[1], p[2], p[3]) / (m * m)
            frac = 1.0
            if tmp > maxexpy - 1:
                frac = (maxexpy - 1) / tmp
            r_k = np.sqrt(X[k, 1] ** 2 + X[k, 2] ** 2)
            hmax = hmax_trk if (r_k < 120.0 and abs(X[k, 3]) < 300.0) else hmax_out
            if sin[0] * frac > hmax:
                frac = hmax / sin[0]
            for c in range(4):
                s[c] = sin[c] * frac
                a[c] = p[c] + F * s[c]
            sa = mdot(s[0], s[1], s[2], s[3], a[0], a[1], a[2], a[3])
            aa = mdot(a[0], a[1], a[2], a[3], a[0], a[1], a[2], a[3])
            for c in range(4):
                sout[c] = 2 * sa / aa * a[c] - s[c]
                dx[c] = s[c] + sout[c]
                pn[c] = p[c] + F * (s[c] - sout[c])
            qk = qs[k]
            if qk != 0.0 and (B0 != 0.0 or bmode == 2):
                xm = X[k, 1] + 0.5 * dx[1]; ym = X[k, 2] + 0.5 * dx[2]; zm = X[k, 3] + 0.5 * dx[3]
                bx, by, bz = bfield(xm, ym, zm, bmode, B0, bgrid, rgrid, zgrid)
                cc = qk * EB_GEV_PER_CM_PER_T
                pn[1] += cc * (dx[2] * bz - dx[3] * by)
                pn[2] += cc * (dx[3] * bx - dx[1] * bz)
                pn[3] += cc * (dx[1] * by - dx[2] * bx)
            nrm = m / np.sqrt(mdot(pn[0], pn[1], pn[2], pn[3], pn[0], pn[1], pn[2], pn[3]))
            for c in range(4):
                pn[c] *= nrm
            # hit recording (linear interpolation on the chord)
            ra = np.sqrt(X[k, 1] ** 2 + X[k, 2] ** 2)
            xb = X[k, 1] + dx[1]; yb = X[k, 2] + dx[2]
            rb = np.sqrt(xb * xb + yb * yb)
            for L in range(rec_radii.shape[0]):
                R = rec_radii[L]
                if (ra - R) * (rb - R) < 0.0:
                    # solve |x0 + f dx|_T = R exactly on the chord
                    A2 = dx[1] ** 2 + dx[2] ** 2
                    B2 = 2 * (X[k, 1] * dx[1] + X[k, 2] * dx[2])
                    C2 = ra * ra - R * R
                    disc = max(B2 * B2 - 4 * A2 * C2, 0.0)
                    f1 = (-B2 + np.sqrt(disc)) / (2 * A2); f2 = (-B2 - np.sqrt(disc)) / (2 * A2)
                    f = f1 if (f1 >= 0 and f1 <= 1) else f2
                    zc = X[k, 3] + f * dx[3]
                    if abs(zc) < rec_zmax[L] and nh < max_hits:
                        ncnt[k, L] += 1
                        hits[nh, 0] = k; hits[nh, 1] = L; hits[nh, 2] = X[k, 0] + f * dx[0]
                        hits[nh, 3] = X[k, 1] + f * dx[1]; hits[nh, 4] = X[k, 2] + f * dx[2]; hits[nh, 5] = zc
                        pp = np.sqrt(pn[1] ** 2 + pn[2] ** 2 + pn[3] ** 2)
                        hits[nh, 6] = pp / pn[0]; hits[nh, 7] = pp; hits[nh, 8] = ncnt[k, L]
                        nh += 1
                    if kick_k == k and (not kicked) and R == kick_R:
                        kicked = True
                        for c in range(3):
                            pn[c + 1] += kick_dp[c]
                        pn[0] = np.sqrt(m * m + pn[1] ** 2 + pn[2] ** 2 + pn[3] ** 2)
            for c in range(4):
                X[k, c] += dx[c]
                P[k, c] = pn[c]
            if do_eloss or do_ms:
                dsx = np.sqrt(dx[1] ** 2 + dx[2] ** 2 + dx[3] ** 2)
                _material_kick(P, X, k, m, qk, dsx, slabs, regions, mat, do_eloss, do_strag, do_ms, eacc)
            # pop / partial consumption
            if frac >= 1.0:
                head[k] += 1; cnt[k] -= 1
            else:
                for c in range(4):
                    Q[k, hidx, c] = sin[c] * (1 - frac)
            if first_step[k]:
                for c in range(4):
                    borrowed[1 - k, c] += s[c]
                if frac >= 1.0:
                    first_step[k] = False
            j = 1 - k
            v0 = sout[0]; scale = 1.0
            if borrowed[j, 0] > 0:
                if borrowed[j, 0] <= v0:
                    scale = 1 - borrowed[j, 0] / v0
                    for c in range(4):
                        borrowed[j, c] = 0.0
                else:
                    f_ = 1 - v0 / borrowed[j, 0]
                    for c in range(4):
                        borrowed[j, c] *= f_
                    scale = 0.0
            if scale * v0 > 0:
                if cnt[j] >= qcap:
                    status = 5
                    return status, hits[:nh].copy(), X, P, eacc, nsteps, maxq
                tidx = (head[j] + cnt[j]) % qcap
                for c in range(4):
                    Q[j, tidx, c] = sout[c] * scale
                cnt[j] += 1
                if cnt[j] > maxq:
                    maxq = cnt[j]
            nsteps += 1
        k = 1 - k
        # termination checks (after each alternation)
        r1 = np.sqrt(X[0, 1] ** 2 + X[0, 2] ** 2); r2 = np.sqrt(X[1, 1] ** 2 + X[1, 2] ** 2)
        if (r1 > r_exit or abs(X[0, 3]) > z_exit) and (r2 > r_exit or abs(X[1, 3]) > z_exit):
            status = 1
            break
        nalt += 1
        if beta_stop > 0.0 and (nalt % 16) == 0:
            # total 4-momentum = quirks + string (F x queued null vectors); the quirks alone are not enough
            Pt = P[0] + P[1]
            for jj in range(2):
                for ii in range(cnt[jj]):
                    idx2 = (head[jj] + ii) % qcap
                    for c in range(4):
                        Pt[c] += F * Q[jj, idx2, c]
            if np.sqrt(Pt[1] ** 2 + Pt[2] ** 2 + Pt[3] ** 2) / Pt[0] < beta_stop:
                status = 2
                break
    return status, hits[:nh].copy(), X, P, eacc, nsteps, maxq


def run_causal(p1, p2, m, lam_keV, B0=3.8112, bmode=0, material=True, ms=True, eloss=True, strag=True,
               slabs=None, regions=None, t_end=None, r_exit=118.0, z_exit=290.0, beta_stop=0.0, max_boost=1e-2,
               hmax_trk=0.2, hmax_out=2.0, first_length=1e-7, seed=1, charges=(1.0, -1.0), grid=None,
               max_hits=400000, max_steps=400_000_000, qcap=1 << 16, rec_radii=REC_RADII, rec_zmax=REC_ZMAX,
               kick=None, _swapped=False):
    sig = sigma_from_lambda_keV(lam_keV)
    slabs = phase2_tracker() if slabs is None else slabs
    regions = cms_outer_regions() if regions is None else regions
    grid = DUMMY_GRID if grid is None else grid
    p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
    if t_end is None:
        P = p1 + p2
        E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
        t_end = 1.3 * r_exit / max(np.hypot(P[0], P[1]) / E, 0.02) + 50.0
    kk, kR, kdp = (-1, 0.0, np.zeros(3)) if kick is None else (int(kick[0]), float(kick[1]), np.asarray(kick[2], float))
    out = causal_propagate(p1, p2, float(m), sig, float(charges[0]), float(charges[1]), int(bmode), float(B0),
                           grid[0], grid[1], grid[2], slabs, regions, MAT, np.asarray(rec_radii, float),
                           np.asarray(rec_zmax, float), bool(material and eloss), bool(material and strag),
                           bool(material and ms), float(t_end), float(r_exit), float(z_exit), float(beta_stop),
                           float(max_boost), float(hmax_trk), float(hmax_out), float(first_length), int(seed),
                           int(max_hits), int(max_steps), int(qcap), kk, kR, kdp)
    status, hits, X, P, eacc, nsteps, maxq = out
    if status == 4 and nsteps < 1000 and not _swapped:
        # bootstrap deadlock (the first reflected vector is shorter than the borrowed one): give the first
        # string vector to the other quirk by swapping the labels, then swap back
        kk2 = None if kick is None else (1 - int(kick[0]), kick[1], kick[2])
        r = run_causal(p2, p1, m, lam_keV, B0, bmode, material, ms, eloss, strag, slabs, regions, t_end, r_exit,
                       z_exit, beta_stop, max_boost, hmax_trk, hmax_out, first_length, seed, (charges[1], charges[0]),
                       grid, max_hits, max_steps, qcap, rec_radii, rec_zmax, kk2, _swapped=True)
        h = r['hits'].copy()
        if len(h):
            h[:, 0] = 1 - h[:, 0]
        r.update(hits=h, X=r['X'][::-1].copy(), P=r['P'][::-1].copy(), eacc=r['eacc'][::-1].copy())
        return r
    return dict(status=status, hits=hits, X=X, P=P, eacc=eacc, nsteps=nsteps, maxq=maxq)


if __name__ == '__main__':
    ok = True
    m = 500.0
    p1 = np.array([200.0, 300.0, 30.0]); p2 = np.array([-100.0, 280.0, -20.0])
    # 1. vacuum vs exact (positions at the recorded hits)
    for lam in (0.3, 1.0, 3.0):
        r = run_causal(p1, p2, m, lam, B0=0.0, material=False)
        ex = ExactPair(p1, p2, m, m, sigma_from_lambda_keV(lam))
        H = r['hits']; err = 0
        for h in H:
            X1, X2 = ex.lab_positions([h[2]])
            err = max(err, np.linalg.norm((X1, X2)[int(h[0])][0] - h[3:6]))
        good = err < 5e-4   # linear chord interpolation, step <= hmax = 0.2 cm (in-plane error)
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] causal vacuum hits vs ExactPair Lambda={lam}: max|dx| = {err*1e4:.3g} um, "
              f"{len(H)} hits, {r['nsteps']} steps, max queue {r['maxq']}", flush=True)
    # 2. uniform B vs T2 CausalNullString (same algorithm, Python) on T2's own event set
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from T2_string_methods_B import make_event, hits_from
    rng = np.random.default_rng(7)
    events = [make_event(rng, m) for _ in range(4)]
    for lam in (0.6, 2.0):
        for ie, (q1v, q2v, bT) in enumerate(events[:2]):
            t_end = 112.0 / max(bT, 1e-3) + 20
            tic = time.time()
            traj, mom = CausalNullString(m, sigma_from_lambda_keV(lam), Bfield=np.array([0, 0, 3.8]), max_boost=1e-2,
                                         first_length=1e-9).run(q1v, q2v, t_end)
            t2 = time.time() - tic
            hh = []
            for T in traj:
                hh += [h[2] for h in hits_from(T[:, 0], T[:, 1:])]
            d2 = plane_fit(np.array(hh))[0]
            tic = time.time()
            r = run_causal(q1v, q2v, m, lam, B0=3.8, material=False, t_end=t_end, r_exit=1e9, z_exit=1e9,
                           first_length=1e-9, hmax_trk=1e9, hmax_out=1e9,
                           rec_radii=REC_RADII[:10], rec_zmax=np.full(10, 1e9))
            t3 = time.time() - tic
            d3 = plane_fit(r['hits'][:, 3:6])[0]
            good = abs(d3 / d2 - 1) < 0.05
            ok &= good
            print(f"[{'PASS' if good else 'FAIL'}] causal 3.8 T, T3 numba vs T2 python, Lambda={lam} ev{ie}: d = {d3*1e4:.3g} vs "
                  f"{d2*1e4:.3g} um; time {t3:.2f} vs {t2:.1f} s", flush=True)
            r2 = run_causal(q1v, q2v, m, lam, B0=3.8, material=False, t_end=t_end, r_exit=1e9, z_exit=1e9,
                            rec_radii=REC_RADII[:10], rec_zmax=np.full(10, 1e9), max_boost=1e-3, hmax_trk=0.05)
            print(f"      convergence: max_boost 1e-3, hmax 0.05 cm: d = {plane_fit(r2['hits'][:, 3:6])[0]*1e4:.3g} um "
                  f"({r2['nsteps']} steps, max queue {r2['maxq']})", flush=True)
    print('ALL PASS' if ok else 'SOME FAILURES')
