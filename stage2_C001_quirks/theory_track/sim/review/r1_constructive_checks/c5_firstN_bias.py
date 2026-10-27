"""R1-constructive check 5: bias of the documented Stage-3 pattern 'iter_events(sample=trig, ptmin=200, eta_max=2.5),
take the first N, treat as unweighted' vs the weighted full TRGS tail.  Observable: median (gamma*-1) (prop. to l_max at
fixed m, Lambda) and fraction with gamma*-1 < 0.1 (short-arc tail relevant to the high-Lambda edge)."""
import numpy as np
def wq(x,w,q=0.5):
    i=np.argsort(x); cw=np.cumsum(w[i]); return x[i][np.searchsorted(cw,q*cw[-1])]
print(f"{'point':10s} {'N':>5s} {'med(all,w)':>10s} {'med(firstN)':>11s} {'bias%':>6s} {'f<0.1 all':>9s} {'f<0.1 firstN':>12s}")
for pre in ('E','S'):
    for m in (200,500,800,1000,1200,1500):
        try: c=np.load(f'../data/sim/npz/{pre}-TRGS_m{m}.npz')
        except FileNotFoundError: continue
        w=c['w']; t=(w>0)&(c['pt_pair']>200)&(np.abs(c['eta_pair'])<2.5); g=c['gamma_star']-1
        ids=np.where(t)[0]; ma=wq(g[t],w[t]); fa=w[t&(g<0.1)].sum()/w[t].sum()
        for N in (200,2000,len(ids)):
            first=ids[:N]; mf=np.median(g[first]); ff=np.mean(g[first]<0.1)
            if N==len(ids) or N==2000: print(f"{pre}{m:<5d} N={N:<6d} {ma:10.4f} {mf:11.4f} {100*(mf/ma-1):6.2f} {fa:9.4f} {ff:12.4f}")
