"""p3a_campaigns.py -- writes the runner campaign files of work package p3-a.  Aurora, 2026-11-24.

  python3 -I p3a_campaigns.py <kind> <files-per-Z-job> [<files-per-B1-job-scale>]
  kind: m (merged, PV draw, all streams, Z events with w_v1 > 0) | m0 (the same, Z events with w_v1 = 0 only) | u (not merged, all streams) | pv0 (true PV, Z only)
        | pv2 (other PV seed, every 4th Z file) | ind (Nils's search, N parts = second argument)
        [these six one-read-per-variant campaigns were NOT run: NFS-bound; superseded by]
        xz (all Z variants + ind from one read per file, N files per job) | xb (B1 / hs / lowpt: m and u)

Pilot file lists: tools/runner/examples/p2w/p2-c-r1v-sub_files.json (the 139 Phase-2 groups, 1,083 files), regrouped.
Per-job NUMBA_CACHE_DIR in the job's scratch (EXP section 10 item 13), seeded by a copy of a warmed cache on the node.
"""
import json
import sys
from pathlib import Path

REPO = Path('/home/users/jdochoa/hllhc-quirks-search')
EX = REPO / 'tools/runner/examples/p3a'
SRC = '$QV2/phase3_selection/src/p3a'
ENV = ('. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh && export NUMBA_CACHE_DIR=$PWD/numba '
       'PYTHONPYCACHEPREFIX=$PWD/pyc PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 && '
       '(cp -r $QV2_SCRATCH/p3a_cache_seed/numba $PWD/numba 2>/dev/null || mkdir -p $PWD/numba) && '
       'PY=$QV2/envs/tt/.pixi/envs/default/bin/python && ')
OPT = dict(m='', m0='--w-select zero', u='--no-merge', pv0='--pv true', pv2='--pv draw2')
DESC = dict(
    m0='FINAL pilot classification, base pass continued: the Z(nunu) events with w_v1 = 0 (in no term under v1 weights; '
       'needed if the v2 MET model gives them a weight, ADD l.607), merged pool, PV draw, 460 files.',
    m='FINAL pilot classification, base pass: merged pool, PV draw of p2t_classify, all 1083 pilot files, Z(nunu) '
      'events with w_v1 > 0. p3a_subset.py (BASE = p2w_subset.py unchanged + categories c0-c4, widths none/75/37.5/'
      '18.75/9.4/4.7 mm, s = 0/3, S/F). Read-only on pilot files; no signal file.',
    u='FINAL pilot classification, variant: pool NOT merged (no chain_inputs.merge_pool), PV draw, all 1083 files, Z '
      'events with w_v1 > 0. Open choice "hit merging before the finder" (EXP section 10 item 10).',
    pv0='FINAL pilot classification, variant: PV = true vertex (no 10/10/15 um draw), merged pool, 460 Z(nunu) files, '
        'w_v1 > 0. Open choice "PV for Z(nunu)" (EXP section 10 item 10).',
    pv2='FINAL pilot classification, variant: PV draw with another seed string, merged pool, every 4th Z(nunu) file '
        '(115), w_v1 > 0: size of the PV-seed effect.',
    ind="Independent re-derivation at R04(75 mm), R05, R06, R07, s = 0 and 3, with Nils's search and verifier "
        '(review_nils_subset.py imported unchanged) on the counted Z(nunu) events of every 2nd pilot file (230 files). p3a_indep.py.')


def multi(kind, n):
    """xz: all variants + independent search from one read of each Z(nunu) file; xb: m and u for the B1 / hs / lowpt files."""
    EX.mkdir(parents=True, exist_ok=True)
    G = json.loads((REPO / 'tools/runner/examples/p2w/p2-c-r1v-sub_files.json').read_text())
    z = sorted(p for k, v in G.items() if '-znn-' in k for p in v)
    assert len(z) == 460
    (EX / 'p3-a-z_all.json').write_text(json.dumps(z))
    camp = f'p3-a-cls{kind}'
    man = {}
    if kind == 'xz':
        for i in range(0, 460, n):
            man[f'p3a-xz-{i // n:03d}'] = z[i:i + n]
        var = 'm,u,pv0,pv2,ind'; outs = ['m.npz', 'u.npz', 'pv0.npz', 'pv2.npz', 'ind.json']
        assert n % 4 == 0
        desc = ('FINAL pilot classification of the 460 Z(nunu) files, ONE read per file (p3a_multi.py): m (merged pool, PV '
                'draw, w_v1 > 0 = Phase-2 configuration), u (pool not merged), pv0 (PV = true vertex), '
                "pv2 (other PV seed, every 4th file), ind (Nils's search on the counted events, every 2nd file). "
                'Read-only on pilot files; no signal file.')
    else:
        for k, v in sorted(G.items()):
            if '-znn-' not in k:
                man[f"p3a-xb-{k.split('-')[2]}-{k.split('-')[3]}"] = v
        var = 'm,u'; outs = ['m.npz', 'u.npz']
        desc = ('FINAL pilot classification of the 623 B1 / hs / lowpt files, ONE read per file (p3a_multi.py): m (merged '
                'pool) and u (pool not merged); stored PV; 21 orientations (hs: 1). Witness hit tables for every row.')
    nfiles = sum(len(v) for v in man.values())
    assert len({p for v in man.values() for p in v}) == nfiles
    mp = EX / f'{camp}_files.json'
    mp.write_text(json.dumps(man, indent=0))
    jobs = [dict(id=jid, outputs=[f'{jid}.{o}' for o in outs],
                 command=ENV + f'nice -n 10 $PY {SRC}/p3a_multi.py --id {jid} --outdir $QV2_OUT_DIR --manifest {mp} '
                 f"--all-z {EX / 'p3-a-z_all.json'} --variants {var}") for jid in man]
    sys.stderr.write(f'{camp}: {len(jobs)} jobs, {nfiles} pilot files\n')
    c = dict(campaign=camp, tier='regenerable', data_prefix='p3a', regenerate=f'phase3_selection/src/p3a/p3a_campaigns.py {kind} {n}',
             description=desc, expected_hours=4.0, defaults=dict(max_rss_mb=3000, timeout_s=1800), after=[], jobs=jobs)
    (EX / f'{camp}.json').write_text(json.dumps(c, indent=1))


def main(kind, n, scale=1.0):
    if kind in ('xz', 'xb'):
        return multi(kind, n)
    EX.mkdir(parents=True, exist_ok=True)
    camp = f'p3-a-cls-{kind}' if kind != 'ind' else 'p3-a-ind'
    jobs = []
    if kind == 'ind':
        for i in range(n):
            jid = f'p3a-ind-{i:02d}'
            jobs.append(dict(id=jid, outputs=[f'{jid}.json'], command=ENV + f'nice -n 10 $PY -B {SRC}/p3a_indep.py '
                             f'--part {i} --nparts {n} --stride 2 --offset 0 --out $QV2_OUT_DIR/{jid}.json'))
    else:
        G = json.loads((REPO / 'tools/runner/examples/p2w/p2-c-r1v-sub_files.json').read_text())
        z = sorted(p for k, v in G.items() if '-znn-' in k for p in v)
        assert len(z) == 460
        if kind == 'pv2':
            z = z[::4]
        man = {}
        for i in range(0, len(z), n):
            man[f'p3a-{kind}-znn-{i // n:03d}'] = z[i:i + n]
        if kind in ('m', 'u'):
            for k, v in sorted(G.items()):
                if '-znn-' in k:
                    continue
                st = k.split('-')[2]
                step = max(1, int(round(len(v) * scale)))
                for j in range(0, len(v), step):
                    man[f"p3a-{kind}-{st}-{k.split('-')[3]}{chr(97 + j // step)}"] = v[j:j + step]
        nfiles = sum(len(v) for v in man.values())
        assert len({p for v in man.values() for p in v}) == nfiles
        mp = EX / f'{camp}_files.json'
        mp.write_text(json.dumps(man, indent=0))
        for jid in man:
            jobs.append(dict(id=jid, outputs=[f'{jid}.npz'], command=ENV + f'nice -n 10 $PY {SRC}/p3a_subset.py --id {jid} '
                             f'--out $QV2_OUT_DIR/{jid}.npz --manifest {mp} {OPT[kind]}'))
        sys.stderr.write(f'{camp}: {len(jobs)} jobs, {nfiles} pilot files\n')
    c = dict(campaign=camp, tier='regenerable', data_prefix='p3a', regenerate=f'phase3_selection/src/p3a/p3a_campaigns.py {kind} {n}',
             description=DESC[kind], expected_hours=3.0, defaults=dict(max_rss_mb=2500, timeout_s=1800), after=[], jobs=jobs)
    (EX / f'{camp}.json').write_text(json.dumps(c, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
