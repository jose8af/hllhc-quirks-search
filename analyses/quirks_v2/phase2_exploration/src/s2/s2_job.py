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


def _sampler(pgid, path, stop, every=15.0):
    """Every `every` s append one block: time, and per process of the step's process group: pid, state, cumulative
    CPU (ps TIME), elapsed, command (diagnosis of wall >> CPU, FxFx)."""
    with open(path, 'a') as f:
        while not stop.wait(every):
            r = subprocess.run(['ps', '-eo', 'pgid=,pid=,stat=,time=,etime=,args='], capture_output=True, text=True)
            rows = [l for l in r.stdout.splitlines() if l.split() and l.split()[0] == str(pgid)]
            f.write(f'--- {time.strftime("%H:%M:%S")} n={len(rows)}\n' + '\n'.join(x[:200] for x in rows) + '\n')
            f.flush()


def timed(name, cmd, cwd, logfile, env=None):
    """Run cmd, wait, record CPU (children rusage delta), wall and max RSS of the step.  Output lines are prefixed
    with the wall-clock time; with QV2_SAMPLE=1 a process sampler writes <logfile>.ps."""
    import threading
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    with open(logfile, 'w') as lf:
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env,
                             stdin=subprocess.DEVNULL, start_new_session=True, text=True, errors='replace')
        stop = threading.Event()
        th = None
        if os.environ.get('QV2_SAMPLE') == '1':
            th = threading.Thread(target=_sampler, args=(p.pid, logfile + '.ps', stop), daemon=True)
            th.start()
        for line in p.stdout:
            lf.write(time.strftime('%H:%M:%S ') + line)
        p.wait()
        stop.set()
    t1 = time.time()
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    rec = dict(step=name, cpu_s=round((r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), 3),
               wall_s=round(t1 - t0, 3), maxrss_mb_children_so_far=round(r1.ru_maxrss / 1024, 1), rc=p.returncode)
    STEPS.append(rec)
    log.info('step %s: %s', name, rec)
    if p.returncode != 0:
        sys.exit(f'step {name} failed rc={p.returncode}; see {logfile}')
    return rec


def use_local_env():
    """QV2_LOCAL_ENV=1: copy the MG python env and the LHAPDF sets to node-local scratch once (flock) and use them, so
    that nothing is read from NFS during the run (FxFx diagnosis, orchestrator ruling 2026-11-16).  lhapdf-config of the
    copy is rewritten to the new prefix (text replacement of the old prefix in that one script)."""
    global ENV, PY, LHAPDF_CONFIG, LHAPDF_DATA
    src_env, src_pdf = ENV, LHAPDF_DATA
    dst_env = os.path.join(LOCAL, 'envs_local', 'mg_default')
    dst_pdf = os.path.join(LOCAL, 'lhapdf_local')
    os.makedirs(os.path.join(LOCAL, '.locks'), exist_ok=True)
    with open(os.path.join(LOCAL, '.locks', 'mgenvcopy.lock'), 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        for src, dst in ((src_env, dst_env), (src_pdf, dst_pdf)):
            ok = os.path.join(dst, '.QV2_COPY_OK')
            if not os.path.exists(ok):
                tmp = dst + f'.tmp{os.getpid()}'
                shutil.rmtree(tmp, ignore_errors=True)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                t0 = time.time()
                subprocess.run(['cp', '-rd', src, tmp], check=True)
                if src == src_env:
                    cfg = os.path.join(tmp, 'bin', 'lhapdf-config')
                    txt = open(cfg).read()
                    open(cfg, 'w').write(txt.replace(src_env, dst_env))
                shutil.rmtree(dst, ignore_errors=True)
                os.rename(tmp, dst)
                open(ok, 'w').write(f'{src} {time.ctime()} {time.time() - t0:.1f}s\n')
    ENV, PY = dst_env, os.path.join(dst_env, 'bin', 'python3')
    LHAPDF_CONFIG, LHAPDF_DATA = os.path.join(dst_env, 'bin', 'lhapdf-config'), dst_pdf


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


NLO_PROCS = {'E': 'generate p p > xe+ xe- [QCD]', 'S': 'generate p p > sxe+ sxe- [QCD]',
             'DY': 'generate p p > e+ e- [QCD]'}
MASSPAR = {'E': 'MXE', 'S': 'MSXE', 'DY': None}

MPAIR_ANA = '''c qv2 (Sebastian): pair invariant mass of particles 3 and 4 (the produced pair), from the MG template
c analysis_HwU_template.f; histogram 1 = total rate, 2 = M(pair) in NB bins on [MLO, MHI]
      subroutine analysis_begin(nwgt,weights_info)
      implicit none
      integer nwgt
      character*(*) weights_info(*)
      call HwU_inithist(nwgt,weights_info)
      call HwU_book(1,'total rate      ', 5,0.5d0,5.5d0)
      call HwU_book(2,'M pair          ', @NB@,@MLO@d0,@MHI@d0)
      return
      end
      subroutine analysis_end(dummy)
      implicit none
      double precision dummy
      call HwU_write_file
      return
      end
      subroutine analysis_fill(p,istatus,ipdg,wgts,ibody)
      implicit none
      include 'nexternal.inc'
      integer istatus(nexternal)
      integer iPDG(nexternal)
      double precision p(0:4,nexternal)
      double precision wgts(*)
      integer ibody
      double precision e,px,py,pz,xm
      call HwU_fill(1,1d0,wgts)
      e=p(0,3)+p(0,4)
      px=p(1,3)+p(1,4)
      py=p(2,3)+p(2,4)
      pz=p(3,3)+p(3,4)
      xm=sqrt(max(e**2-px**2-py**2-pz**2,0d0))
      call HwU_fill(2,xm,wgts)
      return
      end
'''


def parse_hwu(rd, title='M pair'):
    rows, on = [], False
    for l in open(os.path.join(rd, 'MADatNLO.HwU')):
        if l.startswith('<histogram>'):
            on = title in l
            continue
        if l.startswith('<\\histogram>'):
            on = False
            continue
        if on and l.strip():
            v = [float(x) for x in l.split()]
            rows.append(dict(lo=v[0], hi=v[1], val=v[2], err=v[3], scale_min=v[5], scale_max=v[6]))
    return rows


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
    tag, spin, lhaid, masses = a[0], a[1], a[2], [int(x) for x in a[3].split(',')]   # DY: masses = [0] (label only)
    orders = a[a.index('--orders') + 1].split(',') if '--orders' in a else ['LO', 'NLO']
    fixed = a[a.index('--fixed') + 1] if '--fixed' in a else None      # a number, or 'm' (= the mass of each point)
    fixed = fixed if fixed in (None, 'm') else float(fixed)
    acc = a[a.index('--acc') + 1] if '--acc' in a else '0.002'
    pdfunc = '--pdfunc' in a
    mhist = [float(x) for x in a[a.index('--mhist') + 1].split(',')] if '--mhist' in a else None
    mll = a[a.index('--mll') + 1] if '--mll' in a else None
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
    if fixed is not None and fixed != 'm':
        kv.update(fixed_ren_scale='True', fixed_fac_scale='True', muR_ref_fixed=f'{fixed:.4f}',
                  muF_ref_fixed=f'{fixed:.4f}')
    if fixed == 'm':
        kv.update(fixed_ren_scale='True', fixed_fac_scale='True')
    if mll:
        kv['mll'] = mll
    if '--dyn' in a:
        kv['dynamical_scale_choice'] = a[a.index('--dyn') + 1]
    if '--dyn' in a and a[a.index('--dyn') + 1] == '10':   # user scale = M(pair) = invariant mass of particles 3+4
        sf = os.path.join(d, 'SubProcesses', 'setscales.f')
        s = open(sf).read()
        old = ('         write(*,*) "User-defined scale not set"\n         stop 1\n'
               "         temp_scale_id='User-defined dynamical scale' ! use a meaningful string\n         tmp = 0d0\n")
        new = ("         temp_scale_id='qv2: M(pair) of particles 3+4'\n"
               '         tmp=dsqrt(max(0d0,(pp(0,3)+pp(0,4))**2-(pp(1,3)+pp(1,4))**2\n'
               '     &        -(pp(2,3)+pp(2,4))**2-(pp(3,3)+pp(3,4))**2))\n')
        if s.count(old) != 1:
            sys.exit('setscales.f user block not found')
        open(sf, 'w').write(s.replace(old, new))
    set_run(os.path.join(d, 'Cards', 'run_card.dat'), kv)
    if mhist:
        lo, hi, nb = mhist
        open(os.path.join(d, 'FixedOrderAnalysis', 'analysis_HwU_qv2_mpair.f'), 'w').write(
            MPAIR_ANA.replace('@NB@', str(int(nb))).replace('@MLO@', f'{lo:.1f}').replace('@MHI@', f'{hi:.1f}'))
        fc = os.path.join(d, 'Cards', 'FO_analyse_card.dat')
        card = open(fc).read()             # read BEFORE opening for write (the first version truncated the card)
        new, nsub = re.subn(r'(?m)^FO_ANALYSE\s*=.*$', 'FO_ANALYSE = analysis_HwU_qv2_mpair.o', card)
        if nsub != 1:
            sys.exit('FO_ANALYSE line not found in FO_analyse_card.dat')
        open(fc, 'w').write(new)
    res = dict(tag=tag, spin=spin, lhaid=lhaid, fixed_scale=fixed, req_acc_FO=acc, pdfunc=pdfunc,
               node=socket.gethostname(), start=time.strftime('%Y-%m-%d %H:%M:%S %z'), points=[])
    for m in masses:
        for o in orders:
            run = f'{spin}{m}_{o}'
            if fixed == 'm':
                set_run(os.path.join(d, 'Cards', 'run_card.dat'), {'muR_ref_fixed': f'{m:.4f}', 'muF_ref_fixed': f'{m:.4f}'})
            setm = f'set {MASSPAR[spin]} {m}\n' if MASSPAR[spin] else ''
            mg(mgdir, f'launch {d} -n {run}\nfixed_order=ON\norder={o}\ndone\n{setm}done\nexit\n',
               f'launch_{run}', work, f'fo_{o}_m{m}')
            r = parse_summary(os.path.join(d, 'Events', run))
            if mhist:
                r['mpair_hist'] = parse_hwu(os.path.join(d, 'Events', run))
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


FXFX_PTJ, FXFX_QCUT = 30.0, 45.0   # JUDGMENT (logged): v1's MLM xqcut / qCut (produce.py l.51) reused as FxFx mu_Q / qCut


def fxfx_py8_card(sd, nev, qedfsr=True):
    """FxFx shower card: settings of Pythia 8.313 examples/main164fxfx.cmnd (local HEPTools copy) with our qCut/qCutME,
    then v1's CP5 + quirk cards (+ QED-FSR, the S2-d nominal)."""
    L = [f'Main:numberOfEvents = {nev}', 'HEPMCoutput:file = events.hepmc', 'Beams:frameType = 4', 'Check:epTolErr = 2e-2',
         'JetMatching:merge = on', 'JetMatching:scheme = 1', 'JetMatching:setMad = off', f'JetMatching:qCut = {FXFX_QCUT}',
         'JetMatching:coneRadius = 1.0', 'JetMatching:etaJetMax = 10.0', 'SpaceShower:MEcorrections = off',
         'TimeShower:pTmaxMatch = 1', 'TimeShower:pTmaxFudge = 1', 'TimeShower:MEcorrections = off',
         'TimeShower:globalRecoil = on', 'TimeShower:limitPTmaxGlobal = on', 'TimeShower:nMaxGlobalRecoil = 1',
         'TimeShower:globalRecoilMode = 2', 'TimeShower:nMaxGlobalBranch = 1',
         'JetMatching:doFxFx = on', f'JetMatching:qCutME = {FXFX_PTJ}', 'JetMatching:nJetMax = 1']
    for c in ['pythia8_tune_CP5.dat', 'pythia8_quirk_common.dat'] + (['pythia8_quirk_qedfsr.dat'] if qedfsr else []):
        L += strip_comments(open(os.path.join(CARDS, c)).read())
    L += ['LHEFInputs:nSubruns = 1', 'Main:subrun = 0', 'Beams:LHEF = events.lhe.gz', 'Random:setSeed = on',
          f'Random:seed = {sd}']
    return '\n'.join(L) + '\n'


def cmd_fxfx(a):
    """fxfx <tag> <E|S> <mass> <nev> [--shower] [--stage compile|grids|gen] [--acc X]: MC@NLO 0-1j (FxFx) events with
    loop_quirkE, staged so that every runner job stays below 30 min: 'compile' = output + `compile MC` (stamp COMPILED);
    'grids' = first launch without compilation (-x), MINT grids + a few events (stamp READY); 'gen' = launch -x -o
    reusing the grids.  Edgar 2026-11-17 (user exception to the 30-min rule for the first launch, see campaign
    p2-b-s2-fxfx): --save-procdir writes <tag>.procdir.tar.gz (the whole node-local base dir: models, process dir with
    compiled code and MINT grids, COMPILED/READY stamps) to the output dir after the first launch, so that the runner
    publishes it to cajuela; --restore <tar.gz> unpacks such a tarball into the node-local base dir when this node has
    no compiled dir yet (later 'gen' jobs on any worker; the MG copy and env paths are the same on every node).
    The process directory
    lives in node-local /home/scratch/jdochoa/cache/fxfx/<spin>_m<mass> (kept between jobs on the same node): the first
    job makes it (output, compile, grids, first events); later jobs reuse the grids (launch -o)."""
    tag, spin, mass, nev = a[0], a[1], int(a[2]), int(a[3])
    out = os.environ.get('QV2_OUT_DIR', os.getcwd())
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'work')
    os.makedirs(work, exist_ok=True)
    mgdir = local_mg()
    base = os.path.join(LOCAL, 'cache', 'fxfx', f'{spin}_m{mass}')
    d = os.path.join(base, f'{spin}_FXFX')
    ready = os.path.join(base, 'READY')
    info = dict(tag=tag, spin=spin, mass=mass, nev=nev, ptj=FXFX_PTJ, qcut=FXFX_QCUT, node=socket.gethostname(),
                start=time.strftime('%Y-%m-%d %H:%M:%S %z'))
    stage = a[a.index('--stage') + 1] if '--stage' in a else 'all'     # compile | grids | gen | all
    compiled = os.path.join(base, 'COMPILED')
    info['stage'] = stage
    os.makedirs(os.path.join(LOCAL, '.locks'), exist_ok=True)
    with open(os.path.join(LOCAL, '.locks', f'fxfx_{spin}_m{mass}.lock'), 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        if '--restore' in a and not os.path.exists(compiled):
            shutil.rmtree(base, ignore_errors=True)
            os.makedirs(os.path.dirname(base), exist_ok=True)
            with tarfile.open(a[a.index('--restore') + 1], 'r:gz') as tf:
                tf.extractall(os.path.dirname(base))
            info['restored_from'] = a[a.index('--restore') + 1]
        if stage in ('compile', 'all') and not os.path.exists(compiled):
            shutil.rmtree(base, ignore_errors=True)
            models = os.path.join(base, 'models')
            os.makedirs(models)
            timed('make_loop_model', [sys.executable, '-I', os.path.join(QV2, 'phase1_strategy', 'src', 'generators',
                                      'make_loop_quirkE.py'), mgdir, os.path.join(models, 'loop_quirkE')], base,
                  os.path.join(base, 'make_loop.log'))
            pp = 'xe' if spin == 'E' else 'sxe'
            mg(mgdir, f'import model {models}/loop_quirkE-no_b_mass\ndefine p = p b b~\ndefine j = j b b~\n'
                      f'generate p p > {pp}+ {pp}- [QCD] @0\nadd process p p > {pp}+ {pp}- j [QCD] @1\noutput {d}\nexit\n',
               'output_fxfx', base, 'mg_output_fxfx')
            set_conf(os.path.join(d, 'Cards', 'amcatnlo_configuration.txt'),
                     {'lhapdf': LHAPDF_CONFIG, 'lhapdf_py3': LHAPDF_CONFIG, 'run_mode': '0', 'nb_core': '1',
                      'automatic_html_opening': 'False', 'notification_center': 'False', 'fortran_compiler': 'gfortran'})
            set_run(os.path.join(d, 'Cards', 'run_card.dat'),
                    {'ebeam1': '7000.0', 'ebeam2': '7000.0', 'pdlabel': 'lhapdf', 'lhaid': '14400',
                     'parton_shower': 'PYTHIA8', 'ickkw': '3', 'jetalgo': '1', 'jetradius': '1.0',
                     'ptj': f'{FXFX_PTJ:.1f}', 'reweight_scale': 'True', 'reweight_PDF': 'False',
                     'req_acc': a[a.index('--acc') + 1] if '--acc' in a else '-1'})
            pm = os.path.join(d, 'Cards', 'param_card.dat')     # the mass is set once, in the card, for all stages
            txt = open(pm).read()
            txt, nsub = re.subn(r'(?m)^(\s*%d\s+)\S+' % (9000011 if spin == 'E' else 9000013), r'\g<1>%.6e' % mass, txt)
            if nsub < 1:
                sys.exit('mass line not found in param_card')
            open(pm, 'w').write(txt)
            cmdf = os.path.join(base, 'compile.cmd')
            open(cmdf, 'w').write('compile MC -f\nexit\n')
            timed('amcatnlo_compile', [PY, os.path.join(d, 'bin', 'aMCatNLO'), cmdf], base,
                  os.path.join(base, 'compile.log'), mg_env())
            open(compiled, 'w').write(time.ctime() + '\n')
        if stage == 'compile':
            info['steps'] = STEPS
            json.dump(info, open(os.path.join(out, f'{tag}.timing.json'), 'w'), indent=1)
            with tarfile.open(os.path.join(out, f'{tag}.aux.tar.gz'), 'w:gz') as tf:
                for f in glob.glob(os.path.join(base, '*.log')) + glob.glob(os.path.join(base, '*.ps')):
                    tf.add(f, arcname=os.path.basename(f))
            log.info('fxfx compile stage done: %s', STEPS)
            return
        if not os.path.exists(compiled):
            sys.exit('stage %s needs a compiled process dir (run --stage compile first on this node)' % stage)
        first = not os.path.exists(ready)
        if stage == 'gen' and first:
            sys.exit('stage gen needs grids (run --stage grids first on this node)')
        sd = seed(f's2.fxfx.{spin}{mass}', tag, 30000000)
        set_run(os.path.join(d, 'Cards', 'run_card.dat'), {'nevents': str(nev), 'iseed': str(sd)})
        if '--acc' in a:
            set_run(os.path.join(d, 'Cards', 'run_card.dat'), {'req_acc': a[a.index('--acc') + 1]})
        run = tag.replace('-', '_')
        opt = ' -x' + ('' if first else ' -o')
        rec, txt = mg(mgdir, f'launch {d} -n {run}{opt}\nfixed_order=OFF\norder=NLO\nshower=OFF\nmadspin=OFF\n'
                             f'reweight=OFF\ndone\ndone\nexit\n',
                      f'launch_{run}', base, 'amcatnlo_grids_and_events' if first else 'amcatnlo_onlygen')
        if first:
            open(ready, 'w').write(time.ctime() + '\n')
            if '--save-procdir' in a:
                t0 = time.time()
                with tarfile.open(os.path.join(out, f'{tag}.procdir.tar.gz'), 'w:gz') as tf:
                    tf.add(base, arcname=os.path.basename(base))
                info['procdir_tar_s'] = time.time() - t0
    rd = os.path.join(d, 'Events', run)
    lhe = glob.glob(os.path.join(rd, 'events.lhe.gz'))[0]
    m = re.findall(r'Total cross section:\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)\s*pb', txt)
    info.update(first=first, seed_mg=sd, sigma_pb=float(m[-1][0]) if m else None, err_pb=float(m[-1][1]) if m else None)
    with gzip.open(lhe, 'rt') as f:
        nlhe = sum(1 for l in f if l.startswith('<event'))
    info['n_lhe'] = nlhe
    if '--shower' in a:
        pd = os.path.join(work, 'py8')
        os.makedirs(pd)
        shutil.copy(lhe, os.path.join(pd, 'events.lhe.gz'))
        spy = seed(f's2.fxfx.{spin}{mass}', tag + '.py8', 900000000)
        open(os.path.join(pd, 'PY8Card.dat'), 'w').write(fxfx_py8_card(spy, nlhe))
        timed('py8_fxfx', [PY8_EXE, 'PY8Card.dat'], pd, os.path.join(pd, 'PY8_log.txt'), mg_env())
        e = dict(os.environ, NUMBA_CACHE_DIR=os.path.join(work, 'numba'), PYTHONDONTWRITEBYTECODE='1')
        timed('convert_npz', [ANA_PY, os.path.join(SIM, 'scripts', 'convert_hepmc.py'), os.path.join(pd, 'events.hepmc'),
                              os.path.join(out, f'{tag}.npz'), '--mq', str(mass), '--spin', 'F' if spin == 'E' else 'S',
                              '--sigma-lhe-pb', repr(info['sigma_pb'] or 0.0), '--nlhe', str(nlhe), '--tag', tag,
                              '--norm', 'auto'], SIM, os.path.join(work, 'convert.log'), e)
        os.remove(os.path.join(pd, 'events.hepmc'))
    else:
        open(os.path.join(out, f'{tag}.npz'), 'wb').close()
    shutil.copy(lhe, os.path.join(out, f'{tag}.lhe.gz'))
    info['steps'] = STEPS
    info['end'] = time.strftime('%Y-%m-%d %H:%M:%S %z')
    with tarfile.open(os.path.join(out, f'{tag}.aux.tar.gz'), 'w:gz') as tf:
        for f in (glob.glob(os.path.join(base, '*.log')) + glob.glob(os.path.join(rd, '*banner.txt')) +
                  glob.glob(os.path.join(work, '*.log')) + glob.glob(os.path.join(work, 'py8', 'PY8*'))):
            tf.add(f, arcname=os.path.basename(os.path.dirname(f)) + '/' + os.path.basename(f))
    json.dump(info, open(os.path.join(out, f'{tag}.timing.json'), 'w'), indent=1)
    log.info('fxfx done: %s', {k: info[k] for k in ('sigma_pb', 'err_pb', 'n_lhe', 'first')})


VARIANTS = {   # S2-c re-shower variants of the same LHE (STR §4.14 (b)); nominal = CP5, qCut 45, QED-FSR on (S2-d)
    'nom': dict(qc=QCUT, tune='CP5', qedfsr=True),
    'qc30': dict(qc=30.0, tune='CP5', qedfsr=True),
    'qc60': dict(qc=60.0, tune='CP5', qedfsr=True),
    'monash': dict(qc=QCUT, tune='Monash', qedfsr=True),
    'nofsr': dict(qc=QCUT, tune='CP5', qedfsr=False),
}


def shower_convert(lhe, tag, variant, mass, spin, sig_pb, nlhe, work, out, matched=True):
    v = VARIANTS[variant]
    pd = os.path.join(work, f'py8_{variant}')
    os.makedirs(pd)
    shutil.copy(lhe, os.path.join(pd, 'events.lhe.gz'))
    spy = seed(f's2.inc.{tag}', f'py8.{variant}', 900000000)
    open(os.path.join(pd, 'PY8Card.dat'), 'w').write(py8_card(matched, 2, spy, nlhe, qc=v['qc'], tune=v['tune'],
                                                             qedfsr=v['qedfsr']))
    timed(f'py8_{variant}', [PY8_EXE, 'PY8Card.dat'], pd, os.path.join(pd, 'PY8_log.txt'), mg_env())
    e = dict(os.environ, NUMBA_CACHE_DIR=os.path.join(work, 'numba'), PYTHONDONTWRITEBYTECODE='1')
    cmd = [ANA_PY, os.path.join(SIM, 'scripts', 'convert_hepmc.py'), os.path.join(pd, 'events.hepmc'),
           os.path.join(out, f'{tag}.{variant}.npz'), '--mq', str(mass), '--spin', spin, '--sigma-lhe-pb', repr(sig_pb),
           '--nlhe', str(nlhe), '--tag', f'{tag}.{variant}', '--norm', 'auto']
    if matched:
        cmd += ['--merging-nominal', f'{v["qc"]:.3f}']
    timed(f'convert_{variant}', cmd, SIM, os.path.join(work, f'convert_{variant}.log'), e)
    os.remove(os.path.join(pd, 'events.hepmc'))
    return dict(seed_py8=spy, **v)


def cmd_inc(a):
    """inc <tag> <F_INC|S_INC> <mass> <nev>: one S2-c chunk: MLM 0-2j inclusive LHE (v1 INC cards) + nominal shower
    (CP5, qCut 45, QED-FSR) + npz.  Outputs <tag>.lhe.gz, <tag>.nom.npz, <tag>.json, <tag>.aux.tar.gz."""
    tag, proc, mass, nev = a[0], a[1], int(a[2]), int(a[3])
    out = os.environ.get('QV2_OUT_DIR', os.getcwd())
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'work')
    os.makedirs(work, exist_ok=True)
    mgdir = local_mg()
    d = mg_output(mgdir, proc, work, None)
    sd = seed(f's2.inc.{tag}', 'mg', 30000000)
    rd, n, s = mg_launch(mgdir, d, tag.replace('-', '_'), nev, sd, mass, True, 'mg_launch')
    lhe = os.path.join(rd, 'unweighted_events.lhe.gz')
    spin = 'S' if proc.startswith('S') else 'F'
    sh = shower_convert(lhe, tag, 'nom', mass, spin, s, n, work, out)
    shutil.copy(lhe, os.path.join(out, f'{tag}.lhe.gz'))
    info = dict(tag=tag, proc=proc, mass=mass, spin=spin, n_lhe=n, sigma_lhe_pb=s, err_pb=STEPS[-3].get('err_pb'),
                seed_mg=sd, xqcut=XQCUT, nominal=sh, node=socket.gethostname(), steps=STEPS,
                end=time.strftime('%Y-%m-%d %H:%M:%S %z'))
    with tarfile.open(os.path.join(out, f'{tag}.aux.tar.gz'), 'w:gz') as tf:
        for f in glob.glob(os.path.join(rd, '*banner.txt')) + glob.glob(os.path.join(work, '*.log')) + \
                glob.glob(os.path.join(work, 'py8_*', 'PY8*')):
            tf.add(f, arcname=os.path.relpath(f, work))
    json.dump(info, open(os.path.join(out, f'{tag}.json'), 'w'), indent=1)


def cmd_reshower(a):
    """reshower <tag> <inc_dir_on_cajuela> <variant>[,<variant>]: re-shower the LHE of an inc chunk (read from its
    published file; the inc job's done marker is checked by the runner campaign order, and the sha256 here)."""
    tag, src, variants = a[0], a[1], a[2].split(',')
    out = os.environ.get('QV2_OUT_DIR', os.getcwd())
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'work')
    os.makedirs(work, exist_ok=True)
    meta = json.load(open(os.path.join(src, f'{tag}.json')))
    lhe = os.path.join(work, 'in.lhe.gz')
    shutil.copy(os.path.join(src, f'{tag}.lhe.gz'), lhe)
    res = dict(tag=tag, src=src, lhe_sha256=hashlib.sha256(open(lhe, 'rb').read()).hexdigest(), variants={})
    for v in variants:
        res['variants'][v] = shower_convert(lhe, tag, v, meta['mass'], meta['spin'], meta['sigma_lhe_pb'],
                                            meta['n_lhe'], work, out)
    res.update(steps=STEPS, node=socket.gethostname(), end=time.strftime('%Y-%m-%d %H:%M:%S %z'))
    json.dump(res, open(os.path.join(out, f'{tag}.rs.{"_".join(variants)}.json'), 'w'), indent=1)


if __name__ == '__main__':
    args = sys.argv[1:]
    if os.environ.get('QV2_LOCAL_ENV') == '1':
        use_local_env()
    if args[0] in ('inc', 'reshower'):
        {'inc': cmd_inc, 'reshower': cmd_reshower}[args[0]](args[1:])
        sys.exit(0)
    if args[0] == 'fxfx':
        cmd_fxfx(args[1:])
        sys.exit(0)
    {'mlmtime': cmd_mlmtime, 'nlo': cmd_nlo, 'lotree': cmd_lotree}[args[0]](args[1:])
