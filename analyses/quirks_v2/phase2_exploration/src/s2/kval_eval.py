"""kval_eval.py -- S2-a validation 1 (model identity), channel (ii) Sebastian.
Fixed-order LO of loop_quirkE (aMC@NLO, fixed_order=ON, order=LO) against the tree-level v1 UFO (MadEvent LO), both at
mu_R = mu_F = m (fixed), CT18NLO (lhaid 14400), 14 TeV, N_IC = 1 (campaign p2-b-s2-kval).
Criterion (STR §4.14 (a) 1, COM S2-a): |z| < 3 AND |relative difference| < 0.5 %.
z = (sigma_FO - sigma_tree) / sqrt(err_FO^2 + err_tree^2 + r^2), r = half a unit of the 4th significant digit of the
aMC@NLO summary (summary.txt prints 4 digits), added in quadrature as a rounding error.
Run (light, stdlib): python3 -I kval_eval.py -> ../../outputs/s2/kval.json
"""
import json
import logging
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('kval_eval')
D = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p2-b-s2-kval/000')
OUT = Path(__file__).resolve().parents[2] / 'outputs' / 's2'


def main():
    rows = []
    for m in (200, 500, 1000):
        try:
            fo = json.load(open(D / f'kval-folo-e-m{m}.json'))['points'][0]
            tr = json.load(open(D / f'kval-tree-e-m{m}.json'))['points'][0]
        except FileNotFoundError:
            log.info('m=%d: missing', m)
            continue
        s1, e1 = fo['sigma_pb'], fo['err_pb']
        r = 0.5 * 10 ** (math.floor(math.log10(abs(s1))) - 3)
        s2, e2 = tr['sigma_log_pb'] or tr['sigma_pb'], tr['err_pb']
        z = (s1 - s2) / math.sqrt(e1 ** 2 + e2 ** 2 + r ** 2)
        rel = s1 / s2 - 1
        ok = abs(z) < 3 and abs(rel) < 0.005
        rows.append(dict(mass=m, sigma_fo_lo_pb=s1, err_fo=e1, rounding=r, sigma_tree_pb=s2, err_tree=e2, z=round(z, 3),
                         rel=round(rel, 6), verdict='PASS' if ok else 'FAIL'))
        log.info('%s', rows[-1])
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(dict(criterion='|z| < 3 and |rel| < 0.5 % (STR §4.14 (a) 1)', campaign='p2-b-s2-kval', rows=rows,
                   verdict='PASS' if rows and len(rows) == 3 and all(x['verdict'] == 'PASS' for x in rows) else
                   ('FAIL' if any(x['verdict'] == 'FAIL' for x in rows) else 'INCOMPLETE')),
              open(OUT / 'kval.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
