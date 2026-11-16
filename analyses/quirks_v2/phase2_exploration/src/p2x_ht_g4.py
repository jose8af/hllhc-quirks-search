"""p2x_ht_g4.py -- half-turn study, step 2: the charged particles of chain events through Geant4, crossing by crossing,
against the hits Fatras recorded for the same particles.

  <acts python> p2x_ht_g4.py <out.json> <ht-chain file> [max_events]

Every charged row of the Fatras input (`pin`) is fired through Geant4 (g4hv option 'allx': FTFP_BERT, same geometry,
3.8 T; products are not followed) from its own production point, time and momentum.  Geant4 gives every crossing of a
sensitive surface until the particle decays, interacts, stops, leaves the tracker (r > 1200 mm, |z| > 2700 mm) or
reaches 25 ns.  Compared per particle and barrel counting surface (run_chain.BARREL_COUNT) with the written hits of
that particle (generation 0).  Turn of a crossing = transverse path / 2 pi R from its time and the initial momentum
(energy loss neglected).  Not compared: hits and crossings of secondaries made in the detector (conversion legs,
delta rays): Geant4 secondaries are not followed here, Fatras hits with generation >= 1 are not counted.
No selection quantity.
"""
import json
import sys
from pathlib import Path

import numpy as np

import p2c_common as C
import p2c_g4vtx as GV
import p2c_validate as PV
import p2x_validate as XV

log = C.setup_logging('p2x_ht_g4')
B_T = 3.8112
TURN_EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 1e9]
PT_EDGES = [0.05, 0.1, 0.2, 0.3, 0.45, 0.63, 1.0, 2.0, 1e9]
BATCH = 400_000


def run(out, f, max_events=None):
    z, m = C.load_job(f)
    H = z['hits']; ho = z['hit_off']; P = z['pin']; po = z['pin_off']
    n_ev = m['n_events'] if not max_events else min(int(max_events), m['n_events'])
    col = {k: i for i, k in enumerate(m['columns'])}; pc = {k: i for i, k in enumerate(m['pcols'])}
    layers = XV.BARREL_COUNT
    lay_of_sid = {i: layers.index(nm) for i, nm in PV.SID_NAME.items() if nm in layers}
    P = P[:po[n_ev]]
    ev_of = np.repeat(np.arange(n_ev), np.diff(po[:n_ev + 1]))
    # barcode particle number: running count per (event, vp, vsec)
    kk = np.zeros(len(P), np.int64); cnt = {}
    for r in range(len(P)):
        key = (int(ev_of[r]), int(P[r, pc['vp']]), int(P[r, pc['vsec']])); cnt[key] = cnt.get(key, 0) + 1; kk[r] = cnt[key]
    ch = np.nonzero(P[:, pc['q']] != 0)[0]
    pt = np.hypot(P[:, pc['px']], P[:, pc['py']]); pabs = np.sqrt(pt ** 2 + P[:, pc['pz']] ** 2)
    eta = np.arcsinh(P[:, pc['pz']] / np.maximum(pt, 1e-12))
    beta = pabs / np.hypot(pabs, P[:, pc['m']]); rad = pt / (0.299792458e-3 * B_T)
    # Fatras hits per (row, layer)
    nL = len(layers)
    F = np.zeros((len(P), nL), np.int32)
    rowmap = {(int(ev_of[r]), int(P[r, pc['vp']]), int(P[r, pc['vsec']]), int(kk[r])): r for r in range(len(P))}
    n_f_gen0 = 0; n_f_higher = 0; n_f_unmatched = 0
    for i in range(n_ev):
        h = H[ho[i]:ho[i + 1]]
        for sid, vp, vs, pa, ge in zip(h[:, col['sid']].astype(int), h[:, col['vp']].astype(int), h[:, col['vsec']].astype(int),
                                       h[:, col['particle']].astype(int), h[:, col['gen']].astype(int)):
            if sid not in lay_of_sid:
                continue
            if ge != 0:
                n_f_higher += 1
                continue
            r = rowmap.get((i, vp, vs, pa))
            if r is None:
                n_f_unmatched += 1
                continue
            F[r, lay_of_sid[sid]] += 1; n_f_gen0 += 1
    # Geant4 crossings per (row, layer), total and beyond half a turn; end of every particle
    geom = GV.geom_file(); names = GV.Names()
    Gc = np.zeros((len(P), nL), np.int32); Gb = np.zeros((len(P), nL), np.int32)
    hturn = np.zeros(len(TURN_EDGES) - 1); end = {}; end_turn = np.full(len(P), np.nan); end_proc = np.full(len(P), -1)
    g4cpu = 0.0
    for b0 in range(0, len(ch), BATCH):
        rows = ch[b0:b0 + BATCH]
        prim = np.c_[P[rows, pc['pdg']], P[rows, pc['x']], P[rows, pc['y']], P[rows, pc['z']], P[rows, pc['t']],
                     P[rows, pc['px']], P[rows, pc['py']], P[rows, pc['pz']], rows]
        fin = Path('prim_ht.txt'); fout = Path('vtx_ht.txt')
        with open(fin, 'w') as fh:
            for j, r in enumerate(prim):
                fh.write('%d %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n' % (j, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
        kv, _ = GV.run_g4([geom, 'FTFP_BERT', 20261116 + b0, fout, 'prim', fin, 1200.0, 'allx'])
        g4cpu += float(kv['event_cpu_s'])
        cur = None
        with open(fout) as fh:
            for ln in fh:
                c = ln[0]
                if c == 'V':
                    w = ln.split(); cur = int(rows[int(w[1])])
                    pcode = names.code(names.proc, w[2]); end_proc[cur] = pcode
                    end_turn[cur] = beta[cur] * 299.792458 * (float(w[8]) - P[cur, pc['t']]) * pt[cur] / pabs[cur] / (2 * np.pi * rad[cur])
                elif c == 'X':
                    w = ln.split()
                    if w[1] in layers:
                        L = layers.index(w[1])
                        tn = beta[cur] * 299.792458 * (float(w[5]) - P[cur, pc['t']]) * pt[cur] / pabs[cur] / (2 * np.pi * rad[cur])
                        Gc[cur, L] += 1; Gb[cur, L] += tn > 0.5
                        hturn[min(np.searchsorted(TURN_EDGES, tn, side='right') - 1, len(hturn) - 1)] += 1
        fin.unlink(); fout.unlink()
    pname = {v: k for k, v in names.proc.items()}
    c = ch
    miss = np.maximum(Gc[c] - F[c], 0); extra = np.maximum(F[c] - Gc[c], 0)
    central = np.abs(eta[c]) < 1.0; loop = pt[c] < 0.63          # 2 R < 1.1 m (outermost barrel layer) at 3.8 T
    def frac_end(mask):
        d = {}
        for code in np.unique(end_proc[c][mask]):
            d[pname.get(int(code), 'none')] = int((end_proc[c][mask] == code).sum())
        return d
    et = end_turn[c]
    res = dict(file=str(f), kind=m['kind'], n_events=n_ev, layers=layers, charged_particles=int(len(c)),
               charged_per_event=len(c) / n_ev,
               charged_central_per_event=float(central.sum() / n_ev),
               charged_central_pt_below_0p63_per_event=float((central & loop).sum() / n_ev),
               frac_central_charged_that_can_loop_inside_barrel=float((central & loop).sum() / max(central.sum(), 1)),
               fatras_hits_gen0_per_event=n_f_gen0 / n_ev, fatras_hits_higher_generation_per_event=n_f_higher / n_ev,
               fatras_hits_unmatched=n_f_unmatched, written_hits_counting_per_event=(n_f_gen0 + n_f_higher + n_f_unmatched) / n_ev,
               g4_crossings_per_event=float(Gc[c].sum() / n_ev), g4_crossings_beyond_half_turn_per_event=float(Gb[c].sum() / n_ev),
               g4_crossings_without_fatras_hit_per_event=float(miss.sum() / n_ev),
               fatras_hits_without_g4_crossing_per_event=float(extra.sum() / n_ev),
               missing_fraction_of_g4_crossings=float(miss.sum() / max(Gc[c].sum(), 1)),
               beyond_half_turn_fraction_of_g4_crossings=float(Gb[c].sum() / max(Gc[c].sum(), 1)),
               missing_relative_to_written_hits=float(miss.sum() / max(n_f_gen0 + n_f_higher + n_f_unmatched, 1)),
               by_layer=dict(g4=(Gc[c].sum(0) / n_ev).tolist(), g4_beyond_half_turn=(Gb[c].sum(0) / n_ev).tolist(),
                             fatras_gen0=(F[c].sum(0) / n_ev).tolist(), missing=(miss.sum(0) / n_ev).tolist(),
                             extra=(extra.sum(0) / n_ev).tolist()),
               g4_crossings_by_turn=dict(edges=TURN_EDGES[:-1], per_event=(hturn / n_ev).tolist()),
               by_pt=dict(edges=PT_EDGES[:-1],
                          charged_central_per_event=[float((central & (pt[c] >= a) & (pt[c] < b)).sum() / n_ev) for a, b in zip(PT_EDGES[:-1], PT_EDGES[1:])],
                          missing_per_event=[float(miss[(pt[c] >= a) & (pt[c] < b)].sum() / n_ev) for a, b in zip(PT_EDGES[:-1], PT_EDGES[1:])],
                          g4_per_event=[float(Gc[c][(pt[c] >= a) & (pt[c] < b)].sum() / n_ev) for a, b in zip(PT_EDGES[:-1], PT_EDGES[1:])]),
               end_of_central_loopers=dict(n=int((central & loop).sum()), by_process=frac_end(central & loop),
                                           ended_before_half_turn=int((central & loop & (et < 0.5)).sum()),
                                           ended_between_half_and_one_turn=int((central & loop & (et >= 0.5) & (et < 1.0)).sum()),
                                           ended_after_one_turn=int((central & loop & (et >= 1.0)).sum()),
                                           no_g4_record=int((central & loop & np.isnan(et)).sum())),
               end_of_all_charged=frac_end(np.ones(len(c), bool)),
               g4_cpu_s=g4cpu, g4_ms_per_particle=1e3 * g4cpu / max(len(c), 1), chain_s_per_event=m['mean_s_per_event'],
               note='turn from the time since production and the initial momentum; pT < 0.63 GeV: 2R < 1.1 m at 3.8112 T')
    Path(out + '.tmp').write_text(json.dumps(res, indent=1))
    Path(out + '.tmp').replace(out)
    log.info('%s', json.dumps({k: v for k, v in res.items() if k not in ('file', 'layers')}))


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
