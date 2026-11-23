"""Reach re-estimate with pilot-based backgrounds (Tora, 2026-11-23). ESTIMATE on v1 placeholder efficiencies.

Runs Gate A's script phase1_strategy/src/strategy_budget.py UNCHANGED (runpy), checks that it reproduces the stdout of
record (budget_stdout_v9.txt), then calls the script's own functions (pmf_pred, s95_pmf, quant_pmf, reach_of, MAPR)
with the background inputs substituted as in outputs/REACH_REEST_PLAN_tora_2026-11-23.md. No signal file is read; the
only signal input is the plan's s95 -> reach table inside the script (v1 placeholder efficiencies).

Usage (from analyses/quirks_v2): python -I phase2_exploration/src/reach_reest_tora.py <out.json> <script_stdout.txt>
"""
import contextlib
import hashlib
import io
import json
import logging
import math
import runpy
import sys
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("reach_reest")

QV2 = "/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2"
SCRIPT = f"{QV2}/phase1_strategy/src/strategy_budget.py"
STDOUT_REF = f"{QV2}/phase1_strategy/outputs/budget_stdout_v9.txt"
OUT_JSON, OUT_STDOUT = sys.argv[1], sys.argv[2]

t0 = time.process_time()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    G = runpy.run_path(SCRIPT, run_name="__main__")
txt = buf.getvalue()
with open(OUT_STDOUT, "w") as f:
    f.write(txt)
ref = open(STDOUT_REF).read()
new_l, ref_l = txt.splitlines(), ref.splitlines()
ndiff = sum(1 for a, b in zip(new_l, ref_l) if a != b) + abs(len(new_l) - len(ref_l))
i0 = ref_l.index(next(x for x in ref_l if x.startswith("[9b]")))
i1 = next(i for i, x in enumerate(ref_l) if "HEADLINE v6 (T1)" in x)
blk_same = new_l[i0:i1 + 1] == ref_l[i0:i1 + 1]
log.info("script stdout: %d lines, %d differ from budget_stdout_v9.txt; [9b] block l.%d-%d identical: %s",
         len(new_l), ndiff, i0 + 1, i1 + 1, blk_same)
if not blk_same:
    raise SystemExit("Gate A [9b] block not reproduced: stop")
t_script = time.process_time() - t0

pmf_pred, s95_pmf, quant_pmf, reach_of = G["pmf_pred"], G["s95_pmf"], G["quant_pmf"], G["reach_of"]
MAPR, rows, SM_NTRIG, MJK = G["MAPR"], G["rows"], G["SM_NTRIG"], G["MJK"]
K_DIF, kz, PU9, ALPHA, F_GAM, W = G["K_DIF"], G["kz"], G["PU9"], G["ALPHA"], G["F_GAM"], G["W_NORM"]
MJ_PLAN = G["MJ_PLAN"]
S95_243 = MAPR[-1][0]

# ---- substituted inputs (cite file:line in the .md) ----
M_PILOT = 993887.0                                     # Tove l.51-52 (measured sum w / w_max), Ingvild l.25
K_PZ = (sum(SM_NTRIG.values()) + MJ_PLAN) / M_PILOT    # Df-11: every SM process + multijets via the Z(nunu) count
RHO_G = {"R05 10/174": 10 / 174, "R06 1/11": 1 / 11}   # Eskil l.42-43
RHO_G_UL = 4.74 / 22                                   # Eskil l.42 (event-level 95 % UL, R05)
RHO_D_UL = 3.0 / 47                                    # Eskil l.39 (event-level 95 % UL, R05)
TAGS = {"x339": "alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)",
        "x201": "alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201)"}
SM_NAMES = set(SM_NTRIG)
assert all(n in [r[0] for r in rows] for n in SM_NAMES), "SM term names"
FLOORS_NONSM = [(r[4], 0) for r in rows if r[0] != "DIF" and r[0] not in SM_NAMES]
FLOORS_SM_POOL = [(r[4], 0) for r in rows if r[0] in SM_NAMES] + [MJK]
log.info("K_PZ = %.3f events per pilot count; K_DIF %.3f; kz %.3f; W %.2f; S95(243) %.1f", K_PZ, K_DIF, kz, W, S95_243)


def rfmt(sv):
    return "< 243" if sv > S95_243 else f"{reach_of(sv):.0f}"


def build(tag, rate, rho_g, rho_d, z, w):
    """gam / lnn lists for one variant. z: 'pool' (Gate A's SM pool floors) or a pilot count m (int)."""
    d0, g0 = ALPHA[(TAGS[tag], False)]
    g = g0 * F_GAM[rate] * rho_g
    d = d0 * rho_d
    # term order as in Gate A (kap_nodif, then DIF, then conversions): the draws of pmf_pred depend on the order
    gam = list(G["kap_nodif"]) if z == "pool" else list(FLOORS_NONSM)
    lnn = [PU9]
    gam.append((K_DIF, d / K_DIF))                 # rho_d = 0 -> (K_DIF, 0): DIF at its pool floor (max(floor, N H))
    if g > 0:                                      # conversion term exactly as Gate A v6 (T1) (ii), strategy_budget l.812
        if w > 0:
            lnn.append((g, math.sqrt(w ** 2 + 1 / (g / kz + 1)), None))
        else:
            gam.append((kz, g / kz))               # w = 0: counted, as v6 (T1) (i), l.806
    if z == "pool":
        pass                                       # Gate A's SM pool floors and multijet floor are in kap_nodif
    elif z == 0 or w == 0:
        gam.append((K_PZ, z))                      # pilot zero-count floor / counted term (Gamma(m + 1))
    else:                                          # counted pilot term with the width of Gate A's Z ceiling row, l.827
        lnn.append((K_PZ * (z + 1), math.sqrt(w ** 2 + 1 / (z + 1)), None))
    return gam, lnn, g, d


def evaluate(label, tag, rate, rho_g, rho_d, z, w=W):
    gam, lnn, g, d = build(tag, rate, rho_g, rho_d, z, w)
    pm, bq = pmf_pred(gam, lnn)
    l50, l84 = [s95_pmf(pm, quant_pmf(pm, f)) for f in (0.5, 0.84)]
    r = dict(label=label, tag=tag, photon_rate=rate, rho_gamma=rho_g, rho_dif=rho_d, z_term=z, w=w,
             conversions=g, dif=d, B16=bq[0], B50=bq[1], B84=bq[2], s95_median=l50, s95_84=l84,
             reach_median=rfmt(l50), reach_84edge=rfmt(l84))
    log.info("%-58s %s %-26s conv %7.0f DIF %5.0f z %-5s w %.2f | B50 %7.0f | s95 %7.1f [84 %% %7.1f] | reach %s [84 %% edge %s]",
             label, tag, rate, g, d, z, w, bq[1], l50, l84, r["reach_median"], r["reach_84edge"])
    return r


R = []
RATES = list(F_GAM)
# 0. Gate A reproduction through the wrapper (must equal stdout l.330, 334, 338, 342)
for tag in TAGS:
    for rate in RATES:
        R.append(evaluate("GateA reproduction (rho = 1, DIF v1, Z pool)", tag, rate, 1.0, 1.0, "pool"))
        ref6 = G["A1P6"][(TAGS[tag], rate, W)]
        R[-1]["gateA_A1P6"] = list(ref6)
        R[-1]["reproduced_exactly"] = (R[-1]["B50"], R[-1]["s95_median"], R[-1]["s95_84"]) == tuple(ref6)
        log.info("  Gate A A1P6 %s -> reproduced exactly: %s", ref6, R[-1]["reproduced_exactly"])
assert abs(sum(k for k, _ in G["kap_nodif"]) - sum(k for k, _ in FLOORS_NONSM + FLOORS_SM_POOL)) < 1e-9
# 1. the three variants
R.append(evaluate("LOW: rho_g 0, DIF floor, Z pool floors", "x339", RATES[0], 0.0, 0.0, "pool"))
for rk, rg in RHO_G.items():
    for rate in RATES:
        R.append(evaluate(f"CENTRAL: rho_g {rk}, DIF floor, Z pilot after-CKF pass 0", "x339", rate, rg, 0.0, 0))
for tag in TAGS:
    for rate in RATES:
        R.append(evaluate("HIGH/UL: rho_g 0.22, rho_DIF 0.064, Z own-hit pass 11", tag, rate, RHO_G_UL, RHO_D_UL, 11))
# 2. one substitution at a time
for rk, rg in RHO_G.items():
    R.append(evaluate(f"conv x rho_g {rk} only (DIF v1, Z pool)", "x201", RATES[0], rg, 1.0, "pool"))
    R.append(evaluate(f"conv-led x rho (DIF floor), Z pool", "x339", RATES[0], rg, 0.0, "pool"))
R.append(evaluate("Z pilot after-CKF 0 only (Gate A conversions)", "x201", RATES[0], 1.0, 1.0, 0))
R.append(evaluate("conv UL only (DIF floor, Z pool)", "x339", RATES[0], RHO_G_UL, 0.0, "pool"))
R.append(evaluate("Z own-hit pass 11 only (rho_g 0, DIF floor)", "x339", RATES[0], 0.0, 0.0, 11))
for rk, rg in RHO_G.items():
    R.append(evaluate(f"CENTRAL with Z after-CKF near-pass 17 (lower bound): rho_g {rk}", "x339", RATES[0], rg, 0.0, 17))
    R.append(evaluate(f"CENTRAL with DIF kept at v1 size: rho_g {rk}", "x201", RATES[0], rg, 1.0, 0))
# 3. statistics-only (w = 0), as Gate A's (i) rows
R.append(evaluate("LOW, w = 0", "x339", RATES[0], 0.0, 0.0, "pool", w=0.0))
for rk, rg in RHO_G.items():
    R.append(evaluate(f"CENTRAL, w = 0: rho_g {rk}", "x339", RATES[0], rg, 0.0, 0, w=0.0))
R.append(evaluate("HIGH/UL, w = 0", "x201", RATES[0], RHO_G_UL, RHO_D_UL, 11, w=0.0))
# 4. information only: the rule-1 ceiling counts read as if they were background (they are not)
for m, lab in ((253, "finder near-pass N"), (1501, "subset pass S")):
    R.append(evaluate(f"INFO ceiling, not an estimate: Z = rule-1 {lab} {m}, rho_g R05", "x339", RATES[0], RHO_G["R05 10/174"], 0.0, m))

out = dict(tag="ESTIMATE on v1 placeholder efficiencies; no v2 signal efficiency; no signal file read",
           script=SCRIPT, script_sha256=hashlib.sha256(open(SCRIPT, "rb").read()).hexdigest(),
           stdout_ref=STDOUT_REF, stdout_lines_differing=ndiff, block_9b_identical=blk_same,
           constants=dict(K_PZ=K_PZ, M_pilot=M_PILOT, K_DIF=K_DIF, kz=kz, W_NORM=W, S95_243=S95_243, PU9=list(PU9),
                          rho_gamma=RHO_G, rho_gamma_UL=RHO_G_UL, rho_dif_UL=RHO_D_UL,
                          MAPR=[list(x) for x in MAPR], alpha1p={k: list(ALPHA[(v, False)]) for k, v in TAGS.items()},
                          F_GAM=F_GAM, floors_nonSM_sum=sum(k for k, _ in FLOORS_NONSM),
                          floors_SM_pool_sum=sum(k for k, _ in FLOORS_SM_POOL)),
           rows=R, cpu_s_script=t_script, cpu_s_total=time.process_time() - t0)
with open(OUT_JSON, "w") as f:
    json.dump(out, f, indent=1)
log.info("done: %d rows, CPU %.0f s (script %.0f s)", len(R), out["cpu_s_total"], t_script)
