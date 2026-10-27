"""INV_A2FC_E500 step 8: re-run the A2 PU-only chain of one A2 job (run_chain.py pu, A2 job seed, A2 event seeds --
exactly as run_g1b 'a2') and cross the PU / quirk ingredients of A2 and A2FC on the same rows (TT side, frozen modules
read-only):
  A2REP   : A2 PU (re-run) + numpy quirks                    -> must reproduce the stored A2 flags (validation)
  A2PU_FCQ: A2 PU + the A2FC ACTS quirk measurements (CKF bit cleared)
  A2PU_FCF: A2 PU positions, but the CKF flags (bit0) of the A2FC event (matched by sid/truth/barcode) + numpy quirks
  FCPU_A2F: A2FC PU positions with the A2 CKF flags + numpy quirks
  FC      : the A2FC dump as is (validation vs the stored A2FC flags)
Also counts PU measurements whose CKF flag differs between A2 and A2FC, in total and inside the matched candidate band.
usage: python inv_a2fc_e500_a2pu.py F 500 3 <A2 chunk> <scratch dir>"""
import json
import sys
import time
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


def f32s(e):
    e = e.copy(); e[:, 4:6] = e[:, 4:6].astype(np.float32).astype(float); return e


def keys(e, tr):
    t = np.round(np.asarray(tr, np.float32).astype(float), 3)
    return [(int(a), b0, b1, b2, int(p), int(v)) for a, (b0, b1, b2), p, v in zip(e[:, 0], t, e[:, 8], e[:, 7])]


def main():
    spin, m, lam, ch, scr = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5])
    S = RG.s4sig(); fz = RS.frozen_inputs()
    key = S.point_key(spin, m, lam)
    P = S.Point(key, RG.index()); slab = S.slab_table(1.0)
    a = [j for j in C.manifest('C1') if j['sample'] == 'A2' and j['spin'] == spin and int(j['m']) == m
         and j['chunk'] == ch][0]
    f = [j for j in C.manifest('A2FC') if j['point'] == key and j['paired_a2_id'] == a['id']][0]
    cfg, wcfg = RS.finder_configs(fz, a, False)
    cfg_f, wcfg_f = RS.finder_configs(fz, f, False)
    same_cfg = (vars(wcfg) == vars(wcfg_f)) and (repr(cfg) == repr(cfg_f))
    scr.mkdir(parents=True, exist_ok=True)
    tmp = scr / f'a2pu_{a["id"]}.npz'
    t0 = time.time()
    if not tmp.exists():
        mm = float(P.m)
        seeds = [S.hseed('sigpu', spin, mm, r, mod=2 ** 62) for r in a['rows']]
        sf = scr / f'seeds_{a["id"]}.json'; sf.write_text(json.dumps(seeds))
        RG.chain(a, tmp, ['pu', tmp, len(a['rows']), a['seed'], '--event-seeds', sf])
    t_chain = time.time() - t0
    zp = np.load(tmp); zf = np.load(C.PROD.joinpath(*f['out'].split('/')))
    za = np.load(C.PROD.joinpath(*a['out'].split('/')))
    sa = {int(za['sig.tab'][e, 0]): np.unpackbits(za['sig.eff_fckf'][e])[:C.NR].astype(bool)
          for e in range(len(za['sig.tab'])) if za['sig.tab'][e, 1] == lam}
    sf_ = {int(zf['sig.tab'][e, 0]): np.unpackbits(zf['sig.eff_fckf'][e])[:C.NR].astype(bool)
           for e in range(len(zf['sig.tab']))}
    res = dict(a2_job=a['id'], fc_job=f['id'], same_finder_cfg=bool(same_cfg), t_chain_s=round(t_chain, 1), rows={})
    for ie, row in enumerate(a['rows']):
        h, ev, met_true, pv, phimet, tseed = RG.sig_event_inputs(S, P, row, spin, P.m)
        e_pu = zp[f'ev{ie}']; t_pu = zp[f'tru{ie}']
        pre = f'dump.{ie}_0.'
        e_fc = np.c_[zf[pre + 'sid'].astype(float), zf[pre + 'xyz'].astype(float), zf[pre + 's01'].astype(float),
                     zf[pre + 'flag'].astype(float), zf[pre + 'vp'].astype(float), zf[pre + 'particle'].astype(float),
                     zf[pre + 'gen'].astype(float), zf[pre + 'vsec'].astype(float), zf[pre + 'dE'].astype(float),
                     zf[pre + 't'].astype(float)]
        t_fc = zf[pre + 'tru'].astype(np.float32)
        q = e_fc[:, 7].astype(np.int64) == GT.SIG_VP
        d = S.digitise(h, ev, P.m, spin, row, lam, slab)
        # PU CKF flag maps (truth-keyed)
        ka = keys(e_pu, t_pu); kf = keys(e_fc[~q], t_fc[~q])
        fa = dict(zip(ka, (e_pu[:, 6].astype(np.int64) & 1)))
        ff = dict(zip(kf, (e_fc[~q, 6].astype(np.int64) & 1)))
        common = set(fa) & set(ff)
        n_ckf_a2 = int(sum(fa[k] for k in common)); n_ckf_fc = int(sum(ff[k] for k in common))
        n_a2_not_fc = int(sum(1 for k in common if fa[k] and not ff[k]))
        n_fc_not_a2 = int(sum(1 for k in common if ff[k] and not fa[k]))
        e_pu_fcf = e_pu.copy()
        e_pu_fcf[:, 6] = [(int(x) & ~1) | int(ff.get(k, int(x) & 1)) for x, k in zip(e_pu[:, 6], ka)]
        e_fcpu = e_fc[~q].copy()
        e_fcpu[:, 6] = [(int(x) & ~1) | int(fa.get(k, int(x) & 1)) for x, k in zip(e_fcpu[:, 6], kf)]
        qfc = e_fc[q].copy(); qfc[:, 6] = (qfc[:, 6].astype(np.int64) & ~1).astype(float)
        V = {
            'A2REP': (np.concatenate([e_pu, d['meas']]), np.concatenate([t_pu, d['tru'].astype(np.float32)])),
            'A2PU_FCQ': (f32s(np.concatenate([e_pu, qfc])), np.concatenate([t_pu, t_fc[q]])),
            'A2PU_FCF': (np.concatenate([e_pu_fcf, d['meas']]), np.concatenate([t_pu, d['tru'].astype(np.float32)])),
            'FCPU_A2F': (f32s(np.concatenate([e_fcpu, d['meas']])), np.concatenate([t_fc[~q], d['tru'].astype(np.float32)])),
            'FC': (e_fc, t_fc),
        }
        r = dict(stored_a2=[int(sa[row][c]) for c in COLS_OUT], stored_fc=[int(sf_[row][c]) for c in COLS_OUT],
                 pu_common=len(common), pu_only_a2=len(set(fa) - set(ff)), pu_only_fc=len(set(ff) - set(fa)),
                 ckf_flag_a2=n_ckf_a2, ckf_flag_fc=n_ckf_fc, ckf_a2_not_fc=n_a2_not_fc, ckf_fc_not_a2=n_fc_not_a2)
        for name, (ee, tt) in V.items():
            rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
            Pp = GT.assemble(ee, tt, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=True)
            nqw = int((Pp['H0'][:, 7].astype(np.int64) == GT.SIG_VP).sum())
            try:
                _, summ, _ = RG.sig_trial(GT, Pp, nqw, pv, phimet, tseed, cfg, wcfg)
                r[name] = [int(summ['eff_fckf'][c]) for c in COLS_OUT] if summ is not None else None
            except AssertionError as ex:
                r[name] = f'ERR {ex}'
        res['rows'][str(row)] = r
        print(row, r, flush=True)
        (OUT / f'inv_a2fc_e500_a2pu_{a["id"]}_L{lam:g}.json').write_text(json.dumps(res, indent=0))


if __name__ == '__main__':
    main()
