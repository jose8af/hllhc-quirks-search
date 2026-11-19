"""c1_signal_compare.py -- C1 signal comparisons under the Gate-A Q1 tiers (channel (i), Rosalie, 2026-11-16).

Per output file of the C1 signal campaigns, v1's own acts/stage4/analysis/signal.analyse_file decides "event passes
rung r" (signal match on the stored hit record, f_CKF < 0.2, cumulative in-job flags; denominator = every counting row,
status != 1 counted as failure; no probe-row exclusion in v2, see the session log).

open   (channel (i)):  BEFORE analyse_file sees the data, every rung column except R01-R06 is zeroed in cand.rungs and in
       sig.eff*, and F1 / observables are switched off, so no sealed quantity is computed even in memory.  Only the
       declared open quantities are kept: R04 at E200 1.5, E200 2, E500 3 keV and R06 at E200 1.5 keV.  Test: Fisher
       exact against v1's k/200 (STR §4.1 table; D4 §4.2), PASS if p > 0.05/41.
sealed (a separate session, Gate-A Q1; NOT run by channel (i)):  R07 at the three points and the v1 fallback column
       (FB2 at E200 1.5, FB3 at E200 2 and E500 3; F1 on) -> stdout carries only PASS/FAIL per sealed entry, per
       signal-family coherence (joint nested-binomial covariance) and per global chi2_41 form ("frozen-naive",
       "joint-block"; the 35 open z's from outputs/c1_compare_mattias_2026-11-19.json and outputs/c1_signal_open.json),
       n-complete yes/no, path and sha256 of the encrypted file, commit hash.  Counts, p, z, sums and the fallback twin
       ratio go to an AES-256 file (`openssl enc -aes-256-cbc -pbkdf2 -pass file:<key>`, key outside the repo and the
       data tree), written outside the repository.  Guards: n2 != 400 or incomplete input -> stop, nothing printed or
       written; any exception -> only "crashed: <class>".  Choices: outputs/SEALED_PREP_petra_2026-11-19.md.
selftest-sealed: exercises the whole sealed path on SYNTHETIC numbers only (no data file is read) with a throwaway key.

Run (TT env, on a worker):  python c1_signal_compare.py open --a2 p2-a-c1-siga2 --a5 p2-a-c1-siga5
"""
import argparse
import contextlib
import hashlib
import json
import logging
import os
import string
import subprocess
import sys
import warnings
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
        if meta.get("empty_chunk"):
            continue
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


# ---------------------------------------------------------------------------------------------------------------------
# Sealed tier C1-d (advisor ruling Oddny, LOG.md 2026-11-19 10:28; code Petra 2026-11-19).  Every choice below that the
# frozen text (STR_oscar l.593-604, l.629-644) leaves open is pre-registered in
# outputs/SEALED_PREP_petra_2026-11-19.md, committed with this code before any sealed read.
#   * stdout carries ONLY: PASS/FAIL per sealed entry, PASS/FAIL per signal-family coherence, PASS/FAIL per global form,
#     n-complete yes/no, path + sha256 of the encrypted file, commit hash.  Everything else goes into the encrypted file.
#   * while the sealed path runs, file descriptors 1 and 2 point to /dev/null, logging and warnings are off; any
#     exception prints only "crashed: <class>"; a guard (n2 != 400, incomplete input, refused key/out path) prints only
#     "n-complete: no" and the guard's name, and writes nothing.
#   * the key is passed to openssl as -pass file:<key>; sealed mode only encrypts (no decryption path exists in it).
# ---------------------------------------------------------------------------------------------------------------------
REPO = QV2.parents[1]
DATA_TREES = ("/nfs/cajuela/jdochoa/quirks_v2",)
N2_EXPECTED = 400
N_BG = 31                       # background entries of the open read (c1_compare_mattias_2026-11-19.json)
BG_JSON = HERE.parent / "outputs" / "c1_compare_mattias_2026-11-19.json"
OPEN_JSON = HERE.parent / "outputs" / "c1_signal_open.json"
LADDER = {"R04": 3, "R06": 5, "R07": 6}     # column of e["L"] (as cmd_open / SEALED)
# signal family = one "signal" row of the declared-comparison table (STR_oscar l.582-584): the quantities of one point
FAMILIES = {
    "E200_1.5": ("a2", ("F", 200, 1.5), ("R04", "R06", "R07", "FB2")),
    "E200_2": ("a2", ("F", 200, 2.0), ("R04", "R07", "FB3")),
    "E500_3": ("a5", ("F", 500, 3.0), ("R04", "R07", "FB3")),
}
TWINS = {"E200_1.5": "FB2", "E200_2": "FB3"}   # fallback twin ratio full/fast (sealed, STR l.637-638; COM C1-e)
TWIN_FB_EXPECTATION = 0.871
V1 = {**{k: (v[4], v[5]) for k, v in OPEN.items()}, **{k: (v[5], v[6]) for k, v in SEALED.items()}}
K0_CONVENTION = ("a count k = 0 (v1 or v2) enters ln(x2/x1) and its width as k = 0.5 (Haldane), and that quantity's "
                 "covariances with the other quantities of its family are set to 0 in that sample; the Fisher test "
                 "uses the raw counts")


class Stop(Exception):
    """Guard: stop with no quantity printed and nothing written."""


def z_of_p(p):
    """Unsigned z of a two-sided p (the z_i of the global sum)."""
    return float(stats.norm.isf(min(1.0, float(p)) / 2.0))


def _under(path, roots):
    rp = os.path.realpath(path)
    return any(rp == r or rp.startswith(r.rstrip("/") + "/") for r in roots)


def _forbidden_roots():
    return [os.path.realpath(REPO), os.path.realpath(QV2 / "data"), *DATA_TREES]


def check_key(key_file):
    if not key_file:
        raise Stop("key file refused: --key-file missing")
    if _under(key_file, _forbidden_roots()):
        raise Stop("key file refused: inside the repository or the data tree")
    kp = Path(key_file)
    if not kp.is_file():
        raise Stop("key file refused: not a regular file")
    if kp.stat().st_mode & 0o077:
        raise Stop("key file refused: readable by group or others")
    lines = kp.read_bytes().decode("ascii", errors="replace").splitlines()
    ok = len(lines) == 1 and len(lines[0]) >= 32 and all(c in string.hexdigits for c in lines[0])
    del lines
    if not ok:
        raise Stop("key file refused: not one hex text line")


def check_out(out):
    if not out:
        raise Stop("out path refused: --out missing")
    if _under(out, [os.path.realpath(REPO)]):
        raise Stop("out path refused: inside the repository")
    o = Path(out)
    if o.exists() or Path(str(o) + ".part").exists():
        raise Stop("out path refused: exists (no overwrite)")
    o.parent.mkdir(parents=True, exist_ok=True)
    return o


def write_sealed(payload, key_file, out_path):
    """Encrypt only: openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:<key>; .part, fsync, rename; sha256."""
    raw = json.dumps(payload, indent=1, default=float).encode()
    part = Path(str(out_path) + ".part")
    subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt", "-pass", f"file:{key_file}", "-out",
                    str(part)], input=raw, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    del raw
    with open(part, "rb") as fh:
        os.fsync(fh.fileno())
    os.replace(part, out_path)
    return hashlib.sha256(Path(out_path).read_bytes()).hexdigest()


@contextlib.contextmanager
def silenced():
    """fd 1 and 2 -> /dev/null (catches C-level prints too), logging and warnings off, numpy errors ignored."""
    sys.stdout.flush(); sys.stderr.flush()
    saved = (os.dup(1), os.dup(2))
    dn = os.open(os.devnull, os.O_WRONLY)
    os.dup2(dn, 1); os.dup2(dn, 2)
    prev = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    try:
        with warnings.catch_warnings(), np.errstate(all="ignore"):
            warnings.simplefilter("ignore")
            yield
    finally:
        try:
            sys.stdout.flush(); sys.stderr.flush()
        except Exception:       # noqa: BLE001  (a broken stream must not print)
            pass
        os.dup2(saved[0], 1); os.dup2(saved[1], 2)
        for fd in (*saved, dn):
            os.close(fd)
        logging.disable(prev)


# ---- inputs ------------------------------------------------------------------------------------------------------------
def campaign_complete(camp):
    """Every job marker of the campaign has a 'done' line (else Stop).  Reads ledger markers only."""
    ms = sorted((QV2 / "ledger" / "markers" / camp).glob("*/*.marker"))
    if not ms:
        raise Stop(f"incomplete input: no markers for campaign {camp}")
    for p in ms:
        done = False
        for line in p.read_text().splitlines():
            try:
                done |= json.loads(line).get("status") == "done"
            except ValueError:
                continue
        if not done:
            raise Stop(f"incomplete input: unfinished job in campaign {camp}")
    return len(ms)


def load_rows_from_campaigns(a2, a5):
    """Per-row pass indicators of every family quantity (and the fallback twins), unmasked (sealed session only)."""
    nmark = {c: campaign_complete(c) for c in (a2, a5)}
    acc = {}
    for camp in (a2, a5):
        for kd, key, e in entries(done_outputs(camp), masked=False):
            acc.setdefault((kd, key), []).append(e)
    fbn = list(__import__("acts.stage4.analysis.signal", fromlist=["FB_NAMES"]).FB_NAMES)

    def col(e, q):
        return bool(e["L"][LADDER[q]]) if q in LADDER else bool(e["FB"][fbn.index(q)])

    rows = {f: {q: np.array([col(e, q) for e in acc.get((kind, pt), [])], bool) for q in qs}
            for f, (kind, pt, qs) in FAMILIES.items()}
    twins = {f: dict(fast=np.array([col(e, q) for e in acc.get(("a2", FAMILIES[f][1]), [])], bool),
                     full=np.array([col(e, q) for e in acc.get(("a5", FAMILIES[f][1]), [])], bool))
             for f, q in TWINS.items()}
    return rows, twins, dict(markers=nmark)


def check_inputs(rows, twins, open_res, bg):
    for f, (_, _, qs) in FAMILIES.items():
        if f not in rows:
            raise Stop(f"incomplete input: rows of family {f}")
        for q in qs:
            x = rows[f].get(q)
            if x is None:
                raise Stop(f"incomplete input: {f}.{q}")
            if len(x) != N2_EXPECTED:
                raise Stop(f"n2 guard: {f}.{q}")
    for f in TWINS:
        t = twins.get(f) or {}
        for s in ("fast", "full"):
            if s not in t:
                raise Stop(f"incomplete input: twin {f} {s}")
            if len(t[s]) != N2_EXPECTED:
                raise Stop(f"n2 guard: twin {f} {s}")
    for name in OPEN:
        o = open_res.get(name)
        if not o or "v2" not in o or not np.isfinite(o.get("p", np.nan)):
            raise Stop(f"incomplete input: open entry {name} in c1_signal_open.json")
        f, q = name.rsplit(".", 1)
        x = rows[f][q]
        if o["v2"] != f"{int(x.sum())}/{len(x)}":
            raise Stop(f"inconsistent input: open-tier recount of {name} differs from c1_signal_open.json")
    ents = bg.get("entries", {})
    if bg.get("n_declared") != N_DECL or len(ents) != N_BG or len(OPEN) + len(SEALED) + N_BG != N_DECL:
        raise Stop("incomplete input: background entries of c1_compare_mattias_2026-11-19.json")
    zs = [e.get("z", np.nan) for e in ents.values()]
    if not all(np.isfinite(zs)):
        raise Stop("incomplete input: background entry without finite z")
    g = bg.get("global_partial", {})
    if g.get("n_available") != N_BG or not np.isfinite(g.get("sum_z2", np.nan)):
        raise Stop("incomplete input: global_partial of the background read")
    if not np.isclose(g.get("sum_z2_naive", np.nan), float(np.sum(np.square(zs))), rtol=1e-9, atol=0):
        raise Stop("inconsistent input: background sum_z2_naive differs from its entries")


# ---- statistics --------------------------------------------------------------------------------------------------------
def family_stats(X, qs, v1kn):
    """Joint (nested-binomial / multinomial delta-method) covariance of ln(x2/x1) over the quantities of one family.
    X: (n2, K) bool v2 rows.  v2: Cov(ln p_a, ln p_b) = (p_ab/(p_a p_b) - 1)/n2 from the rows (nested pairs give the
    nested-binomial value (1/p_outer - 1)/n2 automatically).  v1 (rows lost): nested ladder pairs (R07 c R06 c R04) the
    nested-binomial value (1/p1_outer - 1)/n1; pairs with the fallback column: v1 correlation = v2's (ESTIMATE, as
    joint_family in c1_compare.py).  Coherence: frozen inverse-variance mean with diagonal weights, variance w'Sw/(sum w)^2
    with the full covariance; |z| < 3.  Block chi2: d' S^-1 d (K dof)."""
    X = np.asarray(X, bool); n2, K = X.shape
    k2 = X.sum(0).astype(float)
    k1 = np.array([v1kn[q][0] for q in qs], float); n1 = np.array([v1kn[q][1] for q in qs], float)
    if np.any(n1 != n1[0]):
        raise ValueError("v1 denominators differ within a family")
    n1 = float(n1[0])
    z2, z1 = k2 == 0, k1 == 0
    p2 = np.where(z2, 0.5, k2) / n2; p1 = np.where(z1, 0.5, k1) / n1
    d = np.log(p2) - np.log(p1)
    Xf = X.astype(float)
    P = Xf.T @ Xf / n2
    S2 = (P / np.outer(p2, p2) - 1.0) / n2
    S1 = np.zeros((K, K))
    for a in range(K):
        S2[a, a] = (1.0 / p2[a] - 1.0) / n2
        S1[a, a] = (1.0 / p1[a] - 1.0) / n1
    viol = {}
    for a in range(K):
        for b in range(a + 1, K):
            qa, qb = qs[a], qs[b]
            if qa in LADDER and qb in LADDER:
                o, i = (a, b) if LADDER[qa] < LADDER[qb] else (b, a)
                S1[a, b] = S1[b, a] = (1.0 / p1[o] - 1.0) / n1
                viol[f"{qs[i]} not in {qs[o]} (v2 rows)"] = int(np.sum(X[:, i] & ~X[:, o]))
            else:
                r2 = S2[a, b] / np.sqrt(S2[a, a] * S2[b, b])
                S1[a, b] = S1[b, a] = r2 * np.sqrt(S1[a, a] * S1[b, b])
    for a in range(K):
        if z2[a]:
            S2[a, :] = S2[:, a] = 0.0; S2[a, a] = (1.0 / p2[a] - 1.0) / n2
        if z1[a] or z2[a]:
            dg = S1[a, a]; S1[a, :] = S1[:, a] = 0.0; S1[a, a] = dg
    S = S1 + S2
    np.linalg.cholesky(S)                       # not positive definite -> exception -> "crashed: LinAlgError"
    w = 1.0 / np.diag(S)
    mu = float(w @ d / w.sum()); smu = float(np.sqrt(w @ S @ w) / w.sum())
    chi2 = float(d @ np.linalg.solve(S, d))
    if not (np.isfinite(mu) and np.isfinite(smu) and np.isfinite(chi2)):
        raise FloatingPointError("non-finite family statistic")
    return dict(quantities=list(qs), v1=[[int(x), int(n1)] for x in k1], v2=[[int(x), int(n2)] for x in k2],
                ln_ratio=d.tolist(), cov_v1=S1.tolist(), cov_v2=S2.tolist(), cov=S.tolist(),
                corr=(S / np.sqrt(np.outer(np.diag(S), np.diag(S)))).round(5).tolist(),
                mean_ln_ratio=mu, s=smu, z=mu / smu, coherent=bool(abs(mu / smu) < 3),
                chi2_block=chi2, chi2_block_ndof=K, chi2_block_p=float(stats.chi2.sf(chi2, K)),
                naive_independent=dict(s=float(1 / np.sqrt(w.sum())), z=float(mu * np.sqrt(w.sum())),
                                       coherent=bool(abs(mu * np.sqrt(w.sum())) < 3)),
                k0_v2=[q for q, t in zip(qs, z2) if t], k0_v1=[q for q, t in zip(qs, z1) if t],
                nesting_violations_v2=viol)


def compute_sealed(rows, twins, open_res, bg):
    check_inputs(rows, twins, open_res, bg)
    thr = 0.05 / N_DECL
    payload = dict(entries={}, open_entries={}, families={}, twins={}, k0_convention=K0_CONVENTION,
                   bonferroni_p=thr, test="Fisher exact (two-sided), STR_oscar l.594-596; z_i = isf(p/2)")
    verdict = dict(entries={}, families={}, globals={})
    for name, (spin, m, lam, typ, col, k1, n1) in SEALED.items():
        f, q = name.rsplit(".", 1)
        x = rows[f][q]; k2, n2 = int(x.sum()), len(x)
        p = fisher(k2, n2, k1, n1)
        payload["entries"][name] = dict(v1=[k1, n1], v2=[k2, n2], p=p, z=z_of_p(p), pass_=bool(p > thr),
                                        v2_over_v1=(k2 / n2) / (k1 / n1))
        verdict["entries"][name] = "PASS" if p > thr else "FAIL"
    for name, (spin, m, lam, col, k1, n1) in OPEN.items():
        f, q = name.rsplit(".", 1)
        x = rows[f][q]
        p = float(open_res[name]["p"])
        p_re = fisher(int(x.sum()), len(x), k1, n1)
        if not np.isclose(p, p_re, rtol=1e-9, atol=1e-12):
            raise Stop(f"inconsistent input: open-tier p of {name} differs from c1_signal_open.json")
        payload["open_entries"][name] = dict(v1=[k1, n1], v2=[int(x.sum()), len(x)], p=p, z=z_of_p(p))
    for f, (_, _, qs) in FAMILIES.items():
        X = np.column_stack([rows[f][q] for q in qs])
        fs = family_stats(X, qs, {q: V1[f"{f}.{q}"] for q in qs})
        payload["families"][f] = fs
        verdict["families"][f] = "PASS" if fs["coherent"] else "FAIL"
    g = bg["global_partial"]
    zs_open = [e["z"] for e in payload["open_entries"].values()]
    zs_seal = [e["z"] for e in payload["entries"].values()]
    c99 = float(stats.chi2.ppf(0.99, N_DECL))
    naive = float(g["sum_z2_naive"] + np.sum(np.square(zs_open)) + np.sum(np.square(zs_seal)))
    blk_sig = float(sum(fs["chi2_block"] for fs in payload["families"].values()))
    joint = float(g["sum_z2"] + blk_sig)
    payload["global"] = {
        "chi2_41_99th": c99,
        "frozen-naive": dict(sum_z2=naive, pass_=bool(naive < c99), background_sum_z2_naive=g["sum_z2_naive"],
                             open_sum_z2=float(np.sum(np.square(zs_open))),
                             sealed_sum_z2=float(np.sum(np.square(zs_seal))),
                             form="all 41 z_i treated as independent (STR_oscar l.597); signal z_i from the Fisher p"),
        "joint-block": dict(sum_z2=joint, pass_=bool(joint < c99), background_sum_z2_joint=g["sum_z2"],
                            signal_family_blocks=blk_sig,
                            background_sum_z2_v1_width_zero_plus_signal=float(g.get("sum_z2_v1_width_zero", np.nan)
                                                                              + blk_sig),
                            form="background: blocks of c1_compare_mattias (pu1,pu2,clos,cppu,sm as d'S^-1 d, other "
                                 "entries z^2); signal: one d'S^-1 d per family (10 dof); 41 dof in total"),
    }
    for k in ("frozen-naive", "joint-block"):
        verdict["globals"][k] = "PASS" if payload["global"][k]["pass_"] else "FAIL"
    for f, q in TWINS.items():
        fa, fc = twins[f]["fast"], twins[f]["full"]
        payload["twins"][f"twin_{q}_{f}"] = dict(fast=[int(fa.sum()), len(fa)], full=[int(fc.sum()), len(fc)],
                                                 ratio_full_over_fast=float(fc.sum() / max(1, fa.sum())),
                                                 v1_expectation=TWIN_FB_EXPECTATION)
    return verdict, payload


def git_commit():
    try:
        h = subprocess.run(["git", "-C", str(QV2), "rev-parse", "HEAD"], capture_output=True, text=True,
                           check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(QV2), "status", "--porcelain", "--", str(Path(__file__).resolve())],
                               capture_output=True, text=True, check=True).stdout.strip()
        return h, not dirty
    except Exception:           # noqa: BLE001
        return "unknown", False


def sealed_run(loader, open_loader, bg_loader, key_file, out, emit, prov=None):
    """The whole sealed path.  Returns 0 (done), 3 (guard stop), 2 (crash).  emit(line) is the ONLY output channel."""
    try:
        with silenced():
            try:
                check_key(key_file)
                o = check_out(out)
                rows, twins, meta = loader()
                open_res, bg = open_loader(), bg_loader()
                verdict, payload = compute_sealed(rows, twins, open_res, bg)
                commit, clean = git_commit()
                payload["provenance"] = dict(commit=commit, script_clean=clean, inputs=meta, **(prov or {}))
                sha = write_sealed(payload, key_file, o)
                del payload, rows, twins
                res = ("ok", verdict, str(o), sha, commit, clean)
            except Stop as s:
                res = ("stop", str(s))
            except BaseException as x:          # noqa: BLE001
                res = ("crash", type(x).__name__)
    except BaseException as x:                  # noqa: BLE001
        res = ("crash", type(x).__name__)
    if res[0] == "crash":
        emit(f"crashed: {res[1]}")
        return 2
    if res[0] == "stop":
        emit("n-complete: no")
        emit(f"STOPPED, nothing written: {res[1]}")
        return 3
    _, v, path, sha, commit, clean = res
    for k, x in v["entries"].items():
        emit(f"sealed entry {k}: {x}")
    for k, x in v["families"].items():
        emit(f"signal-family coherence {k}: {x}")
    for k, x in v["globals"].items():
        emit(f"global chi2_41 {k}: {x}")
    emit("n-complete: yes")
    emit(f"encrypted file: {path}")
    emit(f"sha256: {sha}")
    emit(f"commit: {commit} (script unchanged from commit: {'yes' if clean else 'no'})")
    return 0


def _sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cmd_sealed(a):      # run ONLY by the dedicated sealed session (Gate-A Q1; advisor ruling 2026-11-19 10:28)
    sys.excepthook = lambda t, v, tb: os.write(1, f"crashed: {t.__name__}\n".encode())
    out = logging.getLogger("c1_sealed_stdout"); out.propagate = False
    h = logging.StreamHandler(sys.stdout); h.setFormatter(logging.Formatter("%(message)s")); out.addHandler(h)
    out.setLevel(logging.INFO)

    def jl(p):
        return lambda: json.loads(Path(p).read_text())
    prov = dict(campaigns=[a.a2, a.a5])
    try:
        prov.update(open_json=[str(OPEN_JSON), _sha_file(OPEN_JSON)], bg_json=[str(BG_JSON), _sha_file(BG_JSON)])
    except Exception:           # noqa: BLE001  (a missing input is caught again, as a guard, inside sealed_run)
        pass
    rc = sealed_run(lambda: load_rows_from_campaigns(a.a2, a.a5), jl(OPEN_JSON), jl(BG_JSON), a.key_file, a.out,
                    out.info, prov)
    sys.exit(rc)


# ---- selftest (synthetic numbers only; no data file, no key of the study) ----------------------------------------------
def _synthetic(counts, n=N2_EXPECTED, seed=1):
    """rows with exact counts; ladder rungs nested (R07 c R06 c R04), fallback drawn independently of the ladder."""
    rng = np.random.default_rng(seed)
    rows = {}
    for f, (_, _, qs) in FAMILIES.items():
        perm = rng.permutation(n); rows[f] = {}
        for q in qs:
            x = np.zeros(n, bool)
            k = counts[f"{f}.{q}"]
            if q in LADDER:
                x[perm[:k]] = True
            else:
                x[rng.choice(n, k, replace=False)] = True
            rows[f][q] = x
    twins = {}
    for f, q in TWINS.items():
        full = np.zeros(n, bool); full[rng.choice(n, int(round(0.871 * counts[f"{f}.{q}"])), replace=False)] = True
        twins[f] = dict(fast=rows[f][q].copy(), full=full)
    open_res = {nm: dict(v2=f"{int(rows[nm.rsplit('.', 1)[0]][nm.rsplit('.', 1)[1]].sum())}/{n}",
                         p=fisher(int(rows[nm.rsplit('.', 1)[0]][nm.rsplit('.', 1)[1]].sum()), n, v[4], v[5]))
                for nm, v in OPEN.items()}
    zb = rng.normal(0, 1, N_BG)
    bg = dict(n_declared=N_DECL, entries={f"bg{i}": dict(z=float(z), p=float(2 * stats.norm.sf(abs(z))))
                                          for i, z in enumerate(zb)},
              global_partial=dict(n_available=N_BG, sum_z2=float(np.sum(zb ** 2)) * 1.3,
                                  sum_z2_naive=float(np.sum(zb ** 2)), sum_z2_v1_width_zero=float(np.sum(zb ** 2)) * 2))
    return rows, twins, open_res, bg


def _decrypt_selftest_only(f, key):
    return subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", f"file:{key}", "-in", str(f)],
                          capture_output=True, check=True).stdout


def _no_numbers(lines, safe=()):
    """True if no digit remains once entry/family names and the declared identifiers (path, sha, commit) are removed."""
    names = sorted([*SEALED, *OPEN, *FAMILIES, "chi2_41", "sha256", "n2", BG_JSON.name, OPEN_JSON.name, *safe],
                   key=len, reverse=True)
    for ln in lines:
        for s in names:
            ln = ln.replace(s, "")
        if any(c.isdigit() for c in ln):
            return False
    return True


def cmd_selftest_crash_child(a):     # child of the selftest: prints numbers on fd 1/2 and raises inside sealed_run
    def bad_loader():
        os.write(1, b"k2=37 n2=400\n"); os.write(2, b"p=0.0123\n")
        logging.getLogger("x").warning("z=2.5")
        raise ValueError("k2=37 n2=400 p=0.0123")
    sys.exit(sealed_run(bad_loader, dict, dict, a.key_file, a.out, lambda s: os.write(1, (s + "\n").encode())))


def cmd_selftest(a):    # synthetic numbers only; no data file is read
    import tempfile
    base = os.environ.get("QV2_SCRATCH", "/var/tmp/jdochoa")
    Path(base).mkdir(parents=True, exist_ok=True)
    good = {**{k: 2 * v[4] for k, v in OPEN.items()}, **{k: 2 * v[5] for k, v in SEALED.items()}}
    results = {}
    with tempfile.TemporaryDirectory(dir=base) as td:
        td = Path(td)
        key = td / "k.hex"; key.write_text(os.urandom(32).hex() + "\n"); key.chmod(0o600)

        def run(tag, rows, twins, open_res, bg, loader=None, key_file=key):
            lines = []
            out = td / f"{tag}.bin"
            rc = sealed_run(loader or (lambda: (rows, twins, dict(synthetic=True))), lambda: open_res, lambda: bg,
                            str(key_file), str(out), lines.append)
            return rc, lines, out

        # 1 all-PASS + encryption round trip
        r = _synthetic(good)
        rc, L, out = run("allpass", *r)
        sha = out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()
        back = json.loads(_decrypt_selftest_only(out, key)) if out.exists() else {}
        c, _ = git_commit()
        ok = (rc == 0 and all(x.endswith("PASS") for x in L if ":" in x and ("entry" in x or "coherence" in x
                                                                             or "global" in x))
              and "n-complete: yes" in L and f"sha256: {sha}" in L and _no_numbers(L, (str(out), sha, c))
              and set(back.get("entries", {})) == set(SEALED) and len(back.get("families", {})) == 3
              and all(np.isfinite(back["families"][f]["z"]) for f in FAMILIES)
              and back["global"]["frozen-naive"]["pass_"] and back["global"]["joint-block"]["pass_"]
              and abs(back["families"]["E200_1.5"]["corr"][0][2]) > 0.3)        # R04-R07 nested -> correlated
        results["all-PASS + round trip"] = ok
        results["stdout lines (all-PASS)"] = len(L) == 6 + 3 + 2 + 4
        # 2 one-FAIL (E500_3.R07: 20/400 against 48/200)
        r = _synthetic({**good, "E500_3.R07": 20})
        rc, L, out = run("onefail", *r)
        fails = [x for x in L if x.startswith("sealed entry") and x.endswith("FAIL")]
        results["one-FAIL"] = rc == 0 and fails == ["sealed entry E500_3.R07: FAIL"] and \
            _no_numbers(L, (str(out), hashlib.sha256(out.read_bytes()).hexdigest(), c))
        # 3 n2 guard: 399 rows, and n2 = 0
        for tag, n in (("n2=399", 399), ("n2=0", 0)):
            rows, twins, open_res, bg = _synthetic(good)
            rows["E200_2"]["R07"] = rows["E200_2"]["R07"][:n]
            rc, L, out = run(f"guard{n}", rows, twins, open_res, bg)
            results[f"n2 guard ({tag})"] = (rc == 3 and L[0] == "n-complete: no" and "n2 guard" in L[1]
                                            and not out.exists() and _no_numbers(L))
        rows, twins, open_res, bg = _synthetic(good)
        twins["E200_1.5"]["full"] = twins["E200_1.5"]["full"][:200]
        rc, L, out = run("guardtwin", rows, twins, open_res, bg)
        results["n2 guard (twin)"] = rc == 3 and not out.exists() and _no_numbers(L)
        # incomplete inputs: missing open entry, background short, open recount mismatch
        rows, twins, open_res, bg = _synthetic(good)
        rc1, L1, _ = run("inc1", rows, twins, {k: v for k, v in open_res.items() if k != "E500_3.R04"}, bg)
        bg2 = json.loads(json.dumps(bg)); bg2["entries"].pop("bg0")
        rc2, L2, _ = run("inc2", rows, twins, open_res, bg2)
        op3 = json.loads(json.dumps(open_res)); op3["E200_2.R04"]["v2"] = "1/400"
        rc3, L3, _ = run("inc3", rows, twins, op3, bg)
        results["incomplete/inconsistent inputs"] = (rc1, rc2, rc3) == (3, 3, 3) and _no_numbers(L1 + L2 + L3)
        # 4 k = 0 (E200_2.FB3 0/400)
        r = _synthetic({**good, "E200_2.FB3": 0})
        rc, L, out = run("k0", *r)
        back = json.loads(_decrypt_selftest_only(out, key)) if out.exists() else {}
        fam = back.get("families", {}).get("E200_2", {})
        results["k = 0"] = (rc == 0 and "sealed entry E200_2.FB3: FAIL" in L and fam.get("k0_v2") == ["FB3"]
                            and np.isfinite(fam.get("z", np.nan)) and fam["cov_v2"][2][0] == 0.0
                            and abs(fam["ln_ratio"][2] - np.log((0.5 / 400) / (10 / 200))) < 1e-12)
        # 5 exception paths: in-process (loader raises with numbers in its message), in compute (bad background), and
        #   a child process that also writes numbers to fd 1 and fd 2 before raising (checks the fd-level silencing)
        rows, twins, open_res, bg = _synthetic(good)

        def bad():
            raise ValueError("k2=37 n2=400 p=0.0123")
        rc, L, out = run("crash1", rows, twins, open_res, bg, loader=bad)
        ok1 = rc == 2 and L == ["crashed: ValueError"]
        bg3 = json.loads(json.dumps(bg)); bg3["global_partial"]["sum_z2"] = "x"
        rc, L2, _ = run("crash2", rows, twins, open_res, bg3)
        ok2 = rc == 2 and len(L2) == 1 and L2[0].startswith("crashed: ") and _no_numbers(L2)
        ch = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "_selftest-crash-child",
                             "--key-file", str(key), "--out", str(td / "child.bin")], capture_output=True, text=True)
        ok3 = ch.returncode == 2 and ch.stdout == "crashed: ValueError\n" and ch.stderr == ""
        results["exception path (nothing numeric printed)"] = ok1 and ok2 and ok3
        # 6 key and out refusals
        rows, twins, open_res, bg = _synthetic(good)
        refused = []
        for kf in (QV2 / "no_such.key", QV2 / "data" / "sealed" / "no_such.key", "/nfs/cajuela/jdochoa/quirks_v2/k"):
            rc, L, out = run("keyref", rows, twins, open_res, bg, key_file=kf)
            refused.append(rc == 3 and "key file refused" in L[1] and not out.exists())
        k644 = td / "k644.hex"; k644.write_text(os.urandom(32).hex() + "\n"); k644.chmod(0o644)
        rc, L, out = run("key644", rows, twins, open_res, bg, key_file=k644)
        refused.append(rc == 3 and "readable by group" in L[1])
        kbad = td / "kbad"; kbad.write_bytes(os.urandom(32)); kbad.chmod(0o600)
        rc, L, out = run("keybin", rows, twins, open_res, bg, key_file=kbad)
        refused.append(rc == 3 and "hex" in L[1])
        L = []
        rc = sealed_run(lambda: (rows, twins, {}), lambda: open_res, lambda: bg, str(key),
                        str(QV2 / "phase2_exploration" / "outputs" / "no_such_sealed.bin"), L.append)
        refused.append(rc == 3 and "out path refused" in L[1])
        results["key/out path refusals"] = all(refused)
        # 7 nested-binomial covariance against a bootstrap of the synthetic rows (E200_1.5: R04, R06, R07, FB2)
        rows, _, _, _ = _synthetic(good)
        X = np.column_stack([rows["E200_1.5"][q] for q in FAMILIES["E200_1.5"][2]])
        fs = family_stats(X, FAMILIES["E200_1.5"][2], {q: V1[f"E200_1.5.{q}"] for q in FAMILIES["E200_1.5"][2]})
        rng = np.random.default_rng(7)
        bs = np.array([np.log(X[rng.integers(0, len(X), len(X))].mean(0)) for _ in range(4000)])
        Cb = np.cov(bs, rowvar=False); Ca = np.array(fs["cov_v2"])
        ladder = np.abs(Ca[:3, :3] / Cb[:3, :3] - 1) < 0.1          # nested R04, R06, R07 block (all entries)
        results["nested covariance vs bootstrap (10 %)"] = bool(np.all(ladder) and abs(Ca[3, 3] / Cb[3, 3] - 1) < 0.1)
    for k, v in results.items():
        log.info("selftest-sealed  %-42s %s", k, "OK" if v else "BROKEN")
    log.info("selftest-sealed: %d/%d OK (synthetic numbers only; no data file and no study key read)",
             sum(results.values()), len(results))
    sys.exit(0 if all(results.values()) else 1)


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["open", "sealed", "selftest-sealed", "_selftest-crash-child"])
    ap.add_argument("--a2", default="p2-a-c1-siga2")
    ap.add_argument("--a5", default="p2-a-c1-siga5")
    ap.add_argument("--key-file")
    ap.add_argument("--out")
    a = ap.parse_args()
    {"open": cmd_open, "sealed": cmd_sealed, "selftest-sealed": cmd_selftest,
     "_selftest-crash-child": cmd_selftest_crash_child}[a.mode](a)


if __name__ == "__main__":
    main()
