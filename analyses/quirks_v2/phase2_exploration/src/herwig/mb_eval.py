"""mb_eval.py -- [DP5] evaluation: charged K/pi and p/pi per p_T bin (|eta| < 2.5) in Herwig 7 (cluster) and Pythia 8
CP5 (string) minimum bias at 14 TeV, and the relative difference (Herwig/Pythia - 1) of each ratio, with Poisson errors.
Inputs: the JSON files of mb_species.py (several per generator are summed).  Generator level only; no detector.
Usage: python3 -I mb_eval.py <out.json> --herwig f1.json [f2 ...] --pythia g1.json [g2 ...]
"""
import json
import logging
import math
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('mb_eval')


def summed(files):
    tot, nev, edges = None, 0, None
    for f in files:
        d = json.load(open(f))
        nev += d['n_events']
        edges = d['pt_edges']
        if tot is None:
            tot = {k: list(v) for k, v in d['counts'].items()}
        else:
            for k, v in d['counts'].items():
                tot[k] = [a + b for a, b in zip(tot[k], v)]
    return tot, nev, edges


def ratio(a, b):
    if a == 0 or b == 0:
        return None, None
    r = a / b
    return r, r * math.sqrt(1 / a + 1 / b)


def main():
    a = sys.argv
    out = a[1]
    hw = a[a.index('--herwig') + 1:a.index('--pythia')]
    py = a[a.index('--pythia') + 1:]
    H, nh, edges = summed(hw)
    P, npy, _ = summed(py)
    rows = []
    for i in range(len(edges) - 1):
        row = dict(pt_lo=edges[i], pt_hi=edges[i + 1])
        for sp in ('K', 'p'):
            rh, eh = ratio(H[sp][i], H['pi'][i])
            rp, ep = ratio(P[sp][i], P['pi'][i])
            row[f'{sp}/pi_herwig'] = rh
            row[f'{sp}/pi_herwig_err'] = eh
            row[f'{sp}/pi_pythia'] = rp
            row[f'{sp}/pi_pythia_err'] = ep
            if rh and rp:
                d = rh / rp - 1
                row[f'{sp}/pi_rel_diff'] = d
                row[f'{sp}/pi_rel_diff_err'] = (rh / rp) * math.hypot(eh / rh, ep / rp)
        for sp in ('pi', 'K', 'p'):
            row[f'n_{sp}_per_event_herwig'] = H[sp][i] / nh if nh else None
            row[f'n_{sp}_per_event_pythia'] = P[sp][i] / npy if npy else None
        rows.append(row)
        log.info('%s', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})
    json.dump(dict(n_events_herwig=nh, n_events_pythia=npy, bins=rows, herwig_files=hw, pythia_files=py,
                   tag='generator level, statistical errors only'), open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
