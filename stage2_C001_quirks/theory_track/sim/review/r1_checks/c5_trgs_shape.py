"""R1 check 5: shape closure of the stitched TRGS vs INC in the tail (pT(QQ) 200-1000 GeV, 16 bins; and 2(g*-1) 0-3, 15 bins).
Absolute dsigma per bin (not normalised), chi2 with sum-w2 errors of both samples."""
import os, numpy as np
from scipy.stats import chi2 as C2
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data', 'sim', 'npz')
L = lambda n: dict(np.load(os.path.join(D, n + '.npz'), allow_pickle=False))
def h(v, w, b):
    a, _ = np.histogram(v, b, weights=w); e, _ = np.histogram(v, b, weights=w * w); return a, e
for pre in ('E', 'S'):
    for m in (200, 500, 1000):
        ci, cs, ct = L(f'{pre}-INC_m{m}'), L(f'{pre}-TRGS_m{m}'), L(f'{pre}-TRG_m{m}')
        out = []
        for name, f, b in (('pT', lambda c: c['pt_pair'], np.linspace(200, 1000, 17)),
                           ('x', lambda c: 2 * (c['gamma_star'] - 1), np.linspace(0, 3, 16))):
            for lab, cc in (('TRGS', cs), ('TRG', ct)):
                si = ci['pt_pair'] > 200; ss = cc['pt_pair'] > 200
                a, ea = h(f(ci)[si], ci['w'][si], b); s, es = h(f(cc)[ss], cc['w'][ss], b)
                ok = (ea + es) > 0
                chi = np.sum((a - s)[ok] ** 2 / (ea + es)[ok]); nd = ok.sum()
                out.append(f'{name} {lab}/INC chi2/ndf={chi:.1f}/{nd} p={C2.sf(chi, nd):.3f}')
        print(f'{pre}{m}: ' + '; '.join(out))
