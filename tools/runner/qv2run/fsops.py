"""File operations with the cajuela rules built in: files are renamed, directories never are."""
import hashlib
import os
import stat
from pathlib import Path

CHUNK = 4 << 20


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def fsync_file(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def fsync_dir(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def atomic_rename_file(src, dst):
    """Rename a regular file within one directory. Refuses directories (PREFLIGHT: never rename a dir on cajuela)."""
    src, dst = Path(src), Path(dst)
    st = os.lstat(src)
    if not stat.S_ISREG(st.st_mode):
        raise IsADirectoryError(f"refusing to rename non-regular file {src}")
    if src.parent != dst.parent:
        raise ValueError(f"rename across directories refused: {src} -> {dst}")
    if dst.exists() and not dst.is_file():
        raise IsADirectoryError(f"refusing to replace non-file {dst}")
    os.replace(src, dst)


def write_atomic(path, data, mode=0o644):
    """Write bytes/str to path via path.part + fsync + rename (used on /home for markers and on cajuela for logs)."""
    path = Path(path)
    part = path.with_name(path.name + ".part")
    if isinstance(data, str):
        data = data.encode()
    fd = os.open(part, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    atomic_rename_file(part, path)


def copy_to_part_and_rename(src, final, mode=0o644, before_rename=None):
    """Copy src (scratch) to final.part in the final directory, fsync, rename, re-read.

    Returns (sha256 written, sha256 read back from `final` after the rename, bytes written, size on server).
    """
    final = Path(final)
    part = final.with_name(final.name + ".part")
    h = hashlib.sha256()
    n = 0
    with open(src, "rb") as fi:
        fd = os.open(part, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
        try:
            while True:
                b = fi.read(CHUNK)
                if not b:
                    break
                os.write(fd, b)
                h.update(b)
                n += len(b)
            os.fsync(fd)
        finally:
            os.close(fd)
    os.chmod(part, mode)
    if before_rename:
        before_rename(part)
    atomic_rename_file(part, final)
    fsync_dir(final.parent)
    # Verify after the rename. PREFLIGHT history: one ESTALE on first open after rename (fixed by the admin);
    # keep a short retry so a recurrence is recorded in the log rather than failing silently.
    last = None
    for _ in range(3):
        try:
            back = sha256_file(final)
            size = os.stat(final).st_size
            return h.hexdigest(), back, n, size
        except OSError as e:  # pragma: no cover - only on a cajuela regression
            last = e
    raise last


def makedirs_final(path):
    """Create directories under their final names (never staged and renamed)."""
    os.makedirs(path, mode=0o755, exist_ok=True)
