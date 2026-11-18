"""stitch_100k.py -- channel (i), Ignatius 2026-11-18: closure of v1's TRGS stitching with the 100k INC sample at m = 200.

v1 stitch_trg.py (docstring, QV2/sim/scripts/stitch_trg.py l.4-5): the stitching is exact if
    sigma_TRG(pT(QQ) > 200)  ==  sigma_INC(pT(QQ) > 200, pT(QQ)_ME >= 100),
pT(QQ) = column 'pt_pair' (after the shower), pT(QQ)_ME = hypot(p_qq_hard[:, 1], p_qq_hard[:, 2]) (stitch_trg.py l.40).
Inputs (done markers required): TRG = p2-a-c1-s2 c1s2-trg-m200-c00 (20k LHE); INC = p2-a-c1-s2 c1s2-inc-m200-c00 plus
p2-a-c1-s2inc c1s2-inc-m200-c01..c05 (6 x 20k LHE).  INC chunks merged as merge_chunks.py (l.2-3): w x N_LHE,chunk /
N_LHE,total.  Errors sqrt(sum w^2) of the selected rows; z = (TRG - INC) / sqrt(err_T^2 + err_I^2) (independent samples).
Also per INC chunk (spread check) and the 20k-only result (c00, Rosalie's EXPLORATION §3: 3.798 +- 0.179 fb).
Usage (worker, TT env):  python stitch_100k.py <out.json>
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("stitch")
QV2 = Path(__file__).resolve().parents[2]
D = Path("/nfs/cajuela/jdochoa/quirks_v2/data/phase2")
TRG = ("p2-a-c1-s2", "c1s2-trg-m200-c00")
INC = [("p2-a-c1-s2", "c1s2-inc-m200-c00")] + [("p2-a-c1-s2inc", f"c1s2-inc-m200-c{i:02d}") for i in range(1, 6)]
PT, PTME = 200.0, 100.0


def load(camp, job):
    mk = QV2 / "ledger" / "markers" / camp / "000" / f"{job}.marker"
    assert mk.exists() and '"done"' in mk.read_text(), f"no done marker for {camp}/{job}"
    with np.load(D / camp / "000" / f"{job}.npz", allow_pickle=False) as z:
        H = z["p_qq_hard"]
        return dict(w=z["w"].astype(np.float64), pt=z["pt_pair"].astype(np.float64),
                    ptme=np.hypot(H[:, 1], H[:, 2]).astype(np.float64), nlhe=int(z["nlhe"]))


def sig(c, me):
    m = c["pt"] > PT
    if me:
        m &= c["ptme"] >= PTME
    return float(c["w"][m].sum()), float(np.sqrt((c["w"][m] ** 2).sum())), int(m.sum())


def main(out):
    t = load(*TRG)
    sT, eT, nT = sig(t, False)
    cs = [load(*x) for x in INC]
    N = sum(c["nlhe"] for c in cs)
    per = []
    for (camp, job), c in zip(INC, cs):
        s, e, n = sig(c, True)
        per.append(dict(job=job, nlhe=c["nlhe"], sigma_fb=s, err_fb=e, rows=n, ratio=sT / s))
    mw = np.concatenate([c["w"] * c["nlhe"] / N for c in cs])
    mpt = np.concatenate([c["pt"] for c in cs]); mme = np.concatenate([c["ptme"] for c in cs])
    sel = (mpt > PT) & (mme >= PTME)
    sI, eI, nI = float(mw[sel].sum()), float(np.sqrt((mw[sel] ** 2).sum())), int(sel.sum())
    r = sT / sI
    er = r * np.hypot(eT / sT, eI / sI)
    z = (sT - sI) / np.hypot(eT, eI)
    # spread of the six per-chunk INC values against their own errors (chi2 of a constant)
    v = np.array([p["sigma_fb"] for p in per]); ev = np.array([p["err_fb"] for p in per])
    wm = (v / ev ** 2).sum() / (1 / ev ** 2).sum()
    chi2 = float((((v - wm) / ev) ** 2).sum())
    # what pT_ME < 100 contributes to sigma_INC(pT > 200): the INC-complement share of the stitched tail
    comp = (mpt > PT) & (mme < PTME)
    res = dict(trg=dict(job=TRG[1], nlhe=t["nlhe"], sigma_fb=sT, err_fb=eT, rows=nT),
               inc_merged=dict(nlhe=N, sigma_fb=sI, err_fb=eI, rows=nI,
                               sigma_ptme_lt100_fb=float(mw[comp].sum()),
                               err_ptme_lt100_fb=float(np.sqrt((mw[comp] ** 2).sum())),
                               sigma_all_pt200_fb=float(mw[mpt > PT].sum())),
               ratio=r, ratio_err=er, z=float(z), inc_chunks=per, inc_chunk_chi2=chi2, inc_chunk_ndf=len(per) - 1,
               definition=__doc__)
    Path(out).write_text(json.dumps(res, indent=1))
    log.info("TRG %.4f +- %.4f fb (%d rows); INC(100k, pT_ME>=100) %.4f +- %.4f fb (%d rows); ratio %.4f +- %.4f; z %.2f",
             sT, eT, nT, sI, eI, nI, r, er, z)
    for p in per:
        log.info("  %s: %.4f +- %.4f fb (%d rows) ratio %.3f", p["job"], p["sigma_fb"], p["err_fb"], p["rows"], p["ratio"])
    log.info("chunk chi2 %.2f / %d", chi2, len(per) - 1)


if __name__ == "__main__":
    main(sys.argv[1])
