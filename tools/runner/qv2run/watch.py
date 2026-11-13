"""One lightweight watcher: blocks until a campaign completes (exit 0) or fails/stalls (exit 2); timeout exit 3.

Reads markers every `interval` seconds (local stat/read on /home, no cluster calls except one `kubectl get
workflows` per interval when no driver holds the lock). Prints a line only when the counts change.
"""
import sys
import time

from .driver import driver_alive, read_state
from .ledger import summary


def argo_active(camp):
    try:
        from .argo import our_workflows, wf_phase
        return any(wf_phase(w) in ("Pending", "Running") for w in our_workflows(camp))
    except Exception:  # noqa: BLE001 - kubectl unavailable: rely on the driver lock only
        return False


def watch(camp, interval=60, timeout=None, grace=180, out=sys.stdout):
    t0 = time.time()
    last = None
    while True:
        cnt, st = summary(camp)
        n = len(camp.jobs)
        line = (f"done {cnt['done']}/{n} failed {cnt['failed']} running {cnt['running']} "
                f"retryable {cnt['retryable']} pending {cnt['pending']}")
        if line != last:
            out.write(f"[watch {time.strftime('%H:%M:%S')}] {camp.name}: {line}\n")
            out.flush()
            last = line
        if cnt["done"] == n:
            out.write(f"[watch] {camp.name}: COMPLETE\n")
            return 0
        active = driver_alive(camp) or argo_active(camp)
        if not active and time.time() - t0 > grace:
            ds = read_state(camp)
            out.write(f"[watch] {camp.name}: INCOMPLETE and no driver/workflow active "
                      f"(driver state: {ds.get('status', 'none')}); {line}\n")
            return 2
        if timeout and time.time() - t0 > timeout:
            out.write(f"[watch] {camp.name}: TIMEOUT after {timeout} s; {line}\n")
            return 3
        time.sleep(interval)
