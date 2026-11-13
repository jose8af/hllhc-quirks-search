"""val_v9.py -- Stage-3 validation V9 (plan §5): unweighted (production) vs weighted mode at one point, E 500 GeV,
Lambda = 1 keV, configuration BM (P2 settings: |eta_pair| < 4 with the count inside 2.5, luminous vertex, max_boost 1e-3).

Weighted mode: the same Stage-2 selection (TRGS, w > 0, pT(QQ) > 200 GeV) WITHOUT the hit-or-miss unweighting, rows
in file order, template split, the first 200 rows inside |eta_pair| < 2.5 (+ the forward rows in between), each event
carrying its original weight w_orig.  The input file is built with code/make_inputs.extract (imported read-only; the
unweighting mask is replaced in memory by "accept all", nothing on disk is modified) and propagated with the
production driver code/run_stage3.run_job (same kernel s3.2, same seeds rule) into data/sim_stage3/validation/v9/.
Comparison (criterion, plan §5): the w_orig-weighted medians of ds_all, ds_itps, ell_max, hits per tracker surface and
tracker hits per event agree with the unweighted production medians (p2/F_m500/L1_BM, template, |eta| < 2.5) within
2 sigma (bootstrap, 1000 resamples; weighted bootstrap for the weighted sample).
Cost: ~250 events x ~0.3 s.  Output: sim/stage3/results/V9.json.
Run (theory_track/): pixi run python sim/stage3/scripts/val_v9.py
"""
import json
import sys

import numpy as np

import s3common as C

sys.path.insert(0, str(C.S3 / 'code'))
VD = C.DATA / 'validation' / 'v9'


def wmedian(x, w):
    o = np.argsort(x); xs = x[o]; cw = np.cumsum(w[o]); cw /= cw[-1]
    return float(np.interp(0.5, cw, xs))


def boot(x, w, nb=1000, seed=3):
    rng = np.random.default_rng(seed)
    n = len(x)
    return float(np.std([wmedian(x[i], w[i]) for i in (rng.integers(0, n, n) for _ in range(nb))]))


def build_input():
    import make_inputs as MI
    orig = MI.mg.unweight_mask

    def accept_all(c, seed):
        acc, wmax = orig(c, seed)
        return np.ones_like(acc, dtype=bool), wmax
    MI.mg.unweight_mask = accept_all
    try:
        d, sel = MI.extract('F', 500, 'p2')
    finally:
        MI.mg.unweight_mask = orig
    sel['unweight'] = False
    sel['note'] = 'V9 weighted mode: hit-or-miss unweighting disabled; use w_orig'
    d['selection_json'] = np.array(json.dumps(sel, default=float))
    (VD / 'inputs').mkdir(parents=True, exist_ok=True)
    np.savez_compressed(VD / 'inputs' / 'F_m500_p2w.npz', **d)
    return d


def main():
    import run_stage3 as R
    inp = VD / 'inputs' / 'F_m500_p2w.npz'
    d = build_input() if not inp.exists() else dict(np.load(inp))
    spl = d['tt_split']; ins = d['in_eta25']
    idx = np.where(spl == 0)[0]
    last = int(np.searchsorted(np.cumsum(ins[idx]), 200))
    ev = idx[:last + 1].tolist()
    job = dict(id='v9/F_m500/L1_BM_weighted', out='v9/F_m500/L1_BM_weighted.npz', campaign='v9', spin='F', m=500, lam=1.0,
               cfg='BM', chunk=0, input='F_m500_p2w.npz', ev=ev, max_boost=1e-3, hmax=0.2, vertex='lumi')
    outp = VD / 'out' / 'v9' / 'F_m500' / 'L1_BM_weighted.npz'
    if not outp.exists():
        R.run_job(job, str(VD / 'inputs'), str(VD / 'out'))
    zw = np.load(outp)
    # unweighted production, template, |eta| < 2.5
    S = np.load(C.SUMM / 'events_p2.npz')
    pk = list(S['point_keys']).index('p2/F_m500/L1_BM')
    mu = (S['point'] == pk) & (S['tt_split'] == 0) & S['in_eta25'] & (S['status'] == 1)
    # derived observables for the weighted file (same definitions as extract.py)
    import extract as X
    dw = X.do_file((str(outp.relative_to(C.DATA)), 'v9'))
    mw = dw['in_eta25'] & (dw['status'] == 1)
    ww = zw['w_orig'][mw]
    res = dict(point='E 500 GeV, 1 keV, BM (P2 settings)', n_weighted=int(mw.sum()), n_unweighted=int(mu.sum()),
               kish_neff_weighted=float(ww.sum() ** 2 / (ww ** 2).sum()), observables={})
    ok = True
    for o in ('ds_all_um', 'ds_itps_um', 'ell_max', 'hits_per_surf', 'n_trk', 'N_osc_vac', 'sep_IT_um'):
        if o == 'n_trk':
            xw = (dw['n_trk0'] + dw['n_trk1'])[mw]; xu = (S['n_trk0'] + S['n_trk1'])[mu]
        else:
            xw = np.asarray(dw[o], float)[mw]; xu = np.asarray(S[o], float)[mu]
        fw = np.isfinite(xw); fu = np.isfinite(xu)
        a = wmedian(xw[fw], ww[fw]); sa = boot(xw[fw], ww[fw])
        b = float(np.median(xu[fu])); sb = boot(xu[fu], np.ones(fu.sum()))
        pull = (a - b) / np.hypot(sa, sb) if np.hypot(sa, sb) > 0 else 0.0
        res['observables'][o] = dict(weighted_median=a, err_w=sa, unweighted_median=b, err_u=sb, pull=float(pull),
                                     PASS=bool(abs(pull) <= 2))
        ok &= abs(pull) <= 2
    res['cpu_s'] = float(json.loads(str(zw['meta_json']))['cpu_s'])
    res['PASS'] = bool(ok)
    C.dump('V9.json', res)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
