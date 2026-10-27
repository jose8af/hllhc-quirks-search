"""val_shower.py -- ISR-tail modelling uncertainty (review S2-R1 B5 / constructive B-1; fixer 2026-10-11).
Run: pixi run -e ana python scripts/val_shower.py   ->  results/shower.json
Inputs:
  (a) V-SHOWER (scripts/run_vshower.sh): E-TRG and E-INC m500 chunk 0 re-showered with the Pythia ISR+FSR renormalisation
      scale x1/2 (UP) and x2 (DN).  Nominal = chunk-0 rows of the delivered E-TRG/E-INC m500 files (same LHE, same seeds).
  (b) MG `systematics --alps=0.5,2` (scripts/run_alps.py): per-LHE-event ratios applied to the delivered TRGS and INC files
      (rows mapped by chunk, ievt_lhe, origin) at the benchmark points E/S x 200/500/1000 GeV.  Exact reweighting of the
      same events (no statistical error on the shift beyond the reweighting spread).
  (c) for comparison: the production 9-point (mu_R, mu_F) weights on the same quantities.
Quantities (TRGS-like = TRG U INC[pT_ME < 100]; fractions over the INC sigma_matched):
  f200, f300 = sigma(pT(QQ) > 200 / 300 GeV) / sigma_matched;
  in the tail (pT > 200, |eta_pair| < 2.5): weighted median of x = 2(gamma*-1) (prop. to l_max), q84 of gamma*-1, median N_osc.
Tag: ESTIMATE (single generator, LO-MLM + Pythia 8 CP5)."""
import os

import numpy as np

from vlib import S, DATA, have, save, wquant, nosc

ALPS = os.path.join(DATA, 'aux', 'fixer', 'alps')


def summary(pt, ptme, eta, g, bg, m, w, is_inc, wden):
    """Fractions over wden (sum of INC weights) and tail quantiles; rows = TRG rows + INC rows (is_inc)."""
    keep = (~is_inc) | (ptme < 100)                       # TRGS-like
    t200 = keep & (pt > 200); t300 = keep & (pt > 300)
    tail = t200 & (np.abs(eta) < 2.5) & (w != 0)
    x = 2 * (g - 1)
    no = nosc(g, bg, eta, m)
    return dict(f200=float(w[t200].sum() / wden), f300=float(w[t300].sum() / wden),
                x_median=float(wquant(x[tail], w[tail], (0.5,))[0]), gm1_q84=float(wquant(g[tail] - 1, w[tail], (0.84,))[0]),
                nosc_median=float(wquant(no[tail], w[tail], (0.5,))[0]), n_tail=int(tail.sum()))


def boot(fn, n, nb=100, seed=3):
    rng = np.random.default_rng(seed)
    return [fn(rng.integers(0, n, n)) for _ in range(nb)]


def pair(trg, inc, wt, wi, m):
    pt = np.r_[trg['pt'], inc['pt']]; ptme = np.r_[trg['pt_hard'], inc['pt_hard']]; eta = np.r_[trg['eta'], inc['eta']]
    g = np.r_[trg['g'], inc['g']]; bg = np.r_[trg['bg'], inc['bg']]; w = np.r_[wt, wi]
    is_inc = np.r_[np.zeros(len(wt), bool), np.ones(len(wi), bool)]
    s0 = summary(pt, ptme, eta, g, bg, m, w, is_inc, wi.sum())
    # bootstrap (resample TRG and INC rows separately)
    nt, ni = len(wt), len(wi)
    rng = np.random.default_rng(11)
    bs = []
    for _ in range(60):
        it = rng.integers(0, nt, nt); ii = rng.integers(0, ni, ni)
        ix = np.r_[it, nt + ii]
        bs.append(summary(pt[ix], ptme[ix], eta[ix], g[ix], bg[ix], m, w[ix], is_inc[ix], wi[ii].sum()))
    s0['err'] = {k: float(np.std([b[k] for b in bs])) for k in ('f200', 'f300', 'x_median', 'gm1_q84', 'nosc_median')}
    return s0


def rel(a, b, keys=('f200', 'f300', 'x_median', 'gm1_q84', 'nosc_median')):
    out = {}
    for k in keys:
        out[k] = a[k] / b[k] - 1
        if 'err' in a and 'err' in b:
            out[k + '_stat'] = float(np.hypot(a['err'][k] / a[k], b['err'][k] / b[k]))
    return out


def main():
    R = dict(note=__doc__)
    # ---------------- (a) V-SHOWER
    if have('V-SHOWER-UP-TRG', 500):
        trg, inc = S('E-TRG', 500), S('E-INC', 500)
        st, si = trg['chunk'] == 0, inc['chunk'] == 0
        ft = float(trg['nlhe']) / 50000; fi = float(inc['nlhe']) / 50000      # chunk-0 subset -> its own sigma
        sub = lambda c, s: {k: c[k][s] for k in ('pt', 'pt_hard', 'eta', 'g', 'bg', 'w')}
        nom = pair(sub(trg, st), sub(inc, si), trg['w'][st] * ft, inc['w'][si] * fi, 500.0)
        V = dict(nominal_chunk0=nom)
        for var in ('UP', 'DN'):
            vt, vi = S(f'V-SHOWER-{var}-TRG', 500), S(f'V-SHOWER-{var}-INC', 500)
            v = pair(vt, vi, vt['w'], vi['w'], 500.0)
            v['sigma_matched_INC_fb'] = float(vi['w'].sum()); v['rel_to_nominal'] = rel(v, nom)
            v['sigma_matched_rel'] = float(vi['w'].sum() / (inc['w'][si].sum() * fi) - 1)
            V[var] = v
        V['settings'] = {'UP': 'SpaceShower:renormMultFac = TimeShower:renormMultFac = 0.25 (mu_R x 1/2, larger alpha_s)',
                         'DN': 'SpaceShower:renormMultFac = TimeShower:renormMultFac = 4.0 (mu_R x 2, smaller alpha_s)'}
        R['vshower_m500'] = V
        print('V-SHOWER', {k: {q: round(100 * x, 2) for q, x in V[k]['rel_to_nominal'].items()} for k in ('UP', 'DN')}, flush=True)
    # ---------------- (b) alps and (c) 9-point on the delivered TRGS + INC at the benchmarks
    A = {}
    for spin, pre in (('F', 'E'), ('S', 'S')):
        for m in (200, 500, 1000):
            if not (have(f'{pre}-TRGS', m) and have(f'{pre}-INC', m)):
                continue
            ts, inc = S(f'{pre}-TRGS', m), S(f'{pre}-INC', m)

            def ratio(c, src_of_row, key):
                r = np.ones(len(c['w']))
                for k in np.unique(c['chunk']):
                    for src in np.unique(src_of_row):
                        f = os.path.join(ALPS, f'{src}_m{m}_c{k}.npz')
                        s = (c['chunk'] == k) & (src_of_row == src)
                        if s.any():
                            r[s] = np.load(f)[key][c['ievt_lhe'][s]]
                return r
            src_ts = np.where(ts['origin'] == 1, f'{pre}-INC', f'{pre}-TRG')
            src_inc = np.full(len(inc['w']), f'{pre}-INC')
            trg_part = {k: ts[k] for k in ('pt', 'pt_hard', 'eta', 'g', 'bg')}
            # TRGS already contains the INC complement: treat all TRGS rows as 'TRG' rows (keep), INC only as denominator
            def summ(wts, winc):
                is_inc = np.zeros(len(wts), bool)
                return summary(ts['pt'], ts['pt_hard'], ts['eta'], ts['g'], ts['bg'], float(m), wts, is_inc, winc.sum())
            nom = summ(ts['w'], inc['w'])
            P = dict(nominal=nom)
            for key, lab in (('r_alps0p5', 'alps0p5'), ('r_alps2', 'alps2')):
                P[lab] = summ(ts['w'] * ratio(ts, src_ts, key), inc['w'] * ratio(inc, src_inc, key))
                P[lab]['rel_to_nominal'] = rel(P[lab], nom)
            nm = list(ts['wvar_names'])
            sc = []
            for n in nm:
                if n.startswith('MUF=') and 'PDF=14400_' in n and 'DYN' not in n:
                    sc.append(rel(summ(ts['wvar'][:, nm.index(n)], inc['wvar'][:, list(inc['wvar_names']).index(n)]), nom))
            P['scale9_envelope'] = {k: [min(s[k] for s in sc), max(s[k] for s in sc)] for k in sc[0]}
            A[f'{spin}_{m}'] = P
            print('alps', spin, m, {k: round(100 * v, 2) for k, v in P['alps0p5']['rel_to_nominal'].items()},
                  {k: round(100 * v, 2) for k, v in P['alps2']['rel_to_nominal'].items()}, flush=True)
    R['alps_and_scale9'] = A
    save('shower.json', R)


if __name__ == '__main__':
    main()
