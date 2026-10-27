"""Why no seed?  numpy replica of the seeds_fast (a in TBPX L4, b in L3) pre-cuts on a re-run A1 event."""
import sys, json
import numpy as np
from acts.stage4 import run_g1b as RG, run_stage4 as RS
from acts.stage4.finder import g1b_tt as GT, finder as FF
from acts.stage4.code import s4sig as S
spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]); want = [int(x) for x in sys.argv[4].split(',')]
name = sys.argv[5] if len(sys.argv) > 5 else f'inv_A1_{spin}{m}_L{lam:g}'
OUT = RS.TT / 'data/acts_stage4/investigation'
rows = json.loads((OUT / f'{name}.rows.json').read_text()); z = np.load(OUT / f'{name}.chain.npz')
P = S.Point(S.point_key(spin, m, lam))
fz = RS.frozen_inputs(); cfg, wcfg = RS.finder_configs(fz, dict(campaign='C1'), False)
print('cfg', cfg.road, cfg.w_c, cfg.t_tol, cfg.tseed)
for ie, row in enumerate(rows):
    if row not in want: continue
    h, ev, met_true, pv, phimet, tseed = RG.sig_event_inputs(S, P, row, spin, P.m)
    Pp = GT.assemble(z[f'ev{ie}'], z[f'tru{ie}'], 0, np.random.default_rng(0), inserted_vp=(GT.SIG_VP,), do_topup=False)
    H = Pp['H']; sid = Pp['sid']
    mroad, U0 = FF.road_select(H, sid, pv, phimet, cfg)
    U = U0[mroad]; sd = sid[mroad]
    L4 = np.where(sd == FF.SID['TBPX_L4'])[0]; L3 = np.where(sd == FF.SID['TBPX_L3'])[0]; L2 = np.where(sd == FF.SID['TBPX_L2'])[0]
    phi = np.arctan2(U[:, 1], U[:, 0]); eta = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    allq = (Pp['INT'] % 1_000_000 == 4000)
    print(f'row {row} eta {ev["eta"]:+.2f}: pool {len(H)} road {mroad.sum()} (L4 {len(L4)}, L3 {len(L3)}, L2 {len(L2)}); '
          f'quirk pool hits by layer:', {k: int(np.sum(FF.LC_OF[sid[allq]] == i)) for i, k in enumerate(FF.LAYERS[:4])},
          'dphi(hit,MET) of L4 hits:', np.round(np.abs((np.arctan2(U0[sid == FF.SID['TBPX_L4'], 1], U0[sid == FF.SID['TBPX_L4'], 0]) - phimet + np.pi) % (2*np.pi) - np.pi), 3))
    for a in L4:
        for b in L3:
            ua, ub = U[a], U[b]
            sn = np.linalg.norm(np.cross(ua, ub)) / (np.linalg.norm(ua) * np.linalg.norm(ub))
            dph = abs((phi[a] - phi[b] + np.pi) % (2 * np.pi) - np.pi); de = abs(eta[a] - eta[b])
            nrm = np.cross(ua, ub); nrm /= np.linalg.norm(nrm)
            dc = [abs(U[c] @ nrm) for c in L2]
            print(f'   a{a} b{b}  dphi {dph:.4f} deta {de:.4f} sin {sn:.2e} {"<1e-3 REJECT" if sn < 1e-3 else ""} '
                  f' |d_c| L2 (mm): {np.round(dc, 3)}  q-particle a/b {int(H[mroad][a, 8])}/{int(H[mroad][b, 8])}')
