"""INV item 5 side finding: WP_RULE §7 'low gun counts' (looper: 0/500 C'_PU at R01 -> depth from C'0 factors,
0/100000) -- effect on B84 at the deep rungs (read-only; frozen stats.py)."""
import json
from acts.stage4.analysis import stats as ST
bs = json.load(open('data/acts_stage4/analysis/C12_v1/bsum_wp.json'))
sc = 500 / 100000
out = {}
for name, x in [('R08 G', bs['ladder']['G'][7]), ('R09 G', bs['ladder']['G'][8]), ('R09 T', bs['ladder']['T'][8]),
                ('FB3 G', bs['ladder']['FB']['FB3&h>5&o>5']['G']), ('FB4 G', bs['ladder']['FB']['FB4&h>5&o>5']['G'])]:
    t = [dict(value=v['value'] * (sc if v['label'] == "C' looper" else 1.0), comps=v['comps']) for v in x['terms']]
    b84 = ST.b84(t, nmc=100_000)[0]
    out[name] = dict(B84_frozen=x['B84'], B84_looper_from_C0=b84)
    print(name, '%.3g -> %.3g' % (x['B84'], b84))
json.dump(out, open('data/acts_stage4/investigation/inv_looper.json', 'w'), indent=1)
