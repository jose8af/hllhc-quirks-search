"""p2x_diag_turns.py -- how far along their helix generated particles leave hits in the chain (Fatras), from a
p2x_hs0 file: number of turns (transverse path / 2 pi R) of every written hit of a generation-0 charged particle,
from the hit time, the particle's production time and its generated momentum.  Diagnostic of the finding that the
Fatras parent of the B1 slices has no hit beyond half a turn (p2-c-px-a1d).  No selection quantity.

  <acts python> p2x_diag_turns.py <out.json> <hs0x file> [...]
"""
import json
import sys
from pathlib import Path

import numpy as np

import p2c_common as C
import p2c_validate as PV
import p2x_validate as XV

log = C.setup_logging('p2x_diag_turns')
MASS = {11: 0.51099895e-3, 13: 0.1056583755, 211: 0.13957039, 321: 0.493677, 2212: 0.93827209}     # s4cp.py l.33 / p2c_handover.MASS
B_T = 3.8112
EDGES = [0.0, 0.25, 0.4, 0.45, 0.5, 0.55, 0.75, 1.0, 2.0, 1e9]


def one(path):
    z, m = C.load_job(path)
    H = z['hits']; ho = z['hit_off']; P = z['part']; po = z['part_off']
    col = {k: i for i, k in enumerate(m['columns'])}; pc = {k: i for i, k in enumerate(m['part_cols'])}
    cnt_sid = np.array(sorted(i for i, nm in PV.SID_NAME.items() if nm in XV.BARREL_COUNT))
    hist = np.zeros(len(EDGES) - 1); hist_soft = np.zeros(len(EDGES) - 1); mx = 0.0; n_soft_part = 0; n_part = 0
    for i in range(m['n_events']):
        h = H[ho[i]:ho[i + 1]]; p = P[po[i]:po[i + 1]]
        if not len(h) or not len(p):
            continue
        key_p = p[:, pc['vsec']].astype(np.int64) * 100000 + p[:, pc['particle']].astype(np.int64)
        ok = (h[:, col['gen']] == 0) & np.isin(h[:, col['sid']].astype(int), cnt_sid)
        h = h[ok]
        key_h = h[:, col['vsec']].astype(np.int64) * 100000 + h[:, col['particle']].astype(np.int64)
        order = np.argsort(key_p); pos = np.searchsorted(key_p[order], key_h)
        pos = np.clip(pos, 0, len(order) - 1); row = order[pos]
        good = key_p[row] == key_h
        r = p[row[good]]; hh = h[good]
        apdg = np.abs(r[:, pc['pdg']]).astype(int)
        mass = np.array([MASS.get(int(a), np.nan) for a in apdg])
        sel = np.isfinite(mass) & (r[:, pc['q']] != 0)
        r = r[sel]; hh = hh[sel]; mass = mass[sel]
        pt = r[:, pc['pt']].astype(float); pabs = pt * np.cosh(r[:, pc['eta']].astype(float))
        beta = pabs / np.hypot(pabs, mass); rad = pt / (0.299792458e-3 * B_T)
        turns = beta * 299.792458 * (hh[:, col['t']] - r[:, pc['t']]) * pt / pabs / (2 * np.pi * rad)
        hist += np.histogram(turns, EDGES)[0]
        soft = pt < 0.6
        hist_soft += np.histogram(turns[soft], EDGES)[0]
        mx = max(mx, float(turns.max()) if len(turns) else 0.0)
        ps = p[(p[:, pc['q']] != 0)]
        n_part += len(ps); n_soft_part += int((ps[:, pc['pt']] < 0.6).sum())
    return dict(file=str(path), n_events=m['n_events'], turn_edges=EDGES[:-1], hits_by_turn=hist.tolist(),
                hits_by_turn_pt_below_0p6=hist_soft.tolist(), max_turn=mx, charged_particles_with_hits=n_part,
                of_which_pt_below_0p6=n_soft_part,
                note='energy loss is neglected in the turn estimate (it slightly overestimates the turn of a slowed particle)')


if __name__ == '__main__':
    res = [one(f) for f in sys.argv[2:]]
    Path(sys.argv[1] + '.tmp').write_text(json.dumps(res, indent=1))
    Path(sys.argv[1] + '.tmp').replace(sys.argv[1])
    for r in res:
        log.info('%s', json.dumps({k: v for k, v in r.items() if k != 'file'}))
