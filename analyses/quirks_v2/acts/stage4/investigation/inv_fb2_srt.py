"""INV item 2: FB2 SR-T PU term with the A28 merge population restricted to populations WITHOUT an added cut of the
merged variable (read-only; frozen stats.py for B84 and the toys).  Corrected merged factor: p(R11 | R06 & BTL) = 0/M,
M = N_groups(R06 & BTL) (= the M of the frozen p(R09 | R06) and p(R08 | R06) factors of the same SR-T chain)."""
import json
import numpy as np
from acts.stage4.analysis import stats as ST

D = 'data/acts_stage4/analysis/C12_v1/'
bg = json.load(open(D + 'background.json')); bs = json.load(open(D + 'bsum_wp.json'))
lim = json.load(open(D + 'limits.json'))['points']
col = [r for r in bg['columns_T'] if r['column'] == 'FB2'][0]
mf = col['main_factors']
zb = [f for f in mf if f['zero_bound']][0]
M_R06 = [f for f in bg['columns_T'] if f['column'] == 'R09_p>1e-3'][0]['main_factors'][2]['M']
ratio = (1.14 / M_R06) / zb['used']
print('frozen merged factor', zb['label'], zb['N'], zb['M'], '-> corrected 0 /', M_R06, ' scale', ratio)
out = {}
for fbn in ('FB2&h>5&o>5', 'FB2e>1.3&h>5&o>5', 'FB2e>1.6&h>5&o>5', 'FB2e>2&h>5&o>5'):
    x = bs['ladder']['FB'][fbn]['T']
    terms = [dict(value=t['value'], comps=t['comps']) for t in x['terms']]
    b84_0, med_0, _ = ST.b84(terms, nmc=100_000)
    t2 = [dict(t) for t in terms]
    for t, raw in zip(t2, x['terms']):
        if raw['label'].startswith('PU-SRT') and 'present x P(late)' in raw['label'] and 'not present' not in raw['label']:
            t['value'] = raw['value'] * ratio
    b84_1, med_1, _ = ST.b84(t2, nmc=100_000)
    g = bs['ladder']['FB'][fbn]['G']
    out[fbn] = dict(B84_T_frozen=x['B84'], B84_T_reproduced=b84_0, Bmed_T_frozen=x['B_median'], Bmed_T_reproduced=med_0,
                    B84_T_fixed=b84_1, Bmed_T_fixed=med_1, B84_G=g['B84'], Bmed_G=g['B_median'])
    print(fbn, {k: f'{v:.3g}' for k, v in out[fbn].items()})
for key in ('A2|F|200|1.5|BM', 'A2|F|500|2|BM', 'A2|S|500|3|BM'):
    p = lim[key]; s = p['s']; b = list(p['b']); sg = list(p['sigma_ln'])
    o = out['FB2&h>5&o>5']
    b[0] = o['Bmed_T_fixed']; sg[0] = float(np.log(o['B84_T_fixed'] / o['Bmed_T_fixed']))
    t = ST.expected_limit_toys(s, b, [{}, {}], sg)
    out[key] = dict(s=s, b_frozen=p['b'], sg_frozen=p['sigma_ln'], b_fixed=b, sg_fixed=sg,
                    mu95_toys_frozen=p['expected_toys']['median'], mu95_toys_fixed=t['median'], band1s_fixed=t['band_1s'])
    print(key, 'mu95 toys frozen %.3g -> fixed %.3g' % (p['expected_toys']['median'], t['median']))
json.dump(out, open('data/acts_stage4/investigation/inv_fb2_srt.json', 'w'), indent=1)
