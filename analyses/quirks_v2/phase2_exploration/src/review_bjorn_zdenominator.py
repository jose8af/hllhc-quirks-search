"""review_bjorn_zdenominator.py -- independent check of the Z(nunu) denominator of the rule-1 Z term from the pilot files.

  <tt python> review_bjorn_zdenominator.py '<glob of pilot.hs0.znn npz>' <out.json>

Bjorn (reviewer), 2026-11-19.  Reads only the members meta and evt of every Z(nunu) pilot file (read-only; no signal
file).  Reports: files, events, pile-up setting (meta mu), exact (unrounded) sum of w_v1 in the full-weight class
(w >= 0.5) and in the low class, w_max, M = sum w / w_max, and the number of events with w > 0.
"""
import glob
import json
import sys
from pathlib import Path

import numpy as np


def main(pat, out):
    fs = sorted(glob.glob(pat))
    r = dict(n_files=0, n_events=0, n_full=0, n_low=0, n_zero=0, sum_w_full=0.0, sum_w_low=0.0, w_max=0.0, mu=[],
             streams=[], n_met250=0)
    for f in fs:
        z = np.load(f)
        m = json.loads(str(z['meta'])); ec = m['evt_cols']; e = z['evt']
        w = e[:, ec.index('w_v1')].astype(np.float64)
        r['n_files'] += 1; r['n_events'] += len(w)
        r['n_full'] += int((w >= 0.5).sum()); r['n_low'] += int(((w > 0) & (w < 0.5)).sum()); r['n_zero'] += int((w <= 0).sum())
        r['sum_w_full'] += float(w[w >= 0.5].sum()); r['sum_w_low'] += float(w[(w > 0) & (w < 0.5)].sum())
        r['w_max'] = max(r['w_max'], float(w.max()))
        if m.get('mu') not in r['mu']:
            r['mu'].append(m.get('mu'))
        if m['stream'] not in r['streams']:
            r['streams'].append(m['stream'])
        z.close()
    r['M_full'] = r['sum_w_full'] / r['w_max']
    r['evt_cols'] = ec
    Path(out).write_text(json.dumps(r, indent=1))
    sys.stdout.write(json.dumps(r) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
