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
# CMS NOTE-2018/006 Fig. 35 (printed p. 21), Z->mumu, p_T^Z > 30 GeV, PUPPI, <N_PU> = 200 (blue): by-eye readings,
# ESTIMATE, reading error +-1 GeV (minor ticks 2 GeV), rendered at 300 dpi (/var/tmp/jdochoa/sebastian/retr/cmsnote/fig35-23.png).
# x = PU density [events/mm]; y = sigma(u_par)/(u_par/p_T^Z) and sigma(u_perp)/(u_par/p_T^Z) [GeV].
CMS_FIG35_PAR = {0.1: 30.0, 0.4: 26.0, 0.75: 29.5, 1.1: 29.5, 1.45: 32.0, 1.75: 35.0, 1.9: 33.5}
CMS_FIG35_PERP = {0.1: 26.5, 0.4: 25.5, 0.75: 28.5, 1.1: 30.0, 1.5: 29.5, 1.75: 31.5, 1.9: 32.5}
CMS_READ_ERR = 1.0
CMS_MEAN_DENSITY = 1.4   # "the average event density of 1.4 mm with PU 200", CMS NOTE-2018/006 §2.4, printed p. 9


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
    es_z = {s: round(es2013(s, MU), 1) for s in (0, 250, 500)}
    log.info('2013-004 at mu=200 for a hard-scatter SumET of 0/250/500 GeV (range of a Z->mumu event, not given by '
             'the CMS note): %s', es_z)
    cms = dict(source='CMS NOTE-2018/006 Fig. 35, Z->mumu, PUPPI, <N_PU>=200; ESTIMATE +-1 GeV',
               par=CMS_FIG35_PAR, perp=CMS_FIG35_PERP, reading_err_gev=CMS_READ_ERR, mean_density=CMS_MEAN_DENSITY,
               text_value='"A resolution of about 25 GeV is achieved in the perpendicular component using PUPPI" (§2.9, p. 19)',
               es2013_at_small_sumet=es_z,
               not_comparable=['ATLAS Fig. 18: RMS of E_x,y(reco) - E_x,y(true) in ttbar vs total SumET; CMS Fig. 35: width '
                               'of the hadronic recoil components u_par, u_perp (response-corrected) in Z->mumu (no '
                               'true MET) vs PU density, no SumET axis',
                               'pile-up mitigation: CMS PUPPI vs ATLAS PU-jet tagger + track soft term',
                               'ATLAS 2013-004 is a parametrisation in SumET with an assumed 20 GeV per interaction, '
                               'not a measurement on either process'])
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(dict(mu=MU, tags={'fig18': 'ESTIMATE (by-eye reading, +-0.5 GeV)', 'formulas': 'transcribed, printed pages cited'},
                   note='reading (b) with SumET_hs = SumET - 20*mu is undefined below SumET = 4000 GeV',
                   rows=rows, cms_note=cms), open(OUT / 'met_compare.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
