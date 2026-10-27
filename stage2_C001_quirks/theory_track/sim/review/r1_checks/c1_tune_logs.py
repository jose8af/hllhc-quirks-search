"""R1 check 1: CP5 applied in every production Pythia job? Parse every PY8_log.txt 'changed settings' table."""
import glob, os, re, collections
AUX = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'sim', 'aux')
KEYS = ['PDF:pSet', 'MultipartonInteractions:pT0Ref', 'MultipartonInteractions:ecmPow', 'MultipartonInteractions:coreRadius',
        'MultipartonInteractions:coreFraction', 'MultipartonInteractions:bProfile', 'ColourReconnection:range',
        'SpaceShower:alphaSvalue', 'SpaceShower:alphaSorder', 'TimeShower:alphaSvalue', 'TimeShower:alphaSorder',
        'MultipartonInteractions:alphaSvalue', 'SigmaProcess:alphaSvalue', 'SpaceShower:rapidityOrder',
        'MultipartonInteractions:ecmRef', 'PartonLevel:MPI', 'JetMatching:qCut', 'JetMatching:nJetMax', 'Random:seed']
res = collections.defaultdict(collections.Counter)
nlog = collections.Counter(); seeds = collections.defaultdict(list); bad = []
for f in sorted(glob.glob(os.path.join(AUX, '*', '*', 'split_*', 'PY8_log.txt'))):
    sid = f.split(os.sep)[-4]
    t = open(f, errors='replace').read()
    blocks = re.split(r'PYTHIA Flag \+ Mode \+ Parm \+ Word.*?Settings \(changes only\)', t)
    if len(blocks) < 2:
        bad.append((f, 'no settings table')); continue
    last = blocks[-1].split('PYTHIA Particle Data Table')[0]
    vals = {}
    for k in KEYS:
        m = re.search(r'\|\s*' + re.escape(k) + r'\s*\|\s*(\S+)', last, re.I)
        vals[k] = m.group(1) if m else 'default'
    nlog[sid] += 1
    sig = tuple((k, vals[k]) for k in KEYS if k != 'Random:seed')
    res[sid][sig] += 1
    seeds[sid].append(vals['Random:seed'])
    if 'PYTHIA Abort' in t or 'Error' in t and 'Error in' in t:
        pass
for sid in sorted(res):
    print(f'== {sid}: {nlog[sid]} logs, {len(res[sid])} distinct settings signature(s); seeds unique: {len(set(seeds[sid]))==len(seeds[sid])}')
    for sig, n in res[sid].items():
        print('   ', n, '×', {k.split(':')[-1]: v for k, v in sig})
print('logs without settings table:', bad)
