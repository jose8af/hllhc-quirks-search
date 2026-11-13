"""Per-row A1 vs A2 comparison at one (spin, m, Lambda): read-only on prod outputs, uses the frozen analysis code."""
import sys, json, glob
import numpy as np
from acts.stage4.analysis import common as C, signal as SG
from acts.stage4.code import s4sig as S

spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
TT = C.TT; PROD = C.PROD
def rec(p, job):
    return dict(d=C.load_npz(p), job=job, path=p)
jobs = {j['id']: j for j in C.manifest('C1')}
tag = f"p2_{spin}_m{m}_L{lam:g}_BM"
a1p = PROD / 'C1' / 'A1' / f'A1_{tag}.npz'
r1 = rec(a1p, jobs[f'A1_{tag}'])
e1, _ = SG.analyse_file(r1, want_f1=False, obs=False)
d1 = r1['d']
R04 = C.LADDER_NAMES.index('R04_IP2>=7')
def cand_info(d, ti):
    if 'sig.cand.trial' not in d or ti < 0: return None
    m_ = d['sig.cand.trial'] == ti
    if not m_.any(): return dict(n=0)
    fr = d['sig.cand.frac'][m_]; F = C.rung_flags(d['sig.cand.rungs'][m_]) if d['sig.cand.rungs'].ndim == 2 else None
    j = np.argmax(fr)
    return dict(n=int(m_.sum()), best_frac=float(fr[j]), best_nq=int(d['sig.cand.nq'][m_][j]),
                fckf=float(d['sig.cand.f_ckf'][m_][j]), dphi=float(d['sig.cand.dphi_met'][m_][j]),
                eta=float(d['sig.cand.eta_axis'][m_][j]), nip2=int(d['sig.cand.nip2'][m_][j]), nit2=int(d['sig.cand.nit2'][m_][j]),
                R01=bool(F[j, 0]) if F is not None else None, R04=bool(F[j, 3]) if F is not None else None,
                anyR04=bool(F[:, 3].any()) if F is not None else None)
cols = [str(c) for c in d1['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
A1 = {}
for k, e in enumerate(e1):
    A1[e['row']] = dict(pass_=bool(e['L'][R04]), trial=e['trial'], status=e['status'], nqw=int(d1['sig.tab'][k, ci['n_q_written']]),
                        nqckf=int(d1['sig.tab'][k, ci['n_q_ckf']]), npool=int(d1['sig.tab'][k, ci['n_q_pool']]),
                        nroad=int(d1['sig.tab'][k, ci['n_q_road']]), ci=cand_info(d1, e['trial']), Pinj=bool(e['P_injob_def'][3]))
A2 = {}
for p in sorted((PROD / 'C1' / 'A2').glob(f'A2_{spin}{m}_*.npz')):
    jid = p.stem
    r2 = rec(p, jobs[jid]); d2 = r2['d']
    e2, _ = SG.analyse_file(r2, want_f1=False, obs=False)
    c2 = [str(c) for c in d2['sig.cols']]; c2i = {c: i for i, c in enumerate(c2)}
    for k, e in enumerate(e2):
        if abs(e['lam'] - lam) > 1e-6: continue
        A2[e['row']] = dict(pass_=bool(e['L'][R04]), trial=e['trial'], status=e['status'], probe=e['probe_excluded'],
                            nqw=int(d2['sig.tab'][k, c2i['n_q_written']]), npool=int(d2['sig.tab'][k, c2i['n_q_pool']]),
                            nroad=int(d2['sig.tab'][k, c2i['n_q_road']]), ci=cand_info(d2, e['trial']), Pinj=bool(e['P_injob_def'][3]))
P = S.Point(S.point_key(spin, m, lam))
common = sorted(set(A1) & set(A2))
eta = {r: P.event(r)[1]['eta'] for r in common}
n11 = sum(A1[r]['pass_'] and A2[r]['pass_'] for r in common)
n10 = [r for r in common if A1[r]['pass_'] and not A2[r]['pass_']]
n01 = [r for r in common if A2[r]['pass_'] and not A1[r]['pass_']]
out = dict(point=tag, n_A1=len(A1), n_A2=len(A2), n_common=len(common), eps_A1_all=np.mean([v['pass_'] for v in A1.values()]),
           eps_A2_all=np.mean([v['pass_'] for v in A2.values()]), eps_A1_common=np.mean([A1[r]['pass_'] for r in common]),
           eps_A2_common=np.mean([A2[r]['pass_'] for r in common]), both=n11, A1only=len(n10), A2only=len(n01),
           A1_skipped_common=sum(A1[r]['trial'] < 0 for r in common))
print(json.dumps(out, default=float))
print('--- A2-only passes (row, eta, A1 info, A2 info)')
for r in n01[:25]:
    print(r, f"{eta[r]:+.2f}", 'A1', {k: A1[r][k] for k in ('trial', 'nqw', 'nqckf', 'npool', 'nroad', 'Pinj')}, A1[r]['ci'])
    print('      A2', {k: A2[r][k] for k in ('trial', 'nqw', 'npool', 'nroad', 'Pinj')}, A2[r]['ci'])
print('--- A1-only passes')
for r in n10[:10]:
    print(r, f"{eta[r]:+.2f}", 'A1', A1[r]['ci'], 'A2', A2[r]['ci'])
json.dump(dict(out=out, A1={str(k): v for k, v in A1.items()}, A2={str(k): v for k, v in A2.items()}, eta={str(k): v for k, v in eta.items()}),
          open(TT / 'data/acts_stage4/investigation' / f'cmp_{tag}.json', 'w'), default=float)
