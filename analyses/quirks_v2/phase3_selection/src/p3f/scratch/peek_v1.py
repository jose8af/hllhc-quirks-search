"""V1 failure diagnosis (R04 volumes only): concentration of the expected recapture sum."""
import sys, json
import numpy as np
for fn in sys.argv[1:]:
    z = np.load(fn); M = json.loads(str(z['meta_json']))['planes']
    k = 0
    while f'val{k}_rec' in z.files:
        rec = z[f'val{k}_rec']; V = z[f'val{k}_V'][:, 0]
        for mp in (0, 1):
            v = np.sort(V[rec[:, 0] == mp])[::-1] * M
            print(fn, k, mp, 'n %d sum MV %.0f top1 %.0f top5 %.0f median MV %.3f' % (len(v), v.sum(), v[0], v[:5].sum(), np.median(v)))
        k += 1
