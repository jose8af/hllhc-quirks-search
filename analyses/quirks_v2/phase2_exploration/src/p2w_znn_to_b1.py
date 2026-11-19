"""p2w_znn_to_b1.py -- re-pack the w > 0 events of Z(nunu) pilot files as B1-layout files (Cecilie, 2026-11-19).

  <tt python> p2w_znn_to_b1.py --files a.npz,b.npz --outdir /ABS/DIR      -> /ABS/DIR/b1_<k>.npz, one per input

Plan addendum (a2) of outputs/RULE1_VALID_PLAN_cecilie_2026-11-19.md: injection control of the non-Z branch of
p2t_classify.py.  Rows are copied unchanged (dtype kept); evt (float64) = cls 0, phi_road = phimet_reco_v1, PV = stored
vertex + the N(0, (10, 10, 15) um) draw of p2t_classify.py's Z branch (same seed string), src_event, w_v1.
"""
import argparse
import hashlib
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np

log = logging.getLogger('p2w_znn_to_b1')
PV_SIGMA = np.array([0.010, 0.010, 0.015])          # mm; as p2t_classify.py (checked there against v1 g1b_tt)
EVT_COLS = ['cls', 'phi_road', 'pv_x', 'pv_y', 'pv_z', 'src_event', 'w_v1']


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p2w_znn_to_b1 %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', required=True)
    ap.add_argument('--outdir', required=True)
    a = ap.parse_args()
    for k, path in enumerate(a.files.split(',')):
        z = np.load(path)
        meta = json.loads(str(z['meta']))
        if meta['stream'] != 'pilot.hs0.znn':
            raise SystemExit(f'{path}: not a Z(nunu) pilot file')
        ec = meta['evt_cols']; evt = z['evt']; off = z['hit_off']; hits = z['hits']; tru = z['tru']
        w = evt[:, ec.index('w_v1')]
        vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
        H = []; T = []; o = [0]; E = []
        for i in np.where(w > 0)[0]:
            h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
            pv = vtx[i] + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
            s = slice(int(off[i]), int(off[i + 1]))
            H.append(hits[s]); T.append(tru[s]); o.append(o[-1] + len(H[-1]))
            E.append([0.0, float(evt[i, ec.index('phimet_reco_v1')]), *pv, i, float(w[i])])
        m = dict(stream='ctl.znn.b1', chunk=meta['chunk'], n_events=len(E), evt_cols=EVT_COLS, road_orientations=dict(n=21),
                 source=path)
        out = Path(a.outdir) / f'b1_{k}.npz'
        part = Path(str(out) + '.part')
        with open(part, 'wb') as f:
            np.savez(f, meta=json.dumps(m), hits=np.concatenate(H), tru=np.concatenate(T), hit_off=np.array(o, np.int64),
                     evt=np.array(E, np.float64), n_early_prod=np.zeros(len(E), np.int64))
            f.flush(); os.fsync(f.fileno())
        part.replace(out)
        log.info('%s: %d of %d events written', Path(path).name, len(E), len(w))
    return 0


if __name__ == '__main__':
    sys.exit(main())
