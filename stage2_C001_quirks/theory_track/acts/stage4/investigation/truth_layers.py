"""Truth/numpy-digitised quirk hits per IP layer for chosen rows: is N_IP2 >= 7 reachable from quirk hits alone?"""
import sys, json
import numpy as np
from acts.stage4.code import s4sig as S
from acts.stage4.analysis import common as C
spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
cmpf = json.load(open(C.TT / 'data/acts_stage4/investigation' / f'cmp_p2_{spin}_m{m}_L{lam:g}_BM.json'))
P = S.Point(S.point_key(spin, m, lam)); slab = S.slab_table(1.0)
IPS = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4'] + [f'TBPS_L{k}' for k in (1, 2, 3)]
def layer_counts(row):
    h, ev = P.event(row)
    d = S.digitise(h, ev, P.m, spin, row, lam, slab)
    sid = d['meas'][:, 0].astype(int); q = d['meas'][:, 8].astype(int)
    # also: all physical hits before eff/late (truth)
    sidT = h['h_surf'].astype(int)
    out = {}; outT = {}
    for L in IPS:
        if L.startswith('TBPX'):
            subs = [L]
        else:
            subs = [L + '_in', L + '_out']
        cs = [int(np.isin(sid, [S.NAME.index(s)]).sum()) for s in subs]
        ct = [int(np.isin(sidT, [S.NAME.index(s)]).sum()) for s in subs]
        out[L] = min(cs); outT[L] = min(ct)
    nip2 = sum(v >= 2 for v in out.values()); nip2T = sum(v >= 2 for v in outT.values())
    v = d['v41']
    return nip2, nip2T, out, dict(n_late=v['n_late'], n_ineff=v['n_ineff'], n_meas=v['n_meas'])
A1 = cmpf['A1']; A2 = cmpf['A2']
common = [r for r in A2 if r in A1]
res = dict(both=[], a2only=[], a1only=[], neither_barrel=[])
rows_info = {}
for r in common:
    nip2, nip2T, per, v = layer_counts(int(r))
    rows_info[r] = (nip2, nip2T)
    a1, a2 = A1[r]['pass_'], A2[r]['pass_']
    k = 'both' if a1 and a2 else 'a2only' if a2 else 'a1only' if a1 else None
    if k: res[k].append((int(r), nip2, nip2T, per, v))
for k in ('both', 'a2only', 'a1only'):
    arr = np.array([[x[1], x[2]] for x in res[k]]) if res[k] else np.zeros((0, 2))
    print(k, len(res[k]), 'quirk-only N_IP2>=7 (digitised):', int((arr[:, 0] >= 7).sum()) if len(arr) else 0,
          ' (truth, before eff/late):', int((arr[:, 1] >= 7).sum()) if len(arr) else 0)
for x in res['a2only']:
    print(x[0], 'nip2_dig', x[1], 'nip2_truth', x[2], x[3], x[4])
eta = cmpf['eta']
cen = [r for r in common if abs(eta[r]) < 1.0]
print('central (|eta_pair|<1) common rows', len(cen), 'quirk-only N_IP2>=7 digitised:', sum(rows_info[r][0] >= 7 for r in cen),
      'truth:', sum(rows_info[r][1] >= 7 for r in cen))
print('A1 pass among central', sum(A1[r]['pass_'] for r in cen), 'A2 pass among central', sum(A2[r]['pass_'] for r in cen))
