"""Reference finder for the G2 equivalence test: acts/stage4/probes/f1r_finder.trial() logic, unchanged, except that the
Python duplicate merge is vectorised (same order, same criterion |1 - |n.g|| < 2e-6; f2r_profile.py showed identical
output).  Imports the probe read-only.  ref_refit() is a verbatim copy of f1r_finder.refit() that also returns the
final window axis (needed for w_core / chi2_core, which f1r computes inside refit with that axis).

Run (theory_track):  nice -n 10 pixi run python -m acts.stage4.finder.reference <i0> <i1> [rho]
  -> data/acts_stage4/g2/ref/ref_rho<rho>_t<i>.npz  (one file per trial; existing files are skipped)
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

from . import trials as TR

F = TR.F
TT = TR.TT
OUT = TT / 'data' / 'acts_stage4' / 'g2' / 'ref'


def ref_refit(U, X, Y, S0, S1, LC, SD, n, axis, iters=3):
    """Verbatim f1r_finder.refit() (+ final axis in the output)."""
    pre = np.abs(U @ n) < np.where(LC >= 7, 60.0, 5.0)
    idx = np.where(pre & (LC >= 0))[0]
    if len(idx) < 4:
        return None
    Ui, Xi, Yi, S0i, S1i = U[idx], X[idx], Y[idx], S0[idx], S1[idx]
    for it in range(iters + 1):
        sg = np.sqrt(np.maximum(F.sig_vec(n, Xi, Yi, S0i, S1i), 1e-4) ** 2 + F.T_TOL ** 2)
        d = Ui @ n
        sel = (np.abs(d) < 3 * sg) & ((Ui @ axis) > 0) & (np.abs(Ui @ np.cross(n, axis)) < F.W_C)
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
    cnt = F.counts_of(LC[hidx], SD[hidx])
    cr = F.cross_from_cnt(cnt)
    nit2 = int(np.sum(cr[:4] >= 2)); not2 = int(np.sum(cr[4:] >= 2))
    hits_l = cnt.sum(1)
    not2h = int(np.sum(hits_l[4:] >= 2))
    wv = U[hidx] @ np.cross(n, axis)
    core = (LC[hidx] <= 6)
    dwc = float(1.4826 * np.median(np.abs(wv[core] - np.median(wv[core])))) if core.sum() > 2 else float('nan')
    return dict(n=n, axis=axis, hidx=hidx, nit2=nit2, not2=not2, nl2=nit2 + not2, not2h=not2h, nl2h=nit2 + not2h,
                nip2=int(np.sum(cr[:7] >= 2)), n2s2=int(np.sum(cr[7:] >= 2)),
                nl1=int(np.sum(cr >= 1)), chi2ndf=float(np.sum(d[sel] ** 2 * w) / max(int(sel.sum()) - 2, 1)),
                nhit=int(sel.sum()), dw_old=float(np.std(wv)), dw_core=dwc)


def chi2_core_np(U, X, Y, S0, S1, LC, hidx, n, axis, w_core):
    """Plan §2.2 item 5 one-step core chi2 (f2r_profile core_stats 'one' variant), numpy, final axis."""
    n2v = np.cross(n, axis)
    w = U[hidx] @ n2v
    ip = LC[hidx] <= 6
    if ip.sum() < 3 or not np.isfinite(w_core):
        return float('nan'), 0
    c = np.median(w[ip]); s = w_core
    lo, hi = c - 2.5 * s, c + 2.5 * s
    s2 = np.abs(n2v[2]) * S1[hidx]
    inn = np.where(ip, (w >= lo) & (w <= hi), (w >= lo - 3 * s2) & (w <= hi + 3 * s2))
    h = hidx[inn]
    if len(h) < 4:
        return float('nan'), int(len(h))
    sg = np.sqrt(np.maximum(F.sig_vec(n, X[h], Y[h], S0[h], S1[h]), 1e-4) ** 2 + F.T_TOL ** 2)
    M = (U[h] * (1.0 / sg ** 2)[:, None]).T @ U[h]
    return float(np.linalg.eigvalsh(M)[0]) / max(len(h) - 2, 1), int(len(h))


VARS = ['nit2', 'not2', 'nl2', 'not2h', 'nl2h', 'nl1', 'chi2ndf', 'nhit', 'dw_old', 'dw_core', 'nip2', 'n2s2',
        'chi2_core', 'n_core', 'nz', 'seed_n2']


def ref_trial(H, sid, pv, phimet, tseed=6):
    T = {}
    t0 = time.perf_counter()
    U0 = H[:, 1:4] - pv[None, :]
    r0 = np.hypot(U0[:, 0], U0[:, 1])
    dph = np.abs((np.arctan2(U0[:, 1], U0[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    m = dph < F.ROAD + np.arcsin(np.minimum(1.0, F.W_C / r0))
    U = np.ascontiguousarray(U0[m]); X = np.ascontiguousarray(H[m, 1]); Y = np.ascontiguousarray(H[m, 2])
    S0 = np.ascontiguousarray(H[m, 4]); S1 = np.ascontiguousarray(H[m, 5])
    sd = sid[m]; LC = F.LC_OF[sd]; SD = F.SIDE_OF[sd]
    phiU = np.arctan2(U[:, 1], U[:, 0]); etaU = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    A = np.where(sd == F.SID['TBPX_L4'])[0]; B = np.where(sd == F.SID['TBPX_L3'])[0]; C = np.where(sd == F.SID['TBPX_L2'])[0]
    t1 = time.perf_counter()
    out, ntrip = F.seeds(U, X, Y, S0, S1, LC, SD, A, B, C, phiU, etaU, phimet, F.ROAD, F.W_C, tseed, F.T_TOL)
    T['seeds'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    fast = []
    for ia, ib, n1, n2 in out:
        n = np.cross(U[ia], U[ib]); n /= np.linalg.norm(n)
        axis = U[ia] / np.linalg.norm(U[ia]) + U[ib] / np.linalg.norm(U[ib]); axis /= np.linalg.norm(axis)
        nf, nl2, nit2, chi, ns, axf = F.refit_nb(U, X, Y, S0, S1, LC, SD, n, axis, F.W_C, 3, F.T_TOL)
        if nl2 >= 4:
            fast.append((nl2, chi, nf, n, axis, n2, ia, ib))
    T['refitnb'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    fast.sort(key=lambda t: (-t[0], t[1]))
    kept = []; Kn = np.zeros((len(fast), 3)); nk = 0
    for nl2, chi, nf, n, axis, n2, ia, ib in fast:
        if nk > 0 and bool(np.any(np.abs(np.abs(Kn[:nk] @ nf) - 1.0) < 2e-6)):
            continue
        f = ref_refit(U, X, Y, S0, S1, LC, SD, n, axis)
        if f is None:
            continue
        f['seed_n2'] = int(n2); f['ia'] = int(ia); f['ib'] = int(ib)
        kept.append(f); Kn[nk] = f['n']; nk += 1
    T['dedup_refitnp'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    res = [f for f in kept if f['nl2'] >= 4]
    for f in res:
        f['chi2_core'], f['n_core'] = chi2_core_np(U, X, Y, S0, S1, LC, f['hidx'], f['n'], f['axis'], f['dw_core'])
        f['nz'] = float(abs(f['n'][2]))
    T['core'] = time.perf_counter() - t1
    T['total'] = time.perf_counter() - t0
    return dict(res=res, out=out, ntrip=int(ntrip), n_road=int(m.sum()), n_fast=len(fast), road_mask=m, T=T)


def save_ref(path, r):
    res = r['res']
    V = np.array([[f[k] for k in VARS] for f in res], float).reshape(-1, len(VARS))
    hoff = np.zeros(len(res) + 1, np.int64)
    hoff[1:] = np.cumsum([len(f['hidx']) for f in res])
    hits = np.concatenate([f['hidx'] for f in res]).astype(np.int32) if res else np.zeros(0, np.int32)
    out = np.array([(a, b, n2) for a, b, n1, n2 in r['out']], np.int32).reshape(-1, 3)
    np.savez_compressed(path, V=V, normal=np.array([f['n'] for f in res]).reshape(-1, 3),
                        axis=np.array([f['axis'] for f in res]).reshape(-1, 3),
                        seed_ab=np.array([(f['ia'], f['ib']) for f in res], np.int32).reshape(-1, 2),
                        hoff=hoff, hits=hits, seeds=out, n_road=r['n_road'], ntrip=r['ntrip'], n_fast=r['n_fast'],
                        T=json.dumps(r['T']))


if __name__ == '__main__':
    i0, i1 = int(sys.argv[1]), int(sys.argv[2])
    rho = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    OUT.mkdir(parents=True, exist_ok=True)
    for i in range(i0, i1):
        path = OUT / f'ref_rho{rho}_t{i:03d}.npz'
        if path.exists():
            continue
        x = TR.trial_inputs(i, rho)
        r = ref_trial(x['H'], x['sid'], x['pv'], x['phimet'])
        save_ref(path, r)
        print('ref', rho, i, 'cands', len(r['res']), 'refits', len(r['out']), {k: round(v, 1) for k, v in r['T'].items()},
              flush=True)
