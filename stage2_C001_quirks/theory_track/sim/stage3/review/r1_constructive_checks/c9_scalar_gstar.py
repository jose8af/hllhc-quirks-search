"""R1 constructive check 9: is the scalar (S_m500) paired model deficit a gamma* composition effect?
Median ds_B(meas)/ds_B(model) in gamma* bins, F_m500 vs S_m500, pooled over Lambda = 1, 2, 3, 5 keV."""
import numpy as np
z = np.load('data/sim_stage3/summary/events_p1.npz', allow_pickle=False)
mz = np.load('data/sim_stage3/summary/p1_model_mg.npz', allow_pickle=False)
keys = z['point_keys']; pt = z['point']; row = z['row']; ds = z['ds_barrel_um']; st = z['status']; g = z['gstar']
bins = [1.0, 1.05, 1.15, 1.3, 1.6, 10]
rng = np.random.default_rng(5)
for sp in ('F_m500', 'S_m500', 'F_m1000'):
    R, G = [], []
    for L in (1, 2, 3, 5):
        i = np.where(keys == f'p1/{sp}/L{L}_B')[0][0]; m = (pt == i) & (st == 1)
        mm = (mz['point'] == sp) & np.isclose(mz['lam'], L); mod = dict(zip(mz['row'][mm], mz['ds_model_um'][mm]))
        for q, d_, gg in zip(row[m], ds[m], g[m]):
            if q in mod and mod[q] > 0: R.append(d_ / mod[q]); G.append(gg)
    R, G = np.array(R), np.array(G)
    out = []
    for a, b in zip(bins[:-1], bins[1:]):
        s = (G >= a) & (G < b)
        if s.sum() < 10: out.append(f'[{a},{b}): n={s.sum()}'); continue
        e = np.std([np.median(rng.choice(R[s], s.sum())) for _ in range(300)])
        out.append(f'[{a},{b}): {np.median(R[s]):.3f}+-{e:.3f} (n={s.sum()})')
    print(f'{sp}: median gamma* = {np.median(G):.3f}; ' + ' | '.join(out))
