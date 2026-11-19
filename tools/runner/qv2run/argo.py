"""Argo backend: workflows generated from a campaign file, following brief 5.3 exactly.

Only objects named jdochoa-qv2-* and labelled owner=jdochoa,study=quirks-v2 are created, listed or deleted.
"""
import json
import math
import random
import string
import os
import subprocess
import sys
import time

os.environ.setdefault("KUBECONFIG", "/etc/kubernetes/student.conf")  # unset in non-interactive ssh

from . import campaign, markers, nodes, paths
from .driver import DriverLock, write_state
from .ledger import job_states

MAX_STEPS = 500
MAX_PARALLELISM = 12
LABELS = dict(paths.OWNER_LABELS)
SEL = "owner=jdochoa,study=quirks-v2"


def log(msg):
    sys.stdout.write(f"[argo-driver {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    sys.stdout.flush()


def mem_str(mb):
    return f"{int(math.ceil(mb))}Mi"


def chunks(camp):
    """Deterministic chunking of the full job list: chunk k = jobs[500k : 500(k+1)]."""
    return [camp.jobs[i:i + MAX_STEPS] for i in range(0, len(camp.jobs), MAX_STEPS)]


def render(camp, jobs, chunk, parallelism, node=None, allowed_nodes=None, suffix=None):
    if not 1 <= parallelism <= MAX_PARALLELISM:
        raise ValueError(f"parallelism {parallelism} outside 1..{MAX_PARALLELISM}")
    if len(jobs) > MAX_STEPS:
        raise ValueError(f"{len(jobs)} steps > {MAX_STEPS}")
    suffix = suffix or "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    tag = f"-{node}" if node else ""
    name = f"jdochoa-qv2-{camp.name}-c{chunk}{tag}-{suffix}"[:63].rstrip("-")
    labels = dict(LABELS, **{"qv2-campaign": camp.name, "qv2-chunk": str(chunk)})
    if node:
        labels["qv2-node"] = node
    # One container template per resource class: k8s quantities cannot be templated (argo lint rejects them).
    classes = {}
    for j in jobs:
        classes.setdefault((mem_str(j.max_rss_mb), mem_str(1.5 * j.max_rss_mb)), []).append(j.id)
    entry = (f"umask 022 && exec {paths.JOB_ENTRY} --campaign {camp.source} "
             "--job {{inputs.parameters.job}} --mechanism argo")
    tmpls, steps = [], []
    for i, ((mreq, mlim), ids) in enumerate(sorted(classes.items())):
        t = {
            "name": f"job-r{i}",
            "inputs": {"parameters": [{"name": "job"}]},
            "activeDeadlineSeconds": 2400,
            "retryStrategy": {"limit": 2, "retryPolicy": "OnError"},
            "metadata": {"labels": dict(labels)},
            "container": {
                "image": paths.IMAGE,
                "imagePullPolicy": "IfNotPresent",
                "command": ["nice", "-n", "10", "bash", "-c"],
                "args": [entry],
                "env": [{"name": "QV2_NODE", "valueFrom": {"fieldRef": {"fieldPath": "spec.nodeName"}}},
                        {"name": "ARGO_WORKFLOW_NAME", "value": "{{workflow.name}}"},
                        {"name": "HOME", "value": "/home/users/jdochoa"}],
                "resources": {"requests": {"cpu": "1", "memory": mreq}, "limits": {"memory": mlim}},
                "volumeMounts": [{"name": "home", "mountPath": "/home/users/jdochoa"},
                                 {"name": "data", "mountPath": "/nfs/cajuela/jdochoa/quirks_v2"},
                                 {"name": "scratch", "mountPath": "/home/scratch/jdochoa"}],
            },
        }
        if node:
            t["nodeSelector"] = {"kubernetes.io/hostname": node}
        elif allowed_nodes:
            t["affinity"] = {"nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [{"matchExpressions": [{"key": "kubernetes.io/hostname", "operator": "In",
                                                             "values": sorted(allowed_nodes)}]}]}}}
        tmpls.append(t)
        steps.append({"name": f"run-r{i}", "template": f"job-r{i}",
                      "arguments": {"parameters": [{"name": "job", "value": "{{item}}"}]}, "withItems": ids})
    wf = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Workflow",
        "metadata": {"name": name, "namespace": "argo", "labels": labels},
        "spec": {
            "entrypoint": "main",
            "parallelism": parallelism,
            "podGC": {"strategy": "OnPodSuccess"},
            "ttlStrategy": {"secondsAfterCompletion": 86400},
            "podMetadata": {"labels": dict(labels)},
            "securityContext": {"runAsUser": paths.UID, "runAsGroup": paths.GID},
            "volumes": [
                {"name": "home", "nfs": {"server": paths.NFS_SERVER, "path": "/home/users/jdochoa"}},
                {"name": "data", "nfs": {"server": paths.NFS_SERVER, "path": "/mnt/cajuela/jdochoa/quirks_v2"}},
                {"name": "scratch", "hostPath": {"path": "/home/scratch/jdochoa", "type": "Directory"}},
            ],
            "templates": [{"name": "main", "steps": [steps]}] + tmpls,
        },
    }
    return wf


def plan(camp, node_list, max_parallel=None, expected_hours=None, log=log):
    """Decide pooled vs pinned mode and parallelism from the clock and a node check."""
    tc = nodes.time_cap(expected_hours=camp.expected_hours if expected_hours is None else expected_hours)
    info = nodes.check(node_list, log=log)
    caps = {}
    for n, i in info.items():
        c = i["cap"]
        if i.get("ours_ssh"):
            log(f"node {n}: SSH jobs of ours run there -> excluded (brief 5.3)")
            c = 0
        if c > 0:
            caps[n] = c
    total = min(tc, sum(caps.values()), MAX_PARALLELISM)
    if max_parallel:
        total = min(total, max_parallel)
    log(f"time cap {tc}; node caps {caps}; parallelism {total}")
    if total <= 0:
        return {"mode": "none", "parallelism": 0, "caps": caps, "time_cap": tc}
    uniform = len(set(caps.values())) == 1 and (max_parallel is None or max_parallel >= sum(caps.values()))
    if uniform or len(caps) == 1:
        return {"mode": "pooled", "parallelism": total, "nodes": sorted(caps), "caps": caps, "time_cap": tc}
    # pinned: scale per-node caps down proportionally if the total cap binds
    scale = total / sum(caps.values())
    pinned = {n: max(1, int(c * scale)) for n, c in caps.items()}
    return {"mode": "pinned", "parallelism": sum(pinned.values()), "pinned": pinned, "caps": caps, "time_cap": tc}


def kubectl_json(args):
    r = subprocess.run(["kubectl", "-n", "argo"] + args + ["-o", "json"], capture_output=True, text=True,
                       timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"kubectl {' '.join(args)} failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def our_workflows(camp=None, chunk=None):
    sel = SEL + (f",qv2-campaign={camp.name}" if camp else "") + (f",qv2-chunk={chunk}" if chunk is not None else "")
    items = kubectl_json(["get", "workflows", "-l", sel]).get("items", [])
    return [w for w in items if w["metadata"]["name"].startswith("jdochoa-qv2-")]


def wf_phase(w):
    return (w.get("status") or {}).get("phase") or "Pending"


def submit(wf, path):
    path.write_text(json.dumps(wf, indent=1))
    r = subprocess.run(["argo", "submit", "-n", "argo", str(path), "-o", "name"], capture_output=True, text=True,
                       timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"argo submit failed: {r.stderr.strip()}")
    return r.stdout.strip()


def wait(names):
    for n in names:
        subprocess.run(["argo", "wait", "-n", "argo", n], capture_output=True, text=True)


def delete(name):
    if not name.startswith("jdochoa-qv2-"):
        raise ValueError(f"refusing to delete {name}")
    subprocess.run(["argo", "delete", "-n", "argo", name], capture_output=True, text=True, timeout=120)


def reconcile(camp, cjobs):
    """After our workflows of this campaign end: a job whose marker still says `started` died with its pod.

    Kubernetes kills the whole container on OOM (wrapper included), so the wrapper cannot write the line itself:
    OOMKilled -> terminal `oom` (the request was wrong; never retried), any other pod end -> `lost` (retryable).
    """
    wfs = our_workflows(camp)
    if any(wf_phase(w) in ("Pending", "Running") for w in wfs):
        return
    pod_end = {}
    for w in wfs:
        for n in (w.get("status") or {}).get("nodes", {}).values():
            if n.get("type") != "Pod":
                continue
            jid = next((p.get("value") for p in (n.get("inputs") or {}).get("parameters", []) if p["name"] == "job"),
                       None)
            if jid:
                pod_end.setdefault(jid, []).append((n.get("finishedAt") or "", n.get("phase"), n.get("message", "")))
    st = job_states(camp)
    for j in cjobs:
        s, last, _ = st[j.id]
        if s != "running" or last.get("mechanism") != "argo":
            continue
        ends = sorted(pod_end.get(j.id, []))
        msg = ends[-1][2] if ends else ""
        status = "oom" if "OOMKilled" in msg else "lost"
        markers.append(camp.marker_path(j), {"job_id": j.id, "campaign": camp.name, "mechanism": "argo",
                                             "node": last.get("node", ""), "status": status,
                                             "reason": msg or "no active workflow; pod gone without end line",
                                             "mem_limit_mb": last.get("mem_limit_mb")})
        log(f"{j.id}: marked {status} ({msg or 'pod gone'})")
        node = last.get("node")
        if node in paths.WORKERS:  # the wrapper died with its container: remove its scratch dir on that node
            try:
                subprocess.run(nodes.SSH + [node, f"rm -rf {paths.SCRATCH}/{j.id}"], capture_output=True,
                               timeout=60)
            except (OSError, subprocess.TimeoutExpired):
                log(f"{j.id}: could not clean scratch on {node}")


def launch(camp, node_list, max_parallel=None, keep=False, resubmit_rounds=1):
    """Resumable driver: for each chunk, wait for our running workflow or submit one for the not-done jobs."""
    if any(j.timeout_exception for j in camp.jobs):
        raise campaign.CampaignError("timeout_exception is allowed on the ssh mechanism only")
    lock = DriverLock(camp).acquire()
    try:
        for k, cjobs in enumerate(chunks(camp)):
            for rnd in range(resubmit_rounds + 1):
                st = job_states(camp)
                active = [w for w in our_workflows(camp, k) if wf_phase(w) in ("Pending", "Running")]
                if active:
                    names = [w["metadata"]["name"] for w in active]
                    log(f"chunk {k}: waiting for running workflow(s) {names}")
                    write_state(camp, backend="argo", status="running", chunk=k, workflows=names)
                    wait(names)
                reconcile(camp, cjobs)
                st = job_states(camp)
                todo =[j for j in cjobs if st[j.id][0] in ("pending", "retryable")]
                failed = [j.id for j in cjobs if st[j.id][0] == "failed"]
                if not todo:
                    break
                if rnd == resubmit_rounds and active:
                    break
                p = plan(camp, node_list, max_parallel)
                if p["mode"] == "none":
                    log("no capacity; stopping")
                    write_state(camp, backend="argo", status="no_capacity", force=True)
                    return 2
                names = []
                if p["mode"] == "pooled":
                    wf = render(camp, todo, k, p["parallelism"], allowed_nodes=p["nodes"])
                    names.append(submit(wf, camp.state_dir() / f"wf_c{k}.json"))
                else:
                    tot = sum(p["pinned"].values())
                    start = 0
                    nl = sorted(p["pinned"])
                    for i, n in enumerate(nl):
                        cnt = len(todo) - start if i == len(nl) - 1 else round(len(todo) * p["pinned"][n] / tot)
                        part = todo[start:start + cnt]
                        start += cnt
                        if part:
                            wf = render(camp, part, k, p["pinned"][n], node=n)
                            names.append(submit(wf, camp.state_dir() / f"wf_c{k}_{n}.json"))
                log(f"chunk {k} round {rnd}: submitted {names} for {len(todo)} jobs ({len(failed)} already failed)")
                write_state(camp, backend="argo", status="running", chunk=k, workflows=names, plan=p)
                wait(names)
                for w in our_workflows(camp, k):
                    if wf_phase(w) == "Succeeded" and not keep:
                        delete(w["metadata"]["name"])
        for cjobs in chunks(camp):
            reconcile(camp, cjobs)
        st = job_states(camp)
        bad = [j for j, (s, _, _) in st.items() if s != "done"]
        write_state(camp, backend="argo", status="finished", ok=not bad, failed=bad, force=True)
        log(f"campaign finished: {'all done' if not bad else f'{len(bad)} not done: {bad[:10]}'}")
        return 0 if not bad else 2
    finally:
        lock.release()
