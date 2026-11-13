"""p0_event_budget.py -- Stage-3 probe 0: how many events each TRGS file offers after the Stage-3 selection.

For every TRGS file (E 200-1500, Etilde 200/500/1000): rows with w > 0, pT(QQ) > 200 GeV, |eta_pair| < 2.5 (and < 1),
per template/toy split: raw count, Kish N_eff = (sum w)^2 / sum w^2, and the number of events kept by the loader's
deterministic unweighting (iter_events(unweight=True), seed 12345).  Output: data/sim_stage3/probes/p0_event_budget.json
Run (from theory_track/): pixi run python sim/stage3/probes/p0_event_budget.py
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(TT, 'sim', 'scripts'))
import mg_events as mg  # noqa: E402

OUT = os.path.join(TT, 'data', 'sim_stage3', 'probes'); os.makedirs(OUT, exist_ok=True)
res = {}
pts = [('F', m) for m in range(200, 1600, 100)] + [('S', m) for m in (200, 500, 1000)]
for spin, m in pts:
    c = mg.load(mg.sample_file(m, 'trig', spin))
    acc, wmax = mg.unweight_mask(c, 12345)
    row = {}
    for eta in (2.5, 1.0):
        for split in (None, 'template', 'toy'):
            ids = mg._select(c, eta_max=eta, ptmin=200.0, split=split)
            w = c['w'][ids]
            neff = float(w.sum() ** 2 / (w ** 2).sum())
            nunw = int(acc[ids].sum())
            row[f'eta{eta}_{split or "all"}'] = dict(rows=int(len(ids)), neff=round(neff, 1), n_unweighted=nunw)
    # fraction of the |eta|<2.5 tail cross section with |eta|<1
    i25 = mg._select(c, eta_max=2.5, ptmin=200.0); i10 = mg._select(c, eta_max=1.0, ptmin=200.0)
    row['frac_sigma_eta1_of_eta25'] = round(float(c['w'][i10].sum() / c['w'][i25].sum()), 4)
    row['sigma_norm_tail_eta25_fb'] = mg.sigma_norm_fb(m, 'trig', spin, eta_max=2.5, ptmin=200.0)
    row['yield_3ab_tail_eta25'] = 3000.0 * row['sigma_norm_tail_eta25_fb']
    res[f'{spin}_{m}'] = row
    print(spin, m, row['eta2.5_all'], row['eta2.5_template']['n_unweighted'], row['eta2.5_toy']['n_unweighted'],
          'f(eta<1)=', row['frac_sigma_eta1_of_eta25'], 'yield', round(row['yield_3ab_tail_eta25'], 1), flush=True)
json.dump(res, open(os.path.join(OUT, 'p0_event_budget.json'), 'w'), indent=1)
