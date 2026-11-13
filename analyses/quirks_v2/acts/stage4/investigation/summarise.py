"""Summarise the re-runs: in-job eff_fckf at R04 (frac >= 0.5 of written quirk hits, f_CKF < 0.2) for base and variants,
paired with the production A2 in-job flag (Pinj) of the same rows."""
import json, glob, sys
import numpy as np
from acts.stage4.analysis import common as C
OUT = C.TT / 'data/acts_stage4/investigation'
res = {}
for m, lam in ((500, 3), (500, 5), (200, 5)):
    cmpf = json.load(open(OUT / f'cmp_p2_F_m{m}_L{lam}_BM.json'))
    A2 = cmpf['A2']; A1p = cmpf['A1']
    a1 = json.load(open(OUT / f'inv_A1_F{m}_L{lam}_central.json')) if (OUT / f'inv_A1_F{m}_L{lam}_central.json').exists() else []
    a5 = sum([json.load(open(f)) for f in sorted(glob.glob(str(OUT / f'inv_A5like_F{m}_L{lam}_c*.json'))) if not f.endswith('rows.json')], [])
    rows = [o['row'] for o in a5]
    d = dict(n_A1rerun=len(a1), n_A5like=len(a5))
    if a1:
        d['A1rerun_base'] = np.mean([o.get('eff_fckf_R04', False) for o in a1])
        for v in ('noCKFq', 'nomerge'):
            d[f'A1rerun_{v}'] = np.mean([o['variants'][v].get('eff_fckf_R04', False) for o in a1])
        d['A1prod_injob_same_rows'] = np.mean([A1p[str(o['row'])]['Pinj'] for o in a1])
        d['A2prod_injob_same_rows'] = np.mean([A2[str(o['row'])]['Pinj'] for o in a1])
    if a5:
        d['A5like_base'] = np.mean([o.get('eff_fckf_R04', False) for o in a5])
        d['A5like_noCKFq'] = np.mean([o['variants']['noCKFq'].get('eff_fckf_R04', False) for o in a5])
        d['A2prod_injob_A5rows'] = np.mean([A2[str(r)]['Pinj'] for r in rows])
        d['A2prod_analysis_A5rows'] = np.mean([A2[str(r)]['pass_'] for r in rows])
        d['A5like_ckf_q_frac_mean'] = np.mean([o['n_ckf_q'] / max(o['nqw'], 1) for o in a5])
        both = [(o.get('eff_fckf_R04', False), A2[str(o['row'])]['Pinj']) for o in a5]
        d['A5like_vs_A2_pairs(1,1|1,0|0,1|0,0)'] = [sum(1 for x in both if x == p) for p in ((True, True), (True, False), (False, True), (False, False))]
    res[f'F{m}_L{lam}'] = d
    print(f'F{m} L{lam}', {k: (round(float(v), 3) if not isinstance(v, list) else v) for k, v in d.items()})
json.dump(res, open(OUT / 'rerun_summary.json', 'w'), indent=1, default=float)
