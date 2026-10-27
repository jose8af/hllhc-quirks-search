"""INV_A2FC_E500 step 1: paired per-rung comparison A2 (numpy, C12_v1) vs A2FC (full chain, C12FC_v1) on the stored
per-row pass matrices (signal_rows_a2.npz) at the 9 V4-6 revert points.  Read-only.
-> data/acts_stage4/investigation/inv_a2fc_e500_paired.json"""
import json
import sys
from math import comb
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C  # noqa: E402

AN = TT / 'data/acts_stage4/analysis'
OUT = TT / 'data/acts_stage4/investigation/inv_a2fc_e500_paired.json'
REV = [('F', 200, 3), ('F', 200, 5), ('F', 500, 3), ('F', 500, 5), ('F', 1000, 3), ('F', 1000, 5), ('F', 1500, 3),
       ('F', 1500, 5), ('S', 500, 5)]
EXTRA = [('S', 500, 3), ('F', 500, 2)]          # non-revert controls (must be identical)
FBN = list(C.RUNGS[17:37])


def mcnemar(b, c):
    """exact two-sided McNemar p (binomial on discordant pairs)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def main():
    A = np.load(AN / 'C12_v1/signal_rows_a2.npz', allow_pickle=True)
    F = np.load(AN / 'C12FC_v1/signal_rows_a2.npz', allow_pickle=True)
    res = {}
    for sp, m, lam in REV + EXTRA:
        k = f'A2|{sp}|{m}|{lam}|BM'
        ra, rf = A[k + '|rows'], F[k + '|rows']
        oa, of = np.argsort(ra), np.argsort(rf)
        same_rows = bool(np.array_equal(ra[oa], rf[of]))
        La, Lf = A[k + '|L'][oa], F[k + '|L'][of]
        Ba, Bf = A[k + '|FB'][oa], F[k + '|FB'][of]
        ent = dict(n=int(len(ra)), same_rows=same_rows, row_order_equal=bool(np.array_equal(ra, rf)),
                   identical_L=bool(np.array_equal(La, Lf)), ladder={}, fb={})
        for i, nm in enumerate(C.LADDER_NAMES):
            a, f = La[:, i], Lf[:, i]
            b, c = int((a & ~f).sum()), int((~a & f).sum())
            ent['ladder'][nm] = dict(k_a2=int(a.sum()), k_fc=int(f.sum()), both=int((a & f).sum()), a2_only=b,
                                     fc_only=c, p_mcnemar=mcnemar(b, c))
        for i, nm in enumerate(FBN):
            a, f = Ba[:, i], Bf[:, i]
            b, c = int((a & ~f).sum()), int((~a & f).sum())
            ent['fb'][nm] = dict(k_a2=int(a.sum()), k_fc=int(f.sum()), both=int((a & f).sum()), a2_only=b,
                                 fc_only=c, p_mcnemar=mcnemar(b, c))
        # conditional step losses: among rows passing rung i-1 in BOTH, fraction failing rung i
        ent['rows_R14_a2'] = [int(x) for x in ra[oa][La[:, 13]]]
        ent['rows_R14_fc'] = [int(x) for x in rf[of][Lf[:, 13]]]
        ent['rows_R04_a2'] = [int(x) for x in ra[oa][La[:, 3]]]
        ent['rows_R04_fc'] = [int(x) for x in rf[of][Lf[:, 3]]]
        res[k] = ent
    OUT.write_text(json.dumps(res, indent=1))
    # compact print
    hdr = ['R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14']
    for k, e in res.items():
        print(k, 'n', e['n'], 'same_rows', e['same_rows'], 'order', e['row_order_equal'], 'identical', e['identical_L'])
        s = []
        for i in range(3, 14):
            x = e['ladder'][C.LADDER_NAMES[i]]
            s.append(f"{C.LADDER_NAMES[i][:3]} {x['k_a2']}->{x['k_fc']} ({x['a2_only']}/{x['fc_only']},p={x['p_mcnemar']:.2g})")
        print('   ' + ' | '.join(s))
        fb3 = e['fb'][FBN[3]]
        print('   ', FBN[3], f"{fb3['k_a2']}->{fb3['k_fc']} ({fb3['a2_only']}/{fb3['fc_only']}, p={fb3['p_mcnemar']:.2g})")


if __name__ == '__main__':
    main()
