"""review_bjorn_v1tag.py -- what v1's "hard-scatter candidate" tag counts, measured on the v2 C1 reproduction sample.

  <tt python> review_bjorn_v1tag.py '<glob p2-a-c1-sm/000/c1sm-*.npz>' <surfaces_s3.json> <out.json>

Bjorn (reviewer), 2026-11-19.  Sample: c1.sm = Z(nunu)+jets with pile-up 200, after CKF, v1 chain (2,000 generated events;
NOT a signal sample).  v1's SM rate (background.sm_term l.712) counts candidates with tag bit 0 and n_hs_band >= 1 (at
least one hard-scatter hit inside the candidate's collection band).  The frozen v2 attribution (STR l.747-753) needs
j >= n/2 double-crossing layers whose hits come from the hard scatter (n = 7 at R04-R11: j >= 4).
For every candidate at R05 / R06 (N_IT2 >= 3, N_IP2 >= 7, w_core < 37.5 / 18.75; all have a full hit record) this script
counts j = number of IT+PS layers with a double crossing made of hard-scatter hits alone (IT: >= 2 hits; PS: >= 2 on each
side; hard scatter = interaction id % 10^6 == 3000), and the number of hard-scatter hits among the candidate's hits.
Raw (unweighted) candidate counts; no weights, no efficiency.
"""
import glob
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

LAYERS = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']


def main(pat, surf, out):
    S = json.loads(Path(surf).read_text())['surfaces']
    lc_of = np.full(len(S), -1); side_of = np.zeros(len(S), int)
    for i, s in enumerate(S):
        for k, p in enumerate(LAYERS):
            if s['name'] == p or s['name'].startswith(p + '_'):
                lc_of[i] = k; side_of[i] = 1 if s['name'].endswith('_in') else (2 if s['name'].endswith('_out') else 0)
    res = {r: dict(n_cand=0, n_tagged=0, n_tagged_with_record=0, j_hs=Counter(), n_hs_hits=Counter(), n_hs_band=Counter(),
                   n_frozen_attributed=0, events_tagged=set(), events_attributed=set(), cross_check_bad=0)
           for r in ('R05', 'R06')}
    nev = 0; mus = set(); nfiles = 0
    for f in sorted(glob.glob(pat)):
        z = np.load(f)
        m = json.loads(str(z['meta_json'])); mus.add(m['chain_meta']['mu']); nev += int(m['job']['n_events']); nfiles += 1
        tag = z['cand.tag']; nit2 = z['cand.nit2']; nip2 = z['cand.nip2']; w = z['cand.dw_core']; nhb = z['cand.n_hs_band']
        tr = z['cand.trial'].astype(np.int64); ix = z['cand.idx'].astype(np.int64); cross = z['cand.cross']
        evt = z['trials.ev'][tr]
        rec = {(int(a), int(b)): k for k, (a, b) in enumerate(zip(z['hit.trial'], z['hit.cand']))}
        off = z['hit.off']; ref = z['hit.ref']; sid = z['hit.sid'].astype(np.int64); INT = z['hit.INT']
        base = ((tag & 1) > 0) & (nit2 >= 3) & (nip2 >= 7)
        for r, W in (('R05', 37.5), ('R06', 18.75)):
            d = res[r]
            sel = np.where(base & (w < W))[0]
            d['n_cand'] += len(sel)
            for c in sel:
                if nhb[c] < 1:
                    continue
                d['n_tagged'] += 1; d['n_hs_band'][int(min(nhb[c], 20))] += 1; d['events_tagged'].add((f, int(evt[c])))
                k = rec.get((int(tr[c]), int(ix[c])))
                if k is None:
                    continue
                d['n_tagged_with_record'] += 1
                h = ref[off[k]:off[k + 1]]
                lc = lc_of[sid[h]]; sd = side_of[sid[h]]; hs = (INT[h] % 1_000_000) == 3000
                # self-check of my crossing definition against the stored cand.cross (all hits)
                cr_all = [int((lc == L).sum()) if L < 4 else int(min(((lc == L) & (sd == 1)).sum(), ((lc == L) & (sd == 2)).sum()))
                          for L in range(10)]
                if cr_all != [int(x) for x in cross[c]]:
                    d['cross_check_bad'] += 1
                j = 0
                for L in range(7):
                    a = (lc == L) & hs
                    n = int(a.sum()) if L < 4 else int(min((a & (sd == 1)).sum(), (a & (sd == 2)).sum()))
                    j += n >= 2
                d['j_hs'][j] += 1; d['n_hs_hits'][int(min(hs.sum(), 20))] += 1
                if j >= 4:
                    d['n_frozen_attributed'] += 1; d['events_attributed'].add((f, int(evt[c])))
        z.close()
    o = dict(n_files=nfiles, n_events_generated=nev, mu=sorted(mus))
    for r, d in res.items():
        o[r] = dict(n_cand=d['n_cand'], n_tagged_v1_rule=d['n_tagged'], n_tagged_with_hit_record=d['n_tagged_with_record'],
                    cross_check_bad=d['cross_check_bad'], n_events_with_tagged=len(d['events_tagged']),
                    n_frozen_attributed_j_ge_4=d['n_frozen_attributed'], n_events_frozen_attributed=len(d['events_attributed']),
                    j_hs={str(k): v for k, v in sorted(d['j_hs'].items())},
                    n_hs_hits_in_candidate={str(k): v for k, v in sorted(d['n_hs_hits'].items())},
                    n_hs_band={str(k): v for k, v in sorted(d['n_hs_band'].items())})
    Path(out).write_text(json.dumps(o, indent=1))
    sys.stdout.write(json.dumps(o) + '\n')


if __name__ == '__main__':
    main(*sys.argv[1:4])
