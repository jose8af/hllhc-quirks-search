"""p2w_partial_check.py -- acceptance of p2w_subset.py on the pilot files classified so far (Cecilie, 2026-11-19).

  <tt python> p2w_partial_check.py      (worker; prints: finder near-passes, violations k_sub(F) > k_finder, k_sub < k_finder)
"""
import glob
import json
import logging
import sys

import numpy as np

log = logging.getLogger('p2w_partial_check')
D = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c'
WN = ['R04', 'R05', 'R06', 'R07', 'R08']; WV = dict(R04=1e9, R05=37.5, R06=18.75, R07=9.4, R08=4.7)


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    rows = {}; files = set(); cpu = 0.0; nj = 0; ix = None
    for f in glob.glob(D + '/rule1_valid/p2-c-r1v-s[23][ab]/000/*.npz'):
        z = np.load(f); m = json.loads(str(z['meta'])); r = z['rows']; ix = {k: i for i, k in enumerate(m['row_cols'])}
        cpu += m['cpu_s']; nj += 1
        for fi, fm in enumerate(m['files']):
            files.add(fm['path'])
            for x in r[r[:, 0] == fi]:
                rows[(fm['path'], int(x[1]), int(x[2]))] = x
    log.info('%d jobs, %d files, %d rows, %.2f CPU-h', nj, len(files), len(rows), cpu / 3600)
    acc = {}
    for f in glob.glob(D + '/pilot_class/p2-c-pilot-cls*/000/*.npz'):
        z = np.load(f); m = json.loads(str(z['meta'])); c = z['cand']; cx = {k: i for i, k in enumerate(m['cand_cols'])}
        fk = {}
        for r in c:
            p = m['files'][int(r[0])]['path']
            if p not in files or r[cx['variant']] != 0 or r[cx['nit2']] < 3:
                continue
            key = (p, int(r[1]), int(r[2]))
            for wn in WN:
                if wn == 'R04' or r[cx['dw_core']] < WV[wn]:
                    for s in (0, 3):
                        k = int(7 - r[cx['nip2']] + max(0, s - r[cx['n2s2']])); fk[(key, wn, s)] = min(fk.get((key, wn, s), 99), k)
        for (key, wn, s), k in fk.items():
            if k > (7 + s) // 2:
                continue
            a = acc.setdefault((wn, s), [0, 0, 0, []]); a[0] += 1
            mine = int(rows[key][ix[f'k_{wn}_s{s}_F']]) if key in rows else 99
            if mine > k:
                a[1] += 1; a[3].append((key[0][-9:], key[1], key[2], k, mine))
            elif mine < k:
                a[2] += 1
    for k, a in sorted(acc.items()):
        log.info('%s finder near %d, violations %d, sub lower %d %s', k, a[0], a[1], a[2], a[3][:4])


if __name__ == '__main__':
    main()
