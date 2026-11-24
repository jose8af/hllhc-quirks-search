"""p3g_campaigns.py -- runner campaign files of work package p3-g (Tormod, 2026-11-24).  Pure stdlib; run on einstein:

  python3 -I phase3_selection/src/p3g/p3g_campaigns.py

Writes tools/runner/examples/p3g/<campaign>.json.  Development role (STR §4.17 rows 11, 13, 13a; row 5 regenerated);
no pilot or production campaign.  Prefix p3-g-.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
QV2 = REPO / 'analyses' / 'quirks_v2'
OUTD = REPO / 'tools' / 'runner' / 'examples' / 'p3g'
ENV = ('. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba '
       'PYTHONPYCACHEPREFIX=$QV2_SCRATCH_DIR/pyc QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH_DIR/pythia_init '
       'PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 && ')
PY = '$QV2/envs/tt/.pixi/envs/default/bin/python $QV2/phase3_selection/src/p3g/'
SRC = '/nfs/cajuela/jdochoa/quirks_v2/data/p3g/p3-g-prep/000/'
NPARTS = 6


def camp(name, desc, jobs, hours, rss=1500, timeout=1800):
    return dict(campaign=name, tier='final', data_prefix='p3g', description=desc, expected_hours=hours,
                regenerate='python3 -I phase3_selection/src/p3g/p3g_campaigns.py', defaults=dict(max_rss_mb=rss,
                                                                                               timeout_s=timeout),
                jobs=jobs)


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    C = {}
    jobs = [dict(id=f'prep-npo-p{p}', shard=0, outputs=[f'src_npo_p{p}.npz'],
                 command=ENV + PY + f'p3g_prep.py --mode npo --part {p} --nparts {NPARTS} --out $QV2_OUT_DIR/src_npo_p{p}.npz')
            for p in range(NPARTS)]
    jobs.append(dict(id='prep-dif', shard=0, outputs=['src_dif.npz'],
                     command=ENV + PY + 'p3g_prep.py --mode dif --n 1000 --out $QV2_OUT_DIR/src_dif.npz'))
    C['p3-g-prep'] = camp('p3-g-prep', 'p3-g source events: 1,000 Z(nunu) pilot near-pass events (P3A classes, '
                          'stratified in k(R05) = 0..3; 6 parts) for row 11, and 1,000 unbiased pilot DIF events for '
                          'row 13a', jobs, 2.0, rss=3000)
    jobs = []
    for p in range(NPARTS):
        for f in range(0, 220, 20):
            jid = f'npo-p{p}-{f:03d}'
            chunk = p * 1000 + f
            jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                             command=ENV + PY + f'p3g_ovl_job.py --id {jid} --mode npo --src {SRC}src_npo_p{p}.npz '
                             f'--first {f} --n 20 --stream pilot.ovl --chunk {chunk} --trials T1,T2'))
    C['p3-g-npo'] = camp('p3-g-npo', 'STR §4.17 row 11: the pilot\'s 1,000 near-pass overlays (Z(nunu) near-pass '
                         'events, P3A classes), PU 200, stream pilot.ovl; trials T1 (nominal) and T2 (own hits not '
                         'CKF-removed): per-k promotion, survival, S_CKF', jobs, 16.7)
    jobs = []
    for p in range(NPARTS):
        for f in range(0, 220, 20):
            jid = f'npo0-p{p}-{f:03d}'
            chunk = p * 1000 + f
            jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                             command=ENV + PY + f'p3g_ovl_job.py --id {jid} --mode npo --src {SRC}src_npo_p{p}.npz '
                             f'--first {f} --n 20 --stream pilot.ovl.mu0 --chunk {chunk} --trials T1,T2 --mu 0'))
    C['p3-g-npo0'] = camp('p3-g-npo0', 'reference for row 11: the same 1,000 near-pass events through the same '
                          'injection chain without pile-up (finder pass without pile-up, T1 and T2)', jobs, 0.4)
    jobs = [dict(id=f'dif-{f:04d}', shard=0, outputs=[f'dif-{f:04d}.npz'],
                 command=ENV + PY + f'p3g_ovl_job.py --id dif-{f:04d} --mode dif --src {SRC}src_dif.npz --first {f} '
                 f'--n 20 --stream dev.ovl.dif --chunk {f} --trials T1,T0') for f in range(0, 1000, 20)]
    C['p3-g-ovldif'] = camp('p3-g-ovldif', 'STR §4.17 row 13a: 1,000 unbiased Geant4 DIF overlays (pilot DIF events, '
                            'stored SimHits, PU 200, stream dev.ovl.dif); trials T1 and T0 (paired pile-up-only pass)',
                            jobs, 16.7)
    jobs = [dict(id=f'g4pu-{c:03d}', shard=0, outputs=[f'g4pu-{c:03d}.npz'],
                 command=ENV + PY + f'p3g_ovl_job.py --id g4pu-{c:03d} --mode g4pu --n 10 --stream dev.g4pu '
                 f'--chunk {c} --roads 3') for c in range(100)]
    C['p3-g-g4pu'] = camp('p3-g-g4pu', 'STR §4.17 row 13 (dev.g4pu): 1,000 PU-200 events with the Geant4 secondaries '
                          'of every pile-up hadron (pi, K, p, K0L, n), 3 roads per event; B1-g', jobs, 25.2, rss=2000)
    jobs = [dict(id=f'zhl-{c:03d}', shard=0, outputs=[f'zhl-{c:03d}.npz'],
                 command=ENV + PY + f'p3g_ovl_job.py --id zhl-{c:03d} --mode zhl --n 20 --chunk {c} --trials T1,T0')
            for c in range(25)]
    C['p3-g-zhl'] = camp('p3-g-zhl', 'STR §4.17 row 5 regenerated (stream c1.sm, same seeds: the first 20 events of '
                         'each of the 25 C1 jobs) with the paired pile-up-only pass (hard-scatter hits removed)',
                         jobs, 8.3)
    for k, v in C.items():
        (OUTD / f'{k}.json').write_text(json.dumps(v, indent=1))
        print(k, len(v['jobs']), 'jobs')


if __name__ == '__main__':
    main()
