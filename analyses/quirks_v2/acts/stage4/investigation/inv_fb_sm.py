"""INV item 2b: the same A28 merge-population defect in the SM rows of FB0/FB1 (+e) -- recompute those rows with the
merged chi2_core joint tail on the START population (p(R11 | start) = N / M_start; N(start & R11) = N(start & R09 & R11)
because the p cuts are nested), rebuild the FB0/FB1 B sums (both categories, A12) and re-run the frozen toys for every
limit point whose fallback is FB0/FB1.  Optionally (--with-fb2) also applies the item-2 SR-T FB2 correction.
Read-only on frozen outputs; frozen stats.py for B84 and the toys.  ESTIMATE: exact numbers need the fixed pipeline."""
import json, os, sys
import numpy as np
from acts.stage4.analysis import stats as ST
from acts.stage4.analysis import background as BG

TAG = os.environ.get('TAG', 'C12_v1')
D = f'data/acts_stage4/analysis/{TAG}/'
bg = json.load(open(D + 'background.json')); bs = json.load(open(D + 'bsum_wp.json'))
lim = json.load(open(D + 'limits.json'))['points']
sm = bg['sm']
RUNG_COL = {n: i for i, n in enumerate([r['column'] for r in bg['columns']])}
fix = {}          # (sample, column) -> scale
for s, v in sm.items():
    if s.startswith('_') or v.get('proxy'):
        continue
    for r in v['rows']:
        fs = r['factors']
        mg = [f for f in fs if 'merged' in f['label'] and '& R09_p>1e-3)' in f['label'] and 'R11' in f['label']]
        if not mg:
            continue
        f = mg[0]
        start_lab = fs[0]['label']
        assert 'direct' in start_lab and ('R04' in start_lab or 'R05' in start_lab), start_lab
        ck = [x for x in fs if x['label'].startswith('f_CKF')][0]        # f_CKF is measured on the start population
        M_start = ck['M']
        T = BG.Term('fixed')                     # re-apply the frozen zero-count rule (WP_RULE §4.2) to the fixed chain
        for x in fs:
            if x is f:
                T.add(x['label'] + ' [FIXED: on start population]', x['N'], M_start, s_ln=x['s_ln'])
            else:
                T.add(x['label'], x['N'], x['M'], s_ln=x['s_ln'], value=x['value'])
        ev = T.evaluate()
        T0 = BG.Term('frozen check')
        for x in fs:
            T0.add(x['label'], x['N'], x['M'], s_ln=x['s_ln'], value=x['value'])
        assert abs(T0.evaluate()['value'] / r['P_per_event'] - 1) < 1e-9
        fix[(s, r['column'])] = dict(scale=ev['value'] / r['P_per_event'], N=f['N'], M_frozen=f['M'], M_start=M_start,
                                     P_frozen=r['P_per_event'], B_frozen=r['B'], s_ln_fixed=ev['s_ln'],
                                     s_ln_frozen=r['s_ln'])
print('SM rows affected:', len(fix))
for k, v in fix.items():
    if k[1] in ('FB0', 'FB1'):
        print('  ', k, 'N=%g M %g -> %g  scale %.3g  B %.3g -> %.3g' % (v['N'], v['M_frozen'], v['M_start'], v['scale'],
                                                                        v['B_frozen'], v['B_frozen'] * v['scale']))


def fixed_rows(col):
    """corrected B per SM label (incl. proxies: N_trig,p x max over sources of P/f_presel)."""
    out = {}; P = {}
    for s, v in sm.items():
        if s.startswith('_') or v.get('proxy'):
            continue
        r = v['rows'][RUNG_COL[col]]
        sc = fix.get((s, col), {}).get('scale', 1.0)
        out[f'SM {s}'] = (r['B'] or 0.0) * sc
        P[s] = r['P_per_event'] * sc / v['f_presel_class']
    for s, v in sm.items():
        if s.startswith('_') or not v.get('proxy'):
            continue
        srcs = [w for w in v['proxy_of'] if w in P]
        out[f'SM {s} [PROXY]'] = v['N_trig'] * max(P[w] for w in srcs)
    return out


with_fb2 = '--with-fb2' in sys.argv
fb2 = json.load(open('data/acts_stage4/investigation/inv_fb2_srt.json')) if with_fb2 else None
res = dict(rows={f'{k[0]}|{k[1]}': v for k, v in fix.items()}, fb={}, limits={})
newB = {}
for fbn, x in bs['ladder']['FB'].items():
    col = fbn.split('&')[0]
    rows = fixed_rows(col)
    newB[fbn] = {}
    for c in ('T', 'G'):
        terms = []; changed = False
        for t in x[c]['terms']:
            val = t['value']
            if t['label'] in rows:
                ratio = rows[t['label']] / val if val else 1.0
                if abs(ratio - 1) > 1e-9:
                    changed = True
                val = rows[t['label']]
            if with_fb2 and c == 'T' and col == 'FB2' and t['label'].startswith('PU-SRT') and \
                    'present x P(late)' in t['label'] and 'not present' not in t['label'] and TAG == 'C12_v1':
                val = t['value'] * 0.008537886872998933; changed = True
            terms.append(dict(value=val, comps=t['comps']))
        if changed:
            b84, med, _ = ST.b84(terms, nmc=100_000)
            newB[fbn][c] = dict(B84=b84, B_median=med)
            res['fb'].setdefault(fbn, {})[c] = dict(B84_frozen=x[c]['B84'], Bmed_frozen=x[c]['B_median'], B84_fixed=b84,
                                                    Bmed_fixed=med)
            print('%-18s %s  B84 %.3g -> %.3g   median %.3g -> %.3g' % (fbn, c, x[c]['B84'], b84, x[c]['B_median'], med))
for key, p in lim.items():
    if 'expected_toys' not in p:
        continue
    fbn = p['primary']['admissibility']['r_fb']
    if fbn not in newB or not newB[fbn]:
        continue
    b = list(p['b']); sg = list(p['sigma_ln'])
    for i, c in enumerate(('T', 'G')):
        if c in newB[fbn]:
            b[i] = newB[fbn][c]['B_median']; sg[i] = float(np.log(newB[fbn][c]['B84'] / newB[fbn][c]['B_median']))
    t = ST.expected_limit_toys(p['s'], b, [{}, {}], sg)
    res['limits'][key] = dict(r_fb=fbn, s=p['s'], b_frozen=p['b'], b_fixed=b, sg_frozen=p['sigma_ln'], sg_fixed=sg,
                              mu95_frozen=p['expected_toys']['median'], mu95_fixed=t['median'], band1s_fixed=t['band_1s'])
    print('%-18s %-6s mu95 toys %.3g -> %.3g' % (key, fbn[:3], p['expected_toys']['median'], t['median']))
json.dump(res, open(f'data/acts_stage4/investigation/inv_fb_sm_{TAG}{"_withfb2" if with_fb2 else ""}.json', 'w'), indent=1)
