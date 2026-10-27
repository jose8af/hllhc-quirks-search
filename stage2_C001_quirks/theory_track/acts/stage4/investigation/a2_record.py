"""A2 production hit record of the matched candidate for chosen rows: per-surface quirk vs non-quirk core hits."""
import sys
import numpy as np
from acts.stage4.analysis import common as C, hitrec as HR
from acts.stage4.code import s4sig as S
spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
rows = [int(x) for x in sys.argv[4].split(',')]
for p in sorted((C.PROD / 'C1' / 'A2').glob(f'A2_{spin}{m}_*.npz')):
    d = C.load_npz(p)
    tab = d['sig.tab']; cols = [str(c) for c in d['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
    for e in range(len(tab)):
        r = int(tab[e, ci['row']]); l = tab[e, ci['lam']]
        if r not in rows or abs(l - lam) > 1e-6: continue
        ti = int(d['sig.trial'][e]); lk = HR.cand_lookup(d)
        for k, tr, cidx, h in HR.iter_records(d):
            if tr != ti: continue
            i = lk[(tr, cidx)]; pv = d['trials.pv'][tr]
            g = HR.geom(d, h, pv, d['cand.normal'][i], d['cand.axis'][i]); cm, c, w = HR.core(g)
            mt, nc, nq, nl = HR.signal_match(d, h, g, cm)
            if not mt: continue
            q = (d['hit.INT'][h].astype(np.int64) % 1_000_000) == 4000
            per = {}
            for s_, qq, cc in zip(d['hit.sid'][h], q, cm):
                nm = S.NAME[int(s_)]
                if 'TB2S' in nm: continue
                per.setdefault(nm, [0, 0, 0, 0])[(0 if qq else 1) + (0 if cc else 2)] += 1
            print(r, f'cand {cidx} w_core {w:.2f} nip2 {int(d["cand.nip2"][i])} n_core {nc} nq_core {nq}  [q_core, pu_core, q_out, pu_out]:')
            print('   ', dict(sorted(per.items())))
            break
