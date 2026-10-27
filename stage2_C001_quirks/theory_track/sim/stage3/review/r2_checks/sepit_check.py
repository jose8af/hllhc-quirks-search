"""R2: independent recompute of the median IT pair separation (template, in_eta25, status 1) for F_m1000 and the 1-30 keV log-log slope,
with a bootstrap error on the slope (not given in P2.json)."""
import json, numpy as np
from pathlib import Path
TT = Path('/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track')
S = np.load(TT/'data/sim_stage3/summary/events_p2.npz'); keys = [str(k) for k in S['point_keys']]
P2 = json.load(open(TT/'sim/stage3/results/P2.json'))['sep_IT_handle']
for sp in ('F_m1000', 'F_m300', 'S_m500'):
    lams = [l for l in P2[sp]['lam_keV'] if 1 <= l <= 30]
    i1 = keys.index(f'p2/{sp}/L1_BM') if f'p2/{sp}/L1_BM' in keys else None
    if i1 is None:
        print([k for k in keys if sp in k][:3]); break
    sel1 = S['point'] == i1; evs = np.sort(S['ev_index'][sel1 & (S['tt_split'] == 0) & S['in_eta25']])
    M = []
    for l in lams:
        sel = np.where(S['point'] == keys.index(f'p2/{sp}/L{l:g}_BM'))[0]
        pos = {int(e): j for j, e in zip(sel, S['ev_index'][sel])}
        tk = np.array([pos.get(int(e), -1) for e in evs]); tk = tk[tk >= 0]
        s = S['sep_IT_um'][tk][(S['status'][tk] == 1)]; s = s[np.isfinite(s)]
        M.append(s)
    med = np.array([np.median(s) for s in M])
    ref = np.array([P2[sp]['sep_IT_med_um'][P2[sp]['lam_keV'].index(l)] for l in lams])
    sl = np.polyfit(np.log(lams), np.log(med), 1)[0]
    rng = np.random.default_rng(1)
    bs = [np.polyfit(np.log(lams), np.log([np.median(rng.choice(s, len(s))) for s in M]), 1)[0] for _ in range(300)]
    print(sp, 'n per Lambda', [len(s) for s in M][:3], '... max rel diff np.median vs P2.json', f'{np.max(np.abs(med/ref-1)):.3f}',
          f'slope {sl:.3f} +- {np.std(bs):.3f} (P2.json {P2[sp]["loglog_slope_1to30keV"]:.3f})')
    print('   local slopes', np.round(np.diff(np.log(med))/np.diff(np.log(lams)), 2))
