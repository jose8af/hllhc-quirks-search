"""INV_A2FC_E500 step 4: quirk-hit measurement residuals in the A2FC chain dumps (dump.<ev>_0.{xyz,tru,sid,s01,vp})
vs the stored per-hit sigmas, per detector kind; plus, for the same rows, the Stage-3 quirk SimHits (the numpy-A2
input) vs the A2FC truth (are the quirk SimHits that entered the chain the same ones numpy A2 digitised?).
usage: python inv_a2fc_e500_resid.py F 500 3 [max_jobs]  -> data/acts_stage4/investigation/inv_a2fc_e500_resid_*.json
Read-only."""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C  # noqa: E402
from acts.stage4.code import s4sig as S  # noqa: E402

OUT = TT / 'data/acts_stage4/investigation'


def main():
    spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    mj = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    jobs = sorted((j for j in C.manifest('A2FC') if j['point'] == S.point_key(spin, m, lam)),
                  key=lambda j: j['chunk'])[:mj]
    P = S.Point(S.point_key(spin, m, lam))
    slab = S.slab_table()
    acc = {k: dict(r0=[], r1=[], n=0) for k in ('IT', 'PS', '2S', 'BTL')}
    tru_cmp = dict(n_rows=0, n_rows_same_count=0, max_tru_dist_mm=0.0, n_meas_fc=0, n_meas_numpy=0,
                   n_fc_unmatched=0, frac_merged=None)
    per_row = {}
    for j in jobs:
        with np.load(C.PROD.joinpath(*j['out'].split('/'))) as z:
            evs = sorted({int(k.split('.')[1].split('_')[0]) for k in z.files if k.startswith('dump.')})
            for ie in evs:
                row = j['rows'][ie]
                pre = f'dump.{ie}_0.'
                vp = z[pre + 'vp'].astype(np.int64)
                q = (vp % 1_000_000) == 4000
                xyz = z[pre + 'xyz'][q].astype(float); tru = z[pre + 'tru'][q].astype(float)
                sid = z[pre + 'sid'][q].astype(np.int64); s01 = z[pre + 's01'][q].astype(float)
                kind = S.KIND[sid]
                R = np.hypot(tru[:, 0], tru[:, 1])
                dphi = np.angle(np.exp(1j * (np.arctan2(xyz[:, 1], xyz[:, 0]) - np.arctan2(tru[:, 1], tru[:, 0]))))
                r0 = R * dphi / np.maximum(s01[:, 0], 1e-9); r1 = (xyz[:, 2] - tru[:, 2]) / np.maximum(s01[:, 1], 1e-9)
                for k in acc:
                    mk = kind == k
                    acc[k]['r0'] += r0[mk].tolist(); acc[k]['r1'] += r1[mk].tolist(); acc[k]['n'] += int(mk.sum())
                # numpy-A2 digitisation of the same row (exactly as A2 did, s4sig.digitise)
                h, ev = P.event(row)
                dg = S.digitise(h, ev, P.m, spin, row, lam, slab)
                tn = dg['tru']
                tru_cmp['n_rows'] += 1
                tru_cmp['n_meas_fc'] += int(q.sum()); tru_cmp['n_meas_numpy'] += len(tn)
                tru_cmp['n_rows_same_count'] += int(len(tn) == q.sum())
                if len(tn) and q.any():
                    dd = np.linalg.norm(tru[:, None, :] - tn[None, :, :], axis=2).min(1)
                    tru_cmp['max_tru_dist_mm'] = max(tru_cmp['max_tru_dist_mm'], float(dd.max()))
                    tru_cmp['n_fc_unmatched'] += int((dd > 0.05).sum())
                # IT/PS width of the quirk measurements about truth (rphi), numpy vs FC: same hits
                per_row[row] = dict(n_fc=int(q.sum()), n_np=len(tn),
                                    rms_r0_fc_IT=float(np.sqrt(np.mean(r0[kind == 'IT'] ** 2))) if (kind == 'IT').any() else None)
        print(j['id'], flush=True)
    res = dict(point=f'{spin}{m} L{lam:g}', n_jobs=len(jobs), tru_cmp=tru_cmp, resid={})
    for k, v in acc.items():
        r0 = np.array(v['r0']); r1 = np.array(v['r1'])
        if not len(r0):
            continue
        res['resid'][k] = dict(n=v['n'], rms_r0=float(np.sqrt(np.mean(r0 ** 2))), rms_r1=float(np.sqrt(np.mean(r1 ** 2))),
                               mad_r0=float(1.4826 * np.median(np.abs(r0))), mad_r1=float(1.4826 * np.median(np.abs(r1))),
                               frac_r0_gt5=float(np.mean(np.abs(r0) > 5)), frac_r1_gt5=float(np.mean(np.abs(r1) > 5)),
                               max_abs_r0=float(np.abs(r0).max()), max_abs_r1=float(np.abs(r1).max()))
    p = OUT / f'inv_a2fc_e500_resid_{spin}{m}_L{lam:g}.json'
    p.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
