"""Runner job: repaired thinning (B2-a) of C1 ρ = 2 development jobs (p3-b, Casper).

  python thin_job.py --id ID --jobs c1pu2-0000,c1pu2-0001,... [--K 64]
Reads <pu2 job>.npz (trial PV, ev, road) and <pu2 job>.premerge.npz from the C1 campaign p2-a-c1-pu2 (development role,
STR §4.17 row 2) and writes $QV2_OUT_DIR/ID.npz:
  grp (ntr, K, NCOL) int32 distinct groups per subset and column;  npass (same) passing candidates (union diagnostic);
  n4 (ntr, K) thinned R04 candidates;  job, ev, road (ntr,);  cols;  meta_json (seeds, q, K, code sha256).
Seed of trial t of job J: blake2b("qv2|p3b.thin|J|t") (STR §4.17 seed scheme)."""
import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import thin_core as TC  # noqa: E402

SRC = Path('/nfs/cajuela/jdochoa/quirks_v2/data/phase2/p2-a-c1-pu2/000')
log = logging.getLogger('thin_job')


def seed_of(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % (2 ** 31 - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--K', type=int, default=64)
    ap.add_argument('--q', type=float, default=0.5)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    G, Pn, N4, JB, EV, RD, SEEDS = [], [], [], [], [], [], []
    t0 = time.time()
    for jid in a.jobs.split(','):
        main_npz = np.load(SRC / f'{jid}.npz')
        z = np.load(SRC / f'{jid}.premerge.npz')
        ntr = int(main_npz['n_trials'])
        for t in range(ntr):
            d = TC.trial_inputs(z, t, main_npz['trials.pv'][t])
            sd = seed_of(f'qv2|p3b.thin|{jid}|{t}')
            g, p, n4 = TC.run_trial(d, a.q, a.K, sd)
            G.append(g.astype(np.int32)); Pn.append(p.astype(np.int32)); N4.append(n4.astype(np.int32))
            JB.append(jid); EV.append(int(main_npz['trials.ev'][t])); RD.append(int(main_npz['trials.road'][t]))
            SEEDS.append(sd)
        log.info('%s: %d trials, %.1f s so far', jid, ntr, time.time() - t0)
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in ('thin_core.py', 'thin_job.py')}
    meta = dict(jobs=a.jobs.split(','), K=a.K, q=a.q, seeds=SEEDS, code_sha256=code, src=str(SRC),
                created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), wall_s=time.time() - t0)
    np.savez_compressed(out / f'{a.id}.npz', grp=np.array(G), npass=np.array(Pn), n4=np.array(N4), job=np.array(JB),
                        ev=np.array(EV), road=np.array(RD), cols=np.array(TC.COLS),
                        meta_json=np.array(json.dumps(meta)))


if __name__ == '__main__':
    main()
