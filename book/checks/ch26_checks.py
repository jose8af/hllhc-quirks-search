#!/usr/bin/env python3
"""Checks for Chapter 26: the numbers and the small calculations of the chapter, recomputed from tracked study files.

Every test recomputes something (a ratio, a quantile, a sign test, a pooled statistic, a toy) and compares it with
what the chapter says. Exits nonzero on any FAIL.
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta, binom, norm

TT = Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search/stage2_C001_quirks/theory_track")
A = TT / "data/acts_stage4/analysis/C12FC_v1"
P1 = json.load(open(TT / "sim/stage3/results/P1.json"))
P2 = json.load(open(TT / "sim/stage3/results/P2.json"))
PP = json.load(open(TT / "sim/stage3/results/P2_points.json"))
V2b = json.load(open(TT / "sim/stage3/results/V2b.json"))
S = json.load(open(TT / "data/acts_stage4/analysis/STAGE4_SUMMARY.json"))
ED = json.load(open(A / "edges_det.json"))["points"]
SEP = json.load(open(A / "sep_it_det.json"))["points"]
EFF = json.load(open(A / "signal_eff.json"))["a2"]["points"]
FP = S["fallback_points"]
HBARC = 0.19733  # GeV fm
fails = 0


def check(name, ok, detail=""):
    global fails
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        fails += 1


def near(a, b, tol):
    return abs(a - b) <= tol


def cp(k, n, cl=0.6827):
    al = 1 - cl
    lo = 0.0 if k == 0 else beta.ppf(al / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - al / 2, k + 1, n - k)
    return lo, hi


def sign_p(a, b):
    n = a + b
    return min(1.0, 2 * binom.sf(max(a, b) - 1, n, 0.5))


PTS = ["F_m200", "F_m500", "F_m1000", "F_m1500", "S_m500"]

# ---- the law: eps_B and c
eps1 = 2.254e-4
C = P1["points"]["F_m500"]["by_lambda"]["L1"]["C_ev_median_MG"]
c1 = 1 / (math.log(1 / eps1) + C)
check("c at 1 keV, E 500 from eps_B and C (text 0.104)", near(c1, 0.104, 5e-4) and near(c1, P1["points"]["F_m500"]["by_lambda"]["L1"]["c_ev_median_MG"], 5e-4), f"c={c1:.4f}, C={C:.3f}")
# eps_B from first principles: q B / sigma, with q=e, in natural units
alpha = 1 / 137.036
e = math.sqrt(4 * math.pi * alpha)
GeV2_per_T = 1.95e-16  # 1 T = 195.35 eV^2 in Heaviside-Lorentz natural units
eps_calc = e * 3.8112 * GeV2_per_T / (1e-6) ** 2
check("eps_B at 1 keV in 3.8112 T recomputed (2.254e-4)", near(eps_calc, 2.254e-4, 3e-6), f"{eps_calc:.4e}")

# ---- thickness near 30 um at 1 keV for all masses; exponent about -1.8
vals = [P1["points"][p]["by_lambda"]["L1"]["Ds_B"]["median_um"] for p in PTS]
check("Ds_B at 1 keV about 30 um (28.7 to 33.9)", min(vals) > 28 and max(vals) < 35, str(np.round(vals, 1)))
pt = P1["points"]["F_m500"]["by_lambda"]
sl = math.log(pt["L5"]["Ds_B"]["median_um"] / pt["L1"]["Ds_B"]["median_um"]) / math.log(5)
check("log-log slope of Ds_B 1 to 5 keV about -1.8", near(sl, -1.8, 0.08), f"{sl:.3f}")

# ---- paired ratios: 0.990 to 1.002 for E >= 500 at 0.6-5 keV; 0.975 at 200 (0.966 belongs to 0.45 keV); 0.947 scalar
LS = ["L0.6", "L1", "L2", "L3", "L5"]
r = [P1["points"][p]["by_lambda"][L]["Ds_B"]["paired_ratio_MG_model"] for p in ["F_m500", "F_m1000", "F_m1500"] for L in LS]
check("paired ratio E>=500: 0.990 to 1.002", round(min(r), 3) == 0.990 and round(max(r), 3) == 1.002, f"{min(r):.4f} {max(r):.4f}")
r2 = [P1["points"]["F_m200"]["by_lambda"][L]["Ds_B"]["paired_ratio_MG_model"] for L in LS]
check("paired ratio E 200 lowest over 0.6-5 keV is 0.975", round(min(r2), 3) == 0.975, f"{min(r2):.4f}")
r045 = P1["points"]["F_m200"]["by_lambda"]["L0.45"]["Ds_B"]["paired_ratio_MG_model"]
check("the paper's 0.966 is the 0.45 keV row, outside that range", round(r045, 3) in (0.966, 0.967), f"{r045:.4f}")
r3 = [P1["points"]["S_m500"]["by_lambda"][L]["Ds_B"]["paired_ratio_MG_model"] for L in LS]
check("paired ratio scalar lowest 0.947", round(min(r3), 3) == 0.947, f"{min(r3):.4f}")
g = P1["paired_model_by_gstar"]
hi_bin = [g[p]["bins"]["[1.6,100)"]["median_ratio"] for p in PTS if "[1.6,100)" in g[p]["bins"]]
lo_bin = [g[p]["bins"][b]["median_ratio"] for p in PTS for b in ("[1,1.05)", "[1.05,1.15)", "[1.15,1.3)") if b in g[p]["bins"]]
check("ratio within 0.8% of one for gamma*<1.3", max(abs(x - 1) for x in lo_bin) <= 0.0085, f"{max(abs(x-1) for x in lo_bin):.4f}")
check("ratio 0.89 to 0.93, 7 to 11% low in the median, for gamma* >= 1.6", min(hi_bin) > 0.885 and max(hi_bin) < 0.935, f"{min(hi_bin):.3f} {max(hi_bin):.3f}")
mid_bin = [g[p]["bins"]["[1.3,1.6)"]["median_ratio"] for p in PTS if "[1.3,1.6)" in g[p]["bins"]]
check("ratio 0.96 to 0.98, 2 to 4% low, at gamma* = 1.3 to 1.6, and the source says so", min(mid_bin) > 0.955 and max(mid_bin) < 0.985 and "0.96--0.98 at $\\gst=1.3$--1.6 and 0.89--0.93" in " ".join((TT / "paper/sections/04_truth_p1.tex").read_text().split()), f"{min(mid_bin):.3f} {max(mid_bin):.3f}")
gs = [g[p]["median_gstar"] for p in ["F_m200", "F_m500", "F_m1000", "F_m1500"]]
check("median gamma* 1.15 to 1.35 (fermions)", near(min(gs), 1.15, 0.005) and near(max(gs), 1.35, 0.005), str(np.round(gs, 3)))
check("median gamma* E 500 about 1.27", near(g["F_m500"]["median_gstar"], 1.27, 0.005), "")

# ---- which sample tested the law (round 2, A1): summed from the index of the truth-level production
IDX = json.load(open(TT / "data/sim_stage3/STAGE3_INDEX.json"))["points"]
def ev(camp, cfg, lam=None):
    return sum(p["n_events"] for k, p in IDX.items() if k.split("/")[0] == camp and p["cfg"] == cfg and (lam is None or p["lam_keV"] == lam))
prod = sum(p["n_events"] for k, p in IDX.items() if k.split("/")[0] != "xover")
check("production holds 218571 events", prod == 218571, str(prod))
check("most of the production has field and material together", 0.5 < (ev("p1", "BM") + ev("p2", "BM")) / prod < 0.8, f"{(ev('p1','BM')+ev('p2','BM'))/prod:.3f}")
check("the pile-up grid (p2) has only field and material: no field-only run", {p["cfg"] for k, p in IDX.items() if k.startswith("p2/")} == {"BM"}, "")
check("P1 grid: B 9800, B2 9000, M 11000, BM 11000", (ev("p1", "B"), ev("p1", "B2"), ev("p1", "M"), ev("p1", "BM")) == (9800, 9000, 11000, 11000), "")
b2lams = sorted({p["lam_keV"] for k, p in IDX.items() if k.startswith("p1/") and p["cfg"] == "B2"})
check("half field only up to 5 keV: 5 points x 6 Lambda x 300", max(b2lams) == 5.0 and len(b2lams) == 6 and all(p["n_events"] == 300 for k, p in IDX.items() if k.startswith("p1/") and p["cfg"] == "B2"), str(b2lams))
check("300 events at E 500, 1 keV in P1.json", P1["points"]["F_m500"]["by_lambda"]["L1"]["n_events"] == 300, "")
hi = [p for k, p in IDX.items() if k.startswith("p1/") and p["cfg"] == "BM" and p["lam_keV"] >= 7]
check("200 events per point at 7 and 10 keV, all five points with field and material", len(hi) == 10 and all(p["n_events"] == 200 for p in hi), "")
check("at 7 and 10 keV fewer configurations: field-only at two points of five, no half field", ev("p1", "B", 7.0) == 400 and ev("p1", "B", 10.0) == 400 and ev("p1", "B2", 7.0) == 0, "")
check("the source says the P1 grid is 300 per point inside the production", "218\\,571$ events" in (TT / "paper/sections/04_truth_p1.tex").read_text() and "300 events per point (200 at 7 and $10\\keV$)" in (TT / "paper/sections/04_truth_p1.tex").read_text().replace("\n", " "), "")

# ---- the failed gate
gate = float(re.search(r"<= ([\d.]+) % of median", V2b["criteria"]).group(1))
rel = {p: 100 * P1["points"][p]["by_lambda"]["L1"]["c"]["Dc_pop"] / P1["points"][p]["by_lambda"]["L1"]["c"]["median_c_ev_MG"] for p in PTS}
nf = sum(v > gate for v in rel.values())
check("gate is 1.5%", gate == 1.5, "")
check("gate fails at three of five points", nf == 3, str({k: round(v, 2) for k, v in rel.items()}))
check("V2b stored as not passed", V2b["PASS"] is False, "")
pm = [abs(V2b["points"][p]["by_lambda"]["L1"]["paired_median_diff"] / V2b["points"][p]["by_lambda"]["L1"]["median_c_ev"]) for p in PTS]
check("gate sample: median paired difference of c within 1% at 1 keV, all five points", max(pm) < 0.01, f"max {100*max(pm):.2f}%")
rv = P1["v2b_revisit"]
bl = rv["regime_split"]["1-2 keV (scatter only)"]
check("pooled 1-2 keV excess +1.71 +- 0.29%, toy +2.04%", near(100 * bl["rel_excess_weighted_mean"], 1.71, 0.01) and near(100 * bl["rel_excess_weighted_err"], 0.29, 0.01) and near(100 * bl["zero_median_sym_rel_mean"], 2.04, 0.01), "")
b35 = rv["regime_split"]["3-5 keV (k_B-ordered excess)"]
check("3-5 keV excess +6.2 +- 0.5%", near(100 * b35["rel_excess_weighted_mean"], 6.2, 0.05) and near(100 * b35["rel_excess_weighted_err"], 0.45, 0.02), "")
val = (TT / "sim/stage3/VALIDATION.md").read_text()
check("field-off run: paired +8.6 +- 4.2% on 160 events, and 8.6/4.2 is 2.1 sigma", "+8.6 ± 4.2 % for all" in val and "160 events (2.1σ)" in val and near(8.6 / 4.2, 2.05, 0.01), "")
p04 = (TT / "paper/sections/04_truth_p1.tex").read_text()
check("field-off run: +1.8 +- 0.7 against +9.7 +- 1.3 in the source", r"$+1.8\pm0.7\%$ against $+9.7\pm1.3\%$" in p04, "")

# ---- floor and crossover
ms = {p: [P1["points"][p]["by_lambda"][L]["Ds_MS"]["median_um"] for L in ["L0.45", "L0.6", "L1", "L2", "L3", "L5", "L7", "L10"] if "Ds_MS" in P1["points"][p]["by_lambda"][L]] for p in PTS}
check("floor at 200 GeV about 10 um", 9 < np.median(ms["F_m200"]) < 12, f"{np.median(ms['F_m200']):.1f}")
check("floor at 1500 GeV within 17-29 um", min(ms["F_m1500"]) > 17 and max(ms["F_m1500"]) < 29, f"{min(ms['F_m1500']):.1f} {max(ms['F_m1500']):.1f}")
xc = P1["B_MS_crossover_keV"]
exp = {"F_m200": 1.91, "F_m500": 1.50, "F_m1000": 1.25, "F_m1500": 1.16, "S_m500": 1.59}
check("crossover table", all(near(xc[k], v, 0.006) for k, v in exp.items()), str({k: round(v, 3) for k, v in xc.items()}))
# Crossover by interpolation: Ds_B falls below Ds_MS where stated (E 500)
lamv, dB, dS = [], [], []
for L in ["L1", "L2"]:
    lamv.append(float(L[1:])); dB.append(pt[L]["Ds_B"]["median_um"]); dS.append(pt[L]["Ds_MS"]["median_um"])
x = np.interp(0, np.log(np.array(dB) / np.array(dS))[::-1], np.log(lamv)[::-1])
check("crossover E 500 by own interpolation near 1.5 keV", 1.35 < math.exp(x) < 1.65, f"{math.exp(x):.2f}")
rq = S["p1"]["r_q_by_lambda_band"]["1-3 keV"]
check("below quadrature 0.80 to 0.97 at 1-3 keV", near(rq["min"], 0.80, 0.005) and near(rq["max"], 0.97, 0.005), str(rq))
res = [float(x) for x in re.search(r"resolution (\d+)-(\d+) um", S["p1"]["detector_level"]).groups()]
check("resolution 23 to 30 um", res == [23.0, 30.0], str(res))
plan = (TT / "acts/stage4/plan.md").read_text()
check("resolution is a planning estimate, never measured", "s_eff ≈ 23-30 µm" in plan and "NOT MEASURED" in S["p1"]["detector_level"], "")

# ---- the ruler
m, lam = 500.0, 2e-6
l0 = m / lam**2 * HBARC * 1e-15 * 100
check("l0 at E 500, 2 keV is 2.47 cm", near(l0, 2.47, 0.01), f"{l0:.3f}")
lmax = 2 * (1.27 - 1) * l0
check("lmax from gamma*=1.27 is 1.3 cm", near(lmax, 1.33, 0.03), f"{lmax:.3f}")
lst = PP["F_m500/L2"]["lmax_med_cm"]["value"]
sepv = PP["F_m500/L2"]["sep_IT_med_um"]["value"]
check("stored median lmax 1.43 cm, s_IT 7.0 mm", near(lst, 1.43, 0.005) and near(sepv / 1000, 7.0, 0.02), f"{lst:.3f} {sepv/1000:.3f}")
check("ratio s_IT/lmax about half", near(sepv / 10000 / lst, 0.49, 0.01), f"{sepv/10000/lst:.3f}")
slopes = []
for p in P2["sep_IT_handle"]:
    h = P2["sep_IT_handle"][p]
    slopes.append(h["loglog_slope_1to30keV"])
    # own fit
    x = np.array(h["lam_keV"]); y = np.array(h["sep_IT_med_um"])
    mk = (x >= 1) & (x <= 30)
    own = np.polyfit(np.log(x[mk]), np.log(y[mk]), 1)[0]
    if abs(own - slopes[-1]) > 0.05:
        check(f"own s_IT slope fit for {p}", False, f"{own:.3f} vs {slopes[-1]:.3f}")
check("s_IT slope -1.985 to -2.022", near(max(slopes), -1.985, 0.002) and near(min(slopes), -2.022, 0.002), str(np.round(slopes, 3)))
h = P2["sep_IT_handle"]["F_m1000"]
d = dict(zip(h["lam_keV"], h["sep_IT_med_um"]))
check("E 1000: 38.5 mm at 1 keV, 95 um at 20 keV", near(d[1.0] / 1000, 38.5, 0.05) and near(d[20.0], 95, 0.5), "")
rat = [x for p in PTS for l, x in zip(P2["sep_IT_handle"][p]["lam_keV"], P2["sep_IT_handle"][p]["ratio_sep_to_lmax_med"]) if l > 1.0]
check("s_IT/lmax mostly 0.5 to 0.6 above 1 keV", 0.5 <= np.median(rat) <= 0.6, f"median {np.median(rat):.3f}, range {min(rat):.2f}-{max(rat):.2f}")

# ---- window table
TAB = {"F|200": (0.43, 0.61, 1.05, 4.70, 12.8), "F|500": (0.63, 0.65, 1.03, 5.38, 16.4), "F|1000": (0.68, 0.76, 1.05, 5.89, 19.4),
       "F|1500": (0.78, 0.71, 1.10, 6.05, 19.8), "S|500": (0.78, 0.85, 1.22, 6.60, 22.9)}
ok = True
for k, t in TAB.items():
    a1, a2 = ED[f"A1|{k}"], ED[f"A2|{k}"]
    tr = a1["truth"]
    got = (tr["lower_lmax_RIT_closed"]["value"], a1["R04"]["lower"]["value"], a2["R04"]["lower"]["value"], a1["R04"]["upper"]["value"], tr["upper_merge100_hit"]["value"])
    ok &= all(near(g_, v, 0.0051 if v < 10 else 0.051) for g_, v in zip(got, t))
    ok &= a2["R04"]["upper"]["value"] is None
check("edges table reproduces edges_det.json", ok, "")
nosc = [ED[f"A1|{k}"]["truth"]["lower_Nosc1_closed"]["value"] for k in TAB]
check("one swing at 0.28 to 0.33 keV (all masses in P2)", 0.27 < min(nosc) and max(nosc) < 0.335, str(np.round(nosc, 3)))
up_ratio = [TAB[k][4] / TAB[k][3] for k in TAB]
check("upper-edge miss 2.7 to 3.5", near(min(up_ratio), 2.7, 0.06) and near(max(up_ratio), 3.5, 0.06), str(np.round(up_ratio, 2)))
check("E 200 lower edge 1.4 times truth", near(TAB["F|200"][1] / TAB["F|200"][0], 1.4, 0.03), "")
o = [TAB[k][1] / TAB[k][0] for k in TAB if k != "F|200"]
check("other lower edges within about 10% of truth", min(o) > 0.88 and max(o) < 1.12, str(np.round(o, 2)))

# ---- Chapter 25's event: 3 of 200
q = EFF["A2|F|200|0.45|BM"]
check("E 200, 0.45 keV: 3/200 at R04", q["ladder"]["R04_IP2>=7"]["k"] == 3 and q["n_den"] == 200, "")
check("sample median lmax 13.1 cm and 2.3 swings", near(PP["F_m200/L0.45"]["lmax_med_cm"]["value"], 13.1, 0.05) and near(PP["F_m200/L0.45"]["N_osc_med"]["value"], 2.3, 0.02), "")
# the window of Chapter 25 against that sample. Only medians of lmax are stored, so the wide part is bounded through gamma*.
Wc_cm = json.load(open(TT / "acts/stage4/frozen_inputs.json"))["w_c_mm"] / 10
half = PP["F_m200/L0.45"]["lmax_med_cm"]["value"] / 2
check("median pair reaches 6.6 cm, inside but close to the 7.5 cm window", near(half, 6.6, 0.05) and near(Wc_cm, 7.5, 1e-9) and half < Wc_cm, f"{half:.2f}")
l0_200 = 200.0 / (0.45e-6) ** 2 * HBARC * 1e-15 * 100
g_edge = 1 + 2 * Wc_cm / (2 * l0_200)  # lmax = 2 (gamma* - 1) l0 equals 2 W_c here
bn = P1["paired_model_by_gstar"]["F_m200"]["bins"]
nall = sum(v["n"] for v in bn.values())
f_wide = bn["[1.6,100)"]["n"] / nall
check("a wide part exists: at least 30% of E 200 pairs have gamma* >= 1.6 > the window's gamma*", g_edge < 1.6 and f_wide >= 0.29, f"gamma_edge {g_edge:.3f}, f {f_wide:.3f}")
# no pile-up against pile-up on the same rows: cmp_all.txt, not the all-eta edges_det values
CMP = {r["point"]: r for r in map(json.loads, (TT / "data/acts_stage4/investigation/cmp_all.txt").read_text().splitlines())}
c0 = CMP["p2_F_m200_L0.45_BM"]
n14, n3 = c0["both"] + c0["A1only"], c0["both"] + c0["A2only"]
check("same 200 rows at E 200, 0.45 keV: 7% (14 rows) without pile-up, 1.5% (3 rows) with", c0["n_common"] == 200 and near(c0["eps_A1_common"], 0.07, 1e-9) and near(c0["eps_A2_common"], 0.015, 1e-9) and n14 == 14 and n3 == 3, f"{n14} {n3}")
check("last factor on the same rows is about five (14/3 = 4.7)", near(n14 / n3, 4.67, 0.01), f"{n14/n3:.2f}")
check("the old 5% was on a different denominator: all eta, 463 rows", c0["n_A1"] == 463 and near(c0["eps_A1_all"], 0.0497, 5e-4), "")
# the event of Chapter 25 against its sample (index 16 of the stored candidates)
OB = np.load(A / "signal_obs_a2.npz", allow_pickle=True)
DI = np.load(A / "event_display.npz", allow_pickle=True)
iev, keepd = 16, DI["cls"] < 2
ud = np.c_[DI["x"][keepd], DI["y"][keepd], DI["z"][keepd]].astype(float) - OB["pv"][iev]
n2ev = np.cross(OB["normal"][iev], OB["axis"][iev])
isqd = DI["cls"][keepd] == 1
rd = np.hypot(DI["x"][keepd].astype(float), DI["y"][keepd].astype(float))
u2d = ud @ n2ev
wq = np.abs(u2d[isqd]).max()
check("largest distance of a quirk hit from the axis is 9.8 mm, a tilt and not a width", near(wq, 9.8, 0.05), f"{wq:.2f} mm")
sep_d = [abs(np.diff(u2d[isqd & (np.round(rd, 1) == R)])[0]) for R in np.unique(np.round(rd[rd < 600], 1))]
check("ribbon about half a millimetre wide: at most 0.47 mm apart at the ten pixel and PS sensors", len(sep_d) == 10 and near(max(sep_d), 0.466, 0.002), f"{np.round(sep_d, 3)}")
slope_d = np.polyfit(ud[isqd] @ OB["axis"][iev], u2d[isqd], 1)[0]
check("the 9.8 mm comes from an axis 8 mrad off the line through the quirk hits", near(abs(slope_d), 8.08e-3, 1e-4), f"{slope_d*1e3:.2f} mrad")
check("M_est of that event is 367 GeV, below the physical 2 m_Q = 400 GeV", near(float(OB["M_est"][iev]), 366.6, 0.05) and str(OB["key"][iev]) == "A2|F|200|0.45|BM" and 0.9 < float(OB["M_est"][iev]) / 400 < 1, f"{float(OB['M_est'][iev]):.1f}")
# how far that bounds the swing: MET smearing of 25 GeV per component (Chapter 25) at +2 sigma, gamma* = M/(2 m_Q), lmax = 2 (gamma*-1) l0
_met_ev = float(OB["met"][iev])
_sig_ev = 25.0 / _met_ev
_g_ev = float(OB["M_est"][iev]) * (1 + 2 * _sig_ev) / 400.0
_lm_ev = 2 * (_g_ev - 1) * l0_200
check("MET smearing alone is a 10% error on M_est; at +2 sigma gamma* is about 1.1, lmax under 4 cm", near(_sig_ev, 0.10, 0.002) and 1.09 <= _g_ev <= 1.105 and 3.5 < _lm_ev < 4.0, f"{_sig_ev:.4f} {_g_ev:.4f} {_lm_ev:.2f} cm")
_g_ribbon = 1 + 0.047 / (2 * l0_200)
check("a swing as small as the 0.47 mm ribbon would need gamma*-1 about 1e-3, far below that bound", near(_g_ribbon - 1, 1.2e-3, 1e-4) and (_g_ev - 1) / (_g_ribbon - 1) > 50, f"{_g_ribbon - 1:.2e}")

# ---- efficiencies
K = list(FP)
eps_rfb = np.array([FP[k]["eps_rfb"] for k in K])
check("40 points", len(K) == 40, "")
check("fallback efficiency maximum 0.080", near(eps_rfb.max(), 0.08, 1e-6), "")
check("fallback efficiency zero at seven points", int((eps_rfb == 0).sum()) == 7, "")
ra = [FP[k]["eps_reporting_rungs"]["R_A"] for k in K if float(k.split("|")[3]) >= 1]
check("R04 efficiency 0.085 to 0.31 at 1-5 keV", near(min(ra), 0.085, 1e-3) and near(max(ra), 0.305, 1e-3), f"{min(ra):.3f} {max(ra):.3f}")
ktop = max((k for k in K if float(k.split("|")[3]) >= 1), key=lambda k: FP[k]["eps_reporting_rungs"]["R_A"])
etop, ntop = FP[ktop]["eps_reporting_rungs"]["R_A"], FP[ktop]["n_den"]
check("the 0.31 is at 3 keV with binomial error 0.03", float(ktop.split("|")[3]) == 3.0 and near(math.sqrt(etop * (1 - etop) / ntop), 0.03, 0.004), f"{ktop} {math.sqrt(etop*(1-etop)/ntop):.4f}")
inj = S["cited_investigations"]["a2fc_injob"]["points"]
fcen = [p["injob_eff_fckf_R04_central"]["n"] / p["injob_eff_fckf_R04"]["n"] for p in inj]
check("central fraction of the template rows 0.23 to 0.38 over nine points, about 0.3", len(fcen) == 9 and round(min(fcen), 2) == 0.23 and round(max(fcen), 2) == 0.38 and near(np.median(fcen), 0.31, 0.02), str(np.round(fcen, 3)))
check("V4-5 not run and V4-4 partial in the source", "finder cross-check (V4-5) was not run and the seed-threshold regression check (V4-4) is partial" in (TT / "paper/sections/12_limitations.tex").read_text().replace("\n", " "), "")
res_f = (TT / "acts/stage4/STAGE4_RESULTS.md").read_text()
tab_f = res_f[res_f.index("| Λ (keV) | E200 | E500 | E1000 | E1500 | Ẽ500 |"):res_f.index("With R04 also required")]
rows_f = {r[0]: [float(x) for x in r[1:] if x != "—"] for r in (re.findall(r"[\d.—]+", line) for line in re.findall(r"^\| \**[\d.]+\** \| .*$", tab_f, re.M))}
check("finder 0.90 to 0.96 at 1.5 to 2 keV, and 0.97 only for the scalar at 3 keV, from the results table", min(rows_f["1.5"] + rows_f["2"]) == 0.90 and max(rows_f["1.5"] + rows_f["2"]) == 0.96 and rows_f["3"][-1] == 0.97 and max(rows_f["3"][:-1]) < 0.9 and "$0.90$ to $0.96$" in Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search/book/chapters/ch26_signalresults.tex").read_text(), str(rows_f))
Sv = {m_: max(FP[k]["S_at_rfb"] for k in K if k.split("|")[1] == "F" and k.split("|")[2] == m_) for m_ in ("200", "500", "1000", "1500")}
check("max yield per mass 861, 87, 3.4, 0.29", near(Sv["200"], 861, 1) and near(Sv["500"], 87, 0.5) and near(Sv["1000"], 3.4, 0.05) and near(Sv["1500"], 0.29, 0.005), str(Sv))
n3 = sum(FP[k]["S_at_rfb"] >= 3 for k in K)
check("20 of 40 give three events with no background", n3 == 20, str(n3))
for k in K:
    p = FP[k]
    if abs(p["N_exp_3ab"] * p["eps_rfb"] - p["S_at_rfb"]) > 1e-6:
        check("S = N_exp eps at " + k, False, "")
        break
else:
    check("S = N_exp eps at all points", True, "")
# late-hit share
sh200 = [FP[k]["eps_SRT_rfb"] / FP[k]["eps_rfb"] for k in K if FP[k]["eps_rfb"] > 0 and k.split("|")[2] == "200"]
check("late-hit share at most 27% at 200 GeV", max(sh200) <= 0.28, f"{max(sh200):.3f}")
shhi = [FP[k]["eps_SRT_rfb"] / FP[k]["eps_rfb"] for k in K if FP[k]["eps_rfb"] > 0 and k.split("|")[2] != "200"]
check("late-hit share typically 30 to 70% at >=500 GeV", 0.3 <= np.quantile(shhi, 0.25) and np.quantile(shhi, 0.75) <= 0.7, f"quartiles {np.quantile(shhi, .25):.2f} {np.quantile(shhi, .75):.2f}")
# width admissibility: the chapter's formula with its smoothed Lambda_R gives the stored fallback at every point
_wpr = (TT / "acts/stage4/WP_RULE.md").read_text()
LR = {"F|200": 0.431, "F|500": 0.610, "F|1000": 0.709, "F|1500": 0.741, "S|500": 0.773}
_rowre = {"F|200": "F_m200", "F|500": "F_m500", "F|1000": "F_m1000", "F|1500": "F_m1500", "S|500": "S_m500"}
_stored = {k: float(re.search(rf"^\| {v} \| ([\d.]+) \|", _wpr, re.M).group(1)) for k, v in _rowre.items()}
check("smoothed Lambda_R 0.431, 0.610, 0.709, 0.741, 0.773 keV are the frozen rule's values", all(near(_stored[k], LR[k], 5e-4) for k in LR), str(_stored))


def k_adm(lam, lam_r):
    return max((k for k in range(5) if lam >= lam_r * 2 ** ((k + 1) / 2)), default=0)


_mis, _diff = [], []
for k_ in K:
    sp_, m_, l_ = k_.split("|")[1:4]
    got_ = k_adm(float(l_), _stored[f"{sp_}|{m_}"])
    want_ = int(re.match(r"FB(\d)", FP[k_]["r_fb"]).group(1))
    if got_ != want_ or got_ != FP[k_]["k_adm"]:
        _mis.append((k_, got_, want_))
    if k_adm(float(l_), TAB[f"{sp_}|{m_}"][0]) != got_:
        _diff.append(k_)
check("the width-cut formula with the smoothed Lambda_R reproduces r_fb at all 40 points", len(K) == 40 and not _mis, str(_mis))
check("the table's per-mass column would change the cut at exactly three points", len(_diff) == 3, str(_diff))
check("the smoothed values lie within 5% of the table's column", all(abs(LR[k] / TAB[k][0] - 1) <= 0.0501 for k in LR), str({k: round(LR[k] / TAB[k][0], 3) for k in LR}))
# Pile-up above no pile-up at >= 2 keV, E 500, on the same rows (no pile-up from cmp_all.txt; pile-up as plotted, with the reruns)
a2 = ED["A2|F|500"]
d1 = {l: CMP[f"p2_F_m500_L{l:g}_BM"]["eps_A1_common"] for l in a2["lam_keV"]}
d2 = dict(zip(a2["lam_keV"], a2["R04"]["eff"]))
check("E 500, same rows: pile-up above no pile-up at 2, 3, 5 keV", all(d2[l] > d1[l] for l in (2.0, 3.0, 5.0)), str([(d2[l], d1[l]) for l in (2.0, 3.0, 5.0)]))
check("E 500, same rows: pile-up still below at 1.5 keV (0.24 < 0.27)", near(d2[1.5], 0.24, 1e-9) and near(d1[1.5], 0.27, 1e-9) and d2[1.5] < d1[1.5], "")
check("E 500, same rows: pile-up below no pile-up at 0.85, 1 keV", all(d2[l] < d1[l] for l in (0.85, 1.0)), "")
check("E 500: all plotted no-pile-up values are on 200 common rows; plotted pile-up equals eps_A2_common below 3 keV", all(CMP[f"p2_F_m500_L{l:g}_BM"]["n_common"] == 200 for l in a2["lam_keV"]) and all(near(d2[l], CMP[f"p2_F_m500_L{l:g}_BM"]["eps_A2_common"], 1e-9) for l in a2["lam_keV"] if l < 3), "")
check("E 500: at 3 and 5 keV the plotted pile-up values are the full-chain reruns, not the fast path", near(d2[3.0], S["a2fc_revert"]["points"]["A2|F|500|3|BM"]["eps_R04_fullchain"], 1e-9) and near(d2[5.0], S["a2fc_revert"]["points"]["A2|F|500|5|BM"]["eps_R04_fullchain"], 1e-9) and d2[3.0] < CMP["p2_F_m500_L3_BM"]["eps_A2_common"], "")
# ---- status of the failed gate, stated per point
fail_pts = sorted(k for k, v in rel.items() if v > gate)
check("the gate fails at E 500, E 1500 and the scalar by +2.0, +2.1, +3.2%", fail_pts == ["F_m1500", "F_m500", "S_m500"] and [round(rel[k], 1) for k in ("F_m500", "F_m1500", "S_m500")] == [2.0, 2.1, 3.2], str({k: round(rel[k], 2) for k in fail_pts}))
check("2.2 to 2.4 sigma at the failing points in the source", "2.2--2.4$\\sigma$ at the three failing points" in p04.replace("\n", " "), "")
sig = {k: P1["points"][k]["by_lambda"]["L1"]["c"]["Dc_pop"] / P1["points"][k]["by_lambda"]["L1"]["c"]["sigma_Dc"] for k in fail_pts}
check("the same 2.2 to 2.4 sigma from the stored errors", all(2.1 < v < 2.5 for v in sig.values()), str({k: round(v, 2) for k, v in sig.items()}))
check("R(1/2) = 1 + c ln 2 agrees with the source's per-event definition", "c=[\\mathcal R(1/2)-1]/\\ln2" in p04, "")
check("the floor test is against double precision and was not done", "double-precision floor" in p04 and "was not done" in p04, "")

# ---- full chain
rvp = S["a2fc_revert"]
ag = rvp["paired_aggregate_other_8"]
check("sign test 84/20 reproduces 1.6e-10", near(sign_p(84, 20), 1.638e-10, 0.01e-10) and near(ag["R04"]["sign_test_p"], sign_p(84, 20), 1e-12), f"{sign_p(84,20):.3e}")
check("z for 84/20 is 6.3", near((84 - 52) / math.sqrt(26), 6.28, 0.01), "")
check("sign test 52/37 gives 0.14", near(sign_p(52, 37), 0.137, 0.001), f"{sign_p(52,37):.3f}")
check("sign test 50/33 gives 0.078", near(sign_p(50, 33), 0.078, 0.001), f"{sign_p(50,33):.3f}")
check("50 against 33 is R14 over the same eight points in the stored aggregate", ag["R14"]["numpy_only"] == 50 and ag["R14"]["fullchain_only"] == 33 and near(ag["R14"]["sign_test_p"], sign_p(50, 33), 1e-9), "")
check("sign test 63/39 gives 0.022", near(sign_p(63, 39), 0.022, 0.001), f"{sign_p(63,39):.3f}")
check("loss factors 0.83, 0.87", near(318 / 382, 0.83, 0.005) and near(101 / 116, 0.87, 0.005), "")
rp = rvp["points"]
check("the eight summed points are at 3 and 5 keV only", all(float(k.split("|")[3]) in (3.0, 5.0) for k in rp) and len([k for k in rp if k != "A2|F|500|3|BM"]) == 8, "")
drops = [1 - rp[k]["eps_R04_fullchain"] / rp[k]["eps_R04_numpy"] for k in rp]
check("nine revert points", len(rp) == 9, "")
check("E 200, 3 keV: fast path and full chain coincide at the fallback (the hidden ring of the figure's panel b)", rp["A2|F|200|3|BM"]["eps_rfb_numpy"] == rp["A2|F|200|3|BM"]["eps_rfb_fullchain"], f"{rp['A2|F|200|3|BM']['eps_rfb_fullchain']:.5f}")
check("R04 loss 5 to 30% at all nine", 0.04 < min(drops) and max(drops) < 0.31 and min(drops) > 0, str(np.round(drops, 3)))
e = rp["A2|F|500|3|BM"]
check("E 500, 3 keV: 0.145 to 0.055", near(e["eps_rfb_numpy"], 0.145, 1e-9) and near(e["eps_rfb_fullchain"], 0.055, 1e-9), "")
check("E 500, 3 keV R14: 22 to 4 of 200", round(e["eps_R14_numpy"] * 200) == 22 and round(e["eps_R14_fullchain"] * 200) == 4, "")
_invo = (TT / "acts/stage4/investigation/INV_A2FC_E500.md").read_text()
_pR14 = sum(math.comb(18, j) for j in range(18, 19)) * 2 / 2**18  # exact two-sided sign test, 18 against 0
_pFB = sum(math.comb(20, j) for j in range(19, 21)) * 2 / 2**20  # 19 against 1
check("outlier sign test, exact binomial sum: 18/0 gives 7.6e-6, 19/1 gives 4.0e-5, as recorded", near(_pR14, 7.6e-6, 0.05e-6) and near(_pFB, 4.0e-5, 0.05e-5) and near(sign_p(18, 0), _pR14, 1e-12) and near(sign_p(19, 1), _pFB, 1e-12) and "| R14 | 22 → 4 | 18/0 | 7.6e-6 |" in _invo and "| FB3 | 29 → 11 | 19/1 | 4.0e-5 |" in _invo, f"{_pR14:.3e} {_pFB:.3e}")
check("FB3 is this point's fallback: 29 and 11 of 200 are 0.145 and 0.055", FP["A2|F|500|3|BM"]["r_fb"].startswith("FB3") and near(29 / 200, e["eps_rfb_numpy"], 1e-9) and near(11 / 200, e["eps_rfb_fullchain"], 1e-9), FP["A2|F|500|3|BM"]["r_fb"])
check("look-elsewhere factor 9 to 30 gives about 1e-4 to 1e-3, as the study estimates", "look-elsewhere factor of about 9–30" in " ".join(_invo.split()) and "global p is about 1e-4 to 1e-3 [E]" in " ".join(_invo.split()) and 5e-5 < 9 * _pR14 < 1e-4 and 1e-3 < 30 * _pFB < 1.3e-3, f"{9 * _pR14:.2e} to {30 * _pFB:.2e}")
bp = rvp["fullchain_eps_systematic"]
check("best limit 790 to about 910 to 950", near(S["outcome"]["best_mu95_over_Nexp"]["value"], 790, 0.5) and near(bp["best_ratio_corrected_rfb"], 910, 5) and near(bp["best_ratio_corrected_R04"], 950, 5), f"{bp['best_ratio_corrected_rfb']:.0f} {bp['best_ratio_corrected_R04']:.0f}")
check("910 to 950 in the source", "910$--950" in (TT / "paper/sections/08_results_p2.tex").read_text(), "")
check("31 points stay on the fast path", rvp["n_points_numpy_A2"] == 31, "")

# ---- separation handle
vals = []
for k, v in SEP.items():
    p = k.split("|")
    if p[0] == "A2" and p[4] == "BM" and float(p[3]) >= 1.5 and v["n"] >= 10:
        vals.append(v["sep_det_median_mm"])
check("PU 200 separation about 18 to 26 mm at >=1.5 keV", 17.5 < min(vals) and max(vals) < 27, f"{min(vals):.1f} {max(vals):.1f}")
tv = [v["sep_truth_median_mm"] for k, v in SEP.items() if k.startswith("A2") and float(k.split("|")[3]) >= 1.5 and k.split("|")[4] == "BM"]
check("truth falls 23 to 0.6 mm", near(max(tv), 23, 1.5) and near(min(tv), 0.6, 0.06), f"{max(tv):.1f} {min(tv):.2f}")
check("no pile-up 6.9 vs 7.0 mm", near(SEP["A1|F|500|2|BM"]["sep_det_median_mm"], 6.9, 0.05) and near(SEP["A1|F|500|2|BM"]["sep_truth_median_mm"], 7.0, 0.05), "")
check("PU 200 flagged not measurable", S["p2_detector"]["sep_IT_det_pu200"]["measurable"] is False, "")
# the ruler without pile-up at the five points of the figure, 1.5 to 3 keV: ratio to the truth and its statistical error
_sep = {(sp_, m_, l_): SEP[f"A1|{sp_}|{m_}|{l_}|BM"] for sp_, m_ in (("F", 200), ("F", 500), ("F", 1000), ("F", 1500), ("S", 500)) for l_ in ("1.5", "2", "3")}
_sr = {k_: v_["sep_det_median_mm"] / v_["sep_truth_median_mm"] for k_, v_ in _sep.items()}
_se = {k_: v_["err_mm"] / v_["sep_truth_median_mm"] for k_, v_ in _sep.items()}
check("ruler without pile-up: ratio to truth 0.69 to 1.23 over the 15 values", len(_sr) == 15 and round(min(_sr.values()), 2) == 0.69 and round(max(_sr.values()), 2) == 1.23, f"{min(_sr.values()):.3f} {max(_sr.values()):.3f}")
check("ruler: statistical error on the ratio 8 to 21%", round(100 * min(_se.values())) == 8 and round(100 * max(_se.values())) == 21, f"{100*min(_se.values()):.1f} {100*max(_se.values()):.1f}")
check("ruler: E 1500 at 1.5 keV is 0.69 +- 0.12", round(_sr[("F", 1500, "1.5")], 2) == 0.69 and round(_se[("F", 1500, "1.5")], 2) == 0.12, f"{_sr[('F', 1500, '1.5')]:.3f} {_se[('F', 1500, '1.5')]:.3f}")
check("ruler: the stored ratios are wider than the summary's 10% (five of 15 outside), and the summary does say 10%", sum(abs(v_ - 1) > 0.10 for v_ in _sr.values()) == 5 and "within ≈ 10 % at 1.5–3 keV" in (TT / "acts/stage4/STAGE4_RESULTS.md").read_text(), str(sum(abs(v_ - 1) > 0.10 for v_ in _sr.values())))

# ---- mass handle, recomputed from the stored candidates
def ratios(name):
    z = np.load(A / name, allow_pickle=True)
    key, row, L, f, M, m_ = z["key"], z["row"], z["L"], z["f_ckf"], z["M_est"], z["m"]
    seen, out = set(), []
    for i in range(len(key)):
        k = str(key[i])
        if k.split("|")[4] != "BM" or not L[i][3] or not f[i] < 0.2 or (k, row[i]) in seen:
            continue
        seen.add((k, row[i]))
        if np.isfinite(M[i]):
            out.append(M[i] / m_[i])
    return np.array(out)


r1, r2 = ratios("signal_obs_a1.npz"), ratios("signal_obs_a2.npz")
check("no pile-up: 9551 events, median 2.46, none below 1.5", len(r1) == 9551 and near(np.median(r1), 2.46, 0.005) and (r1 < 1.5).sum() == 0, f"{np.median(r1):.3f} min {r1.min():.2f}")
check("pile-up 200: 850 events, median 2.26", len(r2) == 850 and near(np.median(r2), 2.26, 0.005), f"{np.median(r2):.3f}")
check("pile-up 200: 29% below 1.5, 19% below 0.5", near((r2 < 1.5).mean(), 0.29, 0.005) and near((r2 < 0.5).mean(), 0.19, 0.005), f"{(r2<1.5).mean():.3f} {(r2<0.5).mean():.3f}")


# the two pools differ: restrict the no-pile-up sample to the (species, mass, Lambda) of the 40 points, same selection
def ratios_on(name, keep):
    z = np.load(A / name, allow_pickle=True)
    key, row, L, f, M, m_ = z["key"], z["row"], z["L"], z["f_ckf"], z["M_est"], z["m"]
    seen, out, n = set(), [], 0
    for i in range(len(key)):
        k = str(key[i])
        p = k.split("|")
        if p[4] != "BM" or tuple(p[1:4]) not in keep or not L[i][3] or not f[i] < 0.2 or (k, row[i]) in seen:
            continue
        seen.add((k, row[i]))
        n += 1
        if np.isfinite(M[i]):
            out.append(M[i] / m_[i])
    return np.array(out), n


_keep40 = {tuple(k.split("|")[1:4]) for k in S["fallback_points"]}
_r140, _n140 = ratios_on("signal_obs_a1.npz", _keep40)
check("no pile-up on the 40 points: 2026 defined of 2443, median 2.52, minimum 1.77, none below 1.5", len(_keep40) == 40 and len(_r140) == 2026 and _n140 == 2443 and near(np.median(_r140), 2.52, 0.005) and near(_r140.min(), 1.77, 0.005) and (_r140 < 1.5).sum() == 0, f"{len(_r140)} of {_n140}, median {np.median(_r140):.3f}, min {_r140.min():.2f}")
_cmp = [json.loads(s_) for s_ in (TT / "data/acts_stage4/investigation/cmp_all.txt").read_text().splitlines()]
_nc = sum(r_["n_common"] for r_ in _cmp)
_na = sum(r_["eps_A1_common"] * r_["n_common"] for r_ in _cmp)
_nb = sum(r_["eps_A2_common"] * r_["n_common"] for r_ in _cmp)
check("same rows of the 40 points: 8000 rows; 1245 without pile-up, 1163 with it, a ratio of 0.93", len(_cmp) == 40 and _nc == 8000 and round(_na) == 1245 and round(_nb) == 1163 and near(_nb / _na, 0.934, 0.002), f"{len(_cmp)} points, {_nc} rows, {_na:.1f} {_nb:.1f} {_nb / _na:.3f}")
_panel = S["p2_detector"]["mass_observables"]["M_est_over_mQ_pooled"]["values"]["A2"]
_tex26 = Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search/book/chapters/ch26_signalresults.tex").read_text()
check("the panel's own sample: 1051 events, 850 with M_est; a different population from the 1163", _panel["n_events"] == 1051 and _panel["n_defined"] == 850 and "is $1051$, of which $850$ have $M_{\\rm est}$" in _tex26, f"{_panel['n_events']} {_panel['n_defined']}")
check("the fallback has no passes at 0.45 keV for E 500, as the caption of the efficiency figure says", FP["A2|F|500|0.45|BM"]["k_rfb"] == 0 and "At $0.45\\keV$ the fallback has no passes." in _tex26)
check("the finder table has no value for the scalar at 1.5 keV and has one at 2 keV", len(rows_f["1.5"]) == 4 and len(rows_f["2"]) == 5 and "the scalar has no value at $1.5\\keV$" in _tex26, str(rows_f["1.5"]))
_plan = (TT / "acts/stage4/plan.md").read_text()
check("the no-pile-up sample covers all 307 grid points", "A1 signal-only (no PU) | all 307 p2" in _plan)
_ker = (TT / "acts/stage4/finder/kernels.py").read_text()
_inv = (TT / "acts/stage4/investigation/INV_SIGNAL_EFF.md").read_text()
check("the seed's opening: sin of the angle between the two hit directions from the vertex above 1e-3", "sn = ncn / (na * nbn)" in _ker and "if sn < 1e-3:" in _ker and "seed degenerate" in _inv)
_wpr = (TT / "acts/stage4/WP_RULE.md").read_text()
check("the width cut stops at k = 4", "the largest k ∈ {0, …, 4} with Λ ≥ Λ_R(m)·2^{(k+1)/2}" in _wpr)
check("gamma* from 2.46 is 1.23", near(2.46 / 2, 1.23, 1e-9), "")
med = S["p2_detector"]["M_est_median_A2_GeV"]
check("median ordering 483, 1113, 2070, 3137", [round(med[k]) for k in ("F200", "F500", "F1000", "F1500")] == [483, 1113, 2070, 3137], str(med))
mo = S["p2_detector"]["mass_observables"]["A2"]["pooled_R04"]
q16 = [mo[k]["M_est_GeV"]["q16"] for k in mo]
check("q16 155 to 332 GeV", round(min(q16)) == 155 and round(max(q16)) == 332, str(q16))
fin = [1 - mo[k]["M_est_finite_fraction"] for k in mo]
check("undefined for 6 to 41%", near(min(fin), 0.06, 0.01) and near(max(fin), 0.41, 0.01), str(np.round(fin, 3)))
bm = S["p2_detector"]["mass_observables"]["A1"]["pooled_R04"]["F500"]["beta_tof"]["median"]
check("median beta_ToF at 500 GeV without pile-up 0.33", near(bm, 0.33, 0.005), str(bm))

# ---- Example 26.2 and Exercise 26.4: time of flight
C_M_NS = 0.299792
u = 1.36
t = u / C_M_NS
check("light takes 4.5 ns over 1.36 m", near(t, 4.54, 0.01), f"{t:.2f}")
check("beta 0.33 takes 13.7 ns", near(u / (0.33 * C_M_NS), 13.7, 0.05), "")
b = t / (t + 0.2)
bg = b / math.sqrt(1 - b**2)
Mest = 300 / bg
check("prompt hit: beta 0.96, beta gamma 3.3, M_est 90 GeV", near(b, 0.958, 0.002) and near(bg, 3.3, 0.05) and near(Mest, 90, 1.5), f"{b:.3f} {bg:.2f} {Mest:.1f}")
bg2 = 300 / 1000
b2 = bg2 / math.sqrt(1 + bg2**2)
dt = u / (b2 * C_M_NS) - t
check("Ex 26.4: delay for M_est=2 m_Q at 500 GeV is 11.3 ns, inside window", near(dt, 11.3, 0.1) and 5.955 < dt < 24.035, f"{dt:.2f} ns")
# Self-check of the formula: exact pair kinematics returns the pair mass
M_true, p_true = 1000.0, 400.0
bgt = p_true / M_true
check("eqn M_est returns the pair mass on exact kinematics", near(p_true / bgt, M_true, 1e-9), "")

# ---- the law's scaling at 500 GeV (no exercise now uses these; kept as tests of the stored prediction)
epsi3 = eps1 / 9
c3 = 1 / (math.log(1 / epsi3) + 1.2)
check("law at 3 keV: eps_B=2.50e-5, c(1 keV)=0.104, c(3 keV)=0.0848", near(epsi3, 2.504e-5, 1e-8) and near(c3, 0.0848, 3e-4), f"{epsi3:.3e} {c3:.4f}")
check("law: R(1/2)=1.072, exponent -1.79", near(1 + c1 * math.log(2), 1.072, 5e-4) and near(-2 + 2 * c1, -1.79, 3e-3), "")
check("law: stored prediction at 3 keV near 0.085", near(P1["points"]["F_m500"]["by_lambda"]["L3"]["c"]["median_c_ev_MG"], c3, 1e-3), "")

# ---- Exercise 26.1: median shift by simulation
rng = np.random.default_rng(26)
N = 4_000_000
g_ = rng.standard_normal(N)
cev = 0.1 * np.exp(0.2 * g_)
ct = cev + 0.02 * rng.standard_normal(N)
shift = np.median(ct) / np.median(cev) - 1
check("Ex 26.1: median shifts up by about 1%", 0.008 < shift < 0.012, f"{100*shift:.2f}%")
sym = 0.1 + 0.02 * g_
ct2 = sym + 0.02 * rng.standard_normal(N)
s2 = np.median(ct2) / np.median(sym) - 1
check("Ex 26.1: symmetric population, no shift", abs(s2) < 1e-3, f"{100*s2:.3f}%")

# ---- Exercise 26.2: exact intervals
check("Ex 26.2: CP68 for 9/200 is [0.030, 0.065]", near(cp(9, 200)[0], 0.0304, 2e-4) and near(cp(9, 200)[1], 0.0649, 2e-4), str(np.round(cp(9, 200), 4)))
check("Ex 26.2: agrees with stored interval", near(FP["A2|F|200|1.5|BM"]["eps_rfb_cp68"][0], cp(9, 200)[0], 3e-4), "")
check("Ex 26.2: CP68 for 11/200 is [0.039, 0.076]", near(cp(11, 200)[0], 0.039, 5e-4) and near(cp(11, 200)[1], 0.076, 5e-4), str(np.round(cp(11, 200), 4)))
check("Ex 26.2: S from 9/200 is 480 to 1030", near(1.58e4 * cp(9, 200)[0], 480, 5) and near(1.58e4 * cp(9, 200)[1], 1025, 8), f"{1.58e4*cp(9,200)[0]:.0f} {1.58e4*cp(9,200)[1]:.0f}")

# ---- Exercise 26.3: tails
pu = binom.sf(21, 200, 0.0525)
pl = binom.cdf(4, 200, 0.0525)
zu, zl = norm.isf(pu), norm.isf(pl)
check("Ex 26.3: 22 of 200 is about 3 sigma, 4 of 200 about 2 sigma", near(zu, 3.0, 0.3) and near(zl, 2.0, 0.3), f"p={pu:.2e} z={zu:.2f}; p={pl:.3f} z={zl:.2f}")

print("ALL PASS" if fails == 0 else f"{fails} FAILED")
sys.exit(1 if fails else 0)
