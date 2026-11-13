"""INV item 5: zero-count bounds of the SM and C' terms -- one bound per term, its M and population, and the sample
size needed (zero persisting, bound ~ 1/N_sample) to bring each term / the bounded sum below the 0.11 budget.
Read-only; frozen stats.py for B84."""
import json, os
import numpy as np
from acts.stage4.analysis import stats as ST

TAG = os.environ.get('TAG', 'C12_v1')
D = f'data/acts_stage4/analysis/{TAG}/'
bg = json.load(open(D + 'background.json')); bs = json.load(open(D + 'bsum_wp.json'))
COLS = [r['column'] for r in bg['columns']]
sm, cp = bg['sm'], bg['cprime']
NS = {f'SM {s}': v['n_class_events'] for s, v in sm.items() if not s.startswith('_') and not v.get('proxy')}
for s, v in sm.items():
    if not s.startswith('_') and v.get('proxy'):
        NS[f'SM {s} [PROXY]'] = None
for t, v in cp.items():
    NS[f"C' {t}"] = v['n_with_pu']


def row_of(label, col):
    if label.startswith("C' "):
        return cp[label[3:]]['rows'][COLS.index(col)]
    s = label[3:].replace(' [PROXY]', '')
    r = sm[s]['rows'][COLS.index(col)]
    if sm[s].get('proxy'):
        src = r.get('proxy_of')
        return dict(sm[src]['rows'][COLS.index(col)], proxy_of=src) if src else r
    return r


out = {}
sel = [('R07', 'G', 'ladder', 6), ('R08', 'G', 'ladder', 7), ('R09', 'G', 'ladder', 8), ('R14', 'G', 'ladder', 13),
       ('FB3', 'G', 'FB', 'FB3&h>5&o>5'), ('FB4', 'G', 'FB', 'FB4&h>5&o>5')]
for name, c, kind, idx in sel:
    x = bs['ladder'][c][idx] if kind == 'ladder' else bs['ladder']['FB'][idx][c]
    col = COLS[idx] if kind == 'ladder' else idx.split('&')[0]
    terms = x['terms']
    rec = []
    for t in terms:
        if t['label'].startswith('PU'):
            continue
        r = row_of(t['label'], col)
        fs = r.get('factors') or []
        zb = [f for f in fs if f.get('zero_bound')]
        nz = [f for f in fs if f.get('N') == 0 and f.get('value') is None]
        b84t, medt, _ = ST.b84([dict(value=t['value'], comps=t['comps'])], nmc=100_000)
        k = b84t / 0.11
        src = r.get('proxy_of')
        Ns = NS[t['label']] if NS[t['label']] is not None else (sm[src]['n_class_events'] if src else None)
        rec.append(dict(label=t['label'], value=t['value'], B84_alone=b84t, n_zero_factors=len(nz), n_bounds=len(zb),
                        bound_label=zb[0]['label'] if zb else None, bound_M=zb[0]['M'] if zb else None,
                        bound_used=zb[0]['used'] if zb else None, proxy_of=src,
                        N_sample=Ns, k_needed_alone=(k if zb else None),
                        N_needed_alone=(k * Ns if zb and Ns else None)))
    # bounded-sum scaling: all zero-branch C'/SM terms scale 1/k, measured ones fixed, PU fixed
    pu = [dict(value=t['value'], comps=t['comps']) for t in terms if t['label'].startswith('PU')]
    bnd = [dict(value=t['value'], comps=t['comps']) for t, rr in zip([t for t in terms if not t['label'].startswith('PU')], rec)
           if rr['n_bounds']]
    meas = [dict(value=t['value'], comps=t['comps']) for t, rr in zip([t for t in terms if not t['label'].startswith('PU')], rec)
            if not rr['n_bounds']]
    b84_meas = ST.b84(meas, nmc=100_000)[0] if meas else 0.0
    b84_pu = ST.b84(pu, nmc=100_000)[0] if pu else 0.0

    def b84_scaled(k):
        return ST.b84([dict(v, value=v['value'] / k) for v in bnd], nmc=100_000)[0]
    lo, hi = 1.0, 1e14
    if b84_scaled(hi) > 0.11:
        kb = None
    else:
        for _ in range(60):
            mid = np.sqrt(lo * hi)
            lo, hi = (mid, hi) if b84_scaled(mid) > 0.11 else (lo, mid)
        kb = hi
    out[name] = dict(category=c, column=col, B84_total=x['B84'], B84_PU_only=b84_pu, B84_measured_nonPU=b84_meas,
                     k_bounded_sum=kb, terms=rec)
    print(f'== {name} ({col}, SR-{c}) B84 {x["B84"]:.3g} | PU alone {b84_pu:.3g} | measured (non-bound) SM/C\' alone '
          f'{b84_meas:.3g} | all bounded C\'/SM terms <= 0.11 needs x{kb:.3g} statistics' if kb else f'== {name}: none')
    for rr in sorted(rec, key=lambda r: -r['value'])[:9]:
        print('   %-22s B %.3g B84 %.3g zeros %d bound %s M=%s N_s=%s k=%s N_need=%s' % (
            rr['label'][:22], rr['value'], rr['B84_alone'], rr['n_zero_factors'], rr['n_bounds'],
            rr['bound_M'], rr['N_sample'], ('%.2g' % rr['k_needed_alone']) if rr['k_needed_alone'] else '-',
            ('%.2g' % rr['N_needed_alone']) if rr['N_needed_alone'] else '-'))
json.dump(out, open(f'data/acts_stage4/investigation/inv_zero_bounds_{TAG}.json', 'w'), indent=1)
