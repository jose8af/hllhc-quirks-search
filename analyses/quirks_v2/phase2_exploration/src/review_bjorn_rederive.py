"""review_bjorn_rederive.py -- independent re-derivation of the Z(nunu) own-hit counts of the PRELIMINARY rule-1 reading.

  <tt python> review_bjorn_rederive.py <dir,dir,...> <out.json>

Bjorn (reviewer), 2026-11-19.  Imports nothing of p2t_*.  Reads the stored candidate rows (npz members meta, cand) of the
p2-c-pilot-cls* outputs and counts EVENTS (pilot file path, event index) of the Z(nunu) pilot, variant 0 (all own hits),
with at least one stored candidate satisfying, at rung width W:
  pass       N_IT2 >= 3, N_IP2 >= 7, w_core < W                       (k = 0)
  near-pass  N_IT2 >= 3, w_core < W, k = max(0, 7 - N_IP2) + max(0, s - N_2S2) <= floor((7 + s) / 2)
The event key is the pilot file PATH (not the job name), so a file classified in two outputs would be counted once and
reported.  Also: weighted counts (sum of w_v1 / w_max), k spectrum, composition of the near-pass candidates.
"""
import glob
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

W = {'R04': None, 'R05': 37.5, 'R06': 18.75, 'R07': 9.4, 'R08': 4.7}


def main(dirs, out):
    fs = sorted(f for d in dirs.split(',') for f in glob.glob(str(Path(d) / '*.npz')))
    paths = Counter(); rows = []; nfull = 0; sw = 0.0; wmax = 0.0; nlow = 0; ngen = 0; nz = 0
    whist = Counter()
    for f in fs:
        z = np.load(f)
        m = json.loads(str(z['meta'])); c = z['cand']; col = {k: i for i, k in enumerate(m['cand_cols'])}
        zfile = {}
        for fi, fm in enumerate(m['files']):
            paths[fm['path']] += 1
            if fm['stream'] == 'pilot.hs0.znn':
                zfile[fi] = fm['path']; nz += 1; ngen += fm['n_events']; wmax = max(wmax, fm['w_max'])
                for k, n in fm['w_hist'].items():
                    whist[float(k)] += n
        for r in c:
            fi = int(r[col['file']])
            if fi in zfile:
                rows.append((zfile[fi], int(r[col['event']]), int(r[col['variant']]), r[col['nit2']], r[col['nip2']],
                             r[col['n2s2']], r[col['dw_core']], r[col['w']], r[col['n_particles']], r[col['n_ckf_flag']],
                             r[col['nhit']], r[col['n_product']], r[col['n_fatras_gen']], r[col['orient']],
                             r[col['dphi_met']], r[col['eta_axis']], r[col['p_chi2core']]))
    for w, n in whist.items():
        if w >= 0.5:
            nfull += n; sw += w * n
        elif w > 0:
            nlow += n
    R = np.array([r[2:] for r in rows], float); ev = [r[:2] for r in rows]
    res = dict(n_outputs=len(fs), n_pilot_files=len(paths), n_files_twice=sum(1 for v in paths.values() if v > 1),
               n_z_files=nz, n_generated=ngen, n_full=nfull, n_low=nlow, sum_w_full=sw, w_max=wmax, M_Z=sw / wmax,
               w_hist={str(k): v for k, v in sorted(whist.items())}, n_z_rows=len(rows),
               n_rows_w_core_nan=int(np.isnan(R[:, 4]).sum()), max_abs_dphi=float(R[:, 12].max()),
               max_abs_eta=float(np.abs(R[:, 13]).max()), min_nit2=float(R[:, 1].min()), min_nip2=float(R[:, 2].min()),
               orient_values=sorted(set(R[:, 11].tolist())), counts={})
    for var in (0, 1):
        for rung, w in W.items():
            for s in (0, 3):
                sel = (R[:, 0] == var) & (R[:, 1] >= 3)
                if w is not None:
                    sel &= R[:, 4] < w
                k = np.maximum(0, 7 - R[:, 2]) + np.maximum(0, s - R[:, 3])
                best = {}                                    # per event: smallest k, and weight
                for i in np.where(sel)[0]:
                    e = ev[i]
                    if e not in best or k[i] < best[e][0]:
                        best[e] = (int(k[i]), R[i, 5], i)
                kmax = (7 + s) // 2
                d = dict(kmax=kmax)
                for cls, lo, hi in (('full', 0.5, 9.), ('low', 0., 0.5)):
                    b = {e: v for e, v in best.items() if lo <= v[1] < hi}
                    spec = Counter(v[0] for v in b.values())
                    d[cls] = dict(n_pass=spec.get(0, 0), n_near=sum(n for kk, n in spec.items() if kk <= kmax),
                                  k_spectrum={str(kk): n for kk, n in sorted(spec.items())},
                                  near_weighted_over_wmax=sum(v[1] for v in b.values() if v[0] <= kmax) / wmax,
                                  pass_weighted_over_wmax=sum(v[1] for v in b.values() if v[0] == 0) / wmax)
                    if cls == 'full' and var == 0 and s == 0:
                        ii = [v[2] for v in b.values() if v[0] <= kmax]
                        npart = Counter(int(R[i, 6]) for i in ii)
                        fck = np.array([R[i, 7] / max(R[i, 8], 1) for i in ii])
                        d[cls]['best_cand_n_particles'] = {str(a): n for a, n in sorted(npart.items())}
                        d[cls]['best_cand_all_hits_ckf_flagged'] = int((fck >= 1).sum())
                        d[cls]['best_cand_half_hits_ckf_flagged'] = int((fck >= 0.5).sum())
                        d[cls]['best_cand_no_hit_ckf_flagged'] = int((fck == 0).sum())
                        d[cls]['best_cand_with_secondary_product_hit'] = int(sum(R[i, 9] > 0 for i in ii))
                        d[cls]['best_cand_with_fatras_made_hit'] = int(sum(R[i, 10] > 0 for i in ii))
                res['counts'][f'v{var}_{rung}_s{s}'] = d
    Path(out).write_text(json.dumps(res, indent=1))
    c = res['counts']
    sys.stdout.write(json.dumps({k: v for k, v in res.items() if k != 'counts'}) + '\n')
    for k, v in c.items():
        sys.stdout.write(f"{k} full pass {v['full']['n_pass']} near {v['full']['n_near']} k {v['full']['k_spectrum']} "
                         f"wnear {v['full']['near_weighted_over_wmax']:.2f} | low near {v['low']['n_near']}\n")
    for k in ('v0_R06_s0', 'v0_R08_s0'):
        sys.stdout.write(k + ' ' + json.dumps({a: b for a, b in c[k]['full'].items() if a.startswith('best')}) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
