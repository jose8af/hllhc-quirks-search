"""R2 check: recompute B*-on/off bins from the raw npz (data/sim_stage3/fix_r1/bstar) independently of fix_bstar_off.analyse.
Event metadata (k_B, c_ev, eps, production ds) re-read from summary/events_p1.npz by row."""
import json, numpy as np
from pathlib import Path
TT = Path('/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track')
RAW = TT/'data/sim_stage3/fix_r1/bstar'
S = np.load(TT/'data/sim_stage3/summary/events_p1.npz'); keys = list(S['point_keys'])
J = json.load(open(TT/'sim/stage3/results/FIX_bstar_off.json'))
rand = {(e['point'], e['row']): e['random'] for e in J['events']}
c5 = {(e['point'], e['row']): e['c5kev'] for e in J['events']}
U = 2.2e-16
rng = np.random.default_rng(11)
def bm(x, nb=2000):
    x = np.asarray(x); return np.median(x), np.std([np.median(rng.choice(x, len(x))) for _ in range(nb)])
rows = []
for pk in ('F_m500', 'F_m1000'):
    def get(cfg):
        sel = S['point'] == keys.index(f'p1/{pk}/L5_{cfg}')
        return {c: S[c][sel] for c in ('row', 'ds_barrel_um', 'status', 'c_ev', 'k_B', 'eps_perp')}
    b, h = get('B'), get('B2')
    hrow = {int(r): i for i, r in enumerate(h['row'])}
    for fn in sorted(RAW.glob(f'{pk}_r*.npz')):
        row = int(fn.stem.split('_r')[1]); d = np.load(fn)
        i = int(np.where(b['row'] == row)[0][0]); j = hrow[row]
        st = all(int(d[f'{a}_{c}_st']) == 1 for a in ('on', 'off') for c in ('B', 'B2'))
        cf = lambda a: (2*float(d[f'{a}_B2_ds'])/float(d[f'{a}_B_ds']) - 1)/np.log(2)
        cprod = (2*h['ds_barrel_um'][j]/b['ds_barrel_um'][i] - 1)/np.log(2)
        rows.append(dict(pk=pk, row=row, kB=b['k_B'][i], ce=b['c_ev'][i], eps=b['eps_perp'][i], on=cf('on'), off=cf('off'), prod=cprod,
                         st=st, rand=rand[(pk, row)], c5=c5[(pk, row)]))
print('n files', len(rows), 'all status ok', all(r['st'] for r in rows))
R = [r for r in rows if r['rand']]
for a, bb in ((0, 2), (2, 4), (0, 4), (4, 6), (6, 10), (10, 1e9), (0, 1e9)):
    s = [r for r in R if a <= r['kB'] < bb]
    f = lambda k: bm([(r[k]-r['ce'])/r['ce'] for r in s])
    on, off, pr = f('on'), f('off'), f('prod')
    d = np.array([(r['on']-r['off'])/r['ce'] for r in s])
    idx = [rng.integers(0, len(s), len(s)) for _ in range(2000)]
    eps = np.array([r['eps'] for r in s]); ce = np.median([r['ce'] for r in s])
    fl = [np.median(1.06*3*A*U/eps**2/np.log(2))/ce for A in (1.9, 5.0)]
    print(f'kB[{a},{bb:g}) n={len(s)} prod {100*pr[0]:+.1f}+-{100*pr[1]:.1f}  on {100*on[0]:+.1f}+-{100*on[1]:.1f}  off {100*off[0]:+.1f}+-{100*off[1]:.1f}'
          f'  med(on-off) {100*np.median(d):+.1f}+-{100*np.std([np.median(d[i]) for i in idx]):.1f}  floor(subsample eps) {100*fl[0]:.1f}-{100*fl[1]:.1f} %'
          f'  n|c_on-c_prod|>0.01: {sum(abs(r["on"]-r["prod"])>0.01 for r in s)}')
