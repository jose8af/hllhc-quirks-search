"""p3-b exploratory peek (Casper, 2026-11-24): R04+ candidate structure of one C1 pu1 job (development sample)."""
import json, logging, sys
import numpy as np
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("peek")
f = sys.argv[1]
d = np.load(f)
F = np.unpackbits(d['cand.rungs'], axis=1)[:, :43].astype(bool)
nz = d['cand.normal'][:, 2]
for k, name in [(3, 'R04'), (4, 'R05'), (5, 'R06'), (6, 'R07')]:
    m = F[:, k]
    if not m.any():
        log.info("%s none", name); continue
    log.info("%s n=%d |nz| q10/50/90 %s  dw_core q50 %.1f  n_band q50 %d  n2s2 mean %.2f  nhit q50 %d", name, m.sum(),
             np.round(np.quantile(np.abs(nz[m]), [.1, .5, .9]), 4), np.median(d['cand.dw_core'][m]),
             np.median(d['cand.n_band'][m]), d['cand.n2s2'][m].mean(), np.median(d['cand.nhit'][m]))
ng = d['trials.n_grp'][:, 3:9].sum(0); npass = d['trials.n_pass'][:, 3:9].sum(0)
log.info("n_grp sum R04-R09 %s ; n_pass %s ; trials %d", ng, npass, len(d['trials.ev']))
m = json.loads(str(d['meta_json']))
log.info("wcfg %s finder %s", m['wcfg'], m['finder_cfg'])
