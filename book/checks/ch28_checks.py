#!/usr/bin/env python3
"""Checks for Chapter 28: recompute the chapter's numbers from tracked study files, and solve its exercises.

Every test recomputes something (a sum over stored chunk times, a clock difference from the log, a job-manifest formula, a log-normal
percentile, a scaling) and compares it with the value the chapter states, or confirms that a logged statement is in the named record.
Exits nonzero on any FAIL.
"""
import json
import math
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

REPO = Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search")
TT = REPO / "stage2_C001_quirks/theory_track"
PH = REPO / "stage2_C001_quirks"
TEX = (REPO / "book/chapters/ch28_bottlenecks.tex").read_text()
ANS = (REPO / "book/answers/ch28.tex").read_text()
idx = json.load(open(TT / "data/sim_stage3/STAGE3_INDEX.json"))
S = json.load(open(TT / "data/acts_stage4/analysis/STAGE4_SUMMARY.json"))
BS = json.load(open(TT / "data/acts_stage4/analysis/C12FC_v1/bsum_wp.json"))
rep = (TT / "REPRODUCE.md").read_text()
log = (TT / "LOG.md").read_text()
plog = (PH / "LOG.md").read_text()
plan = (TT / "acts/stage4/plan.md").read_text()
res = (TT / "acts/stage4/STAGE4_RESULTS.md").read_text()
g2a = (TT / "acts/stage4/G2A_REPORT.md").read_text()
g3 = (TT / "acts/stage4/g3/G3_REPORT.md").read_text()
g1b = (TT / "acts/stage4/G1B_REPORT.md").read_text()
wpr = (TT / "acts/stage4/WP_RULE.md").read_text()
feas = (TT / "opendata/STAGE6_FEASIBILITY.md").read_text()
con = (TT / "paper/sections/13_conclusions.tex").read_text()
lim = (TT / "paper/sections/12_limitations.tex").read_text()
s6 = (TT / "paper/sections/06_strategy_wp.tex").read_text()
strat = (PH / "phase1_strategy/outputs/STRATEGY_DRAFT.md").read_text()
oq = (PH / "phase1_strategy/outputs/OPEN_QUESTIONS.md").read_text()
sreq = (PH / "phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md").read_text()
fails = 0


def check(name, ok, detail=""):
    global fails
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        fails += 1


def near(a, b, rel):
    return abs(a - b) <= rel * abs(b)


def tex_has(*needles):
    return all(n in TEX for n in needles)


# ---- the bill
gen = float(re.search(r"\*\*≈ (23\.5) CPU-h\*\*", rep).group(1))
num = float(re.search(r"Total \*\*≈ (10) CPU-h\*\*", rep).group(1))
pts = idx["points"]
cpu = lambda p: sum(c["cpu_s"] for c in p["chunks"]) / 3600
string = sum(cpu(p) for p in pts.values())
det = S["production"]["cpu_h_total"]
check("string = 583 CPU-h from chunk times", near(string, 583, 2e-3), f"{string:.1f}")
check("detector chain = 382", near(det, 382, 2e-3), f"{det}")
check("campaigns add to the detector total", near(sum(v["cpu_h"] for v in S["production"]["cpu_h_by_campaign"].values()), det, 1e-3))
plan2 = (TT / "sim/plan.md").read_text()
check("generation: 2.07 M events, 2 h 48 min, 18 CPU-h in the Stage 2 plan", "2.07 M LHE events" in plan2 and "2 h 48 min wall" in plan2 and "≈ 18 CPU-h" in plan2)
e4 = (TT / "sim/E4_session_log.md").read_text()
check("generation restart 02:44, done 05:32 is 2 h 48 min", (datetime(2026, 10, 11, 5, 32) - datetime(2026, 10, 11, 2, 44)) == timedelta(hours=2, minutes=48) and "DONE 05:32 (restart 02:44" in e4)
check("generation 2.41 M events gives 0.035 s each", abs(gen * 3600 / 2.41e6 - 0.035) < 0.0005 and "2.41 M LHE events" in rep)
check("generation budget 35, 5.5 extra, six jobs", "budget ≈ 35 CPU-h, 6 parallel jobs" in plan2 and "+5.5 CPU-h of events at 200/300 GeV" in log)
val2 = " ".join((TT / "sim/VALIDATION.md").read_text().split())
_extras = re.search(r"≈ ([\d.]+) CPU-h \(top-ups and V-INTERP ≈ ([\d.]+), V-SHOWER ≈ ([\d.]+), QED and regeneration tests ≈ ([\d.]+), alps ≈ ([\d.]+), probes ≈ ([\d.]+)\)", val2)
_ex = [float(x) for x in _extras.groups()]
# The record's parts are each marked approximate: they sum to 5.3 against its "about 5.5", so the chapter says "about" for both.
check("the 5.5 is itemised in the record, and its five rounded parts come to 5.3, within rounding of it; top-ups and the check at 550 GeV are 3.2", abs(sum(_ex[1:]) - 5.3) < 1e-9 and _ex[0] == 5.5 and _ex[1] == 3.2, str(_ex))
check("18 CPU-h is an estimate by the study from wall times cores", "≈ 18 CPU-h (ESTIMATE from wall × cores)" in plan2)
defer2 = (TT / "sim/DEFERRED.md").read_text()
check("QED re-shower about 15 CPU-h, replaced by -1.1 +- 0.8 %", "15 CPU-h" in defer2 and "−1.1 ± 0.8 %" in log)
check("what is omitted: no QED FSR off the quirks; 17% radiate in the test at 500 GeV; the -1.1 is the largest median shift", "no QED FSR off quirks" in defer2 and "(largest median shift)" in " ".join(defer2.split()) and "quirk->gamma in 17 % of LOPS-500 events" in e4)
check("MadGraph's snag: first chunk 975 s, tune reset by the rewritten card, 0.421 against 0.463, outputs deleted, restart", "first 50k chunk through MG's own shower step took 975 s" in e4 and "rewrites the user pythia8_card" in e4 and "matching acceptance 0.421" in e4 and "vs 0.463" in e4 and "Old-flow outputs" in e4 and "deleted" in e4 and "RESTART production with own-shower flow" in e4)
check("own flow about 4 min per 50k chunk", "new flow ~4 min per 50k chunk" in e4)
pap5 = (TT / "paper/sections/05_detector_chain.tex").read_text()
check("tracking 23-60 s to 1.6-3.4 s with 32 sectors, log and paper", "CKF 23-60 s/ev on whole cylinders -> 1.6-3.4 s with 32 phi-sectors" in log and "32 azimuthal sectors" in " ".join(pap5.split()) and "from 23--60\\,s to 1.6--3.4\\,s per event" in " ".join(pap5.split()))
check("the crash comes from the sectors", "absent with nphi=1 -> phi-sector portal artefact" in log and "sector-boundary artefact" in log and "navigation assertion at the $\\phi$-sector boundaries" in " ".join(pap5.split()))
check("weights: 21.5 and 12 ms by Monte Carlo, 4 us exact", "counting MC 21.5 ms/set" in log and "4 us/set vs 12 ms MC" in log)
check("recorder 142 to 74 ns per step; Pythia start-up 13.6 to 0.1 s", "s3.2 recorder 74 vs 142 ns/step" in log and "init 13.6 s -> 0.1 s" in log)
check("the text ranks no speed-up as the one or the largest: the weights' factor (12 ms to 4 us) exceeds the finder's (211 s to 8.02 s, or 5500 s to 3.76 s)", "one place where speed was bought" not in TEX and "largest speed-up" not in TEX and 12e-3 / 4e-6 > 5500 / 3.76 > 211 / 8.02 > 26)

# development sum, from the logged items
dev = [3.5, 1.3, 1.2, 1.0, 30.4, 3.0, 5.5, 0.22, 1.3, 1.1, 1.6, 0.2]
check("development sum about 50 (G2a 3.5, G1 1.3, G1b 1.2, Phase A 1.0, G3 30.4 + 3, fixers 5.5 + 0.22, analysis 1.3 + 1.1 + 1.6, investigations 0.2)", abs(sum(dev) - 50) < 1.5, f"{sum(dev):.2f}")
check("G3 job wall 30.4 h and 5.80 h wall in the report", "The total job wall was 30.4 h" in g3 and "5.80 h wall" in g3)
check("G3 expected 2.5-3 h", "est 16.9 CPU-h ≈ 2.5–3 h" in log)
ana = 2497 / 3600
check("analysis run 2497 s, 0.7 CPU-h, 42 min", "analysis runtime | 2 497 s" in res and round(ana, 1) == 0.7 and round(2497 / 60) == 42)
whole = gen + string + det + num + 50 + ana
check("whole about 1050", near(whole, 1050, 0.005), f"{whole:.0f}")
check("summary shares 2, 56, 36 % of 1050", round(100 * gen / 1050) == 2 and round(100 * string / 1050) == 56 and round(100 * det / 1050) == 36)
check("figures under 30 s CPU", "< 30 s" in (TT / "stage5/FIGURES_FINAL.md").read_text() or "30 s" in (TT / "stage5/FIGURES_FINAL.md").read_text())
wall4 = 8.0 + 24.7 + 23.3 + 1.41
check("detector chain wall 57.4 h", abs(wall4 - 57.4) < 0.05, f"{wall4:.2f}")
check("6.7 of seven workers busy on average", round(det / wall4, 1) == 6.7, f"{det/wall4:.2f}")

# string kernel
to = idx["totals"]
ns = {m: to[m]["cpu_h_jobs"] * 3600 / to[m]["steps"] * 1e9 for m in ("mac", "pc")}
check("161 ns on the laptop, 173 ns on the PC", round(ns["mac"]) == 161 and round(ns["pc"]) == 173, str(ns))
steps = to["mac"]["steps"] + to["pc"]["steps"]
ev = to["mac"]["events"] + to["pc"]["events"]
check("1.24e13 steps for 218 571 events", near(steps, 1.244e13, 1e-3) and ev == 218571, f"{steps:.4g} {ev}")
check("PC 375.5 h for 290 estimated laptop hours", round(to["pc"]["cpu_h_jobs"], 1) == 375.5 and round(to["pc"]["est_cpu_h_M3"]) == 290)
check("PC is 64 % of the string", round(100 * to["pc"]["cpu_h_jobs"] / (to["pc"]["cpu_h_jobs"] + to["mac"]["cpu_h_jobs"])) == 64)
check("string estimates 330, 402, 498 and +96 not +5", "≈ 330 CPU-h" in log and "402 CPU-h" in log and "498 CPU-h" in log and "real cost +96 CPU-h, not the +5 first quoted" in log)


def cost_bm(lam):
    q = [p for k, p in pts.items() if k.startswith("p2/") and k.endswith(f"_BM") and p["lam_keV"] == lam]
    return sum(cpu(p) for p in q) * 3600 / sum(p["n_events"] for p in q)


for lam, val, tol in [(1.0, 0.32, 0.01), (3.0, 7.7, 0.05), (5.0, 31, 0.6), (7.0, 6.6, 0.05), (20.0, 77, 0.6), (30.0, 155, 0.6), (40.0, 182, 0.6)]:
    check(f"production cost per event at {lam} keV = {val} s", abs(cost_bm(lam) - val) < tol, f"{cost_bm(lam):.2f}")
ev_tot = sum(p["n_events"] for p in pts.values())
hi = [p for p in pts.values() if p["lam_keV"] >= 15]
check("Lambda>=15: 371 CPU-h, 64% of CPU, 6% of events", round(sum(cpu(p) for p in hi)) == 371 and round(100 * sum(cpu(p) for p in hi) / string) == 64 and round(100 * sum(p["n_events"] for p in hi) / ev_tot) == 6)
check("Lambda>=15 all on the PC", all(c["machine"] == "pc" for p in hi for c in p["chunks"] if "xover" not in c["id"]))
edges = S["p2_detector"]["edges_A1_R04"]
merge = [e["truth_merge100_median"]["value"] for e in edges.values()]
upper = [e["upper"]["value"] for e in edges.values()]
check("truth merging edge 13 to 23 keV, stored", round(min(merge)) == 13 and round(max(merge)) == 23, f"{min(merge):.1f} {max(merge):.1f}")
check("finder upper edge 4.7 to 6.6 keV without pile-up, stored", round(min(upper), 1) == 4.7 and round(max(upper), 1) == 6.6, f"{min(upper):.2f} {max(upper):.2f}")
check("pile-up grid stops at 5 keV", max(float(k.split("|")[3]) for k in S["fallback_points"]) == 5.0)
check("Athena extension public, kept as reference, port 1-3 person-months", "Athena G4 quirk extension public (Apache-2.0)" in plog and "Reference copy only" in rep and "1-3 person-months" in oq)
check("custom stepper 6-12 weeks", "custom C++ stepper not recommended (6-12 wk" in log)

grid = set()
for k in S["fallback_points"]:
    _, spin, m, lam, cfg = k.split("|")
    grid.add(f"p2/{spin}_m{m}/L{lam}_{cfg}")
check("40 grid points in the string index", len(grid) == 40 and all(g in pts for g in grid))
rows_cpu = sum(200 * cpu(pts[g]) / pts[g]["n_events"] for g in grid)
check("200 rows per point cost 12 CPU-h, 2% of the string", abs(rows_cpu - 12.1) < 0.1 and round(100 * rows_cpu / string) == 2, f"{rows_cpu:.2f}")

# ---- the detector chain by sample
kinds, kind_ev = {}, {}
for name in ["C1a", "C1b", "C2B", "A2FC"]:
    for j in json.load(open(TT / f"acts/stage4/jobs/{name}.json"))["jobs"]:
        kinds[j["sample"]] = kinds.get(j["sample"], 0) + j["est_s"] / 3600
        kind_ev[j["sample"]] = kind_ev.get(j["sample"], 0) + j.get("n_events", 0)
pu, dens = kinds["B1"] + kinds["B2"], kinds["DENSlow"] + kinds["DENShigh"]
sm = sum(v for k, v in kinds.items() if k.startswith("C_"))
single = kinds["Cp0"] + kinds["CpPU"]
sig = kinds["A1"] + kinds["A2"] + kinds["A5"] + kinds["A2FC"]
tot4 = pu + dens + sm + single + sig
check("job estimates: 374; 241, 39, 31, 23, 39", round(tot4) == 374 and round(pu) == 241 and round(dens) == 39 and round(sm) == 31 and round(single) == 23 and round(sig) == 39, f"{tot4:.1f} {pu:.1f} {dens:.1f} {sm:.1f} {single:.1f} {sig:.1f}")
check("the longest wait: pile-up about two thirds of the job estimates (241 of 374)", 0.62 < pu / tot4 < 0.67, f"{pu / tot4:.3f}")
check("background 89% of chain estimates", round(100 * (1 - sig / tot4)) == 89)
check("335 hours on background samples", round(tot4 - sig) == 335, f"{tot4-sig:.1f}")
check("job estimates agree with logged production within 5%", near(tot4, det, 0.05))
check("gun samples: 5.4e5 events, about 2 h", kind_ev["Cp0"] == 540000 and abs(kinds["Cp0"] - 2) < 0.2)
check("with pile-up: 4000 events, 21 h", kind_ev["CpPU"] == 4000 and abs(kinds["CpPU"] - 21) < 0.3)
launch = (TT / "acts/stage4/C1_LAUNCH.md").read_text()
m = re.findall(r"\| (?:C1a|C1b|C2B) \| \d+ \| [\d.]+ \| ≈ (\d+) \|", launch)
check("197 single-process hours", sum(map(int, m)) == 197, str(m))
logged = sum(S["production"]["cpu_h_by_campaign"][c]["cpu_h"] for c in ("C1a", "C1b", "C2B"))
check("373 hours logged", round(logged) == 373, f"{logged:.1f}")

# job formulas from the frozen runner
rs4 = (TT / "acts/stage4/run_stage4.py").read_text()
PU_S = float(re.search(r"^PU_S = ([\d.]+)", rs4, re.M).group(1))
PU_R2 = float(re.search(r"^PU_S_RHO2 = ([\d.]+)", rs4, re.M).group(1))
T1 = float(re.search(r"^T1_S = ([\d.]+)", rs4, re.M).group(1))
T2 = float(re.search(r"^T2_S = ([\d.]+)", rs4, re.M).group(1))
ev1, ev2 = PU_S + 4 * T1, 2 * PU_R2 + 2 * T2
check("normal pile-up event 10.2 + 4 x 8.02 = 42.3 s", PU_S == 10.2 and T1 == 8.02 and round(ev1, 1) == 42.3, f"{ev1:.2f}")
check("double-density event 119.8 s", round(ev2, 1) == 119.8, f"{ev2:.2f}")
check("double-density estimate per event agrees with the job file", near(kinds["B2"] * 3600 / kind_ev["B2"], ev2, 0.01))
# finder hours by the job formulas
f_B1 = kind_ev["B1"] * 4 * T1 / 3600
f_B2 = kind_ev["B2"] * 2 * T2 / 3600
f_dens = dens
f_sm = sum(kind_ev[k] for k in kinds if k.startswith("C_")) * T1 / 3600
f_cp = kind_ev["CpPU"] * T1 / 3600
f_a2 = 8000 * T1 / 3600
f_a5 = kind_ev["A5"] * T1 / 3600
f_fc = kind_ev["A2FC"] * T1 / 3600
finder = f_B1 + f_B2 + f_dens + f_sm + f_cp + f_a2 + f_a5 + f_fc
check("finder 277 of 374, 74%", abs(finder - 277) < 1.5 and round(100 * finder / tot4) == 74, f"{finder:.1f}")
check("gun event 1.5 to 12 ms, with pile-up 18.5 to 20 s, over a thousand times", "0.012 s/ev (ni22), 0.0015 (γ)" in g1b and "18.5–20 s/event loaded" in g1b and 18.5 / 0.012 > 1000)

# finder speed-up
check("211 s, 5500 s, 3.76 s, 24 trials", "t₁ = 3.76 s per trial" in g2a and "211 s with the merge vectorised (≈ 5 500 s as coded)" in g2a.replace("\n", " ") and "On 24 PU-only trials" in g2a)
check("211 / 8.02 = 26", round(211 / T1) == 26, f"{211/T1:.1f}")
check("seed threshold 5.52 to 8.02, x1.45", "t₁: 5.52 → 8.02 s per trial (×1.45)" in g3 and round(5.52, 1) == 5.5)
check("further x1.2-1.3, no x2", "A further ×1.2-1.3 looks possible with more work, but no ×2 without changing the" in g2a)

# review rounds
check("nine plan rounds, all dated 2026-10-13", "Plan review loop R1–R9 complete" in log and "2026-10-13 STAGE-4 PLAN PASS (R9 narrow verifier" in log)
check("analysis fix R6, results R1-R3 + R4_NORM, paper R1-R4", "FIXER R6 (analysis)" in log and "R4_NORM PASS" in log and "R4 PASS" in log)
check("normalisation fix 37.6 to 790", "Best μ₉₅/N_exp 37.6 → 790" in log)

# ---- the calendar
T = lambda d, h, mi=0: datetime(2026, 10, d, h, mi)
for pat in ["PID 42898 since 14:19", "2026-10-12 20:04", "2026-10-13 18:19 WP_RULE FROZEN", "2026-10-16 15:00 PAPER PASS", "2026-10-13 16:12 User D4-16",
            "C1b 760/760 ok (24.7 h, ended Thu 09:11)", "C2B 480/480 ok (23.3 h, ended Fri 08:55)", "DEADLINE moved to Sun 2026-10-18 afternoon",
            "done by Saturday night 2026-10-17", "≈4.5 Mac days", "Cloud dropped: Mac only", "production must take ≲ 24 h wall on the Mac",
            "a few hours over the 1-day cap, accepted", "worst case no orchestrator tokens"]:
    check(f"log has: {pat}", pat in log)
check("first session limit in the project log, 7 Oct 17:10", "2026-10-07 17:10 Fix pass INTERRUPTED by session rate limit" in plog)
check("resets on the 8th at 09:10 and 14:10", "reset 09:10" in log and "reset 14:10" in log)
pc = sorted(datetime.strptime(c["created_utc"][:19], "%Y-%m-%dT%H:%M:%S") - timedelta(hours=5) for p in pts.values() for c in p["chunks"] if c["machine"] == "pc")
span = (pc[-1] - T(11, 14, 19)).total_seconds() / 3600
check("string ended on the PC 00:07 on the 13th, 33.8 h after the laptop's start", pc[-1].strftime("%d %H:%M") == "13 00:07" and round(span, 1) == 33.8, f"{pc[-1]} {span:.2f}")
prod = (T(16, 8, 55) - T(14, 0, 29)).total_seconds() / 3600
check("production 56.4 h", round(prod, 1) == 56.4 or abs(prod - 56.43) < 0.01, f"{prod:.2f}")
check("first run about 8.0 h", abs(((T(15, 9, 11) - timedelta(hours=24.7)) - T(14, 0, 29)).total_seconds() / 3600 - 8.0) < 0.05)
win = (T(18, 15) - T(13, 16, 12)).total_seconds() / 3600
check("window about 119 h", abs(win - 119) < 0.5, f"{win:.1f}")
gates = (T(14, 0, 29) - T(13, 16, 12)).total_seconds() / 3600
check("gates 8.3 h, 7%", round(gates, 1) == 8.3 and round(100 * gates / win) == 7, f"{gates:.2f}")
check("production 47% of the stated 119 h", round(100 * prod / 119) == 47)
post = (T(16, 15) - T(16, 9, 5)).total_seconds() / 3600
check("post-production about 6 h, 5%", abs(post - 6) < 0.2 and round(100 * post / win) == 5, f"{post:.2f}")
left = (T(18, 15) - T(16, 15)).total_seconds() / 3600
check("about 48 h, 40% left", left == 48 and round(100 * left / win) == 40)
check("plan window 47 h, no margin, Wed 10:00 to Fri 12:00", "≈ 47 h of Mac wall, ≈ 329 CPU-h, with **no margin for a rerun**" in plan.replace("\n  ", " ") or "no margin for a rerun" in plan)
check("production started 9.5 h ahead of the plan", abs((T(14, 10) - T(14, 0, 29)).total_seconds() / 3600 - 9.5) < 0.05)
check("production ended before the plan's stop", T(16, 8, 55) < T(16, 12))
check("reruns 1.41 h and 0 errors", "1.41 h wall, 9.7 CPU-h, 0 errors" in log)
left_after_reruns = (T(18, 15) - T(16, 11, 45)).total_seconds() / 3600
check("about 51 h after the reruns; 14 + 22 = 36 h needed", abs(left_after_reruns - 51) < 0.5 and "\\$36\\$" not in TEX and "$36$\\,h of laptop wall" in TEX, f"{left_after_reruns:.2f}")

fp = S["fallback_points"]
ks = [p["k_rfb"] for p in fp.values()]
check("263 passing events over 40 points; 28 with <= 10; 7 with none", sum(ks) == 263 and sum(1 for k in ks if k <= 10) == 28 and sum(1 for k in ks if k == 0) == 7, f"{sum(ks)}")
check("best point 9 of 200, ratio moves by 1.5", fp["A2|F|200|1.5|BM"]["k_rfb"] == 9 and fp["A2|F|200|1.5|BM"]["n_den"] == 200)
cp = fp["A2|F|200|1.5|BM"]["eps_rfb_cp68"]
check("68% interval moves the ratio about 1.5 either way", abs(0.045 / cp[0] - 1.5) < 0.05 and abs(cp[1] / 0.045 - 1.45) < 0.05, str(cp))
check("stalled quote in the report", "no achievable statistics produce a WP with this ladder" in res)

# ---- limits in practice
check("machine: M3, 8 cores, 24 GB; MacBook Air; 7 workers", "Apple M3 MacBook, 8 cores, 24 GB RAM" in rep and "7 workers on the MacBook Air M3" in g3)
check("168 CPU-h per day at 7 workers", 7 * 24 == 168 and "Mac 7 workers ≈ 168 CPU-h" in plan)
check("19 GB, 4 GB, four jobs, 2.84, 3.6-3.8", "only 4 jobs ran at once (the 19 GB" in g3.replace("\n    ", " ") and "**2.84**" in g3 and "3.6-3.8 est-CPU-s" in g3)
check("0.4 TB, 128 GB free", "≈ 0.4 TB over the 8·10⁴ B1 trials" in g2a and "128 GB were free on 2026-10-13" in wpr)
check("R05 would need R03 records", "R05 would need R03 records, which are not stored" in g3)

# ---- table: what computing buys
c2 = json.load(open(TT / "acts/stage4/jobs/C2.json"))
c2c = sum(j["est_s"] for j in c2["jobs"] if j["kind"] == "sm") / 3600
check("row 1: 99 h, 14 h on 7 workers", round(c2c) == 99 and round(c2c / 7) == 14, f"{c2c:.1f}")
check("row 1: all five samples to 5000", "C → all five samples × 5 000" in plan)
row = re.search(r"\| 8 \| 183 \(\*\*26\*\*\) \| 220 \(\*\*31\*\*\) \| (\d+) \((\d+)\) \| 209 \(\*\*30\*\*\) \| (\d+) \((\d+)\) \| (\d+) \((\d+)\) \|", plan)
check("rows 2-4: 163 (23), 157 (22), 128 (18) at t1 = 8 s", row is not None and row.groups() == ("163", "23", "157", "22", "128", "18"))
# Row 4's stated basis, read from the plan: the optional rho = 3 run, its base cost, t3 against t2 and t2 against t1.
_c5 = re.search(r"\+ (\d) (\d{3}) × \(([\d.]+) \+ t₃\) s with t₃ ≈ ([\d.]+) t₂ \(finder ∝ ρ³\)", plan)
_t2t1 = re.search(r"t₂ = (\d+) t₁ until G2b", plan)
_c5scope = re.search(r"\*\*C5 \(optional.*?\n?.*?ρ = 3, (\d) (\d{3}) events × (\d) road", plan)
_n3, _base3, _r32, _r21 = float(_c5.group(1) + _c5.group(2)), float(_c5.group(3)), float(_c5.group(4)), float(_t2t1.group(1))
_c5cost = lambda t1: _n3 * (_base3 + _r32 * _r21 * t1) / 3600
check("row 4's basis in the plan: 2000 events, one road, base 14.1 s, t3 = 3.4 t2, t2 = 8 t1", (_n3, _base3, _r32, _r21) == (2000.0, 14.1, 3.4, 8.0) and _c5scope is not None and _c5scope.group(1) + _c5scope.group(2) == "2000" and _c5scope.group(3) == "1")
check("row 4's cost from that basis: within 1% of the plan's 38 at t1 = 2 and 128 at t1 = 8", near(_c5cost(2), 38, 0.01) and near(_c5cost(8), 128, 0.01), f"{_c5cost(2):.1f} {_c5cost(8):.1f}")
_c5col = {int(r_[0]): int(r_[1]) for r_ in re.findall(r"^\s*\| (\d+) \|(?: [\d]+ \(\*{0,2}\d+\*{0,2}\) \|){5} (\d+) \(\*{0,2}\d+\*{0,2}\) \|", plan, re.M)}
check("the same formula reproduces the plan's whole C5 column within 1%", len(_c5col) >= 6 and all(near(_c5cost(t_), v_, 0.01) for t_, v_ in _c5col.items()), str(_c5col))
check("a rho = 3 trial is about 27 normal trials: the factor rounds to the stated 27, and the old eight would give a third of the plan's cost", round(_r32 * _r21) == 27 and _n3 * (_base3 + 8 * 8) / 3600 < 128 / 2.5 and "about $27$ normal trials" in TEX and "eight normal trials" not in TEX)
check("row 2: reach 1.6e-10 to 1e-10 in the plan; 1.7e-10 stored", "After C3: 10⁻¹⁰" in plan and near(S["pu_reach_per_trial_rho2"]["value"], 1.7e-10, 0.03))
check("row 3: 53 344 events, 2 400 rows, 14 masses against 5", "53 344 more events, 2 400 rows" in plan and "edges in ln m from 14 masses (it has 5)" in plan)
check("row 4: about one decade", "worth about one decade" in con.replace("\n", " "))
check("row 5: 1.4 and 1.0 h at the fast finder", "13 + 13 + 9 + 8 + 1.4 + 1.0" in plan)
extra_a2 = 9 * kinds["A2"]
extra_s = 9 * rows_cpu
check("the signal grid took 21 of the 374 hours, 9 x that is the 192", round(kinds["A2"]) == 21 and round(9 * kinds["A2"]) == 192 and "$21$ of the $374$ hours" in TEX and "$11\\%$ of the detector bill" not in TEX, f"{kinds['A2']:.1f}")
check("row 6: 192 + 109 = about 300 h, 2 days, errors down by 3.2", round(extra_a2) == 192 and round(extra_s) == 109 and near(extra_a2 + extra_s, 300, 0.01) and round((extra_a2 + extra_s) / 7 / 24) == 2 and round(math.sqrt(10), 1) == 3.2, f"{extra_a2:.0f} {extra_s:.0f}")
_nine = 9 * kinds["A2FC"]
check("row 6's nine full-chain points: 1800 events in A2FC, ten times adds 9 x 10.0 = about 90 h, about 390 h in all", kind_ev["A2FC"] == 1800 and abs(kinds["A2FC"] - 10.0) < 0.1 and abs(_nine - 90) < 1 and abs(extra_a2 + extra_s + _nine - 390) < 3 and "about $390$\\,h in all" in TEX, f"{kinds['A2FC']:.2f} {_nine:.1f} {extra_a2 + extra_s + _nine:.1f}")
check("row 7: 3.4e4 h, 200 days", near(100 * (tot4 - sig), 3.35e4, 0.01) and round(100 * (tot4 - sig) / 7 / 24, -1) == 200)
fourrows = 99 + 163 + 157 + 128
check("exercise 1 sum 547: 78 h, 3.3 days, 5.5 h, $22", fourrows == 547 and round(fourrows / 7) == 78 and round(fourrows / 7 / 24, 1) == 3.3 and round(fourrows / 100, 1) == 5.5 and round(fourrows * 0.04) == 22)
check("rental: 550 h at 3 to 5 cents is about $20", 15 < 550 * 0.03 and 550 * 0.05 < 30)
check("rental: 1000 h is a few tens of dollars", 1000 * 0.03 == 30 and 1000 * 0.05 == 50)
check("rental: 3.35e4 h is of order $1500", 1000 < 3.35e4 * 0.03 and 3.35e4 * 0.05 < 1700)

# ---- the k law: refit by the study's recipe
r9 = next(r for r in BS["ladder"]["G"] if r["name"].startswith("R09"))
r9t = next(r for r in BS["ladder"]["T"] if r["name"].startswith("R09"))
SHARED = ("density", "model_spread", "normalisation", "closure", "trend", "srt_pv", "srt_sigt", "T3")


def b84(rung, scale, drop=(), n=400000, seed=28):
    rng = np.random.default_rng(seed)
    zs, tot = {}, np.zeros(n)
    for t in rung["terms"]:
        lz = np.zeros(n)
        ispu = t["label"].startswith("PU")
        for name, s in t["comps"].items():
            if s and not (ispu and name in drop):
                z = zs.setdefault(name, rng.standard_normal(n)) if name in SHARED else rng.standard_normal(n)
                lz += s * z
        tot += t["value"] * scale(t["label"]) * np.exp(lz)
    return float(np.quantile(tot, 0.84))


dec = lambda x: math.log10(x / 0.11)
check("21 terms at R09", len(r9["terms"]) == 21)
b0 = b84(r9, lambda l: 1)
check("recipe reproduces the stored 84th percentile to 1%", near(b0, r9["B84"], 0.01), f"{b0:.4g} vs {r9['B84']:.4g}")
check("lowest B84 = 1.23e6 and is at R09", near(r9["B84"], 1.23e6, 0.005) and min(r["B84"] for r in BS["ladder"]["G"]) == r9["B84"])
check("7.05 decades", abs(dec(r9["B84"]) - 7.05) < 0.005)
k_need = r9["B84"] / 0.11
check("k_need = 1.1e7", near(k_need, 1.1e7, 0.03), f"{k_need:.3g}")
_inv = " ".join((TT / "acts/stage4/investigation/INV_STATS_BKG.md").read_text().split())
check("the study's written 1.4e7 and the earlier minimum 1.57e6 are in its records", "×**1.4 × 10⁷** more statistics at R08/R09" in _inv and "1.57 → 1.23 × 10⁶ (R09)" in _inv and "≈ × 1.4 × 10⁷" in " ".join(res.split()) and "1.6 × 10⁶ / 1.6 × 10⁶ (R09) | 1.23 × 10⁶ / 1.23 × 10⁶ (R09)" in res)
check("the same division: 1.57e6/0.11 = 1.4e7 on the earlier run, 1.23e6/0.11 = 1.1e7 on the final one", near(1.57e6 / 0.11, 1.4e7, 0.03) and near(1.23e6 / 0.11, 1.1e7, 0.03), f"{1.57e6/0.11:.3g} {1.23e6/0.11:.3g}")
check("all samples grown by k_need reach the budget", abs(b84(r9, lambda l: 1 / k_need) / 0.11 - 1) < 0.02)
check("x100 leaves 5 decades, so two of seven", abs(dec(b84(r9, lambda l: 1e-2)) - 5.05) < 0.01)
fl = b84(r9, lambda l: 1 if l.startswith("PU") else 1e-8)
check("floor 2.3e3 when pile-up does not grow", near(fl, 2.3e3, 0.03), f"{fl:.0f}")
check("floor equals the stored pile-up-alone value", near(fl, S["statistics_reach"]["R09_p>1e-3"]["PU_alone_B84"], 0.02))
cost = k_need * (tot4 - sig)
check("cost at the budget about 4e9 h, five months of a million cores", near(cost, 4e9, 0.1) and abs(cost / 1e6 / (8766 / 12) - 5) < 0.3, f"{cost:.3g}")
check("rental: 4e9 h is of order $1e8", 1e8 < cost * 0.03 and cost * 0.05 < 3e8)
check("needed trial count 1e9, trend + density about 1.7", "≈ 1.0 × 10⁹ trials" in res and "σ_ln ≈ 1.7" in res)

# ---- the recorded gains on the stored terms (the figure and its paragraph)
def kind(l):
    return "PU" if l.startswith("PU") else ("SM" if l.startswith("SM") else "CP")


def scen(cp=1.0, smf=1.0, puf=1.0, cp_T=1.0, sm_T=1.0, drop=()):
    g = dec(b84(r9, lambda l: {"PU": puf, "SM": smf, "CP": cp}[kind(l)], drop))
    t = dec(b84(r9t, lambda l: {"PU": puf, "SM": smf * sm_T, "CP": cp * cp_T}[kind(l)], drop))
    return g, t


DEEP = ("trend", "closure")
sys.path.insert(0, str(REPO / "book/figure_src/ch28"))
from remedy_gains import gains  # noqa: E402  the same parser the figure uses; it fails if a source line is absent

GN = gains()
COND, CLOSURE, CREDIT = 1 / GN["cond_mid"], 1 / GN["closure"], 10 ** -GN["credit_decades"]
check("parsed gains: conditionals 100 to 200, middle 150; credit 4 decades; closure 2.41", GN["cond_lo"] == 100 and GN["cond_hi"] == 200 and GN["cond_mid"] == 150 and GN["credit_decades"] == 4 and round(GN["closure"], 2) == 2.41, str(GN))
check("parsed sample sizes: SM 2000 to 5000, x2.5; pile-up 12000 to 20000, x5/3", GN["sm_now"] == 2000 and GN["sm_more"] == 5000 and GN["pu_now"] == 12000 and GN["pu_more"] == 20000)
a = scen(cp=COND)
check("conditionals alone stop near 6 decades", 6.0 < a[0] < 6.3, f"{a}")
check("range of the conditionals hardly matters: /100 and /200 within 0.03", abs(scen(cp=1 / GN["cond_lo"])[0] - scen(cp=1 / GN["cond_hi"])[0]) < 0.03)
b = scen(cp=COND, smf=COND)
check("same factor on SM reaches about 5", abs(b[0] - 5.0) < 0.1, f"{b}")
sm9 = sum(t["value"] for t in r9["terms"] if t["label"].startswith("SM"))
check("SM central value 4.6e4", near(sm9, 4.6e4, 0.01), f"{sm9:.4g}")
c = scen(cp=COND, puf=CLOSURE, cp_T=CREDIT, sm_T=CREDIT, drop=DEEP)
check("late-hit with full credit and a deeper sample stops near 3.8", abs(c[1] - 3.8) < 0.05, f"{c}")
c0 = scen(cp=COND, cp_T=CREDIT, sm_T=CREDIT)
check("late-hit with full credit and no deeper sample stops near 4.3, and the chapter says which is which", abs(c0[1] - 4.3) < 0.1 and "full credit stops near $4.3$" in TEX and "adding a deeper sample takes it to $3.8$" in TEX, f"{c0}")
d = scen(cp=0, smf=0)
check("pile-up alone 4.3 decades", abs(d[0] - 4.3) < 0.05, f"{d}")
e = scen(cp=0, smf=0, puf=CLOSURE, drop=DEEP)
check("and 3.7 with a deeper sample", abs(e[0] - 3.7) < 0.05, f"{e}")


def deeper_gain(name):
    """Decades a deeper sample takes off the pile-up term alone at one rung: closure factor and trend and closure widths removed."""
    rung = next(r for r in BS["ladder"]["G"] if r["name"].startswith(name))
    return dec(b84(rung, lambda l: 1.0 if kind(l) == "PU" else 0.0)) - dec(b84(rung, lambda l: CLOSURE if kind(l) == "PU" else 0.0, DEEP))


_gain = {n_: deeper_gain(n_) for n_ in ("R09", "R14", "R23")}
check("a deeper sample is worth 0.6 at R09, 0.8 at R14, 1.7 at R23, against the study's about one decade", abs(_gain["R09"] - 0.58) < 0.02 and abs(_gain["R14"] - 0.76) < 0.02 and abs(_gain["R23"] - 1.70) < 0.02 and "worth about one decade" in con.replace("\n", " ") and "$0.6$ of a decade at R09" in TEX and "$0.8$ at R14 and $1.7$ at R23" in TEX, str({k_: round(v_, 3) for k_, v_ in _gain.items()}))
check("the closure factor 2.41 applies at every rung from R05, so also at R14 and R23", "| compounded | every column ≥ R05 | **× 2.409** |" in res)
pu_nt = [t for t in r9t["terms"] if "not present" in t["label"]][0]
check("the late-hit term for candidates with no in-time hit stays at the pile-up value 252", abs(pu_nt["value"] - 252) < 0.5)
check("the study's 0-2 and 4-5 are in the conclusions and flagged stale in the report", "\\approx0$--2 (SR-T) and 4--5 (SR-G)" in con and "**stale, not re-derived on C12FC_v1**" in res)
check("the report's remaining 3-4 decades of PU", "The remaining ≈ 3–4 decades of PU need" in res.replace("\n   ", " "))
check("gains: conditionals 2-2.3, credit up to 4", "≈ 2–2.3 decades on the C′ bounds" in res.replace("\n   ", " ") and "up to ≈ 4 decades" in res.replace("\n   ", " "))
check("the credit as the report defines it: prompt SM and single-interaction terms, pile-up per-hit late fraction about 1e-4 per edge, late-hit only", "They are prompt; sharing the PU per-hit late fraction (~10⁻⁴ per edge," in res and "but in SR-T only" in res and "about $10^{-4}$ per window edge: up to four decades, in that category only" in TEX)
check("the deadline's move sits in the entry on the usage limit, with no stated link, and the first entry's only addition is the day for questions", "(user keeps a day to ask questions)" in log and "## 2026-10-15 00:40 — token-outage plan (orchestrator)\n- USER: the parallel project may exhaust the weekly token limit in ~10 h (worst case no orchestrator tokens until Fri 16 09:00); DEADLINE moved to Sun 2026-10-18 afternoon." in log and "the entry does not say that one caused the other" in TEX and "For the date itself the log gives no reason" in TEX)

# ---- computing options
check("options: cloud terms and prices", "≈ $31 for C1 only, ≈ $68 for C1-C4, ≈ $120 for C1-C4 split plus C5" in (TT / "acts/stage4/review/FIX_S4PLAN_R3.md").read_text().replace("\n  ", " ") and "$300/90 days" in log and "cloud ~110" in log)
check("options: no account created", "No account, project, VM or lock" in plan)
check("options: WSL2 half a day, not bit-identical, 20 h instead of 47 h", "≈ ½ day of setup" in plan and "will **not** be bit-identical" in plan and "≈ 20 h of wall time instead of ≈ 47 h" in plan.replace("\n  ", " "))
check("options: CMS scale 24-34k core-h, USFQ unverified", "≈ 24-34k core-h" in oq and "USFQ T2/T3 access is UNVERIFIED" in oq)
check("options: batch systems never in the log", not re.search(r"CRAB|HTCondor|lxplus", log))
_inst = (TT / "acts/INSTALL_CHECK.md").read_text()
check("options: install check of 11 October: lxplus with a CMS account, Linux-only views, Docker daemon, source build 1 to 3 h, wheel used", "(E5, 2026-10-11)" in _inst and "Use on lxplus only (CMS account)" in _inst and "**No** (Linux x86_64/aarch64 only" in _inst and "**daemon not running**" in _inst and "≈ 1-3 h on 8 cores (ESTIMATE" in _inst and "R1 is installed" in _inst)
check("options: PC 10 then 15 workers", "10 then 15 workers" in json.dumps(idx["meta"]))
check("ColliderML: 3.7e4 crossings at mu = 200, ODD at 3 T, not in the track", "3.7×10⁴ at μ = 200" in sreq and "ODD ≠ CMS (3 T" in sreq and "ColliderML" not in log)
check("Linux: untested, wheel recorded, reproduction notes say undocumented", "none of this was tested" in rep and "manylinux_2_34_x86_64" in plan and "**NOT DOCUMENTED**" in rep)
check("cloud volumes 3 + 12 + 12 + 2 = about 30 GB, jobs under 30 min", 3 + 12 + 12 + 2 == 29 and "out ≈ 3 / 12 / 12 / 2 GB" in (TT / "acts/stage4/review/FIX_S4PLAN_R3.md").read_text() and "jobs ≲ 30 min" in (TT / "acts/stage4/review/FIX_S4PLAN_R3.md").read_text())
check("freeze hashes the string index", "is part of the Stage 4 analysis freeze" in rep)
loc = (TT / "DATA_LOCATION.md").read_text()
check("46 GB, drive location blank", "46 GB" in loc and "External drive / path: ____" in loc)

# ---- control region example
wid = 2 * 0.15
check("about 20 roads of 0.30 rad", round(2 * math.pi / wid) == 21)
# the road in hits is wider than in plane axes: half-width 0.15 + arcsin(W_c / r), with W_c = 75 mm, from the finder's source
_kern = (TT / "acts/stage4/finder/kernels.py").read_text()
_hw = 0.15 + math.asin(min(1.0, 75.0 / 146.5))
check("roads overlap in hits: half-width 0.69 rad at the outer pixel layer, so a hit lies in four or five roads", "road + np.arcsin(min(1.0, wc / ra))" in _kern and round(_hw, 2) == 0.69 and 4 < 2 * _hw / wid < 5 and "four or five of them" in TEX, f"{_hw:.3f} rad, {2 * _hw / wid:.1f} roads")
check("T = 0.05 is the ratio of road to sideband in plane axes", abs(wid / (2 * math.pi - wid) - 0.05) < 0.001, f"{wid / (2 * math.pi - wid):.4f}")
Nt = S["n_trig"] if isinstance(S["n_trig"], (int, float)) else S["n_trig"].get("total", S["n_trig"].get("value", S["n_trig"].get("N_trig")))
check("N_trig = 4.08e7", near(Nt, 4.08e7, 0.005), f"{Nt}")
tr = Nt * 20
check("8.2e8 trials; 1.7e4 times 4.8e4", near(tr, 8.2e8, 0.01) and near(tr / S["samples"]["B1_trials"], 1.7e4, 0.01), f"{tr:.3g}")
sb = math.sqrt(1 + 0.47 ** 2)
B = 1.14 * 0.05 * math.exp(sb)
check("B84 = 0.17, within 1.6 of the budget", abs(sb - 1.105) < 0.001 and abs(B - 0.17) < 0.005 and round(B / 0.11, 1) == 1.6, f"{B:.3f}")
check("by sampling too", near(np.quantile(1.14 * 0.05 * np.exp(sb * np.random.default_rng(6).standard_normal(2000000)), 0.8413), B, 0.01))
check("0.05 T S = 0.0025 S", abs(0.05 * 0.05 - 0.0025) < 1e-12)
check("searching the roads: 1.8e6 CPU-h", near(tr * T1 / 3600, 1.8e6, 0.02), f"{tr*T1/3600:.3g}")
check("0.15 rad is the 95% quantile of the pair's angle to MET", "=0.15$\\,rad is the 95\\% quantile" in s6.replace("\n", " "))
check("the control-region remedy is the study's first", "(i) A \\emph{data-driven pile-up fake estimate} in control regions" in con.replace("\n", " "))
check("CMS flat-shape value 0.04/0.90", round(0.04 / 0.90, 3) == 0.044)
check("Run 3 measurement recommended; only data can anchor it; skims defined, 2-3 FTE", "use Run-3 MET-skim and zero-bias data to *measure*" in strat and "only data can anchor it" in oq and "RAW-RECO and cluster-level MET skims" in strat and "~2-3 FTE for 2-3 years" in oq)
check("CMS-internal check still open", "CMS-internal check before anything else" in rep and "**Still open:**" in rep)

# ---- open data
f10 = (200 / 30) ** 10
check("(200/30)^10 = 1.7e8", near(f10, 1.7e8, 0.03), f"{f10:.3g}")
need = S["pu_reach_per_trial_rho2"]["requirement_if_PU_takes_SRG_budget"]
check("need 2.7e-10 per trial, stored", near(need, 2.7e-10, 0.01))
check("becomes 1.6e-18", near(need / f10, 1.6e-18, 0.03))
trials = 2.7e6 * 4
check("1.08e7 trials", trials == 1.08e7 and "$1.08\\times10^7$ trials" in TEX)
check("expected 2e-11 fakes", near(trials * need / f10, 2e-11, 0.2))
ub = 1.14 / trials
check("zero-count bound 1.1e-7 from the 1.08e7 trials as printed", round(ub * 1e7, 1) == 1.1 and "$1.14/(1.08\\times10^7)=1.1\\times10^{-7}$" in TEX, f"{ub:.3g}")
check("scaled to 18 per trial, over ten decades above the need", abs(ub * f10 - 18) < 0.8 and math.log10(ub * f10 / need) > 10)
check("the study's n_int about 20 is its 2^-20 in the reach formula, and the probe's 16 to 23 collisions are in the plan", "2^-20" in S["pu_reach_per_trial_rho2"]["formula"] and "the best PU candidates contain hits from 16-23 PU interactions" in plan)
check("(200/30)^20 = 3e16, the example's n = 10 being half the study's", near((200 / 30) ** 20, 3.0e16, 0.01) and "a factor of $3\\times10^{16}$" in TEX and "the $\\nint$ of Chapter" in TEX, f"{(200 / 30) ** 20:.3g}")
check("2012 MinimumBias record: 2.7 M events and 307 GB", "/MinimumBias/Run2012B-v1/RAW` (62; 2.7 M ev, 307 GB)" in feas)
check("2017 ZeroBias record: about 1.0 TB, no event count", "≈1.0 TB" in feas and "no container, no event count" in feas)
check("one unit of n: 3 to 7", round(200 / 60) == 3 and round(200 / 30) == 7)
check("note: efforts and tests", "about 1–2 weeks" in feas and "about 3–5 weeks" in feas and "may fail" in feas)
check("note: pile-up 10 to 60 unverified", "about 10–60 (UNVERIFIED" in feas)

# ---- table of bottlenecks
eps = [p["eps_rfb"] for p in fp.values()]
check("fallback efficiency at most 0.08", abs(max(eps) - 0.08) < 0.005)
n3 = sum(1 for p in fp.values() if p["S_at_rfb"] >= 3)
check("20 of 40 points reach three events", n3 == 20 and len(fp) == 40)
check("closure z = +52.8", abs(S["closure"]["T1"]["z"] - 52.8) < 0.05, f"{S['closure']['T1']['z']}")
check("compounded 2.41", abs(S["closure"]["compounded_ge_R05"] - 2.41) < 0.005)
check("ceiling 0.3 and remedies in the conclusions", "\\approx0.3$ barrel ceiling" in con.replace("\n", " "))
check("69% and 3.2 and 250", "69 % of counting-set events have \\|η_pair\\| > 1" in plan and round(1 / 0.31, 1) == 3.2 and abs(790 / (1 / 0.31) - 245) < 10)
check("merged-pair selection about a week", "(b) ≈ +1 week" in plan)
check("independent cross-check not run, 50 + 50", "brute force on 50 signal + PU events and 50 PU-only trials" in plan and "seed-threshold regression check (V4-4) is partial" in lim.replace("\n", " "))
check("the study's string estimate for detector work, 12 to 30 CPU-h", 12 <= rows_cpu <= 30 and abs(sum(cpu(pts[g]) for g in grid) - 29.75) < 0.1, f"{sum(cpu(pts[g]) for g in grid):.2f}")

# ---- faster finder and exercise 2
speed = lambda f: ev1 / (PU_S + 4 * T1 / f)
check("finder x10: 13.4 s and factor 3.2", abs(PU_S + 4 * T1 / 10 - 13.4) < 0.05 and abs(speed(10) - 3.2) < 0.06, f"{speed(10):.2f}")
check("perfect finder 4.1", abs(speed(1e12) - 4.1) < 0.06)
check("half a decade from a factor 3.2", abs(math.log10(speed(10)) - 0.5) < 0.01)
f2 = 4 * T1 / (ev1 / 2 - PU_S)
check("ex 2: f = 2.9 makes it twice as fast", round(f2, 1) == 2.9 and abs(speed(f2) - 2) < 1e-9, f"{f2:.2f}")
check("ex 2: with the chain halved, 8.3", round(ev1 / (PU_S / 2), 1) == 8.3)

# ---- exercises 3 to 5
check("ex 3: 6e17 trials", near(1 / (need / f10), 6e17, 0.1), f"{1/(need/f10):.3g}")
check("ex 3: factor 11", round((200 / 60) ** 2) == 11)
Tmax = 0.11 / (1.14 * math.exp(sb))
check("ex 4: T <= 0.032, 31 roads, half-width 0.10", abs(Tmax - 0.032) < 0.0005 and round(1 / Tmax) == 31 and round(math.pi / round(1 / Tmax), 2) == 0.10, f"{Tmax:.4f}")
smp = 1.14 * Tmax * np.exp(sb * np.random.default_rng(5).standard_normal(2000000))
check("ex 4 by sampling: 84th percentile = 0.11", near(np.quantile(smp, 0.8413), 0.11, 0.01))


def ex5(k, n=2000000, seed=4):
    rng = np.random.default_rng(seed)
    a_ = 5e5 / k * np.exp(1.1 * rng.standard_normal(n))
    b_ = 252 * np.exp(2.22 * rng.standard_normal(n))
    return np.quantile(a_ + b_, 0.84)


vals = [ex5(k) for k in (1, 1e2, 1e4, 1e6)]
second = 252 * math.exp(2.22)
check("ex 5: k=1 about 1.5e6", near(vals[0], 1.5e6, 0.03), f"{vals[0]:.3g}")
check("ex 5: k=1e2 about 1.9e4", near(vals[1], 1.9e4, 0.05), f"{vals[1]:.0f}")
check("ex 5: k=1e4 about 2.4e3", near(vals[2], 2.4e3, 0.03), f"{vals[2]:.0f}")
check("ex 5: k=1e6 about 2.3e3", near(vals[3], second, 0.03), f"{vals[3]:.0f}")
kgrid = np.logspace(2, 4, 21)
v = np.array([ex5(k, 1000000) for k in kgrid])
kk = float(np.exp(np.interp(np.log(2 * second), np.log(v[::-1]), np.log(kgrid[::-1]))))
check("ex 5: twice the second term near k about 700", 650 < kk < 800, f"{kk:.3g}")

# ---- the chapter says what these tests tested
for needle in ["$583$", "$382$", "$1.1\\times10^7$", "$2.3\\times10^3$", "$4\\times10^9$", "$1.7\\times10^8$", "$1.6\\times10^{-18}$", "$335$", "$277$", "$263$", "$2.07\\times10^6$", "$119.8$", "$8.2\\times10^8$", "$57.4$", "=0.17 ,"]:
    check(f"chapter states {needle}", needle in TEX)
check("the chapter hands on to Chapter 29", "\\ref{ch:29-account}" in TEX)
check("no Lee-Wick in the chapter", "Lee" not in TEX and "Wick" not in TEX)
check("the account section has moved out", "sec:28-account" not in TEX)

print(f"{fails} failed")
sys.exit(1 if fails else 0)
