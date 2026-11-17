"""marker_files.py -- list the output files of a campaign from its `done` marker lines (ledger rule: a file without a
done marker does not exist).  Channel (ii), executor Edgar, 2026-11-17.  Stdlib only.

done_outputs(campaign, suffix=None, prefix=None, verify=False) -> sorted list of output paths whose job's LAST marker
line has status 'done'; optional filters on the file name; verify=True re-checks the sha256 of each file.
"""
import glob
import hashlib
import json
import os

LEDGER = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/ledger/markers'


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def done_outputs(campaign, suffix=None, prefix=None, verify=False):
    out = []
    for mk in sorted(glob.glob(os.path.join(LEDGER, campaign, '[0-9][0-9][0-9]', '*.marker'))):
        lines = [x for x in open(mk).read().splitlines() if x.strip()]
        if not lines:
            continue
        last = json.loads(lines[-1])
        if last.get('status') != 'done':
            continue
        for o in last.get('outputs', []):
            name = o['name']
            if suffix and not name.endswith(suffix):
                continue
            if prefix and not name.startswith(prefix):
                continue
            if verify and _sha256(o['path']) != o['sha256']:
                raise SystemExit(f'sha256 mismatch: {o["path"]}')
            out.append(o['path'])
    return sorted(out)
