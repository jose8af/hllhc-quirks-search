"""G1b: apply the ADDITIVE run_stage4.py hook for the G1b job kinds (HASH_ADDENDUM.md).  Exact string replacements;
refuses unless the file has the frozen sha256 85b978f5... and every anchor is found exactly once; refuses while a
run_stage4 production run is alive (G3: its outputs record the run_stage4.py sha256 at job end).

  pixi run python acts/stage4/validation/g1b_apply_hook.py [--check-only] [--target PATH]
"""
import hashlib
import subprocess
import sys
from pathlib import Path

TT = Path(__file__).resolve().parents[3]
TARGET = TT / 'acts' / 'stage4' / 'run_stage4.py'
OLD_SHA = '85b978f5d85cee28d290d298bb96bb9895299f916bc4df632a9cf2bb66a4879e'

EDITS = [
    # 1. new kinds are runnable (additive constant)
    ("RUNNABLE = ('pu', 'sm', 'dens')\n",
     "RUNNABLE = ('pu', 'sm', 'dens')\n"
     "G1B_KINDS = ('a1', 'a2', 'a5', 'cp0', 'cppu')      # G1b (run_g1b.py, HASH_ADDENDUM.md): signal A1/A2/A5, C'0, C'_PU\n"
     "G1B_REPLACES = ('A1', 'A2core', 'A5core', 'Cp0', 'CpPU')    # G1_BLOCKS placeholders replaced by G1b jobs\n"
     "RUNNABLE = RUNNABLE + G1B_KINDS\n"),
    # 2. manifest: G1b jobs appended; their placeholder blocks skipped
    ("    for name, desc, cpuh in G1_BLOCKS[camp]:\n"
     "        if name == 'C' and SM_BLOCKS.get(camp):\n"
     "            continue                      # replaced by the per-job SM manifest above\n",
     "    from acts.stage4 import run_g1b as _G1B          # G1b kinds (HASH_ADDENDUM.md)\n"
     "    g1b_jobs = _G1B.manifest_jobs(camp)\n"
     "    jobs.extend(g1b_jobs)\n"
     "    for name, desc, cpuh in G1_BLOCKS[camp]:\n"
     "        if name == 'C' and SM_BLOCKS.get(camp):\n"
     "            continue                      # replaced by the per-job SM manifest above\n"
     "        if g1b_jobs and name in G1B_REPLACES:\n"
     "            continue                      # replaced by the G1b per-job manifest\n"),
    # 3. validate: G1b outputs have their own completeness keys
    ("def validate(job, deep=False):\n    p = out_path(job)\n",
     "def validate(job, deep=False):\n"
     "    if job['kind'] in G1B_KINDS:\n"
     "        from acts.stage4 import run_g1b as _G1B\n"
     "        return _G1B.validate(job, deep)\n"
     "    p = out_path(job)\n"),
    # 4. worker dispatch
    ("def _safe_run(job, allow_interim):\n    try:\n        return run_pu_job(job, allow_interim)\n",
     "def _safe_run(job, allow_interim):\n"
     "    try:\n"
     "        if job['kind'] in G1B_KINDS:\n"
     "            from acts.stage4 import run_g1b as _G1B\n"
     "            return _G1B.run_job(job, allow_interim)\n"
     "        return run_pu_job(job, allow_interim)\n"),
    # 5. dependencies may be a list (C'_PU needs every C'0 job of its topology)
    ("                if j.get('needs') and not PROD.joinpath(*j['needs'].split('/')).is_file():\n",
     "                if j.get('needs') and not all(PROD.joinpath(*p_.split('/')).is_file() for p_ in\n"
     "                                              ([j['needs']] if isinstance(j['needs'], str) else j['needs'])):\n"),
    # 6. check: V4-10 of the C' outputs reported next to V4-1
    ("    print(f'{len(jobs)} PU-only jobs: {len(jobs) - len(bad) - len(missing)} valid, {len(bad)} invalid, {len(missing)} missing; '\n"
     "          f'V4-1 failures: {len(v41_fail)}')\n",
     "    print(f'{len(jobs)} PU-only jobs: {len(jobs) - len(bad) - len(missing)} valid, {len(bad)} invalid, {len(missing)} missing; '\n"
     "          f'V4-1 failures: {len(v41_fail)}')\n"
     "    v410_fail = []\n"
     "    for j in jobs:\n"
     "        if j['kind'] in ('cp0', 'cppu') and out_path(j).exists() and j['id'] not in bad:\n"
     "            from acts.stage4 import run_g1b as _G1B\n"
     "            if _G1B.check_job(j).get('v410_pass') is False:\n"
     "                v410_fail.append(j['id'])\n"
     "    if any(j['kind'] in ('cp0', 'cppu') for j in jobs):\n"
     "        print(f'V4-10 failures (C\\'0 leak / C\\'_PU hash): {len(v410_fail)}')\n"
     "        for b in v410_fail[:20]:\n"
     "            print('  V4-10 FAIL:', b)\n"
     "        bad = bad + v410_fail\n"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv):
    check_only = '--check-only' in argv
    target = Path(argv[argv.index('--target') + 1]) if '--target' in argv else TARGET
    if target == TARGET and not check_only:
        ps = subprocess.run(['pgrep', '-f', 'acts.stage4.run_stage4 run'], capture_output=True, text=True).stdout.split()
        if ps:
            print('REFUSED: a run_stage4 run is alive (PIDs %s); apply after it ends' % ' '.join(ps))
            return 2
    if sha(target) != OLD_SHA:
        print('REFUSED: %s sha256 %s != frozen %s' % (target, sha(target), OLD_SHA))
        return 2
    s = target.read_text()
    for old, new in EDITS:
        if s.count(old) != 1:
            print('REFUSED: anchor found %d times:\n%s' % (s.count(old), old))
            return 2
        s = s.replace(old, new)
    if check_only:
        print('check-only: all %d anchors found once; new sha256 would be %s'
              % (len(EDITS), hashlib.sha256(s.encode()).hexdigest()))
        return 0
    target.write_text(s)
    print('applied %d edits: %s -> %s' % (len(EDITS), OLD_SHA, sha(target)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
