"""Repaired thinning (STR §4.5 (a), [SD4]; COM B2-a) — core kernels.  Phase 3, work package p3-b, executor Casper.

Counted object [SD4]: the per-trial number of DISTINCT HIT SETS AFTER GROUPING APPLIED AT THE TARGET DENSITY.  A ρ = 2
trial (pre-merge store, N_IP2 >= 6 at ρ = 2) is thinned K times; each thinned subset keeps every interaction of the trial
with probability q = 1/ρ, ONE Bernoulli draw per interaction shared by all candidates of the trial (v1's thinning unit:
the interaction id INT of the finder pool; every top-up crossing is its own interaction; `acts/stage4/finder/weights.py`
docstring and `count_weights`).  For each subset, in rank order:
  1. every stored candidate's hit set is reduced to its kept hits (plane and axis fixed at the ρ = 2 values: v1 step 3b,
     no refit after thinning);
  2. counting variables (N_IT2, N_IP2, N_2S2; stacked layers count min(n_in, n_out)) and, for the R04 passers, w_core =
     1.4826 MAD of u.n2 over the kept IP hits, the core, chi2_core = lambda_min of the core scatter matrix and N_2S2 —
     the arithmetic of `kernels.cand_vars` / `production.full_set_flags` (and of v1's `weights._subset_core`);
  3. the R04 passers (N_IT2 >= 3, N_IP2 >= 7, aligned) are grouped with `weights.group_sets` (frac 0.5) on their KEPT hit
     lists, in rank order — the grouping acts at ρ = 1 (the repair);
  4. per column, the number of groups with >= 1 passing member (and, diagnostic, the number of passing candidates).
Only candidates that are aligned with N_IT2 >= 3 and N_IP2 >= 7 at ρ = 2 can pass R04 after thinning (thinning only
removes hits), so only they are processed.

Columns (COLS): cumulative ladder R04-R14; crossing rungs of STR §4.0 point 7 (2S family on R04-R06, fit-probability
family on R05-R06); the s = 3 family (rung AND N_2S2 >= 3) on R07-R09; the fallback parts FB0-FB4 (production.py).
"""
import numpy as np
from numba import njit
from scipy.stats import chi2 as _CHI2

import sys
from pathlib import Path

QV2 = Path(__file__).resolve().parents[3]
if str(QV2) not in sys.path:
    sys.path.insert(0, str(QV2))
from acts.stage4.finder import weights as WG          # noqa: E402  (group_sets, _lam_min: v1 code, unchanged)
from acts.stage4.finder import finder as FF           # noqa: E402

W_K = np.array([37.5, 18.75, 9.4, 4.7])
P_MIN = np.array([1e-3, 0.01, 0.05])
NDF_MAX = 4000
CHI2_ISF = np.array([[_CHI2.isf(p, d) if d >= 1 else 0.0 for d in range(NDF_MAX + 1)] for p in P_MIN])

from cols import COLS, NCOL  # noqa: E402,F401  (column names, shared with the analysis scripts)


@njit(cache=True)
def col_flags(wcore, pk0, pk1, pk2, n2s2, out):
    """Column pass flags of an R04 passer (R04 itself is assumed).  wcore NaN fails every width cut; pk = p > P_MIN."""
    for k in range(out.shape[0]):
        out[k] = False
    w1 = wcore < 37.5
    w2 = w1 and wcore < 18.75
    w3 = w2 and wcore < 9.4
    w4 = w3 and wcore < 4.7
    out[0] = True
    out[1] = w1; out[2] = w2; out[3] = w3; out[4] = w4
    r9 = w4 and pk0
    r10 = r9 and pk1
    r11 = r10 and pk2
    out[5] = r9; out[6] = r10; out[7] = r11
    out[8] = r11 and n2s2 >= 1; out[9] = r11 and n2s2 >= 2; out[10] = r11 and n2s2 >= 3
    for j in range(3):
        out[11 + j] = n2s2 >= j + 1
        out[14 + j] = w1 and n2s2 >= j + 1
        out[17 + j] = w2 and n2s2 >= j + 1
    out[20] = w3 and n2s2 >= 3
    out[21] = w4 and n2s2 >= 3
    out[22] = r9 and n2s2 >= 3
    out[23] = w1 and pk0; out[24] = w1 and pk1; out[25] = w1 and pk2
    out[26] = w2 and pk0; out[27] = w2 and pk1; out[28] = w2 and pk2
    fb0 = pk2 and n2s2 >= 3
    out[29] = fb0
    out[30] = fb0 and w1; out[31] = fb0 and w2; out[32] = fb0 and w3; out[33] = fb0 and w4


@njit(cache=True)
def _set_vars(hl, nk, LC, SD, U, CX, CY, S0, S1, n, a, ttol, chi2isf, wbuf, res):
    """Variables of one (kept) hit list hl[:nk] for plane normal n and axis a (cand_vars arithmetic).
    res = [nit2, nip2, n2s2, wcore, pk0, pk1, pk2]."""
    cnt = np.zeros((10, 3), np.int64)
    for t in range(nk):
        i = hl[t]
        cnt[LC[i], SD[i]] += 1
    nit2 = 0; nip2 = 0; n2s2 = 0
    for l in range(10):
        c = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
        if c >= 2:
            if l < 4:
                nit2 += 1
            if l < 7:
                nip2 += 1
            else:
                n2s2 += 1
    res[0] = nit2; res[1] = nip2; res[2] = n2s2
    res[3] = np.nan; res[4] = 0.0; res[5] = 0.0; res[6] = 0.0
    if not (nit2 >= 3 and nip2 >= 7):
        return
    n2x = n[1] * a[2] - n[2] * a[1]; n2y = n[2] * a[0] - n[0] * a[2]; n2z = n[0] * a[1] - n[1] * a[0]
    nb = 0
    for t in range(nk):
        i = hl[t]
        if LC[i] <= 6:
            wbuf[nb] = U[i, 0] * n2x + U[i, 1] * n2y + U[i, 2] * n2z
            nb += 1
    if nb <= 2:
        return
    cmed = np.median(wbuf[:nb])
    dev = np.abs(wbuf[:nb] - cmed)
    s = 1.4826 * np.median(dev)
    res[3] = s
    lo = cmed - 2.5 * s; hi = cmed + 2.5 * s
    a00 = 0.0; a01 = 0.0; a02 = 0.0; a11 = 0.0; a12 = 0.0; a22 = 0.0
    ncore = 0
    for t in range(nk):
        i = hl[t]
        wv = U[i, 0] * n2x + U[i, 1] * n2y + U[i, 2] * n2z
        if LC[i] <= 6:
            inside = (wv >= lo) and (wv <= hi)
        else:
            s2 = abs(n2z) * S1[i]
            inside = (wv >= lo - 3 * s2) and (wv <= hi + 3 * s2)
        if inside:
            aa = -n[0] * CY[i] + n[1] * CX[i]
            sc = np.sqrt(aa * aa * S0[i] * S0[i] + n[2] * n[2] * S1[i] * S1[i])
            sg = np.sqrt(max(sc, 1e-4) ** 2 + ttol * ttol)
            w = 1.0 / (sg * sg)
            a00 += w * U[i, 0] * U[i, 0]; a01 += w * U[i, 0] * U[i, 1]; a02 += w * U[i, 0] * U[i, 2]
            a11 += w * U[i, 1] * U[i, 1]; a12 += w * U[i, 1] * U[i, 2]; a22 += w * U[i, 2] * U[i, 2]
            ncore += 1
    if ncore >= 4:
        lam = WG._lam_min(a00, a01, a02, a11, a12, a22)
        ndf = min(ncore - 2, NDF_MAX)
        res[4] = 1.0 if lam < chi2isf[0, ndf] else 0.0
        res[5] = 1.0 if lam < chi2isf[1, ndf] else 0.0
        res[6] = 1.0 if lam < chi2isf[2, ndf] else 0.0


@njit(cache=True)
def thin_trial(off, ref, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, NRM, AXS, q, K, seed, ttol, chi2isf, ncol):
    """Repaired thinning of one ρ = 2 trial.  off/ref: CSR of the stored candidates into the union hit table (ascending);
    sel: candidates to process, in rank order; per union hit LC, SD, INTl (compact interaction index < nI), U (hit - PV),
    CX, CY, S0, S1; NRM/AXS per candidate (ρ = 2 plane and axis).  q = keep probability; K subsets.
    q >= 1 keeps every hit (identity check).  Returns grp (K, ncol) distinct groups, npass (K, ncol) passing candidates,
    n4 (K,) thinned R04 candidates."""
    np.random.seed(seed)
    nh = U.shape[0]
    ns = sel.shape[0]
    grp = np.zeros((K, ncol), np.int64)
    npass = np.zeros((K, ncol), np.int64)
    n4 = np.zeros(K, np.int64)
    keep = np.ones(nI, np.bool_)
    maxk = 1
    tot = 0
    for s in range(ns):
        c = sel[s]
        m = off[c + 1] - off[c]
        tot += m
        maxk = max(maxk, m)
    hl = np.empty(maxk, np.int64)
    wbuf = np.empty(maxk)
    res = np.zeros(7)
    fl = np.zeros(ncol, np.bool_)
    ho = np.zeros(ns + 1, np.int64)
    hi = np.empty(tot, np.int64)
    pflag = np.zeros((ns, ncol), np.bool_)
    mark = np.full((ncol, ns), -1, np.int64)
    for k in range(K):
        if q < 1.0:
            for g in range(nI):
                keep[g] = np.random.random() < q
        npas = 0
        nt = 0
        for s in range(ns):
            c = sel[s]
            nk = 0
            for t in range(off[c], off[c + 1]):
                i = ref[t]
                if keep[INTl[i]]:
                    hl[nk] = i
                    nk += 1
            _set_vars(hl, nk, LC, SD, U, CX, CY, S0, S1, NRM[c], AXS[c], ttol, chi2isf, wbuf, res)
            if res[0] >= 3 and res[1] >= 7:
                col_flags(res[3], res[4] > 0.5, res[5] > 0.5, res[6] > 0.5, int(res[2]), fl)
                for j in range(ncol):
                    pflag[npas, j] = fl[j]
                    if fl[j]:
                        npass[k, j] += 1
                for t in range(nk):
                    hi[nt] = hl[t]
                    nt += 1
                npas += 1
                ho[npas] = nt
        n4[k] = npas
        if npas == 0:
            continue
        gid = WG.group_sets(ho[:npas + 1], hi[:nt], nh, 0.5)
        for p in range(npas):
            g = gid[p]
            for j in range(ncol):
                if pflag[p, j] and mark[j, g] != k:
                    mark[j, g] = k
                    grp[k, j] += 1
    return grp, npass, n4


def trial_inputs(z, t, pv):
    """Arrays of trial t of an open pre-merge store z (zip of npy) for thin_trial.  pv: the trial PV (main npz)."""
    p = f't{t}/'
    off = z[p + 'off'].astype(np.int64)
    ref = z[p + 'ref'].astype(np.int64)
    xyz = z[p + 'h_xyz'].astype(np.float64)
    sid = z[p + 'h_sid'].astype(np.int64)
    s01 = z[p + 'h_s01'].astype(np.float64)
    INT = z[p + 'h_INT']
    _, INTl = np.unique(INT, return_inverse=True)
    al = z[p + 'aligned'].astype(bool)
    sel = np.where(al & (z[p + 'v_nit2'] >= 3) & (z[p + 'v_nip2'] >= 7))[0].astype(np.int64)
    r = np.hypot(xyz[:, 0], xyz[:, 1])
    return dict(off=off, ref=ref, sel=sel, LC=FF.LC_OF[sid].astype(np.int64), SD=FF.SIDE_OF[sid].astype(np.int64),
                INTl=INTl.astype(np.int64), nI=int(INTl.max()) + 1 if len(INTl) else 0,
                U=np.ascontiguousarray(xyz - pv[None, :]), CX=xyz[:, 0] / r, CY=xyz[:, 1] / r,
                S0=np.ascontiguousarray(s01[:, 0]), S1=np.ascontiguousarray(s01[:, 1]),
                NRM=z[p + 'normal'].astype(np.float64), AXS=z[p + 'axis'].astype(np.float64),
                gid=z[p + 'gid'].astype(np.int64))


def run_trial(d, q, K, seed, ttol=0.030):
    return thin_trial(d['off'], d['ref'], d['sel'], d['LC'], d['SD'], d['INTl'], d['nI'], d['U'], d['CX'], d['CY'],
                      d['S0'], d['S1'], d['NRM'], d['AXS'], float(q), int(K), int(seed), float(ttol), CHI2_ISF, NCOL)


def direct_cols(F, wcore, p, n2s2):
    """Column flags (ncand, NCOL) of stored ρ = 1 candidates from their full-set variables (same col_flags)."""
    out = np.zeros((len(wcore), NCOL), bool)
    fl = np.zeros(NCOL, np.bool_)
    for i in range(len(wcore)):
        if not F[i]:
            continue
        pi = p[i]
        col_flags(float(wcore[i]), bool(pi > 1e-3), bool(pi > 0.01), bool(pi > 0.05), int(n2s2[i]), fl)
        out[i] = fl
    return out


# ------------------------------------------------------------------ remediation variants of B2-a (diagnostics only)
from acts.stage4.finder import kernels as KK      # noqa: E402  (v1 finder kernels: dedup)


@njit(cache=True)
def _refit(hl, nk, U, CX, CY, S0, S1, n, a, ttol, wc, iters, sel):
    """The finder's plane refit (kernels.refit_packed arithmetic) on the kept hits hl[:nk]: `iters` updates of
    (n, axis) from the in-band selection, then the final in-band selection -> sel[:m].  Returns (m, n, a, nl2, chi2ndf)
    with nl2/chi2ndf of the final selection (counting by the caller)."""
    nx = n[0]; ny = n[1]; nz = n[2]; ax = a[0]; ay = a[1]; az = a[2]
    m = 0
    chi2 = 0.0
    for it in range(iters + 1):
        n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
        M = np.zeros((3, 3)); sx = 0.0; sy = 0.0; sz = 0.0
        m = 0; chi2 = 0.0
        for t in range(nk):
            i = hl[t]
            ux = U[i, 0]; uy = U[i, 1]; uz = U[i, 2]
            d = ux * nx + uy * ny + uz * nz
            aa = -nx * CY[i] + ny * CX[i]
            sc2 = aa * aa * S0[i] * S0[i] + nz * nz * S1[i] * S1[i]
            if not ((d * d < 9.0 * (max(sc2, 1e-8) + ttol * ttol)) and (ux * ax + uy * ay + uz * az > 0)
                    and (abs(ux * n2x + uy * n2y + uz * n2z) < wc)):
                continue
            sc = np.sqrt(sc2)
            sg2 = max(sc, 1e-4) ** 2 + ttol * ttol
            w = 1.0 / sg2
            M[0, 0] += w * ux * ux; M[0, 1] += w * ux * uy; M[0, 2] += w * ux * uz
            M[1, 1] += w * uy * uy; M[1, 2] += w * uy * uz; M[2, 2] += w * uz * uz
            chi2 += d * d * w
            un = np.sqrt(ux * ux + uy * uy + uz * uz)
            sx += ux / un; sy += uy / un; sz += uz / un
            sel[m] = i
            m += 1
        if it == iters or m < 4:
            break
        M[1, 0] = M[0, 1]; M[2, 0] = M[0, 2]; M[2, 1] = M[1, 2]
        ev, evec = np.linalg.eigh(M)
        vx = evec[0, 0]; vy = evec[1, 0]; vz = evec[2, 0]
        if vx * nx + vy * ny + vz * nz < 0:
            vx = -vx; vy = -vy; vz = -vz
        nx = vx; ny = vy; nz = vz
        dd = sx * nx + sy * ny + sz * nz
        sx -= dd * nx; sy -= dd * ny; sz -= dd * nz
        an = np.sqrt(sx * sx + sy * sy + sz * sz)
        if an > 0:
            ax = sx / an; ay = sy / an; az = sz / an
    return m, np.array([nx, ny, nz]), np.array([ax, ay, az]), chi2 / max(m - 2, 1)


@njit(cache=True)
def thin_trial_var(off, ref, sel, LC, SD, INTl, nI, U, CX, CY, S0, S1, NRM, AXS, q, K, seed, ttol, chi2isf, ncol,
                   mode):
    """Variants of thin_trial (same draws for the same seed): mode 1 = refit (3 iterations, finder arithmetic) of every
    thinned R04 passer on its kept hits, re-rank by (-N_L2, chi2/ndf) of the refit set, finder dedup (2 mrad) of the
    refit normals, then grouping; mode 2 = refit and re-rank, no dedup; mode 3 = no refit, re-rank only."""
    np.random.seed(seed)
    nh = U.shape[0]
    ns = sel.shape[0]
    grp = np.zeros((K, ncol), np.int64)
    n4 = np.zeros(K, np.int64)
    keep = np.ones(nI, np.bool_)
    maxk = 1
    tot = 0
    for s in range(ns):
        c = sel[s]
        mlen = off[c + 1] - off[c]
        tot += mlen
        maxk = max(maxk, mlen)
    hl = np.empty(maxk, np.int64)
    sl = np.empty(maxk, np.int64)
    wbuf = np.empty(maxk)
    res = np.zeros(7)
    fl = np.zeros(ncol, np.bool_)
    hi = np.empty(tot, np.int64)
    hstart = np.zeros(ns + 1, np.int64)
    pflag = np.zeros((ns, ncol), np.bool_)
    nl2v = np.zeros(ns); chiv = np.zeros(ns)
    NF = np.zeros((ns, 3))
    mark = np.full((ncol, ns), -1, np.int64)
    for k in range(K):
        if q < 1.0:
            for g in range(nI):
                keep[g] = np.random.random() < q
        npas = 0
        nt = 0
        for s in range(ns):
            c = sel[s]
            nk = 0
            for t in range(off[c], off[c + 1]):
                i = ref[t]
                if keep[INTl[i]]:
                    hl[nk] = i
                    nk += 1
            _set_vars(hl, nk, LC, SD, U, CX, CY, S0, S1, NRM[c], AXS[c], ttol, chi2isf, wbuf, res)
            if not (res[0] >= 3 and res[1] >= 7):
                continue
            n = NRM[c].copy(); a = AXS[c].copy()
            m = nk
            for t in range(nk):
                sl[t] = hl[t]
            if mode in (1, 2):
                m, n, a, chi = _refit(hl, nk, U, CX, CY, S0, S1, NRM[c], AXS[c], ttol, 75.0, 3, sl)
                _set_vars(sl, m, LC, SD, U, CX, CY, S0, S1, n, a, ttol, chi2isf, wbuf, res)
                if not (res[0] >= 3 and res[1] >= 7):
                    continue
            else:
                m, _, _, chi = _refit(hl, nk, U, CX, CY, S0, S1, NRM[c], AXS[c], ttol, 75.0, 0, sl)
            cnt = np.zeros((10, 3), np.int64)
            for t in range(m):
                cnt[LC[sl[t]], SD[sl[t]]] += 1
            nl2 = 0
            for l in range(10):
                cc = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
                if cc >= 2:
                    nl2 += 1
            col_flags(res[3], res[4] > 0.5, res[5] > 0.5, res[6] > 0.5, int(res[2]), fl)
            for j in range(ncol):
                pflag[npas, j] = fl[j]
            nl2v[npas] = nl2; chiv[npas] = chi
            NF[npas] = n
            hstart[npas] = nt
            # kept hit list must be ascending for group_sets' inverted index (any order works for overlap counts)
            tmp = np.sort(sl[:m])
            for t in range(m):
                hi[nt] = tmp[t]
                nt += 1
            npas += 1
        hstart[npas] = nt
        if npas == 0:
            continue
        key = np.empty(npas)
        for r in range(npas):
            key[r] = (10.0 - nl2v[r]) * 1e9 + min(chiv[r], 1e8)       # (-N_L2, chi2/ndf), stable
        order = np.argsort(key, kind='mergesort')
        if mode == 1:
            kp = KK.dedup(NF[:npas], order, 2.1e-3)
        else:
            kp = np.ones(npas, np.bool_)
        ho = np.zeros(npas + 1, np.int64)
        hh = np.empty(nt, np.int64)
        idx = np.empty(npas, np.int64)
        nn = 0; pt = 0
        for r in range(npas):
            c = order[r]
            if not kp[c]:
                continue
            for t in range(hstart[c], hstart[c + 1]):
                hh[pt] = hi[t]
                pt += 1
            idx[nn] = c
            nn += 1
            ho[nn] = pt
        n4[k] = nn
        gid = WG.group_sets(ho[:nn + 1], hh[:pt], nh, 0.5)
        for p in range(nn):
            g = gid[p]
            c = idx[p]
            for j in range(ncol):
                if pflag[c, j] and mark[j, g] != k:
                    mark[j, g] = k
                    grp[k, j] += 1
    return grp, n4


def run_trial_var(d, q, K, seed, mode, ttol=0.030):
    return thin_trial_var(d['off'], d['ref'], d['sel'], d['LC'], d['SD'], d['INTl'], d['nI'], d['U'], d['CX'],
                          d['CY'], d['S0'], d['S1'], d['NRM'], d['AXS'], float(q), int(K), int(seed), float(ttol),
                          CHI2_ISF, NCOL, int(mode))
