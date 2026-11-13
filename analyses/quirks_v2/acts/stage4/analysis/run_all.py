"""run_all.py -- one driver for the Stage-4 analysis (see ANALYSIS_MAP.md, SCHEMA.md).

    nice -n 15 pixi run python -m acts.stage4.analysis.run_all --campaigns C1a,C1b[,C2B] \
        --out data/acts_stage4/analysis/<tag> [--stages signal,background,srt,wp,limits] [--nboot 1000]
    # T_seed = 6 DRY RUN on the G3 pilot (stand-in for C1b; NOT a result):
    nice -n 15 pixi run python -m acts.stage4.analysis.run_all --campaigns G3 --dry-run-g3 --out .../dryrun_g3

Refuses: (i) governing documents changed (WP_RULE 1b2ea9bd..., PC19 d30bcc2f..., HASH_ADDENDUM e273c077...);
(ii) any job failing admission (common.admission) is LEFT OUT and listed; --strict makes it fatal;
(iii) mixing T_seed values in one background union (C1/C2 T_seed = 4 with G3 T_seed = 6).
Records the sha256 of every input file, of the governing documents, of the frozen tables and of this package.
Read-only on data/acts_stage4/prod/.
"""
import argparse
import json as _jsonmod
import os
import time
from pathlib import Path

import numpy as np

from acts.stage4.analysis import common as C

CAMPAIGN_MAP = {            # sub-run -> (manifest, kinds)   (run_stage4.SPLITS)
    'C1a': ('C1', ('a1', 'a2', 'a5', 'cp0', 'cppu')),
    'C1b': ('C1', ('pu', 'sm', 'dens')),
    'C2B': ('C2', ('pu',)),
    'G3': ('G3', ('pu',)),
    'A2FC': ('A2FC', ('a5',)),   # FIX R6: V4-6 revert (run_a2fc.py) -- full-chain replacements of A2 points, NOT A5
}
DEFAULTS = dict(n_trig=None, lumi_pb=3.0e6, k_factor=1.4, sigma_norm=float(np.log(1.3)))


def _json_dumps(o):
    return _jsonmod.dumps(o)


def package_hashes():
    return {str(p.relative_to(C.TT)): C.sha256(p) for p in sorted(C.HERE.glob('*.py'))}


def inputs_table(path):
    import json
    return json.loads(Path(path).read_text())


def validate_outputs(out):
    """Check the required top-level keys and types of every JSON output against inputs/schema.json."""
    import json
    sch = json.loads((C.HERE / 'inputs' / 'schema.json').read_text())['files']
    tmap = {'str': str, 'int': int, 'dict': dict, 'list': list, 'bool': bool}
    res = {}
    for f, spec in sch.items():
        p = Path(out) / f
        if not f.endswith('.json') or '<' in f or not p.exists():
            continue
        d = json.loads(p.read_text())
        bad = []
        for k, t in spec.get('required', {}).items():
            if k not in d:
                bad.append(f'missing {k}')
                continue
            base = t.split()[0].split('|')[0].split('[')[0]
            if base in tmap and d[k] is not None and not isinstance(d[k], tmap[base]):
                bad.append(f'{k}: {type(d[k]).__name__} != {base}')
        res[f] = 'ok' if not bad else bad
    return res


def _regen_provenance():
    return {f: C.sha256(C.TT / f) for f in ('acts/stage4/analysis/gen_d123.py', 'acts/stage4/code/s4pu.py')}


def sm_regen(smj, out, log):
    """Run gen_d123.py smregen (ACTS env, Pythia generator only) on the SM hit-level jobs; cached in <out>/sm_regen.json.
    Verifies that every regenerated hard scatter reproduces the stored hs_met (else sm_term refuses)."""
    import json
    import subprocess
    f = out / 'sm_regen.json'
    if f.exists():
        d = json.loads(f.read_text())
        if all(x['job_id'] in d for x in smj) and d.get('_provenance') == _regen_provenance():   # C-5: hashed cache
            return d
    cmd = ['nice', '-n', '15', 'pixi', 'run', '--manifest-path', str(C.TT / 'acts' / 'pixi.toml'), 'python',
           str(C.HERE / 'gen_d123.py'), 'smregen', str(f)] + [str(x['path']) for x in smj]
    log(f'SM regeneration: {len(smj)} jobs')
    r = subprocess.run(cmd, cwd=str(C.TT), capture_output=True, text=True)
    if r.returncode != 0 or not f.exists():
        log('SM regeneration FAILED: ' + r.stderr[-800:])
        return None
    d = json.loads(f.read_text())
    return {k: v for k, v in d.items() if not k.startswith('_')} | {'_provenance': d.get('_provenance')}


def signal_srt_stage(out, srt_res, b1, log, kinds=('a2', 'a5', 'a1'), stamp=None):
    """PC-19 signal eps_SR-T: per (sample, point) and ladder rung / fallback selection, the fraction of events with a
    matched (f_CKF < 0.2) candidate passing the selection whose earliest in-band BTL hit is in time and in the window."""
    import json
    from acts.stage4.analysis import srt as SR
    tmin, tmax = srt_res['edges']['t_min_ns'], srt_res['edges']['t_max_ns']
    evx = SR.c1_b1_event_index(C.manifest('C1'))     # A-4: C1 B1 events from the MANIFEST, (job id, ev) order
    sig = json.loads((out / 'signal_eff.json').read_text())
    res = dict(window_ns=[tmin, tmax], n_B1_events=len(evx), points={}, oot_checks={}, provenance=stamp)
    for kind in kinds:
        f = out / f'signal_obs_{kind}.npz'
        if not f.exists():
            continue
        z = np.load(f, allow_pickle=False)
        n = len(z['row'])
        obs = [dict(row=int(z['row'][i]), spin=str(z['spin'][i]), m=float(z['m'][i]), pv=z['pv'][i], normal=z['normal'][i],
                    axis=z['axis'][i], t_pv=float(z['t_pv'][i]), t_raw_in=float(z['t_raw_in'][i]),
                    dt_earliest=float(z['dt_earliest'][i])) for i in range(n)]
        tags, ochk = SR.signal_srt(obs, evx, tmin, tmax, log=log)
        res['oot_checks'][kind] = ochk
        if not ochk['pass_']:
            raise SystemExit(f'REFUSED: signal OOT lookups found no BTL hits ({ochk}) -- event-index bug (A-4)')
        T = np.array([t['srt'] for t in tags]); okf = z['f_ckf'] < 0.2
        keys = z['key']; rows = z['row']; L = z['L']; FB = z['FB']
        for key in np.unique(keys):
            mk = keys == key
            nden = sig[kind]['points'][str(key)]['n_den']
            evL = {}; evF = {}
            for i in np.where(mk & okf & T)[0]:
                evL.setdefault(int(rows[i]), np.zeros(L.shape[1], bool)); evF.setdefault(int(rows[i]), np.zeros(FB.shape[1], bool))
                evL[int(rows[i])] |= L[i]; evF[int(rows[i])] |= FB[i]
            kL = np.sum(list(evL.values()), axis=0) if evL else np.zeros(L.shape[1])
            kF = np.sum(list(evF.values()), axis=0) if evF else np.zeros(FB.shape[1])
            res['points'][str(key)] = dict(
                n_den=nden, ladder_SRT={C.LADDER_NAMES[i]: dict(k=int(kL[i]), eps=float(kL[i] / nden) if nden else None)
                                        for i in range(L.shape[1])},
                fallback_SRT={str(z['FB_names'][i]) + '&h>5&o>5': dict(k=int(kF[i]), eps=float(kF[i] / nden) if nden
                                                                      else None) for i in range(FB.shape[1])},
                n_earliest_oot=int(sum(1 for i in np.where(mk)[0] if tags[i]['earliest'] == 'OOT PU')))
    C.jdump(res, out / 'signal_srt.json')
    log(f"signal SR-T: {len(res['points'])} points")
    return res


def limits_stage(sig_dir, bkg_dir, out, log, ntoys=None, sample='A2', dev=False):
    """Plan §2.6 deliverable 2 / D4-13: per (m, Lambda) the primary selection per category (admissibility.primary),
    the two-bin counting likelihood (SR-T, SR-G) with B as a log-normal nuisance, the pyhf workspace and the expected
    95 % CL limit on mu = the number of signal events in the trigger + preselection acceptance in 3 ab^-1 (Stage 5
    divides by sigma x L x A).  Refuses to combine inputs with different T_seed."""
    import json
    from acts.stage4.analysis import admissibility as AD, stats as ST
    sig = json.loads((Path(sig_dir) / 'signal_eff.json').read_text())
    bk = json.loads((Path(bkg_dir) / 'bsum_wp.json').read_text())
    ms = json.loads((Path(sig_dir) / 'manifest.json').read_text()) if (Path(sig_dir) / 'manifest.json').exists() else {}
    mb = json.loads((Path(bkg_dir) / 'manifest.json').read_text()) if (Path(bkg_dir) / 'manifest.json').exists() else {}
    if ms.get('t_seed') is None or mb.get('t_seed') is None or ms.get('t_seed') != mb.get('t_seed'):     # C-3
        raise SystemExit(f"REFUSED: signal T_seed {ms.get('t_seed')} vs background T_seed {mb.get('t_seed')}")
    bgj = Path(bkg_dir) / 'background.json'
    rd = json.loads(bgj.read_text()).get('rho_dens', {}) if bgj.exists() else {}
    up_dev = []          # REVIEW R3 B-1: the EMBEDDED stamps of the consumed files (not the manifest this run rewrote)
    up_dev += C.provenance_issues(sig.get('provenance'), 'signal_eff.json')
    up_dev += C.provenance_issues(bk.get('provenance'), 'bsum_wp.json')
    if bgj.exists():
        up_dev += C.provenance_issues(json.loads(bgj.read_text()).get('provenance'), 'background.json')
    sfj = Path(sig_dir) / 'signal_srt.json'
    if sfj.exists():
        up_dev += C.provenance_issues(json.loads(sfj.read_text()).get('provenance'), 'signal_srt.json')
    ts_ = {(sig.get('provenance') or {}).get('t_seed'), (bk.get('provenance') or {}).get('t_seed')}
    if len(ts_) != 1 or None in ts_:                                   # REVIEW R4 C-1: T_seed from the EMBEDDED stamps
        up_dev.append(f'embedded T_seed mismatch or missing: {sorted(map(str, ts_))}')
        if (sig.get('provenance') or {}).get('t_seed') not in (None,) and (bk.get('provenance') or {}).get('t_seed') \
                not in (None,):
            raise SystemExit(f'REFUSED: embedded T_seed differs between signal and background {sorted(map(str, ts_))}')
    if up_dev and not dev:
        raise SystemExit(f'REFUSED (B-8): upstream {up_dev} output(s) are DEV or not produced with the frozen code/inputs')
    if up_dev:
        dev = True
    if rd.get('trigger'):                                                                     # B-5
        raise SystemExit('REFUSED: rho_dens > 1.05 (WP_RULE §8): eadm_dilution must be re-run with mu_c x rho_dens '
                         'and A.2b replaced before any fallback result')
    adm = AD.Admissibility()
    srtf = json.loads((Path(sig_dir) / 'signal_srt.json').read_text()) if (Path(sig_dir) / 'signal_srt.json').exists() \
        else None
    rule = bk['rule']; lad = bk['ladder']
    rstar = dict(T=rule['wp']['T'], G=rule['wp']['G'])
    flags = [('SR-T signal eps from signal_srt.json (PC-19); SR-G eps = eps(selection) - eps_SR-T' if srtf else
              'signal_srt.json absent: the SR-T bin carries s = 0 and all matched signal is in SR-G (conservative)'),
             'B per bin as one log-normal (median, sigma_eff = ln(B84/B_median)); the cross-category correlation of '
             'shared sources is not carried into the workspace']
    if not rule.get('complete_inputs', False):
        flags.append('B sum INCOMPLETE: ' + '; '.join(lad.get('missing_inputs', [])))
        if not dev:                                                                           # B-8
            raise SystemExit('REFUSED: B sum incomplete (' + '; '.join(lad.get('missing_inputs', [])) + '); use --dev '
                             'for a labelled NOT-A-RESULT run')
    if lad.get('T3s_required'):
        flags.append('T3s REQUIRED (D8) but not implemented: limits NOT VALID')
    res = dict(label=('DEV (not frozen / not a result) | ' if dev else '') +
               f"limits: signal {ms.get('label')} | background {mb.get('label')}", flags=flags, points={}, dev=bool(dev),
               upstream_issues=up_dev, provenance=C.provenance(dev, not dev))
    wsdir = out / 'workspaces'
    wsdir.mkdir(exist_ok=True)
    pts = sig.get(sample.lower(), {}).get('points', {})
    for key, t in pts.items():
        pr = AD.primary(t['spin'], t['m'], t['lam'], rstar, adm)
        s = []; b = []; sg = []; names = []
        for c in ('T', 'G'):
            sel = pr[c]
            if sel['kind'] == 'r*':
                eps = t['ladder'][C.LADDER_NAMES[sel['rung'] - 1]]['eps']
                bb = lad[c][sel['rung'] - 1]
            else:
                fbn = pr['admissibility']['r_fb']
                eps = t['fallback'][fbn]['eps']
                bb = lad['FB'][fbn][c]
            if srtf is not None:
                st = srtf['points'].get(key)
                if st is None:
                    eT = 0.0
                elif sel['kind'] == 'r*':
                    eT = st['ladder_SRT'][C.LADDER_NAMES[sel['rung'] - 1]]['eps'] or 0.0
                else:
                    eT = st['fallback_SRT'][pr['admissibility']['r_fb']]['eps'] or 0.0
                eps = eT if c == 'T' else max((eps or 0.0) - eT, 0.0)
            elif c == 'T':
                eps = 0.0                                    # see flags[0]
            med, b84 = bb.get('B_median'), bb.get('B84')
            s.append(eps or 0.0); b.append(med or 0.0)
            sg.append(float(np.log(b84 / med)) if med and b84 and med > 0 else 1.0)
            names.append(sel['name'])
        ws = ST.workspace(s, b, [{}, {}], sg)
        C.jdump(ws, wsdir / f"{key.replace('|', '_')}.json")
        ent = dict(primary=pr, s=s, b=b, sigma_ln=sg, selections=names)
        if sum(s) > 0:
            ent['expected_toys'] = ST.expected_limit_toys(s, b, [{}, {}], sg) if not ntoys else \
                ST.expected_limit_toys(s, b, [{}, {}], sg, ntoys=ntoys)                         # D4: PRIMARY
            ent['expected_asymptotic'] = ST.expected_limit_asymptotic(s, b, [{}, {}], sg)       # D4: cross-check
            ent['expected_primary'] = ent['expected_toys']['median']
            b84c = None
            if pr['T']['kind'] == 'r*' and pr['G']['kind'] == 'r*' and rule.get('combined_guard', {}).get('accepted'):
                b84c = rule['combined_guard']['combined_b84']
            ent['discovery'] = ST.discovery_reach(s, b, sg, b84_comb=b84c)
            one = [i for i, c in enumerate(('T', 'G')) if pr[c]['kind'] == 'r*']
            if len(one) == 1 and s[one[0]] > 0:      # §5.2: 3-event statement only for the background-free category
                ent['discovery']['mu_3events_single_category'] = dict(category=('T', 'G')[one[0]],
                                                                      mu=3.0 / s[one[0]])
        res['points'][key] = ent
    res['n_points'] = len(res['points'])
    C.jdump(res, out / 'limits.json')
    log(f"limits: {res['n_points']} points")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--campaigns', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--stages', default='signal,background,srt,wp,products,limits')
    ap.add_argument('--nboot', type=int, default=1000)
    ap.add_argument('--dry-run-g3', action='store_true', help='G3 (T_seed = 6) as a stand-in for C1b: labelled DRY RUN')
    ap.add_argument('--strict', action='store_true', help='fatal on any non-admitted job')
    ap.add_argument('--max-jobs', type=int, default=0, help='development only: at most N jobs per kind')
    ap.add_argument('--f1-max', type=int, default=5000)
    ap.add_argument('--inputs', default=str(C.HERE / 'inputs' / 'normalisation.json'))
    ap.add_argument('--no-srt-smear', action='store_true')
    ap.add_argument('--signal-from', default=None, help='limits: directory holding signal_eff.json (default --out)')
    ap.add_argument('--bkg-from', default=None, help='limits: directory holding bsum_wp.json (default --out)')
    ap.add_argument('--ntoys', type=int, default=0, help='--dev only: override the fixed D4 toy count')
    ap.add_argument('--dev', action='store_true', help='development: allowed with a code/input freeze mismatch or an '
                    'incomplete B sum; EVERY output is stamped DEV (B-8)')
    a = ap.parse_args(argv)
    try:
        os.nice(15)
    except OSError:
        pass
    out = Path(a.out)
    if not out.is_absolute():
        out = C.TT / out
    out.mkdir(parents=True, exist_ok=True)
    log = C.logger(out / 'run_all.log')
    t0 = time.time()
    rng = np.random.default_rng(C.SEED)
    stages = set(a.stages.split(','))
    camps = a.campaigns.split(',')
    gov = C.governing_docs()
    bad = [k for k, v in gov.items() if not v['ok'] and k != 'frozen_inputs.json']
    if bad:
        raise SystemExit(f'REFUSED: governing documents changed: {bad}')
    dry = a.dry_run_g3
    if dry and camps != ['G3']:
        raise SystemExit('REFUSED: --dry-run-g3 uses G3 only (no mixing of T_seed 6 with production)')
    if not dry and 'G3' in camps:
        raise SystemExit('REFUSED: G3 (T_seed = 6) cannot enter a production (T_seed = 4) union; use --dry-run-g3')
    tseed = 6 if dry else 4
    label = ('DRY RUN on G3 (T_seed = 6) as a stand-in for C1b -- NOT A RESULT' if dry else
             f"Stage-4 analysis on {'+'.join(camps)} (T_seed = 4)" + ('; preliminary (C1 statistics)' if 'C2B' not in camps
                                                                  else ''))
    fz = C.freeze_status()
    manifest_freeze = dict(match=fz['match'], mismatched=fz['mismatched'][:20], current=fz['current'])
    if not fz['match'] and not a.dev and stages & {'signal', 'limits', 'products'}:
        raise SystemExit(f"REFUSED (B-8 freeze): analysis code/inputs differ from inputs/analysis_freeze.json "
                         f"({fz['mismatched'][:5]}); signal eps and limits are printed only with the frozen code or --dev")
    frozen_inputs_path = (C.HERE / 'inputs' / 'normalisation.json').resolve()
    if Path(a.inputs).resolve() != frozen_inputs_path:          # REVIEW R2 B-2 (i)
        if not a.dev:
            raise SystemExit(f'REFUSED (B-8): --inputs {a.inputs} is not the frozen inputs/normalisation.json; use --dev')
        manifest_freeze['match'] = False
        manifest_freeze['mismatched'] = list(manifest_freeze['mismatched']) + [f'--inputs {a.inputs} (not frozen)']
    if a.dev:
        label = 'DEV (not frozen / not a result) | ' + label
    stamp = C.provenance(a.dev, manifest_freeze['match'], t_seed=tseed, campaigns=camps)   # R3 B-1 / R4 C-1
    norm = inputs_table(a.inputs)
    manifest = dict(label=label, created=time.strftime('%Y-%m-%d %H:%M:%S'), campaigns=camps, t_seed=tseed,
                    governing_documents=gov, analysis_code_sha256=package_hashes(), inputs_file=a.inputs,
                    inputs=norm, stages=sorted(stages), status={}, input_sha256={},
                    ambiguities=inputs_table(C.HERE / 'inputs' / 'ambiguities.json'),
                    analysis_map=inputs_table(C.HERE / 'inputs' / 'analysis_map.json'), freeze=manifest_freeze,
                    dev=bool(a.dev), imported_frozen_sha256={f: C.sha256(C.TT / f) for f in C.IMPORTED_FROZEN})
    log(label)

    def take(kinds, samples=None, keys=None, prefix=None, want_cp=False, max_jobs=None, only=None, exclude=('A2FC',)):
        res = []
        for c in camps:
            if (only is not None and c not in only) or (only is None and c in exclude):
                continue
            man, ks = CAMPAIGN_MAP[c]
            kk = tuple(k for k in kinds if k in ks)
            if not kk:
                continue
            files, st = C.collect([man], kk, tseed, samples=samples, keys=keys, prefix=prefix,
                                  max_jobs=(max_jobs if max_jobs is not None else a.max_jobs),
                                  log=log)
            tag = f"{c}:{','.join(kk)}:{','.join(samples) if samples else '*'}"
            manifest['status'][tag] = {k: (len(v) if k == 'input_sha256' else
                                           (dict(n=len(v), first=list(v)[:10]) if isinstance(v, (list, dict)) else v))
                                       for k, v in st.items()}
            manifest['input_sha256'].update(st['input_sha256'])
            if st['not_admitted'] and a.strict:
                raise SystemExit(f'REFUSED (--strict): not admitted: {list(st["not_admitted"])[:5]}')
            res += files
        return res

    # ------------------------------------------------------------------ signal
    if 'signal' in stages and not dry:
        from acts.stage4.analysis import signal as SG, admissibility as AD
        adm = AD.Admissibility()
        res = {}
        for kind in ('a1', 'a2', 'a5'):
            files = take((kind,))
            if not files:
                continue
            acc, chk = SG.aggregate(files, log=log)
            a2fc = None
            if kind == 'a2':             # FIX R6: pre-registered V4-6 revert (plan l.1254-1255): A2 -> A2FC full chain
                fcf = take(('a5',), only=('A2FC',)) if 'A2FC' in camps else []
                acc_fc, chk_fc = SG.aggregate(fcf, log=log) if fcf else ({}, None)
                fcj = {}
                for r_ in fcf:
                    sp_, m_, l_, cf_, _ = SG.point_of(r_['job'])
                    fcj.setdefault(f"A2FC|{sp_}|{m_:g}|{l_:g}|{cf_}", []).append(r_['job']['id'])
                a2fc = SG.apply_a2fc(acc, acc_fc, SG.a2fc_revert_set(), fcj, dev=a.dev, log=log)
                a2fc['checks_a2fc'] = chk_fc
                if chk_fc:
                    for k_ in ('n_records', 'n_core_mismatch', 'n_matched'):
                        chk[k_] += chk_fc[k_]
                    chk['max_rel_dw'] = max(chk['max_rel_dw'], chk_fc['max_rel_dw'])
            tabs = {k: SG.eff_table(v) for k, v in acc.items()}
            res[kind] = dict(n_files=len(files), checks=chk, self_consistency=SG.self_consistency(acc, chk),
                             points=tabs)
            if a2fc is not None:
                res[kind]['a2fc_revert'] = a2fc
                for k_ in a2fc['points']:
                    tabs[k_]['replaced_by_a2fc'] = a2fc['points'][k_]
            np.savez_compressed(out / f'signal_rows_{kind}.npz', provenance=np.array(_json_dumps(stamp)), **{f'{k}|{m}': v[m] for k, v in acc.items()
                                                                    for m in ('L', 'LT', 'FB', 'P') if len(v['rows'])},
                                **{f'{k}|rows': np.array(v['rows']) for k, v in acc.items()})
            ob = [dict(o, key=k) for k, v in acc.items() for o in v.get('obs', [])]
            if ob:
                np.savez_compressed(out / f'signal_obs_{kind}.npz', provenance=np.array(_json_dumps(stamp)),
                                    **{c: np.array([o[c] for o in ob]) for c in ob[0] if c not in ('L', 'FB')},
                                    L=np.array([o['L'] for o in ob]), FB=np.array([o['FB'] for o in ob]),
                                    L_names=np.array(C.LADDER_NAMES), FB_names=np.array(SG.FB_NAMES))
        pts = sorted({(t['spin'], t['m'], t['lam']) for r in res.values() for t in r['points'].values()})
        res['admissibility'] = {f'{s}|{m:g}|{l:g}': AD.Admissibility.point(adm, s, m, l) for s, m, l in pts}
        res['admissibility_inputs_sha256'] = adm.sha
        res['label'] = label
        res['provenance'] = stamp
        res['NOTE'] = 'numbers only; no physics conclusion; signal used only at the selections the rule fixes (§5.4 item 8)'
        res['rho_dens_check'] = ('enforced at the limits stage (REVIEW R1 B-5): a triggered rho_dens > 1.05 invalidates '
                                 'the A.2b e_adm table and the limits stage refuses')
        C.jdump(res, out / 'signal_eff.json')
        log(f'signal done ({time.time() - t0:.0f} s)')

    # ------------------------------------------------------------------ background
    if stages & {'background', 'srt', 'wp'}:
        from acts.stage4.analysis import background as BG
        b1s = ('G3B1',) if dry else ('B1',)
        b2s = ('G3B2',) if dry else ('B2',)
        keys_tr = ['trials.' + k for k in BG.TR_KEYS] + ['cand.' + k for k in BG.B1_CAND_KEYS] + ['job_id', 'complete']
        b1 = [BG.to_g3_job(r, 1) for r in take(('pu',), samples=b1s, keys=keys_tr)]
        b2 = [BG.to_g3_job(r, 2) for r in take(('pu',), samples=b2s, keys=['trials.' + k for k in BG.TR_KEYS] +
                                                ['job_id', 'complete'])]
        log(f'B1 jobs {len(b1)}, B2 jobs {len(b2)} ({time.time() - t0:.0f} s)')
        S = BG.PUSamples(b1, b2, a.nboot, rng)
        ST_ = BG.PUSamples(b1, b2, a.nboot, rng, t_cols=True)
        cl = BG.closure(S, rng, a.nboot)
        log(f"closure: T1 {cl['T1'].get('branch')} r={cl['T1'].get('ratio')} z={cl['T1'].get('z')}; "
            f"T1w {cl['T1w'].get('branch')} r={cl['T1w'].get('ratio')}; trend sig={cl['trend'].get('significant')}")
        rec = BG.B1Records(b1)
        cdict = G3c = None
        try:
            from acts.stage4.g3 import analyse_g3 as G3
            G3c = G3.c_test([dict(cand=d['cand'], tr=d['tr']) for d in b1], rng)
        except Exception as e:                                  # noqa: BLE001
            G3c = dict(error=str(e))
        cflag = (G3c or {}).get('c_max_flagged')            # B-3: GLOBAL c_max once any pair/triple is flagged
        c_factor = float((G3c.get('c_max') or {}).get('c', 1.0)) if cflag else 1.0
        t3 = None
        try:
            from acts.stage4.g3 import analyse_g3 as G3
            c1 = [c for c in range(3, 14) if S.nobs_ev[:, c].sum() >= 10]
            t3 = G3.t3_test([dict(cand=d['cand'], tr=d['tr'], job=d['job']) for d in b1], c1[-1] if c1 else None,
                            rng, a.nboot)
        except Exception as e:                                  # noqa: BLE001
            t3 = dict(error=str(e))
        # density term (C1 only: DENS low/high + the first 2 000 B1 events = jobs B1_00000..B1_00079)
        dens_info, dens_f = dict(available=False), (lambda col: 1.0)
        rho_d = dict(available=False)
        if not dry:
            lowj = [BG.to_g3_job(r, 1) for r in take(('dens',), samples=('DENSlow',), keys=keys_tr)]
            highj = [BG.to_g3_job(r, 1) for r in take(('dens',), samples=('DENShigh',), keys=keys_tr)]
            nom_ids = {d['job']['src_id'] for d in lowj} | {d['job']['src_id'] for d in highj}
            nomj = [d for d in b1 if d['job_id'] in nom_ids]
            dens_info, dens_f = BG.density_sigma(nomj, lowj, highj)
            rho_d = BG.rho_dens([d['path'] for d in b1 if d['job']['chunk'] < 80])
        else:
            dens_info = dict(available=False, note='dry run: no DENS jobs in G3 -> sigma_ln,dens = 1.0 (rule: no '
                                                   'qualifying rung)')
        rows, reach = BG.bpu_columns(S, cl, rec, c_factor, rng, a.nboot, log=log)
        rowsT, reachT = BG.bpu_columns(ST_, cl, rec, c_factor, rng, a.nboot, log=log, t_cols=True)
        es = BG.end_state(rows, cl, dens_f, DEFAULTS['sigma_norm'], BG.x_of_col, t3=t3)          # B-1
        esT = BG.end_state(rowsT, cl, dens_f, DEFAULTS['sigma_norm'], BG.x_of_col, t3=t3)
        f1 = BG.f1_factors(rec, [13, 14, 15, 16] + list(range(17, 37)), rng, a.nboot, log=log, max_n=a.f1_max)
        sm = cp = None
        if not dry:
            smj = [BG.to_g3_job(r, 1) for r in take(('sm',), keys=keys_tr)]
            sm = None
            if smj:
                regen = sm_regen(smj, out, log)                      # D1/D3: preselection weight + tau class
                sm = BG.sm_term(smj, norm.get('sm_processes', {}), norm['lumi_pb'], regen, c_factor=c_factor)
            cpk = ['job_id', 'complete', 'trials.ev', 'cp.ev', 'cp.ev_cols']
            cp0 = take(('cp0',), keys=cpk, prefix=('cp.cand.',))
            cpp = take(('cppu',), keys=cpk, prefix=('cp.cand.',))
            if cp0 or cpp:
                j0 = [dict(job=r['job'], meta=r['d']['meta'], d_cp=r['d'], tr={'ev': r['d'].get('trials.ev', [])},
                           path=r['path']) for r in cp0]
                jp = [dict(job=r['job'], meta=r['d']['meta'], d_cp=r['d'], tr={'ev': r['d'].get('trials.ev', [])})
                      for r in cpp]
                cp = BG.cprime_term(j0, jp, norm['cprime_rates'], c_factor=c_factor, spectra=norm.get('cprime_spectra'))
        bkg = dict(label=label, provenance=stamp, samples=dict(B1_trials=int(S.n1()), B1_events=int(S.E1), B2_trials=int(S.n2()),
                                             B2_events=int(S.E2)),
                   closure=cl, T3=t3, c_test=G3c, c_factor_applied=c_factor, reach=reach, reach_T=reachT,
                   density=dens_info, rho_dens=rho_d, columns=rows, columns_T=rowsT, end_state=es, end_state_T=esT,
                   f1_factors=f1, sm=sm, cprime=cp,
                   is_checks=dict(n_pull_ge3=int(np.sum(np.abs(S.tr2.get('meanW_pull', np.zeros(0))) >= 3)),
                                  n_trials=int(S.n2())))
        C.jdump(bkg, out / 'background.json')
        log(f'background done ({time.time() - t0:.0f} s)')
        srt_res = None
        if stages & {'srt', 'wp'}:
            from acts.stage4.analysis import srt as SR
            recs = []; recs_s = []; H0 = 0; H1 = 0; chks = []
            for d in b1:
                r_, h0, h1, ck = SR.job_arrays(d)
                recs.append(r_); chks.append(ck)
                if d['job'].get('campaign') in ('C1', 'G3'):     # PC-19: edges from C1 B1 (+ overlay) only
                    H0 = H0 + h0; H1 = H1 + h1
                if not a.no_srt_smear:
                    recs_s.append(SR.job_arrays(d, smear=True)[0])
            Rn = SR.merge(recs); Rs = SR.merge(recs_s) if recs_s else None
            srt_res = SR.srt_factors(Rn, Rs, H0, H1)
            ti = SR.time_independence(Rn, srt_res['edges']['t_min_ns'], srt_res['edges']['t_max_ns'], rng)     # B-4
            srt_res['time_independence'] = ti
            for v in srt_res['columns'].values():
                v['c_time'] = ti['c_time']
            srt_res['kernel_check'] = dict(n_sel=sum(c['n_sel'] for c in chks),
                                           n_mismatch_nband=sum(c['n_mismatch_nband'] for c in chks),
                                           max_abs_ddt0=max((c['max_abs_ddt0'] for c in chks), default=0.0))
            srt_res['label'] = label
            srt_res['provenance'] = stamp
            C.jdump(srt_res, out / 'srt.json')
            log(f"srt done: edges {srt_res['edges']['t_min_ns']}..{srt_res['edges']['t_max_ns']} ns "
                f"({time.time() - t0:.0f} s)")
        if srt_res is not None and (out / 'signal_obs_a2.npz').exists() and not dry:
            signal_srt_stage(out, srt_res, b1, log, stamp=stamp)
        if 'wp' in stages:
            from acts.stage4.analysis import wp as WP
            n_trig = norm['n_trig']['value']
            lad = WP.assemble(es, esT, f1, (srt_res or {}).get('columns'), sm, cp, n_trig, DEFAULTS['sigma_norm'],
                              trend_fn=lambda x: BG.trend_sigma(cl, x))
            rule = WP.apply_rule(lad)
            C.jdump(dict(label=label, provenance=stamp, n_trig=norm['n_trig'], ladder=lad, rule=rule), out / 'bsum_wp.json')
            log(f"WP: {rule['wp']} complete_inputs={rule['complete_inputs']} ({time.time() - t0:.0f} s)")
    if 'products' in stages and not dry:             # Stage-5 inputs (round 3 addition; prints eps-derived numbers)
        import json as _j
        from acts.stage4.analysis import products as PD, background as BG
        if (out / 'signal_eff.json').exists():
            sig_ = _j.loads((out / 'signal_eff.json').read_text())
            iss = C.provenance_issues(sig_.get('provenance'), 'signal_eff.json')        # REVIEW R3 B-1
            for k_ in ('a1', 'a2', 'a5'):
                for nm_ in (f'signal_rows_{k_}.npz', f'signal_obs_{k_}.npz'):
                    if (out / nm_).exists():
                        with np.load(out / nm_, allow_pickle=False) as zz:
                            pv_ = _j.loads(str(zz['provenance'])) if 'provenance' in zz.files else None
                        iss += C.provenance_issues(pv_, nm_)
            if iss and not a.dev:
                raise SystemExit(f'REFUSED (B-8): products inputs not frozen / DEV: {iss[:4]}')
            pdev = bool(a.dev or iss)
            acc_ = PD.acceptance(sig_); acc_['label'] = label + ' | ' + acc_['label']; acc_['dev'] = pdev
            C.jdump(acc_, out / 'acceptance.json')
            rows_ = {k: np.load(out / f'signal_rows_{k}.npz') for k in ('a1', 'a2') if (out / f'signal_rows_{k}.npz').exists()}
            ed = PD.edges(rows_); ed['label'] = label + ' | ' + ed['label']; ed['dev'] = pdev
            C.jdump(ed, out / 'edges_det.json')
            obs_ = {k: np.load(out / f'signal_obs_{k}.npz') for k in ('a1', 'a2', 'a5') if (out / f'signal_obs_{k}.npz').exists()}
            sp_ = PD.sep_it_det(obs_); sp_['label'] = label + ' | ' + sp_['label']; sp_['dev'] = pdev
            C.jdump(sp_, out / 'sep_it_det.json')
            b1j = [BG.to_g3_job(r, 1) for r in take(('pu',), samples=('B1',), keys=['trials.ev', 'cand.tag', 'cand.rungs',
                                                                                     'cand.trial', 'cand.idx', 'job_id',
                                                                                     'complete'], max_jobs=20)] \
                if 'C1b' in camps else []
            PD.event_display(obs_.get('a2'), b1j, out / 'event_display.npz')
            log('products written (acceptance, edges_det, sep_it_det, event_display)')
    if 'limits' in stages:
        C.jdump(manifest, out / 'manifest.json')
        sd = Path(a.signal_from) if a.signal_from else out
        bd = Path(a.bkg_from) if a.bkg_from else out
        if (sd / 'signal_eff.json').exists() and (bd / 'bsum_wp.json').exists():
            lim = limits_stage(sd, bd, out, log, ntoys=(a.ntoys if a.dev else None), dev=a.dev)
            manifest['limits'] = dict(n_points=lim.get('n_points'), flags=lim.get('flags'))
        else:
            log('limits skipped: signal_eff.json or bsum_wp.json missing')
    manifest['runtime_s'] = time.time() - t0
    C.jdump(manifest, out / 'manifest.json')
    manifest['schema_check'] = validate_outputs(out)
    C.jdump(manifest, out / 'manifest.json')
    log(f"schema check: {manifest['schema_check']}")
    log(f'done in {time.time() - t0:.0f} s -> {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
