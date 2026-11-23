"""cpu_attrib_campaigns.py -- NI C'_PU campaigns for the C'_PU attribution measurement (Eskil, 2026-11-19).
Same job form as p2-a-c1-cppua (c1_cp_job.py --kind cppu, 40 slots per job, --sources auto); topo ni22, 1,000 slots,
split into p2-a-c1-cppuni-a (chunks 0-12) and -b (13-24).  Plan: outputs/CPU_ATTRIB_PLAN_eskil_2026-11-19.md addendum.
  python3 -I phase2_exploration/src/cpu_attrib_campaigns.py"""
import json
from pathlib import Path

CAMP = Path("/home/users/jdochoa/hllhc-quirks-search/tools/runner/campaigns")
ref = json.loads((CAMP / "p2-a-c1-cppua.json").read_text())
cmd0 = ref["jobs"][0]["command"]
pre = cmd0[:cmd0.index("--id")]
for name, chunks in (("p2-a-c1-cppuni-a", range(0, 13)), ("p2-a-c1-cppuni-b", range(13, 25))):
    jobs = []
    for ch in chunks:
        jid = f"c1cppu-ni22-{ch:03d}"
        jobs.append(dict(id=jid, shard=0, outputs=[f"{jid}.npz"],
                         command=f"{pre}--id {jid} --kind cppu --topo ni22 --chunk {ch} --start {40 * ch} --n 40 "
                                 "--sources auto"))
    d = dict(campaign=name, tier="final", data_prefix="phase2",
             description="C'_PU attribution (Eskil, approved 2026-11-19): NI 22 mm C'_PU, PU 200 overlays of preselected "
                         "C'_0 ni22 events of p2-a-c1-cp0 (v1 run_g1b cppu unchanged), 1,000 slots in 25 jobs of 40; "
                         "stream c1.cpu",
             expected_hours=4.0, regenerate="python3 -I phase2_exploration/src/cpu_attrib_campaigns.py",
             defaults=dict(max_rss_mb=1500, timeout_s=1800), jobs=jobs)
    (CAMP / f"{name}.json").write_text(json.dumps(d, indent=1) + "\n")
    print(name, len(jobs))
