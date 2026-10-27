"""R1-constructive check 6: is the event order in the npz files random?  Blocks of 2000 tail events: n_me mix, median
gamma*-1, mean pT, and the subprocess (initial-state) proxy p_qq_hard pz sign; plus bootstrap error of a 2000-event median."""
import numpy as np
rng=np.random.default_rng(42)
for f in ('E-TRGS_m1000','E-TRGS_m500','E-TRG_m700','E-INC_m500'):
    c=np.load(f'../data/sim/npz/{f}.npz'); w=c['w']; t=(w>0)&(c['pt_pair']>200)&(np.abs(c['eta_pair'])<2.5)
    ids=np.where(t)[0]; g=c['gamma_star']-1
    print('==',f,'tail N',len(ids))
    B=2000 if len(ids)>8000 else 1000
    for k in range(0,len(ids),B):
        b=ids[k:k+B]
        if len(b)<B//2: continue
        print(f'  block {k//B}: rows {b[0]}-{b[-1]}  med g-1 {np.median(g[b]):.4f}  n_me=0/1/2 {[round(np.mean(c["n_me"][b]==j),3) for j in (0,1,2)]}  med pT {np.median(c["pt_pair"][b]):.0f}  med |y| {np.median(np.abs(c["y_pair"][b])):.3f}')
    bs=[np.median(g[rng.choice(ids,B)]) for _ in range(300)]
    print(f'  bootstrap sd of a {B}-event median: {np.std(bs):.4f}')
