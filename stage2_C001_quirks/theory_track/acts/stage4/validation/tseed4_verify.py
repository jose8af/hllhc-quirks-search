"""tseed4_verify.py -- T_seed := 4 action (G3_REPORT §4, WP_RULE §6.4; HASH_ADDENDUM §5): verify that the PRODUCTION
code path now runs the finder at T_seed = 4.

G3 job G3B1_00000 (unchanged G3 manifest job dict) is run through run_stage4.run_pu_job exactly as a production worker
does (no config override: tseed comes from acts/stage4/frozen_inputs.json -> production.config_from_frozen), with only
its output path redirected to data/acts_stage4/tseed4_verify/.  Every npz array (except meta_json and the wall-clock
timers, as in g1b_regress) must be bit-identical to the stored T_seed = 4 re-run data/acts_stage4/g3/rerun/tseed4/
G3B1_00000.npz (g3_rerun.py: frozen runner, cfg.tseed overridden to 4 after finder_configs).  Negative control: the
stored T_seed = 6 production file prod/G3/G3B1/G3B1_00000.npz must differ in the finder outputs.

    nice -n 10 pixi run python -m acts.stage4.validation.tseed4_verify run
    pixi run python -m acts.stage4.validation.tseed4_verify compare
"""
import json
import os
import sys
import time

import numpy as np

from acts.stage4 import run_stage4 as RS

SKIP = {'meta_json', 'chain.timing', 'trials.times', 'trials.t_total'}    # wall-clock timers only (= g1b_regress)
JOB = 'G3B1_00000'
OUT_REL = f'../tseed4_verify/{JOB}.npz'                 # PROD/../tseed4_verify = data/acts_stage4/tseed4_verify
REF4 = RS.TT / 'data' / 'acts_stage4' / 'g3' / 'rerun' / 'tseed4' / f'{JOB}.npz'
REF6 = RS.PROD / 'G3' / 'G3B1' / f'{JOB}.npz'


def run():
    os.environ.setdefault('OMP_NUM_THREADS', '1')
    job = dict({j['id']: j for j in RS.load_jobs('G3')}[JOB])
    job['out'] = OUT_REL
    t0 = time.time()
    r = RS.run_pu_job(job, allow_interim=False)
    r['elapsed_s'] = time.time() - t0
    print(json.dumps(r, default=str), flush=True)


def diff_keys(pa, pb):
    za = np.load(pa); zb = np.load(pb)
    ka = set(za.files) - SKIP; kb = set(zb.files) - SKIP
    d = []
    for k in sorted(ka | kb):
        if k not in za.files or k not in zb.files:
            d.append(k + ' (missing)')
            continue
        x = za[k]; y = zb[k]
        if x.dtype != y.dtype or x.shape != y.shape or x.tobytes() != y.tobytes():
            d.append(k)
    return len(ka), d, json.loads(str(za['meta_json'])), json.loads(str(zb['meta_json']))


def compare():
    new = RS.out_path(dict(out=OUT_REL))
    n, d4, mn, m4 = diff_keys(new, REF4)
    _, d6, _, m6 = diff_keys(new, REF6)
    res = dict(job=JOB, new=str(new.relative_to(RS.TT)), ref_tseed4=str(REF4.relative_to(RS.TT)),
               ref_tseed6=str(REF6.relative_to(RS.TT)), n_keys=n,
               vs_tseed4=dict(n_diff=len(d4), diff=d4[:40]), vs_tseed6_negative_control=dict(n_diff=len(d6), diff=d6[:40]),
               meta_new=dict(finder_cfg=mn['finder_cfg'], frozen_finder_config=mn['frozen_inputs'].get('finder_config'),
                             frozen_t_seed=mn['frozen_inputs'].get('t_seed'),
                             run_stage4_sha=mn['code_sha256']['acts/stage4/run_stage4.py'],
                             run_chain_sha=mn['code_sha256']['acts/stage4/code/run_chain.py'],
                             replaced_events=mn['chain_meta'].get('replaced_events'), wall_s=mn['wall_s']),
               meta_ref4_finder_cfg=m4['finder_cfg'], meta_ref6_finder_cfg=m6['finder_cfg'])
    res['PASS'] = bool(not d4 and d6 and mn['finder_cfg']['tseed'] == 4)
    p = RS.TT / 'data' / 'acts_stage4' / 'tseed4_verify' / 'tseed4_verify.json'
    p.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    return 0 if res['PASS'] else 1


if __name__ == '__main__':
    sys.exit(run() if sys.argv[1] == 'run' else compare())
