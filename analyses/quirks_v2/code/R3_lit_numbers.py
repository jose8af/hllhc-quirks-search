"""R3_lit_numbers.py -- reviewer R3 literature-number checks (no simulation).

Purpose
  1. Local Lambda exponent of the *numerical* plane thickness already published by
     Li et al. [2002.07503 Fig.4 left], from by-eye modes of the histograms
     (m = 100 GeV, pT > 100 GeV; Lambda = 200 eV, Lambda0 = sqrt(4e5) eV = 632 eV, 2 keV;
     m = 500 GeV at Lambda0 overlaps m = 100 GeV -> m independence).
  2. FASER observed exclusion vs Lambda [2607.26195 Fig.5, read by eye from a 200 dpi render]
     compared with the v3 synthesis' Run-2+3 stopped-pair update (S-8 table) and D0 [1008.3547].
  3. Li/causal gamma* dependence: medians and ranges recomputed from figures/R2_li_gamma*_out.txt.

Inputs : figures/R2_li_gamma_out.txt, figures/R2_li_gamma2_out.txt (R2 outputs); digitised values below.
Run    : from theory_track/:  pixi run python code/R3_lit_numbers.py   (< 1 s)
Output : stdout (copied into review/REVIEW_R3.md).
All digitised values are READINGS BY EYE (+-15 % in d, +-5 GeV in m); treat as such.
"""
import math, re, statistics, pathlib

# ---- 1. Li et al. Fig.4 (left) histogram modes [um] (by eye) ----
li_modes = {200: 600.0, 632: 65.0, 2000: 15.0}
print("1) Li et al. 2002.07503 Fig.4: local exponent of numerical thickness (mode-based, by eye)")
L = sorted(li_modes)
for a, b in zip(L[:-1], L[1:]):
    n = math.log(li_modes[a] / li_modes[b]) / math.log(b / a)
    print(f"   Lambda {a}->{b} eV: d ~ Lambda^-{n:.2f}")
d_formula = lambda m, lam_kev, B=3.8: 1.16 * (m / 100) * lam_kev ** -4 * B
print(f"   formula d at 2 keV, 100 GeV, 3.8 T = {d_formula(100, 2):.2f} um vs Li numerical mode ~15 um (x{15/d_formula(100,2):.0f})")
print("   m = 100 and 500 GeV histograms at Lambda0 coincide (mode 50-80 um): m_Q independence already visible\n")

# ---- 2. FASER Fig.5 observed contour (by eye), GeV ----
faser = {0.3: 57, 0.5: 72, 1: 105, 2: 135, 3: 150, 5: 165, 10: 179, 20: 175, 30: 170, 50: 155, 100: 65}
d0 = (10, 1000, 107)  # keV range, GeV
run23 = {"B=0": (220, 340), "B=10": (170, 260), "B~80": (150, 200)}  # v3 S-8, tau = 0.1-0.5 us
print("2) Run-2+3 stopped-pair update (v3 S-8) vs existing FASER/D0 limit, per Lambda")
print("   Lambda[keV] FASER  D0   best_existing | B=0      B=10     B~80   (beats existing at low end?)")
for lam, mf in faser.items():
    md = d0[2] if d0[0] <= lam <= d0[1] else 0
    best = max(mf, md)
    flags = " ".join(f"{k}:{'yes' if lo > best else ('partly' if hi > best else 'no')}" for k, (lo, hi) in run23.items())
    print(f"   {lam:7.1f}   {mf:5d}  {md:4d}   {best:5d}        | {flags}")
print("   v3 Box A says FASER ~0.11-0.18 TeV 'across the range': true only for ~1-50 keV; 0.06-0.07 TeV at 0.3 and 100 keV.\n")

# ---- 3. gamma* table from R2 outputs ----
root = pathlib.Path(__file__).resolve().parents[1] / "figures"
pat = re.compile(r"gstar=([\d.]+) ev(\d): causal ([\d.e+]+) um \[(\d+)\].*\| Li\(x([\d.]+)\) ([\d.e+]+) um \[(\d+)\] ratio ([\d.]+) max\|dhit\| ([\d.e+]+) um max\|dn\| ([\d.e+]+) um \| \(")
rows = {}
for fn in ["R2_li_gamma_out.txt", "R2_li_gamma2_out.txt"]:
    for line in (root / fn).read_text().splitlines():
        m = pat.search(line)
        if not m:
            continue
        g, ev = float(m.group(1)), int(m.group(2))
        nc, nl = int(m.group(4)), int(m.group(7))
        rows[(g, ev)] = (float(m.group(8)), float(m.group(9)), float(m.group(10)), nc == nl, m.group(5))
print("3) Finest-step Li/causal per gamma* (R2 outputs)")
for g in sorted({k[0] for k in rows}):
    evs = [rows[k] for k in sorted(rows) if k[0] == g]
    r = [e[0] for e in evs]
    matched = [e for e in evs if e[3]]
    s = (f"{len(matched)}/{len(evs)} events with equal hit counts"
         + (f"; among them max|dhit| {max(e[1] for e in matched)/1e3:.2f} mm, max|dn| {max(e[2] for e in matched):.0f} um,"
            f" median ratio {statistics.median(e[0] for e in matched):.3f}" if matched else ""))
    print(f"   gamma*={g}: step x{evs[0][4]}, median {statistics.median(r):.3f}, range {min(r):.3f}-{max(r):.3f}; {s}")
