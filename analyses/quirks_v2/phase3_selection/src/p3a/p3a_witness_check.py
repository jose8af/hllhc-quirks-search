"""p3a_witness_check.py -- the classifier's OWN witnesses under an independent verifier, at every width.  Aurora, 2026-11-24.

  <tt python> p3a_witness_check.py --rows <p3a_counts.json>.rows_m.npz --stride 12 --offset 0 --out /ABS/OUT.json

For every Z(nunu) full-class row of label m in the selected pilot files (every stride-th path of the row export) and
every width at which the row is counted in reading UNION, S (k <= 3 at s = 0 or k <= 5 at s = 3): the witness of
p3a_subset.classify_pool (best subset at s = 0 over c0-c4, target width = that width; unchanged code) is handed to
Nils's pure-numpy verifier (review_nils_subset.verify, imported unchanged; own axis; 3 sigma membership; forward;
window; alignment; w_core < W; layer counts).  The classifier does not store the plane normal, so the normal handed to
the verifier is re-fitted here on the witness hits: PV-constrained weighted least squares with the verifier's own
sigma model (weights 1 / sigma_tot^2, 6 iterations from the unweighted solution; function fit_normal).  A witness that
fails with this re-fitted normal is reported as 'failed' although it may hold with the kernel's normal: 'failed' is
an upper count of problems, 'verified' a lower count of confirmed witnesses.  (First version: unweighted normal; on
real hits it failed the 3 sigma membership for most witnesses, 43 of 62 in two files: the fit, not the witnesses.)  This extends
his check "her witness passes my verifier in 136 / 136" (R08, s = 0) to R04-R07 and to s = 3 (N_2S2 of the verified
witness counted here).  The stored witness is either an own-axis subset (categories c1-c4) or the plane's full set
judged with the FINDER's axis (c0).  For a full-set witness the own-axis verifier is not the convention it was counted
under: it is reported apart (passes the own-axis verifier as well / holds under the finder's axis only).
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p3a_subset as A  # noqa: E402
import p3a_indep as IND  # noqa: E402

NR = IND.NR
B = A.B


def fit_normal(u, cx, cy, s0, s1, ttol, iters=6, extra=40):
    """PV-constrained plane through the hits u (n, 3): smallest eigenvector of sum w u u^T, w = 1 / sigma_tot^2 with
    the sigma model of review_nils_subset.verify (l.343-345), iterated.  If a hit is then outside 3 sigma_tot, up to
    `extra` re-weighted iterations raise the weight of the hits beyond 3 sigma (w x (d^2 / 9 sigma^2)^2, cumulative):
    a search for A normal under which every witness hit is a member, which is what the witness claims exists."""
    _, _, vt = np.linalg.svd(u / np.linalg.norm(u, axis=1)[:, None])
    n = vt[-1] / np.linalg.norm(vt[-1])
    boost = np.ones(len(u))
    for it in range(iters + extra):
        aa = -n[0] * cy + n[1] * cx
        sg2 = np.maximum(aa ** 2 * s0 ** 2 + n[2] ** 2 * s1 ** 2, 1e-8) + ttol ** 2
        if it >= iters:
            pull2 = (u @ n) ** 2 / (9.0 * sg2)
            if not (pull2 >= 1.0).any():
                break
            boost = boost * np.maximum(1.0, pull2) ** 2
        M = (u * (boost / sg2)[:, None]).T @ u
        ev, evec = np.linalg.eigh(M)
        v = evec[:, 0]
        n = v if v @ n > 0 else -v
    return n / np.linalg.norm(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', required=True)
    ap.add_argument('--stride', type=int, default=12)
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    RS, CI, FF, K, GT, cfg, wcfg = B.load_frozen()
    z = np.load(a.rows)
    paths = [str(p) for p in z['paths']]
    rdl = list(z['readings']); wl = list(z['widths']); cats = list(z['cats'])
    KU = z['K'][rdl.index('UNION')]; KC = z['KC']
    zsel = z['term'] == 'Z'
    zp = sorted({paths[i] for i in z['path_idx'][zsel]})
    todo = zp[a.offset::a.stride]
    T = {wn: dict(counted_s0=0, subset_witness=0, subset_verified=0, subset_failed=0, fullset_witness=0,
                  fullset_also_own_axis_verified=0, fullset_finder_axis_only=0, no_witness_at_kmax=0,
                  counted_s3=0, verified_s3=0, s3_not_from_this_witness=0, why={}) for wn in wl}
    fails = []
    for path in todo:
        pi = paths.index(path)
        rows = np.where(zsel & (z['path_idx'] == pi))[0]
        f = np.load(path); meta = json.loads(str(f['meta'])); ec = meta['evt_cols']
        hits = f['hits']; off = f['hit_off'].astype(np.int64); evt = f['evt']; tru = f['tru']
        f.close()
        for r in rows:
            i = int(z['event'][r])
            h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
            pv = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]].astype(np.float64) + \
                np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * NR.PV_SIGMA
            s = slice(int(off[i]), int(off[i + 1]))
            hh = hits[s].astype(np.float64)
            b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
            Hm = CI.merge_pool(hh[b], tru[s][b].astype(np.float64))[0]
            phim = float((evt[i, ec.index('phimet_reco_v1')] + np.pi) % (2 * np.pi) - np.pi)
            U, CX, CY, S0, S1, LC, SD = NR.road_arrays(Hm, pv, phim, FF)
            m, U0 = FF.road_select(Hm, Hm[:, 0].astype(np.int64), pv, phim, cfg)
            Hr = Hm[m]
            assert len(Hr) == len(U)
            for wi, wn in enumerate(wl):
                c0 = KU[r, wi, 0, 0] <= 3; c3 = KU[r, wi, 1, 0] <= 5
                if not (c0 or c3):
                    continue
                res = A.classify_pool(Hm, pv, phim, cfg, wcfg, FF, K, tw=wi)
                W = float(A.WL[wi])
                wr = res['wit_rows']
                mask = np.zeros(len(Hr), bool)
                for row in wr:
                    mask |= (Hr == row[None, :]).all(1)
                t = T[wn]
                ok = False; v = dict(why='no witness', k=99)
                if mask.sum() >= 4:
                    nrm = fit_normal(U[mask], CX[mask], CY[mask], S0[mask], S1[mask], NR.CFG['t_tol'])
                    v = NR.verify(U, CX, CY, S0, S1, LC, SD, mask, nrm, phim, W=W)
                    ok = v['ok']
                # the stored witness is the plane's full set under the FINDER's axis iff c0 has the witness's k (c0 is
                # recorded first and replaced only by a strictly smaller k); otherwise it is an own-axis subset
                is_full = int(KC[r, cats.index('c0'), wi, 0, 0]) == int(res['wk'])
                if c0:
                    t['counted_s0'] += 1
                    if res['wk'] > 3:
                        t['no_witness_at_kmax'] += 1          # counted in UNION through BASE only (its own search)
                    elif is_full:
                        t['fullset_witness'] += 1
                        if ok and v['k'] <= 3:
                            t['fullset_also_own_axis_verified'] += 1
                        else:
                            t['fullset_finder_axis_only'] += 1
                    else:
                        t['subset_witness'] += 1
                        if ok and v['k'] <= 3:
                            t['subset_verified'] += 1
                        else:
                            t['subset_failed'] += 1
                            t['why'][v['why']] = t['why'].get(v['why'], 0) + 1
                            fails.append([path, i, wn, v['why'], int(v['k']), int(res['wk'])])
                if c3:
                    t['counted_s3'] += 1
                    if ok and v['k'] + max(0, 3 - IND.n2s2_of(LC, SD, mask)) <= 5:
                        t['verified_s3'] += 1
                    else:
                        t['s3_not_from_this_witness'] += 1
    out = dict(rows=a.rows, stride=a.stride, offset=a.offset, n_files=len(todo), files=todo, tables=T, fails=fails,
               n_fails=len(fails), cpu_s=time.process_time() - t0,
               nils_sha256=hashlib.sha256(Path(NR.__file__).read_bytes()).hexdigest(),
               p3a_subset_sha256=hashlib.sha256(Path(A.__file__).read_bytes()).hexdigest())
    p = Path(a.out); part = p.with_name(p.name + '.part')
    with open(part, 'w') as fo:
        fo.write(json.dumps(out, indent=1)); fo.flush(); os.fsync(fo.fileno())
    part.replace(p)
    for wn in wl:
        sys.stderr.write(f'{wn} {T[wn]}\n')


if __name__ == '__main__':
    main()
