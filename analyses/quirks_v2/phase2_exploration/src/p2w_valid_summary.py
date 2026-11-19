"""p2w_valid_summary.py -- numbers of the rule-1 validation (a), (c), (d) from the p2-c-r1v-* outputs (Cecilie, 2026-11-19).

  <tt python> p2w_valid_summary.py <part: a|d|c> <out.json>          (on a worker; plan RULE1_VALID_PLAN_cecilie_2026-11-19.md)

a  per control job: per-event candidate counts at R01..R08 from p2t_classify.py (variant 1, orientation 0) against v1's
   trials.n_pass; D = events where they differ.
d  --check-prefilter runs: candidates in skipped orientations; candidate tables with and without the option.
c  subset-pass counts per term / width / s / reading, acceptance against Tove's stored finder candidates, and the
   counts file for p2t_rule1_prelim.py (unchanged).
"""
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np

log = logging.getLogger('p2w_valid_summary')
D = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c'
V = f'{D}/rule1_valid'
QV2 = Path(__file__).resolve().parents[2]
WCUT = [None, None, None, None, 37.5, 18.75, 9.4, 4.7]
NIPMIN = [4, 5, 6, 7, 7, 7, 7, 7]
RN = ['R01', 'R02', 'R03', 'R04', 'R05', 'R06', 'R07', 'R08']
STREAM_TERM = {'pilot.c0.dif': 'DIF', 'pilot.c0.difc': 'DIFC', 'pilot.c0.ni22': 'NI22', 'pilot.c0.ni30': 'NI30',
               'pilot.c0.ni61': 'NI61', 'pilot.c0.nix': 'NIX', 'pilot.c0.nic': 'NIC', 'pilot.c0.hs': 'HS',
               'pilot.c0.lowpt': 'LOWPT'}
TERMS = ['DIF', 'DIFC', 'NI22', 'NI30', 'NI61', 'NIX', 'NIC', 'HS', 'Z', 'Zlow', 'LOWPT']
LOWPT_NT = (2.6e8, 5.2e8)        # as p2t_counts.py (ADD l.395-397)


def rung_counts(c, cols, nev, variant, orient0=True):
    """(nev, 8) number of stored candidates per event passing R01..R08 (rung logic of production.full_set_flags)."""
    ix = {k: i for i, k in enumerate(cols)}
    out = np.zeros((nev, 8), np.int64)
    for r in c:
        if r[ix['variant']] != variant or (orient0 and r[ix['orient']] != 0) or r[ix['nit2']] < 3:
            continue
        for j in range(8):
            if r[ix['nip2']] >= NIPMIN[j] and all(r[ix['dw_core']] < w for w in WCUT[4:j + 1]):
                out[int(r[ix['event']]), j] += 1
    return out


def part_a(out):
    res = dict(jobs={}, topo={})
    for f in sorted(glob.glob(f'{V}/p2-c-r1v-ctl*/000/r1v-ctl*-*.ref.npz')):
        jid = Path(f).name[:-8]
        ref = np.load(f); z = np.load(f[:-8] + '.npz')
        m = json.loads(str(z['meta'])); rm = json.loads(str(ref['meta']))
        nev = int(rm['n_events'])
        mine1 = rung_counts(z['cand'], m['cand_cols'], nev, 1)
        mine0 = rung_counts(z['cand'], m['cand_cols'], nev, 0)
        allor = rung_counts(z['cand'], m['cand_cols'], nev, 0, orient0=False)
        v1 = ref['n_pass'][:, :8]
        diff = (mine1 != v1)
        j = dict(stream=rm['stream'], n_events=nev, float32=rm['float32'], check_prefilter=m['check_prefilter'],
                 n_with_v1_trial=int(ref['has_trial'].sum()), n_pre_in_source=rm['n_pre_in_source'],
                 n_events_in_source=rm['n_events_in_source'], n_errors=m['n_errors'], n_find=m['n_find'],
                 cpu_s=m['cpu_s'], p2t_sha256=m['script_sha256'],
                 n_lost_prefilter=m['n_candidates_in_skipped_orientations'],
                 ref_events_with_cand={RN[k]: int((v1[:, k] > 0).sum()) for k in range(8)},
                 ref_cands={RN[k]: int(v1[:, k].sum()) for k in range(8)},
                 p2t_v1_events_with_cand={RN[k]: int((mine1[:, k] > 0).sum()) for k in range(8)},
                 p2t_v1_cands={RN[k]: int(mine1[:, k].sum()) for k in range(8)},
                 D={RN[k]: int(diff[:, k].sum()) for k in range(8)},
                 D_events_listed={RN[k]: [(int(ref['ev_global'][i]), int(v1[i, k]), int(mine1[i, k]))
                                          for i in np.where(diff[:, k])[0][:20]] for k in range(8)},
                 p2t_v0_events_with_cand={RN[k]: int((mine0[:, k] > 0).sum()) for k in range(8)},
                 p2t_v0_cands_other_orientations={RN[k]: int(allor[:, k].sum() - mine0[:, k].sum()) for k in range(8)})
        res['jobs'][jid] = j
        log.info('%s %s D %s ref %s', jid, j['stream'], j['D'], j['ref_events_with_cand'])
    for jid, j in res['jobs'].items():
        if not jid.startswith('r1v-ctl-'):
            continue
        t = res['topo'].setdefault(j['stream'], dict(n_events=0, n_pre_in_source=0, D_R04=0, D_R05=0, D_any=0,
                                                     ref_R01=0, ref_R04=0, ref_R05=0, v0_R01=0, v0_R04=0))
        t['n_events'] += j['n_events']; t['n_pre_in_source'] += j['n_pre_in_source']
        t['D_R04'] += j['D']['R04']; t['D_R05'] += j['D']['R05']; t['D_any'] += sum(j['D'].values())
        for r in ('R01', 'R04', 'R05'):
            t['ref_' + r] += j['ref_events_with_cand'][r]
        t['v0_R01'] += j['p2t_v0_events_with_cand']['R01']; t['v0_R04'] += j['p2t_v0_events_with_cand']['R04']
    for s, t in res['topo'].items():
        t['verdict'] = ('FAIL' if (t['D_R04'] or t['D_R05']) else ('PASS' if t['ref_R04'] >= 100 else 'NO POWER (D = 0)'))
    Path(out).write_text(json.dumps(res, indent=1))
    log.info('%s', json.dumps(res['topo'], indent=1))


def part_d(out):
    res = dict(control={}, z={})
    for f in sorted(glob.glob(f'{V}/p2-c-r1v-ctlp/000/r1v-ctlp-*.npz')):
        if f.endswith('.ref.npz'):
            continue
        jid = Path(f).name[:-4]
        a = np.load(f); b = np.load(f.replace('p2-c-r1v-ctlp', 'p2-c-r1v-ctl').replace('r1v-ctlp-', 'r1v-ctl-'))
        ma = json.loads(str(a['meta'])); mb = json.loads(str(b['meta']))
        ca = a['cand']; cb = b['cand']
        key = lambda c: len({tuple(r[:4]) for r in c})          # noqa: E731  (file, event, orient, variant)
        res['control'][jid] = dict(n_lost=ma['n_candidates_in_skipped_orientations'], check=ma['check_prefilter'],
                                   n_find_with=ma['n_find'], n_find_without=mb['n_find'], n_cand_with=len(ca),
                                   n_cand_without=len(cb), tables_identical=bool(ca.shape == cb.shape and np.array_equal(ca, cb, equal_nan=True)),
                                   n_orient_variant_with_cand=key(ca))
    tove = {}
    for f in glob.glob(f'{D}/pilot_class/p2-c-pilot-cls*/000/*.npz'):
        z = np.load(f); m = json.loads(str(z['meta'])); c = z['cand']; cols = m['cand_cols']
        for fi, fm in enumerate(m['files']):
            if 'znn' in fm['path']:
                tove[fm['path']] = c[(c[:, 0] == fi) & (c[:, cols.index('variant')] == 0)][:, 1:]
    for f in sorted(glob.glob(f'{V}/p2-c-r1v-zp/000/*.npz')):
        z = np.load(f); m = json.loads(str(z['meta'])); c = z['cand']
        same = True; n = 0; nk = set()
        for fi, fm in enumerate(m['files']):
            mine = c[c[:, 0] == fi][:, 1:]
            n += len(mine); nk |= {(fi, r[0], r[1]) for r in mine}
            same &= bool(mine.shape == tove[fm['path']].shape and np.array_equal(mine, tove[fm['path']], equal_nan=True))
        res['z'][Path(f).name[:-4]] = dict(n_lost=m['n_candidates_in_skipped_orientations'], check=m['check_prefilter'],
                                           n_find=m['n_find'], n_cand=n, n_event_orient_with_cand=len(nk),
                                           identical_to_tove_tables=same, n_errors=m['n_errors'], cpu_s=m['cpu_s'])
    for k in ('control', 'z'):
        res[k + '_total'] = dict(n_lost=sum(v['n_lost'] for v in res[k].values()),
                                 n_with_cand=sum(v.get('n_orient_variant_with_cand', v.get('n_event_orient_with_cand', 0))
                                                 for v in res[k].values()))
    Path(out).write_text(json.dumps(res, indent=1))
    log.info('%s', json.dumps(res, indent=1))


def part_c(out):
    tc = json.loads((QV2 / 'phase2_exploration/outputs/rule1_prelim_counts_tove_2026-11-19.json').read_text())
    WN = ['R04', 'R05', 'R06', 'R07', 'R08']
    rows = {}; nev = {t: 0 for t in TERMS}; nfl = {t: 0 for t in TERMS}; seen = set()
    tot = dict(cpu_s=0.0, n_errors=0, n_pref=0, n_seeds=0, n_planes=0, n_greedy=0, max_seeds=0, max_road=0, n_jobs=0)
    zfull = 0; sha = set()
    for f in sorted(glob.glob(f'{V}/p2-c-r1v-sub[ab]/000/*.npz')):
        z = np.load(f); m = json.loads(str(z['meta'])); r = z['rows']; cols = m['row_cols']
        ix = {k: i for i, k in enumerate(cols)}
        tot['cpu_s'] += m['cpu_s']; tot['n_errors'] += m['n_errors']; tot['n_jobs'] += 1; sha.add(m['script_sha256'])
        for k in ('n_pref', 'n_seeds', 'n_planes', 'n_greedy'):
            tot[k] += m['totals'][k]
        for k in ('max_seeds', 'max_road'):
            tot[k] = max(tot[k], m['totals'][k])
        for fi, fm in enumerate(m['files']):
            if fm['path'] in seen or fm['n_classified_range'] != fm['n_events']:
                raise SystemExit(f'{fm["path"]}: twice or partial')
            seen.add(fm['path'])
            if fm['stream'] == 'pilot.hs0.znn':
                zfull += sum(n for k, n in fm['w_hist'].items() if float(k) >= 0.5)
            else:
                t = STREAM_TERM[fm['stream']]; nev[t] += fm['n_events']; nfl[t] += fm['n_early_events']
            for x in r[r[:, 0] == fi]:
                t = ('Z' if x[ix['w']] >= 0.5 else 'Zlow') if fm['stream'] == 'pilot.hs0.znn' else STREAM_TERM[fm['stream']]
                rows[(fm['path'], int(x[ix['event']]), int(x[ix['orient']]))] = (t, x, ix)
    if len(seen) != 1083:
        raise SystemExit(f'{len(seen)} pilot files, expected 1083')
    for t in TERMS[:8] + ['LOWPT']:
        if nev[t] != tc['M'][t] or nfl[t] != tc['M_flagged_events'][t]:
            raise SystemExit(f'{t}: events {nev[t]} / flagged {nfl[t]} differ from Tove {tc["M"][t]} / {tc["M_flagged_events"][t]}')
    if zfull != tc['z']['n_full']:
        raise SystemExit(f'Z full-weight class {zfull} against Tove {tc["z"]["n_full"]}')
    M = tc['M']; Mfl = tc['M_flagged_events']
    res = dict(n_files=len(seen), totals=tot, script_sha256=sorted(sha), M=M, tables={}, variants={}, acceptance={}, lists={})
    for rd in 'SF':
        for wn in WN:
            for si, s in enumerate((0, 3)):
                for without in (False, True):
                    cnt = {t: 0 for t in TERMS}; kd = {}
                    for key, (t, x, ix) in rows.items():
                        k = int(x[ix[f'k_{wn}_s{s}_{rd}']])
                        if without and x[ix['n_early_prod']] > 0:
                            continue
                        if k <= (7 + s) // 2:
                            cnt[t] += 1
                            if t == 'Z':
                                kd[k] = kd.get(k, 0) + 1
                    name = f"sub{rd}_{wn}_s{s}_{'without' if without else 'with'}"
                    res['tables'][name] = cnt
                    res['tables'][name + '_Z_by_k'] = {str(k): kd[k] for k in sorted(kd)}
                    if wn == 'R08' and s == 0:
                        var = {t: [cnt[t], M[t] - (Mfl[t] if without else 0)] for t in TERMS}
                        if var['LOWPT'][0] > 0:
                            var['extra'] = [['LOWPT_lo', LOWPT_NT[0] / var['LOWPT'][1], var['LOWPT'][0]]]
                            var['extra_hi'] = [['LOWPT_hi', LOWPT_NT[1] / var['LOWPT'][1], var['LOWPT'][0]]]
                        res['variants'][f"sub{rd}_{'without' if without else 'with'}"] = var
    # the B1 / HS / LOWPT rows, all of them (few)
    res['lists']['non_Z_rows'] = [dict(path=key[0], event=key[1], orient=key[2], term=t,
                                       **{c: float(x[ix[c]]) for c in ix if c.startswith('k_') or c in ('n_early_prod', 'n_road')})
                                  for key, (t, x, ix) in rows.items() if t not in ('Z', 'Zlow')][:400]
    # acceptance: k_sub(F) <= k_finder for every (event, orientation) of Tove's stored variant-0 candidates
    WV = dict(R04=1e9, R05=37.5, R06=18.75, R07=9.4, R08=4.7)
    acc = {f'{wn}_s{s}': dict(n_finder_near=0, n_violations=0, n_sub_lower=0, examples=[]) for wn in WN for s in (0, 3)}
    for f in glob.glob(f'{D}/pilot_class/p2-c-pilot-cls*/000/*.npz'):
        z = np.load(f); m = json.loads(str(z['meta'])); c = z['cand']; cols = m['cand_cols']
        cx = {k: i for i, k in enumerate(cols)}
        fk = {}
        for r in c:
            if r[cx['variant']] != 0 or r[cx['nit2']] < 3:
                continue
            key = (m['files'][int(r[cx['file']])]['path'], int(r[cx['event']]), int(r[cx['orient']]))
            for wn in WN:
                if wn == 'R04' or r[cx['dw_core']] < WV[wn]:
                    for s in (0, 3):
                        k = int(7 - r[cx['nip2']] + max(0, s - r[cx['n2s2']]))
                        fk[(key, wn, s)] = min(fk.get((key, wn, s), 99), k)
        for (key, wn, s), k in fk.items():
            if k > (7 + s) // 2:
                continue
            a = acc[f'{wn}_s{s}']; a['n_finder_near'] += 1
            mine = 99
            if key in rows:
                t, x, ix = rows[key]
                mine = int(x[ix[f'k_{wn}_s{s}_F']])
            if mine > k:
                a['n_violations'] += 1
                if len(a['examples']) < 10:
                    a['examples'].append([key[0], key[1], key[2], k, mine])
            elif mine < k:
                a['n_sub_lower'] += 1
    res['acceptance'] = acc
    res['acceptance_violations_total'] = sum(a['n_violations'] for a in acc.values())
    Path(out).write_text(json.dumps(res, indent=1, default=float))
    for n in ('subS_R08_s0_with', 'subF_R08_s0_with', 'subS_R08_s3_with', 'subF_R08_s3_with', 'subS_R07_s0_with',
              'subF_R07_s0_with', 'subF_R04_s0_with', 'subS_R08_s0_with_Z_by_k', 'subF_R08_s0_with_Z_by_k'):
        log.info('%s %s', n, res['tables'][n])
    log.info('acceptance %s', {k: (a['n_finder_near'], a['n_violations'], a['n_sub_lower']) for k, a in acc.items()})
    log.info('totals %s', tot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    dict(a=part_a, d=part_d, c=part_c)[sys.argv[1]](sys.argv[2])
