"""Occupancy model (STR §4.5 (b); COM B2-b) — hit-level kernels.  Phase 3, work package p3-b, executor Casper.

Configuration ensemble θ (the "ribbons through the vertex and along the road"): for a trial with PV pv and MET
direction phimet, a candidate plane is (axis a, normal n): axis azimuth φ_a = phimet + U(-0.15, 0.15) (the frozen road
δ95 = 0.15, |Δφ(n3, MET)| < δ95), axis pseudorapidity η_a ~ U(-1, 1) (|η(n3)| < 1), and n = cos ψ e1 + sin ψ e2 with
e1 = (-sin φ_a, cos φ_a, 0), e2 = a × e1, ψ ~ U(0, π) restricted to |n_z| = |sin ψ|/cosh η_a >= NZ_MIN = 0.2 (planes
that make at least 11.5° with the beam line; a model choice fixed here, before any rung is read).  The band of a plane
is the finder's (`kernels.refit_packed`): |u.n| < 3 σ(n) with σ² = max(sc, 1e-4)² + t_tol², sc² = a² s0² + n_z² s1²,
a = -n_x c_y + n_y c_x;  u.a > 0;  |u.n2| < w_c = 75 mm;  plus the road (finder.road_select).
Real-hit evaluation: the in-band hits of the replayed ρ = 1 finder pool are passed to thin_core._set_vars (the same
cand_vars arithmetic) -> counting rungs, w_core, chi2_core flags.
"""
import numpy as np
from numba import njit

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import thin_core as TC  # noqa: E402
from thin_core import FF  # noqa: E402

NZ_MIN = 0.2
ROAD = 0.15
WC = 75.0
TTOL = 0.030
JLOC_LC = np.array([0, 1, 2, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9], np.int64)
JLOC_SD = np.array([0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2], np.int64)
ZLO, ZHI, DZ = -1400.0, 1400.0, 2.0
NZB = int((ZHI - ZLO) / DZ)


def build_index(H, sid, nphi_mm=2.0):
    """Per local surface j (0..15): hits sorted by (phi bin, z).  Returns arrays for the numba kernels."""
    J = FF.JLOC_OF[sid]
    keep = J >= 0
    idx = np.where(keep)[0]
    J = J[idx]
    x = H[idx, 1]; y = H[idx, 2]; zz = H[idx, 3]
    phi = np.arctan2(y, x)
    R = FF.R_NOM
    nb = np.maximum(8, np.ceil(2 * np.pi * R / nphi_mm)).astype(np.int64)
    boff = np.concatenate([[0], np.cumsum(nb)])
    b = np.minimum(((phi + np.pi) / (2 * np.pi) * nb[J]).astype(np.int64), nb[J] - 1)
    gb = boff[J] + b
    order = np.lexsort((zz, gb))
    gbo = gb[order]
    bstart = np.searchsorted(gbo, np.arange(boff[-1] + 1)).astype(np.int64)
    hid = idx[order]
    s0 = np.zeros(16); s1 = np.zeros(16); rmin = R.copy(); rmax = R.copy()
    rr = np.hypot(x, y)
    for j in range(16):
        m = J == j
        if m.any():
            s0[j] = H[idx[m], 4][0]; s1[j] = H[idx[m], 5][0]
            rmin[j] = rr[m].min(); rmax[j] = rr[m].max()
    return dict(hid=hid.astype(np.int64), Z=zz[order].copy(), bstart=bstart, boff=boff.astype(np.int64),
                nb=nb, s0=s0, s1=s1, rr=np.c_[rmin - 0.5, rmax + 0.5])


@njit(cache=True)
def plane_from(phia, eta, psi):
    ch = np.cosh(eta)
    a = np.array([np.cos(phia) / ch, np.sin(phia) / ch, np.sinh(eta) / ch])
    e1 = np.array([-np.sin(phia), np.cos(phia), 0.0])
    e2 = np.array([a[1] * e1[2] - a[2] * e1[1], a[2] * e1[0] - a[0] * e1[2], a[0] * e1[1] - a[1] * e1[0]])
    n = np.cos(psi) * e1 + np.sin(psi) * e2
    return n, a


@njit(cache=True)
def band_hits(n, a, pv, phimet, H, hid, Z, bstart, boff, nb, Rn, s0, s1, out):
    """Rn: (16, 2) radial range [rmin, rmax] of each surface's hits (flat modules: r varies along phi)."""
    """In-band hit ids (rows of H) of plane (n, a) through pv: the finder band + the road.  Returns the count."""
    n2x = n[1] * a[2] - n[2] * a[1]; n2y = n[2] * a[0] - n[0] * a[2]; n2z = n[0] * a[1] - n[1] * a[0]
    nzabs = abs(n[2])
    pha = np.arctan2(a[1], a[0])
    m = 0
    for j in range(16):
        R = Rn[j, 0]
        R2 = Rn[j, 1]
        sgmax = np.sqrt(s0[j] ** 2 + s1[j] ** 2 + TTOL ** 2)
        dz = 3.0 * sgmax / nzabs + 1.0
        hw = np.arcsin(min(1.0, (WC + 5.0) / R)) + 0.02
        nbj = nb[j]
        bw = 2 * np.pi / nbj
        k0 = int(np.floor((pha - hw + np.pi) / bw))
        k1 = int(np.floor((pha + hw + np.pi) / bw))
        if k1 - k0 + 1 >= nbj or R < WC * 1.5:      # in-plane points can lie behind in azimuth below r ~ sqrt2 w_c
            k0 = 0; k1 = nbj - 1
        for kk in range(k0, k1 + 1):
            k = kk % nbj
            p0 = bstart[boff[j] + k]; p1 = bstart[boff[j] + k + 1]
            if p1 <= p0:
                continue
            fa = -np.pi + k * bw; fb = fa + bw
            zlo = 1e30; zhi = -1e30
            for rq in (R, R2):
                for fq in (fa, fb):
                    zq = pv[2] - (n[0] * (rq * np.cos(fq) - pv[0]) + n[1] * (rq * np.sin(fq) - pv[1])) / n[2]
                    zlo = min(zlo, zq); zhi = max(zhi, zq)
            zlo -= dz + 2.0 * R2 * bw * (abs(n[0]) + abs(n[1])) / nzabs
            zhi += dz + 2.0 * R2 * bw * (abs(n[0]) + abs(n[1])) / nzabs
            q0 = p0 + np.searchsorted(Z[p0:p1], zlo)
            q1 = p0 + np.searchsorted(Z[p0:p1], zhi)
            for q in range(q0, q1):
                i = hid[q]
                ux = H[i, 1] - pv[0]; uy = H[i, 2] - pv[1]; uz = H[i, 3] - pv[2]
                d = ux * n[0] + uy * n[1] + uz * n[2]
                r = np.hypot(H[i, 1], H[i, 2])
                cx = H[i, 1] / r; cy = H[i, 2] / r
                aa = -n[0] * cy + n[1] * cx
                sc2 = aa * aa * H[i, 4] * H[i, 4] + n[2] * n[2] * H[i, 5] * H[i, 5]
                if not (d * d < 9.0 * (max(sc2, 1e-8) + TTOL * TTOL)):
                    continue
                if not (ux * a[0] + uy * a[1] + uz * a[2] > 0):
                    continue
                if not (abs(ux * n2x + uy * n2y + uz * n2z) < WC):
                    continue
                r0 = np.hypot(ux, uy)
                dph = abs((np.arctan2(uy, ux) - phimet + np.pi) % (2 * np.pi) - np.pi)
                if not (dph < ROAD + np.arcsin(min(1.0, WC / r0))):
                    continue
                out[m] = i
                m += 1
    return m


@njit(cache=True)
def real_planes(H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb, Rn, s0, s1, pv, phimet, nplanes, seed,
                chi2isf, ncol):
    """Random-plane ensemble on one trial's real hits.  Returns
    cnt (ncol,) planes passing each thin_core column (R04 required), mask_hist (1024,) planes per 10-bit mask of layers
    with >= 2 crossings (all planes), nin (n,) number of in-band hits per plane (diagnostic sum), npl planes drawn."""
    np.random.seed(seed)
    cnt = np.zeros(ncol, np.int64)
    mh = np.zeros(1024, np.int64)
    out = np.empty(H.shape[0], np.int64)
    wbuf = np.empty(H.shape[0])
    res = np.zeros(7)
    fl = np.zeros(ncol, np.bool_)
    ntot = 0
    npl = 0
    while npl < nplanes:
        phia = phimet + ROAD * (2.0 * np.random.random() - 1.0)
        eta = 2.0 * np.random.random() - 1.0
        psi = np.pi * np.random.random()
        if abs(np.sin(psi)) / np.cosh(eta) < NZ_MIN:
            continue
        npl += 1
        n, a = plane_from(phia, eta, psi)
        m = band_hits(n, a, pv, phimet, H, hid, Z, bstart, boff, nb, Rn, s0, s1, out)
        ntot += m
        c3 = np.zeros((10, 3), np.int64)
        for t in range(m):
            c3[LC[out[t]], SD[out[t]]] += 1
        mask = 0
        for l in range(10):
            c = c3[l, 0] if l < 4 else min(c3[l, 1], c3[l, 2])
            if c >= 2:
                mask |= 1 << l
        mh[mask] += 1
        if (mask & 127) != 127:
            continue
        TC._set_vars(out, m, LC, SD, U, CX, CY, S0, S1, n, a, TTOL, chi2isf, wbuf, res)
        if res[0] >= 3 and res[1] >= 7:
            TC.col_flags(res[3], res[4] > 0.5, res[5] > 0.5, res[6] > 0.5, int(res[2]), fl)
            for j in range(ncol):
                if fl[j]:
                    cnt[j] += 1
    return cnt, mh, ntot


def trial_arrays(H, sid, pv):
    U = np.ascontiguousarray(H[:, 1:4] - pv[None, :])
    r = np.hypot(H[:, 1], H[:, 2])
    return dict(LC=np.maximum(FF.LC_OF[sid], 0).astype(np.int64), SD=FF.SIDE_OF[sid].astype(np.int64), U=U,
                CX=H[:, 1] / r, CY=H[:, 2] / r, S0=np.ascontiguousarray(H[:, 4]), S1=np.ascontiguousarray(H[:, 5]))


def z_hist(H, sid):
    """Per local surface j: counts of hits in z bins (ZLO..ZHI, DZ)."""
    J = FF.JLOC_OF[sid]
    m = J >= 0
    b = np.clip(((H[m, 3] - ZLO) / DZ).astype(np.int64), 0, NZB - 1)
    h = np.zeros((16, NZB), np.int64)
    np.add.at(h, (J[m], b), 1)
    return h
