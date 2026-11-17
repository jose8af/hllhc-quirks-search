"""run_c1b.py -- COM C1-b: v2 arithmetic (v2arith.core) applied to v1's RECORDED counts and factors.

Inputs (v1, read-only): TT/data/acts_stage4/analysis/C12FC_v1/background.json (per-term factor chains N/M, end-state
PU factors, rates, sigma, K) and bsum_wp.json (v1's resulting terms and B84 per rung and category).
For every rung R01-R14 of category SR-G, and the non-PU terms of SR-T, the v2 code recomputes each term from the
recorded inputs (never from v1's recorded term values) and compares:
  central values: relative difference <= 1e-6 (criterion as frozen, STR §4.1 point 3);
  B84 (Monte-Carlo sum; own RNG, 4,000,000 draws: v1 used 100,000, whose own MC error is ≈ 1 % (sd over 20 seeds at 100k: 0.95 % at R04, 1.0 % at R14)): within 1 % of v1's B84 (v1 used 100,000 draws).
SR-T PU terms (PC-19 time-tag factors from srt.json) and the F1 / fallback rungs (h, o factorisation) are not in this
first version: reported as NOT EVALUATED with the reason (they enter the T1 inputs only at the fallback point).
Also: the v1 limits.json background per category at the best point against the fallback rung entries of bsum_wp
(the input channel (iii)'s T1 builder reads), so the two input schemas can be compared.
Run (TT env or any numpy python; light):  python -m v2arith.run_c1b   (from phase2_exploration/src)
Output: phase2_exploration/outputs/c1b_arith.json
"""
import json
import logging
import math
from pathlib import Path

from v2arith.core import Factor, Term, b84, chain, cprime_value, pu_value, sm_value

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "outputs" / "c1b_arith.json"
AN1 = Path("/home/users/jdochoa/hllhc-quirks-search/stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1")
SIGMA_NORM = math.log(1.3)         # v1 run_all.DEFAULTS sigma_norm (normalisation width on every term)
log = logging.getLogger("c1b")


def factors_of(row):
    return [Factor(N=f.get("N"), M=f.get("M"), value=f.get("value"), s_ln=f.get("s_ln")) for f in row["factors"]]


def terms_for(bg, n_trig, col_name):
    out = {}
    es = next(e for e in bg["end_state"] if e["column"] == col_name)
    comps = dict(es["sigma_ln_components"])
    out[f"PU {col_name}"] = Term(f"PU {col_name}", pu_value(n_trig, es["base"], es["closure_factor"],
                                                         es["trend_factor"], es.get("T3_factor", 1.0)), comps)
    for p, v in bg["sm"].items():
        if p.startswith("_"):
            continue
        row = next(r for r in v["rows"] if r["column"] == col_name)
        if v.get("proxy"):
            val = v["N_trig"] * row["P_per_presel_event"] if row.get("P_per_presel_event") is not None else None
            out[f"SM {p} [PROXY]"] = Term(f"SM {p} [PROXY]", val, dict(stat=row["s_ln"], normalisation=SIGMA_NORM))
        else:
            P, s, _, _ = chain(factors_of(row))
            out[f"SM {p}"] = Term(f"SM {p}", sm_value(P, v["sigma_pb"], v["K"]), dict(stat=s, normalisation=SIGMA_NORM))
    for t, v in bg["cprime"].items():
        row = next(r for r in v["rows"] if r["column"] == col_name)
        P, s, _, _ = chain(factors_of(row))
        rate = v["rate"]
        out[f"C' {t}"] = Term(f"C' {t}", cprime_value(P, n_trig, rate["value"], rate.get("pv_line_factor", 1.0)),
                              dict(stat=s, normalisation=SIGMA_NORM, rate=rate.get("sigma_ln", 0.0)))
    return out


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    bg = json.loads((AN1 / "background.json").read_text())
    bs = json.loads((AN1 / "bsum_wp.json").read_text())
    n_trig = bs["n_trig"]["value"]
    res = dict(rungs={}, worst_rel_value=0.0, worst_rel_s_ln=0.0, worst_rel_b84=0.0, not_evaluated=[])
    for cat in ("G", "T"):
        for ent in bs["ladder"][cat][:14]:
            col = ent["name"]
            mine = terms_for(bg, n_trig, col)
            cmp_terms, use = [], []
            complete = True
            for t in ent["terms"]:
                m = mine.get(t["label"])
                if m is None:
                    complete = False
                    res["not_evaluated"].append(f"{cat} {col}: {t['label']} (SR-T time-tag factors; srt.json not in v2arith v1)")
                    continue
                rv = abs(m.value / t["value"] - 1) if t["value"] else abs(m.value or 0.0)
                rs = max((abs(m.comps.get(k, 0.0) - s) / s if s else abs(m.comps.get(k, 0.0)))
                         for k, s in t["comps"].items()) if t["comps"] else 0.0
                res["worst_rel_value"] = max(res["worst_rel_value"], rv)
                res["worst_rel_s_ln"] = max(res["worst_rel_s_ln"], rs)
                cmp_terms.append(dict(label=t["label"], v1=t["value"], v2=m.value, rel=rv, rel_s_ln=rs))
                use.append(m)
            entry = dict(terms=cmp_terms, complete=complete)
            if complete and ent.get("B84"):
                q, med, mean = b84(use, nmc=4_000_000, seed=20261116)
                rb = abs(q / ent["B84"] - 1)
                res["worst_rel_b84"] = max(res["worst_rel_b84"], rb)
                entry.update(B84_v1=ent["B84"], B84_v2=q, rel_b84=rb, B_median_v1=ent.get("B_median"), B_median_v2=med)
            res["rungs"][f"{cat}|{col}"] = entry
    res["pass_values"] = bool(res["worst_rel_value"] <= 1e-6)
    res["pass_b84"] = bool(res["worst_rel_b84"] <= 0.01)
    lim = json.loads((AN1 / "limits.json").read_text())
    res["limits_json_best_point"] = {k: lim["points"]["A2|F|200|1.5|BM"].get(k) for k in ("b", "sigma_ln", "s")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.part")
    tmp.write_text(json.dumps(res, indent=1, default=str) + "\n")
    tmp.replace(OUT)
    log.info("C1-b: worst rel value %.3g (pass %s), worst rel s_ln %.3g, worst rel B84 %.3g (pass %s), %d not evaluated",
             res["worst_rel_value"], res["pass_values"], res["worst_rel_s_ln"], res["worst_rel_b84"], res["pass_b84"],
             len(res["not_evaluated"]))


if __name__ == "__main__":
    main()
