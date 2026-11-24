"""B2-a remediation 1 (control) analysis (p3-b, Casper): hit-level-thinned + re-found ρ = 2 events against (i) the direct
ρ = 1 development counts (is the thinned pool a ρ = 1 pool?) and (ii) the repaired-thinning prediction on the SAME
trials (paired event bootstrap: where does the estimator's excess come from?).  Analysis env; writes
outputs/p3b/b2a_refind_control.json."""
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cols as TC  # noqa: E402

DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p3b')
OUT = HERE.parents[1] / 'outputs' / 'p3b'
log = logging.getLogger('refind_cmp')
NB = 2000
SHOW = ['R04', 'R05', 'R06', 'R07', 'R04x2S>=3', 'R05x2S>=3', 'R06x2S>=3', 'R05xp>0.001', 'R06xp>0.001']


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    rr = [np.load(f) for f in sorted(glob.glob(str(DATA / 'p3-b-refind' / '*' / 'refind-*.npz')))]
    G = np.concatenate([d['grp'][:, 0, :] for d in rr]).astype(float)
    key = np.char.add(np.char.add(np.concatenate([d['job'] for d in rr]).astype(str), '|'),
                      np.concatenate([d['ev'] for d in rr]).astype(str))
    keyt = np.char.add(key, np.char.add('|', np.concatenate([d['road'] for d in rr]).astype(str)))
    # repaired thinning on the same trials
    tt = [np.load(f) for f in sorted(glob.glob(str(DATA / 'p3-b-thin' / '*' / 'thin-*.npz')))]
    Tg = np.concatenate([d['grp'] for d in tt]).astype(float).mean(1)
    tk = np.char.add(np.char.add(np.char.add(np.concatenate([d['job'] for d in tt]).astype(str), '|'),
                                 np.concatenate([d['ev'] for d in tt]).astype(str)),
                     np.char.add('|', np.concatenate([d['road'] for d in tt]).astype(str)))
    pos = {k: i for i, k in enumerate(tk)}
    T = Tg[[pos[k] for k in keyt]]
    u, inv = np.unique(key, return_inverse=True)
    nev = len(u)
    rng = np.random.default_rng(21)
    W = rng.multinomial(nev, np.full(nev, 1 / nev), size=NB).astype(float)
    ne = np.bincount(inv, minlength=nev).astype(float)

    def boot(X):
        S = np.zeros((nev, X.shape[1])); np.add.at(S, inv, X)
        return S.sum(0) / ne.sum(), (W @ S) / (W @ ne)[:, None]

    rn, rrep = boot(G)
    tn, trep = boot(T)
    R = json.loads((OUT / 'b2_dev_closure.json').read_text())
    dr = R['direct']
    out = dict(trials=int(len(G)), events=int(nev), columns={})
    for c in SHOW:
        i = TC.COLS.index(c)
        N = G[:, i].sum()
        rec = dict(refind_count=float(N), refind_rate=float(rn[i]), thin_same_trials_rate=float(tn[i]),
                   direct_rate=dr['rate'][c], direct_count=dr['counts'][c])
        with np.errstate(divide='ignore', invalid='ignore'):
            if N > 0:
                lr = np.log(rrep[:, i] / dr['rate'][c])
                rec['ln_refind_over_direct'] = float(np.log(rn[i] / dr['rate'][c]))
                rec['sd_ln_refind_over_direct'] = float(np.sqrt(np.nanvar(lr, ddof=1) + 1 / dr['counts'][c]))
                lp = np.log(trep[:, i] / rrep[:, i])
                rec['ln_thin_over_refind'] = float(np.log(tn[i] / rn[i]))
                rec['sd_ln_thin_over_refind_paired'] = float(np.nanstd(lp[np.isfinite(lp)], ddof=1))
        out['columns'][c] = rec
        log.info('%-12s refind %.4g (N %d)  thin(same) %.4g  direct %.4g  ln(refind/dir) %s  ln(thin/refind) %s', c,
                 rn[i], N, tn[i], dr['rate'][c], rec.get('ln_refind_over_direct'), rec.get('ln_thin_over_refind'))
    (OUT / 'b2a_refind_control.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
