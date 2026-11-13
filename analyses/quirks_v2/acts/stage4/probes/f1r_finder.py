"""f1r_finder.py -- Stage-4 plan FIXER R1 probe (TT env): BLIND F0 prototype with per-CROSSING layer counting, run identically
on PU-only trials (rho = 1 and superposed rho = 2) and on signal + PU overlays.  No truth enters seed selection, refit,
ranking or counting; truth is read only afterwards (signal fraction, interaction composition, thinning weights).

Changes w.r.t. p5_finder_triplet.py / review_r1/r1_pu_fullrefit.py (critical A-1, B-1, B-2, B-3; constructive A-1, B-1):
  * counting: a layer's number of CROSSINGS is n_hits for single-sensor layers (TBPX L1-4) and min(n_in, n_out) for stacked
    OT layers (TBPS L1-3, TB2S L1-3; one crossing = one in/out pair); N_IT2 = TBPX layers with >= 2 crossings,
    N_OT2 = OT layers with >= 2 crossings, N_L2 = N_IT2 + N_OT2 (barrel, 10 layers).  The R0 count (>= 2 hits on in+out) is
    kept as a diagnostic (N_OT2h).
  * collection window W_c = 75 mm (= R_TBPX,L4 / 2 rounded up; physics rule, plan §2.2) and road 0.25 + asin(min(1, W_c/r)).
  * every distinct (a, b) seed plane with seed N_L2 >= T_SEED is refitted (T_SEED = 6 in the fix-R1 runs; the best-candidate
    N_L2 is unchanged with T_SEED = 4 on 4 trials, which refit 4-5x more seeds; data/acts_stage4/fix_r1/f1r_tseed_check.json).
  * plane-thickness tolerance (fix R1, after the first pass): sigma_tot^2 = sigma_n^2 + t_tol^2 in seeding, collection and
    refit; t_tol = 30 um (default, = the event-level MS floor s_eff 23-30 um of synthesis S-2, a physics number) or 100 um
    (variation).  With t_tol = 0 (first pass, data in fix_r1/finder_tol0_seedaxis/) the 7 um IT band rejects real quirk
    hits (truth residuals to the pair's own best plane are 30-180 um median, Stage-3 res_max_um).
  * window axis: re-estimated at each refit iteration as the mean direction (from the PV) of the selected hits projected
    into the plane (the seed axis from two hits can be 0.05-0.2 rad off the pair axis).
  * refit: 3 x PV-constrained weighted plane fit (as p4.refit; numba refit_nb for ranking, numpy refit for the stored
    variables), with a pre-filter around the seed plane of 5 mm (IT, PS) and 60 mm (2S: > 3 sigma of a 2S hit; a 5 mm 2S
    pre-filter dropped real quirk 2S hits in a first pass).
  * duplicate candidates (normals within 2 mrad) merged; ranking (N_L2, -chi2/ndf).
  * no Delta-w cut anywhere; Delta-w (R0 rms) and a robust core width are only stored.
  * optional density top-up (V4-2): extra random crossings per barrel layer, TDR/Fatras ratio - 1 of the event's Fatras hits,
    z resampled from the event's hits on that layer, phi uniform; stacked layers get in/out pairs (a 'stub'); each top-up
    crossing is its own interaction (k = 1 each).
  * PV of PU-only trials: random luminous-region point (sigma_z 45 mm, sigma_xy 5 um), independent of the PU vertices;
    distance to the nearest PU vertex recorded.  Signal trials: the Stage-3 vertex smeared by (10, 15) um.
  * MET of signal trials: truth pair pT smeared by 25 GeV per component.  PU-only: phi0 random, 4 roads at phi0 + k pi/2.
  * thinning weights (constructive B-1 made exact): for a candidate whose in-band hits come from interactions S, the
    probability that it still passes rung L when each interaction is kept with q = 1/rho, sum over subsets T of S that pass
    of q^|T| (1-q)^(|S|-|T|) (exact enumeration for |S| <= 12, else 2e4 Monte-Carlo subsets; plane not refitted).  At rho = 1 only the
    top-ranked candidate gets k_min (composition); at rho = 2 every stored candidate gets its weights.
Modes: pu (rho = 1), pu2 (rho = 2 superpositions of two distinct PU events), sig (signal overlay on one PU event).
Run (theory_track): pixi run python acts/stage4/probes/f1r_finder.py <mode> <job> <njobs> [topup=0|1|2] [tseed=4]
  topup 0 = Fatras only, 1 = all barrel layers (too slow for the probe at IT x2-4), 2 = OT layers only
Output: data/acts_stage4/fix_r1/finder/<mode>_t<topup>_j<job>.jsonl
"""
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from numba import njit

TT = Path(__file__).resolve().parents[3]
PUD = TT / 'data' / 'acts_stage4' / 'fix_r1' / 'pu'
OUTD = TT / 'data' / 'acts_stage4' / 'fix_r1' / 'finder'
OUTD.mkdir(parents=True, exist_ok=True)
S = json.loads((TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
NS = len(S)
LAYERS = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']
LC_OF = np.full(NS, -1, np.int64)
SIDE_OF = np.zeros(NS, np.int64)
for i, s in enumerate(S):
    for k, p in enumerate(LAYERS):
        if s['name'] == p or s['name'].startswith(p + '_'):
            LC_OF[i] = k
            SIDE_OF[i] = 1 if s['name'].endswith('_in') else (2 if s['name'].endswith('_out') else 0)
SID = {s['name']: i for i, s in enumerate(S)}
RAD = {i: s['p0'] * 10.0 for i, s in enumerate(S) if s['type'] == 0}
W_C = 75.0
T_TOL = 0.030      # mm, intrinsic plane-thickness tolerance added in quadrature to sigma_n (env F1R_TTOL_UM)
ROAD = 0.25
NL = 10
# TDR/Fatras density ratios, nominal (f1r_density_bench.json): IT cluster size 2 (ESTIMATE), OT strip/macro mean
TOPUP = {'TBPX_L1': 2.77, 'TBPX_L2': 2.26, 'TBPX_L3': 2.81, 'TBPX_L4': 3.72, 'TBPS_L1': 2.56, 'TBPS_L2': 3.25,
         'TBPS_L3': 4.31, 'TB2S_L1': 4.00, 'TB2S_L2': 5.16, 'TB2S_L3': 7.27}
RUNGS = [5, 6, 7, 8, 9, 10]
TOPUP_MODE = 0       # N_L2 >= L, with N_IT2 >= 3 always


@njit(cache=True)
def wrap(d):
    while d > np.pi:
        d -= 2 * np.pi
    while d < -np.pi:
        d += 2 * np.pi
    return d


@njit(cache=True)
def sig_cyl(n, x, y, s0, s1):
    r = np.hypot(x, y)
    cx, cy = x / r, y / r
    a = -n[0] * cy + n[1] * cx
    b = n[2]
    return np.sqrt(a * a * s0 * s0 + b * b * s1 * s1)


@njit(cache=True)
def score(cnt):
    n1 = 0; n2 = 0; nit2 = 0
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


@njit(cache=True)
def seeds(U, X, Y, S0, S1, LC, SD, A, B, C, phiU, etaU, phimet, road, wc, tseed, ttol):
    out = []
    ntrip = 0
    for ia in A:
        ra = np.hypot(U[ia, 0], U[ia, 1])
        if abs(wrap(phiU[ia] - phimet)) > road + np.arcsin(min(1.0, wc / ra)):
            continue
        for ib in B:
            rb = np.hypot(U[ib, 0], U[ib, 1])
            if abs(wrap(phiU[ib] - phimet)) > road + np.arcsin(min(1.0, wc / rb)):
                continue
            if abs(wrap(phiU[ia] - phiU[ib])) > 0.3 or abs(etaU[ia] - etaU[ib]) > 0.2:
                continue
            ua = U[ia]; ub = U[ib]
            c = np.cross(ua, ub); na = np.linalg.norm(ua); nb = np.linalg.norm(ub)
            sn = np.linalg.norm(c) / (na * nb)
            if sn < 1e-3:
                continue
            n = c / np.linalg.norm(c)
            sseed = 0.03 / (nb * sn)
            axis = ua / na + ub / nb; axis = axis / np.linalg.norm(axis)
            n2v = np.cross(n, axis)
            best = -1
            for ic in C:
                if abs(wrap(phiU[ic] - phiU[ib])) > 0.4:
                    continue
                uc = U[ic]
                d = uc[0] * n[0] + uc[1] * n[1] + uc[2] * n[2]
                sg = sig_cyl(n, X[ic], Y[ic], S0[ic], S1[ic])
                if abs(d) > 3 * np.sqrt(sg * sg + ttol * ttol + (sseed * np.linalg.norm(uc)) ** 2):
                    continue
                ntrip += 1
                best = 1
                break     # the score depends only on the (a, b) plane: one valid c suffices
            if best < 0:
                continue
            cnt = np.zeros((10, 3), np.int64)
            for i in range(U.shape[0]):
                if LC[i] < 0:
                    continue
                if U[i, 0] * axis[0] + U[i, 1] * axis[1] + U[i, 2] * axis[2] <= 0:
                    continue
                if abs(U[i, 0] * n2v[0] + U[i, 1] * n2v[1] + U[i, 2] * n2v[2]) > wc:
                    continue
                di = U[i, 0] * n[0] + U[i, 1] * n[1] + U[i, 2] * n[2]
                ui = np.sqrt(U[i, 0] ** 2 + U[i, 1] ** 2 + U[i, 2] ** 2)
                sgi = sig_cyl(n, X[i], Y[i], S0[i], S1[i])
                if abs(di) < 3 * np.sqrt(sgi * sgi + ttol * ttol + (sseed * ui) ** 2):
                    cnt[LC[i], SD[i]] += 1
            n1, n2c, nit2 = score(cnt)
            if n2c >= tseed:
                out.append((ia, ib, n1, n2c))
    return out, ntrip


@njit(cache=True)
def refit_nb(U, X, Y, S0, S1, LC, SD, n0, axis0, wc, iters, ttol):
    """numba version of refit(): returns (n, nl2, nit2, chi2ndf, nsel); identical selection logic."""
    n = n0.copy()
    axis = axis0.copy()
    m = U.shape[0]
    idx = np.empty(m, np.int64); k = 0
    for i in range(m):
        if LC[i] >= 0 and abs(U[i, 0] * n[0] + U[i, 1] * n[1] + U[i, 2] * n[2]) < (60.0 if LC[i] >= 7 else 5.0):
            idx[k] = i; k += 1
    idx = idx[:k]
    nl2 = 0; nit2 = 0; chi2 = 0.0; nsel = 0
    if k < 4:
        return n, -1, -1, 1e9, 0, axis
    for it in range(iters + 1):
        n2v = np.cross(n, axis)
        M = np.zeros((3, 3)); chi2 = 0.0; nsel = 0
        cnt = np.zeros((10, 3), np.int64)
        asum = np.zeros(3)
        for j in range(k):
            i = idx[j]
            d = U[i, 0] * n[0] + U[i, 1] * n[1] + U[i, 2] * n[2]
            sg = np.sqrt(max(sig_cyl(n, X[i], Y[i], S0[i], S1[i]), 1e-4) ** 2 + ttol * ttol)
            if abs(d) >= 3 * sg:
                continue
            if U[i, 0] * axis[0] + U[i, 1] * axis[1] + U[i, 2] * axis[2] <= 0:
                continue
            if abs(U[i, 0] * n2v[0] + U[i, 1] * n2v[1] + U[i, 2] * n2v[2]) >= wc:
                continue
            w = 1.0 / (sg * sg)
            for a in range(3):
                for b in range(3):
                    M[a, b] += w * U[i, a] * U[i, b]
            chi2 += d * d * w; nsel += 1
            cnt[LC[i], SD[i]] += 1
            un = np.sqrt(U[i, 0] ** 2 + U[i, 1] ** 2 + U[i, 2] ** 2)
            for a in range(3):
                asum[a] += U[i, a] / un
        if nsel < 4:
            return n, -1, -1, 1e9, nsel, axis
        if it == iters:
            break
        ev, evec = np.linalg.eigh(M)
        v = evec[:, 0].copy()
        if v[0] * n[0] + v[1] * n[1] + v[2] * n[2] < 0:
            v = -v
        n = v
        # axis update: mean direction of the selected hits (from the PV), projected into the new plane
        asum = asum - (asum[0] * n[0] + asum[1] * n[1] + asum[2] * n[2]) * n
        an = np.sqrt(asum[0] ** 2 + asum[1] ** 2 + asum[2] ** 2)
        if an > 0:
            axis = asum / an
    n1, nl2, nit2 = score(cnt)
    return n, nl2, nit2, chi2 / max(nsel - 2, 1), nsel, axis


def sig_vec(n, X, Y, S0, S1):
    r = np.hypot(X, Y); cx, cy = X / r, Y / r
    a = -n[0] * cy + n[1] * cx
    return np.sqrt(a ** 2 * S0 ** 2 + n[2] ** 2 * S1 ** 2)


def counts_of(lc, sd):
    cnt = np.zeros((NL, 3), np.int64)
    np.add.at(cnt, (lc, sd), 1)
    return cnt


def cross_from_cnt(cnt):
    c = np.empty(NL, np.int64)
    c[:4] = cnt[:4, 0]
    c[4:] = np.minimum(cnt[4:, 1], cnt[4:, 2])
    return c


def refit(U, X, Y, S0, S1, LC, SD, n, axis, iters=3):
    pre = np.abs(U @ n) < np.where(LC >= 7, 60.0, 5.0)
    idx = np.where(pre & (LC >= 0))[0]
    if len(idx) < 4:
        return None
    Ui, Xi, Yi, S0i, S1i = U[idx], X[idx], Y[idx], S0[idx], S1[idx]
    for it in range(iters + 1):
        sg = np.sqrt(np.maximum(sig_vec(n, Xi, Yi, S0i, S1i), 1e-4) ** 2 + T_TOL ** 2)
        d = Ui @ n
        sel = (np.abs(d) < 3 * sg) & ((Ui @ axis) > 0) & (np.abs(Ui @ np.cross(n, axis)) < W_C)
        if sel.sum() < 4:
            return None
        if it == iters:
            break
        w = 1.0 / sg[sel] ** 2
        M = (Ui[sel] * w[:, None]).T @ Ui[sel]
        ev, evec = np.linalg.eigh(M)
        n = evec[:, 0] if evec[:, 0] @ n >= 0 else -evec[:, 0]
        asum = (Ui[sel] / np.linalg.norm(Ui[sel], axis=1)[:, None]).sum(0)
        asum = asum - (asum @ n) * n
        if np.linalg.norm(asum) > 0:
            axis = asum / np.linalg.norm(asum)
    w = 1.0 / sg[sel] ** 2
    hidx = idx[sel]
    cnt = counts_of(LC[hidx], SD[hidx])
    cr = cross_from_cnt(cnt)
    nit2 = int(np.sum(cr[:4] >= 2)); not2 = int(np.sum(cr[4:] >= 2))
    hits_l = cnt.sum(1)
    not2h = int(np.sum(hits_l[4:] >= 2))
    wv = U[hidx] @ np.cross(n, axis)
    core = (LC[hidx] <= 6)
    dwc = float(1.4826 * np.median(np.abs(wv[core] - np.median(wv[core])))) if core.sum() > 2 else float('nan')
    return dict(n=n, hidx=hidx, nit2=nit2, not2=not2, nl2=nit2 + not2, not2h=not2h, nl2h=nit2 + not2h,
                nl1=int(np.sum(cr >= 1)), chi2ndf=float(np.sum(d[sel] ** 2 * w) / max(int(sel.sum()) - 2, 1)),
                nhit=int(sel.sum()), dw_old=float(np.std(wv)), dw_core=dwc)


def thin_weights(hidx, LC, SD, INT, rho):
    """P(pass rung L | each interaction kept with q = 1/rho) and k_min(L) for every rung (no refit)."""
    ints, inv = np.unique(INT[hidx], return_inverse=True)
    m = len(ints)
    C = np.zeros((m, NL, 3), np.int64)
    np.add.at(C, (inv, LC[hidx], SD[hidx]), 1)
    C = C.reshape(m, -1)
    q = 1.0 / rho
    if m <= 12:
        masks = np.arange(1 << m, dtype=np.int64)
        Bm = ((masks[:, None] >> np.arange(m)) & 1).astype(np.int64)
        prob = None
    else:
        rng = np.random.default_rng(12345)
        Bm = (rng.random((20000, m)) < q).astype(np.int64)
        prob = 1.0 / len(Bm)
    cnt = (Bm @ C).reshape(len(Bm), NL, 3)
    cr = np.concatenate([cnt[:, :4, 0], np.minimum(cnt[:, 4:, 1], cnt[:, 4:, 2])], axis=1)
    nit2 = (cr[:, :4] >= 2).sum(1); nl2 = (cr >= 2).sum(1)
    size = Bm.sum(1)
    wts = (q ** size) * ((1 - q) ** (m - size)) if prob is None else np.full(len(Bm), prob)
    res = {}
    for L in RUNGS:
        ok = (nit2 >= 3) & (nl2 >= L)
        res[str(L)] = dict(p=float(wts[ok].sum()), kmin=int(size[ok].min()) if ok.any() else -1)
    return res, m


def build_hits(e):
    """e: (n, 12) PU (+signal) measurement array -> finder arrays (barrel counting layers only)."""
    sid = e[:, 0].astype(np.int64)
    keep = LC_OF[sid] >= 0
    e = e[keep]; sid = sid[keep]
    return e, sid


def topup(e, sid, rng, int_offset):
    """Extra random crossings per barrel layer (V4-2 density normalisation); returns rows in the same 12-column format."""
    rows = []
    s01 = {}
    for s_ in np.unique(sid):
        s01[s_] = e[sid == s_][0, 4:6]
    k = int_offset
    for li, name in enumerate(LAYERS):
        if TOPUP_MODE == 2 and li < 4:
            continue                                  # mode 2: OT layers only (IT cluster size not in the TDR)
        f = TOPUP[name] - 1.0
        if li < 4:
            ids = [SID[name]]
        else:
            ids = [SID[name + '_in'], SID[name + '_out']]
        z_pool = e[sid == ids[0], 3]
        if len(z_pool) == 0:
            continue
        ntop = rng.poisson(f * len(z_pool))
        zs = rng.choice(z_pool, ntop); ph = rng.uniform(-np.pi, np.pi, ntop)
        for s_ in ids:
            Rr = RAD[s_]
            blk = np.zeros((ntop, 12))
            blk[:, 0] = s_; blk[:, 1] = Rr * np.cos(ph); blk[:, 2] = Rr * np.sin(ph); blk[:, 3] = zs
            blk[:, 4:6] = s01[s_]; blk[:, 7] = -1; blk[:, 11] = 0
            blk[:, 8] = k + np.arange(ntop)          # unique 'interaction' per top-up crossing (stored in col 8 temporarily)
            rows.append(blk)
        k += ntop
    if not rows:
        return np.zeros((0, 12))
    return np.concatenate(rows)


def interaction_ids(e, vz, tag):
    """Map ACTS vertexPrimary -> interaction (prompt vertices of one interaction share the smeared z)."""
    zkey = {int(v[0]): round(float(v[3]), 6) for v in vz}
    uz = {z: i for i, z in enumerate(sorted(set(zkey.values())))}
    vp = e[:, 7].astype(np.int64)
    return np.array([tag * 100000 + uz.get(zkey.get(int(x), -1e9), 99999) for x in vp], np.int64), np.array(sorted(uz))


def trial(H, sid, INT, SIG, pv, phimet, rho, tseed):
    U0 = H[:, 1:4] - pv[None, :]
    r0 = np.hypot(U0[:, 0], U0[:, 1])
    dph = np.abs((np.arctan2(U0[:, 1], U0[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    m = dph < ROAD + np.arcsin(np.minimum(1.0, W_C / r0))
    U = np.ascontiguousarray(U0[m]); X = np.ascontiguousarray(H[m, 1]); Y = np.ascontiguousarray(H[m, 2])
    S0 = np.ascontiguousarray(H[m, 4]); S1 = np.ascontiguousarray(H[m, 5])
    sd = sid[m]; LC = LC_OF[sd]; SD = SIDE_OF[sd]; INTm = INT[m]; SIGm = SIG[m]
    phiU = np.arctan2(U[:, 1], U[:, 0]); etaU = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    A = np.where(sd == SID['TBPX_L4'])[0]; B = np.where(sd == SID['TBPX_L3'])[0]; C = np.where(sd == SID['TBPX_L2'])[0]
    t0 = time.time()
    out, ntrip = seeds(U, X, Y, S0, S1, LC, SD, A, B, C, phiU, etaU, phimet, ROAD, W_C, tseed, T_TOL)
    t_seed = time.time() - t0
    fast = []
    for ia, ib, n1, n2 in out:
        n = np.cross(U[ia], U[ib]); n /= np.linalg.norm(n)
        axis = U[ia] / np.linalg.norm(U[ia]) + U[ib] / np.linalg.norm(U[ib]); axis /= np.linalg.norm(axis)
        nf, nl2, nit2, chi, ns, axf = refit_nb(U, X, Y, S0, S1, LC, SD, n, axis, W_C, 3, T_TOL)
        if nl2 >= 4:
            fast.append((nl2, chi, nf, n, axis, n2))
    fast.sort(key=lambda t: (-t[0], t[1]))
    kept = []; seedmax = int(max([o[3] for o in out], default=0))
    for nl2, chi, nf, n, axis, n2 in fast:            # merge duplicates (normals within 2 mrad)
        if any(abs(abs(nf @ g['n']) - 1.0) < 2e-6 for g in kept):
            continue
        f = refit(U, X, Y, S0, S1, LC, SD, n, axis)
        if f is None:
            continue
        f['seed_n2'] = int(n2)
        kept.append(f)
    res = []
    for ic_, f in enumerate(kept):
        if f['nl2'] < 4:
            continue
        h = f['hidx']
        d = {k: f[k] for k in ('nit2', 'not2', 'nl2', 'not2h', 'nl2h', 'nl1', 'chi2ndf', 'nhit', 'dw_old', 'dw_core', 'seed_n2')}
        d['sigfrac'] = float(np.mean(SIGm[h] > 0)); d['n_sig'] = int(np.sum(SIGm[h] > 0))
        d['nz'] = float(abs(f['n'][2]))
        if f['nl2'] >= 5 and (rho > 1 or ic_ == 0):
            tw, mint = thin_weights(h[SIGm[h] == 0], LC, SD, INTm, rho) if d['n_sig'] == 0 else ({}, 0)
            d['thin'] = tw; d['n_int'] = mint
            if rho > 1 and d['n_sig'] == 0:
                pass
        res.append(d)
    return dict(n_road=int(m.sum()), n_trip=int(ntrip), n_refit=len(out), seed_n2_max=seedmax, t_seed=round(t_seed, 2),
                t_tot=round(time.time() - t0, 2), cands=res, n_sig_total=int(np.sum(SIG > 0)))


def load_pu():
    evs = []
    for f in sorted(PUD.glob('pu_w*.npz')):
        d = np.load(f)
        w = int(f.stem.split('_w')[1])
        for k in sorted([k for k in d.files if k.startswith('ev')], key=lambda k: int(k[2:])):
            evs.append((w * 100 + int(k[2:]), d[k], d['vz' + k[2:]]))
    return evs


def prep(e, vz, tag, rng, do_top):
    e, sid = build_hits(e)
    INT, uz = interaction_ids(e, vz, tag)
    SIG = np.zeros(len(e), np.int64)
    if do_top:
        t = topup(e, sid, rng, 0)
        if len(t):
            INT = np.concatenate([INT, tag * 100000 + 50000 + t[:, 8].astype(np.int64)])
            e = np.concatenate([e, t]); sid = np.concatenate([sid, t[:, 0].astype(np.int64)])
            SIG = np.concatenate([SIG, np.zeros(len(t), np.int64)])
    return e, sid, INT, SIG, uz


def lum_pv(rng):
    return np.array([rng.normal(0, 5e-3), rng.normal(0, 5e-3), rng.normal(0, 45.0)])


SIGPOINTS = [('F_m1000', 0.6), ('F_m1000', 1), ('F_m1000', 2), ('F_m1000', 3), ('F_m1000', 5), ('S_m500', 1), ('S_m500', 3),
             ('F_m200', 1), ('F_m200', 3), ('F_m1500', 1)]
NSIG = 12


def signal_events(rng):
    """Central (|eta_pair| < 1) status-1 TEMPLATE events from chunk c01 (rows recorded; R0 probes used c00)."""
    CAN = TT / 'data' / 'sim_stage3' / 'canon' / 'p2'
    out = []
    for sp, lam in SIGPOINTS:
        z = np.load(CAN / sp / f'L{lam:g}_BM_c01.npz', allow_pickle=False)
        off = z['hit_offsets']; kinds = [str(k) for k in z['surf_kinds']]; names = [str(k) for k in z['surf_names']]
        sel = [e for e in range(len(off) - 1) if int(z['status'][e]) == 1 and int(z['tt_split'][e]) == 0
               and bool(z['in_eta25'][e]) and abs(float(z['eta'][e])) < 1.0][:NSIG]
        for e in sel:
            sl = slice(off[e], off[e + 1])
            hs = z['h_surf'][sl]
            ok = np.array([kinds[s] not in ('T3V', 'ETL', 'BTL') for s in hs])
            out.append(dict(point=f'{sp}/L{lam:g}', row=int(z['row'][e]), vtx=np.array(z['vtx'][e][:3], float),
                            P=np.array(z['p_qp'][e], float) + np.array(z['p_qm'][e], float),
                            sid=np.array([SID[names[s]] for s in hs[ok]], np.int64),
                            xyz=np.c_[z['h_x'][sl], z['h_y'][sl], z['h_z'][sl]][ok], q=z['h_quirk'][sl][ok]))
    return out


def smear_signal(ev, s01, rng):
    rows = []
    for s_, (x, y, zz), q in zip(ev['sid'], ev['xyz'], ev['q']):
        if S[s_]['type'] != 0:
            continue        # barrel-only probe finder; disc hits are not counted
        s0, s1 = s01[s_]
        Rr = RAD[s_]
        ph = np.arctan2(y, x) + rng.normal(0, s0) / Rr
        rows.append((s_, Rr * np.cos(ph), Rr * np.sin(ph), zz + rng.normal(0, s1), s0, s1, 1 + q, -2, 0, 0, 0, 0))
    return np.array(rows, float).reshape(-1, 12)


if __name__ == '__main__':
    mode = sys.argv[1]; job = int(sys.argv[2]); njobs = int(sys.argv[3])
    TOPUP_MODE = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    do_top = TOPUP_MODE > 0
    tseed = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    evs = load_pu()
    rng = np.random.default_rng(1000 * job + 7 + (500 if do_top else 0) + {'pu': 0, 'pu2': 100, 'sig': 200}[mode])
    outf = OUTD / f'{mode}_t{TOPUP_MODE}_s{tseed}_tol{int(round(T_TOL * 1e3))}_j{job}.jsonl'
    fo = open(outf, 'w')
    import os
    T_TOL = float(os.environ.get('F1R_TTOL_UM', '30')) * 1e-3
    MAXEV = int(os.environ.get('F1R_MAXEV', '100000')); STRIDE = int(os.environ.get('F1R_SIGSTRIDE', '1'))
    MAXPAIRS = int(os.environ.get('F1R_MAXPAIRS', '100000'))
    if mode == 'pu':
        for i, (tag, e, vz) in enumerate(evs):
            if i % njobs != job or i >= MAXEV:
                continue
            H, sid, INT, SIG, uz = prep(e, vz, tag, rng, do_top)
            pv = lum_pv(rng); phi0 = rng.uniform(-np.pi, np.pi)
            dz = float(np.min(np.abs(uz - pv[2])))
            for k in range(4):
                r = trial(H, sid, INT, SIG, pv, float((phi0 + k * np.pi / 2 + np.pi) % (2 * np.pi) - np.pi), 1.0, tseed)
                r.update(ev=tag, road=k, dz_nearest_pu_mm=dz)
                fo.write(json.dumps(r) + '\n'); fo.flush()
                print(mode, tag, k, 'trip', r['n_trip'], 'refit', r['n_refit'], 't', r['t_tot'], 'best',
                      None if not r['cands'] else (r['cands'][0]['nl2'], r['cands'][0]['nit2'], r['cands'][0]['not2'], round(r['cands'][0]['chi2ndf'], 2)), flush=True)
    elif mode == 'pu2':
        pairs = [(2 * i, 2 * i + 1) for i in range(len(evs) // 2)]
        for i, (a, b) in enumerate(pairs):
            if i % njobs != job or i >= MAXPAIRS:
                continue
            Ha, sa, Ia, Sa, ua = prep(evs[a][1], evs[a][2], evs[a][0], rng, do_top)
            Hb, sb, Ib, Sb, ub = prep(evs[b][1], evs[b][2], evs[b][0], rng, do_top)
            H = np.concatenate([Ha, Hb]); sid = np.concatenate([sa, sb]); INT = np.concatenate([Ia, Ib]); SIG = np.concatenate([Sa, Sb])
            pv = lum_pv(rng); phi0 = rng.uniform(-np.pi, np.pi)
            for k in range(2):
                r = trial(H, sid, INT, SIG, pv, float((phi0 + k * np.pi + np.pi) % (2 * np.pi) - np.pi), 2.0, tseed)
                r.update(ev=[evs[a][0], evs[b][0]], road=k)
                fo.write(json.dumps(r) + '\n'); fo.flush()
                print(mode, i, k, 'trip', r['n_trip'], 'refit', r['n_refit'], 't', r['t_tot'], 'best',
                      None if not r['cands'] else (r['cands'][0]['nl2'], r['cands'][0]['nit2'], r['cands'][0]['not2'], round(r['cands'][0]['chi2ndf'], 2)), flush=True)
    elif mode == 'sig':
        sevs = signal_events(np.random.default_rng(5))
        for i, ev in enumerate(sevs):
            if i % njobs != job or i % STRIDE:
                continue
            tag, e, vz = evs[i % len(evs)]
            H, sid, INT, SIG, uz = prep(e, vz, tag, rng, do_top)
            s01 = {s_: H[sid == s_][0, 4:6] for s_ in np.unique(sid)}
            sh = smear_signal(ev, s01, rng)
            # put the signal vertex at the PU frame: the PU event's own vertices are independent luminous-region draws
            H = np.concatenate([H, sh]); sid = np.concatenate([sid, sh[:, 0].astype(np.int64)])
            INT = np.concatenate([INT, np.full(len(sh), -7, np.int64)]); SIG = np.concatenate([SIG, sh[:, 6].astype(np.int64)])
            pv = ev['vtx'] + np.array([rng.normal(0, 0.010), rng.normal(0, 0.010), rng.normal(0, 0.015)])
            met = ev['P'][:2] + rng.normal(0, 25.0, 2)
            r = trial(H, sid, INT, SIG, pv, float(np.arctan2(met[1], met[0])), 1.0, tseed)
            r.update(point=ev['point'], row=ev['row'], pu_ev=tag)
            fo.write(json.dumps(r) + '\n'); fo.flush()
            b = r['cands'][0] if r['cands'] else None
            print(mode, ev['point'], ev['row'], 'nsig', r['n_sig_total'], 'best', None if b is None else
                  (b['nl2'], b['nit2'], b['not2'], round(b['chi2ndf'], 2), b['n_sig'], round(b['sigfrac'], 2)), 't', r['t_tot'], flush=True)
    fo.close()
