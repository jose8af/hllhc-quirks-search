"""p2x_diag_lp.py -- two loose ends of the looper gun: (1) which particles have no Geant4 record, (2) where the SimHit
without a measurement lies.   <acts python> p2x_diag_lp.py <out.json> <truth of an old job> <truth of the rerun>"""
import json
import sys
from pathlib import Path

import numpy as np

import p2c_common as C
import p2c_validate as PV

sys.path.insert(0, str(C.CODE))
import s4geo  # noqa: E402

a = np.load(sys.argv[2]); b = np.load(sys.argv[3])
c = {k: i for i, k in enumerate([str(x) for x in a['cols']])}
pa = json.loads(str(a['proc'])); none = a['truth'][:, c['end_proc']] == pa.get('none', -1)
X = a['truth']
res = dict(old=dict(n=int(len(X)), n_no_record=int(none.sum()),
                    pdg_of_no_record={str(int(k)): int(v) for k, v in zip(*np.unique(X[none, c['pdg']].astype(int), return_counts=True))},
                    pdg_all={str(int(k)): int(v) for k, v in zip(*np.unique(X[:, c['pdg']].astype(int), return_counts=True))},
                    pt_q_no_record=[float(x) for x in np.quantile(X[none, c['pt']], (0.1, 0.5, 0.9))] if none.any() else None))
pb = json.loads(str(b['proc'])); Y = b['truth']; inv = {v: k for k, v in pb.items()}
res['rerun'] = dict(n=int(len(Y)), end_process={inv[int(k)]: int(v) for k, v in zip(*np.unique(Y[:, c['end_proc']].astype(int), return_counts=True))},
                    crossings_of_formerly_unrecorded=float(Y[none, c['n_cross_counting']].mean()) if none.any() else None,
                    max_layer_multiplicity_of_formerly_unrecorded=int(b['layer_cross'][none].max()) if none.any() else None,
                    same_events=bool(np.array_equal(X[:, c['pt']], Y[:, c['pt']])))
L = b['lost']; rows = []
surf = {i: s for i, s in enumerate(PV.SURF)}
for r in L:
    sid = int(r[1]); s = surf.get(sid, {})
    phi = float(np.arctan2(r[6], r[5])); w = 2 * np.pi / 32
    rows.append(dict(event=int(r[0]), sid=sid, name=s.get('name'), x=float(r[5]), y=float(r[6]), z=float(r[7]), r=float(np.hypot(r[5], r[6])),
                     phi=phi, phi_distance_to_nearest_sector_edge_rad=float(min(phi % w, w - phi % w)),
                     rphi_distance_to_sector_edge_mm=float(min(phi % w, w - phi % w) * np.hypot(r[5], r[6])),
                     surface=dict((k, s.get(k)) for k in ('type', 'p0', 'p1', 'p2', 'kind')),
                     particle=dict(pdg=int(Y[int(r[0]), c['pdg']]), pt=float(Y[int(r[0]), c['pt']]), eta=float(Y[int(r[0]), c['eta']]))))
res['lost_simhits'] = rows
Path(sys.argv[1]).write_text(json.dumps(res, indent=1))
sys.stderr.write(json.dumps(res)[:3000] + '\n')
