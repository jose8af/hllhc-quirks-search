"""S1-R3 check: is the per-period (B*-off) part of the 3 keV excess the double-precision floor?
No new string runs. Uses E2's FIX2 raw per-event Delta_s (pure-E*perp 'eperp', B*-off 'off', s = 1 and 1/9) and M2.json (M2b eps scans).
(1) M2b: excess of b_odd and psi_pair over the law vs eps, all gamma*, both step sizes -> shape (eps^-2 ?) and coefficient vs u = 2.2e-16.
(2) Per event: predicted Delta_c(k_f) from the M2b floor curve delta(eps) evaluated at the event's eps_perp(B0/k_f), vs measured.
Run from TT: pixi run python analytic/review/r3_checks/r3_floor_test.py
"""
import os, sys, json
import numpy as np
from scipy.stats import spearmanr
TT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
NUM = os.path.join(TT, 'analytic', 'numerics')
sys.path.insert(0, NUM); sys.path.insert(0, os.path.join(TT, 'code'))
import FIX2_analysis as X
import FU_analysis as F

u = np.finfo(float).eps
# ---------------- (1) M2b floor curve
M2 = json.load(open(os.path.join(NUM, 'results', 'M2.json')))['M2b']
print('(1) M2b floor: relative excess over the eps>=1e-6 law (causal; b_odd normalised, psi_pair = psi_odd + psi_even)')
curve = {}
for key, b in M2.items():
    if 'th90_causal' not in key:
        continue
    rows = {round(np.log10(r['eps']) * 2) / 2: r for r in b['rows'] if r.get('valid')}
    ref = rows[-6.0]; G_dec = rows[-6.0]['psi_odd'] - rows[-5.0]['psi_odd']     # log slope per decade (law region)
    out = []
    for le in (-6.5, -7.0, -7.5):
        r = rows[le]; eps = 10 ** le
        db = r['b_odd'] / ref['b_odd'] - 1
        law = ref['psi_odd'] + G_dec * (-6.0 - le) + ref['psi_even']
        dp = (r['psi_odd'] + r['psi_even']) / law - 1
        out.append((eps, db, dp))
        print(f"  {key:22s} eps={eps:.2e}  db_odd={db:+.4f}  dpsi_pair={dp:+.4f}  db*eps^2/u={db*eps**2/u:6.2f}  dpsi*eps^2/u={dp*eps**2/u:6.2f}")
    curve[key] = out
# log-log slope between 3.2e-7 and 1e-7
for key, out in curve.items():
    s_b = np.log(out[1][1] / out[0][1]) / np.log(out[1][0] / out[0][0])
    s_p = np.log(out[1][2] / out[0][2]) / np.log(out[1][0] / out[0][0])
    print(f"  {key:22s} local power (3.2e-7 -> 1e-7): b_odd eps^{s_b:+.2f}, psi_pair eps^{s_p:+.2f}")

# floor model: delta(eps) = A u / eps^2 (A = 0.76 from gamma* = 1.3, max_boost 1e-3, the FIX2 setting; A = 0.5-1.3 over gamma*),
# capped at the measured 3.2e-8 value (0.18) below that eps
A_FLOOR = 0.76


def delta(eps, A=A_FLOOR):
    return min(A * u / eps ** 2, 0.18)


# ---------------- (2) per-event prediction vs FIX2 measurement
print('\n(2) per event: predicted floor Delta_c = R(f) delta(eps_perp(B0 f))/ln k_f (floor at B0 subtracted) vs measured (FIX2)')
res = {}
for m in (500.0, 1000.0):
    sets = {k: X.load_kind(k, m, 3.0) for k in ('eperp_s1', 'eperp_s9', 'off_s1', 'off_s9')}
    sets['on_s1'] = {i: v for i, v in F.fu_load(m, 3.0, 'fine').items() if i < 40}
    ids = sorted(set.intersection(*[set(v) for v in sets.values()]))
    K = X.evkin(m, 3.0, ids)
    eps0 = np.array([K[i]['eps'] for i in ids]); gs = np.array([K[i]['gstar'] for i in ids])
    kB = np.array([K[i]['kB_perp'] for i in ids]); cE = np.array([K[i]['c_E1'] for i in ids])
    pred = {}
    for j, kf in enumerate((2, 4, 20)):
        R = 1 + cE * np.log(kf)
        pred[kf] = np.array([R[n] * (delta(e / kf) - delta(e)) / np.log(kf) for n, e in enumerate(eps0)])
    ent = dict(n=len(ids), eps_B20_median=float(np.median(eps0 / 20)), eps_B20_p16_p84=np.percentile(eps0 / 20, [16, 84]).tolist(),
               gstar_median=float(np.median(gs)))
    print(f"  m={m:g}: n={len(ids)}, eps_perp(B0/20) median {np.median(eps0/20):.2e} (p16-p84 {np.percentile(eps0/20,16):.1e}-{np.percentile(eps0/20,84):.1e})")
    for kname in ('eperp_s1', 'eperp_s9', 'off_s1', 'off_s9', 'on_s1'):
        meas = np.array([X.cvec(sets[kname][i]) for i in ids]) - cE[:, None]
        row = {}
        for j, kf in enumerate((2, 4, 20)):
            p, d = pred[kf], meas[:, j]
            rho = spearmanr(p, d).correlation
            row[kf] = dict(pred_median=float(np.median(p)), meas_median=float(np.median(d)),
                           median_resid=float(np.median(d - p)), spearman=float(rho))
        res[f'm{m:g}_{kname}'] = row
        print(f"    {kname:9s} " + '  '.join(f"k{kf}: pred {row[kf]['pred_median']:+.4f} meas {row[kf]['meas_median']:+.4f} "
                                             f"resid {row[kf]['median_resid']:+.4f} rho {row[kf]['spearman']:+.2f}" for kf in (4, 20)))
    # per-event power-law dependence of the pure-E*perp Delta_c(20) on eps(B0/20)
    d20 = np.array([X.cvec(sets['eperp_s1'][i])[2] for i in ids]) - cE
    sel = d20 > 0
    sl = np.polyfit(np.log(eps0[sel] / 20), np.log(d20[sel]), 1)[0]
    rg = spearmanr(gs, d20).correlation; re = spearmanr(eps0, d20).correlation
    print(f"    eperp_s1 Delta_c(20): log-log slope vs eps(B0/20) on {sel.sum()} positive events = {sl:+.2f} (floor: -2); "
          f"Spearman vs eps {re:+.2f}, vs gamma* {rg:+.2f}")
    # binned in eps
    edges = np.percentile(eps0 / 20, [0, 33, 67, 100])
    for a, b in zip(edges[:-1], edges[1:]):
        s = (eps0 / 20 >= a) & (eps0 / 20 <= b)
        print(f"      eps(B0/20) in [{a:.1e},{b:.1e}] n={s.sum()}: meas {np.median(d20[s]):+.4f}  pred {np.median(pred[20][s]):+.4f}")
    # least-squares amplitude: meas = a * pred (eperp_s1, k_f = 20), i.e. lab-frame floor coefficient relative to M2b CM-frame
    a_fit = float(np.sum(d20 * pred[20]) / np.sum(pred[20] ** 2)); a_med = float(np.median(d20[pred[20] > 0] / pred[20][pred[20] > 0]))
    print(f"    eperp_s1 Delta_c(20): amplitude meas/pred  LSQ {a_fit:.2f}, median ratio {a_med:.2f}  (1 = M2b CM-frame floor coefficient)")
    ent['amp_lsq'] = a_fit; ent['amp_median_ratio'] = a_med
    ent['loglog_slope_eperp_s1_c20'] = float(sl); ent['spearman_eps'] = float(re); ent['spearman_gstar'] = float(rg)
    res[f'm{m:g}_summary'] = ent
json.dump(res, open(os.path.join(os.path.dirname(__file__), 'r3_floor_test.json'), 'w'), indent=1)
