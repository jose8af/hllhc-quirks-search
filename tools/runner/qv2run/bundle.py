"""Daily / gate repo bundle on cajuela: .part -> verify -> rename -> sha256; keep last 7 repo-* plus all gate-*."""
import os
import subprocess
import sys
import time
from pathlib import Path

from . import paths
from .fsops import atomic_rename_file, fsync_file, makedirs_final, sha256_file

KEEP = 7


def bundle(dest=paths.BACKUP, gate=None, keep=KEEP, out=sys.stdout, date=None):
    dest = Path(dest)
    makedirs_final(dest)
    date = date or time.strftime("%Y-%m-%d")
    name = f"gate-{gate}-{date}.bundle" if gate else f"repo-{date}.bundle"
    final = dest / name
    part = dest / (name + ".part")
    if part.exists():
        part.unlink()
    r = subprocess.run(["git", "-C", str(paths.REPO), "bundle", "create", str(part), "--all"], capture_output=True,
                       text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git bundle create failed: {r.stderr.strip()}")
    fsync_file(part)
    v = subprocess.run(["git", "-C", str(paths.REPO), "bundle", "verify", str(part)], capture_output=True, text=True)
    if v.returncode != 0:
        part.unlink()
        raise RuntimeError(f"git bundle verify failed: {v.stderr.strip()}")
    h_part = sha256_file(part)
    atomic_rename_file(part, final)
    h = sha256_file(final)
    if h != h_part:
        raise RuntimeError(f"sha256 changed across rename: {h_part} -> {h}")
    size = os.stat(final).st_size
    write_side = dest / (name + ".sha256")
    side_part = dest / (name + ".sha256.part")
    side_part.write_text(f"{h}  {name}\n")
    fsync_file(side_part)
    atomic_rename_file(side_part, write_side)
    removed = []
    daily = sorted(p for p in dest.glob("repo-*.bundle"))
    for p in daily[:-keep] if len(daily) > keep else []:
        p.unlink()
        s = dest / (p.name + ".sha256")
        if s.exists():
            s.unlink()
        removed.append(p.name)
    head = subprocess.run(["git", "-C", str(paths.REPO), "rev-parse", "--short", "HEAD"], capture_output=True,
                          text=True).stdout.strip()
    out.write(f"bundle {final} {size} B sha256 {h} (HEAD {head}); verified; removed {removed}\n")
    return final, h, size, removed
