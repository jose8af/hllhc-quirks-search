"""R1: paired per-event ratio Ds_B / c06-model on the same MG events (bootstrap error of the median ratio)."""
import numpy as np, json
from pathlib import Path
TT = Path(__file__).resolve().parents[4]
S = np.load(TT/'data/sim_stage3/summary/events_p1.npz'); MG = np.load(TT/'data/sim_stage3/summary/p1_model_mg.npz')
keys = list(S['point_keys']); rng = np.random.default_rng(1)
P1 = json.load(open(TT/'sim/stage3/results/P1.json'))
for pk in ['F_m200','F_m500','F_m1000','F_m1500','S_m500']:
    line = pk
    for lam in (0.45,0.6,1,2,3,5,7,10):
        k = f'p1/{pk}/L{lam:g}_B'
        if k not in keys: continue
        sel = S['point']==keys.index(k); ok = (S['status'][sel]==1)&(S['ds_barrel_um'][sel]>0)
        rows = S['row'][sel][ok]; ds = S['ds_barrel_um'][sel][ok]
        s2 = (MG['point']==pk)&np.isclose(MG['lam'],lam); mp = dict(zip(MG['row'][s2].tolist(), MG['ds_model_um'][s2].tolist()))
        mo = np.array([mp.get(int(r),np.nan) for r in rows]); q = ds/mo; q=q[np.isfinite(q)]
        m = np.median(q); e = np.std([np.median(rng.choice(q,len(q))) for _ in range(400)])
        pull_unp = P1['points'][pk]['by_lambda'][f'L{lam:g}']['Ds_B']['pull_MG_model_um']
        line += f' | {lam:g}: {m:.3f}+-{e:.3f} ({(m-1)/e:+.1f}s; unpaired {pull_unp:+.1f})'
    print(line)
