"""p3a_subset.py -- FINAL own-hit (subset-pass) classification of pilot files, every reading the frozen text allows.
Aurora, 2026-11-24 (work package p3-a).  Plan: phase3_selection/logs/executor_aurora_2026-11-24_10-16.md.

  <tt python> p3a_subset.py --id ID --out /ABS/OUT.npz (--files a.npz,b.npz | --manifest m.json)
              [--no-merge] [--pv draw|draw2|true] [--w-select pos|zero|all] [--max-events N]

BASE reading = phase2_exploration/src/p2w_subset.py IMPORTED UNCHANGED (sha256 checked): its plane_best, prefilter,
_greedy, _eval, _wcore.  The road loop below is a copy of its subset_road (Phase-2 code may be copied, not edited) with
the calls for the additional categories; the BASE numbers must therefore equal the Phase-2 rows (checked downstream).

Per aligned plane (hits selected by the finder's refit kernel, its final normal and axis) and per width W in
WL = (none, 75, 37.5, 18.75, 9.4, 4.7 mm), the smallest deficit k = (7 - N_IP2) + max(0, s - N_2S2), s = 0 / 3, readings
S (no N_IT2 requirement) and F (N_IT2 >= 3), in five categories of witness:
  c0  the full set, judged with the finder's stored axis (w_core of the finder; 'none': always)   [Phase-2 branch 1]
  c1  the full set, judged with ITS OWN axis (p2w_subset._eval convention)
  c2  window-and-fill subsets, Phase-2 heuristic (axes: the plane's and along each IP hit; NOFF offsets), own axis
  c3  window-and-fill subsets with the centres of PLAN S4 as written (every IP hit and every midpoint of neighbours,
      the plane's axis), own axis
  c4  hard-window witnesses: any own-axis witness (c1, c2, c3, or a pure window [w_j, w_j + 2W/1.4826)) whose IP hits
      all lie inside one window of full width 2 W / 1.4826 (Nils's reading H)
c2, c3 are searched at a width only if c0 or c1 fails there (no subset holds more layers than a passing full set);
pure windows only if c1 is not a hard-window witness.  Every stored k has a witness that passed _eval2 (a copy of
p2w_subset._eval that also returns the spread) or is the finder's full set: exact or a lower bound on the maximum.
For s = 3 the k_IP of the best witness (ties: smallest k_IP) is stored (k per layer type).
Witness of the smallest k at (target width, s = 0, S) over c0..c4: hit-truth summary; full hit table for non-Z rows.
No signal file is read; no efficiency is formed.
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
QV2 = HERE.parents[2]
sys.path.insert(0, str(QV2 / 'phase2_exploration' / 'src'))
import p2w_subset as B  # noqa: E402   (Phase-2 classifier, unchanged)

log = logging.getLogger('p3a_subset')
P2W_SHA256_PREFIX = 'c68b7b69'                         # the hash in all 139 Phase-2 job outputs (ING l.42, NIL l.4)
WL = np.array([1e9, 75.0, 37.5, 18.75, 9.4, 4.7])     # mm; 0 = collection window only, 1 = w_core < W_c (STR l.761-762)
WNAMES = ['R04n', 'R04w', 'R05', 'R06', 'R07', 'R08']
CATS = ['c0', 'c1', 'c2', 'c3', 'c4']
NC = len(CATS)
KMAX = (3, 5)
TW_DEFAULT = 5                                        # witness target: R08
I_COLS = (['file', 'event', 'orient', 'cls', 'n_early_prod', 'n_road', 'n_planes']
          + [f'kb_{wn}_s{s}_{rd}' for wn in WNAMES for s in (0, 3) for rd in 'SF']
          + [f'k_{c}_{wn}_s{s}_{rd}' for c in CATS for wn in WNAMES for s in (0, 3) for rd in 'SF']
          + [f'kip_{c}_{wn}_{rd}' for c in CATS for wn in WNAMES for rd in 'SF']
          + ['wit_k', 'wit_nhit', 'wit_npart', 'wit_nprod', 'wit_ngen', 'wit_nckf', 'wit_nip2', 'wit_n2s2'])
F_COLS = ['w', 'n_seeds']
_pb = B.plane_best
_greedy = B._greedy
_wcore = B._wcore


@njit(cache=True)
def _eval2(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max, buf, c10):
    """Copy of p2w_subset._eval (own axis; 2S hits failing forward / window dropped, an IP hit failing rejects;
    alignment; w_core < W) that also returns the spread max - min of u.n2 over the IP hits of the subset.
    -> (ok, N_IP2, N_IT2, N_2S2, spread)."""
    c = 1.0; s = 0.0
    for it in range(4):
        sx = 0.0; sy = 0.0
        for t in range(k):
            if T[t]:
                r = np.sqrt(p[t] * p[t] + q[t] * q[t])
                sx += p[t] / r; sy += q[t] / r
        nn = np.sqrt(sx * sx + sy * sy)
        if not nn > 0:
            return False, 0, 0, 0, 0.0
        c = sx / nn; s = sy / nn
        changed = False
        for t in range(k):
            if T[t] and not ((p[t] * c + q[t] * s > 0) and (abs(-p[t] * s + q[t] * c) < wc)):
                if lc[t] <= 6:
                    return False, 0, 0, 0, 0.0
                T[t] = False; changed = True
        if not changed:
            break
        if it == 3:
            return False, 0, 0, 0, 0.0
    ax = c * aref[0] + s * n2ref[0]; ay = c * aref[1] + s * n2ref[1]; az = c * aref[2] + s * n2ref[2]
    dph = abs((np.arctan2(ay, ax) - phimet + np.pi) % (2 * np.pi) - np.pi)
    eta = np.arcsinh(az / max(np.sqrt(ax * ax + ay * ay), 1e-12))
    if not (dph < road and abs(eta) < eta_max):
        return False, 0, 0, 0, 0.0
    kk = 0
    c10[:, :] = 0
    lo = 1e300; hi = -1e300
    for t in range(k):
        if T[t]:
            c10[lc[t], sd[t]] += 1
            if lc[t] <= 6:
                v = -p[t] * s + q[t] * c
                buf[kk] = v; kk += 1
                lo = min(lo, v); hi = max(hi, v)
    if kk <= 2:
        return False, 0, 0, 0, 0.0
    med = np.median(buf[:kk])
    for i in range(kk):
        buf[i] = abs(buf[i] - med)
    if not 1.4826 * np.median(buf[:kk]) < W:
        return False, 0, 0, 0, 0.0
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
    return True, nip2, nit2, n2s2, hi - lo


@njit(cache=True)
def _rec(KC, KI, c, wi, nip2, nit2, n2s2):
    """Record a witness in category c at width wi.  KC (NC, nW, 2, 2) min k [s][S/F]; KI (NC, nW, 2) k_IP at s = 3."""
    kip = 7 - nip2
    for si in range(2):
        kk = kip + max(0, 3 * si - n2s2)
        for rd in range(2):
            if rd == 1 and nit2 < 3:
                continue
            if kk < KC[c, wi, si, rd]:
                KC[c, wi, si, rd] = kk
                if si == 1:
                    KI[c, wi, rd] = kip
            elif si == 1 and kk == KC[c, wi, si, rd] and kip < KI[c, wi, rd]:
                KI[c, wi, rd] = kip


@njit(cache=True)
def plane_cats(p, q, lc, sd, k, WLa, wc, aref, n2ref, phimet, road, eta_max, KC, KI, tw, wit, wk, noff):
    """Hits of one aligned plane (p = u.axis, q = u.n2 of the finder's final axis, layer 0..9, side 0/1/2).
    Fills KC, KI (see _rec); wit (k,) / wk[0]: witness mask and k of the smallest k at (tw, s = 0, S).  -> n_eval."""
    nW = WLa.shape[0]
    KC[:, :, :, :] = 99; KI[:, :, :] = 99; wk[0] = 99
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
    T = np.empty(k, np.bool_); ws = np.empty(max(m, 1))
    wfull = _wcore(w, S, m, buf)
    ne = 0
    lo0 = 7 - nipf
    for wi in range(nW):
        W = WLa[wi]
        h = W / 1.4826
        c0ok = (wi == 0) or (wfull < W)
        if c0ok:
            _rec(KC, KI, 0, wi, nipf, nitf, n2sf)
            if wi == tw and lo0 < wk[0]:
                wk[0] = lo0
                for t in range(k):
                    wit[t] = True
        for t in range(k):
            T[t] = True
        ok, nip2, nit2, n2s2, spr = _eval2(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max, buf, c10)
        ne += 1
        c1ok = False; c1hard = False
        if ok:
            c1ok = True
            _rec(KC, KI, 1, wi, nip2, nit2, n2s2)
            if spr < 2.0 * h:
                c1hard = True
                _rec(KC, KI, 4, wi, nip2, nit2, n2s2)
            if wi == tw and 7 - nip2 < wk[0]:
                wk[0] = 7 - nip2
                for t in range(k):
                    wit[t] = T[t]
        if m <= 2:
            continue
        if not (c0ok and c1ok):
            # c2: the Phase-2 heuristic (p2w_subset.plane_best l.232-267), without its early exit
            for a in range(-1, m):
                if a < 0:
                    ca = 1.0; sa = 0.0
                else:
                    r = np.sqrt(p[ipi[a]] ** 2 + q[ipi[a]] ** 2)
                    ca = p[ipi[a]] / r; sa = q[ipi[a]] / r
                for i in range(m):
                    t = ipi[i]
                    w[i] = -p[t] * sa + q[t] * ca
                    el[i] = (p[t] * ca + q[t] * sa > 0) and (abs(w[i]) < wc)
                c0_ = 0.0
                if a < 0:
                    kk = 0
                    for i in range(m):
                        if el[i]:
                            buf[kk] = w[i]; kk += 1
                    if kk == 0:
                        continue
                    c0_ = np.median(buf[:kk])
                for ci in range(noff):
                    cc = c0_ + (ci - noff // 2) * 0.5 * h
                    for mode in range(2):
                        _greedy(w, el, l_, s_, m, W, cc, mode == 1, S, buf, cnt, added)
                        for t in range(k):
                            T[t] = True
                        for i in range(m):
                            T[ipi[i]] = S[i]
                        ok, nip2, nit2, n2s2, spr = _eval2(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max,
                                                           buf, c10)
                        ne += 1
                        if ok:
                            _rec(KC, KI, 2, wi, nip2, nit2, n2s2)
                            if spr < 2.0 * h:
                                _rec(KC, KI, 4, wi, nip2, nit2, n2s2)
                            if wi == tw and 7 - nip2 < wk[0]:
                                wk[0] = 7 - nip2
                                for t in range(k):
                                    wit[t] = T[t]
            # c3: PLAN S4 centres as written: every IP hit and every midpoint of neighbours, the plane's axis
            kk = 0
            for i in range(m):
                t = ipi[i]
                w[i] = q[t]
                el[i] = (p[t] > 0) and (abs(w[i]) < wc)
                if el[i]:
                    ws[kk] = w[i]; kk += 1
            if kk > 0:
                wsrt = np.sort(ws[:kk])
                for ci in range(2 * kk - 1):
                    if ci % 2 == 0:
                        cc = wsrt[ci // 2]
                    else:
                        cc = 0.5 * (wsrt[ci // 2] + wsrt[ci // 2 + 1])
                    for mode in range(2):
                        _greedy(w, el, l_, s_, m, W, cc, mode == 1, S, buf, cnt, added)
                        for t in range(k):
                            T[t] = True
                        for i in range(m):
                            T[ipi[i]] = S[i]
                        ok, nip2, nit2, n2s2, spr = _eval2(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max,
                                                           buf, c10)
                        ne += 1
                        if ok:
                            _rec(KC, KI, 3, wi, nip2, nit2, n2s2)
                            if spr < 2.0 * h:
                                _rec(KC, KI, 4, wi, nip2, nit2, n2s2)
                            if wi == tw and 7 - nip2 < wk[0]:
                                wk[0] = 7 - nip2
                                for t in range(k):
                                    wit[t] = T[t]
        if not c1hard:
            # pure hard windows [w_j, w_j + 2h) over the IP hits (plane's axis), all 2S hits kept, no fill
            for j in range(m):
                tj = ipi[j]
                if not (p[tj] > 0 and abs(q[tj]) < wc):
                    continue
                lo = q[tj]
                for t in range(k):
                    T[t] = True
                for i in range(m):
                    t = ipi[i]
                    T[t] = (p[t] > 0) and (abs(q[t]) < wc) and (q[t] >= lo) and (q[t] < lo + 2.0 * h)
                ok, nip2, nit2, n2s2, spr = _eval2(p, q, lc, sd, k, T, wc, W, aref, n2ref, phimet, road, eta_max, buf, c10)
                ne += 1
                if ok and spr < 2.0 * h:
                    _rec(KC, KI, 4, wi, nip2, nit2, n2s2)
                    if wi == tw and 7 - nip2 < wk[0]:
                        wk[0] = 7 - nip2
                        for t in range(k):
                            wit[t] = T[t]
    return ne


@njit(cache=True)
def road_multi(U, CX, CY, S0, S1, LC, SD, J, phimet, road, eta_max, wc, ttol, iters, WLa, refit, tw, noff, wmask):
    """Copy of p2w_subset.subset_road (seeding, pre-gather 5 / 60 mm, refit, alignment) with both classifications per
    plane.  -> (kb (nW, 2, 2) BASE, KCb (NC, nW, 2, 2), KIb (NC, nW, 2), n_seeds, n_planes, n_eval, n_sigma_bad, wk);
    wmask (n,) is the witness of wk over the road hits."""
    n = U.shape[0]
    nW = WLa.shape[0]
    kb = np.full((nW, 2, 2), 99, np.int64)
    KCb = np.full((NC, nW, 2, 2), 99, np.int64); KIb = np.full((NC, nW, 2), 99, np.int64)
    KC = np.empty((NC, nW, 2, 2), np.int64); KI = np.empty((NC, nW, 2), np.int64)
    wkb = 99
    wmask[:] = False
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
    wit = np.empty(n, np.bool_); wk = np.empty(1, np.int64)
    nseed = 0; nplane = 0; neval = 0
    if bad:
        return kb, KCb, KIb, nseed, nplane, neval, bad, wkb
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
            nl2p = 0
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
            n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
            aref[0] = ax; aref[1] = ay; aref[2] = az; n2ref[0] = n2x; n2ref[1] = n2y; n2ref[2] = n2z
            for q in range(nfin):
                p = sel[q]
                pv_[q] = P[0, p] * ax + P[1, p] * ay + P[2, p] * az
                wv[q] = P[0, p] * n2x + P[1, p] * n2y + P[2, p] * n2z
                lcv[q] = LC[p]; sdv[q] = SD[p]
            _pb(pv_, wv, lcv, sdv, nfin, WLa, wc, aref, n2ref, phimet, road, eta_max, kS, kF)
            nplane += 1
            for wi in range(nW):
                for si in range(2):
                    if kS[wi, si] < kb[wi, si, 0]:
                        kb[wi, si, 0] = kS[wi, si]
                    if kF[wi, si] < kb[wi, si, 1]:
                        kb[wi, si, 1] = kF[wi, si]
            neval += plane_cats(pv_, wv, lcv, sdv, nfin, WLa, wc, aref, n2ref, phimet, road, eta_max, KC, KI, tw, wit, wk,
                                noff)
            for c in range(NC):
                for wi in range(nW):
                    for rd in range(2):
                        if KC[c, wi, 0, rd] < KCb[c, wi, 0, rd]:
                            KCb[c, wi, 0, rd] = KC[c, wi, 0, rd]
                        if KC[c, wi, 1, rd] < KCb[c, wi, 1, rd]:
                            KCb[c, wi, 1, rd] = KC[c, wi, 1, rd]; KIb[c, wi, rd] = KI[c, wi, rd]
                        elif KC[c, wi, 1, rd] == KCb[c, wi, 1, rd] and KI[c, wi, rd] < KIb[c, wi, rd]:
                            KIb[c, wi, rd] = KI[c, wi, rd]
            if wk[0] < wkb:
                wkb = wk[0]
                wmask[:] = False
                for q in range(nfin):
                    if wit[q]:
                        wmask[sel[q]] = True
    return kb, KCb, KIb, nseed, nplane, neval, bad, wkb


def classify_pool(Hm, pv, phim, cfg, wcfg, FF, K, tw=TW_DEFAULT):
    """Pool rows (13 columns), PV, road axis -> dict(kb, KC, KI, n_road, n_seeds, n_planes, n_eval, bad, wk, wit_rows)."""
    sidm = Hm[:, 0].astype(np.int64)
    m, U0 = FF.road_select(Hm, sidm, pv, phim, cfg)
    nr = int(m.sum())
    nW = len(WL)
    if nr < 8:
        return dict(kb=np.full((nW, 2, 2), 99, np.int64), KC=np.full((NC, nW, 2, 2), 99, np.int64),
                    KI=np.full((NC, nW, 2), 99, np.int64), n_road=nr, n_seeds=0, n_planes=0, n_eval=0, bad=0, wk=99,
                    wit_rows=Hm[:0])
    U = np.ascontiguousarray(U0[m]); X = Hm[m, 1]; Y = Hm[m, 2]
    rH = np.hypot(X, Y)
    sd = sidm[m]
    wmask = np.zeros(nr, np.bool_)
    kb, KC, KI, ns, npl, nev, bad, wk = road_multi(
        U, np.ascontiguousarray(X / rH), np.ascontiguousarray(Y / rH), np.ascontiguousarray(Hm[m, 4]),
        np.ascontiguousarray(Hm[m, 5]), FF.LC_OF[sd], FF.SIDE_OF[sd], FF.JLOC_OF[sd], float(phim), float(wcfg.delta95),
        float(wcfg.eta_max), float(cfg.w_c), float(cfg.t_tol), int(cfg.iters), WL, K.refit_packed, int(tw), int(B.NOFF),
        wmask)
    return dict(kb=kb, KC=KC, KI=KI, n_road=nr, n_seeds=ns, n_planes=npl, n_eval=nev, bad=bad, wk=int(wk),
                wit_rows=Hm[m][wmask])


def witness_summary(Hw, FF):
    """Hit-truth summary of a witness (rows of the pool): hits, particles, product hits (vsec >= 1), Fatras-made
    (gen >= 1), CKF-flagged, N_IP2, N_2S2 (same layer rule as the classifier)."""
    if not len(Hw):
        return [0, 0, 0, 0, 0, 0, 0]
    sid = Hw[:, 0].astype(np.int64)
    lc = FF.LC_OF[sid]; sd = FF.SIDE_OF[sid]
    c = np.zeros((10, 3), np.int64)
    np.add.at(c, (lc, sd), 1)
    cr = [c[l, 0] if l < 4 else min(c[l, 1], c[l, 2]) for l in range(10)]
    return [len(Hw), len(np.unique(Hw[:, [7, 8, 10]], axis=0)), int((Hw[:, 10] >= 1).sum()), int((Hw[:, 9] >= 1).sum()),
            int(((Hw[:, 6].astype(np.int64) & 1) == 1).sum()), int(sum(x >= 2 for x in cr[:7])),
            int(sum(x >= 2 for x in cr[7:]))]


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p3a_subset %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--files', default='')
    ap.add_argument('--manifest', default='')
    ap.add_argument('--max-events', type=int, default=0)
    ap.add_argument('--no-merge', action='store_true', help='pool without chain_inputs.merge_pool')
    ap.add_argument('--pv', default='draw', choices=['draw', 'draw2', 'true'], help='Z(nunu) only')
    ap.add_argument('--w-select', default='pos', choices=['pos', 'zero', 'all'],
                    help='Z(nunu): events with w_v1 > 0 (as Phase 2), with w_v1 = 0 only, or all')
    a = ap.parse_args()
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    p2w_sha = hashlib.sha256(Path(B.__file__).read_bytes()).hexdigest()
    if not p2w_sha.startswith(P2W_SHA256_PREFIX):
        raise SystemExit(f'p2w_subset.py sha256 {p2w_sha} is not the reviewed {P2W_SHA256_PREFIX}...')
    RS, CI, FF, K, GT, cfg, wcfg = B.load_frozen()
    PV_SIGMA = np.array([0.010, 0.010, 0.015])
    if not np.allclose(GT.PV_SIGMA, PV_SIGMA):
        raise SystemExit('PV_SIGMA differs from v1 g1b_tt.PV_SIGMA')
    paths = json.loads(Path(a.manifest).read_text())[a.id] if a.manifest else a.files.split(',')
    irows = []; frows = []; files = []; errors = []; dumps = []
    tot = dict(n_pref=0, n_seeds=0, n_planes=0, n_eval=0, max_road=0, t_kernel=0.0)
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
            vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]].astype(np.float64)
            use = {'pos': w > 0, 'zero': w == 0, 'all': np.ones(nev, np.bool_)}[a.w_select].copy()
            pvs = np.zeros((nev, 3))
            tag = {'draw': 'p2t-pv', 'draw2': 'p3a-pv2'}.get(a.pv)
            for i in np.where(use)[0]:
                if a.pv == 'true':
                    pvs[i] = vtx[i]
                else:                              # 'draw' = p2t_classify.py's PV draw, same seed string
                    h = hashlib.blake2b(f'{tag}|{stream}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
                    pvs[i] = vtx[i] + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
        else:
            w = np.ones(nev); cls = evt[:, ec.index('cls')].astype(np.int64); nep = z['n_early_prod'].astype(np.int64)
            axis0 = evt[:, ec.index('phi_road')].astype(np.float64)
            norient = 1 if stream == 'pilot.c0.hs' else int(meta['road_orientations']['n'])
            pvs = evt[:, [ec.index('pv_x'), ec.index('pv_y'), ec.index('pv_z')]].astype(np.float64)
            use = np.ones(nev, np.bool_)
        nmax = nev if not a.max_events else min(nev, a.max_events)
        use[nmax:] = False
        sid_all = hits[:, 0].astype(np.int64)
        lc_all = FF.LC_OF[sid_all]
        pf = B.prefilter(hits[:, 1].astype(np.float64), hits[:, 2].astype(np.float64), hits[:, 3].astype(np.float64),
                         lc_all, FF.SIDE_OF[sid_all], off, pvs, axis0, use, norient, float(cfg.road), float(cfg.w_c))
        fm = dict(path=path, stream=stream, chunk=meta['chunk'], n_events=nev, n_classified_range=nmax, n_orient=norient,
                  n_used=int(use.sum()), n_w_positive=int((w[:nmax] > 0).sum()),
                  n_early_events=int((nep[:nmax] > 0).sum()), n_prefilter_pass=int(pf.sum()),
                  content_sha256=meta.get('content_sha256'), mu=meta.get('mu'), mode=meta.get('mode'),
                  trunc_mode=meta.get('trunc_mode'), n_per_ev_mode=meta.get('n_per_ev_mode'),
                  beta_min=meta.get('beta_min'), handover=meta.get('handover'), sum_w_v1=meta.get('sum_w_v1'))
        if is_z:
            fm['w_max'] = float(w[:nmax].max())
            fm['sum_w_full'] = float(w[:nmax][w[:nmax] >= 0.5].sum()); fm['n_full'] = int((w[:nmax] >= 0.5).sum())
            fm['sum_w_low'] = float(w[:nmax][(w[:nmax] > 0) & (w[:nmax] < 0.5)].sum())
            fm['n_low'] = int(((w[:nmax] > 0) & (w[:nmax] < 0.5)).sum()); fm['n_zero'] = int((w[:nmax] == 0).sum())
        else:
            fm['cls_counts'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax], return_counts=True))}
            fm['cls_counts_flagged'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax][nep[:nmax] > 0],
                                                                                 return_counts=True))}
        files.append(fm)
        for i in np.where(pf.any(1))[0]:
            s = slice(int(off[i]), int(off[i + 1]))
            b = lc_all[s] >= 0
            H0 = hits[s][b].astype(np.float64)
            Hm = H0 if a.no_merge else CI.merge_pool(H0, tru[s][b].astype(np.float64))[0]
            for k in np.where(pf[i])[0]:
                phim = float((axis0[i] + 2 * np.pi * k / norient + np.pi) % (2 * np.pi) - np.pi)
                t0 = time.perf_counter()
                r = classify_pool(Hm, pvs[i], phim, cfg, wcfg, FF, K)
                tot['t_kernel'] += time.perf_counter() - t0
                tot['n_pref'] += 1; tot['n_seeds'] += r['n_seeds']; tot['n_planes'] += r['n_planes']
                tot['n_eval'] += r['n_eval']; tot['max_road'] = max(tot['max_road'], r['n_road'])
                if r['bad']:
                    errors.append(dict(file=fi, event=int(i), orient=int(k), error=f"{r['bad']} hits with non-constant sigma"))
                    continue
                kb, KC, KI = r['kb'], r['KC'], r['KI']
                if ((kb[:, 0, :] <= KMAX[0]).any() or (kb[:, 1, :] <= KMAX[1]).any()
                        or (KC[:, :, 0, :] <= KMAX[0]).any() or (KC[:, :, 1, :] <= KMAX[1]).any()):
                    ws_ = witness_summary(r['wit_rows'], FF)
                    irows.append([fi, i, k, cls[i], nep[i], r['n_road'], r['n_planes'], *kb.reshape(-1), *KC.reshape(-1),
                                  *KI.reshape(-1), r['wk'], *ws_])
                    frows.append([w[i], r['n_seeds']])
                    if not is_z:                       # full witness tables, per width, for the attribution by truth
                        d = dict(file=fi, path=path, event=int(i), orient=int(k), cls=int(cls[i]),
                                 n_early_prod=int(nep[i]), kb=kb.tolist(), witnesses={})
                        for tw in range(len(WL)):
                            rr = classify_pool(Hm, pvs[i], phim, cfg, wcfg, FF, K, tw=tw)
                            d['witnesses'][WNAMES[tw]] = dict(k=rr['wk'], hits=np.round(rr['wit_rows'], 4).tolist())
                        d['pool_columns'] = meta['columns']
                        d['evt'] = dict(zip(ec, [float(x) for x in evt[i]]))
                        dumps.append(d)
        z.close()
        log.info('%s: %d events used, %d prefilter passes, %d rows so far, %.1f s', Path(path).name, fm['n_used'],
                 fm['n_prefilter_pass'], len(irows), time.perf_counter() - t_w0)
    summ = dict(id=a.id, files=files, i_cols=I_COLS, f_cols=F_COLS, widths=WL.tolist(), wnames=WNAMES, cats=CATS,
                kmax=KMAX, n_errors=len(errors), errors=errors[:200], totals=tot, dumps=dumps,
                options=dict(no_merge=bool(a.no_merge), pv=a.pv, w_select=a.w_select, max_events=a.max_events,
                             noff=int(B.NOFF), witness_target=WNAMES[TW_DEFAULT]),
                config=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol, iters=cfg.iters, delta95=wcfg.delta95,
                            eta_max=wcfg.eta_max),
                frozen_inputs_sha256=RS.sha256_file(RS.HERE / 'frozen_inputs.json'), p2w_subset_sha256=p2w_sha,
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                wall_s=time.perf_counter() - t_w0, cpu_s=time.process_time() - t_c0)
    out = Path(a.out)
    part = out.with_name(out.name + '.part')
    with open(part, 'wb') as f:
        np.savez_compressed(f, meta=json.dumps(summ),
                            rows_i=np.array(irows, np.int32).reshape(-1, len(I_COLS)),
                            rows_f=np.array(frows, np.float64).reshape(-1, len(F_COLS)))
        f.flush(); os.fsync(f.fileno())
    part.replace(out)
    log.info('done: %d rows, %d errors, cpu %.1f s, totals %s', len(irows), len(errors), summ['cpu_s'], tot)
    return 0


if __name__ == '__main__':
    sys.exit(main())
