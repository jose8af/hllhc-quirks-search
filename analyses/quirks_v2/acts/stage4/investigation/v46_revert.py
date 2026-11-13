"""V4-6 revert rule (plan l.1254-1255, l.1813) applied per A2 (species-mass, Lambda) point, from the PRODUCTION A1
outputs (full chain, quirk hits through ACTS digitisation + CKF, no PU).  Read-only on prod/ and analysis/ (no import of
the analysis package).  Population as INV_SIGNAL_EFF §4 (ckf_stats.py): status == 1, not probe-excluded,
|eta_pair| < 1 (barrel fiducial).  Per event f = n_q_ckf / n_q_written (barrel written quirk measurements).

Metrics (both pre-declared; a point reverts to the full chain if EITHER exceeds 5 %):
  mean_f   = <f> over fiducial events with n_q_written > 0 (the INV_SIGNAL_EFF §4 number)
  pooled_f = sum n_q_ckf / sum n_q_written over the same events
Info only: pooled_f_alleta (all status-1, non-excluded rows, all eta).
Writes acts/stage4/investigation/V46_REVERT_SET.json (BEFORE any A2FC production)."""
import json
import time
from pathlib import Path

import numpy as np

from acts.stage4 import run_g1b as RG
from acts.stage4.code import s4sig as S

TT = Path(__file__).resolve().parents[3]
PROD = TT / 'data' / 'acts_stage4' / 'prod'
THR = 0.05
idx = RG.index()
tab = []
revert = []
for spin, m in RG.A2_SPECIES:
    for lam in RG.A2_LAMS:
        key = S.point_key(spin, m, lam)
        p = PROD / 'C1' / 'A1' / f"A1_{key.replace('/', '_')}.npz"
        with np.load(p, allow_pickle=False) as z:
            cols = [str(c) for c in z['sig.cols']]; T = z['sig.tab']
        ci = {c: i for i, c in enumerate(cols)}
        P = S.Point(key, idx)
        f = []; nq = 0; nc = 0; nqa = 0; nca = 0; nfid = 0
        for r in T:
            if int(r[ci['status']]) != 1 or int(r[ci['probe_excluded']]):
                continue
            nqw = int(r[ci['n_q_written']]); nqc = int(r[ci['n_q_ckf']])
            nqa += nqw; nca += nqc
            if abs(P.event(int(r[ci['row']]))[1]['eta']) >= 1:
                continue
            nfid += 1
            if nqw:
                f.append(nqc / nqw); nq += nqw; nc += nqc
        mean_f = float(np.mean(f)) if f else 0.0
        pooled = nc / nq if nq else 0.0
        rv = bool(mean_f > THR or pooled > THR)
        tab.append(dict(spin=spin, m=int(m), lam=float(lam), point=key, a1_file=str(p.relative_to(TT)),
                        n_fid_events=nfid, n_fid_with_q=len(f), mean_f=round(mean_f, 4), pooled_f=round(pooled, 4),
                        pooled_f_alleta=round(nca / max(nqa, 1), 4), revert=rv))
        if rv:
            revert.append(dict(spin=spin, m=int(m), lam=float(lam), point=key))
        print(f"{spin}{m:<5d} L{lam:<5g} n_fid {nfid:4d}  <f> {mean_f:.4f}  pooled {pooled:.4f}  "
              f"(all-eta pooled {nca / max(nqa, 1):.4f})  {'REVERT' if rv else ''}")
out = dict(created=time.strftime('%Y-%m-%d %H:%M'), rule='plan.md l.1254-1255 / l.1813 (V4-6): an A2 point with CKF '
           'signal-stealing fraction > 5 % reverts to the full chain (A5 kind, same rows/seeds/PU)',
           source='production A1 (C1/A1, full chain no PU); fiducial = status 1, not probe-excluded, |eta_pair| < 1',
           decision='revert iff mean_f > 0.05 OR pooled_f > 0.05 (pre-declared, conservative union)',
           threshold=THR, script='acts/stage4/investigation/v46_revert.py', table=tab, revert_set=revert,
           n_revert=len(revert))
(TT / 'acts/stage4/investigation/V46_REVERT_SET.json').write_text(json.dumps(out, indent=1))
print('revert set:', [(r['spin'] + str(r['m']), r['lam']) for r in revert])
