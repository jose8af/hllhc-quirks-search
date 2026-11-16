"""c1_sig_job.py -- one Stage-4 signal job of the C1 reproduction (channel (i), Rosalie, 2026-11-16).

Runs v1's acts.stage4.run_g1b.run_signal_job unchanged with the frozen configuration (road 0.15, T_seed 4):
  a2  fast path (numpy quirk digitisation; one PU-200 event per row, row-major over the given Lambda), as v1 at
      E 200 with 1.5 and 2 keV
  a5  full chain (quirk hits through ACTS digitisation + CKF, PU 200), as v1 at E 500 / 3 keV and for the full-chain
      "twins" of the two E 200 points (COM C1-e)
Stage-3 points come from the v2 C1 Stage-3 index: QV2_S3_DATA = phase2_exploration/outputs/c1_s3 (STAGE3_INDEX.json
with absolute file paths); run_g1b.index() is pointed to it here (v1 hard-codes data/sim_stage3).
Rows: all |eta| < 2.5 rows of both splits (400 per point; a2 status1 = False as v1 A2, a5 status1 = True as v1 A5), cut
into chunks of --size.  Job seed = hash_seed("qv2|c1.sig.<kind>|<point>|<chunk>"); the per-row PU / smearing / top-up
seeds are v1's hseed(spin, m, row) rules.  Probe-row exclusion: QV2_ALLOW_NO_F1R=1 (the v1 file is lost and its rows
refer to v1's Stage-2 rows, which do not exist in the regenerated sample; logged decision).

BLINDING: the output holds per-rung signal pass bits (sig.eff*) for all 43 rungs.  This script prints and logs no
count; nobody in channel (i) opens these files except through c1_compare.py, which reads only R04 and R06.
Output in $QV2_OUT_DIR: <id>.npz.
"""
import argparse
import json
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
log = logging.getLogger("c1_sig_job")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--kind", choices=["a2", "a5"], required=True)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--lams", required=True, help="comma list (a2) or one value (a5)")
    ap.add_argument("--chunk", type=int, required=True)
    ap.add_argument("--size", type=int, required=True)
    a = ap.parse_args()
    work = Path.cwd() / "s4work"
    (work / "prod").mkdir(parents=True, exist_ok=True)
    os.environ["QV2_S4_DATA"] = str(work)
    os.environ.setdefault("QV2_S3_DATA", str(HERE.parent / "outputs" / "c1_s3"))
    os.environ["QV2_ALLOW_NO_F1R"] = "1"
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    sys.path.insert(0, str(QV2))
    os.chdir(QV2)
    from acts.stage4 import run_stage4 as RS
    from acts.stage4 import run_g1b as G
    from acts.stage4.code import s4sig as S
    s3 = Path(os.environ["QV2_S3_DATA"])
    idx = json.loads((s3 / "STAGE3_INDEX.json").read_text())
    G.index = lambda: idx
    fz = RS.frozen_inputs()
    if fz is None or fz.get("wp_rule_sha256") != RS.sha256_file(RS.HERE / "WP_RULE.md"):
        raise SystemExit("frozen_inputs / WP_RULE.md mismatch")
    lams = [float(x) for x in a.lams.split(",")]
    key0 = S.point_key("F", a.m, lams[0])
    P = S.Point(key0, idx)
    rows_all = P.rows(template=False, counting=True, status1=(a.kind == "a5"))
    rows = rows_all[a.chunk * a.size:(a.chunk + 1) * a.size]
    if not rows:
        raise SystemExit("empty chunk")
    seed = RS.hash_seed(f"qv2|c1.sig.{a.kind}|{key0 if a.kind == 'a5' else 'F' + str(a.m)}|{a.chunk}")
    job = dict(id=a.id, campaign="C1", sample=a.kind.upper(), kind=a.kind, chunk=a.chunk, n_events=len(rows), roads=1,
               rho=1, seed=seed, dump_events=len(rows) if a.kind == "a5" else 0, est_s=0.0, mem_gb=1.5, rows=rows,
               out=f"{a.id}.npz", requires="G1b", qv2_stream="c1.sig")
    if a.kind == "a2":
        job.update(spin="F", m=a.m, lams=lams)
    else:
        job.update(point=key0)
    log.info("signal job %s kind %s point(s) %s: %d rows (chunk %d of size %d), seed %d", a.id, a.kind,
             a.lams, len(rows), a.chunk, a.size, seed)
    res = G.run_signal_job(job)
    log.info("finished: wall %.0f s, chain %.0f s, %d trials, %d bytes, V4-1 %s", res["wall"], res["t_chain"],
             res["n_trials"], res["bytes"], res["v41_pass"])
    outd = Path(os.environ.get("QV2_OUT_DIR", "."))
    shutil.move(str(RS.out_path(job)), str(outd / f"{a.id}.npz"))
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
