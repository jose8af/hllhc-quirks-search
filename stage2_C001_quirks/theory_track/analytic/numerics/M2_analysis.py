"""M2_analysis.py -- E2: merge and fit the M2 single-crossing runs (results/raw/M2/*.npz) -> results/M2.json + stdout tables.

Definitions (all in the pair CM frame; l0 = m/sigma; v = CM speed of a quirk at the crossing):
  psi_b   = apsidal rotation across a crossing, projected on b-hat (positive = axis turns towards the offset).
  M2a law : psi_b/(b/l0) = A ln(l0/b) + K       (fit on floor <= b/l0 <= 1e-3); equivalently psi_b/(b/l_max) = Ahat ln(L/b),
            Ahat = A l_max/l0, L = l0 exp(K/A); Khat = Ahat ln(L/l_max); K_lmax = K - A ln(l_max/l0)
            dPi_b^TP/(sigma b/v) = A' ln(l0/b) + K'   (TP-to-TP relative transverse momentum, along -b-hat)
  profile : y(tau) = -dJ_b v/(sigma b) = kappa ln(2 v tau/b) + kappa0   (straight-string heuristic: kappa = 1, kappa0 = ln 2)
  M2b     : eps = qE/sigma; b_odd/(eps l0); psi_odd/eps = A_o ln(1/eps) + K_o; psi_even/eps.
Errors on fitted coefficients: standard least-squares errors scaled by the residual rms, and the spread between solvers.
Run: pixi run python analytic/numerics/M2_analysis.py
"""
import os, sys, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nm_stats import dump

RAW = os.path.join(HERE, 'results', 'raw', 'M2')
KI = {k: i for i, k in enumerate(('k', 'parity', 'b', 'bN', 'bP', 'gamma1', 'vrel', 'l_before', 'dA_N', 'dA_P',
                                  'dPiTP_N', 'dPiTP_P', 'dJTP_N', 'dJTP_P', 'aN', 'aP', 'r_lab', 'flag', 'cos_b_E', 't'))}


def linfit(x, y):
    x = np.asarray(x); y = np.asarray(y)
    A = np.vstack([x, np.ones_like(x)]).T
    coef, res, _, _ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ coef
    dof = max(len(x) - 2, 1)
    s2 = (r @ r) / dof
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef, np.sqrt(np.diag(cov)), float(np.sqrt(np.mean(r ** 2)))


def fit_prof(prof_row, sig, b, v, Th, lo=5.0, hi=3e-3):
    tau = prof_row[:, 0] * Th
    y = -prof_row[:, 3] * v / (sig * b)
    sel = (tau >= lo * b / (2 * v)) & (tau <= hi * Th)
    if sel.sum() < 4:
        return np.nan, np.nan
    (k, k0), _, _ = linfit(np.log(2 * v * tau[sel] / b), y[sel])
    return k, k0


def load(pattern):
    out = []
    for f in sorted(glob.glob(os.path.join(RAW, pattern))):
        z = dict(np.load(f, allow_pickle=True))
        z['file'] = os.path.basename(f)
        out.append(z)
    return out


def m2a():
    runs = load('A_*.npz')
    res = {}
    for gs in (1.05, 1.3, 2.0, 3.0):
        res[f'{gs:g}'] = {}
        for solver in ('causal0.01', 'causal0.001', 'conf256', 'conf2048'):
            rows = []
            for z in runs:
                if abs(float(z['gs']) - gs) > 1e-9 or f'_{solver}_' not in z['file'] or '_L1_m500' not in z['file']:
                    continue
                if not bool(z.get('valid', True)):
                    rows.append(dict(dl=float(z['dl']), valid=False)); continue
                T = z['T']; l0 = float(z['l0']); sig = float(z['sig']); v = float(z['v']); Th = float(z['Th'])
                d = float(z['d'])
                for j in range(min(2, len(T))):
                    # (-1)^(k+1): the quirk labels swap sides at every crossing, so the axis convention
                    # A_j = (-1)^j unit(x1 - x2) flips relative to b = x1 - x2 at even k
                    b = T[j, KI['b']]; sgn = np.sign(T[j, KI['bN']]) * (-1) ** j
                    psi_b = T[j, KI['dA_N']] * sgn
                    dpi_b = -T[j, KI['dPiTP_N']] * np.sign(T[j, KI['bN']])   # Pi and b both quirk1 - quirk2; along -b positive
                    k, k0 = fit_prof(z['prof'][j], sig, b, v, Th)
                    rows.append(dict(dl=float(z['dl']), k=j + 1, b_over_d=b / d, b_l0=b / l0, psi_norm=psi_b / (b / l0),
                                     dpi_norm=dpi_b / (sig * b / v), kappa=k, kappa0=k0, lmax_l0=T[j, KI['l_before']] / l0,
                                     valid=True))
            ok = [r for r in rows if r.get('valid') and np.isfinite(r['psi_norm'])]
            entry = dict(rows=rows, n_invalid=len([r for r in rows if not r.get('valid')]))
            # validity: double-precision floor of both solvers at b/l0 ~ 1e-8 (Minkowski products of null vectors
            # at relative angle b/l lose precision ~ angle^2); keep 3e-8 <= b/l0 <= 1e-3 and b = d to 1e-3
            # (floor rises with gamma*: 3e-8 at gamma* <= 1.3, 1e-6 at gamma* >= 2, where crossing 2 departs from b = d)
            fl = 3e-8 if gs <= 1.3 else 1e-6
            fitset = [r for r in ok if fl <= r['b_l0'] <= 1e-3 and abs(r['b_over_d'] - 1) < 3e-4]
            entry['floor_b_over_l0'] = fl
            entry['n_floor_rejected'] = len([r for r in ok if r['b_l0'] < fl or abs(r['b_over_d'] - 1) >= 3e-4])
            if len(fitset) >= 4:
                lm = float(np.median([r['lmax_l0'] for r in ok]))
                x = np.log(1 / np.array([r['b_l0'] for r in fitset]))
                (A, K), (eA, eK), rms = linfit(x, [r['psi_norm'] for r in fitset])
                (A2, K2), (eA2, eK2), rms2 = linfit(x, [r['dpi_norm'] for r in fitset])
                # curvature test: quadratic term
                c2 = np.polyfit(x, [r['psi_norm'] for r in fitset], 2)
                kap = np.array([r['kappa'] for r in fitset]); kap0 = np.array([r['kappa0'] for r in fitset])
                lm = np.median([r['lmax_l0'] for r in ok])
                rr = lm
                entry.update(Ahat=A * rr, Ahat_err=eA * rr, Khat=(K - A * np.log(rr)) * rr, L_over_lmax=float(np.exp((K - A * np.log(rr)) / A)),
                             Khat_err=np.hypot(eK, eA * np.log(rr)) * rr,
                             tp_impulse_mean=float(np.mean([r['dpi_norm'] for r in fitset])),
                             tp_impulse_sd=float(np.std([r['dpi_norm'] for r in fitset])))
                entry.update(A=A, A_err=eA, K=K, K_err=eK, rms=rms, A_tp=A2, A_tp_err=eA2, K_tp=K2, K_tp_err=eK2,
                             rms_tp=rms2, quad_coef=c2[0], K_lmax=K - A * np.log(lm), lmax_over_l0=lm,
                             kappa_med=float(np.nanmedian(kap)), kappa_spread=float(np.nanstd(kap)),
                             kappa0_med=float(np.nanmedian(kap0)), kappa0_spread=float(np.nanstd(kap0)),
                             n_fit=len(fitset), x_range=[float(x.min()), float(x.max())])
            res[f'{gs:g}'][solver] = entry
        # straight string
        ss = [z for z in load('SS_*.npz') if abs(float(z['gs']) - gs) < 1e-9]
        rows = [dict(dl=float(z['dl']), b_over_d=float(z['b'] / z['d']),
                     psi_norm=float(z['psi'] * np.sign(1.0)) / (float(z['b']) / float(z['l0'])),
                     dpi_raw=float(z['dPi'])) for z in ss]
        entry = dict(rows=rows)
        fitset = [r for r in rows if 3e-8 <= r['dl'] <= 1e-3]
        if len(fitset) >= 3:
            x = np.log(1 / np.array([r['dl'] * r['b_over_d'] for r in fitset]))
            (A, K), (eA, eK), rms = linfit(x, [abs(r['psi_norm']) for r in fitset])
            rr = 2 * (gs - 1)
            entry.update(A=A, A_err=eA, K=K, K_err=eK, rms=rms, n_fit=len(fitset), Ahat=A * rr, Ahat_err=eA * rr,
                         Khat=(K - A * np.log(rr)) * rr, L_over_lmax=float(np.exp((K - A * np.log(rr)) / A)))
        res[f'{gs:g}']['straight_string'] = entry
    # scale invariance
    sc = []
    for z in runs:
        if '_L1_m500' in z['file'] or abs(float(z['gs']) - 1.3) > 1e-9:
            continue
        T = z['T']; l0 = float(z['l0'])
        sc.append(dict(file=z['file'], dl=float(z['dl']), psi_norm=float(T[0, KI['dA_N']] * np.sign(T[0, KI['bN']]) / (T[0, KI['b']] / l0))))
    base = {float(z['dl']): float(z['T'][0, KI['dA_N']] * np.sign(z['T'][0, KI['bN']]) / (z['T'][0, KI['b']] / float(z['l0'])))
            for z in runs if '_L1_m500' in z['file'] and '_causal0.01_' in z['file'] and abs(float(z['gs']) - 1.3) < 1e-9}
    for s in sc:
        s['base_psi_norm'] = base.get(s['dl'], np.nan)
        s['rel_diff'] = s['psi_norm'] / s['base_psi_norm'] - 1
    res['scale_invariance'] = sc
    return res


def m2b(m2a_res):
    runs = load('B_*.npz')
    res = {}
    for gs in (1.05, 1.3, 2.0, 3.0):
        for th in (90.0, 60.0, 30.0):
            for solver in ('causal0.01', 'causal0.001', 'conf256', 'conf1024'):
                rows = []
                for z in runs:
                    if abs(float(z['gs']) - gs) > 1e-9 or abs(float(z['theta']) - th) > 1e-9 or f'_{solver}' not in z['file']:
                        continue
                    if not bool(z.get('valid', True)):
                        rows.append(dict(eps=float(z['eps']), valid=False)); continue
                    T = z['T']; l0 = float(z['l0']); eps = float(z['eps']); sig = float(z['sig']); v = float(z['v'])
                    Th = float(z['Th'])
                    epsp = eps * np.sin(np.radians(th))
                    odd = T[:, KI['parity']] == 1; even = ~odd
                    psi_o = T[odd, KI['dA_N']]; psi_e = T[even, KI['dA_N']]
                    kap = [fit_prof(z['prof'][j], sig, T[j, KI['b']], v, Th) for j in range(len(T)) if T[j, KI['parity']] == 1]
                    rows.append(dict(eps=eps, eps_perp=epsp, valid=True,
                                     b_odd=float(np.nanmedian(T[odd, KI['b']]) / (epsp * l0)),
                                     b_even=float(np.nanmedian(T[even, KI['b']]) / (epsp * l0)),
                                     b_even_last=float(T[even, KI['b']][-1] / (epsp * l0)) if even.sum() else np.nan,
                                     psi_odd=float(np.nanmedian(psi_o) / epsp), psi_even=float(np.nanmedian(psi_e) / epsp),
                                     cosbE=float(np.nanmedian(np.abs(T[odd, KI['cos_b_E']]))),
                                     lmax_l0=float(np.nanmedian(T[:, KI['l_before']]) / l0),
                                     kappa=float(np.nanmedian([k[0] for k in kap])), kappa0=float(np.nanmedian([k[1] for k in kap]))))
                if not rows:
                    continue
                entry = dict(rows=rows)
                ok = [r for r in rows if r.get('valid') and np.isfinite(r['psi_odd']) and r['eps_perp'] >= 3e-7]
                if len(ok) >= 3:
                    x = np.log(1 / np.array([r['eps_perp'] for r in ok]))
                    (Ao, Ko), (eAo, eKo), rms = linfit(x, [r['psi_odd'] for r in ok])
                    entry.update(A_odd=Ao, A_odd_err=eAo, K_odd=Ko, K_odd_err=eKo, rms=rms,
                                 b_odd_over_eps_l0=float(np.median([r['b_odd'] for r in ok])),
                                 b_odd_spread=float(np.std([r['b_odd'] for r in ok])),
                                 psi_even_over_eps=float(np.median([r['psi_even'] for r in ok])),
                                 psi_even_spread=float(np.std([r['psi_even'] for r in ok])))
                    # prediction from the M2a vacuum law at the measured b_odd
                    la = m2a_res[f'{gs:g}'].get('causal0.01', {})
                    if 'A' in la:
                        pred = [r['b_odd'] * (la['A'] * np.log(1 / (r['b_odd'] * r['eps_perp'])) + la['K']) for r in ok]
                        entry['psi_odd_pred_from_M2a'] = pred
                        entry['psi_odd_minus_pred'] = [r['psi_odd'] - p for r, p in zip(ok, pred)]
                        entry['pair_sum_minus_pred'] = [r['psi_odd'] + r['psi_even'] - p for r, p in zip(ok, pred)]
                res[f'g{gs:g}_th{th:g}_{solver}'] = entry
    return res


if __name__ == '__main__':
    A = m2a()
    B = m2b(A)
    out = dict(description='M2 controlled single crossings (pair CM frame). Truth level, classical NG. See NUMERICS.md §M2.',
               definitions=__doc__, M2a=A, M2b=B,
               run_parameters=dict(m=500.0, Lambda_keV=1.0, gamma_star=[1.05, 1.3, 2, 3], d_over_l0='1e-10..1e-2 (0.5 dec)',
                                   eps='1e-9..1e-3 (0.5 dec)', causal_max_boost=[1e-2, 1e-3], conformal_N=[256, 1024, 2048]))
    dump(out, os.path.join(HERE, 'results', 'M2.json'))
    print('=== M2a: psi_b/(b/l0) = A ln(l0/b) + K ; TP impulse dPi/(sigma b/v) = A_tp ln(l0/b) + K_tp ; profile kappa, kappa0')
    for gs in ('1.05', '1.3', '2', '3'):
        for s in ('causal0.01', 'causal0.001', 'conf256', 'conf2048', 'straight_string'):
            e = A[gs].get(s, {})
            if 'A' not in e:
                print(f'g*={gs} {s}: no fit ({e.get("n_invalid", "")} invalid)'); continue
            extra = (f" | A_tp={e['A_tp']:.4f}±{e['A_tp_err']:.4f} K_tp={e['K_tp']:.3f}±{e['K_tp_err']:.3f} | kappa={e['kappa_med']:.4f}"
                     f"(sd {e['kappa_spread']:.3f}) kappa0={e['kappa0_med']:.3f} | K_lmax={e['K_lmax']:.3f} quad={e['quad_coef']:.2e}"
                     f" inval={e['n_invalid']}") if s != 'straight_string' else ''
            print(f"g*={gs} {s:16s}: A={e['A']:.4f}±{e['A_err']:.4f} K={e['K']:.3f}±{e['K_err']:.3f} rms={e['rms']:.3g} n={e['n_fit']} | "
                  f"Ahat={e['Ahat']:.4f}±{e['Ahat_err']:.4f} Khat={e['Khat']:.3f} L/lmax={e['L_over_lmax']:.3f}{extra}"
                  + (f" | TPimp={e['tp_impulse_mean']:.3f}(sd {e['tp_impulse_sd']:.3f})" if 'tp_impulse_mean' in e else ''))
    print('scale invariance (g*=1.3):', [(s['file'][:40], round(s['rel_diff'], 6)) for s in A['scale_invariance']])
    print('\n=== M2b: E-driven crossings')
    for key, e in B.items():
        if 'A_odd' not in e:
            continue
        d = np.array(e.get('psi_odd_minus_pred', [np.nan])); ps = np.array(e.get('pair_sum_minus_pred', [np.nan]))
        print(f"{key:24s}: b_odd/(eps l0)={e['b_odd_over_eps_l0']:.4f}(sd {e['b_odd_spread']:.1e}) psi_odd/eps = {e['A_odd']:.4f}±{e['A_odd_err']:.4f} ln(1/eps) "
              f"+ {e['K_odd']:.3f}±{e['K_odd_err']:.3f} (rms {e['rms']:.2g}); psi_even/eps={e['psi_even_over_eps']:.4f}(sd {e['psi_even_spread']:.1e}); "
              f"odd-pred(M2a) med {np.nanmedian(d):.3f} sd {np.nanstd(d):.3f}; pair-pred {np.nanmedian(ps):.3f}")
