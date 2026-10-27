"""In-job rho > 1 thinning weights (plan §4.1 step 2 and the step-3b method table), Phase A of Stage 4.

PU-only machinery; nothing here reads or uses signal.  All kernels are numba, batched over the candidate sets of one trial.

Definitions (plan §4.1 step 2).  A candidate found at density rho with in-band hit set H (interactions S) gets, for a rung r,
    w_r = sum_{T subset of S, T passes r} q^|T| (1 - q)^(|S| - |T|),   q = 1/rho
with the rho-level plane and axis fixed (no refit after thinning; plan step 3b).  Each top-up crossing is its own
interaction (it carries its own interaction id in INT).

1. Counting rungs (N_IT2, N_IP2, N_L2, N_2S2): EXACT, no Monte Carlo (`count_weights`).
   Per layer l the crossing count depends only on the capped per-sensor hit counts: TBPX layers c_l = n_l, stacked OT
   layers c_l = min(n_in, n_out); "c_l >= 2" depends only on (min(n_in, 2), min(n_out, 2)), a 9-state variable.
   Interactions whose hits lie in ONE layer ("single-layer") act independently per layer; the few interactions that hit
   >= 2 layers ("multi-layer"; M <= 10 on rho = 2 PU sets, median 2-3, data/acts_stage4/g2b) are enumerated exactly
   (2^M configurations).  For each configuration the layer outcomes are independent Bernoullis with
   p_l(b_l) = P(single-layer interactions of l bring the base state b_l to >= 2 crossings) (a 9-state DP per layer),
   and the joint law of (N_IT2, N_PS2, N_2S2) is their Poisson-binomial (an 80-cell table).  Exact up to float rounding.
2. Per-subset families (w_core, chi2_core, N_2S2 after the width/chi2 rungs, dE/dx; plan step 3b): importance sampling
   CONDITIONAL on the last counting rung N_IP2 >= 7 (= every IP layer has >= 2 crossings in the barrel)
   (`subset_weights`).  Multi-layer interactions are drawn from Bernoulli(q); each IP layer's single-layer interactions are
   then drawn exactly conditional on that layer reaching >= 2 crossings (forward sampling with the backward success
   table); 2S-layer single-layer interactions are drawn from Bernoulli(q).  The IS weight is
   W = prod_{l in IP} p_l(b_l) = P(N_IP2 >= 7 | multi-layer configuration), so  E[W f(T)] = E_q[1{N_IP2(T) >= 7} f(T)]
   (unbiased).  Per subset the core is re-centred (plan step 3b): c(T), w_core(T) = median, 1.4826 MAD of u.n2 over T's
   IT + PS hits; core(T) = T's IT + PS hits with |u.n2 - c| <= 2.5 w_core plus 2S hits within that interval +- 3 sigma of
   their n2 projection; chi2_core(T) = lambda_min(sum_core w u u^T), ndf = n_core - 2 (>= 2 required, i.e. n_core >= 4);
   p(chi2_core) > p_min  <=>  lambda_min < chi2.isf(p_min, ndf) (tabulated).  Same arithmetic as kernels.cand_vars.
   dE/dx(T) = truncated mean (lowest TRUNC_FRAC of the values) of the path-corrected dE of T's CORE IT (TBPX) hits
   (|u.n2 - c(T)| <= 2.5 w_core(T), the chi2_core core; review WP_RULE R1 B-1: the in-band estimator was diluted by PU),
   in units of mip_gev (WP_RULE.md §1.4; the pooled muon-gun MIP unit of the G1 V4-9 job).

Output columns of subset_weights (cumulative F0 ladder of plan §2.5 item 3 from rung 5 on, every column also requires
N_IT2 >= 3 and N_IP2 >= 7, i.e. counting rung 4):
    0-3  w_core < 37.5, 18.75, 9.4, 4.7 mm           (ladder rungs 5-8)
    4-6  ... and p(chi2_core) > 1e-3, 0.01, 0.05     (rungs 9-11)
    7-9  ... and N_2S2 >= 1, 2, 3                    (rungs 12-14 = full F0)
    10-12 full F0 and dE/dx > 1.3, 1.6, 2.0 MIP      (the F0 x dE/dx part of rungs 21-23; h and o are factorised at
                                                      rho = 1, plan step 3b, so they are not in the job)
    13-17 fallback F0 parts FB_k, k = 0..4: N_IP2 >= 7 and p > 0.05 and N_2S2 >= 3 and (w_core < W_k if k >= 1)
    18-32 FB_k and dE/dx > e, e in (1.3, 1.6, 2.0): column 18 + 3k + j
    33   the IS normalisation check: mean of W (estimates P(N_IP2 >= 7), compared with the exact DP)
"""
import numpy as np
from numba import njit
from scipy.stats import chi2 as _CHI2

# layer groups: 0-3 TBPX (IT), 4-6 TBPS (PS), 7-9 TB2S (2S)
GROUP = np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2], np.int64)
STACKED = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1], np.int64)
W_K = np.array([37.5, 18.75, 9.4, 4.7])            # mm, W_c / 2^k (plan §2.5 item 3)
P_MIN = np.array([1e-3, 0.01, 0.05])
E_MIN = np.array([1.3, 1.6, 2.0])                  # MIP units (plan §2.5 item 3, F1 e_min)
TRUNC_FRAC = 0.6                                   # WP_RULE.md §1.4: lowest 60 % of the core IT dE values
NDF_MAX = 4000
CHI2_ISF = np.array([[_CHI2.isf(p, d) if d >= 1 else 0.0 for d in range(NDF_MAX + 1)] for p in P_MIN])
N_SUB_OUT = 34
COUNT_COLS = ['IT2>=3&IP2>=4', 'IT2>=3&IP2>=5', 'IT2>=3&IP2>=6', 'IT2>=3&IP2>=7'] + \
             ['IT2>=3&L2>=%d' % L for L in (5, 6, 7, 8, 9, 10)] + ['IT2>=3&IP2>=7&2S2>=%d' % k for k in (1, 2, 3)]
SUB_COLS = (['w<37.5', 'w<18.75', 'w<9.4', 'w<4.7', 'p>1e-3', 'p>0.01', 'p>0.05', '2S2>=1', '2S2>=2', '2S2>=3',
             'F0&e>1.3', 'F0&e>1.6', 'F0&e>2.0'] + ['FB%d' % k for k in range(5)] +
            ['FB%d&e>%g' % (k, e) for k in range(5) for e in (1.3, 1.6, 2.0)] + ['meanW'])


@njit(cache=True)
def _add(s, a):
    """capped add of two 9-states s = 3*min(n_in,2) + min(n_out,2) (single-sensor layers use n_in only)."""
    i = min(s // 3 + a // 3, 2)
    o = min(s % 3 + a % 3, 2)
    return 3 * i + o


@njit(cache=True)
def _succ(s, stacked):
    if stacked:
        return (s // 3) >= 2 and (s % 3) >= 2
    return (s // 3) >= 2


@njit(cache=True)
def _prep_set(h, LC, SD, INTl, slot, stamp, tag, jlist, cst, lmask):
    """Map the set's hits to local interactions 0..m-1; per interaction the capped 9-state contribution per layer
    (cst[j, l]) and its layer bitmask.  Returns m."""
    m = 0
    for t in range(h.shape[0]):
        g = INTl[h[t]]
        if stamp[g] != tag:
            stamp[g] = tag
            slot[g] = m
            jlist[m] = g
            for l in range(10):
                cst[m, l] = 0
            lmask[m] = 0
            m += 1
        j = slot[g]
        l = LC[h[t]]
        if STACKED[l] and SD[h[t]] == 2:
            cst[j, l] = _add(cst[j, l], 1)          # out sensor
        else:
            cst[j, l] = _add(cst[j, l], 3)          # TBPX hit or stacked in sensor
        lmask[j] |= (1 << l)
    return m


@njit(cache=True)
def _layer_tables(m, cst, lmask, q, single_of, nsingle, multi, P_l, dist):
    """Single-layer DPs.  single_of[l, :nsingle[l]] = single-layer interactions of l; multi = multi-layer list.
    P_l[l, b] = P(layer l reaches >= 2 crossings | base 9-state b).  Returns M."""
    for l in range(10):
        nsingle[l] = 0
    M = 0
    for j in range(m):
        mk = lmask[j]
        c = 0
        last = -1
        for l in range(10):
            if (mk >> l) & 1:
                c += 1
                last = l
        if c >= 2:
            multi[M] = j
            M += 1
        elif c == 1:
            single_of[last, nsingle[last]] = j
            nsingle[last] += 1
    tmp = np.empty(9)
    for l in range(10):
        for s in range(9):
            dist[s] = 0.0
        dist[0] = 1.0
        for k in range(nsingle[l]):
            a = cst[single_of[l, k], l]
            for s in range(9):
                tmp[s] = dist[s] * (1.0 - q)
            for s in range(9):
                if dist[s] != 0.0:
                    tmp[_add(s, a)] += dist[s] * q
            for s in range(9):
                dist[s] = tmp[s]
        for b in range(9):
            p = 0.0
            for s in range(9):
                if dist[s] != 0.0 and _succ(_add(b, s), STACKED[l]):
                    p += dist[s]
            P_l[l, b] = p
    return M


@njit(cache=True)
def _conv(T, g, p):
    """T (5, 4, 4) Poisson-binomial table over (nIT, nPS, n2S); multiply in a Bernoulli(p) for group g, in place."""
    if g == 0:
        for a in range(4, 0, -1):
            for b in range(4):
                for c in range(4):
                    T[a, b, c] = T[a, b, c] * (1 - p) + T[a - 1, b, c] * p
        for b in range(4):
            for c in range(4):
                T[0, b, c] *= (1 - p)
    elif g == 1:
        for a in range(5):
            for b in range(3, 0, -1):
                for c in range(4):
                    T[a, b, c] = T[a, b, c] * (1 - p) + T[a, b - 1, c] * p
            for c in range(4):
                T[a, 0, c] *= (1 - p)
    else:
        for a in range(5):
            for b in range(4):
                for c in range(3, 0, -1):
                    T[a, b, c] = T[a, b, c] * (1 - p) + T[a, b, c - 1] * p
                T[a, b, 0] *= (1 - p)


@njit(cache=True)
def count_weights(hoff, hits, sel, LC, SD, INTl, nI, q, MMAX):
    """Exact counting-rung weights for the sets sel (rows of the CSR (hoff, hits) of road-hit indices).
    INTl: dense interaction index (0..nI-1) per road hit.  Returns (W (ns, 13) with COUNT_COLS, info (ns, 3) = m, M,
    flag) where flag = 1 if M > MMAX (then W is NaN and the caller must fall back; never seen)."""
    ns = sel.shape[0]
    W = np.full((ns, 13), np.nan)
    info = np.zeros((ns, 3), np.int64)
    slot = np.zeros(nI, np.int64)
    stamp = np.full(nI, -1, np.int64)
    jlist = np.empty(nI, np.int64)
    maxh = 0
    for s in range(ns):
        maxh = max(maxh, hoff[sel[s] + 1] - hoff[sel[s]])
    cst = np.zeros((maxh, 10), np.int64)
    lmask = np.zeros(maxh, np.int64)
    single_of = np.zeros((10, maxh), np.int64)
    nsingle = np.zeros(10, np.int64)
    multi = np.zeros(maxh, np.int64)
    P_l = np.zeros((10, 9))
    dist = np.zeros(9)
    T0 = np.zeros((5, 4, 4))
    T = np.zeros((5, 4, 4))
    A = np.zeros((5, 4, 4))
    base = np.zeros(10, np.int64)
    for s in range(ns):
        c = sel[s]
        h = hits[hoff[c]:hoff[c + 1]]
        m = _prep_set(h, LC, SD, INTl, slot, stamp, s, jlist, cst, lmask)
        M = _layer_tables(m, cst, lmask, q, single_of, nsingle, multi, P_l, dist)
        info[s, 0] = m
        info[s, 1] = M
        if M > MMAX:
            info[s, 2] = 1
            continue
        touched = 0
        for k in range(M):
            touched |= lmask[multi[k]]
        T0[:, :, :] = 0.0
        T0[0, 0, 0] = 1.0
        for l in range(10):
            if not (touched >> l) & 1:
                _conv(T0, GROUP[l], P_l[l, 0])
        A[:, :, :] = 0.0
        for cfg in range(1 << M):
            pr = 1.0
            for l in range(10):
                base[l] = 0
            for k in range(M):
                j = multi[k]
                if (cfg >> k) & 1:
                    pr *= q
                    for l in range(10):
                        if (lmask[j] >> l) & 1:
                            base[l] = _add(base[l], cst[j, l])
                else:
                    pr *= (1.0 - q)
            if pr == 0.0:
                continue
            T[:, :, :] = T0
            for l in range(10):
                if (touched >> l) & 1:
                    _conv(T, GROUP[l], P_l[l, base[l]])
            for a in range(5):
                for b in range(4):
                    for cc in range(4):
                        A[a, b, cc] += pr * T[a, b, cc]
        # rung probabilities
        for k in range(4):
            v = 0.0
            for a in range(3, 5):
                for b in range(4):
                    if a + b >= 4 + k:
                        for cc in range(4):
                            v += A[a, b, cc]
            W[s, k] = v
        for i in range(6):
            L = 5 + i
            v = 0.0
            for a in range(3, 5):
                for b in range(4):
                    for cc in range(4):
                        if a + b + cc >= L:
                            v += A[a, b, cc]
            W[s, 4 + i] = v
        for k in range(3):
            v = 0.0
            for cc in range(k + 1, 4):
                v += A[4, 3, cc]
            W[s, 10 + k] = v
    return W, info


@njit(cache=True)
def _lam_min(a00, a01, a02, a11, a12, a22):
    """Smallest eigenvalue of a symmetric 3x3 (closed form, trigonometric; relative accuracy ~1e-12 here)."""
    p1 = a01 * a01 + a02 * a02 + a12 * a12
    qq = (a00 + a11 + a22) / 3.0
    if p1 == 0.0:
        return min(a00, min(a11, a22))
    p2 = (a00 - qq) ** 2 + (a11 - qq) ** 2 + (a22 - qq) ** 2 + 2.0 * p1
    p = np.sqrt(p2 / 6.0)
    b00 = (a00 - qq) / p; b11 = (a11 - qq) / p; b22 = (a22 - qq) / p
    b01 = a01 / p; b02 = a02 / p; b12 = a12 / p
    detb = b00 * (b11 * b22 - b12 * b12) - b01 * (b01 * b22 - b12 * b02) + b02 * (b01 * b12 - b11 * b02)
    r = detb / 2.0
    if r <= -1.0:
        phi = np.pi / 3.0
    elif r >= 1.0:
        phi = 0.0
    else:
        phi = np.arccos(r) / 3.0
    return qq + 2.0 * p * np.cos(phi + 2.0 * np.pi / 3.0)


@njit(cache=True)
def _trunc_mean(v, n, frac):
    if n < 1:
        return np.nan
    x = np.sort(v[:n])
    k = int(np.ceil(frac * n))
    k = max(1, min(k, n))
    return x[:k].mean()


@njit(cache=True)
def subset_weights(hoff, hits, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, dEc, NRM, AXS, q, nsub, seed, ttol, mip,
                   chi2isf, MMAX):
    """Per-subset family weights (SUB_COLS) for the sets sel, importance-sampled conditional on N_IP2 >= 7.
    dEc: path-corrected dE per road hit (GeV); mip: MIP unit (GeV); mip <= 0 -> dE/dx columns NaN.
    Returns (Wm (ns, 34) means, Wv (ns, 34) variances of the means, nzero (ns,) draws with W = 0)."""
    e = np.zeros(1, np.int64)
    Wm, Wv, nzero, _, _ = _subset_core(hoff, hits, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, dEc, NRM, AXS, q, nsub,
                                       seed, ttol, mip, chi2isf, MMAX, e, e, False)
    return Wm, Wv, nzero


@njit(cache=True)
def subset_weights_btl(hoff, hits, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, dEc, NRM, AXS, q, nsub, seed, ttol, mip,
                       chi2isf, MMAX, boffC, bintC):
    """subset_weights plus the SR-T BTL-presence columns (WP_RULE.md §1.4 SR-T in-job first factor, review WP_RULE R2
    B-2): (Wm, Wv, nzero) bit-identical to subset_weights (same draws; the BTL factor consumes no random number) and
    (WmT, WvT) = the same columns AND >= 1 in-band BTL hit in the thinned subset.
    boffC/bintC: per CANDIDATE (indexed by the candidate id c = sel[s], not by s) CSR of the distinct interactions of the
    candidate's in-band BTL hits (btl_band), in the combined numbering: g < nI = the road-hit interaction INTl index,
    g >= nI = an interaction with no road hit.  Per subset T the factor is
        f(T) = 1                              if T keeps an interaction of S with an in-band BTL hit,
             = 1 - (1 - q)^n_only             otherwise,
    n_only = the number of in-band BTL interactions NOT in S (independent of T: their Bernoulli(q) draw is integrated
    analytically, Rao-Blackwell), so E[W f(T) flag_r(T)] = P_q(T passes r and >= 1 in-band BTL interaction kept)."""
    return _subset_core(hoff, hits, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, dEc, NRM, AXS, q, nsub, seed, ttol, mip,
                        chi2isf, MMAX, boffC, bintC, True)


@njit(cache=True)
def _subset_core(hoff, hits, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, dEc, NRM, AXS, q, nsub, seed, ttol, mip,
                 chi2isf, MMAX, boffC, bintC, want_btl):
    np.random.seed(seed)
    ns = sel.shape[0]
    Wm = np.zeros((ns, N_SUB_OUT))
    Wv = np.zeros((ns, N_SUB_OUT))
    nzero = np.zeros(ns, np.int64)
    nT = ns if want_btl else 0
    WmT = np.zeros((nT, N_SUB_OUT))
    WvT = np.zeros((nT, N_SUB_OUT))
    slot = np.zeros(nI, np.int64)
    stamp = np.full(nI, -1, np.int64)
    jlist = np.empty(nI, np.int64)
    maxh = 0
    for s in range(ns):
        maxh = max(maxh, hoff[sel[s] + 1] - hoff[sel[s]])
    cst = np.zeros((maxh, 10), np.int64)
    lmask = np.zeros(maxh, np.int64)
    single_of = np.zeros((10, maxh), np.int64)
    nsingle = np.zeros(10, np.int64)
    multi = np.zeros(maxh, np.int64)
    P_l = np.zeros((10, 9))
    dist = np.zeros(9)
    G = np.zeros((10, maxh + 1, 9))                 # backward success tables of the IP layers
    keep = np.zeros(maxh, np.bool_)
    jb = np.zeros(maxh, np.bool_)                   # local interaction carries an in-band BTL hit (want_btl)
    pnone = 1.0
    fT = 1.0
    hj = np.zeros(maxh, np.int64)
    hw = np.zeros(maxh); hip = np.zeros(maxh, np.bool_); hs2 = np.zeros(maxh); hit_ = np.zeros(maxh, np.bool_)
    huu = np.zeros((maxh, 6)); hde = np.zeros(maxh); hl = np.zeros(maxh, np.int64); hsd = np.zeros(maxh, np.int64)
    buf = np.zeros(maxh); dbuf = np.zeros(maxh)
    base = np.zeros(10, np.int64)
    flags = np.zeros(N_SUB_OUT)
    in2 = np.zeros(3, np.int64); out2 = np.zeros(3, np.int64)
    pk = np.zeros(3, np.bool_)
    for s in range(ns):
        c = sel[s]
        h = hits[hoff[c]:hoff[c + 1]]
        nh = h.shape[0]
        m = _prep_set(h, LC, SD, INTl, slot, stamp, s, jlist, cst, lmask)
        M = _layer_tables(m, cst, lmask, q, single_of, nsingle, multi, P_l, dist)
        if M > MMAX:
            for k in range(N_SUB_OUT):
                Wm[s, k] = np.nan
                if want_btl:
                    WmT[s, k] = np.nan
            continue
        if want_btl:
            for j in range(m):
                jb[j] = False
            nonly = 0
            for kb in range(boffC[c], boffC[c + 1]):
                g = bintC[kb]
                if g < nI and stamp[g] == s:        # interaction of S (stamped by _prep_set with tag s)
                    jb[slot[g]] = True
                else:
                    nonly += 1
            pnone = (1.0 - q) ** nonly
        # backward tables for the IP layers: G[l, k, st] = P(layer ok | state after the first k singles is st)
        for l in range(7):
            n_l = nsingle[l]
            for st in range(9):
                G[l, n_l, st] = 1.0 if _succ(st, STACKED[l]) else 0.0
            for k in range(n_l - 1, -1, -1):
                a = cst[single_of[l, k], l]
                for st in range(9):
                    G[l, k, st] = q * G[l, k + 1, _add(st, a)] + (1.0 - q) * G[l, k + 1, st]
        # per-hit quantities (plane and axis fixed)
        nx = NRM[c, 0]; ny = NRM[c, 1]; nz = NRM[c, 2]
        ax = AXS[c, 0]; ay = AXS[c, 1]; az = AXS[c, 2]
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        for t in range(nh):
            i = h[t]
            hj[t] = slot[INTl[i]]
            hl[t] = LC[i]; hsd[t] = SD[i]
            hw[t] = U[i, 0] * n2x + U[i, 1] * n2y + U[i, 2] * n2z
            hip[t] = LC[i] <= 6
            hit_[t] = LC[i] <= 3
            hs2[t] = 3.0 * abs(n2z) * S1[i]
            aa = -nx * CY[i] + ny * CX[i]
            sc = np.sqrt(aa * aa * S0[i] * S0[i] + nz * nz * S1[i] * S1[i])
            sg = np.sqrt(max(sc, 1e-4) ** 2 + ttol * ttol)
            w = 1.0 / (sg * sg)
            huu[t, 0] = w * U[i, 0] * U[i, 0]; huu[t, 1] = w * U[i, 0] * U[i, 1]; huu[t, 2] = w * U[i, 0] * U[i, 2]
            huu[t, 3] = w * U[i, 1] * U[i, 1]; huu[t, 4] = w * U[i, 1] * U[i, 2]; huu[t, 5] = w * U[i, 2] * U[i, 2]
            hde[t] = dEc[i]
        for d in range(nsub):
            # multi-layer interactions ~ Bernoulli(q)
            for l in range(10):
                base[l] = 0
            for j in range(m):
                keep[j] = False
            for k in range(M):
                j = multi[k]
                if np.random.random() < q:
                    keep[j] = True
                    for l in range(10):
                        if (lmask[j] >> l) & 1:
                            base[l] = _add(base[l], cst[j, l])
            Wt = 1.0
            for l in range(7):
                Wt *= P_l[l, base[l]]
            if Wt == 0.0:
                nzero[s] += 1
                continue
            # IP layers: singles conditional on success; 2S layers: singles ~ Bernoulli(q)
            for l in range(7):
                st = base[l]
                for k in range(nsingle[l]):
                    j = single_of[l, k]
                    a = cst[j, l]
                    sa = _add(st, a)
                    pin = q * G[l, k + 1, sa]
                    den = pin + (1.0 - q) * G[l, k + 1, st]
                    if np.random.random() * den < pin:
                        keep[j] = True
                        st = sa
            for l in range(7, 10):
                for k in range(nsingle[l]):
                    if np.random.random() < q:
                        keep[single_of[l, k]] = True
            # evaluate the subset
            nb = 0
            ndE = 0
            for k in range(3):
                in2[k] = 0; out2[k] = 0; pk[k] = False
            for t in range(nh):
                if not keep[hj[t]]:
                    continue
                if hip[t]:
                    buf[nb] = hw[t]
                    nb += 1
                if hl[t] >= 7:
                    if hsd[t] == 2:
                        out2[hl[t] - 7] += 1
                    else:
                        in2[hl[t] - 7] += 1
            n2s2 = 0
            for k in range(3):
                if min(in2[k], out2[k]) >= 2:
                    n2s2 += 1
            for k in range(N_SUB_OUT):
                flags[k] = 0.0
            if nb >= 3:
                cmed = np.median(buf[:nb])
                for t in range(nb):
                    buf[t] = abs(buf[t] - cmed)
                wcore = 1.4826 * np.median(buf[:nb])
                lo = cmed - 2.5 * wcore; hi = cmed + 2.5 * wcore
                a00 = 0.0; a01 = 0.0; a02 = 0.0; a11 = 0.0; a12 = 0.0; a22 = 0.0; ncore = 0
                for t in range(nh):
                    if not keep[hj[t]]:
                        continue
                    if hip[t]:
                        inn = (hw[t] >= lo) and (hw[t] <= hi)
                    else:
                        inn = (hw[t] >= lo - hs2[t]) and (hw[t] <= hi + hs2[t])
                    if inn:
                        a00 += huu[t, 0]; a01 += huu[t, 1]; a02 += huu[t, 2]
                        a11 += huu[t, 3]; a12 += huu[t, 4]; a22 += huu[t, 5]
                        ncore += 1
                        if hit_[t]:                 # dE/dx: core IT hits only (review WP_RULE R1 B-1)
                            dbuf[ndE] = hde[t]
                            ndE += 1
                if ncore >= 4:
                    lam = _lam_min(a00, a01, a02, a11, a12, a22)
                    ndf = min(ncore - 2, NDF_MAX)
                    for k in range(3):
                        pk[k] = lam < chi2isf[k, ndf]
                ede = np.nan
                if mip > 0.0:
                    ede = _trunc_mean(dbuf, ndE, TRUNC_FRAC) / mip
                # cumulative ladder (rungs 5-14)
                ok = True
                for k in range(4):
                    ok = ok and (wcore < W_K[k])
                    flags[k] = 1.0 if ok else 0.0
                for k in range(3):
                    ok = ok and pk[k]
                    flags[4 + k] = 1.0 if ok else 0.0
                for k in range(3):
                    ok = ok and (n2s2 >= k + 1)
                    flags[7 + k] = 1.0 if ok else 0.0
                for k in range(3):
                    flags[10 + k] = 1.0 if (ok and ede > E_MIN[k]) else 0.0
                fb0 = pk[2] and (n2s2 >= 3)
                for kk in range(5):
                    fk = fb0 and (kk == 0 or wcore < W_K[kk - 1])
                    flags[13 + kk] = 1.0 if fk else 0.0
                    for e in range(3):
                        flags[18 + 3 * kk + e] = 1.0 if (fk and ede > E_MIN[e]) else 0.0
            flags[33] = 1.0
            for k in range(N_SUB_OUT):
                if flags[k] != 0.0:
                    Wm[s, k] += Wt
                    Wv[s, k] += Wt * Wt
            if want_btl:
                fT = 1.0 - pnone
                for j in range(m):
                    if jb[j] and keep[j]:
                        fT = 1.0
                        break
                wf = Wt * fT
                for k in range(N_SUB_OUT):
                    if flags[k] != 0.0:
                        WmT[s, k] += wf
                        WvT[s, k] += wf * wf
        for k in range(N_SUB_OUT):
            mu = Wm[s, k] / nsub
            Wv[s, k] = max(Wv[s, k] / nsub - mu * mu, 0.0) / nsub
            Wm[s, k] = mu
            if want_btl:
                mu = WmT[s, k] / nsub
                WvT[s, k] = max(WvT[s, k] / nsub - mu * mu, 0.0) / nsub
                WmT[s, k] = mu
        if mip <= 0.0:
            for k in (10, 11, 12):
                Wm[s, k] = np.nan
                if want_btl:
                    WmT[s, k] = np.nan
            for k in range(18, 33):
                Wm[s, k] = np.nan
                if want_btl:
                    WmT[s, k] = np.nan
    return Wm, Wv, nzero, WmT, WvT


# ----------------------------------------------------------------------------------------------- plain-MC references
@njit(cache=True)
def count_weights_mc(hoff, hits, sel, LC, SD, INTl, nI, q, nmc, seed):
    """Plain Monte Carlo reference for count_weights (independent draws per set; the f1r thin_weights method with the
    ladder columns added).  Returns the MC estimates (ns, 13)."""
    np.random.seed(seed)
    ns = sel.shape[0]
    W = np.zeros((ns, 13))
    slot = np.zeros(nI, np.int64)
    stamp = np.full(nI, -1, np.int64)
    keepI = np.zeros(nI, np.bool_)
    for s in range(ns):
        c = sel[s]
        h = hits[hoff[c]:hoff[c + 1]]
        m = 0
        for t in range(h.shape[0]):
            g = INTl[h[t]]
            if stamp[g] != s:
                stamp[g] = s
                slot[g] = m
                m += 1
        loc = np.empty(h.shape[0], np.int64)
        for t in range(h.shape[0]):
            loc[t] = slot[INTl[h[t]]]
        kp = np.zeros(m, np.bool_)
        for d in range(nmc):
            for j in range(m):
                kp[j] = np.random.random() < q
            cnt = np.zeros((10, 3), np.int64)
            for t in range(h.shape[0]):
                if kp[loc[t]]:
                    cnt[LC[h[t]], SD[h[t]]] += 1
            nit = 0; nps = 0; n2s = 0
            for l in range(10):
                cr = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
                if cr >= 2:
                    if l < 4:
                        nit += 1
                    elif l < 7:
                        nps += 1
                    else:
                        n2s += 1
            if nit >= 3:
                for k in range(4):
                    if nit + nps >= 4 + k:
                        W[s, k] += 1.0
                for i in range(6):
                    if nit + nps + n2s >= 5 + i:
                        W[s, 4 + i] += 1.0
                if nit + nps >= 7:
                    for k in range(3):
                        if n2s >= k + 1:
                            W[s, 10 + k] += 1.0
    return W / nmc


@njit(cache=True)
def subset_weights_mc(hoff, hits, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, dEc, NRM, AXS, q, nsub, seed, ttol, mip,
                      chi2isf):
    """Plain (unconditional) Monte Carlo reference for subset_weights: interactions ~ Bernoulli(q), the same subset
    evaluation, counting rung N_IT2 >= 3 and N_IP2 >= 7 evaluated directly.  Returns means (ns, 34)."""
    np.random.seed(seed)
    ns = sel.shape[0]
    Wm = np.zeros((ns, N_SUB_OUT))
    slot = np.zeros(nI, np.int64)
    stamp = np.full(nI, -1, np.int64)
    for s in range(ns):
        c = sel[s]
        h = hits[hoff[c]:hoff[c + 1]]
        nh = h.shape[0]
        m = 0
        for t in range(nh):
            g = INTl[h[t]]
            if stamp[g] != s:
                stamp[g] = s
                slot[g] = m
                m += 1
        loc = np.empty(nh, np.int64)
        for t in range(nh):
            loc[t] = slot[INTl[h[t]]]
        nx = NRM[c, 0]; ny = NRM[c, 1]; nz = NRM[c, 2]
        ax = AXS[c, 0]; ay = AXS[c, 1]; az = AXS[c, 2]
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        kp = np.zeros(m, np.bool_)
        buf = np.zeros(nh); dbuf = np.zeros(nh)
        for d in range(nsub):
            for j in range(m):
                kp[j] = np.random.random() < q
            cnt = np.zeros((10, 3), np.int64)
            for t in range(nh):
                if kp[loc[t]]:
                    cnt[LC[h[t]], SD[h[t]]] += 1
            nit = 0; nip = 0; n2s2 = 0
            for l in range(10):
                cr = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
                if cr >= 2:
                    if l < 4:
                        nit += 1
                    if l < 7:
                        nip += 1
                    else:
                        n2s2 += 1
            if not (nit >= 3 and nip >= 7):
                continue
            Wm[s, 33] += 1.0
            nb = 0; ndE = 0
            for t in range(nh):
                if kp[loc[t]]:
                    i = h[t]
                    if LC[i] <= 6:
                        buf[nb] = U[i, 0] * n2x + U[i, 1] * n2y + U[i, 2] * n2z
                        nb += 1
            if nb < 3:
                continue
            cmed = np.median(buf[:nb])
            for t in range(nb):
                buf[t] = abs(buf[t] - cmed)
            wcore = 1.4826 * np.median(buf[:nb])
            lo = cmed - 2.5 * wcore; hi = cmed + 2.5 * wcore
            M3 = np.zeros((3, 3)); ncore = 0
            for t in range(nh):
                if not kp[loc[t]]:
                    continue
                i = h[t]
                wv = U[i, 0] * n2x + U[i, 1] * n2y + U[i, 2] * n2z
                if LC[i] <= 6:
                    inn = (wv >= lo) and (wv <= hi)
                else:
                    s2 = 3.0 * abs(n2z) * S1[i]
                    inn = (wv >= lo - s2) and (wv <= hi + s2)
                if inn:
                    if LC[i] <= 3:                  # dE/dx: core IT hits only (review WP_RULE R1 B-1)
                        dbuf[ndE] = dEc[i]
                        ndE += 1
                    aa = -nx * CY[i] + ny * CX[i]
                    sc = np.sqrt(aa * aa * S0[i] * S0[i] + nz * nz * S1[i] * S1[i])
                    sg = np.sqrt(max(sc, 1e-4) ** 2 + ttol * ttol)
                    w = 1.0 / (sg * sg)
                    for a_ in range(3):
                        for b_ in range(3):
                            M3[a_, b_] += w * U[i, a_] * U[i, b_]
                    ncore += 1
            pk = np.zeros(3, np.bool_)
            if ncore >= 4:
                lam = np.linalg.eigvalsh(M3)[0]
                ndf = min(ncore - 2, NDF_MAX)
                for k in range(3):
                    pk[k] = lam < chi2isf[k, ndf]
            ede = np.nan
            if mip > 0.0:
                ede = _trunc_mean(dbuf, ndE, TRUNC_FRAC) / mip
            ok = True
            for k in range(4):
                ok = ok and (wcore < W_K[k])
                if ok:
                    Wm[s, k] += 1.0
            for k in range(3):
                ok = ok and pk[k]
                if ok:
                    Wm[s, 4 + k] += 1.0
            for k in range(3):
                ok = ok and (n2s2 >= k + 1)
                if ok:
                    Wm[s, 7 + k] += 1.0
            for k in range(3):
                if ok and ede > E_MIN[k]:
                    Wm[s, 10 + k] += 1.0
            fb0 = pk[2] and (n2s2 >= 3)
            for kk in range(5):
                fk = fb0 and (kk == 0 or wcore < W_K[kk - 1])
                if fk:
                    Wm[s, 13 + kk] += 1.0
                for e in range(3):
                    if fk and ede > E_MIN[e]:
                        Wm[s, 18 + 3 * kk + e] += 1.0
    return Wm / nsub


# --------------------------------------------------------------------------------------------- distinct hit sets
@njit(cache=True)
def group_sets(hoff, hits, nroad, frac):
    """Greedy distinct-hit-set grouping in rank order (plan §4.1 step 2; the review-R2 r2_dupcheck rule): candidate c
    joins the first existing group (in creation order) whose LEADER shares >= frac * min(|H_c|, |H_leader|) in-band hits
    with it; otherwise it founds a new group.  Exact (inverted index of the leaders' hits).  Returns group id per row."""
    n = hoff.shape[0] - 1
    gid = np.full(n, -1, np.int64)
    tot = hits.shape[0]
    head = np.full(nroad, -1, np.int64)       # per road hit: linked list of leaders containing it
    nxt = np.empty(tot, np.int64)
    lead_of = np.empty(tot, np.int64)
    ne = 0
    cnt = np.zeros(n, np.int64)
    touched = np.empty(n, np.int64)
    lsize = np.zeros(n, np.int64)
    ng = 0
    for c in range(n):
        h0 = hoff[c]; h1 = hoff[c + 1]
        nt = 0
        for t in range(h0, h1):
            e = head[hits[t]]
            while e >= 0:
                g = lead_of[e]
                if cnt[g] == 0:
                    touched[nt] = g
                    nt += 1
                cnt[g] += 1
                e = nxt[e]
        best = -1
        nc = h1 - h0
        for k in range(nt):
            g = touched[k]
            if cnt[g] >= frac * min(nc, lsize[g]):
                if best < 0 or g < best:
                    best = g
        for k in range(nt):
            cnt[touched[k]] = 0
        if best >= 0:
            gid[c] = best
        else:
            gid[c] = ng
            lsize[ng] = nc
            for t in range(h0, h1):
                lead_of[ne] = ng
                nxt[ne] = head[hits[t]]
                head[hits[t]] = ne
                ne += 1
            ng += 1
    return gid


@njit(cache=True)
def _overlap(hits, a0, a1, b0, b1):
    """|A & B| for two ascending-sorted hit lists."""
    i = a0; j = b0; o = 0
    while i < a1 and j < b1:
        if hits[i] == hits[j]:
            o += 1; i += 1; j += 1
        elif hits[i] < hits[j]:
            i += 1
        else:
            j += 1
    return o


@njit(cache=True)
def group_sets_fast(hoff, hits, nroad, frac):
    """Same output as group_sets (exactly), via a prefix filter.  Hits of every set are ordered by a global rarity
    order (number of sets containing the hit, then hit index).  If |A & B| >= alpha then the first |A| - alpha + 1
    elements of A (in that order) meet B.  With alpha = ceil(frac * min(|c|, |L|)):
      leaders with |L| <= |c|: L's first |L| - ceil(frac |L|) + 1 rarest hits meet c   (prefix index pidx, probed by
                                every hit of c);
      leaders with |L| >= |c|: c's first |c| - ceil(frac |c|) + 1 rarest hits meet L   (full index fidx, probed by c's
                                prefix).
    Every surviving leader is verified exactly; the smallest qualifying group id wins (= the reference's first group).
    hits of each set must be ascending (finder output).  Returns group id per set."""
    n = hoff.shape[0] - 1
    tot = hits.shape[0]
    freq = np.zeros(nroad, np.int64)
    for t in range(tot):
        freq[hits[t]] += 1
    key = np.empty(tot, np.int64)
    for t in range(tot):
        key[t] = freq[hits[t]] * nroad + hits[t]
    rs = np.empty(tot, np.int64)            # per set, its hits in rarity order
    for c in range(n):
        h0 = hoff[c]; h1 = hoff[c + 1]
        o = np.argsort(key[h0:h1])
        for k in range(h1 - h0):
            rs[h0 + k] = hits[h0 + o[k]]
    gid = np.full(n, -1, np.int64)
    lead = np.empty(n, np.int64)
    lsize = np.zeros(n, np.int64)
    phead = np.full(nroad, -1, np.int64); pnxt = np.empty(tot, np.int64); plead = np.empty(tot, np.int64)
    fhead = np.full(nroad, -1, np.int64); fnxt = np.empty(tot, np.int64); flead = np.empty(tot, np.int64)
    npe = 0; nfe = 0
    mark = np.full(n, -1, np.int64)
    cand = np.empty(n, np.int64)
    ng = 0
    for c in range(n):
        h0 = hoff[c]; h1 = hoff[c + 1]
        x = h1 - h0
        nc = 0
        for t in range(h0, h1):                         # channel A
            e = phead[hits[t]]
            while e >= 0:
                g = plead[e]
                if lsize[g] <= x and mark[g] != c:
                    mark[g] = c; cand[nc] = g; nc += 1
                e = pnxt[e]
        px = x - int(np.ceil(frac * x)) + 1
        for k in range(min(px, x)):                     # channel B
            e = fhead[rs[h0 + k]]
            while e >= 0:
                g = flead[e]
                if lsize[g] >= x and mark[g] != c:
                    mark[g] = c; cand[nc] = g; nc += 1
                e = fnxt[e]
        best = -1
        if nc:
            cs = np.sort(cand[:nc])
            for k in range(nc):
                g = cs[k]
                L = lead[g]
                o = _overlap(hits, h0, h1, hoff[L], hoff[L + 1])
                if o >= frac * min(x, lsize[g]):
                    best = g
                    break
        if best >= 0:
            gid[c] = best
        else:
            gid[c] = ng
            lead[ng] = c
            lsize[ng] = x
            py = x - int(np.ceil(frac * x)) + 1
            for k in range(min(py, x)):
                hh = rs[h0 + k]
                plead[npe] = ng; pnxt[npe] = phead[hh]; phead[hh] = npe; npe += 1
            for t in range(h0, h1):
                hh = hits[t]
                flead[nfe] = ng; fnxt[nfe] = fhead[hh]; fhead[hh] = nfe; nfe += 1
            ng += 1
    return gid


# ------------------------------------------------------------------------------- SR-T in-job BTL presence (fix WP_RULE R2)
C_MM_PER_NS = 299.792458


@njit(cache=True)
def _btl_inband(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, ux, uy, uz, cx, cy, s0, s1, ttol, wc):
    """WP_RULE.md §1.4 SR-T in-band BTL hit about the candidate's final plane (n), axis (n3 = ax) and PV:
    u.n3 > 0, |u.n2| < W_c, |n.u| < 3 sigma_tot with sigma_tot^2 = max(sigma_n, 1e-4)^2 + t_tol^2 and
    sigma_n^2 = (-n_x c_y + n_y c_x)^2 s0^2 + n_z^2 s1^2 (the BTL local errors projected on n; the tracker formula of
    §1.1 item 3, c = the hit's transverse direction)."""
    if ux * ax + uy * ay + uz * az <= 0.0:
        return False
    if abs(ux * n2x + uy * n2y + uz * n2z) >= wc:
        return False
    d = ux * nx + uy * ny + uz * nz
    aa = -nx * cy + ny * cx
    sn = np.sqrt(aa * aa * s0 * s0 + nz * nz * s1 * s1)
    st2 = max(sn, 1e-4) ** 2 + ttol * ttol
    return d * d < 9.0 * st2


@njit(cache=True)
def btl_band(NRM, AXS, sel, UB, CXB, CYB, S0B, S1B, TB, gB, nG, ttol, wc):
    """In-band BTL hits of the candidates sel (WP_RULE.md §1.4): brute force over all BTL hits of the trial (no road
    pre-filter; the definition has none).  gB: combined interaction id per BTL hit (0..nG-1).  Returns
      boff (ns+1), bint: CSR (by s) of the DISTINCT interaction ids of each candidate's in-band BTL hits;
      nhit (ns,): in-band BTL hit count;
      dt0 (ns,): t - |u|/c (ns) of the in-band hit with the smallest raw time t (the 'earliest' hit; t_PV = 0, i.e.
                 the PU-only trial PV carries no time; NaN if no in-band hit or no time column)."""
    ns = sel.shape[0]
    nb = UB.shape[0]
    nhit = np.zeros(ns, np.int64)
    nint = np.zeros(ns, np.int64)
    dt0 = np.full(ns, np.nan)
    stamp = np.full(max(nG, 1), -1, np.int64)
    boff = np.zeros(ns + 1, np.int64)
    bint = np.empty(0, np.int64)
    for p in range(2):
        if p == 1:
            for s in range(ns):
                boff[s + 1] = boff[s] + nint[s]
            bint = np.empty(boff[ns], np.int64)
            stamp[:] = -1
        for s in range(ns):
            c = sel[s]
            nx = NRM[c, 0]; ny = NRM[c, 1]; nz = NRM[c, 2]
            ax = AXS[c, 0]; ay = AXS[c, 1]; az = AXS[c, 2]
            n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
            k = 0
            tbest = np.inf
            for b in range(nb):
                if not _btl_inband(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, UB[b, 0], UB[b, 1], UB[b, 2], CXB[b], CYB[b],
                                   S0B[b], S1B[b], ttol, wc):
                    continue
                g = gB[b]
                if p == 0:
                    nhit[s] += 1
                    if TB[b] < tbest:
                        tbest = TB[b]
                        dt0[s] = TB[b] - np.sqrt(UB[b, 0] ** 2 + UB[b, 1] ** 2 + UB[b, 2] ** 2) / C_MM_PER_NS
                    if stamp[g] != s:
                        stamp[g] = s
                        nint[s] += 1
                else:
                    if stamp[g] != s:
                        stamp[g] = s
                        bint[boff[s] + k] = g
                        k += 1
    return boff, bint, nhit, dt0


@njit(cache=True)
def drop_interactions(hoff, hits, sel, INTl, nI, boffC, bintC):
    """CSR of the sets sel with the hits of their in-band-BTL interactions removed (S minus I_B; boffC/bintC per
    candidate as in subset_weights_btl).  Used for the exact counting-rung BTL columns:
        w_{r and BTL}(S) = w_r(S) - (1 - q)^|I_B| w_r(S minus I_B)
    (P(T passes r and T misses every in-band BTL interaction) factorises because interactions are independent and the
    rung depends only on T's hits).  Returns (hoff_r (ns+1), hits_r, ndrop (ns,) hits removed)."""
    ns = sel.shape[0]
    mark = np.full(max(nI, 1), -1, np.int64)
    ndrop = np.zeros(ns, np.int64)
    tot = 0
    for s in range(ns):
        c = sel[s]
        tot += hoff[c + 1] - hoff[c]
    out = np.empty(tot, hits.dtype)
    hoff_r = np.zeros(ns + 1, np.int64)
    k = 0
    for s in range(ns):
        c = sel[s]
        for kb in range(boffC[c], boffC[c + 1]):
            g = bintC[kb]
            if g < nI:
                mark[g] = s
        for t in range(hoff[c], hoff[c + 1]):
            if mark[INTl[hits[t]]] == s:
                ndrop[s] += 1
            else:
                out[k] = hits[t]
                k += 1
        hoff_r[s + 1] = k
    return hoff_r, out[:k], ndrop
