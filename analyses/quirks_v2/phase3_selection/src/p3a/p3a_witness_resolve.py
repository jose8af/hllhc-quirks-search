"""p3a_witness_resolve.py -- the witnesses that p3a_witness_check.py reported as 'subset_failed', re-checked with the
KERNEL's plane normal instead of a re-fitted one.  Aurora, 2026-11-24.

  <tt python> p3a_witness_resolve.py <p3a_witness_check.json> <out.json>

p3a_witness_check.py hands Nils's verifier a normal re-fitted on the witness hits, because the classifier does not
store the normal of the plane a witness lives in.  For the failures (all '3sigma': plane membership) this script
recovers the classifier's planes: the seed loop of p3a_subset.road_multi (itself a copy of p2w_subset.subset_road) is
repeated in Python with the finder's refit kernel (kernels.refit_packed, unchanged), first over the seed pairs inside
the witness, then over every seed pair of the road; for every plane whose selected hits contain the witness, the
witness is given to review_nils_subset.verify with THAT plane's normal.  'resolved' = the verifier accepts it with
k <= 3 for at least one such plane.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p3a_subset as A  # noqa: E402
import p3a_indep as IND  # noqa: E402

NR = IND.NR
B = A.B


def planes_with(mask, U, CX, CY, S0, S1, LC, SD, J, cfg, K, pairs):
    """Yield the normals of the classifier's planes (seed pairs `pairs`) whose selected hit set contains `mask`."""
    n = len(U)
    P = np.empty((6, n)); P[0] = U[:, 0]; P[1] = U[:, 1]; P[2] = U[:, 2]; P[3] = CX; P[4] = CY
    P[5] = np.linalg.norm(U, axis=1)
    SF = np.zeros((16, 8))
    for i in range(n):
        SF[J[i], 3] = S0[i]; SF[J[i], 4] = S1[i]
    pid = np.arange(n).astype(np.int64)
    L = np.empty(n, np.int64); sel = np.empty(n, np.int64); selp = np.empty(n, np.int64); selw = np.empty(n)
    M = np.zeros((3, 3)); cnt = np.zeros((10, 3), np.int64); sgu = np.empty(16)
    want = set(np.where(mask)[0].tolist())
    for ia, ib in pairs:
        c = np.cross(U[ia], U[ib]); nc = np.linalg.norm(c)
        if not nc >= 1e-3 * P[5, ia] * P[5, ib]:
            continue
        a0 = U[ia] / P[5, ia] + U[ib] / P[5, ib]; an = np.linalg.norm(a0)
        if not an > 1e-9:
            continue
        n0 = c / nc; ax0 = a0 / an
        d = np.abs(U @ n0)
        Lm = np.where(d < np.where(LC >= 7, 60.0, 5.0))[0]
        m = len(Lm); L[:m] = Lm
        r = K.refit_packed(L, m, P, J, LC, SD, pid, n0, ax0, float(cfg.w_c), int(cfg.iters), float(cfg.t_tol), 2.5, SF, sel, M,
                           cnt, sgu, selp, selw, 0, n0[0], n0[1], n0[2])
        st, nx, ny, nz, nfin = r[0], r[1], r[2], r[3], r[12]
        if st != 0:
            continue
        if want <= set(sel[:nfin].tolist()):
            yield np.array([nx, ny, nz])


def main(win, out):
    RS, CI, FF, K, GT, cfg, wcfg = B.load_frozen()
    Wj = json.loads(Path(win).read_text())
    res = []
    cache = {}
    for path, i, wn, why, vk, wk in Wj['fails']:
        if path not in cache:
            cache.clear()
            f = np.load(path); meta = json.loads(str(f['meta']))
            cache[path] = (meta, f['hits'], f['hit_off'].astype(np.int64), f['evt'], f['tru'])
            f.close()
        meta, hits, off, evt, tru = cache[path]; ec = meta['evt_cols']
        h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
        pv = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]].astype(np.float64) + \
            np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * NR.PV_SIGMA
        s = slice(int(off[i]), int(off[i + 1]))
        hh = hits[s].astype(np.float64)
        b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
        Hm = CI.merge_pool(hh[b], tru[s][b].astype(np.float64))[0]
        phim = float((evt[i, ec.index('phimet_reco_v1')] + np.pi) % (2 * np.pi) - np.pi)
        U, CX, CY, S0, S1, LC, SD = NR.road_arrays(Hm, pv, phim, FF)
        sidm = Hm[:, 0].astype(np.int64)
        m, U0 = FF.road_select(Hm, sidm, pv, phim, cfg)
        Hr = Hm[m]; J = FF.JLOC_OF[sidm[m]]
        wi = A.WNAMES.index(wn); W = float(A.WL[wi])
        r0 = A.classify_pool(Hm, pv, phim, cfg, wcfg, FF, K, tw=wi)
        mask = np.zeros(len(Hr), bool)
        for row in r0['wit_rows']:
            mask |= (Hr == row[None, :]).all(1)
        ipw = [t for t in np.where(mask)[0] if LC[t] <= 6]
        allip = [t for t in range(len(U)) if LC[t] <= 6]
        best = None; nplanes = 0; stage = ''
        for stage, idx in (('witness pairs', ipw), ('all road pairs', allip)):
            pairs = [(a, c) for a in idx for c in idx if LC[c] < LC[a]]
            for nrm in planes_with(mask, U, CX, CY, S0, S1, LC, SD, J, cfg, K, pairs):
                nplanes += 1
                v = NR.verify(U, CX, CY, S0, S1, LC, SD, mask, nrm / np.linalg.norm(nrm), phim, W=W)
                if v['ok'] and v['k'] <= 3:
                    best = v
                    break
                best = best or v
            if best is not None and best['ok'] and best['k'] <= 3:
                break
        ok = bool(best is not None and best['ok'] and best['k'] <= 3)
        res.append(dict(path=path.split('/')[-1], event=i, width=wn, k_classifier=wk, resolved=ok, stage=stage,
                        n_planes_containing_witness=nplanes, verifier=(None if best is None else
                                                                     dict(ok=best['ok'], k=best['k'], why=best['why']))))
        sys.stderr.write(f'{res[-1]}\n')
    o = dict(n=len(res), n_resolved=sum(r['resolved'] for r in res), items=res)
    Path(out).write_text(json.dumps(o, indent=1))
    sys.stderr.write(f"resolved {o['n_resolved']} of {o['n']}\n")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
