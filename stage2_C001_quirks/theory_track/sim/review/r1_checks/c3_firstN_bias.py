"""R1 check 3: what does a Stage-3 user get from iter_events(sample='trig') 'first N' (unweighted) vs the weighted TRGS?
Tail selection pT(QQ)>200, |eta|<2.5.  Observables: median pT(QQ), median 2(g*-1), median N_osc (1 keV), median lead-jet pT,
fraction with pT>300 among pT>200, fraction with 0 jets>20 GeV within |eta|<2.5 ... (MET-plane proxies)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mg_events import iter_events, sample_file, load
SIG = 50.68
def nosc(g, bg, eta, m):
    D = 2 * m * np.sqrt(g**2 - 1) * bg / SIG; th = 2 * np.arctan(np.exp(-eta))
    s = np.minimum(110 / np.abs(np.sin(th)), 270 / np.abs(np.cos(th))); return s / D / 2
def wmed(v, w):
    i = np.argsort(v); c = np.cumsum(w[i]); c /= c[-1]; return v[i][np.searchsorted(c, 0.5)]
for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('S', 500)):
    c = load(sample_file(m, 'trig', spin))
    sel = (c['w'] > 0) & (c['pt_pair'] > 200) & (np.abs(c['eta_pair']) < 2.5)
    obs = dict(pt=c['pt_pair'], x=2 * (c['gamma_star'] - 1), nosc=nosc(c['gamma_star'], c['bg_pair'], c['eta_pair'], m),
               j1=c['jets'][:, 0, 0], f300=(c['pt_pair'] > 300).astype(float))
    out = []
    for N in (2000, 10000):
        ev = list(iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200))[:N]
        idx = np.array([e[2]['idx'] for e in ev])
        for k, v in obs.items():
            full = wmed(v[sel], c['w'][sel]) if k != 'f300' else np.average(v[sel], weights=c['w'][sel])
            fN = np.median(v[idx]) if k != 'f300' else v[idx].mean()
            out.append(f'N={N} {k}: firstN-unweighted {fN:.4g} vs TRGS-weighted {full:.4g} ({100*(fN/full-1):+.1f}%)')
    print(spin, m); [print('   ', o) for o in out]
