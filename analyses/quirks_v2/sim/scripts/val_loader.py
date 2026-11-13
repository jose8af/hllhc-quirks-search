"""val_loader.py -- VALIDATION §6: round trip of the Stage-2 samples through the theory-track propagator.
Run from theory_track/ in the THEORY-TRACK env (needs code/ and numba):  pixi run python sim/scripts/val_loader.py
Checks: (a) loader kinematics consistency (p1 + p2 vs stored pair observables; p1 = positive quirk);
(b) iter_events determinism; (c) run_causal (B = 3.8 T, material on, Lambda = 1 keV) on 500 events per point drawn
with sample_events_mg (trig, pT > 200, |eta| < 2.5) vs the same number drawn from the old LO cache with
T3_propagator.sample_events ('isr'); (d) legacy path: write_t2_compat_cache + T2_CACHE env + the unchanged
T3_propagator.sample_events; (e) first-N regression check (review S2-R1 A1/A-1): for the stitched 'trig' files, the share
of the selected weight carried by INC-origin rows and the weighted median of 2(gamma*-1) in the first N = 500/2000/5000
selected events (file order, weighted) and in the first N unweighted events (iter_events(unweight=True)) must agree
with the full file within statistics (|pull| < 3, binomial/bootstrap error); also the template/toy split.
Output: sim/results/loader.json."""
import json
import os
import subprocess
import sys
import time

import numpy as np

TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(TT, 'sim', 'scripts')); sys.path.insert(0, os.path.join(TT, 'code'))
from mg_events import sample_events_mg, iter_events, sample_file, load, write_t2_compat_cache   # noqa
from T3_causal import run_causal   # noqa
from T3_propagator import sample_events, plane_fit   # noqa

N = int(os.environ.get('VAL_N', 500))
LAM = 1.0


def gstar_of(p1, p2, m):
    e1, e2 = np.hypot(m, np.linalg.norm(p1)), np.hypot(m, np.linalg.norm(p2))
    P = p1 + p2; E = e1 + e2
    M = np.sqrt(E ** 2 - P @ P)
    return M / (2 * m), M, np.hypot(P[0], P[1])


def propagate(evs, m):
    st, nh, th, tt = [], [], [], []
    for p1, p2, info in evs:
        t0 = time.time()
        r = run_causal(np.asarray(p1), np.asarray(p2), float(m), LAM)
        tt.append(time.time() - t0)
        st.append(int(r['status'])); H = r['hits']; nh.append(len(H))
        th.append(plane_fit(H[:, 3:6])[0] * 1e4 if len(H) > 3 else np.nan)
    th = np.array(th)
    return dict(status_counts={str(k): int(v) for k, v in zip(*np.unique(st, return_counts=True))},
                nhits_q=np.percentile(nh, [16, 50, 84]).tolist(), thickness_um_q=np.nanpercentile(th, [16, 50, 84]).tolist(),
                time_per_event_s=float(np.mean(tt)))


def wmed(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); return float(x[i][np.searchsorted(c, c[-1] / 2)])


def firstn_check(m, spin):
    """(e) prefix-fairness regression check on the stitched file (pT > 200, |eta| < 2.5)."""
    full = [(e[2]['w'], e[2]['origin'], 2 * (e[2]['gstar'] - 1)) for e in iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200)]
    W = np.array([a[0] for a in full]); O = np.array([a[1] for a in full]); X = np.array([a[2] for a in full])
    share_full = float(W[O == 1].sum() / W.sum()); med_full = wmed(X, W)
    rng = np.random.default_rng(7)
    out = dict(n_selected=len(W), inc_share_full=share_full, x_median_full=med_full, prefixes={})
    ok = True
    for n in (500, 2000, 5000):
        if n > len(W):
            continue
        w, o, x = W[:n], O[:n], X[:n]
        share = float(w[o == 1].sum() / w.sum())
        # error of a weighted share from a random n-subsample (bootstrap over the full file)
        bs = [(lambda ix: W[ix][O[ix] == 1].sum() / W[ix].sum())(rng.integers(0, len(W), n)) for _ in range(300)]
        bm = [(lambda ix: wmed(X[ix], W[ix]))(rng.integers(0, len(W), n)) for _ in range(150)]
        ps, pm = (share - share_full) / np.std(bs), (wmed(x, w) - med_full) / np.std(bm)
        out['prefixes'][n] = dict(inc_share=share, inc_share_pull=float(ps), x_median=wmed(x, w), x_median_pull=float(pm))
        ok &= abs(ps) < 3 and abs(pm) < 3
    # unweighted prefix: equal-weight events, so plain counts / plain medians
    uw = [(e[2]['origin'], 2 * (e[2]['gstar'] - 1)) for e in iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200, unweight=True)]
    Ou = np.array([a[0] for a in uw]); Xu = np.array([a[1] for a in uw])
    out['unweighted'] = dict(n_accepted=len(Ou), efficiency=len(Ou) / len(W), inc_count_share=float(Ou.mean()),
                             x_median=float(np.median(Xu)))
    for n in (500, 2000):
        if n <= len(Ou):
            sh = float(Ou[:n].mean()); e = np.sqrt(share_full * (1 - share_full) / n)
            pm = (np.median(Xu[:n]) - med_full) / np.std([np.median(Xu[rng.integers(0, len(Xu), n)]) for _ in range(150)])
            out['unweighted'][f'first{n}'] = dict(inc_count_share=sh, pull=float((sh - share_full) / e), x_median=float(np.median(Xu[:n])),
                                                  x_median_pull=float(pm))
            ok &= abs((sh - share_full) / e) < 3 and abs(pm) < 3
    # template / toy split: both halves reproduce the full weighted median
    for sp in ('template', 'toy'):
        ev = [(e[2]['w'], 2 * (e[2]['gstar'] - 1)) for e in iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200, split=sp)]
        out[f'split_{sp}'] = dict(n=len(ev), x_median=wmed(np.array([a[1] for a in ev]), np.array([a[0] for a in ev])))
    out['PASS'] = bool(ok)
    return out


def main():
    R = dict(note=__doc__, lambda_keV=LAM, n_per_point=N, points={})
    rng = np.random.default_rng(2026)
    for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('S', 500)):
        try:
            path = sample_file(m, 'trig', spin)
        except KeyError:
            continue
        c = load(path)
        P = {}
        # (a) consistency
        evs = sample_events_mg(m, N, sample='trig', spin=spin, rng=rng, eta_max=2.5, ptmin=200)
        dev = []
        for p1, p2, info in evs:
            g, M, pt = gstar_of(p1, p2, m)
            dev.append(max(abs(g / info['gstar'] - 1), abs(M / info['M'] - 1), abs(pt / info['pt'] - 1)))
            assert np.allclose(p1, c['p_qp'][info['idx'], 1:]) and np.allclose(p2, c['p_qm'][info['idx'], 1:])
        P['max_rel_dev_kinematics'] = float(np.max(dev))
        P['p1_is_positive_quirk'] = 'p1 = p_qp (pid < 0: xe+/sxe+, charge +1) checked for all drawn events'
        # (b) determinism
        a = [e[2]['idx'] for e in iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200)]
        b = [e[2]['idx'] for e in iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200)]
        P['iter_events_deterministic'] = a == b; P['n_selected'] = len(a)
        P['firstN_regression'] = firstn_check(m, spin)
        print(spin, m, 'first-N check', P['firstN_regression']['PASS'], flush=True)
        # (c) propagation, new vs old
        P['new_MG'] = propagate(evs, m)
        oldev = sample_events(m, N, sample='isr', spin=spin, rng=rng, eta_max=2.5, ptmin=200)
        P['old_LO_cache'] = propagate(oldev, m)
        P['gstar_median_new'] = float(np.median([e[2]['gstar'] for e in evs]))
        P['gstar_median_old'] = float(np.median([e[2]['gstar'] for e in oldev]))
        R['points'][f'{spin}_{m}'] = P
        print(spin, m, P['new_MG'], P['old_LO_cache'], flush=True)
    # (d) legacy path
    compat = os.path.join(TT, 'data', 'sim', 'npz', 'aux', 'T2compat_cache.npz')   # non-physics files in npz/aux (C-16)
    ent = []
    for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('S', 200), ('S', 500), ('S', 1000)):
        try:
            ent.append((spin, m, 'isr', sample_file(m, 'trig', spin)))
        except KeyError:
            pass
    write_t2_compat_cache(compat, ent)
    code = ("import sys,numpy as np; sys.path.insert(0,'code'); from T3_propagator import sample_events as s; "
            "ms=[np.median([e[2]['gstar'] for e in s(500,2000,'isr','F',np.random.default_rng(k),eta_max=2.5,ptmin=200)]) for k in range(5,25)]; "
            "print(np.std(ms), np.mean(ms))")   # 20 x 2000 draws: a single 2000-event median fluctuates by 0.6 % (fixer S2-R1)
    out = subprocess.run([sys.executable, '-c', code], cwd=TT, env=dict(os.environ, T2_CACHE=compat), capture_output=True, text=True)
    g_legacy = float(out.stdout.strip().split()[-1]); g_legacy_sd = float(out.stdout.strip().split()[-2])
    c = load(sample_file(500, 'trig', 'F'))
    sel = (c['w'] > 0) & (c['pt_pair'] > 200) & (np.abs(c['eta_pair']) < 2.5)
    i = np.argsort(c['gamma_star'][sel]); cw = np.cumsum(c['w'][sel][i]); g_direct = float(c['gamma_star'][sel][i][np.searchsorted(cw, cw[-1] / 2)])
    R['legacy_path'] = dict(file=os.path.relpath(compat, TT), gstar_median_via_old_reader_mean_of_20x2000ev=g_legacy, spread_of_one_2000ev_median=g_legacy_sd,
                            gstar_weighted_median_direct=g_direct,
                            note='the old reader re-randomises azimuths; only (gamma*, cos theta*, beta gamma, eta) survive')
    json.dump(R, open(os.path.join(TT, 'sim', 'results', 'loader.json'), 'w'), indent=1)
    print('legacy', g_legacy, g_direct)


if __name__ == '__main__':
    main()
