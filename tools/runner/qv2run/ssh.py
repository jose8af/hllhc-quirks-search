"""SSH backend: dispatch campaign jobs to workers with `ssh -x`, per-node slots, resumable from markers.

Jobs run detached on the worker (setsid nohup), so neither a dropped connection nor the death of this driver
kills them. A restarted driver rebuilds its view from markers plus a liveness check (pid + boot id) per node.
"""
import json
import shlex
import subprocess
import sys
import time

from . import markers, nodes, paths
from .driver import DriverLock, write_state
from .fsops import write_atomic
from .ledger import job_states

DISPATCH_GRACE_S = 120  # a dispatched job must write its `started` line within this time
LIVENESS_EVERY_S = 30


def log(msg):
    sys.stdout.write(f"[ssh-driver {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    sys.stdout.flush()


def remote_cmd(camp, job):
    err = f"{paths.SCRATCH}/.locks/{job.id}.driver.err"
    inner = (f"{shlex.quote(str(paths.JOB_ENTRY))} --campaign {shlex.quote(str(camp.source))} "
             f"--job {shlex.quote(job.id)} --mechanism ssh")
    # Each command separately: a backgrounded `a && b && c &` list would keep ssh's channel open until the job ends.
    return (f"mkdir -p {paths.SCRATCH}/.locks || exit 1; cd {paths.SCRATCH} || exit 1; "
            f"setsid nohup nice -n 10 {inner} > {err} 2>&1 < /dev/null & echo dispatched")


def alive_on(node, recs):
    """recs: list of `started` records on this node. Returns set of job ids whose wrapper process is alive."""
    if not recs:
        return set()
    pids = ",".join(str(r["pid"]) for r in recs)
    cmd = f"cat /proc/sys/kernel/random/boot_id; ps -o pid=,args= -p {pids} || true"
    try:
        r = subprocess.run(nodes.SSH + [node, cmd], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None  # unknown: do not declare anything lost
    if r.returncode != 0:
        return None
    lines = r.stdout.splitlines()
    if not lines:
        return None
    boot = lines[0].strip()
    procs = {}
    for ln in lines[1:]:
        f = ln.strip().split(None, 1)
        if len(f) == 2:
            procs[int(f[0])] = f[1]
    out = set()
    for rec in recs:
        a = procs.get(int(rec["pid"]), "")
        if rec.get("boot_id", boot) == boot and rec["job_id"] in a and "qv2run" in a:
            out.add(rec["job_id"])
    return out


def launch(camp, node_list, max_per_node=None, retries=2, poll_s=5, dry_run=False):
    lock = DriverLock(camp).acquire()
    disp_path = camp.state_dir() / "ssh_dispatch.json"
    try:
        dispatched = json.loads(disp_path.read_text())
    except (OSError, json.JSONDecodeError):
        dispatched = {}
    try:
        info = nodes.check(node_list, log=log)
        caps = {}
        for n, i in info.items():
            c = i["cap"]
            if i.get("ours_argo"):
                log(f"node {n}: an Argo pod of ours runs there -> excluded (brief 5.3)")
                c = 0
            if max_per_node is not None:
                c = min(c, max_per_node)
            # our own running jobs of THIS campaign count against the slots below, not against the cap
            caps[n] = c + 0
        log(f"slots per node: {caps}")
        if sum(caps.values()) == 0:
            log("no capacity on any node; exiting")
            write_state(camp, backend="ssh", status="no_capacity", caps=caps)
            return 2
        disp_dirty = False
        extra_fail = {}  # dispatch failures per job (counted as retries)
        last_live = 0.0
        st = job_states(camp)  # full marker scan once; afterwards only active jobs are re-read (NFS read budget)
        watch_ids = set()
        while True:
            for jid in list(watch_ids) + list(dispatched):
                st[jid] = markers.state(markers.read(camp.marker_path(camp.by_id[jid])))
            watch_ids = {j for j, (s, _, _) in st.items() if s == "running"}
            now = time.time()
            # running jobs per node, with liveness check
            running = {}
            for jid, (s, last, _) in st.items():
                if s == "running":
                    running.setdefault(last.get("node"), []).append(last)
                    dispatched.pop(jid, None)
            if now - last_live >= LIVENESS_EVERY_S:
                last_live = now
                for n, recs in running.items():
                    alive = alive_on(n, recs)
                    if alive is None:
                        continue
                    for rec in recs:
                        if rec["job_id"] not in alive:
                            mp = camp.marker_path(camp.by_id[rec["job_id"]])
                            s2, l2, _ = markers.state(markers.read(mp))
                            if s2 == "running" and l2.get("pid") == rec["pid"]:
                                log(f"{rec['job_id']}: wrapper pid {rec['pid']} gone on {n} -> lost")
                                markers.append(mp, {"job_id": rec["job_id"], "campaign": camp.name,
                                                    "mechanism": "ssh", "node": n, "status": "lost",
                                                    "reason": "wrapper process not found (driver liveness check)"})
                            st[rec["job_id"]] = markers.state(markers.read(mp))
            # dispatched but not started yet
            for jid, d in list(dispatched.items()):
                if st[jid][0] != "pending" and st[jid][0] != "retryable":
                    dispatched.pop(jid)
                    disp_dirty = True
                elif now - d["t"] > DISPATCH_GRACE_S:
                    log(f"{jid}: no `started` line {DISPATCH_GRACE_S} s after dispatch to {d['node']}")
                    extra_fail[jid] = extra_fail.get(jid, 0) + 1
                    dispatched.pop(jid)
            busy = {n: 0 for n in caps}
            for jid, (s, last, _) in st.items():
                if s == "running" and last.get("node") in busy:
                    busy[last["node"]] += 1
            for jid, d in dispatched.items():
                busy[d["node"]] = busy.get(d["node"], 0) + 1
            # what is left
            todo, final_fail = [], []
            for j in camp.jobs:
                s, last, att = st[j.id]
                if j.id in dispatched or s in ("running", "done"):
                    continue
                if s == "failed":
                    final_fail.append(j.id)
                    continue
                n_retry = extra_fail.get(j.id, 0)
                if s == "retryable":  # only then is the marker re-read (NFS read budget)
                    n_retry += sum(1 for r in markers.read(camp.marker_path(j)) if r.get("status") in markers.RETRYABLE)
                if n_retry > retries:
                    final_fail.append(j.id)
                    continue
                todo.append(j)
            n_run = sum(busy.values())
            write_state(camp, backend="ssh", status="running", caps=caps, busy=busy, todo=len(todo),
                        failed=len(final_fail), done=sum(1 for s, _, _ in st.values() if s == "done"))
            if not todo and n_run == 0:
                ok = not final_fail
                log(f"campaign finished: {'all done' if ok else f'{len(final_fail)} failed: {final_fail[:10]}'}")
                write_state(camp, backend="ssh", status="finished", ok=ok, failed=final_fail, force=True)
                return 0 if ok else 2
            for j in todo:
                free = [n for n in caps if busy.get(n, 0) < caps[n]]
                if not free:
                    break
                n = min(free, key=lambda x: busy.get(x, 0) / max(caps[x], 1))
                if dry_run:
                    log(f"would dispatch {j.id} -> {n}")
                    continue
                try:
                    r = subprocess.run(nodes.SSH + [n, remote_cmd(camp, j)], capture_output=True, text=True,
                                       timeout=60)
                    okd = r.returncode == 0 and "dispatched" in r.stdout
                except (OSError, subprocess.TimeoutExpired) as e:
                    okd, r = False, e
                if not okd:
                    log(f"dispatch {j.id} -> {n} failed: {getattr(r, 'stderr', r)}")
                    extra_fail[j.id] = extra_fail.get(j.id, 0) + 1
                    continue
                dispatched[j.id] = {"node": n, "t": time.time()}
                busy[n] = busy.get(n, 0) + 1
                log(f"dispatched {j.id} -> {n}")
                disp_dirty = True
            if disp_dirty:
                write_atomic(disp_path, json.dumps(dispatched))
                disp_dirty = False
            if dry_run:
                return 0
            time.sleep(poll_s)
    finally:
        try:
            write_atomic(disp_path, json.dumps(dispatched))
        except OSError:
            pass
        lock.release()
