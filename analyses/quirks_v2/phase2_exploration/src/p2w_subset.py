"""p2w_subset.py -- width-only subset-pass classification of pilot files (STR l.755-761).  Cecilie, 2026-11-19.

  <tt python> p2w_subset.py --id ID --out /ABS/OUT.npz (--files a.npz,b.npz | --manifest m.json) [--max-events N]

Plan: outputs/RULE1_VALID_PLAN_cecilie_2026-11-19.md (c), readings S1-S5 (mine, listed there; not an amendment).
Read-only on pilot files.  Pool, PV, road axes, weights: exactly those of p2t_classify.py variant 0 (all own hits on
the barrel counting surfaces, CKF-flagged rows kept, chain_inputs.merge_pool, no top-up).

Per (event, road orientation):
  planes   every pair (a, b) of road hits on two different IP layers (b the inner one, sin angle >= 1e-3) seeds the
           finder's own PV-constrained plane refit (kernels.refit_packed, unchanged, on the full pre-filter scan: hits
           within 3 sigma_tot, forward, |u.n2| < W_c, `iters` refits).  No seed score, no seed cuts, no merge.
           A plane is used if its final axis is aligned (|dphi(axis, MET)| < delta95, |eta(axis)| < eta_max).
  subset   for width W the subset of the plane's hits with w_core < W (w_core = 1.4826 MAD of u.n2 over the subset's
           IP hits, as kernels.cand_vars; > 2 IP hits) that holds the most double-crossing IP layers; all 2S hits kept.
           A subset is judged with ITS OWN axis (in-plane mean hit direction, as the finder's refit; forward,
           |u.n2| < W_c, alignment and w_core all with that axis), the full set with the finder's stored axis.
           Search: full set; else, for candidate axes (the plane's own; along each IP hit), windows of half-width
           W / 1.4826 at NOFF offsets, layers completed by outside hits, cheapest first, each addition kept only if
           w_core stays < W.  Every subset found is a witness: the result is exact or a lower bound on the maximum.
  k        (7 - N_IP2) + max(0, s - N_2S2) for s = 0 (n = 7) and s = 3 (n = 10); reading S: no N_IT2 requirement,
           reading F: N_IT2 >= 3 required of the subset.  Stored: min k over planes, per width (none, 37.5, 18.75, 9.4,
           4.7 mm), s, reading, for every (event, orientation) with some k <= floor((7 + s) / 2).
Exact prefilter (numba, on the unmerged rows, which are a superset): a road needs >= 4 double IP layers or >= 5 double
layers.  No signal file is read; no efficiency is formed.
"""
import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger('p2w_subset')
WL = np.array([1e9, 37.5, 18.75, 9.4, 4.7])          # mm; index 0 = no width cut (R04), then R05..R08
WNAMES = ['R04', 'R05', 'R06', 'R07', 'R08']
ROW_COLS = ['file', 'event', 'orient', 'cls', 'n_early_prod', 'w', 'n_road', 'n_seeds', 'n_planes', 'n_greedy'] + \
    [f'k_{wn}_s{s}_{rd}' for wn in WNAMES for s in (0, 3) for rd in 'SF']
KMAX = (3, 5)
NOFF = 7                                              # window centres per candidate axis, step W / 2.97


@njit(cache=True)
def _wcore(w, S, m, buf):
    k = 0
    for i in range(m):
        if S[i]:
            buf[k] = w[i]; k += 1
    if k <= 2:
        return np.inf
    c = np.median(buf[:k])
    for i in range(k):
        buf[i] = abs(buf[i] - c)
    return 1.4826 * np.median(buf[:k])


@njit(cache=True)
def _counts(lc, sd, S, m, cnt):
    cnt[:, :] = 0
    for i in range(m):
        if S[i]:
            cnt[lc[i], sd[i]] += 1
    nip2 = 0; nit2 = 0
    for l in range(7):
        cr = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
        if cr >= 2:
            nip2 += 1
            if l < 4:
                nit2 += 1
    return nip2, nit2


@njit(cache=True)
def _greedy(w, el, lc, sd, m, W, c, itfirst, S, buf, cnt, added):
    """Window of half-width W / 1.4826 around c over the eligible IP hits, plus outside hits completing layers
    (cheapest layer first; an addition is kept only if w_core stays < W).  The subset is left in S."""
    h = W / 1.4826
    for i in range(m):
        S[i] = el[i] and abs(w[i] - c) < h
    done = np.zeros(7, np.bool_)
    out = np.zeros((7, 3), np.int64)
    for step in range(7):
        _counts(lc, sd, S, m, cnt)
        out[:, :] = 0
        for i in range(m):
            if el[i] and not S[i]:
                out[lc[i], sd[i]] += 1
        best = -1; bkey = 10000
        for l in range(7):
            if done[l]:
                continue
            if l < 4:
                cost = max(0, 2 - cnt[l, 0]); av = out[l, 0] >= cost
            else:
                n1 = max(0, 2 - cnt[l, 1]); n2 = max(0, 2 - cnt[l, 2])
                cost = n1 + n2; av = (out[l, 1] >= n1) and (out[l, 2] >= n2)
            if cost == 0 or not av:
                done[l] = True
                continue
            key = cost + (100 if (itfirst and l >= 4) else 0)
            if key < bkey:
                bkey = key; best = l
        if best < 0:
            break
        done[best] = True
        na = 0
        for side in range(3):
            if (best < 4) != (side == 0):
                continue
            need = max(0, 2 - cnt[best, side])
            for q in range(need):
                bi = -1; bd = 1e300
                for i in range(m):
                    if el[i] and (not S[i]) and lc[i] == best and sd[i] == side and abs(w[i] - c) < bd:
                        bd = abs(w[i] - c); bi = i
                S[bi] = True; added[na] = bi; na += 1
        if not _wcore(w, S, m, buf) < W:
            for q in range(na):
                S[added[q]] = False


@njit(cache=True)
def _eval(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max, buf, c10):
    """Subset T of the plane's hits, judged with ITS OWN axis (in-plane mean hit direction, as the finder's refit):
    every IP hit forward and inside the collection window (2S hits that are not are dropped), axis aligned,
    w_core < W.  -> (ok, N_IP2, N_IT2, N_2S2)."""
    c = 1.0; s = 0.0
    for it in range(4):
        sx = 0.0; sy = 0.0
        for t in range(k):
            if T[t]:
                r = np.sqrt(p[t] * p[t] + q[t] * q[t])
                sx += p[t] / r; sy += q[t] / r
        nn = np.sqrt(sx * sx + sy * sy)
        if not nn > 0:
            return False, 0, 0, 0
        c = sx / nn; s = sy / nn
        changed = False
        for t in range(k):
            if T[t] and not ((p[t] * c + q[t] * s > 0) and (abs(-p[t] * s + q[t] * c) < wc)):
                if lc[t] <= 6:
                    return False, 0, 0, 0
                T[t] = False; changed = True
        if not changed:
            break
        if it == 3:
            return False, 0, 0, 0
    ax = c * aref[0] + s * n2ref[0]; ay = c * aref[1] + s * n2ref[1]; az = c * aref[2] + s * n2ref[2]
    dph = abs((np.arctan2(ay, ax) - phimet + np.pi) % (2 * np.pi) - np.pi)
    eta = np.arcsinh(az / max(np.sqrt(ax * ax + ay * ay), 1e-12))
    if not (dph < road and abs(eta) < eta_max):
        return False, 0, 0, 0
    kk = 0
    c10[:, :] = 0
    for t in range(k):
        if T[t]:
            c10[lc[t], sd[t]] += 1
            if lc[t] <= 6:
                buf[kk] = -p[t] * s + q[t] * c; kk += 1
    if kk <= 2:
        return False, 0, 0, 0
    med = np.median(buf[:kk])
    for i in range(kk):
        buf[i] = abs(buf[i] - med)
    if not 1.4826 * np.median(buf[:kk]) < W:
        return False, 0, 0, 0
    nip2 = 0; nit2 = 0; n2s2 = 0
    for l in range(10):
        cr = c10[l, 0] if l < 4 else min(c10[l, 1], c10[l, 2])
        if cr >= 2:
            if l < 7:
                nip2 += 1
                if l < 4:
                    nit2 += 1
            else:
                n2s2 += 1
    return True, nip2, nit2, n2s2


@njit(cache=True)
def plane_best(p, q, lc, sd, k, WLa, wc, aref, n2ref, phimet, road, eta_max, kS, kF):
    """Hits of one aligned plane: p = u.axis, q = u.n2 (the finder's final axis), layer 0..9, side 0/1/2.
    Fills kS, kF (nW, 2): the smallest k = (7 - N_IP2) + max(0, s - N_2S2), s = 0 / 3, over the subsets found with
    w_core < W (kF: N_IT2 >= 3 required); 99 = none.  -> n_greedy."""
    nW = WLa.shape[0]
    kS[:, :] = 99; kF[:, :] = 99
    ipi = np.empty(k, np.int64)
    m = 0
    c10 = np.zeros((10, 3), np.int64)
    for t in range(k):
        c10[lc[t], sd[t]] += 1
        if lc[t] <= 6:
            ipi[m] = t; m += 1
    nipf = 0; nitf = 0; n2sf = 0
    for l in range(10):
        cr = c10[l, 0] if l < 4 else min(c10[l, 1], c10[l, 2])
        if cr >= 2:
            if l < 7:
                nipf += 1
                if l < 4:
                    nitf += 1
            else:
                n2sf += 1
    w = np.empty(m); el = np.ones(m, np.bool_); l_ = np.empty(m, np.int64); s_ = np.empty(m, np.int64)
    for i in range(m):
        w[i] = q[ipi[i]]; l_[i] = lc[ipi[i]]; s_[i] = sd[ipi[i]]
    S = np.ones(m, np.bool_); buf = np.empty(max(k, 1)); cnt = np.zeros((7, 3), np.int64); added = np.empty(8, np.int64)
    T = np.empty(k, np.bool_)
    wfull = _wcore(w, S, m, buf)               # the finder's w_core of the full set (its own stored axis)
    ng = 0
    for wi in range(nW):
        W = WLa[wi]
        if wi == 0 or wfull < W:               # the full set (the finder's choice) holds every layer of the plane
            for si in range(2):
                kS[wi, si] = 7 - nipf + max(0, 3 * si - n2sf)
                if nitf >= 3:
                    kF[wi, si] = kS[wi, si]
            continue                           # no subset has more layers than the full set
        if m <= 2:
            continue
        lo0 = 7 - nipf; lo1 = 7 - nipf + max(0, 3 - n2sf)
        h = W / 1.4826
        for a in range(-1, m):                 # candidate axes: the plane's own (a = -1), then along each IP hit
            if a < 0:
                ca = 1.0; sa = 0.0
            else:
                r = np.sqrt(p[ipi[a]] ** 2 + q[ipi[a]] ** 2)
                ca = p[ipi[a]] / r; sa = q[ipi[a]] / r
            for i in range(m):
                t = ipi[i]
                w[i] = -p[t] * sa + q[t] * ca
                el[i] = (p[t] * ca + q[t] * sa > 0) and (abs(w[i]) < wc)
            c0 = 0.0
            if a < 0:
                kk = 0
                for i in range(m):
                    if el[i]:
                        buf[kk] = w[i]; kk += 1
                if kk == 0:
                    continue
                c0 = np.median(buf[:kk])
            for ci in range(NOFF):
                c = c0 + (ci - NOFF // 2) * 0.5 * h
                for mode in range(2):
                    _greedy(w, el, l_, s_, m, W, c, mode == 1, S, buf, cnt, added)
                    ng += 1
                    for t in range(k):
                        T[t] = True
                    for i in range(m):
                        T[ipi[i]] = S[i]
                    ok, nip2, nit2, n2s2 = _eval(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max, buf, c10)
                    if ok:
                        for si in range(2):
                            kk_ = 7 - nip2 + max(0, 3 * si - n2s2)
                            if kk_ < kS[wi, si]:
                                kS[wi, si] = kk_
                            if nit2 >= 3 and kk_ < kF[wi, si]:
                                kF[wi, si] = kk_
            if kS[wi, 0] <= lo0 and kS[wi, 1] <= lo1 and (nitf < 3 or (kF[wi, 0] <= lo0 and kF[wi, 1] <= lo1)):
                break
    return ng


@njit(cache=True)
def subset_road(U, CX, CY, S0, S1, LC, SD, J, phimet, road, eta_max, wc, ttol, iters, WLa, refit):
    """All road hits of one (event, orientation) in the PV frame.  -> (kb (nW, 2, 2) min k [s = 0 / 3][S / F], n_seeds,
    n_planes evaluated, n_greedy, n_sigma_bad)."""
    n = U.shape[0]
    nW = WLa.shape[0]
    kb = np.full((nW, 2, 2), 99, np.int64)
    P = np.empty((6, n))
    SF = np.zeros((16, 8)); seen = np.zeros(16, np.bool_); bad = 0
    for i in range(n):
        P[0, i] = U[i, 0]; P[1, i] = U[i, 1]; P[2, i] = U[i, 2]; P[3, i] = CX[i]; P[4, i] = CY[i]
        P[5, i] = np.sqrt(U[i, 0] ** 2 + U[i, 1] ** 2 + U[i, 2] ** 2)
        j = J[i]
        if not seen[j]:
            seen[j] = True; SF[j, 3] = S0[i]; SF[j, 4] = S1[i]
        elif SF[j, 3] != S0[i] or SF[j, 4] != S1[i]:
            bad += 1
    pid = np.arange(n).astype(np.int64)
    L = np.empty(n, np.int64); sel = np.empty(n, np.int64); selp = np.empty(n, np.int64); selw = np.empty(n)
    M = np.zeros((3, 3)); cnt = np.zeros((10, 3), np.int64); sgu = np.empty(16)
    n0 = np.empty(3); ax0 = np.empty(3)
    wv = np.empty(n); lcv = np.empty(n, np.int64); sdv = np.empty(n, np.int64)
    kS = np.empty((nW, 2), np.int64); kF = np.empty((nW, 2), np.int64)
    pv_ = np.empty(n); aref = np.empty(3); n2ref = np.empty(3)
    sigs = set()
    sigs.add(np.int64(-1))
    nseed = 0; nplane = 0; ngreedy = 0
    if bad:
        return kb, nseed, nplane, ngreedy, bad
    for ia in range(n):
        if LC[ia] > 6:
            continue
        for ib in range(n):
            if LC[ib] >= LC[ia]:
                continue
            cx_ = U[ia, 1] * U[ib, 2] - U[ia, 2] * U[ib, 1]
            cy_ = U[ia, 2] * U[ib, 0] - U[ia, 0] * U[ib, 2]
            cz_ = U[ia, 0] * U[ib, 1] - U[ia, 1] * U[ib, 0]
            nc = np.sqrt(cx_ * cx_ + cy_ * cy_ + cz_ * cz_)
            na = P[5, ia]; nb = P[5, ib]
            if not nc >= 1e-3 * na * nb:
                continue
            a0x = U[ia, 0] / na + U[ib, 0] / nb; a0y = U[ia, 1] / na + U[ib, 1] / nb; a0z = U[ia, 2] / na + U[ib, 2] / nb
            an = np.sqrt(a0x * a0x + a0y * a0y + a0z * a0z)
            if not an > 1e-9:
                continue
            n0[0] = cx_ / nc; n0[1] = cy_ / nc; n0[2] = cz_ / nc
            ax0[0] = a0x / an; ax0[1] = a0y / an; ax0[2] = a0z / an
            m = 0
            cnt[:, :] = 0
            for p in range(n):
                if abs(P[0, p] * n0[0] + P[1, p] * n0[1] + P[2, p] * n0[2]) < (60.0 if LC[p] >= 7 else 5.0):
                    L[m] = p; m += 1
                    cnt[LC[p], SD[p]] += 1
            nseed += 1
            nl2p = 0                    # exact: the refit selects among L only, and a plane needs N_L2 >= 4 below
            for l in range(10):
                if (cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])) >= 2:
                    nl2p += 1
            if nl2p < 4:
                continue
            (st, nx, ny, nz, nl2, nit2, chi, nsel, ax, ay, az, dmax, nfin,
             itr) = refit(L, m, P, J, LC, SD, pid, n0, ax0, wc, iters, ttol, 2.5, SF, sel, M, cnt, sgu, selp, selw, 0,
                          n0[0], n0[1], n0[2])
            if st != 0 or nl2 < 4:
                continue
            dph = abs((np.arctan2(ay, ax) - phimet + np.pi) % (2 * np.pi) - np.pi)
            eta = np.arcsinh(az / max(np.sqrt(ax * ax + ay * ay), 1e-12))
            if not (dph < road and abs(eta) < eta_max):
                continue
            sg = np.int64(nfin)
            for q in range(nfin):
                sg = (sg * 1000003 + sel[q] + 1) % 2305843009213693951
            if sg in sigs:
                continue
            sigs.add(sg)
            n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
            aref[0] = ax; aref[1] = ay; aref[2] = az; n2ref[0] = n2x; n2ref[1] = n2y; n2ref[2] = n2z
            for q in range(nfin):
                p = sel[q]
                pv_[q] = P[0, p] * ax + P[1, p] * ay + P[2, p] * az
                wv[q] = P[0, p] * n2x + P[1, p] * n2y + P[2, p] * n2z
                lcv[q] = LC[p]; sdv[q] = SD[p]
            ng = plane_best(pv_, wv, lcv, sdv, nfin, WLa, wc, aref, n2ref, phimet, road, eta_max, kS, kF)
            nplane += 1; ngreedy += ng
            for wi in range(nW):
                for si in range(2):
                    if kS[wi, si] < kb[wi, si, 0]:
                        kb[wi, si, 0] = kS[wi, si]
                    if kF[wi, si] < kb[wi, si, 1]:
                        kb[wi, si, 1] = kF[wi, si]
    return kb, nseed, nplane, ngreedy, bad


@njit(cache=True)
def prefilter(x, y, z, lc, sd, off, pvs, axis0, use, norient, road, wc):
    """-> (n_events, norient) bool: the road holds >= 4 double IP layers or >= 5 double layers (necessary for any
    stored k).  lc < 0 rows (not barrel counting surfaces) are ignored.  Road as finder.road_select."""
    nev = off.shape[0] - 1
    ok = np.zeros((nev, norient), np.bool_)
    cnt = np.zeros((10, 3), np.int64)
    for i in range(nev):
        if not use[i]:
            continue
        a = off[i]; b = off[i + 1]
        nb = 0
        for h in range(a, b):
            if lc[h] >= 0:
                nb += 1
        if nb < 8:
            continue
        cnt[:, :] = 0
        for h in range(a, b):
            if lc[h] >= 0:
                cnt[lc[h], sd[h]] += 1
        nip = 0; nall = 0
        for l in range(10):
            cr = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
            if cr >= 2:
                nall += 1
                if l < 7:
                    nip += 1
        if nip < 4 and nall < 5:
            continue
        for k in range(norient):
            phim = (axis0[i] + 2 * np.pi * k / norient + np.pi) % (2 * np.pi) - np.pi
            cnt[:, :] = 0
            for h in range(a, b):
                if lc[h] < 0:
                    continue
                ux = x[h] - pvs[i, 0]; uy = y[h] - pvs[i, 1]
                r0 = np.sqrt(ux * ux + uy * uy)
                dph = abs((np.arctan2(uy, ux) - phim + np.pi) % (2 * np.pi) - np.pi)
                if dph < road + np.arcsin(min(1.0, wc / r0)):
                    cnt[lc[h], sd[h]] += 1
            nip = 0; nall = 0
            for l in range(10):
                cr = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
                if cr >= 2:
                    nall += 1
                    if l < 7:
                        nip += 1
            ok[i, k] = (nip >= 4) or (nall >= 5)
    return ok


def classify_pool(Hm, pv, phim, cfg, wcfg, FF, K):
    """Merged pool rows (13 columns), PV, road axis -> (kb, n_road, n_seeds, n_planes, n_greedy, n_sigma_bad)."""
    sidm = Hm[:, 0].astype(np.int64)
    m, U0 = FF.road_select(Hm, sidm, pv, phim, cfg)
    nr = int(m.sum())
    if nr < 8:
        return np.full((len(WL), 2, 2), 99, np.int64), nr, 0, 0, 0, 0
    U = np.ascontiguousarray(U0[m]); X = Hm[m, 1]; Y = Hm[m, 2]
    rH = np.hypot(X, Y)
    sd = sidm[m]
    kb, ns, npl, ng, bad = subset_road(U, np.ascontiguousarray(X / rH), np.ascontiguousarray(Y / rH),
                                       np.ascontiguousarray(Hm[m, 4]), np.ascontiguousarray(Hm[m, 5]), FF.LC_OF[sd],
                                       FF.SIDE_OF[sd], FF.JLOC_OF[sd], float(phim), float(wcfg.delta95),
                                       float(wcfg.eta_max), float(cfg.w_c), float(cfg.t_tol), int(cfg.iters), WL,
                                       K.refit_packed)
    return kb, nr, ns, npl, ng, bad


def load_frozen():
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)
    from acts.stage4 import run_stage4 as RS
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import finder as FF
    from acts.stage4.finder import kernels as K
    from acts.stage4.finder import production as PR
    from acts.stage4.finder import g1b_tt as GT
    fz = RS.frozen_inputs()
    if fz is None or fz.get('wp_rule_sha256') != RS.sha256_file(RS.HERE / 'WP_RULE.md'):
        raise SystemExit('frozen_inputs / WP_RULE.md mismatch')
    cfg, wcfg = PR.config_from_frozen(fz)
    return RS, CI, FF, K, GT, cfg, wcfg


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p2w_subset %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--files', default='')
    ap.add_argument('--manifest', default='')
    ap.add_argument('--max-events', type=int, default=0)
    a = ap.parse_args()
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    RS, CI, FF, K, GT, cfg, wcfg = load_frozen()
    PV_SIGMA = np.array([0.010, 0.010, 0.015])
    if not np.allclose(GT.PV_SIGMA, PV_SIGMA):
        raise SystemExit('PV_SIGMA differs from v1 g1b_tt.PV_SIGMA')
    paths = json.loads(Path(a.manifest).read_text())[a.id] if a.manifest else a.files.split(',')
    rows = []; files = []; errors = []
    tot = dict(n_pref=0, n_seeds=0, n_planes=0, n_greedy=0, max_seeds=0, max_road=0, t_kernel=0.0)
    for fi, path in enumerate(paths):
        z = np.load(path)
        meta = json.loads(str(z['meta']))
        stream = meta['stream']; ec = meta['evt_cols']
        hits = z['hits']; off = z['hit_off'].astype(np.int64); evt = z['evt']
        tru = z['tru']
        nev = int(meta['n_events'])
        if len(off) != nev + 1 or len(evt) != nev:
            raise SystemExit(f'{path}: offsets/evt do not match n_events')
        is_z = stream == 'pilot.hs0.znn'
        if is_z:
            w = evt[:, ec.index('w_v1')].astype(np.float64); cls = np.full(nev, -1); nep = np.zeros(nev, np.int64)
            axis0 = evt[:, ec.index('phimet_reco_v1')].astype(np.float64); norient = 1
            vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
            pvs = np.zeros((nev, 3))
            for i in np.where(w > 0)[0]:           # p2t_classify.py's PV draw, same seed string
                h = hashlib.blake2b(f'p2t-pv|{stream}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
                pvs[i] = vtx[i] + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
        else:
            w = np.ones(nev); cls = evt[:, ec.index('cls')].astype(np.int64); nep = z['n_early_prod'].astype(np.int64)
            axis0 = evt[:, ec.index('phi_road')].astype(np.float64)
            norient = 1 if stream == 'pilot.c0.hs' else int(meta['road_orientations']['n'])
            pvs = evt[:, [ec.index('pv_x'), ec.index('pv_y'), ec.index('pv_z')]].astype(np.float64)
        nmax = nev if not a.max_events else min(nev, a.max_events)
        use = w > 0
        use[nmax:] = False
        sid_all = hits[:, 0].astype(np.int64)
        lc_all = FF.LC_OF[sid_all]
        pf = prefilter(hits[:, 1].astype(np.float64), hits[:, 2].astype(np.float64), hits[:, 3].astype(np.float64),
                       lc_all, FF.SIDE_OF[sid_all], off, pvs, axis0, use, norient, float(cfg.road), float(cfg.w_c))
        fm = dict(path=path, stream=stream, chunk=meta['chunk'], n_events=nev, n_classified_range=nmax, n_orient=norient,
                  n_w_positive=int((w[:nmax] > 0).sum()), n_early_events=int((nep[:nmax] > 0).sum()),
                  n_prefilter_pass=int(pf.sum()))
        if is_z:
            fm['w_max'] = float(w[:nmax].max())
            fm['w_hist'] = {str(k): int(c) for k, c in zip(*np.unique(np.round(w[:nmax], 4), return_counts=True))}
        else:
            fm['cls_counts'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax], return_counts=True))}
        files.append(fm)
        for i in np.where(pf.any(1))[0]:
            s = slice(int(off[i]), int(off[i + 1]))
            b = lc_all[s] >= 0
            Hm = CI.merge_pool(hits[s][b].astype(np.float64), tru[s][b].astype(np.float64))[0]
            for k in np.where(pf[i])[0]:
                phim = float((axis0[i] + 2 * np.pi * k / norient + np.pi) % (2 * np.pi) - np.pi)
                t0 = time.perf_counter()
                kb, nr, ns, npl, ng, bad = classify_pool(Hm, pvs[i], phim, cfg, wcfg, FF, K)
                tot['t_kernel'] += time.perf_counter() - t0
                tot['n_pref'] += 1; tot['n_seeds'] += ns; tot['n_planes'] += npl; tot['n_greedy'] += ng
                tot['max_seeds'] = max(tot['max_seeds'], ns); tot['max_road'] = max(tot['max_road'], nr)
                if bad:
                    errors.append(dict(file=fi, event=int(i), orient=int(k), error=f'{bad} hits with non-constant sigma'))
                    continue
                if (kb[:, 0, :] <= KMAX[0]).any() or (kb[:, 1, :] <= KMAX[1]).any():
                    rows.append([fi, i, k, cls[i], nep[i], w[i], nr, ns, npl, ng, *kb.reshape(-1)])
        z.close()
        log.info('%s: %d events, %d prefilter passes, %d rows so far, %.1f s', Path(path).name, nmax, fm['n_prefilter_pass'],
                 len(rows), time.perf_counter() - t_w0)
    summ = dict(id=a.id, files=files, row_cols=ROW_COLS, widths=WL.tolist(), kmax=KMAX, n_errors=len(errors),
                errors=errors[:200], totals=tot,
                config=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol, iters=cfg.iters, delta95=wcfg.delta95,
                            eta_max=wcfg.eta_max),
                frozen_inputs_sha256=RS.sha256_file(RS.HERE / 'frozen_inputs.json'),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                wall_s=time.perf_counter() - t_w0, cpu_s=time.process_time() - t_c0)
    out = Path(a.out)
    part = out.with_name(out.name + '.part')
    with open(part, 'wb') as f:
        np.savez_compressed(f, meta=json.dumps(summ), rows=np.array(rows, np.float64).reshape(-1, len(ROW_COLS)))
        f.flush(); os.fsync(f.fileno())
    part.replace(out)
    log.info('done: %d rows, %d errors, cpu %.1f s, totals %s', len(rows), len(errors), summ['cpu_s'], tot)
    return 0


if __name__ == '__main__':
    sys.exit(main())
