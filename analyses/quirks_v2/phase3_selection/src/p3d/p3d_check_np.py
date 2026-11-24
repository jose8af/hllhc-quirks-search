"""p3d_check_np.py -- T1-a check of a spec with the numpy pyhf env (maxwell): schema, consistency of the explicit
expected counts with pyhf, parameter list, censoring bounds, predictive B quantiles and f0, one Asimov fit pair, the
workspace JSON.  Gorm, 2026-11-24.   <out> <specname>"""
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pyhf  # noqa: E402

import p3d_model as pm  # noqa: E402
import p3d_specs  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
logging.getLogger('pyhf').setLevel(logging.WARNING)
log = logging.getLogger('p3d_check_np')


def main(out, name):
    pyhf.set_backend('numpy', pyhf.optimize.scipy_optimizer(tolerance=1e-10))
    spec = p3d_specs.get(name)
    res = dict(spec=name, pyhf=pyhf.__version__)
    for censor in (True, False):
        ws, model = pm.build(spec, censor=censor)        # raises if not schema-valid
        lab = 'on' if censor else 'off'
        res[f'schema_valid_censor_{lab}'] = True
        res[f'gen_check_censor_{lab}'] = pm.consistency(spec, model, np.random.default_rng(424242), censor=censor)
        res[f'n_par_censor_{lab}'] = int(model.config.npars)
        res[f'bounds_censor_{lab}'] = {p: model.config.suggested_bounds()[model.config.par_slice(p).start]
                                       for p in model.config.par_order}
        if censor:
            res['workspace'] = dict(ws); res['par_order'] = list(model.config.par_order)
            ex = pm.Explicit(spec, censor)
            lam = np.where(ex.fixed, ex.fixval, ex.m + 1.0)
            n = ex.expected(np.array([0.0]), lam[None, :], np.zeros((1, len(ex.nk))))[0]
            aux = np.where(ex.fixed, ex.m, ex.m + 1.0)
            d = list(n) + list(aux) + list(model.config.auxdata)
            p0 = ex.par_vector(model, 0.0, lam, np.zeros(len(ex.nk)))
            pf, tf = pyhf.infer.mle.fixed_poi_fit(1.0, d, model, list(p0), return_fitted_val=True, do_stitch=True)
            pu, tu = pyhf.infer.mle.fit(d, model, list(p0), return_fitted_val=True)
            res['asimov'] = dict(n=list(map(float, n)), t_fix_mu1=float(tf), t_free=float(tu),
                                 muhat=float(pu[model.config.poi_index]), q_mu1=float(max(tf - tu, 0.0)))
    res['predictive'] = pm.predictive(spec, nmc=200000, seed=20261124)
    res['predictive_no_drawn_bound'] = None
    pu = spec['nuis'].get('closure_PU')
    if pu and pu.get('bound_draw'):
        b = pu['bound_draw']
        res['pu_bound'] = dict(fit_bound_theta=pu['bound'], fit_bound_events=b['phi0'] * float(np.exp(pu['bound'] * b['s'])),
                               bound_95_theta=pu['bound_95'],
                               bound_95_events=b['phi0'] * float(np.exp(pu['bound_95'] * b['s'])), drawn=b)
        sp = json.loads(json.dumps(spec)); sp['nuis']['closure_PU'].pop('bound_draw')
        res['predictive_no_drawn_bound'] = pm.predictive(sp, nmc=200000, seed=20261124)['terms']['PU']
        res['predictive_pu_drawn'] = res['predictive']['terms']['PU']
    res['leading_zero_term'] = pm.leading_zero_term(spec, res['predictive'])
    res['terms'] = pm.term_table(spec); res['signal_label'] = spec['signal']['label']
    res['n_counted'] = len(spec['counted']); res['n_samples'] = len(spec['samples'])
    with open(out + '.tmp', 'w') as fh:
        json.dump(res, fh, indent=1)
    os.replace(out + '.tmp', out)
    log.info('%s: %d parameters (censor on), gen_check %.2g, asimov q(mu=1) %.4g, mu_hat %.3g', name,
             res['n_par_censor_on'], res['gen_check_censor_on'], res['asimov']['q_mu1'], res['asimov']['muhat'])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
