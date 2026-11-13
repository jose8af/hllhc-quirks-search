"""merge_index.py -- Stage-3 merge (E8, 2026-10-13): build data/sim_stage3/STAGE3_INDEX.json and the canonical symlink
tree data/sim_stage3/canon/ WITHOUT copying the bulky outputs.

Inputs : jobs/{all,mac,pc,overlap}.json; outputs data/sim_stage3/out (Mac) and data/sim_stage3/out_pc (PC).
Checks :
  * every job of all.json (= mac + pc) is present exactly once, in the tree of the machine it was assigned to, and is
    valid (job id, complete flag, n_events, CSR offsets); the 3 overlap clones are present on BOTH machines;
  * the job definition stored in each file (job_json) equals the job list entry (events, cfg, Lambda, m, max_boost,
    vertex, input) -- i.e. the PC ran the same job list;
  * no (campaign, spin, m, Lambda, cfg, event) appears twice in the canonical set;
  * per file: kernel/runner version, code md5s, original-code md5s, input md5 (vs data/sim_stage3/inputs), platform,
    numpy/numba/python versions; flags every file whose code md5 differs from the current sim/stage3/code md5s;
  * extra files in either tree (not in any job list) are listed.
Totals : events, hits, CPU-s (per-event process time summed, and the job-level process time) and wall per machine.
Output : data/sim_stage3/STAGE3_INDEX.json, data/sim_stage3/canon/<campaign>/<spin>_m<m>/L<lam>_<cfg>_cNN.npz (relative
         symlinks; xover clones under canon/xover/<machine>/), sim/stage3/results/merge.json.
Run (theory_track/): pixi run python sim/stage3/scripts/merge_index.py
"""
import hashlib
import json
import os
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import s3common as C

CODE_FILES = ('T3_causal_s3.py', 's3_physics.py', 'run_stage3.py', 'surfaces_s3.json')
JOB_KEYS = ('id', 'campaign', 'spin', 'm', 'lam', 'cfg', 'chunk', 'input', 'ev', 'max_boost', 'hmax', 'vertex')


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def inspect(args):
    machine, job = args
    p = C.OUT[machine].joinpath(*job['out'].split('/'))
    r = dict(id=job['id'], machine=machine, path=str(p.relative_to(C.DATA)), exists=p.is_file())
    if not r['exists']:
        return r
    try:
        with np.load(p, allow_pickle=False) as z:
            meta = json.loads(str(z['meta_json']))
            jj = json.loads(str(z['job_json']))
            n = int(z['n_events'])
            offs = z['hit_offsets']
            nh = len(z['h_x'])
            valid = (str(z['job_id']) == job['id'] and int(z['complete']) == 1 and n == len(job['ev'])
                     and len(offs) == n + 1 and int(offs[-1]) == nh)
            same_job = all(jj.get(k) == job.get(k) for k in JOB_KEYS if k != 'id' or job['campaign'] != 'xover')
            st = np.bincount(z['status'].astype(int), minlength=6).tolist()
            r.update(valid=bool(valid), same_job=bool(same_job), n_events=n, n_hits=nh, status=st,
                     n_rerun=int(np.sum(z['rerun'])), n_swapped=int(np.sum(z['swapped'])),
                     n_floor=int(np.sum(z['floor_flag'])), cpu_ev_s=float(np.sum(z['cpu_s'])),
                     wall_ev_s=float(np.sum(z['wall_s'])), cpu_job_s=float(meta['cpu_s']), wall_job_s=float(meta['wall_s']),
                     nsteps=int(np.sum(z['nsteps'])), maxq=int(np.max(z['maxq'])) if n else 0,
                     kernel_version=meta['kernel_version'], runner_version=meta['runner_version'],
                     code_md5=meta['code_md5'], orig_md5=meta['orig_md5'], input=meta['input'], input_md5=meta['input_md5'],
                     stage2_source_md5=meta['stage2_source_md5'], env=meta['env'], created_utc=meta['created_utc'],
                     est_s=float(job.get('est_s', 0.0)), max_boost=float(z['max_boost']),
                     rows=z['row'].tolist())
    except Exception as e:  # noqa: BLE001
        r.update(valid=False, error=repr(e))
        return r
    r['file_md5'] = md5_file(p)
    r['bytes'] = p.stat().st_size
    return r


def main():
    alljobs = C.load_joblist('all'); mac = C.load_joblist('mac'); pc = C.load_joblist('pc'); ov = C.load_joblist('overlap')
    ids_all = [j['id'] for j in alljobs]
    assert len(set(ids_all)) == len(ids_all)
    ids_mac = {j['id'] for j in mac}; ids_pc = {j['id'] for j in pc}
    part = dict(n_all=len(alljobs), n_mac=len(mac), n_pc=len(pc), n_overlap=len(ov),
                mac_pc_disjoint=not (ids_mac & ids_pc), mac_pc_cover_all=(ids_mac | ids_pc) == set(ids_all))
    tasks = [('mac', j) for j in mac] + [('pc', j) for j in pc] + [('mac', j) for j in ov] + [('pc', j) for j in ov]
    with Pool(7) as pool:
        recs = pool.map(inspect, tasks, chunksize=20)
    # inputs md5
    inp_md5 = {p.name: md5_file(p) for p in (C.DATA / 'inputs').glob('*.npz')}
    cur_md5 = {n: md5_file(C.S3 / 'code' / n) for n in CODE_FILES}
    # extra files
    listed = {(t[0], str(C.OUT[t[0]].joinpath(*t[1]['out'].split('/')))) for t in tasks}
    extra = {}
    for mach, root in C.OUT.items():
        ex = [str(p.relative_to(root)) for p in root.rglob('*.npz')
              if (mach, str(p)) not in listed]
        extra[mach] = sorted(ex)
    # checks
    missing = [r['id'] + '@' + r['machine'] for r in recs if not r['exists']]
    invalid = [r['id'] + '@' + r['machine'] for r in recs if r['exists'] and not r.get('valid')]
    diffjob = [r['id'] + '@' + r['machine'] for r in recs if r.get('valid') and not r['same_job']]
    md5_bad = [r['id'] + '@' + r['machine'] for r in recs if r.get('valid') and r['code_md5'] != cur_md5]
    inp_bad = [r['id'] + '@' + r['machine'] for r in recs if r.get('valid') and inp_md5.get(r['input']) != r['input_md5']]
    canon = [r for r in recs if not r['id'].startswith('xover/')]
    cnt = Counter(r['id'] for r in canon)
    dup_jobs = [k for k, v in cnt.items() if v != 1]
    evkeys = Counter()
    for r in canon:
        j = r['id'].rsplit('_c', 1)[0]
        for row in r.get('rows', []):
            evkeys[(j, row)] += 1
    dup_events = sum(1 for v in evkeys.values() if v > 1)
    # consistency tables
    combos = Counter()
    for r in recs:
        if r.get('valid'):
            e = r['env']
            combos[(r['machine'], r['kernel_version'], r['runner_version'], json.dumps(r['code_md5'], sort_keys=True),
                    json.dumps(r['orig_md5'], sort_keys=True), e['platform'], e['machine'], e['hostname'], e['python'],
                    e['numpy'], e['numba'])] += 1
    combo_list = [dict(machine=k[0], kernel_version=k[1], runner_version=k[2], code_md5=json.loads(k[3]),
                       orig_md5=json.loads(k[4]), platform=k[5], arch=k[6], hostname=k[7], python=k[8], numpy=k[9],
                       numba=k[10], n_files=v) for k, v in combos.items()]
    # totals per machine (canonical set + overlap separately)
    tot = {}
    for label, sel in (('mac', lambda r: r['machine'] == 'mac' and not r['id'].startswith('xover/')),
                       ('pc', lambda r: r['machine'] == 'pc' and not r['id'].startswith('xover/')),
                       ('xover_mac', lambda r: r['machine'] == 'mac' and r['id'].startswith('xover/')),
                       ('xover_pc', lambda r: r['machine'] == 'pc' and r['id'].startswith('xover/'))):
        R = [r for r in recs if r.get('valid') and sel(r)]
        st = np.sum([r['status'] for r in R], axis=0).tolist() if R else []
        tot[label] = dict(files=len(R), events=sum(r['n_events'] for r in R), hits=sum(r['n_hits'] for r in R),
                          cpu_h_events=sum(r['cpu_ev_s'] for r in R) / 3600, cpu_h_jobs=sum(r['cpu_job_s'] for r in R) / 3600,
                          wall_h_events=sum(r['wall_ev_s'] for r in R) / 3600, est_cpu_h_M3=sum(r['est_s'] for r in R) / 3600,
                          bytes=sum(r['bytes'] for r in R), status_counts=st, n_rerun=sum(r['n_rerun'] for r in R),
                          n_swapped=sum(r['n_swapped'] for r in R), n_floor_flag=sum(r['n_floor'] for r in R),
                          steps=sum(r['nsteps'] for r in R), max_queue=max((r['maxq'] for r in R), default=0))
    by_camp = defaultdict(lambda: dict(files=0, events=0, hits=0, cpu_h=0.0, est_cpu_h_M3=0.0))
    for r in canon:
        if not r.get('valid'):
            continue
        camp = r['id'].split('/')[0]
        lam = float(r['id'].split('/L')[1].split('_')[0])
        k = f"{camp}{'_hi' if camp == 'p2' and lam >= 15 else ''}@{r['machine']}"
        d = by_camp[k]
        d['files'] += 1; d['events'] += r['n_events']; d['hits'] += r['n_hits']; d['cpu_h'] += r['cpu_ev_s'] / 3600
        d['est_cpu_h_M3'] += r['est_s'] / 3600
    # index: points -> chunks
    points = defaultdict(lambda: dict(chunks=[]))
    for r in sorted(recs, key=lambda r: r['id']):
        if not r.get('valid'):
            continue
        j = r['id']
        if j.startswith('xover/'):
            key = f"xover/{r['machine']}/{j.split('/', 1)[1].rsplit('_c', 1)[0]}"
        else:
            key = j.rsplit('_c', 1)[0]
        P = points[key]
        P['chunks'].append(dict(id=j, file=r['path'], machine=r['machine'], n_events=r['n_events'], n_hits=r['n_hits'],
                                md5=r['file_md5'], bytes=r['bytes'], cpu_s=round(r['cpu_ev_s'], 2),
                                status=r['status'], created_utc=r['created_utc']))
    for key, P in points.items():
        c0 = P['chunks'][0]
        P['n_events'] = sum(c['n_events'] for c in P['chunks'])
        P['n_hits'] = sum(c['n_hits'] for c in P['chunks'])
        P['machines'] = sorted({c['machine'] for c in P['chunks']})
    # attach point metadata from the job list
    jl = {j['id']: j for j in alljobs + ov}
    for key, P in points.items():
        j = jl[P['chunks'][0]['id']]
        P.update(campaign=j['campaign'], spin=j['spin'], m=j['m'], lam_keV=j['lam'], cfg=j['cfg'], max_boost=j['max_boost'],
                 vertex=j['vertex'], input=j['input'])
    # canonical symlink tree
    canon_root = C.DATA / 'canon'
    n_links = 0
    for r in recs:
        if not r.get('valid'):
            continue
        rel = r['id'] + '.npz'
        if r['id'].startswith('xover/'):
            rel = f"xover/{r['machine']}/{r['id'].split('/', 1)[1]}.npz"
        link = canon_root / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        target = os.path.relpath(C.DATA / r['path'], link.parent)
        if link.is_symlink() or link.exists():
            link.unlink()
        os.symlink(target, link)
        n_links += 1
    checks = dict(partition=part, n_expected_files=len(tasks), n_found=sum(r['exists'] for r in recs),
                  missing=missing, invalid=invalid, job_definition_differs=diffjob, code_md5_differs=md5_bad,
                  input_md5_differs=inp_bad, canonical_jobs_not_exactly_once=dup_jobs, duplicate_events_in_canonical=dup_events,
                  extra_files=extra, current_code_md5=cur_md5, n_canon_symlinks=n_links)
    checks['PASS'] = bool(not missing and not invalid and not diffjob and not md5_bad and not inp_bad and not dup_jobs
                          and dup_events == 0 and part['mac_pc_disjoint'] and part['mac_pc_cover_all'])
    index = dict(meta=dict(created_by='sim/stage3/scripts/merge_index.py (E8, 2026-10-13)',
                           note='Canonical Stage-3 production: every job of jobs/all.json exactly once (paths relative to '
                                'data/sim_stage3/), plus the 3 cross-machine overlap clones per machine under xover/<machine>/. '
                                'Campaign mv = the plan\'s "matvar". canon/ holds relative symlinks with the same layout. '
                                'Units in the files: mm, ns, GeV; thickness in um. Truth level.',
                           units=dict(length='mm', time='ns', momentum='GeV', thickness='um'),
                           machines=dict(mac='data/sim_stage3/out (Apple M3, macOS, 7 workers)',
                                         pc='data/sim_stage3/out_pc (AMD 7800X3D, Windows 11, 10 then 15 workers)')),
                 checks=checks, environments=combo_list, totals=tot, by_campaign=dict(by_camp),
                 points=dict(sorted(points.items())))
    json.dump(index, open(C.INDEX, 'w'), indent=1, default=C._default)
    small = {k: v for k, v in index.items() if k != 'points'}
    small['n_points'] = len(points)
    C.dump('merge.json', small)
    print(json.dumps(dict(checks={k: (v if not isinstance(v, list) or len(v) < 10 else f'{len(v)} items') for k, v in checks.items()},
                          totals=tot, n_points=len(points), environments=len(combo_list)), indent=1, default=C._default))


if __name__ == '__main__':
    main()
