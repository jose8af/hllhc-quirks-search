"""bench_s4_pu.py -- feasibility A (Anselm): one B1-like Stage-4 PU-200 job of N events, for timing.

Calls acts.stage4.run_stage4.run_pu_job (the v1 production path, unmodified logic): the acts-env chain
acts/stage4/code/run_chain.py (Pythia8 PU 200 overlay -> Fatras -> smearing digitisation -> GridTriplet + CKF), then on
the TT side the TDR top-up, CKF removal, analysis-level merging (finder/chain_inputs.py) and the plane finder
(finder/production.process_trial) on `roads` trials per event.  Development configuration (campaign 'smoke':
freeze-candidate values are absent in v2, so the planning values are used, as v1's smoke did).
Background only (pile-up); no signal is touched.

Run from analyses/quirks_v2 in the TT env, with QV2_S4_DATA pointing to the output area:
  QV2_S4_DATA=<dir> pixi run --manifest-path envs/tt/pixi.toml python phase1_strategy/src/bench_s4_pu.py \
      <tag> <n_events> <roads> <rho> <seed>
Prints one JSON line: wall, chain wall (t_chain), TT-side time, finder time per trial, output bytes.
"""
import json
import os
import sys
import time
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(QV2))
os.chdir(QV2)


def main():
    tag, n, roads, rho, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    from acts.stage4 import run_stage4 as RS
    job = dict(id=f'{tag}_00000', campaign='smoke', sample=tag, kind='pu', chunk=0, ev0=0, n_events=n, roads=roads,
               rho=rho, seed=seed, dump_events=0, est_s=0.0, mem_gb=1.5, order=0, out=f'bench/{tag}/{tag}_00000.npz',
               requires='pu-chain')
    t0 = time.perf_counter(); c0 = time.process_time()
    r = RS.run_pu_job(job, allow_interim=False)
    wall = time.perf_counter() - t0
    import numpy as np
    with np.load(RS.out_path(job)) as z:
        m = json.loads(str(z['meta_json']))
        tim = z['chain.timing'] if 'chain.timing' in z.files else None
        cols = [str(c) for c in z['chain.timing_cols']] if 'chain.timing_cols' in z.files else []
    res = dict(tag=tag, n_events=n, roads=roads, rho=rho, n_trials=r['n_trials'], wall_s=wall, t_chain_s=r['t_chain'],
               tt_side_s=wall - r['t_chain'], tt_cpu_s=time.process_time() - c0, bytes=r['bytes'],
               v41_pass=r.get('v41_pass'), chain_stage_s=(dict(zip(cols, tim.sum(0).tolist())) if tim is not None else None),
               finder_s_per_trial=(wall - r['t_chain']) / max(r['n_trials'], 1), out=str(RS.out_path(job)))
    sys.stdout.write('BENCH_S4 ' + json.dumps(res) + '\n')


if __name__ == '__main__':
    main()
