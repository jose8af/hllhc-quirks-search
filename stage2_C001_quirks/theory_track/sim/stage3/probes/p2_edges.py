"""p2_edges.py -- Stage-3 probe 2: physics scales that place the Lambda grid edges, per mass, on the Stage-3 selection.

Selection: E/Etilde TRGS, pT(QQ) > 200 GeV, |eta_pair| < 2.5, template half, weights w (Kish).  Closed forms [T2 §2.2;
synthesis Box B]: l_max = 2(gamma*-1) m/sigma, sigma = 50.68 GeV/cm (Lambda/keV)^2; N_osc(r < R_eff) = sigma R_eff/(2 beta* pT)
with R_eff = min(108.3 cm, 265 cm/|sinh eta_pair|) (last OT barrel layer or last TEPX disc).
Output per mass: weighted median and 16/84 % of x = 2(gamma*-1); the Lambda [keV] at which the weighted median of
  l_max = R_OT (108.3 cm), = R_IT (14.6 cm), = 100 um (PS/IT long pitch), = 25 um (IT short pitch);
  N_osc = 1 (median) and the fraction of events with N_osc < 1 at 0.3/0.4/0.5 keV;
  eps_B and the median b_odd/l0 (analytic, c06 pair_params) at 10/20/30/40 keV vs the precision floor 3e-8.
Run (from theory_track/): pixi run python sim/stage3/probes/p2_edges.py  -> data/sim_stage3/probes/p2_edges.json
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(TT, 'sim', 'scripts')); sys.path.insert(0, os.path.join(TT, 'analytic', 'checks'))
import mg_events as mg  # noqa
from c06_rotating_yoyo import pair_params  # noqa

SIG1 = 50.68   # GeV/cm at 1 keV


def wq(x, w, q):
    i = np.argsort(x); cw = np.cumsum(w[i]) / w.sum()
    return np.interp(q, cw, x[i])


out = {}
for spin, m in [('F', mm) for mm in (200, 300, 500, 700, 1000, 1200, 1500)] + [('S', mm) for mm in (200, 500, 1000)]:
    ev = list(mg.iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200.0, split='template'))
    gs = np.array([e[2]['gstar'] for e in ev]); w = np.array([e[2]['w'] for e in ev])
    eta = np.array([e[2]['eta'] for e in ev]); pt = np.array([e[2]['pt'] for e in ev])
    x = 2 * (gs - 1); bs = np.sqrt(1 - 1 / gs ** 2)
    Reff = np.minimum(108.3, 265.0 / np.maximum(np.abs(np.sinh(eta)), 1e-9))
    xm = wq(x, w, 0.5)
    lam_at = lambda L: float(np.sqrt(xm * m / SIG1 / L))       # median l_max = L  ->  Lambda
    n1 = SIG1 * Reff / (2 * bs * pt)                            # N_osc at 1 keV per event
    row = dict(x_med=round(float(xm), 4), x_p16=round(float(wq(x, w, 0.16)), 4), x_p84=round(float(wq(x, w, 0.84)), 4),
               lam_lmax_eq_ROT=round(lam_at(108.3), 3), lam_lmax_eq_RIT=round(lam_at(14.6), 3),
               lam_lmax_eq_100um=round(lam_at(0.01), 2), lam_lmax_eq_25um=round(lam_at(0.0025), 2),
               Nosc1keV_med=round(float(wq(n1, w, 0.5)), 2), lam_Nosc_eq_1=round(float(1 / np.sqrt(wq(n1, w, 0.5))), 3),
               f_Nosc_lt1={str(L): round(float(w[n1 * L * L < 1].sum() / w.sum()), 3) for L in (0.3, 0.4, 0.5)})
    sub = ev[:300]
    for L in (5.0, 10.0, 20.0, 30.0, 40.0):
        bl = np.array([pair_params(p1, p2, float(m), L)['bodd'] / pair_params(p1, p2, float(m), L)['l0'] for p1, p2, _ in sub])
        row[f'bodd_l0_med_{L:g}keV'] = float(np.median(bl)); row[f'f_bodd_l0_lt_1e-7_{L:g}keV'] = round(float((bl < 1e-7).mean()), 3)
    out[f'{spin}_{m}'] = row
    print(spin, m, row, flush=True)
json.dump(out, open(os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p2_edges.json'), 'w'), indent=1)
