"""p1_eval.py -- P1 readings (STR §4.15, COM P1-a/b/c) from the p2-b-p1-run JSON outputs, pre-declared criteria:
P1-b B*-off (paired): per event r = c_on - c_off (c from Delta_s at B0 and B0/2).
     5 keV: "B* attribution supported" if the paired median of (on - off) is positive at >= 3 sigma overall AND for
            k_B >= 6 (sigma from a paired bootstrap, 2000 resamples).
     1 keV: the paired difference must be compatible with zero (|median| <= 2 sigma).
P1-c population estimator at 1 keV: paired median of (c2 - c_ev) over events per point, paired bootstrap (2000);
     criterion |median| / median(c_ev) <= 1.5 % AND |median| <= 2 sigma, at all five points.
P1-a floor test 2: c_k = (Delta_s(B/k) k / Delta_s(B) - 1)/ln k per event and kernel (k = 2, 2.5, 4, 20); reading: if the
     excess is the double-precision floor, the 44-bit kernel's Delta_c at k = 2.5 reproduces the nominal kernel's Delta_c
     at k = 20 (two-sample KS test p > 0.05), Delta_c = c_k - c_ev.  The dd (double-double mdot) kernel is reported beside.
Events with any run status != 1 or a non-finite Delta_s are dropped and counted.
Usage: python p1_eval.py <run_dir> <out.json>   (TT env: numpy, scipy)
"""
import glob
import json
import logging
import math
import os
import sys

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p1_eval')
NB = 2000


def boot_median(x, rng):
    x = np.asarray(x)
    if len(x) < 2:
        return float('nan')
    return float(np.std([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(NB)]))


def load(pattern):
    ev = []
    for f in sorted(glob.glob(pattern)):
        ev += json.load(open(f))['events']
    return ev


def good_bstar(e, arms):
    return all(e.get(f'{a}_status') == [1, 1] and math.isfinite(e.get(f'c_{a}', float('nan'))) for a in arms)


def main():
    d, out = sys.argv[1], sys.argv[2]
    rng = np.random.default_rng(20261116)
    res = {}
    # P1-b at 5 keV
    for p in ('e500', 'e1000'):
        ev = load(os.path.join(d, f'bstar5-{p}-*.json'))
        ok = [e for e in ev if good_bstar(e, ('on', 'off'))]
        r = np.array([e['c_on'] - e['c_off'] for e in ok])
        kb = np.array([e['k_B'] for e in ok])
        ent = dict(n_events=len(ev), n_used=len(ok))
        for lab, m in (('all', np.ones(len(r), bool)), ('kB_ge6', kb >= 6), ('kB_lt6', kb < 6)):
            if m.sum() >= 2:
                med, s = float(np.median(r[m])), boot_median(r[m], rng)
                ent[lab] = dict(n=int(m.sum()), paired_median=med, sigma=s, signif=med / s if s > 0 else None)
        res[f'P1b_5keV_{p}'] = ent
    allr = []
    for p in ('e500', 'e1000'):
        for e in load(os.path.join(d, f'bstar5-{p}-*.json')):
            if good_bstar(e, ('on', 'off')):
                allr.append((e['c_on'] - e['c_off'], e['k_B']))
    if allr:
        r = np.array([x[0] for x in allr]); kb = np.array([x[1] for x in allr])
        tot = {}
        for lab, m in (('all', np.ones(len(r), bool)), ('kB_ge6', kb >= 6)):
            med, s = float(np.median(r[m])), boot_median(r[m], rng)
            tot[lab] = dict(n=int(m.sum()), paired_median=med, sigma=s, signif=med / s if s > 0 else None)
        tot['reading'] = ('B* attribution supported' if all(tot[k]['signif'] and tot[k]['signif'] >= 3 for k in ('all', 'kB_ge6'))
                          else 'B* attribution not supported at 3 sigma')
        res['P1b_5keV_combined'] = tot
    # P1-b at 1 keV and P1-c at 1 keV (same events)
    pc_all = True
    for p in ('e200', 'e500', 'e1000', 'e1500', 's500'):
        ev = load(os.path.join(d, f'bstar1-{p}.json'))
        okb = [e for e in ev if good_bstar(e, ('on', 'off'))]
        okc = [e for e in ev if good_bstar(e, ('on',)) and math.isfinite(e['c_ev'])]
        ent = dict(n_events=len(ev))
        if len(okb) >= 2:
            r = np.array([e['c_on'] - e['c_off'] for e in okb])
            med, s = float(np.median(r)), boot_median(r, rng)
            ent['P1b_1keV'] = dict(n=len(okb), paired_median=med, sigma=s, compatible_zero_2sigma=abs(med) <= 2 * s)
        if len(okc) >= 2:
            r = np.array([e['c_on'] - e['c_ev'] for e in okc])
            cev = float(np.median([e['c_ev'] for e in okc]))
            med, s = float(np.median(r)), boot_median(r, rng)
            ok = abs(med) / cev <= 0.015 and abs(med) <= 2 * s
            pc_all &= ok
            ent['P1c'] = dict(n=len(okc), paired_median_c2_minus_cev=med, sigma=s, median_c_ev=cev, rel=med / cev,
                              passes=ok)
        res[f'1keV_{p}'] = ent
    res['P1c_verdict'] = 'PASS' if pc_all else 'FAIL'
    # P1-a floor test 2 and dd diagnostic
    def ck(ds, fr):
        out = {}
        for k, f in ((2, 0.5), (2.5, 0.4), (4, 0.25), (20, 0.05)):
            if f in fr and ds[0] > 0:
                out[k] = (ds[fr.index(f)] * k / ds[0] - 1) / math.log(k)
        return out
    fl = {}
    for p in ('e500', 'e1000'):
        per = {}
        for kern in ('nominal', 't44', 'dd'):
            ev = load(os.path.join(d, f'floor-{p}-{kern}.json'))
            rows = []
            for e in ev:
                if all(s == 1 for s in e['status']) and all(math.isfinite(x) and x > 0 for x in e['ds']):
                    c = ck(e['ds'], e['fr'])
                    rows.append({str(k): c[k] - e['c_ev'] for k in c})
            per[kern] = rows
            fl[f'{p}_{kern}'] = {k: dict(n=len(rows), median=float(np.median([r[k] for r in rows])) if rows else None)
                                 for k in ('2', '2.5', '4', '20')}
        if per['nominal'] and per['t44']:
            from scipy.stats import ks_2samp
            a = [r['20'] for r in per['nominal']]; b = [r['2.5'] for r in per['t44']]
            ks = ks_2samp(a, b)
            fl[f'{p}_test2'] = dict(nominal_dc20_median=float(np.median(a)), t44_dc2p5_median=float(np.median(b)),
                                    ks_p=float(ks.pvalue), reading='floor (same distribution)' if ks.pvalue > 0.05 else
                                    'not the floor pattern (distributions differ)')
    res['P1a_floor'] = fl
    json.dump(res, open(out, 'w'), indent=1)
    log.info('%s', json.dumps(res, indent=1)[:3000])


if __name__ == '__main__':
    main()
