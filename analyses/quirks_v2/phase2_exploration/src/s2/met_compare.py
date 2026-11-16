"""met_compare.py -- R-3 hand-over: ATLAS 2013 MET-resolution formulas evaluated at the Fig. 18 points of
ATL-PHYS-PUB-2019-005 (mu = 200), against the by-eye readings of that figure.  No parameter is fitted or tuned.

Sources (retrieval_log.md #12, #15):
  ATL-PHYS-PUB-2013-004 §8, printed p. 13: sigma(E_x,y^miss) = (0.40 + 0.09*sqrt(mu)) * sqrt(SumET + 20*mu)
      ("SumET of the hard scattering event and mu*20 GeV")
  ATL-PHYS-PUB-2013-009 Table 5, p. 8 (mu = 140, SumET > 1700 GeV): 32.1 + 0.720*sqrt(SumET)
  ATL-PHYS-PUB-2019-005 Fig. 18, printed p. 21: by-eye readings, ESTIMATE, reading error +-0.5 GeV
      (page rendered at 150 dpi: /var/tmp/jdochoa/sebastian/retr/perf/f18-21.png on einstein)
Two readings of the 2013-004 SumET: (a) SumET = hard-scatter SumET (formula adds 20*mu); (b) SumET = the figure's total
SumET, i.e. the hard-scatter part is SumET - 20*mu (only possible where SumET > 20*mu = 4000 GeV) -- and, as a bound,
(b') the formula with the figure's SumET inserted directly without the 20*mu term.
Run (light, stdlib): python3 -I met_compare.py  -> ../../outputs/s2/met_compare.json
"""
import json
import logging
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('met_compare')
OUT = Path(__file__).resolve().parents[2] / 'outputs' / 's2'

MU = 200
FIG18_FULL_ETA = {1000: 37.5, 2000: 42.0, 3000: 46.5, 4000: 50.5}   # ESTIMATE, +-0.5 GeV, curve "ITk full eta coverage"
FIG18_ETA25 = {1000: 38.5, 2000: 46.0, 3000: 51.5, 4000: 56.0}       # ESTIMATE, +-0.5 GeV, curve "ITk |eta|<2.5"
READ_ERR = 0.5


def es2013(sumet_hs, mu):
    return (0.40 + 0.09 * math.sqrt(mu)) * math.sqrt(sumet_hs + 20.0 * mu)


def zfit140(sumet):
    return 32.1 + 0.720 * math.sqrt(sumet)


def main():
    rows = []
    for s, r in FIG18_FULL_ETA.items():
        a = es2013(s, MU)
        bprime = (0.40 + 0.09 * math.sqrt(MU)) * math.sqrt(s)
        rows.append(dict(sumet_gev=s, fig18_full_eta_gev=r, fig18_eta25_gev=FIG18_ETA25[s], reading_err_gev=READ_ERR,
                         es2013_sumet_is_hard_scatter=round(a, 1), es2013_sumet_is_total_no_pu_term=round(bprime, 1),
                         ratio_a_to_fig18=round(a / r, 2), ratio_bprime_to_fig18=round(bprime / r, 2),
                         zfit_mu140_2013_009=round(zfit140(s), 1) if s > 1700 else None))
        log.info('%s', rows[-1])
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(dict(mu=MU, tags={'fig18': 'ESTIMATE (by-eye reading, +-0.5 GeV)', 'formulas': 'transcribed, printed pages cited'},
                   note='reading (b) with SumET_hs = SumET - 20*mu is undefined below SumET = 4000 GeV',
                   rows=rows), open(OUT / 'met_compare.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
