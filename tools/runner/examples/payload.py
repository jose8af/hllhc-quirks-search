"""Deterministic test payload for the runner (TEST ONLY, no physics).

--hash-mib N   CPU-bound: sha256 over N repetitions of a fixed 1 MiB block (known digest for a given N)
--out NAME     write NAME: a header line with the digest, then --pad-kib KiB of deterministic filler
--mem-mib M    allocate and touch M MiB in 8 MiB steps (memory-limit test), then hold for --hold s
--sleep S      sleep S seconds first (kill-midway tests)
--fail         exit 1 after the work (failure-path test)
"""
import argparse
import hashlib
import os
import sys
import time


def block():
    seed = hashlib.sha256(b"qv2-runner-test-block").digest()
    return (seed * (1 << 15))[: 1 << 20]


def stream_digest(n):
    h = hashlib.sha256()
    b = block()
    for _ in range(n):
        h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash-mib", type=int, default=0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--pad-kib", type=int, default=64)
    ap.add_argument("--mem-mib", type=int, default=0)
    ap.add_argument("--hold", type=float, default=2)
    ap.add_argument("--sleep", type=float, default=0)
    ap.add_argument("--fail", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    if a.sleep:
        time.sleep(a.sleep)
    hold = []
    if a.mem_mib:
        for i in range(0, a.mem_mib, 8):
            x = bytearray(8 << 20)
            for k in range(0, len(x), 4096):
                x[k] = 1
            hold.append(x)
            sys.stdout.write(f"allocated {i + 8} MiB\n")
            sys.stdout.flush()
        time.sleep(a.hold)
    d = stream_digest(a.hash_mib) if a.hash_mib else "none"
    sys.stdout.write(f"hash-mib {a.hash_mib} digest {d} wall {time.time() - t0:.2f} s pid {os.getpid()}\n")
    if a.out:
        filler = (block() * (a.pad_kib // 1024 + 1))[: a.pad_kib * 1024]
        with open(a.out, "wb") as f:
            f.write(f"qv2-runner-test hash-mib {a.hash_mib} sha256 {d}\n".encode())
            f.write(filler)
    return 1 if a.fail else 0


if __name__ == "__main__":
    sys.exit(main())
