"""stitch_trg.py -- build the unbiased trigger-region samples <P>-TRGS_m<m>.npz = <P>-TRG (ME cut pT(QQ)_ME >= 100 GeV,
high statistics) U <P>-INC restricted to pT(QQ)_ME < 100 GeV (the complement of the generation cut), weights unchanged.
Why: MLM matches jets to partons by angle, so hard shower emissions can sit on a soft ME jet; at m = 500 GeV 7.1 +- 0.4 %
of the matched sigma(pT(QQ) > 200 GeV after the shower) has pT(QQ)_ME < 100 GeV (VALIDATION §4.4).  The generation cut
itself closes exactly: sigma_TRG(pT>200) = sigma_INC(pT>200, pT_ME >= 100) within MC stat.  So TRG U INC[pT_ME<100] is the
full MLM prediction with TRG statistics where it matters.  Column 'origin' = 0 (TRG) / 1 (INC complement).
ROW ORDER (review S2-R1 A1/A-1, fixer 2026-10-11): the stitched rows are written in a deterministic random order
(numpy default_rng(SHUFFLE_SEED + m + (0 for E, 100000 for S)).permutation), stored as 'shuffle_seed' and as 'row_src'
(index of the row in the unshuffled TRG-then-INC concatenation), so ANY prefix of the file is a fair sample.  The weights
are NOT equal: the INC rows carry 3.7-9.6x the TRG per-event weight -> always use w (mg_events.iter_events returns it) or the
loader's deterministic unweighting (iter_events(..., unweight=True)).
Metadata: kind = 'stitched', nlhe = nlhe_trg + nlhe_inc (C-10; the weights are NOT N_LHE-averaged across the two pieces),
sigma_ref_fb = INC sigma_matched (denominator for fractions; mg_events.sigma_norm_fb).  sigma_lhe_fb is not defined for a
stitched file (two LHE samples): use sigma_lhe_fb_trg / sigma_lhe_fb_inc.
Also re-points the loader aliases in ../data/sim/SAMPLES_INDEX.json: '{spin}_{m}_trig' -> TRGS, '{spin}_{m}_trig_mecut' -> TRG.
Run: pixi run -e ana python scripts/stitch_trg.py"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data', 'sim'))
CUT = 100.0
SHUFFLE_SEED = 20261011


def main():
    idxp = os.path.join(DATA, 'SAMPLES_INDEX.json')
    idx = json.load(open(idxp))
    for pre, spin in (('E', 'F'), ('S', 'S')):
        for m in range(200, 1600, 100):
            fi = os.path.join(DATA, 'npz', f'{pre}-INC_m{m}.npz'); ft = os.path.join(DATA, 'npz', f'{pre}-TRG_m{m}.npz')
            if not (os.path.exists(fi) and os.path.exists(ft)):
                continue
            ci = dict(np.load(fi, allow_pickle=False)); ct = dict(np.load(ft, allow_pickle=False))
            assert list(ci['wvar_names']) == list(ct['wvar_names'])
            H = ci['p_qq_hard']; pth = np.hypot(H[:, 1], H[:, 2])
            comp = pth < CUT
            n = len(ct['w'])
            out = {}
            for k, v in ct.items():
                if hasattr(v, 'shape') and v.ndim >= 1 and len(v) == n and k != 'wvar_names':
                    out[k] = np.concatenate([v, ci[k][comp]])
            out['origin'] = np.concatenate([np.zeros(n, np.int8), np.ones(comp.sum(), np.int8)])
            seed = SHUFFLE_SEED + m + (0 if pre == 'E' else 100000)
            perm = np.random.default_rng(seed).permutation(len(out['w']))
            for k in list(out):
                out[k] = out[k][perm]
            out['row_src'] = perm.astype(np.int32)
            out['shuffle_seed'] = seed
            for k in ('wvar_names', 'mq', 'spin', 'merging_nominal', 'n_ic_included'):
                out[k] = ct[k]
            out['nlhe_trg'] = ct['nlhe']; out['nlhe_inc'] = ci['nlhe']; out['me_cut'] = CUT
            out['nlhe'] = int(ct['nlhe']) + int(ci['nlhe']); out['kind'] = 'stitched'
            out['sigma_lhe_fb_trg'] = ct['sigma_lhe_fb']; out['sigma_lhe_fb_inc'] = ci['sigma_lhe_fb']
            out['sigma_ref_fb'] = float(ci['w'].sum())
            out['source_ids'] = np.array([f'{pre}-TRG', f'{pre}-INC'])
            dst = os.path.join(DATA, 'npz', f'{pre}-TRGS_m{m}.npz')
            np.savez_compressed(dst, **out)
            pt = out['pt_pair']; w = out['w']
            s_st = w[pt > 200].sum(); s_inc = ci['w'][ci['pt_pair'] > 200].sum()
            print(f'{pre} m={m}: TRGS {len(w)} ev ({comp.sum()} from INC), sigma(pT>200) stitched {s_st:.5g} vs INC {s_inc:.5g} fb; '
                  f'shuffle seed {seed}')
            idx[f'{spin}_{m}_TRGS'] = os.path.relpath(dst, DATA)
            idx[f'{spin}_{m}_trig'] = os.path.relpath(dst, DATA)
            idx[f'{spin}_{m}_trig_mecut'] = os.path.relpath(ft, DATA)
    import sys
    if '--no-index' not in sys.argv:
        json.dump(idx, open(idxp, 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
