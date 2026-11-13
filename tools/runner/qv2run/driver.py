"""Driver bookkeeping shared by both backends: one driver per campaign (flock on /home), driver state file."""
import fcntl
import json
import os
import socket
import time

from .fsops import makedirs_final, write_atomic


class DriverBusy(RuntimeError):
    pass


class DriverLock:
    def __init__(self, camp):
        self.dir = camp.state_dir()
        makedirs_final(self.dir)
        self.path = self.dir / "driver.lock"
        self.fd = None

    def acquire(self):
        self.fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # POSIX lock: works over NFSv4 (/home)
        except OSError:
            os.close(self.fd)
            self.fd = None
            raise DriverBusy(f"another driver holds {self.path}")
        return self

    def release(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


def driver_alive(camp):
    """True if some process holds the campaign's driver lock (any host)."""
    p = camp.state_dir() / "driver.lock"
    if not p.exists():
        return False
    fd = os.open(p, os.O_RDWR)
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.lockf(fd, fcntl.LOCK_UN)
        return False
    except OSError:
        return True
    finally:
        os.close(fd)


_last = {"key": None, "t": 0.0}
HEARTBEAT_S = 60


def write_state(camp, force=False, **kw):
    """driver.json on /home: rewritten only when the state changes or once per HEARTBEAT_S (NFS-home write budget).

    `heartbeat` (epoch) lets a tiny watcher on einstein detect a dead driver without locks or marker scans.
    """
    kw.setdefault("host", socket.gethostname())
    kw.setdefault("pid", os.getpid())
    key = json.dumps(kw, sort_keys=True, default=str)
    now = time.time()
    if not force and key == _last["key"] and now - _last["t"] < HEARTBEAT_S:
        return
    kw["heartbeat"] = int(now)
    kw["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    write_atomic(camp.state_dir() / "driver.json", json.dumps(kw, indent=1, sort_keys=True, default=str) + "\n")
    _last.update(key=key, t=now)


def read_state(camp):
    try:
        return json.loads((camp.state_dir() / "driver.json").read_text())
    except (OSError, json.JSONDecodeError):
        return {}
