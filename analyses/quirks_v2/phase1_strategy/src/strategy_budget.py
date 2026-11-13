#!/usr/bin/env python3
"""Arithmetic behind STRATEGY_brigitte (Phase 1): CPU-h, storage, capacity, sample sizes.

Standard library only; run as `python3 -I strategy_budget.py` (milliseconds; allowed on einstein).
Every unit cost is a measured value from the feasibility reports (source in the comment) or is marked ESTIMATE.
CPU-h here are slot-hours on a worker with 4 jobs per node (the "4 concurrent" columns of FEAS_A).
"""
import math

H = 3600.0
# ---- measured unit costs (seconds) ------------------------------------------------------------------------------
CHAIN = 13.53      # PU-200 event, chain, 4 concurrent: FEAS_A §3.3 (benchmarks_chain.json)
TRIAL = 11.71      # finder trial, TT side incl. top-up, CKF removal, merging, packing, 4 concurrent: FEAS_A §3.4
B1EV = 60.4        # chain + 4 trials, whole job per event, 4 concurrent: FEAS_A §1 / §3.7
RHO2 = 206.0       # one rho = 2 event (2 crossings, 2 roads), smoke SMB2 wall: FEAS_A §3.7  (ESTIMATE: N = 1)
NOPU = 0.0115      # no-PU single interaction, 4 concurrent: FEAS_A §3.6
G4GUN = 0.000134   # Geant4 pion gun, primary-only mode: FEAS_B Task 5
LHE = 0.034        # MG LO + Pythia shower + npz conversion per LHE event: FEAS_B summary 6
MLM = 0.050        # MLM 0-2j per LHE event: NOT BENCHMARKED (FEAS_B open issue 7) -> ESTIMATE
SHOWER = 0.021     # Pythia shower per event: FEAS_B Task 3
S3 = {1: 0.651, 3: 18.8, 5: 67.8}   # Stage 3, F 500 toy, 4 concurrent, s/event: FEAS_A §3.5
TOYS1000 = 652.0   # pyhf 1000 toys at one mu point, 31 parameters: FEAS_C R9
SCAN20 = 10.44     # pyhf 20-point asymptotic scan: FEAS_C R9
SIG = CHAIN + TRIAL  # one signal row: chain with injected quirk hits + 1 trial (ESTIMATE from measured parts)

# ---- Stage 3 summed over the 8 Lambda values (per event) -----------------------------------------------------------
# v1 M3 per-event CPU, p2/BM, F 500 (STAGE3_INDEX.json, read this session)
v1 = {0.45: 0.037, 0.6: 0.080, 0.85: 0.212, 1: 0.334, 1.5: 1.070, 2: 2.528, 3: 8.175, 5: 32.286}
ratio = sum(S3[k] for k in S3) / sum(v1[k] for k in S3)          # measured maxwell / v1 M3 at the 3 anchors
s3_sum = sum(S3[k] for k in S3) + ratio * sum(v for k, v in v1.items() if k not in S3)
s3_at = {k: (S3[k] if k in S3 else ratio * v) for k, v in v1.items()}

# ---- capacity ----------------------------------------------------------------------------------------------------
slot_week = 5 * (11 * 9 + 13 * 12) + 2 * 24 * 12      # weekdays 08-19 at 9 slots, else 12
slot_day = slot_week / 7.0
cap = {"development phases (0.50)": 0.50 * slot_day, "planning value (0.60)": 0.60 * slot_day,
       "production phases (0.75)": 0.75 * slot_day}

items = []  # (phase, item, priority, label, cpu_h, arithmetic)


def add(phase, item, prio, label, seconds, arith):
    items.append((phase, item, prio, label, seconds / H, arith))


# ---- Phase 2 -------------------------------------------------------------------------------------------------------
add("2", "S2/base", "MUST", "Stage 2: 5 species-masses, MLM, 250k LHE each", 5 * 250e3 * MLM, "1.25e6 x 50 ms (ESTIMATE)")
add("2", "S2", "MUST", "NLO K(m): 18 mass points + 2 process generations", 18 * 120 + 2 * 180, "18 x 2 min + 2 x 3 min")
add("2", "S2", "MUST", "FxFx 0-1j point at 500 GeV", 20 * H, "5-20 CPU-h ESTIMATE (FEAS_B); upper value")
add("2", "S2", "MUST", "re-showers: QED FSR, qCut 30/60, Monash (4 variants)", 4 * 1.25e6 * SHOWER, "4 x 1.25e6 x 21 ms")
add("2", "C1", "MUST", "Stage 3 at the 3 C1 points", 463 * s3_at[1.5] + 463 * s3_at[2] + 492 * s3_at[3], "463 x 2.2 + 463 x 5.2 + 492 x 18.8 s")
add("2", "S1", "MUST", "Stage 3 truth, 2000 rows x 5 species-masses x 8 Lambda", 5 * 2000 * s3_sum, f"1e4 x {s3_sum:.1f} s")
add("2", "P1", "MUST", "floor tests, paired B*-off, new gate events", 30 * H, "ESTIMATE: 16 (B*-off, 970 ev) + 2 x 2 (floor) + 10 margin")
add("2", "C1", "MUST", "PU rho = 1, 4000 events x 4 roads", 4000 * B1EV, "4000 x 60.4 s")
add("2", "C1", "MUST", "PU rho = 2, 1000 events (pre-merge dump on)", 1000 * RHO2, "1000 x 206 s")
add("2", "C1", "MUST", "no-PU C'0, v1 sizes (5.4e5 events)", 5.4e5 * NOPU, "5.4e5 x 11.5 ms")
add("2", "C1", "MUST", "C'_PU: 5000 events x 1 road", 5000 * SIG, "5000 x 25.2 s")
add("2", "C1", "MUST", "SM Z(nunu) hit level, 2000 events x 1 road", 2000 * SIG, "2000 x 25.2 s")
add("2", "C1", "MUST", "generator-level N_trig and rates", 5 * H, "ESTIMATE")
add("2", "C1", "MUST", "signal: 3 points x 2 x 200 rows", 3 * 400 * SIG, "1200 x 25.2 s")
add("2", "C2", "MUST", "V4-5 brute force, 100 events", 100 * 0.3 * H, "100 x 0.3 CPU-h ESTIMATE")
add("2", "C2", "MUST", "T_seed 4 -> 2 regression (500 rho=1 + 200 rho=2 events)", 500 * 4 * TRIAL * 3 + 200 * 2 * 74 * 3, "trials x 3 (ESTIMATE slow-down)")
add("2", "C2", "MUST", "V4-4: 20 jobs x 2 reruns x 2 nodes", 20 * 4 * 300, "80 x 5 min")
add("2", "B2", "MUST", "rho = 2 RSS and pre-merge size measurement; frozen-road timing", 10 * H, "ESTIMATE")
# ---- Phase 3 (development, signal blind) ---------------------------------------------------------------------------
add("3", "B1", "MUST", "Geant4 hand-over tests, small P_geo and C_PU samples", 60 * H, "ESTIMATE")
add("3", "B4", "MUST", "MET model, biased multijet generation, small hit samples", 50 * H, "ESTIMATE")
add("3", "B3", "MUST", "conditionals on development samples", 10 * H, "ESTIMATE")
add("3", "B2", "MUST", "occupancy estimator on the Phase-2 PU samples", 10 * H, "ESTIMATE")
add("3", "T1/T2", "MUST", "workspace on v1 counts, toys, injection", 30 * H, "ESTIMATE (40 x 652 s = 7.2 CPU-h per toy pass)")
add("3", "B5", "SHOULD", "sideband prototype", 20 * H, "ESTIMATE")
add("3", "B6", "SHOULD", "variation switches, PU-hit inefficiency", 10 * H, "ESTIMATE")
# ---- Phase 4a (production, after the freeze) ------------------------------------------------------------------------
add("4a", "B2", "MUST", "PU rho = 1 direct, 24000 events x 4 roads", 24000 * B1EV, "24000 x 60.4 s")
add("4a", "B2", "MUST", "PU rho = 2 with pre-merge candidates, 3000 events", 3000 * RHO2, "3000 x 206 s")
add("4a", "B1", "MUST", "Geant4 vertices (1e8 guns, biased)", 20 * H, "1e8 x 0.134 ms = 3.7 CPU-h; x5 for spectra/discs (ESTIMATE)")
add("4a", "B1", "MUST", "no-PU P_geo samples, 4e7 events", 4e7 * NOPU, "4e7 x 11.5 ms")
add("4a", "B1", "MUST", "C_PU overlays, 8 topologies x 2000", 16000 * SIG, "16000 x 25.2 s")
add("4a", "B1", "MUST", "direct full-PU closure samples (3 x 6000 + 5 x 1000)", 23000 * SIG, "23000 x 25.2 s")
add("4a", "B3", "MUST", "conditionals, vertex veto, time tag (re-analysis)", 20 * H, "ESTIMATE")
add("4a", "B4", "MUST", "hit level: 11 new processes x 2000 + Z(nunu) 10000 + 3 x 2000", 38000 * SIG, "38000 x 25.2 s")
add("4a", "B4", "MUST", "no-PU hard-scatter P_geo, 15 x 1e6 events", 15e6 * 0.015, "1.5e7 x 15 ms (ESTIMATE)")
add("4a", "B4", "MUST", "multijet generator level, 1e7 biased events", 1e7 * 0.010, "1e7 x 10 ms (ESTIMATE)")
add("4a", "S1", "MUST", "signal full chain, 40 points x 2000 rows", 80000 * SIG, "80000 x 25.2 s")
add("4a", "T1", "MUST", "expected results with v1 placeholders", 20 * H, "ESTIMATE")
add("4a", "B5", "SHOULD", "FULL: 20 roads on 8000 SM + 500 PU events", 8000 * 19 * TRIAL + 500 * 16 * TRIAL, "8000 x 19 + 500 x 16 trials x 11.7 s")
add("4a", "B5", "SHOULD-red", "REDUCED: 8 roads on 6000 SM + 20 roads on 500 PU events", 6000 * 7 * TRIAL + 500 * 16 * TRIAL, "6000 x 7 + 500 x 16 trials x 11.7 s")
add("4a", "B6", "SHOULD", "FULL: bkg 7 var x 1000 ev; signal 6 pts x 500 rows x 6 var; Stage-3 mv", 7 * 1000 * B1EV + 6 * 500 * 6 * SIG + 2 * 2 * 500 * (s3_at[1.5] + s3_at[3] + s3_at[5]), "see text")
add("4a", "B6", "SHOULD-red", "REDUCED: bkg 7 var x 600 ev; signal 4 pts x 300 rows x 6 var; Stage-3 mv", 7 * 600 * B1EV + 4 * 300 * 6 * SIG + 2 * 2 * 300 * (s3_at[1.5] + s3_at[3]), "see text")
add("4a", "B7", "SHOULD", "toy acceptance for cosmics and halo", 5 * H, "ESTIMATE")
# ---- Phase 4b/4c, 5 --------------------------------------------------------------------------------------------------
add("4b/4c", "T2", "MUST", "ranking: 16 selections x 40 points asymptotic", 16 * 40 * SCAN20, "640 x 10.4 s")
add("4b/4c", "T1", "MUST", "toys: 3 selections x 40 points x 8 mu x 1000 toys", 3 * 40 * 8 * TOYS1000, "960 x 652 s")
add("4b/4c", "MVA", "cross-check", "BDT cross-check (training + evaluation)", 5 * H, "ESTIMATE")
add("5", "figs", "MUST", "figures, reproduction package tests", 10 * H, "ESTIMATE")

print(f"Stage 3: maxwell/M3 ratio at the 3 measured anchors = {ratio:.2f}; sum over 8 Lambda = {s3_sum:.1f} s/event")
print("  per Lambda:", {k: round(v, 2) for k, v in s3_at.items()})
print(f"signal row = {SIG:.1f} s")
print(f"slot-hours per week = {slot_week}, per day = {slot_day:.1f}")
for k, v in cap.items():
    print(f"  effective core-h per day, {k}: {v:.0f}")
print()
print("| phase | item | priority | what | CPU-h | arithmetic |")
print("|---|---|---|---|---|---|")
for p, i, pr, lab, h, a in items:
    print(f"| {p} | {i} | {pr} | {lab} | {h:.1f} | {a} |")


def tot(pred):
    return sum(h for p, i, pr, lab, h, a in items if pred(p, i, pr))


print()
for ph in ["2", "3", "4a", "4b/4c", "5"]:
    print(f"phase {ph}: MUST {tot(lambda p, i, pr: p == ph and pr in ('MUST', 'cross-check')):.0f}"
          f" | SHOULD full {tot(lambda p, i, pr: p == ph and pr == 'SHOULD'):.0f}"
          f" | SHOULD reduced {tot(lambda p, i, pr: p == ph and (pr == 'SHOULD-red' or (pr == 'SHOULD' and i not in ('B5', 'B6')) or (pr == 'SHOULD' and p == '3'))):.0f}")
must = tot(lambda p, i, pr: pr in ("MUST", "cross-check"))
sh_full = tot(lambda p, i, pr: pr == "SHOULD")
sh_red = tot(lambda p, i, pr: pr == "SHOULD-red" or (pr == "SHOULD" and (p == "3" or i == "B7")))
print(f"MUST total {must:.0f}; SHOULD full {sh_full:.0f}; SHOULD reduced {sh_red:.0f}")
print(f"TOTAL full {must + sh_full:.0f}; TOTAL with reduced B5/B6 {must + sh_red:.0f}; with 20 % contingency {1.2 * (must + sh_red):.0f}")
for it in ["C1", "C2", "P1", "S1", "S2", "S2/base", "B1", "B2", "B3", "B4", "T1", "T2", "T1/T2", "B5", "B6", "B7"]:
    print(f"  {it}: MUST/SHOULD-full {tot(lambda p, i, pr: i == it and pr in ('MUST', 'SHOULD')):.0f}"
          f"  reduced {tot(lambda p, i, pr: i == it and pr in ('MUST', 'SHOULD-red')) + tot(lambda p, i, pr: i == it and pr == 'SHOULD' and p == '3'):.0f}")

# ---- storage (GB) ----------------------------------------------------------------------------------------------------
MB_EV = 0.52   # compressed npz per PU-200 event with 4 roads, no dumps: FEAS_A §3.3
pu_events = (4000 + 1000 + 5000 + 2000 + 1200) + (24000 + 3000 + 16000 + 23000 + 38000 + 80000) + (7 * 600 + 4 * 300 * 6)
sto = {
    "PU-200 chain + trial records (%d events x 0.52 MB)" % pu_events: pu_events * MB_EV / 1024,
    "event dumps for 5000 events (2.4 MB each: SMB1 5.30 MB / 2 events minus 0.52)": 5000 * 2.4 / 1024,
    "rho = 2 pre-merge candidates (planning value; cap 400)": 200.0,
    "no-PU samples as per-event summaries (5.5e7 x 50 B) + full records of R04 passers": 5.5e7 * 50 / 1e9 + 15,
    "Stage 2: LHE.gz 0.72 kB + npz 1.05 kB per event, 1.25e6 events, 5 shower variants": 1.25e6 * (0.72 + 5 * 1.05) / 1e6,
    "Stage 3 (8 kB x 80000 rows + C1)": 85000 * 8 / 1e6,
    "Geant4 vertices, job logs, pyhf outputs": 5.0,
    "repo bundles (7 + gates)": 10.0,
}
print()
for k, v in sto.items():
    print(f"  {k}: {v:.1f} GB")
print(f"  storage total {sum(sto.values()):.0f} GB (with the pre-merge cap of 400 GB: {sum(sto.values()) + 200:.0f} GB)")
print(f"  no-PU full records if kept (8.2 kB x 5.5e7): {8.2e3 * 5.5e7 / 1e9:.0f} GB  -> not kept")

# ---- sample-size checks ------------------------------------------------------------------------------------------------
r07 = 35 / 48000.0   # v1 direct rate per trial at R07 (D4 §2.3)
for n in (4000, 12000, 24000):
    c = r07 * 4 * n
    print(f"R07 direct counts for {n} events x 4 roads (v1 rate): {c:.0f}, sigma_ln = {1 / math.sqrt(c):.2f}")
r06 = 11858 / 48000.0
print(f"R06 counts for 4000 events: {r06 * 16000:.0f}")


def binom_tail(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


print(f"V4-5: P(>= 48 of 50 | true agreement 0.85) = {binom_tail(50, 48, 0.85):.4f}; | 0.90: {binom_tail(50, 48, 0.90):.3f}; | 0.98: {binom_tail(50, 48, 0.98):.3f}")
print(f"B*-off paired: N for 5 sigma from 2.1 sigma at N = 171: {171 * (5 / 2.1) ** 2:.0f}; for 3 sigma in the k_B >= 6 subset (2.3 sigma now): x{(3 / 2.3) ** 2:.2f}")
for eps in (0.03, 0.045, 0.08, 0.2):
    n = 1000
    print(f"S1: eps = {eps} (v1 placeholder), n = {n}: relative binomial error {math.sqrt(eps * (1 - eps) / n) / eps:.2f}")
print(f"checks: 0.3/2.71 = {0.3 / 2.71:.4f}; 1.5001 x 1.6061 = {1.5001 * 1.6061:.3f}; log10(1.2346e6/0.11) = {math.log10(1.2346e6 / 0.11):.2f}")
print(f"N_exp(E200) = 219.2 fb x 0.04764 x 3000 fb^-1 x 0.5035 = {219.2 * 0.04764 * 3000 * 0.5035:.0f}; 1.2458e7 / 15775 = {1.2458e7 / 15775:.1f}")
print(f"sideband example: 1.14 x 0.05 x exp(1.105) = {1.14 * 0.05 * math.exp(1.105):.3f}")
print(f"S x eps: 15775 x 9/200 = {15775 * 9 / 200:.0f}")
print(f"jobs: total CPU-h / 0.4 h per job = {(must + sh_red) / 0.4:.0f}; Argo overhead 17 s each = {(must + sh_red) / 0.4 * 17 / H:.0f} slot-h")
