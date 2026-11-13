"""INV_A2FC_E500 step 9: per-row pass probability under smearing replicas (TT side, frozen modules read-only).
For selected rows of one A2 chunk: K re-draws of the numpy quirk smearing (same hits, same truth, same sigmas, new
Gaussian seeds hseed('inv-resmear', k, ...)) on (a) the A2 PU event (re-run chain, step 8) and (b) the A2FC PU event
(dump, quirk rows removed).  k = -1 is the production numpy smear.  Outcome: in-job eff_fckf at R04/R08/R10/R11/R14.
usage: python inv_a2fc_e500_replica.py F 500 3 <A2 chunk> <scratch dir> <K> [row,row,...]"""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4 import run_g1b as RG  # noqa: E402
from acts.stage4 import run_stage4 as RS  # noqa: E402
from acts.stage4.analysis import common as C  # noqa: E402
from acts.stage4.finder import g1b_tt as GT  # noqa: E402

OUT = TT / 'data/acts_stage4/investigation'
COLS_OUT = (3, 7, 9, 10, 13)


def resmear(S, d, k, spin, m, row):
    meas = d['meas'].copy(); tru = d['tru']
    if k < 0:
        return meas
    g = np.random.default_rng(S.hseed('inv-resmear', k, spin, m, row)).normal(0.0, 1.0, (len(meas), 2))
    sid = meas[:, 0].astype(np.int64)
    btl = S.KIND[sid] == 'BTL'
    R = S.RAD[sid]
    phim = np.arctan2(tru[:, 1], tru[:, 0]) + meas[:, 4] * g[:, 0] / R
    nb = ~btl
    meas[nb, 1] = R[nb] * np.cos(phim[nb]); meas[nb, 2] = R[nb] * np.sin(phim[nb])
    meas[nb, 3] = tru[nb, 2] + meas[nb, 5] * g[nb, 1]
    return meas


def main():
    spin, m, lam, ch, scr, K = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]), \
        int(sys.argv[6])
    S = RG.s4sig(); fz = RS.frozen_inputs()
    key = S.point_key(spin, m, lam)
    P = S.Point(key, RG.index()); slab = S.slab_table(1.0)
    a = [j for j in C.manifest('C1') if j['sample'] == 'A2' and j['spin'] == spin and int(j['m']) == m
         and j['chunk'] == ch][0]
    f = [j for j in C.manifest('A2FC') if j['point'] == key and j['paired_a2_id'] == a['id']][0]
    rows = [int(x) for x in sys.argv[7].split(',')] if len(sys.argv) > 7 else a['rows']
    rows = [r for r in rows if r in a['rows']]
    pa = scr / f'a2pu_{a["id"]}.npz'
    cfg, wcfg = RS.finder_configs(fz, a, False)
    zp = np.load(pa) if pa.exists() else None      # A2 PU re-run (step 8) only where available
    zf = np.load(C.PROD.joinpath(*f['out'].split('/')))
    outp = OUT / f'inv_a2fc_e500_replica_{a["id"]}_L{lam:g}.json'
    res = json.loads(outp.read_text()) if outp.exists() else {}
    for row in rows:
        ie = a['rows'].index(row)
        h, ev, met_true, pv, phimet, tseed = RG.sig_event_inputs(S, P, row, spin, P.m)
        pre = f'dump.{ie}_0.'
        e_fc = np.c_[zf[pre + 'sid'].astype(float), zf[pre + 'xyz'].astype(float), zf[pre + 's01'].astype(float),
                     zf[pre + 'flag'].astype(float), zf[pre + 'vp'].astype(float), zf[pre + 'particle'].astype(float),
                     zf[pre + 'gen'].astype(float), zf[pre + 'vsec'].astype(float), zf[pre + 'dE'].astype(float),
                     zf[pre + 't'].astype(float)]
        t_fc = zf[pre + 'tru'].astype(np.float32)
        q = e_fc[:, 7].astype(np.int64) == GT.SIG_VP
        d = S.digitise(h, ev, P.m, spin, row, lam, slab)
        r = {'A2PU': {}, 'FCPU': {}} if zp is not None else {'FCPU': {}}
        V = [('FCPU', (e_fc[~q], t_fc[~q]))]
        if zp is not None:
            V = [('A2PU', (zp[f'ev{ie}'], zp[f'tru{ie}']))] + V
        for k in range(-1, K):
            mq = resmear(S, d, k, spin, P.m, row)
            for name, (ep, tp) in V:
                ee = np.concatenate([ep, mq]); tt = np.concatenate([tp, d['tru'].astype(np.float32)])
                ee[:, 4:6] = ee[:, 4:6].astype(np.float32).astype(float)
                rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
                Pp = GT.assemble(ee, tt, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=True)
                nqw = int((Pp['H0'][:, 7].astype(np.int64) == GT.SIG_VP).sum())
                _, summ, _ = RG.sig_trial(GT, Pp, nqw, pv, phimet, tseed, cfg, wcfg)
                r[name][str(k)] = [int(summ['eff_fckf'][c]) for c in COLS_OUT] if summ is not None else None
        for name in list(r):
            v = np.array([x for kk, x in r[name].items() if kk != '-1' and x is not None])
            r[name + '_rate'] = v.mean(0).round(3).tolist() if len(v) else None
        res[str(row)] = r
        print(row, {k: (v['-1'] if isinstance(v, dict) else v) for k, v in r.items()}, flush=True)
        outp.write_text(json.dumps(res, indent=0))


if __name__ == '__main__':
    main()
