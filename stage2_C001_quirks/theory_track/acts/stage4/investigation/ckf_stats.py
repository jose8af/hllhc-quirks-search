"""A1 (no PU, full ACTS chain incl. CKF on quirk hits): CKF stealing of quirk measurements in the barrel fiducial vs
Lambda; and the share of fiducial R04 failures with > 20 % of the quirk hits on CKF tracks."""
import sys
import numpy as np
from acts.stage4.analysis import common as C, signal as SG
from acts.stage4.code import s4sig as S
jobs = {j['id']: j for j in C.manifest('C1')}
R04 = C.LADDER_NAMES.index('R04_IP2>=7')
for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)):
    line = []
    for lam in (1, 2, 3, 5, 7, 10):
        tag = f"p2_{spin}_m{m}_L{lam:g}_BM"; p = C.PROD / 'C1' / 'A1' / f'A1_{tag}.npz'
        rec = dict(d=C.load_npz(p), job=jobs[f'A1_{tag}'], path=p); d = rec['d']
        cols = [str(c) for c in d['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
        ents = SG.analyse_file(rec, want_f1=False, obs=False)[0]; P = S.Point(S.point_key(spin, m, lam))
        fr = []; fail_ckf = 0; nfail = 0; n = 0
        for k, e in enumerate(ents):
            if e['probe_excluded'] or e['status'] != 1 or abs(P.event(e['row'])[1]['eta']) >= 1: continue
            n += 1
            nqw = d['sig.tab'][k, ci['n_q_written']]; nqc = d['sig.tab'][k, ci['n_q_ckf']]
            f = nqc / nqw if nqw else 0.0; fr.append(f)
            if not e['L'][R04]:
                nfail += 1; fail_ckf += int(f > 0.2)
        fr = np.array(fr)
        line.append(f"{lam:g}keV: <f>={fr.mean():.3f} P(f>0.2)={np.mean(fr > 0.2):.2f} fails-with-f>0.2 {fail_ckf}/{nfail} (of n={n})")
    print(f'{spin}{m}:', ' | '.join(line))
