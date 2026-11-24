"""p3-b exploratory peek 3 (Casper): pre-merge store content of one C1 pu2 job (development sample)."""
import json, logging, sys, time
import numpy as np
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("peek3")
t0 = time.time()
z = np.load(sys.argv[1])
keys = sorted({k.split('/')[1] for k in z.files if k.startswith('t0/')})
log.info("keys t0: %s", keys)
meta = json.loads(str(z['meta_json.npy'] if 'meta_json.npy' in z.files else z['meta_json']))
log.info("meta: %s", {k: meta[k] for k in meta if k != 'job'})
for t in range(2):
    p = f't{t}/'
    nip2 = z[p + 'v_nip2']; nit2 = z[p + 'v_nit2']; al = z[p + 'aligned']
    sel = al & (nit2 >= 3) & (nip2 >= 7)
    off = z[p + 'off']; nref = np.diff(off)
    log.info("trial %d: ncand %d, aligned %d, presel(R04 at rho2) %d, refs total %d, refs presel %d, union hits %d, nINT %d",
             t, len(nip2), al.sum(), sel.sum(), off[-1], nref[sel].sum(), len(z[p + 'h_sid']), len(np.unique(z[p + 'h_INT'])))
log.info("read time %.1f s", time.time() - t0)
d = np.load(sys.argv[2])
log.info("main npz: trials %d, n_grp R04-R07 sum %s, rho %s", len(d['trials.ev']), d['trials.n_grp'][:, 3:7].sum(0), d['trials.rho'][:2])
log.info("S_ded R04-R07 sum %s", d['trials.S_ded'][:, 3:7].sum(0) if 'trials.S_ded' in d.files else 'n/a')
