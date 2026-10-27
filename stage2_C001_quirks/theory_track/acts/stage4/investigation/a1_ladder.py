"""A1 (no PU) cumulative efficiencies inside |eta_pair| < 1 (status 1, not probe-excluded), in-job quirk-fraction match
(>= 50 % of written barrel quirk measurements, the run_g1b definition) -- V4-3-style numbers -- plus the analysis R04."""
import sys, json
import numpy as np
from acts.stage4.analysis import common as C, signal as SG
from acts.stage4.code import s4sig as S
spin, m = sys.argv[1], int(sys.argv[2]); lams = [float(x) for x in sys.argv[3].split(',')]
jobs = {j['id']: j for j in C.manifest('C1')}
R04 = C.LADDER_NAMES.index('R04_IP2>=7')
out = {}
for lam in lams:
    tag = f"p2_{spin}_m{m}_L{lam:g}_BM"; p = C.PROD / 'C1' / 'A1' / f'A1_{tag}.npz'
    rec = dict(d=C.load_npz(p), job=jobs[f'A1_{tag}'], path=p); d = rec['d']
    ents = SG.analyse_file(rec, want_f1=False, obs=False)[0]
    P = S.Point(S.point_key(spin, m, lam))
    c = dict(n=0, cand_any_q=0, matched_any=0, matched_R01=0, matched_R04=0, matched_R04_fckf=0, analysis_R04=0, all_eta_n=0, all_eta_R04=0)
    for k, e in enumerate(ents):
        if e['probe_excluded'] or e['status'] != 1: continue
        c['all_eta_n'] += 1; c['all_eta_R04'] += int(e['L'][R04])
        if abs(P.event(e['row'])[1]['eta']) >= 1: continue
        c['n'] += 1; ti = e['trial']
        c['analysis_R04'] += int(e['L'][R04])
        if ti < 0: continue
        msk = d['sig.cand.trial'] == ti
        if not msk.any(): continue
        c['cand_any_q'] += 1
        fr = d['sig.cand.frac'][msk]
        if (fr >= 0.5).any(): c['matched_any'] += 1
        eff = np.unpackbits(d['sig.eff'][k])[:C.NR].astype(bool); efc = np.unpackbits(d['sig.eff_fckf'][k])[:C.NR].astype(bool)
        c['matched_R01'] += int(eff[0]); c['matched_R04'] += int(eff[3]); c['matched_R04_fckf'] += int(efc[3])
    n = max(c['n'], 1)
    out[lam] = {k: (v / n if k not in ('n', 'all_eta_n', 'all_eta_R04') else v) for k, v in c.items()}
    out[lam]['all_eta_eps_R04'] = c['all_eta_R04'] / c['all_eta_n']
    out[lam]['barrel_fraction'] = c['n'] / c['all_eta_n']
    print(f'L={lam:g}', {k: round(v, 3) for k, v in out[lam].items()})
json.dump(out, open(C.TT / 'data/acts_stage4/investigation' / f'a1_ladder_{spin}{m}.json', 'w'), indent=1)
