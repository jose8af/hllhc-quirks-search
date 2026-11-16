"""c1_s3_index.py -- STAGE3_INDEX.json for the C1 Stage-3 chunks (channel (i), Rosalie, 2026-11-16).

Stdlib only (light; einstein is fine).  Reads the `done` markers of campaign p2-a-c1-s3 (a file without a done marker
does not exist) and writes phase2_exploration/outputs/c1_s3/STAGE3_INDEX.json in the layout acts/stage4/code/s4sig.py
reads: points["p2/F_m<m>/L<lam>_BM"]["chunks"] = [{"file": <absolute path>, "sha256", "bytes"}], in chunk order.
Usage: python3 -I c1_s3_index.py
"""
import json
import logging
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
MARK = QV2 / "ledger" / "markers" / "p2-a-c1-s3"
OUT = HERE.parent / "outputs" / "c1_s3" / "STAGE3_INDEX.json"
PAT = re.compile(r"^p2_F_m(\d+)_L([0-9.]+)_BM_c(\d+)\.npz$")
log = logging.getLogger("c1_s3_index")


def build(require_complete=True):
    """Index dict from the done markers; with require_complete, refuse unless every job of the campaign is done."""
    camp = json.loads((QV2.parents[1] / "tools" / "runner" / "campaigns" / "p2-a-c1-s3.json").read_text())
    pts = {}
    n_done = 0
    for p in sorted(MARK.glob("*/*.marker")):
        done = None
        for line in p.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("status") == "done":
                done = d
        if not done:
            continue
        n_done += 1
        for o in done["outputs"]:
            mt = PAT.match(o["name"])
            if mt:
                key = f"p2/F_m{mt.group(1)}/L{float(mt.group(2)):g}_BM"
                pts.setdefault(key, []).append((int(mt.group(3)), dict(file=o["path"], sha256=o["sha256"],
                                                                         bytes=o["bytes"], job=done["job_id"])))
    idx = dict(meta=dict(created_by="phase2_exploration/src/c1_s3_index.py", note="C1 v2 Stage-3 chunks (campaign "
                         "p2-a-c1-s3), absolute paths on cajuela; only chunks with a done marker"),
               points={k: dict(campaign="p2", spin="F", cfg="BM", chunks=[c for _, c in sorted(v, key=lambda t: t[0])])
                       for k, v in pts.items()})
    if require_complete and n_done != len(camp["jobs"]):
        raise SystemExit(f"p2-a-c1-s3: {n_done} of {len(camp['jobs'])} jobs done; the index needs all of them")
    return idx


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    idx = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.part")
    tmp.write_text(json.dumps(idx, indent=1) + "\n")
    tmp.replace(OUT)
    log.info("wrote %s: %s", OUT, {k: len(v["chunks"]) for k, v in idx["points"].items()})


if __name__ == "__main__":
    main()
