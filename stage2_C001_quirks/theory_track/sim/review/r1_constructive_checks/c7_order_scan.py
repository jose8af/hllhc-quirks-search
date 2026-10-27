"""R1-constructive check 7: systematic scan of file-order structure.  For every non-stitched physics npz: split the
w>0 rows into 12 equal consecutive blocks (~ the 6 shower splits x 2 halves per chunk); KS-like test of gamma*-1 of each block vs the rest,
and the z-score of the block mean of (gamma*-1).  Random order => z ~ N(0,1)."""
import numpy as np, glob, os
allz=[]; first=[]
for f in sorted(glob.glob('../data/sim/npz/*.npz')):
    b=os.path.basename(f)
    if any(s in b for s in ('TRGS','P-INC','T2compat')): continue
    c=np.load(f); w=c['w']; ok=w>0; g=(c['gamma_star']-1)[ok]
    n=len(g); K=12; blocks=np.array_split(np.arange(n),K)
    zs=[]
    for bl in blocks:
        rest=np.setdiff1d(np.arange(n),bl)
        z=(g[bl].mean()-g[rest].mean())/np.sqrt(g[bl].var()/len(bl)+g[rest].var()/len(rest))
        zs.append(z)
    zs=np.array(zs); allz+=list(zs); first.append(zs[0])
    print(f'{b:24s} n={n:6d} z(block0)={zs[0]:+5.2f} max|z|={np.abs(zs).max():4.2f} rms z={np.sqrt(np.mean(zs**2)):4.2f}')
allz=np.array(allz); first=np.array(first)
print(f'ALL blocks: N={len(allz)} rms z={np.sqrt(np.mean(allz**2)):.2f}  frac |z|>2: {np.mean(np.abs(allz)>2):.3f} (expect 0.046)')
print(f'block 0 only: N={len(first)} mean z={first.mean():+.2f} rms={np.sqrt(np.mean(first**2)):.2f}')
