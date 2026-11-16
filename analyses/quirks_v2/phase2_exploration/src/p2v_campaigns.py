"""p2v_campaigns.py -- runner campaign files of the T1 toy-cost study (executor Viktor, 2026-11-16).

  python3 -I p2v_campaigns.py <name>       (light: einstein; writes tools/runner/examples/p2v/<campaign>.json)

Campaign names p2-c-toy-*; outputs data/p2c/<campaign>/000/<job>.json, markers ledger/markers/<campaign>/.
Synthetic sizes as p2-c-t-pyhf: (terms, nuisances) = (25, 5) -> 31, (45, 14) -> 60, (60, 19) -> 80, (75, 24) -> 100
parameters.  Every job runs src/p2v_toys.py (see its docstring for the config keys).
"""
import json
import logging
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = REPO / 'tools' / 'runner' / 'examples' / 'p2v'
SRC = str(HERE)
PY = {'old': str(REPO / 'analyses/quirks_v2/phase1_strategy/src/pyhf_bench/.pixi/envs/default/bin/python'),
      'new': '/home/scratch/jdochoa/envs/pyhf_toys/.pixi/envs/default/bin/python'}
SIZES = {31: (25, 5), 60: (45, 14), 80: (60, 19), 100: (75, 24)}
ENV = ('export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 '
       "XLA_FLAGS='--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1' "
       'JAX_PLATFORMS=cpu && ')
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p2v_campaigns')


def job(camp, tag, npar, ntoy, mu, conf='-', env='old', toy_seed=None):
    nt, nn = SIZES[npar]
    jid = f'{camp}-{tag}'
    ts = f' 20261116 {toy_seed}' if toy_seed else ''
    return dict(id=jid, outputs=[f'{jid}.json'],
                command=ENV + f"{PY[env]} -I {SRC}/p2v_toys.py $QV2_OUT_DIR/{jid}.json {nt} {nn} {ntoy} {mu} '{conf}'{ts}")


def write(name, jobs, hours, description, rss=1500):
    d = dict(campaign=name, tier='regenerable', data_prefix='p2c',
             regenerate=f'python3 -I {SRC}/p2v_campaigns.py {name}', description=description,
             expected_hours=hours, defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / f'.{name}.json.tmp'
    tmp.write_text(json.dumps(d, indent=1) + '\n')
    tmp.replace(OUT / f'{name}.json')
    log.info('%s: %d jobs -> %s', name, len(jobs), OUT / f'{name}.json')


def main(argv):
    name = argv[0]
    c = name
    if name.startswith('p2-c-toy-smoke'):   # every code path on 5 + 5 toys at 31 parameters
        jobs = [job(c, 'std', 31, 5, 3),
                job(c, 'jax-scipy', 31, 5, 3, 'backend=jax', 'new'),
                job(c, 'jax-minuit-merged-chain', 31, 5, 3, 'backend=jax,opt=minuit,layout=merged,start=chain', 'new'),
                job(c, 'np-stitch-prev-fix', 31, 5, 3, 'stitch=1,start=prev,fixneg=0.05,tol=1e-6', 'new')]
        write(name, jobs, 0.1, 'T1 toy cost: smoke of every code path of p2v_toys.py')
    elif name == 'p2-c-toy-jax':       # (b) gradient backend, (d) merged layout, (e) start values / stitch; mu pilot
        J = 'backend=jax'
        jobs = [job(c, f'pilot-n31-mu{m}', 31, 500, m, J, 'new') for m in ('1.5', '2', '4', '6')]
        jobs += [job(c, 'js-n31-mu3', 31, 200, 3, J, 'new'),
                 job(c, 'js-n60-mu3-a', 60, 50, 3, J, 'new'),
                 job(c, 'js-n60-mu3-b', 60, 50, 3, J, 'new', toy_seed=20261217),
                 job(c, 'js-n80-mu3', 80, 100, 3, J, 'new'),
                 job(c, 'js-n100-mu3', 100, 100, 3, J, 'new'),
                 job(c, 'jm-n31-mu3', 31, 100, 3, J + ',opt=minuit', 'new'),
                 # pyhf's minuit optimiser always runs hesse() (N^2 calls): 1254 s per unit at 31 par; 60 par on 4
                 # toys only (same id: the 50-toy attempt was stopped at 14:18, > 30 min projected; the runner needs the id); no 100-par job
                 job(c, 'jm-n60-mu3-a', 60, 4, 3, J + ',opt=minuit', 'new'),
                 job(c, 'jsmerged-n31-mu3', 31, 200, 3, J + ',layout=merged', 'new'),
                 job(c, 'jsmerged-n60-mu3-a', 60, 50, 3, J + ',layout=merged', 'new'),
                 job(c, 'jsmerged-n100-mu3', 100, 100, 3, J + ',layout=merged', 'new'),
                 job(c, 'jschain-n60-mu3-a', 60, 50, 3, J + ',start=chain', 'new'),
                 job(c, 'jschain-n100-mu3', 100, 100, 3, J + ',start=chain', 'new'),
                 job(c, 'jsstitch-n60-mu3-a', 60, 50, 3, J + ',stitch=1', 'new'),
                 job(c, 'jsstitch-n100-mu3', 100, 100, 3, J + ',stitch=1', 'new'),
                 job(c, 'jsprev-n60-mu3-a', 60, 50, 3, J + ',start=prev', 'new')]
        write(name, jobs, 1.0, 'T1 toy cost: jax backend with scipy and minuit, merged layout, start values, stitch')
    elif name == 'p2-c-toy-ref':       # CLs check at mu_c = 5 (pilot p2-c-toy-jax: CLs 0.24 at 4, 0.04 at 6), 31 par
        J = 'backend=jax'
        R = ',record=1'
        jobs = [job(c, 'np-n31-mu5', 31, 1000, 5, 'record=1'),
                job(c, 'js-n31-mu5', 31, 1000, 5, J + R, 'new'),
                job(c, 'jsms-n31-mu5', 31, 1000, 5, J + ',layout=merged,stitch=1' + R, 'new'),
                job(c, 'jschain-n31-mu5', 31, 1000, 5, J + ',start=chain' + R, 'new'),
                job(c, 'jsmsp2-n31-mu5', 31, 1000, 5, J + ',layout=merged,stitch=1,start=prev2' + R, 'new'),
                job(c, 'jsmsp-n31-mu5', 31, 1000, 5, J + ',layout=merged,stitch=1,start=prev' + R, 'new'),
                job(c, 'jm-n31-mu5', 31, 500, 5, J + ',opt=minuit' + R, 'new'),
                job(c, 'mina-n31-mu5', 31, 300, 5, 'opt=minuit' + R)]
        write(name, jobs, 0.6, 'T1 toy cost: CLs correctness check at mu = 5 on 31 parameters, 1000 + 1000 paired toys')
    elif name == 'p2-c-toy-tune':      # accuracy of the minima (NLL recorded) and the combined configuration
        J = 'backend=jax'; R = ',record=1'; MS = ',layout=merged,stitch=1'
        jobs = [job(c, 'rec-js-n100-mu3', 100, 100, 3, J + R, 'new'),
                job(c, 'rec-jstight-n100-mu3', 100, 100, 3, J + ',tol=1e-10' + R, 'new'),
                job(c, 'rec-jschain-n100-mu3', 100, 100, 3, J + ',start=chain' + R, 'new'),
                job(c, 'rec-jm-n31-mu3', 31, 100, 3, J + ',opt=minuit' + R, 'new'),
                job(c, 'rec-jmtight-n31-mu3', 31, 50, 3, J + ',opt=minuit,tol=1e-4,strategy=1' + R, 'new'),
                job(c, 'jsms-n60-mu3-a', 60, 100, 3, J + MS + R, 'new'),
                job(c, 'jsms-n80-mu3', 80, 100, 3, J + MS + R, 'new'),
                job(c, 'jsms-n100-mu3', 100, 100, 3, J + MS + R, 'new'),
                job(c, 'jsmsc-n100-mu3', 100, 100, 3, J + MS + ',start=chain' + R, 'new'),
                job(c, 'jsmsp-n60-mu3-a', 60, 100, 3, J + MS + ',start=prev' + R, 'new'),
                job(c, 'jsmsp-n80-mu3', 80, 100, 3, J + MS + ',start=prev' + R, 'new'),
                job(c, 'jsmsp-n100-mu3', 100, 100, 3, J + MS + ',start=prev' + R, 'new'),
                job(c, 'jsmsp2-n100-mu3', 100, 100, 3, J + MS + ',start=prev2' + R, 'new'),
                job(c, 'jsmsp2-n31-mu3', 31, 200, 3, J + MS + ',start=prev2' + R, 'new')]
        write(name, jobs, 0.6, 'T1 toy cost: minimum accuracy with recorded NLL; merged + stitch at 60/80/100')
    elif name == 'p2-c-toy-base':      # step 1: baseline reproduction, profile; (a) minuit on numpy; stitch; 100 par pair
        jobs = [job(c, 'n31-mu3', 31, 200, 3),
                job(c, 'n60-mu3-a', 60, 50, 3),
                job(c, 'n60-mu3-b', 60, 50, 3, toy_seed=20261217),
                job(c, 'prof-n31', 31, 30, 3, 'profile=1'),
                job(c, 'prof-n60', 60, 10, 3, 'profile=1'),
                job(c, 'mina-n31-mu3', 31, 200, 3, 'opt=minuit'),
                job(c, 'mina-n60-mu3-a', 60, 6, 3, 'opt=minuit'),
                job(c, 'stitch-n60-mu3-a', 60, 50, 3, 'stitch=1'),
                job(c, 'n100-mu3', 100, 20, 3)]
        write(name, jobs, 1.5, 'T1 toy cost: baseline numpy+scipy at 31/60/100 par, profile, minuit on numpy, stitch')
    else:
        raise SystemExit(f'unknown campaign {name}')


if __name__ == '__main__':
    main(sys.argv[1:])
