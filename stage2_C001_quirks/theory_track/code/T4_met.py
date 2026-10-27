"""T4_met.py -- alignment of the quirk-pair strip axis with the MET direction (Q4a; open problem G-T5-10).

Physics (exact in vacuum, T2 Sec.2.1): the hits of the pair lie in the plane spanned by the CM axis n and the pair
velocity; the pair centre moves on the straight line through the PV along P_QQ.  In the transverse plane the strip
axis (direction of the hit pattern from the PV) is therefore phi_pair exactly; in 3.8 T the CM momentum oscillates by
q (x1 - x2) x B, |dP| <= q B l_max = 0.0114 GeV/cm * l_max (< 0.1 GeV for l_max < 8 cm), i.e. <~ 3e-4 rad.
The quirks are invisible to calorimeter MET (<~ 5 GeV within 25 ns [1911.02223 Sec.V]), so the true MET vector is
the pair p_T.  The measured MET differs by the hadronic-recoil resolution sigma_perp per component (PU 200, PUPPI;
UNVERIFIED: scanned 15/25/35 GeV).  Random-plane background: strip azimuth uniform relative to MET (PU hits,
the hard-scatter jets are removed with the helix tracks), acceptance delta/pi for |dphi| < delta.
Method: LO DY+ISR pairs from the T2 cache (pT(QQ) > 200 GeV, |eta| < 1), MET = pT + Gaussian smearing; the strip-axis
phi from hits has negligible error (Fisher, T4_fisher_report: << 1 mrad).
Output: printed table (signal efficiency vs background rejection), figures/T4_met_alignment.png.
Run: pixi run python code/T4_met.py
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import load_cache  # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')


def main():
    c = load_cache()
    rng = np.random.default_rng(5)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
    print('m_Q | sigma_perp | median |dphi| | 68% |dphi| | 95% |dphi| | eff(|dphi|<0.1) rej | eff(<0.2) rej | eff(<0.3) | '
          'delta for 95% eff -> rejection')
    for m, col in zip((200, 500, 1000), ('C0', 'C1', 'C2')):
        key = f'F_{m}_isr'
        w = c[key + '_w']; gs = c[key + '_gamma_star']; bg = c[key + '_bg_pair']; eta = c[key + '_eta_pair']
        sel = np.abs(eta) < 1.0
        pt = (2 * m * gs * bg / np.cosh(eta))[sel]; ww = w[sel] / w[sel].sum()
        idx = rng.choice(len(pt), size=200000, p=ww)
        PT = pt[idx]
        for sp, ls in zip((15.0, 25.0, 35.0), (':', '-', '--')):
            mx = PT + rng.normal(0, sp, PT.size); my = rng.normal(0, sp, PT.size)
            dphi = np.abs(np.arctan2(my, mx))
            qs = np.quantile(dphi, [0.5, 0.68, 0.95])
            effs = [(dphi < d).mean() for d in (0.1, 0.2, 0.3)]
            d95 = qs[2]
            print(f'{m:5d} | {sp:4.0f} GeV | {qs[0]:.3f} | {qs[1]:.3f} | {qs[2]:.3f} | {effs[0]:.3f} x{np.pi/0.1:.0f} | '
                  f'{effs[1]:.3f} x{np.pi/0.2:.0f} | {effs[2]:.3f} x{np.pi/0.3:.1f} | {d95:.3f} -> x{np.pi/d95:.1f}')
            ds = np.linspace(0.005, 1.0, 200)
            eff = np.array([(dphi < d).mean() for d in ds])
            axs[0].plot(np.pi / ds, eff, ls=ls, color=col, label=f'm={m} GeV, σ⊥={sp:.0f} GeV')
            if sp == 25.0:
                axs[1].hist(dphi, bins=np.linspace(0, 0.4, 81), histtype='step', density=True, color=col,
                            label=f'm={m} GeV (median pT {np.median(PT):.0f} GeV)')
    axs[0].set_xscale('log'); axs[0].set_xlabel('random-plane rejection π/δ'); axs[0].set_ylabel('signal efficiency |Δφ| < δ')
    axs[0].grid(alpha=0.3, which='both'); axs[0].legend(fontsize=6)
    axs[1].set_xlabel('|φ(MET) − φ(strip axis)| [rad]'); axs[1].set_ylabel('density'); axs[1].legend(fontsize=7)
    axs[1].set_title('σ⊥(MET) = 25 GeV per component (UNVERIFIED)', fontsize=9)
    fig.suptitle('T4: quirk strip axis vs MET direction (LO DY+ISR, pT(QQ̄) > 200 GeV, |η| < 1)', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'T4_met_alignment.png'), dpi=130)


if __name__ == '__main__':
    main()
