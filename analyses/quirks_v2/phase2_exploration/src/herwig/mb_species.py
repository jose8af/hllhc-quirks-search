"""mb_species.py -- [DP5] string (Pythia 8) against cluster (Herwig 7) hadronisation at generator level: charged
pi, K, p yields in minimum-bias pp at 14 TeV, |eta| < 2.5, in p_T bins (channel (ii), Sebastian, 2026-11-16).

  herwig <out.json> <nev> <seed>   run Herwig 7.3.0 LHC-MB setup (snippets/MB.in + Diffraction.in, its own CT14lo tune
                                   PDF) at sqrt(s) = 14 TeV, HepMC2 GenEvent output in scratch, then count
  pythia <out.json> <nev> <seed>   Pythia 8.312 (acts env) with v1 PY_MB + CP5 (acts/stage4/code/s4pu.py l.32-34)

Stable-particle convention made equal in both: particles with c*tau > 1000 mm are not decayed (v1 PY_MB:
ParticleDecays:limitTau0 = on, tau0Max = 1000; Herwig: DecayHandler MaxLifeTime 1000*mm, LifeTimeOption Average),
so pi+-, K+- and K_L are final, K_S and hyperons decay.  Counted: final-state |pdg| 211, 321, 2212, |eta| < 2.5.
Output: counts per species and p_T bin, the number of events, CPU; ratios are formed by the evaluation step.
"""
import json
import logging
import math
import os
import resource
import subprocess
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stdout)
log = logging.getLogger('mb_species')
PT_EDGES = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 1e9]
SPECIES = {211: 'pi', 321: 'K', 2212: 'p'}
ETA_MAX = 2.5
HW_ENV = '/home/scratch/jdochoa/envs/herwig/.pixi/envs/default'
HW_PDF = '/home/scratch/jdochoa/lhapdf_herwig'
CP5 = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/sim/cards/pythia8_tune_CP5.dat'


def empty():
    return {s: [0] * (len(PT_EDGES) - 1) for s in SPECIES.values()}


def fill(cnt, pdg, px, py, pz):
    a = abs(pdg)
    if a not in SPECIES:
        return
    pt = math.hypot(px, py)
    if pt < PT_EDGES[0]:
        return
    p = math.sqrt(pt * pt + pz * pz)
    eta = 0.5 * math.log((p + pz) / (p - pz)) if p > abs(pz) else 99.0
    if abs(eta) >= ETA_MAX:
        return
    for i in range(len(PT_EDGES) - 1):
        if pt < PT_EDGES[i + 1]:
            cnt[SPECIES[a]][i] += 1
            return


def run_herwig(out, nev, seed):
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'hw')
    os.makedirs(work, exist_ok=True)
    inp = f"""read snippets/PPCollider.in
cd /Herwig/Generators
set EventGenerator:EventHandler:LuminosityFunction:Energy 14000.0
set /Herwig/Shower/ShowerHandler:IntrinsicPtGaussian 2.2*GeV
read snippets/MB.in
read snippets/Diffraction.in
set /Herwig/Decays/DecayHandler:MaxLifeTime 1000*mm
set /Herwig/Decays/DecayHandler:LifeTimeOption Average
read snippets/HepMC.in
set /Herwig/Analysis/HepMC:PrintEvent {nev}
cd /Herwig/Generators
saverun qv2mb EventGenerator
"""
    open(os.path.join(work, 'qv2mb.in'), 'w').write(inp)
    env = dict(os.environ, LHAPDF_DATA_PATH=HW_PDF, PATH=os.path.join(HW_ENV, 'bin') + ':' + os.environ['PATH'])
    env.pop('LD_LIBRARY_PATH', None)
    t0 = time.time()
    for cmd in (['Herwig', 'read', 'qv2mb.in'], ['Herwig', 'run', 'qv2mb.run', '-N', str(nev), '-s', str(seed)]):
        r = subprocess.run(cmd, cwd=work, env=env, stdout=open(os.path.join(work, cmd[1] + '.log'), 'w'),
                           stderr=subprocess.STDOUT)
        if r.returncode != 0:
            sys.exit(f'{cmd} failed: see {work}/{cmd[1]}.log')
    t_gen = time.time() - t0
    hep = [f for f in os.listdir(work) if f.endswith('.hepmc')]
    if not hep:
        sys.exit('no HepMC output')
    cnt, nevt = empty(), 0
    with open(os.path.join(work, hep[0])) as f:
        for line in f:
            if line[0] == 'E':
                nevt += 1
            elif line[0] == 'P':
                v = line.split()
                if v[8] == '1':
                    fill(cnt, int(v[2]), float(v[3]), float(v[4]), float(v[5]))
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    res = dict(generator='Herwig 7.3.0 (ThePEG 2.3.0), LHC-MB setup, CT14lo, 14 TeV', n_events=nevt, seed=seed,
               counts=cnt, pt_edges=PT_EDGES, eta_max=ETA_MAX, cpu_children_s=ru.ru_utime + ru.ru_stime,
               wall_gen_s=t_gen, input=inp)
    json.dump(res, open(out, 'w'), indent=1)
    log.info('herwig: %d events, counts %s', nevt, {k: sum(v) for k, v in cnt.items()})


def run_pythia(out, nev, seed):
    import pythia8
    py = pythia8.Pythia('', False)
    py.readFile(CP5)
    for l in ('Beams:eCM = 14000.', 'SoftQCD:inelastic = on', 'ParticleDecays:limitTau0 = on',
              'ParticleDecays:tau0Max = 1000.', 'Print:quiet = on', 'Next:numberCount = 0', 'Random:setSeed = on',
              f'Random:seed = {seed}'):
        py.readString(l)
    if not py.init():
        sys.exit('pythia init failed')
    cnt, nevt = empty(), 0
    t0 = time.process_time()
    for _ in range(nev):
        if not py.next():
            continue
        nevt += 1
        ev = py.event
        for i in range(ev.size()):
            p = ev[i]
            if p.isFinal():
                fill(cnt, p.id(), p.px(), p.py(), p.pz())
    res = dict(generator='Pythia 8.312 (acts env), CP5 + v1 PY_MB without the pi/K/mu/K_L mayDecay-off lines '
                         '(tau0Max = 1000 mm keeps them stable anyway)', n_events=nevt, seed=seed, counts=cnt,
               pt_edges=PT_EDGES, eta_max=ETA_MAX, cpu_s=time.process_time() - t0)
    json.dump(res, open(out, 'w'), indent=1)
    log.info('pythia: %d events, counts %s', nevt, {k: sum(v) for k, v in cnt.items()})


if __name__ == '__main__':
    mode, out, nev, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    {'herwig': run_herwig, 'pythia': run_pythia}[mode](out, nev, seed)
