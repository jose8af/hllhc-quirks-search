#!/usr/bin/env python3
"""Checks for Chapter 29, and the chapter's one new calculation: the reach against an assumed background.

The functions s95, yields and reach are the calculation; figure_src/ch29/exclusion.py imports them, so the plot and the
tests use one piece of code. Everything else recomputes a number of the chapter from a tracked file, or confirms that a
logged statement is in the named record. Run as a script it prints PASS or FAIL per test and exits nonzero on any FAIL.
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, stats

REPO = Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search")
TT = REPO / "stage2_C001_quirks/theory_track"
PH = REPO / "stage2_C001_quirks"
SUMMARY = TT / "data/acts_stage4/analysis/STAGE4_SUMMARY.json"
LAMBDAS = [0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5]
MASSES = [200, 500, 1000, 1500]


def cls_value(s, n, B, sigma, z=None, w=None):
    """CLs = P(N <= n | s + b) / P(N <= n | b), with b log-normal of median B and width sigma."""
    if sigma == 0 or B == 0:
        return stats.poisson.cdf(n, s + B) / stats.poisson.cdf(n, B)
    b = B * np.exp(sigma * z)
    return np.sum(w * stats.poisson.cdf(n, s + b)) / np.sum(w * stats.poisson.cdf(n, b))


def s95(B, sigma=0.0, cl=0.05):
    """Expected 95% CLs upper limit on signal events: one bin, median observed count, log-normal background.

    The observed count is the median of Poisson(B), so for B = 0 it is zero and s95 = -ln 0.05.
    The log-normal integral is done on a grid fine enough to resolve the step of the Poisson cumulative at large n.
    """
    n = stats.poisson.median(B) if B > 0 else 0
    z = w = None
    if sigma > 0 and B > 0:
        dz = min(0.02, 0.25 / (sigma * math.sqrt(max(n, 1.0))))
        z = np.arange(-8.0, 8.0 + dz, dz)
        w = np.exp(-0.5 * z * z)
    f = lambda s: cls_value(s, n, B, sigma, z, w) - cl  # noqa: E731
    hi = 3.0 + 4.0 * math.sqrt(B + 1) + 4.0 * B * (1 + sigma)
    return optimize.brentq(f, 1e-6, hi, xtol=1e-4 * max(1.0, math.sqrt(B)))


def load_summary():
    return json.load(open(SUMMARY))


def yields(fp=None, lumi_scale=1.0, sig_scale=1.0):
    """Best-Lambda signal count at the fallback per mass of E, from the stored S_at_rfb at 3 ab-1."""
    if fp is None:
        fp = load_summary()["fallback_points"]
    return {m: max(fp[f"A2|F|{m}|{l:g}|BM"]["S_at_rfb"] for l in LAMBDAS) * lumi_scale * sig_scale for m in MASSES}


def fixed_lambda_yields(fp, lam):
    return {m: fp[f"A2|F|{m}|{lam:g}|BM"]["S_at_rfb"] for m in MASSES}


def reach(limit, S):
    """Largest mass with S(m) >= limit, S log-linear in m between the stored masses. None below the lightest mass."""
    ms = sorted(S)
    if S[ms[0]] < limit:
        return None
    for a, b in zip(ms, ms[1:]):
        if S[b] < limit:
            return a + (b - a) * (math.log(S[a]) - math.log(limit)) / (math.log(S[a]) - math.log(S[b]))
    return float(ms[-1])


def curve_end(S0, sigma=0.0):
    """Largest median background with any reach: the B at which s95(B, sigma) equals the signal S0 at the lightest stored mass."""
    hi = 1e7 if sigma == 0 else 1e5
    return 10 ** optimize.brentq(lambda lb: s95(10 ** lb, sigma) - S0, 0.0, math.log10(hi), xtol=1e-4)


def external_edge(ext, lam_lo=LAMBDAS[0], lam_hi=LAMBDAS[-1]):
    """The heaviest mass of each published curve for E inside the grid's range of Lambda, from stage5/external_bounds.json."""
    return {k: max(p[0] for p in c["points"] if lam_lo <= p[1] <= lam_hi)
            for k, c in ext["curves"].items()
            if "E" in c["applies_to"] and any(lam_lo <= p[1] <= lam_hi for p in c["points"])}


def break_even(S0, sigma):
    """Largest median background whose expected limit still reaches a signal S0."""
    Bs = np.logspace(-3, 8, 111)
    last = 0.0
    for B in Bs:
        if s95(B, sigma) <= S0:
            last = B
        else:
            break
    lo, hi = last, last * 10 ** (11 / 110)
    for _ in range(14):
        mid = math.sqrt(lo * hi) if lo > 0 else hi / 2
        if s95(mid, sigma) <= S0:
            lo = mid
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    fails = 0

    def check(name, ok, detail=""):
        global fails
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
        if not ok:
            fails += 1

    def near(a, b, rel):
        return abs(a - b) <= rel * abs(b)

    S = load_summary()
    fp = S["fallback_points"]
    Y = yields(fp)
    TEX = (REPO / "book/chapters/ch29_account.tex").read_text()
    ANS = (REPO / "book/answers/ch29.tex").read_text()

    def tex_has(*needles):
        return all(n in TEX for n in needles)

    def src(rel):
        return (TT / rel).read_text()

    strat = (PH / "phase1_strategy/outputs/STRATEGY_DRAFT.md").read_text()
    nov = src("paper/P2_NOVELTY_AUDIT.md")
    log = src("LOG.md")
    plog = (PH / "LOG.md").read_text()
    res = src("acts/stage4/STAGE4_RESULTS.md")
    plan4 = src("acts/stage4/plan.md")
    _money = TEX[TEX.index("\\label{sec:29-money}"):TEX.index("\\label{sec:29-reach}")]
    _others = [r_ for r_ in ("fig:25-event", "fig:27-pileup", "fig:26-handles", "fig:28-budget") if "\\ref{" + r_ + "}" in _money]
    check("money plots: three drawn in that section, four others named, seven in all, and the substitute kept apart", _money.count("\\includegraphics{ch29/") == 3 and len(_others) == 4 and "Three of them follow" in _money and "which makes seven" in _money and "Four of them follow" not in TEX, f"{_money.count(chr(92) + 'includegraphics{ch29/')} and {len(_others)}")
    check("the wide-background limit is not said to forget the count", "no longer knows the count" not in TEX and "not with its Poisson fluctuation" in TEX)
    check("the barrel cut names the third 2S layer, and the rule's 0.94 is that layer's, needed from R14", "the third 2S layer, the one R14 needs, at $0.94$" in TEX and "TB2S L3 **0.94** (needed by N_2S2 ≥ 3, i.e. R14" in " ".join(src("acts/stage4/WP_RULE.md").split()))
    wpr = src("acts/stage4/WP_RULE.md")
    plan3 = src("sim/stage3/plan.md")
    rvw1 = src("acts/stage4/review/REVIEW_WP_RULE_R1.md")
    inve = src("acts/stage4/investigation/INV_SIGNAL_EFF.md")
    con = src("paper/sections/13_conclusions.tex")
    lim = src("paper/sections/12_limitations.tex")
    p02 = src("paper/sections/02_model_samples.tex")
    p05 = src("paper/sections/05_detector_chain.tex")
    p06 = src("paper/sections/06_strategy_wp.tex")
    p07 = src("paper/sections/07_backgrounds.tex")
    p08 = src("paper/sections/08_results_p2.tex")
    p10 = src("paper/sections/10_bounds.tex")
    def2 = src("sim/DEFERRED.md")
    dec3 = src("sim/stage3/DECISIONS_PENDING.md")
    rep = src("REPRODUCE.md")
    g3 = src("acts/stage4/g3/G3_REPORT.md")
    g2a = src("acts/stage4/G2A_REPORT.md")
    s6 = src("opendata/STAGE6_FEASIBILITY.md")
    sreq = (PH / "phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md").read_text()
    figfinal = src("stage5/FIGURES_FINAL.md")

    # ---- the limit s95: independent evaluations
    check("s95 at B=0 is -ln 0.05", near(s95(0), -math.log(0.05), 1e-3), f"{s95(0):.4f}")
    # explicit Poisson sum, no scipy, B = n = 10
    def pcdf(n, mu):
        return sum(math.exp(-mu + k * math.log(mu) - math.lgamma(k + 1)) for k in range(n + 1))
    s10 = s95(10)
    check("s95(10) solves the CLs equation by an explicit Poisson sum", abs(pcdf(10, 10 + s10) / pcdf(10, 10) - 0.05) < 2e-4, f"s95={s10:.3f}")
    # Gauss-Hermite against the grid integral at a moderate background
    xg, wg = np.polynomial.hermite_e.hermegauss(120)
    def cls_gh(s, n, B, sg):
        b = B * np.exp(sg * xg)
        return np.sum(wg * stats.poisson.cdf(n, s + b)) / np.sum(wg * stats.poisson.cdf(n, b))
    s2 = s95(30, 1.0)
    check("log-normal grid integral agrees with Gauss-Hermite at B=30, width 1", abs(cls_gh(s2, 30, 30, 1.0) - 0.05) < 1e-3, f"s95={s2:.2f}")
    # the strategy's table, the study's own statement of this method
    line = re.search(r"Results: s95 = 3\.0 \(B = 0\), .*?8\.1 \(B = 10\), 12\.6 \(B = 30\), 26\.6 \(B = 160\), 45\.2 \(B = 480\), 174 \(B = 7680\)", strat)
    check("the strategy states the method and table", line is not None and "n = median of Poisson(B)" in strat)
    for B, v in [(0, 3.0), (10, 8.1), (30, 12.6), (160, 26.6), (480, 45.2), (7680, 174)]:
        check(f"s95({B}) against the strategy's {v}", near(s95(B), v, 0.012), f"{s95(B):.2f}")
    check("the chapter quotes the same limits", tex_has("$s_{95}=3.00$, $8.08$, $12.55$, $26.56$, $44.69$ and $173.5$", "$3.0$, $8.1$, $12.6$, $26.6$, $45.2$ and $174$"))
    check("large B, no width: s95 near 1.96 sqrt(B)", near(s95(1e6), 1.96 * 1e3, 0.01), f"{s95(1e6):.1f}")
    check("large B, width dominant: s95 near B(1-exp(-1.96 w))", near(s95(1e5, 1.0), 1e5 * (1 - math.exp(-1.96)), 0.01) and near(s95(1e4, 0.2), 1e4 * (1 - math.exp(-1.96 * 0.2)), 0.02), f"{s95(1e5, 1.0):.0f}")

    # ---- the reach, tested against limits the study states
    r0 = reach(s95(0), Y)
    rec = float(re.search(r"B=0 reach recomputed ([\d.]+) TeV@3ab", log).group(1))
    check("reach at B=0 against the logged 1.03 TeV", near(r0, 1000 * rec, 0.01), f"{r0:.1f} against {rec} TeV")
    check("the paper's about 1 TeV at B=0 is in the record", "exclude $E$ up to $\\approx1\\TeV$ with $3\\abinv$" in p10)
    Y300 = yields(fp, lumi_scale=0.1)
    r3 = reach(s95(0), Y300)
    r5 = reach(5, Y300)
    check("300 fb-1, three events inside the recorded 630 to 665 GeV", 630 <= round(r3) <= 665 and "3-event exclusion up to ≈ **630–665 GeV**" in nov, f"{r3:.1f}")
    rec5 = float(re.search(r"([\d.]+) TeV@300fb", log).group(1))
    check("300 fb-1, five events against the logged 0.59 TeV", near(r5, 1000 * rec5, 0.01), f"{r5:.1f}")
    pb = fp["A2|F|200|1.5|BM"]
    w = math.log(pb["B84_rfb"]["G"] / pb["B_median_rfb"]["G"])
    mu = s95(pb["B_median_rfb"]["G"], w) / pb["eps_rfb"]
    check("one bin at the best point gives the stored asymptotic limit", near(mu, pb["mu95_asymptotic_events"], 0.005), f"{mu:.4g} against {pb['mu95_asymptotic_events']:.4g}")
    check("and lies 5% above the stored toys", near(mu / pb["mu95_toys_events"], 1.05, 0.01), f"{mu / pb['mu95_toys_events']:.3f}")
    be = {"E200": ("A2|F|200|1.5|BM", 1.35e5, 8.3e2), "E500": ("A2|F|500|2|BM", 1.9e3, 95), "E1000": ("A2|F|1000|5|BM", 0.69, 0.64)}
    for k, (key, r_0, r_1) in be.items():
        s0 = fp[key]["S_at_rfb"]
        a0, a1 = break_even(s0, 0.0), break_even(s0, 1.0)
        check(f"break-even at {k} against the novelty audit's table", near(a0, r_0, 0.08) and near(a1, r_1, 0.085), f"{a0:.3g}, {a1:.3g} against {r_0}, {r_1}")
    check("the audit's table is in the record", "| E200 1.5 keV | 723 | 1.35 × 10⁵ | **8.3 × 10²** |" in nov and "| E500 2 keV | 87 | 1.9 × 10³ | 95 |" in nov and "| E1000 5 keV | 3.4 | 0.69 | 0.64 |" in nov)
    a0 = break_even(pb["S_at_rfb"], 0.0)
    a02 = break_even(pb["S_at_rfb"], 0.2)
    a1 = break_even(pb["S_at_rfb"], 1.0)
    check("break-even at S=710 as quoted", f"{a0 / 1e5:.2f}" == "1.31" and f"{a02 / 1e3:.1f}" == "2.2" and f"{a1 / 1e2:.1f}" == "8.2" and tex_has("$1.31\\times10^5$", "$8.2\\times10^2$"), f"{a0:.4g}, {a02:.4g}, {a1:.4g}")
    # the table of the chapter, recomputed
    BS = [0, 1, 10, 30, 100, 1e3, 1e4, 1e5]
    for lab, sg in [(r"\$\\sigma_\{\\ln\}=0\$ &", 0.0), (r"\$\\sigma_\{\\ln\}=0\.2\$ &", 0.2), (r"\$\\sigma_\{\\ln\}=1\$ &", 1.0)]:
        got = [c.strip().strip("$") for c in re.search(lab + r"(.*?)\\\\", TEX).group(1).split("&")]
        want = [reach(s95(B, sg), Y) for B in BS]
        want = ["--" if x is None else f"{x:.0f}" for x in want]
        check(f"reach table, width {sg}", got == want, f"{got}")
    Ye = yields(fp, sig_scale=1 / 0.31)
    got = [c.strip().strip("$") for c in re.search(r"endcap, \$g=1\$ &(.*?)\\\\", TEX).group(1).split("&")]
    want = [f"{reach(s95(B), Ye):.0f}" for B in BS]
    check("reach table, endcap row", got == want, f"{got}")
    drops = [reach(s95(a), Y) - reach(s95(b), Y) for a, b in [(10, 100), (100, 1e3), (1e3, 1e4), (1e4, 1e5)]]
    check("150 to 170 GeV per decade of B", 149 <= min(drops) and max(drops) <= 170, str(np.round(drops, 1)))
    check("at B=100 a width of 1 costs 222 GeV; width 1 at B=10 gives 796 with s95 12.8",
          round(reach(s95(100), Y)) - round(reach(s95(100, 1.0), Y)) == 222 and round(reach(s95(10, 1.0), Y)) == 796 and f"{s95(10, 1.0):.1f}" == "12.8")
    F15 = fixed_lambda_yields(fp, 1.5)
    check("fixed Lambda 1.5 keV at B=0 gives 923", round(reach(s95(0), F15)) == 923 and "923" in TEX)
    check("example: 867 with rounded inputs, 866 unrounded", round(500 + 500 * (math.log(87.2) - math.log(8.08)) / (math.log(87.2) - math.log(3.40))) == 867 and round(reach(s95(10), Y)) == 866)
    check("best-Lambda signals as quoted", f"{Y[500]:.1f}" == "87.2" and f"{Y[1000]:.2f}" == "3.40" and f"{Y[1500]:.3f}" == "0.295", str(Y))

    # ---- the map and the outcome
    ratios = {k: fp[k]["mu95_over_Nexp"] for k in fp}
    vals = sorted(v for v in ratios.values() if v)
    check("33 limits, 7 points with no limit", len(vals) == 33 and sum(1 for v in ratios.values() if not v) == 7)
    check("best 790, next 820, worst about 6e7", round(vals[0]) == 790 and round(vals[1]) == 820 and near(vals[-1], 6e7, 0.01), f"{vals[0]:.1f} {vals[1]:.1f} {vals[-1]:.3g}")
    check("no cell below one", vals[0] > 1)
    check("20 of 40 points reach three events; E 1500 never", sum(1 for k in fp if fp[k]["S_at_rfb"] >= 3) == 20 and max(fp[f"A2|F|1500|{l:g}|BM"]["S_at_rfb"] for l in LAMBDAS) < 3)
    check("263 passes over 40 points", sum(fp[k]["k_rfb"] for k in fp) == 263)
    best = [min(fp[f"A2|F|{m}|{l:g}|BM"]["mu95_over_Nexp"] for l in LAMBDAS if fp[f"A2|F|{m}|{l:g}|BM"]["mu95_over_Nexp"]) for m in MASSES]
    check("the limit lies 2.9 to 6.6 decades above the prediction", f"{math.log10(best[0]):.1f}" == "2.9" and f"{math.log10(best[-1]):.1f}" == "6.6", str(np.round(np.log10(best), 2)))
    check("per-mass best ratios against the log", "per-mass 1.3e4/3.8e5/3.8e6/2.8e5" in log and near(best[1], 1.3e4, 0.03) and near(best[2], 3.8e5, 0.01) and near(best[3], 3.8e6, 0.01), str(np.round(best)))
    check("31 fast-path points", sum(1 for k in fp if not fp[k]["replaced_by_a2fc"]) == 31)
    check("no stored 3-event reach or working point", S["outcome"]["wp_T"] is None and S["outcome"]["wp_G"] is None and "`mu_3events` = null everywhere" in res and "no 3-event discovery reach where B₈₄ > 0.3" in wpr)
    B84G5 = sorted([fp["A2|F|200|1.5|BM"]["B_median_rfb"]["T"], fp["A2|F|200|1.5|BM"]["B_median_rfb"]["G"]])
    check("stored medians at the best point lie beyond any reach", reach(s95(B84G5[0]), Y) is None, str(B84G5))
    # where the curves of Fig. 29.4b stop: S(200 GeV) = s95
    Ye4 = yields(fp, sig_scale=1 / 0.31)
    ends = [curve_end(Y[200], 0.0), curve_end(Y[200], 0.2), curve_end(Y[200], 1.0), curve_end(Ye4[200], 0.0)]
    check("curves end at B = 1.92e5, 2635, 997; endcap 2.01e6", near(ends[0], 1.92e5, 0.01) and near(ends[1], 2635, 0.01) and near(ends[2], 997, 0.01) and near(ends[3], 2.01e6, 0.01), str(np.round(ends)))
    check("just below each end the reach exists, just above it does not", all(reach(s95(e * 0.98, sg), y) is not None and reach(s95(e * 1.02, sg), y) is None for e, sg, y in zip(ends, [0.0, 0.2, 1.0, 0.0], [Y, Y, Y, Ye4])))
    rec = [reach(s95(b), Ye4) for b in B84G5]
    check("endcap case g = 1 at the stored medians reaches 298 and 280 GeV, above the published limits", round(rec[0]) == 298 and round(rec[1]) == 280 and tex_has("about $280$ to $300\\GeV$ (\\EST)"), str(rec))
    # the shaded edge of Fig. 29.4b
    ext_edges = external_edge(json.load(open(TT / "stage5/external_bounds.json")))
    check("published limits in the grid's range: FASER observed 172, its +1 sigma expected 180, nothing higher", ext_edges["FASER_obs"] == 172 and ext_edges["FASER_exp_p1s"] == 180 and max(ext_edges.values()) == 180, str(ext_edges))
    mt16 = re.search(r"multiplies that background by (\d+)", strat)
    check("the planning factor of 16 is in the strategy", mt16 is not None and mt16.group(1) == "16")
    mt30 = re.search(r"with the μ = 50 background rate \(B ≈ (\d+);", strat)
    check("the planning background of 30 is the strategy's rate at pile-up 50, and 30 x 16 = 480, the diamonds' third", mt30 is not None and mt30.group(1) == "30" and int(mt30.group(1)) * int(mt16.group(1)) == 480 and "| Phase 2, 3 ab⁻¹ | 480 (×16) |" in strat and tex_has("for backgrounds of $0$, $30$ and $480$ events", "the $30$ is that document's rate at pile-up 50"), mt30.group(0) if mt30 else "")
    check("the diamonds are the strategy's 0, 30 and 480: the figure's script takes B = 0, the rate and the rate times the factor", "plan_x = [XZERO, float(mt.group(3)), float(mt.group(4)) * float(mt.group(3))]" in (REPO / "book/figure_src/ch29/exclusion.py").read_text())
    val3 = src("sim/stage3/VALIDATION.md")
    check("the slope test over the grid: 9 of 30 in the record, and in the final account with the 7 standard deviations and the six lesser checks", "9/30 cells pass" in val3 and tex_has("over all $30$ combinations of point and $\\Lam$ the same criterion passes in $9$", "$7$ standard deviations high", "Six lesser pre-set checks also failed as written"))
    check("the deadline's move stated with its log entry, no cause claimed", "DEADLINE moved to Sun 2026-10-18 afternoon" in log and tex_has("sits in the entry on the usage limit, with no stated link", "no reason for the date in the log"))

    # ---- signal against background
    RUN = TT / "data/acts_stage4/analysis/C12FC_v1"
    SE = json.load(open(RUN / "signal_eff.json"))["a2"]["points"]
    BSUM = json.load(open(RUN / "bsum_wp.json"))
    G = BSUM["ladder"]["G"]
    T = BSUM["ladder"]["T"]
    names = [r["name"] for r in G]
    p = fp["A2|F|200|1.5|BM"]
    N0, N1, N2 = p["sigma_norm_fb"] * 3000, p["sigma_norm_fb"] * 3000 * p["f_tail"], p["N_exp_3ab"]
    Sr = [N2 * SE["A2|F|200|1.5|BM"]["ladder"][n]["eps"] for n in names]
    check("E 200 chain: 6.6e5, 3.1e4, 1.6e4, 3.2e3", f"{N0:.1e}" == "6.6e+05" and f"{N1:.1e}" == "3.1e+04" and f"{N2:.1e}" == "1.6e+04" and f"{Sr[0]:.1e}" == "3.2e+03", f"{N0:.3g} {N1:.3g} {N2:.3g} {Sr[0]:.3g}")
    check("the step to the first rung is a factor of about 5", near(N2 / Sr[0], 5, 0.05), f"{N2 / Sr[0]:.2f}")
    check("signal at R09 is 394", round(Sr[8]) == 394, f"{Sr[8]:.1f}")
    Bg = [r["B84"] for r in G]
    check("background minimum 1.23e6 at R09, about seven decades below R01 (7.42 across the change of counting at R04)", int(np.argmin(Bg)) == 8 and f"{min(Bg):.2e}" == "1.23e+06" and round(math.log10(Bg[0] / min(Bg)), 2) == 7.42, f"{min(Bg):.4g} {math.log10(Bg[0] / min(Bg)):.2f}")
    check("of those decades, R04 to R09 is 4.78, within the one counting convention", round(math.log10(Bg[3] / min(Bg)), 2) == 4.78, f"{math.log10(Bg[3] / min(Bg)):.2f}")
    bud = float(re.search(r"B₈₄,c\(r\) ≤ ([\d.]+) events in 3 ab⁻¹", wpr).group(1))
    check("no rung of either category reaches the budget, seven decades away", min(Bg) > bud and min(r["B84"] for r in T) > bud and near(math.log10(min(Bg) / bud), 7.05, 0.001), f"{math.log10(min(Bg) / bud):.3f}")
    worst = 0
    for k in SE:
        for i, n in enumerate(names):
            worst = max(worst, fp[k]["N_exp_3ab"] * SE[k]["ladder"][n]["eps"] / min(G[i]["B84"], T[i]["B84"]))
    check("at no rung of any of the 40 hypotheses does the signal reach the background", worst < 1, f"largest S/B84 {worst:.3g}")
    check("zero-count bounds from R08 on", "From R08 on every leading term" in TEX and "**Conclusion: no achievable statistics produce a WP with this ladder.**" in res)

    # ---- thickness
    P1 = json.load(open(TT / "sim/stage3/results/P1.json"))
    spread = 0
    for l in ["L0.45", "L0.6", "L1", "L2", "L3", "L5"]:
        f = [P1["points"][k]["by_lambda"][l]["Ds_B"]["median_um"] for k in ["F_m200", "F_m500", "F_m1000", "F_m1500"]]
        spread = max(spread, max(f) / min(f) - 1)
    check("four fermion masses within 14% at each Lambda", f"{100 * spread:.0f}" == "14", f"{spread:.3f}")
    sc = [P1["points"]["S_m500"]["by_lambda"][l]["Ds_B"]["median_um"] / P1["points"][k]["by_lambda"][l]["Ds_B"]["median_um"] for k in ["F_m200", "F_m500", "F_m1000", "F_m1500"] for l in ["L0.45", "L0.6", "L1", "L2", "L3", "L5"]]
    check("scalar within about 25% of each fermion mass at every Lambda (largest 24% at 0.45 keV)", 0.99 < min(sc) and 1.23 < max(sc) < 1.25, f"{min(sc):.3f} {max(sc):.3f}")
    hi_ms = {k: [P1["points"][k]["by_lambda"][l]["Ds_MS"]["median_um"] for l in ("L7", "L10")] for k in P1["points"]}
    check("the floor exists at 7 and 10 keV at all five points, highest 28.1 um", len(hi_ms) == 5 and round(max(max(v) for v in hi_ms.values()), 1) == 28.1, str({k: np.round(v, 1).tolist() for k, v in hi_ms.items()}))
    hi_f = sorted(k for k in P1["points"] if P1["points"][k]["by_lambda"]["L7"].get("Ds_B", {}).get("median_um") is not None and P1["points"][k]["by_lambda"]["L10"].get("Ds_B", {}).get("median_um") is not None)
    check("above 5 keV only E 500 and E 1000 have field-only runs", hi_f == ["F_m1000", "F_m500"], str(hi_f))
    allr = [e["Ds_B"]["median_ratio_to_MG_model_per_event"] for k in P1["points"] for e in P1["points"][k]["by_lambda"].values() if e.get("Ds_B", {}).get("median_ratio_to_MG_model_per_event")]
    check("median per-event ratio within about 5% of one", 0.945 < min(allr) and max(allr) < 1.03, f"{min(allr):.3f} {max(allr):.3f}")
    ms = [e["Ds_MS"]["median_um"] for k in P1["points"] for e in P1["points"][k]["by_lambda"].values() if "Ds_MS" in e]
    check("floor 10 to 28 um", round(min(ms)) == 10 and round(max(ms)) == 28, f"{min(ms):.1f} {max(ms):.1f}")
    xc = S["p1"]["lambda_cross_keV"]
    check("crossing 1.2 to 1.9 keV", f"{min(xc.values()):.1f}" == "1.2" and f"{max(xc.values()):.1f}" == "1.9")

    # ---- the barrel
    check("eta edge is a polar angle of 40.4 deg, 49.6 out of the transverse plane", f"{math.degrees(2 * math.atan(math.exp(-1))):.1f}" == "40.4" and f"{90 - math.degrees(2 * math.atan(math.exp(-1))):.1f}" == "49.6")
    check("case g = 1: signal factor 1 + 0.69/0.31 = 1/0.31 = 3.2, best ratio about 250", abs(1 + 0.69 / 0.31 - 1 / 0.31) < 1e-12 and f"{1 + 0.69 / 0.31:.1f}" == "3.2" and near(790 / (1 + 0.69 / 0.31), 250, 0.03))
    _eps = pb["eps_rfb"]
    _ceil = 1 + 0.69 / _eps  # every pair outside the barrel passes, at the best point
    _g = (0.69 / _eps) / (0.69 / 0.31)  # the same factor written as 1 + (0.69/0.31) g
    check("3.2 is no ceiling: every outside pair passing gives 16.3, g = 6.9, ratio 48 at the best point, efficiency stored 0.045", near(_eps, 0.045, 1e-6) and f"{_ceil:.1f}" == "16.3" and f"{_g:.1f}" == "6.9" and abs(1 + (0.69 / 0.31) * _g - _ceil) < 1e-9 and round(790 / _ceil) == 48 and 790 / _ceil > 1, f"{_ceil:.2f} {_g:.2f} {790 / _ceil:.1f}")
    check("and the chapter and the answer say so, with no upper bound left", tex_has("$1+0.69/0.045=16$", "($g=6.9$)", "about $48$") and "$g=6.9$" in ANS and "endcap bound" not in TEX and "upper bound on the" not in TEX)
    check("plan and rule: 69% outside the barrel, half a day", "**yes** (69 % of counting-set events have \\|η_pair\\| > 1) | +½ day" in plan4 and "69 % of counting-set events have |η_pair| > 1" in wpr)
    check("log: approved, then re-decided at 17:29", "D4-12" in log and re.search(r"17:29.*USER D4-12 RE-DECIDED: barrel-only frozen selection", log) is not None)
    check("review: two routes, recommended the second under the deadline", "Reviewer recommendation under the deadline: (b)" in rvw1 and "needs a G2a/G2b re-timing (t₁ rises)" in rvw1)
    check("rule: 1.0 is geometry only, from 0.94; seeding layer 1.12", "η_max = 1.0 is the TB2S L3 edge (0.94) rounded UP" in wpr and "TBPX L4 1.12" in wpr and "no signal input" in wpr)
    check("barrel fraction 0.19-0.28", "A1 barrel fraction is 0.19-0.28" in inve and "the barrel fraction without pile-up is 0.19--0.28" in lim)
    rows_f = {r[0]: [float(x) for x in r[1:] if x not in ("—",)] for r in (re.findall(r"[\d.—]+", line) for line in re.findall(r"^\| \**[\d.]+\** \| .*$", res[res.index("| Λ (keV) | E200 | E500 | E1000 | E1500 | Ẽ500 |"):res.index("With R04 also required")], re.M))}
    check("finder inside the barrel 0.90 to 0.96 at 1.5 to 2 keV, recomputed from the table", min(rows_f["1.5"] + rows_f["2"]) == 0.90 and max(rows_f["1.5"] + rows_f["2"]) == 0.96 and tex_has("$0.90$ to $0.96$"), str(rows_f))
    check("0.97 is the scalar at 3 keV, and the record says so", rows_f["3"][-1] == 0.97 and max(rows_f["3"][:-1]) < 0.9 and "Ẽ500 also at 3 keV" in res)
    check("total efficiency 0.005 against at most 0.021", "ε_tot = f·A·ε ≈ 0.005 at E500 2–5 keV, against their ≤ 0.021" in nov)
    check("neither seed family has three layers in the transition", "1.0 ≲ |η| ≲ 1.3 where neither family has three layers" in plan4)
    check("timing stops at 1.5; disc resolution varies by 2.5", "limits SR-T to |η| ≲ 1.5" in plan4 and "varies ×2.5 across the radius" in plan4 and "is not in the ACTS geometry" in plan4)
    check("string carried pairs to |eta|<4, about +15% of main CPU; disc material", "≈ +15 % P2 CPU" in plan3 and "$|\\eta_{\\rm pair}|<4$ propagated" in p05 and "add TFPX/TEPX/TEDD slabs" in plan3)
    check("own background-only ladder", "gets its own background-only ladder, frozen before its first signal efficiency" in wpr)

    # ---- the audit's rows, against the records
    needles = [
        ("seed family not in scope", wpr, "missing-L4 family of plan §2.2 item 2 are **not in scope**"),
        ("merged option, a week", plan4, "(b) build a merged-pair selection now | **(a)** | (b) ≈ +1 week"),
        ("upper edges without pile-up", res, "**4.70 / 5.38 / 5.89 / 6.05 / 6.60**"),
        ("lower edges with pile-up", res, "| **A2, PU 200** | 1.05 / 1.03 / 1.05 / 1.10 / 1.22 |"),
        ("seven points with zero efficiency", res, "Seven points have ε = 0 in"),
        ("wide regime, about a week and 40 CPU-h", plan4, "D4-14 (fix R1) | Wide regime"),
        ("no detector-level thickness", res, "out-of-plane resolution (23–30 µm) equals the MS floor"),
        ("trigger on MET", src("paper/sections/06_strategy_wp.tex"), "not used, because quirk hits form few stubs and no helices"),
        ("25 ns window", p05, "acc}=25\\ns$"),
        ("E1500 timing hits", plan4, "at E1500 only\n  26-30 % of counting-set events have a BTL hit within 1-25 ns"),
        ("rescale with N_IC", res, "Another N_IC rescales every ratio by 2/N_IC"),
        ("40 of 307", res, "at only 40 of the 307 points"),
        ("masses for edges", plan4, "the edges in ln m from 14 masses (it has 5)"),
        ("rest of the grid: cost", plan4, "| 8 | 183 (**26**) | 220 (**31**) | 163 (23) | 209 (**30**) | 157 (22) | 128 (18) |"),
        ("rest of the grid dropped", log, "C4′ dropped (future work)"),
        ("programme minimum of 200", plan3, "≥ 200 effective events per grid point"),
        ("9/200 and factor 1.5", res, "uncertain by a factor ≈ 1.5 either way at 68 % CL"),
        ("noise flips rows", res, "≈ 25–50 % of the passing rows at R08–R14"),
        ("500 fits the cap", plan4, "500 per topology is the size that fits C1 under the cap and the deadline"),
        ("events needed per term", res, "**10⁸–3 × 10⁹ events per sample are needed, against 500–2 000 now**"),
        ("second W samples dropped", log, "C2-C (SM W/Z/tt extra stats) → future work"),
        ("thinning reach", res, "**1.7 × 10⁻¹⁰** [E]"),
        ("toys and material on seven", plan4, "13 + 13 + 9 + 8 + 1.4 + 1.0"),
        ("wall time remark", plan3, "the question is wall time"),
        ("model cross-check not delivered, low risk, 0.12 %", src("sim/VALIDATION.md"), "the 500 GeV σ agrees to 0.12 %"),
        ("no cross-variable test for the deep rungs", res, "no cross-variable closure\n   test exists for R07–R23"),
        ("second set of rows at two masses", dec3, "toys exist only for E 1000/1200"),
        ("string per mass", dec3, "≈ 25 CPU-h per mass for 200 events × 4 Λ"),
        ("finer step costs ten times", rep, "max_boost ≤ 10⁻⁴ at ≥ 7 keV (≈ 10× cost)"),
        ("0.4 TB", g2a, "≈ 0.4 TB over the 8·10⁴ B1 trials"),
        ("R03 records", g3, "R05 would need R03 records, which are not stored"),
        ("cap", log, "NEW HARD CONSTRAINT: production must take ≲ 24 h wall on the Mac"),
        ("no Windows build of ACTS", plan4, "**Native Windows: not possible.**"),
        ("WSL2 not recommended", log, "pyacts has no win-64 wheel: PC only via WSL2, not recommended"),
        ("late-hit window", p06, "$[5.955,\\,24.035]\\ns$"),
        ("window variations", p06, "varied to 150 and 230\\,ps"),
        ("late-hit window approved 14 October", log, "2026-10-14 01:50 **SR-T t_min fix (PC-19) frozen.**"),
        ("factor 0.22 conservative", p07, "a conservative factor 0.22 for a vertex on the PV line"),
        ("toys for nuclear interactions and decays in flight", p07, "Nuclear interactions and decays in flight are not simulated by Fatras and are modelled by toys"),
        ("cap relaxed", log, "each ~27–30 h, a few hours over the 1-day cap, accepted"),
        ("cloud dropped; deadline", log, "Cloud dropped: Mac only. NEW DEADLINE: whole work incl. Stage 5"),
        ("deadline moved", log, "DEADLINE moved to Sun 2026-10-18 afternoon"),
        ("contention", g3, "**wall/estimate 1.85**"),
        ("PC benefit", plan4, "would take ≈ 330/17 ≈ 20 h of wall time instead of ≈ 47 h"),
        ("47 h, no margin", plan4, "≈ 47 h of production and no rerun margin"),
        ("usage limits", plog, "INTERRUPTED by session rate limit"),
        ("QED", def2, "≈ 15 CPU-h, beyond the"),
        ("QED systematic", p02, "$-1.1\\pm0.8\\%$"),
        ("concise note", log, "full 50-100 pp AN declined"),
        ("not a CMS result", con, "The study uses public information only and is not a CMS result"),
        ("port and core hours", sreq, "Port Athena `Simulation/G4Extensions/Quirks`"),
        ("material exponent", lim, "$\\DsMS\\propto(x/X_0)^{0.36\\ldots0.62}$"),
        ("17 092 modules", dec3, "17 092 modules"),
        ("acceptance optimistic", plan4, "acceptance is optimistic by a few % (ESTIMATE)"),
        ("smearing", plan4, "**Smearing digitisation** (no clusters, charge sharing, Lorentz drift"),
        ("forward timing half a day", plan4, "an outer R-shell (ESTIMATE ½ day)"),
        ("Fatras gaps", p05, "Fatras has no hadronic\ninteractions and does no decays in flight"),
        ("no Geant4 option", plan4, "(b) 1-3 h build + ~2 GB + integration days"),
        ("density widths", res, "the density normalisation dominates (1.15–1.89)"),
        ("Fatras low", plan4, "×2.3-7 per layer"),
        ("open-data check", s6, "about 3–5 weeks"),
        ("parametrised, not propagated", p08, "are not propagated to the final limits"),
        ("proxies", res, "They make up 15–45 % of B_SM"),
        ("left-out processes", res, "multijets are not in N_trig"),
        ("K-factors", p02, "at $13.6\\TeV$, applied at $14\\TeV$"),
        ("tail uncertainty", lim, "$+12$--15\\%/$-11$--13\\%"),
        ("left-out production", p02, "photon fusion ($+4\\%$"),
        ("Sommerfeld", p02, "no calculation exists"),
        ("analytic scattering later", log, "analytic MS = possible later extension"),
        ("floor test", src("sim/stage3/VALIDATION.md"), "**NOT DONE**"),
        ("floor test cost", rep, "≈ 1 CPU-h + 1–2 person-days"),
        ("decisive item", con, "the decisive item"),
        ("remainder", con, "leaves $\\approx0$--2 (SR-T) and 4--5 (SR-G) decades"),
        ("no change after freeze", con, "None of the following can be applied to the frozen analysis"),
        ("closure end state", log, "decline the +50 % statistics steps"),
        ("seed threshold", g3, "t₁: 5.52 → 8.02 s per trial (×1.45)"),
        ("factorisation", res, "B there could be off in either direction by an unknown factor"),
        ("late-hit credit", res, "is worth up to ≈ 4 decades, but in SR-T only"),
        ("23 of 33", p08, "(23 of the 33 points with a limit)"),
        ("fallback by plan", plan4, "but essentially no exclusion, at Λ ≲ 1 keV and at E200"),
        ("fast path", lim, "31 of 40 points use the fast signal path"),
        ("best ratio with full chain", res, "≈ 950\n  with the R04 factor 0.83"),
        ("independent check", S["validations"]["V4-5"], "NOT RUN"),
        ("brute force 50+50", plan4, "brute force on 50 signal + PU events and 50 PU-only trials"),
        ("variations", p08, "None of these can\nturn the null result into an exclusion"),
        ("handles", res, "**not measurable at PU 200**"),
        ("open data", s6, "no data downloaded, nothing analysed"),
        ("hit pool", sreq, "7.33 M sub-events"),
        ("bookkeeping", lim, "three unmeasured pile-up hits out of 145\\,007"),
        ("figures not made", figfinal, "**Ẽ σ-limit vs m and Ẽ exclusion map.** Only one Ẽ mass (500 GeV) exists in A2"),
        ("label", log, "Private work (simulation)"),
    ]
    for name, text, needle in needles:
        check(f"record: {name}", needle in text, "" if needle in text else needle[:60])
    check("failed tests in the record", "V2b GATE FAILED" in log and "+0.70/+2.00/+1.07/+2.10/+3.15" in log and "past the V2b gate (V2b recorded as a finding" in log)
    check("run hours as quoted", "$8.0$, $24.7$ and $23.3$" in TEX and all(k in log for k in ["24.7", "23.3"]))
    check("no Lee-Wick in the chapter", "Lee" not in TEX and "Wick" not in TEX)

    # ---- exercises and answers
    check("29.1", f"{s95(30):.2f}" == "12.55" and round(500 + 500 * (math.log(87.2) - math.log(12.55)) / (math.log(87.2) - math.log(3.40))) == 799 and "799" in ANS)
    Ya = {500: 87.2, 1000: 3.40, 1500: 0.295}
    check("29.2 values", round(reach(s95(0), Ya)) == 1026 and round(reach(s95(0), {k: v / 10 for k, v in Ya.items()})) == 665 and round(reach(5, {k: v / 10 for k, v in Ya.items()})) == 586 and near(math.log(10) / math.log(87.2 / 3.40), 0.71, 0.005))
    g = 0.5
    fac = 1 + (0.69 / 0.31) * g
    Yg = {k: v * fac for k, v in Y.items()}
    check("29.3", f"{fac:.1f}" == "2.1" and round(790 / fac) == 374 and round(Yg[500]) == 184 and f"{Yg[1000]:.2f}" == "7.18" and round(reach(s95(10), Yg)) == 982 and near((790 - 1) / (0.69 / 0.31), 354, 0.002), f"{fac:.3f} {790 / fac:.1f} {reach(s95(10), Yg):.1f}")
    pk = fp["A2|F|1000|5|BM"]
    lo = stats.beta.ppf(0.1587, pk["k_rfb"], pk["n_den"] - pk["k_rfb"] + 1)
    hi = stats.beta.ppf(0.8413, pk["k_rfb"] + 1, pk["n_den"] - pk["k_rfb"])
    check("29.4 interval from the beta quantiles", abs(lo - pk["eps_rfb_cp68"][0]) < 2e-4 and abs(hi - pk["eps_rfb_cp68"][1]) < 2e-4 and f"{lo:.4f}" == "0.0443" and f"{hi:.4f}" == "0.0839", f"{lo:.4f} {hi:.4f}")
    Sl, Sh = pk["N_exp_3ab"] * lo, pk["N_exp_3ab"] * hi
    Yl, Yh = dict(Y), dict(Y)
    Yl[1000], Yh[1000] = Sl, Sh
    check("29.4 range of S and reach", f"{Sl:.2f}" == "2.45" and f"{Sh:.2f}" == "4.63" and round(reach(s95(0), Yl)) == 972 and round(reach(s95(0), Yh)) == 1079, f"{Sl:.2f} {Sh:.2f} {reach(s95(0), Yl):.1f} {reach(s95(0), Yh):.1f}")
    check("29.5", f"{(710 / 1.96) ** 2:.3g}" == "1.31e+05" and f"{710 / (1 - math.exp(-1.96 * 0.2)):.3g}" == "2.19e+03" and round(710 / (1 - math.exp(-1.96))) == 826)
    labels = re.findall(r"\\label\{(ex:29-[^}]+)\}", TEX)
    check("five exercises with five answers", len(labels) == 5 and len(re.findall(r"\\answer\{29\.\d\}", ANS)) == 5, str(labels))
    sys.exit(1 if fails else 0)
