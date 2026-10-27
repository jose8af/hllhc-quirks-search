"""R1 constructive check 7: paired per-event test of the MG rotating-yo-yo model (P-9): median over events of
ds_B(meas)/ds_B(model) with bootstrap error, all / floor-flagged / unflagged. Compare with the unpaired README pulls."""
import numpy as np
z = np.load('data/sim_stage3/summary/events_p1.npz', allow_pickle=False)
mz = np.load('data/sim_stage3/summary/p1_model_mg.npz', allow_pickle=False)
print('model note:', str(mz['note'])[:300])
keys = z['point_keys']; pt = z['point']; row = z['row']; ds = z['ds_barrel_um']; st = z['status']; ff = z['floor_flag']
mpt = mz['point']; mlam = mz['lam']; mrow = mz['row']; mds = mz['ds_model_um']
print('model point dtype/sample:', mpt[:2], mlam[:2])
rng = np.random.default_rng(3)
def boot(r):
    return np.std([np.median(rng.choice(r, len(r))) for _ in range(400)]) if len(r) > 5 else np.nan
for sp in ['F_m200', 'F_m500', 'F_m1000', 'F_m1500', 'S_m500']:
    for L in [0.45, 0.6, 1, 2, 3, 5, 7, 10]:
        k = f'p1/{sp}/L{L:g}_B'
        i = np.where(keys == k)[0]
        if not len(i): continue
        m = (pt == i[0]) & (st == 1)
        mm = (mpt == sp) & np.isclose(mlam, L)
        if not mm.any(): continue
        mod = dict(zip(mrow[mm], mds[mm]))
        rows = row[m]; sel = np.array([q in mod for q in rows])
        r = ds[m][sel] / np.array([mod[q] for q in rows[sel]]); f = ff[m][sel].astype(bool)
        bad = ~np.isfinite(r)
        if bad.any(): print(f"  {sp} L{L:g}: {bad.sum()} non-finite ratios (model={[mod[q] for q in rows[sel][bad]][:3]}, meas={ds[m][sel][bad][:3]}) dropped")
        r, f = r[~bad], f[~bad]
        out = f'{sp:8s} L{L:<5g} n={len(r):3d} paired median ratio = {np.median(r):.4f} +- {boot(r):.4f}'
        if f.sum() >= 10:
            out += f' | unflagged {np.median(r[~f]):.4f} +- {boot(r[~f]):.4f} (n={(~f).sum()}) | flagged {np.median(r[f]):.4f} +- {boot(r[f]):.4f} (n={f.sum()})'
        print(out)
