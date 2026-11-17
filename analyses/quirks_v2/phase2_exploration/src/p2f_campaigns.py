"""p2f_campaigns.py -- runner campaign files of the T1-b check (executor Flora, 2026-11-17).

  python3 -I p2f_campaigns.py smoke <N>            every code path on a few toys (seeds 999001...; no result)
  python3 -I p2f_campaigns.py setup                set-up checks (asymptotic 828.67, Viktor's CLs, numpy vs jax)
  python3 -I p2f_campaigns.py prod <mu_a>          the frozen procedure, one job per seed of p2f_t1.SEEDS
  python3 -I p2f_campaigns.py diag <mu_a>          diagnostics without verdict (v1 statistic; exact-q large ensemble)
  python3 -I p2f_campaigns.py sum <mu_a>           verdict assembly from the stored q values
(light: einstein; writes tools/runner/examples/p2f/<campaign>.json).  Campaigns p2-c-t1f-*; outputs
data/p2c/<campaign>/000/, markers ledger/markers/<campaign>/.  Launch (ONE job at a time on schrodinger):
  R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
  ssh -x schrodinger "pgrep -u jdochoa -af '[q]v2run job' | wc -l"        # must be <= 2
  $R/bin/qv2run ssh launch $R/examples/p2f/<campaign>.json --nodes schrodinger --max-per-node 1 --on schrodinger
"""
import json
import logging
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = REPO / 'tools' / 'runner' / 'examples' / 'p2f'
SRC = str(HERE)
DATA = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c'
PYJ = '/home/scratch/jdochoa/envs/pyhf_toys/.pixi/envs/default/bin/python'            # jax env (schrodinger only)
PYN = str(REPO / 'analyses/quirks_v2/phase1_strategy/src/pyhf_bench/.pixi/envs/default/bin/python')   # numpy backend
ENV = ('export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 '
       "XLA_FLAGS='--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1' JAX_PLATFORMS=cpu && ")
T1 = f'{SRC}/p2f_t1.py'
SEEDS = tuple(2026111701 + i for i in range(10))
CONF = 'tol=1e-10'       # SLSQP tolerance selected by p2-c-t1f-setup2 (variant a), log 2026-11-17 08:42
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p2f_campaigns')


def write(name, jobs, hours, description, rss=1500):
    d = dict(campaign=name, tier='regenerable', data_prefix='p2c',
             regenerate=f'python3 -I {SRC}/p2f_campaigns.py (see docstring)', description=description,
             expected_hours=hours, defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / f'.{name}.json.tmp'
    tmp.write_text(json.dumps(d, indent=1) + '\n')
    tmp.replace(OUT / f'{name}.json')
    log.info('%s: %d jobs -> %s', name, len(jobs), OUT / f'{name}.json')


def job(jid, steps, outputs):
    return dict(id=jid, outputs=outputs, command=ENV + ' && '.join(steps))


def main(argv):
    key = argv[0]
    O = '$QV2_OUT_DIR'
    if key == 'smoke':
        c = f'p2-c-t1f-smoke{argv[1]}'
        o = [f'{c}-{x}.json' for x in ('setup', 'ws', 'ptj', 'ptn', 'pair', 'r1', 'r2', 'sum', 'v1stat', 'ref')]
        f = {x: f'{O}/{c}-{x}.json' for x in ('setup', 'ws', 'ptj', 'ptn', 'pair', 'r1', 'r2', 'sum', 'v1stat', 'ref')}
        steps = [f"{PYJ} -I {T1} setup {f['setup']} {f['ws']} quick",
                 f"{PYJ} -I {T1} pt {f['ptj']} jax 621.5 20 999001",
                 f"{PYN} -I {T1} pt {f['ptn']} numpy 621.5 20 999001",
                 f"{PYJ} -I {T1} pair {f['pair']} {f['ptj']} {f['ptn']}",
                 f"{PYJ} -I {T1} t1b {f['r1']} 828.67 999001 30 2",
                 f"{PYJ} -I {T1} t1b {f['r2']} 828.67 999002 30 2",
                 f"{PYJ} -I {T1} summary {f['sum']} 828.67 {f['r1']} {f['r2']}",
                 f"{PYJ} -I {T1} v1stat {f['v1stat']} 300",
                 f"{PYJ} -I {T1} ref {f['ref']} 828.67 3000"]
        write(c, [job(c + '-all', steps, o)], 0.1, 'T1-b: smoke of every code path of p2f_t1.py (no result)')
    elif key == 'setup':
        c = 'p2-c-t1f-setup'
        jobs = [job(f'{c}-asym', [f"{PYJ} -I {T1} setup {O}/{c}-asym.json {O}/{c}-workspace.json"],
                    [f'{c}-asym.json', f'{c}-workspace.json']),
                job(f'{c}-vcheck',
                    [f"{PYJ} -I {SRC}/p2v_toys.py {O}/{c}-viktor-jsmsp-n31-mu5.json 25 5 1000 5 "
                     "'backend=jax,layout=merged,stitch=1,start=prev,record=1'",
                     f"{PYJ} -I {T1} vcheck {O}/{c}-vcheck.json {O}/{c}-viktor-jsmsp-n31-mu5.json"],
                    [f'{c}-viktor-jsmsp-n31-mu5.json', f'{c}-vcheck.json']),
                job(f'{c}-pair',
                    [f"{PYJ} -I {T1} pt {O}/{c}-pt-jax.json jax 621.5 300 2026111700",
                     f"{PYN} -I {T1} pt {O}/{c}-pt-numpy.json numpy 621.5 300 2026111700",
                     f"{PYJ} -I {T1} pair {O}/{c}-pair.json {O}/{c}-pt-jax.json {O}/{c}-pt-numpy.json"],
                    [f'{c}-pt-jax.json', f'{c}-pt-numpy.json', f'{c}-pair.json'])]
        write(c, jobs, 0.2, 'T1-b set-up checks: asymptotic 828.67 and mu_a; Viktor CLs 0.1372; numpy vs jax paired on the v1 workspace')
    elif key == 'setup2':          # check 2b failed with the default SLSQP tolerance: fit-accuracy variants, same toys
        c = 'p2-c-t1f-setup2'
        jobs = []
        for tag, conf in (('a', 'tol=1e-10'), ('b', 'tol=1e-10,newton_t=1'), ('c', 'tol=1e-12,newton_t=1')):
            st = []; o = []
            for mu, mt in (('621.5', 'm0621'), ('828.7069', 'm0828'), ('1118.754', 'm1118')):
                st.append(f"{PYJ} -I {T1} pt {O}/{c}-{tag}-jax-{mt}.json jax {mu} 300 2026111700 {conf}")
                o.append(f'{c}-{tag}-jax-{mt}.json')
            st.append(f"{PYN} -I {T1} pt {O}/{c}-{tag}-numpy-m0621.json numpy 621.5 300 2026111700 {conf}")
            st.append(f"{PYJ} -I {T1} pair {O}/{c}-{tag}-pair.json {O}/{c}-{tag}-jax-m0621.json {O}/{c}-{tag}-numpy-m0621.json")
            o += [f'{c}-{tag}-numpy-m0621.json', f'{c}-{tag}-pair.json']
            jobs.append(job(f'{c}-{tag}', st, o))
        write(c, jobs, 0.1, 'T1-b set-up check 2b repeated with tighter SLSQP tolerance (fit accuracy), same pseudo-data')
    elif key == 'prod':
        mu_a = argv[1]
        c = 'p2-c-t1f-prod'
        jobs = [job(f'{c}-s{sd}', [f"{PYJ} -I {T1} t1b {O}/{c}-s{sd}.json {mu_a} {sd} 1000 6 {CONF}"], [f'{c}-s{sd}.json'])
                for sd in SEEDS]
        write(c, jobs, 2.0, f'T1-b: the frozen toy procedure (STR 4.11 pt 2) in v1 mode, 10 replicas, mu_a = {mu_a}')
    elif key == 'diag':
        mu_a = argv[1]
        c = 'p2-c-t1f-diag'
        jobs = [job(f'{c}-v1stat', [f"{PYJ} -I {T1} v1stat {O}/{c}-v1stat.json 5000"], [f'{c}-v1stat.json']),
                job(f'{c}-ref', [f"{PYJ} -I {T1} ref {O}/{c}-ref.json {mu_a} 200000"], [f'{c}-ref.json'])]
        write(c, jobs, 0.3, 'T1-b diagnostics (no verdict): v1 number-count statistic over 12 seeds; exact-q large ensemble')
    elif key == 'sum':
        mu_a = argv[1]
        c = 'p2-c-t1f-sum' + (argv[2] if len(argv) > 2 else '')
        files = ' '.join(f'{DATA}/p2-c-t1f-prod/000/p2-c-t1f-prod-s{sd}.json' for sd in SEEDS)
        write(c, [job(f'{c}-verdict', [f"{PYJ} -I {T1} summary {O}/{c}-verdict.json {mu_a} {files}"],
                      [f'{c}-verdict.json'])], 0.05, 'T1-b verdict assembly from the stored q values (rules of the plan)')
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
