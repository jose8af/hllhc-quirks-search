"""p2c_campaigns.py -- writes the runner campaign files of Phase-2 channel (iii) to tools/runner/examples/p2c/.

  python3 -I p2c_campaigns.py <name> [args]      (light: run on einstein; prints the file written)

Campaign names start with p2-c-; outputs go to data/p2c/<campaign>/<shard>/, markers to ledger/markers/<campaign>/.
"""
import json
import logging
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = REPO / 'tools' / 'runner' / 'examples' / 'p2c'
SRC = str(HERE)
ACTSPY = str(REPO / 'analyses/quirks_v2/acts/.pixi/envs/default/bin/python')
PYHFPY = str(REPO / 'analyses/quirks_v2/phase1_strategy/src/pyhf_bench/.pixi/envs/default/bin/python')
G4ENV = '/home/scratch/jdochoa/envs/g4/.pixi/envs/default'
ACTSENV = str(REPO / 'analyses/quirks_v2/acts/.pixi/envs/default')
ENV = (f'export CONDA_PREFIX={ACTSENV} PYTHIA8={ACTSENV} PYTHIA8_DIR={ACTSENV} PYTHIA8DATA={ACTSENV}/share/Pythia8/xmldoc '
       'PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/home/scratch/jdochoa/cache/pyc '
       'QV2_PYTHIA_INIT_DIR=/home/scratch/jdochoa/cache/pythia_init OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 && ')
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p2c_campaigns')


def write(name, jobs, hours, rss, regenerate, description, tier='regenerable'):
    d = dict(campaign=name, tier=tier, data_prefix='p2c', regenerate=regenerate, description=description,
             expected_hours=hours, defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / f'.{name}.json.tmp'
    tmp.write_text(json.dumps(d, indent=1) + '\n')
    tmp.replace(OUT / f'{name}.json')
    log.info('%s: %d jobs -> %s', name, len(jobs), OUT / f'{name}.json')


def hs0_jobs(camp, sample, tag, stream, n_jobs, n_ev, chunk0=0, per_shard=500):
    return [dict(id=f'{camp}-{tag}-{k:04d}', shard=(k - chunk0) // per_shard, outputs=[f'{camp}-{tag}-{k:04d}.npz'],
                 command=ENV + f'{ACTSPY} {SRC}/p2c_hs0.py {sample} $QV2_OUT_DIR/{camp}-{tag}-{k:04d}.npz {n_ev} {stream} {k}')
            for k in range(chunk0, chunk0 + n_jobs)]


def main(argv):
    what = argv[0]
    me = f'python3 -I {SRC}/p2c_campaigns.py ' + ' '.join(argv)
    if what == 't-hs0s':          # smoke: 200 events per process
        jobs = []
        for s, t in (('Znunu_j', 'znn'), ('Wtaunu_j', 'wtn'), ('ttbar_1l', 'tt1')):
            jobs += hs0_jobs('p2-c-t-hs0s2', s, t, f'time.hs0s2.{t}', 1, 200)
        write('p2-c-t-hs0s2', jobs, 0.2, 1500, me, 'timing smoke: no-PU hard-scatter events, 200 per process')
    elif what == 't-hs0':         # STR Table 4.0: 10^4 events each of Z(nunu), W, ttbar with the filter
        jobs = []          # tt-bar: 0.54 s per event in the smoke job (filter), so smaller jobs
        for s, t, n_ev in (('Znunu_j', 'znn', 2500), ('Wtaunu_j', 'wtn', 2500), ('ttbar_1l', 'tt1', 1250)):
            jobs += hs0_jobs('p2-c-t-hs0', s, t, f'time.hs0.{t}', 10000 // n_ev, n_ev)
        write('p2-c-t-hs0', jobs, 1.0, 1500, me, 'day-0 timing of the no-PU hard-scatter event (the guessed 45 ms)')
    elif what == 't-g4':          # Geant4 vertex yield and cost per firing on the natural spectrum; material scan
        name = argv[1] if len(argv) > 1 else 'p2-c-t-g4'
        ho = argv[2] if len(argv) > 2 else 'vertex'
        nj, sizes = (3, '40000 500000 3000000') if ho == 'vertex' else (2, '20000 200000 1500000')
        jobs = [dict(id=f'{name}-y{k}', outputs=[f'{name}-y{k}.npz'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_g4vtx.py time $QV2_OUT_DIR/{name}-y{k}.npz {sizes} '
                                   f'time.g4 {k} FTFP_BERT {ho}') for k in range(nj)]
        jobs.append(dict(id=f'{name}-scan', outputs=[f'{name}-scan.npz'],
                         command=ENV + f'{ACTSPY} {SRC}/p2c_g4vtx.py scan $QV2_OUT_DIR/{name}-scan.npz 20'))
        write(name, jobs, 0.5, 1500, me, 'timing: Geant4 vertex yield per firing, cost per firing, geantino scan')
    elif what == 't-pyhf':        # toy cost against the number of parameters (STR §4.11 pt 5, [L4])
        name = 'p2-c-t-pyhf'
        jobs = [dict(id=f'{name}-n{1 + nt + nn}', outputs=[f'{name}-n{1 + nt + nn}.json'],
                     command=f'export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 && {PYHFPY} '
                             f'{SRC}/p2c_t1.py time $QV2_OUT_DIR/{name}-n{1 + nt + nn}.json {nt} {nn} {ntoy}')
                for nt, nn, ntoy in ((25, 5, 100), (45, 14, 100), (60, 19, 20), (75, 24, 20))]   # 20: 30-min limit
        write(name, jobs, 0.5, 600, me, 'timing: hybrid toys (two fits each) at 31, 60, 80, 100 parameters')
    elif what == 't-b1':          # hand-over slice: 2,000 events per term from the vertices of p2-c-t-g4
        name = argv[1] if len(argv) > 1 else 'p2-c-t-b1'
        g4c = argv[3] if len(argv) > 3 else 'p2-c-t-g4'
        vdir = f'/nfs/cajuela/jdochoa/quirks_v2/data/p2c/{g4c}/000'
        files = ' '.join(f'{vdir}/{g4c}-y{k}.npz' for k in range(2))
        n_ev = int(argv[2]) if len(argv) > 2 else 2000
        jobs = [dict(id=f'{name}-{t}', outputs=[f'{name}-{t}.npz'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_b1.py {t} $QV2_OUT_DIR/{name}-{t}.npz {n_ev} time.c0.{t} 0 0 {files}')
                for t in ('dif', 'ni22', 'ni30', 'ni61')]
        write(name, jobs, 0.3, 1500, me, 'timing and hand-over slice: no-PU B1 events from Geant4 vertices')
    elif what == 'matscan':       # B1-d: ACTS geometry and material against the Geant4 scan of p2-c-t-g4
        name = 'p2-c-matscan'
        scan = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c/p2-c-t-g4/000/p2-c-t-g4-scan.npz'
        jobs = [dict(id=f'{name}-0', outputs=[f'{name}-0.json'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_matscan.py $QV2_OUT_DIR/{name}-0.json {scan}')]
        write(name, jobs, 0.1, 1000, me, 'B1-d: positions, x/X0 per layer, Fatras physics record')
    elif what == 'val-b1':        # hand-over validation on the slice of p2-c-t-b1
        name = argv[1] if len(argv) > 1 else 'p2-c-val-b1'
        b1c = argv[2] if len(argv) > 2 else 'p2-c-t-b1'
        d = f'/nfs/cajuela/jdochoa/quirks_v2/data/p2c/{b1c}/000'
        files = ' '.join(f'{d}/{b1c}-{t}.npz' for t in ('dif', 'ni22', 'ni30', 'ni61'))
        jobs = [dict(id=f'{name}-0', outputs=[f'{name}-0.json'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_validate.py $QV2_OUT_DIR/{name}-0.json {files}')]
        write(name, jobs, 0.1, 1000, me, 'hand-over validation: truncation, product times, variant A against B')
    elif what == 'prof':          # cost-reduction study (orchestrator order 2026-11-16)
        name = argv[1] if len(argv) > 1 else 'p2-c-prof'
        spec = [('gen-znn', 'gen', 'Znunu_j 1500'), ('gen-wtn', 'gen', 'Wtaunu_j 1000'), ('gen-tt1', 'gen', 'ttbar_1l 300'),
                ('gen-tt1f', 'gen', 'ttbar_1l 300 tt_forced'), ('chain-znn', 'chain', 'Znunu_j 400'), ('g4', 'g4', '')]
        if len(argv) > 2:
            spec = [x for x in spec if x[0] in argv[2:]]
        jobs = [dict(id=f'{name}-{t}', outputs=[f'{name}-{t}.json'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_prof.py {m} $QV2_OUT_DIR/{name}-{t}.json {args}') for t, m, args in spec]
        write(name, jobs, 0.5, 1500, me, 'profile of the no-PU hard-scatter event and of the Geant4 firing')
    elif what == 'rule1':         # rule-1 readings, pool and toy projections (ESTIMATE; copy of the Phase-1 script)
        name = argv[1] if len(argv) > 1 else 'p2-c-rule1'
        costs = str(HERE.parent / 'outputs' / 'costs_after_step1.json')
        jobs = [dict(id=f'{name}-0', outputs=[f'{name}-0.json'],
                     command=f'PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I {SRC}/p2c_rule1.py $QV2_OUT_DIR/{name}-0.json {costs}')]
        write(name, jobs, 0.2, 300, me, 'rule-1 readings and projections with measured costs')
    elif what == 'addendum1':     # tables of strategy addendum 1 (ESTIMATE)
        name = argv[1] if len(argv) > 1 else 'p2-c-addendum1'
        jobs = [dict(id=f'{name}-0', outputs=[f'{name}-0.json'],
                     command=f'PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I {SRC}/p2c_addendum1.py $QV2_OUT_DIR/{name}-0.json')]
        write(name, jobs, 0.2, 300, me, 'rule-1 basis, day-15 table and Table 4.4a rows for strategy addendum 1')
    elif what == 't-ttf':         # forced tt-bar decays through the chain (addendum 1 §3.3)
        jobs = []
        for smp, t in (('ttbar_1l_pos', 'ttp'), ('ttbar_1l_neg', 'ttn')):
            jobs += hs0_jobs('p2-c-t-ttf', smp, t, f'time.hs0.{t}', 1, 1250)
        write('p2-c-t-ttf', jobs, 0.3, 1500, me, 'timing: tt-bar 1-lepton with forced W decays, no pile-up, through the chain')
    elif what == 't1-v1':         # COM T1-b: v1 best point in v1 mode
        name = argv[1] if len(argv) > 1 else 'p2-c-t1-v1'
        nt = argv[2] if len(argv) > 2 else '500'
        jobs = [dict(id=f'{name}-0', outputs=[f'{name}-0.json'],
                     command=f'export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 && {PYHFPY} '
                             f'{SRC}/p2c_t1.py v1 $QV2_OUT_DIR/{name}-0.json {nt}')]
        write(name, jobs, 0.4, 600, me, 'T1-b: v1 best-point limit with the T1 builder in v1 mode')
    elif what == 't1b':           # refined T1-b: one job per mu (1000 + 1000 toys), plus the diagnostics job
        name = 'p2-c-t1b'
        pre = f'export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 && {PYHFPY} {SRC}/p2c_t1.py '
        mus = [760, 790, 810, 825, 835, 845, 855, 870, 890, 915]
        jobs = [dict(id=f'{name}-mu{m}', outputs=[f'{name}-mu{m}.json'],
                     command=pre + f'v1pt $QV2_OUT_DIR/{name}-mu{m}.json {m} 1000 {20261200 + m}') for m in mus]
        jobs.insert(0, dict(id=f'{name}-diag', outputs=[f'{name}-diag.json'], command=pre + f'v1diag $QV2_OUT_DIR/{name}-diag.json'))
        write(name, jobs, 1.0, 600, me, 'T1-b refined: hybrid toys with q-tilde per mu; fine asymptotic scan; v1-statistic diagnostic')
    elif what == 'fix1':          # addendum-1 fix measurements: partition, Fatras no-decay check
        jobs = [dict(id='p2-c-part-0', outputs=['p2-c-part-0.npz'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_g4vtx.py part $QV2_OUT_DIR/p2-c-part-0.npz 25000 1500000 fix.part 0'),
                dict(id='p2-c-part-fatras', outputs=['p2-c-part-fatras.json'],
                     command=ENV + f'{ACTSPY} {SRC}/p2c_fatras_check.py $QV2_OUT_DIR/p2-c-part-fatras.json 4000')]
        write('p2-c-part', jobs, 0.5, 2500, me, 'addendum 1 fix: complete Geant4 vertex partition; Fatras no-decay check')
    elif what == 'fix2':          # O13 (b) slices on every proposed pilot stream, from the partition vertices
        vf = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c/p2-c-part/000/p2-c-part-0.npz'
        terms = ('dif', 'difc', 'k0l', 'ni22', 'ni30', 'ni61', 'nix', 'nic')
        jobs = [dict(id=f'p2-c-b1y-{t}', outputs=[f'p2-c-b1y-{t}.npz'],
                     command='export P2C_BETA_MIN=0.1 && ' + ENV + f'{ACTSPY} {SRC}/p2c_b1.py {t} $QV2_OUT_DIR/p2-c-b1y-{t}.npz '
                             f'{int(argv[1]) if len(argv) > 1 else 1000} fix.c0.{t} 0 0 {vf}') for t in terms]
        d = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c/p2-c-b1y/000'
        files = ' '.join(f'{d}/p2-c-b1y-{t}.npz' for t in terms)
        jobs.append(dict(id='p2-c-b1y-val', outputs=['p2-c-b1y-val.json'],
                         command=ENV + f'{ACTSPY} {SRC}/p2c_validate.py $QV2_OUT_DIR/p2-c-b1y-val.json {files}'))
        write('p2-c-b1y', jobs, 0.3, 1500, me, 'addendum 1 fix: hand-over O13 (b) validated on every proposed pilot stream')
    else:
        raise SystemExit(f'unknown campaign {what}')


if __name__ == '__main__':
    main(sys.argv[1:])
