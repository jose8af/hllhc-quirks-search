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
PT_EDGES = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 1e9]
ETA_EDGES = [0.0, 1.0, 1.5, 2.5]   # |eta| bins (orchestrator request 2026-11-16: |eta| < 1 and 1-1.5)
SPECIES = {211: 'pi', 321: 'K', 2212: 'p'}
ETA_MAX = 2.5
HW_ENV = '/home/scratch/jdochoa/envs/herwig/.pixi/envs/default'
HW_PDF = '/home/scratch/jdochoa/lhapdf_herwig'
CP5 = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/sim/cards/pythia8_tune_CP5.dat'


def empty():
    """counts[species][eta_bin][pt_bin]; species pi, K, p and 'ch' = all charged final-state particles."""
    return {s: [[0] * (len(PT_EDGES) - 1) for _ in range(len(ETA_EDGES) - 1)] for s in list(SPECIES.values()) + ['ch']}


def fill(cnt, pdg, px, py, pz, charged):
    a = abs(pdg)
    if a not in SPECIES and not charged:
        return
    pt = math.hypot(px, py)
    if pt < PT_EDGES[0]:
        return
    p = math.sqrt(pt * pt + pz * pz)
    eta = abs(0.5 * math.log((p + pz) / (p - pz))) if p > abs(pz) else 99.0
    if eta >= ETA_EDGES[-1]:
        return
    ie = next(k for k in range(len(ETA_EDGES) - 1) if eta < ETA_EDGES[k + 1])
    ip = next(k for k in range(len(PT_EDGES) - 1) if pt < PT_EDGES[k + 1])
    if charged:
        cnt['ch'][ie][ip] += 1
    if a in SPECIES:
        cnt[SPECIES[a]][ie][ip] += 1


def charge3(pid):
    """3 x electric charge from the PDG Monte Carlo numbering scheme (leptons, gauge bosons, mesons, baryons).
    Quark charges in units of e/3: d,s,b = -1; u,c,t = +2."""
    a = abs(pid)
    s = 1 if pid > 0 else -1
    q = {1: -1, 2: 2, 3: -1, 4: 2, 5: -1, 6: 2}
    if a in (11, 13, 15):
        return -3 * s
    if a in (12, 14, 16, 22, 21, 23, 25, 130, 310):
        return 0
    if a == 24:
        return 3 * s
    n = a % 10000
    nq1, nq2, nq3 = (n // 1000) % 10, (n // 100) % 10, (n // 10) % 10
    if nq1 == 0:            # meson: quark nq2, antiquark nq3
        if nq2 == 0 or nq3 == 0:
            return 0
        c = q[nq2] - q[nq3]
        if nq2 % 2 == 1 and nq2 != nq3 and q[nq2] == q[nq3]:
            pass
        # sign convention: for mesons the heavier quark sets the particle; PDG: e.g. 211 = u d~ -> +3
        c = abs(c) * (1 if (q[nq2] - q[nq3]) * (1 if nq2 % 2 == 0 else -1) >= 0 else -1) if c else 0
        return c * s
    return (q.get(nq1, 0) + q.get(nq2, 0) + q.get(nq3, 0)) * s


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
                    pid = int(v[2])
                    fill(cnt, pid, float(v[3]), float(v[4]), float(v[5]), charge3(pid) != 0)
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    res = dict(generator='Herwig 7.3.0 (ThePEG 2.3.0), LHC-MB setup, CT14lo, 14 TeV', n_events=nevt, seed=seed,
               counts=cnt, pt_edges=PT_EDGES, eta_edges=ETA_EDGES, eta_max=ETA_MAX, cpu_children_s=ru.ru_utime + ru.ru_stime,
               wall_gen_s=t_gen, input=inp)
    json.dump(res, open(out, 'w'), indent=1)
    log.info('herwig: %d events, counts %s', nevt, {k: sum(map(sum, v)) for k, v in cnt.items()})


def run_pythia(out, nev, seed):
    import pythia8
    xml = os.environ.get('PYTHIA8DATA') or os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'share', 'Pythia8', 'xmldoc')
    py = pythia8.Pythia(xml, False)   # the conda activation (PYTHIA8DATA) is not run by the job
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
                fill(cnt, p.id(), p.px(), p.py(), p.pz(), p.isCharged())
    res = dict(generator='Pythia 8.312 (acts env), CP5 + v1 PY_MB without the pi/K/mu/K_L mayDecay-off lines '
                         '(tau0Max = 1000 mm keeps them stable anyway)', n_events=nevt, seed=seed, counts=cnt,
               pt_edges=PT_EDGES, eta_edges=ETA_EDGES, eta_max=ETA_MAX, cpu_s=time.process_time() - t0)
    json.dump(res, open(out, 'w'), indent=1)
    log.info('pythia: %d events, counts %s', nevt, {k: sum(map(sum, v)) for k, v in cnt.items()})


if __name__ == '__main__':
    mode, out, nev, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    {'herwig': run_herwig, 'pythia': run_pythia}[mode](out, nev, seed)
