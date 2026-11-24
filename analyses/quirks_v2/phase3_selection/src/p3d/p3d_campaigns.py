"""p3d_campaigns.py -- writes the runner campaign files tools/runner/campaigns/p3-d-*.json.  Gorm, 2026-11-24.
Light (standard library only; einstein).  Usage: python3 -I p3d_campaigns.py <name> [args]
  pyhf            maxwell (numpy env): pyhf ToyCalculator demonstration (m = 0) and shapesys references; exact sums
  one             schrodinger (jax env): T1-c (i), (ii) with our convention; recipe test on the v1-mode workspace
  lim <spec> <settings> <tag> <seed> <ntoys> <quantiles> [prior campaign:job ...]   one resumable limit job
  store <spec> <settings> <tag> <fid> <m' list> <mu list>                           stored distributions
  cover <spec> <settings> <tag> <fid> <mu_true> <npe> <store campaign>               coverage pseudo-experiments
  exact_cref <tag> <kappa> <s> <b0>                                                   c_ref sums (maxwell)
"""
import json
import sys
from pathlib import Path

REPO = Path('/home/users/jdochoa/hllhc-quirks-search')
SRC = REPO / 'analyses/quirks_v2/phase3_selection/src/p3d'
CAMP = REPO / 'tools/runner/campaigns'
DATA = REPO / 'analyses/quirks_v2/data/p3d'
PY_JAX = '/home/scratch/jdochoa/envs/pyhf_toys/.pixi/envs/default/bin/python'
PY_NP = str(REPO / 'analyses/quirks_v2/phase1_strategy/src/pyhf_bench/.pixi/envs/default/bin/python')
ENV = ("export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 "
       "XLA_FLAGS='--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1' JAX_PLATFORMS=cpu && ")


def job(jid, py, args, ext='json'):
    out = f'{jid}.{ext}'
    return {'id': jid, 'shard': 0, 'outputs': [out],
            'command': ENV + f'{py} -I {SRC}/{args[0]} ' + ' '.join([args[1], f'$QV2_OUT_DIR/{out}'] + list(args[2:]))}


def write(name, jobs, desc, hours, rss=1500):
    c = {'campaign': name, 'tier': 'regenerable', 'data_prefix': 'p3d',
         'regenerate': f'python3 -I {SRC}/p3d_campaigns.py (see docstring)', 'description': desc,
         'expected_hours': hours, 'defaults': {'max_rss_mb': rss, 'timeout_s': 1800}, 'jobs': jobs}
    p = CAMP / f'{name}.json'
    p.write_text(json.dumps(c, indent=1) + '\n')
    sys.stdout.write(f'{p}: {len(jobs)} jobs\n')


def q(s):
    return "'" + s + "'"


def main(a):
    if a[0] == 'pyhf':
        jobs = [job(f'p3-d-pyhf-demo0-k{k}', PY_NP, ['p3d_pyhfstd.py', 'demo0', k, '2000']) for k in ('1', '10', '35')]
        jobs += [job(f'p3-d-pyhf-std-k{k}-m{m}', PY_NP, ['p3d_pyhfstd.py', 'std', k, m, '2000', '2026112400'])
                 for k in ('1', '10', '35') for m in ('100', '1000')]
        mus = ','.join(f'{x:g}' for x in (0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 80,
                                          100))
        jobs += [job('p3-d-exact-table', PY_NP, ['p3d_exact.py', 'table']),
                 job('p3-d-exact-curves', PY_NP, ['p3d_exact.py', 'curves', '1,10,35', '0', mus])]
        write('p3-d-pyhf', jobs, "T1-c (i)/(ii) references: pyhf's own ToyCalculator (numpy) and exact one-bin sums", 2.0)
    elif a[0] == 'one':
        jobs = []
        for k in ('1', '10', '35'):
            jobs.append(job(f'p3-d-one-c1-k{k}', PY_JAX, ['p3d_toys.py', 'limit', f'onebin_k{k}_m0', 'censor=1',
                                                            '2026112401', '2000', '0.16,0.5,0.84', '1500']))
        for k in ('1', '10', '35'):
            for m in ('100', '1000'):
                jobs.append(job(f'p3-d-one-c2-k{k}-m{m}', PY_JAX, ['p3d_toys.py', 'limit', f'onebin_k{k}_m{m}',
                                                                    'censor=1', '2026112402', '2000', '0.16,0.5,0.84',
                                                                    '1500']))
        for i in range(10):
            jid = f'p3-d-one-rec-{i:02d}'
            jobs.append({'id': jid, 'shard': 0, 'outputs': [f'{jid}.json'],
                         'command': ENV + f'{PY_JAX} -I {SRC}/p3d_rec_v1mode.py $QV2_OUT_DIR/{jid}.json '
                                    f'{2026111701 + i} 1000 1500'})
        write('p3-d-one', jobs, 'T1-c (i), (ii) with the convention; the refined recipe on the v1-mode workspace', 4.0)
    elif a[0] == 'ph':
        jobs = [{'id': f'p3-d-ph-check-{n}', 'shard': 0, 'outputs': [f'p3-d-ph-check-{n}.json'],
                 'command': ENV + f'{PY_NP} -I {SRC}/p3d_check_np.py $QV2_OUT_DIR/p3-d-ph-check-{n}.json {n}'}
                for n in ('v2ph', 'v1count_p1', 'v1count_p2')]
        write('p3-d-ph', jobs, 'T1-a: schema, consistency, predictive of the v2 placeholder and v1-count workspaces', 0.1)
    elif a[0] == 'phcost':
        jobs = [job(f'p3-d-phcost-{n}', PY_JAX, ['p3d_toys.py', 'cost', n, '-', '200', mu])
                for n, mu in (('v2ph', '0.03'),)]
        jobs += [job('p3-d-phcost-v2ph-check', PY_JAX, ['p3d_toys.py', 'check', 'v2ph', '-'])]
        write('p3-d-phcost', jobs, 'toy cost probe and jax check on the v2 placeholder workspace', 0.3)
    elif a[0] == 'lim':
        spec, settings, tag, seed, ntoys, qs = a[1:7]
        priors = [str(DATA / c / '000' / f'{j}.json') for c, j in (x.split(':') for x in a[7:])]
        name = f'p3-d-lim-{tag}'
        write(name, [job(name, PY_JAX, ['p3d_toys.py', 'limit', spec, settings, seed, ntoys, qs, '1500'] + priors)],
              f'expected limit {spec} {settings}', 0.5)
    elif a[0] == 'store':
        spec, settings, tag, fid, mps, mus = a[1:7]
        jobs = [job(f'p3-d-st-{tag}-m{mp}', PY_JAX, ['p3d_toys.py', 'store', spec, settings, '2026112410', '1000',
                                                     q(fid), mp, mus]) for mp in mps.split(',')]
        write(f'p3-d-st-{tag}', jobs, f'stored q distributions {spec} {settings}', 0.5 * len(jobs))
    elif a[0] == 'cover':
        spec, settings, tag, fid, mu_true, npe, scamp = a[1:8]
        files = sorted(str(p) for p in (DATA / scamp / '000').glob(f'{scamp}-m*.json'))
        jobs = [job(f'p3-d-cov-{tag}-l{lam}', PY_JAX, ['p3d_toys.py', 'cover', spec, settings, '2026112420', q(fid),
                                                       mu_true, lam, npe] + files + (['--bonly'] if i == 0 else []))
                for i, lam in enumerate(('0.5', '1.139', '2', '3'))]
        write(f'p3-d-cov-{tag}', jobs, f'coverage pseudo-experiments {spec} {settings}', 2.0)
    elif a[0] == 'exact_cref':
        tag, kappa, s, b0 = a[1:5]
        write(f'p3-d-cref-{tag}', [job(f'p3-d-cref-{tag}', PY_NP, ['p3d_exact.py', 'cref', kappa, s, b0,
                                                                     '0.5,1.139,2,3'])], 'c_ref exact sums', 0.2)


if __name__ == '__main__':
    main(sys.argv[1:])
