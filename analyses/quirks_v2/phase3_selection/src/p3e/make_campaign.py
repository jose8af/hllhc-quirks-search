"""Write the runner campaign p3-e-devpu1 (STR §4.17 row 12: enlarged development closure sample, rho = 1, stream dev.pu1).

  python3 -I phase3_selection/src/p3e/make_campaign.py        (from AN; writes src/p3e/campaigns/p3-e-devpu1.json)

Same chain, job script and output schema as the C1 rho = 1 sample c1.pu1 (tools/runner/campaigns/p2-a-c1-pu1.json):
phase2_exploration/src/c1_pu_job.py --rho 1 --roads 4 --dump <n> --kind pu, 20 events per job, so that the p3-b readers
(direct_job.job_counts, occ_replay.replay) read it unchanged.  Differences from c1.pu1: the stream name (dev.pu1), the
per-job NUMBA_CACHE_DIR / pyc / Pythia-init caches under the job scratch $QV2_SCRATCH_DIR (EXP §10 item 13; c1.pu1 used
a per-node cache), data_prefix p3e, and max_rss_mb = the measured c1.pu1 maximum (the wrapper's memory limit is 1.5x).
Job seed = blake2b("qv2|dev.pu1|<chunk>") (c1_pu_job.py -> run_stage4.hash_seed).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = 'p3-e-devpu1'
STREAM = 'dev.pu1'
N_EVENTS = 5960            # STR §4.17 row 12 "≈ 5,960 events"
PER_JOB = 20               # as c1.pu1 (max measured job 1318 CPU-s, 1329 s wall; cap 1800 s)
MAX_RSS_MB = 703           # c1.pu1 max RSS 702.6 MB over 200 done markers (ledger/markers/p2-a-c1-pu1/000)
ENV = ('. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba '
       'PYTHONPYCACHEPREFIX=$QV2_SCRATCH_DIR/pyc QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH_DIR/pythia_init '
       'PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1')
PY = '$QV2/envs/tt/.pixi/envs/default/bin/python $QV2/phase2_exploration/src/c1_pu_job.py'


def jobs():
    assert N_EVENTS % PER_JOB == 0
    out = []
    for k in range(N_EVENTS // PER_JOB):
        jid = f'devpu1-{k:04d}'
        cmd = (f'{ENV} && {PY} --id {jid} --stream {STREAM} --chunk {k} --ev0 {PER_JOB * k} --n {PER_JOB} '
               f'--rho 1 --roads 4 --dump {PER_JOB} --kind pu')
        out.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'], command=cmd))
    return out


def main():
    J = jobs()
    c = dict(campaign=NAME, tier='final', data_prefix='p3e',
             description=(f'STR §4.17 row 12: enlarged development closure sample, pile-up rho = 1, 4 roads, '
                          f'{N_EVENTS:,} events ({4 * N_EVENTS:,} trials), {PER_JOB} per job, {len(J)} jobs, stream '
                          f'{STREAM}, role development (decision point 2, s_model, crossing rungs); same chain and '
                          f'output schema as c1.pu1 (hit dumps for every event); independent of prod.pu1 (row 14)'),
             expected_hours=round(len(J) * 1115 / 3600, 1),
             regenerate='python3 -I phase3_selection/src/p3e/make_campaign.py',
             defaults=dict(max_rss_mb=MAX_RSS_MB, timeout_s=1800),
             jobs=J)
    p = HERE / 'campaigns' / f'{NAME}.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(c, indent=1, ensure_ascii=False) + '\n')
    print(p, len(J), 'jobs')


if __name__ == '__main__':
    main()
