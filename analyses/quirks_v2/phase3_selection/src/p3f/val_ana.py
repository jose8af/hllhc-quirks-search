"""p3-f validation analysis (method V1 recapture at R04, V2 saturation at R04).  Reads validate-mode outputs of
occx_job.py; prints and writes JSON.  Code check only: R04 is the only rung read.

  python val_ana.py OUT.json file1.npz [file2.npz ...]
"""
import json
import logging
import sys

import numpy as np

log = logging.getLogger('val_ana')


def sets(off, hits):
    return [frozenset(hits[off[k]:off[k + 1]].tolist()) for k in range(len(off) - 1)]


def same(A, B):
    return len(A & B) >= 0.5 * min(len(A), len(B))


def greedy_groups(order, S):
    """Greedy leader grouping in the given rank order (weights.group_sets semantics)."""
    leaders = []
    for k in order:
        if not any(same(S[k], S[g]) for g in leaders):
            leaders.append(k)
    return len(leaders)


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    out = {'trials': []}
    tot = {0: [0.0, 0.0], 1: [0.0, 0.0]}
    for fn in sys.argv[2:]:
        z = np.load(fn)
        meta = json.loads(str(z['meta_json']))
        M = meta['planes']
        k = 0
        while f'val{k}_rec' in z.files:
            rec = z[f'val{k}_rec']; aux = z[f'val{k}_aux']; V = z[f'val{k}_V']
            S = sets(z[f'val{k}_off'], z[f'val{k}_hits'])
            tr = dict(file=fn, val=k, M=M)
            for mp in (0, 1):
                ix = np.where(rec[:, 0] == mp)[0]
                Rc = 0
                for i in ix:
                    Rc += sum(1 for j in ix if j != i and same(S[i], S[j]))
                Ex = float((M - 1) * V[ix, 0].sum())
                tot[mp][0] += Rc; tot[mp][1] += Ex
                HT = float((1.0 / V[ix, 0]).sum() / M) if len(ix) else 0.0
                # saturation: rank order (-N_IP2 of the candidate, chi2/ndf), prefixes of the draw order
                sat = {}
                for frac in (0.1, 0.3, 1.0):
                    mlim = int(round(frac * len(ix)))
                    sub = ix[:mlim]
                    order = sub[np.lexsort((aux[sub, 2], -aux[sub, 0]))]
                    sat[str(frac)] = greedy_groups(order, S)
                tr[f'map{mp}'] = dict(n_R04=int(len(ix)), recapture=int(Rc), expected=Ex, HT_G_R04=HT,
                                      greedy_groups_at_fraction_of_M=sat)
                log.info('%s val%d map %d: n %d recapture %d expected %.1f HT G(R04) %.1f greedy %s', fn, k, mp,
                         len(ix), Rc, Ex, HT, sat)
            out['trials'].append(tr)
            k += 1
    for mp in (0, 1):
        r, e = tot[mp]
        out[f'map{mp}_ratio'] = dict(recapture=r, expected=e, ratio=r / e if e > 0 else None,
                                     sigma_approx=float(np.sqrt(2 * r) / e) if e > 0 else None)
        log.info('map %d: recapture/expected = %.0f / %.1f = %.3f (+- %.3f approx)', mp, r, e, r / e,
                 np.sqrt(2 * r) / e)
    with open(sys.argv[1], 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
