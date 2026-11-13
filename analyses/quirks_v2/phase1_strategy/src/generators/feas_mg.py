"""feas_mg.py -- MG5_aMC 2.9.22 + Pythia 8.313 feasibility driver (quirks v2 Phase 1, executor Basil, 2026-11-13).
Stdlib only; run with any python3 >= 3.8.  It calls MG through the pixi env `sw/envs/mg` (Python 3.9) and the
MG5aMC_PY8_interface from HEPTools.  Mirrors the v1 flow of TT/sim/scripts/produce.py (shower OFF in MG, our own PY8
card with the tune first, one interface job per split) for one process at a time.

  python3 feas_mg.py output <proc> <outdir>                      # MG process generation (+ code output)
  python3 feas_mg.py launch <outdir> <run> <nev> <seed> [mass]   # LO events (LHE), nb_core=1
  python3 feas_mg.py shower <outdir> <run> <seed> [qedfsr]       # PY8 shower of the run's LHE -> HepMC
  python3 feas_mg.py xsec <outdir> <run>                         # print sigma +- err from the banner / results
Processes: E_LOPS (p p > xe+ xe-, v1 F_LOPS), ZNN_J (p p > vl vl~ j, MET > 200 GeV; v1 SM list: Z(nunu)+j),
           E_NLO (p p > xe+ xe- [QCD], loop_quirkE, fixed order).
"""
import glob
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SW = os.environ.get('QV2_SW', '/home/users/jdochoa/sw')
MG = os.path.join(SW, 'mg5', 'MG5_aMC_v2_9_22')
ENV = os.path.join(SW, 'envs', 'mg', '.pixi', 'envs', 'default')
PY = os.path.join(ENV, 'bin', 'python3')
LHAPDF_CONFIG = os.path.join(ENV, 'bin', 'lhapdf-config')
LHAPDF_DATA = os.path.join(SW, 'lhapdf_data')
TT = '/home/users/jdochoa/hllhc-quirks-search/stage2_C001_quirks/theory_track'
CARDS = os.path.join(TT, 'sim', 'cards')          # v1 cards, read-only
MODELS = os.environ.get('QV2_MODELS', os.path.join(HERE, 'models'))   # copy to local scratch before running
MODEL = os.path.join(MODELS, 'quirkE-no_b_mass')   # copy of v1 TT/sim/models/quirkE (imported with restriction)
LOOPMODEL = os.path.join(MODELS, 'loop_quirkE-no_b_mass')
SYST = "['--mur=0.5,1,2', '--muf=0.5,1,2', '--dyn=-1,1,2,3,4', '--pdf=CT18NLO,NNPDF23_lo_as_0130_qed@0']"

PROCS = {
    'E_LOPS': (f'import model {MODEL}\ndefine p = p b b~\ndefine j = j b b~\ngenerate p p > xe+ xe-\n', 'lo'),
    'ZNN_J': ('import model sm-no_b_mass\ndefine p = p b b~\ndefine j = j b b~\ngenerate p p > vl vl~ j\n', 'lo'),
    'E_NLO': (f'import model {LOOPMODEL}\ndefine p = p b b~\ndefine j = j b b~\ngenerate p p > xe+ xe- [QCD]\n', 'nlo'),
}
RUNKV = {'lo': {'ebeam1': '7000.0', 'ebeam2': '7000.0', 'pdlabel': 'lhapdf', 'lhaid': '14400', 'use_syst': 'True',
                'systematics_arguments': SYST},
         'nlo': {'ebeam1': '7000.0', 'ebeam2': '7000.0', 'pdlabel': 'lhapdf', 'lhaid': '14400',
                 'store_rwgt_info': 'False', 'reweight_scale': 'False', 'reweight_PDF': 'False'}}
EXTRA = {'ZNN_J': {'misset': '200.0'}}


def env():
    e = dict(os.environ)
    e['LHAPDF_DATA_PATH'] = LHAPDF_DATA
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    e['PATH'] = os.path.join(ENV, 'bin') + ':' + e.get('PATH', '')
    # NOT the conda env lib dir: it holds libgfortran 16, whose runtime rejects the '$' edit descriptor that MG 2.9.22
    # Fortran uses (symmetry.f l.233 "(I1$)" -> "Missing comma between descriptors"); MG code is compiled with the
    # system gfortran 13 and must run with its runtime.
    e.pop('LD_LIBRARY_PATH', None)
    return e


def mg(script, log, cwd):
    p = os.path.join(cwd, log + '.mg')
    open(p, 'w').write(script)
    with open(os.path.join(cwd, log + '.log'), 'w') as lf:
        r = subprocess.run([PY, os.path.join(MG, 'bin', 'mg5_aMC'), p], cwd=cwd, stdout=lf, stderr=subprocess.STDOUT,
                           env=env(), stdin=subprocess.DEVNULL)
    t = open(os.path.join(cwd, log + '.log')).read()
    if r.returncode != 0 or 'interrupted with error' in t or 'ERROR DETECTED' in t or 'Command "' in t and 'Error' in t:
        sys.exit(f'MG failed: see {cwd}/{log}.log')
    return t


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
    txt = open(path).read()
    for k, v in kv.items():
        new, n = re.subn(r'^(\s*)(\S.*?)(\s*=\s*%s\b)' % re.escape(k), lambda m: f'{m.group(1)}{v}{m.group(3)}', txt,
                         flags=re.M)
        if n == 0:
            sys.exit(f'run_card key {k} not found in {path}')
        txt = new
    open(path, 'w').write(txt)


def cmd_output(proc, outdir):
    gen, kind = PROCS[proc]
    outdir = os.path.abspath(outdir)
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    cwd = os.path.dirname(outdir)
    # NLO: MadLoop asks which loop-reduction tools to install into the MG install (on NFS). Answer: CutTools + IREGI only
    # (built inside the local output dir); no ninja / collier / OneLOop (enough for a 2 -> 2 DY-like process).
    # The install's input/mg5_configuration.txt now has ninja/collier/golem = None (install_generators.sh), so MG no
    # longer asks; set them here too only if the question would still come.
    cfg = open(os.path.join(MG, 'input', 'mg5_configuration.txt')).read()
    ans = '' if kind == 'lo' or re.search(r'^ninja = None', cfg, re.M) else 'ninja noinstall\ncollier noinstall\ngolem noinstall\ndone\n'
    mg(gen + f'output {outdir}{" -nojpeg" if kind == "lo" else ""}\n{ans}exit\n', f'output_{proc}', cwd)
    conf = {'lhapdf': LHAPDF_CONFIG, 'lhapdf_py3': LHAPDF_CONFIG, 'pythia8_path': os.path.join(MG, 'HEPTools', 'pythia8'),
            'mg5amc_py8_interface_path': os.path.join(MG, 'HEPTools', 'MG5aMC_PY8_interface'),
            'run_mode': '0', 'nb_core': '1', 'automatic_html_opening': 'False', 'notification_center': 'False',
            'fortran_compiler': 'gfortran'}
    set_conf(os.path.join(outdir, 'Cards', 'me5_configuration.txt' if kind == 'lo' else 'amcatnlo_configuration.txt'), conf)
    kv = dict(RUNKV[kind]); kv.update(EXTRA.get(proc, {}))
    set_run(os.path.join(outdir, 'Cards', 'run_card.dat'), kv)
    open(os.path.join(outdir, 'KIND'), 'w').write(kind)
    print('output done', outdir)


def cmd_launch(outdir, run, nev, seed, mass=None):
    outdir = os.path.abspath(outdir)
    kind = open(os.path.join(outdir, 'KIND')).read().strip()
    set_run(os.path.join(outdir, 'Cards', 'run_card.dat'), {'nevents': str(nev), 'iseed': str(seed)})
    if kind == 'nlo':   # fixed-order: target 0.2 % MC accuracy, scale band by reweighting (no extra runs)
        set_run(os.path.join(outdir, 'Cards', 'run_card.dat'), {'req_acc_FO': '0.002', 'reweight_scale': 'True'})
    rd = os.path.join(outdir, 'Events', run)
    if os.path.exists(rd):
        shutil.rmtree(rd)
    s = f'launch {outdir} -n {run}\n'
    if kind == 'lo':
        s += 'shower=OFF\n' if os.path.isdir(os.path.join(MG, 'HEPTools', 'pythia8')) else ''
    else:
        s += 'fixed_order=ON\n' + ('order=LO\n' if run.endswith('_LO') else 'order=NLO\n')
    s += 'done\n'                      # end of the switch question; the card-edit question follows
    if mass:
        s += f'set MXE {mass}\n'
    s += 'done\nexit\n'
    t = mg(s, f'launch_{run}', os.path.dirname(outdir))
    print('\n'.join(l for l in t.split('\n') if 'ross-section' in l or 'Nb of events' in l or 'Total cross' in l))


def banner(outdir, run):
    b = glob.glob(os.path.join(outdir, 'Events', run, '*_banner.txt'))[0]
    t = open(b).read()
    n = int(re.search(r'#\s*Number of Events\s*:\s*(\d+)', t).group(1))
    s = float(re.search(r'#\s*Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)', t).group(1))
    return n, s


def strip_comments(t):
    o = []
    for l in t.split('\n'):
        l = l.split('!')[0].rstrip()
        if l:
            o.append(l)
    return o


def cmd_shower(outdir, run, seed, qedfsr=False):
    """PY8 card for an UNMATCHED sample, as produce.py:py8_card(matched=False) (l.170-194), tune first."""
    outdir = os.path.abspath(outdir)
    rd = os.path.join(outdir, 'Events', run)
    n, s = banner(outdir, run)
    tag = 'py8' + ('_qed' if qedfsr else '')
    pd = os.path.join(rd, tag)
    os.makedirs(pd, exist_ok=True)
    lhe = os.path.join(rd, 'unweighted_events.lhe.gz')
    if not os.path.exists(os.path.join(pd, 'events.lhe.gz')):
        os.symlink(lhe, os.path.join(pd, 'events.lhe.gz'))
    L = [f'Main:numberOfEvents = {n}', 'HEPMCoutput:file = events.hepmc', 'SysCalc:fullCutVariation = off']
    cards = ['pythia8_tune_CP5.dat', 'pythia8_quirk_common.dat'] + (['pythia8_quirk_qedfsr.dat'] if qedfsr else [])
    for c in cards:
        L += strip_comments(open(os.path.join(CARDS, c)).read())
    L += ['Beams:frameType=4', 'HEPMCoutput:scaling=1.0e+09', 'Check:epTolErr=1.0e-02', 'JetMatching:etaJetMax=1.0e+03',
          'JetMatching:setMad=off', 'LHEFInputs:nSubruns=1', 'Main:subrun=0', 'Beams:LHEF=events.lhe.gz',
          'Random:setSeed=on', f'Random:seed={seed}']
    open(os.path.join(pd, 'PY8Card.dat'), 'w').write('\n'.join(L) + '\n')
    exe = os.path.join(MG, 'HEPTools', 'MG5aMC_PY8_interface', 'MG5aMC_PY8_interface')
    with open(os.path.join(pd, 'PY8_log.txt'), 'w') as lf:
        r = subprocess.run([exe, 'PY8Card.dat'], cwd=pd, stdout=lf, stderr=subprocess.STDOUT, env=env())
    if r.returncode != 0 or not os.path.exists(os.path.join(pd, 'events.hepmc')):
        sys.exit(f'PY8 failed, see {pd}/PY8_log.txt')
    print('shower done', pd, os.path.getsize(os.path.join(pd, 'events.hepmc')))


def cmd_xsec(outdir, run):
    n, s = banner(os.path.abspath(outdir), run)
    rh = glob.glob(os.path.join(outdir, 'Events', run, '*banner.txt'))[0]
    t = open(rh).read()
    m = re.search(r'#\s*Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)', t)
    print(f'N={n} sigma_pb={s}')


if __name__ == '__main__':
    a = sys.argv[1:]
    {'output': lambda: cmd_output(a[1], a[2]),
     'launch': lambda: cmd_launch(a[1], a[2], int(a[3]), int(a[4]), a[5] if len(a) > 5 else None),
     'shower': lambda: cmd_shower(a[1], a[2], int(a[3]), len(a) > 4 and a[4] == 'qedfsr'),
     'xsec': lambda: cmd_xsec(a[1], a[2])}[a[0]]()
