"""Pre-launch node checks shared by both backends (brief 5.1, 5.3): load, `who`, our own jobs on each worker."""
import datetime as dt
import json
import subprocess

from . import paths

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Guayaquil")
except Exception:  # noqa: BLE001 - no tzdata: Ecuador is UTC-5 all year (no DST)
    TZ = dt.timezone(dt.timedelta(hours=-5))

SSH = ["ssh", "-x", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]
PROBE = ("cat /proc/loadavg; echo '--who'; who; echo '--ours'; "
         "pgrep -u $(id -u) -f '[q]v2run job .*--mechanism ssh' | wc -l")


def is_graphical(who_lines):
    """A graphical session: seat0, an X display ':N', or a wayland/greeter login screen."""
    for ln in who_lines:
        f = ln.split()
        if len(f) < 2:
            continue
        if f[1].startswith("seat") or f[1].startswith(":") or "(:" in ln or "login screen" in ln:
            return True
    return False


def parse_probe(text):
    load1, who, ours, sec = 0.0, [], 0, "load"
    for ln in text.splitlines():
        if ln == "--who":
            sec = "who"
            continue
        if ln == "--ours":
            sec = "ours"
            continue
        if sec == "load" and ln.strip():
            load1 = float(ln.split()[0])
        elif sec == "who" and ln.strip():
            who.append(ln)
        elif sec == "ours" and ln.strip():
            ours = int(ln.strip())
    return load1, who, ours


def node_cap(load1, graphical, ours, base=4, our_running_here=0):
    """Jobs we may run on a node now: 4 (3 with a graphical session) minus foreign load.

    Foreign load = load1 minus our own running jobs there (ours from pgrep; Argo pods of ours via
    `our_running_here`), rounded. Never negative.
    """
    cap = 3 if graphical else base
    foreign = max(0.0, load1 - ours - our_running_here)
    return max(0, min(cap, base - int(round(foreign))))


def probe(node, timeout=30):
    r = subprocess.run(SSH + [node, PROBE], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"probe {node} failed rc={r.returncode}: {r.stderr.strip()}")
    load1, who, ours = parse_probe(r.stdout)
    return {"node": node, "load1": load1, "who": who, "graphical": is_graphical(who), "ours_ssh": ours}


def our_argo_pods_by_node():
    """Running pods of ours (label owner=jdochoa,study=quirks-v2) per node. {} if kubectl fails."""
    try:
        r = subprocess.run(["kubectl", "get", "pods", "-n", "argo", "-l", "owner=jdochoa,study=quirks-v2",
                            "--field-selector=status.phase=Running", "-o", "json"],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            return None
        out = {}
        for it in json.loads(r.stdout).get("items", []):
            n = it.get("spec", {}).get("nodeName")
            if n:
                out[n] = out.get(n, 0) + 1
        return out
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def time_cap(now=None, expected_hours=0.0):
    """12, or 9 if [now, now + expected_hours] touches a weekday 08:00-19:00 America/Guayaquil."""
    now = (now or dt.datetime.now(TZ)).astimezone(TZ)
    end = now + dt.timedelta(hours=max(0.0, expected_hours))
    t = now
    while True:  # sample every 5 minutes plus the end point
        if t.weekday() < 5 and 8 <= t.hour < 19:
            return 9
        if t >= end:
            return 12
        t = min(end, t + dt.timedelta(minutes=5))


def check(nodes, log=print):
    """Probe each node; return {node: info with 'cap'}. A node that cannot be probed gets cap 0."""
    argo = our_argo_pods_by_node() or {}
    res = {}
    for n in nodes:
        try:
            info = probe(n)
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as e:
            log(f"node {n}: probe failed ({e}); cap 0")
            res[n] = {"node": n, "cap": 0, "error": str(e)}
            continue
        info["ours_argo"] = argo.get(n, 0)
        info["cap"] = node_cap(info["load1"], info["graphical"], info["ours_ssh"], our_running_here=info["ours_argo"])
        log(f"node {n}: load1 {info['load1']:.2f} graphical {info['graphical']} our ssh jobs {info['ours_ssh']} "
            f"our argo pods {info['ours_argo']} -> cap {info['cap']}")
        res[n] = info
    return res


__all__ = ["check", "time_cap", "node_cap", "is_graphical", "parse_probe", "our_argo_pods_by_node", "SSH",
           "paths"]
