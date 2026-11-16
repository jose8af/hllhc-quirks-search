"""c1_signal_compare.py -- C1 signal comparisons under the Gate-A Q1 tiers (channel (i), Rosalie, 2026-11-16).

Per output file of the C1 signal campaigns, v1's own acts/stage4/analysis/signal.analyse_file decides "event passes
rung r" (signal match on the stored hit record, f_CKF < 0.2, cumulative in-job flags; denominator = every counting row,
status != 1 counted as failure; no probe-row exclusion in v2, see the session log).

open   (channel (i)):  BEFORE analyse_file sees the data, every rung column except R01-R06 is zeroed in cand.rungs and in
       sig.eff*, and F1 / observables are switched off, so no sealed quantity is computed even in memory.  Only the
       declared open quantities are kept: R04 at E200 1.5, E200 2, E500 3 keV and R06 at E200 1.5 keV.  Test: Fisher
       exact against v1's k/200 (STR §4.1 table; D4 §4.2), PASS if p > 0.05/41.
sealed (a separate session, Gate-A Q1; NOT run by channel (i)):  R07 at the three points and the v1 fallback column
       (FB2 at E200 1.5, FB3 at E200 2 and E500 3; F1 on) -> only PASS/FAIL per quantity is printed; counts and p-values
       go to an AES-256 file encrypted with `openssl enc -aes-256-cbc -pbkdf2 -pass file:<key>` (key held by the
       orchestrator), written outside the repository, and its sha256 is printed for the ledger.
selftest-sealed: exercises the sealed write path on SYNTHETIC numbers only (no file is read) with a throwaway key.

Run (TT env, on a worker):  python c1_signal_compare.py open --a2 p2-a-c1-siga2 --a5 p2-a-c1-siga5
"""
import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
sys.path.insert(0, str(QV2))
os.environ.setdefault("QV2_S3_DATA", str(HERE.parent / "outputs" / "c1_s3"))
log = logging.getLogger("c1_signal_compare")
N_DECL = 41
OPEN = {  # (point, rung index in the 23-col ladder, v1 k, v1 n)  [STR §4.1 table; D4 §4.2 V]
    "E200_1.5.R04": ("F", 200, 1.5, 3, 41, 200),
    "E200_1.5.R06": ("F", 200, 1.5, 5, 33, 200),
    "E200_2.R04": ("F", 200, 2.0, 3, 45, 200),
    "E500_3.R04": ("F", 500, 3.0, 3, 61, 200),
}
SEALED = {  # (point, kind, column, v1 k, v1 n): R07 = ladder index 6; FB_k = fallback column k of signal.FB_NAMES
    "E200_1.5.R07": ("F", 200, 1.5, "L", 6, 18, 200), "E200_1.5.FB2": ("F", 200, 1.5, "FB", "FB2", 9, 200),
    "E200_2.R07": ("F", 200, 2.0, "L", 6, 31, 200), "E200_2.FB3": ("F", 200, 2.0, "FB", "FB3", 10, 200),
    "E500_3.R07": ("F", 500, 3.0, "L", 6, 48, 200), "E500_3.FB3": ("F", 500, 3.0, "FB", "FB3", 11, 200),
}


def done_outputs(camp):
    out = []
    for p in sorted((QV2 / "ledger" / "markers" / camp).glob("*/*.marker")):
        done = None
        for line in p.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("status") == "done":
                done = d
        if done:
            out += [o["path"] for o in done["outputs"] if o["name"].endswith(".npz")]
    return out


def mask_open(d):
    """Zero every rung bit outside R01-R06 (columns 0-5 of the 43 in-job columns) before any analysis."""
    keep = np.zeros(43, bool); keep[:6] = True
    for k in ("cand.rungs", "sig.eff", "sig.eff_fckf", "sig.eff_T", "sig.eff_fckf_T", "trials.n_pass", "trials.n_grp",
              "trials.n_pass_T", "trials.n_grp_T"):
        if k not in d:
            continue
        if k.startswith("trials."):
            x = d[k].copy(); x[:, ~keep] = 0; d[k] = x
        else:
            b = np.unpackbits(d[k], axis=1)[:, :43]
            b[:, ~keep] = 0
            d[k] = np.packbits(b, axis=1)
    return d


def entries(paths, masked):
    from acts.stage4.analysis import signal as SG
    for p in paths:
        with np.load(p, allow_pickle=False) as z:
            d = {k: z[k] for k in z.files}
        meta = json.loads(str(d["meta_json"]))
        if masked:
            d = mask_open(d)
        ents, _ = SG.analyse_file(dict(d=d, job=meta["job"], path=p), want_f1=not masked, obs=False)
        job = meta["job"]
        for e in ents:
            key = ("F", int(job["m"]) if job["kind"] == "a2" else int(job["point"].split("_m")[1].split("/")[0]),
                   float(e["lam"]))
            yield job["kind"], key, e


def fisher(k2, n2, k1, n1):
    return float(stats.fisher_exact([[k2, n2 - k2], [k1, n1 - k1]])[1])


def cmd_open(a):
    acc = {}
    for camp, kind in ((a.a2, "a2"), (a.a5, "a5")):
        for kd, key, e in entries(done_outputs(camp), masked=True):
            acc.setdefault((kd, key), []).append(bool(e["L"][3]))
            acc.setdefault((kd, key, "R06"), []).append(bool(e["L"][5]))
    res = {}
    for name, (spin, m, lam, col, k1, n1) in OPEN.items():
        kind = "a5" if m == 500 else "a2"          # v1 path per point (COM C1-e)
        lst = acc.get((kind, (spin, m, lam)) if col == 3 else (kind, (spin, m, lam), "R06"), [])
        n2 = len(lst); k2 = int(np.sum(lst))
        p = fisher(k2, n2, k1, n1) if n2 else float("nan")
        res[name] = dict(v1=f"{k1}/{n1}", v2=f"{k2}/{n2}", p=p, pass_=bool(p > 0.05 / N_DECL), test="Fisher exact",
                         mde_note="gross check: 2-sigma detectable shift about 34 % at R04 (STR §4.1 point 4)")
    # twins at R04 (open diagnostic; declared expectation x0.832, D4 l.342)
    for lam in (1.5, 2.0):
        fa = acc.get(("a2", ("F", 200, lam)), []); fc = acc.get(("a5", ("F", 200, lam)), [])
        if fa and fc:
            res[f"twin_R04_E200_{lam:g}"] = dict(fast=f"{int(np.sum(fa))}/{len(fa)}", full=f"{int(np.sum(fc))}/{len(fc)}",
                                                ratio_full_over_fast=float(np.sum(fc) / max(1, np.sum(fa))),
                                                v1_expectation=0.832)
    out = HERE.parent / "outputs" / "c1_signal_open.json"
    out.write_text(json.dumps(res, indent=1))
    log.info("open tier: %s", json.dumps(res))


def write_sealed(payload, key_file, out_path):
    raw = json.dumps(payload, indent=1).encode()
    p = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt", "-pass", f"file:{key_file}", "-out",
                        str(out_path)], input=raw, check=True)
    del p
    return hashlib.sha256(Path(out_path).read_bytes()).hexdigest()


def cmd_sealed(a):      # run ONLY by the dedicated sealed session (Gate-A Q1)
    acc = {}
    for camp in (a.a2, a.a5):
        for kd, key, e in entries(done_outputs(camp), masked=False):
            acc.setdefault((kd, key), []).append(e)
    names = list(__import__("acts.stage4.analysis.signal", fromlist=["FB_NAMES"]).FB_NAMES)
    payload, verdict = {}, {}
    for name, (spin, m, lam, typ, col, k1, n1) in SEALED.items():
        kind = "a5" if m == 500 else "a2"
        ents = acc.get((kind, (spin, m, lam)), [])
        v = [bool(e["L"][col]) if typ == "L" else bool(e["FB"][names.index(col)]) for e in ents]
        k2, n2 = int(np.sum(v)), len(v)
        p = fisher(k2, n2, k1, n1) if n2 else float("nan")
        payload[name] = dict(v1=[k1, n1], v2=[k2, n2], p=p)
        verdict[name] = "PASS" if p > 0.05 / N_DECL else "FAIL"
    sha = write_sealed(payload, a.key_file, a.out)
    log.info("sealed verdicts: %s; sealed file %s sha256 %s", json.dumps(verdict), a.out, sha)


def cmd_selftest(a):    # synthetic numbers only; no data file is read
    import tempfile
    with tempfile.TemporaryDirectory(dir=os.environ.get("QV2_SCRATCH", "/var/tmp")) as td:
        key = Path(td) / "k"; key.write_bytes(os.urandom(32))
        payload = {"SYNTHETIC": dict(v1=[18, 200], v2=[40, 400], p=fisher(40, 400, 18, 200))}
        f = Path(td) / "sealed.bin"
        sha = write_sealed(payload, key, f)
        back = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", f"file:{key}", "-in", str(f)],
                              capture_output=True, check=True).stdout
        ok = json.loads(back) == payload
        log.info("selftest-sealed: round trip %s, sha256 %s, synthetic PASS/FAIL %s", "OK" if ok else "BROKEN", sha,
                 "PASS" if payload["SYNTHETIC"]["p"] > 0.05 / N_DECL else "FAIL")


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["open", "sealed", "selftest-sealed"])
    ap.add_argument("--a2", default="p2-a-c1-siga2")
    ap.add_argument("--a5", default="p2-a-c1-siga5")
    ap.add_argument("--key-file")
    ap.add_argument("--out")
    a = ap.parse_args()
    {"open": cmd_open, "sealed": cmd_sealed, "selftest-sealed": cmd_selftest}[a.mode](a)


if __name__ == "__main__":
    main()
