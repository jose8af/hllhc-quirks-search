"""p2x_diag_a1.py -- where along the parent's path Fatras parent hits are missing with respect to the Geant4 parent
crossings (review of addendum v2, A-1; diagnostic of slice p2-c-px-tr).

  <acts python> p2x_diag_a1.py <out.json> <b1x file> [...]

Per file, over the events with a charged parent: counting-surface crossings of the Geant4 parent before the vertex and
written Fatras parent hits, both binned in the number of turns of the parent at that time (transverse path / 2 pi R,
from the time since the origin and the initial momentum; R = pT / (0.29979e-3 B)); the turn at which the Fatras
parent's hits end against the turn of the vertex.  No selection quantity.
"""
import json
import sys
from pathlib import Path

import numpy as np

import p2c_common as C
import p2c_validate as PV
import p2x_validate as XV

log = C.setup_logging('p2x_diag_a1')
MASS = {211: 0.13957039, 321: 0.493677, 2212: 0.93827209}          # s4cp.py l.33-34 (as p2c_g4vtx.MASS)
B_T = 3.8112
EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 1e9]


def one(path):
    z, m = C.load_job(path)
    H = z['hits']; ho = z['hit_off']; ev = z['evt']; G = z['gvtx']; gc = z['gcross']; gco = z['gcross_off']
    vc = {k: i for i, k in enumerate(m['vcols'])}; col = {k: i for i, k in enumerate(m['columns'])}
    code_name = {v: k for k, v in m['surface_names'].items()}
    cnt_sid = {i for i, nm in PV.SID_NAME.items() if nm in XV.BARREL_COUNT}
    cnt_code = {c for c, nm in code_name.items() if nm in XV.BARREL_COUNT}
    hg = np.zeros(len(EDGES) - 1); hf = np.zeros(len(EDGES) - 1)
    nev = 0; n_nohit = 0; tv = []; tl = []; n_end_early = 0; ng_ev = []; nf_ev = []
    for i in range(len(ev)):
        if ev[i, 8] <= 0:
            continue
        nev += 1
        g = G[i]
        pt = np.hypot(g[vc['px0']], g[vc['py0']]); p = np.sqrt(pt ** 2 + g[vc['pz0']] ** 2)
        mass = MASS.get(abs(int(g[vc['parent_pdg']])), 0.13957039)
        beta = p / np.hypot(p, mass); rad = pt / (0.299792458e-3 * B_T)
        turns = lambda t: beta * 299.792458 * (t - g[vc['t0']]) * pt / p / (2 * np.pi * rad)  # noqa: E731
        h = H[ho[i]:ho[i + 1]]
        par = (h[:, col['vsec']] == 0) & (h[:, col['gen']] == 0) & (h[:, col['particle']] == 1)
        par &= np.isin(h[:, col['sid']].astype(int), list(cnt_sid))
        tf = turns(h[par, col['t']].astype(float))
        X = gc[gco[i]:gco[i + 1]]
        X = X[np.isin(X[:, 0].astype(int), list(cnt_code))]
        tg = turns(X[:, 4].astype(float))
        hg += np.histogram(tg, EDGES)[0]; hf += np.histogram(tf, EDGES)[0]
        ng_ev.append(len(tg)); nf_ev.append(len(tf))
        v = float(turns(g[vc['t']])); tv.append(v)
        last = float(tf.max()) if len(tf) else 0.0
        tl.append(last)
        n_nohit += len(tf) == 0
        n_end_early += bool(len(tg) and last < float(tg.max()) - 0.1)
    tv = np.array(tv); tl = np.array(tl)
    q = lambda a: [float(x) for x in np.quantile(a, (0.1, 0.5, 0.9, 0.99))] if len(a) else None  # noqa: E731
    return dict(file=str(path), sample=m['sample'], trunc_mode=m.get('trunc_mode'), events_charged_parent=nev,
                turn_edges=EDGES[:-1], g4_crossings_by_turn=hg.tolist(), fatras_parent_hits_by_turn=hf.tolist(),
                ratio_fatras_over_g4=[float(a / b) if b else None for a, b in zip(hf, hg)],
                events_without_fatras_parent_hit=int(n_nohit),
                events_fatras_ends_0p1_turn_before_last_g4_crossing=int(n_end_early),
                vertex_turn_q10_q50_q90_q99=q(tv), last_fatras_hit_turn_q10_q50_q90_q99=q(tl),
                max_last_fatras_hit_turn=float(tl.max()) if len(tl) else None,
                g4_crossings_per_event=float(np.mean(ng_ev)), fatras_hits_per_event=float(np.mean(nf_ev)))


if __name__ == '__main__':
    res = [one(f) for f in sys.argv[2:]]
    Path(sys.argv[1] + '.tmp').write_text(json.dumps(res, indent=1))
    Path(sys.argv[1] + '.tmp').replace(sys.argv[1])
    for r in res:
        log.info('%s', json.dumps({k: v for k, v in r.items() if k != 'file'}))
