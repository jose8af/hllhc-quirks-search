"""Fix R4 (Stage-4 plan), review R4 B-1 and the deadline: arithmetic only, no simulation, no acts env.

Campaigns as fix R3 (probes/f3r_campaigns.py; same per-event inputs, imported) with C' (topology guns and toys) moved INTO
C1 as production (review R4 B-1):
  C'0  no-PU part: gamma, K0S/Lambda, PV-pair, looper guns 1e5 each; NI toy 3 r_NI x 3e4; DIF toy 5e4  -> 12 CPU-h flat
       (plan §4.2 / review R3 S-cap; Fatras on <= 6 particles + finder on <= 50 hits, no t1 dependence beyond noise);
  C'PU with-PU part: 8 topologies (gamma, V0, PV pair, looper, NI 22 / 30 / 61.5 mm, DIF) x 500 events, each a
       PU-200 event + the gun/toy particles, 1 road (aimed into it): 4 000 x (4.7 + t1) s.
Mac only (user decision 2026-10-13: cloud dropped): 7 workers -> 168 CPU-h per 24 h wall.
Deadline (user, 2026-10-13): everything done by Sat 2026-10-17 night. Production window assumed Wed 14 13:00 -> Fri 16
12:00 = 47 h wall (plan §11 schedule), i.e. ~329 CPU-h with no rerun margin.
Output: data/acts_stage4/fix_r4/f4r_deadline.json
"""

import json
from pathlib import Path

TT = Path(__file__).resolve().parents[3]
OUT = TT / "data/acts_stage4/fix_r4"
OUT.mkdir(parents=True, exist_ok=True)
# f3r writes its own outputs on import; load only the blocks() function by exec of its source up to the helpers
src = Path(__file__).with_name("f3r_campaigns.py").read_text().split("def mac_cloud_wall")[0]
ns = {"__file__": str(Path(__file__).with_name("f3r_campaigns.py"))}
exec(compile(src, "f3r_campaigns.py(blocks)", "exec"), ns)
PU, MAC_W, DAY = ns["PU"], ns["MAC_W"], ns["DAY"]
H = 1 / 3600
CAP = MAC_W * DAY                       # 168 CPU-h per Mac day
CP0 = 12.0                              # C' no-PU part, CPU-h
N_CPU_PER_TOPO, N_TOPO = 500, 8         # C' with-PU part


def blocks(c, t1, t2):
    bl = dict(ns["blocks"](c, t1, t2))
    if c == "C1":
        bl["Cp_noPU"] = CP0
        bl["Cp_PU"] = N_TOPO * N_CPU_PER_TOPO * (PU + t1) * H
    return bl


def cpu(c, t1, t2=None, drop=()):
    t2 = 8 * t1 if t2 is None else t2
    return sum(v for k, v in blocks(c, t1, t2).items() if k not in drop)


def c1_reduced(t1, t2=None):
    """Pre-defined reduced C1 (fallback only if C1 cannot run as <= 2 one-day sub-runs before the deadline)."""
    t2 = 8 * t1 if t2 is None else t2
    return {"A1": 2.0, "A2core_100ev": (1000 * PU + 4000 * (0.1 + t1)) * H, "A5core_3pts": 5.0 + 600 * t1 * H,
            "B1_2500": 2500 * (PU + 4 * t1) * H, "B2_500": 500 * (2 * PU + 2 * t2) * H,
            "C_3x1000": 3000 * (PU + t1) * H, "Cp_noPU": CP0, "Cp_PU_250": N_TOPO * 250 * (PU + t1) * H, "val": 10.0}


def root(fn, lo=0.1, hi=200.0):
    """Largest t with fn(t) <= 0 (fn increasing)."""
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fn(mid) <= 0 else (lo, mid)
    return round(lo, 2)


res = {"inputs": {"pu_event_s": PU, "mac_cpu_h_per_day": CAP, "Cprime_noPU_cpu_h": CP0,
                  "Cprime_PU_events": N_TOPO * N_CPU_PER_TOPO, "t2_convention": "t2 = 8 t1 until G2b",
                  "production_window_h": 47, "production_window_cpu_h": round(47 * MAC_W, 1)},
       "Cprime_cost_vs_t1": {}, "campaigns": {}, "t1_max_one_mac_day": {}, "deadline_sets": {}, "g2b_t2max_C1": {}}
T1S = [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20]
for t1 in T1S:
    res["Cprime_cost_vs_t1"][t1] = {"noPU": CP0, "withPU_4000ev": round(4000 * (PU + t1) * H, 1),
                                    "total": round(CP0 + 4000 * (PU + t1) * H, 1),
                                    "R4_quote_1e4_withPU": round(1e4 * (PU + t1) * H, 1),
                                    "R4_quote_1e5_withPU": round(1e5 * (PU + t1) * H, 1)}
    row = {}
    for c in ["C1", "C2", "C3", "C4", "C5"]:
        v = cpu(c, t1)
        row[c] = {"cpu_h": round(v, 1), "wall_h": round(v / MAC_W, 1), "fits_1day": v <= CAP}
    v4p = cpu("C4", t1, drop=("A3", "A4"))
    row["C4prime(no A3,A4)"] = {"cpu_h": round(v4p, 1), "wall_h": round(v4p / MAC_W, 1), "fits_1day": v4p <= CAP}
    row["A3+A4"] = round(cpu("C4", t1) - v4p, 1)
    row["C1-C4"] = round(sum(cpu(c, t1) for c in ["C1", "C2", "C3", "C4"]), 1)
    r1 = sum(c1_reduced(t1).values())
    row["C1_reduced"] = {"cpu_h": round(r1, 1), "wall_h": round(r1 / MAC_W, 1)}
    res["campaigns"][t1] = row
for c in ["C1", "C2", "C3", "C4", "C5"]:
    res["t1_max_one_mac_day"][c] = root(lambda t: cpu(c, t) - CAP)
res["t1_max_one_mac_day"]["C4prime"] = root(lambda t: cpu("C4", t, drop=("A3", "A4")) - CAP)
res["t1_max_one_mac_day"]["C1_reduced"] = root(lambda t: sum(c1_reduced(t).values()) - CAP)
# C1 split into two pre-defined sub-runs: C1a = signal + C' (A1, A2core, A5core, Cp, val/2), C1b = B1, B2, C (+val/2)
sig = ("A1", "A2core", "A5core", "Cp_noPU", "Cp_PU")


def c1a(t):
    return sum(v for k, v in blocks("C1", t, 8 * t).items() if k in sig) + 7.5


def c1b(t):
    return sum(v for k, v in blocks("C1", t, 8 * t).items() if k not in sig and k != "val") + 7.5


res["t1_max_one_mac_day"]["C1a(signal+Cprime)"] = root(lambda t: c1a(t) - CAP)
res["t1_max_one_mac_day"]["C1b(B1,B2,C)"] = root(lambda t: c1b(t) - CAP)
res["t1_max_C1_within_window"] = root(lambda t: cpu("C1", t) - 47 * MAC_W)
res["t1_max_C1reduced_within_window"] = root(lambda t: sum(c1_reduced(t).values()) - 47 * MAC_W)

# deadline sets (wall days on the Mac); window 47 h = 1.96 d
for t1 in (2, 3, 5):
    c = {k: cpu(k, t1) for k in ["C1", "C2", "C3", "C4"]}
    c4p = cpu("C4", t1, drop=("A3", "A4"))
    sets = {"C1+C2+C4+C3": c["C1"] + c["C2"] + c["C4"] + c["C3"], "C1+C2+C4": c["C1"] + c["C2"] + c["C4"],
            "C1+C2+C4prime": c["C1"] + c["C2"] + c4p, "C1+C2": c["C1"] + c["C2"], "C1+C4prime": c["C1"] + c4p,
            "C1": c["C1"]}
    res["deadline_sets"][t1] = {k: {"cpu_h": round(v, 1), "wall_h": round(v / MAC_W, 1),
                                    "fits_47h": v / MAC_W <= 47} for k, v in sets.items()}
# G2b: largest t2 with C1 (incl. C') <= 1 Mac day, and with the chosen set inside the window
for t1 in (2, 3, 4, 5, 6):
    res["g2b_t2max_C1"][t1] = root(lambda t2: cpu("C1", t1, t2) - CAP, 0.1, 5000)
res["dev_and_gates_cpu_h"] = {t1: {"G1": 2, "G2(A1,V4-3,V4-5,G2b)": 6,
                                   "G3_pilot": round((2000 * (PU + 4 * t1) + 500 * (2 * PU + 16 * t1)) * H, 1)}
                              for t1 in (2, 3, 5)}
for t1, d in res["dev_and_gates_cpu_h"].items():
    d["total"] = round(sum(d.values()), 1)
    d["wall_h"] = round(d["total"] / MAC_W, 1)

# G2b t2,max for the decision-table rows (every campaign <= 1 Mac day AND the set inside the 47 h window),
# including the rows trimmed in the deferral order (A3, A4, then C3)
ROWS = {"t1=2 full C1-C4": (2, [("C1", ()), ("C2", ()), ("C4", ()), ("C3", ())]),
        "t1=2 without A3,A4": (2, [("C1", ()), ("C2", ()), ("C4", ("A3", "A4")), ("C3", ())]),
        "t1=2 without A3,A4,C3": (2, [("C1", ()), ("C2", ()), ("C4", ("A3", "A4"))]),
        "t1=3 C1+C2+C4prime": (3, [("C1", ()), ("C2", ()), ("C4", ("A3", "A4"))]),
        "t1=5 C1+C2": (5, [("C1", ()), ("C2", ())])}
res["g2b_t2max_rows"] = {}
for name, (t1, cs) in ROWS.items():
    def worst(t2, t1=t1, cs=cs):
        per = max(cpu(c, t1, t2, d) - CAP for c, d in cs)
        win = sum(cpu(c, t1, t2, d) for c, d in cs) - 47 * MAC_W
        return max(per, win)
    res["g2b_t2max_rows"][name] = root(worst, 0.1, 5000)
# C2 split for 5 < t1 <= 7: C2-B = the B1/B2 (PU-reach) part of C2
res["C2B_reach_part"] = {t1: {"cpu_h": round(cpu("C2", t1, drop=("C",)), 1),
                              "wall_h": round(cpu("C2", t1, drop=("C",)) / MAC_W, 1),
                              "C1+C2B_wall_h": round((cpu("C1", t1) + cpu("C2", t1, drop=("C",))) / MAC_W, 1)}
                         for t1 in (5, 6, 7)}
(OUT / "f4r_deadline.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: res[k] for k in ["t1_max_one_mac_day", "t1_max_C1_within_window", "t1_max_C1reduced_within_window",
                                      "g2b_t2max_C1", "dev_and_gates_cpu_h", "g2b_t2max_rows", "C2B_reach_part"]}, indent=0))
for t1 in (2, 3, 5):
    print(t1, {k: (v["cpu_h"], v["wall_h"]) for k, v in res["deadline_sets"][t1].items()})
for t1 in T1S:
    r = res["campaigns"][t1]
    print(t1, {k: (v["cpu_h"], v["wall_h"]) if isinstance(v, dict) else v for k, v in r.items()},
          res["Cprime_cost_vs_t1"][t1])
