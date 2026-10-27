"""R2 c1: independent check of the TRGS stitching / shuffling and first-N composition.
For each TRGS file: (1) rows = permutation of TRG ++ INC[pT_ME<100] (row_src, seed reproducible);
(2) sum w = INC sigma_matched; (3) first-N (tail: w>0, pT>200, |eta|<2.5) INC share of w and count vs full file,
with binomial/bootstrap errors; position of the first INC tail row; (4) unweighting efficiency and determinism."""
import os, sys
import numpy as np
D = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/data/sim/npz'
sys.path.insert(0, '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/scripts')
import mg_events as M

def wmed(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); return float(x[i][np.searchsorted(c, c[-1] / 2)])

rng = np.random.default_rng(99)
pts = [('E', m) for m in range(200, 1600, 100)] + [('S', m) for m in (200, 500, 1000)]
worst = 0
for pre, m in pts:
    s = dict(np.load(f'{D}/{pre}-TRGS_m{m}.npz')); t = dict(np.load(f'{D}/{pre}-TRG_m{m}.npz')); i = dict(np.load(f'{D}/{pre}-INC_m{m}.npz'))
    H = i['p_qq_hard']; comp = np.hypot(H[:, 1], H[:, 2]) < 100
    cat_w = np.concatenate([t['w'], i['w'][comp]]); cat_px = np.concatenate([t['p_qp'][:, 1], i['p_qp'][comp, 1]])
    seed = 20261011 + m + (0 if pre == 'E' else 100000)
    perm = np.random.default_rng(seed).permutation(len(cat_w))
    ok_perm = np.array_equal(perm, s['row_src']) and np.array_equal(cat_w[perm], s['w']) and np.array_equal(cat_px[perm], s['p_qp'][:, 1])
    ok_orig = np.array_equal(s['origin'], (perm >= len(t['w'])).astype(np.int8))
    sumw = s['w'].sum(); sinc = i['w'].sum()
    sel = (s['w'] > 0) & (s['pt_pair'] > 200) & (np.abs(s['eta_pair']) < 2.5)
    W = s['w'][sel]; O = s['origin'][sel]; X = 2 * (s['gamma_star'][sel] - 1)
    share = W[O == 1].sum() / W.sum(); first_inc = int(np.argmax(O == 1))
    neff = W.sum() ** 2 / (W ** 2).sum()
    ratio = W[O == 1].mean() / W[O == 0].mean()
    line = (f'{pre}{m:5d}: perm_ok={ok_perm} origin_ok={ok_orig} sumw/sigINC-1={sumw/sinc-1:+.1e} ntail={len(W)} '
            f'INCshare(w)={100*share:.2f}% wINC/wTRG={ratio:.2f} Neff={neff:.0f} first_INC_pos={first_inc}')
    for n in (500, 2000, 5000):
        if n > len(W):
            continue
        sh = W[:n][O[:n] == 1].sum() / W[:n].sum()
        bs = np.std([(lambda ix: W[ix][O[ix] == 1].sum() / W[ix].sum())(rng.integers(0, len(W), n)) for _ in range(300)])
        pull = (sh - share) / bs; worst = max(worst, abs(pull))
        line += f' | N{n}: share {100*sh:.2f}% pull {pull:+.2f}'
    acc, wmax = M.unweight_mask(s, 12345); acc2, _ = M.unweight_mask(s, 12345)
    eff_tail = acc[sel].sum() / sel.sum(); eff_all = acc.sum() / (s['w'] > 0).sum()
    # unbiasedness: count-share of INC among accepted tail rows vs weight share
    Oa = s['origin'][sel & acc]
    line += f' | unw: det={np.array_equal(acc, acc2)} eff_all={100*eff_all:.1f}% eff_tail={100*eff_tail:.1f}% INCcount={100*Oa.mean():.2f}%'
    print(line, flush=True)
print('worst |pull| of first-N share:', round(worst, 2))
