"""R2 c3: independent spot-check of (a) the ME-alps tail-rate shift at E 200 and E 500, (b) the V-SHOWER f(pT>200) shift,
(c) the quadrature total quoted (+12..+15 % / -11..-13 %), (d) the shape shift of the median of x = 2(gamma*-1).
Own code; reads only the npz + alps ratio files."""
import json
import numpy as np
D = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/data/sim'
SIM = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim'
L = lambda n: dict(np.load(f'{D}/npz/{n}.npz'))

def wmed(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); return float(x[i][np.searchsorted(c, c[-1] / 2)])

def ratio(c, pre, m, src, key):
    r = np.full(len(c['w']), np.nan)
    for k in np.unique(c['chunk']):
        for s in np.unique(src):
            sel = (c['chunk'] == k) & (src == s)
            if sel.any():
                a = np.load(f'{D}/aux/fixer/alps/{s}_m{m}_c{k}.npz')[key]
                r[sel] = a[c['ievt_lhe'][sel]]
    assert np.isfinite(r).all()
    return r

out = {}
sh = json.load(open(f'{SIM}/results/shower.json'))
for pre, spin, m in (('E', 'F', 200), ('E', 'F', 500), ('S', 'S', 1000)):
    ts, inc = L(f'{pre}-TRGS_m{m}'), L(f'{pre}-INC_m{m}')
    src_ts = np.where(ts['origin'] == 1, f'{pre}-INC', f'{pre}-TRG'); src_i = np.full(len(inc['w']), f'{pre}-INC')
    res = {}
    t200 = ts['pt_pair'] > 200; tail = t200 & (np.abs(ts['eta_pair']) < 2.5) & (ts['w'] > 0)
    x = 2 * (ts['gamma_star'] - 1)
    f0 = ts['w'][t200].sum() / inc['w'].sum(); x0 = wmed(x[tail], ts['w'][tail])
    for key in ('r_alps0p5', 'r_alps2'):
        rt = ratio(ts, pre, m, src_ts, key); ri = ratio(inc, pre, m, src_i, key)
        wt = ts['w'] * rt; wi = inc['w'] * ri
        f = wt[t200].sum() / wi.sum()
        res[key] = dict(f_rel=f / f0 - 1, x_rel=wmed(x[tail], wt[tail]) / x0 - 1, sigINC_rel=wi.sum() / inc['w'].sum() - 1)
        # sanity: n_me = 0 rows must have r = 1 (no emission alpha_s)
        res[key]['max|r-1|_nme0'] = float(np.max(np.abs(rt[ts['n_me'] == 0] - 1))) if (ts['n_me'] == 0).any() else None
        res[key]['mean_r_nme1'] = float(rt[ts['n_me'] == 1].mean()); res[key]['mean_r_nme2'] = float(rt[ts['n_me'] == 2].mean())
    j = sh['alps_and_scale9'][f'{spin}_{m}']
    res['json'] = dict(a05=j['alps0p5']['rel_to_nominal']['f200'], a2=j['alps2']['rel_to_nominal']['f200'],
                       x05=j['alps0p5']['rel_to_nominal']['x_median'], x2=j['alps2']['rel_to_nominal']['x_median'])
    out[f'{pre}{m}'] = res
    print(pre, m, {k: ({q: round(100 * v, 2) if isinstance(v, float) and 'r' not in q[:2] else v for q, v in r.items()} if isinstance(r, dict) else r) for k, r in res.items()}, flush=True)

# (b) V-SHOWER f(pT>200) from the raw files, own code
trg, inc = L('E-TRG_m500'), L('E-INC_m500')
def fTRGS(t, i, st=None, si=None, ft=1., fi=1.):
    st = np.ones(len(t['w']), bool) if st is None else st; si = np.ones(len(i['w']), bool) if si is None else si
    H = i['p_qq_hard']; comp = np.hypot(H[:, 1], H[:, 2]) < 100
    num = (t['w'][st & (t['pt_pair'] > 200)].sum() * ft + i['w'][si & comp & (i['pt_pair'] > 200)].sum() * fi)
    return num / (i['w'][si].sum() * fi)
ft = float(trg['nlhe']) / 50000; fi = float(inc['nlhe']) / 50000
fn = fTRGS(trg, inc, trg['chunk'] == 0, inc['chunk'] == 0, ft, fi)
vs = {}
for v in ('UP', 'DN'):
    vt, vi = L(f'V-SHOWER-{v}-TRG_m500'), L(f'V-SHOWER-{v}-INC_m500')
    vs[v] = fTRGS(vt, vi) / fn - 1
print('V-SHOWER f200 nominal(chunk0)', round(fn, 4), 'UP', round(100 * vs['UP'], 2), '% DN', round(100 * vs['DN'], 2), '%',
      'json', round(100 * sh['vshower_m500']['UP']['rel_to_nominal']['f200'], 2), round(100 * sh['vshower_m500']['DN']['rel_to_nominal']['f200'], 2))
# chunk-0 nominal: is TRG chunk-0 weight normalisation consistent? (TRG chunk 0 sigma vs full)
print('TRG chunk0 sum w * nlhe/50k vs full:', trg['w'][trg['chunk'] == 0].sum() * ft / trg['w'].sum() - 1,
      ' INC:', inc['w'][inc['chunk'] == 0].sum() * fi / inc['w'].sum() - 1)
# (c) quadrature
mer_up, mer_dn, shw = 0.037, -0.055, max(abs(vs['UP']), abs(vs['DN']))
for k, r in out.items():
    up = np.sqrt(r['r_alps0p5']['f_rel'] ** 2 + mer_up ** 2 + shw ** 2); dn = np.sqrt(r['r_alps2']['f_rel'] ** 2 + mer_dn ** 2 + shw ** 2)
    print(k, 'total tail-rate', f'+{100*up:.1f} / -{100*dn:.1f} %')
