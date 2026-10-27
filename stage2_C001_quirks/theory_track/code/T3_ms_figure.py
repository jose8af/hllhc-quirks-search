"""T3_ms_figure.py -- figure of the plane thickness vs Lambda with/without multiple scattering (from T3_ms_thickness.npy).
Run: pixi run python code/T3_ms_figure.py   ->  figures/T3_ms_thickness.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
rows = np.load(os.path.join(FIG, 'T3_ms_thickness.npy'))
LAMS = [0.3, 1.0, 3.0, 10.0, 30.0]
SER = [('B (3.8 T, no material)', 6, '#2a78d6', 'o'), ('B + material (MS, dE/dx)', 14, '#eb6834', 's'),
       ('material only (B = 0)', 18, '#1baf7a', '^')]
fig, axs = plt.subplots(1, 3, figsize=(13, 4.3), sharey=True)
for ax, m in zip(axs, (200.0, 500.0, 1000.0)):
    for lab, col, c, mk in SER:
        q = np.array([np.nanpercentile(rows[(rows[:, 0] == m) & (rows[:, 1] == l), col] * 1e4, [16, 50, 84]) for l in LAMS])
        ax.plot(LAMS, q[:, 1], marker=mk, color=c, lw=2, ms=8, label=lab)
        ax.fill_between(LAMS, q[:, 0], q[:, 2], color=c, alpha=0.15, lw=0)
    lam = np.logspace(np.log10(0.3), np.log10(30), 50)
    ax.plot(lam, 1.16 * (m / 100) * lam ** -4 * 3.8112, color='#52514e', ls='--', lw=1.2,
            label='analytic formula [1911.02223 Eq.III.12]')
    ax.axhline(100, color='#0b0b0b', lw=1, ls=':')
    ax.text(2.2, 120, 'Δs = 100 µm cut [1708.02243]', fontsize=8, color='#52514e')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_ylim(0.05, 3000); ax.set_xlim(0.25, 35)
    ax.set_title(f'm_Q = {m:.0f} GeV', fontsize=10); ax.set_xlabel('Λ = √σ [keV]')
    ax.grid(alpha=0.25, which='major')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
axs[0].set_ylabel('plane thickness Δs [µm]  (median, 16-84% band)')
axs[0].legend(fontsize=8, loc='lower left', frameon=False)
fig.suptitle('Causal Nambu-Goto propagation, CMS Phase-2 barrel hits, pT(QQ̄) > 200 GeV, |η| < 1  (T3 ESTIMATE)', fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(FIG, 'T3_ms_thickness.png'), dpi=140)
print('written')
