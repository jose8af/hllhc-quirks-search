"""A1 failure decomposition inside the barrel fiducial (|eta_pair| < 1, status 1, not probe-excluded), per Lambda,
plus A1 vs A2 eps(R_A) on the same rows.  Read-only on prod outputs; frozen analysis code for the pass flag."""
import sys, json
import numpy as np
from acts.stage4.analysis import common as C, signal as SG
from acts.stage4.code import s4sig as S
spin, m = sys.argv[1], int(sys.argv[2]); lams = [float(x) for x in sys.argv[3].split(',')]
R04 = C.LADDER_NAMES.index('R04_IP2>=7')
jobs = {j['id']: j for j in C.manifest('C1')}
# A2 per-row pass, all Lambda at once
A2 = {}
for p in sorted((C.PROD / 'C1' / 'A2').glob(f'A2_{spin}{m}_*.npz')):
    r2 = dict(d=C.load_npz(p), job=jobs[p.stem], path=p)
    for e in SG.analyse_file(r2, want_f1=False, obs=False)[0]:
        if e['status'] == 1 and not e['probe_excluded']:
            A2[(e['row'], round(e['lam'], 4))] = bool(e['L'][R04])
res = {}
for lam in lams:
    tag = f"p2_{spin}_m{m}_L{lam:g}_BM"
    p = C.PROD / 'C1' / 'A1' / f'A1_{tag}.npz'
    rec = dict(d=C.load_npz(p), job=jobs[f'A1_{tag}'], path=p); d = rec['d']
    ents = SG.analyse_file(rec, want_f1=False, obs=False)[0]
    cols = [str(c) for c in d['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
    ev = d['chain.evstats']; ec = [str(c) for c in d['chain.evstats_cols']]; ei = {c: i for i, c in enumerate(ec)}
    P = S.Point(S.point_key(spin, m, lam))
    cnt = dict(n=0, pass_=0, no_trial=0, no_qcand=0, split=0, align_dphi=0, align_eta=0, count_merge=0, count_ckf=0,
               count_other=0, fckf=0, match_core=0, other=0)
    ex = {}
    a1c = []; a2c = []
    for k, e in enumerate(ents):
        if e['probe_excluded'] or e['status'] != 1:
            continue
        r = e['row']; eta = P.event(r)[1]['eta']
        if abs(eta) >= 1.0:
            continue
        cnt['n'] += 1
        ps = bool(e['L'][R04])
        if (r, round(lam, 4)) in A2:
            a1c.append(ps); a2c.append(A2[(r, round(lam, 4))])
        if ps:
            cnt['pass_'] += 1; continue
        ti = e['trial']
        if ti < 0:
            cnt['no_trial'] += 1; continue
        msk = d['sig.cand.trial'] == ti if 'sig.cand.trial' in d else np.zeros(0, bool)
        if not msk.any():
            cnt['no_qcand'] += 1; ex.setdefault('no_qcand', []).append(r); continue
        fr = d['sig.cand.frac'][msk]; j = int(np.argmax(fr))
        g = lambda key: d['sig.cand.' + key][msk][j]
        ie = int(d['trials.ev'][ti]); row_ev = ev[ev[:, 0] == ie][0]
        nqckf = int(d['sig.tab'][k, ci['n_q_ckf']])
        if fr[j] < 0.5:
            cnt['split'] += 1; cat = 'split'
        elif abs(g('dphi_met')) >= 0.15:
            cnt['align_dphi'] += 1; cat = 'dphi'
        elif abs(g('eta_axis')) >= 1.0:
            cnt['align_eta'] += 1; cat = 'eta'
        elif g('nit2') < 3 or g('nip2') < 7:
            if row_ev[ei['n_merged_groups']] > 0:
                cnt['count_merge'] += 1; cat = 'merge'
            elif nqckf > 0:
                cnt['count_ckf'] += 1; cat = 'ckf'
            else:
                cnt['count_other'] += 1; cat = 'count_other'
        elif not (np.nan_to_num(g('f_ckf'), nan=1.0) < 0.2):
            cnt['fckf'] += 1; cat = 'fckf'
        elif bool(np.unpackbits(d['sig.eff_fckf'][k])[3]):
            cnt['match_core'] += 1; cat = 'match_core'
        else:
            cnt['other'] += 1; cat = 'other'
        ex.setdefault(cat, []).append(r)
    cnt['eps_A1_central'] = cnt['pass_'] / max(cnt['n'], 1)
    if a1c:
        cnt['common_central_n'] = len(a1c); cnt['eps_A1_common_central'] = float(np.mean(a1c)); cnt['eps_A2_common_central'] = float(np.mean(a2c))
    cnt['examples'] = {k: v[:40] for k, v in ex.items()}
    res[lam] = cnt
    print(f"L={lam:g}", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in cnt.items() if k != 'examples'})
json.dump(res, open(C.TT / 'data/acts_stage4/investigation' / f'classify_{spin}{m}.json', 'w'), indent=1, default=float)
