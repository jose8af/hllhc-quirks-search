"""p2a_diag_early.py -- diagnostic (Albert, 2026-11-16): the product hits EARLIER than the Geant4 vertex time that the
hard check of p2c_validate.one counts (found in 25,000-event files of p2-c-px-b1: 6 in nix-big, 1 in nic-big).

  <acts python> p2a_diag_early.py <out.json> [own] <b1 file.npz> [...]   (own: hits earlier than their product's OWN production time)

Per offending hit: the hit (surface, time, barcode, truth radius), the vertex (time, radius, z, volume, process, parent),
the Fatras input rows of the event (inj: vsec, pdg, production point and time, momentum, beta) and the Geant4 products.
No selection quantity."""
import json
import sys
from pathlib import Path

import numpy as np

import p2c_common as C
import p2c_validate as PV

log = C.setup_logging('p2a_diag_early')


def one(path):
    z, m = C.load_job(path)
    H = z['hits']; ho = z['hit_off']; T = z['tru']; G = z['gvtx']; vc = {k: i for i, k in enumerate(m['vcols'])}
    col = {k: i for i, k in enumerate(m['columns'])}
    inj = z['inj']; io = z['inj_off']; gp = z['gprod']; gpo = z['gprod_off']
    vol = {v: k for k, v in m['surface_names'].items()}; proc = {v: k for k, v in m['proc_names'].items()}
    out = []; n_prod_hits = 0; dts = []
    for i in range(len(G)):
        h = H[ho[i]:ho[i + 1]].astype(float); t = T[ho[i]:ho[i + 1]].astype(float)
        g = G[i]
        pr = h[:, col['vsec']] >= 1
        btl = np.array([PV.SID_NAME[int(s)] == 'BTL' for s in h[:, col['sid']]], bool)
        n_prod_hits += int((pr & ~btl).sum())
        dts += list(h[pr & ~btl, col['t']] - g[vc['t']])
        P = inj[io[i]:io[i + 1]]
        if OWN:                                   # hits earlier than the production time of their own input row
            cnt = {}; tprod = {}
            for r in P:
                v = int(r[1]); cnt[v] = cnt.get(v, 0) + 1; tprod[(v, cnt[v])] = r[8]
            tp = np.array([tprod.get((int(a), int(b)), -1e9) for a, b in zip(h[:, col['vsec']], h[:, col['particle']])])
            bad = np.nonzero(pr & ~btl & (h[:, col['t']] < tp - 0.010))[0]
        else:
            bad = np.nonzero(pr & ~btl & (h[:, col['t']] < g[vc['t']] - 0.010))[0]
        if not len(bad):
            continue
        rows = []
        for r in P:
            p = float(np.sqrt(r[9] ** 2 + r[10] ** 2 + r[11] ** 2)); e = float(np.hypot(p, r[4]))
            rows.append(dict(vsec=int(r[1]), pdg=int(r[2]), q=float(r[3]), m=float(r[4]), r_prod=float(np.hypot(r[5], r[6])), z_prod=float(r[7]),
                             t_prod=float(r[8]), pt=float(np.hypot(r[9], r[10])), p=p, beta=p / max(e, 1e-12)))
        out.append(dict(event=i, vertex=dict(t=float(g[vc['t']]), r=float(np.hypot(g[vc['x']], g[vc['y']])), z=float(g[vc['z']]),
                                             vol=vol[int(g[vc['vol']])], proc=proc[int(g[vc['proc']])], parent_pdg=int(g[vc['parent_pdg']]),
                                             t0=float(g[vc['t0']]), pt0=float(np.hypot(g[vc['px0']], g[vc['py0']]))),
                        hits=[dict(surface=PV.SID_NAME[int(h[k, col['sid']])], t=float(h[k, col['t']]), dt=float(h[k, col['t']] - g[vc['t']]),
                                   vsec=int(h[k, col['vsec']]), particle=int(h[k, col['particle']]), gen=int(h[k, col['gen']]),
                                   r_truth=float(np.hypot(t[k, 0], t[k, 1])), z_truth=float(t[k, 2])) for k in bad],
                        all_hits_of_those_particles=[dict(surface=PV.SID_NAME[int(h[k, col['sid']])], t=float(h[k, col['t']]), vsec=int(h[k, col['vsec']]),
                                                          particle=int(h[k, col['particle']]), gen=int(h[k, col['gen']]),
                                                          r_truth=float(np.hypot(t[k, 0], t[k, 1])))
                                                     for k in np.nonzero(pr)[0] if (h[k, col['vsec']], h[k, col['particle']]) in
                                                     {(h[b, col['vsec']], h[b, col['particle']]) for b in bad}],
                        fatras_input=rows,
                        geant4_products=[dict(pdg=int(q[0]), p=float(np.sqrt(q[1] ** 2 + q[2] ** 2 + q[3] ** 2)), E=float(q[4]),
                                              r=float(np.hypot(q[5], q[6])), z=float(q[7]), t=float(q[8])) for q in gp[gpo[i]:gpo[i + 1]]]))
    dts = np.array(dts)
    return dict(file=str(path), n_events=int(len(G)), n_product_hits=n_prod_hits, n_early=sum(len(o['hits']) for o in out),
                dt_quantiles_ns=[float(x) for x in np.quantile(dts, (0, 1e-5, 1e-4, 1e-3, 0.01, 0.5))] if len(dts) else None,
                n_dt_below={str(c): int((dts < c).sum()) for c in (-1.0, -0.1, -0.03, -0.01, -0.003, 0.0)}, events=out)


OWN = False

if __name__ == '__main__':
    OWN = sys.argv[2] == 'own'
    res = [one(f) for f in sys.argv[2:] if f != 'own']
    Path(sys.argv[1] + '.tmp').write_text(json.dumps(res, indent=1)); Path(sys.argv[1] + '.tmp').replace(sys.argv[1])
    for r in res:
        log.info('%s', json.dumps({k: v for k, v in r.items() if k != 'events'}))
