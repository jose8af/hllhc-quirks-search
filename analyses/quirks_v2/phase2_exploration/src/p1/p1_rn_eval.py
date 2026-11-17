"""p1_rn_eval.py -- P1-a floor DIAGNOSTIC (not a pre-declared test; channel (ii), Edgar, 2026-11-17).

Question (Sebastian's caveat, EXPLORATION_ii_sebastian §3.6): the pre-declared floor test 2 emulated reduced precision by
TRUNCATING mdot to 44 bits, a biased rounding; the like-for-like emulation of double-precision round-off is
round-to-nearest.  This script reads the same 40 events per point run with
  nominal (float64), t44 (truncation, 44 bits; p2-b-p1-run), dd (double-double mdot; p2-b-p1-run),
  rn44 (round-to-nearest, 44 bits, u'/u = 2^9 = 512) and rn47 (round-to-nearest, 47 bits, u'/u = 2^6 = 64; p2-b-p1-rn)
and forms, exactly as p1_eval.py does, Delta_c(k) = c_k - c_ev with c_k = (Delta_s(B/k) k / Delta_s(B) - 1)/ln k for
k = 2, 2.5, 4, 20, dropping events with any status != 1 or a non-positive / non-finite Delta_s.
Reported:
  * per kernel: median Delta_c(k), k = 2, 2.5, 4, 20 (n used);
  * the pre-declared comparison form applied to the RN kernels: two-sample KS of nominal Delta_c(20) against
    kernel Delta_c(2.5) (the "8x larger eps_perp" of the spec, which presumes u' = 64 u);
  * the scaling-consistent form for rn44: under the floor hypothesis Delta_c ~ u / eps_perp^2 and eps_perp ~ B/k, u'/u = 512
    moves the nominal k = 20 pattern to k = 20/sqrt(512) = 0.88, outside the measured fractions; so for rn44 the
    nearest available comparison (k = 2) and the predicted amplitude ratio are reported, not a verdict;
  * paired differences (kernel - nominal) of Delta_c(k) on common events, median with a paired bootstrap (2000).
No reading is attached: the pre-declared reading of floor test 2 stays "not the floor pattern" as recorded.
Usage: python p1_rn_eval.py <out.json>   (TT env: numpy, scipy)
"""
import json
import logging
import math
import os
import sys

import numpy as np
from scipy.stats import ks_2samp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 's2'))
from marker_files import done_outputs  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p1_rn_eval')
KS = ((2, 0.5), (2.5, 0.4), (4, 0.25), (20, 0.05))
NB = 2000


def per_event(path):
    rows = {}
    for e in json.load(open(path))['events']:
        if not (all(s == 1 for s in e['status']) and all(math.isfinite(x) and x > 0 for x in e['ds'])):
            continue
        ds, fr = e['ds'], e['fr']
        rows[e['i']] = {str(k): (ds[fr.index(f)] * k / ds[0] - 1) / math.log(k) - e['c_ev'] for k, f in KS if f in fr}
    return rows


def main():
    out = sys.argv[1]
    files = {os.path.basename(p)[:-5]: p for p in done_outputs('p2-b-p1-run', suffix='.json', prefix='floor-')
             + done_outputs('p2-b-p1-rn', suffix='.json', prefix='floor-')}
    rng = np.random.default_rng(20261117)
    res = dict(definition=__doc__.split('Usage')[0], points={})
    for p in ('e500', 'e1000'):
        ev = {k: per_event(files[f'floor-{p}-{k}']) for k in ('nominal', 't44', 'dd', 'rn44', 'rn47')
              if f'floor-{p}-{k}' in files}
        r = dict(n_used={k: len(v) for k, v in ev.items()}, median_dc={}, ks_nominal20_vs_kernel2p5={}, paired_minus_nominal={})
        for k, v in ev.items():
            r['median_dc'][k] = {kk: float(np.median([x[kk] for x in v.values()])) for kk in ('2', '2.5', '4', '20')}
        a = [x['20'] for x in ev['nominal'].values()]
        for k in ('t44', 'rn44', 'rn47'):
            if k in ev:
                b = [x['2.5'] for x in ev[k].values()]
                t = ks_2samp(a, b)
                r['ks_nominal20_vs_kernel2p5'][k] = dict(ks_stat=float(t.statistic), p=float(t.pvalue), n_a=len(a), n_b=len(b))
        for k in ('t44', 'dd', 'rn44', 'rn47'):
            if k not in ev:
                continue
            common = sorted(set(ev[k]) & set(ev['nominal']))
            d = {}
            for kk in ('2', '2.5', '4', '20'):
                x = np.array([ev[k][i][kk] - ev['nominal'][i][kk] for i in common])
                bs = np.std([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(NB)])
                d[kk] = dict(n=len(common), median=float(np.median(x)), sigma=float(bs))
            r['paired_minus_nominal'][k] = d
        # floor-hypothesis amplitude prediction (ESTIMATE, the spec's own scaling): the relative floor error of Delta_s at
        # B/k grows as u * k^2 (eps_perp^-2, eps_perp ~ B/k).  (a) spec form, ratio of the floor errors:
        # kernel(k)/nominal(20) = (u'/u)(k/20)^2;  (b) with the 1/ln k of the c_k definition: (u'/u)(k^2/ln k)/(400/ln 20).
        pred = {}
        for kern, ur in (('rn44', 512.0), ('rn47', 64.0), ('t44_if_rn', 512.0)):
            pred[kern] = {kk: dict(spec=ur * (float(kk) / 20) ** 2,
                                   with_ln=ur * (float(kk) ** 2 / math.log(float(kk))) / (400 / math.log(20)))
                          for kk in ('2', '2.5', '4')}
        r['floor_hypothesis_ratio_kernel_k_over_nominal_20'] = pred
        res['points'][p] = r
        log.info('%s %s', p, json.dumps(r, indent=1)[:2500])
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
