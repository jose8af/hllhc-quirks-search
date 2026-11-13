"""INV_A2FC_E500 step 7: TT-side hybrid re-run (no ACTS) on A2FC chain dumps.  For each row of an A2FC job:
  FC   : the dumped full-chain event (PU + ACTS quirk measurements, CKF flags) -> g1b_tt.assemble + sig_trial with the
         production seeds  (must reproduce the stored A2FC sig.eff_fckf: validation of the re-run);
  NOCKF: FC with the CKF flag (bit0) cleared on the quirk measurements (no quirk-hit stealing);
  HYB  : FC PU (re-smeared, FC CKF flags) with the ACTS quirk measurements REPLACED by the numpy-A2 quirk measurements
         (s4sig.digitise, exactly as A2 does; flag 0) -> isolates the quirk-hit path from the PU re-draw.
Outcome: the in-job eff_fckf rung flags (R04, R08, R10, R11, R14) -- same pattern as the analysis match here.
Uses frozen modules read-only (run_g1b.sig_event_inputs / sig_trial, g1b_tt.assemble, s4sig.digitise).
usage: python inv_a2fc_e500_hybrid.py F 500 3 chunk[,chunk...]"""
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


def main():
    spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    chunks = [int(x) for x in sys.argv[4].split(',')]
    S = RG.s4sig()
    fz = RS.frozen_inputs()
    key = S.point_key(spin, m, lam)
    P = S.Point(key, RG.index())
    slab = S.slab_table(1.0)
    jobs = {j['chunk']: j for j in C.manifest('A2FC') if j['point'] == key}
    a2jobs = {j['id']: j for j in C.manifest('C1') if j['sample'] == 'A2'}
    outp = OUT / f'inv_a2fc_e500_hybrid_{spin}{m}_L{lam:g}.json'
    res = json.loads(outp.read_text()) if outp.exists() else {}
    for ch in chunks:
        job = jobs[ch]
        cfg, wcfg = RS.finder_configs(fz, job, False)
        z = np.load(C.PROD.joinpath(*job['out'].split('/')))
        stored = {int(z['sig.tab'][e, 0]): np.unpackbits(z['sig.eff_fckf'][e])[:C.NR].astype(bool)
                  for e in range(len(z['sig.tab']))}
        # stored A2 (numpy) flags of the same rows at this Lambda
        za = np.load(C.PROD.joinpath(*a2jobs[job['paired_a2_id']]['out'].split('/')))
        sa = {int(za['sig.tab'][e, 0]): np.unpackbits(za['sig.eff_fckf'][e])[:C.NR].astype(bool)
              for e in range(len(za['sig.tab'])) if za['sig.tab'][e, 1] == lam}
        for ie, row in enumerate(job['rows']):
            t0 = time.process_time()
            pre = f'dump.{ie}_0.'
            e = np.c_[z[pre + 'sid'].astype(float), z[pre + 'xyz'].astype(float), z[pre + 's01'].astype(float),
                      z[pre + 'flag'].astype(float), z[pre + 'vp'].astype(float), z[pre + 'particle'].astype(float),
                      z[pre + 'gen'].astype(float), z[pre + 'vsec'].astype(float), z[pre + 'dE'].astype(float),
                      z[pre + 't'].astype(float)]
            tr = z[pre + 'tru'].astype(np.float32)
            h, ev, met_true, pv, phimet, tseed = RG.sig_event_inputs(S, P, row, spin, P.m)
            q = e[:, 7].astype(np.int64) == GT.SIG_VP
            e_nockf = e.copy()
            e_nockf[q, 6] = (e_nockf[q, 6].astype(np.int64) & ~1).astype(float)
            d = S.digitise(h, ev, P.m, spin, row, lam, slab)
            d['meas'][:, 4:6] = d['meas'][:, 4:6].astype(np.float32).astype(float)   # dump s01 is float32
            e_hyb = np.concatenate([e[~q], d['meas']]); tr_hyb = np.concatenate([tr[~q], d['tru'].astype(np.float32)])
            r = dict(stored_fc=[int(stored[row][c]) for c in COLS_OUT], stored_a2=[int(sa[row][c]) for c in COLS_OUT]
                     if row in sa else None, n_q_ckf_flag=int(((e[q, 6].astype(np.int64) & 1) == 1).sum()))
            for name, ee, tt in (('FC', e, tr), ('NOCKF', e_nockf, tr), ('HYB', e_hyb, tr_hyb)):
                rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
                Pp = GT.assemble(ee, tt, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=True)
                nqw = int((Pp['H0'][:, 7].astype(np.int64) == GT.SIG_VP).sum())
                _, summ, _ = RG.sig_trial(GT, Pp, nqw, pv, phimet, tseed, cfg, wcfg)
                r[name] = [int(summ['eff_fckf'][c]) for c in COLS_OUT] if summ is not None else None
            r['cpu_s'] = round(time.process_time() - t0, 1)
            res[str(row)] = r
            print(row, r, flush=True)
            outp.write_text(json.dumps(res, indent=0))


if __name__ == '__main__':
    main()
