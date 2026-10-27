"""T1_figure.py -- figure theory_track/figures/T1_lambda_plane.png

Purpose : (m_Q, Lambda=sqrt(sigma)) plane for the E quirk, N_IC = 2 (left) and 3 (right):
          - theory-favoured strips: SUSY-GUT ladder (1012.2072 anchor, T1_running.py), +-1.5 in 1/alpha
          - cosmology: contours of the maximal reheat temperature T_RH,max allowed by UV freeze-in
            (overclosure, solid; self-interacting sub-component f<0.025, dashed) from T1_cosmo.py
          - mesoscopic band 0.1-100 keV and CMS coplanar window 0.6-15 keV (theory_signal_model.md Sec.4)
          - FASER observed exclusion (HEPData ins3184325 t2) and D0 (1008.3547; N=2, Lambda > 10 keV)
Inputs  : code/T1_running_strips.npz, code/T1_cosmo_grid.npz (run T1_running.py and T1_cosmo.py first)
Run     : cd theory_track && pixi run python code/T1_figure.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S = np.load("code/T1_running_strips.npz")
C = np.load("code/T1_cosmo_grid.npz")
mQ = S["mQ"]
BLUE, ORANGE, AQUA, GRAY, INK, INK2 = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#0b0b0b", "#52514e"

faser_L = np.array([0.3, 0.5, 1.0, 1.7, 3.0, 10., 30., 100.]) * 1e-6
faser_m = np.array([57, 72, 113, 149, 163, 179, 173, 71])

fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), sharey=True)
for ax, N in zip(axes, (2, 3)):
    ax.set_facecolor("#fcfcfb")
    ax.axhspan(0.1e-6, 100e-6, color=GRAY, alpha=0.10, lw=0)
    ax.axhspan(0.6e-6, 15e-6, color=AQUA, alpha=0.16, lw=0)
    ax.text(2900, 3e-6, "CMS coplanar window\n0.6-15 keV", ha="right", va="center", color=INK2, fontsize=9)
    ax.text(2900, 60e-6, "mesoscopic band 0.1-100 keV", ha="right", va="center", color=INK2, fontsize=8.5)
    # FASER exclusion (N=2 benchmark; for N=3 sigma x 1.5 -> shown only for N=2)
    if N == 2:
        ax.fill_betweenx(faser_L, 90, faser_m, color=GRAY, alpha=0.45, lw=0)
        ax.plot(faser_m, faser_L, color=GRAY, lw=1.5)
        ax.text(95, 2.2e-7, "FASER\nexcl.", color=INK, fontsize=8, va="center")
        ax.plot([107, 107], [10e-6, 1e-2], color=GRAY, lw=1.5, ls=":")
        ax.text(110, 2e-3, "D0", color=INK2, fontsize=8)
    # theory strips
    for key in S.files:
        if not key.startswith(f"susy_N{N}_"):
            continue
        cen, lo, hi = S[key]
        nS = key.split("nS")[1]
        ax.fill_between(mQ, lo, hi, color=BLUE, alpha=0.18, lw=0)
        ax.plot(mQ, cen, color=BLUE, lw=2)
        i = np.argmin(abs(mQ - (160 if cen[np.argmin(abs(mQ-160))] > 2e-8 else 700)))
        if 1e-8 < cen[i] < 1e-2:
            ax.text(mQ[i], cen[i] * 1.35, f"SUSY GUT, $n_S$={nS}", color=BLUE, fontsize=8.5, rotation=14)
    # cosmology contours of T_RH,max
    lams, mqs = C["lams"], C["mqs"]
    X, Y = np.meshgrid(mqs, lams, indexing="ij")
    for k, ls in ((f"N{N}_oc", "-"), (f"N{N}_sidm", "--")):
        Z = C[k]
        for lev in (3, 10, 30):
            mm, ll = [], []
            for i, m in enumerate(mqs):
                z = Z[i]
                ok = np.isfinite(z)
                if ok.sum() < 2 or not (z[ok].min() < lev < z[ok].max()):
                    continue
                zz, la = np.log(z[ok][::-1]), np.log(lams[ok][::-1])   # increasing z
                mm.append(m); ll.append(np.exp(np.interp(np.log(lev), zz, la)))
            if len(mm) > 1:
                ax.plot(mm, ll, color=ORANGE, ls=ls, lw=1.6)
                if ls == "-":
                    j = int(np.argmin(abs(np.log(np.array(ll) / 3e-4))))
                    ax.text(mm[j] * 0.97, ll[j], f"{lev} GeV", color=ORANGE, fontsize=8, ha="right", va="center")
    # off-scale theory expectations
    ax.annotate("neutral naturalness (folded SUSY, quirky little Higgs,\nnatural quirks): $\\sqrt{\\sigma}\\sim$2-40 GeV (off scale)",
                xy=(1500, 9.5e-3), xytext=(1500, 2.3e-3), ha="center", fontsize=7.8, color=INK2,
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(90, 3000); ax.set_ylim(1e-8, 1e-2)
    ax.set_xlabel("$m_Q$ [GeV]", color=INK)
    ax.set_title(f"E quirk, SU({N}) infracolor", color=INK, fontsize=11)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=INK2)
    yt = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    ax.set_yticks(yt); ax.set_yticklabels(["10 eV", "100 eV", "1 keV", "10 keV", "100 keV", "1 MeV", "10 MeV"])
axes[0].set_ylabel(r"$\Lambda\equiv\sqrt{\sigma}$", color=INK)
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
h = [Line2D([], [], color=BLUE, lw=2), Patch(color=BLUE, alpha=0.18),
     Line2D([], [], color=ORANGE, lw=1.6), Line2D([], [], color=ORANGE, lw=1.6, ls="--"),
     Patch(color=GRAY, alpha=0.45), Patch(color=AQUA, alpha=0.16)]
l = ["SUSY-GUT ladder (MSSM + N copies of 5+5bar quirks + $n_S$ IC singlets; anchor 1012.2072)",
     "strip width: $\\pm$1.5 in $\\alpha_{IC}^{-1}(m_Q)$ (O(1) thresholds) and $\\pm$10% lattice",
     "UV freeze-in contour $T_{RH}^{max}$ = 3, 10, 30 GeV (overclosure): left/above a line is excluded if $T_{RH}$ exceeds its label",
     "same, self-interacting sub-component $f<0.025$",
     "FASER observed exclusion (N=2, HEPData)", "CMS coplanar window (theory_signal_model.md Sec.4)"]
fig.legend(h, l, loc="lower center", ncol=2, fontsize=8, frameon=False, bbox_to_anchor=(0.5, -0.01))
fig.suptitle("If the dark sector was EVER in equilibrium with the SM (standard thermal history, $T_{RH}>m_Q/25$), the whole plane above "
             "$\\sqrt{\\sigma}\\approx$12-60 eV is excluded\n(glueball overclosure, $\\Omega_G h^2\\approx$2-10 $\\times\\sqrt{\\sigma}$/keV for SU(2)) "
             "unless entropy dilution D $\\gtrsim$ 50-1300 occurs between T ~ 30 GeV and BBN.", fontsize=9, color=INK, y=0.995)
fig.tight_layout(rect=(0, 0.09, 1, 0.94))
fig.savefig("figures/T1_lambda_plane.png", dpi=150)
print("saved figures/T1_lambda_plane.png")
