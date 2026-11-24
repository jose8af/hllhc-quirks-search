"""Check of the B2-a remediation variants (p3-b, Casper): q = 1 sanity (refit of converged ρ = 2 planes changes little)
and the first look at q = 1/2 on two trials, against the frozen estimator with the same draws."""
import logging
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thin_core as TC  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger('test_thinvar')
main = np.load(sys.argv[1]); z = np.load(sys.argv[2])
for t in range(2):
    d = TC.trial_inputs(z, t, main['trials.pv'][t])
    log.info('trial %d stored rho=2 n_grp R04-R06 %s', t, main['trials.n_grp'][t, 3:6])
    for mode in (1, 2, 3):
        t0 = time.time()
        g, n4 = TC.run_trial_var(d, 1.0, 1, 1, mode)
        log.info('  q=1 mode %d: grp R04-R06 %s (n4 %d) %.1f s', mode, g[0, :3], n4[0], time.time() - t0)
    g0, _, _ = TC.run_trial(d, 0.5, 16, 99)
    log.info('  q=1/2 frozen: grp R04-R06 %s', np.round(g0[:, :3].mean(0), 2))
    for mode in (1, 2, 3):
        t0 = time.time()
        g, n4 = TC.run_trial_var(d, 0.5, 16, 99, mode)
        log.info('  q=1/2 mode %d: grp R04-R06 %s, n4 %.0f, %.1f s', mode, np.round(g[:, :3].mean(0), 2), n4.mean(),
                 time.time() - t0)
