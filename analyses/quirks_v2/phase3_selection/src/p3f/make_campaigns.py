"""Writes the p3-f campaigns (investigator Jorunn): p3-f-occx (Task A, method CAUSE_METHOD_jorunn.md) and p3-f-refind
(Task B).  python3 -I make_campaigns.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '$QV2/envs/tt/.pixi/envs/default/bin/python'
ENV = ('. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba '
       'PYTHONPYCACHEPREFIX=$QV2_SCRATCH_DIR/pyc PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 && ')
S = '$QV2/phase3_selection/src/p3f/'


def camp(name, desc, jobs, hours, rss):
    return dict(campaign=name, tier='final', data_prefix='p3f', description=desc, expected_hours=hours,
                regenerate='python3 -I phase3_selection/src/p3f/make_campaigns.py',
                defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)


def main():
    (HERE / 'campaigns').mkdir(exist_ok=True)
    jobs = []
    for k in range(100):
        ids = ','.join(f'c1pu1-{2 * k + i:04d}' for i in range(2))
        jid = f'occx-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}occx_job.py --id {jid} --jobs {ids} --planes 10000 --mode counts --nip-elig 5'))
    c = camp('p3-f-occx', 'p3-f Task A (CAUSE_METHOD_jorunn.md): frozen p3-b configuration ensemble on the C1 rho = 1 '
             'development hits (c1.pu1, 4,000 events, 16,000 trials), 10,000 configurations per trial, fixed and '
             'refit maps (amendment A1: per-configuration refit transfer; refit eligibility N_IP2 >= 5, N_IP2 = 5 '
             'stored separately)', jobs, 12.0, 1500)
    (HERE / 'campaigns' / 'p3-f-occx.json').write_text(json.dumps(c, indent=1))
    jobs = []
    for k in range(20):
        ids = ','.join(f'c1pu2-{2 * k + i:04d}' for i in range(2))
        jid = f'refind3-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}refind3_job.py --id {jid} --jobs {ids} --draws 3'))
    c = camp('p3-f-refind', 'p3-f Task B: thinning re-find yield, the 400 control trials of P3B R1 (C1 pu2 jobs '
             '0000-0039), 3 new thinning draws per trial, frozen rho = 1 finder re-run, hit sets stored', jobs, 4.2,
             2500)
    (HERE / 'campaigns' / 'p3-f-refind.json').write_text(json.dumps(c, indent=1))


if __name__ == '__main__':
    main()
