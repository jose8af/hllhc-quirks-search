"""fix_unmatched_named_weights.py -- one-off repair (E4, 2026-10-11) of unmatched (LOPS) npz files converted before the
converter fix: the named '..._MERGING=0.000' weight columns were left in the interface's sigma/N_job normalisation.
Per event, all named columns are multiplied by Weight / Weight_MERGING=0.000 (no MLM veto in unmatched samples, so this
ratio is the pure normalisation factor).  Idempotent (skips files whose ratio is already 1).
Usage: pixi run -e ana python scripts/fix_unmatched_named_weights.py <npz> [...]"""
import sys
import numpy as np
for f in sys.argv[1:]:
    c = dict(np.load(f, allow_pickle=False))
    names = [str(x) for x in c['wvar_names']]
    if str(c['merging_nominal']) != 'None':
        print('skip (matched)', f); continue
    W = c['wvar']; i0 = names.index('Weight'); i1 = names.index('Weight_MERGING=0.000')
    r = W[:, i0] / W[:, i1]
    if np.allclose(r, 1):
        print('already fixed', f); continue
    named = np.array(['_MERGING=' in n for n in names])
    W[:, named] *= r[:, None]
    c['wvar'] = W; c['merged_col_factor_fix'] = float(np.median(r))
    np.savez_compressed(f, **c)
    print('fixed', f, 'median factor', np.median(r))
