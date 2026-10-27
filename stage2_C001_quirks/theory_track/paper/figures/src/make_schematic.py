"""Conceptual diagram (not data) for the quirk P1/P2 note: the field-driven yo-yo in the pair CM frame.

Purpose : illustrate (left) the alternating odd near-miss / even head-on crossings and the axis rotation that
          accumulates toward E*_perp, and (right) the near-miss geometry with the three scales b << |x| << l_max.
Inputs  : none (all shapes are schematic, exaggerated by orders of magnitude; no physics numbers are plotted).
Run     : from theory_track/:  pixi run python paper/figures/src/make_schematic.py
Output  : paper/figures/schematic_nearmiss.{pdf,png}
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 16})
from matplotlib.patches import FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "schematic_nearmiss")

fig, (axl, axr) = plt.subplots(1, 2, figsize=(13, 5.6))

# ---------------- left: axis rotation over periods (exaggerated) ----------------
theta_step = np.deg2rad(7.0)     # exaggerated per-period rotation
nper = 5
cmap = plt.get_cmap("viridis")
for k in range(nper):
    th = k * theta_step
    d = np.array([np.cos(th), np.sin(th)])
    col = cmap(0.15 + 0.7 * k / nper)
    axl.plot([-d[0], d[0]], [-d[1], d[1]], color=col, lw=2.2, alpha=0.9)
axl.plot(0, 0, "ko", ms=5)
axl.annotate("", xy=(0.0, 0.9), xytext=(0.0, 0.25),
             arrowprops=dict(arrowstyle="-|>", lw=2.0, color="crimson"))
axl.text(0.05, 0.62, r"$\mathbf{E}^*_\perp$", color="crimson", fontsize=15)
axl.add_patch(FancyArrowPatch((1.05, 0.0), (1.05 * np.cos(4 * theta_step), 1.05 * np.sin(4 * theta_step)),
                              connectionstyle="arc3,rad=0.25", arrowstyle="-|>", mutation_scale=15, lw=1.5,
                              color="0.3"))
axl.text(1.10, 0.22, r"$\Theta = N_{\rm odd}\,\vartheta$", fontsize=17, color="0.2")
axl.text(0.25, -0.80, "axis after period 0, 1, 2, ...\n(rotation exaggerated)", fontsize=15,
         color="0.25")
axl.text(-1.15, 0.80, "pair CM frame", fontsize=16, style="italic")
axl.set_xlim(-1.25, 1.55)
axl.set_ylim(-0.95, 1.0)
axl.set_aspect("equal")
axl.axis("off")

# ---------------- right: one odd near-miss crossing ----------------
t = np.linspace(-1, 1, 400)
v = 0.8
b = 0.12
x1 = v * t
axr.plot(t, x1 * 0 + b / 2 + 0.0 * t, alpha=0)  # placeholder for limits
# end trajectories in the (x along axis, y transverse) plane, plotted as y vs x
xs = np.linspace(-1.0, 1.0, 400)
axr.plot(xs, np.full_like(xs, +b / 2), color="tab:blue", lw=2.2, label="end 1 (+q)")
axr.plot(xs, np.full_like(xs, -b / 2), color="tab:orange", lw=2.2, label="end 2 (-q)")
axr.annotate("", xy=(0.85, b / 2), xytext=(0.55, b / 2), arrowprops=dict(arrowstyle="-|>", color="tab:blue", lw=1.8))
axr.annotate("", xy=(-0.85, -b / 2), xytext=(-0.55, -b / 2),
             arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=1.8))
# miss distance
axr.annotate("", xy=(0.0, b / 2), xytext=(0.0, -b / 2), arrowprops=dict(arrowstyle="<->", lw=1.3))
axr.text(0.03, -0.035, r"$b_{\rm odd}$", fontsize=18)
# string pieces (schematic): short segment linking the ends at separation x
for xx in (0.35, 0.65):
    axr.plot([xx, -xx], [b / 2, -b / 2], color="0.55", lw=1.0, ls="--")
axr.text(0.30, 0.20, r"transverse pull $\sigma b/|x|$", fontsize=16, color="0.25")
# scales
axr.annotate("", xy=(0.95, -0.33), xytext=(0.08, -0.33), arrowprops=dict(arrowstyle="<->", lw=1.0, color="0.3"))
axr.text(0.17, -0.42, r"$b_{\rm odd} \ll |x| \ll \ell_{\max}$:  $\int dx/|x| \simeq \ln(\ell_{\max}/b_{\rm odd}) + O(1)$",
         fontsize=16, color="0.2")
axr.text(-1.0, 0.36, "odd crossing: ends miss by $b_{\\rm odd}$\neven crossing: head-on ($b=0$), no logarithm",
         fontsize=15, color="0.25")
axr.set_xlim(-1.05, 1.05)
axr.set_ylim(-0.5, 0.5)
axr.axis("off")
axr.legend(loc="lower left", fontsize=15, frameon=False)

fig.subplots_adjust(wspace=0.05, left=0.01, right=0.99, top=0.98, bottom=0.02)
fig.savefig(OUT + ".pdf", bbox_inches="tight")
fig.savefig(OUT + ".png", bbox_inches="tight", dpi=200)
print("wrote", OUT)
