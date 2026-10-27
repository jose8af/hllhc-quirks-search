"""R1-constructive check 1: weight bookkeeping in TRGS / INC / LOPS files."""
import numpy as np, re, sys
D='../data/sim/npz/'
for f in ['E-TRGS_m500','E-INC_m500','E-LOPS_m500','E-TRGS_m1500']:
    c=np.load(D+f+'.npz'); w=c['w']; W=c['wvar']; n=list(c['wvar_names'])
    print('==',f,'rows',len(w),'w<0',(w<0).sum(),'w==0',(w==0).sum(),'sum w',w.sum())
    def s(name): return W[:,n.index(name)].sum()
    for name in ['Weight','Weight_MERGING=45.000','Weight_MERGING=67.500','Weight_MERGING=90.000','AUX_1','AUX_2','AUX_50']:
        if name in n: print(f'  {name:28s} sum={s(name):.5g}  ratio to sum w={s(name)/w.sum():.4f}  nonzero where w==0: {(W[w==0,n.index(name)]!=0).sum()}')
    named=[x for x in n if x.startswith('MUF=')]
    print('  n named', len(named), 'n AUX', sum(x.startswith('AUX') for x in n))
    cen=[x for x in named if 'MUF=1.0_MUR=1.0_PDF=14400' in x]
    print('  central named:', cen[:6])
    for x in cen[:3]:
        print('   ', x, 'ratio', s(x)/w.sum(), 'max per-event |rel diff| to w (w>0):', np.max(np.abs(W[w>0,n.index(x)]/w[w>0]-1)))
    # scale envelope
    sc=[x for x in named if re.match(r'MUF=[0-9.]+_MUR=[0-9.]+_PDF=14400_MERGING=45.000$',x)]
    print('  9-pt names', len(sc), [round(s(x)/w.sum(),4) for x in sc])
    dyn=[x for x in named if 'DYN' in x]
    print('  dyn names', dyn[:8])
    if 'origin' in c.files:
        o=c['origin']; sel=(c['pt_pair']>200)&(np.abs(c['eta_pair'])<2.5)&(w>0)
        ws=w[sel]; neff=ws.sum()**2/(ws**2).sum()
        print(f'  TAIL: N={sel.sum()} Kish Neff={neff:.0f} ({neff/sel.sum():.3f}); sigma frac from INC part={w[sel&(o==1)].sum()/ws.sum():.4f}; event frac={((o==1)&sel).sum()/sel.sum():.4f}; w ratio INC/TRG={np.median(w[(o==1)&(w>0)])/np.median(w[(o==0)&(w>0)]):.2f}')
        idx=np.where(sel)[0]; first=idx[:2000]
        print('  first 200/2000 selected rows: INC-origin count', (o[idx[:200]]==1).sum(), (o[first]==1).sum(), '; first INC-origin selected position', np.argmax(o[idx]==1))
        g=c['gamma_star']-1
        def wmed(x,ww):
            i=np.argsort(x); cw=np.cumsum(ww[i]); return x[i][np.searchsorted(cw,cw[-1]/2)]
        print(f'  median gamma*-1: all {wmed(g[sel],w[sel]):.4f}  TRG-origin only (weighted) {wmed(g[sel&(o==0)],w[sel&(o==0)]):.4f}  INC-origin {wmed(g[sel&(o==1)],w[sel&(o==1)]):.4f}')
        print(f'  sum w all rows {w.sum():.5g} vs INC file sigma_matched (see SAMPLES)')
        print('  unique w values (TRG part, w>0):', np.unique(np.round(w[(o==0)&(w>0)],12))[:5], len(np.unique(np.round(w[(o==0)&(w>0)],12))))
