#!/usr/bin/env python3
"""Checks for Chapter 25 (From MadGraph to the plane finder).

Every study number is read from tracked repository files, then the arithmetic and statements of the
chapter are recomputed from them. The toys (log-normal budget, best-of-K) are real simulations.
Prints PASS or FAIL per test; exits nonzero on any FAIL.
"""
import json, re, sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[2] / "stage2_C001_quirks" / "theory_track"
AN = TT / "data/acts_stage4/analysis/C12FC_v1"
KEY = "A2|F|200|0.45|BM"
HBARC = 0.19733  # GeV fm
fails = 0


def check(name, ok, detail=""):
    global fails
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        fails += 1


def close(a, b, tol):
    return abs(a - b) <= tol * abs(b)


# ---------- files
sm = json.load(open(TT / "data/acts_stage4/analysis/STAGE4_SUMMARY.json"))
idx = json.load(open(TT / "data/sim_stage3/STAGE3_INDEX.json"))
acc = json.load(open(AN / "acceptance.json"))["points"][KEY]
xs = json.load(open(TT / "sim/results/xsec.json"))["trigger_yields_E"]["rows"]["200"]
frozen = json.load(open(TT / "acts/stage4/frozen_inputs.json"))
revert = json.load(open(TT / "acts/stage4/investigation/V46_REVERT_SET.json"))
repro = (TT / "REPRODUCE.md").read_text()
addendum = (TT / "acts/stage4/HASH_ADDENDUM.md").read_text()
g1b = (TT / "acts/stage4/G1B_REPORT.md").read_text()
g2a = (TT / "acts/stage4/G2A_REPORT.md").read_text()
samples_tex = (TT / "paper/sections/02_model_samples.tex").read_text()
detector_tex = (TT / "paper/sections/05_detector_chain.tex").read_text()
strategy_tex = (TT / "paper/sections/06_strategy_wp.tex").read_text()
obs = np.load(AN / "signal_obs_a2.npz", allow_pickle=True)
rows = np.load(AN / "signal_rows_a2.npz", allow_pickle=True)
disp = np.load(AN / "event_display.npz", allow_pickle=True)

# ---------- the benchmark's scales
sigma_norm = float(re.search(r"^200\s*&\s*[\d.]+\s*&\s*([\d.]+)", samples_tex, re.M).group(1))
l0_cm = 200.0 / (0.45e-6) ** 2 * HBARC * 1e-13
check("l0 = m/Lambda^2 at 200 GeV, 0.45 keV is 19.5 cm", close(l0_cm, 19.5, 0.01), f"{l0_cm:.2f} cm")
check("swings about twice: (11 to 12) (Lambda/keV)^2 at 0.45 keV", 2.0 < 11 * 0.45**2 < 2.5 and 2.0 < 12 * 0.45**2 < 2.5,
      f"{11*0.45**2:.2f} to {12*0.45**2:.2f}")

# ---------- yield chain, eq. (25.1) and exercise 25.1
f200 = xs["f_pt200_TRG_over_INC"]
A = acc["A_trig_presel"]
fac = acc["factors"]
L = 3000.0  # fb^-1
check("A is the product of its factors", close(A, fac["fiducial_eta25"] * fac["trigger"] * fac["preselection_given_trigger"], 1e-6), f"A={A:.4f}")
pairs = sigma_norm * L
tail = pairs * f200
check("pairs in 3/ab = 6.6e5", close(pairs, 6.6e5, 0.01), f"{pairs:.4g}")
check("tail agrees with the stored N_3iab_pt200", close(tail, xs["N_3iab_pt200"], 0.002), f"{tail:.5g} vs {xs['N_3iab_pt200']:.5g}")
Nexp = tail * A
check("N_exp = 1.58e4", close(Nexp, 1.58e4, 0.005), f"{Nexp:.5g}")
check("S at 3/200 is about 240", 230 < Nexp * 3 / 200 < 245, f"{Nexp*3/200:.1f}")
p = 3 / 200
check("relative error of 3/200 is 0.57", close(np.sqrt((1 - p) / (200 * p)), 0.57, 0.01))

# ---------- generation cost
cpu_gen = float(re.search(r"\*\*≈ 23\.5 CPU-h\*\*", repro).group(0).split()[1])
n_lhe = 2.41e6
check("47 points and 2.41e6 events are stated in the source", "47 points" in samples_tex and "2.41\\times10^6" in samples_tex)
check("generation costs 0.035 s per event", close(cpu_gen * 3600 / n_lhe, 0.035, 0.01), f"{cpu_gen*3600/n_lhe:.4f}")

# ---------- string propagator cost
tot = idx["totals"]
cpu_str = tot["mac"]["cpu_h_events"] + tot["pc"]["cpu_h_events"]
steps = tot["mac"]["steps"] + tot["pc"]["steps"]
events = tot["mac"]["events"] + tot["pc"]["events"]
check("218571 events", events == 218571, str(events))
check("583 CPU-h", close(cpu_str, 583, 0.002), f"{cpu_str:.1f}")
check("1.24e13 steps", close(steps, 1.24e13, 0.005), f"{steps:.4g}")
ns = cpu_str * 3600 / steps * 1e9
check("about 170 ns per step", 160 < ns < 175, f"{ns:.1f} ns")
lam, cost, boost = [], [], []
for k, q in idx["points"].items():
    if q["campaign"] in ("p2", "p2_hi") and q["spin"] == "F" and q["m"] == 500 and q["cfg"] == "BM":
        lam.append(q["lam_keV"]); cost.append(sum(c["cpu_s"] for c in q["chunks"]) / q["n_events"]); boost.append(q["max_boost"])
lam, cost, boost = map(np.array, (lam, cost, boost))
fine = boost == 1e-3
slope = np.polyfit(np.log(lam[fine]), np.log(cost[fine]), 1)[0]
check("cost grows as Lambda^2.8 on 0.3 to 5 keV with the fine step", close(slope, 2.8, 0.02) and lam[fine].max() == 5 and lam[fine].min() == 0.3, f"slope {slope:.3f}")
c1, c3, c30 = cost[lam == 1][0], cost[lam == 3][0], cost[lam == 30][0]
check("0.334 s at 1 keV, 8.17 s at 3 keV, 167 s at 30 keV", close(c1, 0.334, 0.002) and close(c3, 8.17, 0.002) and close(c30, 167, 0.005), f"{c1:.3f} {c3:.2f} {c30:.1f}")
check("the step above 5 keV is ten times coarser", set(boost[~fine]) == {0.01} and lam[~fine].min() == 7)
pt = idx["points"]["p2/F_m200/L0.45_BM"]
ours = sum(c["cpu_s"] for c in pt["chunks"]) / pt["n_events"]
check("our point: 0.038 s and 46 hits per event", close(ours, 0.038, 0.02) and close(pt["n_hits"] / pt["n_events"], 46, 0.01), f"{ours:.4f} s, {pt['n_hits']/pt['n_events']:.1f} hits")
hi_c = hi_n = all_c = all_n = 0
for q in idx["points"].values():
    c = sum(x["cpu_s"] for x in q["chunks"])
    all_c += c; all_n += q["n_events"]
    if q["lam_keV"] >= 15:
        hi_c += c; hi_n += q["n_events"]
check("Lambda >= 15 keV: 64% of the CPU on 6% of the events", 0.63 < hi_c / all_c < 0.65 and 0.055 < hi_n / all_n < 0.065, f"{hi_c/all_c:.3f} {hi_n/all_n:.3f}")

# ---------- detector chain cost
t_finder = float(re.search(r"`T1_S` 3\.26 → ([\d.]+) s", addendum).group(1))
t_chain = float(re.search(r"`PU_S` 4\.83 → ([\d.]+) s", addendum).group(1))
check("chain 10.2 s, road 8.02 s, event with four roads 42 s", t_chain == 10.2 and t_finder == 8.02 and close(t_chain + 4 * t_finder, 42, 0.01), f"{t_chain + 4*t_finder:.2f}")
m = re.search(r"56 s per row loaded \(PU chain 11\.9 s \+ 8 × 5\.5 s\)", g1b)
check("a row of eight: 56 s = 11.9 + 8 x 5.5 (source, and sum)", m is not None and close(11.9 + 8 * 5.5, 56, 0.005))
_jobs = json.load(open(TT / "acts/stage4/jobs/C1a.json"))["jobs"]
_a2 = [j for j in _jobs if j["kind"] == "a2"]
_a2_s = sum(j["est_s"] for j in _a2)
_a2_rows = sum(j["n_events"] for j in _a2)
check("a row at the production setting: job file gives 76.8 s (about 77 s), over 1000 rows", _a2_rows == 1000 and close(_a2_s / _a2_rows, 76.8, 0.002), f"{_a2_s / _a2_rows:.2f} s, {_a2_s / 3600:.2f} h")
check("and 9 x that sum is the 192 h of Chapter 28 for ten times the rows", close(9 * _a2_s / 3600, 192, 0.002), f"{9 * _a2_s / 3600:.1f} h")
run4 = (TT / "acts/stage4/run_stage4.py").read_text()
check("the 5.5 s road is the old seed threshold and 8.02 s the production one, in the runner", "T1_S = 8.02" in run4 and "T_seed 6: 5.52" in run4)
det = sm["production"]["cpu_h_total"]
total = cpu_gen + cpu_str + det
check("shares: 990 CPU-h; 2%, 59%, 39%", close(total, 990, 0.005) and round(100 * cpu_gen / total) == 2 and round(100 * cpu_str / total) == 59 and round(100 * det / total) == 39, f"{total:.1f}")
check("funnel of the timing test in the source", "1.76·10⁵ refits → 1.04·10⁵ after the merge; 8.0·10⁴ pass the loosest rung; 589 have N_IP2 ≥ 7" in g2a)
check("pile-up: 1.33e5 hits, factor up to 7.3, 13.9% removed, 1540 tracks", all(s in detector_tex for s in ["1.33\\times10^5", "4.0--7.3", "13.9\\%", "1540"]))
check("resolutions in the source: 7.2, 28.9, 26.0 um; 14.5 mm", all(s in detector_tex for s in ["7.2\\um", "28.9\\um", "26.0\\um", "14.5\\mm"]))

# ---------- the shortcut and its check
tab = {(r["spin"], r["m"], r["lam"]): r for r in revert["table"]}
r0 = tab[("F", 200, 0.45)]
n_rev = sm["a2fc_revert"]["meta"]["n_revert"]
check("our point lost no hits and did not go back; nine points did", r0["mean_f"] == 0 and r0["pooled_f"] == 0 and not r0["revert"] and n_rev == 9 and sum(r["revert"] for r in revert["table"]) == 9)
check("threshold is 5%, signal grid 40 points", revert["threshold"] == 0.05 and sm["outcome"]["n_points"] == 40)

# ---------- our event
i = int(np.argmax(obs["L"][:, :14].sum(1)))
check("the stored display event is this candidate", json.loads(str(disp["label"]))["signal"]["row"] == int(obs["row"][i]) and str(obs["key"][i]) == KEY)
met = float(obs["met"][i])
check("MET 248 GeV is 2 GeV under the 250 GeV cut", 248 <= met < 248.5 and "MET$\\,>250\\GeV$" in strategy_tex, f"{met:.1f}")
check("eta_pair = 0.59; axis eta = 0.59", close(float(obs["eta_pair"][i]), 0.59, 0.01) and close(float(obs["eta_axis"][i]), 0.59, 0.01))
ax, nrm = obs["axis"][i], obs["normal"][i]
dphi = abs((np.arctan2(ax[1], ax[0]) - float(obs["phimet_reco"][i]) + np.pi) % (2 * np.pi) - np.pi)
check("axis within 0.06 rad of MET, inside 0.15 rad", close(dphi, 0.06, 0.05) and dphi < frozen["delta95"], f"{dphi:.4f}")
keep = disp["cls"] < 2
X = np.c_[disp["x"][keep], disp["y"][keep], disp["z"][keep]].astype(float)
isq = disp["cls"][keep] == 1
check("77 hits: 28 quirk, 49 pile-up", len(X) == 77 and isq.sum() == 28 and (~isq).sum() == 49)
check("f_CKF = 2/79", close(float(obs["f_ckf"][i]), 2 / 79, 1e-5), f"{float(obs['f_ckf'][i]):.5f}")
check("w_core = 4.33 mm, inside the 4.7 mm rung", close(float(obs["w_core"][i]), 4.33, 0.002) and obs["w_core"][i] < 4.7)
check("h = 1.9e6, o = 9.3e6, dE/dx = 1.84", close(float(obs["h"][i]), 1.9e6, 0.02) and close(float(obs["o"][i]), 9.3e6, 0.01) and close(float(obs["dedx"][i]), 1.84, 0.002))
names = [str(x) for x in obs["L_names"]]
Li = obs["L"][i]
check("23 rungs; passes R22, fails R23", len(names) == 23 and Li[:22].all() and not Li[22] and names[21].startswith("R22") and names[22].startswith("R23"))
dt = float(obs["dt_earliest"][i])
ulen_ns = float(obs["t_raw_in"][i]) - float(obs["t_pv"][i]) - dt
beta = ulen_ns / (ulen_ns + dt)
check("Delta t = 2.71 ns, under the window, |u| = 1.36 m, beta = 0.625", close(dt, 2.71, 0.003) and dt < sm["srt_window_ns"][0] and close(ulen_ns * 0.299792, 1.36, 0.005) and close(beta, 0.625, 0.002), f"dt {dt:.3f} |u| {ulen_ns*0.299792:.3f} m beta {beta:.4f}")
check("beta agrees with the stored time-of-flight value", close(beta, float(obs["beta_tof"][i]), 1e-3))
wmin, wmax = sm["srt_window_ns"]
check("late-hit window 5.955 to 24.035 ns", wmin == 5.955 and wmax == 24.035)
b_hi = ulen_ns / (ulen_ns + wmin); b_lo = ulen_ns / (ulen_ns + wmax)
check("exercise 25.3: beta from 0.16 to 0.43", close(b_hi, 0.43, 0.01) and close(b_lo, 0.16, 0.02), f"{b_lo:.3f} {b_hi:.3f}")

# per-layer crossing counts recomputed from the hits
r = np.hypot(X[:, 0], X[:, 1])
sensors = np.unique(np.round(r, 1))           # every barrel surface is a cylinder, so its radius labels it
check("16 barrel sensors: 4 pixel layers plus 6 stacked layers of two", len(sensors) == 16, str(sensors))


def on(R):
    return np.round(r, 1) == R


q_it = [int((on(R) & isq).sum()) for R in sensors[:4]]
pairs_st = [(sensors[4 + 2 * j], sensors[5 + 2 * j]) for j in range(6)]
q_st = [(int((on(a) & isq).sum()), int((on(b) & isq).sum())) for a, b in pairs_st]
all_st = [(int(on(a).sum()), int(on(b).sum())) for a, b in pairs_st]
check("pixel and PS layers have two quirk hits per sensor", all(n == 2 for n in q_it) and all(a == 2 and b == 2 for a, b in q_st[:3]), f"{q_it} {q_st[:3]}")
check("outer two 2S layers have one quirk hit per sensor", q_st[4] == (1, 1) and q_st[5] == (1, 1), f"{q_st[3:]}")
check("pile-up supplies the second crossing: N_2S2 = 3 with all hits, 1 with quirk hits alone",
      sum(min(a, b) >= 2 for a, b in all_st[3:]) == 3 and sum(min(a, b) >= 2 for a, b in q_st[3:]) == 1, f"{all_st[3:]}")

# band widths: eq. (25.3) with the resolution table
it = re.search(r"IT pixel.*?&\s*\$([\d.]+)\\um\$\s*&\s*\$([\d.]+)\\um\$", detector_tex).groups()
ss = re.search(r"2S \(strips\).*?&\s*\$([\d.]+)\\um\$\s*&\s*\$([\d.]+)\\mm\$", detector_tex).groups()
ttol = frozen["t_tol_mm"]
band_it = 3 * np.sqrt((abs(nrm[2]) * float(it[1]) * 1e-3) ** 2 + ttol**2)
band_2s = 3 * abs(nrm[2]) * float(ss[1])
# eq. (25.2) bounds |u.n| by 3 sigma_tot, so these are half-widths: every stored hit lies within them on its own side of the plane
ures = np.abs((X - obs["pv"][i]) @ nrm)
check("band half-width about 0.1 mm in the pixels and 37 mm in the 2S layers", 0.09 < band_it < 0.13 and close(band_2s, 37, 0.02), f"{band_it:.3f} {band_2s:.1f}")
check("the 2S half-width is reached: largest 2S |u.n| lies within it and above half of it", band_2s / 2 < ures[r > 600].max() <= band_2s, f"{ures[r > 600].max():.1f}")
check("the same in the pixels", band_it / 2 < ures[r < 200].max() <= band_it, f"{ures[r < 200].max():.3f}")

# how unusual the event is, from the per-row pass matrix
Lm = rows[KEY + "|L"]
check("200 rows: 3 reach R04, 1 reaches R14, 0 reach R23", Lm.shape[0] == 200 and Lm[:, 3].sum() == 3 and Lm[:, 13].sum() == 1 and Lm[:, 22].sum() == 0, f"{Lm[:,3].sum()} {Lm[:,13].sum()} {Lm[:,22].sum()}")
rep = fac["finder_at_report_rungs"]
check("the same fractions in the stored acceptance file", rep["R_A"] == 0.015 and rep["R_D"] == 0.005 and rep["R_E"] == 0.0)

# ---------- ladder and rule
wc = frozen["w_c_mm"]
check("width rungs are W_c/2^k (37.5, 18.75, 9.4, 4.7)", [round(wc / 2**k, 2) for k in range(1, 3)] == [37.5, 18.75] and round(wc / 8, 1) == 9.4 and round(wc / 16, 1) == 4.7)
check("window, tolerance and road are the frozen values", wc == 75 and ttol == 0.03 and frozen["delta95"] == 0.15 and frozen["t_seed"] == 4)
check("exercise 25.4: 1.14/M with sigma_ln = 1 has B84 = 3.1/M", close(1.14 * np.exp(1), 3.1, 0.002))
rng = np.random.default_rng(20261105)
zz = rng.normal(size=(2, 4000000))
s_ln = 2.3
comb = np.percentile(np.exp(s_ln * (zz[0] - 1)) + np.exp(s_ln * (zz[1] - 1)), 84.13)
check("log-normal budget: two categories combine at 2.71", close(comb, 2.71, 0.01), f"{comb:.3f}")
check("exercise 25.4: fully correlated, the ratio is 2", close(np.percentile(2 * np.exp(s_ln * (zz[0] - 1)), 84.13), 2.0, 0.005))
check("0.3/2.71 = 0.11", round(0.3 / 2.71, 2) == 0.11)


def rule(b, budget=0.11):
    """Loosest rung (1-based) with b <= budget there and at every tighter rung."""
    best = None
    for j in range(len(b) - 1, -1, -1):
        if b[j] <= budget:
            best = j + 1
        else:
            break
    return best


ex = [5, 0.09, 0.2, 0.07, 0.05]
naive = next(j + 1 for j, x in enumerate(ex) if x <= 0.11)
check("exercise 25.2: the rule picks rung 4, naive picks rung 2", rule(ex) == 4 and naive == 2)
check("outcome: no working point in either category", sm["outcome"]["wp_T"] is None and sm["outcome"]["wp_G"] is None)
lad = sm["ladder"]["SR-T"]
check("lowest B84 is 1.2e6 at R09, seven decades over 0.11", close(lad["min_B84"], 1.2e6, 0.03) and lad["min_B84_rung"].startswith("R09") and 7 <= np.log10(lad["min_B84"] / 0.11) < 7.1, f"{lad['min_B84']:.3g}")

# ---------- example 25.2 and exercise 25.5: the price of picking the best
sims = rng.binomial(200, 0.05, size=(400000, 20)) / 200
best = sims.max(1).mean()
check("best of 20 at a true 5% reads 8.1%, about 60% high", close(best, 0.081, 0.01) and 0.58 < best / 0.05 - 1 < 0.64, f"{best:.4f}")
check("spread of 200 events at 5% is 3.1 events", close(np.sqrt(200 * 0.05 * 0.95), 3.1, 0.01))
m300 = rng.binomial(200, 0.05, size=(40000, 300)).max(1).mean() / 200
m400 = rng.binomial(200, 0.05, size=(30000, 400)).max(1).mean() / 200
check("exercise 25.5: the best of 300 to 400 is close to 10%", 0.097 < m300 < 0.103 and 0.097 < m400 < 0.103, f"{m300:.4f} {m400:.4f}")

# ---------- why this event: first in the file to pass all of the first 14 rungs (depth counted from the stored rung flags)
L14 = obs["L"][:, :14]
depth = np.where(L14.all(axis=1), 14, np.argmin(L14, axis=1))
first14 = int(np.argmax(depth == 14))
check("displayed event is the first candidate with depth 14; none before it passes all 14", first14 == 16 and depth[:16].max() < 14, f"index {first14}, depth before {depth[:16].max()}")
check("its point is simply the first key in the file", str(obs["key"][0]) == "A2|F|200|0.45|BM" and str(obs["key"][first14]) == "A2|F|200|0.45|BM")
check("all candidates pass the four counting rungs (the old 'basic cuts' singled out none)", depth.min() == 4, str(depth.min()))
disp_sig = json.loads(str(disp["label"]))["signal"]
check("it is the event of the display file", int(obs["row"][first14]) == disp_sig["row"] and disp_sig["depth"] == 14 and disp_sig["key"] == str(obs["key"][first14]), str(disp_sig))

# ---------- how narrow the displayed ribbon is, against the sample's median swing
n2 = np.cross(nrm, ax)
u_ev = X - obs["pv"][i]
u2, u3 = u_ev @ n2, u_ev @ ax
inner = r < 600  # pixel and PS sensors
wq = np.abs(u2[isq]).max()
check("largest distance of a quirk hit from the axis is 9.8 mm (a tilt, not a width)", close(wq, 9.8, 0.005), f"{wq:.2f} mm")
seps = []
for R in sensors:
    s = on(R) & isq & inner
    if s.sum() == 2:
        seps.append(abs(np.diff(u2[s])[0]))
check("ten pixel and PS sensors: the two quirks at most 0.47 mm apart in the plane, across the axis (within 0.5 mm)", len(seps) == 10 and close(max(seps), 0.466, 0.005) and max(seps) < 0.5, f"{np.round(seps, 3)}")
slope, icpt = np.polyfit(u3[isq], u2[isq], 1)
check("the stored axis lies 8 mrad off the line through the quirk hits", close(abs(slope), 8.08e-3, 0.01), f"{slope*1e3:.2f} mrad, intercept {icpt:.2f} mm")
res_in = u2[isq & inner] - (slope * u3[isq & inner] + icpt)
rms_in = np.sqrt(np.mean(res_in**2))
check("pixel and PS quirk hits have rms 0.15 mm about that line", close(rms_in, 0.15, 0.05), f"{rms_in:.3f} mm")
v_in = u2[inner]
wcore_all = 1.4826 * np.median(np.abs(v_in - np.median(v_in)))
check("w_core 4.33 mm is reproduced from all in-band pixel and PS hits", close(wcore_all, float(obs["w_core"][i]), 1e-3) and inner.sum() == 38, f"{wcore_all:.4f} mm on {inner.sum()} hits")
v_q = u2[isq & inner]
wcore_q = 1.4826 * np.median(np.abs(v_q - np.median(v_q)))
check("the quirk hits alone give less than half of it (1.91 mm, all of it tilt)", close(wcore_q, 1.91, 0.01) and rms_in < wcore_q / 10, f"{wcore_q:.2f} mm")
pts = json.load(open(TT / "sim/stage3/results/P2_points.json"))
lmax_med = pts["F_m200/L0.45"]["lmax_med_cm"]["value"]
check("median lmax of this sample is 13 cm", close(lmax_med, 13.1, 0.005))

# ---------- the event swings more often than the typical pair: T_h = 2 p*/sigma, full period 4 beta*gamma* l0, times the pair's beta gamma


def swing_period_cm(gamma_star, bg_pair):
    return 4 * np.sqrt(gamma_star**2 - 1) * l0_cm * bg_pair


bg_pair = beta / np.sqrt(1 - beta**2)
g_typ = 1 + lmax_med / (2 * l0_cm)
per_typ = swing_period_cm(g_typ, bg_pair)
per_low = swing_period_cm(1.05, bg_pair)
path_cm = ulen_ns * 0.299792 * 100
check("pair beta gamma 0.80; median lmax gives gamma* 1.34", close(bg_pair, 0.80, 0.005) and close(g_typ, 1.34, 0.005), f"{bg_pair:.3f} {g_typ:.3f}")
check("typical pair: period 55 cm, 2.5 swings in 1.36 m, near the stored 2.3", close(per_typ, 55, 0.02) and close(path_cm / per_typ, 2.5, 0.03) and close(pts["F_m200/L0.45"]["N_osc_med"]["value"], 2.3, 0.02), f"{per_typ:.1f} cm, {path_cm/per_typ:.2f}")
check("gamma* = 1.05: period about 20 cm, about 7 swings: more often, not less", 19 < per_low < 21 and 6.5 < path_cm / per_low < 7.2 and per_low < per_typ, f"{per_low:.1f} cm, {path_cm/per_low:.2f}")

# ---------- the rerun rule could not fire as first placed
inv = (TT / "acts/stage4/investigation/INV_SIGNAL_EFF.md").read_text()
a2fc = (TT / "acts/stage4/A2FC_REPORT.md").read_text()
check("the source says the rule could not fire: the check ran at 1 keV only", "so the rule could never fire" in inv and "could not fire because A5 was placed only at 1 keV" in inv.replace("\n", " "))
check("the source says the investigation triggered the reruns, on the no-pile-up sample, with the list fixed first", "`investigation/INV_SIGNAL_EFF.md` item 3" in a2fc and "Revert set (pre-declared, before any production)" in a2fc and "Production C1 A1 (full chain, no PU)" in a2fc)

# ---- which vertex (final review): the finder is told; the estimate of what a wrong one costs
import math
dt_one = " ".join(detector_tex.split())
check("vertex smearing 10 and 15 um with a 93% efficiency, unverified, in the source", "(10,15)\\um" in dt_one and "93\\%" in dt_one and "\\UNV" in dt_one)
bg07 = " ".join((TT / "paper/sections/07_backgrounds.tex").read_text().split())
check("pile-up trials draw a vertex independently, in the source", "a PV drawn from the luminous region independently of the pile-up vertices" in bg07)
spacing = 1 / (200 / (2.5066282746 * 45.0))
check("one vertex spacing is 0.56 mm", close(spacing, 0.564, 0.01), f"{spacing:.3f}")
_sig_rphi, _sig_z = float(it[0]) * 1e-3, float(it[1]) * 1e-3  # pixel resolutions, mm, from the same table as the band above


def shift_over_band(nz):
    """A z shift dz moves hits off the plane by dz n_z. Band full width: 6 sigma_tot of eq. (25.2), with sigma_n projected on the same normal."""
    return spacing * nz / (6 * np.sqrt((nz * _sig_z) ** 2 + (1 - nz**2) * _sig_rphi**2 + ttol**2))


_nz_scan = np.linspace(0, 1, 1001)
_ratios = shift_over_band(_nz_scan)
check("pixel resolutions 7.2 and 28.9 um, tolerance 30 um", float(it[0]) == 7.2 and float(it[1]) == 28.9 and ttol == 0.03, str(it))
check("shift over full band width: largest at n_z = 1, 2.26 (at most 2.3)", int(np.argmax(_ratios)) == 1000 and close(_ratios.max(), 2.26, 0.005), f"{_ratios.max():.3f}")
check("and 2.04 at our event's n_z = 0.843 (about 2)", close(abs(float(nrm[2])), 0.843, 0.002) and close(float(shift_over_band(abs(float(nrm[2])))), 2.04, 0.005), f"n_z {abs(float(nrm[2])):.3f}, {float(shift_over_band(abs(float(nrm[2])))):.3f}")
check("the two acceptances: 0.104 x 0.567 = 0.059", close(0.104 * 0.567, 0.059, 0.001))

# ---- what moved after the first results (Table 25.2), from the report's table of the two runs and the investigation
TEX25 = (TT.parents[1] / "book/chapters/ch25_chain.tex").read_text()
check("the chapter gives the projected ratio, and the old 'nearly three' and 'tiny' swing have gone", "nearly three" not in TEX25 and "about $2$ full widths" in TEX25 and "at most $2.3$" in TEX25 and "swing is tiny" not in TEX25)
_g3 = (TT / "acts/stage4/g3/G3_REPORT.md").read_text()
check("the seed test at R06: +16% and +37%, more than 2 sigma, at both densities", "| B1 | R06 | **trial pass fraction** | 0.178 | 0.206 | +16 % | **+3.16** |" in _g3 and "| B2 | R06 | **trial pass fraction** | 0.317 | 0.433 | +37 % | **+2.61** |" in _g3 and round(100 * (0.206 / 0.178 - 1)) == 16 and round(100 * (0.433 / 0.317 - 1)) == 37 and "($+16\\%$ and $+37\\%$ at the two densities)" in TEX25)
res25 = (TT / "acts/stage4/STAGE4_RESULTS.md").read_text()
inv25 = (TT / "acts/stage4/investigation/INV_STATS_BKG.md").read_text()
_num = lambda s_: float(s_.replace(" × 10", "e").translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")))
_fb = {n_: [_num(x_) for x_ in re.findall(r"\d\.?\d* × 10[⁰¹²³⁴⁵⁶⁷⁸⁹]+", re.search(rf"^\| B₈₄ T / G at {n_} \|.*$", res25, re.M).group(0))] for n_ in ("FB0", "FB1", "FB2")}
_f = {n_: (v_[0] / v_[2], v_[1] / v_[3]) for n_, v_ in _fb.items()}
check("merge fix: general x4 and x8 at the two loosest fallbacks", round(_f["FB0"][1]) == 4 and round(_f["FB1"][1]) == 8, str(_f))
check("merge fix: late-hit about 50 and 60 at those two (49, 64), and 36 at the next", 45 < _f["FB0"][0] < 55 and 55 < _f["FB1"][0] < 65 and round(_f["FB2"][0]) == 36 and "by $36$ in the late-hit category at the next" in TEX25)
check("the investigation classes it as a bug that is conservative, with toy limits changed at 23 of 33 points, as an estimate", "**(ii) bug** (conservative, but large)" in inv25 and "`limits.json` toys (primary) at 23 of 33 points" in inv25 and "**[E]** re-evaluated here" in inv25 and "at $23$ of $33$ points (\\EST)" in TEX25)
_br = re.search(r"^\| best μ₉₅/N_exp \(FIX R3-NORM normalisation; 53 / 37\.6 before\) \| ([\d.]+) × 10³ .*?\*\*(\d+)\*\*", res25, re.M)
check("best ratio on the final normalisation: 1.1e3 before these fixes, 790 after", _br is not None and _br.group(1) == "1.1" and _br.group(2) == "790" and "from $1.1\\times10^3$ in the run before these fixes to $790$ in the final run" in TEX25)
check("no selection moved: the ladder and working-point decision are unchanged by the merge fix", "Ladder and WP decision unchanged" in inv25 and "No selection moved." in TEX25)

print("ALL PASS" if fails == 0 else f"{fails} FAILED")
sys.exit(1 if fails else 0)
