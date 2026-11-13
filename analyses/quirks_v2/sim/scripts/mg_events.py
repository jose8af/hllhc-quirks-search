"""mg_events.py -- thin loader of the Stage-2 MadGraph5_aMC + Pythia8 quirk-pair samples for the theory-track
propagators (code/T3_causal.run_causal, code/T3_propagator.run_pair).  Does not modify code/.

Drop-in replacement for T3_propagator.sample_events (same return type), plus an ordered iterator for Stage 3
(the SAME events are propagated at every Lambda, so Lambda-to-Lambda differences carry no generator noise):

    import sys; sys.path.insert(0, 'sim/scripts'); sys.path.insert(0, 'code')
    from mg_events import sample_events_mg, iter_events, sample_file
    from T3_causal import run_causal
    for p1, p2, info in sample_events_mg(500, 10, sample='trig', spin='F', eta_max=2.5):
        r = run_causal(p1, p2, 500.0, 1.0)           # p1 = positive quirk (charges=(+1,-1) default)

Samples are located through the index file ../data/sim/SAMPLES_INDEX.json (written by the production scripts),
keyed '{spin}_{m}_{sample}' (sample in {'incl', 'trig', ...}); a file path can also be given explicitly.
Event = (p1, p2, info): p1/p2 = 3-momenta [GeV] of the positive/negative quirk after the Pythia8 shower;
info = dict(w=weight [fb, N_IC=1], gstar, cstar, bg, eta, pt, M, vtx (cm), recoil (4-vector), jets, idx, origin, tt_split).

WEIGHTS (review S2-R1 A1/A-1).  Events are NOT equal-weight in general: in the stitched trigger samples ('trig' = TRGS)
the INC-complement rows carry 3.7-9.6x the per-event weight of the TRG rows, and MLM leaves O(0.1 %) spreads elsewhere.
Every iterator returns the per-event weight info['w'] [fb, N_IC = 1]; Stage-3/4 summaries (efficiencies, medians,
histograms) MUST be weighted with it.  For code that needs equal-weight events, iter_events(..., unweight=True) performs a
deterministic hit-or-miss unweighting (keep row k if u_k < w_k / w_max, u_k from default_rng(unweight_seed) over ALL rows
of the file, w_max = max w of the file): the kept set does not depend on the selection, so the same events are used at
every Lambda, and info['w'] is then the common weight w_max (sums still give sigma).  Efficiency of the unweighting =
<w>/w_max (TRGS: 10.3-28.4 % for the tail rows pT > 200, |eta| < 2.5; 37-59 % over all rows with w > 0;
results/trgs_stats.json).  Rows with w = 0 (kept in the files for the qCut 67.5/90 variations) are never returned.
Any prefix of a file is a fair sample (TRGS rows are shuffled with a recorded seed; the other files are in MG order,
which is random), so taking the first N selected events is valid PROVIDED the weights are used (or unweight=True).

SPLIT (B-8).  Column tt_split (0 = template, 1 = toy, deterministic hash of the LHE event; ~50/50).  Use
iter_events(..., split='template') to build templates/efficiency maps and split='toy' for pseudo-data, never the same rows.

NORMALISATION (B6, B-2).  sigma_lo_mlm_fb() (alias sigma_fb, kept for old code) = N_IC x sum of LO-MLM weights in MG's Gmu
scheme, WITHOUT K-factor: 17-38 % below the recommended normalisation.  For yields use sigma_norm_fb() =
sigma_norm(N_IC = 2, LO(alpha(MZ)) x K, theory_signal_model §2.3; stored per file as 'sigma_norm_fb') x sum(w_sel) /
sigma_ref_fb ('sigma_ref_fb' = the INC sigma_matched at the same mass for TRG/TRGS files, the file's own sum(w) otherwise).
Not included in sigma_norm: inelastic gamma-gamma -> QQbar (+4.0-4.2 %), the infracolour Sommerfeld factor (+5-15 %), NLO EW
(UNVERIFIED, -few %); see SAMPLES.md.

Legacy path (no code change at all): write_t2_compat_cache() writes an npz with the old T2 cache keys
('{spin}_{m}_{sample}_{gamma_star,w,cstar,bg_pair,eta_pair}'); export T2_CACHE=<that file> and the old
T3_propagator.sample_events reads it.  It re-randomises the azimuths (as the old LO cache did), so it loses the
ISR-jet / quirk-plane correlation needed for MET-plane studies (S-4/S-5): prefer the loader.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data', 'sim'))
INDEX = os.path.join(DATA, 'SAMPLES_INDEX.json')
_CACHE = {}


def sample_file(m, sample='trig', spin='F'):
    idx = json.load(open(INDEX))
    return os.path.join(DATA, idx[f'{spin}_{int(m)}_{sample}'])


def load(path):
    if path not in _CACHE:
        _CACHE[path] = dict(np.load(path, allow_pickle=False))
    return _CACHE[path]


SPLITS = {'template': 0, 'toy': 1}


def _select(c, eta_max=None, ptmin=None, positive_only=True, split=None):
    sel = np.ones(len(c['w']), bool)
    if positive_only:
        sel &= c['w'] > 0
    if split is not None:
        if 'tt_split' not in c:
            raise KeyError('file has no tt_split column (run scripts/add_rowmap.py)')
        sel &= c['tt_split'] == SPLITS[split]
    if eta_max is not None:
        sel &= np.abs(c['eta_pair']) < eta_max
    if ptmin is not None:
        sel &= c['pt_pair'] > ptmin
    return np.where(sel)[0]


def _event(c, k):
    info = dict(w=float(c['w'][k]), gstar=float(c['gamma_star'][k]), cstar=float(c['cstar'][k]),
                bg=float(c['bg_pair'][k]), eta=float(c['eta_pair'][k]), pt=float(c['pt_pair'][k]),
                M=float(c['m_pair'][k]), vtx=c['vtx'][k].copy(), recoil=c['recoil'][k].copy(),
                jets=c['jets'][k].copy(), idx=int(k), origin=int(c['origin'][k]) if 'origin' in c else 0,
                tt_split=int(c['tt_split'][k]) if 'tt_split' in c else -1)
    return c['p_qp'][k, 1:].copy(), c['p_qm'][k, 1:].copy(), info


def _split_factor(c, split):
    """sum(w, all rows) / sum(w, rows of the split): rescales a split-restricted sum to the full sample (exact, not 2)."""
    if split is None:
        return 1.0
    return float(c['w'].sum() / c['w'][c['tt_split'] == SPLITS[split]].sum())


def unweight_mask(c, seed=12345):
    """Deterministic hit-or-miss acceptance over ALL rows of the file (independent of any selection)."""
    w = c['w']
    wmax = float(w[w > 0].max())
    u = np.random.default_rng(seed).random(len(w))
    return (w > 0) & (u < w / wmax), wmax


def iter_events(m=None, sample='trig', spin='F', path=None, eta_max=None, ptmin=None, split=None, unweight=False,
                unweight_seed=12345):
    """All selected events in file order, as (p1, p2, info).  info['w'] = per-event weight [fb, N_IC=1]: the events are
    NOT equal-weight (TRGS: INC-complement rows carry 3.7-9.6x the TRG weight) -> weight every summary with info['w'].
    unweight=True: deterministic hit-or-miss unweighting (see module docstring); info['w'] = w_max (common weight),
    info['w_orig'] = the original weight.  split = None | 'template' | 'toy' (column tt_split)."""
    c = load(path or sample_file(m, sample, spin))
    ids = _select(c, eta_max, ptmin, split=split)
    if unweight:
        acc, wmax = unweight_mask(c, unweight_seed)
        ids = ids[acc[ids]]
    for k in ids:
        p1, p2, info = _event(c, k)
        if unweight:
            info['w_orig'] = info['w']; info['w'] = wmax
        yield p1, p2, info


def sample_events_mg(m, n, sample='trig', spin='F', rng=None, eta_max=None, ptmin=None, path=None, replace=True, split=None):
    """Same signature/return type as T3_propagator.sample_events: n events drawn with probability proportional to w
    (so the drawn events are equal-weight; info['w'] keeps the original row weight)."""
    rng = rng or np.random.default_rng(1)
    c = load(path or sample_file(m, sample, spin))
    ids = _select(c, eta_max, ptmin, split=split)
    p = c['w'][ids] / c['w'][ids].sum()
    pick = rng.choice(ids, size=n, p=p, replace=replace)
    return [_event(c, k) for k in pick]


def sigma_lo_mlm_fb(m=None, sample='trig', spin='F', path=None, n_ic=2, eta_max=None, ptmin=None, weight=None, split=None):
    """LO-MLM cross section [fb] of the selection in MG's Gmu scheme, times N_IC (default 2), NO K-factor.
    NOT the yield normalisation (17-38 % below sigma_norm): use sigma_norm_fb for yields.  weight = a name in wvar_names
    (use only the merged '..._MERGING=...' columns; AUX_*/Weight are unmerged LHE weights, see SAMPLES.md)."""
    c = load(path or sample_file(m, sample, spin))
    ids = _select(c, eta_max, ptmin, positive_only=False, split=split)
    w = c['w'] if weight is None else c['wvar'][:, list(c['wvar_names']).index(weight)]
    f = _split_factor(c, split)
    return f * n_ic * float(w[ids].sum())


sigma_fb = sigma_lo_mlm_fb      # backward-compatible alias (LO-MLM, Gmu, no K)


def sigma_norm_fb(m=None, sample='trig', spin='F', path=None, eta_max=None, ptmin=None, weight=None, split=None):
    """Recommended yield normalisation [fb, N_IC = 2 included]: sigma_norm x (sum w_sel / sigma_ref).
    sigma_norm = 2 x K(TH §2.3) x LO(alpha = 1/127.9) (file scalar 'sigma_norm_fb'); sigma_ref = INC sigma_matched at the
    same mass (file scalar 'sigma_ref_fb').  Yield at 3 ab^-1 = 3000 * sigma_norm_fb(...)."""
    c = load(path or sample_file(m, sample, spin))
    if 'sigma_norm_fb' not in c:
        raise KeyError('file has no sigma_norm_fb (run scripts/annotate_npz.py)')
    ids = _select(c, eta_max, ptmin, positive_only=False, split=split)
    w = c['w'] if weight is None else c['wvar'][:, list(c['wvar_names']).index(weight)]
    f = _split_factor(c, split)
    return float(c['sigma_norm_fb']) * f * float(w[ids].sum()) / float(c['sigma_ref_fb'])


def write_t2_compat_cache(out, entries):
    """entries: list of (spin, m, sample_key_old, path) e.g. ('F', 500, 'isr', '.../E_m500_trig.npz').
    Old T2 sample keys: 'incl' (pT = 0 assumed by the old reader!) and 'isr'.  Use 'isr' for every MG sample."""
    d = {}
    for spin, m, key, path in entries:
        c = load(path)
        ok = c['w'] > 0
        for k in ('gamma_star', 'w', 'cstar', 'bg_pair', 'eta_pair'):
            d[f'{spin}_{int(m)}_{key}_{k}'] = c[k][ok]
    np.savez_compressed(out, **d)
    return out


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    c = load(path)
    print({k: (v.shape if hasattr(v, 'shape') else v) for k, v in c.items() if k not in ('wvar_names',)})
    ev = sample_events_mg(None, 3, path=path)
    for p1, p2, info in ev:
        print(np.round(p1, 2), np.round(p2, 2), {k: (round(v, 4) if isinstance(v, float) else v) for k, v in info.items()
                                                if k in ('w', 'gstar', 'cstar', 'pt', 'M')})
