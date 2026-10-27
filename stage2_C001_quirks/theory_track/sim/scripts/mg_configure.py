"""mg_configure.py -- set the local tool paths and run-card values of a MadGraph output directory in sim/mg_out/
(never touches the MG install).  Usage (any python >= 3.8):
  python scripts/mg_configure.py <mg_out_dir> key=value [key=value ...]
Keys go to Cards/run_card.dat ('nevents=1000', 'lhaid=14400', ...).  Special keys: nb_core=N (me5_configuration).
Always sets: lhapdf/lhapdf_py3 -> sim/.pixi/envs/mg/bin/lhapdf-config (conda-forge LHAPDF 6.5.5 with working py3.9
bindings; the HEPTools py3.9 bindings segfault: linked to a missing libpython3.9.dylib), pythia8 and PY8-interface paths
from HEPTools, run_mode=2 (multicore), automatic_html_opening=False, notification_center=False.
"""
import os, re, sys

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MG = os.environ.get('MG5_DIR', '')     # MadGraph5_aMC v2.9.22 install with HEPTools (Pythia8, MG5aMC_PY8_interface); see REPRODUCE.md
CONF = {'lhapdf': os.path.join(SIM, '.pixi/envs/mg/bin/lhapdf-config'),
        'lhapdf_py3': os.path.join(SIM, '.pixi/envs/mg/bin/lhapdf-config'),
        'pythia8_path': os.path.join(MG, 'HEPTools/pythia8'),
        'mg5amc_py8_interface_path': os.path.join(MG, 'HEPTools/MG5aMC_PY8_interface'),
        'run_mode': '2', 'nb_core': '6', 'automatic_html_opening': 'False', 'notification_center': 'False'}


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
        new, n = re.subn(r'^(\s*)(\S.*?)(\s*=\s*%s\b)' % re.escape(k), lambda m: f'{m.group(1)}{v}{m.group(3)}', txt, flags=re.M)
        if n == 0:
            new = txt + f'\n {v} = {k}\n'
        txt = new
    open(path, 'w').write(txt)


if __name__ == '__main__':
    if not MG:
        sys.exit('set MG5_DIR to the MadGraph5_aMC v2.9.22 install (see REPRODUCE.md)')
    d = sys.argv[1]
    kv = dict(a.split('=', 1) for a in sys.argv[2:])
    conf = dict(CONF)
    if 'nb_core' in kv:
        conf['nb_core'] = kv.pop('nb_core')
    set_conf(os.path.join(d, 'Cards', 'me5_configuration.txt'), conf)
    set_run(os.path.join(d, 'Cards', 'run_card.dat'), kv)
    print('configured', d, kv)
