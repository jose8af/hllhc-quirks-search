"""T4_comb.py -- linearity of the quirk-pair hit model: 1-D chi^2 scans (Q1).

For one LO DY+ISR event (m_Q = 500 GeV, fermion E, |eta| < 1) and Lambda in {1, 3, 10} keV, scan two directions of
parameter space with the causal-string model (T4_model, B = 3.8112 T, no material) and compute
    chi2(delta) = sum_hits [(y(delta) - y(0)) / sigma_res]^2      (positions r*phi and z, Phase-2 resolutions)
  (a) the oscillation-scale direction  d ln m = d ln pT = delta at fixed Lambda (all velocities fixed, l0 = m/sigma
      changes by delta) -> sensitive to the oscillation phase at every layer; expected "comb" (aliasing);
  (b) the vacuum-degenerate direction  d ln m = d ln pT = 2 d ln Lambda = delta (l0 and all velocities fixed; only
      eps_B = qB/sigma changes) -> the pure B-field handle on Lambda (smooth).
Output: figures/T4_comb.png and printed widths (delta at chi2 = 1, location of secondary minima).
Run: pixi run python code/T4_comb.py     (~5 min)
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T4_model import run, sample_theta, B_CMS, SIG_RPHI, SIG_Z, SENS_R, momenta  # noqa: E402
from T2_propagator import sigma_from_lambda_keV  # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')


def ypos(hits, phi_ref):
    y = {}
    for h in hits:
        k, L, n = int(h[0]), int(h[1]), int(h[9])
        if L <= 9:
            ph = (np.arctan2(h[4], h[3]) - phi_ref + np.pi) % (2 * np.pi) - np.pi
            y[(k, L, n, 'r')] = (SENS_R[L] * ph, SIG_RPHI[L])
            y[(k, L, n, 'z')] = (h[5], SIG_Z[L])
    return y


def chi2(y, y0, miss_pen=25.0):
    c = 0.0
    for kk, (v, s) in y0.items():
        if kk in y:
            c += ((y[kk][0] - v) / s) ** 2
        else:
            c += miss_pen          # a hit that disappears / appears counts as a 5-sigma outlier
    c += miss_pen * len(set(y) - set(y0))
    return c


def main():
    rng = np.random.default_rng(2024)
    th0 = sample_theta(500.0, 1, rng, eta_max=1.0)[0]
    p1, p2, _, m, _ = momenta(th0)
    gs = 1 + np.exp(th0[4]); bs = np.sqrt(1 - 1 / gs ** 2); pt = np.exp(th0[1])
    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    store = {}
    for j, lam in enumerate((1.0, 3.0, 10.0)):
        th = th0.copy(); th[8] = np.log(lam)
        nosc = sigma_from_lambda_keV(lam) * 108.3 / (2 * bs * pt)
        y0 = ypos(run(th)['hits'], th[2])
        for row, (name, vec, span) in enumerate((
                ('(a) l0 at fixed velocities: d ln m = d ln pT', np.array([0, 1, 0, 0, 0, 0, 0, 1, 0.]), 2.5 / nosc),
                ('(b) vacuum-degenerate: d ln m = d ln pT = 2 d ln L', np.array([0, 1, 0, 0, 0, 0, 0, 1, 0.5]), 0.6))):
            ds = np.linspace(-span, span, 161)
            c2 = np.array([chi2(ypos(run(th + d * vec)['hits'], th[2]), y0) for d in ds])
            # local width (chi2 = 1) from a fit to the 7 central points
            mid = len(ds) // 2
            sl = slice(mid - 3, mid + 4)
            a = np.polyfit(ds[sl], c2[sl], 2)[0]
            w = 1 / np.sqrt(a) if a > 0 else np.inf
            # secondary minima
            loc = [i for i in range(1, len(ds) - 1) if c2[i] < c2[i - 1] and c2[i] < c2[i + 1] and i != mid]
            sec = sorted([(c2[i], ds[i]) for i in loc])[:3]
            print(f'Lambda={lam} keV, N_osc(tracker)={nosc:.1f}, scan {name[:3]}: sigma_local = {w:.3g}; '
                  f'lowest secondary minima (chi2, delta): {[(round(c, 1), float(f"{d:.3g}")) for c, d in sec]}',
                  flush=True)
            # departure from the quadratic (linear-model) approximation: chi2 / (delta/w)^2 at multiples of w
            dev = []
            for mult in (1, 3, 10, 30, 100, 300, 1000, 3000):
                d = mult * w
                if d > span:
                    break
                cq = 0.5 * (chi2(ypos(run(th + d * vec)['hits'], th[2]), y0) + chi2(ypos(run(th - d * vec)['hits'], th[2]), y0))
                dev.append((mult, cq / mult ** 2))
            print('      chi2(k w)/k^2 [=1 if linear]: ' + ', '.join(f'k={a}: {b:.2f}' for a, b in dev), flush=True)
            store[(lam, row)] = (ds, c2, w, dev)
            ax = axs[row, j]
            ax.semilogy(ds, np.maximum(c2, 1e-2), lw=1.2)
            ax.axhline(1, color='gray', lw=0.6, ls='--'); ax.axhline(25, color='gray', lw=0.6, ls=':')
            ax.set_title(f'{name[:3]} Λ = {lam:g} keV (N_osc ≈ {nosc:.0f}); σ_loc = {w:.2g}', fontsize=9)
            ax.set_xlabel('δ (shift of ln parameter)' if row else 'δ = δ ln ℓ0 (velocities fixed)')
            if j == 0:
                ax.set_ylabel('χ² (positions, no MS)\n' + name, fontsize=8)
    fig.suptitle('T4: 1-D χ² scans of the causal-string hit model, m_Q = 500 GeV, one DY+ISR event, 3.8 T', fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'T4_comb.png'), dpi=130)
    np.save(os.path.join(FIG, 'T4_comb.npy'), np.array([store], dtype=object))


if __name__ == '__main__':
    main()
