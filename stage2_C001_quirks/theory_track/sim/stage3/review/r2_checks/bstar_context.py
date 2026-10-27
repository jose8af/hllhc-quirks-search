"""R2: (i) full-production 5 keV median r/c_ev per k_B bin for E500+E1000 only (the B*-off sample's population);
(ii) paired difference-of-medians on-off for k_B>=6 and k_B<4 combined, with paired bootstrap."""
import json, numpy as np
from pathlib import Path
TT = Path('/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track')
S = np.load(TT/'data/sim_stage3/summary/events_p1.npz'); keys = list(S['point_keys'])
rng = np.random.default_rng(7)
def bm(x, nb=1000):
    x = np.asarray(x); return np.median(x), np.std([np.median(rng.choice(x, len(x))) for _ in range(nb)])
R, K = [], []
for pk in ('F_m500', 'F_m1000'):
    def get(cfg):
        sel = S['point'] == keys.index(f'p1/{pk}/L5_{cfg}'); o = np.argsort(S['ev_index'][sel], kind='stable')
        return {c: S[c][sel][o] for c in ('ds_barrel_um', 'status', 'c_ev', 'k_B')}
    b, h = get('B'), get('B2'); ok = (b['status'] == 1) & (h['status'] == 1) & (b['ds_barrel_um'] > 0)
    c2 = (2*h['ds_barrel_um']/b['ds_barrel_um'] - 1)/np.log(2)
    R.append(((c2 - b['c_ev'])/b['c_ev'])[ok]); K.append(b['k_B'][ok])
R = np.concatenate(R); K = np.concatenate(K)
for a, bb in ((0, 2), (2, 4), (0, 4), (4, 6), (6, 10), (10, 1e9), (6, 1e9), (0, 1e9)):
    s = (K >= a) & (K < bb); m, e = bm(R[s]); print(f'prod E500+E1000 kB[{a},{bb:g}) n={s.sum()} {100*m:+.1f}+-{100*e:.1f} %')
d = json.load(open(TT/'sim/stage3/results/FIX_bstar_off.json'))
ev = [e for e in d['events'] if e['random']]
for a, bb in ((0, 4), (6, 1e9), (0, 1e9)):
    s = [e for e in ev if a <= e['k_B'] < bb]
    on = np.array([(e['c_on']-e['c_ev'])/e['c_ev'] for e in s]); off = np.array([(e['c_off']-e['c_ev'])/e['c_ev'] for e in s])
    n = len(s); bs = [np.median(on[i])-np.median(off[i]) for i in (rng.integers(0, n, n) for _ in range(2000))]
    dm = np.median(on)-np.median(off); print(f'paired diff of medians kB[{a},{bb:g}) n={n}: {100*dm:+.1f}+-{100*np.std(bs):.1f} % ({dm/np.std(bs):.1f} sigma); frac(on>off)={np.mean(on>off):.2f}')
