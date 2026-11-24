"""Semi-analytic occupancy model (STR §4.5 (b); COM B2-b) — the model kernels.  p3-b, executor Casper.

For a configuration θ of the ensemble of occ_core (PV, road, axis a, normal n) the model treats the hits of every barrel
surface j as a Poisson process with the MEASURED mean density ρ_j(z) of the ρ = 1 development pool (φ-uniform; hits per
mm² per event, the finder input after CKF removal and merging, top-up included).  The finder band of θ on surface j
(radius R_j) is, at azimuth φ, the z-interval |z - z*(φ)| < δ(φ) with
    z*(φ) = pv_z - [n_x (R cos φ - pv_x) + n_y (R sin φ - pv_y)] / n_z,      δ(φ) = 3 σ(φ) / |n_z|,
    σ² = max(sc², 1e-8) + t_tol²,  sc² = (-n_x sin φ + n_y cos φ)² s0_j² + n_z² s1_j²
(derivation: u.n = n_z (z - z*) at fixed φ, so |u.n| < 3σ  <=>  |z - z*| < 3σ/|n_z|), restricted to u.a > 0,
|u.n2| < 75 mm and the road.  The expected number of hits in an azimuth step Δφ is R Δφ ∫ ρ_j dz over the interval.
Stacked layers (in/out sensors at R_in < R_out): a crossing is a PAIR of hits at one (φ, z) (top-up by construction,
Fatras to the module tilt); pairs in both bands (b), in the in band only (i), in the out band only (o) are three
independent Poisson numbers with means from the pair density (ρ_in + ρ_out)/2 over the overlap and the two remainders.
Crossings of the layer = min(b + i, b + o) (cand_vars).  Then
    P(TBPX layer >= 2) = 1 - e^{-λ}(1 + λ);
    P(stacked >= 2) = P(b >= 2) + P(b = 1) P(i >= 1) P(o >= 1) + P(b = 0) P(i >= 2) P(o >= 2);
    R04: all 7 IP layers >= 2 (N_IP2 >= 7 implies N_IT2 = 4 >= 3);  N_2S2: Poisson-binomial of the three 2S layers.
Width rungs: w_core = 1.4826 MAD of the u.n2 positions of the pooled IP hits (pairs count twice): toys conditional on
R04 (counts drawn from the exact conditional law, positions from the band's position density); plain Monte Carlo and,
for the deep rungs, importance sampling of the positions (a window of half-width h = W/1.4826 at a centre c drawn
uniformly from a grid; each unit from the mixture (1 - β) g + β g·1_win/G(c); weight = g/proposal, exact).
"""
import numpy as np
from numba import njit

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import occ_core as OC  # noqa: E402

DPHI_MM = 0.5
KZ = np.array([1, 1, 1, 1, 3, 3, 3, 9, 9, 9], np.int64)   # sub-steps across the band (z): TBPX, PS, 2S
W_K = np.array([37.5, 18.75, 9.4, 4.7])
NCAT = 13          # IP categories: TBPX L1-L4 (4), then per PS layer (b, i, o)
MAXP = 60000


@njit(cache=True)
def _cdf_at(cdf, z):
    """cumulative ∫ρ dz (hits per mm of arc) at z; cdf on the edges ZLO + k DZ."""
    x = (z - OC.ZLO) / OC.DZ
    if x <= 0:
        return cdf[0]
    n = cdf.shape[0] - 1
    if x >= n:
        return cdf[n]
    k = int(x)
    f = x - k
    return cdf[k] * (1 - f) + cdf[k + 1] * f


@njit(cache=True)
def _ok(ux, uy, uz, a, n2, phimet):
    if ux * a[0] + uy * a[1] + uz * a[2] <= 0:
        return False
    if abs(ux * n2[0] + uy * n2[1] + uz * n2[2]) >= OC.WC:
        return False
    r0 = np.hypot(ux, uy)
    dph = abs((np.arctan2(uy, ux) - phimet + np.pi) % (2 * np.pi) - np.pi)
    return dph < OC.ROAD + np.arcsin(min(1.0, OC.WC / r0))


@njit(cache=True)
def _zstar(R, phi, n, pv):
    return pv[2] - (n[0] * (R * np.cos(phi) - pv[0]) + n[1] * (R * np.sin(phi) - pv[1])) / n[2]


@njit(cache=True)
def _delta(phi, n, s0, s1):
    sc2 = (-n[0] * np.sin(phi) + n[1] * np.cos(phi)) ** 2 * s0 * s0 + n[2] * n[2] * s1 * s1
    return 3.0 * np.sqrt(max(sc2, 1e-8) + OC.TTOL ** 2) / abs(n[2])


@njit(cache=True)
def _add_interval(R, phi, z1, z2, kz, cdf, dphi, pv, a, n2, phimet, R2, s_out, w_out, m):
    """Split [z1, z2] into kz pieces; per piece, if the point passes the band conditions at R (and at R2 if R2 > 0),
    append (s, expected hits).  Returns the new count."""
    if z2 <= z1:
        return m
    dz = (z2 - z1) / kz
    for q in range(kz):
        za = z1 + q * dz
        zc = za + 0.5 * dz
        ux = R * np.cos(phi) - pv[0]; uy = R * np.sin(phi) - pv[1]; uz = zc - pv[2]
        if not _ok(ux, uy, uz, a, n2, phimet):
            continue
        if R2 > 0:
            vx = R2 * np.cos(phi) - pv[0]; vy = R2 * np.sin(phi) - pv[1]
            if not _ok(vx, vy, uz, a, n2, phimet):
                continue
        w = R * dphi * (_cdf_at(cdf, za + dz) - _cdf_at(cdf, za))
        if w <= 0:
            continue
        s_out[m] = ux * n2[0] + uy * n2[1] + uz * n2[2]
        w_out[m] = w
        m += 1
    return m


@njit(cache=True)
def config_units(n, a, pv, phimet, R, s0, s1, CDF, CDFP, ip_only, S, Wt, off, lam):
    """Units of configuration θ.  R, s0, s1: per surface (16); CDF (16, nz+1) per surface; CDFP (3+3, nz+1) pair CDF per
    stacked layer (index l - 4).  Output: S, Wt (positions, expected hits) per category in CSR off (ncat + 1);
    categories 0-3 TBPX, then for each stacked layer l = 4..9: (b, i, o) -> cat 4 + 3 (l - 4) + {0, 1, 2}.
    lam (22,) = total expected units per category.  ip_only: skip the 2S layers."""
    n2 = np.array([n[1] * a[2] - n[2] * a[1], n[2] * a[0] - n[0] * a[2], n[0] * a[1] - n[1] * a[0]])
    pha = np.arctan2(a[1], a[0])
    m = 0
    off[0] = 0
    nl = 7 if ip_only else 10
    for l in range(nl):
        if l < 4:
            j = l
            Rj = R[j]
            if Rj < OC.WC * 1.5:
                f0 = -np.pi; f1 = np.pi
            else:
                hw = np.arcsin(min(1.0, (OC.WC + 5.0) / Rj)) + 0.02
                f0 = pha - hw; f1 = pha + hw
            nph = int(np.ceil((f1 - f0) * Rj / DPHI_MM))
            dphi = (f1 - f0) / nph
            for k in range(nph):
                phi = f0 + (k + 0.5) * dphi
                zs = _zstar(Rj, phi, n, pv)
                d = _delta(phi, n, s0[j], s1[j])
                m = _add_interval(Rj, phi, zs - d, zs + d, KZ[l], CDF[j], dphi, pv, a, n2, phimet, -1.0, S, Wt, m)
            off[l + 1] = m
        else:
            ji = 4 + 2 * (l - 4); jo = ji + 1
            Ri = R[ji]; Ro = R[jo]
            hw = np.arcsin(min(1.0, (OC.WC + 5.0) / Ri)) + 0.02
            f0 = pha - hw; f1 = pha + hw
            nph = int(np.ceil((f1 - f0) * Ri / DPHI_MM))
            dphi = (f1 - f0) / nph
            cp = CDFP[l - 4]
            base = 4 + 3 * (l - 4)
            # three passes so that each category is contiguous
            for cat in range(3):
                for k in range(nph):
                    phi = f0 + (k + 0.5) * dphi
                    zi = _zstar(Ri, phi, n, pv); di = _delta(phi, n, s0[ji], s1[ji])
                    zo = _zstar(Ro, phi, n, pv); do = _delta(phi, n, s0[jo], s1[jo])
                    lo = max(zi - di, zo - do); hi = min(zi + di, zo + do)
                    if cat == 0:
                        m = _add_interval(Ri, phi, lo, hi, KZ[l], cp, dphi, pv, a, n2, phimet, Ro, S, Wt, m)
                    elif cat == 1:
                        if hi > lo:
                            m = _add_interval(Ri, phi, zi - di, min(zi + di, lo), KZ[l], cp, dphi, pv, a, n2,
                                              phimet, -1.0, S, Wt, m)
                            m = _add_interval(Ri, phi, max(zi - di, hi), zi + di, KZ[l], cp, dphi, pv, a, n2,
                                              phimet, -1.0, S, Wt, m)
                        else:
                            m = _add_interval(Ri, phi, zi - di, zi + di, KZ[l], cp, dphi, pv, a, n2, phimet, -1.0,
                                              S, Wt, m)
                    else:
                        if hi > lo:
                            m = _add_interval(Ro, phi, zo - do, min(zo + do, lo), KZ[l], cp, dphi, pv, a, n2,
                                              phimet, -1.0, S, Wt, m)
                            m = _add_interval(Ro, phi, max(zo - do, hi), zo + do, KZ[l], cp, dphi, pv, a, n2,
                                              phimet, -1.0, S, Wt, m)
                        else:
                            m = _add_interval(Ro, phi, zo - do, zo + do, KZ[l], cp, dphi, pv, a, n2, phimet, -1.0,
                                              S, Wt, m)
                    if m > S.shape[0] - 100:
                        return -1
                off[base + cat + 1] = m
    ncat = 4 + 3 * (nl - 4)
    for c in range(ncat):
        t = 0.0
        for q in range(off[c], off[c + 1]):
            t += Wt[q]
        lam[c] = t
    return ncat


@njit(cache=True)
def _pge(lam, k):
    """P(Pois(lam) >= k) for k = 0, 1, 2."""
    if k <= 0:
        return 1.0
    e = np.exp(-lam)
    if k == 1:
        return 1.0 - e
    return 1.0 - e * (1.0 + lam)


@njit(cache=True)
def layer_probs(lam, pl):
    """pl (10,): P(layer >= 2 crossings) from the category means."""
    for l in range(4):
        pl[l] = _pge(lam[l], 2)
    for l in range(4, 10):
        c = 4 + 3 * (l - 4)
        lb = lam[c]; li = lam[c + 1]; lo = lam[c + 2]
        eb = np.exp(-lb)
        pl[l] = (1.0 - eb * (1.0 + lb)) + lb * eb * _pge(li, 1) * _pge(lo, 1) + eb * _pge(li, 2) * _pge(lo, 2)


@njit(cache=True)
def p2s(pl, k):
    """P(N_2S2 >= k) for the three 2S layers (Poisson-binomial)."""
    p = np.zeros(4)
    p[0] = 1.0
    for l in range(7, 10):
        q = pl[l]
        for t in range(3, 0, -1):
            p[t] = p[t] * (1 - q) + p[t - 1] * q
        p[0] = p[0] * (1 - q)
    s = 0.0
    for t in range(k, 4):
        s += p[t]
    return s


@njit(cache=True)
def _pois_trunc(lam, kmin):
    """Pois(lam) conditional on >= kmin (inverse CDF)."""
    if kmin <= 0:
        return np.random.poisson(lam)
    pk = np.exp(-lam)
    cum = 0.0
    tail = 1.0
    for k in range(kmin):
        tail -= pk
        pk *= lam / (k + 1)
    # pk now = P(N = kmin); tail = P(N >= kmin)
    u = np.random.random() * tail
    k = kmin
    while True:
        cum += pk
        if u <= cum or k > kmin + 1000:
            return k
        k += 1
        pk *= lam / k


@njit(cache=True)
def draw_counts(lam, cnt):
    """Counts per IP category conditional on R04 (every IP layer >= 2 crossings), exact conditional law."""
    for l in range(4):
        cnt[l] = _pois_trunc(lam[l], 2)
    for l in range(4, 7):
        c = 4 + 3 * (l - 4)
        lb = lam[c]; li = lam[c + 1]; lo = lam[c + 2]
        eb = np.exp(-lb)
        w2 = 1.0 - eb * (1.0 + lb)
        w1 = lb * eb * _pge(li, 1) * _pge(lo, 1)
        w0 = eb * _pge(li, 2) * _pge(lo, 2)
        u = np.random.random() * (w2 + w1 + w0)
        if u < w2:
            cnt[c] = _pois_trunc(lb, 2); cnt[c + 1] = np.random.poisson(li); cnt[c + 2] = np.random.poisson(lo)
        elif u < w2 + w1:
            cnt[c] = 1; cnt[c + 1] = _pois_trunc(li, 1); cnt[c + 2] = _pois_trunc(lo, 1)
        else:
            cnt[c] = 0; cnt[c + 1] = _pois_trunc(li, 2); cnt[c + 2] = _pois_trunc(lo, 2)


@njit(cache=True)
def _sample(cw, lo, hi):
    """index q in [lo, hi) with probability ∝ weight, cw cumulative (cw[q] = sum up to and including q)."""
    base = cw[lo - 1] if lo > 0 else 0.0
    u = base + np.random.random() * (cw[hi - 1] - base)
    q = np.searchsorted(cw[lo:hi], u) + lo
    return min(q, hi - 1)


@njit(cache=True)
def _wcore(x, nx):
    med = np.median(x[:nx])
    d = np.abs(x[:nx] - med)
    return 1.4826 * np.median(d)


@njit(cache=True)
def plain_toys(S, cw, off, lam, ntoy, out):
    """Plain Monte Carlo conditional on R04: out[k] += pass fraction of w_core < W_K[k] (k = 0..3)."""
    cnt = np.zeros(NCAT, np.int64)
    x = np.empty(4000)
    for t in range(ntoy):
        draw_counts(lam, cnt)
        nx = 0
        for c in range(NCAT):
            mult = 2 if (c >= 4 and (c - 4) % 3 == 0) else 1
            for u in range(cnt[c]):
                q = _sample(cw, off[c], off[c + 1])
                for mm in range(mult):
                    if nx < 4000:
                        x[nx] = S[q]
                        nx += 1
        w = _wcore(x, nx)
        for k in range(4):
            if w < W_K[k]:
                out[k] += 1.0 / ntoy


@njit(cache=True)
def is_toys(S, cw, off, lam, ntoy, k, beta, sorted_s, sorted_cw, sorted_idx, res):
    """Importance-sampled P(w_core < W_K[k] | R04, θ).  sorted_*: per category, positions sorted with cumulative
    weights (for window probabilities and window sampling).  res[0] += mean weight·pass, res[1] += mean (weight·pass)²
    (for the variance), res[2] += number of passing toys."""
    h = W_K[k] / 1.4826
    step = 0.5 * h
    M = int(np.ceil(160.0 / step))
    cs = np.empty(M)
    for i in range(M):
        cs[i] = -80.0 + (i + 0.5) * step
    G = np.zeros((M, NCAT))
    for c in range(NCAT):
        lo = off[c]; hi = off[c + 1]
        if hi <= lo:
            continue
        tot = sorted_cw[hi - 1] - (sorted_cw[lo - 1] if lo > 0 else 0.0)
        base = sorted_cw[lo - 1] if lo > 0 else 0.0
        ss = sorted_s[lo:hi]
        for i in range(M):
            a = np.searchsorted(ss, cs[i] - h) + lo
            b = np.searchsorted(ss, cs[i] + h) + lo
            wa = sorted_cw[a - 1] if a > lo else base
            wb = sorted_cw[b - 1] if b > lo else base
            G[i, c] = (wb - wa) / tot if tot > 0 else 0.0
    cnt = np.zeros(NCAT, np.int64)
    x = np.empty(4000)
    cat = np.empty(4000, np.int64)
    lw = np.empty(M)
    su = np.empty(4000)
    cu = np.empty(4000, np.int64)
    sw = 0.0; sw2 = 0.0; npass = 0
    for t in range(ntoy):
        draw_counts(lam, cnt)
        im = int(np.random.random() * M)
        c0 = cs[im]
        nx = 0
        nu = 0
        for c in range(NCAT):
            lo = off[c]; hi = off[c + 1]
            mult = 2 if (c >= 4 and (c - 4) % 3 == 0) else 1
            for u in range(cnt[c]):
                if G[im, c] > 0 and np.random.random() < beta:
                    base = sorted_cw[lo - 1] if lo > 0 else 0.0
                    a = np.searchsorted(sorted_s[lo:hi], c0 - h) + lo
                    b = np.searchsorted(sorted_s[lo:hi], c0 + h) + lo
                    wa = sorted_cw[a - 1] if a > lo else base
                    wb = sorted_cw[b - 1] if b > lo else base
                    uu = wa + np.random.random() * (wb - wa)
                    q = min(np.searchsorted(sorted_cw[a:b], uu) + a, b - 1)
                    s = sorted_s[q]
                else:
                    q = _sample(cw, lo, hi)
                    s = S[q]
                if nu < 4000:
                    su[nu] = s; cu[nu] = c; nu += 1
                for mm in range(mult):
                    if nx < 4000:
                        x[nx] = s
                        nx += 1
        w = _wcore(x, nx)
        if not (w < W_K[k]):
            continue
        # weight = 1 / mean_m prod_u [(1 - β_mu) + β_mu 1_win/G]
        for i in range(M):
            ls = 0.0
            for u in range(nu):
                g = G[i, cu[u]]
                if g > 0:
                    inw = abs(su[u] - cs[i]) < h
                    r = (1.0 - beta) + (beta / g if inw else 0.0)
                    ls += np.log(r)
            lw[i] = ls
        mx = lw.max()
        acc = 0.0
        for i in range(M):
            acc += np.exp(lw[i] - mx)
        logden = mx + np.log(acc / M)
        wt = np.exp(-logden)
        sw += wt; sw2 += wt * wt; npass += 1
    res[0] += sw / ntoy
    res[1] += sw2 / ntoy
    res[2] += npass
