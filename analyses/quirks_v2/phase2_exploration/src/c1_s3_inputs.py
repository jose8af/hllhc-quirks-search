"""c1_s3_inputs.py -- C1 signal: Stage-2 chunks -> stitched TRGS -> Stage-3 input file (channel (i), Rosalie, 2026-11-16).

Re-implements, for the C1 points only and without writing into data/sim, the v1 steps (all read-only copies of logic):
  sim/scripts/merge_chunks.py   weights rescaled by N_LHE,chunk / N_LHE,total
  sim/scripts/stitch_trg.py     TRGS = TRG (pT(QQ)_ME >= 100) U INC[pT(QQ)_ME < 100], rows shuffled with
                                default_rng(20261011 + m).permutation (v1 SHUFFLE_SEED, spin F)
  sim/scripts/add_rowmap.py     per-row provenance: chunk, tt_split.  v2 simplification (logged): ievt_lhe = index of the
                                row inside its chunk npz (not re-matched to the LHE), py8_seed = the chunk's Pythia seed,
                                tt_split = bit 0 of blake2b("qv2|c1.s2.split|<ID>|m|chunk|i")
  sim/stage3/code/make_inputs.py  extract(spin, m, 'p2'): w > 0, pT(QQ) > 200, |eta_pair| < 4, deterministic hit-or-miss
                                unweighting (seed 12345 over ALL rows), file order, per split up to the N_STORE-th
                                |eta| < 2.5 event; luminous vertex from blake2b("vtx|spin|m|row"); tilt weights.
N_STORE per split = 220 (v1: 300) so that both splits together hold >= 400 counting rows (C1: 400 rows per point).
sigma_norm_fb is not computed (annotate_npz.py not run; not used by Stage 3 or the C1 counts): stored as NaN.

Run as a runner job with the sim `ana` env:
  sim/.pixi/envs/ana/bin/python c1_s3_inputs.py <m> --trg A.npz,B.npz --trg-json A.json,B.json --inc ... --inc-json ...
Outputs in $QV2_OUT_DIR: F_m<m>_p2.npz (Stage-3 input schema of v1), E-TRGS_m<m>.npz, c1_inputs_m<m>.json.
"""
import argparse
import hashlib
import json
import logging
import os
from pathlib import Path

import numpy as np

log = logging.getLogger("c1_s3_inputs")
UNW_SEED = 12345
PTMIN = 200.0
N_STORE = 220
CUT_ME = 100.0
SHUFFLE_SEED = 20261011
SIG_XY_MM, SIG_Z_MM, SIG_T_NS = 0.005, 45.0, 0.190


def hseed(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "little")


def md5_file(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def merge(files, jsons, label, m):
    cs = [dict(np.load(f, allow_pickle=False)) for f in files]
    meta = [json.load(open(j)) for j in jsons]
    names = cs[0]["wvar_names"]
    for c in cs[1:]:
        assert list(c["wvar_names"]) == list(names), "weight names differ between chunks"
    ntot = sum(int(c["nlhe"]) for c in cs)
    n0 = len(cs[0]["w"])
    per_event = [k for k, v in cs[0].items() if hasattr(v, "shape") and v.ndim >= 1 and len(v) == n0 and k != "wvar_names"]
    out = {}
    for k in per_event:
        out[k] = np.concatenate([c[k] * (int(c["nlhe"]) / ntot) if k in ("w", "wvar") else c[k] for c in cs])
    out["chunk"] = np.concatenate([np.full(len(c["w"]), i, np.int16) for i, c in enumerate(cs)])
    out["ievt_lhe"] = np.concatenate([np.arange(len(c["w"]), dtype=np.int32) for c in cs])
    out["py8_seed"] = np.concatenate([np.full(len(c["w"]), int(mt["seed_py8"]), np.int64) for c, mt in zip(cs, meta)])
    out["tt_split"] = np.array([hseed(f"qv2|c1.s2.split|{label}|{m}|{int(ch)}|{int(i)}") & 1
                                for ch, i in zip(out["chunk"], out["ievt_lhe"])], np.int8)
    for k in ("wvar_names", "mq", "spin", "merging_nominal", "n_ic_included"):
        out[k] = cs[0][k]
    out["nlhe"] = ntot
    out["sigma_lhe_fb"] = sum(float(c["sigma_lhe_fb"]) * int(c["nlhe"]) for c in cs) / ntot
    out["chunk_tags"] = np.array([mt["tag"] for mt in meta])
    return out


def stitch(ct, ci, m):
    H = ci["p_qq_hard"]
    comp = np.hypot(H[:, 1], H[:, 2]) < CUT_ME
    n = len(ct["w"])
    out = {}
    for k, v in ct.items():
        if hasattr(v, "shape") and v.ndim >= 1 and len(v) == n and k != "wvar_names":
            out[k] = np.concatenate([v, ci[k][comp]])
    out["origin"] = np.concatenate([np.zeros(n, np.int8), np.ones(int(comp.sum()), np.int8)])
    seed = SHUFFLE_SEED + m
    perm = np.random.default_rng(seed).permutation(len(out["w"]))
    for k in list(out):
        out[k] = out[k][perm]
    out["row_src"] = perm.astype(np.int32)
    out["shuffle_seed"] = seed
    for k in ("wvar_names", "mq", "spin", "merging_nominal", "n_ic_included"):
        out[k] = ct[k]
    out["nlhe_trg"] = ct["nlhe"]; out["nlhe_inc"] = ci["nlhe"]; out["me_cut"] = CUT_ME
    out["nlhe"] = int(ct["nlhe"]) + int(ci["nlhe"]); out["kind"] = "stitched"
    out["sigma_lhe_fb_trg"] = ct["sigma_lhe_fb"]; out["sigma_lhe_fb_inc"] = ci["sigma_lhe_fb"]
    out["sigma_ref_fb"] = float(ci["w"].sum())
    out["sigma_norm_fb"] = float("nan")
    out["chunk_tags_trg"] = ct["chunk_tags"]; out["chunk_tags_inc"] = ci["chunk_tags"]
    pt = out["pt_pair"]
    chk = dict(n_rows=int(len(out["w"])), n_from_inc=int(comp.sum()),
               sigma_pt200_stitched_fb=float(out["w"][pt > 200].sum()),
               sigma_pt200_inc_fb=float(ci["w"][ci["pt_pair"] > 200].sum()))
    return out, chk


def wmedian(x, w):
    o = np.argsort(x); xs = x[o]; cw = np.cumsum(w[o]); cw /= cw[-1]
    return float(np.interp(0.5, cw, xs))


def tilt(x, target):
    xt = np.median(x)
    goal = (1 + target) * wmedian(x, np.ones_like(x))

    def f(a):
        return wmedian(x, (x / xt) ** a) - goal
    lo, hi = (0.0, 20.0) if target > 0 else (-20.0, 0.0)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise RuntimeError("tilt bracket failed")
    for _ in range(80):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def extract(c, spin, m, src_name, src_md5):
    w = c["w"]
    wmax = float(w[w > 0].max())
    acc = (w > 0) & (np.random.default_rng(UNW_SEED).random(len(w)) < w / wmax)
    sel = (w > 0) & (np.abs(c["eta_pair"]) < 4.0) & (c["pt_pair"] > PTMIN)
    ids = np.where(sel)[0]
    ids = ids[acc[ids]]
    eta = c["eta_pair"][ids]; spl = c["tt_split"][ids]
    keep = np.zeros(len(ids), bool)
    reached = {}
    for s in (0, 1):
        ins = (spl == s) & (np.abs(eta) < 2.5)
        csum = np.cumsum(ins)
        reached[s] = int(csum[-1]) if len(csum) else 0
        last = np.searchsorted(csum, N_STORE)
        keep |= (spl == s) & (np.arange(len(ids)) <= last)
    ids = ids[keep]
    names = [str(x) for x in c["wvar_names"]]
    merged = [i for i, nm in enumerate(names) if "_MERGING=" in nm]
    w_orig = c["w"][ids]
    d = dict(row=ids.astype(np.int64), chunk=c["chunk"][ids], ievt_lhe=c["ievt_lhe"][ids], py8_seed=c["py8_seed"][ids],
             tt_split=c["tt_split"][ids], origin=c["origin"][ids], w_orig=w_orig,
             wvar_ratio=(c["wvar"][ids][:, merged] / w_orig[:, None]).astype(np.float32),
             wvar_names=np.array([names[i] for i in merged]),
             p_qp=c["p_qp"][ids, 1:].copy(), p_qm=c["p_qm"][ids, 1:].copy(), recoil=c["recoil"][ids], jets=c["jets"][ids],
             njet=c["njet"][ids], gstar=c["gamma_star"][ids], cstar=c["cstar"][ids], bg=c["bg_pair"][ids],
             eta=c["eta_pair"][ids], pt=c["pt_pair"][ids], M=c["m_pair"][ids],
             in_eta25=np.abs(c["eta_pair"][ids]) < 2.5)
    vt = np.zeros((len(ids), 4))
    for i, r in enumerate(ids):
        g = np.random.default_rng(hseed(f"vtx|{spin}|{m}|{int(r)}"))
        vt[i] = g.normal(0.0, [SIG_XY_MM, SIG_XY_MM, SIG_Z_MM, SIG_T_NS])
    d["vtx_lumi"] = vt
    x = 2 * (d["gstar"] - 1)
    cset = d["in_eta25"]
    tilts = {}
    for key, tgt in (("w_lmax_up", 0.05), ("w_lmax_dn", -0.05), ("w_qed", -0.011), ("w_qed_19", -0.019)):
        a = tilt(x[cset], tgt)
        ww = (x / np.median(x[cset])) ** a
        d[key] = ww / ww[cset].mean()
        tilts[key] = dict(a=a, target=tgt)
    selection = dict(sample="trig (TRGS), C1 v2 regeneration", file=src_name, positive_weights=True, ptmin=PTMIN,
                     eta_max=4.0, count_region_eta=2.5, split="template+toy", n_store_per_split=N_STORE, unweight=True,
                     unweight_seed=UNW_SEED, w_max=wmax, vertex=dict(sig_xy_mm=SIG_XY_MM, sig_z_mm=SIG_Z_MM,
                     sig_t_ns=SIG_T_NS, seed_rule='default_rng(blake2b("vtx|spin|m|row") 8-byte little endian)'),
                     tilts=tilts, accepted_in_eta25_per_split=reached)
    d.update(source_file=np.array(src_name), source_md5=np.array(src_md5), sigma_norm_fb=np.array(float("nan")),
             sigma_ref_fb=np.array(float(c["sigma_ref_fb"])), w_max=np.array(wmax),
             selection_json=np.array(json.dumps(selection, default=float)), spin=np.array(spin), m=np.array(float(m)),
             sel=np.array("p2"))
    return d, selection


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    for k in ("trg", "trg-json", "inc", "inc-json"):
        ap.add_argument("--" + k, required=True)
    a = ap.parse_args()
    out = Path(os.environ.get("QV2_OUT_DIR", "."))
    ct = merge(a.trg.split(","), a.trg_json.split(","), "E-TRG", a.m)
    ci = merge(a.inc.split(","), a.inc_json.split(","), "E-INC", a.m)
    st, chk = stitch(ct, ci, a.m)
    sname = f"E-TRGS_m{a.m}.npz"
    np.savez_compressed(out / sname, **st)
    d, sel = extract(st, "F", a.m, sname, md5_file(out / sname))
    np.savez_compressed(out / f"F_m{a.m}_p2.npz", **d)
    info = dict(m=a.m, stitch=chk, n_stored=int(len(d["row"])),
                n_in_eta25_template=int(np.sum(d["in_eta25"] & (d["tt_split"] == 0))),
                n_in_eta25_toy=int(np.sum(d["in_eta25"] & (d["tt_split"] == 1))),
                accepted_in_eta25_per_split=sel["accepted_in_eta25_per_split"], w_max=sel["w_max"],
                nlhe_trg=int(ct["nlhe"]), nlhe_inc=int(ci["nlhe"]), chunks_trg=list(map(str, ct["chunk_tags"])),
                chunks_inc=list(map(str, ci["chunk_tags"])))
    (out / f"c1_inputs_m{a.m}.json").write_text(json.dumps(info, indent=1))
    log.info("done: %s", json.dumps(info))


if __name__ == "__main__":
    main()
