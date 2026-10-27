"""produce.py -- resumable Stage-2 production driver (E4): MadGraph5_aMC 2.9.22 + Pythia8 (MG5aMC_PY8_interface)
-> HepMC (transient) -> compact npz (convert_hepmc.py) -> merged npz per (sample, mass) + SAMPLES_INDEX.json.

Run from sim/ with the system python3 (only stdlib; it calls the pixi envs itself):
    python3 scripts/produce.py [--only ID[,ID...]] [--dry]
Resumability: one npz per chunk in ../data/sim/npz/chunks/<ID>/; a finished (sample, mass) point is
../data/sim/npz/<ID>_m<mass>.npz; existing files are skipped, so the script can be restarted at any time.
Chunks of <= CHUNK events, distinct seeds (seed = base(ID) + 100*mass_index + chunk).  HepMC files are converted
by a background worker and deleted afterwards; LHE files are kept in ../data/sim/lhe/<ID>/.
MG install: untouched (models are imported by absolute path; per-output Cards/me5_configuration.txt).
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zlib

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.normpath(os.path.join(SIM, '..', 'data', 'sim'))
MG = os.environ.get('MG5_DIR', '')     # MadGraph5_aMC v2.9.22 install with HEPTools (Pythia8, MG5aMC_PY8_interface); see REPRODUCE.md
MODEL = os.path.join(SIM, 'models', 'quirkE-no_b_mass')
LHAPDF_DIR = os.path.join(DATA, 'lhapdf')
LOGDIR = os.path.join(SIM, 'logs')
CHUNK = 50000
NB_CORE = 6
SYST = "['--mur=0.5,1,2', '--muf=0.5,1,2', '--dyn=-1,1,2,3,4', '--pdf=CT18NLO,NNPDF23_lo_as_0130_qed@0']"
FINE = [300, 400, 600, 700, 800, 900, 1100, 1200, 1300, 1400, 1500]
BENCH = [200, 500, 1000]

# process classes -> MG output directories (one output per class; the mass is a run-time parameter)
PROCS = {
    'F_LOPS': ('xe', 'generate p p > xe+ xe-'),
    'F_INC': ('xe', 'generate p p > xe+ xe- @0\nadd process p p > xe+ xe- j @1\nadd process p p > xe+ xe- j j @2'),
    'F_TRG': ('xe', 'generate p p > xe+ xe- @0\nadd process p p > xe+ xe- j @1\nadd process p p > xe+ xe- j j @2'),
    'F_NJ1': ('xe', 'generate p p > xe+ xe- @0\nadd process p p > xe+ xe- j @1'),
    'S_LOPS': ('sxe', 'generate p p > sxe+ sxe-'),
    'S_INC': ('sxe', 'generate p p > sxe+ sxe- @0\nadd process p p > sxe+ sxe- j @1\nadd process p p > sxe+ sxe- j j @2'),
    'S_TRG': ('sxe', 'generate p p > sxe+ sxe- @0\nadd process p p > sxe+ sxe- j @1\nadd process p p > sxe+ sxe- j j @2'),
}
PTCUT = {'F_TRG': 100.0, 'S_TRG': 100.0}

# production tasks (approved plan §4/§7, 2026-10-11).  Order = execution order.
T = lambda id_, proc, masses, n, **kw: dict(id=id_, proc=proc, masses=masses, n=n, tune=kw.get('tune', 'CP5'),
                                             xq=kw.get('xq', 30.0), qc=kw.get('qc', 45.0), mpi=kw.get('mpi', True),
                                             qedfsr=kw.get('qedfsr', False))   # qedfsr: opt-in cards/pythia8_quirk_qedfsr.dat (not used so far)
TASKS = [
    T('E-INC', 'F_INC', [500], 100000), T('E-TRG', 'F_TRG', [500], 100000), T('E-LOPS', 'F_LOPS', [500], 50000),
    T('E-INC', 'F_INC', [200, 1000], 100000), T('E-TRG', 'F_TRG', [200, 1000], 100000),
    T('E-LOPS', 'F_LOPS', [200, 1000], 50000),
    T('V-TUNE-TRG', 'F_TRG', [500], 50000, tune='Monash'), T('V-TUNE-INC', 'F_INC', [500], 50000, tune='Monash'),
    T('V-MERGE-20', 'F_INC', [500], 50000, xq=20.0, qc=30.0), T('V-MERGE-50', 'F_INC', [500], 50000, xq=50.0, qc=75.0),
    T('V-NJ1', 'F_NJ1', [500], 50000), T('V-MPI', 'F_TRG', [500], 50000, mpi=False),
    T('S-INC', 'S_INC', BENCH, 50000), T('S-TRG', 'S_TRG', BENCH, 50000), T('S-LOPS', 'S_LOPS', BENCH, 20000),
    T('E-TRG', 'F_TRG', FINE, 40000), T('E-INC', 'F_INC', FINE, 20000),
    # off-grid interpolation closure point (review S2-R1 B-7; fixer 2026-10-11): INC only, 50k
    T('V-INTERP', 'F_INC', [550], 50000),
    # pilot (pipeline test only; run with --only P-INC,P-TRG,P-LOPS)
    T('P-INC', 'F_INC', [500], 2000), T('P-TRG', 'F_TRG', [500], 2000), T('P-LOPS', 'F_LOPS', [500], 2000),
]


# top-ups (review S2-R1 B-4, fixer 2026-10-11): extra chunks appended to an existing merged point.  The effective tail
# statistics (Kish N_eff, pT(QQ) > 200, |eta| < 2.5) of TRGS at 200/300 GeV were below 5x the expected 3 ab^-1 signal after a
# Knapen-like selection efficiency 0.18 (24.3k / 7.9k needed vs 12.3k / 4.4k).  Chunk index continues after the existing chunks,
# so seeds stay unique (seed = base(ID) + 10*m + ichunk + 1).  Run: python3 scripts/produce.py --topup
TOPUP = [('E-TRG', 200, [50000, 50000]), ('E-INC', 200, [50000, 50000]), ('E-TRG', 300, [40000]), ('E-INC', 300, [50000])]


def log(msg):
    line = time.strftime('%Y-%m-%d %H:%M:%S ') + msg
    print(line, flush=True)
    with open(os.path.join(LOGDIR, 'produce.log'), 'a') as f:
        f.write(line + '\n')


def env():
    e = dict(os.environ)
    e['LHAPDF_DATA_PATH'] = LHAPDF_DIR
    e['PYTHONDONTWRITEBYTECODE'] = '1'      # never write __pycache__/*.pyc into the MG install (review S2-R1 B2)
    return e


def mg_run(script_txt, tag):
    if not MG:
        sys.exit('set MG5_DIR to the MadGraph5_aMC v2.9.22 install (see REPRODUCE.md)')
    path = os.path.join(LOGDIR, f'{tag}.mg')
    open(path, 'w').write(script_txt)
    with open(os.path.join(LOGDIR, f'{tag}.log'), 'w') as lf:
        r = subprocess.run(['pixi', 'run', '-e', 'mg', 'python', os.path.join(MG, 'bin', 'mg5_aMC'), path],
                           cwd=SIM, stdout=lf, stderr=subprocess.STDOUT, env=env())
    txt = open(os.path.join(LOGDIR, f'{tag}.log')).read()
    if r.returncode != 0 or 'interrupted with error' in txt or 'ERROR DETECTED' in txt:
        raise RuntimeError(f'MG failed ({tag}); see logs/{tag}.log')
    return txt


def ensure_output(proc):
    d = os.path.join(SIM, 'mg_out', f'prod_{proc}')
    if os.path.exists(os.path.join(d, 'bin', 'generate_events')):
        return d
    gen = PROCS[proc][1]
    mg_run(f'import model {MODEL}\ndefine p = p b b~\ndefine j = j b b~\n{gen}\noutput {d} -nojpeg\nexit\n',
           f'output_{proc}')
    sp = os.path.join(SIM, 'scripts')
    subprocess.run([sys.executable, os.path.join(sp, 'mg_configure.py'), d, 'ebeam1=7000.0', 'ebeam2=7000.0',
                    'pdlabel=lhapdf', 'lhaid=14400', 'use_syst=True', f'nb_core={NB_CORE}'], check=True)
    if proc in PTCUT:
        subprocess.run([sys.executable, os.path.join(sp, 'patch_ptqq_cut.py'), d, str(PTCUT[proc])], check=True)
    log(f'created output {d}')
    return d


def write_pythia_card(d, task, matched):
    lines = open(os.path.join(d, 'Cards', 'pythia8_card_default.dat')).read().split('\n')
    out = []
    for l in lines:
        if matched and l.strip().startswith('JetMatching:qCut'):
            l = f'JetMatching:qCut         = {task["qc"]:.1f}'
        out.append(l)
    txt = '\n'.join(out) + '\n'
    for card in (f'pythia8_tune_{task["tune"]}.dat', 'pythia8_quirk_common.dat'):
        txt += strip_comments(open(os.path.join(SIM, 'cards', card)).read())
    if not task['mpi']:
        txt += 'PartonLevel:MPI = off\n'
    open(os.path.join(d, 'Cards', 'pythia8_card.dat'), 'w').write(txt)


def strip_comments(t):
    o = []
    for l in t.split('\n'):
        l = l.split('!')[0].rstrip()
        if l:
            o.append(l)
    return '\n'.join(o) + '\n'


def banner_info(rundir):
    b = glob.glob(os.path.join(rundir, '*_banner.txt'))[0]
    t = open(b).read()
    n = int(re.search(r'#\s*Number of Events\s*:\s*(\d+)', t).group(1))
    s = float(re.search(r'#\s*Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)', t).group(1))
    return n, s


pending = []   # background converters: (Popen, hepmc_path, out_npz)
PY8_EXE = os.path.join(MG, 'HEPTools', 'MG5aMC_PY8_interface', 'MG5aMC_PY8_interface')
NJOBS = 6


def reap(block=False, maxpending=6):
    """Finish converters: all if block, else the finished ones and the oldest while too many are pending."""
    while pending:
        p, hep, out = pending[0]
        if not (block or p.poll() is not None or len(pending) >= maxpending):
            break
        rc = p.wait()
        pending.pop(0)
        if rc != 0 or not os.path.exists(out):
            log(f'ERROR converter rc={rc} for {hep}; HepMC kept')
            continue
        os.remove(hep)
        log(f'converted {os.path.relpath(out, DATA)}; HepMC deleted')


def py8_card(task, matched, njmax, seed, nev):
    """Same content as the card MG5aMC writes for its own split PY8 jobs (checked against tag_1_pythia8.cmd of the
    MG-showered pilot/first chunk), plus an explicit random seed per job."""
    L = [f'Main:numberOfEvents = {nev}', 'HEPMCoutput:file = events.hepmc']
    if matched:
        L += [f'JetMatching:qCut = {task["qc"]:.4f}', 'JetMatching:doShowerKt = off', f'JetMatching:nJetMax = {njmax}']
    L += ['SysCalc:fullCutVariation = off']
    body = ''
    for card in (f'pythia8_tune_{task["tune"]}.dat', 'pythia8_quirk_common.dat') + (('pythia8_quirk_qedfsr.dat',) if task.get('qedfsr') else ()):
        body += strip_comments(open(os.path.join(SIM, 'cards', card)).read())
    L += body.strip().split('\n')
    if not task['mpi']:
        L += ['PartonLevel:MPI = off']
    L += ['Beams:frameType=4']
    if matched:
        L += ['Beams:setProductionScalesFromLHEF=on']
    L += ['HEPMCoutput:scaling=1.0e+09', 'Check:epTolErr=1.0e-02', 'JetMatching:etaJetMax=1.0e+03']
    if matched:
        L += ['JetMatching:merge=on', 'JetMatching:doVeto=off', 'JetMatching:scheme=1', 'JetMatching:setMad=off',
              'JetMatching:coneRadius=1.0', 'JetMatching:nQmatch=5',
              f'SysCalc:qCutList={1.5 * task["qc"]:.3f},{2.0 * task["qc"]:.3f}', f'SysCalc:qWeed={task["xq"]:.4f}']
    else:
        L += ['JetMatching:setMad=off']
    L += ['LHEFInputs:nSubruns=1', 'Main:subrun=0', 'Beams:LHEF=events.lhe.gz', 'Random:setSeed=on', f'Random:seed={seed}']
    return '\n'.join(L) + '\n'


def split_lhe(src, dst_dir, k):
    import gzip
    with gzip.open(src, 'rt') as f:
        txt = f.read()
    i0 = txt.index('<event>')
    head = txt[:i0]
    body = txt[i0:txt.rindex('</LesHouchesEvents>')]
    evs = body.split('</event>')
    evs = [e + '</event>\n' for e in evs if '<event>' in e]
    n = len(evs)
    sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]
    out, s = [], 0
    for j, sz in enumerate(sizes):
        d = os.path.join(dst_dir, f'split_{j}')
        os.makedirs(d, exist_ok=True)
        with gzip.open(os.path.join(d, 'events.lhe.gz'), 'wt', compresslevel=1) as g:
            g.write(head); g.writelines(evs[s:s + sz]); g.write('</LesHouchesEvents>\n')
        out.append((d, sz)); s += sz
    return out, n


def run_chunk(task, m, ichunk, nev, seed):
    """MG (LHE + systematics, shower OFF) -> own parallel MG5aMC_PY8_interface jobs (NJOBS splits, uncompressed HepMC,
    no MG merge/gzip step) -> one converter per split (norm 'auto') -> HepMC deleted."""
    proc = task['proc']
    d = ensure_output(proc)
    pname, spin = PROCS[proc][0], proc[0]
    matched = not proc.endswith('LOPS')
    njmax = 1 if proc.endswith('NJ1') else 2
    run = f'{task["id"]}_m{m}_c{ichunk}'
    chunkdir = os.path.join(DATA, 'npz', 'chunks', task['id'])
    os.makedirs(chunkdir, exist_ok=True)
    old_style = os.path.join(chunkdir, f'm{m}_c{ichunk}.npz')
    done = os.path.join(chunkdir, f'm{m}_c{ichunk}.done.json')
    if os.path.exists(old_style):
        return [old_style]
    if os.path.exists(done):
        return json.load(open(done))['files']
    rundir = os.path.join(d, 'Events', run)
    if os.path.exists(rundir):
        shutil.rmtree(rundir)          # incomplete previous attempt
    sp = os.path.join(SIM, 'scripts')
    kv = [f'nevents={nev}', f'iseed={seed}', f'systematics_arguments={SYST}']
    if matched:
        kv += [f'xqcut={task["xq"]:.1f}', 'ickkw=1']
    subprocess.run([sys.executable, os.path.join(sp, 'mg_configure.py'), d] + kv, check=True, stdout=subprocess.DEVNULL)
    mpar = 'MXE' if pname == 'xe' else 'MSXE'
    t0 = time.time()
    mg_run(f'launch {d} -n {run}\nshower=OFF\nset {mpar} {m}\ndone\nexit\n', f'launch_{run}')
    lhe = os.path.join(rundir, 'unweighted_events.lhe.gz')
    n, s = banner_info(rundir)
    lhedir = os.path.join(DATA, 'lhe', task['id'])
    auxdir = os.path.join(DATA, 'aux', task['id'], f'm{m}_c{ichunk}')
    os.makedirs(lhedir, exist_ok=True); os.makedirs(auxdir, exist_ok=True)
    shutil.copy(lhe, os.path.join(lhedir, f'm{m}_c{ichunk}.lhe.gz'))
    for f in glob.glob(os.path.join(rundir, '*banner.txt')) + glob.glob(os.path.join(rundir, '*systematics.log')):
        shutil.copy(f, auxdir)
    t1 = time.time()
    pydir = os.path.join(rundir, 'py8')
    splits, ntot = split_lhe(lhe, pydir, NJOBS)
    assert ntot == n, (ntot, n)
    os.remove(lhe)
    jobs = []
    e = env(); e['DYLD_LIBRARY_PATH'] = os.path.join(MG, 'HEPTools', 'lib') + ':' + e.get('DYLD_LIBRARY_PATH', '')
    for j, (sd, sz) in enumerate(splits):
        open(os.path.join(sd, 'PY8Card.dat'), 'w').write(py8_card(task, matched, njmax, (seed * 10 + j) % 900000000 + 1, sz))
        lf = open(os.path.join(sd, 'PY8_log.txt'), 'w')
        jobs.append((subprocess.Popen([PY8_EXE, 'PY8Card.dat'], cwd=sd, stdout=lf, stderr=subprocess.STDOUT, env=e), sd, sz, j))
    files = []
    while jobs:
        for job in list(jobs):
            p, sd, sz, j = job
            if p.poll() is None:
                continue
            jobs.remove(job)
            hep = os.path.join(sd, 'events.hepmc')
            if p.returncode != 0 or not os.path.exists(hep):
                raise RuntimeError(f'PY8 job {j} of {run} failed (rc={p.returncode}); see {sd}/PY8_log.txt')
            sub = os.path.join(auxdir, f'split_{j}')
            os.makedirs(sub, exist_ok=True)
            for f in ('djrs.dat', 'pts.dat', 'PY8_log.txt', 'PY8Card.dat'):
                if os.path.exists(os.path.join(sd, f)):
                    shutil.copy(os.path.join(sd, f), sub)
            out = os.path.join(chunkdir, f'm{m}_c{ichunk}_s{j}.npz')
            cmd = ['pixi', 'run', '-e', 'ana', 'python', os.path.join(sp, 'convert_hepmc.py'), hep, out, '--mq', str(m),
                   '--spin', spin, '--sigma-lhe-pb', repr(s), '--nlhe', str(sz), '--tag', f'{run}_s{j}', '--norm', 'auto']
            if matched:
                cmd += ['--merging-nominal', f'{task["qc"]:.3f}']
            lf = open(os.path.join(LOGDIR, f'convert_{run}_s{j}.log'), 'w')
            pending.append((subprocess.Popen(cmd, cwd=SIM, stdout=lf, stderr=subprocess.STDOUT), hep, out))
            files.append(out)
        reap(maxpending=8)
        time.sleep(2)
    log(f'MG {run}: N_LHE={n} sigma_LHE={s:.6g} pb, MG {t1 - t0:.0f} s, PY8 {time.time() - t1:.0f} s')
    reap(block=True)
    for f in files:
        if not os.path.exists(f):
            raise RuntimeError(f'missing converted split {f}')
    json.dump(dict(files=files, n_lhe=n, sigma_lhe_pb=s, seed=seed), open(done, 'w'))
    shutil.rmtree(pydir, ignore_errors=True)
    return files


def merge_point(task, m, chunks):
    final = os.path.join(DATA, 'npz', f'{task["id"]}_m{m}.npz')
    r = subprocess.run(['pixi', 'run', '-e', 'ana', 'python', os.path.join(SIM, 'scripts', 'merge_chunks.py'), final] + chunks,
                       cwd=SIM, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError('merge failed: ' + r.stderr[-2000:])
    log(r.stdout.strip())
    idxp = os.path.join(DATA, 'SAMPLES_INDEX.json')
    idx = json.load(open(idxp)) if os.path.exists(idxp) else {}
    spin = task['proc'][0]
    key = f'{spin}_{m}_{task["id"]}'
    idx[key] = os.path.relpath(final, DATA)
    # loader aliases: 'incl' / 'trig' / 'lops' for the nominal samples
    alias = {'E-INC': 'incl', 'E-TRG': 'trig', 'E-LOPS': 'lops', 'S-INC': 'incl', 'S-TRG': 'trig', 'S-LOPS': 'lops'}
    if task['id'] in alias:
        idx[f'{spin}_{m}_{alias[task["id"]]}'] = os.path.relpath(final, DATA)
    json.dump(idx, open(idxp, 'w'), indent=1, sort_keys=True)


def topup(dry=False):
    """Append the TOPUP chunks to existing merged points (idempotent: a point whose merged N_LHE already contains the
    chunks is skipped).  The existing merged npz is passed to merge_chunks.py as one 'chunk' with its N_LHE, so the
    weights are renormalised to the new total exactly as a fresh merge would do."""
    for id_, m, sizes in TOPUP:
        task = next(t for t in TASKS if t['id'] == id_ and m in t['masses'])
        final = os.path.join(DATA, 'npz', f'{id_}_m{m}.npz')
        chunkdir = os.path.join(DATA, 'npz', 'chunks', id_)
        n_old = len(glob.glob(os.path.join(chunkdir, f'm{m}_c*.done.json')))
        n_base = (task['n'] + CHUNK - 1) // CHUNK
        base = zlib.crc32(id_.encode()) % 1000 * 100000
        r = subprocess.run(['pixi', 'run', '-e', 'ana', 'python', '-c', f"import numpy as np; print(int(np.load('{final}')['nlhe']))"],
                           cwd=SIM, capture_output=True, text=True)
        nlhe_now = int(r.stdout.strip().split()[-1])
        target = task['n'] + sum(sizes)
        if nlhe_now >= target:
            log(f'TOPUP {id_} m={m}: already at N_LHE={nlhe_now}'); continue
        if dry:
            log(f'DRY TOPUP {id_} m={m}: N_LHE {nlhe_now} -> {target}, chunks {list(range(n_base, n_base + len(sizes)))}'); continue
        new = []
        for k, nev in enumerate(sizes):
            ic = n_base + k
            new += run_chunk(task, m, ic, nev, seed=base + 10 * m + ic + 1)
        reap(block=True)
        tmp = final.replace('.npz', '.pre_topup.npz')
        shutil.move(final, tmp)
        rr = subprocess.run(['pixi', 'run', '-e', 'ana', 'python', os.path.join(SIM, 'scripts', 'merge_chunks.py'), final, tmp] + new,
                            cwd=SIM, capture_output=True, text=True)
        if rr.returncode != 0:
            shutil.move(tmp, final)
            raise RuntimeError('top-up merge failed: ' + rr.stderr[-2000:])
        os.remove(tmp)
        for f in new:
            os.remove(f)
        log('TOPUP ' + rr.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=None)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--topup', action='store_true', help='append the TOPUP chunks (review S2-R1 B-4)')
    a = ap.parse_args()
    os.makedirs(LOGDIR, exist_ok=True)
    if a.topup:
        topup(a.dry)
        return
    only = set(a.only.split(',')) if a.only else None
    for task in TASKS:
        if task['id'].startswith('P-') and not (only and task['id'] in only):
            continue
        if only and task['id'] not in only:
            continue
        base = zlib.crc32(task['id'].encode()) % 1000 * 100000
        for im, m in enumerate(task['masses']):
            final = os.path.join(DATA, 'npz', f'{task["id"]}_m{m}.npz')
            if os.path.exists(final):
                continue
            nch = (task['n'] + CHUNK - 1) // CHUNK
            sizes = [CHUNK] * (task['n'] // CHUNK) + ([task['n'] % CHUNK] if task['n'] % CHUNK else [])
            if a.dry:
                log(f'DRY {task["id"]} m={m}: {nch} chunks {sizes}')
                continue
            chunks = []
            for ic, nev in enumerate(sizes):
                chunks += run_chunk(task, m, ic, nev, seed=base + 10 * m + ic + 1)
            reap(block=True)
            merge_point(task, m, chunks)
            log(f'DONE {task["id"]} m={m}')
    reap(block=True)
    log('ALL TASKS DONE' if not only else f'DONE tasks {only}')


if __name__ == '__main__':
    main()
