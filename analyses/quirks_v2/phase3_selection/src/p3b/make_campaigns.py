"""Writes the p3-b development campaigns (Casper): p3-b-thin (repaired thinning on C1 pu2) and p3-b-direct (direct
development counts on C1 pu1).  python3 -I make_campaigns.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '$QV2/envs/tt/.pixi/envs/default/bin/python'
ENV = ('. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba '
       'PYTHONPYCACHEPREFIX=$QV2_SCRATCH_DIR/pyc PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 && ')
S = '$QV2/phase3_selection/src/p3b/'


def camp(name, desc, jobs, hours, rss):
    return dict(campaign=name, tier='final', data_prefix='p3b', description=desc, expected_hours=hours,
                regenerate='python3 -I phase3_selection/src/p3b/make_campaigns.py',
                defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)


def main():
    jobs = []
    for k in range(50):
        ids = ','.join(f'c1pu2-{4 * k + i:04d}' for i in range(4))
        jid = f'thin-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}thin_job.py --id {jid} --jobs {ids} --K 64'))
    c = camp('p3-b-thin', 'B2-a repaired thinning (STR §4.5 (a), [SD4]) of the C1 rho = 2 development sample '
             '(p2-a-c1-pu2, 1,000 events, 2,000 trials), K = 64, q = 1/2, grouping at rho = 1', jobs, 1.5, 1500)
    (HERE / 'campaigns' / 'p3-b-thin.json').write_text(json.dumps(c, indent=1))
    jobs = []
    for k in range(4):
        ids = ','.join(f'c1pu1-{50 * k + i:04d}' for i in range(50))
        jid = f'direct-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}direct_job.py --id {jid} --jobs {ids}'))
    c = camp('p3-b-direct', 'B2 direct rho = 1 development counts per trial and column (p2-a-c1-pu1, 4,000 events, '
             '16,000 trials), same column flags as the thinning', jobs, 0.1, 1500)
    (HERE / 'campaigns' / 'p3-b-direct.json').write_text(json.dumps(c, indent=1))
    jobs = []
    for k in range(20):
        ids = ','.join(f'c1pu1-{10 * k + i:04d}' for i in range(10))
        jid = f'occin-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}occin_job.py --id {jid} --jobs {ids} --planes 1000'))
    c = camp('p3-b-occin', 'B2-b occupancy-model inputs on the C1 rho = 1 development sample (p2-a-c1-pu1, 4,000 '
             'events): replayed finder pools, per-surface z densities, random-plane ensemble on real hits (1,000 '
             'planes per trial)', jobs, 1.0, 2000)
    (HERE / 'campaigns' / 'p3-b-occin.json').write_text(json.dumps(c, indent=1))
    jobs = []
    for k in range(8):
        jid = f'occmod-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}occmod_job.py --id {jid} --inputs $QV2_DATA/p3b/p3-b-occin '
                                       f'--seed {1000 + k} --nA 50000 --nB 800 --nplain 200 --nis 200 --beta 0.5'))
    c = camp('p3-b-occmod', 'B2-b occupancy model evaluated on the configuration ensemble with the development '
             'densities of p3-b-occin (8 independent seeds)', jobs, 3.5, 2000)
    c['after'] = [str(HERE / 'campaigns' / 'p3-b-occin.json')]
    (HERE / 'campaigns' / 'p3-b-occmod.json').write_text(json.dumps(c, indent=1))
    jobs = []
    for k in range(20):
        ids = ','.join(f'c1pu2-{2 * k + i:04d}' for i in range(2))
        jid = f'refind-{k:03d}'
        jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                         command=ENV + f'{PY} {S}refind_job.py --id {jid} --jobs {ids} --draws 1'))
    c = camp('p3-b-refind', 'B2-a remediation 1 (control): rho = 2 development events with dumps (C1 pu2 jobs '
             '0000-0039, 200 events, 400 trials) thinned at hit level, frozen rho = 1 finder re-run', jobs, 1.7, 2500)
    (HERE / 'campaigns' / 'p3-b-refind.json').write_text(json.dumps(c, indent=1))


if __name__ == '__main__':
    main()
