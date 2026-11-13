"""qv2run command line. Run through tools/runner/bin/qv2run (picks the runner's pixi Python)."""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from . import campaign as campaign_mod
from . import paths


def _camp(path):
    return campaign_mod.load(path)


def _detach(args, backend):
    """Re-exec this command detached (setsid nohup) with output to the campaign's driver log; print the pid."""
    camp = _camp(args.campaign)
    from .fsops import makedirs_final
    makedirs_final(camp.state_dir())
    logp = camp.state_dir() / f"{backend}_driver.log"
    argv = [a for a in sys.argv[1:] if a != "--detach"]
    cmd = [str(paths.RUNNER / "bin" / "qv2run")] + argv
    with open(logp, "ab") as lf:
        p = subprocess.Popen(["setsid", "nohup", "nice", "-n", "19"] + cmd, stdout=lf, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, start_new_session=True)
    sys.stdout.write(f"{backend} driver started, pid {p.pid}, log {logp}\n")
    return 0


def _remote(args, backend):
    """Start the driver detached on a worker (light, standard library, ~20 MB): keeps einstein free."""
    import shlex
    camp = _camp(args.campaign)
    argv = [a for a in sys.argv[1:] if a not in ("--detach",)]
    i = argv.index("--on")
    node = argv[i + 1]
    del argv[i:i + 2]
    logp = f"{paths.SCRATCH}/drivers/{camp.name}.{backend}.log"
    cmd = " ".join(shlex.quote(x) for x in [str(paths.RUNNER / "bin" / "qv2run")] + argv)
    remote = (f"mkdir -p {paths.SCRATCH}/drivers || exit 1; setsid nohup nice -n 10 {cmd} >> {logp} 2>&1 "
              f"< /dev/null & echo $!")
    r = subprocess.run(["ssh", "-x", "-o", "BatchMode=yes", node, remote], capture_output=True, text=True,
                       timeout=60)
    sys.stdout.write(f"{backend} driver started on {node}, pid {r.stdout.strip()}, log {node}:{logp}\n"
                     f"watch: {paths.RUNNER / 'bin' / 'qv2-watch'} {camp.source}\n")
    return r.returncode


def main(argv=None):
    ap = argparse.ArgumentParser(prog="qv2run")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("job", help="run one job (used inside pods and over SSH)")
    p.add_argument("--campaign", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--mechanism", choices=("argo", "ssh", "local"), required=True)
    p.add_argument("--force", action="store_true", help="re-run even if done")
    p.add_argument("--mem-limit-mb", type=float, default=None)

    for name in ("status", "verify", "manifest", "watch"):
        q = sub.add_parser(name)
        q.add_argument("campaign")
        if name == "status":
            q.add_argument("-v", "--verbose", action="count", default=0)
            q.add_argument("--json", action="store_true")
            q.add_argument("--live", action="store_true", help="check that 'running' jobs are really alive")
        if name == "manifest":
            q.add_argument("--verify", action="store_true")
        if name == "watch":
            q.add_argument("--interval", type=float, default=60)
            q.add_argument("--timeout", type=float, default=None)
            q.add_argument("--grace", type=float, default=180)

    q = sub.add_parser("rebuild-ledger")
    q.add_argument("--ledger", default=str(paths.LEDGER_MARKERS))
    q.add_argument("--out", default=None)

    q = sub.add_parser("usage")
    q.add_argument("--ledger", action="append", default=None)

    q = sub.add_parser("bundle")
    q.add_argument("--gate", default=None)
    q.add_argument("--dest", default=str(paths.BACKUP))
    q.add_argument("--keep", type=int, default=7)

    q = sub.add_parser("nodes", help="pre-launch node check and parallelism")
    q.add_argument("--nodes", default=",".join(paths.WORKERS))
    q.add_argument("--expected-hours", type=float, default=0)

    for backend in ("ssh", "argo"):
        b = sub.add_parser(backend)
        bs = b.add_subparsers(dest="action", required=True)
        lq = bs.add_parser("launch")
        lq.add_argument("campaign")
        lq.add_argument("--nodes", default=",".join(paths.WORKERS))
        lq.add_argument("--detach", action="store_true", help="run detached on this host")
        lq.add_argument("--on", default=None, help="run the driver detached on this worker (recommended)")
        if backend == "ssh":
            lq.add_argument("--max-per-node", type=int, default=None)
            lq.add_argument("--retries", type=int, default=2)
            lq.add_argument("--poll", type=float, default=5)
            lq.add_argument("--dry-run", action="store_true")
        else:
            lq.add_argument("--max-parallel", type=int, default=None)
            lq.add_argument("--keep", action="store_true", help="keep succeeded workflows")
            rq = bs.add_parser("render", help="print the workflow(s) without submitting")
            rq.add_argument("campaign")
            rq.add_argument("--parallelism", type=int, default=2)
            rq.add_argument("--node", default=None)

    a = ap.parse_args(argv)

    if a.cmd == "job":
        from . import wrapper
        return wrapper.main(a)
    if a.cmd == "status":
        from . import ledger
        camp = _camp(a.campaign)
        if a.json:
            cnt, st = ledger.summary(camp)
            sys.stdout.write(json.dumps({"campaign": camp.name, "counts": dict(cnt), "jobs": len(camp.jobs)}) + "\n")
            return 0
        ledger.print_status(camp, verbose=a.verbose, live=a.live)
        return 0
    if a.cmd == "verify":
        from . import ledger
        return 1 if ledger.verify(_camp(a.campaign)) else 0
    if a.cmd == "manifest":
        from . import manifest
        manifest.write_manifest(_camp(a.campaign), verify=a.verify)
        return 0
    if a.cmd == "watch":
        from . import watch
        return watch.watch(_camp(a.campaign), interval=a.interval, timeout=a.timeout, grace=a.grace)
    if a.cmd == "rebuild-ledger":
        from . import ledger
        out = Path(a.out) if a.out else (paths.JOBS_TSV if Path(a.ledger) == paths.LEDGER_MARKERS
                                         else Path(a.ledger).parent / "jobs.tsv")
        n = ledger.rebuild(a.ledger, out)
        sys.stdout.write(f"wrote {out} ({n} rows)\n")
        return 0
    if a.cmd == "usage":
        from . import manifest
        manifest.usage(a.ledger or [str(paths.LEDGER_MARKERS)])
        return 0
    if a.cmd == "bundle":
        from . import bundle
        bundle.bundle(dest=a.dest, gate=a.gate, keep=a.keep)
        return 0
    if a.cmd == "nodes":
        from . import nodes
        info = nodes.check(a.nodes.split(","), log=lambda m: sys.stdout.write(m + "\n"))
        tc = nodes.time_cap(expected_hours=a.expected_hours)
        sys.stdout.write(f"time cap {tc}; sum of node caps {sum(i['cap'] for i in info.values())}\n")
        return 0
    if a.cmd in ("ssh", "argo") and getattr(a, "on", None):
        return _remote(a, a.cmd)
    if a.cmd == "ssh":
        if a.detach:
            return _detach(a, "ssh")
        from . import ssh
        return ssh.launch(_camp(a.campaign), a.nodes.split(","), max_per_node=a.max_per_node, retries=a.retries,
                          poll_s=a.poll, dry_run=a.dry_run)
    if a.cmd == "argo":
        from . import argo
        if a.action == "render":
            camp = _camp(a.campaign)
            for k, cj in enumerate(argo.chunks(camp)):
                sys.stdout.write(json.dumps(argo.render(camp, cj, k, a.parallelism, node=a.node), indent=1) + "\n")
            return 0
        if a.detach:
            return _detach(a, "argo")
        return argo.launch(_camp(a.campaign), a.nodes.split(","), max_parallel=a.max_parallel, keep=a.keep)
    return 1


if __name__ == "__main__":
    sys.exit(main())
