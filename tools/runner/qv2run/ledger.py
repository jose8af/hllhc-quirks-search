"""Ledger rebuilt from markers (one writer), status from markers, and output re-verification."""
import os
import sys
from collections import Counter
from pathlib import Path

from . import markers, paths
from .fsops import write_atomic
from .wrapper import outputs_intact

COLUMNS = ("job_id", "campaign", "mechanism", "node", "status", "cpu_s", "max_rss_mb", "wall_s", "output", "sha256",
           "bytes", "attempts", "end_time")


def iter_marker_files(ledger_dir):
    ledger_dir = Path(ledger_dir)
    if not ledger_dir.is_dir():
        return
    for camp in sorted(p for p in ledger_dir.iterdir() if p.is_dir()):
        for shard in sorted(p for p in camp.iterdir() if p.is_dir() and not p.name.startswith("_")):
            for m in sorted(shard.glob("*.marker")):
                yield camp.name, m


def rows_from_marker(camp_name, path):
    recs = markers.read(path)
    st, last, attempts = markers.state(recs)
    job_id = path.name[: -len(".marker")]
    if last is None:
        return []
    base = {"job_id": job_id, "campaign": camp_name, "mechanism": last.get("mechanism", ""),
            "node": last.get("node", ""), "status": last.get("status", ""), "cpu_s": last.get("cpu_s", ""),
            "max_rss_mb": last.get("max_rss_mb", ""), "wall_s": last.get("wall_s", ""), "attempts": attempts,
            "end_time": last.get("t", "")}
    outs = last.get("outputs") or [{}]
    return [dict(base, output=o.get("name", ""), sha256=o.get("sha256", ""), bytes=o.get("bytes", ""))
            for o in outs]


def rebuild(ledger_dir=paths.LEDGER_MARKERS, out=paths.JOBS_TSV):
    lines = ["\t".join(COLUMNS)]
    n = 0
    for camp_name, m in iter_marker_files(ledger_dir):
        for r in rows_from_marker(camp_name, m):
            lines.append("\t".join(str(r[c]) for c in COLUMNS))
            n += 1
    write_atomic(out, "\n".join(lines) + "\n")
    return n


def job_states(camp):
    """{job_id: (state, last_record, attempts)} from markers only."""
    return {j.id: markers.state(markers.read(camp.marker_path(j))) for j in camp.jobs}


def summary(camp):
    st = job_states(camp)
    return Counter(s for s, _, _ in st.values()), st


def liveness(camp, st):
    """For jobs whose marker says running: {job_id: True/False/None} (None = could not check)."""
    from . import ssh as ssh_mod
    res, by_node = {}, {}
    for jid, (s, last, _) in st.items():
        if s != "running":
            continue
        if last.get("mechanism") == "argo" and last.get("pod"):
            import subprocess
            r = subprocess.run(["kubectl", "-n", "argo", "get", "pod", last["pod"], "-o",
                                "jsonpath={.status.phase}"], capture_output=True, text=True, timeout=60)
            res[jid] = (r.stdout.strip() in ("Pending", "Running")) if r.returncode in (0, 1) else None
        else:
            by_node.setdefault(last.get("node"), []).append(last)
    for node, recs in by_node.items():
        alive = ssh_mod.alive_on(node, recs)
        for r in recs:
            res[r["job_id"]] = None if alive is None else (r["job_id"] in alive)
    return res


def print_status(camp, verbose=False, out=sys.stdout, live=False):
    cnt, st = summary(camp)
    if live:
        lv = liveness(camp, st)
        dead = [j for j, v in lv.items() if v is False]
        cnt["running"] -= len(dead)
        cnt["dead"] = len(dead)
        for j in dead:
            st[j] = ("dead", st[j][1], st[j][2])
    tot = len(camp.jobs)
    out.write(f"campaign {camp.name}: {tot} jobs | done {cnt['done']} | failed {cnt['failed']} | "
              f"running {cnt['running']} | retryable {cnt['retryable']} | pending {cnt['pending']}"
              + (f" | dead {cnt['dead']} (resume the driver to retry them)" if live else "") + "\n")
    if verbose:
        for jid, (s, last, att) in st.items():
            if s != "done" or verbose > 1:
                out.write(f"  {jid}\t{s}\t{(last or {}).get('status', '')}\tattempts={att}\t"
                          f"node={(last or {}).get('node', '')}\n")
    return cnt


def verify(camp, out=sys.stdout):
    """Re-hash every output of every done job against its marker. Returns list of (job_id, reason) failures."""
    bad = []
    for j in camp.jobs:
        s, last, _ = markers.state(markers.read(camp.marker_path(j)))
        if s != "done":
            continue
        ok, why = outputs_intact(camp, j, last, rehash=True)
        if not ok:
            bad.append((j.id, why))
            markers.append(camp.marker_path(j), {"job_id": j.id, "campaign": camp.name, "status": "corrupt",
                                                  "reason": why, "mechanism": "verify",
                                                  "node": os.uname().nodename})
            out.write(f"CORRUPT {j.id}: {why}\n")
    out.write(f"verify {camp.name}: {len(bad)} corrupt output(s)\n")
    return bad
