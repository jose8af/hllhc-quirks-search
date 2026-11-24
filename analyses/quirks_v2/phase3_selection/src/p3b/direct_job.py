"""Runner job: direct ρ = 1 development counts per trial (p3-b, Casper).

  python direct_job.py --id ID --jobs c1pu1-0000,...
From the C1 pu1 job files (development role, STR §4.17 row 1; every R04 passer is stored with its group id) the per
trial number of distinct groups with >= 1 passing member, and of passing candidates, for every column of
thin_core.COLS (same col_flags as the thinning).  Check: the cumulative columns R04-R14 must equal trials.n_grp[:, 3:14]
of the file (the job raises otherwise).  Output $QV2_OUT_DIR/ID.npz: grp (ntr, NCOL), npass (ntr, NCOL), job, ev, road,
trial_seed, cols, meta_json."""
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

SRC = Path('/nfs/cajuela/jdochoa/quirks_v2/data/phase2/p2-a-c1-pu1/000')
log = logging.getLogger('direct_job')


def job_counts(f):
    keys = ['trials.n_grp', 'trials.n_pass', 'trials.ev', 'trials.road', 'trials.trial_seed', 'cand.trial',
            'cand.group', 'cand.rungs', 'cand.dw_core', 'cand.p_chi2core', 'cand.n2s2']
    with np.load(f) as z:
        d = {k: z[k] for k in keys}
    ntr = len(d['trials.ev'])
    F = np.unpackbits(d['cand.rungs'], axis=1)[:, :43].astype(bool)
    r4 = F[:, 3]
    C = TC.direct_cols(r4, d['cand.dw_core'].astype(np.float64), d['cand.p_chi2core'].astype(np.float64),
                       d['cand.n2s2'].astype(np.int64))
    grp = np.zeros((ntr, TC.NCOL), np.int64); npass = np.zeros((ntr, TC.NCOL), np.int64)
    tr = d['cand.trial']; gid = d['cand.group']
    for j in range(TC.NCOL):
        m = C[:, j]
        npass[:, j] = np.bincount(tr[m], minlength=ntr)
        if m.any():
            u = np.unique(np.c_[tr[m], gid[m]], axis=0)
            grp[:, j] = np.bincount(u[:, 0], minlength=ntr)
    # identity checks against the in-job counts (cumulative ladder) and the stored rung bits
    if np.any(grp[:, :11] != d['trials.n_grp'][:, 3:14]) or np.any(npass[:, :11] != d['trials.n_pass'][:, 3:14]):
        raise RuntimeError(f'{f}: recomputed R04-R14 counts differ from trials.n_grp / n_pass')
    if np.any(C[:, :11] != F[:, 3:14]):
        raise RuntimeError(f'{f}: recomputed rung flags differ from cand.rungs R04-R14')
    return grp, npass, d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--jobs', required=True)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    G, P, JB, EV, RD, TS = [], [], [], [], [], []
    for jid in a.jobs.split(','):
        g, p, d = job_counts(SRC / f'{jid}.npz')
        G.append(g); P.append(p); JB += [jid] * len(g); EV.append(d['trials.ev']); RD.append(d['trials.road'])
        TS.append(d['trials.trial_seed'])
        log.info('%s: %d trials, R04-R07 groups %s', jid, len(g), g[:, :4].sum(0))
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in ('thin_core.py', 'direct_job.py')}
    meta = dict(jobs=a.jobs.split(','), code_sha256=code, src=str(SRC),
                created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    np.savez_compressed(out / f'{a.id}.npz', grp=np.concatenate(G).astype(np.int32),
                        npass=np.concatenate(P).astype(np.int32), job=np.array(JB), ev=np.concatenate(EV),
                        road=np.concatenate(RD), trial_seed=np.concatenate(TS), cols=np.array(TC.COLS),
                        meta_json=np.array(json.dumps(meta)))


if __name__ == '__main__':
    main()
