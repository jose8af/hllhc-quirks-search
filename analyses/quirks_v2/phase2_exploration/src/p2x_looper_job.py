"""p2x_looper_job.py -- one job of the proper looper gun: v1's C'0 job (acts.stage4.run_g1b.run_cp0_job, UNCHANGED:
frozen finder configuration, rung ladder, looper attribution rule) on a chain file made by p2x_looper_chain.py instead
of `run_chain.py cp --topo looper`.  Only run_g1b.chain (the function that produces the chain file) is replaced.

  <tt python> p2x_looper_job.py --id ID --set nat|flat --chunk K --start EV0 --n N --pool <p2-c-px-ht-mb file>

Pattern of channel (i)'s c1_cp_job.py.  Outputs in $QV2_OUT_DIR: <id>.npz (v1 format: trials.*, cand.*, cp.*),
<id>.truth.npz (per-event particle and Geant4 record), <id>.summary.json (per-rung counts; no signal quantity).
"""
import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger('p2x_looper_job')
ACTSPY = str(QV2 / 'acts/.pixi/envs/default/bin/python')
ACTSENV = str(QV2 / 'acts/.pixi/envs/default')


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True); ap.add_argument('--set', required=True, choices=['nat', 'flat'])
    ap.add_argument('--chunk', type=int, required=True); ap.add_argument('--start', type=int, required=True)
    ap.add_argument('--n', type=int, required=True); ap.add_argument('--pool', required=True)
    a = ap.parse_args()
    job_dir = Path.cwd()
    work = job_dir / 's4work'
    (work / 'prod').mkdir(parents=True, exist_ok=True)
    os.environ['QV2_S4_DATA'] = str(work)
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)
    import numpy as np
    from acts.stage4 import run_stage4 as RS
    from acts.stage4 import run_g1b as G
    fz = RS.frozen_inputs()
    if fz is None or fz.get('wp_rule_sha256') != RS.sha256_file(RS.HERE / 'WP_RULE.md'):
        raise SystemExit('frozen_inputs / WP_RULE.md mismatch')
    seed = RS.hash_seed(f'qv2|px.looper.{a.set}|{a.chunk}')
    truth_tmp = {}

    def chain(job, tmp, args):          # replaces run_g1b.chain: same contract (writes the chain npz at `tmp`, returns seconds)
        env = dict(os.environ, CONDA_PREFIX=ACTSENV, PYTHIA8=ACTSENV, PYTHIA8_DIR=ACTSENV,
                   PYTHIA8DATA=ACTSENV + '/share/Pythia8/xmldoc', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
        env.pop('QV2_S4_DATA', None)
        t0 = time.time()
        p = subprocess.run([ACTSPY, str(HERE / 'p2x_looper_chain.py'), str(tmp), str(job['n_events']), str(job['seed']),
                            a.set, str(job['ev0']), a.pool], cwd=str(job_dir), env=env, capture_output=True, text=True)
        if p.returncode != 0 or not Path(tmp).exists():
            raise RuntimeError(f'looper chain failed ({p.returncode}): {p.stderr[-4000:]}')
        sys.stderr.write(p.stderr[-1500:])
        truth_tmp['f'] = str(tmp) + '.truth.npz'
        return time.time() - t0
    G.chain = chain
    job = dict(id=a.id, campaign='C1', sample='cp0', kind='cp0', topo='looper', chunk=a.chunk, n_events=a.n, roads=1, rho=1,
               seed=seed, dump_events=0, est_s=0.0, mem_gb=1.5, out=f'{a.id}.npz', requires='G1b', qv2_stream=f'px.looper.{a.set}',
               ev0=a.start)
    res = G.run_job(job)
    outd = Path(os.environ.get('QV2_OUT_DIR', str(job_dir)))
    final = RS.out_path(job)
    # ---- summary (counts of v1's own outputs; nothing is re-derived)
    z = np.load(final)
    rungs = json.loads(str(z['meta_json']))['rungs']
    E = z['cp.ev']; ec = [str(x) for x in z['cp.ev_cols']]
    nt = int(z['n_trials'])
    summ = dict(id=a.id, set=a.set, n_events=a.n, ev0=a.start, n_trials=nt, rungs=rungs[:14],
                events_skipped_fewer_than_3_pool_hits=int(E[:, ec.index('skipped')].sum()),
                events_with_candidate=int((E[:, ec.index('n_cand')] > 0).sum()),
                events_with_attributed_candidate=int((E[:, ec.index('n_attr_all')] > 0).sum()),
                events_with_attributed_candidate_passing_a_rung=int((E[:, ec.index('n_attr_any')] > 0).sum()),
                finder_cfg=json.loads(str(z['meta_json']))['finder_cfg'], v41_pass=res.get('v41_pass'), wall_s=res.get('wall'),
                t_chain_s=res.get('t_chain'))
    if nt:
        npass = z['trials.n_pass']
        summ.update(events_passing_rung={r: int((npass[:, k] > 0).sum()) for k, r in enumerate(rungs[:14])},
                    candidates_passing_rung={r: int(npass[:, k].sum()) for k, r in enumerate(rungs[:14])},
                    trials_with_road_hits_ge3=nt,
                    trials_with_seed=int((z['trials.n_trip'] > 0).sum()), trials_with_refit=int((z['trials.n_refit'] > 0).sum()),
                    trials_with_kept_candidate=int((z['trials.n_kept_all'] > 0).sum()),
                    trials_ip2ge6=int((z['trials.n_ip2ge6'] > 0).sum()), trials_ip2ge7=int((z['trials.n_ip2ge7'] > 0).sum()),
                    mean_n_road=float(z['trials.n_road'].mean()))
        deep = [int(t) for t in np.nonzero(npass[:, 3] > 0)[0]]          # R04 or deeper
        summ['trials_passing_R04'] = [dict(trial=t, cp_ev=int(z['trials.ev'][t]) + a.start) for t in deep[:50]]
    z.close()
    shutil.move(str(final), str(outd / f'{a.id}.npz'))
    shutil.move(truth_tmp['f'], str(outd / f'{a.id}.truth.npz'))
    (outd / f'{a.id}.summary.json').write_text(json.dumps(summ, indent=1))
    log.info('summary: %s', json.dumps(summ))
    shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    main()
