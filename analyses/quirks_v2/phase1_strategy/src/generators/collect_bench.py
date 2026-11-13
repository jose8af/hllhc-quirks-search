"""collect_bench.py -- merge bench.sh results.tsv files (copied from schrodinger) + the fixed facts of tasks 1/2/4/5 into
phase1_strategy/outputs/feasibility/benchmarks_generators.json.  Stdlib only.
Usage: python3 -I collect_bench.py <dir with <name>/results.tsv> <out.json>
"""
import json
import os
import statistics
import sys

src, out = sys.argv[1], sys.argv[2]
facts = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bench_facts.json')))
bench = {}
for name in sorted(os.listdir(src)):
  d = {}
  for fn, suffix in (('results.tsv', ''), ('inner.tsv', '_timed_step')):
    p = os.path.join(src, name, fn)
    if not os.path.exists(p):
        continue
    rows = [l.rstrip('\n').split('\t') for l in open(p) if l.strip()]
    for mode in ('single', 'conc'):
        r = [x for x in rows if x[1] == mode and x[7] == '0']
        bad = [x for x in rows if x[1] == mode and x[7] != '0']
        if not r:
            continue
        cpu = [float(x[3]) + float(x[4]) for x in r]
        wall = [float(x[5]) for x in r]
        rss = [float(x[6]) / 1024 for x in r]
        f = lambda v: {'mean': round(statistics.mean(v), 3), 'min': round(min(v), 3), 'max': round(max(v), 3)}
        d[mode + suffix] = {'N': len(r), 'failed': len(bad), 'cpu_s': f(cpu), 'wall_s': f(wall), 'max_rss_mb': f(rss)}
  if d:
    bench[name] = d
facts['benchmarks'] = bench
facts['benchmarks_note'] = ('VERIFIED: /usr/bin/time -v on schrodinger (i5-7500), nice 10, node-local scratch; '
                            'cpu = user + sys including waited children; single = 3 sequential runs, conc = 3 at once; '
                            'mean/min/max over N. Raw: <scratch>/basil_bench/<name>/results.tsv, copied to '
                            'phase1_strategy/outputs/feasibility/bench_raw/.')
json.dump(facts, open(out, 'w'), indent=1)
print('wrote', out, len(bench), 'benchmarks')
