"""val_v6.py -- Stage-3 validation V6: seeds and reproducibility of the production runner.

50 jobs drawn at random (seed 2026) from jobs/all.json among the cheap ones (estimate < 20 M3-CPU-s, so all campaigns
and stochastic configurations M/BM/variants are represented) are run TWICE through run_stage3.py (spawn start method)
into two scratch output trees with different worker counts (7 and 3, so the job-to-worker assignment and order differ).
PASS: every array of every output is bit-identical between the two runs, except the timing fields (cpu_s, wall_s,
meta_json); and no two DIFFERENT events (within and across the 50 files) have identical hit arrays.
Output: sim/stage3/results/V6.json.  Run: nice pixi run python sim/stage3/validation/val_v6.py
"""
import json
import shutil
import subprocess
import sys
import time

import numpy as np

import vcommon as V

if __name__ == '__main__':
    allj = json.load(open(V.S3 / 'jobs' / 'all.json'))['jobs']
    cheap = [j for j in allj if j['est_s'] < 20]
    rng = np.random.default_rng(2026)
    pick = [cheap[i] for i in sorted(rng.choice(len(cheap), 50, replace=False))]
    jf = V.VOUT / 'v6_jobs.json'
    json.dump(dict(name='v6', jobs=pick), open(jf, 'w'))
    runner = V.S3 / 'code' / 'run_stage3.py'
    tic = time.time()
    reuse = len(sys.argv) > 1 and sys.argv[1] == '--compare-only'
    for tag, nw in (('A', 7), ('B', 3)):
        od = V.VOUT / f'v6_{tag}'
        if reuse:
            continue
        if od.exists():
            shutil.rmtree(od)
        subprocess.run([sys.executable, str(runner), 'run', '--jobs', str(jf), '--workers', str(nw), '--inputs',
                        str(V.TT / 'data' / 'sim_stage3' / 'inputs'), '--out', str(od)], check=True)
    skip = {'cpu_s', 'wall_s', 'meta_json'}
    ndiff = 0; diffs = []; sigs = {}; ndup = 0
    for j in pick:
        a = np.load(V.VOUT / 'v6_A' / j['out']); b = np.load(V.VOUT / 'v6_B' / j['out'])
        for k in a.files:
            if k in skip:
                continue
            if not np.array_equal(a[k], b[k], equal_nan=(a[k].dtype.kind == 'f')):     # NaN ds (< 4 hits) == NaN
                ndiff += 1; diffs.append((j['id'], k))
        off = a['hit_offsets']
        for e in range(len(off) - 1):
            sl = slice(off[e], off[e + 1])
            key = (a['h_x'][sl].tobytes(), a['h_t'][sl].tobytes())
            if off[e + 1] > off[e]:
                if key in sigs:
                    ndup += 1
                sigs[key] = (j['id'], e)
    meta = json.loads(str(np.load(V.VOUT / 'v6_A' / pick[0]['out'])['meta_json']))
    out = dict(n_jobs=len(pick), campaigns=sorted({j['campaign'] for j in pick}), cfgs=sorted({j['cfg'] for j in pick}),
               n_events=int(sum(len(j['ev']) for j in pick)), n_array_differences=ndiff, differences=diffs[:20],
               n_duplicate_event_hit_arrays=ndup, start_method='spawn (ProcessPoolExecutor, mp_context spawn)',
               seed_rule=meta['seed_rule'], wall_s=time.time() - tic)
    out['PASS'] = bool(ndiff == 0 and ndup == 0)
    V.dump('V6.json', out)
    print(json.dumps(out, indent=1))
