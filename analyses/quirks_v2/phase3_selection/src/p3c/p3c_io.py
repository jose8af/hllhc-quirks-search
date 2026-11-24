"""p3c_io.py -- read p3c_gen or pilot (p2x_hs0) summaries into model inputs (work package p3-c)."""
import json

import numpy as np

import metmodel as M


def load(path):
    """-> dict(meta, n, w_gen, pthat, met (n,2) neutrino MET, px5, py5, sumet5, inp=model inputs, extra)"""
    z = np.load(path); meta = json.loads(str(z['meta']))
    if meta.get('mode') == 'p3c_gen':
        c = {k: i for i, k in enumerate(meta['evt_cols'])}; e = z['evt']
        d = dict(w_gen=e[:, c['weight']], pthat=e[:, c['pthat']], met=e[:, [c['met_x'], c['met_y']]],
                 px5=e[:, c['px_eta5']], py5=e[:, c['py_eta5']], sumet5=e[:, c['sumet_eta5']],
                 n_tau_had=e[:, c['n_tau_had']], n_tau=e[:, c['n_tau']])
    else:                       # pilot file of p2x_hs0 (Z(nunu), truth MET > 200 GeV filter, unweighted)
        g = z['gsum']; c = {k: i for i, k in enumerate(meta['gsum_cols'])}; e = z['evt']
        ec = {k: i for i, k in enumerate(meta['evt_cols'])}
        d = dict(w_gen=g[:, c['gen_weight']], pthat=g[:, c['pthat']], met=e[:, [ec['met_x'], ec['met_y']]],
                 px5=g[:, c['px_eta5']], py5=g[:, c['py_eta5']], sumet5=g[:, c['sumet_eta5']],
                 w_v1=e[:, ec['w_v1']], met_reco_v1=e[:, ec['met_reco_v1']], hs_tries=e[:, ec['hs_tries']],
                 sigma_gen_mb=e[:, ec['sigma_gen_mb']], seed_lo=e[:, ec['ev_seed_lo']], seed_hi=e[:, ec['ev_seed_hi']])
    d['inp'] = M.build_inputs(d['px5'], d['py5'], z['jets'], z['jet_off'], z['lep'], z['lep_off'])
    d['lep'] = z['lep']; d['lep_off'] = z['lep_off']
    d['meta'] = meta; d['n'] = len(d['px5'])
    return d


def sub(inp, sl):
    return {k: v[sl] for k, v in inp.items()}
