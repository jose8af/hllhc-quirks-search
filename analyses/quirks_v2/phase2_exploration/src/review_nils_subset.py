"""review_nils_subset.py -- independent re-check of the subset-pass count of p2w_subset.py (advisor ruling (ii)).
Nils (Fable 5.2, second-agent reviewer), 2026-11-23.

  <tt python> -B review_nils_subset.py --part I --nparts N --full-mod K --out /ABS/OUT.json

Does NOT import p2w_subset.  Own code: road selection, exhaustive IP-pair seeding, PV-constrained plane fit (written
from the finder README / STR definition), subset search inside a plane, and a separate pure-numpy VERIFIER of every
witness.  Reused, unchanged, from the frozen v1 chain (inputs, not classifier): finder.LC_OF / SIDE_OF tables and
chain_inputs.merge_pool; the PV draw convention of p2t_classify.py (blake2b seed string).

Only R08 (W = 4.7 mm), s = 0 (n = 7, k = 7 - N_IP2, k_max = 3).  Per event the smallest VERIFIED k for
  S  any subset with w_core < W                       (plan reading S)
  F  the same with N_IT2 >= 3                         (plan reading F)
  H  hard window: every IP hit of the subset inside one window of full width 2 W / 1.4826 (strictest reading;
     such a subset satisfies S3 as well), N_IT2 not required
A witness = (set of road hits, unit normal n through the PV).  The verifier recomputes everything from the road
arrays: axis = in-plane mean hit direction of the subset; every hit within 3 sigma_tot of the plane, forward,
|u.n2| < W_c; axis in road and barrel; >= 3 IP hits; w_core = 1.4826 MAD(u.n2 over IP hits) < W; N_IP2 from layer
counts (IT layer: >= 2 hits; PS layer: >= 2 hits on each sensor).
Modes per file: 'rows' = only the events that have a row in the p2-c-r1v-s[23] outputs; 'full' = every w > 0 event.
Z(nu nu) pilot files only.  No signal file is read; no efficiency is formed.
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit

QV2 = Path(__file__).resolve().parents[2]
V = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c/rule1_valid'
CFG = dict(road=0.15, w_c=75.0, t_tol=0.03, iters=3, delta95=0.15, eta_max=1.0)   # checked against every output meta
W8 = 4.7
PV_SIGMA = np.array([0.010, 0.010, 0.015])


@njit(cache=True)
def _mad(buf, k):
    c = np.median(buf[:k])
    for i in range(k):
        buf[i] = abs(buf[i] - c)
    return 1.4826 * np.median(buf[:k])


@njit(cache=True)
def _nip(lc, sd, T, k, cnt):
    cnt[:, :] = 0
    for t in range(k):
        if T[t] and lc[t] <= 6:
            cnt[lc[t], sd[t]] += 1
    nip2 = 0; nit2 = 0
    for l in range(7):
        cr = cnt[l, 0] if l < 4 else min(cnt[l, 1], cnt[l, 2])
        if cr >= 2:
            nip2 += 1
            if l < 4:
                nit2 += 1
    return nip2, nit2


@njit(cache=True)
def _eval(p, q, un, lc, sd, k, T, W, wc, aref, n2ref, phimet, d95, etamax, buf, cnt):
    """Subset T of plane hits (p = u.a, q = u.n2 of the plane's axis a).  Own axis = mean hit direction of T in the
    plane; 2S hits failing forward / window are dropped (and the axis recomputed), an IP hit failing rejects.
    -> (ok, N_IP2, N_IT2, hard, c, s)"""
    c = 1.0; s = 0.0
    stable = False
    for it in range(6):
        sx = 0.0; sy = 0.0
        for t in range(k):
            if T[t]:
                sx += p[t] / un[t]; sy += q[t] / un[t]
        nn = np.sqrt(sx * sx + sy * sy)
        if not nn > 0:
            return False, 0, 0, False, c, s
        c = sx / nn; s = sy / nn
        ch = False
        for t in range(k):
            if T[t]:
                if not (p[t] * c + q[t] * s > 0 and abs(q[t] * c - p[t] * s) < wc):
                    if lc[t] <= 6:
                        return False, 0, 0, False, c, s
                    T[t] = False; ch = True
        if not ch:
            stable = True
            break
    if not stable:
        return False, 0, 0, False, c, s
    ax = c * aref[0] + s * n2ref[0]; ay = c * aref[1] + s * n2ref[1]; az = c * aref[2] + s * n2ref[2]
    dph = abs((np.arctan2(ay, ax) - phimet + np.pi) % (2 * np.pi) - np.pi)
    eta = np.arcsinh(az / max(np.sqrt(ax * ax + ay * ay), 1e-12))
    if not (dph < d95 and abs(eta) < etamax):
        return False, 0, 0, False, c, s
    kk = 0; lo = 1e300; hi = -1e300
    for t in range(k):
        if T[t] and lc[t] <= 6:
            w = q[t] * c - p[t] * s
            buf[kk] = w; kk += 1
            lo = min(lo, w); hi = max(hi, w)
    if kk < 3:
        return False, 0, 0, False, c, s
    if not _mad(buf, kk) < W:
        return False, 0, 0, False, c, s
    nip2, nit2 = _nip(lc, sd, T, k, cnt)
    return True, nip2, nit2, (hi - lo) < 2.0 * W / 1.4826, c, s


@njit(cache=True)
def _fill(w, el, lc, sd, k, W, lo, hi, itfirst, T, buf, cnt):
    """Core = eligible IP hits with lo <= w < hi; then layers completed with outside hits (fewest needed first, IT
    first if itfirst), an addition kept only if the MAD width stays < W.  2S hits are all in T."""
    cc = 0.5 * (lo + hi)
    for t in range(k):
        T[t] = (lc[t] > 6) or (el[t] and w[t] >= lo and w[t] < hi)
    done = np.zeros(7, np.bool_)
    add = np.empty(4, np.int64)
    out = np.zeros((7, 3), np.int64)
    for step in range(7):
        _nip(lc, sd, T, k, cnt)
        out[:, :] = 0
        for t in range(k):
            if lc[t] <= 6 and el[t] and not T[t]:
                out[lc[t], sd[t]] += 1
        best = -1; bkey = 1000000
        for l in range(7):
            if done[l]:
                continue
            if l < 4:
                need = max(0, 2 - cnt[l, 0]); av = out[l, 0] >= need
            else:
                n1 = max(0, 2 - cnt[l, 1]); n2 = max(0, 2 - cnt[l, 2])
                need = n1 + n2; av = out[l, 1] >= n1 and out[l, 2] >= n2
            if need == 0 or not av:
                done[l] = True
                continue
            key = need * 10 + l + (1000 if (itfirst and l >= 4) else 0)
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
            for r in range(need):
                bi = -1; bd = 1e300
                for t in range(k):
                    if lc[t] == best and sd[t] == side and el[t] and not T[t] and abs(w[t] - cc) < bd:
                        bd = abs(w[t] - cc); bi = t
                if bi >= 0:
                    T[bi] = True; add[na] = bi; na += 1
        kk = 0
        for t in range(k):
            if T[t] and lc[t] <= 6:
                buf[kk] = w[t]; kk += 1
        if kk < 3 or not _mad(buf, kk) < W:
            for r in range(na):
                T[add[r]] = False


@njit(cache=True)
def search_event(U, CX, CY, S0, S1, LC, SD, phimet, W, wc, ttol, iters, d95, etamax):
    """-> bk (3,) best k [S, F, H] (99 = none), wm (3, N) witness masks, wn (3, 3) normals, stats (n_seed, n_fit,
    n_plane, n_eval)."""
    N = U.shape[0]
    bk = np.full(3, 99, np.int64)
    wm = np.zeros((3, N), np.bool_)
    wn = np.zeros((3, 3))
    st = np.zeros(4, np.int64)
    UN = np.empty(N)
    for i in range(N):
        UN[i] = np.sqrt(U[i, 0] ** 2 + U[i, 1] ** 2 + U[i, 2] ** 2)
    sel = np.empty(N, np.int64)
    p = np.empty(N); q = np.empty(N); un = np.empty(N); w = np.empty(N)
    lc = np.empty(N, np.int64); sd = np.empty(N, np.int64); el = np.empty(N, np.bool_)
    T = np.empty(N, np.bool_); T2 = np.empty(N, np.bool_)
    buf = np.empty(N); cnt = np.zeros((7, 3), np.int64); c7 = np.zeros((7, 3), np.int64)
    M = np.zeros((3, 3)); aref = np.empty(3); n2ref = np.empty(3)
    ws = np.empty(N); h = W / 1.4826
    for ia in range(N):
        if LC[ia] > 6:
            continue
        for ib in range(N):
            if LC[ib] >= LC[ia]:
                continue
            nx = U[ia, 1] * U[ib, 2] - U[ia, 2] * U[ib, 1]
            ny = U[ia, 2] * U[ib, 0] - U[ia, 0] * U[ib, 2]
            nz = U[ia, 0] * U[ib, 1] - U[ia, 1] * U[ib, 0]
            nc = np.sqrt(nx * nx + ny * ny + nz * nz)
            if not nc >= 1e-3 * UN[ia] * UN[ib]:
                continue
            nx /= nc; ny /= nc; nz /= nc
            st[0] += 1
            # quick necessary condition for N_IP2 >= 4 on this seed: >= 4 double IP layers within 5 mm of the plane
            c7[:, :] = 0
            for i in range(N):
                if LC[i] <= 6 and abs(U[i, 0] * nx + U[i, 1] * ny + U[i, 2] * nz) < 5.0:
                    c7[LC[i], SD[i]] += 1
            nd = 0
            for l in range(7):
                if (c7[l, 0] if l < 4 else min(c7[l, 1], c7[l, 2])) >= 2:
                    nd += 1
            if nd < 4:
                continue
            ax = U[ia, 0] / UN[ia] + U[ib, 0] / UN[ib]; ay = U[ia, 1] / UN[ia] + U[ib, 1] / UN[ib]
            az = U[ia, 2] / UN[ia] + U[ib, 2] / UN[ib]
            an = np.sqrt(ax * ax + ay * ay + az * az)
            if not an > 1e-9:
                continue
            ax /= an; ay /= an; az /= an
            st[1] += 1
            ns = 0; good = True
            for it in range(iters + 1):
                n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
                M[:, :] = 0.0
                sx = 0.0; sy = 0.0; sz = 0.0
                ns = 0
                for i in range(N):
                    ux = U[i, 0]; uy = U[i, 1]; uz = U[i, 2]
                    d = ux * nx + uy * ny + uz * nz
                    a = -nx * CY[i] + ny * CX[i]
                    sc2 = a * a * S0[i] * S0[i] + nz * nz * S1[i] * S1[i]
                    sg2 = max(sc2, 1e-8) + ttol * ttol
                    if d * d < 9.0 * sg2 and ux * ax + uy * ay + uz * az > 0 and abs(ux * n2x + uy * n2y + uz * n2z) < wc:
                        sel[ns] = i; ns += 1
                        wt = 1.0 / sg2
                        M[0, 0] += wt * ux * ux; M[0, 1] += wt * ux * uy; M[0, 2] += wt * ux * uz
                        M[1, 1] += wt * uy * uy; M[1, 2] += wt * uy * uz; M[2, 2] += wt * uz * uz
                        sx += ux / UN[i]; sy += uy / UN[i]; sz += uz / UN[i]
                if ns < 4:
                    good = False
                    break
                if it == iters:
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
            if not good:
                continue
            dph = abs((np.arctan2(ay, ax) - phimet + np.pi) % (2 * np.pi) - np.pi)
            eta = np.arcsinh(az / max(np.sqrt(ax * ax + ay * ay), 1e-12))
            if not (dph < d95 and abs(eta) < etamax):
                continue
            n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
            aref[0] = ax; aref[1] = ay; aref[2] = az; n2ref[0] = n2x; n2ref[1] = n2y; n2ref[2] = n2z
            k = ns
            for t in range(k):
                i = sel[t]
                p[t] = U[i, 0] * ax + U[i, 1] * ay + U[i, 2] * az
                q[t] = U[i, 0] * n2x + U[i, 1] * n2y + U[i, 2] * n2z
                un[t] = UN[i]; lc[t] = LC[i]; sd[t] = SD[i]; T[t] = True
            nipf, nitf = _nip(lc, sd, T, k, cnt)
            if nipf < 4:
                continue
            st[2] += 1
            lob = 7 - nipf
            if bk[0] <= lob and bk[2] <= lob and (bk[1] <= lob or nitf < 3):
                continue                          # this plane cannot improve any of the three
            # candidate in-plane axes: the plane's own, then along each IP hit
            for a_ in range(-1, k):
                if a_ >= 0 and lc[a_] > 6:
                    continue
                if a_ < 0:
                    ca = 1.0; sa = 0.0
                else:
                    r = np.sqrt(p[a_] ** 2 + q[a_] ** 2)
                    ca = p[a_] / r; sa = q[a_] / r
                m = 0
                for t in range(k):
                    w[t] = q[t] * ca - p[t] * sa
                    el[t] = lc[t] <= 6 and (p[t] * ca + q[t] * sa > 0) and abs(w[t]) < wc
                    if el[t]:
                        ws[m] = w[t]; m += 1
                if m < 3:
                    continue
                wsort = np.sort(ws[:m])
                # variants: 0 = all eligible hits (the full set), then windows [w_j, w_j + 2h) and [w_j - 2h, w_j]
                for v in range(-1, 2 * m):
                    if v < 0:
                        lo = -1e300; hi = 1e300
                    elif v < m:
                        lo = wsort[v]; hi = lo + 2 * h
                    else:
                        hi = wsort[v - m] + 1e-9; lo = hi - 2 * h
                    for mode in range(3):         # 0 core only, 1 fill (fewest first), 2 fill (IT first)
                        if v < 0 and mode > 0:
                            break
                        if mode == 0:
                            for t in range(k):
                                T[t] = (lc[t] > 6) or (el[t] and w[t] >= lo and w[t] < hi)
                        else:
                            _fill(w, el, lc, sd, k, W, lo, hi, mode == 2, T, buf, cnt)
                        st[3] += 1
                        ok, nip2, nit2, hard, c_, s_ = _eval(p, q, un, lc, sd, k, T, W, wc, aref, n2ref, phimet, d95,
                                                             etamax, buf, cnt)
                        if not ok:
                            continue
                        kk = 7 - nip2
                        for cat in range(3):
                            if cat == 1 and nit2 < 3:
                                continue
                            if cat == 2 and not hard:
                                continue
                            if kk < bk[cat]:
                                bk[cat] = kk
                                wm[cat, :] = False
                                for t in range(k):
                                    if T[t]:
                                        wm[cat, sel[t]] = True
                                wn[cat, 0] = nx; wn[cat, 1] = ny; wn[cat, 2] = nz
                if bk[0] <= lob and bk[2] <= lob and (bk[1] <= lob or nitf < 3):
                    break
    return bk, wm, wn, st


def verify(U, CX, CY, S0, S1, LC, SD, mask, n, phimet, W=W8, c=CFG):
    """Independent pure-numpy check of one witness.  -> dict(ok, k, nip2, nit2, w_core, hard, n_ip, why)."""
    idx = np.where(mask)[0]
    out = dict(ok=False, k=99, nip2=0, nit2=0, w_core=float('nan'), hard=False, n_ip=0, why='')
    if len(idx) < 4 or abs(np.linalg.norm(n) - 1) > 1e-9:
        out['why'] = 'size/normal'; return out
    u = U[idx]
    s = (u / np.linalg.norm(u, axis=1)[:, None]).sum(0)
    s = s - (s @ n) * n
    if not np.linalg.norm(s) > 0:
        out['why'] = 'axis'; return out
    a = s / np.linalg.norm(s)
    n2 = np.cross(n, a)
    d = u @ n
    aa = -n[0] * CY[idx] + n[1] * CX[idx]
    sg2 = np.maximum(aa ** 2 * S0[idx] ** 2 + n[2] ** 2 * S1[idx] ** 2, 1e-8) + c['t_tol'] ** 2
    if not np.all(d ** 2 < 9.0 * sg2):
        out['why'] = '3sigma'; return out
    wv = u @ n2
    if not (np.all(u @ a > 0) and np.all(np.abs(wv) < c['w_c'])):
        out['why'] = 'forward/window'; return out
    dph = abs((np.arctan2(a[1], a[0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    eta = np.arcsinh(a[2] / max(np.hypot(a[0], a[1]), 1e-12))
    if not (dph < c['delta95'] and abs(eta) < c['eta_max']):
        out['why'] = 'alignment'; return out
    ip = LC[idx] <= 6
    out['n_ip'] = int(ip.sum())
    if ip.sum() < 3:
        out['why'] = 'n_ip'; return out
    wi = wv[ip]
    wcore = 1.4826 * np.median(np.abs(wi - np.median(wi)))
    out['w_core'] = float(wcore)
    if not wcore < W:
        out['why'] = 'w_core'; return out
    nip2 = 0; nit2 = 0
    for l in range(7):
        if l < 4:
            cr = int(((LC[idx] == l)).sum())
        else:
            cr = min(int(((LC[idx] == l) & (SD[idx] == 1)).sum()), int(((LC[idx] == l) & (SD[idx] == 2)).sum()))
        if cr >= 2:
            nip2 += 1; nit2 += l < 4
    out.update(ok=True, k=7 - nip2, nip2=nip2, nit2=int(nit2), hard=bool(wi.max() - wi.min() < 2 * W / 1.4826))
    return out


def road_arrays(Hm, pv, phim, FF, c=CFG):
    sid = Hm[:, 0].astype(np.int64)
    U0 = Hm[:, 1:4] - pv[None, :]
    r0 = np.hypot(U0[:, 0], U0[:, 1])
    dph = np.abs((np.arctan2(U0[:, 1], U0[:, 0]) - phim + np.pi) % (2 * np.pi) - np.pi)
    m = (FF.LC_OF[sid] >= 0) & (dph < c['road'] + np.arcsin(np.minimum(1.0, c['w_c'] / r0)))
    X = Hm[m, 1]; Y = Hm[m, 2]; rH = np.hypot(X, Y)
    return (np.ascontiguousarray(U0[m]), np.ascontiguousarray(X / rH), np.ascontiguousarray(Y / rH),
            np.ascontiguousarray(Hm[m, 4]), np.ascontiguousarray(Hm[m, 5]), FF.LC_OF[sid[m]], FF.SIDE_OF[sid[m]])


def classify(Hm, pv, phim, FF):
    """-> (k [S, F, H] verified, info) for one event."""
    U, CX, CY, S0, S1, LC, SD = road_arrays(Hm, pv, phim, FF)
    res = dict(n_road=len(U), k=[99, 99, 99], raw=[99, 99, 99], bad=[])
    if len(U) < 8:
        return res
    cr = np.zeros((7, 3), np.int64)
    np.add.at(cr, (LC[LC <= 6], SD[LC <= 6]), 1)
    if sum((cr[l, 0] if l < 4 else min(cr[l, 1], cr[l, 2])) >= 2 for l in range(7)) < 4:
        return res
    bk, wm, wn, st = search_event(U, CX, CY, S0, S1, LC, SD, float(phim), W8, CFG['w_c'], CFG['t_tol'], CFG['iters'],
                                  CFG['delta95'], CFG['eta_max'])
    res['raw'] = [int(x) for x in bk]; res['stats'] = [int(x) for x in st]
    for cat in range(3):
        if bk[cat] < 99:
            v = verify(U, CX, CY, S0, S1, LC, SD, wm[cat], wn[cat], phim)
            good = v['ok'] and v['k'] <= bk[cat] and (cat != 1 or v['nit2'] >= 3) and (cat != 2 or v['hard'])
            if good:
                res['k'][cat] = v['k']
                if cat == 0:
                    res['wit'] = [v['nip2'], v['nit2'], round(v['w_core'], 3), v['n_ip'], int(wm[cat].sum())]
            else:
                res['bad'].append([cat, int(bk[cat]), v['why'], v['k']])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', type=int, default=0)
    ap.add_argument('--nparts', type=int, default=1)
    ap.add_argument('--full-mod', type=int, default=0, help='files with global index %% K == 0 are classified in full')
    ap.add_argument('--max-files', type=int, default=0)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    t_c0 = time.process_time(); t_w0 = time.perf_counter()
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    sys.path.insert(0, str(QV2)); os.chdir(QV2)
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import finder as FF
    # her rows of the Z files: path -> {event: (w, kS_R08_s0, kF_R08_s0)}
    theirs = {}
    for f in sorted(glob.glob(f'{V}/p2-c-r1v-s[23][ab]/000/r1v-s2-znn-*.npz')):
        z = np.load(f); m = json.loads(str(z['meta'])); r = z['rows']; ix = {k: i for i, k in enumerate(m['row_cols'])}
        if any(abs(m['config'][k] - CFG[k]) > 1e-12 for k in CFG):
            raise SystemExit(f'{f}: config differs from CFG')
        for fi, fm in enumerate(m['files']):
            assert fm['stream'] == 'pilot.hs0.znn' and fm['path'] not in theirs
            theirs[fm['path']] = {int(x[ix['event']]): (float(x[ix['w']]), int(x[ix['k_R08_s0_S']]), int(x[ix['k_R08_s0_F']]))
                                  for x in r[r[:, 0] == fi]}
    paths = sorted(theirs)
    if len(paths) != 460:
        raise SystemExit(f'{len(paths)} Z files, expected 460')
    out = dict(part=a.part, nparts=a.nparts, full_mod=a.full_mod, files=[], events=[], bad=[], cfg=CFG)
    todo = [(gi, p) for gi, p in enumerate(paths) if gi % a.nparts == a.part]
    if a.max_files:
        todo = todo[:a.max_files]
    for gi, path in todo:
        full = bool(a.full_mod) and gi % a.full_mod == 0
        z = np.load(path); meta = json.loads(str(z['meta'])); ec = meta['evt_cols']
        assert meta['stream'] == 'pilot.hs0.znn'
        hits = z['hits']; off = z['hit_off'].astype(np.int64); evt = z['evt']; tru = z['tru']
        w = evt[:, ec.index('w_v1')]; ph = evt[:, ec.index('phimet_reco_v1')]
        vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
        evs = [i for i in range(len(w)) if w[i] > 0] if full else sorted(theirs[path])
        nk = 0; tk = 0.0
        for i in evs:
            assert w[i] > 0
            hsh = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
            pv = vtx[i] + np.random.default_rng(int.from_bytes(hsh, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
            s = slice(int(off[i]), int(off[i + 1]))
            hh = hits[s].astype(np.float64); tt = tru[s].astype(np.float64)
            b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
            if b.sum() < 8:
                continue
            Hm = CI.merge_pool(hh[b], tt[b])[0]
            phim = float((ph[i] + np.pi) % (2 * np.pi) - np.pi)
            t0 = time.perf_counter()
            r = classify(Hm, pv, phim, FF)
            tk += time.perf_counter() - t0; nk += 1
            th = theirs[path].get(i)
            if r['bad']:
                out['bad'].append([gi, i, r['bad']])
            if th is not None or min(r['k']) <= 3:
                out['events'].append([gi, i, float(w[i]), th[1] if th else -1, th[2] if th else -1, *r['k'],
                                      r['n_road'], *(r.get('wit') or [0, 0, 0, 0, 0])])
        out['files'].append(dict(gi=gi, path=path, full=full, n_checked=nk, n_rows=len(theirs[path]), t_kernel=round(tk, 2)))
        z.close()
        print(f'{gi} {Path(path).name} full={full} checked={nk} t_kernel={tk:.1f} cpu={time.process_time() - t_c0:.0f}',
              file=sys.stderr, flush=True)
    out['cpu_s'] = time.process_time() - t_c0; out['wall_s'] = time.perf_counter() - t_w0
    out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    p = Path(a.out); part = p.with_name(p.name + '.part')
    part.write_text(json.dumps(out)); part.replace(p)
    print(f'done cpu {out["cpu_s"]:.0f} s, {len(out["events"])} event records, {len(out["bad"])} bad', file=sys.stderr)


if __name__ == '__main__':
    main()
