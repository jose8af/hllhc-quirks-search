"""kdy_eval.py -- S2-a validation 3 (process independence, differential): K(M) = dsigma_NLO/dM / dsigma_LO/dM in bins of
the pair invariant mass, for p p > e+ e- (DY) and for the quirk pairs E and Etilde, aMC@NLO fixed order, loop_quirkE,
mu_R = mu_F = M(pair) (user scale 10), CT18NLO, campaign p2-b-s2-kdy.
Criterion (STR §4.14 (a) 3, COM S2-a): per bin, |K_E(M) - K_DY(M)| <= max(2 % of K_DY, 3 sigma), sigma from the
integration errors of the four histograms (independent runs).  K_E/K_Etilde is reported (v1 'spin-independent' test).
Bins with an LO entry below 1e-3 of the histogram maximum are not evaluated (no events in the kinematic range).
Run (light, stdlib): python3 -I kdy_eval.py -> ../../outputs/s2/kdy.json
"""
import json
import logging
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('kdy_eval')
D = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p2-b-s2-kdy/000')
OUT = Path(__file__).resolve().parents[2] / 'outputs' / 's2'


def khist(tag):
    d = json.load(open(D / f'{tag}.json'))
    h = {p['order']: p['mpair_hist'] for p in d['points']}
    lo, nlo = h['LO'], h['NLO']
    vmax = max(b['val'] for b in lo)
    rows = []
    for a, b in zip(lo, nlo):
        if a['val'] <= 1e-3 * vmax or a['val'] <= 0:
            rows.append(dict(lo=a['lo'], hi=a['hi'], K=None))
            continue
        k = b['val'] / a['val']
        e = k * math.hypot(b['err'] / b['val'], a['err'] / a['val'])
        rows.append(dict(lo=a['lo'], hi=a['hi'], K=k, err=e))
    return rows


def compare(a, b):
    out, ok_all, n = [], True, 0
    for x, y in zip(a, b):
        if x['K'] is None or y['K'] is None:
            out.append(dict(lo=x['lo'], hi=x['hi'], evaluated=False))
            continue
        d = x['K'] - y['K']
        s = math.hypot(x['err'], y['err'])
        tol = max(0.02 * y['K'], 3 * s)
        ok = abs(d) <= tol
        ok_all &= ok
        n += 1
        out.append(dict(lo=x['lo'], hi=x['hi'], K_a=round(x['K'], 4), K_b=round(y['K'], 4), diff=round(d, 4),
                        sigma=round(s, 4), tol=round(tol, 4), pass_=ok))
    return out, ok_all, n


def main():
    res = {}
    for label, a, b in (('E200_vs_DY', 'kdy-e200', 'kdy-dy400'), ('Etilde200_vs_DY', 'kdy-s200', 'kdy-dy400'),
                        ('E500_vs_DY', 'kdy-e500', 'kdy-dy1000'), ('E200_vs_Etilde200', 'kdy-e200', 'kdy-s200')):
        try:
            rows, ok, n = compare(khist(a), khist(b))
        except FileNotFoundError as ex:
            log.info('%s: missing %s', label, ex)
            continue
        res[label] = dict(bins=rows, n_evaluated=n, verdict=('PASS' if ok else 'FAIL') if n else 'NOT EVALUABLE')
        log.info('%s: %s (%d bins)', label, res[label]['verdict'], n)
    OUT.mkdir(parents=True, exist_ok=True)
    main_v = [res[k]['verdict'] for k in ('E200_vs_DY', 'E500_vs_DY') if k in res]
    json.dump(dict(criterion='per bin |K_E - K_DY| <= max(2 % K_DY, 3 sigma)', campaign='p2-b-s2-kdy', results=res,
                   verdict_validation3=('PASS' if main_v and all(v == 'PASS' for v in main_v) and len(main_v) == 2 else
                                        'FAIL' if 'FAIL' in main_v else 'INCOMPLETE')),
              open(OUT / 'kdy.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
