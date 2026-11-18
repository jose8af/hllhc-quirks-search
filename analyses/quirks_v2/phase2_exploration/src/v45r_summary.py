"""v45r_summary.py -- channel (i), Ignatius 2026-11-18: COMMITMENTS amendment E2 part (ii) verdict from the restricted
V4-5 scans (p2-a-c2-v45rpu, p2-a-c2-v45rsig; v45_bruteforce.py --restrict), next to part (i) (F0 vs independent fit).

Criterion (E2 (ii), as worded): the exhaustive 0.2 mrad scan within ±0.3 rad restricted to F0's inlier hits and the hits
within 3 sigma of the F0 plane, |dn| < 1 mrad in >= 48 of 50 per half.  If (ii) fails, (i) alone is the accuracy test
and the scan is reported as failed.  Signal half: direction differences and scores only (no row counts, no fractions of
scanned rows).  Reads only the done-marker JSON outputs (no npz).  Usage: python3 v45r_summary.py <out.json>
"""
import json
import statistics as st
import sys
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
MARK = QV2 / "ledger" / "markers"


def outputs(camp):
    res = []
    for p in sorted((MARK / camp).glob("*/*.marker")):
        done = None
        for line in p.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("status") == "done":
                done = d
        if done:
            res += [o["path"] for o in done["outputs"] if o["name"].endswith(".json")]
    return res


def half(camp):
    T = []
    for p in outputs(camp):
        d = json.loads(Path(p).read_text())
        assert d.get("restrict") is True, f"{p} is not a restricted run"
        T += d["trials"]
    dn = [t["dn_F0_opt_mrad"] for t in T]
    fit = [t["dn_F0_fit_mrad"] for t in T]
    sc = [t.get("selfcheck_band_vs_direct") for t in T if t.get("selfcheck_band_vs_direct") is not None]
    bad = [dict(file=t["file"], trial=t["trial"], dn_opt_mrad=t["dn_F0_opt_mrad"], dn_fit_mrad=t["dn_F0_fit_mrad"],
                dn_opt_fit_mrad=t["dn_opt_fit_mrad"], score_F0=t["score_F0"], score_opt=t["score_opt"],
                on_edge=t["opt_on_grid_edge"], n_restricted=t["n_restricted"], local_dn_mrad=t["local_dn_F0_mrad"])
           for t in T if not t["agree_opt"]]
    return dict(campaign=camp, n=len(T), n_agree_restricted=sum(t["agree_opt"] for t in T),
                n_agree_fit=sum(t["agree_fit"] for t in T), pass_ii=sum(t["agree_opt"] for t in T) >= 48 and len(T) == 50,
                dn_opt_max=max(dn), dn_opt_median=st.median(dn), dn_fit_max=max(fit),
                dn_opt_fit_max=max(t["dn_opt_fit_mrad"] for t in T),
                n_restricted_median=st.median(t["n_restricted"] for t in T),
                n_restricted_range=[min(t["n_restricted"] for t in T), max(t["n_restricted"] for t in T)],
                n_band3s_median=st.median(t["n_band3s"] for t in T),
                f0_record_found=sum(t["n_f0_record"] > 0 for t in T),
                f0_record_all_matched=sum(t["n_f0_record"] > 0 and t["n_f0_record_matched"] == t["n_f0_record"] for t in T),
                f0_record_outside_band_total=sum(t["n_f0_record_outside_band"] for t in T),
                pool_reproduced=sum(t["pool_reproduced"] for t in T), opt_on_edge=sum(t["opt_on_grid_edge"] for t in T),
                selfcheck_max=max(sc) if sc else None, local_is_global=sum(t["local_is_global"] for t in T),
                disagreements=bad)


def main(dst):
    out = dict(definition=__doc__, pu=half("p2-a-c2-v45rpu"), sig=half("p2-a-c2-v45rsig"))
    out["verdict_ii"] = "PASS" if (out["pu"]["pass_ii"] and out["sig"]["pass_ii"]) else "FAIL"
    Path(dst).write_text(json.dumps(out, indent=1))
    for h in ("pu", "sig"):
        x = out[h]
        sys.stderr.write(f"{h}: restricted {x['n_agree_restricted']}/{x['n']}, fit {x['n_agree_fit']}/{x['n']}, "
                         f"max dn {x['dn_opt_max']:.3f} mrad, median {x['dn_opt_median']:.3f}\n")
    sys.stderr.write(f"E2 (ii): {out['verdict_ii']}\n")


if __name__ == "__main__":
    main(sys.argv[1])
