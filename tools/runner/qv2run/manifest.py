"""Campaign MANIFEST (from markers), the DATA_MANIFEST.md row, and a df/du-free usage report."""
import hashlib
import sys
import time
from collections import defaultdict

from . import markers, paths
from .fsops import makedirs_final, sha256_file, write_atomic
from .ledger import iter_marker_files


def human(n):
    for u in ("B", "kB", "MB", "GB", "TB"):
        if abs(n) < 1000 or u == "TB":
            return f"{n:.1f} {u}" if u != "B" else f"{n} B"
        n /= 1000.0


def campaign_files(camp):
    """[(path, bytes, sha256)] of all outputs of done jobs, from markers only."""
    rows, missing = [], []
    for j in camp.jobs:
        s, last, _ = markers.state(markers.read(camp.marker_path(j)))
        if s != "done":
            missing.append(j.id)
            continue
        for o in last["outputs"]:
            rows.append((o["path"], o["bytes"], o["sha256"]))
    return sorted(rows), missing


def write_manifest(camp, verify=False, out=sys.stdout):
    rows, missing = campaign_files(camp)
    if verify:
        for p, b, h in rows:
            if sha256_file(p) != h:
                raise RuntimeError(f"verify failed: {p}")
    text = "".join(f"{p}\t{b}\t{h}\n" for p, b, h in rows)
    d = camp.campaign_dir()
    makedirs_final(d)
    write_atomic(d / "MANIFEST", text)
    msha = hashlib.sha256(text.encode()).hexdigest()
    size = sum(b for _, b, _ in rows)
    rel = str(camp.campaign_dir().relative_to(paths.DATA)) + "/"
    regen = camp.regenerate or f"tools/runner/bin/qv2run argo launch {camp.source.relative_to(paths.REPO) if str(camp.source).startswith(str(paths.REPO)) else camp.source}"
    row = (f"| {camp.name} | `{rel}` | {human(size)} | {len(rows)} | `{msha[:16]}` | {camp.tier} | `{regen}` |")
    out.write(f"MANIFEST written: {d / 'MANIFEST'} ({len(rows)} files, {size} B, sha256 {msha})\n")
    if missing:
        out.write(f"WARNING: {len(missing)} job(s) not done, not in manifest: {missing[:10]}\n")
    out.write("DATA_MANIFEST.md row:\n" + row + "\n")
    return row, msha, size, len(rows), missing


def usage(ledger_dirs=(paths.LEDGER_MARKERS,), out=sys.stdout):
    """Per-campaign bytes and file counts from done markers (no du/df over NFS)."""
    per = defaultdict(lambda: [0, 0])
    for ld in ledger_dirs:
        for camp_name, m in iter_marker_files(ld):
            s, last, _ = markers.state(markers.read(m))
            if s == "done":
                for o in last.get("outputs", []):
                    per[camp_name][0] += o["bytes"]
                    per[camp_name][1] += 1
    tot_b = sum(v[0] for v in per.values())
    tot_n = sum(v[1] for v in per.values())
    out.write(f"### cajuela usage from markers ({time.strftime('%Y-%m-%d %H:%M %z')})\n\n")
    out.write("| campaign | size | files |\n|---|---|---|\n")
    for c in sorted(per):
        out.write(f"| {c} | {human(per[c][0])} | {per[c][1]} |\n")
    out.write(f"| **total** | **{human(tot_b)}** | **{tot_n}** |\n\n")
    out.write(f"Budget: {tot_b / 1.5e12 * 100:.3f}% of the 1.5 TB soft budget (stop and ask at 2.0 TB).\n")
    return tot_b, tot_n, dict(per)
