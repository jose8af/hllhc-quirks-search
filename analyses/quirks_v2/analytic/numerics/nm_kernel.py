"""nm_kernel.py -- E2 (Stage 1 numerics): instrumented copy of the causal null-vector Nambu-Goto propagator.

Purpose: per-crossing diagnostics need the full endpoint world lines and the absorbed null vectors.  This file is a
line-by-line copy of code/T3_causal.causal_propagate (Athena/T2 algorithm: first string vector, borrowing,
max-boost splitting, first-order field kick + mass-shell renormalisation, step cap hmax, hit recording) with
material REMOVED (B-only studies) and three additions:
  * uniform electric field E (GeV/cm per unit charge): kick dp^0 += q E.dx, dp_vec += q E dx^0, before the same
    mass-shell renormalisation as the B kick (used for CM-frame single-crossing experiments, M2b);
  * optional initial endpoint positions and initial queues (static straight string of length d between the ends:
    Q1 = (d/2)(1, -e), Q2 = (d/2)(1, +e) for x1 - x2 = d e; queue vectors point from the owner to the partner);
  * selective record of steps (dense near crossings, log-spaced in separation elsewhere, see kernel docstring):
    X^4 and P^4 before the step, absorbed null vector s^4, cumulative string impulse J^4 = sum F(s - s_out).
    (P after a step equals P before the next step of the same quirk: nothing else acts between them.)
Validation (run this file): with E = 0 and default initial data the hits are bit-identical to
T3_causal.run_causal(material=False).
Inputs: none (library).  Run checks:  pixi run python analytic/numerics/nm_kernel.py   (from theory_track/)
Units: cm, GeV, c = 1; B in tesla.
"""
import os, sys
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, '..', '..', 'code')
sys.path.insert(0, CODE)
from T2_propagator import sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T  # noqa: E402
from T3_propagator import REC_RADII, REC_ZMAX  # noqa: E402

B_CMS = 3.8112


@njit(cache=True, inline='always')
def mdot(a0, a1, a2, a3, b0, b1, b2, b3):
    return a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3


@njit(cache=True)
def kernel(p1, p2, m, F, q1, q2, B0, Bxy, Evec, x1_0, x2_0, init_mode, d_init, e_init,
           rec_radii, rec_zmax, t_end, r_exit, z_exit, max_boost, hmax_trk, hmax_out, first_length,
           max_hits, max_steps, qcap, do_rec, max_rec, rec_near, rec_dlog, rec_dt):
    """Uniform B = (Bxy[0], Bxy[1], B0) [T] and E = Evec [GeV/cm per unit charge] (Bxy = 0 reproduces T3_causal bit by bit).
    init_mode 0: Athena bootstrap (both ends at x1_0 = x2_0 = 0 required); 1: static straight string of length
    d_init along e_init between x1_0 and x2_0 (x1_0 - x2_0 = d_init e_init).
    Record (do_rec): a step of quirk k is stored (state BEFORE the step) if
      (a) lab separation |x_k - x_j| (current positions) < rec_near * (s0_k + s0_j_last)  [dense near crossings], or
      (b) |ln(sep / sep_at_last_record_k)| > rec_dlog                                   [log sampling], or
      (c) t_k - t_at_last_record_k > rec_dt                                             [turning points];
    row = [X^4, P^4, s^4 (absorbed piece), J^4 (cumulative string impulse F(s - s_out) on k, before the step)].
    Returns (status, hits[n,9], X, P, nsteps, maxq, rec0[n0,16], rec1[n1,16])."""
    maxexpy = np.sqrt((1 + max_boost) / (1 - max_boost))
    P = np.zeros((2, 4)); X = np.zeros((2, 4))
    P[0, 1:] = p1; P[1, 1:] = p2
    P[0, 0] = np.sqrt(m * m + p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    P[1, 0] = np.sqrt(m * m + p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2)
    for c in range(3):
        X[0, c + 1] = x1_0[c]; X[1, c + 1] = x2_0[c]
    qs = np.array([q1, q2])
    Q = np.zeros((2, qcap, 4))
    head = np.zeros(2, np.int64); cnt = np.zeros(2, np.int64)
    borrowed = np.zeros((2, 4))
    if init_mode == 0:
        first_step = np.array([False, True])
        u0 = P[0] / m; u1 = P[1] / m
        dot = mdot(u1[0], u1[1], u1[2], u1[3], u0[0], u0[1], u0[2], u0[3])
        s0 = u0 - u1 * (dot - np.sqrt(dot * dot - 1))
        s0 = s0 * (first_length / s0[0])
        s0[0] = np.sqrt(s0[1] ** 2 + s0[2] ** 2 + s0[3] ** 2)
        Q[1, 0] = s0; cnt[1] = 1
    else:
        first_step = np.array([False, False])
        Q[0, 0, 0] = 0.5 * d_init; Q[1, 0, 0] = 0.5 * d_init
        for c in range(3):
            Q[0, 0, c + 1] = -0.5 * d_init * e_init[c]
            Q[1, 0, c + 1] = 0.5 * d_init * e_init[c]
        cnt[0] = 1; cnt[1] = 1
    hits = np.zeros((max_hits, 9)); nh = 0
    ncnt = np.zeros((2, rec_radii.shape[0]))
    nr = max_rec if do_rec else 1
    rec0 = np.zeros((nr, 16)); rec1 = np.zeros((nr, 16)); nr0 = 0; nr1 = 0
    J = np.zeros((2, 4)); lsep = np.full(2, -1.0); lt = np.full(2, -1e300); ls0 = np.zeros(2)
    nsteps = 0; maxq = 1
    status = 0
    k = 1
    hasE = (Evec[0] != 0.0) or (Evec[1] != 0.0) or (Evec[2] != 0.0)
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
            if do_rec:
                jq = 1 - k
                sep = np.sqrt((X[k, 1] - X[jq, 1]) ** 2 + (X[k, 2] - X[jq, 2]) ** 2 + (X[k, 3] - X[jq, 3]) ** 2)
                want = sep < rec_near * (s[0] + ls0[jq]) or lsep[k] < 0.0 or X[k, 0] - lt[k] > rec_dt
                if not want and sep > 0.0:
                    want = abs(np.log(sep / lsep[k])) > rec_dlog
                ls0[k] = s[0]
                if want:
                    lsep[k] = sep if sep > 0.0 else 1e-300
                    lt[k] = X[k, 0]
                    if k == 0:
                        if nr0 < max_rec:
                            for c in range(4):
                                rec0[nr0, c] = X[0, c]; rec0[nr0, 4 + c] = p[c]; rec0[nr0, 8 + c] = s[c]
                                rec0[nr0, 12 + c] = J[0, c]
                            nr0 += 1
                        else:
                            status = 6
                    else:
                        if nr1 < max_rec:
                            for c in range(4):
                                rec1[nr1, c] = X[1, c]; rec1[nr1, 4 + c] = p[c]; rec1[nr1, 8 + c] = s[c]
                                rec1[nr1, 12 + c] = J[1, c]
                            nr1 += 1
                        else:
                            status = 6
            sa = mdot(s[0], s[1], s[2], s[3], a[0], a[1], a[2], a[3])
            aa = mdot(a[0], a[1], a[2], a[3], a[0], a[1], a[2], a[3])
            for c in range(4):
                sout[c] = 2 * sa / aa * a[c] - s[c]
                dx[c] = s[c] + sout[c]
                pn[c] = p[c] + F * (s[c] - sout[c])
                J[k, c] += F * (s[c] - sout[c])
            qk = qs[k]
            if qk != 0.0 and (B0 != 0.0 or Bxy[0] != 0.0 or Bxy[1] != 0.0):
                bz = B0; bx = Bxy[0]; by = Bxy[1]
                cc = qk * EB_GEV_PER_CM_PER_T
                # uniform B (bx = by = 0.0 gives the identical arithmetic of T3_causal for bmode 0)
                pn[1] += cc * (dx[2] * bz - dx[3] * by)
                pn[2] += cc * (dx[3] * bx - dx[1] * bz)
                pn[3] += cc * (dx[1] * by - dx[2] * bx)
            if qk != 0.0 and hasE:
                pn[0] += qk * (Evec[0] * dx[1] + Evec[1] * dx[2] + Evec[2] * dx[3])
                pn[1] += qk * Evec[0] * dx[0]
                pn[2] += qk * Evec[1] * dx[0]
                pn[3] += qk * Evec[2] * dx[0]
            nrm = m / np.sqrt(mdot(pn[0], pn[1], pn[2], pn[3], pn[0], pn[1], pn[2], pn[3]))
            for c in range(4):
                pn[c] *= nrm
            ra = np.sqrt(X[k, 1] ** 2 + X[k, 2] ** 2)
            xb = X[k, 1] + dx[1]; yb = X[k, 2] + dx[2]
            rb = np.sqrt(xb * xb + yb * yb)
            for L in range(rec_radii.shape[0]):
                R = rec_radii[L]
                if (ra - R) * (rb - R) < 0.0:
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
            for c in range(4):
                X[k, c] += dx[c]
                P[k, c] = pn[c]
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
                    return status, hits[:nh].copy(), X, P, nsteps, maxq, rec0[:nr0].copy(), rec1[:nr1].copy()
                tidx = (head[j] + cnt[j]) % qcap
                for c in range(4):
                    Q[j, tidx, c] = sout[c] * scale
                cnt[j] += 1
                if cnt[j] > maxq:
                    maxq = cnt[j]
            nsteps += 1
        k = 1 - k
        r1 = np.sqrt(X[0, 1] ** 2 + X[0, 2] ** 2); r2 = np.sqrt(X[1, 1] ** 2 + X[1, 2] ** 2)
        if (r1 > r_exit or abs(X[0, 3]) > z_exit) and (r2 > r_exit or abs(X[1, 3]) > z_exit):
            status = 1 if status == 0 else status
            break
    return status, hits[:nh].copy(), X, P, nsteps, maxq, rec0[:nr0].copy(), rec1[:nr1].copy()


def run(p1, p2, m, lam_keV=None, sigma=None, B0=B_CMS, Bxy=(0.0, 0.0), E=(0.0, 0.0, 0.0), x1_0=(0, 0, 0), x2_0=(0, 0, 0),
        d_init=0.0, e_init=(1.0, 0, 0), t_end=None, r_exit=118.0, z_exit=290.0, max_boost=1e-2, hmax_trk=0.2,
        hmax_out=2.0, first_length=1e-7, charges=(1.0, -1.0), rec=False, max_rec=4_000_000, rec_near=8.0, rec_dlog=0.05, rec_dt=1e30, max_hits=400000,
        max_steps=400_000_000, qcap=1 << 16, rec_radii=REC_RADII, rec_zmax=REC_ZMAX, _swapped=False):
    sig = sigma_from_lambda_keV(lam_keV) if sigma is None else float(sigma)
    p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
    if t_end is None:
        P = p1 + p2
        Etot = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
        t_end = 1.3 * r_exit / max(np.hypot(P[0], P[1]) / Etot, 0.02) + 50.0
    init_mode = 1 if d_init > 0 else 0
    out = kernel(p1, p2, float(m), sig, float(charges[0]), float(charges[1]), float(B0), np.asarray(Bxy, float), np.asarray(E, float),
                 np.asarray(x1_0, float), np.asarray(x2_0, float), init_mode, float(d_init),
                 np.asarray(e_init, float), np.asarray(rec_radii, float), np.asarray(rec_zmax, float),
                 float(t_end), float(r_exit), float(z_exit), float(max_boost), float(hmax_trk), float(hmax_out),
                 float(first_length), int(max_hits), int(max_steps), int(qcap), bool(rec), int(max_rec), float(rec_near),
                 float(rec_dlog), float(rec_dt))
    status, hits, X, P, nsteps, maxq, r0, r1 = out
    if status == 4 and nsteps < 1000 and not _swapped and init_mode == 0:
        # same bootstrap-deadlock fix as T3_causal.run_causal: swap labels, then swap back
        r = run(p2, p1, m, lam_keV, sigma, B0, Bxy, E, x2_0, x1_0, d_init, e_init, t_end, r_exit, z_exit, max_boost,
                hmax_trk, hmax_out, first_length, (charges[1], charges[0]), rec, max_rec, rec_near, rec_dlog, rec_dt,
                max_hits, max_steps, qcap, rec_radii, rec_zmax, _swapped=True)
        h = r['hits'].copy()
        if len(h):
            h[:, 0] = 1 - h[:, 0]
        r.update(hits=h, X=r['X'][::-1].copy(), P=r['P'][::-1].copy(), rec=(r['rec'][1], r['rec'][0]))
        return r
    return dict(status=status, hits=hits, X=X, P=P, nsteps=nsteps, maxq=maxq, rec=(r0, r1), sigma=sig)


if __name__ == '__main__':
    import time
    from T3_causal import run_causal
    from T3_propagator import sample_events
    ok = True
    rng = np.random.default_rng(5)
    evs = sample_events(500.0, 3, rng=rng, eta_max=1.0)
    for lam in (0.6, 1.0, 3.0):
        for (p1, p2, info) in evs:
            t0 = time.time()
            a = run_causal(p1, p2, 500.0, lam, B0=B_CMS, material=False)
            t1 = time.time()
            b = run(p1, p2, 500.0, lam, rec=True, rec_dt=1.0)
            t2 = time.time()
            same = a['hits'].shape == b['hits'].shape and np.array_equal(a['hits'], b['hits'])
            ok &= same
            print(f"[{'PASS' if same else 'FAIL'}] Lambda={lam}: hits bit-identical to T3_causal "
                  f"({len(b['hits'])} hits, {b['nsteps']} steps, rec {len(b['rec'][0])}+{len(b['rec'][1])}; "
                  f"{t1-t0:.2f} s vs {t2-t1:.2f} s)", flush=True)
    print('ALL PASS' if ok else 'SOME FAILURES')
