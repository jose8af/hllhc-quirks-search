"""R2: R(1/2) = median 2 Ds(B0/2)/Ds(B0) at E500, 1 keV (P1 B, B2, both status 1) and BM/sqrt(B^2+M^2) at E500 1 keV."""
import numpy as np
S = np.load('/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/data/sim_stage3/summary/events_p1.npz'); keys = list(S['point_keys'])
def get(cfg, L='1'):
    sel = S['point'] == keys.index(f'p1/F_m500/L{L}_{cfg}'); o = np.argsort(S['ev_index'][sel], kind='stable')
    return {c: S[c][sel][o] for c in ('ds_barrel_um', 'status', 'ev_index')}
print(sorted(set(k.split('_')[-1] for k in keys if k.startswith('p1/F_m500/L1_'))))
b, h = get('B'), get('B2'); assert (b['ev_index'] == h['ev_index']).all()
ok = (b['status'] == 1) & (h['status'] == 1) & (b['ds_barrel_um'] > 0)
R = 2*h['ds_barrel_um'][ok]/b['ds_barrel_um'][ok]; rng = np.random.default_rng(2)
print('R(1/2) E500 1 keV', np.median(R), '+-', np.std([np.median(rng.choice(R, len(R))) for _ in range(1000)]), 'n', ok.sum(), '-> c', (np.median(R)-1)/np.log(2))
