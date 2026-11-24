"""Identity and timing check of the repaired thinning (p3-b, Casper).  Run on a worker (numba):
   python test_thin.py <pu2 job npz> <its premerge npz> [trials]
q = 1 (keep every interaction) must reproduce the stored ρ = 2 per-trial n_grp and n_pass of the main npz at R04-R14
(production.process_trial grouping and rung flags); then one K = 64, q = 1/2 trial is timed."""
import logging
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thin_core as TC  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("test_thin")
main = np.load(sys.argv[1])
z = np.load(sys.argv[2])
ntr = int(sys.argv[3]) if len(sys.argv) > 3 else 2
bad = 0
for t in range(ntr):
    d = TC.trial_inputs(z, t, main['trials.pv'][t])
    t0 = time.time()
    grp, npass, n4 = TC.run_trial(d, 1.0, 1, 1)
    ref_g = main['trials.n_grp'][t, 3:14]; ref_p = main['trials.n_pass'][t, 3:14]
    log.info("trial %d q=1: %.1f s; grp %s vs stored %s; npass %s vs %s", t, time.time() - t0, grp[0, :11], ref_g,
             npass[0, :11], ref_p)
    bad += int(np.any(grp[0, :11] != ref_g) or np.any(npass[0, :11] != ref_p))
    # stored rho = 2 group ids of the R04 set: same partition?
    t0 = time.time()
    g64, p64, n464 = TC.run_trial(d, 0.5, 64, 12345 + t)
    log.info("trial %d q=1/2 K=64: %.1f s; mean grp R04..R08 %s; mean n4 %.1f", t, time.time() - t0,
             np.round(g64[:, :5].mean(0), 3), n464.mean())
log.info("identity mismatches: %d of %d trials", bad, ntr)
