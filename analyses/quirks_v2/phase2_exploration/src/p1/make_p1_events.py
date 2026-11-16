"""make_p1_events.py -- new P1 event sets (deviation EXPLORATION §3.1): from the S2-c inclusive samples (p2-b-s2c-inc,
nominal shower), the v1 P1 selection (sim/stage3/code/make_inputs.py l.1-20, l.42-48): w > 0, p_T(QQbar) > 200 GeV,
|eta_pair| < 1, vertex at the origin.  MLM inclusive weights are equal for kept events, so w > 0 is an unweighted set
(checked: the script asserts that the positive weights are equal to 1e-6 relative).  Per event the closed-form
quantities of sim/stage3/code/s3_physics.pair_truth (gamma*, eps_perp, k_B, c_ev, ...) are stored at the requested Lambda.
Usage (worker, TT env): python make_p1_events.py <out.npz> <inc_dir_glob_prefix> <mass> <spin F|S> <lam_keV> [<nmax>]
  e.g. ... /nfs/cajuela/jdochoa/quirks_v2/data/p2-b-s2c-inc/001/finc-m500 500 F 5.0
This selects truth-level signal kinematics only (no detector, no selection efficiency is formed or printed).
"""
import glob
import logging
import os
import sys

QV2 = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2'
for p in (f'{QV2}/sim/stage3/code', f'{QV2}/code'):
    sys.path.insert(0, p)
import numpy as np  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('make_p1_events')


def main():
    out, prefix, m, spin, lam = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], float(sys.argv[5])
    nmax = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 9
    from s3_physics import pair_truth
    files = sorted(glob.glob(prefix + '*.nom.npz'))
    rows = []
    for f in files:
        d = np.load(f)
        w = d['w']
        pos = w > 0
        wp = w[pos]
        if len(wp) and np.max(np.abs(wp / wp[0] - 1)) > 1e-6:
            raise SystemExit(f'unequal positive weights in {f}: not an unweighted set')
        sel = pos & (d['pt_pair'] > 200.0) & (np.abs(d['eta_pair']) < 1.0)
        for i in np.where(sel)[0]:
            rows.append((os.path.basename(f), int(i), d['p_qp'][i, 1:4], d['p_qm'][i, 1:4]))
            if len(rows) >= nmax:
                break
        if len(rows) >= nmax:
            break
    keys = ('gstar', 'x', 'eps_perp', 'eps_B', 'bodd_l0', 'k_B', 'c_ev', 'C_ev', 'N_osc_vac')
    q = {k: [] for k in keys}
    for _, _, p1, p2 in rows:
        t = pair_truth(p1, p2, m, lam)
        for k in keys:
            q[k].append(t[k])
    tmp = out + '.part'
    np.savez(tmp, src=np.array([r[0] for r in rows]), row=np.array([r[1] for r in rows]),
             p_qp=np.array([r[2] for r in rows]), p_qm=np.array([r[3] for r in rows]), mass=m, spin=spin, lam_keV=lam,
             **{k: np.array(v) for k, v in q.items()})
    os.replace(tmp + '.npz' if not tmp.endswith('.npz') else tmp, out)
    log.info('%d events from %d files -> %s', len(rows), len(files), out)


if __name__ == '__main__':
    main()
