"""p3a_attrib.py -- attribution by truth (STR l.747-753) of every stored B1 / hs / lowpt row, from the witness hit tables
dumped by p3a_multi.py.  Aurora, 2026-11-24.

  <tt python> p3a_attrib.py <p3a_counts.json> <out.json>          (on a worker: imports the frozen finder's layer tables)

Origin classes inside a B1-type pilot event (one Geant4 vertex, no pile-up; route table STR l.228-233):
  product  hits of particles produced at or after the Geant4 vertex (vsec >= 1): the B1 class of the sample
  parent   hits of the parent hadron (vsec = 0), a Fatras particle: for the minimum-bias share a pile-up particle (B2
           route), in pilot.c0.hs a hard-scatter particle (B4 route)
For each witness (per width; the best subset at s = 0, reading S): per double-crossing layer (IT: >= 2 hits; PS / 2S:
>= 2 hits on each sensor) the class that makes it BY ITSELF (product-only, parent-only) or 'both needed' (the layer is
double-crossing only with hits of both classes).  j_product / j_parent = number of layers made by one class alone.
Attributed to the B1 class if j_product >= n/2 (n = 7 at s = 0: j >= 4, STR l.749-750 as read in BJO section 3 (ii));
'mixed' if 1 <= j < n/2 for every class; 'pure pile-up'-like (parent only) if j_product = 0.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

QV2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(QV2)); os.chdir(QV2)
from acts.stage4.finder import finder as FF  # noqa: E402


def layers(lc, sd, sel):
    c = np.zeros((10, 3), np.int64)
    np.add.at(c, (lc[sel], sd[sel]), 1)
    return np.array([(c[l, 0] if l < 4 else min(c[l, 1], c[l, 2])) >= 2 for l in range(10)])


def main(cin, cout):
    C = json.loads(Path(cin).read_text())
    out = {}
    for lab, L in C['labels'].items():
        res = []
        for d in L['dumps']:
            col = {k: i for i, k in enumerate(d['pool_columns'])}
            r = dict(job=d['job'], path=d['path'].split('/')[-1], event=d['event'], orient=d['orient'], cls=d['cls'],
                     n_early_prod=d['n_early_prod'], parent_pdg=d['evt'].get('parent_pdg'), parent_pt0=d['evt'].get('parent_pt0'),
                     vtx_r=d['evt'].get('vtx_r'), road_dphi=d['evt'].get('road_dphi'), widths={})
            for wn, w in d['witnesses'].items():
                H = np.array(w['hits'], float).reshape(-1, len(col))
                if not len(H):
                    r['widths'][wn] = dict(k=w['k'], n_hits=0)
                    continue
                sid = H[:, col['sid']].astype(np.int64)
                lc = FF.LC_OF[sid]; sd = FF.SIDE_OF[sid]
                prod = H[:, col['vsec']] >= 1
                la = layers(lc, sd, np.ones(len(H), bool)); lp = layers(lc, sd, prod); lq = layers(lc, sd, ~prod)
                ip = slice(0, 7)
                jprod = int(lp[ip].sum()); jpar = int(lq[ip].sum())
                both = int((la[ip] & ~lp[ip] & ~lq[ip]).sum())
                cls_ = ('attributed (B1 class)' if jprod >= 4 else 'attributed (parent class)' if jpar >= 4
                        else 'parent only (no product layer)' if jprod == 0 and both == 0 else 'mixed')
                r['widths'][wn] = dict(k=w['k'], n_hits=int(len(H)), n_product_hits=int(prod.sum()), n_parent_hits=int((~prod).sum()),
                                       n_fatras_made=int((H[:, col['gen']] >= 1).sum()), N_IP2=int(la[ip].sum()), N_2S2=int(la[7:].sum()),
                                       j_product=jprod, j_parent=jpar, layers_needing_both=both, attribution_s0=cls_,
                                       n_particles=int(len(np.unique(H[:, [col['vp'], col['particle'], col['vsec']]], axis=0))))
            res.append(r)
        out[lab] = res
    Path(cout).write_text(json.dumps(out, indent=1))
    for lab, res in out.items():
        for r in res:
            sys.stderr.write(f"{lab} {r['path']} ev {r['event']} or {r['orient']} cls {r['cls']} pt0 {r['parent_pt0']}: "
                             + '; '.join(f"{wn} k={v['k']} jp={v.get('j_product')} jq={v.get('j_parent')} {v.get('attribution_s0', '')}"
                                         for wn, v in r['widths'].items()) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
