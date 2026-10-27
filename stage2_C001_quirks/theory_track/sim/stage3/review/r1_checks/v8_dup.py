"""R1: for the 4 V8 production files (first 10 events), count SimHits that share (event, quirk, surface) with an earlier
hit (repeated crossings) and hits sharing (event, surface) across quirks, vs the missing ACTS measurements."""
import numpy as np, json
from pathlib import Path
TT = Path(__file__).resolve().parents[4]; D = TT/'data/sim_stage3'
V8 = json.load(open(TT/'sim/stage3/results/V8_production.json'))['runs']
for f, r in V8.items():
    z = np.load(D/f); o = z['hit_offsets']; n = 10
    s = slice(0, o[n]); hq = z['h_quirk'][s].astype(np.int64); hs = z['h_surf'][s].astype(np.int64); ev = np.repeat(np.arange(n), np.diff(o[:n+1]))
    kinds = z['surf_kinds'][hs]
    key = ev*100000 + hq*10000 + hs
    _, cnt = np.unique(key, return_counts=True); rep_same_q = int((cnt - 1).sum())
    key2 = ev*100000 + hs; _, c2 = np.unique(key2, return_counts=True); rep_any = int((c2 - 1).sum())
    ic = z['h_icross'][s]
    print(f, 'simhits', len(hs), 'meas', r['n_measurements'], 'missing', len(hs)-r['n_measurements'],
          '| repeated (ev,q,surf):', rep_same_q, ' repeated (ev,surf) any quirk:', rep_any, ' h_icross>0:', int((ic > 0).sum()))
print('cross-quirk same-surface hit pairs closer than d (um), first 10 events:')
for f, r in V8.items():
    z = np.load(D/f); o = z['hit_offsets']; out = {}
    for thr in (10, 30, 100, 300):
        nclose = 0
        for e in range(10):
            s = slice(o[e], o[e+1]); hq = z['h_quirk'][s]; hs = z['h_surf'][s]
            X = np.stack([z['h_x'][s], z['h_y'][s], z['h_z'][s]], 1)
            for sf in np.unique(hs):
                a = X[(hs == sf) & (hq == 0)]; b = X[(hs == sf) & (hq == 1)]
                if len(a) and len(b):
                    d = np.sqrt(((a[:, None] - b[None]) ** 2).sum(-1)) * 1e3
                    nclose += int((d.min(1) < thr).sum())
        out[thr] = nclose
    print(f, 'missing', len(z['h_surf'][:o[10]]) - r['n_measurements'], 'close pairs', out)
