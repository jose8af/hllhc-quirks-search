"""R2 c2: loader -> T3_causal round trip (regression after the S2-R1 fixes), plus loader API checks.
Run from theory_track/:  pixi run python sim/review/r2_checks/c2_roundtrip.py"""
import os, sys
import numpy as np
TT = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track'
sys.path.insert(0, f'{TT}/sim/scripts'); sys.path.insert(0, f'{TT}/code')
import mg_events as M
from T3_causal import run_causal

# API checks
for spin, m in (('F', 500), ('S', 500)):
    c = M.load(M.sample_file(m, 'trig', spin))
    ev = list(M.iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200))
    assert all('w' in e[2] for e in ev)
    W = np.array([e[2]['w'] for e in ev])
    s_lo = M.sigma_lo_mlm_fb(m, 'trig', spin, n_ic=2, ptmin=200)
    s_n = M.sigma_norm_fb(m, 'trig', spin, ptmin=200)
    s_n_t = M.sigma_norm_fb(m, 'trig', spin, ptmin=200, split='template'); s_n_y = M.sigma_norm_fb(m, 'trig', spin, ptmin=200, split='toy')
    evu = list(M.iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200, unweight=True))
    Wu = np.array([e[2]['w'] for e in evu])
    print(f'{spin}{m}: n_sel={len(ev)} sum w={W.sum():.5g}  unweighted n={len(evu)} n*wmax={Wu.sum():.5g} (ratio {Wu.sum()/W.sum():.4f}); '
          f'sigma_lo_mlm(pT>200,NIC2)={s_lo:.4f} sigma_norm(pT>200)={s_n:.4f} -> N(3/ab)={3000*s_n:.0f}; template/toy {s_n_t:.4f}/{s_n_y:.4f}; '
          f'sigma_norm_fb scalar={float(c["sigma_norm_fb"]):.4g} sigma_ref={float(c["sigma_ref_fb"]):.5g}', flush=True)

# round trip: 100 unweighted events at E 500 and 100 weighted draws at S 500
rt = {}
for spin, m in (('F', 500), ('S', 500)):
    evs = M.sample_events_mg(m, 100, 'trig', spin, rng=np.random.default_rng(11), eta_max=2.5, ptmin=200)
    st = []; nh = []
    for p1, p2, info in evs:
        r = run_causal(np.asarray(p1), np.asarray(p2), float(m), 1.0)
        st.append(int(r['status'])); nh.append(len(r['hits']))
    print(spin, m, 'status', dict(zip(*np.unique(st, return_counts=True))), 'Nhits median', np.median(nh), flush=True)
