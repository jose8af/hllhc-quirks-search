"""p3a_dbg_indep.py -- diagnostic: why does Nils's verifier reject some witnesses of his own search at W > 4.7 mm?
  <tt python> -B p3a_dbg_indep.py <p3a_indep output json>     (prints one line per (W, category, reason))
"""
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

QV2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(QV2 / 'phase2_exploration' / 'src'))
import review_nils_subset as NR  # noqa: E402

sys.path.insert(0, str(QV2)); os.chdir(QV2)
from acts.stage4.finder import chain_inputs as CI  # noqa: E402
from acts.stage4.finder import finder as FF  # noqa: E402

d = json.load(open(sys.argv[1]))
C = Counter(); zc = {}
for path, i, w, r in d['events']:
    if path not in zc:
        z = np.load(path); zc[path] = (json.loads(str(z['meta'])), z['hits'], z['hit_off'].astype(np.int64), z['evt'], z['tru'])
    meta, hits, off, evt, tru = zc[path]; ec = meta['evt_cols']
    hsh = hashlib.blake2b(f"p2t-pv|{meta['stream']}|{meta['chunk']}|{i}".encode(), digest_size=8).digest()
    pv = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]] + \
        np.random.default_rng(int.from_bytes(hsh, 'little')).normal(0, 1, 3) * NR.PV_SIGMA
    s = slice(int(off[i]), int(off[i + 1])); hh = hits[s].astype(np.float64); tt = tru[s].astype(np.float64)
    b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
    Hm = CI.merge_pool(hh[b], tt[b])[0]; phim = float((evt[i, ec.index('phimet_reco_v1')] + np.pi) % (2 * np.pi) - np.pi)
    U, CX, CY, S0, S1, LC, SD = NR.road_arrays(Hm, pv, phim, FF); c = NR.CFG
    for W in (75., 37.5, 18.75, 9.4, 4.7):
        bk, wm, wn, st = NR.search_event(U, CX, CY, S0, S1, LC, SD, phim, W, c['w_c'], c['t_tol'], c['iters'], c['delta95'],
                                         c['eta_max'])
        for cat in range(3):
            if bk[cat] < 99:
                v = NR.verify(U, CX, CY, S0, S1, LC, SD, wm[cat], wn[cat], phim, W=W)
                good = v['ok'] and v['k'] <= bk[cat] and (cat != 1 or v['nit2'] >= 3) and (cat != 2 or v['hard'])
                C[(W, cat, bool(good), v['why'], int(bk[cat]), v['k'] if v['ok'] else -1, v['hard'])] += 1
for k, v in sorted(C.items(), key=lambda x: (x[0][2], -x[0][0])):
    if not k[2]:
        sys.stdout.write(f'{k} {v}\n')
sys.stdout.write(f"good {sum(v for k, v in C.items() if k[2])} bad {sum(v for k, v in C.items() if not k[2])}\n")
