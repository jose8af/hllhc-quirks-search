#!/usr/bin/env python3
"""Stop-rule checkpoint 1: CPU, unit costs and node utilisation from the job markers (read-only, stdlib only).

Reads every ledger/markers/<campaign>/**/<job>.marker (JSON Lines), skips _driver/. Counts CPU of EVERY attempt
(done, failed, timeout, killed), unlike jobs.tsv, which keeps the last line only (tools/runner/qv2run/ledger.py:32)
and one row per output file. Lost attempts (power loss, 19 Nov 17:54:50) have no CPU in their marker; their wall
time up to the power loss is reported separately as an upper bound.

Usage: nice -n 19 python3 checkpoint1_ledger.py <markers_dir> <out.json>
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-5))
POWER_LOSS = datetime(2026, 11, 19, 17, 54, 50, tzinfo=TZ).timestamp()
DAY0 = datetime(2026, 11, 16, 0, 0, tzinfo=TZ).timestamp()
TERMINAL = {"done", "failed", "timeout", "oom", "killed", "corrupt", "verify_failed"}


def parse_marker(path):
    lines = []
    with open(path) as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                try:
                    lines.append(json.loads(ln))
                except json.JSONDecodeError:
                    lines.append({"status": "unparseable"})
    return lines


def attempts(lines):
    """Yield (status, node, t_start, t_end, cpu_s, wall_s, n_outputs) per attempt."""
    open_start = None
    open_node = None
    for d in lines:
        st = d.get("status")
        if st == "started":
            open_start = d.get("t_wrapper") or d.get("ts")
            open_node = d.get("node")
        elif st in TERMINAL:
            t_end = d.get("t_end") or d.get("ts")
            t0 = d.get("t_cmd_start") or d.get("t_wrapper") or open_start
            if t0 is None and d.get("wall_s") is not None and t_end is not None:
                t0 = t_end - d["wall_s"]
            yield (st, d.get("node") or open_node, t0, t_end, d.get("cpu_s"), d.get("wall_s"),
                   len(d.get("outputs") or []))
            open_start = None
        elif st == "lost":
            t0 = open_start
            t_end = min(d.get("ts") or POWER_LOSS, POWER_LOSS) if t0 and t0 < POWER_LOSS else d.get("ts")
            yield ("lost", d.get("node") or open_node, t0, t_end, None, None, 0)
            open_start = None
    if open_start is not None:
        yield ("running", open_node, open_start, None, None, None, 0)


def main(mdir, out):
    camp = defaultdict(lambda: defaultdict(float))
    intervals = []  # (node, t0, t1, cpu_s)
    for root, dirs, files in os.walk(mdir):
        if "_driver" in root.split(os.sep):
            continue
        for fn in files:
            if not fn.endswith(".marker"):
                continue
            rel = os.path.relpath(root, mdir).split(os.sep)[0]
            lines = parse_marker(os.path.join(root, fn))
            c = camp[rel]
            c["jobs"] += 1
            last = [d for d in lines if d.get("status") != "started"]
            last_st = last[-1].get("status") if last else "started"
            c["last_" + last_st] += 1
            if last and last[-1].get("cpu_s") is not None:
                c["cpu_last_s"] += last[-1]["cpu_s"]
            for st, node, t0, t1, cpu, wall, nout in attempts(lines):
                c["att_" + st] += 1
                if cpu is not None:
                    c["cpu_all_s"] += cpu
                if wall is not None:
                    c["wall_all_s"] += wall
                if st == "lost" and t0 and t1:
                    c["lost_wall_s"] += max(0.0, t1 - t0)
                if t0 and t1:
                    intervals.append((node or "?", t0, t1, cpu))
                    c["t_first"] = min(c["t_first"] or t0, t0)
                    c["t_last"] = max(c["t_last"], t1)
                if st == "done":
                    c["bytes"] += 0
    # per-day delivered slot-hours (wall overlap) and CPU-h per node
    day_slot = defaultdict(lambda: defaultdict(float))
    day_cpu = defaultdict(lambda: defaultdict(float))
    for node, t0, t1, cpu in intervals:
        if t1 <= t0:
            continue
        t = t0
        while t < t1:
            dstart = DAY0 + 86400 * int((t - DAY0) // 86400)
            seg_end = min(t1, dstart + 86400)
            day = datetime.fromtimestamp(dstart, TZ).strftime("%Y-%m-%d")
            day_slot[day][node] += (seg_end - t) / 3600
            if cpu is not None:
                day_cpu[day][node] += cpu * (seg_end - t) / (t1 - t0) / 3600
            t = seg_end
    res = {"campaigns": {}, "day_slot_h": {}, "day_cpu_h": {}}
    for k, v in sorted(camp.items()):
        d = dict(v)
        for key in ("t_first", "t_last"):
            if d.get(key):
                d[key] = datetime.fromtimestamp(d[key], TZ).isoformat()
        res["campaigns"][k] = d
    res["day_slot_h"] = {k: dict(v) for k, v in sorted(day_slot.items())}
    res["day_cpu_h"] = {k: dict(v) for k, v in sorted(day_cpu.items())}
    with open(out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
