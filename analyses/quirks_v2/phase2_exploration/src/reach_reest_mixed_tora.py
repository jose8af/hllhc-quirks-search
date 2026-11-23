"""Reach vs the mixed fraction f surviving into the conversion term (Tora, 2026-11-23; advisor Ulla, LOG 23 Nov 16:39).
ESTIMATE on v1 placeholder efficiencies. Same method as reach_reest_tora.py: Gate A's strategy_budget.py run unchanged
(runpy; stdout checked against budget_stdout_v9.txt), its own functions called with substituted background inputs.
Conversion term = v1 (alpha1') conversions x photon-rate factor x (rho_g + f x mu_mixed), mu_mixed = 105/174 (Eskil l.65-73).
No signal file is read.

Usage (from analyses/quirks_v2): python -I phase2_exploration/src/reach_reest_mixed_tora.py <out.json>
"""
import contextlib
import io
import json
import logging
import math
import runpy
import sys
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("reach_mixed")
QV2 = "/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2"
SCRIPT = f"{QV2}/phase1_strategy/src/strategy_budget.py"
OUT_JSON = sys.argv[1]

t0 = time.process_time()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    G = runpy.run_path(SCRIPT, run_name="__main__")
same = buf.getvalue() == open(f"{QV2}/phase1_strategy/outputs/budget_stdout_v9.txt").read()
log.info("script stdout identical to budget_stdout_v9.txt: %s", same)
if not same:
    raise SystemExit("stdout of record not reproduced: stop")

pmf_pred, s95_pmf, quant_pmf, reach_of = G["pmf_pred"], G["s95_pmf"], G["quant_pmf"], G["reach_of"]
MAPR, rows, SM_NTRIG = G["MAPR"], G["rows"], G["SM_NTRIG"]
K_DIF, kz, PU9, ALPHA, F_GAM, W = G["K_DIF"], G["kz"], G["PU9"], G["ALPHA"], G["F_GAM"], G["W_NORM"]
S95_243 = MAPR[-1][0]
K_PZ = (sum(SM_NTRIG.values()) + G["MJ_PLAN"]) / 993887.0   # Df-11 pilot term, M = 993,887 (Tove l.51-52)
MU_MIX = (51 + 35 + 19) / 174                                # gamma R05, 1 <= j < 4 (Eskil l.65-67, l.73: 60 %)
TAG = "alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339)"
D0, G0 = ALPHA[(TAG, False)]
FLOORS_NONSM = [(r[4], 0) for r in rows if r[0] != "DIF" and r[0] not in SM_NTRIG]
F_GRID = (0.0, 0.1, 0.2, 0.3, 1.0)
RHO = (0.0, 0.074, 0.12, 0.22)
SM_M = (0, 17)


def rfmt(sv):
    return "< 243" if sv > S95_243 else f"{reach_of(sv):.0f}"


def evaluate(f, rho, m, rate):
    g = G0 * F_GAM[rate] * (rho + f * MU_MIX)
    gam = list(FLOORS_NONSM) + [(K_DIF, 0.0)]          # DIF at its pool floor (rho_DIF = 0), as in REACH_REEST
    lnn = [PU9]
    if g > 0:
        lnn.append((g, math.sqrt(W ** 2 + 1 / (g / kz + 1)), None))   # Gate A v6 (T1) (ii) form, l.812
    if m == 0:
        gam.append((K_PZ, 0))
    else:
        lnn.append((K_PZ * (m + 1), math.sqrt(W ** 2 + 1 / (m + 1)), None))   # Gate A Z ceiling row form, l.827
    pm, bq = pmf_pred(gam, lnn)
    l50, l84 = [s95_pmf(pm, quant_pmf(pm, q)) for q in (0.5, 0.84)]
    return dict(f=f, rho_gamma=rho, sm_count=m, photon_rate=rate, conversions=g, B50=bq[1], s95_median=l50,
                s95_84=l84, reach_median=rfmt(l50), reach_84edge=rfmt(l84))


grid, cross = [], []
for rate in F_GAM:
    for m in SM_M:
        for rho in RHO:
            for f in F_GRID:
                r = evaluate(f, rho, m, rate)
                grid.append(r)
                log.info("%-26s SM %2d rho %.3f f %.1f conv %7.0f B50 %7.0f s95 %7.1f [%7.1f] reach %s [%s]", rate, m, rho, f,
                         r["conversions"], r["B50"], r["s95_median"], r["s95_84"], r["reach_median"], r["reach_84edge"])
            # smallest f with median s95 > S95_243 (reach < 243), bisection to 0.005
            lo_r, hi_r = evaluate(0.0, rho, m, rate), evaluate(1.0, rho, m, rate)
            if lo_r["s95_median"] > S95_243:
                fc = "already below at f = 0"
            elif hi_r["s95_median"] <= S95_243:
                fc = "not below up to f = 1"
            else:
                lo, hi = 0.0, 1.0
                while hi - lo > 0.005:
                    mid = 0.5 * (lo + hi)
                    if evaluate(mid, rho, m, rate)["s95_median"] > S95_243:
                        hi = mid
                    else:
                        lo = mid
                fc = round(0.5 * (lo + hi), 3)
            g_c = G0 * F_GAM[rate] * (rho + fc * MU_MIX) if isinstance(fc, float) else None
            cross.append(dict(photon_rate=rate, sm_count=m, rho_gamma=rho, f_cross=fc, conversions_at_cross=g_c))
            log.info("  crossing: %s SM %d rho %.3f -> f = %s (conversions %s)", rate, m, rho, fc, g_c)

json.dump(dict(tag="ESTIMATE on v1 placeholder efficiencies; no v2 signal efficiency; no signal file read",
               stdout_identical=same, mu_mixed=MU_MIX, K_PZ=K_PZ, S95_243=S95_243, v1_conversions=G0, F_GAM=F_GAM,
               grid=grid, crossing=cross, cpu_s=time.process_time() - t0), open(OUT_JSON, "w"), indent=1)
log.info("done, CPU %.0f s", time.process_time() - t0)
