"""INV_A2FC_E500 step 5: do the quirk hits stored in the A2 (numpy) hit records of a (spin, m, Lambda) point equal the
deterministic s4sig.digitise output of that row and Lambda (BM)?  Also tests the other Lambdas of the same row and
reports which Lambda each stored quirk hit belongs to.  Read-only.
usage: python inv_a2fc_e500_a2check.py F 500 3 [max_jobs]"""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C  # noqa: E402
from acts.stage4.analysis import hitrec as HR  # noqa: E402
from acts.stage4.code import s4sig as S  # noqa: E402

OUT = TT / 'data/acts_stage4/investigation'


def main():
    spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    mj = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    jobs = sorted((j for j in C.manifest('C1') if j['sample'] == 'A2' and j['spin'] == spin and int(j['m']) == m),
                  key=lambda j: j['chunk'])[:mj]
    lams = [float(x) for x in jobs[0]['lams']]
    slab = S.slab_table()
    pts = {l: S.Point(S.point_key(spin, m, l)) for l in lams}
    res = dict(point=f'{spin}{m} L{lam:g}', lams=lams, n_rows=0, n_q_hits=0, n_match_target=0,
               n_match_other={}, n_unmatched=0, rows_bad=[])
    for j in jobs:
        d = C.load_npz(C.PROD.joinpath(*j['out'].split('/')), prefix=('sig.', 'hit.', 'trials.'))
        tab = d['sig.tab']; ci = {str(c): i for i, c in enumerate(d['sig.cols'])}
        q_by_trial = {}
        for k, tr, cidx, h in HR.iter_records(d):
            q = (d['hit.INT'][h].astype(np.int64) % 1_000_000) == C.SIG_VP
            q_by_trial.setdefault(tr, set()).update(int(x) for x in h[q])
        for e in range(len(tab)):
            if abs(float(tab[e, ci['lam']]) - lam) > 1e-9:
                continue
            row = int(tab[e, ci['row']]); ti = int(d['sig.trial'][e])
            hs = sorted(q_by_trial.get(ti, ()))
            if not hs:
                continue
            res['n_rows'] += 1
            X = d['hit.xyz'][hs].astype(float)
            ref = {}
            for l, P in pts.items():
                hh, ev = P.event(row)
                ref[l] = S.digitise(hh, ev, P.m, spin, row, l, slab)['meas'][:, 1:4]
            bad = 0
            for x in X:
                dl = {l: float(np.linalg.norm(r - x, axis=1).min()) if len(r) else 1e9 for l, r in ref.items()}
                res['n_q_hits'] += 1
                if dl[lam] < 1e-3:
                    res['n_match_target'] += 1
                else:
                    best = min(dl, key=dl.get)
                    if dl[best] < 1e-3:
                        res['n_match_other'][f'{best:g}'] = res['n_match_other'].get(f'{best:g}', 0) + 1
                    else:
                        res['n_unmatched'] += 1
                        res.setdefault('unmatched_detail', []).append(
                            [row, round(float(np.hypot(x[0], x[1])), 2), round(float(x[2]), 2),
                             {f'{a:g}': round(b, 3) for a, b in dl.items()}])
                    bad += 1
            if bad:
                res['rows_bad'].append([row, bad, len(X)])
        print(j['id'], res['n_q_hits'], res['n_match_target'], flush=True)
    (OUT / f'inv_a2fc_e500_a2check_{spin}{m}_L{lam:g}.json').write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != 'rows_bad'}), 'rows_bad', res['rows_bad'][:10])


if __name__ == '__main__':
    main()
