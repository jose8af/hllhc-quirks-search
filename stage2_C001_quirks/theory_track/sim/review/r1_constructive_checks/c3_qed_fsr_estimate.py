"""R1-constructive check 3: soft-photon (eikonal, final-state dipole) estimate of P(E_gamma > Emin) off a heavy
opposite-charge pair, per event, using the sample's gamma*:  dP = (2 alpha/pi) [ (1+b^2)/(2b) ln((1+b)/(1-b)) - 1 ] dE/E,
b = beta* = sqrt(1-1/g*^2), the speed of each quirk in the pair CM (massless limit gives 2[ln(s/m^2)-1]; NOT the relative
v_rel = 2beta*/(1+beta*^2)); E from Emin to Emax = (sqrt(s_hat) - 2m) (kinematic limit, generous).  Leading-log only."""
import numpy as np
a=1/137.036
for f,m in [('E-LOPS_m200',200),('E-LOPS_m500',500),('E-LOPS_m1000',1000),('E-TRGS_m200',200)]:
    c=np.load('../data/sim/npz/'+f+'.npz'); w=c['w']; g=c['gamma_star']
    sel=w>0
    if 'TRGS' in f: sel&=(c['pt_pair']>200)
    b=np.sqrt(1-1/g[sel]**2)
    R=(1+b**2)/(2*b)*np.log((1+b)/(1-b))-1
    emax=np.maximum(2*m*(g[sel]-1),1e-9)
    for emin in (5.,20.):
        L=np.clip(np.log(emax/emin),0,None)
        P=np.clip(2*a/np.pi*R*L,0,1)
        print(f'{f:14s} Emin={emin:4.0f} GeV: <P> = {np.average(P,weights=w[sel]):.4f}  (median g*-1 {np.median(g[sel]-1):.3f})')
