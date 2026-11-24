"""B2 production campaign DEFINITIONS (p3-b, Casper) — written, NOT launched (PHASE3_BRIEF §2: production is launched by
the orchestrator, after PREREG_v2.md is hashed; STR §4.17: samples 14-25 do not exist before the hash, brief D7).

  B2-d  sample 14  pile-up ρ = 1 direct, 24,000 events × 4 roads = 96,000 trials, stream prod.pu1 (test sample of
        B2-a / B2-b, cumulative and crossing rungs; direct counts R04-R07).  20 events per job (C1 unit cost 55.7 s per
        event [EXP §3.1] -> ≈ 1,114 s per job, below the 30-min limit), 1,200 jobs, ≈ 371 CPU-h; no chain dumps
        (the R04 candidate records with their variables and the hit records of R05 passers are kept by the job, as C1).
  ρ = 2 sample 15  3,000 events × 2 roads = 6,000 trials, stream prod.pu2, pre-merge store N_IP2 >= 6 (B2-a production);
        5 events per job (203 s per event -> ≈ 1,015 s per job), 600 jobs, ≈ 169 CPU-h; max RSS 2.1 GB at 5-8
        events per job -> at most 2 ρ = 2 jobs per node (EXP §3.1, STR §4.5 rule 2); pre-merge ≈ 33.8 MB per trial ->
        ≈ 203 GB (below the 400 GB cap, D-i-1).
  The repaired thinning of sample 15 is then run with p3-b-thin's code (thin_job.py, K = 64) pointed at prod-pu2.
Launch (orchestrator):  qv2run ssh launch <json> --nodes landau,maxwell,schrodinger [--max-per-node N] --on <node>
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '$QV2/envs/tt/.pixi/envs/default/bin/python'
ENV = ('. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba '
       'PYTHONPYCACHEPREFIX=$QV2_SCRATCH_DIR/pyc QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH_DIR/pythia_init '
       'PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 && ')
JOB = '$QV2/phase2_exploration/src/c1_pu_job.py'


def main():
    jobs = []
    for k in range(1200):
        jid = f'prodpu1-{k:04d}'
        jobs.append(dict(id=jid, shard=k // 400, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {JOB} --id {jid} --stream prod.pu1 --chunk {k} --ev0 {20 * k} --n 20 '
                                       f'--rho 1 --roads 4 --dump 0 --kind pu'))
    c = dict(campaign='p4a-b2-prod-pu1', tier='final', data_prefix='prod',
             description='B2-d (STR §4.17 row 14): pile-up rho = 1 direct test sample, 24,000 events, 96,000 trials, '
                         'stream prod.pu1, independent of c1.pu1/dev.pu1. DO NOT LAUNCH before PREREG_v2 is hashed.',
             expected_hours=371.0, regenerate='python3 -I phase3_selection/src/p3b/make_prod_campaigns.py',
             defaults=dict(max_rss_mb=1200, timeout_s=1800), jobs=jobs)
    (HERE / 'campaigns' / 'prod' / 'p4a-b2-prod-pu1.json').write_text(json.dumps(c, indent=1))
    jobs = []
    for k in range(600):
        jid = f'prodpu2-{k:04d}'
        jobs.append(dict(id=jid, shard=k // 300, outputs=[f'{jid}.npz', f'{jid}.premerge.npz'],
                         command=ENV + f'{PY} {JOB} --id {jid} --stream prod.pu2 --chunk {k} --ev0 {5 * k} --n 5 '
                                       f'--rho 2 --roads 2 --dump 0 --kind pu --premerge 6'))
    c = dict(campaign='p4a-b2-prod-pu2', tier='final', data_prefix='prod',
             description='B2 (STR §4.17 row 15): pile-up rho = 2, 3,000 events, 6,000 trials, pre-merge store '
                         'N_IP2 >= 6, stream prod.pu2. At most 2 jobs per node (RSS 2.1 GB). DO NOT LAUNCH before '
                         'PREREG_v2 is hashed.',
             expected_hours=169.0, regenerate='python3 -I phase3_selection/src/p3b/make_prod_campaigns.py',
             defaults=dict(max_rss_mb=2300, timeout_s=1800), jobs=jobs)
    (HERE / 'campaigns' / 'prod' / 'p4a-b2-prod-pu2.json').write_text(json.dumps(c, indent=1))


if __name__ == '__main__':
    main()
