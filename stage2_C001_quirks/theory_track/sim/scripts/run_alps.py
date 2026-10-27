"""run_alps.py -- MG standalone `systematics` with the emission-alpha_s variation (--alps=0.5,1,2) on the kept LHE of the
benchmark points (review S2-R1 B-1 / constructive B-1(1); fixer 2026-10-11).

In MLM (ickkw = 1) MG evaluates alpha_s of each extra ME parton at its CKKW clustering scale; `--alps` rescales those
scales (x0.5, x2), which the production `--mur` weights do NOT do (they rescale only the hard-process alpha_s, absent in
Drell-Yan-like production).  Per kept LHE event we store r = w(alps)/w(central); the merged weight of a row is then
w_row * r[ievt_lhe] (the Pythia MLM veto does not depend on the LHE weights).  Rows are mapped with the columns written by
scripts/add_rowmap.py (chunk, ievt_lhe).
Run (sim/): pixi run -e ana python scripts/run_alps.py [ID_m<m> ...]   (default: E/S INC and TRG at 200, 500, 1000 GeV)
Output: ../data/sim/aux/fixer/alps/<ID>_m<m>_c<k>.npz with r_alps0p5, r_alps2 (float64, length N_LHE of the chunk), plus
the MG cross-section summary in the same directory (.log).  The rewritten LHE is a temporary file (deleted).
"""
import glob
import gzip
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.normpath(os.path.join(SIM, '..', 'data', 'sim'))
OUT = os.path.join(DATA, 'aux', 'fixer', 'alps')
DEFAULT = [f'{p}-{k}_m{m}' for p in ('E', 'S') for k in ('INC', 'TRG') for m in (200, 500, 1000)]
WGT = re.compile(r"<wgt id='(\d+)'>\s*([-+0-9.eE]+)\s*</wgt>")


def one(id_, m, lhe):
    k = int(re.search(r'_c(\d+)\.lhe', lhe).group(1))
    dst = os.path.join(OUT, f'{id_}_m{m}_c{k}.npz')
    if os.path.exists(dst):
        return f'skip {dst}'
    proc = ('F' if id_.startswith('E') else 'S') + ('_TRG' if 'TRG' in id_ else '_INC')
    tool = os.path.join(SIM, 'mg_out', f'prod_{proc}', 'bin', 'internal', 'systematics.py')
    tmp = tempfile.NamedTemporaryFile(suffix='.lhe', dir=OUT, delete=False).name
    env = dict(os.environ, LHAPDF_DATA_PATH=os.path.join(DATA, 'lhapdf'), PYTHONDONTWRITEBYTECODE='1')
    r = subprocess.run(['pixi', 'run', '-e', 'mg', 'python', tool, lhe, tmp, '--mur=1', '--muf=1', '--dyn=-1', '--pdf=CT18NLO@0',
                        '--alps=0.5,1,2', '--remove_wgts=all'], cwd=SIM, env=env, capture_output=True, text=True)
    open(dst.replace('.npz', '.log'), 'w').write(r.stdout[-3000:] + r.stderr[-3000:])
    if r.returncode != 0:
        raise RuntimeError(f'systematics failed for {lhe}')
    txt = open(tmp).read()
    ids = re.findall(r'<weight id="(\d+)"[^>]*ALPSFACT="([0-9.]+)"', txt)
    idmap = {a: float(f) for a, f in ids}
    import numpy as np
    r05, r2 = [], []
    for ev in txt.split('<event>')[1:]:
        lines = ev.strip().split('\n')
        x0 = float(lines[0].split()[2])
        w = {idmap[a]: float(v) for a, v in WGT.findall(ev) if a in idmap}
        r05.append(w[0.5] / x0); r2.append(w[2.0] / x0)
    os.remove(tmp)
    np.savez_compressed(dst, r_alps0p5=np.array(r05), r_alps2=np.array(r2), source=lhe)
    return f'{id_}_m{m}_c{k}: {len(r05)} events, <r05> = {np.mean(r05):.4f}, <r2> = {np.mean(r2):.4f}'


def main():
    os.makedirs(OUT, exist_ok=True)
    todo = sys.argv[1:] or DEFAULT
    jobs = []
    for t in todo:
        id_, m = t.rsplit('_m', 1)
        for lhe in sorted(glob.glob(os.path.join(DATA, 'lhe', id_, f'm{m}_c*.lhe.gz'))):
            jobs.append((id_, int(m), lhe))
    with ThreadPoolExecutor(int(os.environ.get('NPROC', 3))) as ex:
        for r in ex.map(lambda a: one(*a), jobs):
            print(r, flush=True)


if __name__ == '__main__':
    main()
