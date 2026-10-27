"""Fix R3 (Stage-4 plan): arithmetic only, no simulation, no acts env.

(1) Production campaigns C1-C4 (+ optional C5 = rho 3) as a function of the finder time per trial t1 (rho = 1) and
    t2 (rho = 2), with the same per-event inputs as plan §6.2 / f2r_cost.py: non-finder PU event 4.7 s; row-major extra
    (row, Lambda) 0.1 s + t1; B1 event 4.7 + 4 t1; B2 event 2 x 4.7 + 2 t2; SM event 4.7 + t1 (1 road);
    rho = 3 event 3 x 4.7 + t3 (1 road), t3 = (3/2)^3 t2.
    Capacity per 24 h wall (user decision 2026-10-13): Mac 7 workers -> 168 Mac-M3 CPU-h (user range 170-200);
    cloud free-trial VM 8 vCPU x s_c Mac-M3-core equivalents, s_c = 0.6 ESTIMATE (0.4-0.8), unmeasured.
    Mac + cloud wall = best whole-block partition, max(Mac CPU-h / 7, cloud CPU-h / (8 s_c)).
(2) Budget split: combined 84th percentile of two log-normal category backgrounds vs per-category B84, sigma_ln and
    correlation; per-category value that keeps the combined B84 <= 0.3.
(3) PU-extrapolation reach per campaign; cloud budget burn (prices UNVERIFIED, to be read from the GCP pricing page
    before anything is created).
Output: data/acts_stage4/fix_r3/f3r_campaigns.json, f3r_split.json.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
OUT = TT / "data/acts_stage4/fix_r3"
OUT.mkdir(parents=True, exist_ok=True)

PU = 4.7          # s, PU event without finder (plan §6.2)
MAC_W = 7         # workers (Stage-3 throughput ~ 7 M3-CPU-s per wall-s)
CLOUD_VCPU = 8    # free-trial limit as reported by the user (UNVERIFIED)
S_C = 0.6         # Mac-M3-core equivalents per cloud vCPU (ESTIMATE, unmeasured)
DAY = 24.0


def blocks(c, t1, t2):
    """CPU-h per block of campaign c (dict). Event counts are the pre-defined campaign contents (plan §6.2)."""
    h = 1 / 3600
    if c == "C1":   # core, self-contained (= review-R3 S-cap without the k = 1 guns, which are C' = development)
        return {"A1": 2.0,
                "A2core": (1000 * PU + 8000 * (0.1 + t1)) * h,     # 5 species-masses x 8 Lambda x 200, 1000 rows
                "A5core": 8.0 + 1000 * t1 * h,                     # 5 points, full chain
                "B1": 5000 * (PU + 4 * t1) * h,                    # 5000 events x 4 roads
                "B2": 1000 * (2 * PU + 2 * t2) * h,                # 1000 rho = 2 events x 2 roads
                "C": 6000 * (PU + t1) * h,                         # Z(nunu)+j, W(taunu)+j, ttbar 1l x 2000
                "val": 15.0}
    if c == "C2":   # backgrounds I
        return {"B1": 7000 * (PU + 4 * t1) * h,                    # -> 12 000
                "B2": 2000 * (2 * PU + 2 * t2) * h,                # -> 3 000
                "C": 19000 * (PU + t1) * h,                        # W(enu), W(munu) 5000 each; +3000 x 3 -> 5 x 5000
                "val": 5.0}
    if c == "C3":   # backgrounds II
        return {"B1": 8000 * (PU + 4 * t1) * h,                    # -> 20 000 (8 x 10^4 trials)
                "B2": 2000 * (2 * PU + 2 * t2) * h,                # -> 5 000 (10^4 trials)
                "val": 5.0}
    if c == "C4":   # signal grid completion + toys + material + systematics
        return {"A2rest": (2400 * PU + 53344 * (0.1 + t1)) * h,
                "A3": (1400 * PU + 9000 * (0.1 + t1)) * h,
                "A4": (2000 * PU + 12000 * (0.1 + t1)) * h,
                "A5rest": 22.0 + 3000 * t1 * h,                    # 15 points + PU 140 rerun
                "val": 5.0}
    if c == "C5":   # optional rho = 3, behind G2c
        t3 = 3.375 * t2
        return {"B2rho3": 2000 * (3 * PU + t3) * h}
    raise KeyError(c)


def mac_cloud_wall(bl, s_c=S_C):
    """Best whole-block partition between the Mac and the cloud VM; returns (wall_h, cloud_blocks)."""
    names = list(bl)
    cloud_rate = CLOUD_VCPU * s_c
    best = (float("inf"), ())
    for r in range(len(names) + 1):
        for sub in itertools.combinations(names, r):
            cl = sum(bl[n] for n in sub)
            mac = sum(bl[n] for n in names if n not in sub)
            w = max(mac / MAC_W, cl / cloud_rate)
            if w < best[0]:
                best = (w, sub)
    return best


T1S = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
res = {"inputs": {"pu_event_s": PU, "mac_workers": MAC_W, "mac_cap_cpu_h_per_day": MAC_W * DAY,
                  "cloud_vcpu": CLOUD_VCPU, "cloud_s_c_estimate": S_C,
                  "cloud_cpu_h_per_day": CLOUD_VCPU * S_C * DAY,
                  "t2_convention": "t2 = 8 t1 (finder ~ rho^3) until G2b measures t2"},
       "campaigns": {}}
for c in ["C1", "C2", "C3", "C4", "C5"]:
    rows = []
    for t1 in T1S:
        t2 = 8 * t1
        bl = blocks(c, t1, t2)
        tot = sum(bl.values())
        w_mc, cl = mac_cloud_wall(bl)
        w_lo, _ = mac_cloud_wall(bl, 0.4)
        w_hi, _ = mac_cloud_wall(bl, 0.8)
        rows.append({"t1": t1, "t2": t2, "cpu_h": round(tot, 1),
                     "blocks": {k: round(v, 1) for k, v in bl.items()},
                     "wall_mac_h": round(tot / MAC_W, 1),
                     "wall_mac_cloud_h": round(w_mc, 1),
                     "wall_mac_cloud_h_sc0.4_0.8": [round(w_lo, 1), round(w_hi, 1)],
                     "cloud_blocks": list(cl),
                     "fits_mac_1day": tot / MAC_W <= DAY,
                     "fits_mac_cloud_1day": w_mc <= DAY})
    # largest t1 (0.1 s grid, t2 = 8 t1) that fits one day
    def tmax(fn):
        t = 0.1
        last = None
        while t < 60:
            if fn(t):
                last = t
            else:
                break
            t = round(t + 0.1, 1)
        return last
    res["campaigns"][c] = {
        "rows": rows,
        "t1_max_mac_1day": tmax(lambda t: sum(blocks(c, t, 8 * t).values()) / MAC_W <= DAY),
        "t1_max_mac_cloud_1day": tmax(lambda t: mac_cloud_wall(blocks(c, t, 8 * t))[0] <= DAY),
    }

# full scope (C1-C4) totals and number of 1-day runs if each campaign is split along pre-defined halves
full = []
for t1 in T1S:
    t2 = 8 * t1
    tot = sum(sum(blocks(c, t1, t2).values()) for c in ["C1", "C2", "C3", "C4"])
    n_mac = sum(math.ceil(sum(blocks(c, t1, t2).values()) / MAC_W / DAY) for c in ["C1", "C2", "C3", "C4"])
    n_mc = sum(math.ceil(mac_cloud_wall(blocks(c, t1, t2))[0] / DAY) for c in ["C1", "C2", "C3", "C4"])
    full.append({"t1": t1, "t2": t2, "cpu_h_C1_C4": round(tot), "n_1day_runs_mac": n_mac,
                 "n_1day_runs_mac_cloud": n_mc})
res["full_scope_C1_C4"] = full

# G2b: largest t2 at which C1 still fits one day, for given t1 (Mac only and Mac + cloud)
g2b = []
for t1 in [2, 4, 5, 6, 8]:
    def fit(t2, cloud):
        bl = blocks("C1", t1, t2)
        return (mac_cloud_wall(bl)[0] if cloud else sum(bl.values()) / MAC_W) <= DAY
    out = {"t1": t1}
    for cloud in (False, True):
        t2 = 0.0
        while fit(t2 + 1, cloud) and t2 < 2000:
            t2 += 1
        out["t2_max_C1_" + ("mac_cloud" if cloud else "mac")] = t2 if fit(t2, cloud) else None
    g2b.append(out)
res["g2b_t2_max_C1"] = g2b

# PU-extrapolation reach (plan §4.1 step 2 convention: one candidate with k_min = 20 at rho = 2 has w = 2^-20)
w20 = 2.0 ** -20
reach = {}
for name, n_b1, n_b2 in [("C1", 5000, 1000), ("C1+C2", 12000, 3000), ("C1+C2+C3", 20000, 5000)]:
    trials2 = 2 * n_b2
    trials1 = 4 * n_b1
    reach[name] = {"B2_trials_rho2": trials2, "thinning_reach_per_trial": w20 / trials2,
                   "B1_trials": trials1, "direct_zero_count_95cl_per_trial": 3.0 / trials1}
n_trig = 3.3e7   # plan §2.6 / review R3 §6
for b84c in (0.15, 0.11):
    reach[f"required_P_PU_per_event_B84c_{b84c}"] = b84c / math.exp(2.3) / n_trig
res["reach"] = reach

# cloud budget burn (all prices UNVERIFIED; GCP pricing page to be read before anything is created)
price = {"t2d-standard-8_on_demand_usd_h": 0.34, "e2-standard-8_on_demand_usd_h": 0.27,
         "spot_8vcpu_usd_h_range": [0.07, 0.12], "pd_balanced_usd_gb_month": 0.10,
         "internet_egress_usd_gb": 0.12}
def burn(vm_days, disk_gb=100, disk_days=60, egress_gb=30, rate=price["t2d-standard-8_on_demand_usd_h"]):
    return round(vm_days * 24 * rate + disk_gb * price["pd_balanced_usd_gb_month"] * disk_days / 30
                 + egress_gb * price["internet_egress_usd_gb"], 1)
res["cloud_budget"] = {
    "prices_UNVERIFIED": price,
    "per_campaign_day_on_demand_usd": round(24 * price["t2d-standard-8_on_demand_usd_h"], 1),
    "setup_validation_speed_vm_days": 1.5,
    "egress_gb_per_campaign": {"C1": 3, "C2": 12, "C3": 12, "C4": 2},
    "scenarios_usd": {
        "C1 only (1.5 dev + 1 campaign VM-days, 3 GB out)": burn(2.5, disk_days=30, egress_gb=3),
        "C1-C4 (1.5 dev + 4 campaign VM-days, 29 GB out)": burn(5.5, egress_gb=29),
        "C1-C4 split to 2 days each + C5 (1.5 + 9 VM-days)": burn(10.5, disk_days=90, egress_gb=35),
    },
    "credit_usd": 300, "credit_days": 90}
(OUT / "f3r_campaigns.json").write_text(json.dumps(res, indent=1))

# (2) budget split
rng = np.random.default_rng(20261013)
N = 2_000_000
z1 = rng.standard_normal(N)
z0 = rng.standard_normal(N)
split = {"note": "ratio = q84(B_T + B_G) / q84(B_c) for two log-normals with equal median and sigma_ln",
         "ratio": {}, "combined_B84_each_0p11": {}, "combined_B84_each_0p15": {}, "unequal": {}}
for s in (1.0, 1.5, 2.0, 2.3, 2.5, 3.0):
    for rho in (0.0, 0.5, 1.0):
        z2 = rho * z1 + math.sqrt(1 - rho ** 2) * z0
        tot = np.exp(s * z1) + np.exp(s * z2)
        q = float(np.quantile(tot, 0.841345))
        r = q / math.exp(s)
        key = f"sigma={s},rho={rho}"
        split["ratio"][key] = round(r, 3)
        split["combined_B84_each_0p11"][key] = round(0.11 * r, 3)
        split["combined_B84_each_0p15"][key] = round(0.15 * r, 3)
s = 2.3
for frac in (0.5, 0.2, 0.05):   # second category's median as a fraction of the first, both at most 0.11
    z2 = z0
    tot = 0.11 / math.exp(s) * (np.exp(s * z1) + frac * np.exp(s * z2))
    split["unequal"][f"B84_T=0.11,B84_G={0.11 * frac:.4f},indep"] = round(float(np.quantile(tot, 0.841345)), 3)
split["per_category_for_combined_0p3_indep_sigma2p3"] = round(0.3 / split["ratio"]["sigma=2.3,rho=0.0"], 4)
(OUT / "f3r_split.json").write_text(json.dumps(split, indent=1))
print(json.dumps({k: res[k] for k in ("full_scope_C1_C4", "g2b_t2_max_C1", "reach")}, indent=1))
for c in res["campaigns"]:
    print(c, res["campaigns"][c]["t1_max_mac_1day"], res["campaigns"][c]["t1_max_mac_cloud_1day"])
    for r in res["campaigns"][c]["rows"]:
        print("  ", r["t1"], r["cpu_h"], r["wall_mac_h"], r["wall_mac_cloud_h"], r["wall_mac_cloud_h_sc0.4_0.8"], r["cloud_blocks"])
print(json.dumps(res["cloud_budget"]["scenarios_usd"], indent=1))
print(json.dumps(split, indent=1))
