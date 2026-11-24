"""p3-b exploratory peek 2 (Casper): hit composition of R05/R06 direct pile-up candidates (one C1 pu1 job)."""
import logging, sys
import numpy as np
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("peek2")
d = np.load(sys.argv[1])
F = np.unpackbits(d['cand.rungs'], axis=1)[:, :43].astype(bool)
hc = d['hit.cand']; ht = d['hit.trial']; off = d['hit.off']; ref = d['hit.ref']
part = d['hit.particle']; INT = d['hit.INT']; sid = d['hit.sid']
ctr = d['cand.trial']; cidx = d['cand.idx']
key = {(int(t), int(c)): i for i, (t, c) in enumerate(zip(ctr, cidx))}
for k, name in [(4, 'R05'), (5, 'R06')]:
    stats = []
    for h in range(len(hc)):
        i = key[(int(ht[h]), int(hc[h]))]
        if not F[i, k] or (k == 4 and F[i, 5]):
            continue
        r = ref[off[h]:off[h + 1]]
        p = part[r]; I = INT[r]
        topup = (I % 1_000_000) >= 500_000
        fat = ~topup
        up, cnt = np.unique(p[fat], return_counts=True) if fat.any() else (np.zeros(0), np.zeros(0, int))
        ui = np.unique(I[fat])
        stats.append((len(r), topup.mean(), len(up), cnt.max() if len(cnt) else 0, len(ui)))
    s = np.array(stats, float)
    if len(s):
        log.info("%s(excl deeper) n=%d nhit %.0f topup_frac %.2f n_particles %.1f max_hits_1particle q50 %.0f q90 %.0f n_int(fatras) %.1f",
                 name, len(s), s[:, 0].mean(), s[:, 1].mean(), s[:, 2].mean(), np.median(s[:, 3]), np.quantile(s[:, 3], .9), s[:, 4].mean())
