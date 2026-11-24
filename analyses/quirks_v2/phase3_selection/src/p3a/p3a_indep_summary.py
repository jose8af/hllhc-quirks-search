"""p3a_indep_summary.py -- summary of the p3-a-ind outputs (Nils's search at the widths / s his review did not cover).

  <tt python> -I p3a_indep_summary.py <dir with *ind*.json> <out.json>

Per width (R04 'none' and 75 mm, R05..R08), s = 0 / 3, reading S / F, Z full-weight class (w >= 0.5): of the events
the Phase-2 classifier COUNTS (k <= 3 or 5), how many have a VERIFIED witness of the independent search with
k <= k_max ("confirmed"), with k <= the Phase-2 k ("same or lower"), and how many were not found.  Also the number of
counted events with a verified hard-window witness (category H of his search; N_IT2 not required).
"""
import glob
import json
import sys
from pathlib import Path

NAMES = ['R04n', 'R04w', 'R05', 'R06', 'R07', 'R08']
KMAX = (3, 5)


def main(d, out):
    fs = sorted(glob.glob(str(Path(d) / '*ind*.json')))
    res = dict(n_outputs=len(fs), n_files=0, n_events=0, n_bad=0, cpu_s=0.0, tables={}, nils_sha256=set(), parts=[])
    T = {}
    for f in fs:
        j = json.loads(Path(f).read_text())
        res['n_files'] += len(j['files']); res['n_bad'] += j['n_bad']; res['cpu_s'] += j['cpu_s']
        res['nils_sha256'].add(j['nils_sha256']); res['parts'].append([j['part'], j['nparts'], j['stride'], j['offset']])
        wmap = j['wmap']
        for path, i, w, r, kk in j['events']:
            if w < 0.5:
                continue
            res['n_events'] += 1
            for ni, (wi, W) in enumerate(wmap):
                rr = r.get(str(float(W)))
                if rr is None:
                    continue
                for si in range(2):
                    for ri in range(2):
                        hers = kk[wi * 4 + si * 2 + ri]
                        if hers > KMAX[si]:
                            continue
                        t = T.setdefault(f"{NAMES[ni]}_s{3 * si}_{'SF'[ri]}", dict(counted=0, confirmed=0, same_or_lower=0,
                                                                                    not_found=0, hard=0, not_found_in_reach=0,
                                                                                    not_found_out_of_reach=0))
                        t['counted'] += 1
                        v = rr[ri]
                        mine = 99 if v is None else v[0] + (max(0, 3 - v[1]) if si else 0)
                        if mine <= KMAX[si]:
                            t['confirmed'] += 1
                            t['same_or_lower'] += mine <= hers
                        else:
                            t['not_found'] += 1
                            # his search looks at planes with N_IP2 >= 4 only: an s = 3 row whose s = 0 deficit is
                            # above 3 in the Phase-2 row needs k_IP >= 4 and is outside its reach
                            if si == 1 and kk[wi * 4 + ri] > 3:
                                t['not_found_out_of_reach'] += 1
                            else:
                                t['not_found_in_reach'] += 1
                        h = rr[2]
                        if h is not None and h[0] + (max(0, 3 - h[1]) if si else 0) <= KMAX[si] and ri == 0:
                            t['hard'] += 1
    res['tables'] = T; res['nils_sha256'] = sorted(res['nils_sha256'])
    Path(out).write_text(json.dumps(res, indent=1))
    for k in sorted(T):
        sys.stderr.write(f'{k} {T[k]}\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
