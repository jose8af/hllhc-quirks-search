#!/usr/bin/env python3
"""Arithmetic behind the Phase-1 STRATEGY v2 (STRATEGY_dmitri_2026-11-13_19-25.md).

Standard library only; run as `python3 -I strategy_budget.py` (about a second; allowed on einstein).
History: v1 by Brigitte (17:55); rewritten by the fixer Dmitri for review cycle 1 (arbiter findings M1-M35).
Every unit cost carries a provenance letter:
  M = measured in the feasibility phase (source in the comment);
  D = derived from measured parts, or measured on one event / toy inputs;
  G = guess (not benchmarked).
CPU-h are slot-hours on a worker with 4 jobs per node (the "4 concurrent" columns of FEAS_A).
Sections printed: [1] unit costs, [2] capacity, [3] budget table, [4] totals and variants, [5] deltas per finding,
[6] contingency, [7] calendar, [8] storage, [9] zero-count floors (M6), [10] zero-count likelihood checks (M1),
[11] closure-test size and power (M5, M15), [12] extrapolation width (M4), [13] other checks.
"""
import math
import random

H = 3600.0
# ---- [1] unit costs (seconds) -----------------------------------------------------------------------------------
CHAIN = 13.53      # M  PU-200 event, chain, 4 concurrent: FEAS_A §3.3
TRIAL = 11.71      # M  finder trial incl. top-up, CKF removal, merging, packing: FEAS_A §3.4
B1EV = 60.4        # M  chain + 4 trials, whole job per event: FEAS_A §1 / §3.7
RHO2 = 206.0       # D  one rho = 2 event (2 crossings, 2 roads), one smoke event: FEAS_A §3.7
NOPU = 0.0115      # M  no-PU single minimum-bias interaction through the chain: FEAS_A §3.6
GUN = 0.0141       # M  10-muon gun through Fatras: FEAS_A §3.6
G4GUN = 0.000134   # M  Geant4 pion gun, primary-only mode: FEAS_B Task 5
LHE = 0.034        # D  MG LO + Pythia shower + npz conversion per LHE event: FEAS_B (listed there as derived)
MLM = 0.050        # G  MLM 0-2j per LHE event: not benchmarked (FEAS_B open issue 7)
SHOWER = 0.021     # M  Pythia shower per signal event: FEAS_B Task 3
SHOWER_ZJ = 0.0234  # M  Pythia shower per Z(nunu)+j event: FEAS_B Task 3
MINBIAS = 0.0025   # M  Pythia minimum bias per interaction (2.0-2.5 ms): FEAS_B Task 3
NOPU_HS = 0.045    # G  no-PU hard-scatter event = shower 23.4 ms + chain on a few tracks 14.1 ms + 7.5 ms margin;
#                       the generation filter efficiency is not measured (arbiter §2: 15 ms was below the shower alone)
S3 = {1: 0.651, 3: 18.8, 5: 67.8}   # D  Stage 3, F 500 toy kinematics, s/event: FEAS_A §3.5
TOYS1000 = 652.0   # D  pyhf 1000 s+b and 1000 b toys at one mu point, 31 parameters: FEAS_C R9 (scaling unmeasured)
SCAN20 = 10.44     # D  pyhf 20-point asymptotic scan, 31 parameters: FEAS_C R9
FIT = 0.12         # D  one pyhf fit, 31 parameters: FEAS_C R9
SIG = CHAIN + TRIAL  # D  one PU-200 row with one trial (signal row, overlay, hit-level SM event)

v1s3 = {0.45: 0.037, 0.6: 0.080, 0.85: 0.212, 1: 0.334, 1.5: 1.070, 2: 2.528, 3: 8.175, 5: 32.286}  # STAGE3_INDEX.json
ratio = sum(S3[k] for k in S3) / sum(v1s3[k] for k in S3)
s3_sum = sum(S3[k] for k in S3) + ratio * sum(v for k, v in v1s3.items() if k not in S3)
s3_at = {k: (S3[k] if k in S3 else ratio * v) for k, v in v1s3.items()}

print("[1] unit costs")
print(f"  Stage 3: maxwell/M3 ratio at the 3 anchors = {ratio:.2f}; sum over 8 Lambda = {s3_sum:.1f} s/event")
print("  per Lambda:", {k: round(v, 2) for k, v in s3_at.items()})
print(f"  PU-200 row with one trial = {SIG:.1f} s; trial share of a B1-type event = {4 * TRIAL / B1EV:.3f}")

# ---- [2] capacity --------------------------------------------------------------------------------------------------
# 12 worker cores; 9 on weekdays 08-19 (brief §5.3). Two of three workers had a graphical session at preflight
# (LOG.md 14:34) and are capped at 3 jobs: 3 + 3 + 4 = 10 slots off-hours.
slot_week_12 = 5 * (11 * 9 + 13 * 12) + 2 * 24 * 12
slot_week = 5 * (11 * 9 + 13 * 10) + 2 * 24 * 10
slot_day = slot_week / 7.0
CAP_DEV, CAP_AVG, CAP_PROD = 0.50 * slot_day, 0.60 * slot_day, 0.75 * slot_day
print("\n[2] capacity")
print(f"  slot-h per week: {slot_week} with 10 off-hours slots ({slot_week_12} with 12); per day {slot_day:.1f}")
print(f"  effective core-h per day: development 0.50 -> {CAP_DEV:.0f}; average 0.60 -> {CAP_AVG:.0f}; production 0.75 -> {CAP_PROD:.0f}")
print(f"  if utilisation is 0.40: {0.40 * slot_day:.0f} per day")

# ---- [9a] zero-count floors: inputs (needed before the budget because the no-PU pool is allocated from them) ------
NTRIG = 4.0848e7                      # bsum_wp.json -> n_trig.value (read this session)
RATE = {"PV pair": 30.31, "DIF": 1.5945, "gamma": 0.379, "looper": 0.30, "V0": 0.052,
        "NI 22 mm": 0.11 * 0.22, "NI 30 mm": 0.11 * 0.22, "NI 61.5 mm": 0.11 * 0.22}
#   PV pair, DIF, gamma: D4 l.395 (cprime.<t>.rate); looper 0.30, V0 0.052, NI 0.10-0.12 x 0.22: D2 l.69 (UNVERIFIED)
SM_NTRIG = {"Z(nunu)+j": 25078824.8, "W(tau_h)": 5407122.7, "W(e nu)": 2536644.1, "tt 1l": 2379799.0,
            "W(tau_l)": 2257327.6, "W(mu nu)": 2238036.6, "tW": 259273.4, "tt 2l": 212934.8, "WZ": 137419.5,
            "WW": 126435.9, "t-channel": 110124.9, "ZZ": 104504.5}   # bsum_wp.json -> n_trig.breakdown (read this session)
terms = [(t, NTRIG * r, NOPU) for t, r in RATE.items()] + [(p, n, NOPU_HS) for p, n in SM_NTRIG.items()]
C_POOL = 600.0                        # CPU-h given to the no-PU P_geo pool (GA-3 default)


def allocate(c_total_h, sel=lambda t: True):
    """M_t proportional to sqrt(N_t / c_t) at fixed total cost: minimises sum_t N_t / M_t (Lagrange multiplier)."""
    use = [(t, n, c) for t, n, c in terms if sel(t)]
    norm = sum(math.sqrt(n * c) for t, n, c in use)
    return {t: (c_total_h * H) * math.sqrt(n / c) / norm for t, n, c in use}


alloc = allocate(C_POOL)
SI = [t for t in RATE]
SMP = [p for p in SM_NTRIG]
m_si = sum(alloc[t] for t in SI)
m_sm = sum(alloc[p] for p in SMP)

# ---- [3] budget ------------------------------------------------------------------------------------------------------
items = []  # (phase, item, priority, label, cpu_h, arithmetic, provenance, finding)


def add(phase, item, prio, label, seconds, arith, prov, finding=""):
    items.append((phase, item, prio, label, seconds / H, arith, prov, finding))


# Phase 2
add("2", "S2", "MUST", "Stage 2: 5 species-masses, MLM, 250k LHE each", 5 * 250e3 * MLM, "1.25e6 x 50 ms", "G")
add("2", "S2", "MUST", "NLO K(m): 18 masses + 2 process generations; same scan with PDF4LHC21", 2 * 18 * 120 + 2 * 180, "2 x 18 x 2 min + 2 x 3 min", "M", "C(P-C4)")
add("2", "S2", "MUST", "FxFx 0-1j points at 500 and 1500 GeV", 2 * 20 * H, "2 x 20 CPU-h (upper value of FEAS_B's 5-20)", "G", "C(P-C5)")
add("2", "S2", "MUST", "re-showers: QED FSR, qCut 30/60, Monash (4 variants)", 4 * 1.25e6 * SHOWER, "4 x 1.25e6 x 21 ms", "M")
add("2", "S1", "MUST", "migration sample: generator cut lowered to 150 GeV, 5 x 100k LHE", 5 * 1e5 * MLM, "5e5 x 50 ms", "G", "M27")
add("2", "C1", "MUST", "Stage 3 at the 3 C1 points", 463 * s3_at[1.5] + 463 * s3_at[2] + 492 * s3_at[3], "463 x 2.3 + 463 x 5.4 + 492 x 18.8 s", "D")
add("2", "S1", "MUST", "Stage 3 truth, 2000 rows x 5 species-masses x 8 Lambda", 5 * 2000 * s3_sum, f"1e4 x {s3_sum:.1f} s", "D")
add("2", "P1", "MUST", "B*-off paired, 970 events at 5 keV, on and off", 970 * 2 * S3[5], "970 x 2 x 67.8 s (maxwell timing)", "D", "M19")
add("2", "P1", "MUST", "floor tests, 1 keV B*-off and 5 x 300 new gate events, margin", 14.5 * H, "4 (floor) + 0.5 (1 keV) + 10 margin", "G", "M19")
add("2", "C1", "MUST", "PU rho = 1, 4000 events x 4 roads", 4000 * B1EV, "4000 x 60.4 s", "M")
add("2", "C1", "MUST", "PU rho = 2, 1000 events (pre-merge dump on)", 1000 * RHO2, "1000 x 206 s", "D")
add("2", "C1", "MUST", "no-PU C'0, v1 sizes (5.4e5 events)", 5.4e5 * NOPU, "5.4e5 x 11.5 ms", "M")
add("2", "C1", "MUST", "C'_PU: 5000 events x 1 road", 5000 * SIG, "5000 x 25.2 s", "D")
add("2", "C1", "MUST", "SM Z(nunu) hit level, 2000 events x 1 road", 2000 * SIG, "2000 x 25.2 s", "D")
add("2", "C1", "MUST", "generator-level N_trig and rates", 5 * H, "", "G")
add("2", "C1", "MUST", "signal: 3 points x 400 rows on the v1 path", 3 * 400 * SIG, "1200 x 25.2 s", "D")
add("2", "C1", "MUST", "signal: full-chain twins of the two fast-path points", 2 * 400 * SIG, "800 x 25.2 s", "D", "M21")
add("2", "C2", "MUST", "V4-5 brute force, 100 events", 100 * 0.3 * H, "100 x 0.3 CPU-h", "G")
add("2", "C2", "MUST", "T_seed 4 -> 2 regression (500 rho=1 + 200 rho=2 events)", 500 * 4 * TRIAL * 3 + 200 * 2 * 74 * 3, "trials x 3", "G")
add("2", "C2", "MUST", "V4-4: 20 jobs x 2 reruns x 2 nodes", 20 * 4 * 300, "80 x 5 min", "M")
add("2", "B2", "MUST", "rho = 2 RSS, pre-merge size, thinning N_eff per rung, frozen-road timing", 10 * H, "", "G")
add("2", "B1", "MUST", "enrichment pilot: 1e7 minimum-bias interactions at generator level", 1e7 * MINBIAS, "1e7 x 2.5 ms", "M", "M6")
add("2", "B1", "MUST", "enrichment pilot: 4 x 1e6 unbiased no-PU events (f_k, sagitta bound)", 4e6 * NOPU, "4e6 x 11.5 ms", "M", "M6")
add("2", "B1", "MUST", "enrichment pilot: 1000 overlays of near-pass events", 1000 * SIG, "1000 x 25.2 s", "D", "M3/M6")
add("2", "B3", "MUST", "time-tag: hit-level late-hit density on the C1 events", 5 * H, "", "G", "M16")
add("2", "all", "MUST", "unit-cost timing jobs (no-PU hard scatter, signal row, MLM, 60-100-parameter workspace)", 5 * H, "", "G", "M19")
# Phase 3 (development, signal blind)
add("3", "B1", "MUST", "Geant4 hand-over tests, small P_geo and overlay samples", 60 * H, "", "G")
add("3", "B1", "MUST", "pile-up-vertex secondaries test: 1000 PU events with Geant4 secondaries", 1000 * (B1EV + 2.7), "1000 x (60.4 + 2.7) s", "D", "M26")
add("3", "B4", "MUST", "MET model, biased multijet generation, small hit samples", 50 * H, "", "G")
add("3", "B3", "MUST", "conditionals on development samples", 10 * H, "", "G")
add("3", "B2", "MUST", "occupancy estimator on the Phase-2 PU samples", 10 * H, "", "G")
add("3", "T1", "MUST", "workspace on v1 counts; zero-count tests (limiting case, large count, coverage); injection", 60 * H, "30 (v1) + 30", "G", "M1/M7")
add("3", "dev", "MUST", "enlarged development closure samples (idle pre-freeze capacity)", 100 * H, "about 5,960 B1-type events", "G", "C(N-C-6)")
add("3", "B5", "SHOULD", "sideband prototype", 20 * H, "", "G")
add("3", "B6", "SHOULD", "variation switches, PU-hit inefficiency", 10 * H, "", "G")
# Phase 4a (production, after the freeze)
add("4a", "B2", "MUST", "PU rho = 1 direct, 24000 events x 4 roads", 24000 * B1EV, "24000 x 60.4 s", "M")
add("4a", "B2", "MUST", "PU rho = 2 with pre-merge candidates, 3000 events", 3000 * RHO2, "3000 x 206 s", "D")
G4_DEC, G4_NI = 0.011, 0.042   # M  vertices per pion gun (pT 1-10 GeV, |eta| < 1): decays, inelastic: FEAS_B Task 5
add("4a", "B1", "MUST", "Geant4 vertices, unbiased: one distinct vertex per no-PU event (DIF and NI)", (alloc["DIF"] / G4_DEC + 3 * alloc["NI 22 mm"] / G4_NI) * G4GUN,
    f"({alloc['DIF']:.3g} / 0.011 + {3 * alloc['NI 22 mm']:.3g} / 0.042) guns x 0.134 ms", "D", "C(K-C7)")
add("4a", "B1", "MUST", "Geant4: photon conversions, realistic spectra, discs, I/O", 15 * H, "", "G")
add("4a", "B1", "MUST", "QGSP_BERT and composition variations: Geant4 + 5e6 no-PU events each", 2 * (10 * H + 5e6 * NOPU), "2 x (10 CPU-h + 5e6 x 11.5 ms)", "G", "M19")
add("4a", "B1", "MUST", f"no-PU pool, single-interaction share: {m_si:.3g} events", m_si * NOPU, f"{m_si:.3g} x 11.5 ms", "M", "M6")
add("4a", "B4", "MUST", f"no-PU pool, SM hard-scatter share: {m_sm:.3g} events", m_sm * NOPU_HS, f"{m_sm:.3g} x 45 ms", "G", "M6/M19")
add("4a", "B1", "MUST", "overlays: 4 x 9000 + 4 x 1500 events (derivation, near-pass, held-out test)", 42000 * SIG, "42000 x 25.2 s", "D", "M3/M5")
add("4a", "B3", "MUST", "conditionals, vertex veto, stability across rungs, time-tag closure (re-analysis)", 25 * H, "20 + 5", "G", "M16")
add("4a", "B4", "MUST", "hit level: 11 new processes x 2000 + Z(nunu) 10000 + 3 x 2000", 38000 * SIG, "38000 x 25.2 s", "D")
add("4a", "B4", "MUST", "multijet generator level, 1e7 biased events", 1e7 * SHOWER_ZJ, "1e7 x 23.4 ms (shower alone)", "D", "M19")
add("4a", "B4", "MUST", "multijet loose population through the no-PU chain, 1e6 events", 1e6 * NOPU_HS, "1e6 x 45 ms", "G", "M33")
add("4a", "S1", "MUST", "signal full chain, 40 points x 2000 rows", 80000 * SIG, "80000 x 25.2 s", "D")
add("4a", "T1", "MUST", "expected results with v1 placeholders", 20 * H, "", "G")
add("4a", "T1", "MUST", "coverage test: null distributions for m' = 0..6 at 2 points", 2 * 7 * 8 * TOYS1000, "2 x 7 x 8 x 652 s", "G", "M1")
add("4a", "B5", "SHOULD", "FULL: 20 roads on 8000 SM + 500 PU events", 8000 * 19 * TRIAL + 500 * 16 * TRIAL, "(8000 x 19 + 500 x 16) x 11.7 s", "M")
add("4a", "B5", "SHOULD-red", "REDUCED: 8 roads on 6000 SM + 20 roads on 500 PU events", 6000 * 7 * TRIAL + 500 * 16 * TRIAL, "(6000 x 7 + 500 x 16) x 11.7 s", "M")
add("4a", "B5", "SHOULD-both", "hard-scatter T(dphi) on the no-PU samples (road rotation)", 10 * H, "", "G", "M31")
add("4a", "B6", "SHOULD", "FULL: bkg 7 var x 1000 ev; signal 6 pts x 500 rows x 6 var; Stage-3 material",
    7 * 1000 * B1EV + 6 * 500 * 6 * SIG + 2 * 2 * 500 * (s3_at[1.5] + s3_at[3] + s3_at[5]), "see text", "D")
add("4a", "B6", "SHOULD-red", "REDUCED: bkg 7 var x 600 ev; signal 4 pts x 300 rows x 6 var; Stage-3 material",
    7 * 600 * B1EV + 4 * 300 * 6 * SIG + 2 * 2 * 300 * (s3_at[1.5] + 2 * s3_at[3] + s3_at[5]), "points E200/1.5, E500/3, E500/5, E1000/3", "D", "M13")
add("4a", "B6", "SHOULD", "FULL: nominal partners of the varied samples (1000 bkg events, 6 x 500 signal rows)", 1000 * B1EV + 6 * 500 * SIG, "1000 x 60.4 s + 3000 x 25.2 s", "D", "M17")
add("4a", "B6", "SHOULD-red", "REDUCED: nominal partners (600 bkg events, 4 x 300 signal rows)", 600 * B1EV + 4 * 300 * SIG, "600 x 60.4 s + 1200 x 25.2 s", "D", "M17")
add("4a", "B6", "SHOULD-both", "variations propagated to single-interaction and SM terms: 4 x (2e6 + 5e5) no-PU events",
    4 * (2e6 * NOPU + 5e5 * NOPU_HS), "4 x (2e6 x 11.5 ms + 5e5 x 45 ms)", "G", "M12")
add("4a", "B7", "SHOULD-both", "toy acceptance for cosmics, halo, beam gas", 5 * H, "", "G")
# Phase 4b/4c, 5
add("4b", "T2", "MUST", "ranking: 16 selections x 40 points asymptotic", 16 * 40 * SCAN20, "640 x 10.4 s", "D")
add("4b", "T2", "MUST", "background-side bootstrap: 50 replicas x 5 selections x 20 points", 50 * 5 * 20 * SCAN20, "5000 x 10.4 s", "D", "M29")
add("4b", "T1", "MUST", "toys pass 1: 5 best selections x 20 window points x 8 mu x 1000", 5 * 20 * 8 * TOYS1000, "800 x 652 s", "G", "M8/C(P-C3)")
add("4c", "T1", "MUST", "toys pass 2: 3 selections x 40 points x 8 mu x 1000", 3 * 40 * 8 * TOYS1000, "960 x 652 s", "G", "M8")
add("4c", "T1", "MUST", "coverage at injected mu: 500 pseudo-experiments x 2 points x 16 fits", 500 * 2 * 16 * FIT, "16000 x 0.12 s", "D", "M8")
add("4c", "MVA", "MUST", "BDT cross-check; dE/dx forgone-gain ratio", 7 * H, "5 + 2", "G", "M30")
add("5", "figs", "MUST", "figures, reproduction package tests", 10 * H, "", "G")

print("\n[3] budget lines")
print("| phase | item | priority | what | CPU-h | arithmetic | prov. | finding |")
print("|---|---|---|---|---|---|---|---|")
for p, i, pr, lab, h, a, pv, f in items:
    print(f"| {p} | {i} | {pr} | {lab} | {h:.1f} | {a} | {pv} | {f} |")


def tot(pred):
    return sum(h for p, i, pr, lab, h, a, pv, f in items if pred(p, i, pr))


def is_must(pr):
    return pr == "MUST"


def in_red(pr):
    return pr in ("SHOULD-red", "SHOULD-both")


def in_full(pr):
    return pr in ("SHOULD", "SHOULD-both")


def sh_red(p, i, pr):   # reduced SHOULD variant: Phase-3 prototypes are needed in both variants
    return in_red(pr) or (pr == "SHOULD" and p == "3")


def sh_full(p, i, pr):
    return in_full(pr)


PH = ["2", "3", "4a", "4b", "4c", "5"]
print("\n[4] totals")
for ph in PH:
    print(f"  phase {ph}: MUST {tot(lambda p, i, pr: p == ph and is_must(pr)):.0f}"
          f" | SHOULD full {tot(lambda p, i, pr: p == ph and sh_full(p, i, pr)):.0f}"
          f" | SHOULD reduced {tot(lambda p, i, pr: p == ph and sh_red(p, i, pr)):.0f}")
must = tot(lambda p, i, pr: is_must(pr))
shf = tot(sh_full)
shr = tot(sh_red)
print(f"  MUST-only {must:.0f}; MUST + SHOULD reduced {must + shr:.0f}; MUST + SHOULD full {must + shf:.0f}")
print(f"  SHOULD reduced {shr:.0f}; SHOULD full {shf:.0f}; DP1 + DP2 saving {shf - shr:.0f}")
for it in ["C1", "C2", "P1", "S1", "S2", "B1", "B2", "B3", "B4", "T1", "T2", "MVA", "dev", "all", "figs", "B5", "B6", "B7"]:
    print(f"  {it}: MUST {tot(lambda p, i, pr: i == it and is_must(pr)):.0f}"
          f" | SHOULD full {tot(lambda p, i, pr: i == it and sh_full(p, i, pr)):.0f}"
          f" | reduced {tot(lambda p, i, pr: i == it and sh_red(p, i, pr)):.0f}")
prod_must_bkg = tot(lambda p, i, pr: p == "4a" and is_must(pr) and i != "S1")
prod_s1 = tot(lambda p, i, pr: p == "4a" and i == "S1")
prod_red = tot(lambda p, i, pr: p == "4a" and sh_red(p, i, pr))
prod_full = tot(lambda p, i, pr: p == "4a" and sh_full(p, i, pr))
print(f"  Phase 4a: background and T1 MUST {prod_must_bkg:.0f}; S1 chain {prod_s1:.0f}; SHOULD reduced {prod_red:.0f}; SHOULD full {prod_full:.0f}")

# ---- [5] deltas against v1 per finding ---------------------------------------------------------------------------------
V1 = {"MUST": 2950.0, "RED": 3275.0, "FULL": 3798.0}
p_geo_v1 = 4e7 * NOPU / H + 15e6 * 0.015 / H
deltas = [
    ("M6 no-PU pool 600 CPU-h (v1: 4e7 x 11.5 ms + 1.5e7 x 15 ms)", C_POOL - p_geo_v1),
    ("  of which M19: v1 hard-scatter line at 45 ms instead of 15 ms", 15e6 * (NOPU_HS - 0.015) / H),
    ("M6 enrichment pilot (Phase 2)", (1e7 * MINBIAS + 4e6 * NOPU + 1000 * SIG) / H),
    ("M3/M5 overlays 42,000 instead of 39,000 events", 3000 * SIG / H),
    ("M8 second toy pass and five selections in pass 1 (v1: 174)", (5 * 20 * 8 + 3 * 40 * 8) * TOYS1000 / H - 174.0),
    ("M1/M7/M8 T1 development and validation (Phase 3 +30, coverage toys, pseudo-experiments)", 30 + 2 * 7 * 8 * TOYS1000 / H + 500 * 2 * 16 * FIT / H),
    ("M29 background-side bootstrap of T2", 50 * 5 * 20 * SCAN20 / H),
    ("M19 multijet generator level at 23.4 ms (v1: 10 ms)", 1e7 * (SHOWER_ZJ - 0.010) / H),
    ("M33 multijet loose population", 1e6 * NOPU_HS / H),
    ("M19 P1 on maxwell timing (v1: 30)", (970 * 2 * S3[5] + 14.5 * H) / H - 30.0),
    ("M19 QGSP_BERT and composition variations", 2 * (10 * H + 5e6 * NOPU) / H),
    ("C(K-C7) Geant4 vertices sized to one distinct vertex per event (v1: 20)", (alloc["DIF"] / G4_DEC + 3 * alloc["NI 22 mm"] / G4_NI) * G4GUN / H + 15.0 - 20.0),
    ("M19 unit-cost timing jobs", 5.0),
    ("M26 pile-up-vertex secondaries test", 1000 * (B1EV + 2.7) / H),
    ("M16 time-tag hit-level measurement and closure", 10.0),
    ("M21 full-chain twins of the two C1 fast-path points", 800 * SIG / H),
    ("M27 migration sample", 5e5 * MLM / H),
    ("M30 dE/dx forgone-gain ratio", 2.0),
    ("C(P-C4, P-C5) PDF4LHC21 K scan and FxFx at 1500 GeV", 18 * 120 / H + 20.0),
    ("C(N-C-6) enlarged development samples", 100.0),
    ("M12 detector variations on single-interaction and SM terms (SHOULD, both variants)", 4 * (2e6 * NOPU + 5e5 * NOPU_HS) / H),
    ("M31 hard-scatter T(dphi) on no-PU samples (SHOULD, both variants)", 10.0),
    ("M13 reduced B6 keeps 5 keV and E 1000 (SHOULD reduced)", 2 * 2 * 300 * (s3_at[3] + s3_at[5]) / H),
    ("M17 B6 nominal partner samples (SHOULD reduced; full: +%.1f)" % ((1000 * B1EV + 6 * 500 * SIG) / H), (600 * B1EV + 4 * 300 * SIG) / H),
]
print("\n[5] deltas against v1, per finding (CPU-h; days at the production capacity)")
for lab, d in deltas:
    print(f"  {d:+8.1f} CPU-h  {d / CAP_PROD:+5.2f} d   {lab}")
print(f"  v1 -> v2: MUST {V1['MUST']:.0f} -> {must:.0f} ({must - V1['MUST']:+.0f}); reduced {V1['RED']:.0f} -> {must + shr:.0f} ({must + shr - V1['RED']:+.0f});"
      f" full {V1['FULL']:.0f} -> {must + shf:.0f} ({must + shf - V1['FULL']:+.0f})")

# ---- [6] contingency from provenance --------------------------------------------------------------------------------------
FRAC = {"M": 0.10, "D": 0.30, "G": 1.00}
print("\n[6] provenance and contingency (reduced variant)")
cont = 0.0
for pv in "MDG":
    s = sum(h for p, i, pr, lab, h, a, v, f in items if v == pv and (is_must(pr) or sh_red(p, i, pr)))
    cont += FRAC[pv] * s
    print(f"  provenance {pv}: {s:.0f} CPU-h, carried at {FRAC[pv]:.0%} -> {FRAC[pv] * s:.0f}")
RESERVE = 24000 * B1EV / H
print(f"  contingency from provenance {cont:.0f} CPU-h; fresh-sample reserve (one B2 direct sample) {RESERVE:.0f} CPU-h")
print(f"  reduced total with both: {must + shr + cont + RESERVE:.0f} CPU-h; stop-and-ask threshold 1.3 x {must + shr:.0f} = {1.3 * (must + shr):.0f}")
print(f"  S1 at 4000 rows (GA-2): +{80000 * SIG / H + 5 * 2000 * s3_sum / H:.0f} CPU-h = {(80000 * SIG / H + 5 * 2000 * s3_sum / H) / CAP_PROD:.1f} production days")
print(f"  S4 if requested: finder rerun on background samples = {(24000 * 4 * TRIAL + 3000 * 2 * 74 + (42000 + 38000) * TRIAL) / H:.0f} CPU-h")

# ---- [7] calendar -------------------------------------------------------------------------------------------------------------
print("\n[7] calendar (days after Gate A)")
ph2_cpu = tot(lambda p, i, pr: p == "2" and is_must(pr))
ph3_cpu = tot(lambda p, i, pr: p == "3" and (is_must(pr) or pr == "SHOULD"))
print(f"  Phase 2 CPU {ph2_cpu:.0f} (of which S1 string {5 * 2000 * s3_sum / H:.0f} is filler into Phase 3): critical part"
      f" {ph2_cpu - 5 * 2000 * s3_sum / H:.0f} / {CAP_DEV:.0f} = {(ph2_cpu - 5 * 2000 * s3_sum / H) / CAP_DEV:.1f} days")
print(f"  Phase 3 CPU {ph3_cpu:.0f}; capacity in Phases 2 + 3 + freeze (20 days x {CAP_DEV:.0f}) = {20 * CAP_DEV:.0f}; idle {20 * CAP_DEV - ph2_cpu - ph3_cpu:.0f}")
FIXED = [("Phase 2", 7), ("Phase 3 development", 9), ("freeze: PREREG_v2 and 4-bot review", 2), ("ITERATE allowance (freeze)", 2),
         ("4a review (4-bot + bib)", 3), ("ITERATE allowance (4a)", 2), ("4b: T2, toys, 4-bot + bib", 3), ("ITERATE allowance (4b)", 2),
         ("Gate B turnaround", 2), ("4c and 1-bot review", 3), ("Phase 5", 7), ("ITERATE allowance (5-bot)", 2)]
nonprod = sum(d for _, d in FIXED)
for lab, d in FIXED:
    print(f"    {d:2d} d  {lab}")
print(f"  non-production days: {nonprod} (v1 schedule: 30.7 without allowances) -> already above the 28 days of a 4-week target")
for name, cpu in [("MUST-only", prod_must_bkg), ("MUST + SHOULD reduced", prod_must_bkg + prod_red), ("MUST + SHOULD full", prod_must_bkg + prod_full)]:
    d = cpu / CAP_PROD
    s1d = prod_s1 / CAP_PROD
    print(f"  {name}: 4a background production {cpu:.0f} CPU-h = {d:.1f} days; S1 chain {prod_s1:.0f} CPU-h = {s1d:.1f} days runs during the"
          f" 4a review (5 days); total {nonprod + d:.1f} days = {(nonprod + d) / 7:.1f} weeks;"
          f" at utilisation 0.50 in production: {nonprod + cpu / CAP_DEV:.1f} days")
toys = (5 * 20 * 8 + 3 * 40 * 8) * TOYS1000 / H
print(f"  toys 4b {5 * 20 * 8 * TOYS1000 / H:.1f} + 4c {3 * 40 * 8 * TOYS1000 / H:.1f} = {toys:.1f} CPU-h; at {CAP_PROD:.0f}/day: {5 * 20 * 8 * TOYS1000 / H / CAP_PROD:.1f} and {3 * 40 * 8 * TOYS1000 / H / CAP_PROD:.1f} days (inside the 3-day windows)")
print(f"  old T1-g if done with nested toys: 500 x 2 x 8 x 652 s = {500 * 2 * 8 * 652 / H:.0f} CPU-h (not done)")

# ---- [8] storage (GB) -----------------------------------------------------------------------------------------------------------
MB_EV = 0.52
pu_events = (4000 + 5000 + 2000 + 1200 + 800 + 1000 + 1000) + (24000 + 42000 + 38000 + 80000) + (8 * 600 + 4 * 300 * 7) + 5960
rho2_events = 1000 + 3000 + 200
nopu_events = m_si + m_sm + 5.4e5 + 4e6 + 1e7 + 1e6 + 4 * 2.5e6
sto = {
    "PU-200 chain + trial records (%d events x 0.52 MB)" % pu_events: pu_events * MB_EV / 1024,
    "rho = 2 events with dumps (%d x 4.0 MB)" % rho2_events: rho2_events * 4.0 / 1024,
    "hit dumps for 10,000 events (C2 700, B5 6,500, occupancy model and time tag 2,800; 2.4 MB each)": 10000 * 2.4 / 1024,
    "rho = 2 pre-merge candidates (planning value; cap 400)": 200.0,
    "no-PU samples as per-event summaries (%.3g x 50 B) + full records of R04 passers and near-pass events" % nopu_events: nopu_events * 50 / 1e9 + 25,
    "Stage 2: 1.75e6 LHE events, 5 shower variants": 1.75e6 * (0.72 + 5 * 1.05) / 1e6,
    "Stage 3 (8 kB x 85000 rows)": 85000 * 8 / 1e6,
    "Geant4 vertices, job logs, pyhf outputs, toy distributions": 8.0,
    "repo bundles (7 + gates)": 10.0,
}
print("\n[8] storage")
for k, v in sto.items():
    print(f"  {k}: {v:.1f} GB")
print(f"  storage total {sum(sto.values()):.0f} GB (with the pre-merge cap of 400 GB: {sum(sto.values()) + 200:.0f} GB)")
print(f"  no-PU full records if kept (8.2 kB x {nopu_events:.3g}): {8.2e3 * nopu_events / 1e9:.0f} GB -> not kept")
print(f"  jobs: reduced total / 0.4 h per job = {(must + shr) / 0.4:.0f}; Argo overhead 17 s each = {(must + shr) / 0.4 * 17 / H:.0f} slot-h")

# ---- [9] zero-count floors (M6) ----------------------------------------------------------------------------------------------------
print("\n[9] zero-count floors: events in 3 ab^-1 that a zero count still allows (before pile-up factors and conditionals)")
print("  convention: 68 % upper value 1.14 N_t / M_t (= -ln 0.32); predictive mean N_t / M_t")
U68 = -math.log(0.32)
v1_m = {"PV pair": 1e7, "DIF": 1e7, "gamma": 1e7, "V0": 1e7}
print("  v1 plan (1e7 for four topologies, 1e6 per SM process):")
f_v1 = {t: U68 * NTRIG * RATE[t] / v1_m[t] for t in v1_m}
f_v1_sm = sum(U68 * n / 1e6 for n in SM_NTRIG.values())
print("   ", {t: round(v, 2) for t, v in f_v1.items()}, f"sum {sum(f_v1.values()):.1f}; SM sum {f_v1_sm:.1f} (Z(nunu) {U68 * SM_NTRIG['Z(nunu)+j'] / 1e6:.1f})")
sq = sum(math.sqrt(RATE[t]) for t in v1_m)
f_sq = {t: U68 * NTRIG * RATE[t] / (4e7 * math.sqrt(RATE[t]) / sq) for t in v1_m}
print(f"    same 4e7 events by sqrt(rate): sum {sum(f_sq.values()):.1f}")


def floor_table(c_h):
    al = allocate(c_h)
    rows = [(t, n, al[t], U68 * n / al[t], n / al[t]) for t, n, c in terms]
    return rows


for c_h in (315.3, C_POOL, 1200.0):
    rows = floor_table(c_h)
    s68 = sum(r[3] for r in rows)
    si68 = sum(r[3] for r in rows if r[0] in RATE)
    print(f"  pool {c_h:.0f} CPU-h: sum of floors {s68:.1f} (single interaction {si68:.1f}, SM {s68 - si68:.1f}); sum of means {sum(r[4] for r in rows):.1f}")
print(f"  | term | N_t in 3 ab^-1 | M_t planned | transfer factor N_t/M_t | floor at 68 % (1.14 N/M) |   (pool {C_POOL:.0f} CPU-h)")
rows = floor_table(C_POOL)
for t, n, m, f68, mean in rows:
    print(f"  | {t} | {n:.3g} | {m:.3g} | {mean:.2f} | {f68:.2f} |")
print(f"  events in the pool: single interaction {m_si:.3g}, SM {m_sm:.3g}")
random.seed(20261113)
means = [r[4] for r in rows]
draws = sorted(sum(mu * random.expovariate(1.0) for mu in means) for _ in range(200000))
q = lambda f: draws[int(f * len(draws))]
print(f"  predictive distribution of the summed floor (each term N/M x Exp(1)): 16 % {q(0.16):.1f}, median {q(0.5):.1f}, 84 % {q(0.84):.1f},"
      f" mean {sum(means):.1f}; sigma_ln = 0.5 ln(q84/q16) = {0.5 * math.log(q(0.84) / q(0.16)):.2f}")
print(f"  enrichment G needed to bring the summed 68 % floor to 10 / 1 / 0.11 events: {sum(r[3] for r in rows) / 10:.1f} / {sum(r[3] for r in rows):.0f} / {sum(r[3] for r in rows) / 0.11:.0f}")
print(f"  road-multiplicity ceiling for unoriented single interactions: 2 pi / 0.30 = {2 * math.pi / 0.30:.1f}")


def trigamma(x):
    s = 0.0
    while x < 30:
        s += 1.0 / (x * x)
        x += 1
    return s + 1 / x + 1 / (2 * x * x) + 1 / (6 * x ** 3) - 1 / (30 * x ** 5)


print("  sd of ln(lambda) for lambda ~ Gamma(m + 1):", {m: round(math.sqrt(trigamma(m + 1)), 2) for m in (0, 1, 2, 3, 5, 10, 100)})
print("  quantiles of Gamma(1) (m = 0): 16 %% %.3f, median %.3f, 68 %% %.3f, 84 %% %.3f, 95 %% %.3f" % (
    -math.log(0.84), math.log(2), U68, -math.log(0.16), -math.log(0.05)))

# ---- [10] zero-count likelihood: one-bin analytic checks (M1) ----------------------------------------------------------------------
# One bin, one background term B = kappa * lambda, auxiliary count m = 0, lambda ~ Gamma(1) (flat prior).
# Marginal: P(n | s) = sum_k Pois(k | s) q^(n-k) (1-q), q = kappa / (1 + kappa)   [integral of Pois(n | kappa lambda) e^-lambda].
# CLs(s; n_obs) = P(n <= n_obs | s) / P(n <= n_obs | 0); s95 solves CLs = 0.05.


def pois_pmf(k, mu):
    if mu <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(mu) - mu - math.lgamma(k + 1))


def cdf_hybrid(nobs, s, kappa):
    qq = kappa / (1.0 + kappa)
    return sum(pois_pmf(k, s) * (1.0 - qq ** (nobs - k + 1)) for k in range(0, nobs + 1))


def cdf_pois(nobs, mu):
    return sum(pois_pmf(k, mu) for k in range(0, nobs + 1))


def s95(nobs, cls):
    lo, hi = 0.0, 50.0 + 20.0 * (nobs + 1)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if cls(nobs, mid) > 0.05:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def quant_geo(kappa, f):
    qq = kappa / (1.0 + kappa)
    n = 0
    while 1.0 - qq ** (n + 1) < f:
        n += 1
    return n


def median_pois(mu):
    n, c = 0, pois_pmf(0, mu)
    while c < 0.5:
        n += 1
        c += pois_pmf(n, mu)
    return n


print("\n[10] one bin, one zero-count term with transfer factor kappa = N/M: expected 95 % CLs limit on the signal yield s")
print("  check of the marginal: sum_n kappa^n/(1+kappa)^(n+1) = 1 and mean = kappa:",
      [(k, round(sum((k / (1 + k)) ** n / (1 + k) for n in range(4000)), 6), round(sum(n * (k / (1 + k)) ** n / (1 + k) for n in range(4000)), 3)) for k in (0.5, 10.0)])
print("  | kappa | term dropped (lambda = 0) | fixed B = 1.14 kappa | hybrid Gamma(1): median [16 %, 84 %] | true lambda = 0.5 / 1.14 / 2 / 3: median limit of the same procedure |")
for kappa in (0.1, 1.0, 10.0, 35.0, 124.0):
    cls_h = lambda n, s, k=kappa: cdf_hybrid(n, s, k) / cdf_hybrid(n, 0.0, k)
    cls_f = lambda n, s, k=kappa: cdf_pois(n, s + U68 * k) / cdf_pois(n, U68 * k)
    hyb = [s95(quant_geo(kappa, f), cls_h) for f in (0.16, 0.5, 0.84)]
    fix = s95(median_pois(U68 * kappa), cls_f)
    tru = [s95(median_pois(lam * kappa), cls_h) for lam in (0.5, U68, 2.0, 3.0)]
    print(f"  | {kappa:g} | {-math.log(0.05):.2f} | {fix:.1f} | {hyb[1]:.1f} [{hyb[0]:.1f}, {hyb[2]:.1f}] | " + " / ".join(f"{x:.1f}" for x in tru) + " |")
print("  coverage of the hybrid limit, one bin, true signal s = 10, simulation redone in every pseudo-experiment (exact sums):")
for kappa in (1.0, 10.0):
    for lam in (0.5, U68, 2.0, 3.0):
        # m ~ Pois(lam): for m = 0 the procedure above; for m >= 1 the posterior Gamma(m+1) (negative binomial marginal)
        def cdf_nb(nobs, s, m, k=kappa):
            p = 1.0 / (1.0 + k)
            tot_ = 0.0
            for j in range(0, nobs + 1):
                pj = pois_pmf(j, s)
                if pj < 1e-15:
                    continue
                c = 0.0
                for b in range(0, nobs - j + 1):
                    c += math.exp(math.lgamma(b + m + 1) - math.lgamma(b + 1) - math.lgamma(m + 1) + (m + 1) * math.log(p) + b * math.log(1 - p))
                tot_ += pj * c
            return tot_
        cov = 0.0
        cov0 = 0.0
        for m in range(0, 14):
            pm = pois_pmf(m, lam)
            if pm < 1e-6:
                continue
            mu_true = 10.0 + lam * kappa
            cm = 0.0
            for n in range(0, int(mu_true + 12 * math.sqrt(mu_true) + 12)):
                pn = pois_pmf(n, mu_true)
                if pn < 1e-9:
                    continue
                cls = cdf_nb(n, 10.0, m) / cdf_nb(n, 0.0, m)
                if cls > 0.05:      # s = 10 not excluded: limit >= true value
                    cm += pn
            cov += pm * cm
            if m == 0:
                cov0 = cm
        print(f"    kappa {kappa:g}, true lambda {lam:.2f}: P(m = 0) = {math.exp(-lam):.2f}; coverage {cov:.3f}; given m = 0: {cov0:.3f}")

# ---- [11] closure tests: size and power (M5, M15) ----------------------------------------------------------------------------------


def Phi(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


print("\n[11] closure criterion (a) |ln r| <= ln F evaluated only where sigma_tot = sqrt(1/N + s_P^2) <= ln F / 3")
for F in (1.5, 2.0):
    lim = math.log(F) / 3
    nmin = {sp: (math.ceil(1.0 / (lim * lim - sp * sp)) if lim > sp else None) for sp in (0.0, 0.05, 0.10)}
    print(f"  F = {F}: ln F = {math.log(F):.3f}, sigma limit {lim:.3f}; minimum direct count N for s_P = 0 / 0.05 / 0.10: {nmin[0.0]} / {nmin[0.05]} / {nmin[0.10]}")
    for mult in (1.0, 1.5, 2.0):
        d = mult * math.log(F)
        pf = Phi((d - math.log(F)) / lim) + Phi((-d - math.log(F)) / lim)
        print(f"    at the limit precision: P(fail | true ln r = {mult} ln F) = {pf:.4f}")
    print(f"    false fail at r = 1: {2 * Phi(-3):.4f}")
print("  v1 criterion (N >= 20, s_P = 0.1) for comparison: false fail at r = 1, F = 1.5: %.3f at N = 20, %.3f at N = 30; F = 2 at N = 20: %.4f" % (
    2 * Phi(-math.log(1.5) / math.sqrt(1 / 20 + 0.01)), 2 * Phi(-math.log(1.5) / math.sqrt(1 / 30 + 0.01)), 2 * Phi(-math.log(2) / math.sqrt(1 / 20 + 0.01))))
print("  family-wise: probability that a correct analysis passes K independent p > 0.05 tests:", {K: round(0.95 ** K, 2) for K in (8, 12, 20)})
for K in (8, 12, 20):
    per = 0.05 / K + (0.05 - 0.05 / K) * 0.05
    print(f"    v2 rule, K = {K}: per-test false fail {per:.4f} (outright {0.05 / K:.4f} + investigate-then-fail {(0.05 - 0.05 / K) * 0.05:.4f});"
          f" family {1 - (1 - per) ** K:.3f}; with criterion (a) at 0.0027 each: {1 - ((1 - per) * (1 - 0.0027)) ** K:.3f};"
          f" expected fresh-sample retests {K * (0.05 - 0.05 / K):.2f}")
lnr = [0.406, 0.474, -0.455, -0.954]
print(f"  retroactive v1 thinning (ln r = {lnr}): criterion (a) at F = 1.5 fails at {sum(abs(x) > math.log(1.5) for x in lnr)} of 4 rungs;"
      f" diagonal chi2 with s_model at the cap = {sum(x * x for x in lnr) / math.log(1.5) ** 2:.1f} on 4 dof")
print("  expected direct attributed counts, unenriched, from the v1 C'_PU record (per 500 events; D4 l.196-200):")
per500 = {"DIF": (166, 81, 2, 1), "gamma": (153, 86, 13, 2), "V0": (859, 358, 6, 0), "PV pair": (1, 0.25, 0, 0)}
for t, c in per500.items():
    print(f"    {t}: in 4000 events R04..R07 = {[round(x * 8, 1) for x in c]}; events needed for N = 24 at R06: "
          + (f"{24 / c[2] * 500:.0f}" if c[2] else "no count in v1") + "; at R07: " + (f"{24 / c[3] * 500:.0f}" if c[3] else "no count in v1"))
print(f"  pile-up direct: 96,000 trials x 7.29e-4 = {96000 * 35 / 48000:.0f} counts at R07, sigma_ln = {1 / math.sqrt(70):.3f} (limit for F = 1.5: {math.log(1.5) / 3:.3f})")
print(f"  thinning effective counts per 6000 rho = 2 trials (1/s_boot^2): R04 {1 / 0.0077 ** 2:.0f}, R05 {1 / 0.0079 ** 2:.0f}, R06 {1 / 0.0060 ** 2:.0f};"
      f" direct counts in 6000 rho = 1 trials at R06: {0.2470 * 6000:.0f}, at R07: {35 / 48000 * 6000:.1f}")

# ---- [12] extrapolation width (M4) ----------------------------------------------------------------------------------------------------
print("\n[12] extrapolation width s_tot(r)^2 = s_model^2 + (b^2 + sigma_b^2) d_in^2 + b0^2 d_out^2")
print("  (d_in: rungs beyond the last tested rung inside a tested cut family; d_out: rungs in untested families; b0 = ln F)")
FAM = {"width": (5, 8), "chi2": (9, 11), "2S": (12, 14), "shape": (15, 20)}
for name, sb, F, smod in (("pile-up (sigma_b = 0.029, F = 1.5, s_model = 0.20)", 0.029, 1.5, 0.20), ("single interaction (sigma_b = 0.097, F = 2, s_model = 0.35)", 0.097, 2.0, 0.35)):
    out = {}
    for r in (8, 9, 11, 14, 17, 20):
        d_in = max(0, min(r, 8) - 7)
        d_out = max(0, r - 8)
        out["R%02d" % r] = round(math.sqrt(smod ** 2 + (sb * d_in) ** 2 + (math.log(F) * d_out) ** 2), 2)
    print(f"  {name}: {out}")
print("  slope-only part sigma_b x distance, as in the constructive review: 0.097 x 7 = %.2f, 0.097 x 10 = %.2f" % (0.097 * 7, 0.097 * 10))
print("  v1 thinning slope for scale: 0.36 per rung; ln 1.5 = %.3f, ln 2 = %.3f" % (math.log(1.5), math.log(2)))

# ---- [13] other checks -------------------------------------------------------------------------------------------------------------------
print("\n[13] other checks")
r07 = 35 / 48000.0
for n in (4000, 12000, 24000):
    c = r07 * 4 * n
    print(f"  R07 direct counts for {n} events x 4 roads (v1 rate): {c:.0f}, sigma_ln = {1 / math.sqrt(c):.2f}")


def binom_tail(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


print(f"  V4-5: P(>= 48 of 50 | true agreement 0.85) = {binom_tail(50, 48, 0.85):.4f}; | 0.90: {binom_tail(50, 48, 0.90):.3f}; | 0.98: {binom_tail(50, 48, 0.98):.3f}")
print(f"  B*-off paired: N for 5 sigma from 2.1 sigma at N = 171: {171 * (5 / 2.1) ** 2:.0f}")
for n in (1000, 2000):
    print(f"  S1 with {n} rows on the evaluation half (v1 placeholder efficiencies): relative binomial error "
          + ", ".join(f"eps {e}: {math.sqrt(e * (1 - e) / n) / e:.3f}" for e in (0.03, 0.045, 0.2)))
print(f"  v1 best point: eps 0.045 on 200 rows: {math.sqrt(0.045 * 0.955 / 200) / 0.045:.2f}")
print(f"  checks: 0.3/2.71 = {0.3 / 2.71:.4f}; log10(1.2346e6/0.11) = {math.log10(1.2346e6 / 0.11):.2f}")
print(f"  N_exp(E200) = 219.2 fb x 0.04764 x 3000 fb^-1 x 0.5035 = {219.2 * 0.04764 * 3000 * 0.5035:.0f}; x 9/200 = {15775 * 9 / 200:.0f}; 1.2458e7 / 15775 = {1.2458e7 / 15775:.1f}")
print(f"  sideband example: 1.14 x 0.05 x exp(1.105) = {1.14 * 0.05 * math.exp(1.105):.3f}")
print(f"  injection test: standard error of the mean of mu_hat over 200 pseudo-experiments = {1 / math.sqrt(200):.3f} sd(mu_hat)")
print(f"  coverage test: binomial error at 95 % on 500 pseudo-experiments = {math.sqrt(0.05 * 0.95 / 500):.4f}")
b0 = 22.0 / 3.0
for mq, lam_kev in ((200.0, 1.0), (200.0, 0.45), (1500.0, 5.0)):
    a = 2 * math.pi / (b0 * math.log(mq / (lam_kev * 1e-6)))
    print(f"  one-loop alpha_IC(m = {mq:g} GeV, Lambda = {lam_kev} keV), b0 = 22/3: {a:.4f}; C_F alpha (pi/(2 beta) - 4/pi) at beta 0.7/0.5/0.3: "
          + "/".join(f"{0.75 * a * (math.pi / (2 * b) - 4 / math.pi):+.3f}" for b in (0.7, 0.5, 0.3)))
print(f"  B5 hard-scatter share of candidates in SM + PU samples: R04 {19.52 / (19.52 + 171.55):.3f}, R05 {4.51 / (4.51 + 49.72):.3f}, R06 {0.0162 / (0.0162 + 0.2470):.3f};"
      f" DP1 R07 counts per process: {10500 * r07:.1f} (full: {38000 * r07:.1f})")
print(f"  B6 pooled error on eps_var/eps_nom, unpaired, eps = 0.2: 1200 rows {math.sqrt(2 * 0.8 / (0.2 * 1200)):.3f}, 3000 rows {math.sqrt(2 * 0.8 / (0.2 * 3000)):.3f}")
print(f"  pile-up vertices per crossing, upper estimate: 200 x 100 particles x 0.053 = {200 * 100 * 0.053:.0f}; Geant4 per PU event 200 x 100 x 0.134 ms = {200 * 100 * 0.134e-3:.1f} s")
for n2 in (200, 400, 1000):
    def mde(eps, s1):
        return 2 * math.sqrt(s1 ** 2 + (1 - eps) / (eps * n2))
    print(f"  C1 signal, {n2} v2 rows against 200 v1 rows: detectable shift (2 sigma) at R04 (eps 0.205, v1 14 %): {mde(0.205, 0.14):.2f};"
          f" at FB2 (eps 0.045, v1 33 %): {mde(0.045, 0.33):.2f}")
print(f"  pile-up no-credit value beyond the last direct count: N_trig x 1.14 / 96,000 trials = {NTRIG * U68 / 96000:.0f} events (mean {NTRIG / 96000:.0f})")
print(f"  S1 chain share that could be cut by 500 rows at the 15 points below 1 keV: {15 * 1500 * SIG / H:.0f} CPU-h (listed, not proposed)")
print(f"  toy parametrisation lever: pass 2 on an 11-value f_T grid for 3 selections = {3 * 11 * 8 * TOYS1000 / H:.0f} CPU-h instead of {3 * 40 * 8 * TOYS1000 / H:.0f}")
print(f"  paired B6 at six points, 300 rows: signal {6 * 300 * 6 * SIG / H:.0f} CPU-h (reduced unpaired at four points: {4 * 300 * 6 * SIG / H:.0f})")
print(f"  chi2 = 9.2 on 4 dof: p = exp(-x/2)(1 + x/2) = {math.exp(-4.6) * 5.6:.3f}")
print(f"  GA-1: 1 sigma binomial error of a v2 count on 400 rows (v1 placeholders): R07 (eps 0.09) {math.sqrt(0.91 / (0.09 * 400)):.2f}; fallback (eps 0.045) {math.sqrt(0.955 / (0.045 * 400)):.2f}")
print(f"  GA-4: minimum count for F = 1.25 at s_P = 0: {math.ceil(9 / math.log(1.25) ** 2)}; pile-up width at R14 with independent steps: {math.sqrt(0.2 ** 2 + 0.029 ** 2 + 6 * math.log(1.5) ** 2):.2f}")
print(f"  GA-6: re-digitisation of 24,000 direct + 80,000 signal events at the chain cost: {104000 * CHAIN / H:.0f} CPU-h")
print(f"  GA-7: paired B6 at six points: signal +{2 * 300 * 6 * SIG / H:.0f}, partners +{2 * 300 * SIG / H:.0f}, Stage-3 material for two more points at 3 to 5 keV +{2 * 2 * 300 * s3_at[3] / H:.0f} to +{2 * 2 * 300 * s3_at[5] / H:.0f} CPU-h")
print(f"  GA-8: levers (i) + (iii): {C_POOL - 315.3 + 6000 * 7 * TRIAL / H:.0f} CPU-h = {(C_POOL - 315.3 + 6000 * 7 * TRIAL / H) / CAP_PROD:.1f} days")
