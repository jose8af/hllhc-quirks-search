"""run_c1b.py -- COM C1-b: v2 arithmetic (v2arith.core) applied to v1's RECORDED counts and factors, full ladder.

Inputs (v1, read-only, TT/data/acts_stage4/analysis/C12FC_v1): background.json (per-term N/M factor chains,
end_state and end_state_T PU factors, f1_factors, closure trend, rates, sigma, K), srt.json (time-tag factors per
column) and bsum_wp.json (v1's resulting terms and B84 per rung, category and fallback selection).
Every term of SR-T and SR-G at the 23 ladder rungs and at the 20 fallback selections FB_k[e] & h>5 & o>5 is recomputed
from the recorded inputs (never from v1's recorded term values) and compared:
  central values: relative difference <= 1e-6 (criterion as frozen, STR §4.1 point 3);
  B84: Monte-Carlo sum with 4,000,000 draws (own RNG) within 1 % of v1's B84.  Power: v1 computed its B84 with
  100,000 draws, whose own Monte-Carlo spread is about 1 % (sd over 20 seeds at 1e5 draws: 0.95 % at R04, 1.0 % at R14).
Composition (transcribed from v1 wp.assemble; rung r <= 14: in-job column r - 1; R15-R20: column 13 x p(h/o | R14);
R21-R23: F0e>x columns x p(h>5 & o>5 | F0e>x); FB: FB_k[e] x p(h>5 & o>5 | FB_k[e]); the trend term re-evaluated at
the rung for R15-R20; C' rows take the larger of (with F1, without F1)).
Also: limits.json input of channel (iii)'s T1 builder against the fallback entries of bsum_wp.
Run (any numpy python; light):  python -B -m v2arith.run_c1b   (from phase2_exploration/src)
Output: phase2_exploration/outputs/c1b_arith.json
"""
import json
import logging
import math
from pathlib import Path

from v2arith.core import (Factor, Term, b84, chain, cprime_value, f1_conditional, pu_value, pu_with_f1, sm_value,
                          srt_pu, times_f1, trend_at)

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "outputs" / "c1b_arith.json"
AN1 = Path("/home/users/jdochoa/hllhc-quirks-search/stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1")
SIGMA_NORM = math.log(1.3)         # v1 run_all.DEFAULTS sigma_norm
NMC = 4_000_000
F1_OF_RUNG = {15: ("h>2", 13), 16: ("h>3", 13), 17: ("h>5", 13), 18: ("h>5&o>2", 13), 19: ("h>5&o>3", 13),
              20: ("h>5&o>5", 13), 21: ("h>5&o>5", 14), 22: ("h>5&o>5", 15), 23: ("h>5&o>5", 16)}   # v1 wp.F1_OF_RUNG
log = logging.getLogger("c1b")


def factors_of(row):
    return [Factor(N=f.get("N"), M=f.get("M"), value=f.get("value"), s_ln=f.get("s_ln")) for f in row["factors"]]


def build(bg, srt_cols, n_trig, cols, col, f1x, label):
    """-> (terms_T, terms_G) for in-job column index col (with the F1 factor f1x or None)."""
    name = cols[col]
    tG, tT = [], []
    esA = bg["end_state"][col]; esT = bg["end_state_T"][col]
    if esA.get("P_per_trial") is not None:
        P = pu_value(1.0, esA["base"], esA["closure_factor"], esA["trend_factor"], esA.get("T3_factor", 1.0))
        v, c, _ = pu_with_f1(P, esA["sigma_ln_components"], bool(esA.get("zero_branch")), f1x, n_trig)
        tG.append(Term(f"PU {label}", v, c))
        tG[-1].trend_factor = esA.get("trend_factor", 1.0)
    for nm, v, c, tf in srt_pu(esT, esA, f1x, (srt_cols or {}).get(name), n_trig):
        t = Term(f"PU-SRT {label} {nm}", v, c); t.trend_factor = tf
        tT.append(t)
    others = []
    for p, sv in bg["sm"].items():
        if p.startswith("_"):
            continue
        row = sv["rows"][col]
        if sv.get("proxy"):
            if row.get("B") is None:
                continue
            base, st, zb = sv["N_trig"] * row["P_per_presel_event"], row["s_ln"], bool(row["zero_branch"])
            lab = f"SM {p} [PROXY]"
        else:
            P, st, zb, _ = chain(factors_of(row))
            base, lab = sm_value(P, sv["sigma_pb"], sv["K"]), f"SM {p}"
        val, s, _ = times_f1(base, st, zb, f1x)
        others.append(Term(lab, val, dict(stat=s, normalisation=SIGMA_NORM)))
    for t, cv in bg["cprime"].items():
        row = cv["rows"][col]
        if row.get("P_given_t") is None:
            continue
        P, st, zb, _ = chain(factors_of(row))
        rate = cv["rate"]
        base = cprime_value(P, n_trig, rate["value"], 0.22 if t.startswith("ni") else 1.0)
        rA = times_f1(base, st, zb, f1x); rB = (base, st, zb)
        val, s, _ = rB if (rB[0], rB[1]) > (rA[0], rA[1]) else rA
        others.append(Term(f"C' {t}", val, dict(stat=s, normalisation=SIGMA_NORM, rate=rate.get("sigma_ln", 0.0))))
    return tT + others, tG + others


def retrend(terms, trend, x):
    s_new, f_new = trend_at(trend, x)
    for t in terms:
        if t.label.startswith("PU") and "trend" in t.comps:
            t.comps = dict(t.comps, trend=s_new)
            t.value = t.value * f_new / max(getattr(t, "trend_factor", 1.0), 1e-300)
    return terms


def compare(res, key, mine, ent):
    by = {t.label: t for t in mine}
    rows, use, complete = [], [], True
    for t in ent["terms"]:
        m = by.get(t["label"])
        if m is None or t.get("value") is None:
            complete = complete and t.get("value") is None
            if m is None and t.get("value") is not None:
                res["unmatched"].append(f"{key}: {t['label']}")
            continue
        rv = abs(m.value / t["value"] - 1) if t["value"] else abs(m.value)
        rs = max([abs(m.comps.get(k, 0.0) - s) / s if s else abs(m.comps.get(k, 0.0)) for k, s in t["comps"].items()]
                 or [0.0])
        res["worst_rel_value"] = max(res["worst_rel_value"], rv)
        res["worst_rel_s_ln"] = max(res["worst_rel_s_ln"], rs)
        rows.append(dict(label=t["label"], v1=t["value"], v2=m.value, rel=rv, rel_s_ln=rs))
        use.append(m)
    extra = sorted(set(by) - {t["label"] for t in ent["terms"]})
    if extra:
        res["unmatched"].append(f"{key}: v2-only terms {extra}")
    entry = dict(n_terms=len(rows), terms=rows, complete=complete)
    if complete and ent.get("B84"):
        q, med, mean = b84(use, nmc=NMC, seed=20261116)
        rb = abs(q / ent["B84"] - 1)
        res["worst_rel_b84"] = max(res["worst_rel_b84"], rb)
        entry.update(B84_v1=ent["B84"], B84_v2=q, rel_b84=rb, B_median_v1=ent.get("B_median"), B_median_v2=med)
    res["entries"][key] = entry


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    bg = json.loads((AN1 / "background.json").read_text())
    bs = json.loads((AN1 / "bsum_wp.json").read_text())
    srt = json.loads((AN1 / "srt.json").read_text())["columns"]
    n_trig = bs["n_trig"]["value"]
    cols = [e["column"] for e in bg["end_state"]]
    trend = bg["closure"]["trend"]
    f1 = bg["f1_factors"]
    res = dict(nmc=NMC, entries={}, unmatched=[], worst_rel_value=0.0, worst_rel_s_ln=0.0, worst_rel_b84=0.0)
    for r in range(1, 24):
        if r <= 14:
            col, f1x = r - 1, None
        else:
            name, col = F1_OF_RUNG[r]
            f1x = f1_conditional(f1.get(cols[col]), name)
        lab = bs["ladder"]["G"][r - 1]["name"]
        tT, tG = build(bg, srt, n_trig, cols, col, f1x, lab)
        if 15 <= r <= 20:
            tT = retrend(tT, trend, r); tG = retrend(tG, trend, r)
        compare(res, f"T|{lab}", tT, bs["ladder"]["T"][r - 1])
        compare(res, f"G|{lab}", tG, bs["ladder"]["G"][r - 1])
    for col in range(17, 37):
        fbn = cols[col] + "&h>5&o>5"
        f1x = f1_conditional(f1.get(cols[col]), "h>5&o>5")
        tT, tG = build(bg, srt, n_trig, cols, col, f1x, fbn)
        for c, terms in (("T", tT), ("G", tG)):
            compare(res, f"FB|{c}|{fbn}", terms, bs["ladder"]["FB"][fbn][c])
    res["n_entries"] = len(res["entries"])
    res["n_b84_compared"] = sum("rel_b84" in e for e in res["entries"].values())
    res["pass_values"] = bool(res["worst_rel_value"] <= 1e-6 and not res["unmatched"])
    res["pass_b84"] = bool(res["worst_rel_b84"] <= 0.01)
    lim = json.loads((AN1 / "limits.json").read_text())["points"]["A2|F|200|1.5|BM"]
    fb = bs["ladder"]["FB"]["FB2&h>5&o>5"]
    res["T1_input_schema"] = dict(limits_json_b=lim["b"], limits_json_sigma_ln=lim["sigma_ln"],
                                  bsum_median=[fb["T"]["B_median"], fb["G"]["B_median"]],
                                  ln_B84_over_median=[math.log(fb[c]["B84"] / fb[c]["B_median"]) for c in ("T", "G")],
                                  v2_median=[res["entries"][f"FB|{c}|FB2&h>5&o>5"].get("B_median_v2") for c in ("T", "G")],
                                  v2_ln_B84_over_median=[math.log(res["entries"][f"FB|{c}|FB2&h>5&o>5"]["B84_v2"] /
                                                                  res["entries"][f"FB|{c}|FB2&h>5&o>5"]["B_median_v2"])
                                                         for c in ("T", "G")])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.part")
    tmp.write_text(json.dumps(res, indent=1, default=str) + "\n")
    tmp.replace(OUT)
    log.info("C1-b: %d entries (%d with B84), worst rel value %.3g, worst rel s_ln %.3g, worst rel B84 %.3g, "
             "unmatched %d; pass values %s, pass B84 %s", res["n_entries"], res["n_b84_compared"],
             res["worst_rel_value"], res["worst_rel_s_ln"], res["worst_rel_b84"], len(res["unmatched"]),
             res["pass_values"], res["pass_b84"])


if __name__ == "__main__":
    main()
