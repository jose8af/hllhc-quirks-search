"""reshower.py -- deterministic re-shower of kept Stage-2 LHE events (fixer S2-R1, 2026-10-11).

Every npz row can be traced back to its LHE event and Pythia job (columns `chunk`, `ievt_lhe`, `py8_job`, `ievt_job`,
`py8_seed`; written by scripts/add_rowmap.py; `py8_job` = j of split_<j> below; corrected S2-R2 C-6).  This script rebuilds the split LHE file of one Pythia job from the kept
chunk LHE (data/sim/lhe/<ID>/m<m>_c<k>.lhe.gz; the split is the same deterministic cut as produce.split_lhe) and reruns
the MG5aMC_PY8_interface with the card stored in data/sim/aux/<ID>/m<m>_c<k>/split_<j>/PY8Card.dat (same seed), optionally
with extra / replaced Pythia settings.  Uses:
  * Stage 4: regenerate the full particle record (HepMC) of selected rows (B-5): a Pythia job must be rerun from the start
    of its split (the random stream is sequential), then event `ievt_job` of that job is the row.  --keep-hepmc keeps it.
  * V-SHOWER (ISR/FSR renormalisation-scale variations) and the QED-FSR test: --set 'Key = value' (repeatable).
Run (sim/, system python3; calls the pixi envs):
  python3 scripts/reshower.py --id E-TRG --m 500 --chunk 0 [--splits 0,1,...] --out <dir> [--set 'X = y' ...]
          [--convert out_prefix] [--keep-hepmc]
Output: <dir>/split_<j>/{events.hepmc, PY8_log.txt, PY8Card.dat}; with --convert, <out_prefix>_s<j>.npz in the converter
format (norm 'auto', same arguments as produce.py) and the HepMC is deleted unless --keep-hepmc.
"""
import argparse
import gzip
import json
import os
import subprocess
import sys
import time

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.normpath(os.path.join(SIM, '..', 'data', 'sim'))
sys.path.insert(0, os.path.join(SIM, 'scripts'))
from produce import MG, PY8_EXE, NJOBS, env  # noqa


def split_events(lhe, k=NJOBS):
    """Same cut as produce.split_lhe: returns (header, [list of event strings per split])."""
    with gzip.open(lhe, 'rt') as f:
        txt = f.read()
    i0 = txt.index('<event>')
    head = txt[:i0]
    body = txt[i0:txt.rindex('</LesHouchesEvents>')]
    evs = [e + '</event>\n' for e in body.split('</event>') if '<event>' in e]
    n = len(evs)
    sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]
    out, s = [], 0
    for sz in sizes:
        out.append(evs[s:s + sz]); s += sz
    return head, out


def card(id_, m, chunk, j, sets):
    src = os.path.join(DATA, 'aux', id_, f'm{m}_c{chunk}', f'split_{j}', 'PY8Card.dat')
    L = open(src).read().rstrip('\n').split('\n')
    keys = {s.split('=')[0].strip(): s for s in sets}
    out, used = [], set()
    for l in L:
        k = l.split('=')[0].strip()
        if k in keys:
            out.append(keys[k]); used.add(k)
        else:
            out.append(l)
    # extra settings go before the LHEF/seed block (order does not matter for these keys; Tune:pp stays first)
    extra = [keys[k] for k in keys if k not in used]
    i = next(n for n, l in enumerate(out) if l.startswith('Beams:frameType'))
    return '\n'.join(out[:i] + extra + out[i:]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True); ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--chunk', type=int, required=True); ap.add_argument('--splits', default=None)
    ap.add_argument('--out', required=True); ap.add_argument('--set', action='append', default=[])
    ap.add_argument('--convert', default=None); ap.add_argument('--keep-hepmc', action='store_true')
    ap.add_argument('--max-events', type=int, default=None, help='shower only the first N events of each split')
    a = ap.parse_args()
    lhe = os.path.join(DATA, 'lhe', a.id, f'm{a.m}_c{a.chunk}.lhe.gz')
    done = json.load(open(os.path.join(DATA, 'npz', 'chunks', a.id, f'm{a.m}_c{a.chunk}.done.json')))
    head, splits = split_events(lhe)
    assert sum(len(s) for s in splits) == done['n_lhe'], 'kept LHE does not match the chunk record'
    js = [int(x) for x in a.splits.split(',')] if a.splits else list(range(len(splits)))
    e = env(); e['DYLD_LIBRARY_PATH'] = os.path.join(MG, 'HEPTools', 'lib') + ':' + e.get('DYLD_LIBRARY_PATH', '')
    jobs = []
    t0 = time.time()
    for j in js:
        d = os.path.join(a.out, f'split_{j}'); os.makedirs(d, exist_ok=True)
        evs = splits[j] if a.max_events is None else splits[j][:a.max_events]
        with gzip.open(os.path.join(d, 'events.lhe.gz'), 'wt', compresslevel=1) as g:
            g.write(head); g.writelines(evs); g.write('</LesHouchesEvents>\n')
        c = card(a.id, a.m, a.chunk, j, a.set)
        if a.max_events is not None:
            c = '\n'.join(f'Main:numberOfEvents = {len(evs)}' if l.startswith('Main:numberOfEvents') else l for l in c.split('\n'))
        open(os.path.join(d, 'PY8Card.dat'), 'w').write(c)
        lf = open(os.path.join(d, 'PY8_log.txt'), 'w')
        jobs.append((subprocess.Popen([PY8_EXE, 'PY8Card.dat'], cwd=d, stdout=lf, stderr=subprocess.STDOUT, env=e), d, j, len(evs)))
    conv = []
    for p, d, j, n in jobs:
        rc = p.wait()
        if rc != 0:
            raise RuntimeError(f'PY8 failed in {d}')
        if a.convert:
            mn = None
            for l in open(os.path.join(d, 'PY8Card.dat')):
                if l.startswith('JetMatching:qCut'):
                    mn = f'{float(l.split("=")[1]):.3f}'
            cmd = ['pixi', 'run', '-e', 'ana', 'python', os.path.join(SIM, 'scripts', 'convert_hepmc.py'), os.path.join(d, 'events.hepmc'),
                   f'{a.convert}_s{j}.npz', '--mq', str(a.m), '--spin', 'S' if a.id.startswith('S') else 'F',
                   '--sigma-lhe-pb', repr(done['sigma_lhe_pb']), '--nlhe', str(n), '--tag', f'reshower_{a.id}_m{a.m}_c{a.chunk}_s{j}',
                   '--norm', 'auto'] + (['--merging-nominal', mn] if mn else [])
            conv.append((subprocess.Popen(cmd, cwd=SIM, stdout=open(os.path.join(d, 'convert.log'), 'w'), stderr=subprocess.STDOUT), d))
    for p, d in conv:
        if p.wait() != 0:
            raise RuntimeError(f'conversion failed in {d}')
        if not a.keep_hepmc:
            os.remove(os.path.join(d, 'events.hepmc'))
    print(f'reshower {a.id} m={a.m} c{a.chunk} splits {js}: {time.time() - t0:.0f} s wall; settings {a.set}')


if __name__ == '__main__':
    main()
