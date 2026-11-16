"""s2_job.py -- channel (ii) Stage-2 / S2 job driver (quirks v2, Phase 2, executor Sebastian, 2026-11-16).

Stdlib only; run on a worker by the runner (`python3 -I s2_job.py <cmd> ...`), never on einstein.
It follows the v1 Stage-2 flow (`sim/scripts/produce.py`: MG with shower OFF, our own MG5aMC_PY8_interface job with
the v1 cards, `convert_hepmc.py` to npz) and Basil's Phase-1 driver (`phase1_strategy/src/generators/feas_mg.py`:
pixi Python 3.9 for MG, no conda lib dir on LD_LIBRARY_PATH, LHAPDF from `sw/lhapdf_data`), with two changes:
  * MG runs from a node-local copy of the install (/home/scratch/jdochoa/mg5/<stamp>/, made once per node under flock;
    FEAS_B open issue 1: MG writes into its install at run time);
  * every step is timed with the rusage of its waited-for children (CPU = utime + stime, as the runner).
Work happens in $QV2_SCRATCH_DIR/work; the files named as outputs are written to $QV2_OUT_DIR (the runner publishes them).

Commands
  mlmtime <tag> <proc> <mass> <n1> <n2> [--ptcut X] [--qedfsr]
      MLM 0-2j timing: output; warm-up launch of 100 events (compilation); launch n1 events; launch n2 events; PY8 MLM shower of the n2-event run;
      conversion to npz.  Outputs <tag>.timing.json, <tag>.lhe.gz, <tag>.npz, <tag>.aux.tar.gz.
Seeds: blake2b("qv2|<stream>|<chunk>") (STR §4.17), reduced mod 3e7 (MG iseed) and mod 9e8 (Pythia).
"""
import fcntl
import glob
import gzip
import hashlib
import json
import logging
import os
import re
import resource
import shutil
import socket
import subprocess
import sys
import tarfile
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', stream=sys.stdout)
log = logging.getLogger('s2_job')

REPO = '/home/users/jdochoa/hllhc-quirks-search'
QV2 = os.path.join(REPO, 'analyses', 'quirks_v2')
SIM = os.path.join(QV2, 'sim')
SW = '/home/users/jdochoa/sw'
MG_NFS = os.path.join(SW, 'mg5', 'MG5_aMC_v2_9_22')
ENV = os.path.join(SW, 'envs', 'mg', '.pixi', 'envs', 'default')
PY = os.path.join(ENV, 'bin', 'python3')
LHAPDF_CONFIG = os.path.join(ENV, 'bin', 'lhapdf-config')
LHAPDF_DATA = os.path.join(SW, 'lhapdf_data')
ANA_PY = os.path.join(SIM, '.pixi', 'envs', 'ana', 'bin', 'python')
CARDS = os.path.join(SIM, 'cards')
MODEL_SRC = os.path.join(SIM, 'models', 'quirkE')
PY8_EXE = os.path.join(MG_NFS, 'HEPTools', 'MG5aMC_PY8_interface', 'MG5aMC_PY8_interface')
LOCAL = '/home/scratch/jdochoa'
SYST = "['--mur=0.5,1,2', '--muf=0.5,1,2', '--dyn=-1,1,2,3,4', '--pdf=CT18NLO,NNPDF23_lo_as_0130_qed@0']"  # produce.py l.33

# process classes, as produce.py l.38-46
PROCS = {
    'F_LOPS': ('xe', 'generate p p > xe+ xe-'),
    'F_INC': ('xe', 'generate p p > xe+ xe- @0\nadd process p p > xe+ xe- j @1\nadd process p p > xe+ xe- j j @2'),
    'F_TRG': ('xe', 'generate p p > xe+ xe- @0\nadd process p p > xe+ xe- j @1\nadd process p p > xe+ xe- j j @2'),
    'S_INC': ('sxe', 'generate p p > sxe+ sxe- @0\nadd process p p > sxe+ sxe- j @1\nadd process p p > sxe+ sxe- j j @2'),
    'S_TRG': ('sxe', 'generate p p > sxe+ sxe- @0\nadd process p p > sxe+ sxe- j @1\nadd process p p > sxe+ sxe- j j @2'),
    'S_LOPS': ('sxe', 'generate p p > sxe+ sxe-'),
}
XQCUT, QCUT = 30.0, 45.0   # v1 nominal merging (produce.py l.51; SAMPLES.md "30.0/45.0")

STEPS = []


def seed(stream, chunk, mod):
    h = hashlib.blake2b(f'qv2|{stream}|{chunk}'.encode(), digest_size=8).digest()
    return int.from_bytes(h, 'big') % mod + 1


def timed(name, cmd, cwd, logfile, env=None):
    """Run cmd, wait, record CPU (children rusage delta), wall and max RSS of the step."""
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    with open(logfile, 'w') as lf:
        p = subprocess.run(cmd, cwd=cwd, stdout=lf, stderr=subprocess.STDOUT, env=env, stdin=subprocess.DEVNULL)
    t1 = time.time()
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    rec = dict(step=name, cpu_s=round((r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), 3),
               wall_s=round(t1 - t0, 3), maxrss_mb_children_so_far=round(r1.ru_maxrss / 1024, 1), rc=p.returncode)
    STEPS.append(rec)
    log.info('step %s: %s', name, rec)
    if p.returncode != 0:
        sys.exit(f'step {name} failed rc={p.returncode}; see {logfile}')
    return rec


def mg_env():
    e = dict(os.environ)
    e['LHAPDF_DATA_PATH'] = LHAPDF_DATA
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    e['PATH'] = os.path.join(ENV, 'bin') + ':' + e.get('PATH', '')
    e.pop('LD_LIBRARY_PATH', None)   # FEAS_B pitfall 4: never the conda lib dir (libgfortran 16)
    return e


def local_mg():
    """Node-local copy of the MG install, keyed by a stamp of the NFS install's top-level tree (made once, flock)."""
    st = hashlib.sha256()
    for root, dirs, files in os.walk(MG_NFS):
        dirs.sort()
        rel = os.path.relpath(root, MG_NFS)
        if rel.count(os.sep) > 1:   # stamp the top two levels only (cheap on NFS)
            dirs[:] = []
            continue
        for f in sorted(files):
            st.update(f'{rel}/{f}'.encode())
    stamp = st.hexdigest()[:12]
    dst = os.path.join(LOCAL, 'mg5', stamp)
    ok = os.path.join(dst, '.QV2_COPY_OK')
    os.makedirs(os.path.join(LOCAL, '.locks'), exist_ok=True)
    with open(os.path.join(LOCAL, '.locks', 'mg5copy.lock'), 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        if not os.path.exists(ok):
            tmp = dst + f'.tmp{os.getpid()}'
            shutil.rmtree(tmp, ignore_errors=True)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            t0 = time.time()
            subprocess.run(['cp', '-rd', MG_NFS, tmp], check=True)   # plain cp: preserving NFS4 ACL/mode fails on ext4
            if os.path.exists(dst):
                shutil.rmtree(dst)
            os.rename(tmp, dst)   # node-local ext4, not cajuela
            open(ok, 'w').write(f'{MG_NFS} {stamp} {time.ctime()} {time.time() - t0:.1f}s\n')
            log.info('local MG copy made: %s (%.1f s)', dst, time.time() - t0)
    return dst


def mg(mgdir, script, tag, cwd, name):
    p = os.path.join(cwd, tag + '.mg')
    open(p, 'w').write(script)
    rec = timed(name, [PY, os.path.join(mgdir, 'bin', 'mg5_aMC'), p], cwd, os.path.join(cwd, tag + '.log'), mg_env())
    t = open(os.path.join(cwd, tag + '.log')).read()
    if 'interrupted with error' in t or 'ERROR DETECTED' in t:
        sys.exit(f'MG error in {tag}; see {cwd}/{tag}.log')
    return rec, t


def set_conf(path, kv):
    lines = open(path).read().split('\n')
    for k, v in kv.items():
        pat = re.compile(r'^\s*#?\s*%s\s*=' % re.escape(k))
        hit = [i for i, l in enumerate(lines) if pat.match(l)]
        if hit:
            lines[hit[0]] = f'{k} = {v}'
        else:
            lines.append(f'{k} = {v}')
    open(path, 'w').write('\n'.join(lines))


def set_run(path, kv):
    """as sim/scripts/mg_configure.py set_run (adds the key if absent)."""
    txt = open(path).read()
    for k, v in kv.items():
        new, n = re.subn(r'^(\s*)(\S.*?)(\s*=\s*%s\b)' % re.escape(k), lambda m: f'{m.group(1)}{v}{m.group(3)}', txt,
                         flags=re.M)
        if n == 0:
            new = txt + f'\n {v} = {k}\n'
        txt = new
    open(path, 'w').write(txt)


def strip_comments(t):
    o = []
    for l in t.split('\n'):
        l = l.split('!')[0].rstrip()
        if l:
            o.append(l)
    return o


def py8_card(matched, njmax, sd, nev, qc=QCUT, xq=XQCUT, tune='CP5', qedfsr=False, mpi=True):
    """Same content as produce.py:py8_card (l.172-196), v1's MLM shower card, plus the opt-in QED-FSR card."""
    L = [f'Main:numberOfEvents = {nev}', 'HEPMCoutput:file = events.hepmc']
    if matched:
        L += [f'JetMatching:qCut = {qc:.4f}', 'JetMatching:doShowerKt = off', f'JetMatching:nJetMax = {njmax}']
    L += ['SysCalc:fullCutVariation = off']
    for c in [f'pythia8_tune_{tune}.dat', 'pythia8_quirk_common.dat'] + (['pythia8_quirk_qedfsr.dat'] if qedfsr else []):
        L += strip_comments(open(os.path.join(CARDS, c)).read())
    if not mpi:
        L += ['PartonLevel:MPI = off']
    L += ['Beams:frameType=4']
    if matched:
        L += ['Beams:setProductionScalesFromLHEF=on']
    L += ['HEPMCoutput:scaling=1.0e+09', 'Check:epTolErr=1.0e-02', 'JetMatching:etaJetMax=1.0e+03']
    if matched:
        L += ['JetMatching:merge=on', 'JetMatching:doVeto=off', 'JetMatching:scheme=1', 'JetMatching:setMad=off',
              'JetMatching:coneRadius=1.0', 'JetMatching:nQmatch=5',
              f'SysCalc:qCutList={1.5 * qc:.3f},{2.0 * qc:.3f}', f'SysCalc:qWeed={xq:.4f}']
    else:
        L += ['JetMatching:setMad=off']
    L += ['LHEFInputs:nSubruns=1', 'Main:subrun=0', 'Beams:LHEF=events.lhe.gz', 'Random:setSeed=on', f'Random:seed={sd}']
    return '\n'.join(L) + '\n'


def banner(rundir):
    b = glob.glob(os.path.join(rundir, '*_banner.txt'))[0]
    t = open(b).read()
    n = int(re.search(r'#\s*Number of Events\s*:\s*(\d+)', t).group(1))
    s = float(re.search(r'#\s*Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)', t).group(1))
    return n, s


def mg_output(mgdir, proc, work, ptcut):
    """MG process output in the job scratch (as produce.py ensure_output, l.104-117, with nb_core = 1)."""
    models = os.path.join(work, 'models')
    shutil.copytree(MODEL_SRC, os.path.join(models, 'quirkE'),
                    ignore=shutil.ignore_patterns('*.pkl', '__pycache__'))
    d = os.path.join(work, f'prod_{proc}')
    gen = PROCS[proc][1]
    script = (f'import model {models}/quirkE-no_b_mass\ndefine p = p b b~\ndefine j = j b b~\n{gen}\n'
              f'output {d} -nojpeg\nexit\n')
    rec, _ = mg(mgdir, script, f'output_{proc}', work, 'mg_output')
    conf = {'lhapdf': LHAPDF_CONFIG, 'lhapdf_py3': LHAPDF_CONFIG,
            'pythia8_path': os.path.join(MG_NFS, 'HEPTools', 'pythia8'),
            'mg5amc_py8_interface_path': os.path.join(MG_NFS, 'HEPTools', 'MG5aMC_PY8_interface'),
            'run_mode': '0', 'nb_core': '1', 'automatic_html_opening': 'False', 'notification_center': 'False',
            'fortran_compiler': 'gfortran'}
    set_conf(os.path.join(d, 'Cards', 'me5_configuration.txt'), conf)
    set_run(os.path.join(d, 'Cards', 'run_card.dat'),
            {'ebeam1': '7000.0', 'ebeam2': '7000.0', 'pdlabel': 'lhapdf', 'lhaid': '14400', 'use_syst': 'True'})
    if ptcut:
        subprocess.run([sys.executable, '-I', os.path.join(SIM, 'scripts', 'patch_ptqq_cut.py'), d, str(ptcut)],
                       check=True, stdout=subprocess.DEVNULL)
    return d


def mg_launch(mgdir, d, run, nev, sd, mass, matched, name):
    pname = 'MXE'
    set_run(os.path.join(d, 'Cards', 'run_card.dat'),
            dict(nevents=str(nev), iseed=str(sd), systematics_arguments=SYST,
                 **({'xqcut': f'{XQCUT:.1f}', 'ickkw': '1'} if matched else {})))
    rd = os.path.join(d, 'Events', run)
    shutil.rmtree(rd, ignore_errors=True)
    proc_mass = 'MSXE' if open(os.path.join(d, 'Cards', 'proc_card_mg5.dat')).read().count('sxe+') else pname
    rec, txt = mg(mgdir, f'launch {d} -n {run}\nshower=OFF\ndone\nset {proc_mass} {mass}\ndone\nexit\n',
                  f'launch_{run}', os.path.dirname(d), name)
    n, s = banner(rd)
    rec.update(n_lhe=n, sigma_pb=s)
    me = re.findall(r'Cross-section :\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)\s*pb', txt)
    if me:
        rec.update(sigma_log_pb=float(me[-1][0]), err_pb=float(me[-1][1]))
    return rd, n, s


def cmd_mlmtime(a):
    tag, proc, mass, n1, n2 = a[0], a[1], int(a[2]), int(a[3]), int(a[4])
    ptcut = float(a[a.index('--ptcut') + 1]) if '--ptcut' in a else None
    qedfsr = '--qedfsr' in a
    out = os.environ.get('QV2_OUT_DIR', os.getcwd())
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'work')
    os.makedirs(work, exist_ok=True)
    info = dict(tag=tag, proc=proc, mass=mass, n1=n1, n2=n2, ptcut_gev=ptcut, qedfsr=qedfsr, xqcut=XQCUT, qcut=QCUT,
                node=socket.gethostname(), start=time.strftime('%Y-%m-%d %H:%M:%S %z'))
    t0 = time.time()
    mgdir = local_mg()
    info['mg_local'] = mgdir
    info['t_local_copy_s'] = round(time.time() - t0, 2)
    d = mg_output(mgdir, proc, work, ptcut)
    matched = not proc.endswith('LOPS')
    s1 = seed(f's2.time.{tag}', 'mg1', 30000000)
    s2 = seed(f's2.time.{tag}', 'mg2', 30000000)
    s0 = seed(f's2.time.{tag}', 'mg0', 30000000)
    mg_launch(mgdir, d, f'{tag}_w', 100, s0, mass, matched, 'mg_launch_warm100')   # compilation lands here
    rd1, n_1, sig1 = mg_launch(mgdir, d, f'{tag}_a', n1, s1, mass, matched, 'mg_launch_n1')
    rd2, n_2, sig2 = mg_launch(mgdir, d, f'{tag}_b', n2, s2, mass, matched, 'mg_launch_n2')
    info.update(seed_mg=[s1, s2], sigma_pb=[sig1, sig2], n_lhe=[n_1, n_2])
    lhe = os.path.join(rd2, 'unweighted_events.lhe.gz')
    pd = os.path.join(rd2, 'py8')
    os.makedirs(pd)
    shutil.copy(lhe, os.path.join(pd, 'events.lhe.gz'))
    spy = seed(f's2.time.{tag}', 'py8', 900000000)
    info['seed_py8'] = spy
    open(os.path.join(pd, 'PY8Card.dat'), 'w').write(py8_card(matched, 2, spy, n_2, qedfsr=qedfsr))
    timed('py8_shower', [PY8_EXE, 'PY8Card.dat'], pd, os.path.join(pd, 'PY8_log.txt'), mg_env())
    hep = os.path.join(pd, 'events.hepmc')
    info['hepmc_bytes'] = os.path.getsize(hep)
    npz = os.path.join(out, f'{tag}.npz')
    spin = 'S' if proc.startswith('S') else 'F'
    cmd = [ANA_PY, os.path.join(SIM, 'scripts', 'convert_hepmc.py'), hep, npz, '--mq', str(mass), '--spin', spin,
           '--sigma-lhe-pb', repr(sig2), '--nlhe', str(n_2), '--tag', tag, '--norm', 'auto']
    if matched:
        cmd += ['--merging-nominal', f'{QCUT:.3f}']
    e = dict(os.environ)
    e['NUMBA_CACHE_DIR'] = os.path.join(work, 'numba')
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    timed('convert_npz', cmd, SIM, os.path.join(work, 'convert.log'), e)
    os.remove(hep)
    shutil.copy(lhe, os.path.join(out, f'{tag}.lhe.gz'))
    # per-event costs (ESTIMATE from the two launches; the shower and conversion per showered LHE event)
    st = {r['step']: r for r in STEPS}
    c1, c2 = st['mg_launch_n1']['cpu_s'], st['mg_launch_n2']['cpu_s']
    info['derived'] = dict(
        mg_per_lhe_event_ms=round(1e3 * (c2 - c1) / max(n_2 - n_1, 1), 3) if n_2 != n_1 else None,
        mg_launch_fixed_s=round(c1 - n_1 * (c2 - c1) / max(n_2 - n_1, 1), 2) if n_2 != n_1 else None,
        py8_per_lhe_event_ms=round(1e3 * st['py8_shower']['cpu_s'] / n_2, 3),
        convert_per_lhe_event_ms=round(1e3 * st['convert_npz']['cpu_s'] / n_2, 3),
        total_cpu_s=round(sum(r['cpu_s'] for r in STEPS), 2))
    info['derived']['chain_per_lhe_event_ms_excl_output'] = round(
        1e3 * (c2 + st['py8_shower']['cpu_s'] + st['convert_npz']['cpu_s']) / n_2, 3)
    info['steps'] = STEPS
    info['end'] = time.strftime('%Y-%m-%d %H:%M:%S %z')
    with tarfile.open(os.path.join(out, f'{tag}.aux.tar.gz'), 'w:gz') as tf:
        for f in (glob.glob(os.path.join(rd2, '*banner.txt')) + glob.glob(os.path.join(rd1, '*banner.txt')) +
                  [os.path.join(pd, 'PY8Card.dat'), os.path.join(pd, 'PY8_log.txt'), os.path.join(work, 'convert.log')] +
                  glob.glob(os.path.join(work, '*.log')) + glob.glob(os.path.join(work, '*.mg'))):
            if os.path.exists(f):
                tf.add(f, arcname=os.path.relpath(f, work))
    json.dump(info, open(os.path.join(out, f'{tag}.timing.json'), 'w'), indent=1)
    log.info('done: %s', json.dumps(info['derived']))


NLO_PROCS = {'E': 'generate p p > xe+ xe- [QCD]', 'S': 'generate p p > sxe+ sxe- [QCD]'}
MASSPAR = {'E': 'MXE', 'S': 'MSXE'}


def parse_summary(rd):
    t = open(os.path.join(rd, 'summary.txt')).read()
    m = re.search(r'Total cross section:\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)\s*pb', t)
    r = dict(sigma_pb=float(m.group(1)), err_pb=float(m.group(2)))
    s = re.search(r'Scale variation.*?\n.*?\n\s*[0-9.eE+-]+ pb\s*\+([0-9.]+)%\s*-([0-9.]+)%', t, re.S)
    if s:
        r.update(scale_up_pct=float(s.group(1)), scale_dn_pct=float(s.group(2)))
    p = re.search(r'PDF variation.*?\n.*?\n\s*[0-9.eE+-]+ pb\s*\+([0-9.]+)%\s*-([0-9.]+)%', t, re.S)
    if p:
        r.update(pdf_up_pct=float(p.group(1)), pdf_dn_pct=float(p.group(2)))
    r['summary_txt'] = t
    return r


def cmd_nlo(a):
    """nlo <tag> <E|S> <lhaid> <m1,m2,...> [--orders LO,NLO] [--fixed MU] [--pdfunc] [--acc 0.002]
    aMC@NLO fixed-order runs with the loop model loop_quirkE (Basil's make_loop_quirkE.py, built in scratch).
    --fixed MU: fixed mu_R = mu_F = MU (GeV) instead of the default dynamical H_T/2 (validation 1)."""
    tag, spin, lhaid, masses = a[0], a[1], a[2], [int(x) for x in a[3].split(',')]
    orders = a[a.index('--orders') + 1].split(',') if '--orders' in a else ['LO', 'NLO']
    fixed = float(a[a.index('--fixed') + 1]) if '--fixed' in a else None
    acc = a[a.index('--acc') + 1] if '--acc' in a else '0.002'
    pdfunc = '--pdfunc' in a
    out = os.environ.get('QV2_OUT_DIR', os.getcwd())
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'work')
    os.makedirs(work, exist_ok=True)
    mgdir = local_mg()
    models = os.path.join(work, 'models')
    os.makedirs(models)
    timed('make_loop_model', [sys.executable, '-I', os.path.join(QV2, 'phase1_strategy', 'src', 'generators',
                                                                 'make_loop_quirkE.py'), mgdir,
                              os.path.join(models, 'loop_quirkE')], work, os.path.join(work, 'make_loop.log'))
    for r in ('restrict_no_b_mass.dat',):
        if not os.path.exists(os.path.join(models, 'loop_quirkE', r)):
            sys.exit(f'loop model lacks {r}')
    d = os.path.join(work, f'{spin}_NLO')
    mg(mgdir, f'import model {models}/loop_quirkE-no_b_mass\ndefine p = p b b~\ndefine j = j b b~\n{NLO_PROCS[spin]}\n'
              f'output {d}\nexit\n', f'output_{spin}_NLO', work, 'mg_output_nlo')
    conf = {'lhapdf': LHAPDF_CONFIG, 'lhapdf_py3': LHAPDF_CONFIG, 'run_mode': '0', 'nb_core': '1',
            'automatic_html_opening': 'False', 'notification_center': 'False', 'fortran_compiler': 'gfortran'}
    set_conf(os.path.join(d, 'Cards', 'amcatnlo_configuration.txt'), conf)
    kv = {'ebeam1': '7000.0', 'ebeam2': '7000.0', 'pdlabel': 'lhapdf', 'lhaid': lhaid, 'store_rwgt_info': 'True',
          'reweight_scale': 'True', 'reweight_PDF': 'True' if pdfunc else 'False', 'req_acc_FO': acc}
    if fixed:
        kv.update(fixed_ren_scale='True', fixed_fac_scale='True', muR_ref_fixed=f'{fixed:.4f}',
                  muF_ref_fixed=f'{fixed:.4f}')
    set_run(os.path.join(d, 'Cards', 'run_card.dat'), kv)
    res = dict(tag=tag, spin=spin, lhaid=lhaid, fixed_scale=fixed, req_acc_FO=acc, pdfunc=pdfunc,
               node=socket.gethostname(), start=time.strftime('%Y-%m-%d %H:%M:%S %z'), points=[])
    for m in masses:
        for o in orders:
            run = f'{spin}{m}_{o}'
            mg(mgdir, f'launch {d} -n {run}\nfixed_order=ON\norder={o}\ndone\nset {MASSPAR[spin]} {m}\ndone\nexit\n',
               f'launch_{run}', work, f'fo_{o}_m{m}')
            r = parse_summary(os.path.join(d, 'Events', run))
            r.update(mass=m, order=o, cpu_s=STEPS[-1]['cpu_s'])
            res['points'].append(r)
            log.info('%s m=%d %s: %.6g +- %.2g pb', spin, m, o, r['sigma_pb'], r['err_pb'])
    res['steps'] = STEPS
    res['end'] = time.strftime('%Y-%m-%d %H:%M:%S %z')
    with tarfile.open(os.path.join(out, f'{tag}.aux.tar.gz'), 'w:gz') as tf:
        for f in glob.glob(os.path.join(work, '*.log')) + glob.glob(os.path.join(work, '*.mg')) + \
                glob.glob(os.path.join(d, 'Events', '*', '*banner.txt')) + [os.path.join(d, 'Cards', 'run_card.dat')]:
            tf.add(f, arcname=os.path.relpath(f, work))
    json.dump(res, open(os.path.join(out, f'{tag}.json'), 'w'), indent=1)


def cmd_lotree(a):
    """lotree <tag> <E|S> <lhaid> <m1,...> <nevents> [--fixed MU]: tree-level LO sigma with the v1 UFO (validation 1)."""
    tag, spin, lhaid, masses, nev = a[0], a[1], a[2], [int(x) for x in a[3].split(',')], int(a[4])
    fixed = float(a[a.index('--fixed') + 1]) if '--fixed' in a else None
    out = os.environ.get('QV2_OUT_DIR', os.getcwd())
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'work')
    os.makedirs(work, exist_ok=True)
    mgdir = local_mg()
    d = mg_output(mgdir, 'F_LOPS' if spin == 'E' else 'S_LOPS', work, None)
    kv = {'lhaid': lhaid, 'use_syst': 'False'}
    if fixed:
        kv.update(fixed_ren_scale='True', fixed_fac_scale='True', scale=f'{fixed:.4f}',
                  dsqrt_q2fact1=f'{fixed:.4f}', dsqrt_q2fact2=f'{fixed:.4f}')
    set_run(os.path.join(d, 'Cards', 'run_card.dat'), kv)
    res = dict(tag=tag, spin=spin, lhaid=lhaid, fixed_scale=fixed, nevents=nev, node=socket.gethostname(), points=[])
    for i, m in enumerate(masses):
        sd = seed(f's2.lotree.{tag}', m, 30000000)
        rd, n, s = mg_launch(mgdir, d, f'{spin}{m}_tree', nev, sd, m, False, f'lotree_m{m}')
        res['points'].append(dict(mass=m, sigma_pb=s, n=n, seed=sd, cpu_s=STEPS[-1]['cpu_s'],
                                  sigma_log_pb=STEPS[-1].get('sigma_log_pb'), err_pb=STEPS[-1].get('err_pb')))
    res['steps'] = STEPS
    with tarfile.open(os.path.join(out, f'{tag}.aux.tar.gz'), 'w:gz') as tf:
        for f in glob.glob(os.path.join(work, '*.log')) + glob.glob(os.path.join(d, 'Events', '*', '*banner.txt')):
            tf.add(f, arcname=os.path.relpath(f, work))
    json.dump(res, open(os.path.join(out, f'{tag}.json'), 'w'), indent=1)


if __name__ == '__main__':
    args = sys.argv[1:]
    {'mlmtime': cmd_mlmtime, 'nlo': cmd_nlo, 'lotree': cmd_lotree}[args[0]](args[1:])
