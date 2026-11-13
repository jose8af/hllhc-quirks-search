#!/usr/bin/env python3
"""Checks for Chapter 27: recompute the chapter's numbers and small calculations from tracked study files.

Every test recomputes something (a product of factors, a percentile, a CLs solution, a thinning weight, a toy) and
compares it with what the chapter says. Exits nonzero on any FAIL.
"""
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm, poisson

TT = Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search/stage2_C001_quirks/theory_track")
A = TT / "data/acts_stage4/analysis/C12FC_v1"
S = json.load(open(TT / "data/acts_stage4/analysis/STAGE4_SUMMARY.json"))
BS = json.load(open(A / "bsum_wp.json"))
BG = json.load(open(A / "background.json"))
FP = S["fallback_points"]
fails = 0


def check(name, ok, detail=""):
    global fails
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        fails += 1


def near(a, b, rel):
    return abs(a - b) <= rel * abs(b)


Nt = S["n_trig"]["value"]
G, T = BS["ladder"]["G"], BS["ladder"]["T"]
rung = {r["name"][:3]: r for r in G}
rungT = {r["name"][:3]: r for r in T}

# ---- budget
check("N_trig 4.08e7 and Z(nunu) 2.5e7", near(Nt, 4.08e7, 0.002) and near(BS["n_trig"]["breakdown"]["Znunu_j"]["N_trig"], 2.5e7, 0.01), f"{Nt:.4g}")
_res = (TT / "acts/stage4/STAGE4_RESULTS.md").read_text()
check("N_trig is an estimate as physics, generator-level Pythia, 5% veto loss, in the results file", "an ESTIMATE as physics" in _res and "generator-level" in _res and "5 % per-object veto inefficiency** [E]" in _res)
check("one fake per about 4e8 triggered", near(Nt / 0.11, 3.7e8, 0.01), f"{Nt/0.11:.3g}")
med = 0.11 * math.exp(-2.3)
check("median 0.011 at sigma 2.3", near(med, 0.011, 0.01), f"{med:.4f}")
need = med / Nt
check("2.7e-10 per trial, equals stored", near(need, 2.7e-10, 0.01) and near(need, S["pu_reach_per_trial_rho2"]["requirement_if_PU_takes_SRG_budget"], 0.01), f"{need:.3g}")
cols = BG["columns"]
check("172 false planes per trial at R04", near(cols[3]["B1_per_trial"], 172, 0.003), f"{cols[3]['B1_per_trial']:.2f}")
check("11.8 decades from 172 to the need", abs(math.log10(172 / need) - 11.8) < 0.05, f"{math.log10(172/need):.2f}")
check("48000 trials, 6000 at rho=2", S["samples"]["B1_trials"] == 48000 and S["samples"]["B2_trials"] == 6000)
check("35 direct at R07, zero at R08", cols[6]["B1_groups"] == 35 and cols[7]["B1_groups"] == 0)

# ---- thinning: Example, brute force over subsets
def weight_bruteforce(layers, q, need_per_layer=2):
    """layers: list of lists of interaction ids (one id per hit). Sum over subsets of interactions."""
    ids = sorted({i for L in layers for i in L})
    tot = 0.0
    for keep in itertools.product([0, 1], repeat=len(ids)):
        K = {i for i, k in zip(ids, keep) if k}
        if all(sum(h in K for h in L) >= need_per_layer for L in layers):
            tot += q ** sum(keep) * (1 - q) ** (len(ids) - sum(keep))
    return tot


# fewer layers for brute force of the 3-hit case: the layers are independent, so check per layer then take the power
L2 = [[2 * j, 2 * j + 1] for j in range(7)]
w14 = weight_bruteforce(L2, 0.5)
check("two hits per layer: w = 2^-14 = 6.1e-5", near(w14, 2 ** -14, 1e-12) and near(w14, 6.1e-5, 0.01), f"{w14:.3g}")
L3 = [[3 * j, 3 * j + 1, 3 * j + 2] for j in range(3)]
w3 = weight_bruteforce(L3, 0.5)
check("three hits on 3 layers: w = (1/2)^3 by brute force", near(w3, 0.5 ** 3, 1e-12), f"{w3:.4f}")
check("three hits per layer: w=2^-7=7.8e-3, 128 times larger", near(2 ** -7, 7.8e-3, 0.002) and 2 ** -7 / 2 ** -14 == 128)
check("layer pass probability at q=1/2", near(3 * 0.25 * 0.5 + 0.125, 0.5, 1e-12))
check("2^-20/6000 = 1.7e-10, equals stored reach", near(2 ** -20 / 6000, 1.6e-10, 0.01) and near(1e-6 / 6000, S["pu_reach_per_trial_rho2"]["value"], 1e-6), f"{2**-20/6000:.3g}")

# a real toy: thinning from rho=2 predicts the rho=1 fake rate without bias, per event
rng = np.random.default_rng(27)
lam, nlay = 3.0, 3  # mean hits per layer in the window at rho=1; each interaction gives at most one hit
# rho=1 truth, closed form: each layer needs at least 2 hits
p1 = (1 - poisson.cdf(1, lam)) ** nlay
n_ev = 200000
counts = rng.poisson(2 * lam, size=(n_ev, nlay))
# weight of an event at rho=2 with q=1/2: per layer P(at least 2 of n survive)
pl = 1 - 0.5 ** counts - counts * 0.5 ** counts
w = np.prod(pl, axis=1)
est, err = w.mean(), w.std() / math.sqrt(n_ev)
direct = (rng.poisson(lam, size=(n_ev, nlay)) >= 2).all(axis=1)
check("toy: thinned estimate equals closed form (3 sigma)", abs(est - p1) < 3 * err, f"{est:.5f}+-{err:.5f} vs {p1:.5f}")
check("toy: direct count equals closed form (3 sigma)", abs(direct.mean() - p1) < 3 * direct.std() / math.sqrt(n_ev), f"{direct.mean():.5f}")

# ---- closure
cl = BG["closure"]
r1 = cl["T1"]["N_obs"] / cl["T1"]["N_pred"]
check("T1 counts 8234601 and 5489513, ratio 1.500", cl["T1"]["N_obs"] == 8234601 and round(cl["T1"]["N_pred"]) == 5489513 and near(r1, 1.500, 1e-3), f"{r1:.4f}")
check("T1 z = +52.8", near(cl["T1"]["z"], 52.8, 2e-3), f"{cl['T1']['z']:.2f}")
r2 = cl["T1w"]["N_obs"] / cl["T1w"]["N_pred"]
check("T1w ratio 1.606, z = +59.4", near(r2, 1.606, 1e-3) and near(cl["T1w"]["z"], 59.4, 2e-3), f"{r2:.4f}")
check("compounded 2.41", near(r1 * r2, 2.409, 1e-3) and near(r1 * r2, S["closure"]["compounded_ge_R05"], 1e-6), f"{r1*r2:.4f}")
pts = cl["trend"]["points"]
check("ratio 0.63 at R06, 0.39 at R07", abs(math.exp(pts[2]["ln_r"]) - 0.63) < 0.005 and abs(math.exp(pts[3]["ln_r"]) - 0.39) < 0.006)
# trend formula against the stored per-rung sigma
i0, sl = cl["trend"]["intercept_at_x0"], cl["trend"]["slope"]
check("trend coefficients 1.985, -0.361", near(i0, 1.985, 1e-3) and near(sl, -0.361, 2e-3))
# the fit behind them: weighted least squares on ln r against the rung number, weights from the stored errors
xs_t = np.array([p_["x"] for p_ in pts], float)
ys_t = np.array([p_["ln_r"] for p_ in pts])
es_t = np.array([p_["sig"] for p_ in pts])
sl_w, i0_w = np.polyfit(xs_t, ys_t, 1, w=1 / es_t)
sl_u, i0_u = np.polyfit(xs_t, ys_t, 1)
check("weighted fit to the stored points returns 1.985 and -0.361", near(i0_w, i0, 2e-3) and near(sl_w, sl, 2e-3), f"{i0_w:.4f} {sl_w:.4f}")
check("the weights matter: an unweighted fit does not return them", abs(sl_u - sl) > 0.1, f"{i0_u:.3f} {sl_u:.3f}")
check("rungs R04 to R07, errors about 1% at R04 to R06 and 17% at R07", list(xs_t) == [4, 5, 6, 7] and max(es_t[:3]) < 0.012 and min(es_t[:3]) > 0.007 and abs(es_t[3] - 0.17) < 0.002, str(np.round(es_t, 4)))
ok = True
for r in G:
    n = int(r["name"][1:3])
    ok &= abs(abs(i0 + sl * n) - r["terms"][0]["comps"]["trend"]) < 0.01
check("eqn trend reproduces stored sigma_trend at every rung", ok)
check("trend 1.26 at R09, 6.31 at R23", abs(abs(i0 + sl * 9) - 1.26) < 0.005 and abs(abs(i0 + sl * 23) - 6.31) < 0.005)
check("stored trend at R23 = 6.31", abs(rung["R23"]["terms"][0]["comps"]["trend"] - 6.31) < 0.005)
check("e^6.31 about 550", abs(math.exp(6.31) - 550) < 5, f"{math.exp(6.31):.0f}")
check("f_corr = 1.196", near(S["closure"]["c_factor"], 1.196, 5e-4))
check("T3 degenerate and not informative", BG["T3"]["degenerate"] and not BG["T3"]["informative"])
check("reach: rho=2 R06, direct R07", S["closure"]["reach"]["deepest_reachable_rho2"].startswith("R06") and S["closure"]["reach"]["deepest_B1_ge10"].startswith("R07"))

# ---- sigma_ln adds in quadrature
c9 = rung["R09"]["terms"][0]["comps"]
q = math.sqrt(sum(v ** 2 for v in c9.values()))
check("PU sigma_ln at R09 from its parts = 2.22", abs(q - 2.22) < 0.01, f"{q:.3f}")
check("trend and density leave 1.7", abs(math.hypot(c9["trend"], c9["density"]) - 1.7) < 0.01, f"{math.hypot(c9['trend'], c9['density']):.3f}")
check("median needed 0.02 at 1.7", abs(0.11 * math.exp(-1.7) - 0.02) < 0.0005)

# ---- SM and single-interaction
check("SM central 1.9e9 at R04", near(sum(t["value"] for t in rung["R04"]["terms"] if t["label"].startswith("SM")), 1.9e9, 0.03))
fr = S["sm_proxy_fraction_of_B_SM"].values()
check("proxies 15 to 45% of SM term", 0.14 < min(fr) < 0.16 and 0.43 < max(fr) < 0.45, f"{min(fr):.3f} {max(fr):.3f}")
cp = S["cprime"]
check("rates 30.3, 1.59, 0.38", abs(cp["pvpair"]["rate_t"] - 30.3) < 0.05 and abs(cp["dif"]["rate_t"] - 1.59) < 0.01 and abs(cp["gamma"]["rate_t"] - 0.38) < 0.005)
check("1.14 from exp(-m)=0.32", abs(-math.log(0.32) - 1.14) < 0.001, f"{-math.log(0.32):.4f}")
# Example: the decay-in-flight chain from its factors
Ndif = Nt * cp["dif"]["rate_t"] * cp["dif"]["f_pre"]
check("6.5e7 decays, 0.949 pass the hit-level requirement, leaving 6.2e7", near(Nt * cp["dif"]["rate_t"], 6.5e7, 0.005) and near(cp["dif"]["f_pre"], 0.949, 0.001) and near(Ndif, 6.2e7, 0.01), f"{Nt * cp['dif']['rate_t']:.3g} {Ndif:.3g}")
c = S["closure"]["c_factor"]
Bdif = Ndif * 81 / 500 * 1.14 / 81 * c
stored = S["statistics_reach"]["R09_p>1e-3"]["C' dif"]["central"]
check("chain gives stored decay-in-flight bound 1.7e5", near(Bdif, stored, 2e-3) and near(Bdif, 1.7e5, 0.01), f"{Bdif:.4g} vs {stored:.4g}")
Bdif40 = Ndif * 40 / 500 * 1.14 / 40 * c
check("the population cancels", near(Bdif40, Bdif, 1e-12))

# ---- the ladder table
tab = {"R04": (1.1e10, 1.94, 2.6e9, 7.5e10), "R06": (3.8e7, 1.36, 3.8e6, 1.5e8), "R07": (1.4e5, 1.53, 1.4e6, 2.0e6), "R08": (4.4e3, 1.92, 1.4e6, 1.4e6),
       "R09": (2.5e2, 2.22, 1.2e6, 1.2e6), "R14": (2.6e3, 5.95, 3.3e6, 2.7e6), "R23": (8.0e2, 8.12, 8.7e6, 6.3e6)}
for k, (pu, sg, bt, bg) in tab.items():
    t0 = rung[k]["terms"][0]
    sgc = math.sqrt(sum(v ** 2 for v in t0["comps"].values()))
    good = near(t0["value"], pu, 0.05) and abs(sgc - sg) < 0.01 and near(rungT[k]["B84"], bt, 0.05) and near(rung[k]["B84"], bg, 0.05)
    check(f"table row {k}", good, f"{t0['value']:.3g} {sgc:.2f} {rungT[k]['B84']:.3g} {rung[k]['B84']:.3g}")
largest = {}
for k in tab:
    largest[k] = max(rung[k]["terms"], key=lambda t: t["value"])
check("largest central term flat R09 to R23 (within 15%)", abs(rung["R23"]["terms"][13]["value"] / rung["R09"]["terms"][13]["value"] - 1) < 0.15 and all(abs(r["terms"][13]["value"] / rung["R09"]["terms"][13]["value"] - 1) < 0.15 for r in G[8:]) and rung["R09"]["terms"][13]["label"] == "C' dif")
check("largest term: pile-up at R04, R06", largest["R04"]["label"].startswith("PU") and largest["R06"]["label"].startswith("PU"))
check("largest term: decays in flight from R07", all(largest[k]["label"] == "C' dif" for k in ("R07", "R08", "R09", "R14", "R23")))
check("zero-count from R08: decays in flight", not largest["R07"]["zero_branch"] and all(largest[k]["zero_branch"] for k in ("R08", "R09", "R14", "R23")))
puc = {k: rung[k]["terms"][0]["value"] for k in tab}
check("pile-up falls 4.9 decades R04 to R07", abs(math.log10(puc["R04"] / puc["R07"]) - 4.9) < 0.02)
check("R09 pile-up bound below R08 and R11", puc["R09"] < puc["R08"] and puc["R09"] < rung["R11"]["terms"][0]["value"])
check("minimum 1.23e6 at R09, both categories", S["ladder"]["SR-G"]["min_B84_rung"].startswith("R09") and S["ladder"]["SR-T"]["min_B84_rung"].startswith("R09") and near(S["ladder"]["SR-G"]["min_B84"], 1.23e6, 0.005) and near(S["ladder"]["SR-T"]["min_B84"], 1.23e6, 0.005))
check("7.05 decades", abs(math.log10(S["ladder"]["SR-G"]["min_B84"] / 0.11) - 7.05) < 0.005)
check("B84 > 0.11 everywhere and no WP", all(r["B84"] > 0.11 for r in G + T) and S["outcome"]["wp_T"] is None and S["outcome"]["wp_G"] is None)
check("B84 climbs after R09 in general", rung["R10"]["B84"] > rung["R09"]["B84"] and rung["R23"]["B84"] > rung["R09"]["B84"])
def pu_total(r):
    return sum(t["value"] for t in r["terms"] if t["label"].startswith("PU"))


ratios = [pu_total(rung[k]) / pu_total(rungT[k]) for k in ("R04", "R05", "R06")]
check("late-hit has (0.6-3)e4 less pile-up, R04 to R06", 0.55e4 < min(ratios) and max(ratios) < 3.2e4, str([f"{x:.2g}" for x in ratios]))
pu23 = 803 * math.exp(8.12)
check("pile-up alone at R23 is 2.7e6", near(pu23, 2.7e6, 0.01), f"{pu23:.3g}")
pu_cols = BG["columns"]
ratio117 = pu_cols[10]["P_fact"] / pu_cols[10]["P_main"]
check("factor 117 between routes at R11", abs(ratio117 - 117) < 2, f"{ratio117:.1f}")
inv_s = (TT / "acts/stage4/investigation/INV_STATS_BKG.md").read_text()
chi2_main = (2 / 35) * (32 / 126) * (12 / 32)
check("main route's plane-fit rejection 0.0054 from its stored fractions", abs(chi2_main - 0.0054) < 5e-5 and "**0.0054**" in inv_s and "**1 → 1**" in inv_s, f"{chi2_main:.5f}")
check("the source classes the 117 a legitimate model difference", "legitimate model difference" in inv_s)
bs_07 = (TT / "paper/sections/07_backgrounds.tex").read_text()
check("helix and opening pass every pile-up record and earn no credit in the source", "pass every pile-up record and earn no credit" in bs_07.replace("\n", " "))
ft_t = cols[6]
check("R07 lies past thinning's reach: no groups at rho=2, reach false", ft_t["B2_groups"] == 0 and ft_t["reachable_rho2"] is False, str(ft_t["main_method"]))

# ---- reach
k_all = rung["R09"]["B84"] / 0.11
check("all bounded terms: about 1e7 times today's statistics", near(k_all, 1.1e7, 0.03), f"{k_all:.3g}")
ratTG = [rungT[f"R{n:02d}"]["B84"] / rung[f"R{n:02d}"]["B84"] for n in range(14, 24)]
check("past R13 late-hit is higher, by at most a factor of 2", min(ratTG) > 1.15 and max(ratTG) < 2.0, f"{min(ratTG):.2f} {max(ratTG):.2f}")
near_equal = [abs(rungT[f"R{n:02d}"]["B84"] / rung[f"R{n:02d}"]["B84"] - 1) for n in range(8, 14)]
check("R08 to R13: the two categories nearly agree (within 1%)", max(near_equal) < 0.01, f"{max(near_equal):.4f}")
check("late-hit sum has two pile-up terms, general one", all(sum(t["label"].startswith("PU") for t in rungT[f"R{n:02d}"]["terms"]) == 2 and sum(t["label"].startswith("PU") for t in rung[f"R{n:02d}"]["terms"]) == 1 for n in range(1, 24)))
c14 = [t["value"] for t in rungT["R14"]["terms"] if t["label"].startswith("PU")]
check("late-hit pile-up terms at R14 are 4194 and 2557", abs(c14[0] - 4194) < 1 and abs(c14[1] - 2557) < 1, str(c14))
# the parts of the pile-up width and why R04 stands above the direct count
es4 = BG["end_state"][3]
check("R04 stored per trial = direct upper envelope x 1.500", near(es4["P_per_trial"], es4["base"] * es4["closure_factor"], 1e-9) and near(es4["base"], cols[3]["B1_per_trial"], 1e-9) and near(es4["base"], max(cols[3]["P_main"], cols[3]["P_fact"]), 1e-9))
check("R04 estimate 1.1e10 against direct 7.0e9", near(rung["R04"]["terms"][0]["value"], 1.05e10, 0.01) and near(cols[3]["B1_per_trial"] * Nt, 7.0e9, 0.01), f"{cols[3]['B1_per_trial'] * Nt:.3g}")
c11 = rung["R11"]["terms"][0]["comps"]
check("model spread is ln 117 = 4.76 at R11", abs(math.log(BG["columns"][10]["P_fact"] / BG["columns"][10]["P_main"]) - c11["model_spread"]) < 0.01 and abs(c11["model_spread"] - 4.76) < 0.005, f"{c11['model_spread']:.3f}")
others = [max(r["terms"][0]["comps"][k] for r in G) for k in ("closure", "normalisation")]
check("closure and normalisation at most 0.47 (not drawn)", max(others) < 0.48, str(others))
sr = S["statistics_reach"]["R09_p>1e-3"]
check("decays in flight need 2.2e9, have 500", near(sr["C' dif"]["events_needed_alone"], 2.2e9, 0.02) and sr["C' dif"]["events_now"] == 500)
sdif = sr["C' dif"]["sigma_ln"]
ratio = 1.14 * c * math.exp(sdif) / 0.11
check("eqn nature: about 35, and equals stored need / nature", abs(ratio - 35) < 1 and near(sr["C' dif"]["events_needed_alone"] / Ndif, ratio, 0.01), f"{ratio:.1f}")
check("sigma 1.05 for decays in flight", abs(sdif - 1.05) < 0.005)
check("ideal ratio is 10", abs(1.14 / 0.11 - 10) < 0.5, f"{1.14/0.11:.1f}")
Npv = Nt * cp["pvpair"]["rate_t"] * cp["pvpair"]["f_pre"]
Nz = BS["n_trig"]["breakdown"]["Znunu_j"]["N_trig"] / BS["n_trig"]["breakdown"]["Znunu_j"]["f_presel"]
Ng = Nt * cp["gamma"]["rate_t"] * cp["gamma"]["f_pre"]
rpv = sr["C' pvpair"]["events_needed_alone"] / Npv
rz = sr["SM Znunu_j"]["events_needed_alone"] / Nz
rg = sr["C' gamma"]["events_needed_alone"] / Ng
rpu = S["samples"]["B1_trials"] * sr["PU_alone_B84"] / 0.11 / Nt
check("vertex pairs ratio 2", abs(rpv - 2) < 0.3, f"{rpv:.2f}")
check("others 7 to 25", abs(rg - 7) < 0.5 and abs(rpu - 25) < 0.5 and 7 < rz < 25, f"{rg:.1f} {rz:.1f} {rpu:.1f}")
check("pile-up alone 2.3e3 at R09", near(sr["PU_alone_B84"], 2.33e3, 0.01))
check("4.3 decades", abs(math.log10(sr["PU_alone_B84"] / 0.11) - 4.3) < 0.05, f"{math.log10(sr['PU_alone_B84']/0.11):.2f}")
trials = S["samples"]["B1_trials"] * sr["PU_alone_B84"] / 0.11
check("about 1e9 trials", near(trials, 1.0e9, 0.03), f"{trials:.3g}")
cpuh = trials / 4 * 42 / 3600
check("3e6 CPU-hours", near(cpuh, 3e6, 0.05), f"{cpuh:.3g}")

# ---- the limit: one-bin CLs
def s95_exact(n, Bm, sig, cl=0.05):
    den = norm.cdf(math.log(n / Bm) / sig)
    f = lambda s: norm.cdf(math.log((n - s) / Bm) / sig) / den - cl
    return brentq(f, 1e-9 * n, n * (1 - 1e-14))


p = FP["A2|F|200|1.5|BM"]
Bm, B84 = p["B_median_rfb"]["G"], p["B84_rfb"]["G"]
sg = math.log(B84 / Bm)
eps = p["eps_rfb"]
check("best point: k/n, S, N_exp, mu95, ratio", p["k_rfb"] == 9 and p["n_den"] == 200 and near(p["S_at_rfb"], 710, 2e-3) and near(p["N_exp_3ab"], 1.58e4, 2e-3) and near(p["mu95_toys_events"], 1.25e7, 5e-3) and near(p["mu95_over_Nexp"], 790, 2e-3))
check("late-hit efficiency zero", p["eps_SRT_rfb"] == 0)
check("B_m 5.91e5, B84 8.87e6, sigma 2.71, factor 15", near(Bm, 5.91e5, 2e-3) and near(B84, 8.87e6, 2e-3) and abs(sg - 2.71) < 0.005 and abs(B84 / Bm - 15) < 0.1, f"{sg:.3f}")
check("Poisson error about 770", abs(math.sqrt(Bm) - 770) < 5, f"{math.sqrt(Bm):.0f}")
closed = Bm * (1 - math.exp(-1.96 * sg))
check("closed form equals numerical CLs solution", near(closed, s95_exact(Bm, Bm, sg), 1e-3), f"{closed:.5g}")
check("0.995 B_m", abs(closed / Bm - 0.995) < 0.0006, f"{closed/Bm:.4f}")
mu = closed / eps
check("mu95 estimate 1.31e7 = stored asymptotic", near(mu, 1.31e7, 3e-3) and near(mu, p["mu95_asymptotic_events"], 3e-3), f"{mu:.4g}")
check("5% above toys", abs(mu / p["mu95_toys_events"] - 1.05) < 0.005, f"{mu/p['mu95_toys_events']:.3f}")
lo = s95_exact(Bm * math.exp(-sg), Bm, sg) / eps
hi = s95_exact(Bm * math.exp(sg), Bm, sg) / eps
check("band [8.6e5, 2.0e8] against toys [8.6e5, 1.9e8]", near(lo, 8.6e5, 0.01) and near(hi, 2.0e8, 0.02) and near(p["mu95_toys_band1s"][0], 8.6e5, 0.01) and near(p["mu95_toys_band1s"][1], 1.9e8, 0.03), f"{lo:.3g} {hi:.3g}")
# a real toy of the same statement with Poisson noise: the limit from a hybrid CLs on the count
ntoy = 400000
rng = np.random.default_rng(2727)
bs = Bm * np.exp(sg * rng.standard_normal(ntoy))
nb = rng.poisson(bs)
def cls_toy(s, nobs):
    return (rng.poisson(bs + s) <= nobs).mean() / (nb <= nobs).mean()
sols = brentq(lambda s: cls_toy(s, Bm) - 0.05, 0.5 * Bm, 0.99999 * Bm, xtol=1e-3 * Bm)
check("hybrid toy with Poisson noise agrees with the formula (2%)", near(sols, closed, 0.02), f"{sols:.4g}")
check("ratio about B_m / S = 830", abs(closed / p["S_at_rfb"] - 830) < 5, f"{closed/p['S_at_rfb']:.0f}")
check("sigma95 1.7e5 fb, sigma_norm 219", near(p["sigma95_fb"], 1.7e5, 0.02) and near(p["sigma_norm_fb"], 219, 2e-3))
check("eff 68% interval [0.030,0.065]", near(p["eps_rfb_cp68"][0], 0.030, 0.02) and near(p["eps_rfb_cp68"][1], 0.065, 0.01))
check("factor 1.5 either way", abs(p["eps_rfb_cp68"][1] / eps - 1.44) < 0.02 and abs(eps / p["eps_rfb_cp68"][0] - 1.48) < 0.02)
r95 = 790 * eps / p["eps_rfb_cp95"][1]
check("95% upper 0.084 gives 420", near(p["eps_rfb_cp95"][1], 0.084, 0.01) and abs(r95 - 420) < 8, f"{r95:.0f}")
check("exclusion needs eff about 36", abs(eps * 790 - 36) < 0.6, f"{eps*790:.1f}")
_fc = S["a2fc_revert"]["fullchain_eps_systematic"]
check("full chain about 910 to 950", abs(790 / 0.87 - 910) < 3 and abs(_fc["best_ratio_corrected_rfb"] - 910) < 5 and abs(_fc["best_ratio_corrected_R04"] - 950) < 5, f"{_fc['best_ratio_corrected_rfb']:.0f} {_fc['best_ratio_corrected_R04']:.0f}")
need_b = p["S_at_rfb"] / (1 - math.exp(-1.96))
check("exclusion needs background about 8e2 at sigma 1", abs(need_b - 826) < 3, f"{need_b:.0f}")
vals = [(k, v) for k, v in FP.items() if v["mu95_over_Nexp"]]
rs = sorted(v["mu95_over_Nexp"] for k, v in vals)
check("33 limits, 7 without", len(vals) == 33 and sum(1 for v in FP.values() if v["eps_rfb"] == 0) == 7)
check("second best 820, worst 6e7", abs(rs[1] - 820) < 3 and near(rs[-1], 6.0e7, 0.01))
check("none below 1", min(rs) > 1)
both = sum(1 for k, v in vals if 0 < v["eps_SRT_rfb"] < v["eps_rfb"])
check("23 points with signal in both categories", both == 23, str(both))
fb = S["fallback_B"]
all84 = [v[c]["B84"] for k, v in fb.items() for c in "TG" if "e>" not in k]
check("fallback B84 from 2.0e6 to 6.4e7", near(min(all84), 2.0e6, 0.02) and near(max(all84), 6.4e7, 0.01), f"{min(all84):.3g} {max(all84):.3g}")
check("FB3 width cut 9.4 mm has the smallest", near(fb["FB3&h>5&o>5"]["G"]["B84"], 2.0e6, 0.02))
_tex27 = (TT.parents[1] / "book/chapters/ch27_backgroundresults.tex").read_text()
check("the 6.4e7 is the general category alone: late-hit 3.5e6 with no width cut", near(fb["FB0&h>5&o>5"]["G"]["B84"], 6.4e7, 0.01) and near(fb["FB0&h>5&o>5"]["T"]["B84"], 3.5e6, 0.02) and "to $6.4\\times10^7$ (general) with no width cut" in _tex27, f"{fb['FB0&h>5&o>5']['T']['B84']:.3g}")
check("the table's p is defined in its caption", "$p$ is the core $\\chi^2$ probability of Table~\\ref{tab:25-ladder}." in _tex27)
check("median background about 6e5", near(Bm, 6e5, 0.02))
check("detector production 382 CPU-h, part of the 990 total", near(S["production"]["cpu_h_total"], 382, 0.01), f"{S['production']['cpu_h_total']}")

# ---- exercises
m95 = -math.log(0.05)
check("ex1: 1.14 and 3.00", abs(m95 - 3.0) < 0.01)
check("ex1: 95% version 4.4e5", near(Ndif * 3.0 / 500 * c, 4.4e5, 0.01), f"{Ndif*3.0/500*c:.3g}")
check("ex1: 5000 events gives 1.7e4", near(Bdif / 10, 1.7e4, 0.02))
check("ex2: 3^-20/6000 = 4.8e-14", near(3.0 ** -20 / 6000, 4.8e-14, 0.01), f"{3.0**-20/6000:.3g}")
check("ex2: about 3300 times further than rho=2", abs(1.5 ** 20 - 3300) < 50, f"{1.5**20:.0f}")
# Poisson thinning toy
xs = rng.binomial(rng.poisson(10.0, 500000), 0.3)
check("ex2: thinned Poisson has mean = var = q lambda", abs(xs.mean() - 3) < 0.02 and abs(xs.var() - 3) < 0.03, f"{xs.mean():.3f} {xs.var():.3f}")
p1k = FP["A2|F|200|1|BM"]
check("ex3: inputs match store", p1k["k_rfb"] == 4 and p1k["n_den"] == 188 and near(p1k["B_median_rfb"]["G"], 8.12e5, 2e-3) and near(p1k["B84_rfb"]["G"], 2.54e7, 2e-3) and p1k["eps_SRT_rfb"] == 0)
sg1 = math.log(2.54e7 / 8.12e5)
mu1 = 8.12e5 * (1 - math.exp(-1.96 * sg1)) / (4 / 188)
check("ex3: estimate 3.8e7 against stored 3.59e7", near(mu1, 3.8e7, 0.01) and near(p1k["mu95_toys_events"], 3.59e7, 2e-3), f"{mu1:.3g}")
check("ex3: B_m 826 for ratio one", abs(710 / (1 - math.exp(-1.96)) - 826) < 2)
yrs = 2.2e9 * 19 / 3600 / 8766
check("ex4: about 1300 CPU-years at 19 s per event", abs(yrs - 1300) < 50, f"{yrs:.0f}")

# ---- Example 27.routes: the two chains at R11, recomputed from the stored factors
_cols = json.loads((TT / "data/acts_stage4/analysis/C12FC_v1/background.json").read_text())["columns"]
_r11 = _cols[10]
check("routes: column 10 is R11", _r11["column"].startswith("R11"), _r11["column"])


def _prod(fs):
    out = 1.0
    for f_ in fs:
        out *= f_["used"]
    return out


_pf, _pm = _prod(_r11["fact_factors"]), _prod(_r11["main_factors"])
check("routes: factorisation chain multiplies to the stored 2.84e-5", near(_pf, _r11["P_fact"], 1e-6) and near(_pf, 2.84e-5, 2e-3), f"{_pf:.4g}")
check("routes: main chain multiplies to the stored 2.44e-7", near(_pm, _r11["P_main"], 1e-6) and near(_pm, 2.44e-7, 2e-3), f"{_pm:.4g}")
check("routes: 35/48000 x 1.14/35 x 1.196 is the factorisation value", near(35 / 48000 * 1.14 / 35 * 1.196, 2.84e-5, 2e-3))
check("routes: first factor of the factorisation chain is 35/48000", near(_r11["fact_factors"][0]["used"], 35 / 48000, 1e-6))
check("routes: main chain's plane-fit counts are 2/35, 32/126, 12/32", [(f_["N"], f_["M"]) for f_ in _r11["main_factors"][3:6]] == [(2.0, 35.0), (32.0, 126.0), (12.0, 32.0)])
check("routes: plane-fit rejection 0.0054", abs(2 / 35 * 32 / 126 * 12 / 32 - 0.0054) < 5e-5, f"{2/35*32/126*12/32:.5f}")
check("routes: ratio 117 and log 4.76", abs(_pf / _pm - 117) < 0.5 and abs(math.log(_pf / _pm) - 4.76) < 0.005, f"{_pf/_pm:.1f}")
# the whole main route as printed in the example, and the two sources of the ratio
_mf = _r11["main_factors"]
check("routes: main chain starts at the thinned 0.389 at R06, stored from the same column", _mf[0]["label"].startswith("P(R06") and abs(_mf[0]["used"] - 0.389) < 5e-4 and near(_mf[0]["used"], _cols[5]["P_thin"], 1e-6), f"{_mf[0]['used']:.4f} {_cols[5]['P_thin']:.4f}")
check("routes: then 35/11858 and the bound 1.14/35", (_mf[1]["N"], _mf[1]["M"]) == (35.0, 11858.0) and near(_mf[1]["used"], 35 / 11858, 1e-9) and _mf[2]["zero_bound"] and near(_mf[2]["used"], 1.14 / 35, 1e-9) and _mf[2]["M"] == 35.0)
_chain = 0.38948 * (35 / 11858) * (1.14 / 35) * (2 / 35 * 32 / 126 * 12 / 32) * 1.19636
check("routes: the printed chain reproduces the stored P_main", near(_chain, _r11["P_main"], 1e-4), f"{_chain:.4g}")
_at7m = _mf[0]["used"] * _mf[1]["used"]
_at7d = _r11["fact_factors"][0]["used"]
check("routes: at R07 the main route is 1.15e-3 against the direct 7.3e-4", near(_at7m, 1.15e-3, 2e-3) and near(_at7d, 7.3e-4, 2e-3), f"{_at7m:.4g} {_at7d:.4g}")
check("routes: those two sources make the whole ratio: (7.29e-4/1.15e-3)/0.00544 = 116.5", near((_at7d / _at7m) / (2 / 35 * 32 / 126 * 12 / 32), _pf / _pm, 1e-6), f"{(_at7d / _at7m) / (2 / 35 * 32 / 126 * 12 / 32):.2f}")
# counting conventions in the pile-up figure: candidate counts below R04, distinct hit sets from R04
_dt = [_cols[i_]["B1_per_trial"] / _cols[i_]["P_thin"] for i_ in range(7)]
check("direct over thinned: below one at R01 to R03 (candidate counts); 1.50, 1.61, 0.63, 0.39 from R04", all(v_ < 1 for v_ in _dt[:3]) and [round(v_, 2) for v_ in _dt[3:7]] == [1.5, 1.61, 0.63, 0.39], str(np.round(_dt, 3)))
_wpr = (TT / "acts/stage4/WP_RULE.md").read_text()
check("the rule: R01-R03 carry candidate counts, the per-hit-set convention governs from R04", "carry candidate (union) counts only" in _wpr and "over the rungs ≥ R04" in _wpr.replace("\n    ", " "))
_pu11 = json.loads((TT / "data/acts_stage4/analysis/C12FC_v1/bsum_wp.json").read_text())["ladder"]["G"][10]["terms"][0]
check("routes: 2.84e-5 x 4.08e7 x 2.41 is about 2.8e3, the general category's stored pile-up term at R11", _pu11["label"].startswith("PU R11") and near(2.84e-5 * 4.08e7 * 2.41, 2.8e3, 0.005) and near(_pu11["value"], 2.8e3, 0.005), f"{_pu11['value']:.0f}")

print("FAILED" if fails else "ALL PASS")
sys.exit(1 if fails else 0)
