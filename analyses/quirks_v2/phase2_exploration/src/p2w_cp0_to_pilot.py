"""p2w_cp0_to_pilot.py -- re-pack stored C'_0 hit rows into the pilot record layout (Cecilie, 2026-11-19).

  <tt python> p2w_cp0_to_pilot.py --src c1cp0-<topo>-NNN.npz --first I0 --n N --out /ABS/ctl.npz --ref /ABS/ref.npz [--float32]

Plan: outputs/RULE1_VALID_PLAN_cecilie_2026-11-19.md (a).  Positive control of p2t_classify.py: nothing is computed
here.  The eligible events of the C'_0 job (cp.ev 'eligible' = 1: rows cp.toyev.<g>, cp.toytru.<g> stored by v1's
run_g1b.run_cp0_job) number I0 .. I0+N-1 in file order are written as one pilot-layout file (hits, hit_off, tru, evt,
n_early_prod, meta) with stream 'ctl.cp0.<topo>', 21 road orientations, phi_road = the event's phimet, PV = the
event's PV.  The reference (v1 path, after CKF) goes to --ref: per event g, has_trial and trials.n_pass (43 rungs).
"""
import argparse
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np

log = logging.getLogger('p2w_cp0_to_pilot')
EVT_COLS = ['cls', 'phi_road', 'pv_x', 'pv_y', 'pv_z', 'ev_global']


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p2w_cp0_to_pilot %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--first', type=int, default=0)
    ap.add_argument('--n', type=int, default=0)
    ap.add_argument('--out', required=True)
    ap.add_argument('--ref', required=True)
    ap.add_argument('--float32', action='store_true')
    a = ap.parse_args()
    z = np.load(a.src, allow_pickle=False)
    cols = [str(c) for c in z['cp.ev_cols']]
    E = z['cp.ev']
    m = json.loads(str(z['meta_json']))
    topo = m['job']['topo'] if 'job' in m else m['v410']['topo']
    el = np.where(E[:, cols.index('eligible')] == 1)[0]
    take = el[a.first:a.first + a.n] if a.n else el[a.first:]
    ev0 = int(E[0, 0])
    ntr = int(z['n_trials'])
    npass = {}
    if ntr:
        tev = z['trials.ev'].astype(np.int64) + ev0
        NP = z['trials.n_pass']
        if len(set(tev.tolist())) != len(tev):
            raise SystemExit('more than one trial per event')
        npass = {int(g): NP[i] for i, g in enumerate(tev)}
    H = []; T = []; off = [0]; evt = []; ref = []; has = []
    dt = np.float32 if a.float32 else np.float64
    for r in take:
        g = int(E[r, 0])
        h = z[f'cp.toyev.{g}']; t = z[f'cp.toytru.{g}']
        if h.shape[1] != 13 or len(h) != len(t) or len(h) != int(E[r, cols.index('n_toy_all')]):
            raise SystemExit(f'event {g}: unexpected stored rows {h.shape} {t.shape}')
        H.append(h.astype(dt)); T.append(t.astype(dt)); off.append(off[-1] + len(h))
        evt.append([0, E[r, cols.index('phimet')], *E[r, cols.index('phimet') + 1:cols.index('phimet') + 4], g])
        has.append(g in npass)
        ref.append(npass.get(g, np.zeros(NP.shape[1] if ntr else 43, np.int64)))
    nev = len(take)
    meta = dict(stream=f'ctl.cp0.{topo}', chunk=f'{Path(a.src).stem}:{a.first}', n_events=nev, evt_cols=EVT_COLS,
                road_orientations=dict(n=21), source=a.src, first=a.first, float32=bool(a.float32),
                pv_cols=cols[cols.index('phimet') + 1:cols.index('phimet') + 4],
                n_eligible_in_source=int(len(el)), n_pre_in_source=int((E[:, cols.index('pre')] == 1).sum()),
                n_events_in_source=int(len(E)))
    for path, arrs in ((a.out, dict(hits=np.concatenate(H) if H else np.zeros((0, 13), dt),
                                    tru=np.concatenate(T) if T else np.zeros((0, 3), dt),
                                    hit_off=np.array(off, np.int64), evt=np.array(evt, np.float64).reshape(nev, len(EVT_COLS)),
                                    n_early_prod=np.zeros(nev, np.int64))),
                       (a.ref, dict(ev_global=np.array([e[5] for e in evt], np.int64), has_trial=np.array(has, bool),
                                    n_pass=np.array(ref, np.int64).reshape(nev, -1),
                                    cp_ev=E[take], cp_ev_cols=np.array(cols)))):
        part = Path(str(path) + '.part')
        with open(part, 'wb') as f:
            np.savez_compressed(f, meta=json.dumps(meta), **arrs)
            f.flush(); os.fsync(f.fileno())
        part.replace(path)
    log.info('%s: %d eligible events written (%d hits), %d with a v1 trial; source n_pre %d of %d', topo, nev, off[-1],
             int(np.sum(has)), meta['n_pre_in_source'], meta['n_events_in_source'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
