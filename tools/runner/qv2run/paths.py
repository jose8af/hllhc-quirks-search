"""Fixed locations of the quirks-v2 study (brief 5.2). Same absolute paths on every node and in every pod.

Environment overrides exist only so the unit tests can run in a private temp tree.
"""
import os
from pathlib import Path

REPO = Path(os.environ.get("QV2_REPO", "/home/users/jdochoa/hllhc-quirks-search"))
QV2 = REPO / "analyses" / "quirks_v2"
DATA = Path(os.environ.get("QV2_DATA", "/nfs/cajuela/jdochoa/quirks_v2/data"))
LOGS = Path(os.environ.get("QV2_LOGS", "/nfs/cajuela/jdochoa/quirks_v2/logs"))
BACKUP = Path(os.environ.get("QV2_BACKUP", "/nfs/cajuela/jdochoa/quirks_v2/backup"))
SCRATCH = Path(os.environ.get("QV2_SCRATCH", "/home/scratch/jdochoa"))
LEDGER_MARKERS = QV2 / "ledger" / "markers"
JOBS_TSV = QV2 / "ledger" / "jobs.tsv"
RUNNER = REPO / "tools" / "runner"
JOB_ENTRY = RUNNER / "bin" / "qv2-job"

# Pinned image (tools/PREFLIGHT.md): never pull anything else.
IMAGE = "ubuntu@sha256:2198e4c65076e9cb0b3d695219df667c0e3b0072da64ca3c2648aca17dcecaf5"
NFS_SERVER = "192.168.10.254"
WORKERS = ("landau", "maxwell", "schrodinger")
UID, GID = 10015, 10000
MAX_JOB_SECONDS = 1800  # 30-minute rule
OWNER_LABELS = {"owner": "jdochoa", "study": "quirks-v2"}
