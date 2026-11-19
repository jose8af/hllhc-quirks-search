"""p2t_counts.py -- own-hit counts per term, rung and reading from the p2-c-pilot-cls outputs (Tove, 2026-11-19).

  <tt python> p2t_counts.py <dir[,dir...] with p2-c-pilot-cls*-*.npz> <counts.json>   (every pilot file exactly once: 1083)

Readings (plan RULE1_PRELIM_PLAN_tove_2026-11-19.md section 3, ambiguity A1), per (file, event, orientation), variant 0
(all own hits, before CKF); variant 1 (CKF-flagged rows removed) is tabulated for information:
  P  finder pass:       a stored candidate with N_IT2 >= 3, N_IP2 >= 7, N_2S2 >= s, w_core < W
  N  finder near-pass:  a stored candidate with w_core < W and deficit k = (7 - N_IP2) + max(0, s - N_2S2) <= floor((7 + s) / 2)
for W in (75 [no width cut, R04], 37.5 [R05], 18.75 [R06], 9.4 [R07], 4.7 [R08 = R09 = R11]) and s in (0, 3 [R14 = R17 = R20, FB]).
"with" = all events (binding per the D9 ruling); "without" = events with n_early_prod > 0 removed from m and M.
Terms: DIF (classes dif + k0l), DIFC, NI22, NI30, NI61, NIX, NIC on their streams; HS (all classes of pilot.c0.hs);
Z (w_v1 >= 0.5: full-weight class, M = sum w / w_max) and Zlow (0 < w_v1 < 0.5; M of the full class, as in the addendum);
LOWPT (alarm).
"""
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np

log = logging.getLogger('p2t_counts')
STREAM_TERM = {'pilot.c0.dif': 'DIF', 'pilot.c0.difc': 'DIFC', 'pilot.c0.ni22': 'NI22', 'pilot.c0.ni30': 'NI30',
               'pilot.c0.ni61': 'NI61', 'pilot.c0.nix': 'NIX', 'pilot.c0.nic': 'NIC', 'pilot.c0.hs': 'HS',
               'pilot.c0.lowpt': 'LOWPT'}
WIDTHS = {'R04': 75.0, 'R05': 37.5, 'R06': 18.75, 'R07': 9.4, 'R08': 4.7}
TERMS = ['DIF', 'DIFC', 'NI22', 'NI30', 'NI61', 'NIX', 'NIC', 'HS', 'Z', 'Zlow', 'LOWPT']
LOWPT_NT = (2.6e8, 5.2e8)        # ADD (addendum 1 v5) l.395-397: N_t at one to two times the pool's vertex yield [E]


def main(d, out):
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    fs = sorted(f for dd in d.split(',') for f in glob.glob(str(Path(dd) / 'p2-c-pilot-cls*-*.npz')))
    seen = {}
    M = {t: 0.0 for t in TERMS}; Mfl = {t: 0.0 for t in TERMS}      # events; flagged events
    nfiles = {t: 0 for t in TERMS}; zinfo = dict(n_gen=0, n_full=0, n_low=0, sum_w_full=0.0, sum_w_low=0.0, w_max=0.0,
                                                 low_values={})
    rows = []; errs = 0; nfind = 0; cpu = 0.0; cls_hs = {}
    for f in fs:
        z = np.load(f)
        m = json.loads(str(z['meta'])); c = z['cand']
        errs += m['n_errors']; nfind += m['n_find']; cpu += m['cpu_s']
        cols = m['cand_cols']
        term_of_file = {}
        for fi, fm in enumerate(m['files']):
            if fm['path'] in seen:
                raise SystemExit(f'{fm["path"]} classified twice: {seen[fm["path"]]} and {f}')
            seen[fm['path']] = f
            if fm['n_classified_range'] != fm['n_events']:
                raise SystemExit(f'{f}: partial file {fm["path"]}')
            if fm['stream'] == 'pilot.hs0.znn':
                term_of_file[fi] = 'Z'
                zinfo['n_gen'] += fm['n_events']; zinfo['w_max'] = max(zinfo['w_max'], fm['w_max'])
                for k, n in fm['w_hist'].items():
                    w = float(k)
                    if w >= 0.5:
                        zinfo['n_full'] += n; zinfo['sum_w_full'] += w * n
                    elif w > 0:
                        zinfo['n_low'] += n; zinfo['sum_w_low'] += w * n
                        zinfo['low_values'][k] = zinfo['low_values'].get(k, 0) + n
                nfiles['Z'] += 1
            else:
                t = STREAM_TERM[fm['stream']]
                term_of_file[fi] = t
                M[t] += fm['n_events']; Mfl[t] += fm['n_early_events']; nfiles[t] += 1
                if t == 'HS':
                    for k, n in fm['cls_counts'].items():
                        cls_hs[k] = cls_hs.get(k, 0) + n
        if len(c):
            fi = c[:, cols.index('file')].astype(int)
            w = c[:, cols.index('w')]
            for i in range(len(c)):
                t = term_of_file[fi[i]]
                if t == 'Z' and w[i] < 0.5:
                    t = 'Zlow'
                rows.append((t, Path(f).name, *c[i]))
        z.close()
    if len(seen) != 460 + 623:
        raise SystemExit(f'{len(seen)} pilot files classified, expected 1083 (460 Z + 623 B1/hs/lowpt)')
    cols = ['term', 'job'] + cols
    ix = {k: i for i, k in enumerate(cols)}
    wmax = zinfo['w_max']
    M['Z'] = zinfo['sum_w_full'] / wmax; M['Zlow'] = M['Z']
    zinfo['M_full_sum_w_over_wmax'] = M['Z']
    res = dict(n_outputs=len(fs), n_errors=errs, n_find=nfind, cpu_s_in_jobs=cpu, n_files=nfiles, M=M, M_flagged_events=Mfl,
               z=zinfo, hs_class_counts=cls_hs, n_candidates_stored=len(rows), tables={}, variants={}, lists={})
    key = lambda r: (r[ix['job']], r[ix['file']], r[ix['event']], r[ix['orient']])      # noqa: E731

    def count(variant, W, s, near, without):
        got = {t: set() for t in TERMS}
        for r in rows:
            if r[ix['variant']] != variant or not r[ix['dw_core']] < W:
                continue
            if without and r[ix['n_early_prod']] > 0:
                continue
            nip2, n2s2 = r[ix['nip2']], r[ix['n2s2']]
            if near:
                ok = (7 - nip2) + max(0, s - n2s2) <= (7 + s) // 2
            else:
                ok = nip2 >= 7 and n2s2 >= s
            if ok and r[ix['nit2']] >= 3:
                got[r[ix['term']]].add(key(r))
        return got

    for variant in (0, 1):
        for rung, W in WIDTHS.items():
            for s in (0, 3):
                for near in (False, True):
                    for without in (False, True):
                        g = count(variant, W, s, near, without)
                        name = f"v{variant}_{'N' if near else 'P'}_{rung}_s{s}_{'without' if without else 'with'}"
                        res['tables'][name] = {t: len(g[t]) for t in TERMS}
                        if variant == 0 and rung == 'R08' and s == 0:
                            var = {t: [len(g[t]), M[t] - (Mfl[t] if without else 0)] for t in TERMS}
                            ml = var['LOWPT'][0]
                            if ml > 0:
                                var['extra'] = [['LOWPT_lo', LOWPT_NT[0] / var['LOWPT'][1], ml]]
                                var['extra_hi'] = [['LOWPT_hi', LOWPT_NT[1] / var['LOWPT'][1], ml]]
                            res['variants'][f"{'N' if near else 'P'}_{'without' if without else 'with'}"] = var
                            res['lists'][name] = [dict(zip(cols, r)) for r in rows
                                                  if r[ix['variant']] == 0 and key(r) in g[r[ix['term']]]
                                                  and r[ix['dw_core']] < W][:300]
    # alarms: off-road orientations (k != 0) and events passing in several orientations, B1 class streams, loosest reading
    g = count(0, 75.0, 0, True, False)
    b1 = [k for t in TERMS[:7] for k in g[t]]
    ev = {}
    for k in b1:
        ev.setdefault(k[:3], set()).add(k[3])
    res['alarm_offroad'] = dict(reading='v0 N R04 (any stored loose aligned candidate)', n_passes=len(b1),
                                n_offroad=sum(1 for k in b1 if k[3] != 0),
                                n_events_multi_orientation=sum(1 for v in ev.values() if len(v) > 1))
    Path(out).write_text(json.dumps(res, indent=1, default=float))
    log.info('M %s', {t: round(v, 1) for t, v in M.items()})
    for n in ('v0_P_R04_s0_with', 'v0_N_R04_s0_with', 'v0_P_R06_s0_with', 'v0_N_R06_s0_with', 'v0_P_R07_s0_with',
              'v0_N_R07_s0_with', 'v0_P_R08_s0_with', 'v0_N_R08_s0_with', 'v0_N_R08_s0_without', 'v0_N_R08_s3_with',
              'v1_N_R08_s0_with', 'v1_P_R08_s0_with'):
        log.info('%s %s', n, res['tables'][n])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
