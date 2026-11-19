"""The job wrapper. Runs identically under Argo (inside the pod) and under SSH (on the worker).

    qv2run job --campaign FILE --job ID --mechanism argo|ssh

Steps: idempotency check -> node-local lock -> fresh scratch dir -> `started` marker line -> run the command under
niceness >= 10 with rusage accounting, a 30-minute limit and (SSH) a memory limit -> copy each output to
`<final>/<name>.part`, fsync, rename (files only), verify sha256 on the server copy -> job log to cajuela ->
`done` marker line -> delete scratch. Any failure: kill the process group, delete scratch and own .part files,
write the failure line.
"""
import fcntl
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from . import campaign as campaign_mod
from . import markers, paths
from .fsops import copy_to_part_and_rename, makedirs_final, sha256_file, write_atomic

EXIT = {"done": 0, "skip": 0, "failed": 1, "timeout": 2, "killed": 3, "verify_failed": 4, "setup_error": 5,
        "busy": 6, "oom": 7, "io_error": 8}
KILL_GRACE_S = 30
# Back-off for cajuela / NFS-home I/O errors (cluster incident 2026-11-13: cajuela gave EIO for 8 min). The budget
# fits inside the pod deadline: command <= 1800 s + I/O budget 480 s < activeDeadlineSeconds 2400.
IO_BUDGET_S = float(os.environ.get("QV2_IO_RETRY_S", "480"))
IO_FIRST_WAIT_S = 5
STASH = ".qv2_stash.json"


class IOBudgetExceeded(RuntimeError):
    pass


def with_io_retry(fn, what, say, budget=None):
    """Run fn(); on OSError wait 5, 10, 20, ... s (cap 120 s) until the budget is spent, then raise."""
    budget = IO_BUDGET_S if budget is None else budget
    t0, wait, n = time.time(), IO_FIRST_WAIT_S, 0
    while True:
        try:
            return fn()
        except OSError as e:
            n += 1
            left = budget - (time.time() - t0)
            if left <= 0:
                raise IOBudgetExceeded(f"{what}: {e!r} after {n} tries") from e
            say(f"I/O error on {what} (try {n}): {e!r}; retrying in {min(wait, left):.0f} s")
            time.sleep(min(wait, left))
            wait = min(wait * 2, 120)


def test_pause(stage, scratch):
    """TEST ONLY: if QV2_TEST_PAUSE_AT == stage, flag it in scratch and sleep so a test can kill -9 the wrapper."""
    if os.environ.get("QV2_TEST_PAUSE_AT") == stage:
        try:
            Path(scratch, f".qv2_paused_{stage}").write_text(str(os.getpid()))
        except OSError:
            pass
        time.sleep(float(os.environ.get("QV2_TEST_PAUSE_S", "300")))


def node_name():
    return os.environ.get("QV2_NODE") or socket.gethostname().split(".")[0]


def boot_id():
    try:
        return Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    except OSError:
        return ""


def proc_start_time():
    """Wall-clock start time of this process (from /proc), to measure interpreter start-up from NFS."""
    try:
        st = Path("/proc/self/stat").read_text()
        ticks = int(st[st.rindex(")") + 2:].split()[19])
        btime = next(int(ln.split()[1]) for ln in Path("/proc/stat").read_text().splitlines()
                     if ln.startswith("btime"))
        return round(btime + ticks / os.sysconf("SC_CLK_TCK"), 2)
    except (OSError, ValueError, StopIteration, IndexError):
        return None


def outputs_intact(camp, job, rec, rehash=True):
    """True if every output recorded in `rec` exists with the recorded size (and sha256 when rehash)."""
    recorded = {o["name"]: o for o in rec.get("outputs", [])}
    if set(recorded) != set(job.outputs):
        return False, "output list differs from campaign"
    for name, o in recorded.items():
        p = camp.final_dir(job) / name
        try:
            size = os.stat(p).st_size
        except FileNotFoundError:
            return False, f"{name} missing"
        if size != o["bytes"]:
            return False, f"{name} size {size} != {o['bytes']}"
        if rehash:
            h = sha256_file(p)
            if h != o["sha256"]:
                return False, f"{name} sha256 {h[:12]} != {o['sha256'][:12]}"
    return True, "ok"


def _cgroup_file(name):
    p = Path("/sys/fs/cgroup") / name
    try:
        return p.read_text()
    except OSError:
        return None


def _oom_kills(cgdir):
    try:
        txt = (Path(cgdir) / "memory.events").read_text()
    except OSError:
        return None
    for ln in txt.splitlines():
        k, _, v = ln.partition(" ")
        if k == "oom_kill":
            return int(v)
    return None


def stop_orphan_scopes(job_id, say):
    """Stop leftover systemd user scopes of earlier attempts of this job (wrapper SIGKILLed, payload orphaned)."""
    if not shutil.which("systemctl"):
        return []
    try:
        r = subprocess.run(["systemctl", "--user", "list-units", "--plain", "--no-legend", "--all",
                            f"qv2-{job_id}-*.scope"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return []
    units = [ln.split()[0] for ln in r.stdout.splitlines() if ln.strip()]
    for u in units:
        say(f"stopping orphan scope {u} of an earlier attempt")
        subprocess.run(["systemctl", "--user", "kill", "--signal=SIGKILL", u], capture_output=True, timeout=20)
        subprocess.run(["systemctl", "--user", "stop", u], capture_output=True, timeout=30)
    return units


def _have_user_scope():
    if not shutil.which("systemd-run"):
        return False
    try:
        r = subprocess.run(["systemd-run", "--user", "--scope", "-q", "-p", "MemoryMax=64M", "true"],
                           capture_output=True, timeout=20)
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


class Runner:
    def __init__(self, camp, job, mechanism, force=False, mem_limit_mb=None, log=None):
        self.c, self.j, self.mech, self.force = camp, job, mechanism, force
        self.mem_limit_mb = mem_limit_mb if mem_limit_mb is not None else round(1.5 * job.max_rss_mb)
        self.node = node_name()
        self.marker = camp.marker_path(job)
        self.scratch = camp.scratch_dir(job)
        self.final = camp.final_dir(job)
        self.child = None
        self.killed_by = None  # "timeout" | "signal" | "watchdog"
        self.logf = None
        self.parts = []

    # ---- logging ----------------------------------------------------------------------------------------------
    def say(self, msg):
        line = f"[qv2run {time.strftime('%H:%M:%S')} {self.node}] {msg}\n"
        sys.stderr.write(line)
        if self.logf:
            self.logf.write(line.encode())
            self.logf.flush()

    def mark(self, status, **kw):
        rec = {"job_id": self.j.id, "campaign": self.c.name, "mechanism": self.mech, "node": self.node,
               "status": status, "pid": os.getpid(), "boot_id": boot_id()}
        for k in ("ARGO_WORKFLOW_NAME", "HOSTNAME"):
            if self.mech == "argo" and os.environ.get(k):
                rec["pod" if k == "HOSTNAME" else "workflow"] = os.environ[k]
        rec.update(kw)
        return with_io_retry(lambda: markers.append(self.marker, rec), f"marker {status}", self.say)

    # ---- process control --------------------------------------------------------------------------------------
    def _killpg(self, why):
        if self.child is None:
            return
        if self.killed_by is None:
            self.killed_by = why
        try:
            os.killpg(self.child.pid, signal.SIGTERM)
        except ProcessLookupError:
            return

        def hard():
            try:
                os.killpg(self.child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        t = threading.Timer(KILL_GRACE_S, hard)
        t.daemon = True
        t.start()

    def _on_signal(self, signum, frame):
        self.say(f"received signal {signum}; terminating job process group")
        if self.child is None:
            raise KeyboardInterrupt
        self._killpg("signal")

    def _watchdog(self, limit_kb):
        """Fallback memory guard when no cgroup limit is available: sums RSS of the process group every second."""
        pg = self.child.pid
        while self.child.poll() is None:
            tot = 0
            for d in os.listdir("/proc"):
                if not d.isdigit():
                    continue
                try:
                    st = Path(f"/proc/{d}/stat").read_text()
                    fields = st[st.rindex(")") + 2:].split()
                    if int(fields[2]) != pg:  # pgrp
                        continue
                    tot += int(fields[21]) * (os.sysconf("SC_PAGE_SIZE") // 1024)
                except (OSError, ValueError, IndexError):
                    continue
            if tot > limit_kb:
                self.say(f"watchdog: RSS {tot // 1024} MB > limit {limit_kb // 1024} MB")
                self._killpg("watchdog")
                return
            time.sleep(1)

    # ---- main -------------------------------------------------------------------------------------------------
    def run(self):
        recs = markers.read(self.marker)
        st, last, attempts = markers.state(recs)
        if st == "done" and not self.force:
            ok, why = with_io_retry(lambda: outputs_intact(self.c, self.j, last), "idempotency check", self.say)
            if ok:
                self.say(f"skip: {self.j.id} already done and outputs verified")
                return "skip"
            self.say(f"marker says done but {why}: re-running")
            self.mark("corrupt", reason=why)
        lockdir = paths.SCRATCH / ".locks"
        makedirs_final(lockdir)
        lockfd = os.open(lockdir / f"{self.j.id}.lock", os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.say(f"busy: another instance of {self.j.id} runs on this node")
            os.close(lockfd)
            return "busy"
        old = {s: signal.signal(s, self._on_signal) for s in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
        try:
            return self._run_locked(attempts + 1)
        finally:
            for s, h in old.items():
                signal.signal(s, h)
            os.close(lockfd)

    def _cleanup(self):
        if not getattr(self, "keep_scratch", False):
            shutil.rmtree(self.scratch, ignore_errors=True)
        for p in self.parts:
            try:
                os.unlink(p)
            except OSError:  # gone already, or cajuela unavailable: the next attempt removes stale .part files
                pass

    def _ship_log(self, attempt):
        try:
            self.logf.flush()
            ld = self.c.log_dir(self.j)
            dst = ld / f"{self.j.id}.a{attempt}.log"
            data = (self.scratch / ".qv2_job.log").read_bytes()
            with_io_retry(lambda: (makedirs_final(ld), write_atomic(dst, data)), "job log", self.say, budget=60)
            return str(dst)
        except (OSError, IOBudgetExceeded) as e:
            sys.stderr.write(f"[qv2run] could not ship log: {e}\n")
            return ""

    def _load_stash(self):
        """A stash = command finished, outputs hashed, copy to cajuela not completed (killed or I/O error)."""
        try:
            st = json.loads((self.scratch / STASH).read_text())
        except (OSError, ValueError):
            return None
        if st.get("job_id") != self.j.id or set(st.get("outputs", {})) != set(self.j.outputs):
            return None
        for name, h in st["outputs"].items():
            p = self.scratch / name
            if not p.is_file() or sha256_file(p) != h:
                return None
        return st

    def _run_locked(self, attempt):
        self.keep_scratch = False
        if self.j.timeout_exception and self.mech != "ssh":
            self.mark("setup_error", attempt=attempt, error="timeout_exception is allowed on the ssh mechanism only")
            return "setup_error"
        orphans = stop_orphan_scopes(self.j.id, self.say) if self.mech != "argo" else []
        stash = self._load_stash()
        try:
            if stash is None:
                shutil.rmtree(self.scratch, ignore_errors=True)  # leftovers of a killed run
            makedirs_final(self.scratch)
            for p in self.scratch.glob(".qv2_paused_*"):
                p.unlink()
            self.logf = open(self.scratch / ".qv2_job.log", "ab", buffering=0)
            if orphans:
                self.say(f"stopped orphan scope(s) of an earlier attempt: {orphans}")

            def setup_final():
                makedirs_final(self.final)
                for name in self.j.outputs:  # stale .part of a killed run
                    p = self.final / (name + ".part")
                    if p.exists() and p.is_file():
                        p.unlink()
                        self.say(f"removed stale {p}")
            with_io_retry(setup_final, "final dir on cajuela", self.say)
        except IOBudgetExceeded as e:
            self.keep_scratch = stash is not None
            self.mark("io_error", attempt=attempt, error=str(e), stage="setup")
            self._cleanup()
            return "io_error"
        except OSError as e:
            self.mark("setup_error", attempt=attempt, error=str(e))
            self._cleanup()
            return "setup_error"
        t0 = time.time()
        self.mark("started", attempt=attempt, scratch=str(self.scratch), mem_limit_mb=self.mem_limit_mb,
                  timeout_s=self.j.timeout_s, t_proc_start=proc_start_time(), t_wrapper=round(t0, 3),
                  resumed_from_stash=stash is not None, runner_py=os.environ.get("QV2_RUNNER_PY", sys.executable),
                  **({"timeout_exception": self.j.timeout_exception} if self.j.timeout_exception else {}))
        self.say(f"job {self.j.id} attempt {attempt} mechanism {self.mech} in {self.scratch}"
                 + (" (resuming from stash: command already finished)" if stash else ""))
        try:
            if stash:
                result = self._publish(attempt, dict(stash["acct"], resumed_from_stash=True))
            else:
                result = self._execute(attempt, t0)
        except IOBudgetExceeded as e:
            self.say(f"giving up for now: {e}; scratch kept for the next attempt")
            self.keep_scratch = (self.scratch / STASH).exists()
            try:
                self.mark("io_error", attempt=attempt, error=str(e), stash=self.keep_scratch)
            except IOBudgetExceeded:
                pass  # NFS home down too: the marker stays 'started'; liveness -> 'lost' -> retry
            result = "io_error"
        except Exception as e:  # noqa: BLE001 - any wrapper bug must still leave a marker line and no debris
            self.say(f"wrapper error: {e!r}")
            self._killpg("signal")
            logp = self._ship_log(attempt)
            self.mark("setup_error", attempt=attempt, error=repr(e), log=logp, wall_s=round(time.time() - t0, 3))
            result = "setup_error"
        finally:
            if self.logf:
                self.logf.close()
            self._cleanup()
        return result

    def _execute(self, attempt, t0):
        env = dict(os.environ)
        if env.get("HOME", "/") in ("", "/"):
            env["HOME"] = "/home/users/jdochoa"
        env.update(QV2_JOB_ID=self.j.id, QV2_CAMPAIGN=self.c.name, QV2_SHARD=f"{self.j.shard:03d}",
                   QV2_OUT_DIR=str(self.scratch), QV2_SCRATCH_DIR=str(self.scratch), QV2_FINAL_DIR=str(self.final),
                   QV2_REPO=str(paths.REPO), QV2_NODE=self.node, QV2_ATTEMPT=str(attempt))
        argv = ["bash", "-c", self.j.command]
        memguard = "pod-cgroup" if self.mech == "argo" else "none"
        if self.mech != "argo" and self.mem_limit_mb:
            if _have_user_scope():
                memguard = "systemd-scope"
                unit = f"qv2-{self.j.id}-{os.getpid()}"
                argv = ["systemd-run", "--user", "--scope", "-q", f"--unit={unit}",
                        "-p", f"MemoryMax={int(self.mem_limit_mb)}M", "-p", "MemorySwapMax=0",
                        "-p", f"RuntimeMaxSec={self.j.timeout_s + 2 * KILL_GRACE_S}", "--"] + argv
            else:
                memguard = "watchdog"
        cur = os.nice(0)
        if cur < 10:  # brief 5.3: every job command runs under nice 10 (no-op inside pods, already nice 10)
            argv = ["nice", "-n", str(10 - cur)] + argv
        os.umask(0o022)
        self.say(f"command: {self.j.command}")
        self.say(f"memory guard: {memguard} limit {self.mem_limit_mb} MB; timeout {self.j.timeout_s} s")
        oom0 = _oom_kills("/sys/fs/cgroup") if self.mech == "argo" else None
        t_spawn = time.time()
        self.child = subprocess.Popen(argv, cwd=self.scratch, env=env, stdin=subprocess.DEVNULL, stdout=self.logf,
                                      stderr=subprocess.STDOUT, start_new_session=True)
        cgdir = None
        if memguard == "systemd-scope":
            time.sleep(0.2)
            try:
                rel = Path(f"/proc/{self.child.pid}/cgroup").read_text().strip().split("::", 1)[1]
                cgdir = "/sys/fs/cgroup" + rel
            except (OSError, IndexError):
                pass
        if memguard == "watchdog":
            threading.Thread(target=self._watchdog, args=(int(self.mem_limit_mb * 1024),), daemon=True).start()
        timer = threading.Timer(self.j.timeout_s, self._killpg, args=("timeout",))
        timer.daemon = True
        timer.start()
        oom_seen = [0]

        def oom_poll():
            while self.child.poll() is None and cgdir:
                n = _oom_kills(cgdir)
                if n:
                    oom_seen[0] = n
                time.sleep(0.5)
        if cgdir:
            threading.Thread(target=oom_poll, daemon=True).start()
        _, wstatus, ru = os.wait4(self.child.pid, 0)
        self.child.returncode = os.waitstatus_to_exitcode(wstatus)
        timer.cancel()
        t1 = time.time()
        cpu_s = round(ru.ru_utime + ru.ru_stime, 3)
        rss_mb = round(ru.ru_maxrss / 1024, 1)
        rc = self.child.returncode
        acct = {"attempt": attempt, "exit_code": rc, "cpu_s": cpu_s, "user_s": round(ru.ru_utime, 3),
                "sys_s": round(ru.ru_stime, 3), "max_rss_mb": rss_mb, "wall_s": round(t1 - t0, 3),
                "t_wrapper": round(t0, 3), "t_cmd_start": round(t_spawn, 3),
                "t_cmd_end": round(t1, 3), "cmd_wall_s": round(t1 - t_spawn, 3), "mem_guard": memguard,
                "mem_limit_mb": self.mem_limit_mb, "nice": cur if cur >= 10 else 10}
        if self.mech == "argo":
            peak = _cgroup_file("memory.peak")
            if peak:
                acct["cgroup_peak_mb"] = round(int(peak) / 2**20, 1)
            oom1 = _oom_kills("/sys/fs/cgroup")
            if oom0 is not None and oom1 is not None and oom1 > oom0:
                oom_seen[0] = oom1 - oom0
        self.say(f"exit {rc}; cpu {cpu_s} s; max RSS {rss_mb} MB; wall {acct['wall_s']} s")
        if rc != 0:
            if oom_seen[0] or self.killed_by == "watchdog" or (
                    rc in (-9, 137) and rss_mb >= 0.8 * self.mem_limit_mb and self.killed_by is None):
                status = "oom"
            elif self.killed_by == "timeout":
                status = "timeout"
            elif self.killed_by == "signal":
                status = "killed"
            else:
                status = "failed"
            logp = self._ship_log(attempt)
            self.mark(status, log=logp, **acct)
            return status
        # ---- command succeeded: stash (local) so finished work survives a crash or a cajuela outage ---------
        hashes = {}
        for name in self.j.outputs:
            src = self.scratch / name
            if not src.is_file():
                self.say(f"missing output {name}")
                logp = self._ship_log(attempt)
                self.mark("failed", log=logp, reason=f"missing output {name}", **acct)
                return "failed"
            hashes[name] = sha256_file(src)
        write_atomic(self.scratch / STASH, json.dumps({"job_id": self.j.id, "campaign": self.c.name,
                                                       "outputs": hashes, "acct": acct}))
        test_pause("before_copy", self.scratch)
        return self._publish(attempt, acct)

    def _publish(self, attempt, acct):
        """scratch -> name.part -> fsync -> rename -> verify (with I/O back-off), then the `done` line."""
        stash = json.loads((self.scratch / STASH).read_text())
        outs = []
        for name in self.j.outputs:
            src, dst = self.scratch / name, self.final / name
            part = dst.with_name(name + ".part")
            self.parts.append(part)

            def one():
                try:
                    return copy_to_part_and_rename(src, dst, before_rename=lambda p: test_pause("during_copy",
                                                                                                 self.scratch))
                except OSError:
                    try:
                        part.unlink()
                    except OSError:
                        pass
                    raise
            h_written, h_back, n, size = with_io_retry(one, f"copy {name} to cajuela", self.say)
            h_scratch = stash["outputs"][name]
            if not (h_scratch == h_written == h_back) or n != size:
                self.say(f"verification failed for {name}: {h_scratch[:12]} {h_written[:12]} {h_back[:12]}")
                with_io_retry(lambda: os.unlink(dst), f"remove bad {name}", self.say)
                logp = self._ship_log(attempt)
                self.mark("verify_failed", log=logp, output=name, **acct)
                return "verify_failed"
            outs.append({"name": name, "path": str(dst), "sha256": h_back, "bytes": size})
            self.say(f"output {dst} {size} B sha256 {h_back}")
        test_pause("after_rename", self.scratch)
        acct["t_end"] = round(time.time(), 3)
        logp = self._ship_log(attempt)
        self.mark("done", log=logp, outputs=outs, **acct)
        return "done"


def main(args):
    try:
        camp = campaign_mod.load(args.campaign)
        job = camp.by_id[args.job]
    except (campaign_mod.CampaignError, KeyError) as e:
        sys.stderr.write(f"[qv2run] setup error: {e}\n")
        return EXIT["setup_error"]
    try:
        r = Runner(camp, job, args.mechanism, force=args.force, mem_limit_mb=args.mem_limit_mb).run()
    except IOBudgetExceeded as e:  # NFS home or cajuela unavailable before any marker could be written
        sys.stderr.write(f"[qv2run] io_error: {e}\n")
        r = "io_error"
    sys.stderr.write(f"[qv2run] result {json.dumps(r)}\n")
    return EXIT[r]
