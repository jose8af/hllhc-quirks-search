"""INV_A2FC_E500 step 10: which column of the A2FC (ACTS) quirk measurements makes the difference?  On the A2FC PU
event (dump), quirk rows built as: ACTS (production), NUMPY (production numpy digitise), and column swaps matched hit
by hit through the truth position (same SimHits): ACTSPOS_NPOTHER (ACTS x,y,z + numpy s0,s1,flag,particle,gen,vsec,dE,t),
NPPOS_ACTSOTHER (numpy x,y,z + ACTS other columns), and single-column swaps of dE and t into NUMPY.  Also dumps the
per-column differences.  usage: python inv_a2fc_e500_cols.py F 500 3 row[,row...]"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4 import run_g1b as RG  # noqa: E402
from acts.stage4 import run_stage4 as RS  # noqa: E402
from acts.stage4.analysis import common as C  # noqa: E402
from acts.stage4.finder import g1b_tt as GT  # noqa: E402

OUT = TT / 'data/acts_stage4/investigation'
COLS_OUT = (3, 7, 9, 10, 13)
NAMES = ['sid', 'x', 'y', 'z', 's0', 's1', 'flag', 'vp', 'particle', 'gen', 'vsec', 'dE', 't']


def main():
    spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    rows = [int(x) for x in sys.argv[4].split(',')]
    S = RG.s4sig(); fz = RS.frozen_inputs()
    key = S.point_key(spin, m, lam)
    P = S.Point(key, RG.index()); slab = S.slab_table(1.0)
    fj = [j for j in C.manifest('A2FC') if j['point'] == key]
    outp = OUT / f'inv_a2fc_e500_cols_{spin}{m}_L{lam:g}.json'
    res = json.loads(outp.read_text()) if outp.exists() else {}
    for row in rows:
        f = [j for j in fj if row in j['rows']][0]; ie = f['rows'].index(row)
        cfg, wcfg = RS.finder_configs(fz, f, False)
        zf = np.load(C.PROD.joinpath(*f['out'].split('/')))
        pre = f'dump.{ie}_0.'
        e = np.c_[zf[pre + 'sid'].astype(float), zf[pre + 'xyz'].astype(float), zf[pre + 's01'].astype(float),
                  zf[pre + 'flag'].astype(float), zf[pre + 'vp'].astype(float), zf[pre + 'particle'].astype(float),
                  zf[pre + 'gen'].astype(float), zf[pre + 'vsec'].astype(float), zf[pre + 'dE'].astype(float),
                  zf[pre + 't'].astype(float)]
        tr = zf[pre + 'tru'].astype(np.float32)
        q = e[:, 7].astype(np.int64) == GT.SIG_VP
        h, ev, met_true, pv, phimet, tseed = RG.sig_event_inputs(S, P, row, spin, P.m)
        d = S.digitise(h, ev, P.m, spin, row, lam, slab)
        nm = d['meas'].copy(); nm[:, 4:6] = nm[:, 4:6].astype(np.float32).astype(float)
        aq = e[q]; atr = tr[q].astype(float)
        dist, ix = cKDTree(atr).query(d['tru'])          # numpy row i <-> ACTS row ix[i]
        aq = aq[ix]; atr_ = tr[q][ix]
        diff = {}
        for c, n in enumerate(NAMES):
            dd = np.abs(nm[:, c] - aq[:, c])
            diff[n] = dict(max=float(dd.max()), n_diff=int((dd > 1e-6 * np.maximum(1, np.abs(nm[:, c]))).sum()))
        diff['dE_ratio_median_act_over_np'] = float(np.median(aq[:, 11] / np.maximum(nm[:, 11], 1e-12)))
        diff['t_diff_median'] = float(np.median(aq[:, 12] - nm[:, 12]))
        diff['flag_values_acts'] = sorted({int(x) for x in aq[:, 6]})
        diff['match_max_dist_mm'] = float(dist.max())
        act_clr = aq.copy(); act_clr[:, 6] = (act_clr[:, 6].astype(np.int64) & ~1).astype(float)
        V = {'ACTS': aq, 'ACTS_noCKF': act_clr, 'NUMPY': nm}
        x = nm.copy(); x[:, 1:4] = aq[:, 1:4]; V['ACTSPOS_NPOTHER'] = x
        x = act_clr.copy(); x[:, 1:4] = nm[:, 1:4]; V['NPPOS_ACTSOTHER'] = x
        x = nm.copy(); x[:, 11] = aq[:, 11]; V['NUMPY_ACTSdE'] = x
        x = nm.copy(); x[:, 12] = aq[:, 12]; V['NUMPY_ACTSt'] = x
        r = dict(job=f['id'], diff=diff)
        for name, qq in V.items():
            ee = np.concatenate([e[~q], qq]); tt = np.concatenate([tr[~q], atr_])
            rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
            Pp = GT.assemble(ee, tt, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=True)
            nqw = int((Pp['H0'][:, 7].astype(np.int64) == GT.SIG_VP).sum())
            _, summ, _ = RG.sig_trial(GT, Pp, nqw, pv, phimet, tseed, cfg, wcfg)
            r[name] = [int(summ['eff_fckf'][c]) for c in COLS_OUT] if summ is not None else None
        res[str(row)] = r
        print(row, {k: v for k, v in r.items() if k != 'diff'}, flush=True)
        print('   diff', json.dumps(diff), flush=True)
        outp.write_text(json.dumps(res, indent=0))


if __name__ == '__main__':
    main()
