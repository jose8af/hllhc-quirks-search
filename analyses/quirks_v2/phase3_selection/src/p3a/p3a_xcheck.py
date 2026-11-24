"""p3a_xcheck.py -- cross-check: rows of p3a_subset.py (campaign p3-a-cls-m, stopped after 60 files) against variant m of
p3a_multi.py (campaign p3-a-clsxz) on the same pilot files.  <tt python> -I p3a_xcheck.py <dir cls-m> <glob xz m> <out.json>"""
import glob
import json
import sys
from pathlib import Path

import numpy as np


def rows(fs):
    d = {}; files = set()
    for f in fs:
        z = np.load(f); m = json.loads(str(z['meta']))
        for fi, fm in enumerate(m['files']):
            files.add(fm['path'])
        for ri, rf in zip(z['rows_i'], z['rows_f']):
            d[(m['files'][int(ri[0])]['path'], int(ri[1]), int(ri[2]))] = (ri[3:].tolist(), rf.tolist())
    return d, files


a, fa = rows(sorted(glob.glob(str(Path(sys.argv[1]) / '*.npz'))))
b, fb = rows(sorted(glob.glob(sys.argv[2])))
common = fa & fb
ka = {k for k in a if k[0] in common}; kb = {k for k in b if k[0] in common}
res = dict(n_common_files=len(common), n_rows_subset=len(ka), n_rows_multi=len(kb), n_only_subset=len(ka - kb),
           n_only_multi=len(kb - ka), n_different=sum(a[k] != b[k] for k in ka & kb))
res['passes'] = res['n_only_subset'] == 0 and res['n_only_multi'] == 0 and res['n_different'] == 0 and len(ka) > 0
Path(sys.argv[3]).write_text(json.dumps(res, indent=1))
sys.stderr.write(json.dumps(res) + '\n')
