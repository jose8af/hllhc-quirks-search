"""T3_causal_s3.py -- Stage-3 versioned copy of code/T3_causal.py (causal null-vector Nambu-Goto quirk-string propagator
with B field and material).  KERNEL_VERSION "s3.2" (s3.1 + candidate-surface binary search in the recorder: a pure
speed change, hits identical to s3.1 by construction and checked on the V2b outputs; s3.1 cost 2.1x per step).  E7 (executor), 2026-10-11, plan sim/stage3/plan.md §4.1.

Derived from code/T3_causal.py (md5 c09c84a441b5195c27c7172acb8aac68) with the material/field helpers of
code/T3_propagator.py (md5 2328bb685c1dbae8cc3c5122011c16f2) and two constants of code/T2_propagator.py
(md5 fdacaeba505d28be593d54b291a4946d) COPIED here, so the file is self-contained (the Windows bundle ships no other
theory-track code).  code/T3_causal.py is not modified.  The step map, borrowing, max-boost splitting, B kick +
mass-shell renormalisation, Bethe loss, Bohr straggling and Highland MS arithmetic are copied unchanged.

Changes (plan §4.1 items 1-7; nothing else):
  1. generic recording surfaces: cylinders (R, zmin, zmax) and discs (z, rmin, rmax); EVERY root of a chord in [0, 1)
     is recorded (two roots when a chord dips across a cylinder; one per disc);
  2. per hit: quirk, surface id, crossing index on that surface, t, x, y, z, the 4-momentum at the crossing (3-momentum
     linearly interpolated between the pre- and post-chord momenta, E on shell) and the chord length;
  3. an initial vertex (x, y, z, t): both endpoints start there; t_end is shifted by t0 (the null-vector string
     bootstrap does not depend on position);
  4. endcap-disc material slabs (TFPX/TEPX/TEDD; `dslabs`, from surfaces_s3.json), same Si model as the barrel slabs;
  5. vacuum fast path in the material kick: material_at is evaluated FIRST and the kick returns at once in vacuum
     (pure function, no state change in that case, so bit-identical by construction; probe p5 measured x1.18-1.24);
  6. defaults (non-legacy) qcap = 2^19, max_steps = 2e10, z_exit = 293 cm (so the ETL proxy at |z| = 292 cm is
     reachable; still inside the tracker volume, which ends at 293.5 cm); BTL and ETL proxy surfaces;
  7. legacy=True: barrel REC_RADII, one root per chord, vertex at 0, no disc material and the original defaults ->
     must reproduce code/T3_causal.run_causal BIT FOR BIT (validation V1, sim/stage3/validation/val_v1.py).
Units inside: cm, GeV, c = 1 (time in cm).  The runner converts hits to mm / ns / GeV.
Library; checks: sim/stage3/validation/val_v1.py.
"""
import json
import math
from pathlib import Path

import numpy as np
from numba import njit

KERNEL_VERSION = 's3.2'
ORIG_MD5 = {'code/T3_causal.py': 'c09c84a441b5195c27c7172acb8aac68',
            'code/T3_propagator.py': '2328bb685c1dbae8cc3c5122011c16f2',
            'code/T2_propagator.py': 'fdacaeba505d28be593d54b291a4946d'}
HERE = Path(__file__).resolve().parent

# ---- copied from code/T2_propagator.py -------------------------------------------------------------------------
HBARC_GEV_CM = 1.973269804e-14
C_CM_PER_NS = 29.9792458
EB_GEV_PER_CM_PER_T = 2.99792458e-3   # e * c * 1 T in GeV/cm


def sigma_from_lambda_keV(lam_keV: float) -> float:
    """String tension sigma = Lambda^2 in GeV/cm for Lambda in keV."""
    return (lam_keV * 1e-6) ** 2 / HBARC_GEV_CM


# ---- copied from code/T3_propagator.py -------------------------------------------------------------------------
ME = 0.51099895e-3          # GeV
KBB = 0.307075e-3            # GeV cm^2 / mol  (PDG K)
MAT = np.array([
    [0.0,     1.0e-7,  1e30,    0.0],
    [0.49848, 173e-9,  9.370,   2.329],
    [0.41315, 600.7e-9, 0.8903, 8.300],
    [0.45636, 322e-9,  1.436,   8.960],
    [0.46557, 286e-9,  1.757,   7.874],
    [0.49919, 85.7e-9, 30390.,  0.0012],
])


def phase2_tracker(scale=1.0, it_layers=(3.0, 6.1, 10.4, 14.6), ot_layers=(24.9, 37.2, 52.3, 68.8, 86.0, 108.3)):
    """Thin cylindrical slabs: R [cm], x/X0 (normal incidence), radial width w [cm], |z| half-length [cm], is_sensor."""
    rows = [[2.2, 0.0023, 0.1, 300.0, 0]]
    for R in it_layers:
        rows.append([R, 0.012, 1.0, 20.0, 1])
    rows.append([19.0, 0.010, 1.0, 120.0, 0])
    for R in ot_layers[:3]:
        rows.append([R, 0.025, 2.0, 120.0, 1])
    for R in ot_layers[3:]:
        rows.append([R, 0.018, 2.0, 120.0, 1])
    a = np.array(rows, float)
    a[:, 1] *= scale
    return a


def cms_outer_regions():
    R = [
        [118.5, 181.1, 0.0, 293.5, 2, 0.33, 0],
        [0.0, 181.1, 293.5, 390.0, 2, 0.33, 1],
        [181.1, 286.4, 0.0, 568.0, 3, 0.68, 0],
        [0.0, 286.4, 390.0, 568.0, 3, 0.68, 1],
        [295.0, 380.0, 0.0, 645.0, 4, 0.5, 0],
        [380.0, 410.0, 0.0, 140.0, 4, 1.0, 0],
        [455.0, 490.5, 0.0, 724.0, 4, 1.0, 0],
        [528.5, 597.5, 0.0, 661.0, 4, 1.0, 0],
        [635.5, 700.0, 0.0, 661.0, 4, 1.0, 0],
        [0.0, 105.0, 568.0, 630.0, 4, 1.0, 1],
        [0.0, 270.0, 630.0, 724.0, 4, 1.0, 1],
        [0.0, 695.5, 724.0, 791.5, 4, 1.0, 1],
        [0.0, 129.0, 791.5, 849.5, 4, 1.0, 1],
        [0.0, 695.5, 849.5, 917.0, 4, 1.0, 1],
        [0.0, 140.0, 917.0, 975.0, 4, 1.0, 1],
        [0.0, 695.5, 975.0, 1005.0, 4, 1.0, 1],
        [0.0, 150.0, 1005.0, 1063.0, 4, 1.0, 1],
        [0.0, 695.5, 1063.0, 1083.0, 4, 1.0, 1],
    ]
    return np.array(R, float)


DUMMY_GRID = (np.zeros((2, 2, 2)), np.array([0.0, 1.0]), np.array([0.0, 1.0]))
REC_RADII = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3, 114.8, 129.0])
REC_ZMAX = np.array([20.0] * 4 + [120.0] * 6 + [130.0, 300.0])
NO_DSLABS = np.zeros((0, 5))


@njit(cache=True)
def stopping_power(beta, q2, za_rho, I):
    """Mean dE/dx [GeV/cm] (Bethe without density effect; L >= 0.6; linear in beta below 0.02)."""
    if za_rho <= 0.0:
        return 0.0
    bp = 0.02
    b = beta if beta > bp else bp
    g2 = 1.0 / (1.0 - b * b)
    L = np.log(2.0 * ME * b * b * g2 / I)
    if L < 0.6:
        L = 0.6
    s = KBB * za_rho * q2 / (b * b) * (L - b * b)
    if beta < bp:
        s *= beta / bp
    return s


@njit(cache=True)
def material_at_s3(x, y, z, slabs, dslabs, regions, mat):
    """As T3_propagator.material_at, plus endcap-disc slabs dslabs[k] = (zc>0, rmin, rmax, x/X0, w) applied at |z|.
    Returns (za_rho, I, X0_eff, layer_xX0, region id); region id 200+k for disc slab k."""
    r = np.sqrt(x * x + y * y)
    az = abs(z)
    if r < 118.5 and az < 293.5:
        for k in range(slabs.shape[0]):
            R = slabs[k, 0]; w = slabs[k, 2]
            if abs(r - R) < 0.5 * w and az < slabs[k, 3]:
                xX0 = slabs[k, 1]
                rho = mat[1, 3] * xX0 * mat[1, 2] / w
                return mat[1, 0] * rho, mat[1, 1], w / xX0, xX0, 100 + k
        for k in range(dslabs.shape[0]):
            w = dslabs[k, 4]
            if abs(az - dslabs[k, 0]) < 0.5 * w and r >= dslabs[k, 1] and r < dslabs[k, 2]:
                xX0 = dslabs[k, 3]
                rho = mat[1, 3] * xX0 * mat[1, 2] / w
                return mat[1, 0] * rho, mat[1, 1], w / xX0, xX0, 200 + k
        return 0.0, 1.0, 1e30, 1.0, -1
    for j in range(regions.shape[0]):
        rmin = regions[j, 0]
        if regions[j, 6] > 0.5:
            rmin = az / np.sinh(3.0)
        if r >= rmin and r < regions[j, 1] and az >= regions[j, 2] and az < regions[j, 3]:
            mc = int(regions[j, 4]); zeta = regions[j, 5]
            return mat[mc, 0] * mat[mc, 3] * zeta, mat[mc, 1], mat[mc, 2] / zeta, 1.0, j
    return mat[5, 0] * mat[5, 3], mat[5, 1], mat[5, 2], 1.0, -1


@njit(cache=True)
def bfield(x, y, z, bmode, B0, bgrid, rgrid, zgrid):
    """bmode 0: uniform B0 zhat; 1: simplified CMS; 2: (Br, Bz) map (copied unchanged from T3_propagator)."""
    if bmode == 0:
        return 0.0, 0.0, B0
    r = np.sqrt(x * x + y * y)
    az = abs(z)
    if bmode == 1:
        if r < 295.0 and az < 645.0:
            return 0.0, 0.0, B0
        if r >= 380.0 and r < 700.0 and az < 661.0:
            if (r < 410.0 and az < 140.0) or (r >= 455.0 and r < 490.5) or (r >= 528.5 and r < 597.5) or (r >= 635.5):
                return 0.0, 0.0, -1.8
        return 0.0, 0.0, 0.0
    nr = rgrid.shape[0]; nz = zgrid.shape[0]
    dr = rgrid[1] - rgrid[0]; dz = zgrid[1] - zgrid[0]
    fr = (r - rgrid[0]) / dr; fz = (az - zgrid[0]) / dz
    i = int(fr); j = int(fz)
    if i < 0: i = 0
    if j < 0: j = 0
    if i > nr - 2: i = nr - 2
    if j > nz - 2: j = nz - 2
    a = fr - i; b = fz - j
    br = (1 - a) * (1 - b) * bgrid[0, i, j] + a * (1 - b) * bgrid[0, i + 1, j] + (1 - a) * b * bgrid[0, i, j + 1] + a * b * bgrid[0, i + 1, j + 1]
    bz = (1 - a) * (1 - b) * bgrid[1, i, j] + a * (1 - b) * bgrid[1, i + 1, j] + (1 - a) * b * bgrid[1, i, j + 1] + a * b * bgrid[1, i + 1, j + 1]
    if z < 0:
        br = -br
    if r > 0:
        return br * x / r, br * y / r, bz
    return 0.0, 0.0, bz


# ---- kernel (from code/T3_causal.py) ---------------------------------------------------------------------------
@njit(cache=True, inline='always')
def mdot(a0, a1, a2, a3, b0, b1, b2, b3):
    return a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3


@njit(cache=True)
def _material_kick_s3(P, X, k, m, q, dsx, slabs, dslabs, regions, mat, do_eloss, do_strag, do_ms, eacc):
    """Apply energy loss / MS to 4-momentum P[k] for a path dsx at the endpoint position X[k].
    s3: material_at first (vacuum fast path, item 5); the arithmetic below is unchanged."""
    za_rho, I, X0, xlay, reg = material_at_s3(X[k, 1], X[k, 2], X[k, 3], slabs, dslabs, regions, mat)
    if za_rho <= 0.0:
        return
    px = P[k, 1]; py = P[k, 2]; pz = P[k, 3]
    p = np.sqrt(px * px + py * py + pz * pz)
    if p <= 0.0 or dsx <= 0.0:
        return
    E = np.sqrt(m * m + p * p)
    beta = p / E
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
def causal_propagate_s3(p1, p2, x0, m, F, q1, q2, bmode, B0, bgrid, rgrid, zgrid, slabs, dslabs, regions, mat,
                        rec_mode, rec_radii, rec_zmax, surf, cR, cI, dZ, dI, do_eloss, do_strag, do_ms, t_end, r_exit, z_exit,
                        beta_stop, max_boost, hmax_trk, hmax_out, first_length, seed, max_hits, max_steps, qcap,
                        kick_k, kick_R, kick_dp):
    """Returns (status, hits[n, 12], X[2,4], P[2,4], eacc[2], nsteps, max_queue).
    rec_mode 0 (legacy): hit columns 0-8 = [quirk, layer, t, x, y, z, beta, p, count] exactly as code/T3_causal.py
    (one root per chord on rec_radii, |z| < rec_zmax); columns 9-11 are zero.
    rec_mode 1 (s3): every root on the surfaces surf[i] = (type, p0, p1, p2) (type 0 cylinder (R, zmin, zmax), 1 disc
    (z, rmin, rmax)); columns [quirk, surf, icross, t, x, y, z, px, py, pz, E, chord length].
    cR/cI, dZ/dI: cylinder radii and disc z sorted ascending with their surface indices (s3.2 candidate search; the
    candidates of a chord are then processed in surface-table order, so the hits are identical to s3.1).
    x0 = initial vertex (t, x, y, z) of both endpoints.  kick_k >= 0: deterministic kick kick_dp to quirk kick_k at its
    first crossing of r = kick_R (legacy: when R == kick_R in the radius loop, as the original)."""
    if seed >= 0:
        np.random.seed(seed)
    maxexpy = np.sqrt((1 + max_boost) / (1 - max_boost))
    P = np.zeros((2, 4)); X = np.zeros((2, 4))
    for c in range(4):
        X[0, c] = x0[c]; X[1, c] = x0[c]
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
    hits = np.zeros((max_hits, 12)); nh = 0
    nsurf = rec_radii.shape[0] if rec_mode == 0 else surf.shape[0]
    ncnt = np.zeros((2, nsurf))
    eacc = np.zeros(2)
    kicked = False
    nsteps = 0; maxq = 1
    status = 0
    k = 1
    nalt = 0
    s = np.zeros(4); a = np.zeros(4); sout = np.zeros(4); dx = np.zeros(4); pn = np.zeros(4)
    cand = np.zeros(max(nsurf, 1), np.int64)
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
            if rec_mode == 0:
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
            else:
                za = X[k, 3]; zb = za + dx[3]
                A2 = dx[1] ** 2 + dx[2] ** 2
                B2 = 2 * (X[k, 1] * dx[1] + X[k, 2] * dx[2])
                # chord transverse radius range (quick rejection): minimum of |x0 + f dx|_T on [0, 1]
                rlo2 = min(ra * ra, rb * rb)
                if A2 > 0.0:
                    fs = -B2 / (2 * A2)
                    if fs > 0.0 and fs < 1.0:
                        xs = X[k, 1] + fs * dx[1]; ys = X[k, 2] + fs * dx[2]
                        r2s = xs * xs + ys * ys
                        if r2s < rlo2:
                            rlo2 = r2s
                rlo = np.sqrt(rlo2); rhi = max(ra, rb)
                zlo = min(za, zb); zhi = max(za, zb)
                # s3.2: candidate surfaces by binary search, then table order (identical hits to the s3.1 full loop)
                nc = 0
                jj = np.searchsorted(cR, rlo)
                while jj < cR.shape[0] and cR[jj] <= rhi:
                    cand[nc] = cI[jj]; nc += 1; jj += 1
                jj = np.searchsorted(dZ, zlo)
                while jj < dZ.shape[0] and dZ[jj] <= zhi:
                    cand[nc] = dI[jj]; nc += 1; jj += 1
                for i1 in range(1, nc):
                    v = cand[i1]; i2 = i1 - 1
                    while i2 >= 0 and cand[i2] > v:
                        cand[i2 + 1] = cand[i2]; i2 -= 1
                    cand[i2 + 1] = v
                dl = np.sqrt(dx[1] ** 2 + dx[2] ** 2 + dx[3] ** 2) if nc > 0 else 0.0
                for ic in range(nc):
                    L = cand[ic]
                    if surf[L, 0] < 0.5:
                        R = surf[L, 1]
                        if R < rlo or R > rhi or A2 <= 0.0:
                            continue
                        C2 = ra * ra - R * R
                        disc = B2 * B2 - 4 * A2 * C2
                        if disc <= 0.0:
                            continue
                        sq = np.sqrt(disc)
                        qq = -0.5 * (B2 + sq) if B2 >= 0.0 else -0.5 * (B2 - sq)
                        fa = qq / A2
                        fb = C2 / qq if qq != 0.0 else fa
                        if fb < fa:
                            fa, fb = fb, fa
                        for ir in range(2):
                            f = fa if ir == 0 else fb
                            if f < 0.0 or f >= 1.0:
                                continue
                            zc = za + f * dx[3]
                            if zc <= surf[L, 2] or zc >= surf[L, 3] or nh >= max_hits:
                                continue
                            ncnt[k, L] += 1
                            hits[nh, 0] = k; hits[nh, 1] = L; hits[nh, 2] = ncnt[k, L]
                            hits[nh, 3] = X[k, 0] + f * dx[0]
                            hits[nh, 4] = X[k, 1] + f * dx[1]; hits[nh, 5] = X[k, 2] + f * dx[2]; hits[nh, 6] = zc
                            hpx = p[1] + f * (pn[1] - p[1]); hpy = p[2] + f * (pn[2] - p[2]); hpz = p[3] + f * (pn[3] - p[3])
                            hits[nh, 7] = hpx; hits[nh, 8] = hpy; hits[nh, 9] = hpz
                            hits[nh, 10] = np.sqrt(m * m + hpx * hpx + hpy * hpy + hpz * hpz)
                            hits[nh, 11] = dl
                            nh += 1
                    else:
                        zd = surf[L, 1]
                        if zd < zlo or zd > zhi or dx[3] == 0.0:
                            continue
                        f = (zd - za) / dx[3]
                        if f < 0.0 or f >= 1.0:
                            continue
                        xc = X[k, 1] + f * dx[1]; yc = X[k, 2] + f * dx[2]
                        rc = np.sqrt(xc * xc + yc * yc)
                        if rc < surf[L, 2] or rc >= surf[L, 3] or nh >= max_hits:
                            continue
                        ncnt[k, L] += 1
                        hits[nh, 0] = k; hits[nh, 1] = L; hits[nh, 2] = ncnt[k, L]
                        hits[nh, 3] = X[k, 0] + f * dx[0]
                        hits[nh, 4] = xc; hits[nh, 5] = yc; hits[nh, 6] = zd
                        hpx = p[1] + f * (pn[1] - p[1]); hpy = p[2] + f * (pn[2] - p[2]); hpz = p[3] + f * (pn[3] - p[3])
                        hits[nh, 7] = hpx; hits[nh, 8] = hpy; hits[nh, 9] = hpz
                        hits[nh, 10] = np.sqrt(m * m + hpx * hpx + hpy * hpy + hpz * hpz)
                        hits[nh, 11] = dl
                        nh += 1
                if kick_k == k and (not kicked) and (ra - kick_R) * (rb - kick_R) < 0.0:
                    kicked = True
                    for c in range(3):
                        pn[c + 1] += kick_dp[c]
                    pn[0] = np.sqrt(m * m + pn[1] ** 2 + pn[2] ** 2 + pn[3] ** 2)
            for c in range(4):
                X[k, c] += dx[c]
                P[k, c] = pn[c]
            if do_eloss or do_ms:
                dsx = np.sqrt(dx[1] ** 2 + dx[2] ** 2 + dx[3] ** 2)
                _material_kick_s3(P, X, k, m, qk, dsx, slabs, dslabs, regions, mat, do_eloss, do_strag, do_ms, eacc)
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


# ---- surfaces / disc material ----------------------------------------------------------------------------------
_SURF = None


def load_surfaces(path=None):
    """surfaces_s3.json -> dict(surf=(n,4) array [type, p0, p1, p2] in cm, names, kinds, t_sens, dslabs=(k,5))."""
    global _SURF
    if path is None and _SURF is not None:
        return _SURF
    d = json.load(open(path or (HERE / 'surfaces_s3.json')))
    S = d['surfaces']
    out = dict(surf=np.array([[s['type'], s['p0'], s['p1'], s['p2']] for s in S], float),
               names=[s['name'] for s in S], kinds=[s['kind'] for s in S],
               t_sens=np.array([s['t_sens'] for s in S], float),
               dslabs=np.array([[x['zc'], x['rmin'], x['rmax'], x['xX0'], x['w']] for x in d['disc_material']], float),
               dslab_names=[x['name'] for x in d['disc_material']], raw=d)
    sf = out['surf']
    ic = np.where(sf[:, 0] < 0.5)[0]; idd = np.where(sf[:, 0] >= 0.5)[0]
    oc = np.argsort(sf[ic, 1], kind='stable'); od = np.argsort(sf[idd, 1], kind='stable')
    out.update(cR=sf[ic, 1][oc].copy(), cI=ic[oc].astype(np.int64), dZ=sf[idd, 1][od].copy(), dI=idd[od].astype(np.int64))
    if path is None:
        _SURF = out
    return out


def run_causal_s3(p1, p2, m, lam_keV, B0=3.8112, bmode=0, material=True, ms=True, eloss=True, strag=True,
                  mat_scale=1.0, disc_material=None, slabs=None, regions=None, t_end=None, r_exit=118.0,
                  z_exit=None, beta_stop=0.0, max_boost=1e-2, hmax_trk=0.2, hmax_out=2.0, first_length=1e-7, seed=1,
                  charges=(1.0, -1.0), grid=None, max_hits=400000, max_steps=None, qcap=None, rec_radii=REC_RADII,
                  rec_zmax=REC_ZMAX, vertex=None, kick=None, legacy=False, _swapped=False):
    """legacy=True: exactly code/T3_causal.run_causal (same defaults: z_exit 290, max_steps 4e8, qcap 2^16, barrel
    recorder, vertex 0, no disc material); hits[:, :9] returned.
    legacy=False (Stage 3): surfaces of surfaces_s3.json, all roots, vertex (t, x, y, z) [cm], disc material, z_exit 293,
    qcap 2^19, max_steps 2e10; hits[n, 12] = [quirk, surf, icross, t, x, y, z, px, py, pz, E, dl] (cm, GeV).
    mat_scale scales the x/X0 of every barrel and disc slab (material x0.5 / x2 configurations)."""
    sig = sigma_from_lambda_keV(lam_keV)
    if legacy:
        z_exit = 290.0 if z_exit is None else z_exit
        max_steps = 400_000_000 if max_steps is None else max_steps
        qcap = (1 << 16) if qcap is None else qcap
        dsl = NO_DSLABS
        surf = np.zeros((0, 4)); rec_mode = 0
        cR = np.zeros(0); cI = np.zeros(0, np.int64); dZ = np.zeros(0); dI = np.zeros(0, np.int64)
        x0 = np.zeros(4)
        if vertex is not None or disc_material:
            raise ValueError('legacy mode has no vertex and no disc material')
    else:
        z_exit = 293.0 if z_exit is None else z_exit
        max_steps = 20_000_000_000 if max_steps is None else max_steps
        qcap = (1 << 19) if qcap is None else qcap
        S = load_surfaces()
        surf = S['surf']; rec_mode = 1
        cR, cI, dZ, dI = S['cR'], S['cI'], S['dZ'], S['dI']
        dsl = S['dslabs'].copy() if (disc_material is None or disc_material) else NO_DSLABS
        if len(dsl):
            dsl[:, 3] *= mat_scale
        x0 = np.zeros(4) if vertex is None else np.asarray(vertex, float)
    slabs = phase2_tracker(scale=mat_scale) if slabs is None else slabs
    regions = cms_outer_regions() if regions is None else regions
    grid = DUMMY_GRID if grid is None else grid
    p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
    if t_end is None:
        P = p1 + p2
        E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
        t_end = 1.3 * r_exit / max(np.hypot(P[0], P[1]) / E, 0.02) + 50.0 + float(x0[0])
    kk, kR, kdp = (-1, 0.0, np.zeros(3)) if kick is None else (int(kick[0]), float(kick[1]), np.asarray(kick[2], float))
    out = causal_propagate_s3(p1, p2, x0, float(m), sig, float(charges[0]), float(charges[1]), int(bmode), float(B0),
                              grid[0], grid[1], grid[2], slabs, dsl, regions, MAT, int(rec_mode),
                              np.asarray(rec_radii, float), np.asarray(rec_zmax, float), surf, cR, cI, dZ, dI,
                              bool(material and eloss), bool(material and strag), bool(material and ms), float(t_end),
                              float(r_exit), float(z_exit), float(beta_stop), float(max_boost), float(hmax_trk),
                              float(hmax_out), float(first_length), int(seed), int(max_hits), int(max_steps), int(qcap),
                              kk, kR, kdp)
    status, hits, X, P, eacc, nsteps, maxq = out
    if legacy:
        hits = hits[:, :9].copy()
    if status == 4 and nsteps < 1000 and not _swapped:
        # bootstrap deadlock (as the original): give the first string vector to the other quirk, then swap back
        kk2 = None if kick is None else (1 - int(kick[0]), kick[1], kick[2])
        r = run_causal_s3(p2, p1, m, lam_keV, B0, bmode, material, ms, eloss, strag, mat_scale, disc_material, slabs,
                          regions, t_end, r_exit, z_exit, beta_stop, max_boost, hmax_trk, hmax_out, first_length, seed,
                          (charges[1], charges[0]), grid, max_hits, max_steps, qcap, rec_radii, rec_zmax, vertex, kk2,
                          legacy, _swapped=True)
        h = r['hits'].copy()
        if len(h):
            h[:, 0] = 1 - h[:, 0]
        r.update(hits=h, X=r['X'][::-1].copy(), P=r['P'][::-1].copy(), eacc=r['eacc'][::-1].copy(), swapped=True)
        return r
    return dict(status=status, hits=hits, X=X, P=P, eacc=eacc, nsteps=nsteps, maxq=maxq, swapped=False)
