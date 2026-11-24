"""vilde_ind2_tally.py -- tally of the independent search (Nils's search_event/verify via p3a_indep.py, unchanged) on the
SECOND half of the Z(nunu) pilot files (--stride 2 --offset 1), and the two halves combined.  Vilde, reviewer, 2026-11-24.
Does not import p3a_indep_summary.py.  Usage: python3 -I vilde_ind2_tally.py <dir second half> <dir first half> <out.json>
A counted event (Phase-2 k <= k_max in the stored row, reading S or F) is 'confirmed' if the independent search has a
VERIFIED witness with k_IP + (max(0, 3 - N_2S2) if s = 3) <= k_max.  Full-weight class only (w >= 0.5)."""
import glob, json, sys
NAMES = ['R04n', 'R04w', 'R05', 'R06', 'R07', 'R08']; KMAX = (3, 5)
def tally(files):
    T = {}; nf = 0; nev = 0; nbad = 0; cpu = 0.0; paths = set()
    for f in files:
        j = json.load(open(f)); nf += len(j['files']); nbad += j['n_bad']; cpu += j['cpu_s']
        for x in j['files']:
            assert x['path'] not in paths; paths.add(x['path'])
        for path, i, w, r, kk in j['events']:
            if w < 0.5:
                continue
            nev += 1
            for ni, (wi, W) in enumerate(j['wmap']):
                rr = r.get(str(float(W)))
                for si in (0, 1):
                    for ri in (0, 1):
                        if kk[wi * 4 + si * 2 + ri] > KMAX[si]:
                            continue
                        t = T.setdefault(f"{NAMES[ni]}_s{3 * si}_{'SF'[ri]}", dict(counted=0, confirmed=0, not_found=0, out_of_reach=0))
                        t['counted'] += 1
                        v = None if rr is None else rr[ri]
                        k = 99 if v is None else v[0] + (max(0, 3 - v[1]) if si else 0)
                        if k <= KMAX[si]:
                            t['confirmed'] += 1
                        else:
                            t['not_found'] += 1
                            t['out_of_reach'] += int(si == 1 and kk[wi * 4 + ri] > 3)
    return dict(n_files=nf, n_events=nev, n_bad=nbad, cpu_s=cpu, tables=T), paths
a, pa = tally(sorted(glob.glob(sys.argv[1] + '/*.ind.json')))
b, pb = tally(sorted(glob.glob(sys.argv[2] + '/*.ind.json')))
assert not (pa & pb), 'the two halves share files'
c = {k: {x: a['tables'][k][x] + b['tables'][k][x] for x in a['tables'][k]} for k in a['tables']}
for d in (a['tables'], b['tables'], c):
    for k in d:
        d[k]['frac'] = round(100.0 * d[k]['confirmed'] / d[k]['counted'], 2)
json.dump(dict(second_half=a, first_half=b, combined=dict(n_files=a['n_files'] + b['n_files'], n_events=a['n_events'] + b['n_events'], tables=c)),
          open(sys.argv[3], 'w'), indent=1)
for k in sorted(c):
    print(k, 'second', a['tables'][k]['confirmed'], '/', a['tables'][k]['counted'], a['tables'][k]['frac'],
          '| first', b['tables'][k]['confirmed'], '/', b['tables'][k]['counted'], b['tables'][k]['frac'],
          '| all', c[k]['confirmed'], '/', c[k]['counted'], c[k]['frac'], 'out of reach', c[k]['out_of_reach'])
print('files', a['n_files'], b['n_files'], 'events', a['n_events'], b['n_events'], 'n_bad', a['n_bad'], b['n_bad'], 'cpu_s', a['cpu_s'], b['cpu_s'])
