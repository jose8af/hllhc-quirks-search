"""INV_A2FC_E500 step 6: trial-level inputs/counters A2 (numpy) vs A2FC on the same rows, per revert point.
Equality of the seeded inputs (pv, phimet, trial seeds, n_btl) and signed paired differences (FC - A2) of the pool
counters (n_road, n_ckf_hits, n_trip, n_kept_all, n_groups, n_ip2ge7).  Read-only.
-> data/acts_stage4/investigation/inv_a2fc_e500_trials.json"""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C  # noqa: E402

EQ = ['trials.phimet', 'trials.pv', 'trials.trial_seed', 'trials.seed', 'trials.delta95', 'trials.n_btl']
SD = ['trials.n_road', 'trials.n_ckf_hits', 'trials.n_trip', 'trials.n_kept_all', 'trials.n_groups', 'trials.n_ip2ge7']
PTS = [('F', 200, 3), ('F', 200, 5), ('F', 500, 3), ('F', 500, 5), ('F', 1000, 3), ('F', 1000, 5), ('F', 1500, 3),
       ('F', 1500, 5), ('S', 500, 5)]


def main():
    out = {}
    man = C.manifest('C1'); fcm = C.manifest('A2FC')
    for spin, m, lam in PTS:
        A = [j for j in man if j['sample'] == 'A2' and j['spin'] == spin and int(j['m']) == m]
        F = {j['paired_a2_id']: j for j in fcm if j['point'] == f'p2/{spin}_m{m}/L{lam:g}_BM'}
        eq = {k: 0 for k in EQ}; sd = {k: [] for k in SD}; n = 0
        for j in A:
            a = C.load_npz(C.PROD.joinpath(*j['out'].split('/')), prefix=('sig.', 'trials.'))
            f = C.load_npz(C.PROD.joinpath(*F[j['id']]['out'].split('/')), prefix=('sig.', 'trials.'))
            ci = {str(c): i for i, c in enumerate(a['sig.cols'])}
            frow = {int(f['sig.tab'][i, ci['row']]): int(f['sig.trial'][i]) for i in range(len(f['sig.tab']))}
            for e in range(len(a['sig.tab'])):
                if a['sig.tab'][e, ci['lam']] != lam:
                    continue
                ta = int(a['sig.trial'][e]); tf = frow[int(a['sig.tab'][e, ci['row']])]
                if ta < 0 or tf < 0:
                    continue
                n += 1
                for k in EQ:
                    eq[k] += int(np.array_equal(a[k][ta], f[k][tf]))
                for k in SD:
                    sd[k].append(float(f[k][tf]) - float(a[k][ta]))
        out[f'{spin}{m}_L{lam:g}'] = dict(n=n, equal={k: f'{v}/{n}' for k, v in eq.items()},
                                          signed={k: dict(mean=float(np.mean(v)), median=float(np.median(v)),
                                                          frac_pos=float(np.mean(np.array(v) > 0)))
                                                  for k, v in sd.items()})
        o = out[f'{spin}{m}_L{lam:g}']
        print(f'{spin}{m}_L{lam:g}', 'n', n, 'eq', list(o['equal'].values()),
              ' '.join(f"{k.split('.')[1]} {v['mean']:+.1f}/{v['frac_pos']:.2f}" for k, v in o['signed'].items()),
              flush=True)
    (TT / 'data/acts_stage4/investigation/inv_a2fc_e500_trials.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
