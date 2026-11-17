"""trigger_turnon.py -- S2-e (COM S2-e, STR §4.14 (d)): the Level-1 MET turn-on from the public CMS Phase-2 L1 TDR,
written as data, plus the numbers the branch decision needs.  Channel (ii), executor Edgar, 2026-11-17.  Stdlib only
(runs on einstein: no event data, a few arithmetic lines).

Sources (retrieval_log #11, #31):
  * CERN-LHCC-2020-004 (CMS-TDR-021), Table 4.1, printed p. 210: PuppiE_T^miss seed, offline (generator-level visible)
    MET threshold 200 GeV at 90 % of the plateau, 128 GeV at 50 %, reconstruction-efficiency plateau 100 %, tt-bar,
    <PU> = 200.  No uncertainty is stated.
  * same TDR, Fig. 3.125, printed p. 188 (PDF p. 197): PuppiMET, online threshold 112 GeV (18.1 kHz), efficiency vs
    gen. MET in 20 GeV bins, 14 TeV, 200 PU.  Read by eye from a 400 dpi rendering (ESTIMATE, reading error +-0.01;
    the plotted statistical bars are <= 0.01 below 350 GeV and about 0.01-0.03 above 390 GeV).
Parametrisations (not fits):
  (a) DIGITISED: linear interpolation of the Fig. 3.125 readings (bin centres).
  (b) ERF-2PT: eps = Phi((x - mu)/sigma) through Table 4.1's two points: mu = 128 GeV (50 %), sigma = (200 - 128)/z90 with
      z90 = Phi^-1(0.9) computed here (statistics.NormalDist), plateau 1.0 (Table 4.1).
  (c) v1: 0.98 * Phi((x - 200)/20) (D5 §4, products.py l.43-45 as quoted in STR §4.14 (d)).
Pre-declared wide nuisance of the "parametrised, not sourced" branch (STR §4.14 acceptance criteria S2-e): the full
difference between the curve and the curve with its 50 % point shifted by one width; evaluated for (b): eps(x) against
Phi((x - mu - sigma)/sigma).
Usage: python3 -I trigger_turnon.py <out.json>
"""
import json
import logging
import sys
from statistics import NormalDist

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('turnon')

# Fig. 3.125 PuppiMET (112 GeV) readings: (bin centre GeV, efficiency); ESTIMATE +-0.01
FIG3125 = [(10, 0.035), (30, 0.04), (50, 0.05), (70, 0.085), (90, 0.15), (110, 0.27), (130, 0.445), (150, 0.62),
           (170, 0.775), (190, 0.875), (210, 0.93), (230, 0.955), (250, 0.975), (270, 0.985), (290, 0.98),
           (310, 0.985), (330, 0.99), (350, 0.995), (370, 1.0), (390, 0.985), (410, 0.975), (430, 0.985),
           (450, 1.0), (470, 1.0), (490, 1.0)]
N = NormalDist()


def digitised(x):
    if x <= FIG3125[0][0]:
        return FIG3125[0][1]
    for (x0, y0), (x1, y1) in zip(FIG3125, FIG3125[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return FIG3125[-1][1]


def crossing(level):
    for (x0, y0), (x1, y1) in zip(FIG3125, FIG3125[1:]):
        if y0 < level <= y1:
            return x0 + (level - y0) * (x1 - x0) / (y1 - y0)
    return None


def main():
    out = sys.argv[1]
    z90 = N.inv_cdf(0.9)
    mu, sig = 128.0, (200.0 - 128.0) / z90
    erf2 = lambda x: N.cdf((x - mu) / sig)                    # noqa: E731
    erf2_shift = lambda x: N.cdf((x - mu - sig) / sig)        # noqa: E731
    v1 = lambda x: 0.98 * N.cdf((x - 200.0) / 20.0)           # noqa: E731
    grid = [150, 175, 200, 225, 250, 275, 300, 350, 400, 500]
    rows = [dict(met=x, digitised=round(digitised(x), 4), erf_2pt=round(erf2(x), 4),
                 erf_2pt_shifted_1width=round(erf2_shift(x), 4),
                 wide_nuisance_abs=round(erf2(x) - erf2_shift(x), 4), v1=round(v1(x), 4)) for x in grid]
    # limiting / substitution checks
    chk = dict(z90=z90, sigma_gev=sig, erf_2pt_at_128=erf2(128.0), erf_2pt_at_200=erf2(200.0),
               v1_at_250=v1(250.0), v1_at_250_STR='0.974 (STR §4.14 (d))',
               digitised_50pct_crossing_gev=crossing(0.5), digitised_90pct_crossing_gev=crossing(0.9),
               digitised_95pct_crossing_gev=crossing(0.95), digitised_975pct_crossing_gev=crossing(0.975))
    res = dict(sources=['CERN-LHCC-2020-004 Table 4.1 p. 210', 'CERN-LHCC-2020-004 Fig. 3.125 p. 188 (by-eye, ESTIMATE)'],
               variable='generator-level MET of visible particles (neutrinos excluded), tt-bar, <PU> = 200; L1 only (HLT not sourced)',
               fig3125_readings=FIG3125, erf_2pt=dict(mu_gev=mu, sigma_gev=sig, plateau=1.0), checks=chk, table=rows,
               stated_uncertainty='none in the TDR text; Fig. 3.125 shows statistical bars only')
    json.dump(res, open(out, 'w'), indent=1)
    for r in rows:
        log.info('%s', r)
    log.info('%s', chk)


if __name__ == '__main__':
    main()
