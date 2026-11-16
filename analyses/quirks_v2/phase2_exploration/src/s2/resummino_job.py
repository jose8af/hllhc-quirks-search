"""resummino_job.py -- S2-a validation 2 reference: Resummino 3.1.2 (conda-forge, node-local env on maxwell) for
right-handed selectron pairs (PDG 2000011) at 14 TeV, fixed order LO and NLO (`--nlo` stops after NLO), and NLO+NLL
(no flag) for the resummed cross-check of S2-b (channel (ii), Sebastian, 2026-11-16).

Settings matched to our loop_quirkE runs: CT18NLO (LHAPDF 14400) for LO and NLO, mu_R = mu_F = (m1 + m2)/2 = m
(Resummino's central scale), SM inputs of the v1 UFO (restrict_no_b_mass.dat: aEWM1 132.507, Gf 1.16639e-5, MZ 91.188),
W mass computed with the UFO's own formula (parameters.py: MW = sqrt(MZ^2/2 + sqrt(MZ^4/4 - aEW*pi*MZ^2/(Gf*sqrt2)))).
The SLHA file is the HEPcodes/resummino example input/slha.in (sha256 cef17bfc..., retrieval_log #18) with SMINPUTS,
MASS 24 and MASS 2000011 replaced.  The card is the example input/resummino.in (sha256 c938e187...) with the collider,
particles, PDF and precision lines replaced.
Usage: python3 -I resummino_job.py <out.json> <m1,m2,...> [--modes lo_nlo,nll]
"""
import json
import math
import os
import re
import resource
import subprocess
import sys
import time

ENV = '/home/scratch/jdochoa/envs/herwig/.pixi/envs/default'
RETR = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/s2/resummino_inputs'
AEWM1, GF, MZ = 132.50698, 1.16639e-5, 91.188     # sim/models/quirkE/parameters.py l.21-32, l.125-128 (v1 UFO)


def mw():
    aew = 1.0 / AEWM1
    return math.sqrt(MZ ** 2 / 2 + math.sqrt(MZ ** 4 / 4 - aew * math.pi * MZ ** 2 / (GF * math.sqrt(2))))


DECOUPLE = '--decouple' in sys.argv   # squarks (PDG 100000[1-6], 200000[1-6]) and gluino (1000021) at 1e5 GeV


def slha(m):
    t = open(os.path.join(RETR, 'slha.in')).read()
    if DECOUPLE:
        t = re.sub(r'(?m)^(\s*(?:[12]00000[1-6]|1000021)\s+)\S+(\s*#.*)$', r'\g<1>1.00000000E+05\2', t)
    t = re.sub(r'(?m)^(\s*1\s+)\S+(\s*#\s*alpha_em\^-1.*)$', rf'\g<1>{AEWM1:.8E}\2', t)
    t = re.sub(r'(?m)^(\s*4\s+)\S+(\s*#\s*M_Z pole mass.*)$', rf'\g<1>{MZ:.8E}\2', t)
    t = re.sub(r'(?m)^(\s*24\s+)\S+(\s*#\s*W\+.*)$', rf'\g<1>{mw():.8E}\2', t)
    t = re.sub(r'(?m)^(\s*2000011\s+)\S+(\s*#\s*~e_R.*)$', rf'\g<1>{float(m):.8E}\2', t)
    return t


def card():
    t = open(os.path.join(RETR, 'resummino.in')).read()
    rep = {'center_of_mass_energy': '14000', 'particle1': '2000011', 'particle2': '-2000011', 'pdf_lo': 'CT18NLO',
           'pdfset_lo': '0', 'pdf_nlo': 'CT18NLO', 'pdfset_nlo': '0', 'precision': '0.001', 'max_iters': '10',
           'slha': 'slha.in'}
    for k, v in rep.items():
        t, n = re.subn(rf'(?m)^{k}\s*=\s*\S+', f'{k} = {v}', t)
        if n != 1:
            sys.exit(f'card key {k} found {n} times')
    return t


def parse(txt):
    out = {}
    for lab in ('LO', 'NLO', 'NLO+NLL'):
        m = re.search(rf'^{re.escape(lab)}\s*=\s*\(?\s*([0-9.eE+-]+)\s*(?:\+-|±)\s*([0-9.eE+-]+)\s*\)?\s*pb', txt, re.M)
        if m:
            out[lab] = (float(m.group(1)), float(m.group(2)))
    return out


def main():
    outp, masses = sys.argv[1], [int(x) for x in sys.argv[2].split(',')]
    modes = sys.argv[sys.argv.index('--modes') + 1].split(',') if '--modes' in sys.argv else ['lo_nlo', 'nll']
    work = os.path.join(os.environ.get('QV2_SCRATCH_DIR', os.getcwd()), 'rs')
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, LHAPDF_DATA_PATH='/home/users/jdochoa/sw/lhapdf_data',
               PATH=os.path.join(ENV, 'bin') + ':' + os.environ['PATH'])
    env.pop('LD_LIBRARY_PATH', None)
    res = dict(code='Resummino 3.1.2 (conda-forge)', decouple=DECOUPLE, mw_gev=mw(), aewm1=AEWM1, gf=GF, mz=MZ, points=[])
    open(os.path.join(work, 'resummino.in'), 'w').write(card())
    for m in masses:
        open(os.path.join(work, 'slha.in'), 'w').write(slha(m))
        for mode in modes:
            flag = ['--nlo'] if mode == 'lo_nlo' else ['--nll']
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
            t0 = time.time()
            p = subprocess.run([os.path.join(ENV, 'bin', 'resummino')] + flag +
                               [f'--parameter-log=params_m{m}.log', 'resummino.in'], cwd=work, env=env,
                               capture_output=True, text=True)
            r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            open(os.path.join(work, f'out_m{m}_{mode}.txt'), 'w').write(p.stdout + p.stderr)
            res['points'].append(dict(mass=m, mode=mode, rc=p.returncode, results=parse(p.stdout),
                                      cpu_s=(r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime),
                                      wall_s=time.time() - t0, stdout_tail=p.stdout[-1500:], stderr_tail=p.stderr[-800:]))
            pl = os.path.join(work, f'params_m{m}.log')
            if os.path.exists(pl):
                res['points'][-1]['params_log_head'] = open(pl).read()[:3000]
    json.dump(res, open(outp, 'w'), indent=1)


if __name__ == '__main__':
    main()
