"""R2 c7: N_eff / expected-signal ratios of VALIDATION §1.2 (B-4) from the files, via the loader's sigma_norm_fb."""
import sys
import numpy as np
sys.path.insert(0, '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/scripts')
import mg_events as M
for m in (200, 300, 400, 500, 600, 1000, 1500):
    c = M.load(M.sample_file(m, 'trig', 'F'))
    s = (c['w'] > 0) & (c['pt_pair'] > 200) & (np.abs(c['eta_pair']) < 2.5)
    w = c['w'][s]; neff = w.sum() ** 2 / (w ** 2).sum()
    N = 3000 * M.sigma_norm_fb(m, 'trig', 'F', eta_max=2.5, ptmin=200)
    print(f'm={m}: N_eff={neff:.0f}  N(3/ab, pT>200, |eta|<2.5)={N:.4g}  N_eff/N={neff/N:.2f}  N_eff/(0.18 N)={neff/(0.18*N):.2f}')
