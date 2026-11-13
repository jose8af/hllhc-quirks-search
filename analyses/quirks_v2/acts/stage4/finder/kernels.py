"""Numba kernels of the fast F0 finder (G2a).  Selection logic identical to acts/stage4/probes/f1r_finder.py
(seeds / refit_nb / refit / duplicate merge); what changes is how hits are VISITED (always an exact superset of the
hits the reference tests, each visited hit gets the reference's per-hit test):

  * per-trial (phi, z) index: for each of the 16 barrel counting surfaces the road hits sit in phi bins (PV frame) and
    z cells.  A plane through the PV with normal n crosses a cylinder of radius r along n_x x + n_y y + n_z z = 0, so
    inside one phi bin the hits with |n.u| < tol lie in a z interval that follows from the range of
    r (n_x cos phi + n_y sin phi) over the bin (exact bounds incl. the extremum; bin_range / gather).
  * window lobes (seed score): a hit with |u.n2| <= W_c and |u.n| < tol is within W_c + tol of the axis line in 3D,
    hence (projection onto xy is a contraction) within W_c + tol of the projected axis line in xy:
    |sin(phi - phi_axis)| <= (W_c + tol)/r.  Only the two phi lobes around phi_axis and phi_axis + pi are visited.
  * seed score: layer-level early termination (a seed passes iff N_L2(seed) >= T_seed; layers are counted up to 2
    crossings and the scan stops as soon as the outcome is decided).  Pass/fail identical; the seed N_L2 returned for
    a passing seed is a lower bound (>= T_seed); the exact value is recomputed on request (seed_n2_exact).
  * refit: hits are gathered once per seed for every plane within delta of the gather centre (bound proven in
    gather()); |n_it - centre| <= delta is verified at every iteration and, if violated, the hits are re-gathered
    around n_it (the reference 5 / 60 mm pre-filter always w.r.t. the SEED normal) and the refit resumes at that
    iteration.  Selection in two phases (branch-free test, then accumulation over the selected hits).  The smallest
    eigenvector comes from inverse iteration with the adjugate (LAPACK eigh as fallback): same vector to ~1e-15.
  * duplicate merge: hash grid on the normal (cells of 2.1 mrad > the 2 mrad chord), same greedy order and the same
    criterion |1 - |n.g|| < 2e-6 as the reference.
  Float-level differences only (summation order, squared-form comparisons, eigen-solver): the G2 equivalence test
  (test_equivalence.py) finds identical seed sets and identical candidate hit sets on 24 PU-only trials.
"""
import numpy as np
from numba import njit

PI = np.pi
TWO_PI = 2 * np.pi
# local surface j (0..15): TBPX L1-4, TBPS L1 in/out, L2 in/out, L3 in/out, TB2S L1 in/out, L2, L3
SURF_LC = np.array([0, 1, 2, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9], np.int64)
SURF_SD = np.array([0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2], np.int64)
LAYER_S0 = np.array([0, 1, 2, 3, 4, 6, 8, 10, 12, 14], np.int64)      # first surface of layer k
# seed-score layer order: the discriminating layers first, the saturated TBPX L2/L1 last
SEED_ORDER = np.array([3, 2, 4, 5, 6, 7, 8, 9, 1, 0], np.int64)


@njit(cache=True, error_model='numpy')
def wrap(d):
    while d > np.pi:
        d -= 2 * np.pi
    while d < -np.pi:
        d += 2 * np.pi
    return d


@njit(cache=True, error_model='numpy')
def score_cnt(cnt):
    n1 = 0
    n2 = 0
    nit2 = 0
    for k in range(10):
        if k < 4:
            c = cnt[k, 0]
        else:
            c = min(cnt[k, 1], cnt[k, 2])
        if c >= 1:
            n1 += 1
        if c >= 2:
            n2 += 1
            if k < 4:
                nit2 += 1
    return n1, n2, nit2


@njit(cache=True, error_model='numpy')
def zcells(j, k, SF, SI, CS, zlo, zhi):
    """Positions [i0, i1) of the (phi bin k, z cells) of surface j overlapping [zlo, zhi] (superset; cells are
    contiguous in the (bin, z)-sorted position array)."""
    zmin = SF[j, 6]; dz = SF[j, 7]; nzc = SI[j, 6]
    c0 = (zlo - zmin) / dz
    c1 = (zhi - zmin) / dz
    if c1 < 0 or c0 >= nzc:
        return 0, 0
    i0c = int(c0) if c0 > 0 else 0
    i1c = int(c1) if c1 < nzc - 1 else nzc - 1
    base = SI[j, 5] + k * (nzc + 1)
    return CS[base + i0c], CS[base + i1c + 1]


@njit(cache=True, error_model='numpy')
def bin_range(k, j, SF, SI, CS, bstart, ce, se, nx, ny, nz, A, kmx, kmn, tol, t2b, ss):
    """Positions [i0, i1) of bin k of surface j whose z can satisfy |r g(phi) + n_z z| < tol for some r in
    [rmin, rmax] and phi in the bin, g = n_x cos(phi) + n_y sin(phi).  Exact superset (g range from the bin edges
    plus the extremum; z cells of the 2-D grid)."""
    boff = SI[j, 1]; eoff = SI[j, 2]
    p0 = bstart[boff + k]
    p1 = bstart[boff + k + 1]
    if p0 == p1:
        return p0, p0
    rmin = SF[j, 0]; rmax = SF[j, 1]
    g0 = nx * ce[eoff + k] + ny * se[eoff + k]
    g1 = nx * ce[eoff + k + 1] + ny * se[eoff + k + 1]
    gmin = min(g0, g1)
    gmax = max(g0, g1)
    if k == kmx:
        gmax = A
    if k == kmn:
        gmin = -A
    plo = gmin * rmax if gmin < 0 else gmin * rmin
    phi = gmax * rmax if gmax > 0 else gmax * rmin
    t = tol + 1e-6
    if nz > 0:
        zlo = (-t - phi) / nz
        zhi = (t - plo) / nz
    elif nz < 0:
        zlo = (t - plo) / nz
        zhi = (-t - phi) / nz
    else:
        if (-t - phi) < 0 and (t - plo) > 0:
            return p0, p1
        return p0, p0
    if ss > 0:
        # second pass: the band tolerance 3 sqrt(t2b + (ss |u|)^2) grows with |u| <= sqrt(rmax^2 + z^2)
        zl = max(zlo, SF[j, 6]); zh = min(zhi, SF[j, 6] + SF[j, 7] * SI[j, 6])
        if zl > zh:
            return p0, p0
        ub = np.sqrt(rmax * rmax + max(zl * zl, zh * zh))
        t2 = 3 * np.sqrt(t2b + (ss * ub) ** 2) + 1e-6
        if t2 < t:
            if nz > 0:
                zlo = max(zl, (-t2 - phi) / nz); zhi = min(zh, (t2 - plo) / nz)
            else:
                zlo = max(zl, (t2 - plo) / nz); zhi = min(zh, (-t2 - phi) / nz)
            if zlo > zhi:
                return p0, p0
    return zcells(j, k, SF, SI, CS, zlo, zhi)


@njit(cache=True, error_model='numpy')
def lobe_bins(nb, bw, center, hw, buf, nbuf, stamp, boff, qid):
    """Append the bins of the phi interval [center - hw, center + hw] (wrapped) not yet stamped with qid."""
    if hw >= np.pi:
        k0 = 0
        k1 = nb - 1
    else:
        c = wrap(center)
        k0 = int(np.floor((c - hw + np.pi) / bw))
        k1 = int(np.floor((c + hw + np.pi) / bw))
        if k1 - k0 + 1 >= nb:
            k0 = 0
            k1 = nb - 1
    for kk in range(k0, k1 + 1):
        k = kk % nb
        if k < 0:
            k += nb
        if stamp[boff + k] != qid:
            stamp[boff + k] = qid
            buf[nbuf] = k
            nbuf += 1
    return nbuf


@njit(cache=True, error_model='numpy')
def ext_bins(nb, bw, nx, ny):
    """Bins holding the max (phi_n) and min (phi_n + pi) of g(phi) = n_x cos + n_y sin."""
    phn = np.arctan2(ny, nx)
    kmx = int(np.floor((phn + np.pi) / bw)) % nb
    phm = wrap(phn + np.pi)
    kmn = int(np.floor((phm + np.pi) / bw)) % nb
    return kmx, kmn


@njit(cache=True, error_model='numpy')
def count_surface(j, cap, nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol,
                  P, CS, bstart, ce, se, SF, SI, stamp, qid, buf, pa, phn):
    """Seed-score count on surface j (reference seeds() per-hit test), stopping at `cap` hits."""
    rmin = SF[j, 0]; rmax = SF[j, 1]; umax = SF[j, 2]; s0 = SF[j, 3]; s1 = SF[j, 4]; bw = SF[j, 5]
    nb = SI[j, 0]; boff = SI[j, 1]; eoff = SI[j, 2]
    A = np.sqrt(nx * nx + ny * ny)
    sgm = np.sqrt(A * A * s0 * s0 + nz * nz * s1 * s1)
    tol = 3 * np.sqrt(sgm * sgm + ttol * ttol + (sseed * umax) ** 2)
    hw = np.arcsin(min(1.0, (wc + tol) / rmin))
    nbuf = 0
    if ax == 0.0 and ay == 0.0:
        nbuf = lobe_bins(nb, bw, 0.0, 4.0, buf, nbuf, stamp, boff, qid)
    else:
        nbuf = lobe_bins(nb, bw, pa, hw, buf, nbuf, stamp, boff, qid)
        nbuf = lobe_bins(nb, bw, pa + np.pi, hw, buf, nbuf, stamp, boff, qid)
    kmx = int(np.floor((phn + np.pi) / bw)) % nb
    kmn = int(np.floor((wrap(phn + np.pi) + np.pi) / bw)) % nb
    cnt = 0
    for q in range(nbuf):
        i0, i1 = bin_range(buf[q], j, SF, SI, CS, bstart, ce, se, nx, ny, nz, A, kmx, kmn, tol,
                           sgm * sgm + ttol * ttol, 0.0)
        for p in range(i0, i1):      # branch-free per hit; the cap is checked per bin (count >= cap is all we need)
            ux = P[0, p]; uy = P[1, p]; uz = P[2, p]
            di = ux * nx + uy * ny + uz * nz
            a = -nx * P[4, p] + ny * P[3, p]
            ui = P[5, p]
            # |d| < 3 sqrt(sg^2 + t^2 + (s u)^2) in squared form (float-level only)
            ok = ((ux * ax + uy * ay + uz * az > 0) & (abs(ux * n2x + uy * n2y + uz * n2z) <= wc)
                  & (di * di < 9.0 * (a * a * s0 * s0 + nz * nz * s1 * s1 + ttol * ttol + (sseed * ui) ** 2)))
            cnt += np.int64(ok)
        if cnt >= cap:
            return cnt
    return cnt


@njit(cache=True, error_model='numpy')
def seed_score(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, tseed, early,
               P, CS, bstart, ce, se, SF, SI, stamp, qid0, buf, order):
    """Seed N_L2 (crossings >= 2 per layer).  early=True: stop as soon as pass/fail is decided (returns a lower bound
    >= tseed on pass, -1 on fail); early=False: exact value (reference seeds())."""
    n2 = 0
    qid = qid0
    pa = np.arctan2(ay, ax)
    phn = np.arctan2(ny, nx)
    for t in range(10):
        k = order[t]
        j = LAYER_S0[k]
        cap = 2 if early else 1 << 30
        if k < 4:
            qid += 1
            c = count_surface(j, cap, nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, P, CS, bstart, ce, se,
                              SF, SI, stamp, qid, buf, pa, phn)
        else:
            qid += 1
            ci = count_surface(j, cap, nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, P, CS, bstart, ce, se,
                               SF, SI, stamp, qid, buf, pa, phn)
            if ci >= 2:
                qid += 1
                co = count_surface(j + 1, cap, nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, P, CS, bstart, ce,
                                   se, SF, SI, stamp, qid, buf, pa, phn)
                c = min(ci, co)
            else:
                c = ci
        if c >= 2:
            n2 += 1
        if early:
            if n2 >= tseed:
                return n2, qid
            if n2 + (9 - t) < tseed:
                return -1, qid
    return n2, qid


@njit(cache=True, error_model='numpy')
def norm3(x, y, z):
    return np.sqrt(x * x + y * y + z * z)


@njit(cache=True, error_model='numpy')
def seeds_fast(U, phiU, etaU, A_idx, posB, posC, P, CS, bstart, ce, se, SF, SI, phimet, road, wc, tseed, ttol, early,
               order):
    """Reference seeds(): (a in TBPX L4, b in L3) with |dphi| <= 0.3, |deta| <= 0.2, sin > 1e-3, a valid c in L2,
    seed N_L2 >= tseed.  Returns arrays (ia, ib, n2) in reference order (ia, then ib ascending) and ntrip."""
    nbins_tot = bstart.shape[0]
    stamp = np.zeros(nbins_tot, np.int64)
    buf = np.empty(nbins_tot, np.int64)
    qid = 0
    cap = 1 << 16
    oa = np.empty(cap, np.int64); ob = np.empty(cap, np.int64); on = np.empty(cap, np.int64)
    nout = 0
    ntrip = 0
    jB = 2; jC = 1
    bl = np.empty(4096, np.int64)
    for t in range(A_idx.shape[0]):
        ia = A_idx[t]
        ra = np.hypot(U[ia, 0], U[ia, 1])
        if abs(wrap(phiU[ia] - phimet)) > road + np.arcsin(min(1.0, wc / ra)):
            continue
        # candidate b hits: L3 bins within phi_a +- 0.3
        qid += 1
        nb = SI[jB, 0]; boff = SI[jB, 1]; bw = SF[jB, 5]
        nbuf = lobe_bins(nb, bw, phiU[ia], 0.3 + 1e-9, buf, 0, stamp, boff, qid)
        nbl = 0
        for q in range(nbuf):
            k = buf[q]
            for p in range(bstart[boff + k], bstart[boff + k + 1]):
                ib = posB[p]
                if nbl >= bl.shape[0]:
                    nbl2 = np.empty(2 * bl.shape[0], np.int64); nbl2[:nbl] = bl[:nbl]; bl = nbl2
                bl[nbl] = ib
                nbl += 1
        bls = np.sort(bl[:nbl])
        for q in range(nbl):
            ib = bls[q]
            rb = np.hypot(U[ib, 0], U[ib, 1])
            if abs(wrap(phiU[ib] - phimet)) > road + np.arcsin(min(1.0, wc / rb)):
                continue
            if abs(wrap(phiU[ia] - phiU[ib])) > 0.3 or abs(etaU[ia] - etaU[ib]) > 0.2:
                continue
            uax = U[ia, 0]; uay = U[ia, 1]; uaz = U[ia, 2]
            ubx = U[ib, 0]; uby = U[ib, 1]; ubz = U[ib, 2]
            cx_ = uay * ubz - uaz * uby
            cy_ = uaz * ubx - uax * ubz
            cz_ = uax * uby - uay * ubx
            na = norm3(uax, uay, uaz); nbn = norm3(ubx, uby, ubz)
            ncn = norm3(cx_, cy_, cz_)
            sn = ncn / (na * nbn)
            if sn < 1e-3:
                continue
            nx = cx_ / ncn; ny = cy_ / ncn; nz = cz_ / ncn
            sseed = 0.03 / (nbn * sn)
            ax = uax / na + ubx / nbn; ay = uay / na + uby / nbn; az = uaz / na + ubz / nbn
            an = norm3(ax, ay, az)
            ax /= an; ay /= an; az /= an
            n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
            # c search on TBPX L2 (no window), |dphi(c, b)| <= 0.4
            qid += 1
            rminC = SF[jC, 0]; rmaxC = SF[jC, 1]; umaxC = SF[jC, 2]; s0C = SF[jC, 3]; s1C = SF[jC, 4]; bwC = SF[jC, 5]
            nbC = SI[jC, 0]; boffC = SI[jC, 1]; eoffC = SI[jC, 2]
            Aab = np.sqrt(nx * nx + ny * ny)
            sgm = np.sqrt(Aab * Aab * s0C * s0C + nz * nz * s1C * s1C)
            tolc = 3 * np.sqrt(sgm * sgm + ttol * ttol + (sseed * umaxC) ** 2)
            nbuf = lobe_bins(nbC, bwC, phiU[ib], 0.4 + 1e-9, buf, 0, stamp, boffC, qid)
            kmx, kmn = ext_bins(nbC, bwC, nx, ny)
            found = False
            for q2 in range(nbuf):
                i0, i1 = bin_range(buf[q2], jC, SF, SI, CS, bstart, ce, se, nx, ny, nz, Aab, kmx, kmn, tolc,
                                   sgm * sgm + ttol * ttol, 0.0)
                nok = 0
                for p in range(i0, i1):          # branch-free per hit, existence checked per bin
                    ic = posC[p]
                    ucx = P[0, p]; ucy = P[1, p]; ucz = P[2, p]
                    d = ucx * nx + ucy * ny + ucz * nz
                    a = -nx * P[4, p] + ny * P[3, p]
                    ok = ((abs(wrap(phiU[ic] - phiU[ib])) <= 0.4)
                          & (d * d <= 9.0 * (a * a * s0C * s0C + nz * nz * s1C * s1C + ttol * ttol
                                             + (sseed * P[5, p]) ** 2)))
                    nok += np.int64(ok)
                if nok > 0:
                    found = True
                    break
            if not found:
                continue
            ntrip += 1
            n2, qid = seed_score(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, tseed, early,
                                 P, CS, bstart, ce, se, SF, SI, stamp, qid, buf, order)
            if n2 >= tseed:
                if nout >= oa.shape[0]:
                    m = 2 * oa.shape[0]
                    t1 = np.empty(m, np.int64); t1[:nout] = oa[:nout]; oa = t1
                    t2 = np.empty(m, np.int64); t2[:nout] = ob[:nout]; ob = t2
                    t3 = np.empty(m, np.int64); t3[:nout] = on[:nout]; on = t3
                oa[nout] = ia; ob[nout] = ib; on[nout] = n2
                nout += 1
    return oa[:nout], ob[:nout], on[:nout], ntrip


@njit(cache=True, error_model='numpy')
def min_eigvec(M, nx, ny, nz):
    """Eigenvector of the smallest eigenvalue of the symmetric PSD 3x3 M (lower triangle, as LAPACK uses) by inverse
    iteration from the current normal n: x <- adj(M) x / |adj(M) x|.  The error shrinks by lambda1/lambda2 (~1e-6 for
    a plane fit) per step; returns ok = False (caller falls back to eigh) if not converged to 1e-15 in 12 steps."""
    a = M[0, 0]; b = M[1, 1]; c = M[2, 2]; d = M[1, 0]; e = M[2, 0]; f = M[2, 1]
    A00 = b * c - f * f; A11 = a * c - e * e; A22 = a * b - d * d
    A01 = e * f - d * c; A02 = d * f - b * e; A12 = d * e - a * f
    x = nx; y = ny; z = nz
    for it in range(12):
        X = A00 * x + A01 * y + A02 * z
        Y = A01 * x + A11 * y + A12 * z
        Z = A02 * x + A12 * y + A22 * z
        nrm = np.sqrt(X * X + Y * Y + Z * Z)
        if not (nrm > 0):
            return False, nx, ny, nz
        X /= nrm; Y /= nrm; Z /= nrm
        ch = (X - x) ** 2 + (Y - y) ** 2 + (Z - z) ** 2
        x = X; y = Y; z = Z
        if it >= 1 and ch < 1e-30:
            return True, x, y, z
    return False, nx, ny, nz


@njit(cache=True, error_model='numpy')
def zint(plo, phi, nz, tol):
    """z interval where |p + n_z z| < tol is possible for p in [plo, phi]; returns (zlo, zhi, ok)."""
    t = tol + 1e-6
    if nz > 0:
        return (-t - phi) / nz, (t - plo) / nz, True
    elif nz < 0:
        return (t - plo) / nz, (-t - phi) / nz, True
    if (-t - phi) < 0 and (t - plo) > 0:
        return -1e300, 1e300, True
    return 0.0, 0.0, False


@njit(cache=True, error_model='numpy')
def gather(n0x, n0y, n0z, delta, P, CS, bstart, ce, se, SF, SI, PRE, ttol, out, NEB, NEO, f0x, f0y, f0z):
    """Write into out the index positions of every road hit with |u.n0| < PRE (reference pre-filter) that can pass
    |u.n| < 3 sg(n) for SOME unit n with |n - n0| <= delta.  Bound: |u.n0| <= |u.n| + |u| delta < 3 sg(n) + delta |u|;
    sig(n)^2 = a(n)^2 s0^2 + n_z^2 s1^2 with |a(n)| <= sqrt(n_x^2 + n_y^2) <= A0 + delta and |n_z| <= |n0_z| + delta,
    so sg(n) <= sqrt(max(sqrt((A0 + delta)^2 s0^2 + (|n0_z| + delta)^2 s1^2), 1e-4)^2 + t_tol^2).
    Every non-empty road bin (list NEB) of every surface is visited; per bin the z interval uses
    |u| <= sqrt(rmax^2 + z^2) (two passes).  n0 here is the gather centre (the seed normal, or the current normal
    after a re-gather); the reference pre-filter is always applied with the SEED normal f0.  Returns the count."""
    m = 0
    A = np.sqrt(n0x * n0x + n0y * n0y)
    for j in range(16):
        rmin = SF[j, 0]; rmax = SF[j, 1]; umax = SF[j, 2]; s0 = SF[j, 3]; s1 = SF[j, 4]; bw = SF[j, 5]
        nb = SI[j, 0]; boff = SI[j, 1]; eoff = SI[j, 2]; kf = SI[j, 3]; kn = SI[j, 4]
        pre = PRE[j]
        sgb = np.sqrt((A + delta) ** 2 * s0 * s0 + (abs(n0z) + delta) ** 2 * s1 * s1)
        T = 3 * np.sqrt(max(sgb, 1e-4) ** 2 + ttol * ttol) + 1e-9
        tol1 = min(pre, T + delta * umax)
        kmx, kmn = ext_bins(nb, bw, n0x, n0y)
        for tt in range(NEO[j], NEO[j + 1]):
            k = NEB[tt]
            p0 = bstart[boff + k]; p1 = bstart[boff + k + 1]
            g0 = n0x * ce[eoff + k] + n0y * se[eoff + k]
            g1 = n0x * ce[eoff + k + 1] + n0y * se[eoff + k + 1]
            gmin = min(g0, g1); gmax = max(g0, g1)
            if k == kmx:
                gmax = A
            if k == kmn:
                gmin = -A
            plo = gmin * rmax if gmin < 0 else gmin * rmin
            phi = gmax * rmax if gmax > 0 else gmax * rmin
            zlo, zhi, ok = zint(plo, phi, n0z, tol1)
            if not ok:
                continue
            zlo = max(zlo, SF[j, 6]); zhi = min(zhi, SF[j, 6] + SF[j, 7] * SI[j, 6])
            if zlo > zhi:
                continue
            ub = np.sqrt(rmax * rmax + max(zlo * zlo, zhi * zhi))
            tol2 = min(pre, T + delta * ub)
            if tol2 < tol1:
                zlo2, zhi2, ok = zint(plo, phi, n0z, tol2)
                if not ok:
                    continue
                zlo = max(zlo, zlo2); zhi = min(zhi, zhi2)
                if zlo > zhi:
                    continue
            i0, i1 = zcells(j, k, SF, SI, CS, zlo, zhi)
            for p in range(i0, i1):
                ad = abs(P[0, p] * n0x + P[1, p] * n0y + P[2, p] * n0z)
                af = abs(P[0, p] * f0x + P[1, p] * f0y + P[2, p] * f0z)
                out[m] = p
                m += np.int64((af < pre) & (ad <= T + delta * P[5, p]))     # branch-free (no short-circuit)
    return m


@njit(cache=True, error_model='numpy')
def refit_packed(L, m, P, PJ, PLC, PSD, pid, n0, axis0, wc, iters, ttol, delta, SF, sel, M, cnt, sgu, selp, selw,
                 it0, cx0, cy0, cz0):
    """Reference refit_nb() on the gathered positions L[:m], starting at iteration it0 with normal n0 and axis axis0.
    The gathered list covers every plane within delta of the gather centre c.  Returns (status, n, nl2, nit2, chi2ndf,
    nsel, axis, dmax, nfin, it); status 1 = |n_it - c| > delta at iteration it (the caller re-gathers around n_it and
    resumes at it with the returned n, axis).  sel[:nfin] = positions selected at the final iteration."""
    nx = n0[0]; ny = n0[1]; nz = n0[2]
    ax = axis0[0]; ay = axis0[1]; az = axis0[2]
    chi2 = 0.0; nsel = 0
    dmax = 0.0
    nfin = 0
    for it in range(it0, iters + 1):
        dn = np.sqrt((nx - cx0) ** 2 + (ny - cy0) ** 2 + (nz - cz0) ** 2)
        if dn > dmax:
            dmax = dn
        if dn > delta:
            return 1, nx, ny, nz, -1, -1, 1e9, 0, ax, ay, az, dmax, 0, it
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        for aa in range(3):
            for bb in range(3):
                M[aa, bb] = 0.0
        chi2 = 0.0; nsel = 0
        cnt[:, :] = 0
        s_x = 0.0; s_y = 0.0; s_z = 0.0
        last = it == iters
        # phase 1 (branch-free): positions passing the reference selection -> sel_pos
        ns = 0
        for q in range(m):
            p = L[q]
            ux = P[0, p]; uy = P[1, p]; uz = P[2, p]
            d = ux * nx + uy * ny + uz * nz
            j = PJ[p]
            a = -nx * P[4, p] + ny * P[3, p]
            s0 = SF[j, 3]; s1 = SF[j, 4]
            sc2 = a * a * s0 * s0 + nz * nz * s1 * s1
            # |d| < 3 sg  <=>  d^2 < 9 (max(sc, 1e-4)^2 + t_tol^2)   (squared form, no sqrt; float-level only)
            ok = ((d * d < 9.0 * (max(sc2, 1e-8) + ttol * ttol)) & (ux * ax + uy * ay + uz * az > 0)
                  & (abs(ux * n2x + uy * n2y + uz * n2z) < wc))
            selp[ns] = p
            ns += np.int64(ok)
        # phase 2: accumulate over the selected hits (same order as the reference loop over the gathered list)
        for q in range(ns):
            p = selp[q]
            ux = P[0, p]; uy = P[1, p]; uz = P[2, p]
            d = ux * nx + uy * ny + uz * nz
            j = PJ[p]
            a = -nx * P[4, p] + ny * P[3, p]
            sc = np.sqrt(a * a * SF[j, 3] * SF[j, 3] + nz * nz * SF[j, 4] * SF[j, 4])
            sg = np.sqrt(max(sc, 1e-4) ** 2 + ttol * ttol)
            w = 1.0 / (sg * sg)
            M[0, 0] += w * ux * ux; M[0, 1] += w * ux * uy; M[0, 2] += w * ux * uz
            M[1, 0] += w * uy * ux; M[1, 1] += w * uy * uy; M[1, 2] += w * uy * uz
            M[2, 0] += w * uz * ux; M[2, 1] += w * uz * uy; M[2, 2] += w * uz * uz
            chi2 += d * d * w; nsel += 1
            cnt[PLC[p], PSD[p]] += 1
            un = P[5, p]
            s_x += ux / un; s_y += uy / un; s_z += uz / un
            if last:
                sel[nfin] = p           # sorted-index position (ascending: L is ascending)
                nfin += 1
        if nsel < 4:
            return 0, nx, ny, nz, -1, -1, 1e9, nsel, ax, ay, az, dmax, 0, it
        if last:
            break
        ok, vx, vy, vz = min_eigvec(M, nx, ny, nz)
        if not ok:
            ev, evec = np.linalg.eigh(M)
            vx = evec[0, 0]; vy = evec[1, 0]; vz = evec[2, 0]
        if vx * nx + vy * ny + vz * nz < 0:
            vx = -vx; vy = -vy; vz = -vz
        nx = vx; ny = vy; nz = vz
        dd = s_x * nx + s_y * ny + s_z * nz
        s_x = s_x - dd * nx; s_y = s_y - dd * ny; s_z = s_z - dd * nz
        an = np.sqrt(s_x ** 2 + s_y ** 2 + s_z ** 2)
        if an > 0:
            ax = s_x / an; ay = s_y / an; az = s_z / an
    n1, nl2, nit2 = score_cnt(cnt)
    return 0, nx, ny, nz, nl2, nit2, chi2 / max(nsel - 2, 1), nsel, ax, ay, az, dmax, nfin, iters


@njit(cache=True, error_model='numpy')
def n_reg_s_guard(delta):
    """Never loops forever: every re-gather resumes at the failing iteration (it never decreases), so at most
    iters + 1 re-gathers per seed occur; delta is kept (the guard is a no-op hook)."""
    return False


@njit(cache=True, error_model='numpy')
def refit_all(U, LC, oa, ob, P, CS, PJ, PLC, PSD, pid, bstart, ce, se, SF, SI, PRE, NEB, NEO, wc, iters, ttol,
              dfac, dmin):
    """Refit every passing seed.  Returns per seed: nl2, nit2, chi2ndf, nsel, n (3), axis (3), n0 (3), axis0 (3),
    dmax, the final selected hit lists (CSR: hoff, hits; sorted road indices) for nl2 >= 4, and counters."""
    ns = oa.shape[0]
    NL2 = np.empty(ns, np.int64); NIT2 = np.empty(ns, np.int64); CHI = np.empty(ns); NSEL = np.empty(ns, np.int64)
    NF = np.empty((ns, 3)); AX = np.empty((ns, 3)); N0 = np.empty((ns, 3)); A0 = np.empty((ns, 3))
    DM = np.empty(ns)
    hoff = np.zeros(ns + 1, np.int64)
    hcap = max(ns * 96, 1024)
    hits = np.empty(hcap, np.int32)
    nh = 0
    nr = P.shape[1]
    L = np.empty(nr, np.int64)
    sel = np.empty(nr, np.int64); selp = np.empty(nr, np.int64); selw = np.empty(nr)
    M = np.zeros((3, 3)); cnt = np.zeros((10, 3), np.int64); sgu = np.empty(16)
    n0 = np.empty(3); ax0 = np.empty(3); cn = np.empty(3); st_n = np.empty(3); st_a = np.empty(3)
    n_reg = 0; n_full = 0
    for s in range(ns):
        ia = oa[s]; ib = ob[s]
        cx_ = U[ia, 1] * U[ib, 2] - U[ia, 2] * U[ib, 1]
        cy_ = U[ia, 2] * U[ib, 0] - U[ia, 0] * U[ib, 2]
        cz_ = U[ia, 0] * U[ib, 1] - U[ia, 1] * U[ib, 0]
        nc = norm3(cx_, cy_, cz_)
        n0[0] = cx_ / nc; n0[1] = cy_ / nc; n0[2] = cz_ / nc
        na = norm3(U[ia, 0], U[ia, 1], U[ia, 2]); nbn = norm3(U[ib, 0], U[ib, 1], U[ib, 2])
        a0x = U[ia, 0] / na + U[ib, 0] / nbn; a0y = U[ia, 1] / na + U[ib, 1] / nbn; a0z = U[ia, 2] / na + U[ib, 2] / nbn
        an = norm3(a0x, a0y, a0z)
        ax0[0] = a0x / an; ax0[1] = a0y / an; ax0[2] = a0z / an
        sn = nc / (na * nbn)
        sseed = 0.03 / (nbn * sn)
        delta = max(dmin, dfac * sseed)
        # resumable refit: gather around centre c (first the seed normal); if an iteration's normal leaves the
        # delta-ball around c, re-gather around that normal (pre-filter still w.r.t. the seed normal) and resume
        cn[0] = n0[0]; cn[1] = n0[1]; cn[2] = n0[2]
        st_n[0] = n0[0]; st_n[1] = n0[1]; st_n[2] = n0[2]
        st_a[0] = ax0[0]; st_a[1] = ax0[1]; st_a[2] = ax0[2]
        it0 = 0
        dmax_all = 0.0
        while True:
            if delta >= 2.0:
                # full pre-filter scan: exactly the reference pre-filter (any unit n is within 2 of c)
                m = 0
                for p in range(nr):
                    if abs(P[0, p] * n0[0] + P[1, p] * n0[1] + P[2, p] * n0[2]) < (60.0 if PLC[p] >= 7 else 5.0):
                        L[m] = p
                        m += 1
                n_full += 1
            else:
                m = gather(cn[0], cn[1], cn[2], delta, P, CS, bstart, ce, se, SF, SI, PRE, ttol, L, NEB, NEO,
                           n0[0], n0[1], n0[2])
            (st, nx, ny, nz, nl2, nit2, chi, nsel, ax, ay, az, dmax,
             nfin, itr) = refit_packed(L, m, P, PJ, PLC, PSD, pid, st_n, st_a, wc, iters, ttol, delta, SF, sel, M, cnt,
                                       sgu, selp, selw, it0, cn[0], cn[1], cn[2])
            dn0 = np.sqrt((nx - n0[0]) ** 2 + (ny - n0[1]) ** 2 + (nz - n0[2]) ** 2)
            if dn0 > dmax_all:
                dmax_all = dn0
            if st == 0:
                break
            n_reg += 1
            it0 = itr
            cn[0] = nx; cn[1] = ny; cn[2] = nz
            st_n[0] = nx; st_n[1] = ny; st_n[2] = nz
            st_a[0] = ax; st_a[1] = ay; st_a[2] = az
            if n_reg_s_guard(delta):
                delta = 2.0
        dmax = dmax_all
        NL2[s] = nl2; NIT2[s] = nit2; CHI[s] = chi; NSEL[s] = nsel; DM[s] = dmax
        NF[s, 0] = nx; NF[s, 1] = ny; NF[s, 2] = nz; AX[s, 0] = ax; AX[s, 1] = ay; AX[s, 2] = az
        N0[s] = n0; A0[s] = ax0
        if nl2 >= 4:
            if nh + nfin > hits.shape[0]:
                h2 = np.empty(2 * (nh + nfin), np.int32); h2[:nh] = hits[:nh]; hits = h2
            for q in range(nfin):
                hits[nh + q] = sel[q]
            nh += nfin
        hoff[s + 1] = nh
    return NL2, NIT2, CHI, NSEL, NF, AX, N0, A0, DM, hoff, hits[:nh], n_reg, n_full


@njit(cache=True, error_model='numpy')
def _hkey(ix, iy, iz):
    h = (ix * 73856093) ^ (iy * 19349663) ^ (iz * 83492791)
    return h


@njit(cache=True, error_model='numpy')
def dedup(NF, order, cell):
    """Greedy merge in `order`: drop a candidate if |1 - |n.g|| < 2e-6 for a kept g (reference criterion).  Hash grid
    on the normal components with cell size `cell` (> 2 mrad chord) and a 27-cell neighbourhood around n and -n."""
    N = order.shape[0]
    size = 1
    while size < 4 * N + 16:
        size *= 2
    mask = size - 1
    tkey_x = np.empty(size, np.int64); tkey_y = np.empty(size, np.int64); tkey_z = np.empty(size, np.int64)
    thead = np.full(size, -1, np.int64)
    used = np.zeros(size, np.bool_)
    nxt = np.full(NF.shape[0], -1, np.int64)
    keep = np.zeros(NF.shape[0], np.bool_)
    for r in range(N):
        c = order[r]
        nx = NF[c, 0]; ny = NF[c, 1]; nz = NF[c, 2]
        dup = False
        for sgn in (1.0, -1.0):
            ix = int(np.floor(sgn * nx / cell)); iy = int(np.floor(sgn * ny / cell)); iz = int(np.floor(sgn * nz / cell))
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        kx = ix + dx; ky = iy + dy; kz = iz + dz
                        slot = _hkey(kx, ky, kz) & mask
                        while used[slot]:
                            if tkey_x[slot] == kx and tkey_y[slot] == ky and tkey_z[slot] == kz:
                                g = thead[slot]
                                while g >= 0:
                                    dot = nx * NF[g, 0] + ny * NF[g, 1] + nz * NF[g, 2]
                                    if abs(abs(dot) - 1.0) < 2e-6:
                                        dup = True
                                        break
                                    g = nxt[g]
                                break
                            slot = (slot + 1) & mask
                        if dup:
                            break
                    if dup:
                        break
                if dup:
                    break
            if dup:
                break
        if dup:
            continue
        keep[c] = True
        ix = int(np.floor(nx / cell)); iy = int(np.floor(ny / cell)); iz = int(np.floor(nz / cell))
        slot = _hkey(ix, iy, iz) & mask
        while used[slot] and not (tkey_x[slot] == ix and tkey_y[slot] == iy and tkey_z[slot] == iz):
            slot = (slot + 1) & mask
        if not used[slot]:
            used[slot] = True
            tkey_x[slot] = ix; tkey_y[slot] = iy; tkey_z[slot] = iz
        nxt[c] = thead[slot]
        thead[slot] = c
    return keep


@njit(cache=True, error_model='numpy')
def cand_vars(U, CX, CY, S0, S1, LC, SD, hoff, hits, cands, NF, AX, ttol, pid, loose_only):
    """Stored variables of the kept candidates (reference refit() outputs + the plan's ladder variables).
    Columns: 0 nit2, 1 not2, 2 nl2, 3 not2h, 4 nl2h, 5 nl1, 6 chi2ndf, 7 nhit, 8 dw_old, 9 dw_core (= w_core),
    10 nip2, 11 n2s2, 12 chi2_core (one-step core, plan §2.2 item 5), 13 n_core, 14 |n_z|."""
    nc = cands.shape[0]
    V = np.full((nc, 15), np.nan)
    for q in range(nc):
        c = cands[q]
        h0 = hoff[c]; h1 = hoff[c + 1]
        k = h1 - h0
        n = NF[c]; axis = AX[c]
        n2v = np.cross(n, axis)
        cnt = np.zeros((10, 3), np.int64)
        chi2 = 0.0
        wv = np.empty(k)
        ip = np.zeros(k, np.bool_)
        nip = 0
        for t in range(k):
            i = pid[hits[h0 + t]]
            cnt[LC[i], SD[i]] += 1
            d = U[i, 0] * n[0] + U[i, 1] * n[1] + U[i, 2] * n[2]
            a = -n[0] * CY[i] + n[1] * CX[i]
            sc = np.sqrt(a * a * S0[i] * S0[i] + n[2] * n[2] * S1[i] * S1[i])
            sg = np.sqrt(max(sc, 1e-4) ** 2 + ttol * ttol)
            chi2 += d * d / (sg * sg)
            wv[t] = U[i, 0] * n2v[0] + U[i, 1] * n2v[1] + U[i, 2] * n2v[2]
            if LC[i] <= 6:
                ip[t] = True
                nip += 1
        cr = np.empty(10, np.int64)
        for l in range(10):
            cr[l] = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
        nit2 = 0; not2 = 0; nip2 = 0; n2s2 = 0; nl1 = 0; not2h = 0
        for l in range(10):
            if cr[l] >= 2:
                if l < 4:
                    nit2 += 1
                else:
                    not2 += 1
                if l < 7:
                    nip2 += 1
                else:
                    n2s2 += 1
            if cr[l] >= 1:
                nl1 += 1
            if l >= 4 and cnt[l, 0] + cnt[l, 1] + cnt[l, 2] >= 2:
                not2h += 1
        V[q, 0] = nit2; V[q, 1] = not2; V[q, 2] = nit2 + not2; V[q, 3] = not2h; V[q, 4] = nit2 + not2h
        V[q, 5] = nl1; V[q, 6] = chi2 / max(k - 2, 1); V[q, 7] = k
        V[q, 8] = np.std(wv) if k > 0 else np.nan
        V[q, 10] = nip2; V[q, 11] = n2s2; V[q, 14] = abs(n[2])
        if loose_only and not (nit2 >= 3 and nip2 >= 4):
            continue                     # w_core / chi2_core only needed for candidates passing the loosest rung
        if nip > 2:
            wi = wv[ip]
            cmed = np.median(wi)
            s = 1.4826 * np.median(np.abs(wi - cmed))
            V[q, 9] = s
            lo = cmed - 2.5 * s; hi = cmed + 2.5 * s
            M = np.zeros((3, 3)); ncore = 0
            for t in range(k):
                i = pid[hits[h0 + t]]
                if ip[t]:
                    inside = (wv[t] >= lo) and (wv[t] <= hi)
                else:
                    s2 = abs(n2v[2]) * S1[i]
                    inside = (wv[t] >= lo - 3 * s2) and (wv[t] <= hi + 3 * s2)
                if inside:
                    a = -n[0] * CY[i] + n[1] * CX[i]
                    sc = np.sqrt(a * a * S0[i] * S0[i] + n[2] * n[2] * S1[i] * S1[i])
                    sg = np.sqrt(max(sc, 1e-4) ** 2 + ttol * ttol)
                    w = 1.0 / (sg * sg)
                    for aa in range(3):
                        for bb in range(3):
                            M[aa, bb] += w * U[i, aa] * U[i, bb]
                    ncore += 1
            V[q, 13] = ncore
            if ncore >= 4:
                V[q, 12] = np.linalg.eigvalsh(M)[0] / max(ncore - 2, 1)
    return V


@njit(cache=True, error_model='numpy')
def seed_layer_mask(U, oa, ob, P, CS, bstart, ce, se, SF, SI, wc, ttol):
    """For each seed (a, b): bit k set iff layer k has >= 2 crossings in the seed band (reference seeds() counting)."""
    stamp = np.zeros(bstart.shape[0], np.int64)
    buf = np.empty(bstart.shape[0], np.int64)
    out = np.zeros(oa.shape[0], np.int64)
    qid = 0
    for s in range(oa.shape[0]):
        ia = oa[s]; ib = ob[s]
        uax = U[ia, 0]; uay = U[ia, 1]; uaz = U[ia, 2]
        ubx = U[ib, 0]; uby = U[ib, 1]; ubz = U[ib, 2]
        cx_ = uay * ubz - uaz * uby; cy_ = uaz * ubx - uax * ubz; cz_ = uax * uby - uay * ubx
        na = norm3(uax, uay, uaz); nbn = norm3(ubx, uby, ubz); ncn = norm3(cx_, cy_, cz_)
        sn = ncn / (na * nbn)
        nx = cx_ / ncn; ny = cy_ / ncn; nz = cz_ / ncn
        sseed = 0.03 / (nbn * sn)
        ax = uax / na + ubx / nbn; ay = uay / na + uby / nbn; az = uaz / na + ubz / nbn
        an = norm3(ax, ay, az); ax /= an; ay /= an; az /= an
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        msk = 0
        pa = np.arctan2(ay, ax)
        phn = np.arctan2(ny, nx)
        for k in range(10):
            j = LAYER_S0[k]
            qid += 1
            c = count_surface(j, 2, nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, P, CS, bstart, ce, se,
                              SF, SI, stamp, qid, buf, pa, phn)
            if k >= 4 and c >= 2:
                qid += 1
                c = min(c, count_surface(j + 1, 2, nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, P, CS,
                                         bstart, ce, se, SF, SI, stamp, qid, buf, pa, phn))
            if c >= 2:
                msk |= (1 << k)
        out[s] = msk
    return out


@njit(cache=True, error_model='numpy')
def seed_n2_exact(U, oa, ob, P, CS, bstart, ce, se, SF, SI, wc, ttol, tseed):
    """Exact seed N_L2 (no early termination) of the seeds (oa, ob): the reference seeds() value."""
    stamp = np.zeros(bstart.shape[0], np.int64)
    buf = np.empty(bstart.shape[0], np.int64)
    out = np.empty(oa.shape[0], np.int64)
    qid = 0
    for s in range(oa.shape[0]):
        ia = oa[s]; ib = ob[s]
        uax = U[ia, 0]; uay = U[ia, 1]; uaz = U[ia, 2]
        ubx = U[ib, 0]; uby = U[ib, 1]; ubz = U[ib, 2]
        cx_ = uay * ubz - uaz * uby; cy_ = uaz * ubx - uax * ubz; cz_ = uax * uby - uay * ubx
        na = norm3(uax, uay, uaz); nbn = norm3(ubx, uby, ubz); ncn = norm3(cx_, cy_, cz_)
        sn = ncn / (na * nbn)
        nx = cx_ / ncn; ny = cy_ / ncn; nz = cz_ / ncn
        sseed = 0.03 / (nbn * sn)
        ax = uax / na + ubx / nbn; ay = uay / na + uby / nbn; az = uaz / na + ubz / nbn
        an = norm3(ax, ay, az); ax /= an; ay /= an; az /= an
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        v, qid = seed_score(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, sseed, wc, ttol, tseed, False,
                            P, CS, bstart, ce, se, SF, SI, stamp, qid, buf, SEED_ORDER)
        out[s] = v
    return out


@njit(cache=True, error_model='numpy')
def chi2core_subsets(w, ip, s2, uu, hint, nint, nsub, q, seed):
    """G2b timing utility (plan §4.1 step 3b): chi2_core of nsub random interaction subsets (each interaction kept
    with probability q) of ONE stored candidate, plane and axis fixed.  Per subset the core is re-centred: c(T), w_core(T)
    = median / 1.4826 MAD of u.n2 over T's IT+PS hits; core = T's IT+PS hits within c +- 2.5 w_core, 2S hits within
    that interval +- s2 (3 sigma of their n2 projection); chi2_core = lambda_min(sum_core w u u^T) / (n_core - 2).
    Inputs per hit: w = u.n2, ip (IT/PS flag), s2, uu (6 weighted products xx, xy, xz, yy, yz, zz), hint (interaction
    index 0..nint-1).  Returns the chi2_core array (nan if < 3 IT+PS hits or < 4 core hits)."""
    np.random.seed(seed)
    nh = w.shape[0]
    out = np.full(nsub, np.nan)
    keepI = np.empty(nint, np.bool_)
    buf = np.empty(nh)
    M = np.empty((3, 3))
    for s in range(nsub):
        for i in range(nint):
            keepI[i] = np.random.random() < q
        nb = 0
        for h in range(nh):
            if keepI[hint[h]] and ip[h]:
                buf[nb] = w[h]
                nb += 1
        if nb < 3:
            continue
        c = np.median(buf[:nb])
        for t in range(nb):
            buf[t] = abs(buf[t] - c)
        wc = 1.4826 * np.median(buf[:nb])
        lo = c - 2.5 * wc; hi = c + 2.5 * wc
        a00 = 0.0; a01 = 0.0; a02 = 0.0; a11 = 0.0; a12 = 0.0; a22 = 0.0; nc = 0
        for h in range(nh):
            if not keepI[hint[h]]:
                continue
            if ip[h]:
                inn = (w[h] >= lo) and (w[h] <= hi)
            else:
                inn = (w[h] >= lo - s2[h]) and (w[h] <= hi + s2[h])
            if inn:
                a00 += uu[h, 0]; a01 += uu[h, 1]; a02 += uu[h, 2]; a11 += uu[h, 3]; a12 += uu[h, 4]; a22 += uu[h, 5]
                nc += 1
        if nc < 4:
            continue
        M[0, 0] = a00; M[0, 1] = a01; M[0, 2] = a02; M[1, 0] = a01; M[1, 1] = a11; M[1, 2] = a12
        M[2, 0] = a02; M[2, 1] = a12; M[2, 2] = a22
        out[s] = np.linalg.eigvalsh(M)[0] / max(nc - 2, 1)
    return out


@njit(cache=True, error_model='numpy')
def csr_hits(hoff, hits, kept, pid):
    """Phase A: road-hit lists of the kept candidates as one CSR, each list ascending (= find(want_hits) lists)."""
    n = kept.shape[0]
    off = np.zeros(n + 1, np.int64)
    for q in range(n):
        off[q + 1] = off[q] + hoff[kept[q] + 1] - hoff[kept[q]]
    out = np.empty(off[n], np.int64)
    for q in range(n):
        c = kept[q]
        k = hoff[c + 1] - hoff[c]
        for t in range(k):
            out[off[q] + t] = pid[hits[hoff[c] + t]]
        out[off[q]:off[q + 1]] = np.sort(out[off[q]:off[q + 1]])
    return off, out
