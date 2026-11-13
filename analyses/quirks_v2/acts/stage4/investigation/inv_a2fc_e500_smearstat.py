"""INV_A2FC_E500 step 11: statistics of the ACTS quirk-measurement smearing in the A2FC dumps of one point:
normalised residuals (r0 = R dphi / s0, r1 = dz / s1) per kind -- shape (fraction |r| < 0.5, kurtosis, distinct values)
and the per-event coherence sqrt(n) * mean(r) (variance 1 if independent per hit, n if fully coherent); also for PU.
usage: python inv_a2fc_e500_smearstat.py F 500 3"""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C  # noqa: E402
from acts.stage4.code import s4sig as S  # noqa: E402


def main():
    spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    jobs = [j for j in C.manifest('A2FC') if j['point'] == S.point_key(spin, m, lam)]
    acc = {}
    for j in jobs:
        with np.load(C.PROD.joinpath(*j['out'].split('/'))) as z:
            for ie in range(j['n_events']):
                p = f'dump.{ie}_0.'
                sid = z[p + 'sid'].astype(int); xyz = z[p + 'xyz']; tru = z[p + 'tru'].astype(float)
                s01 = z[p + 's01'].astype(float); vp = z[p + 'vp'].astype(np.int64)
                q = vp % 1_000_000 == 4000
                R = np.hypot(tru[:, 0], tru[:, 1])
                dphi = np.angle(np.exp(1j * (np.arctan2(xyz[:, 1], xyz[:, 0]) - np.arctan2(tru[:, 1], tru[:, 0]))))
                r0 = R * dphi / s01[:, 0]; r1 = (xyz[:, 2] - tru[:, 2]) / s01[:, 1]
                for k in ('IT', 'PS', '2S'):
                    for nm, mk in (('quirk', q), ('pu', ~q)):
                        mm = mk & (S.KIND[sid] == k)
                        if nm == 'pu':
                            mm &= np.random.default_rng(ie).random(len(mm)) < 0.02     # 2 % PU subsample
                        a = acc.setdefault(f'{nm}_{k}', dict(r0=[], r1=[], c0=[], c1=[]))
                        if mm.sum():
                            a['r0'] += r0[mm].tolist(); a['r1'] += r1[mm].tolist()
                            a['c0'].append(r0[mm].mean() * np.sqrt(mm.sum())); a['c1'].append(r1[mm].mean() * np.sqrt(mm.sum()))
    out = {}
    for k, a in acc.items():
        o = {}
        for c in ('r0', 'r1'):
            r = np.array(a[c])
            o[c] = dict(n=len(r), rms=round(float(r.std()), 3), frac_lt05=round(float(np.mean(np.abs(r) < 0.5)), 3),
                        kurt=round(float(np.mean(r ** 4) / np.mean(r ** 2) ** 2), 2),
                        frac_gt2=round(float(np.mean(np.abs(r) > 2)), 4))
        o['coh_var_r0'] = round(float(np.var(a['c0'])), 2); o['coh_var_r1'] = round(float(np.var(a['c1'])), 2)
        out[k] = o
        print(k, o)
    print('Gaussian: frac|r|<0.5 = 0.383, kurt 3, frac|r|>2 = 0.0455; uniform: 0.289, 1.8, 0')
    (TT / f'data/acts_stage4/investigation/inv_a2fc_e500_smearstat_{spin}{m}_L{lam:g}.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
