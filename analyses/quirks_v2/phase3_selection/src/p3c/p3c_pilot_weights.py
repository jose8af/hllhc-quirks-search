"""p3c_pilot_weights.py -- v2 (MET-model) preselection weights of the Z(nunu) pilot events (p3-c; ADD §3 "41 is
provisional ... recomputed with the v2 MET model").

  <python> p3c_pilot_weights.py <out.npz> <list of pilot files.txt> [model.json]

Reads only evt, jets, lep, gsum of each pilot file.  One row per pilot event (COLS).  The single-throw weights are
reproducible: generator seeded with (job_seed of the pilot file, variation-independent constant), events in file
order, the same random numbers for every variation (so variations are correlated event by event).
The pilot holds only events with truth MET(nu) > 200 GeV and pT-hat > 150 GeV (its generator filter).
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np

import metmodel as M
import p3c_io as IO

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3c_pilot_weights')
HERE = Path(__file__).resolve().parent
MODEL = HERE.parents[1] / 'outputs' / 'p3c' / 'model.json'
VARS = ['nominal', 'core_up', 'core_dn', 'jes_up', 'jes_dn', 'soft_up', 'soft_dn', 'tail_up', 'tail_dn', 'soft_mix',
        'all_up', 'all_dn']
COLS = (['chunk', 'event', 'truth_met', 'w_v1', 'n_gamma_veto', 'met_reco_v2', 'p_v2_mean20', 'w_v2_trig_erf_shifted']
        + [f'w_v2_{v}' for v in VARS] + ['phimet_reco_v2'])
K_MEAN = 20


def main(argv):
    out = Path(argv[0]); files = [l for l in Path(argv[1]).read_text().split() if l]
    model = json.loads((Path(argv[2]) if len(argv) > 2 else MODEL).read_text())
    rows = []; names = []
    for f in files:
        d = IO.load(f); meta = d['meta']; n = d['n']
        a = np.zeros((n, len(COLS)), np.float32)
        a[:, 0] = meta['chunk']; a[:, 1] = np.arange(n); a[:, 2] = np.hypot(d['met'][:, 0], d['met'][:, 1])
        a[:, 3] = d['w_v1']; a[:, 4] = d['inp']['ngam']
        for j, v in enumerate(VARS):
            rng = np.random.default_rng([int(meta['job_seed']), 20261124])
            o = M.apply(d['inp'], M.params(v, model), rng, 1, return_met=True)
            a[:, 8 + j] = o['w'][:, 0]
            if v == 'nominal':
                a[:, 5] = o['met'][:, 0]
                a[:, 8 + len(VARS)] = np.arctan2(-o['hy'][:, 0], -o['hx'][:, 0])   # road axis of v2
        rng = np.random.default_rng([int(meta['job_seed']), 20261124])
        a[:, 7] = M.apply(d['inp'], dict(M.params('nominal', model), trig='erf_shifted'), rng, 1)['w'][:, 0]
        rng = np.random.default_rng([int(meta['job_seed']), 20261125])
        p = np.zeros(n)
        for s in range(0, n, 1000):
            p[s:s + 1000] = M.apply(IO.sub(d['inp'], slice(s, s + 1000)), M.params('nominal', model), rng, K_MEAN)['w'].mean(1)
        a[:, 6] = p
        rows.append(a); names.append(Path(f).name)
        log.info('%s: n %d  sum w_v1 %.1f  sum w_v2 %.1f  (mean of 20 throws %.1f)', names[-1], n, a[:, 3].sum(),
                 a[:, 8].sum(), a[:, 6].sum())
    A = np.concatenate(rows)
    meta = dict(mode='p3c_pilot_weights', cols=COLS, files=names, model=model, nominal=M.params('nominal', model),
                n_events=int(len(A)))
    tmp = out.with_name(out.name + '.tmp.npz')
    np.savez_compressed(tmp, meta=np.array(json.dumps(meta)), w=A)
    tmp.replace(out)


if __name__ == '__main__':
    main(sys.argv[1:])
