"""R2 c4: spot-check (a) V-MERGE-20/50 shift of the tail median of x = 2(gamma*-1) vs E-INC 500 (the dominant ±4.6 % of the
l_max budget) and (b) the V-INTERP 550 GeV closure (sigma_matched, f(pT>200), tail median x, inclusive median gamma*-1),
with bootstrap errors.  Own code."""
import json
import numpy as np
D = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/data/sim/npz'
SIM = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim'
L = lambda n: dict(np.load(f'{D}/{n}.npz'))
rng = np.random.default_rng(5)

def wmed(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); return float(x[i][np.searchsorted(c, c[-1] / 2)])

def tailx(c):
    s = (c['w'] > 0) & (c['pt_pair'] > 200) & (np.abs(c['eta_pair']) < 2.5)
    x = 2 * (c['gamma_star'][s] - 1); w = c['w'][s]
    med = wmed(x, w)
    bs = [wmed(x[ix], w[ix]) for ix in (rng.integers(0, len(x), len(x)) for _ in range(200))]
    return med, np.std(bs) / med, len(x)

ref = tailx(L('E-INC_m500'))
for v in ('V-MERGE-20', 'V-MERGE-50'):
    t = tailx(L(f'{v}_m500'))
    print(f'{v}: x_med {t[0]:.4f} (N={t[2]}) vs E-INC500 {ref[0]:.4f} (N={ref[2]}): {100*(t[0]/ref[0]-1):+.2f} ± {100*np.hypot(t[1], ref[1]):.2f} %')

# V-INTERP
I = L('V-INTERP_m550'); i5, i6 = L('E-INC_m500'), L('E-INC_m600'); t5, t6 = L('E-TRGS_m500'), L('E-TRGS_m600')
s550, s5, s6 = I['w'].sum(), i5['w'].sum(), i6['w'].sum()
sint = np.exp(0.5 * (np.log(s5) + np.log(s6)))
f550 = I['w'][I['pt_pair'] > 200].sum() / s550
f5 = t5['w'][t5['pt_pair'] > 200].sum() / s5; f6 = t6['w'][t6['pt_pair'] > 200].sum() / s6
x550, ex550, n550 = tailx(I); x5, ex5, _ = tailx(t5); x6, ex6, _ = tailx(t6)
xi = 0.5 * (x5 + x6); exi = 0.5 * np.hypot(ex5 * x5, ex6 * x6) / xi
def incl(c):
    s = c['w'] > 0; return wmed(c['gamma_star'][s] - 1, c['w'][s])
g550, g5, g6 = incl(I), incl(i5), incl(i6)
J = json.load(open(f'{SIM}/results/interp.json'))['points']['F_550']
print(f'sigma: {s550:.4f} vs loglin {sint:.4f}: {100*(s550/sint-1):+.2f} %   json {100*J["sigma_matched_fb"]["rel"]:+.2f}')
print(f'f200: {f550:.4f} vs lin {0.5*(f5+f6):.4f}: {100*(f550/(0.5*(f5+f6))-1):+.2f} %   json {100*J["f_pt200"]["rel"]:+.2f}')
print(f'x tail median: {x550:.4f} (N={n550}) vs lin {xi:.4f}: {100*(x550/xi-1):+.2f} ± {100*np.hypot(ex550, exi):.2f} %   json {100*J["x_tail"]["rel"]:+.2f} ± {100*J["x_tail"]["err"]:.2f}')
print(f'incl gamma*-1 median: {g550:.4f} vs lin {0.5*(g5+g6):.4f}: {100*(g550/(0.5*(g5+g6))-1):+.2f} %')
