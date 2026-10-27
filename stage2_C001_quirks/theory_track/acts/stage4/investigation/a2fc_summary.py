"""A2FC summary (read-only on prod/; no analysis-package import): per revert point
  jobs/events, V4-1 pass, V4-6 WITH PU (run_g1b meta v46: quirk measurements on CKF tracks, all surfaces; and the
  barrel fiducial <n_q_ckf / n_q_written> as in V46_REVERT_SET), in-job efficiency eff_fckf at R04 (diagnostic, the
  run_g1b definition) for A2FC vs the paired A2 entries on the same rows (all rows / |eta_pair| < 1), CPU.
Writes data/acts_stage4/investigation/a2fc_summary.json."""
import json

import numpy as np

from acts.stage4 import run_stage4 as RS
from acts.stage4.code import s4sig as S

jobs = json.loads((RS.JOBS / 'A2FC.json').read_text())['jobs']
c1 = {j['id']: j for j in json.loads((RS.JOBS / 'C1.json').read_text())['jobs']}
R04 = 3
pts = {}
for j in jobs:
    p = pts.setdefault(j['point'], dict(point=j['point'], jobs=0, events=0, v41_fail=0, nsm=0, nck=0, fid_f=[],
                                         eff_fc=[], eff_a2=[], eff_fc_c=[], eff_a2_c=[], wall_s=0.0, missing=0,
                                         bytes=0))
    f = RS.out_path(j)
    if not f.exists():
        p['missing'] += 1; continue
    P = S.Point(j['point'])
    with np.load(f) as z:
        m = json.loads(str(z['meta_json']))
        ci = {str(c): i for i, c in enumerate(z['sig.cols'])}
        tab = z['sig.tab']; ef = np.unpackbits(z['sig.eff_fckf'], axis=1)[:, R04].astype(bool)
    with np.load(RS.out_path(c1[j['paired_a2_id']])) as za:
        ta = za['sig.tab']; ea = np.unpackbits(za['sig.eff_fckf'], axis=1)[:, R04].astype(bool)
    sel = np.isclose(ta[:, ci['lam']], j['lam'])
    ta = ta[sel]; ea = ea[sel]
    assert ta[:, ci['row']].astype(int).tolist() == tab[:, ci['row']].astype(int).tolist()
    p['jobs'] += 1; p['events'] += len(tab); p['wall_s'] += m['wall_s']; p['bytes'] += f.stat().st_size
    p['v41_fail'] += int(m.get('v41_pass') is not True)
    p['nsm'] += m['v46']['n_quirk_meas_all_surfaces']; p['nck'] += m['v46']['n_on_ckf_tracks']
    for k, r in enumerate(tab):
        if int(r[ci['status']]) != 1 or int(r[ci['probe_excluded']]):
            continue
        c = abs(P.event(int(r[ci['row']]))[1]['eta']) < 1
        p['eff_fc'].append(ef[k]); p['eff_a2'].append(ea[k])
        if c:
            p['eff_fc_c'].append(ef[k]); p['eff_a2_c'].append(ea[k])
            if r[ci['n_q_written']] > 0:
                p['fid_f'].append(r[ci['n_q_ckf']] / r[ci['n_q_written']])
out = []
for k, p in pts.items():
    o = dict(point=k, jobs=p['jobs'], events=p['events'], missing=p['missing'], v41_fail=p['v41_fail'],
             v46_allsurf_PU=round(p['nck'] / max(p['nsm'], 1), 4),
             v46_barrel_fid_mean_f_PU=round(float(np.mean(p['fid_f'])), 4) if p['fid_f'] else None,
             injob_eff_fckf_R04=dict(A2FC=round(float(np.mean(p['eff_fc'])), 4), A2=round(float(np.mean(p['eff_a2'])), 4),
                                     n=len(p['eff_fc'])),
             injob_eff_fckf_R04_central=dict(A2FC=round(float(np.mean(p['eff_fc_c'])), 4),
                                             A2=round(float(np.mean(p['eff_a2_c'])), 4), n=len(p['eff_fc_c'])),
             wall_s=round(p['wall_s'], 1), gb=round(p['bytes'] / 1e9, 3))
    out.append(o)
    print(json.dumps(o))
tot = dict(jobs=sum(o['jobs'] for o in out), events=sum(o['events'] for o in out),
           cpu_h_job_wall_sum=round(sum(o['wall_s'] for o in out) / 3600, 2), gb=round(sum(o['gb'] for o in out), 2),
           v41_fail=sum(o['v41_fail'] for o in out), missing=sum(o['missing'] for o in out))
print(tot)
(RS.TT / 'data/acts_stage4/investigation/a2fc_summary.json').write_text(json.dumps(dict(points=out, total=tot), indent=1))
