"""R1 reviewer check: recompute the P1 B-only thickness on the T3V layers with an SVD plane fit (double-precision
accurate) instead of the stored eigh value, for B and B2 at all Lambda <= 5 keV, and compare c2.
Output: review/r1_checks/c_svd.npz  (point key, ev_index, ds_stored, ds_svd, nhits)."""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[4]
D = TT / 'data' / 'sim_stage3'
idx = json.load(open(D / 'STAGE3_INDEX.json'))
keys = [k for k in idx['points'] if k.startswith('p1/') and (k.endswith('_B') or k.endswith('_B2'))]
out = dict(key=[], ev=[], row=[], ds_st=[], ds_svd=[], ds_eig=[], nh=[])
for k in keys:
    for ch in idx['points'][k]['chunks']:
        with np.load(D / ch['file']) as z:
            kinds = z['surf_kinds']; t3 = np.where(kinds == 'T3V')[0]; o = z['hit_offsets']
            hs, hx, hy, hz = z['h_surf'], z['h_x'], z['h_y'], z['h_z']
            ds = z['ds_barrel_um']; evi = z['ev_index'] if 'ev_index' in z.files else None; row = z['row']
            vtx = z['vtx']
            for e in range(int(z['n_events'])):
                s = slice(o[e], o[e + 1]); m = np.isin(hs[s], t3)
                H = np.stack([hx[s][m], hy[s][m], hz[s][m]], 1) - np.asarray(vtx[e] if vtx.ndim == 2 else vtx)[:3] * 0
                n = len(H)
                if n >= 4:
                    sv = np.linalg.svd(H, compute_uv=False)
                    T = H.T @ H / (n - 1); w = np.linalg.eigvalsh(T)
                    out['ds_svd'].append(sv[-1] / np.sqrt(n - 1) * 1e3); out['ds_eig'].append(np.sqrt(max(w[0], 0)) * 1e3)
                else:
                    out['ds_svd'].append(np.nan); out['ds_eig'].append(np.nan)
                out['key'].append(k); out['ev'].append(int(evi[e]) if evi is not None else -1); out['row'].append(int(row[e]))
                out['ds_st'].append(float(ds[e])); out['nh'].append(n)
np.savez(Path(__file__).with_name('c_svd.npz'), **{a: np.array(b) for a, b in out.items()})
print(len(out['key']))
