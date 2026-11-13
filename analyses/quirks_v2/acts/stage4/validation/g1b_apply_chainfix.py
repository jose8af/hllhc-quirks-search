"""G1b: ADDITIVE run_chain.py fix for the ACTS navigation assertion seen in G3 (G3B1_00021, G3B1_00059):
  RuntimeError: Checking volume outside of bounds: Assertion 'surface().insideBounds(position, BoundaryTolerance::None())'
  failed in GridPortalLink.hpp:584   (raised from Sequencer.run(); the whole chain job died)

Fix (HASH_ADDENDUM.md): if s.run() raises THIS assertion, the first event without a Dump record is the failing event k;
the whole chain job is re-run in-process (fresh geometry and sequencer) with event k's generator seed replaced by
hseed('nav-replace', mode, job seed, k, old seed) (deterministic), up to 5 replacements per job.  Every other event
is bit-identical (the Fatras/digitisation RNG is keyed by (job seed, event number), Pythia by the event seed; checked:
validation/g1b_chainfix_test.py).  The replaced events (event, old seed, new seed, reason) are recorded in the chain
meta ('replaced_events') and hence in the job output meta.  A job that never hits the assertion executes exactly
the old code path (bit-identical output; regression g1b_regress).

  pixi run python acts/stage4/validation/g1b_apply_chainfix.py [--check-only] [--target PATH]
"""
import hashlib
import subprocess
import sys
from pathlib import Path

TT = Path(__file__).resolve().parents[3]
TARGET = TT / 'acts' / 'stage4' / 'code' / 'run_chain.py'
OLD_SHA = 'b1130b40f6c729a1145d23ad15b8a176060d0cf3b718e8794f2efe5a9819e8c0'

HELPER = '''
NAV_ERR = 'insideBounds'          # G1b fix (HASH_ADDENDUM.md): ACTS GridPortalLink navigation assertion
MAX_REPLACE = 5


def _apply_replace(ev_seeds, a, meta, tag):
    """G1b fix: replace the generator seed of the events listed in --replace-event (deterministic new seed)."""
    rep = []
    for k in a.replace_event:
        old = int(ev_seeds[k])
        new = s4pu.hseed('nav-replace', tag, a.seed, k, old, mod=2 ** 62)
        ev_seeds[k] = new
        rep.append(dict(event=int(k), old_seed=old, new_seed=int(new),
                        reason="ACTS navigation assertion (GridPortalLink insideBounds) in this event's original run"))
    if rep:
        meta['replaced_events'] = rep
    return ev_seeds


def _failed_event(store, n):
    for i in range(n):
        if 'ev' not in store.get(i, {}):
            return i
    return None


def main(argv=None):
'''

EDITS = [
    ("\n\ndef main(argv=None):\n", "\n" + HELPER),
    ("    ap.add_argument('--no-pu', action='store_true', help='sig: no PU (A1)')\n",
     "    ap.add_argument('--no-pu', action='store_true', help='sig: no PU (A1)')\n"
     "    ap.add_argument('--replace-event', type=int, action='append', default=[],\n"
     "                    help='G1b fix: replace this event\\'s generator seed (set automatically after a navigation assertion)')\n"),
    ("                assert len(ev_seeds) == a.n_events\n            meta['event_seeds'] = ev_seeds\n",
     "                assert len(ev_seeds) == a.n_events\n            _apply_replace(ev_seeds, a, meta, 'pu')\n"
     "            meta['event_seeds'] = ev_seeds\n"),
    ("                ev_seeds = [s4pu.hseed('sigpu', spin, P.m, r, mod=2 ** 62) for r in rows]\n",
     "                ev_seeds = [s4pu.hseed('sigpu', spin, P.m, r, mod=2 ** 62) for r in rows]\n"
     "                _apply_replace(ev_seeds, a, meta, 'sig')\n"),
    ("            ev_seeds = [s4pu.hseed('sm', a.sample, a.seed, i, mod=2 ** 62) for i in range(a.n_events)]\n",
     "            ev_seeds = [s4pu.hseed('sm', a.sample, a.seed, i, mod=2 ** 62) for i in range(a.n_events)]\n"
     "            _apply_replace(ev_seeds, a, meta, 'sm')\n"),
    ("            ev_seeds = [s4pu.hseed('cp0', a.topo, a.seed, i, mod=2 ** 62) for i in range(a.n_events)]\n",
     "            ev_seeds = [s4pu.hseed('cp0', a.topo, a.seed, i, mod=2 ** 62) for i in range(a.n_events)]\n"
     "            _apply_replace(ev_seeds, a, meta, 'cp0')\n"),
    ("            ev_seeds = [s4pu.hseed('cppu', mc['topo'], mc['job_seed'], e, a.seed, mod=2 ** 62) for e in evs]\n",
     "            ev_seeds = [s4pu.hseed('cppu', mc['topo'], mc['job_seed'], e, a.seed, mod=2 ** 62) for e in evs]\n"
     "            _apply_replace(ev_seeds, a, meta, 'cppu')\n"),
    ("        s.run()\n",
     "        try:\n"
     "            s.run()\n"
     "        except RuntimeError as exc:          # G1b fix (HASH_ADDENDUM.md): rerun with the failing event replaced\n"
     "            k = _failed_event(store, a.n_events)\n"
     "            if (NAV_ERR not in str(exc) or k is None or k in a.replace_event or len(a.replace_event) >= MAX_REPLACE\n"
     "                    or a.mode == 'gun'):\n"
     "                raise\n"
     "            print(f'[run_chain] navigation assertion in event {k}; rerunning the job with that event replaced',\n"
     "                  file=sys.stderr, flush=True)\n"
     "            TIMES.clear()\n"
     "            return main(list(sys.argv[1:] if argv is None else argv) + ['--replace-event', str(k)])\n"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv):
    check_only = '--check-only' in argv
    target = Path(argv[argv.index('--target') + 1]) if '--target' in argv else TARGET
    if target == TARGET and not check_only:
        ps = subprocess.run(['pgrep', '-f', 'run_stage4 run'], capture_output=True, text=True).stdout.split()
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
