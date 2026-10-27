# flow test: shower the old-flow E-INC m500 c0 LHE (first 2 of 6 splits) with our own PY8 job setup; compare acceptance
import os, sys, subprocess
sys.path.insert(0, 'scripts')
import produce as P
T = [t for t in P.TASKS if t['id'] == 'E-INC'][0]
out = sys.argv[1]
splits, n = P.split_lhe('../data/sim/lhe/E-INC/m500_c0.lhe.gz', out, 6)
e = P.env(); e['DYLD_LIBRARY_PATH'] = os.path.join(P.MG, 'HEPTools', 'lib')
ps = []
for j, (sd, sz) in enumerate(splits[:2]):
    open(os.path.join(sd, 'PY8Card.dat'), 'w').write(P.py8_card(T, True, 2, 777 + j, sz))
    ps.append(subprocess.Popen([P.PY8_EXE, 'PY8Card.dat'], cwd=sd, stdout=open(os.path.join(sd, 'log.txt'), 'w'), stderr=subprocess.STDOUT, env=e))
for p in ps: p.wait()
print('done', [p.returncode for p in ps])
