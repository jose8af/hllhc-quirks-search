"""sep_IT^det as computed (all band hits of the record) vs restricted to the CORE hits, for matched candidates passing
R04 (A2 production hit records, E500 and E200), vs the Stage-3 truth median sep_IT."""
import sys, json
import numpy as np
from acts.stage4.analysis import common as C, hitrec as HR, products as PD
spin, m = sys.argv[1], int(sys.argv[2])
truth = json.loads(PD.P2.read_text()).get('sep_IT_handle', {})
t = truth.get(f'{spin}_m{m}', {})
tl = dict(zip(t.get('lam_keV', []), t.get('sep_IT_med_um', [])))
vals = {}
for p in sorted((C.PROD / 'C1' / 'A2').glob(f'A2_{spin}{m}_*.npz')):
    d = C.load_npz(p)
    lk = HR.cand_lookup(d)
    trl = {}
    tab = d['sig.tab']; cols = [str(c) for c in d['sig.cols']]; ci = {c: i for i, c in enumerate(cols)}
    for e in range(len(tab)):
        if d['sig.trial'][e] >= 0: trl[int(d['sig.trial'][e])] = float(tab[e, ci['lam']])
    Fc = C.rung_flags(d['cand.rungs'])
    seen = set()
    for k, tr, cidx, h in HR.iter_records(d):
        if tr in seen or tr not in trl: continue
        i = lk[(tr, cidx)]
        if not Fc[i][3]: continue
        pv = d['trials.pv'][tr]
        g = HR.geom(d, h, pv, d['cand.normal'][i], d['cand.axis'][i]); cm, c, w = HR.core(g)
        mt = HR.signal_match(d, h, g, cm)[0]
        if not mt: continue
        seen.add(tr)
        s_all = HR.sep_it(g, c)
        gc = {kk: (vv[cm] if hasattr(vv, '__len__') and len(vv) == len(cm) else vv) for kk, vv in g.items()}
        s_core = HR.sep_it(gc, c)
        q = (d['hit.INT'][h].astype(np.int64) % 1_000_000) == 4000
        gq = {kk: (vv[q] if hasattr(vv, '__len__') and len(vv) == len(q) else vv) for kk, vv in g.items()}
        s_q = HR.sep_it(gq, np.median(gq['wv'][gq['ip']]) if gq['ip'].any() else np.nan)
        vals.setdefault(trl[tr], []).append((s_all, s_core, s_q))
for lam in sorted(vals):
    a = np.array(vals[lam], float)
    print(f'L={lam:g}: n={len(a)} median sep_IT^det all-band {np.nanmedian(a[:,0]):.2f} mm | core-only {np.nanmedian(a[:,1]):.2f} mm | '
          f'quirk-only (truth-labelled, diagnostic) {np.nanmedian(a[:,2]):.2f} mm | truth {tl.get(lam, np.nan)/1e3 if lam in tl else float("nan"):.2f} mm')
