"""R2 c5: compare my re-shower of E-TRG m500 chunk 0 job 0 (review/r2_checks/repro_trg/r_s0.npz) with the delivered rows."""
import numpy as np
D = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/data/sim/npz'
c = np.load(f'{D}/E-TRG_m500.npz'); n = np.load('/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/review/r2_checks/repro_trg/r_s0.npz')
s = (c['chunk'] == 0) & (c["py8_job"] == 0)
print('rows delivered', s.sum(), 'reshowered', len(n['w']))
for col in ('p_qp', 'p_qm', 'p_qq_hard', 'recoil', 'recoil_eta5', 'nu', 'jets', 'njet', 'n_me', 'gamma_star', 'pt_pair', 'eta_pair', 'cstar', 'bg_pair', 'm_pair'):
    a, b = c[col][s], n[col]
    print(f'{col:12s} bitwise={np.array_equal(a, b)}  max|diff|={np.max(np.abs(a.astype(float)-b.astype(float))):.3g}')
wc, wn = c['w'][s], n['w']
print('w normalised max rel diff', np.max(np.abs(wc / wc.sum() - wn / wn.sum()) / np.where(wn > 0, wn / wn.sum(), 1)))
print('w ratio delivered/reshower (should be const = N_LHE(job)/N_LHE(point)):', np.unique(np.round(wc[wn > 0] / wn[wn > 0], 12))[:5])
print('ievt_job delivered monotonic:', bool(np.all(np.diff(c['ievt_job'][s]) > 0)))
