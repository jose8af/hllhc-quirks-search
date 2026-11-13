"""Per-job markers: JSON Lines on /home, one event per line, appended with O_APPEND + fsync (one writer per job).

The last terminal line decides the job state. `started` without a later line = running (or lost, if the process
is gone). A job without a marker is pending. Completeness is judged only from these files, never from cajuela.
"""
import json
import os
import time

from .fsops import makedirs_final

TERMINAL_OK = ("done",)
TERMINAL_FAIL = ("failed", "timeout", "oom", "verify_failed", "setup_error")
RETRYABLE = ("killed", "lost", "corrupt")  # infrastructure-like: the runner may retry (Argo OnError analogue)


def read(path):
    try:
        with open(path) as f:
            text = f.read()
    except FileNotFoundError:
        return []
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                out.append({"status": "unparseable", "raw": line})
    return out


def append(path, record):
    """Append one JSON line with O_APPEND + fsync (one writer per job at a time).

    Brief/orchestrator rule (2026-11-13): /home/users is a `sync` NFS export on a rotational disk, so per-job writes
    there are kept to this single small file and to the fewest metadata operations: no .part/rename per event (the
    first event creates the file; later events only append). A torn last line after a crash is tolerated by read().
    """
    record = dict(record)
    record.setdefault("t", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    record.setdefault("ts", round(time.time(), 3))
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        makedirs_final(d)
    line = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        size = os.fstat(fd).st_size
        if size and os.pread(fd, 1, size - 1) != b"\n":
            line = b"\n" + line  # isolate a torn line left by a crash
        os.write(fd, line)
        os.fsync(fd)
    finally:
        os.close(fd)
    return record


def state(records):
    """Return (state, last_record, n_attempts). state in pending/running/done/failed/retryable."""
    records = [r for r in records if r.get("status") != "unparseable"]
    if not records:
        return "pending", None, 0
    attempts = sum(1 for r in records if r.get("status") == "started")
    last = records[-1]
    s = last.get("status")
    if s == "started":
        return "running", last, attempts
    if s in TERMINAL_OK:
        return "done", last, attempts
    if s in TERMINAL_FAIL:
        return "failed", last, attempts
    return "retryable", last, attempts


def last_done(records):
    for r in reversed(records):
        if r.get("status") == "done":
            return r
    return None
