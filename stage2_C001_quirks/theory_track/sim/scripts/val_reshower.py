"""val_reshower.py -- B-5 regeneration test (fixer S2-R1): compare a re-showered Pythia job (scripts/reshower.py, same LHE
piece, same card and seed) with the rows of the delivered npz that carry the same (chunk, py8_job).  Reports whether every
stored column is reproduced bit-for-bit, else the max deviation.  Usage:
  pixi run -e ana python scripts/val_reshower.py <delivered.npz> <chunk> <job> <reshowered_s<job>.npz> [label]
Appends the result to results/reshower_repro.json."""
import json
import os
import sys

import numpy as np

f, k, j, r = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
lab = sys.argv[5] if len(sys.argv) > 5 else os.path.basename(f)
c = np.load(f); n = np.load(r)
s = (c['chunk'] == k) & (c['py8_job'] == j)
w_c = c['w'][s]; w_n = n['w']
# delivered weights are renormalised by N_LHE(job)/N_LHE(point) at merging; compare shapes after normalising both to unit sum
out = dict(file=os.path.basename(f), chunk=k, job=j, rows_delivered=int(s.sum()), rows_reshowered=int(len(w_n)))
cols = ['p_qp', 'p_qm', 'p_qq_hard', 'recoil', 'recoil_eta5', 'nu', 'jets', 'njet', 'n_me', 'gamma_star', 'pt_pair']
res = {}
if s.sum() == len(w_n):
    for col in cols:
        a, b = c[col][s], n[col]
        res[col] = dict(bitwise=bool(np.array_equal(a, b)), max_abs_diff=float(np.max(np.abs(a.astype(float) - b.astype(float)))) if a.size else 0.0)
    res['w_normalised'] = dict(bitwise=False, max_rel_diff=float(np.max(np.abs(w_c / w_c.sum() - w_n / w_n.sum()) / (w_n / w_n.sum() + 1e-300))))
    res['wvar_normalised_max_rel_diff'] = float(np.nanmax(np.abs(c['wvar'][s] / c['wvar'][s].sum(0) - n['wvar'] / n['wvar'].sum(0)) /
                                                     (np.abs(n['wvar'] / n['wvar'].sum(0)) + 1e-300)))
out['columns'] = res
out['all_kinematics_bitwise'] = bool(res) and all(v['bitwise'] for kk, v in res.items() if isinstance(v, dict) and kk in cols)
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results', 'reshower_repro.json')
R = json.load(open(p)) if os.path.exists(p) else {}
R[lab] = out
json.dump(R, open(p, 'w'), indent=1)
print(json.dumps(out, indent=1))
