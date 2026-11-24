"""p3c_campaigns.py -- writes the runner campaign files of work package p3-c to tools/runner/campaigns/.

  python3 -I p3c_campaigns.py <val|zx|mjw|mjs|pw|step4bg> [n_jobs]      (light; run on einstein)

Campaign names start with p3-c-; outputs go to data/p3c/<campaign>/<shard>/, markers to ledger/markers/<campaign>/.
"""
import json
import logging
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = REPO / 'tools' / 'runner' / 'campaigns'
SRC = str(HERE)
ACTSENV = str(REPO / 'analyses/quirks_v2/acts/.pixi/envs/default')
PY = f'{ACTSENV}/bin/python'
ENV = (f'export PYTHIA8DATA={ACTSENV}/share/Pythia8/xmldoc PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 '
       'OPENBLAS_NUM_THREADS=1 && ')
PILOT = '/nfs/cajuela/jdochoa/quirks_v2/data/pilot'
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p3c_campaigns')


def write(name, jobs, hours, rss, me, description):
    d = dict(campaign=name, tier='regenerable', data_prefix='p3c', regenerate=me, description=description,
             expected_hours=hours, defaults=dict(max_rss_mb=rss, timeout_s=1800), jobs=jobs)
    tmp = OUT / f'.{name}.json.tmp'
    tmp.write_text(json.dumps(d, indent=1) + '\n')
    tmp.replace(OUT / f'{name}.json')
    log.info('%s: %d jobs -> %s', name, len(jobs), OUT / f'{name}.json')


def gen_jobs(camp, proc, n_jobs, n_ev, chunk0=0):
    return [dict(id=f'{camp}-{proc}-{k:03d}', shard=0, outputs=[f'{camp}-{proc}-{k:03d}.npz'],
                 command=ENV + f'{PY} {SRC}/p3c_gen.py {proc} $QV2_OUT_DIR/{camp}-{proc}-{k:03d}.npz {n_ev} p3c.gen.{proc} {k}')
            for k in range(chunk0, chunk0 + n_jobs)]


def main(argv):
    what = argv[0]
    me = f'python3 -I {SRC}/p3c_campaigns.py ' + ' '.join(argv)
    if what == 'val':
        jobs = gen_jobs('p3-c-val', 'zmm', 8, 80000) + gen_jobs('p3-c-val', 'tt', 4, 80000)
        write('p3-c-val', jobs, 3.5, 1200, me, 'MET-model validation samples: inclusive Z->mumu 6.4e5, tt-bar 3.2e5 '
              '(generator level)')
    elif what == 'zx':
        jobs = []
        for p in ('znn', 'ztt', 'zll'):
            jobs += gen_jobs('p3-c-zx', p, 5, 80000)
        write('p3-c-zx', jobs, 4.5, 1200, me, 'Z(nunu), Z(tautau), Z(ll) + parton, pT-hat > 80 GeV, biased pT-hat^4, '
              'no MET filter: 4e5 each (generator level)')
    elif what in ('mjw', 'mjw2'):
        n = int(argv[1]) if len(argv) > 1 else 20
        c0 = 0 if what == 'mjw' else int(argv[2])
        write(f'p3-c-{what}', gen_jobs(f'p3-c-{what}', 'mjw', n, 60000, c0), 0.33 * n, 1500, me,
              'multijets, pT-hat > 100 GeV, biased pT-hat^5 (weighted), generator level')
    elif what in ('mjs', 'mjs2'):
        n = int(argv[1]) if len(argv) > 1 else 4
        c0 = 0 if what == 'mjs' else int(argv[2])
        jobs = []
        for s in range(5):
            jobs += gen_jobs(f'p3-c-{what}', f'mjs{s}', n, 60000, c0)
        write(f'p3-c-{what}', jobs, 0.33 * 5 * n, 1500, me, 'multijets, unweighted pT-hat slices 100-200-400-800-1600-inf')
    elif what in ('pw', 'pw2'):
        files = sorted(str(p) for p in Path(PILOT).glob('p2-c-pilot-znn-*/000/*.npz'))
        assert len(files) == 460, len(files)
        per = 20
        lists = REPO / 'tools/runner/examples/p3c'; lists.mkdir(parents=True, exist_ok=True)
        jobs = []
        for k in range(0, len(files), per):
            lf = lists / f'p3-c-pw-{k // per:02d}.txt'
            lf.write_text('\n'.join(files[k:k + per]) + '\n')
            jid = f'p3-c-{what}-{k // per:02d}'
            jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.npz'],
                             command=ENV + f'{PY} {SRC}/p3c_pilot_weights.py $QV2_OUT_DIR/{jid}.npz {lf}'))
        write(f'p3-c-{what}', jobs, 2.0, 1500, me, 'v2 MET-model preselection weights of the 2.3e6 Z(nunu) pilot events '
              '(reads evt, jets, lep, gsum; one output row per pilot event)')
    elif what == 'ap':            # ap <campaign name> <K> <f_tail_prop> <input campaign> <files per job> <proc:n_files> ...
        name, K, fprop, src, per = argv[1], int(argv[2]), argv[3], argv[4], int(argv[5])
        ddir = f'/nfs/cajuela/jdochoa/quirks_v2/data/p3c/{src}/000'
        model = REPO / 'analyses/quirks_v2/phase3_selection/outputs/p3c/model.json'
        jobs = []
        for spec in argv[6:]:
            proc, nf = spec.split(':'); c0 = 0
            if '@' in nf:
                nf, c0 = nf.split('@')
            fl = [f'{ddir}/{src}-{proc}-{k:03d}.npz' for k in range(int(c0), int(c0) + int(nf))]
            for j in range(0, len(fl), per):
                jid = f'{name}-{proc}-{(int(c0) + j) // per:02d}'
                jobs.append(dict(id=jid, shard=0, outputs=[f'{jid}.json'],
                                 command=ENV + f'{PY} {SRC}/p3c_apply.py $QV2_OUT_DIR/{jid}.json {model} {K} {fprop} '
                                 + ' '.join(fl[j:j + per])))
        write(name, jobs, 0.15 * len(jobs), 2500, me, f'MET model applied to {src} (K = {K} throws, tail proposal {fprop})')
    else:
        raise SystemExit(f'unknown campaign {what}')


if __name__ == '__main__':
    main(sys.argv[1:])
