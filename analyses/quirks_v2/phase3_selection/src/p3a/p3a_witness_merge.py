"""p3a_witness_merge.py -- merge the outputs of p3a_witness_check.py.  python3 -I p3a_witness_merge.py <out.json> <in.json> ..."""
import json
import sys
from pathlib import Path

out = dict(parts=[], n_files=0, tables={}, n_fails=0, fails=[], cpu_s=0.0)
for f in sys.argv[2:]:
    j = json.loads(Path(f).read_text())
    out['parts'].append(dict(file=Path(f).name, stride=j['stride'], offset=j['offset'], n_files=j['n_files'], cpu_s=j['cpu_s']))
    out['n_files'] += j['n_files']; out['cpu_s'] += j['cpu_s']; out['n_fails'] += j['n_fails']; out['fails'] += j['fails']
    out['nils_sha256'] = j['nils_sha256']; out['p3a_subset_sha256'] = j['p3a_subset_sha256']; out['rows'] = j['rows']
    for wn, t in j['tables'].items():
        o = out['tables'].setdefault(wn, {})
        for k, v in t.items():
            if k == 'why':
                w = o.setdefault('why', {})
                for a, b in v.items():
                    w[a] = w.get(a, 0) + b
            else:
                o[k] = o.get(k, 0) + v
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
for wn, t in out['tables'].items():
    sys.stdout.write(f'{wn} {t}\n')
sys.stdout.write(f"files {out['n_files']} cpu_s {out['cpu_s']:.0f} n_fails {out['n_fails']}\n")
