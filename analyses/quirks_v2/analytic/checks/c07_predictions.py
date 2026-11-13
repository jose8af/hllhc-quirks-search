"""c07_predictions.py -- E1: population predictions of the analytic theory (NEAR_MISS_IMPULSE.md §5, §8).

Uses the rotating-yo-yo model of c06 (exact vacuum yo-yo + rigid rotation eta = eps_perp G(gamma*)[ln(l_max/b_odd)
+ K(gamma*)] at each odd crossing; no causal propagation, no fit) on the T3 event sample (sample_events, |eta_pair|<1)
to predict, at B = 3.8112 T:
  * median Delta s_B(Lambda) for m = 200, 500, 1000 GeV and the local exponents d ln Ds / d ln Lambda;
  * per-event c_ev = 1/(L + K) (median, 16-84 %);
  * the response per unit B, R(f) = median[Ds(fB)/(f Ds(B))] at f = 1/4, 1/20, 1/80, 1/1000 (event-wise analytic:
    R_ev(f) = (L + K + ln(1/f))/(L + K), since in the model Ds is linear in eta), plus the effective exponent
    d ln Ds / d ln B.
Run: pixi run python analytic/checks/c07_predictions.py [nev] > analytic/checks/c07_predictions_out.txt
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c06_rotating_yoyo import model_hits, pair_params, K_of, plane_fit, sample_events  # noqa: E402

LAMS = [0.3, 0.6, 1.0, 2.0, 3.0, 5.0, 10.0]
FR = [1 / 4, 1 / 20, 1 / 80, 1 / 1000]

if __name__ == '__main__':
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    for m in (200.0, 500.0, 1000.0):
        rng = np.random.default_rng(2026)
        ev = sample_events(m, nev, rng=rng, eta_max=1.0)
        print(f'\n=== m = {m:.0f} GeV, {nev} events (T3 sample, seed 2026), B = 3.8112 T')
        print('Lambda | median Ds_model [um] (16-84) | c_ev median (16-84) | local exponent to next Lambda | '
              'R(1/4) R(1/20) R(1/80) R(1/1000) | dlnDs/dlnB at B (=1-c, median)')
        meds = []
        for lam in LAMS:
            ds, cs, Rs = [], [], []
            for (p1, p2, info) in ev:
                H, pp = model_hits(p1, p2, m, lam, npts=(4000 if lam <= 3 else 600))
                if len(H) < 4:
                    continue
                ds.append(plane_fit(H[:, 2:5])[0])
                LK = pp['L'] + K_of(pp['gs'])
                cs.append(1 / LK)
                Rs.append([(LK + np.log(1 / f)) / LK for f in FR])
            ds = np.array(ds) * 1e4; cs = np.array(cs); Rs = np.array(Rs)
            meds.append(np.median(ds))
            q = np.percentile(ds, [16, 50, 84]); qc = np.percentile(cs, [16, 50, 84])
            Rm = np.median(Rs, axis=0)
            print(f'{lam:5.1f} | {q[1]:9.3g} ({q[0]:.3g}-{q[2]:.3g}) | {qc[1]:.4f} ({qc[0]:.4f}-{qc[2]:.4f}) | '
                  f'{"":>8s} | ' + ' '.join(f'{r:.3f}' for r in Rm) + f' | {1 - qc[1]:.3f}', flush=True)
        print('local exponents (median Ds): ' + ', '.join(
            f'{LAMS[i]}->{LAMS[i+1]}: {np.log(meds[i+1]/meds[i])/np.log(LAMS[i+1]/LAMS[i]):+.3f}' for i in range(len(LAMS) - 1)))
