"""mb_eval.py -- [DP5] evaluation: string (Pythia 8 CP5) vs cluster (Herwig 7) minimum bias at 14 TeV, generator level.
Per |eta| bin (mb_species.ETA_EDGES: 0-1, 1-1.5, 1.5-2.5) and p_T bin (p_T > 0.1 GeV):
  - K/pi and p/pi (charged, particles + antiparticles) in each generator, and (Herwig/Pythia - 1) of each ratio;
  - charged multiplicity per event (all charged final-state particles, p_T > 0.1 GeV) and its Herwig/Pythia ratio;
  - charged p_T spectrum per event, Herwig/Pythia ratio per p_T bin.
Errors: Poisson on counts (events treated as independent, particle correlations within an event ignored: ESTIMATE of the
error, slightly low for multiplicities).  Inputs: JSON files of mb_species.py (summed per generator).
Usage: python3 -I mb_eval.py <out.json> --herwig f1.json [...] --pythia g1.json [...]
"""
import json
import logging
import math
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('mb_eval')


def summed(files):
    tot, nev, meta = None, 0, None
    for f in files:
        d = json.load(open(f))
        nev += d['n_events']
        meta = d
        c = d['counts']
        if tot is None:
            tot = json.loads(json.dumps(c))
        else:
            for k in c:
                for i, row in enumerate(c[k]):
                    tot[k][i] = [a + b for a, b in zip(tot[k][i], row)]
    return tot, nev, meta


def rat(a, b):
    if a <= 0 or b <= 0:
        return None, None
    r = a / b
    return r, r * math.sqrt(1 / a + 1 / b)


def main():
    a = sys.argv
    out = a[1]
    hw = a[a.index('--herwig') + 1:a.index('--pythia')]
    py = a[a.index('--pythia') + 1:]
    H, nh, mh = summed(hw)
    P, npy, mp = summed(py)
    pt, eta = mh['pt_edges'], mh.get('eta_edges', [0.0, 1.0, 1.5, 2.5])
    res = dict(n_events_herwig=nh, n_events_pythia=npy, generators=dict(herwig=mh['generator'], pythia=mp['generator']),
               pt_edges=pt, eta_edges=eta, eta_bins=[])
    for ie in range(len(eta) - 1):
        eb = dict(eta_lo=eta[ie], eta_hi=eta[ie + 1], pt_bins=[])
        nch_h, nch_p = sum(H['ch'][ie]), sum(P['ch'][ie])
        m_h, m_p = nch_h / nh, nch_p / npy
        rr = (m_h / m_p) if m_p else None
        eb['nch_per_event_herwig'] = m_h
        eb['nch_per_event_pythia'] = m_p
        eb['nch_ratio_h_over_p'] = rr
        eb['nch_ratio_err'] = rr * math.sqrt(1 / nch_h + 1 / nch_p) if rr else None
        for ip in range(len(pt) - 1):
            row = dict(pt_lo=pt[ip], pt_hi=pt[ip + 1])
            for sp in ('K', 'p'):
                rh, eh = rat(H[sp][ie][ip], H['pi'][ie][ip])
                rp, ep = rat(P[sp][ie][ip], P['pi'][ie][ip])
                row[f'{sp}/pi_herwig'], row[f'{sp}/pi_herwig_err'] = rh, eh
                row[f'{sp}/pi_pythia'], row[f'{sp}/pi_pythia_err'] = rp, ep
                if rh and rp:
                    row[f'{sp}/pi_rel_diff'] = rh / rp - 1
                    row[f'{sp}/pi_rel_diff_err'] = (rh / rp) * math.hypot(eh / rh, ep / rp)
            ch, cp = H['ch'][ie][ip], P['ch'][ie][ip]
            if ch > 0 and cp > 0:
                s = (ch / nh) / (cp / npy)
                row['ch_spectrum_ratio_h_over_p'] = s
                row['ch_spectrum_ratio_err'] = s * math.sqrt(1 / ch + 1 / cp)
            eb['pt_bins'].append(row)
        res['eta_bins'].append(eb)
        log.info('|eta| %.1f-%.1f: Nch/ev H %.3f P %.3f ratio %s', eta[ie], eta[ie + 1], m_h, m_p, rr)
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
