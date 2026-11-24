"""p3c_apply.py -- yields of generator-level samples under the MET model and its pre-declared variations (p3-c).

  <python> p3c_apply.py <out.json> <model.json> <K throws> <f_tail_prop or 0> <file> [...]

One record per input file: sum of generator weights, and per variation S1 = sum_i w_i p_i, S2 = sum_i (w_i p_i)^2 with
p_i the mean event weight over K throws (eps_trig x preselection x vetoes).  sigma(presel) = sigma_gen x S1 / sum w.
Background and validation samples only.
"""
import json
import logging
import math
import sys
from pathlib import Path

import numpy as np

import metmodel as M
import p3c_io as IO

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3c_apply')
CHUNK = 4000
PT_EDGES = [0, 100, 150, 200, 300, 400, 600, 800, 1200, 1600, 2400, 1e9]
MET_CUTS = (200.0, 225.0, 250.0, 275.0, 300.0)


def pvec(inp, par, rng, K):
    n = len(inp['ux']); p = np.zeros(n)
    for a in range(0, n, CHUNK):
        p[a:a + CHUNK] = M.apply(IO.sub(inp, slice(a, a + CHUNK)), par, rng, K)['w'].mean(1)
    return p


def v1_weight(d, rng, K):
    """v1's generator-level preselection (gen_d123.presel) emulated on the summaries: MET = neutrino MET + N(0, 25
    GeV) per component, jets smeared 10 %/sqrt(E) (+) 5 %, trigger 0.98 Phi((MET - 200)/20), flat 0.05 per vetoable
    prompt isolated e / mu / gamma; truth MET > 200 GeV generator filter.  Jet energy = pT cosh(eta) (massless)."""
    inp = d['inp']; jp, jm, lp, lm = inp['jp'], inp['jm'], inp['lp'], inp['lm']
    n = d['n']; w = np.zeros(n)
    truth = np.hypot(d['met'][:, 0], d['met'][:, 1]) > 200.0
    nveto = (lm & (np.abs(lp[:, :, 2]) < 2.5) & (lp[:, :, 4] > 0.5)).sum(1) + inp['ngam']
    erf = np.vectorize(math.erf)
    for _ in range(K):
        mx = d['met'][:, 0] + rng.normal(0, 25.0, n); my = d['met'][:, 1] + rng.normal(0, 25.0, n)
        met = np.hypot(mx, my); phm = np.arctan2(my, mx)
        e = np.maximum(jp[:, :, 0] * np.cosh(jp[:, :, 1]), 1e-3)
        pts = np.where(jm, jp[:, :, 0] * np.maximum(0, 1 + np.hypot(0.10 / np.sqrt(e), 0.05) * rng.standard_normal(e.shape)), 0)
        lead = ((pts > 100) & (np.abs(jp[:, :, 1]) < 2.4)).any(1)
        ps = np.where(pts > 30, pts, -1.0); o = np.argsort(-ps, 1)[:, :4]
        p4 = np.take_along_axis(ps, o, 1); f4 = np.take_along_axis(jp[:, :, 2], o, 1)
        dp = np.where(p4 > 0, np.abs(M.dphi(f4, phm[:, None])), 9.0).min(1)
        eps = 0.98 * 0.5 * (1 + erf((met - 200.0) / (20.0 * math.sqrt(2))))
        w += truth * (met > 250) * lead * (dp > 0.5) * eps * 0.05 ** nveto
    return w / K


def one_file(path, model, K, fprop, rng):
    d = IO.load(path); meta = d['meta']; wg = d['w_gen']; inp = d['inp']
    rec = dict(file=str(path), process=meta.get('process', meta.get('sample')), n=int(d['n']),
               sigma_gen_mb=meta.get('sigma_gen_mb'), sigma_err_mb=meta.get('sigma_err_mb'), sum_w=float(wg.sum()),
               sum_w2=float((wg ** 2).sum()), K=K, f_tail_prop=fprop, var={})
    for v in M.VARIATIONS:
        par = M.params(v, model)
        if fprop and par['f_tail'] > 0:
            par['f_tail_prop'] = fprop
        p = pvec(inp, par, rng, K)
        x = wg * p
        rec['var'][v] = dict(S1=float(x.sum()), S2=float((x ** 2).sum()), n_pos=int((p > 0).sum()),
                             max_share=float(x.max() / x.sum()) if x.sum() > 0 else None)
        if v == 'nominal':
            pt = d['pthat']
            rec['nominal_by_pthat'] = dict(edges=PT_EDGES, S1=np.histogram(pt, PT_EDGES, weights=x)[0].tolist(),
                                           S2=np.histogram(pt, PT_EDGES, weights=x ** 2)[0].tolist(),
                                           sum_w=np.histogram(pt, PT_EDGES, weights=wg)[0].tolist())
            tm = np.hypot(d['met'][:, 0], d['met'][:, 1])
            rec['nominal_truthmet_lt200_S1'] = float(x[tm < 200].sum())
            rec['nominal_truthmet_lt150_S1'] = float(x[tm < 150].sum())
            rec['nominal_pthat_lt150_S1'] = float(x[pt < 150].sum())
            if 'n_tau_had' in d:
                rec['nominal_by_ntauhad_S1'] = [float(x[d['n_tau_had'] == k].sum()) for k in (0, 1, 2)]
    par = M.params('nominal', model)
    if fprop:
        par['f_tail_prop'] = fprop
    # trigger variants and MET thresholds (nominal model)
    rec['trig'] = {}
    for kind in ('none', 'erf_shifted'):
        x = wg * pvec(inp, dict(par, trig=kind), rng, K)
        rec['trig'][kind] = dict(S1=float(x.sum()), S2=float((x ** 2).sum()))
    rec['met_cut'] = {}
    for c in MET_CUTS:
        x = wg * pvec(inp, dict(par, met_cut=c), rng, K)
        rec['met_cut'][f'{c:g}'] = dict(S1=float(x.sum()), S2=float((x ** 2).sum()))
    # cut flow (nominal, no trigger weight): MET only; + jet; + min dphi; + vetoes
    cf = np.zeros(5)
    for a in range(0, d['n'], CHUNK):
        sl = slice(a, a + CHUNK)
        o = M.apply(IO.sub(inp, sl), dict(par, trig='none'), rng, K, return_met=True)
        iw = o['iw'] if o['iw'] is not None else 1.0
        g = wg[sl, None] * iw / K
        c1 = o['met'] > par['met_cut']; c2 = c1 & o['lead']; c3 = c2 & (o['mindphi'] > par['mindphi']); c4 = c3 & ~o['veto']
        cf += [float((g * np.ones_like(c1)).sum()), float((g * c1).sum()), float((g * c2).sum()), float((g * c3).sum()),
               float((g * c4 * (par['veto_gamma_w'] ** inp['ngam'][sl, None])).sum())]
    rec['cutflow_nominal_notrig'] = dict(steps=['all', 'MET>250', '+jet>100', '+mindphi>0.5', '+vetoes'], S1=cf.tolist())
    x = wg * v1_weight(d, rng, max(K // 4, 4))
    rec['v1_like'] = dict(S1=float(x.sum()), S2=float((x ** 2).sum()))
    return rec


def main(argv):
    out = Path(argv[0]); model = json.loads(Path(argv[1]).read_text()); K = int(argv[2]); fprop = float(argv[3]) or None
    rng = np.random.default_rng([20261124, abs(hash(out.name)) % 2 ** 31])
    recs = []
    for f in argv[4:]:
        recs.append(one_file(f, model, K, fprop, rng))
        r = recs[-1]
        log.info('%s %s: n %d  f_presel(nominal) %.4g  n_pos %d', r['process'], Path(f).name, r['n'],
                 r['var']['nominal']['S1'] / r['sum_w'], r['var']['nominal']['n_pos'])
    tmp = out.with_name(out.name + '.tmp'); tmp.write_text(json.dumps(dict(model=model, records=recs)) + '\n')
    tmp.replace(out)


if __name__ == '__main__':
    main(sys.argv[1:])
