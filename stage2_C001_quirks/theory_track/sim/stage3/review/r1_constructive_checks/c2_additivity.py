"""R1 constructive check 2: per-event additivity of B and MS thickness in P1 (same rows): ds_BM / sqrt(ds_B^2+ds_M^2)."""
import numpy as np
z = np.load('data/sim_stage3/summary/events_p1.npz', allow_pickle=False)
keys = z['point_keys']; pt = z['point']; row = z['row']; ds = z['ds_barrel_um']; st = z['status']
print(keys[:8])
def get(k):
    i = np.where(keys == k)[0]
    if len(i) == 0: return None
    m = (pt == i[0]) & (st == 1)
    return dict(zip(row[m], ds[m]))
rng = np.random.default_rng(1)
for sp in ['F_m200', 'F_m500', 'F_m1000', 'F_m1500', 'S_m500']:
    for L in ['0.45', '0.6', '1', '2', '3', '5']:
        B, M, BM = (get(f'p1/{sp}/L{L}_{c}') for c in ('B', 'M', 'BM'))
        if not (B and M and BM): continue
        rows = sorted(set(B) & set(M) & set(BM))
        r = np.array([BM[q] / np.hypot(B[q], M[q]) for q in rows])
        lin = np.array([BM[q] / (B[q] + M[q]) for q in rows])
        bs = [np.median(rng.choice(r, len(r))) for _ in range(300)]
        print(f'{sp:8s} L{L:5s} n={len(rows):3d} median BM/quad = {np.median(r):.3f} +- {np.std(bs):.3f}   median BM/lin = {np.median(lin):.3f}  ratio-of-medians quad = {np.median([BM[q] for q in rows])/np.hypot(np.median([B[q] for q in rows]), np.median([M[q] for q in rows])):.3f}')
