"""g3_rerun.py -- G3 variant re-runs of finished G3 PU-only jobs (C001 Stage 4, G3 pilot; PU-only, no signal).

Pre-registered G3 checks that need the trials re-processed (the PU events are not stored; they are regenerated from the
job seed by the same chain, so the variant run sees the identical events, PV, MET roads and trial seeds):
  * (iv) T_seed stability (WP_RULE.md §6.4; plan §2.2 item 4, §11 G3 (iv)): the same job with finder.Config.tseed = 4
    instead of the frozen 6; analyse_g3.py compares the per-family pass fractions paired with the stored T_seed = 6 job.
  * C-4 diagnostic (WP_RULE.md §6.3): a rho = 2 job with nsub = 256 instead of 64; analyse_g3.py reports the S_ded shift.

The frozen runner is used UNCHANGED (acts.stage4.run_stage4.run_pu_job); only its config hook finder_configs is wrapped
to override the one variant parameter, and the job's output path is redirected to data/acts_stage4/g3/rerun/<tag>/, so
the G3 production files are never touched.  Reproducibility of the regenerated events is checked offline by
analyse_g3.py (chain.evstats and V4-1 records identical to the stored job).

    nice -n 15 pixi run python -m acts.stage4.g3.g3_rerun G3B1_00000 --tseed 4
    nice -n 15 pixi run python -m acts.stage4.g3.g3_rerun G3B2_00000 --nsub 256
"""
import argparse
import json
import os
import time

from acts.stage4 import run_stage4 as R


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('job_id')
    p.add_argument('--tseed', type=int, default=None)
    p.add_argument('--nsub', type=int, default=None)
    p.add_argument('--nice', type=int, default=15)
    a = p.parse_args(argv)
    if a.tseed is None and a.nsub is None:
        p.error('give --tseed and/or --nsub')
    try:
        os.nice(a.nice)
    except OSError:
        pass
    os.environ.setdefault('OMP_NUM_THREADS', '1')
    jobs = {j['id']: j for j in R.load_jobs('G3')}
    job = dict(jobs[a.job_id])
    tag = '_'.join(([f'tseed{a.tseed}'] if a.tseed is not None else []) + ([f'nsub{a.nsub}'] if a.nsub is not None else []))
    job['out'] = f'../g3/rerun/{tag}/{a.job_id}.npz'          # PROD/../g3/rerun/... = data/acts_stage4/g3/rerun/...
    orig = R.finder_configs

    def finder_configs(fz, job_, allow_interim):
        cfg, wcfg = orig(fz, job_, allow_interim)
        if a.tseed is not None:
            cfg.tseed = int(a.tseed)
        if a.nsub is not None:
            wcfg.nsub = int(a.nsub)
        return cfg, wcfg

    R.finder_configs = finder_configs
    t0 = time.time()
    res = R.run_pu_job(job, allow_interim=False)
    res['variant'] = tag
    res['elapsed_s'] = time.time() - t0
    print(json.dumps(res, default=str))
    log = R.out_path(job).parent / '_rerun_log.jsonl'
    with open(log, 'a') as f:
        f.write(json.dumps(res, default=str) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
