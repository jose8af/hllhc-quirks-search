"""R1 check 4: are events within the npz files (= MG LHE order) randomly ordered?  Compare blocks of 2000 consecutive
events (tail selection) for ME multiplicity mix and median 2(g*-1); a KS-style test of x vs file position."""
import os, numpy as np
from scipy.stats import ks_2samp, spearmanr
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data', 'sim', 'npz')
for n in ('E-TRG_m500', 'E-INC_m500', 'E-LOPS_m500', 'E-TRG_m1000', 'E-TRG_m1500'):
    c = dict(np.load(os.path.join(D, n + '.npz'), allow_pickle=False))
    sel = np.where((c['w'] > 0) & (c['pt_pair'] > 200) & (np.abs(c['eta_pair']) < 2.5))[0]
    if len(sel) < 4000:
        sel = np.where(c['w'] > 0)[0]
    x = 2 * (c['gamma_star'][sel] - 1); nme = c['n_me'][sel]
    B = 2000; nb = len(sel) // B
    meds = [np.median(x[i*B:(i+1)*B]) for i in range(nb)]
    f2 = [np.mean(nme[i*B:(i+1)*B] == 2) for i in range(nb)]
    rho, p = spearmanr(np.arange(len(x)), x)
    ks = ks_2samp(x[:B], x[B:]).pvalue
    print(f'{n}: {len(sel)} ev; block medians of 2(g*-1): {np.round(meds,3)}; frac n_me=2 per block: {np.round(f2,3)}; '
          f'Spearman(index, x) rho={rho:.3f} p={p:.2g}; KS(first {B} vs rest) p={ks:.2g}')
