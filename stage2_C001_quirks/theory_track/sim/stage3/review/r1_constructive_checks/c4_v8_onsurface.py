"""R1 constructive check 4: V8 hypothesis. Distance of each hit from its nominal surface (|r-R| cylinders, |z-z0| discs)
in the 4 V8 production files (first 10 events), vs the ACTS default on-surface tolerance 1e-4 mm (0.1 um).
Measurement deficit in V8_production.json: 0/491, 7/470, 30/472, 73/448."""
import numpy as np
D = 'data/sim_stage3/'
files = ['out/p2/F_m1000/L1_BM_c00.npz', 'out/p2/F_m1000/L10_BM_c00.npz', 'out_pc/p2/F_m1000/L15_BM_c00.npz', 'out_pc/p2/F_m1000/L30_BM_c00.npz']
for f in files:
    z = np.load(D + f, allow_pickle=False)
    off = z['hit_offsets']; n = int(off[10]); S = z['surf_table']
    sid = z['h_surf'][:n].astype(int); x, y, zz = z['h_x'][:n], z['h_y'][:n], z['h_z'][:n]
    ty = S[sid, 0]
    d = np.where(ty < 0.5, np.abs(np.hypot(x, y) - S[sid, 1] * 10.0), np.abs(zz - S[sid, 1] * 10.0))  # mm
    kinds = np.array([str(k) for k in z['surf_kinds']])[sid]
    mb = float(z['max_boost'])
    print(f"{f:36s} max_boost={mb:g} n={n} max|d|={d.max()*1e3:.3g} um  n(d>0.1um)={(d>1e-4).sum()}  n(d>0.01um)={(d>1e-5).sum()}  "
          f"n(d>1e-4mm, T3V)={((d>1e-4)&(kinds=='T3V')).sum()}  n(icross>0)={(z['h_icross'][:n]>0).sum()}")
