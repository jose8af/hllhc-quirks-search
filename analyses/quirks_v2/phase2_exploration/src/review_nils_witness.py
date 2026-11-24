"""review_nils_witness.py -- diagnostics of p2w_subset.py's OWN witnesses (Nils, reviewer, 2026-11-23).

p2w_subset.py stores only the smallest k, not the subset that gave it.  This script re-runs HER code on single
events with a recorder around her `_eval` (her compiled `_greedy`, `_eval`, `_wcore`, `K.refit_packed` are called
unchanged; `plane_best` runs as its `.py_func` so that the recorder is seen; the seed loop of `subset_road` is
transcribed with numpy, l.300-356) and hands every recorded witness to MY verifier (pure numpy, below).
It is a diagnostic of her code, so it imports p2w_subset; the independent re-derivation is review_nils_subset.py.

  <tt python> -B review_nils_witness.py events  IN.json OUT.json [CPU_S]   # IN: [[path, event, kS, kF], ...]
  <tt python> -B review_nils_witness.py t7      OUT.json             # the 200 T7 trials of test_p2w_subset.py
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2w_subset as W                                   # noqa: E402  (diagnosed code)
import review_nils_subset as R                           # noqa: E402  (my search, for T7)

REC = {}
_eval_orig = W._eval


def _eval_rec(p, q, lc, sd, k, T, wc, Wd, aref, n2ref, phimet, road, eta_max, buf, c10):
    out = _eval_orig(p, q, lc, sd, k, T, wc, Wd, aref, n2ref, phimet, road, eta_max, buf, c10)
    if out[0]:
        REC['calls'].append((float(Wd), T[:k].copy(), int(out[1]), int(out[2]), int(out[3])))
    return out



def verify(U, CX, CY, S0, S1, LC, SD, idx, n, phimet, Wd, axis=None, c=R.CFG):
    """My check of one witness (hit indices idx, normal n).  axis None: the subset's own in-plane mean direction;
    else the given axis (the finder's convention for a full set).  -> (ok, why, N_IP2, N_IT2, N_2S2, w_core)."""
    u = U[idx]
    if axis is None:
        s = (u / np.linalg.norm(u, axis=1)[:, None]).sum(0); s = s - (s @ n) * n
        a = s / np.linalg.norm(s)
    else:
        a = np.asarray(axis, float)
        if abs(a @ n) > 1e-9 or abs(np.linalg.norm(a) - 1) > 1e-9:
            return False, 'axis not in plane', 0, 0, 0, np.nan
    n2 = np.cross(n, a)
    aa = -n[0] * CY[idx] + n[1] * CX[idx]
    sg2 = np.maximum(aa ** 2 * S0[idx] ** 2 + n[2] ** 2 * S1[idx] ** 2, 1e-8) + c['t_tol'] ** 2
    if not np.all((u @ n) ** 2 < 9 * sg2):
        return False, '3sigma', 0, 0, 0, np.nan
    wv = u @ n2
    if not (np.all(u @ a > 0) and np.all(np.abs(wv) < c['w_c'])):
        return False, 'forward/window', 0, 0, 0, np.nan
    dph = abs((np.arctan2(a[1], a[0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    eta = np.arcsinh(a[2] / max(np.hypot(a[0], a[1]), 1e-12))
    if not (dph < c['delta95'] and abs(eta) < c['eta_max']):
        return False, 'alignment', 0, 0, 0, np.nan
    ip = LC[idx] <= 6
    if ip.sum() < 3:
        return False, 'n_ip', 0, 0, 0, np.nan
    wi = wv[ip]; wcore = 1.4826 * np.median(np.abs(wi - np.median(wi)))
    if not wcore < Wd:
        return False, 'w_core', 0, 0, 0, float(wcore)
    cr = []
    for l in range(10):
        m = LC[idx] == l
        cr.append(int(m.sum()) if l < 4 else min(int((m & (SD[idx] == 1)).sum()), int((m & (SD[idx] == 2)).sum())))
    dbl = [x >= 2 for x in cr]
    return True, '', sum(dbl[:7]), sum(dbl[:4]), sum(dbl[7:]), float(wcore)


def her_witnesses(Hm, pv, phim, cfg, wcfg, FF, K):
    """Her classification of one pool with every witness recorded and verified by me.
    -> dict(kb her (nW, 2, 2), n_planes, wit {(wi, si, rd): record}, n_unverified)."""
    sidm = Hm[:, 0].astype(np.int64)
    m, U0 = FF.road_select(Hm, sidm, pv, phim, cfg)
    nW = len(W.WL)
    kb = np.full((nW, 2, 2), 99, np.int64)
    res = dict(kb=kb, n_planes=0, wit={}, n_road=int(m.sum()))
    if m.sum() < 8:
        return res
    U = np.ascontiguousarray(U0[m]); X = Hm[m, 1]; Y = Hm[m, 2]; rH = np.hypot(X, Y)
    CX = np.ascontiguousarray(X / rH); CY = np.ascontiguousarray(Y / rH)
    S0 = np.ascontiguousarray(Hm[m, 4]); S1 = np.ascontiguousarray(Hm[m, 5])
    sd = sidm[m]; LC = FF.LC_OF[sd]; SD = FF.SIDE_OF[sd]; J = FF.JLOC_OF[sd]
    n = len(U)
    P = np.empty((6, n)); P[:3] = U.T; P[3] = CX; P[4] = CY; P[5] = np.linalg.norm(U, axis=1)
    SF = np.zeros((16, 8))
    for j in range(16):
        if (J == j).any():
            SF[j, 3] = S0[J == j][0]; SF[j, 4] = S1[J == j][0]
            assert np.all(S0[J == j] == SF[j, 3]) and np.all(S1[J == j] == SF[j, 4])
    pid = np.arange(n).astype(np.int64)
    ipi = np.where(LC <= 6)[0]
    IA, IB = np.meshgrid(ipi, ipi, indexing='ij')
    ok = LC[IB] < LC[IA]
    IA = IA[ok]; IB = IB[ok]                         # same order as her double loop (ia outer, ib inner)
    thr = np.where(LC >= 7, 60.0, 5.0)
    G = np.zeros((16, n)); G[J, np.arange(n)] = 1.0   # surface membership
    sel = np.empty(n, np.int64); M = np.zeros((3, 3)); cnt = np.zeros((10, 3), np.int64); sgu = np.empty(16)
    selp = np.empty(n, np.int64); selw = np.empty(n)
    kS = np.empty((nW, 2), np.int64); kF = np.empty((nW, 2), np.int64)
    for c0 in range(0, len(IA), 4000):
        ia = IA[c0:c0 + 4000]; ib = IB[c0:c0 + 4000]
        N0 = np.cross(U[ia], U[ib]); nc = np.linalg.norm(N0, axis=1)
        good = nc >= 1e-3 * P[5, ia] * P[5, ib]
        A0 = U[ia] / P[5, ia][:, None] + U[ib] / P[5, ib][:, None]; an = np.linalg.norm(A0, axis=1)
        good &= an > 1e-9
        N0 = N0 / np.maximum(nc, 1e-300)[:, None]
        inpl = (np.abs(U @ N0.T) < thr[:, None]).astype(np.float64)       # (n, seeds)
        cs = G @ inpl                                                     # (16, seeds) hits per surface
        cr = np.concatenate([cs[:4], np.minimum(cs[4::2], cs[5::2])])     # (10, seeds)
        good &= (cr >= 2).sum(0) >= 4
        for q in np.where(good)[0]:
            L = np.where(inpl[:, q] > 0)[0].astype(np.int64)
            n0 = N0[q].copy(); ax0 = A0[q] / an[q]
            (st, nx, ny, nz, nl2, nit2, chi, nsel, ax, ay, az, dmax, nfin,
             itr) = K.refit_packed(L, len(L), P, J, LC, SD, pid, n0, ax0, float(cfg.w_c), int(cfg.iters),
                                   float(cfg.t_tol), 2.5, SF, sel, M, cnt, sgu, selp, selw, 0, n0[0], n0[1], n0[2])
            if st != 0 or nl2 < 4:
                continue
            dph = abs((np.arctan2(ay, ax) - phim + np.pi) % (2 * np.pi) - np.pi)
            eta = np.arcsinh(az / max(np.sqrt(ax * ax + ay * ay), 1e-12))
            if not (dph < wcfg.delta95 and abs(eta) < wcfg.eta_max):
                continue
            nv = np.array([nx, ny, nz]); av = np.array([ax, ay, az]); n2v = np.cross(nv, av)
            hs = sel[:nfin].copy()
            pv_ = U[hs] @ av; wv = U[hs] @ n2v
            lcv = LC[hs].astype(np.int64); sdv = SD[hs].astype(np.int64)
            REC['calls'] = []
            W._eval = _eval_rec          # seen by plane_best.py_func only; restored below (the compiled kernels
            W.plane_best.py_func(pv_, wv, lcv, sdv, nfin, W.WL, float(cfg.w_c), av, n2v, float(phim),
                                 float(wcfg.delta95), float(wcfg.eta_max), kS, kF)
            W._eval = _eval_orig         # of TT.run must never be compiled against the recorder)
            res['n_planes'] += 1
            # full-set branch (her l.222-227): the witness is the whole plane, judged with the finder's axis
            ipm = lcv <= 6
            wfull = 1.4826 * np.median(np.abs(wv[ipm] - np.median(wv[ipm]))) if ipm.sum() > 2 else np.inf
            for wi in range(nW):
                for si in range(2):
                    for rd, kk in ((0, kS), (1, kF)):
                        if kk[wi, si] < kb[wi, si, rd]:
                            kb[wi, si, rd] = kk[wi, si]
                            Wd = float(W.WL[wi])
                            if wi == 0 or wfull < Wd:
                                v = verify(U, CX, CY, S0, S1, LC, SD, hs, nv, phim, Wd, axis=av)
                                v2 = verify(U, CX, CY, S0, S1, LC, SD, hs, nv, phim, Wd)
                                kind = 'full'
                            else:
                                v = None; kind = 'subset'
                                for (Wc, T, nip2, nit2, n2s2) in REC['calls']:
                                    if Wc == Wd and 7 - nip2 + max(0, 3 * si - n2s2) == kk[wi, si] and (rd == 0 or nit2 >= 3):
                                        v = verify(U, CX, CY, S0, S1, LC, SD, hs[T], nv, phim, Wd)
                                        if v[0]:
                                            break
                                v2 = v
                            if v is None:
                                rec = dict(kind=kind, her_k=int(kk[wi, si]), ok=False, why='no recorded call', my_k=99)
                            else:
                                myk = 7 - v[2] + max(0, 3 * si - v[4]) if v[0] and (rd == 0 or v[3] >= 3) else 99
                                rec = dict(kind=kind, her_k=int(kk[wi, si]), ok=bool(v[0] and myk <= kk[wi, si]), why=v[1],
                                           my_k=int(myk), w_core=v[5], own_axis_ok=bool(v2 is not None and v2[0]))
                            res['wit'][(wi, si, rd)] = rec
    res['arrays'] = (U, CX, CY, S0, S1, LC, SD)
    return res


def load_event(path, i, FF, CI, cache={}):
    if path not in cache:
        cache.clear()
        z = np.load(path); meta = json.loads(str(z['meta']))
        cache[path] = (meta, z['hits'], z['hit_off'].astype(np.int64), z['evt'], z['tru'])
    meta, hits, off, evt, tru = cache[path]
    ec = meta['evt_cols']
    vtx = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
    h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
    pv = vtx + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * R.PV_SIGMA
    phim = float((evt[i, ec.index('phimet_reco_v1')] + np.pi) % (2 * np.pi) - np.pi)
    s = slice(int(off[i]), int(off[i + 1]))
    hh = hits[s].astype(np.float64); tt = tru[s].astype(np.float64)
    b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
    return CI.merge_pool(hh[b], tt[b])[0], pv, phim


def main():
    t0 = time.process_time()
    mode = sys.argv[1]
    RS, CI, FF, K, GT, cfg, wcfg = W.load_frozen()
    out = dict(mode=mode, records=[])
    if mode == 'events':
        todo = json.loads(Path(sys.argv[2]).read_text()); dst = sys.argv[3]
        budget = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
        out['n_todo'] = len(todo)
        for path, i, kS_stored, kF_stored in todo:          # given order (unconfirmed first); stops at the CPU budget
            if time.process_time() - t0 > budget:
                out['stopped_at_budget'] = True
                break
            Hm, pv, phim = load_event(path, i, FF, CI)
            r = her_witnesses(Hm, pv, phim, cfg, wcfg, FF, K)
            kb = r['kb']
            out['records'].append(dict(path=path, event=i, stored=[kS_stored, kF_stored],
                                       rerun=[int(kb[4, 0, 0]), int(kb[4, 0, 1])],
                                       S=r['wit'].get((4, 0, 0)), F=r['wit'].get((4, 0, 1)), n_planes=r['n_planes']))
            print(out['records'][-1], file=sys.stderr, flush=True)
    else:
        dst = sys.argv[2]
        import test_p2w_subset as TT
        rng = np.random.default_rng(11)
        for it in range(200):                         # same draws, same order as test_T7_monotone_T8_finder
            ax, n2, n = TT.frame(0.3 + rng.uniform(-0.1, 0.1), rng.uniform(-0.7, 0.7), rng.uniform(0, np.pi))
            pair = [(rng.uniform(-3, 3), rng.uniform(-0.02, 0.02)), (rng.uniform(-3, 3), rng.uniform(-0.02, 0.02))]
            drop = tuple(rng.choice(10, rng.integers(0, 4), replace=False))
            H = TT.event(ax, n2, pair, drop=drop)
            if len(H) < 8:
                continue
            k0 = TT.run(H)
            ex = []
            for _q in range(rng.integers(1, 40)):
                s = TT.SURF[rng.integers(len(TT.SURF))]
                ex.append(TT.hit(s, ax, n2, rng.uniform(-70, 70), off_n=rng.choice([0.0, 0.0, rng.normal(0, 3.0)]), nrm=n))
            ex = np.array(ex); ex = ex[np.isfinite(ex).all(1)]
            H2 = np.concatenate([H, ex])
            k1 = TT.run(H2)
            if not (k1 > k0).any():
                continue
            r0 = her_witnesses(H, TT.PV, 0.3, cfg, wcfg, FF, K)        # her witnesses BEFORE the hits were added
            r1 = her_witnesses(H2, TT.PV, 0.3, cfg, wcfg, FF, K)
            assert (r0['kb'] == k0).all() and (r1['kb'] == k1).all(), 'instrumented rerun differs from her kernel'
            for wi, si, rd in np.argwhere(k1 > k0).tolist():
                w0 = r0['wit'].get((wi, si, rd)); w1 = r1['wit'].get((wi, si, rd))
                rec = dict(trial=it, n_hits=[len(H), len(H2)], entry=[wi, si, rd], k0=int(k0[wi, si, rd]),
                           k1=int(k1[wi, si, rd]), wit0=w0, wit1=w1)
                if si == 0 and wi > 0:                   # my own search on the enlarged event (s = 0 only)
                    U, CX, CY, S0, S1, LC, SD = R.road_arrays(H2, TT.PV, 0.3, FF)
                    bk, wm, wn, st = R.search_event(U, CX, CY, S0, S1, LC, SD, 0.3, float(W.WL[wi]), R.CFG['w_c'],
                                                    R.CFG['t_tol'], R.CFG['iters'], R.CFG['delta95'], R.CFG['eta_max'])
                    c = 1 if rd else 0
                    v = verify(U, CX, CY, S0, S1, LC, SD, np.where(wm[c])[0], wn[c], 0.3, float(W.WL[wi])) if bk[c] < 99 else None
                    rec['mine_on_H2'] = [int(bk[c]), bool(v[0]) if v else False, (7 - v[2]) if v and v[0] else 99]
                out['records'].append(rec)
                print(rec, file=sys.stderr, flush=True)
    out['cpu_s'] = time.process_time() - t0
    Path(dst).write_text(json.dumps(out, default=str))
    print(f'done cpu {out["cpu_s"]:.0f} s', file=sys.stderr)


if __name__ == '__main__':
    main()
