"""R2 c6: file inventory vs SAMPLES.md (md5, N rows/kept, sigma_matched, N_LHE), index aliases, sigma regression vs R1 values,
sigma_norm scalars vs xsec.json, and npz metadata presence."""
import glob, hashlib, json, os, re
import numpy as np
TT = '/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track'
D = f'{TT}/data/sim'
S = open(f'{TT}/sim/SAMPLES.md').read()
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
rows = {}
for l in S.splitlines():
    m = re.search(r'`([A-Za-z0-9\-]+_m\d+\.npz)` \(([0-9a-f]{8})\)', l)
    if m:
        cells = [c.strip() for c in l.strip('|').split('|')]
        rows[m.group(1)] = (m.group(2), cells)
for m in re.finditer(r'\| `([A-Za-z0-9\-]+_m\d+\.npz)` \| (\d+) \| (\d+) \| ([0-9.]+) \| ([0-9a-f]{8}) \|', S):
    rows[m.group(1)] = (m.group(5), ['vshower', m.group(2), m.group(3), m.group(4)])
trgs = {m.group(1): m.groups() for m in re.finditer(r'\| `([ES]-TRGS_m\d+\.npz)` \| (\d+) \| (\d+) \|', S)}
disk = sorted(os.path.basename(p) for p in glob.glob(f'{D}/npz/*.npz'))
print('on disk:', len(disk), ' in SAMPLES main/vshower tables:', len(rows), ' TRGS table:', len(trgs))
print('on disk, not in SAMPLES:', [f for f in disk if f not in rows and f not in trgs])
print('in SAMPLES, not on disk:', [f for f in list(rows) + list(trgs) if f not in disk])
bad = []
for f, (h, cells) in rows.items():
    p = f'{D}/npz/{f}'
    if not os.path.exists(p):
        continue
    c = np.load(p)
    hh = md5(p)
    if hh != h:
        bad.append((f, 'md5', h, hh))
    sw = float(c['w'].sum())
    if cells[0] == 'vshower':
        if int(cells[2]) != len(c['w']) or abs(float(cells[3]) / sw - 1) > 1e-3:
            bad.append((f, 'vshower', cells[1:], len(c['w']), sw))
        continue
    nlhe, kept, sm = int(cells[7]), int(cells[8]), float(cells[14])
    if nlhe != int(c['nlhe']) or kept != len(c['w']) or abs(sm / sw - 1) > 1.5e-3:
        bad.append((f, 'cells', nlhe, int(c['nlhe']), kept, len(c['w']), sm, sw))
    for k in ('sigma_norm_fb', 'sigma_ref_fb', 'chunk', 'ievt_lhe', 'tt_split'):
        if k not in c.files:
            bad.append((f, 'missing', k))
for f, g in trgs.items():
    c = np.load(f'{D}/npz/{f}')
    if int(g[1]) != len(c['w']) or int(g[2]) != int((c['origin'] == 1).sum()):
        bad.append((f, 'trgs', g, len(c['w']), int((c['origin'] == 1).sum())))
    for k in ('sigma_norm_fb', 'sigma_ref_fb', 'shuffle_seed', 'row_src', 'kind', 'tt_split'):
        if k not in c.files:
            bad.append((f, 'missing', k))
print('mismatches:', bad if bad else 'none')
# R1 sigma regression (values R1 recomputed): unchanged samples must be unchanged
ref = {'E-INC_m500': 2.5070, 'E-TRG_m500': 0.51413, 'E-LOPS_m500': 2.4536, 'S-INC_m500': 0.18864, 'E-INC_m1500': 0.0051986, 'E-TRG_m1500': 0.0014678,
       'V-TUNE-INC_m500': 2.2597, 'V-TUNE-TRG_m500': 0.4588, 'V-MPI_m500': 0.5152}
for k, v in ref.items():
    sw = float(np.load(f'{D}/npz/{k}.npz')['w'].sum()); print(f'  {k}: sigma {sw:.5g} vs R1 {v:.5g} ({100*(sw/v-1):+.3f} %)')
# topped-up points: per-chunk sigma consistency
for k in ('E-INC_m200', 'E-TRG_m200', 'E-INC_m300', 'E-TRG_m300'):
    c = np.load(f'{D}/npz/{k}.npz'); ch = c['chunk']
    per = []
    for q in np.unique(ch):
        n_q = json.load(open(f'{D}/npz/chunks/{k.split("_m")[0]}/m{k.split("_m")[1]}_c{q}.done.json'))['n_lhe']
        per.append((int(q), n_q, float(c['w'][ch == q].sum() * float(c['nlhe']) / n_q)))
    print(f'  {k}: total {float(c["w"].sum()):.5g}; per-chunk sigma estimates', [(q, n, round(s, 4)) for q, n, s in per])
# index
idx = json.load(open(f'{D}/SAMPLES_INDEX.json'))
missing = [k for k, v in idx.items() if not k.startswith('_') and isinstance(v, str) and not os.path.exists(os.path.join(D, v))]
print('index entries:', sum(1 for k in idx if not k.startswith('_')), ' dangling:', missing)
print('trig aliases ->', sorted({v for k, v in idx.items() if k.endswith('_trig')}))
# sigma_norm scalars vs xsec.json
X = json.load(open(f'{TT}/sim/results/xsec.json'))
for m in (200, 500, 1000, 1500):
    c = np.load(f'{D}/npz/E-TRGS_m{m}.npz')
    print(f'  E{m}: npz sigma_norm {float(c["sigma_norm_fb"]):.5g}, xsec.json {X["normalisation_E"]["rows"][str(m)]["sigma_norm_nic2_fb"]:.5g}; sigma_ref {float(c["sigma_ref_fb"]):.5g} = INC sum w {float(np.load(f"{D}/npz/E-INC_m{m}.npz")["w"].sum()):.5g}')
print('  xsec.json normalisation_E row keys:', list(X['normalisation_E']['rows']['500'].keys()))
