"""Unit tests for the runner (standard library only):  cd tools/runner && python3 -m unittest -v

All files go to a private tree under /var/tmp/jdochoa/runner_tests (never /tmp, never cajuela).
"""
import datetime as dt
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(os.environ.get("QV2_TEST_BASE", "/var/tmp/jdochoa/runner_tests"))
BASE.mkdir(parents=True, exist_ok=True)
ROOT = Path(tempfile.mkdtemp(prefix="t", dir=BASE))
os.environ.update(QV2_DATA=str(ROOT / "data"), QV2_LOGS=str(ROOT / "logs"), QV2_SCRATCH=str(ROOT / "scratch"),
                  QV2_BACKUP=str(ROOT / "backup"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qv2run import argo, campaign, fsops, ledger, manifest, markers, nodes, paths, wrapper  # noqa: E402
from qv2run import bundle as bundle_mod  # noqa: E402

PY = sys.executable
PAYLOAD = Path(__file__).resolve().parents[1] / "examples" / "payload.py"


def camp_dict(n=3, **over):
    d = {"campaign": "ut-camp", "tier": "test", "ledger": str(ROOT / "ledger"), "data_prefix": "feasibility/ut",
         "defaults": {"max_rss_mb": 50, "timeout_s": 60},
         "jobs": [{"id": f"ut-{i:03d}", "shard": i % 2, "outputs": [f"ut-{i:03d}.dat"],
                   "command": f"{PY} {PAYLOAD} --hash-mib 2 --out ut-{i:03d}.dat"} for i in range(n)]}
    d.update(over)
    return d


def tearDownModule():
    shutil.rmtree(ROOT, ignore_errors=True)


class TestCampaign(unittest.TestCase):
    def test_valid(self):
        c = campaign.from_dict(camp_dict())
        self.assertEqual(len(c.jobs), 3)
        j = c.jobs[1]
        self.assertEqual(c.final_dir(j), paths.DATA / "feasibility/ut/ut-camp/001")
        self.assertEqual(c.marker_path(j), ROOT / "ledger/ut-camp/001/ut-001.marker")
        self.assertEqual(c.log_dir(j), paths.LOGS / "feasibility/ut/ut-camp/001")

    def test_rejects(self):
        bad = [
            dict(campaign="Bad_Name"),
            dict(tier="nope"),
            dict(data_prefix="../x"),
            dict(ledger=str(paths.DATA / "markers")),
            dict(jobs=[{"id": "a", "command": "x", "outputs": ["d/x"]}]),
            dict(jobs=[{"id": "a", "command": "x", "outputs": ["x.part"]}]),
            dict(jobs=[{"id": "a", "command": "x", "timeout_s": 1801}]),
            dict(jobs=[{"id": "a", "command": "x"}, {"id": "a", "command": "y"}]),
            dict(jobs=[{"id": "a", "command": "x", "outputs": ["o"]}, {"id": "b", "command": "y", "outputs": ["o"]}]),
            dict(jobs=[{"id": "UPPER", "command": "x"}]),
            dict(jobs=[]),
        ]
        for b in bad:
            with self.subTest(b=b), self.assertRaises(campaign.CampaignError):
                campaign.from_dict(camp_dict(**b))


class TestFsops(unittest.TestCase):
    def setUp(self):
        self.d = ROOT / "fs"
        self.d.mkdir(exist_ok=True)

    def test_refuses_directory_rename(self):
        (self.d / "sub").mkdir(exist_ok=True)
        with self.assertRaises(IsADirectoryError):
            fsops.atomic_rename_file(self.d / "sub", self.d / "sub2")
        self.assertTrue((self.d / "sub").is_dir())

    def test_refuses_cross_directory(self):
        (self.d / "a").write_text("x")
        (self.d / "sub").mkdir(exist_ok=True)
        with self.assertRaises(ValueError):
            fsops.atomic_rename_file(self.d / "a", self.d / "sub" / "a")

    def test_copy_part_rename(self):
        src = self.d / "src"
        src.write_bytes(os.urandom(100000))
        h1, h2, n, size = fsops.copy_to_part_and_rename(src, self.d / "out.dat")
        self.assertEqual(h1, h2)
        self.assertEqual(h1, fsops.sha256_file(src))
        self.assertEqual(n, size)
        self.assertFalse((self.d / "out.dat.part").exists())
        self.assertEqual(stat.S_IMODE(os.stat(self.d / "out.dat").st_mode), 0o644)


class TestMarkers(unittest.TestCase):
    def test_states(self):
        p = ROOT / "m" / "x.marker"
        self.assertEqual(markers.state(markers.read(p))[0], "pending")
        markers.append(p, {"status": "started"})
        self.assertEqual(markers.state(markers.read(p))[0], "running")
        markers.append(p, {"status": "killed"})
        self.assertEqual(markers.state(markers.read(p))[0], "retryable")
        markers.append(p, {"status": "started"})
        markers.append(p, {"status": "done", "outputs": []})
        s, last, att = markers.state(markers.read(p))
        self.assertEqual((s, att), ("done", 2))
        self.assertFalse(p.with_name("x.marker.part").exists())
        with open(p, "a") as f:  # torn last line (crash mid-write) is tolerated
            f.write('{"status": "do')
        self.assertEqual(markers.state(markers.read(p))[0], "done")  # torn line ignored
        markers.append(p, {"status": "started"})
        self.assertEqual(markers.state(markers.read(p))[0], "running")  # new line not glued to the torn one
        markers.append(p, {"status": "timeout"})
        self.assertEqual(markers.state(markers.read(p))[0], "failed")


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.c = campaign.from_dict(camp_dict(campaign=f"ut-w-{self._testMethodName[-12:].replace('_', '-')}"))

    def run_job(self, job, **kw):
        return wrapper.Runner(self.c, job, "local", mem_limit_mb=0, **kw).run()

    def test_success_skip_and_corrupt(self):
        j = self.c.jobs[0]
        self.assertEqual(self.run_job(j), "done")
        out = self.c.final_dir(j) / j.outputs[0]
        self.assertTrue(out.is_file())
        self.assertEqual(stat.S_IMODE(os.stat(out).st_mode), 0o644)
        self.assertFalse(self.c.scratch_dir(j).exists(), "scratch must be deleted on success")
        recs = markers.read(self.c.marker_path(j))
        done = recs[-1]
        self.assertEqual(done["status"], "done")
        self.assertEqual(done["outputs"][0]["sha256"], fsops.sha256_file(out))
        self.assertGreater(done["cpu_s"], 0)
        self.assertGreater(done["max_rss_mb"], 1)
        self.assertTrue(Path(done["log"]).is_file())
        self.assertFalse(list(self.c.final_dir(j).glob("*.part")))
        # idempotent: second run skips without a new marker line
        self.assertEqual(self.run_job(j), "skip")
        self.assertEqual(len(markers.read(self.c.marker_path(j))), len(recs))
        # corrupt the output: verify catches it, the wrapper re-runs
        with open(out, "r+b") as f:
            f.seek(10)
            f.write(b"X")
        bad = ledger.verify(self.c, out=io.StringIO())
        self.assertEqual([b[0] for b in bad], [j.id])
        self.assertEqual(self.run_job(j), "done")
        self.assertEqual(markers.read(self.c.marker_path(j))[-1]["outputs"][0]["sha256"], done["outputs"][0]["sha256"])

    def test_failure_cleans_up(self):
        j = self.c.jobs[1]
        j.command += " --fail"
        self.assertEqual(self.run_job(j), "failed")
        self.assertFalse(self.c.scratch_dir(j).exists())
        self.assertFalse(list(self.c.final_dir(j).glob("*.part")))
        self.assertEqual(markers.read(self.c.marker_path(j))[-1]["exit_code"], 1)

    def test_missing_output(self):
        j = self.c.jobs[2]
        j.command = "true"
        self.assertEqual(self.run_job(j), "failed")
        self.assertIn("missing output", markers.read(self.c.marker_path(j))[-1]["reason"])

    def test_timeout(self):
        j = self.c.jobs[0]
        j.command, j.timeout_s = "sleep 30", 2
        self.assertEqual(self.run_job(j), "timeout")
        r = markers.read(self.c.marker_path(j))[-1]
        self.assertLess(r["wall_s"], 10)
        self.assertFalse(self.c.scratch_dir(j).exists())

    def test_stale_part_and_scratch_removed(self):
        j = self.c.jobs[1]
        fsops.makedirs_final(self.c.final_dir(j))
        stale = self.c.final_dir(j) / (j.outputs[0] + ".part")
        stale.write_text("stale")
        fsops.makedirs_final(self.c.scratch_dir(j))
        (self.c.scratch_dir(j) / "junk").write_text("junk")
        markers.append(self.c.marker_path(j), {"status": "started", "pid": 1})
        self.assertEqual(self.run_job(j), "done")
        self.assertFalse(stale.exists())
        self.assertEqual(markers.state(markers.read(self.c.marker_path(j)))[2], 2)

    def test_accounting_matches_rusage(self):
        j = self.c.jobs[0]
        j.command = f"{PY} {PAYLOAD} --mem-mib 64 --hold 0 --out {j.outputs[0]}"
        self.assertEqual(self.run_job(j), "done")
        r = markers.read(self.c.marker_path(j))[-1]
        self.assertGreater(r["max_rss_mb"], 60)
        self.assertLess(r["max_rss_mb"], 120)


class TestIOResilience(unittest.TestCase):
    def setUp(self):
        self.c = campaign.from_dict(camp_dict(campaign=f"ut-io-{self._testMethodName[-10:].replace('_', '-')}"))
        self.orig = wrapper.copy_to_part_and_rename
        self.budget, self.first = wrapper.IO_BUDGET_S, wrapper.IO_FIRST_WAIT_S
        wrapper.IO_FIRST_WAIT_S = 0.05

    def tearDown(self):
        wrapper.copy_to_part_and_rename = self.orig
        wrapper.IO_BUDGET_S, wrapper.IO_FIRST_WAIT_S = self.budget, self.first

    def flaky(self, n_fail):
        calls = {"n": 0}

        def f(*a, **k):
            calls["n"] += 1
            if calls["n"] <= n_fail:
                raise OSError(5, "Input/output error (simulated cajuela outage)")
            return self.orig(*a, **k)
        wrapper.copy_to_part_and_rename = f
        return calls

    def test_transient_outage_is_retried(self):
        j = self.c.jobs[0]
        wrapper.IO_BUDGET_S = 30
        calls = self.flaky(2)
        self.assertEqual(wrapper.Runner(self.c, j, "local", mem_limit_mb=0).run(), "done")
        self.assertEqual(calls["n"], 3)

    def test_long_outage_keeps_work_then_resumes_without_rerun(self):
        j = self.c.jobs[1]
        counter = ROOT / f"count-{j.id}"
        j.command += f" && echo x >> {counter}"
        wrapper.IO_BUDGET_S = 0.3
        self.flaky(10**6)
        self.assertEqual(wrapper.Runner(self.c, j, "local", mem_limit_mb=0).run(), "io_error")
        self.assertTrue((self.c.scratch_dir(j) / wrapper.STASH).is_file(), "finished work must be kept")
        self.assertEqual(markers.state(markers.read(self.c.marker_path(j)))[0], "retryable")
        self.assertFalse(list(self.c.final_dir(j).glob("*.dat")), "no output may appear without a marker")
        wrapper.copy_to_part_and_rename = self.orig
        self.assertEqual(wrapper.Runner(self.c, j, "local", mem_limit_mb=0).run(), "done")
        self.assertEqual(counter.read_text().count("x"), 1, "command must not run twice")
        recs = markers.read(self.c.marker_path(j))
        self.assertTrue(recs[-2]["resumed_from_stash"])
        self.assertFalse(self.c.scratch_dir(j).exists())


class TestLedgerManifest(unittest.TestCase):
    def test_rebuild_and_manifest(self):
        c = campaign.from_dict(camp_dict(campaign="ut-ledger", n=2))
        for j in c.jobs:
            self.assertEqual(wrapper.Runner(c, j, "local", mem_limit_mb=0).run(), "done")
        out = ROOT / "jobs.tsv"
        n = ledger.rebuild(c.ledger, out)
        rows = out.read_text().splitlines()
        self.assertEqual(rows[0].split("\t"), list(ledger.COLUMNS))
        self.assertGreaterEqual(n, 2)
        self.assertTrue(any(r.startswith("ut-000\tut-ledger\tlocal") for r in rows))
        buf = io.StringIO()
        row, msha, size, nfiles, missing = manifest.write_manifest(c, verify=True, out=buf)
        self.assertEqual(nfiles, 2)
        self.assertEqual(missing, [])
        self.assertTrue((c.campaign_dir() / "MANIFEST").is_file())
        self.assertIn("| ut-ledger |", row)
        tot, nf, per = manifest.usage([c.ledger], out=io.StringIO())
        self.assertEqual(per["ut-ledger"], [size, 2])


class TestNodes(unittest.TestCase):
    def test_graphical(self):
        self.assertTrue(nodes.is_graphical(["jochoaf  seat0        2026-11-13 13:41 (login screen)"]))
        self.assertTrue(nodes.is_graphical(["bob      :0           2026-11-13 13:41 (:0)"]))
        self.assertFalse(nodes.is_graphical(["bob      pts/0        2026-11-13 13:41 (192.168.10.5)"]))

    def test_parse_and_cap(self):
        load, who, ours = nodes.parse_probe("1.20 0.5 0.3 2/300 1234\n--who\nx seat0 d (login screen)\n--ours\n1\n")
        self.assertEqual((load, ours), (1.2, 1))
        self.assertEqual(nodes.node_cap(0.0, False, 0), 4)
        self.assertEqual(nodes.node_cap(0.0, True, 0), 3)
        self.assertEqual(nodes.node_cap(2.0, False, 0), 2)    # 2 foreign busy cores
        self.assertEqual(nodes.node_cap(2.0, False, 2), 4)    # the load is our own jobs
        self.assertEqual(nodes.node_cap(3.9, True, 0), 0)

    def test_time_cap(self):
        tz = nodes.TZ
        self.assertEqual(nodes.time_cap(dt.datetime(2026, 11, 13, 10, 0, tzinfo=tz)), 9)     # Friday 10:00
        self.assertEqual(nodes.time_cap(dt.datetime(2026, 11, 13, 19, 30, tzinfo=tz)), 12)   # Friday 19:30
        self.assertEqual(nodes.time_cap(dt.datetime(2026, 11, 14, 10, 0, tzinfo=tz)), 12)    # Saturday
        self.assertEqual(nodes.time_cap(dt.datetime(2026, 11, 13, 7, 0, tzinfo=tz), 1.5), 9)  # runs into 08:00
        self.assertEqual(nodes.time_cap(dt.datetime(2026, 11, 15, 22, 0, tzinfo=tz), 10), 9)  # Sun 22:00 + 10 h reaches Mon 08:00
        self.assertEqual(nodes.time_cap(dt.datetime(2026, 11, 15, 22, 0, tzinfo=tz), 8), 12)


class TestArgoRender(unittest.TestCase):
    def test_render_spec(self):
        c = campaign.from_dict(camp_dict(n=5, campaign="ut-argo"))
        c.jobs[0].max_rss_mb = 1600
        wf = argo.render(c, c.jobs, 0, 9, allowed_nodes=["landau"], suffix="abcde")
        m, s = wf["metadata"], wf["spec"]
        self.assertTrue(m["name"].startswith("jdochoa-qv2-ut-argo-c0-"))
        self.assertLessEqual(len(m["name"]), 63)
        self.assertEqual(m["labels"]["owner"], "jdochoa")
        self.assertEqual(m["labels"]["study"], "quirks-v2")
        self.assertEqual(s["podMetadata"]["labels"]["owner"], "jdochoa")
        self.assertEqual(s["securityContext"], {"runAsUser": 10015, "runAsGroup": 10000})
        self.assertEqual(s["podGC"], {"strategy": "OnPodSuccess"})
        self.assertEqual(s["ttlStrategy"], {"secondsAfterCompletion": 86400})
        self.assertEqual(s["parallelism"], 9)
        vols = {v["name"]: v for v in s["volumes"]}
        self.assertEqual(vols["home"]["nfs"], {"server": "192.168.10.254", "path": "/home/users/jdochoa"})
        self.assertEqual(vols["data"]["nfs"]["path"], "/mnt/cajuela/jdochoa/quirks_v2")
        self.assertEqual(vols["scratch"]["hostPath"], {"path": "/home/scratch/jdochoa", "type": "Directory"})
        t = s["templates"][1]
        self.assertEqual(t["activeDeadlineSeconds"], 2400)
        self.assertEqual(t["retryStrategy"], {"limit": 2, "retryPolicy": "OnError"})
        ct = t["container"]
        self.assertEqual(ct["image"], paths.IMAGE)
        self.assertEqual(ct["imagePullPolicy"], "IfNotPresent")
        self.assertEqual(ct["command"][:3], ["nice", "-n", "10"])
        self.assertIn("umask 022", ct["args"][0])
        mounts = {v["name"]: v["mountPath"] for v in ct["volumeMounts"]}
        self.assertEqual(mounts, {"home": "/home/users/jdochoa", "data": "/nfs/cajuela/jdochoa/quirks_v2",
                                  "scratch": "/home/scratch/jdochoa"})
        self.assertEqual(ct["resources"]["requests"]["cpu"], "1")
        res = {tt["name"]: tt["container"]["resources"] for tt in s["templates"][1:]}
        self.assertIn({"requests": {"cpu": "1", "memory": "1600Mi"}, "limits": {"memory": "2400Mi"}}, res.values())
        self.assertIn({"requests": {"cpu": "1", "memory": "50Mi"}, "limits": {"memory": "75Mi"}}, res.values())
        ids = sorted(i for st in s["templates"][0]["steps"][0] for i in st["withItems"])
        self.assertEqual(ids, [j.id for j in c.jobs])
        self.assertNotIn("pvc", json.dumps(wf).lower().replace("pvc-mynfs", "FORBIDDEN"))

    def test_limits(self):
        c = campaign.from_dict(camp_dict(n=1201, campaign="ut-chunks"))
        ch = argo.chunks(c)
        self.assertEqual([len(x) for x in ch], [500, 500, 201])
        with self.assertRaises(ValueError):
            argo.render(c, c.jobs[:10], 0, 13)
        with self.assertRaises(ValueError):
            argo.render(c, c.jobs[:501], 0, 4)
        with self.assertRaises(ValueError):
            argo.delete("someone-elses-workflow")


class TestBundleRotation(unittest.TestCase):
    def test_keep_last_and_gates(self):
        dest = ROOT / "backup"
        dest.mkdir(exist_ok=True)
        for d in range(1, 10):
            (dest / f"repo-2026-10-0{d}.bundle").write_text("x")
        (dest / "gate-A-2026-10-01.bundle").write_text("g")
        final, h, size, removed = bundle_mod.bundle(dest=dest, keep=7, out=io.StringIO(), date="2026-10-10")
        left = sorted(p.name for p in dest.glob("*.bundle"))
        self.assertIn("gate-A-2026-10-01.bundle", left)
        self.assertEqual(len([x for x in left if x.startswith("repo-")]), 7)
        self.assertIn("repo-2026-10-10.bundle", left)
        self.assertFalse(list(dest.glob("*.part")))
        self.assertEqual(h, fsops.sha256_file(final))


if __name__ == "__main__":
    unittest.main()
