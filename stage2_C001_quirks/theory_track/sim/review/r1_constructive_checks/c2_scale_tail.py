"""R1-constructive check 2: does the 9-point (muR, muF) weight set vary the ISR tail? (alpha_s of emissions)"""
import numpy as np
D='../data/sim/npz/'
for f in ['E-INC_m500','E-TRGS_m500','E-TRGS_m1000','E-TRGS_m200']:
    c=np.load(D+f+'.npz'); w=c['w']; W=c['wvar']; n=[str(x) for x in c['wvar_names']]
    tail=(c['pt_pair']>200)&(np.abs(c['eta_pair'])<2.5)
    print('==',f)
    for muf in ('0.5','1.0','2.0'):
        row=[]
        for mur in ('0.5','1.0','2.0'):
            k=n.index(f'MUF={muf}_MUR={mur}_PDF=14400_MERGING=45.000'); x=W[:,k]
            row.append(f'muF{muf}/muR{mur}: incl {x.sum()/w.sum():.4f} tail {x[tail].sum()/w[tail].sum():.4f} f_tail {x[tail].sum()/x.sum():.4f}/{w[tail].sum()/w.sum():.4f}')
        print('  '+' | '.join(row))
    # per-event: is muR weight ratio ever != 1?
    k=n.index('MUF=1.0_MUR=2.0_PDF=14400_MERGING=45.000'); r=W[w>0,k]/w[w>0]
    print('  per-event muR=2 ratio: min %.4f max %.4f, frac |r-1|>1e-3: %.4f'%(r.min(),r.max(),np.mean(np.abs(r-1)>1e-3)))
    for nme in (0,1,2):
        s=(c['n_me']==nme)&(w>0)
        if s.any(): print(f'   n_me={nme}: mean muR=2 ratio {np.mean(W[s,k]/w[s]):.4f}')
