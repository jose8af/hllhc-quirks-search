"""p3-f (investigator Jorunn): hit-level emulation of distinct finder-like groups from the frozen p3-b configuration
ensemble.  Method: `outputs/p3f/CAUSE_METHOD_jorunn.md` (sha256 in the session log).  Imports p3-b code, edits none.

Per configuration θ (frozen ensemble of `p3b/occ_core`):
  fixed map : the fixed ribbon of θ (occ_core.band_hits) -> layer counts, R04, w_core, flags (thin_core arithmetic).
  refit map : eligible if the fixed band has N_IT2 >= 3, N_IP2 >= NIP_ELIG; the finder's refit (thin_core._refit = the
              kernels.refit_packed arithmetic) from (n, a) of θ on the road hits within the finder's pre-filter
              |u.n0| < 5 mm (60 mm on 2S) of the starting normal; R04 also needs the aligned cuts on the refitted axis.
Basin volume V_r(θ): ensemble probability of {θ' : candidate(θ') passes r, shares >= 1/2 min(|S'|, |S|) hits with S(θ)},
by uniform local sampling in body-frame rotation coordinates ω = (ω_a, ω_2, ω_n) about (a, n2, n) of θ, weight
J(ω) cosh²η' 1_D(θ') / Vol(D)  (Haar density in exponential coordinates; dφ dη dψ = cosh²η dμ_Haar).
"""
import sys
from pathlib import Path

import numpy as np
from numba import njit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'p3b'))
import occ_core as OC  # noqa: E402
import thin_core as TC  # noqa: E402

ROAD = OC.ROAD
WC = OC.WC
TTOL = OC.TTOL
NZ_MIN = OC.NZ_MIN
ETA_MAX = 1.0                     # frozen_inputs.json eta_max
ITERS = 3                         # finder.Config.iters
# rungs carried in the volume / HT bookkeeping (indices into cols.COLS)
RL = np.array([0, 1, 2, 3, 13, 16, 19, 20], np.int64)     # R04 R05 R06 R07 R04x2S>=3 R05x2S>=3 R06x2S>=3 R07x2S>=3
NRL = RL.shape[0]


def vol_D():
    """Vol(D) = 0.3 * int_{-1}^{1} (pi - 2 arcsin(NZ_MIN cosh eta)) d eta  (Simpson, 20001 points)."""
    eta = np.linspace(-1.0, 1.0, 20001)
    f = np.pi - 2 * np.arcsin(np.minimum(1.0, NZ_MIN * np.cosh(eta)))
    h = eta[1] - eta[0]
    s = f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum()
    return 2 * ROAD * s * h / 3


def pre_of_surface():
    """finder pre-filter tolerance per local surface j: 60 mm on 2S (LC >= 7), else 5 mm (finder.find PRE)."""
    return np.where(OC.JLOC_LC >= 7, 60.0, 5.0)


@njit(cache=True)
def slab_hits(n, pv, phimet, H, hid, Z, bstart, boff, nb, Rn, prej, out):
    """Road hits with |u.n| < prej[j] (the finder's pre-filter w.r.t. the starting normal).  Returns the count."""
    nzabs = abs(n[2])
    m = 0
    for j in range(16):
        R = Rn[j, 0]
        R2 = Rn[j, 1]
        tol = prej[j]
        dz = tol / nzabs + 1.0
        hw = ROAD + np.arcsin(min(1.0, WC / max(R - 1.0, 1.0))) + 0.02
        nbj = nb[j]
        bw = 2 * np.pi / nbj
        k0 = int(np.floor((phimet - hw + np.pi) / bw))
        k1 = int(np.floor((phimet + hw + np.pi) / bw))
        if k1 - k0 + 1 >= nbj:
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
                if not (abs(d) < tol):
                    continue
                r0 = np.hypot(ux, uy)
                dph = abs((np.arctan2(uy, ux) - phimet + np.pi) % (2 * np.pi) - np.pi)
                if not (dph < ROAD + np.arcsin(min(1.0, WC / r0))):
                    continue
                out[m] = i
                m += 1
    return m


@njit(cache=True)
def layer_counts(hl, m, LC, SD):
    c3 = np.zeros((10, 3), np.int64)
    for t in range(m):
        c3[LC[hl[t]], SD[hl[t]]] += 1
    nit2 = 0; nip2 = 0
    for l in range(7):
        c = c3[l, 0] if l < 4 else min(c3[l, 1], c3[l, 2])
        if c >= 2:
            nip2 += 1
            if l < 4:
                nit2 += 1
    return nit2, nip2


@njit(cache=True)
def fixed_part(bufA, m, nit2, nip2, n, a, LC, SD, U, CX, CY, S0, S1, chi2isf, bufS, wbuf, res, fl):
    """Fixed map on a computed band bufA[:m]: R04 and flags.  Returns passes_R04 (bufS[:m] = the set)."""
    if not (nit2 >= 3 and nip2 >= 7):
        return False
    for t in range(m):
        bufS[t] = bufA[t]
    TC._set_vars(bufS, m, LC, SD, U, CX, CY, S0, S1, n, a, TTOL, chi2isf, wbuf, res)
    if res[0] >= 3 and res[1] >= 7:
        TC.col_flags(res[3], res[4] > 0.5, res[5] > 0.5, res[6] > 0.5, int(res[2]), fl)
        return True
    return False


@njit(cache=True)
def refit_part(n, a, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb, Rn, prej, chi2isf, bufB,
               bufS, wbuf, res, fl, nout):
    """Refit map from an eligible (n, a): returns (m, passes_R04, chi2ndf); bufS[:m] = the refitted candidate set."""
    k = slab_hits(n, pv, phimet, H, hid, Z, bstart, boff, nb, Rn, prej, bufB)
    mm, nn, aa, chi = TC._refit(bufB, k, U, CX, CY, S0, S1, n, a, TTOL, WC, ITERS, bufS)
    if mm < 4:
        return 0, False, 0.0
    nit2b, nip2b = layer_counts(bufS, mm, LC, SD)
    nout[0] = nip2b; nout[1] = mm
    if not (nit2b >= 3 and nip2b >= 7):
        return mm, False, chi
    dphi = abs((np.arctan2(aa[1], aa[0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    eta = np.arcsinh(aa[2] / max(np.hypot(aa[0], aa[1]), 1e-12))
    if not (dphi < ROAD and abs(eta) < ETA_MAX):
        return mm, False, chi
    TC._set_vars(bufS, mm, LC, SD, U, CX, CY, S0, S1, nn, aa, TTOL, chi2isf, wbuf, res)
    if res[0] >= 3 and res[1] >= 7:
        TC.col_flags(res[3], res[4] > 0.5, res[5] > 0.5, res[6] > 0.5, int(res[2]), fl)
        return mm, True, chi
    return mm, False, chi


@njit(cache=True)
def eval_cfg(n, a, mapk, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb, Rn, s0, s1, prej,
             chi2isf, nip_elig, bufA, bufB, bufS, wbuf, res, fl, nout):
    """Candidate of configuration (n, a) under map mapk (0 fixed, 1 refit): bufS[:m] = hit list, fl = column flags
    (all False if no R04 candidate).  Returns (m, passes_R04, eligible, chi2ndf)."""
    for k in range(fl.shape[0]):
        fl[k] = False
    m = OC.band_hits(n, a, pv, phimet, H, hid, Z, bstart, boff, nb, Rn, s0, s1, bufA)
    nit2, nip2 = layer_counts(bufA, m, LC, SD)
    nout[0] = nip2; nout[1] = m
    if mapk == 0:
        ok = fixed_part(bufA, m, nit2, nip2, n, a, LC, SD, U, CX, CY, S0, S1, chi2isf, bufS, wbuf, res, fl)
        return m, ok, True, 0.0
    if not (nit2 >= 3 and nip2 >= nip_elig):
        return 0, False, False, 0.0
    mm, ok, chi = refit_part(n, a, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb, Rn, prej,
                             chi2isf, bufB, bufS, wbuf, res, fl, nout)
    return mm, ok, True, chi


@njit(cache=True)
def rodrigues(w0, w1, w2):
    th = np.sqrt(w0 * w0 + w1 * w1 + w2 * w2)
    Rm = np.eye(3)
    if th < 1e-15:
        return Rm, 1.0
    kx = w0 / th; ky = w1 / th; kz = w2 / th
    K = np.array([[0.0, -kz, ky], [kz, 0.0, -kx], [-ky, kx, 0.0]])
    Rm = Rm + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)
    J = 2 * (1 - np.cos(th)) / (th * th)
    return Rm, J


NS_SCALE = 11         # nested boxes: base x 2^s, s = S_MIN .. S_MIN + NS_SCALE - 1, equal mixture weights
S_MIN = -6


@njit(cache=True)
def local_volume(n, a, S, mS, mapk, flags0, nloc, seed, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart,
                 boff, nb, Rn, s0, s1, prej, chi2isf, nip_elig, volD, stamp, sid_mark, bufA, bufB, bufS, wbuf, res,
                 fl, nout, maxdbl):
    """V_r(θ) for r in RL.  S[:mS] = candidate hits of θ.
    Local coordinates: c = (c1, c2, c3); (ω_a, ω_2) = c1 e1 + c2 e2 with (e1, e2) the eigenvectors of
    Q = Σ g g^T, g_i = (-w_i, ρ_i)/σ_i over the IP hits of S (Δd_i = -ω_a w_i + ω_2 ρ_i); ω_n = c3.
    Proposal: equal mixture of NS_SCALE nested uniform boxes, half-widths base_k 2^s, s = S_MIN..S_MIN+NS_SCALE-1, with
    base_j = 0.5 * 3 / median|g_i.e_j| (j = 1, 2) and base_3 = 0.5 * min(0.3, 75 mm / ρ75).  Estimator
    V = mean[w(θ') 1_member / q(c)], unbiased for any proposal that covers the neighbourhood.  Edge rule: a member
    beyond 0.75 of the largest box in coordinate k doubles base_k (fresh draws; <= maxdbl).  Boost: fewer than 3
    members at a rung θ passes -> nloc x 4 once.  Returns (V (NRL,), ndbl, edge, nmem_R04, base (3,))."""
    np.random.seed(seed)
    for t in range(mS):
        stamp[S[t]] = sid_mark
    n2 = np.array([n[1] * a[2] - n[2] * a[1], n[2] * a[0] - n[0] * a[2], n[0] * a[1] - n[1] * a[0]])
    rho = np.empty(mS); wv = np.empty(mS); sg = np.empty(mS); nip = 0
    for t in range(mS):
        i = S[t]
        if LC[i] <= 6:
            rho[nip] = U[i, 0] * a[0] + U[i, 1] * a[1] + U[i, 2] * a[2]
            wv[nip] = U[i, 0] * n2[0] + U[i, 1] * n2[1] + U[i, 2] * n2[2]
            aa = -n[0] * CY[i] + n[1] * CX[i]
            sc = np.sqrt(aa * aa * S0[i] * S0[i] + n[2] * n[2] * S1[i] * S1[i])
            sg[nip] = np.sqrt(max(sc, 1e-4) ** 2 + TTOL * TTOL)
            nip += 1
    Q = np.zeros((2, 2))
    for t in range(nip):
        g0 = -wv[t] / sg[t]; g1 = rho[t] / sg[t]
        Q[0, 0] += g0 * g0; Q[0, 1] += g0 * g1; Q[1, 1] += g1 * g1
    Q[1, 0] = Q[0, 1]
    ev, E = np.linalg.eigh(Q)
    base = np.zeros(3)
    for j in range(2):
        pr = np.empty(nip)
        for t in range(nip):
            pr[t] = abs((-wv[t] * E[0, j] + rho[t] * E[1, j]) / sg[t])
        base[j] = 0.5 * 3.0 / max(np.median(pr), 1e-3)
    r75 = np.percentile(rho[:nip], 75.0)
    base[2] = 0.5 * min(0.3, 75.0 / max(r75, 10.0))
    F = np.empty((3, 3))
    for c in range(3):
        F[c, 0] = a[c]; F[c, 1] = n2[c]; F[c, 2] = n[c]
    V = np.zeros(NRL)
    ndbl = 0
    edge = False
    nmem = 0
    boosted = False
    big = 2.0 ** (S_MIN + NS_SCALE - 1)
    while True:
        sums = np.zeros(NRL)
        cntk = np.zeros(NRL, np.int64)
        edge_c = np.zeros(3, np.bool_)
        nmem = 0
        vols = np.empty(NS_SCALE)
        for sc_ in range(NS_SCALE):
            vols[sc_] = 8 * base[0] * base[1] * base[2] * (2.0 ** (S_MIN + sc_)) ** 3
        for s in range(nloc):
            sc_ = np.random.randint(0, NS_SCALE)
            f = 2.0 ** (S_MIN + sc_)
            c1 = base[0] * f * (2 * np.random.random() - 1); c2 = base[1] * f * (2 * np.random.random() - 1)
            c3 = base[2] * f * (2 * np.random.random() - 1)
            # proposal density: boxes containing c
            q = 0.0
            for s2 in range(NS_SCALE):
                f2 = 2.0 ** (S_MIN + s2)
                if abs(c1) <= base[0] * f2 and abs(c2) <= base[1] * f2 and abs(c3) <= base[2] * f2:
                    q += 1.0 / (NS_SCALE * vols[s2])
            w0 = c1 * E[0, 0] + c2 * E[0, 1]; w1 = c1 * E[1, 0] + c2 * E[1, 1]; w2 = c3
            Rm, J = rodrigues(w0, w1, w2)
            G = F @ Rm
            ap = G[:, 0].copy(); np_ = G[:, 2].copy()
            ph = np.arctan2(ap[1], ap[0])
            et = np.arcsinh(ap[2] / max(np.hypot(ap[0], ap[1]), 1e-12))
            if abs((ph - phimet + np.pi) % (2 * np.pi) - np.pi) >= ROAD or abs(et) >= 1.0 or abs(np_[2]) < NZ_MIN:
                continue
            wt = J * np.cosh(et) ** 2 / volD / q
            mm, ok, el, chi = eval_cfg(np_, ap, mapk, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart,
                                       boff, nb, Rn, s0, s1, prej, chi2isf, nip_elig, bufA, bufB, bufS, wbuf, res,
                                       fl, nout)
            if not ok:
                continue
            ov = 0
            for t in range(mm):
                if stamp[bufS[t]] == sid_mark:
                    ov += 1
            if ov < 0.5 * min(mm, mS):
                continue
            nmem += 1
            if abs(c1) > 0.75 * big * base[0]:
                edge_c[0] = True
            if abs(c2) > 0.75 * big * base[1]:
                edge_c[1] = True
            if abs(c3) > 0.75 * big * base[2]:
                edge_c[2] = True
            for k in range(NRL):
                if fl[RL[k]] and flags0[RL[k]]:
                    sums[k] += wt
                    cntk[k] += 1
        if (edge_c[0] or edge_c[1] or edge_c[2]) and ndbl < maxdbl:
            for c in range(3):
                if edge_c[c]:
                    base[c] *= 2.0
            ndbl += 1
            continue
        few = False
        for k in range(NRL):
            if flags0[RL[k]] and cntk[k] < 3:
                few = True
        if few and not boosted:
            nloc *= 4
            boosted = True
            continue
        edge = edge_c[0] or edge_c[1] or edge_c[2]
        for k in range(NRL):
            V[k] = sums[k] / nloc
        break
    return V, ndbl, edge, nmem, base


@njit(cache=True)
def draw_cfg(phimet):
    while True:
        phia = phimet + ROAD * (2.0 * np.random.random() - 1.0)
        eta = 2.0 * np.random.random() - 1.0
        psi = np.pi * np.random.random()
        if abs(np.sin(psi)) / np.cosh(eta) >= NZ_MIN:
            return phia, eta, psi


@njit(cache=True)
def scan_trial(nplanes, seed, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb, Rn, s0, s1, prej,
               chi2isf, nip_elig, ncol, cap):
    """Pass 1: draw nplanes configurations; fixed and refit flags.  Returns
    cnt (2, ncol) passing configurations per column per map, nelig refit-eligible count,
    rec (cap, 4) [map, phia, eta, psi] of R04 passers (either map), recf (cap, ncol) their flags, nrec,
    aux (cap, 4) [cand N_IP2, |S|, chi2/ndf, fixed N_IP2], nip5 (count of refit R04 passers whose fixed N_IP2 == 5; 0 if nip_elig > 5)."""
    np.random.seed(seed)
    cnt = np.zeros((2, ncol), np.int64)
    cnt5 = np.zeros(ncol, np.int64)
    rec = np.zeros((cap, 4)); recf = np.zeros((cap, ncol), np.bool_); aux = np.zeros((cap, 4))
    nrec = 0
    nelig = 0
    nip5 = 0
    nh = H.shape[0]
    bufA = np.empty(nh, np.int64); bufB = np.empty(nh, np.int64); bufS = np.empty(nh, np.int64)
    wbuf = np.empty(nh); res = np.zeros(7); fl = np.zeros(ncol, np.bool_); nout = np.zeros(2, np.int64)
    for p in range(nplanes):
        phia, eta, psi = draw_cfg(phimet)
        n, a = OC.plane_from(phia, eta, psi)
        m = OC.band_hits(n, a, pv, phimet, H, hid, Z, bstart, boff, nb, Rn, s0, s1, bufA)
        nit2, nip2 = layer_counts(bufA, m, LC, SD)
        for mapk in range(2):
            for k in range(ncol):
                fl[k] = False
            chi = 0.0
            if mapk == 0:
                ok = fixed_part(bufA, m, nit2, nip2, n, a, LC, SD, U, CX, CY, S0, S1, chi2isf, bufS, wbuf, res, fl)
                nout[0] = nip2; nout[1] = m
            else:
                if not (nit2 >= 3 and nip2 >= nip_elig):
                    continue
                nelig += 1
                mm, ok, chi = refit_part(n, a, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb,
                                         Rn, prej, chi2isf, bufB, bufS, wbuf, res, fl, nout)
            if ok:
                for k in range(ncol):
                    if fl[k]:
                        cnt[mapk, k] += 1
                        if mapk == 1 and nip2 == 5:
                            cnt5[k] += 1
                if nrec >= cap:
                    raise RuntimeError('record capacity exceeded')
                rec[nrec, 0] = mapk; rec[nrec, 1] = phia; rec[nrec, 2] = eta; rec[nrec, 3] = psi
                for k in range(ncol):
                    recf[nrec, k] = fl[k]
                aux[nrec, 0] = nout[0]; aux[nrec, 1] = nout[1]; aux[nrec, 2] = chi; aux[nrec, 3] = nip2
                nrec += 1
                if mapk == 1 and nip2 == 5:
                    nip5 += 1
    return cnt, nelig, rec[:nrec], recf[:nrec], aux[:nrec], nip5, cnt5


@njit(cache=True)
def volumes(rec, recf, sel, nloc_v, seeds, maxdbl, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff,
            nb, Rn, s0, s1, prej, chi2isf, nip_elig, volD, ncol, want_sets):
    """Pass 2: V_r for the selected records sel (indices into rec).  Returns V (ns, NRL), ndbl, edge, nmem, h (ns, 3),
    and (want_sets) the candidate hit lists of the selected records as CSR (off, hits)."""
    ns = sel.shape[0]
    nh = H.shape[0]
    V = np.zeros((ns, NRL)); ND = np.zeros(ns, np.int64); ED = np.zeros(ns, np.bool_); NM = np.zeros(ns, np.int64)
    HB = np.zeros((ns, 3))
    stamp = np.full(nh, -1, np.int64)
    bufA = np.empty(nh, np.int64); bufB = np.empty(nh, np.int64); bufS = np.empty(nh, np.int64)
    S = np.empty(nh, np.int64)
    wbuf = np.empty(nh); res = np.zeros(7); fl = np.zeros(ncol, np.bool_); nout = np.zeros(2, np.int64)
    off = np.zeros(ns + 1, np.int64)
    tot = 0
    hits = np.empty(max(1, ns * 400 if want_sets else 1), np.int64)
    for q in range(ns):
        r = sel[q]
        mapk = int(rec[r, 0])
        n, a = OC.plane_from(rec[r, 1], rec[r, 2], rec[r, 3])
        mS, ok, el, chi = eval_cfg(n, a, mapk, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb,
                                   Rn, s0, s1, prej, chi2isf, nip_elig, bufA, bufB, bufS, wbuf, res, fl, nout)
        if not ok:
            raise RuntimeError('record does not reproduce')
        for t in range(mS):
            S[t] = bufS[t]
        if want_sets:
            if tot + mS > hits.shape[0]:
                h2 = np.empty(2 * (tot + mS), np.int64); h2[:tot] = hits[:tot]; hits = h2
            for t in range(mS):
                hits[tot + t] = S[t]
            tot += mS
            off[q + 1] = tot
        f0 = recf[r].copy()
        Vq, nd, ed, nm, hb = local_volume(n, a, S, mS, mapk, f0, nloc_v[q], seeds[q], pv, phimet, H, LC, SD, U, CX,
                                          CY, S0, S1, hid, Z, bstart, boff, nb, Rn, s0, s1, prej, chi2isf, nip_elig,
                                          volD, stamp, q, bufA, bufB, bufS, wbuf, res, fl, nout, maxdbl)
        V[q] = Vq; ND[q] = nd; ED[q] = ed; NM[q] = nm; HB[q] = hb
    return V, ND, ED, NM, HB, off, hits[:tot]


@njit(cache=True)
def sets_of(rec, sel, pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart, boff, nb, Rn, s0, s1, prej, chi2isf,
            nip_elig, ncol):
    """Candidate hit lists (CSR) of records sel (validation: recapture and saturation)."""
    ns = sel.shape[0]
    nh = H.shape[0]
    bufA = np.empty(nh, np.int64); bufB = np.empty(nh, np.int64); bufS = np.empty(nh, np.int64)
    wbuf = np.empty(nh); res = np.zeros(7); fl = np.zeros(ncol, np.bool_); nout = np.zeros(2, np.int64)
    off = np.zeros(ns + 1, np.int64)
    hits = np.empty(max(1, ns * 200), np.int64)
    tot = 0
    for q in range(ns):
        r = sel[q]
        n, a = OC.plane_from(rec[r, 1], rec[r, 2], rec[r, 3])
        mS, ok, el, chi = eval_cfg(n, a, int(rec[r, 0]), pv, phimet, H, LC, SD, U, CX, CY, S0, S1, hid, Z, bstart,
                                   boff, nb, Rn, s0, s1, prej, chi2isf, nip_elig, bufA, bufB, bufS, wbuf, res, fl,
                                   nout)
        if tot + mS > hits.shape[0]:
            h2 = np.empty(2 * (tot + mS), np.int64); h2[:tot] = hits[:tot]; hits = h2
        for t in range(mS):
            hits[tot + t] = bufS[t]
        tot += mS
        off[q + 1] = tot
    return off, hits[:tot]
