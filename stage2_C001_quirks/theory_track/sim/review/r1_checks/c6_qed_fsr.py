"""R1 check 6: m(QQ) before (Pythia status 23 = LHE) vs after shower: any sign of QED FSR off the quirks?"""
import os, numpy as np
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data', 'sim', 'npz')
mi = lambda P: np.sqrt(np.maximum(P[:, 0]**2 - (P[:, 1:]**2).sum(1), 0))
for n in ('E-LOPS_m500', 'E-LOPS_m1000', 'E-INC_m1000', 'S-LOPS_m500'):
    c = dict(np.load(os.path.join(D, n + '.npz'), allow_pickle=False))
    d = mi(c['p_qq_hard']) - c['m_pair']; r = d / c['m_pair']
    print(f"{n}: dM=M_hard-M_shower: mean {d.mean():.3g} GeV, q(1,50,99,99.9)={np.round(np.percentile(d,[1,50,99,99.9]),4)}, "
          f"frac dM>0.1 GeV={np.mean(d>0.1):.2e}, frac dM<-0.1 GeV={np.mean(d<-0.1):.2e}, max|dM/M|={np.abs(r).max():.2e}")
