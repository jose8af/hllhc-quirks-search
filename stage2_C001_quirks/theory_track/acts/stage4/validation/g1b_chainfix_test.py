"""G1b navigation-assertion fix: determinism test (HASH_ADDENDUM.md).
  (1) frozen run_chain.py vs patched (candidate or applied) without replacement: every array bit-identical;
  (2) patched with --replace-event 1: events 0 and 2 bit-identical to (1), event 1 replaced, meta records it.
  PYTHONPATH=. pixi run python -m acts.stage4.validation.g1b_chainfix_test <frozen chain .py> <patched chain .py>
-> data/acts_stage4/g1b/navfix/chainfix_test.json
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
OUT = TT / 'data' / 'acts_stage4' / 'g1b' / 'navfix'
SEED = 424242
N = 3


def run(script, tag, extra=()):
    out = OUT / f'test_{tag}.npz'
    cmd = ['pixi', 'run', '--manifest-path', str(TT / 'acts' / 'pixi.toml'), 'python', str(script), 'pu', str(out), str(N),
           str(SEED)] + list(extra)
    p = subprocess.run(cmd, cwd=str(TT / 'acts'), capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])
    return np.load(out)


def same(a, b, k):
    return a[k].dtype == b[k].dtype and a[k].shape == b[k].shape and a[k].tobytes() == b[k].tobytes()


def main(frozen, patched):
    OUT.mkdir(parents=True, exist_ok=True)
    a = run(frozen, 'frozen'); b = run(patched, 'patched'); c = run(patched, 'replace1', ['--replace-event', '1'])
    skip = {'meta', 'timing'}
    keys = sorted(set(a.files) - skip)
    r = dict(t1_identical_keys=[k for k in keys if same(a, b, k)], t1_diff_keys=[k for k in keys if not same(a, b, k)])
    ev_keys = lambda i: [k for k in keys if k.endswith(str(i)) and k[:-1] in ('ev', 'tru', 'vz', 'lost', 'toy', 'mom')]  # noqa
    r['t2_events_0_2_identical'] = all(same(a, c, k) for i in (0, 2) for k in ev_keys(i))
    r['t2_event_1_differs'] = not all(same(a, c, k) for k in ev_keys(1))
    mc = json.loads(str(c['meta']))
    r['t2_meta_replaced_events'] = mc.get('replaced_events')
    r['t2_event_seeds'] = mc.get('event_seeds')
    r['t1_meta_has_no_replaced'] = 'replaced_events' not in json.loads(str(b['meta']))
    r['pass'] = bool(not r['t1_diff_keys'] and r['t2_events_0_2_identical'] and r['t2_event_1_differs']
                     and r['t2_meta_replaced_events'] and r['t1_meta_has_no_replaced'])
    (OUT / 'chainfix_test.json').write_text(json.dumps(r, indent=1))
    print(json.dumps({k: v for k, v in r.items() if k != 't1_identical_keys'}, indent=1))


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
