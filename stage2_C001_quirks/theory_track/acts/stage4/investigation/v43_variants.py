"""V4-3 W_c / t_tol variations stored in A1 (sig.var_eff, in-job def, eff_fckf, R01 and R04), central events."""
import sys
import numpy as np
from acts.stage4.analysis import common as C
from acts.stage4.code import s4sig as S
spin, m = sys.argv[1], int(sys.argv[2])
for lam in (0.6, 1, 2, 3, 5):
    tag = f"p2_{spin}_m{m}_L{lam:g}_BM"; d = C.load_npz(C.PROD / 'C1' / 'A1' / f'A1_{tag}.npz')
    cols = [str(c) for c in d['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
    P = S.Point(S.point_key(spin, m, lam))
    cen = np.array([abs(P.event(int(r))[1]['eta']) < 1 for r in d['sig.tab'][:, ci['row']]])
    V = np.unpackbits(d['sig.var_eff'], axis=-1)[..., :C.NR].astype(bool)     # (event, variant, 4, NR)
    nom = np.unpackbits(d['sig.eff_fckf'], axis=1)[:, :C.NR].astype(bool)
    names = [str(x) for x in d['sig.var_names']]
    s = f'L={lam:g} nominal(Wc75,tt30) R01 {nom[cen,0].mean():.2f} R04 {nom[cen,3].mean():.2f} | '
    s += ' '.join(f'{n}: {V[cen, i, 1, 0].mean():.2f}/{V[cen, i, 1, 3].mean():.2f}' for i, n in enumerate(names))
    print(s)
