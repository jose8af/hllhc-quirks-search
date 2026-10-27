"""Why does the A1 no-trial count rise with Lambda? Rows with 0 written barrel quirk hits: eta, late, ineff."""
import sys
import numpy as np
from acts.stage4.analysis import common as C
from acts.stage4.code import s4sig as S
spin, m = sys.argv[1], int(sys.argv[2])
slab = S.slab_table(1.0)
for lam in [float(x) for x in sys.argv[3].split(',')]:
    tag = f"p2_{spin}_m{m}_L{lam:g}_BM"
    d = C.load_npz(C.PROD / 'C1' / 'A1' / f'A1_{tag}.npz', keys=['sig.tab', 'sig.cols', 'sig.trial'])
    cols = [str(c) for c in d['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
    tab = d['sig.tab']; P = S.Point(S.point_key(spin, m, lam))
    sk = d['sig.trial'] < 0
    eta = np.array([P.event(int(r))[1]['eta'] for r in tab[:, ci['row']]])
    nqw = tab[:, ci['n_q_written']]
    late = []; written_surf = []; nall = []; tmax = []
    for r in tab[sk, ci['row']]:
        h, ev = P.event(int(r)); dg = S.digitise(h, ev, P.m, spin, int(r), lam, slab)
        v = dg['v41']; late.append(v['n_late']); written_surf.append(v['n_barrel_written_surfaces']); nall.append(v['n_hits'])
    late = np.array(late); ws = np.array(written_surf)
    cen = np.abs(eta) < 1
    print(f"L={lam:g}: N {len(tab)} no_trial {sk.sum()} | central(|eta|<1) {cen.sum()} no_trial_central {(sk & cen).sum()} | "
          f"no_trial rows: median |eta| {np.median(np.abs(eta[sk])):.2f}, with barrel-surface truth hits {np.sum(ws > 0)}, "
          f"all those late(>25ns) {np.sum((ws > 0) & (late == ws))}, partly late {np.sum((late > 0) & (late < ws))}")
