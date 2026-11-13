"""G2a: the plan §6.2 campaign table evaluated at the MEASURED finder speed (arithmetic only).

Uses blocks() of acts/stage4/probes/f3r_campaigns.py unchanged (executed up to its table loop, read-only): per-event
inputs PU 4.7 s (ESTIMATE), B1 = 4.7 + 4 t1, B2 = 2 x 4.7 + 2 t2, etc.  Capacity: Mac 7 workers (plan convention).
CPU-h are proportional to the MEAN time per trial, so the mean t1 (and t2) is used; the G2a statistic quoted in the
report is the median.  t2 options: (a) measured finder-only t2; (b) (a) + the per-subset chi2_core recomputation for
every rho = 2 set passing N_IP2 >= 7 at the measured per-set cost; (c) plan convention t2 = 8 t1.  The counting-rung
thinning weights are NOT in (a)-(c) (the existing 2e4-subset MC is unaffordable, see the report).
Run (theory_track): pixi run python -m acts.stage4.finder.g2a_campaigns  -> data/acts_stage4/g2/g2a_campaigns.json
"""
import json
import math

import numpy as np

from .trials import TT

SRC = (TT / 'acts' / 'stage4' / 'probes' / 'f3r_campaigns.py').read_text()
NS = {'__file__': str(TT / 'acts' / 'stage4' / 'probes' / 'f3r_campaigns.py')}
exec(SRC[:SRC.index('T1S = [')], NS)          # constants + blocks() + mac_cloud_wall(), nothing else
blocks = NS['blocks']; MAC_W = NS['MAC_W']; DAY = NS['DAY']
G2 = TT / 'data' / 'acts_stage4' / 'g2'


def table(t1, t2):
    out = {}
    tot = 0.0
    for c in ('C1', 'C2', 'C3', 'C4', 'C5'):
        bl = blocks(c, t1, t2)
        cpu = sum(bl.values())
        out[c] = dict(cpu_h=round(cpu, 1), wall_mac_h=round(cpu / MAC_W, 1), fits_1day_mac=bool(cpu / MAC_W <= DAY),
                      blocks={k: round(v, 1) for k, v in bl.items()})
        if c != 'C5':
            tot += cpu
    out['C1_C4'] = dict(cpu_h=round(tot, 1), wall_mac_h=round(tot / MAC_W, 1),
                        mac_days=round(tot / MAC_W / DAY, 2))
    return out


def t2max_C1(t1):
    """Largest t2 (s) for which C1 still fits one Mac day (G2b criterion for C1 at this t1)."""
    t2 = 0.0
    while sum(blocks('C1', t1, t2 + 1).values()) / MAC_W <= DAY and t2 < 5000:
        t2 += 1
    return t2


if __name__ == '__main__':
    t1r = json.loads((G2 / 'timing_rho1.json').read_text())
    t1_mean = t1r['summary_wall']['mean']; t1_med = t1r['summary_wall']['median']
    res = dict(t1_mean=t1_mean, t1_median=t1_med, t1_p90=t1r['summary_wall']['p90'])
    t2_opts = {}
    try:
        t2r = json.loads((G2 / 'timing_rho2.json').read_text())
        tr = t2r['trials']
        core = json.loads((G2 / 'timing_rho2_chi2core.json').read_text())
        ms_core = core['ms_per_set_mean']                       # numba kernel, 1e3 subsets per set
        n7 = np.mean([r['n_sets_ip2ge7'] for r in tr]); n6 = np.mean([r['n_sets_ip2ge6'] for r in tr])
        nl = np.mean([r['n_sets_loose'] for r in tr])
        t2_find = float(np.mean([r['t_find_s'] for r in tr]))
        t2_opts['a_finder_only'] = t2_find
        t2_opts['b_finder_plus_chi2core_all_ip2ge7'] = float(t2_find + n7 * ms_core / 1e3)
        # plan §4.1 step 3b strata (f_lo = 0.01 below N_IP2 >= 6, f_hi = 0.1 at/above) for the chi2_core and the
        # counting-rung weights; counting weights at an ASSUMED 1 ms per set (plan's DP ESTIMATE; the existing MC is
        # ~21 ms per set, measured)
        t2_opts['c_finder_plus_strata_weights_ESTIMATE'] = float(t2_find + 0.1 * n7 * ms_core / 1e3
                                                             + (0.01 * (nl - n6) + 0.1 * n6) * 1.0 / 1e3)
        res['rho2_sets_per_trial_mean'] = dict(loose=float(nl), ip2ge6=float(n6), ip2ge7=float(n7))
        res['rho2_ms_per_set'] = dict(chi2core_numba_1e3=ms_core,
                                      thin_mc_2e4_measured=float(np.mean([r['ms_per_set_thin_mc2e4'] for r in tr])),
                                      chi2core_numpy_proxy_1e3=float(np.mean([r['ms_per_set_chi2core_1e3sub'] for r in tr])))
        res['rho2_t_all_counting_weights_mc_s'] = float(nl * res['rho2_ms_per_set']['thin_mc_2e4_measured'] / 1e3)
        res['t2_median_finder'] = t2r['summary_wall']['median']
    except FileNotFoundError:
        pass
    t2_opts['d_plan_8t1'] = 8 * t1_mean
    res['t2_options_mean_s'] = t2_opts
    res['tables'] = {k: table(t1_mean, v) for k, v in t2_opts.items()}
    res['t2_max_C1_mac_1day_at_t1_mean'] = t2max_C1(t1_mean)
    res['t1_max_C1_mac_1day_at_t2_finder'] = None
    if 'a_finder_only' in t2_opts:
        r = t2_opts['a_finder_only'] / t1_mean
        t = 0.1
        while sum(blocks('C1', t + 0.1, r * (t + 0.1)).values()) / MAC_W <= DAY and t < 60:
            t = round(t + 0.1, 1)
        res['t1_max_C1_mac_1day_at_t2_finder'] = t
        res['t2_over_t1'] = r
    res['note'] = ('blocks() from acts/stage4/probes/f3r_campaigns.py (fix R3), Mac 7 workers = 168 CPU-h per 24 h; '
                   'PU event without finder 4.7 s is the plan ESTIMATE (gate G1 measures it)')
    (G2 / 'g2a_campaigns.json').write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != 'tables'}, indent=1))
    for weff in (7.0, 5.5):
        res.setdefault('C1_C4_wall_h_by_effective_workers', {})[str(weff)] = {
            k: round(tb['C1_C4']['cpu_h'] / weff, 1) for k, tb in res['tables'].items()}
        res.setdefault('C1_wall_h_by_effective_workers', {})[str(weff)] = {
            k: round(tb['C1']['cpu_h'] / weff, 1) for k, tb in res['tables'].items()}
    (G2 / 'g2a_campaigns.json').write_text(json.dumps(res, indent=1))
    for k, tb in res['tables'].items():
        print(k, {c: (tb[c]['cpu_h'], tb[c]['wall_mac_h']) for c in tb if c != 'C1_C4'}, 'C1-C4', tb['C1_C4'])
