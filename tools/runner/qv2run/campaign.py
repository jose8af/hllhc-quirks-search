"""Campaign description: a JSON file listing jobs. See tools/runner/README in FEAS_C_runner_boris.md."""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import paths

ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,62}$")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")  # used inside k8s names/labels
PREFIX_RE = re.compile(r"^[a-z0-9][a-z0-9_/-]*$")
TIERS = ("final", "regenerable", "scratch", "test")
MAX_ENTRIES_PER_DIR = 10000


class CampaignError(ValueError):
    pass


@dataclass
class Job:
    id: str
    command: str
    outputs: list
    shard: int = 0
    cpu: float = 1
    max_rss_mb: float = 100
    timeout_s: int = paths.MAX_JOB_SECONDS
    tier: str = "scratch"


@dataclass
class Campaign:
    name: str
    tier: str
    jobs: list
    source: Path
    data_prefix: str = ""
    ledger: Path = paths.LEDGER_MARKERS
    regenerate: str = ""
    description: str = ""
    expected_hours: float = 0.0
    by_id: dict = field(default_factory=dict)

    # ---- locations --------------------------------------------------------------------------------------------
    def _rel(self):
        return Path(self.data_prefix) / self.name if self.data_prefix else Path(self.name)

    def campaign_dir(self):
        return paths.DATA / self._rel()

    def final_dir(self, job):
        return self.campaign_dir() / f"{job.shard:03d}"

    def log_dir(self, job):
        return paths.LOGS / self._rel() / f"{job.shard:03d}"

    def marker_dir(self, job):
        return self.ledger / self.name / f"{job.shard:03d}"

    def marker_path(self, job):
        return self.marker_dir(job) / f"{job.id}.marker"

    def state_dir(self):
        """Driver state on /home (locks, driver logs): one writer each."""
        return self.ledger / self.name / "_driver"

    def scratch_dir(self, job):
        return paths.SCRATCH / job.id


def load(path):
    path = Path(path).resolve()
    try:
        raw = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise CampaignError(f"cannot read campaign {path}: {e}") from e
    return from_dict(raw, path)


def from_dict(raw, source=Path("<memory>")):
    name = raw.get("campaign", "")
    if not NAME_RE.match(name):
        raise CampaignError(f"campaign name {name!r} must match {NAME_RE.pattern}")
    tier = raw.get("tier", "")
    if tier not in TIERS:
        raise CampaignError(f"tier {tier!r} not in {TIERS}")
    prefix = raw.get("data_prefix", "")
    if prefix and (not PREFIX_RE.match(prefix) or ".." in prefix.split("/") or prefix.startswith("/")):
        raise CampaignError(f"bad data_prefix {prefix!r}")
    ledger = Path(raw["ledger"]) if raw.get("ledger") else paths.LEDGER_MARKERS
    if not ledger.is_absolute():
        ledger = paths.REPO / ledger
    if str(ledger).startswith(("/nfs/cajuela", "/mnt/cajuela", str(paths.DATA) + "/")):
        raise CampaignError("markers must live on /home, never on cajuela")
    d = raw.get("defaults", {})
    jobs, by_id, per_shard = [], {}, {}
    for j in raw.get("jobs", []):
        jid = j.get("id", "")
        if not ID_RE.match(jid):
            raise CampaignError(f"job id {jid!r} must match {ID_RE.pattern}")
        if jid in by_id:
            raise CampaignError(f"duplicate job id {jid}")
        outs = list(j.get("outputs", d.get("outputs", [])))
        for o in outs:
            if not o or "/" in o or o.endswith(".part") or o.startswith("."):
                raise CampaignError(f"job {jid}: output {o!r} must be a bare file name (no '/', not .part)")
        timeout = int(j.get("timeout_s", d.get("timeout_s", paths.MAX_JOB_SECONDS)))
        if not 0 < timeout <= paths.MAX_JOB_SECONDS:
            raise CampaignError(f"job {jid}: timeout_s {timeout} outside (0, {paths.MAX_JOB_SECONDS}]")
        cmd = j.get("command", d.get("command"))
        if not cmd:
            raise CampaignError(f"job {jid}: no command")
        job = Job(id=jid, command=cmd.replace("{id}", jid), outputs=outs, shard=int(j.get("shard", d.get("shard", 0))),
                  cpu=float(j.get("cpu", d.get("cpu", 1))), max_rss_mb=float(j.get("max_rss_mb", d.get("max_rss_mb", 100))),
                  timeout_s=timeout, tier=tier)
        if not 0 <= job.shard <= 999:
            raise CampaignError(f"job {jid}: shard {job.shard} outside 0..999")
        if job.max_rss_mb <= 0:
            raise CampaignError(f"job {jid}: max_rss_mb must be > 0")
        names = per_shard.setdefault(job.shard, set())
        for o in outs:
            if o in names:
                raise CampaignError(f"output {o} appears twice in shard {job.shard}")
            names.add(o)
        if len(names) > MAX_ENTRIES_PER_DIR:
            raise CampaignError(f"shard {job.shard} exceeds {MAX_ENTRIES_PER_DIR} files")
        jobs.append(job)
        by_id[jid] = job
    if not jobs:
        raise CampaignError("campaign has no jobs")
    return Campaign(name=name, tier=tier, jobs=jobs, source=Path(source), data_prefix=prefix, ledger=ledger,
                    regenerate=raw.get("regenerate", ""), description=raw.get("description", ""),
                    expected_hours=float(raw.get("expected_hours", 0)), by_id=by_id)
