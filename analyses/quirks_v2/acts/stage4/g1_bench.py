"""G1 benchmark: PU-only production jobs (G1 chain + finder) timed end to end.  Signal-blind (PU only).

  pixi run python -m acts.stage4.g1_bench run  <tag> <rho> <n_jobs> <events_per_job> <roads> [workers]
  pixi run python -m acts.stage4.g1_bench summary <tag>
Jobs are ordinary run_stage4 PU jobs (run_pu_job; planning delta95 = 0.25, no freeze: development), seeds
blake2b("stage4|G1BENCH<tag>|<chunk>") (disjoint from every campaign).  Outputs data/acts_stage4/g1/bench/<tag>/.
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

import numpy as np

from . import run_stage4 as RS

OUT = RS.TT / 'data' / 'acts_stage4' / 'g1' / 'bench'


def jobs(tag, rho, n_jobs, per, roads):
    js = []
    for c in range(n_jobs):
        js.append(dict(id=f'G1BENCH{tag}_{c:05d}', campaign='g1bench', sample=f'G1BENCH{tag}', kind='pu', chunk=c,
                       ev0=c * per, n_events=per, roads=roads, rho=rho, seed=RS.hash_seed(f'stage4|G1BENCH{tag}|{c}'),
                       dump_events=0, est_s=0.0, mem_gb=1.5,
                       out=f'../g1/bench/{tag}/G1BENCH{tag}_{c:05d}.npz', requires='pu-chain'))
    return js


def _run(j):
    RS._worker_init(10)
    t0 = time.time()
    r = RS._safe_run(j, True)
    r['wall_job'] = time.time() - t0
    return r


def cmd_run(tag, rho, n_jobs, per, roads, workers=4):
    (OUT / tag).mkdir(parents=True, exist_ok=True)
    js = jobs(tag, rho, n_jobs, per, roads)
    RS.warmup()
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context('spawn')) as ex:
        res = list(ex.map(_run, js))
    for r in res:
        if 'error' in r:
            print(r['error'])
    (OUT / tag / 'run.json').write_text(json.dumps(dict(wall_s=time.time() - t0, workers=workers, res=res), default=str,
                                                   indent=1))
    return summary(tag)


def summary(tag):
    rows = []; ch = []; tr = []; v41 = []; est = []
    for p in sorted((OUT / tag).glob('*.npz')):
        with np.load(p) as z:
            m = json.loads(str(z['meta_json']))
            rho = m['job']['rho']; ne = m['job']['n_events']
            ct = z['chain.timing']
            ch.append(ct.sum(1))
            tt = z['trials.t_total']
            tr.append(tt)
            v41.append(m['v41_pass'])
            if 'chain.evstats' in z.files:
                est.append(z['chain.evstats'])
            rows.append(dict(file=p.name, wall_s=m['wall_s'], t_chain_s=m['t_chain_s'], n_events=ne, rho=rho,
                             trials=int(m['job']['n_events'] * m['job']['roads'])))
    ch = np.concatenate(ch); tr = np.concatenate(tr)
    rho = rows[0]['rho']
    wall = sum(r['wall_s'] for r in rows); nev = sum(r['n_events'] for r in rows); ntr = sum(r['trials'] for r in rows)
    tch = sum(r['t_chain_s'] for r in rows)
    E = np.concatenate(est) if est else None
    cols = ['ev', 'k'] + RS.EVSTAT_COLS
    d = dict(tag=tag, rho=rho, n_jobs=len(rows), n_events=nev, n_chain_events=len(ch), n_trials=ntr,
             chain_s_per_chain_event=dict(mean=float(ch.mean()), median=float(np.median(ch)),
                                          p90=float(np.percentile(ch, 90))),
             chain_wall_s_per_physics_event_incl_startup=tch / nev,
             trial_s=dict(mean=float(tr.mean()), median=float(np.median(tr)), p90=float(np.percentile(tr, 90))),
             job_wall_s_per_physics_event=wall / nev,
             v41_pass_all=bool(all(v41)),
             evstats_mean={c: float(E[:, k].mean()) for k, c in enumerate(cols) if k >= 2} if E is not None else None)
    (OUT / tag / 'summary.json').write_text(json.dumps(d, indent=1))
    print(json.dumps(d, indent=1))
    return d


if __name__ == '__main__':
    if sys.argv[1] == 'run':
        cmd_run(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]),
                int(sys.argv[7]) if len(sys.argv) > 7 else 4)
    else:
        summary(sys.argv[2])
