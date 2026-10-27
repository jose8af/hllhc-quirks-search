# shower the MG-flow 'cardgrab' LHE with our split jobs using MG's own split card (PY8Card_0.dat, seeds unset);
# compare event-by-event with MG's merged HepMC.
import os, sys, subprocess, shutil
sys.path.insert(0, 'scripts'); import produce as P
G, lhe = sys.argv[1], sys.argv[2]
splits, n = P.split_lhe(lhe, G + '/mine', 6)
e = P.env(); e['DYLD_LIBRARY_PATH'] = os.path.join(P.MG, 'HEPTools', 'lib')
card = open(G + '/PY8Card_0.dat').read()
ps = []
for j, (sd, sz) in enumerate(splits):
    open(os.path.join(sd, 'PY8Card.dat'), 'w').write(card.replace('Main:numberOfEvents      = 334', f'Main:numberOfEvents      = {sz}'))
    ps.append(subprocess.Popen([P.PY8_EXE, 'PY8Card.dat'], cwd=sd, stdout=open(sd + '/log.txt', 'w'), stderr=subprocess.STDOUT, env=e))
for p in ps: p.wait()
print([p.returncode for p in ps], [sz for _, sz in splits])
