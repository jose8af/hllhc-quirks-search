"""mc_power.py -- C1-b power statement: the Monte-Carlo spread of a 1e5-draw B84 (v1's draws) at every entry, and the
pull of v1's B84 against the 4e6-draw v2 value in units of that spread.  Run from src/: python -B -m v2arith.mc_power"""
import json
import logging

import numpy as np

from v2arith import run_c1b as R
from v2arith.core import b84, f1_conditional

log = logging.getLogger("mc_power")


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    bg = json.loads((R.AN1 / "background.json").read_text()); bs = json.loads((R.AN1 / "bsum_wp.json").read_text())
    srt = json.loads((R.AN1 / "srt.json").read_text())["columns"]
    nt = bs["n_trig"]["value"]; cols = [e["column"] for e in bg["end_state"]]; f1 = bg["f1_factors"]
    res = json.loads(R.OUT.read_text())
    out = {}
    for r in range(1, 24):
        col, f1x = (r - 1, None) if r <= 14 else (R.F1_OF_RUNG[r][1], f1_conditional(f1.get(cols[R.F1_OF_RUNG[r][1]]),
                                                                                      R.F1_OF_RUNG[r][0]))
        lab = bs["ladder"]["G"][r - 1]["name"]
        tT, tG = R.build(bg, srt, nt, cols, col, f1x, lab)
        if 15 <= r <= 20:
            tT = R.retrend(tT, bg["closure"]["trend"], r); tG = R.retrend(tG, bg["closure"]["trend"], r)
        for c, t in (("T", tT), ("G", tG)):
            out[f"{c}|{lab}"] = t
    for col in range(17, 37):
        fbn = cols[col] + "&h>5&o>5"
        tT, tG = R.build(bg, srt, nt, cols, col, f1_conditional(f1.get(cols[col]), "h>5&o>5"), fbn)
        out[f"FB|T|{fbn}"] = tT; out[f"FB|G|{fbn}"] = tG
    pulls = {}
    for k, terms in out.items():
        e = res["entries"][k]
        q = np.array([b84(terms, 100_000, s)[0] for s in range(10)])
        sd = float(q.std(ddof=1))
        pulls[k] = dict(rel_sd_1e5=sd / e["B84_v2"], pull_v1=(e["B84_v1"] - e["B84_v2"]) / sd, rel_b84=e["rel_b84"])
    res["mc_power"] = dict(note="sd of a 1e5-draw B84 over 10 seeds; pull = (B84_v1 - B84_v2[4e6]) / sd", entries=pulls,
                           max_abs_pull=max(abs(v["pull_v1"]) for v in pulls.values()),
                           n_abs_pull_gt_3=sum(abs(v["pull_v1"]) > 3 for v in pulls.values()),
                           rel_sd_range=[min(v["rel_sd_1e5"] for v in pulls.values()),
                                         max(v["rel_sd_1e5"] for v in pulls.values())])
    tmp = R.OUT.with_suffix(".json.part"); tmp.write_text(json.dumps(res, indent=1, default=str) + "\n"); tmp.replace(R.OUT)
    log.info("mc power: max |pull| %.2f, n(|pull| > 3) %d, rel sd(1e5) %.4f-%.4f", res["mc_power"]["max_abs_pull"],
             res["mc_power"]["n_abs_pull_gt_3"], *res["mc_power"]["rel_sd_range"])


if __name__ == "__main__":
    main()
