"""kref_eval.py -- S2-a validation 2 (published matching limit, like with like): sigma_NLO(Etilde, N_IC = 1) from
loop_quirkE (aMC@NLO fixed order, mu_R = mu_F = m, CT18NLO; job kref-s-fixm) against the fixed-order NLO of Resummino
3.1.2 (`--nlo`; ~e_R pair, same PDF, scale and SM inputs; jobs kref-resummino and, with squarks and gluino decoupled,
kref-resummino-dec), at 200, 500, 1000 GeV.  Criterion (STR §4.14 (a) 2, COM S2-a): within 3 % at each mass.
The LO ratio (identical Born, same inputs) is printed as the set-up check; the NLO/LO K of both codes beside it.
Whether this self-run reference counts as the strategy's reference is the orchestrator's call (EXPLORATION §2.3).
Run (light, stdlib): python3 -I kref_eval.py -> ../../outputs/s2/kref.json
"""
import json
import logging
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('kref_eval')
D = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p2-b-hw-smoke/000')
OUT = Path(__file__).resolve().parents[2] / 'outputs' / 's2'


def resummino(tag):
    try:
        d = json.load(open(D / f'{tag}.json'))
    except FileNotFoundError:
        return None
    return {p['mass']: p['results'] for p in d['points'] if p['mode'] == 'lo_nlo'}, \
           {p['mass']: p['results'].get('NLO+NLL') for p in d['points'] if p['mode'] == 'nll'}


def main():
    ours = {}
    d = json.load(open(D / 'kref-s-fixm.json'))
    for p in d['points']:
        ours.setdefault(p['mass'], {})[p['order']] = (p['sigma_pb'], p['err_pb'])
    res = {}
    for tag in ('kref-resummino', 'kref-resummino-dec'):
        r = resummino(tag)
        if r is None:
            continue
        fo, nll = r
        rows, ok_all = [], True
        for m in sorted(ours):
            if m not in fo:
                continue
            o, f = ours[m], fo[m]
            lo_r = o['LO'][0] / f['LO'][0]
            nlo_r = o['NLO'][0] / f['NLO'][0]
            nlo_e = nlo_r * math.hypot(o['NLO'][1] / o['NLO'][0], f['NLO'][1] / f['NLO'][0])
            ok = abs(nlo_r - 1) <= 0.03
            ok_all &= ok
            row = dict(mass=m, sigma_nlo_ours_pb=o['NLO'][0], sigma_nlo_resummino_pb=f['NLO'][0], ratio_nlo=round(nlo_r, 5),
                       ratio_nlo_err=round(nlo_e, 5), ratio_lo=round(lo_r, 5), K_ours=round(o['NLO'][0] / o['LO'][0], 4),
                       K_resummino=round(f['NLO'][0] / f['LO'][0], 4), within_3pct=ok)
            if nll and nll.get(m):
                row['nlonll_over_nlo_resummino'] = round(nll[m][0] / f['NLO'][0], 5)
            rows.append(row)
            log.info('%s %s', tag, row)
        res[tag] = dict(rows=rows, verdict='PASS' if rows and ok_all else ('FAIL' if rows else 'INCOMPLETE'))
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(dict(criterion='|sigma_NLO(ours)/sigma_NLO(ref) - 1| <= 3 % at each mass (STR §4.14 (a) 2)',
                   reference='Resummino 3.1.2 --nlo, self-run (see EXPLORATION §2.3)', results=res),
              open(OUT / 'kref.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
