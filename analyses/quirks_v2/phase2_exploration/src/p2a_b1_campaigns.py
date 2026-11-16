"""p2a_b1_campaigns.py -- campaign generator of the single-interaction (B1) pilot (Phase 2 channel (iii), executor Albert,
2026-11-16).  Standard library only: runs on einstein.  It writes campaign files, a PLAN and launch scripts; it launches nothing.

  python3 -I p2a_b1_campaigns.py slices [--znn N]                     validation slices p2-c-pa-* (data p2c/pa_validation)
  python3 -I p2a_b1_campaigns.py yields <out.json> <validation.json> [...]   vertices per firing, per parent population
  python3 -I p2a_b1_campaigns.py b1 [--params F.json] [--set a.b=v ...] [--outdir D]   the B1 campaigns + PLAN + scripts
  python3 -I p2a_b1_campaigns.py preflight <PLAN.json>                 read-only checks before a launch
  python3 -I p2a_b1_campaigns.py defaults                              print the default parameter set

DEFAULTS = strategy addendum 1 version 3 (sizes, class list, streams).  Every size, class list, grouping, seed stream,
hand-over mode, beta cut, seam window, number of road orientations, Geant4 job size and optional population is a
parameter: a changed decision is `--set` / `--params` and a regenerated set of campaign files, no code change.

Blocks (parameter `only`, default: every enabled block): `class` (Geant4 'all' and 'ni' passes over the pilot.mb pool
and the seven class samples), `hs` (hard-scatter parents: pool from the Z(nunu) pilot files, Geant4, chain), and the
optional populations `lowpt`, `fwd`, `offroad`, each with its own Geant4 and chain campaigns, so that any of them can be
generated and launched later as a plan of its own (`--set 'only=["fwd"]' --set fwd.enabled=true --set plan_suffix=fwd`).

Sample sizes are exact without knowing the outcome of the Geant4 campaigns (Xavier's layout, p2x_pilot_campaigns.py):
a chain job reads the vertices [first, first + n) of its classes in ONE vertex file; n per file is the expected number
minus a margin (3 x relative error of the measured yield and 5 sigma Poisson); a job fails loudly if its file holds fewer.
"""
import copy
import json
import logging
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import p2x_pilot_campaigns as PG  # noqa: E402  (job builders, layout helpers; standard library only; not modified)

REPO, QV2, SRC, ENV, ACTSPY, DATA, RUNNER = PG.REPO, PG.QV2, PG.SRC, PG.ENV, PG.ACTSPY, PG.DATA, PG.RUNNER
CAMP_DIR = PG.CAMP_DIR
PILOT_DIR = CAMP_DIR / 'pilot'
B1_CLASSES = PG.B1_CLASSES
OUT = QV2 / 'phase2_exploration' / 'outputs'
PART = OUT / 'partition_p2-c-part-0.json'
log = logging.getLogger('p2a_b1_campaigns')

# what the B1 jobs execute or read: hashed into the PLAN, checked by `preflight`, FROZEN from the launch to the last job
JOB_SCRIPTS = ['p2x_g4prod.py', 'p2x_b1.py', 'p2a_hspool.py', 'p2x_common.py', 'p2c_common.py', 'p2c_g4vtx.py', 'p2c_handover.py',
               'p2c_b1.py', 'p2c_campaigns.py', 'p2x_queue.sh', 'g4/g4hv.cc', 'g4/g4hv.sh', 'g4/make_geom_g4.py', 'g4/CMakeLists.txt']
GEN_SCRIPTS = ['p2a_b1_campaigns.py', 'p2x_pilot_campaigns.py', 'p2x_validate.py', 'p2c_validate.py']     # hashed, not frozen
INPUTS = PG.CHAIN + ['../../tools/install/g4/pixi.lock']

MIXED = ('hs', 'lowpt', 'fwd', 'offroad')
DEFAULTS = {
    'name': '',
    'only': [],                                 # [] = every enabled block; or a subset of class, hs, lowpt, fwd, offroad
    'prefix': 'p2-c-pilot',
    'data_prefix': 'pilot',
    'plan_suffix': '',
    'beta_min': 0.1,                            # hand-over P6: the VALIDATED variant (0 would be the variant that failed)
    'n_road_orientations': 21,                  # ADD3 P2 (recorded in every file; nothing is simulated per orientation)
    'seam_ns': 0.005,                           # hybrid parent: the validated seam window (fixed before its validation)
    # parent hand-over per sample: radius = v1's cut (first-arc classes); hybrid = option (a) (Fatras parent to half a
    # turn + Geant4 crossings beyond); autoh = hybrid for the classes difc, nic and radius for the others (mixed samples)
    'trunc': {'default': 'radius', 'difc': 'hybrid', 'nic': 'hybrid', 'hs': 'autoh', 'lowpt': 'autoh', 'fwd': 'autoh',
              'offroad': 'autoh'},
    'yields': str(OUT / 'b1_yields_albert.json'),
    'wait_for_inputs': True,                    # campaigns wait (p2x_queue.sh `after`) for the pilot campaigns they read;
                                                # False: no wait, and preflight requires every input file to be done
    # inputs made by pilot part 1 (read-only)
    'mb': {'campaign_file': str(PILOT_DIR / 'p2-c-pilot-mb.json'), 'first': 0, 'n_files': 40},
    'znn': {'campaign_glob': str(PILOT_DIR / 'p2-c-pilot-znn-??.json'), 'chunk_lo': 0, 'chunk_hi': 460},
    'g4': {'stream': 'pilot.g4', 'all_per_job': 2_000_000, 'ni_per_job': 12_500_000, 'pool_files_per_job': 2,
           'chunk0': {'all': 0, 'ni': 1000, 'hs': 2000, 'lowpt': 3000, 'fwd': 4000, 'offroad': 5000},
           'pool_file_offset': {'all': 0, 'ni': 17, 'lowpt': 5, 'fwd': 11},
           'files_per_part': 16,                # a Geant4 pass is cut into campaigns of this many jobs, and each class sample
                                                # into one chain campaign per part, so that the lanes can share them (0: no cut)
           'margin_sigma': 5.0, 'margin_yield_err': 3.0,
           'extra_firings': 0.03},              # ADD3 P7: the 'all' pass fires 3 % more than the smallest class needs
    # the seven class samples of ADD3 P3-P5: classes, events M, Geant4 pass, stream, events per chain job (upper value)
    'samples': {
        'dif':  {'classes': ['dif', 'k0l'], 'events': 4_000_000, 'pass': 'all', 'stream': 'pilot.c0.dif', 'per_job': 40_000},
        'difc': {'classes': ['difc'], 'events': 4_000_000, 'pass': 'all', 'stream': 'pilot.c0.difc', 'per_job': 40_000},
        'ni22': {'classes': ['ni22'], 'events': 1_000_000, 'pass': 'ni', 'stream': 'pilot.c0.ni22', 'per_job': 40_000},
        'ni30': {'classes': ['ni30'], 'events': 1_000_000, 'pass': 'ni', 'stream': 'pilot.c0.ni30', 'per_job': 40_000},
        'ni61': {'classes': ['ni61'], 'events': 1_000_000, 'pass': 'ni', 'stream': 'pilot.c0.ni61', 'per_job': 40_000},
        'nix':  {'classes': ['nix'], 'events': 4_000_000, 'pass': 'all', 'stream': 'pilot.c0.nix', 'per_job': 40_000},
        'nic':  {'classes': ['nic'], 'events': 2_000_000, 'pass': 'all', 'stream': 'pilot.c0.nic', 'per_job': 40_000},
    },
    # mixed samples: every B1 class in its natural mixture, class recorded per event
    # hs = H1 of ADD3 P2: parents = in-road pool-phase-space hadrons of the Z(nunu) pilot events, drawn ~ w_v1
    'hs': {'enabled': True, 'stream': 'pilot.c0.hs', 'pool_stream': 'pilot.c0.hs.pool', 'events': 2_000_000, 'per_job': 40_000,
           'classes': B1_CLASSES, 'pool_prefix': 'pool', 'draw': 'weighted', 'sel': None, 'source': 'znn',
           'znn_files_per_pool_job': 46, 'pool_files_per_g4_job': 0, 'pool_margin': 0.10},      # 0 = every pool file
    # ADD3 P2 "Lower pT edge": alarm sample of 2e5 vertices in the draft (decision D4 may make it a term: 1.0-2.1e7)
    'lowpt': {'enabled': True, 'stream': 'pilot.c0.lowpt', 'events': 200_000, 'per_job': 40_000, 'classes': B1_CLASSES,
              'pool_prefix': 'xpool', 'draw': 'uniform', 'sel': [0.3, 0.5, 0.0, 1.0], 'source': 'mb', 'pool_margin': 0.10},
    # ADD3 P2 "|eta| > 1": no sample in the draft
    'fwd': {'enabled': False, 'stream': 'pilot.c0.fwd', 'events': 200_000, 'per_job': 40_000, 'classes': B1_CLASSES,
            'pool_prefix': 'xpool', 'draw': 'uniform', 'sel': [0.5, 20.0, 1.0, 1.5], 'source': 'mb', 'pool_margin': 0.10},
    # ADD3 D2 "second stratum": hard-scatter hadrons outside the road (7.3e6 vertices as a term; not in the draft)
    'offroad': {'enabled': False, 'stream': 'pilot.c0.offroad', 'pool_stream': 'pilot.c0.offroad.pool', 'events': 7_300_000,
                'per_job': 40_000, 'classes': B1_CLASSES, 'pool_prefix': 'opool', 'draw': 'weighted', 'sel': None,
                'source': 'znn', 'znn_files_per_pool_job': 23, 'pool_files_per_g4_job': 1, 'pool_margin': 0.10},
    # unit costs for the CPU, wall and storage estimates (measured on the slices p2-c-pa-*; see B1_READY)
    'costs': {'g4_ms': {'all': 0.338, 'ni': 0.054, 'hs': 0.40, 'lowpt': 0.40, 'fwd': 0.40, 'offroad': 0.40},
              'b1_ms': {'default': 4.5}, 'b1_bytes': {'default': 3500.0}, 'vtx_bytes': 800.0, 'job_overhead_s': 12.0,
              'hsp_s_per_file': 3.0, 'hsp_bytes_per_event': {'hs': 30.0, 'offroad': 800.0},
              'rss_mb': {'g4': 1500, 'g4_ni': 600, 'b1': 1500, 'hsp': 1500}},
    'slots': [1, 2, 3],
}


def write_campaign(outdir, name, jobs, hours, rss, regenerate, description, data_prefix, after=()):
    """As PG.write_campaign, with `after` given as absolute campaign-file paths (read by p2x_queue.sh only)."""
    assert len(name) <= 40, f'campaign name {name} longer than 40 characters'
    d = dict(campaign=name, tier='regenerable', data_prefix=data_prefix, regenerate=regenerate, description=description,
             expected_hours=round(hours, 2), defaults=dict(max_rss_mb=rss, timeout_s=1800), after=[str(a) for a in after], jobs=jobs)
    outdir.mkdir(parents=True, exist_ok=True)
    tmp = outdir / f'.{name}.json.tmp'
    tmp.write_text(json.dumps(d, indent=1) + '\n')
    tmp.replace(outdir / f'{name}.json')
    log.info('%s: %d jobs -> %s', name, len(jobs), outdir / f'{name}.json')
    return str(outdir / f'{name}.json')


def job_g4(jid, gpass, n, stream, chunk, pool_prefix, groups, pool_files, sel=None, draw='uniform'):
    opts = ([f'sel={sel[0]}:{sel[1]}:{sel[2]}:{sel[3]}'] if sel else []) + ([f'draw={draw}'] if draw != 'uniform' else [])
    return PG.job_g4(jid, gpass, n, stream, chunk, pool_prefix, groups, list(pool_files) + opts)


def job_b1(jid, sample, classes, n, stream, chunk, first, beta, vfile, trunc, n_orient, seam):
    j = PG.job_b1(jid, sample, classes, n, stream, chunk, first, beta, vfile, trunc, n_orient)
    j['command'] += f' {seam}'
    return j


def job_hsp(jid, stream, chunk, keep_offroad, files):
    return dict(id=jid, outputs=[f'{jid}.npz', f'{jid}.npz.sha.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2a_hspool.py $QV2_OUT_DIR/{jid}.npz {stream} {chunk} {int(keep_offroad)} ' + ' '.join(files))


def job_val(jid, files):
    return dict(id=jid, outputs=[f'{jid}.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2x_validate.py $QV2_OUT_DIR/{jid}.json {PART} ' + ' '.join(files))


def campaign_outputs(cfile, suffix='.npz'):
    d = json.loads(Path(cfile).read_text())
    return [PG.dpath(d['data_prefix'], d['campaign'], o) for jb in d['jobs'] for o in jb['outputs'] if o.endswith(suffix)]


def done_ids(campaign):
    """Job ids of a campaign with a `done` line in their marker (markers only; never a listing of cajuela)."""
    out = set()
    for m in (QV2 / 'ledger' / 'markers' / campaign).glob('*/*.marker'):
        lines = [ln for ln in m.read_text().splitlines() if ln.strip()]
        if lines and json.loads(lines[-1]).get('status') == 'done':
            out.add(m.stem)
    return out


def znn_files(p):
    """[(chunk, job id, file path, campaign file)] of the Z(nunu) pilot jobs in [chunk_lo, chunk_hi), from the campaign files."""
    z = p['znn']; out = []
    g = Path(z['campaign_glob'])
    for cf in sorted(g.parent.glob(g.name)):
        d = json.loads(cf.read_text())
        for jb in d['jobs']:
            chunk = int(jb['id'].rsplit('-', 1)[1])
            if z['chunk_lo'] <= chunk < z['chunk_hi']:
                out.append((chunk, jb['id'], PG.dpath(d['data_prefix'], d['campaign'], f"{jb['id']}.npz"), str(cf)))
    return sorted(out)


def mb_files(p):
    m = p['mb']; d = json.loads(Path(m['campaign_file']).read_text())
    jobs = d['jobs'][m['first']:m['first'] + m['n_files']]
    return [(jb['id'], PG.dpath(d['data_prefix'], d['campaign'], f"{jb['id']}.npz")) for jb in jobs]


# ---- validation slices --------------------------------------------------------------------------------------------------
def slices(n_znn=None, sub='slices_pa', ver=''):
    """Slices of every B1 sample type in its production mode, at full job size.  Campaigns p2-c-pa-*, streams pa.*,
    data prefix p2c/pa_validation.  They READ finished pilot files (pilot.mb pools, Z(nunu) hadron lists) and Xavier's
    slice files; they write only under the validation prefix."""
    out = CAMP_DIR / sub; dp = 'p2c/pa_validation'
    me = f'python3 -I {SRC}/p2a_b1_campaigns.py slices'
    c = {k: f'p2-c-pa-{k}{ver}' for k in ('val0', 'hsp', 'g4', 'b1', 'val1')}
    F = {}
    # 0: validation of Xavier's slices that never went through a validation job
    old = campaign_outputs(CAMP_DIR / 'slices_step1b' / 'p2-c-px-g4.json') + campaign_outputs(CAMP_DIR / 'slices_step1b' / 'p2-c-px-b1.json')
    F['val0'] = write_campaign(out, c['val0'], [job_val(f"{c['val0']}-0", old)], 0.2, 3000, me,
                               'B1 slice: validation job on p2-c-px-g4 and p2-c-px-b1 (Xavier; radius cut)', dp)
    # 1: hard-scatter pools from the Z(nunu) pilot files that are done now
    p = copy.deepcopy(DEFAULTS)
    zf = [f for (ch, jid, f, cf) in znn_files(p) if jid in done_ids(Path(cf).stem)]
    zf = zf[:n_znn] if n_znn else zf
    assert len(zf) >= 4, f'only {len(zf)} finished Z(nunu) pilot files'
    h = c['hsp']
    j = [job_hsp(f'{h}-r0', 'pa.c0.hs.pool', 0, 1, zf[:2]), job_hsp(f'{h}-r1', 'pa.c0.hs.pool', 0, 1, zf[:2]),
         job_hsp(f'{h}-d', 'pa.c0.hs.pool', 1, 1, zf[2:4]), job_hsp(f'{h}-big', 'pa.c0.hs.pool', 2, 1, zf)]
    F['hsp'] = write_campaign(out, h, j, 0.05, 1500, me, f'B1 slice: hard-scatter parent pools from {len(zf)} finished Z(nunu) pilot files', dp)
    hp = lambda t: PG.dpath(dp, h, f'{h}-{t}.npz')  # noqa: E731
    # 2: Geant4 vertices
    mb = [f for (jid, f) in mb_files(p) if jid in done_ids('p2-c-pilot-mb')][:2]
    assert len(mb) == 2
    g_all = {k: s['classes'] for k, s in p['samples'].items()}
    g_ni = {k: s['classes'] for k, s in p['samples'].items() if s['pass'] == 'ni'}
    mix = lambda k: {k: B1_CLASSES}  # noqa: E731
    g = c['g4']; st = 'pa.g4'
    pxmb = PG.dpath('p2c/px_validation', 'p2-c-px-mbb', 'p2-c-px-mbb-big.npz')
    j = [job_g4(f'{g}-reg', 'all', 200000, 'px.g4', 0, 'pool', g_all, [pxmb]),          # = p2-c-px-g4-all-r0: default path unchanged?
         job_g4(f'{g}-all-r0', 'all', 200000, st, 0, 'pool', g_all, mb[:1]),
         job_g4(f'{g}-all-r1', 'all', 200000, st, 0, 'pool', g_all, mb[:1]),
         job_g4(f'{g}-all-d', 'all', 200000, st, 1, 'pool', g_all, mb[:1]),
         job_g4(f'{g}-all-full', 'all', 2000000, st, 2, 'pool', g_all, mb),
         job_g4(f'{g}-ni-full', 'ni', 12500000, st, 101, 'pool', g_ni, mb),
         job_g4(f'{g}-hs-r0', 'all', 200000, st, 200, 'pool', mix('hs'), [hp('big')], draw='weighted'),
         job_g4(f'{g}-hs-r1', 'all', 200000, st, 200, 'pool', mix('hs'), [hp('big')], draw='weighted'),
         job_g4(f'{g}-hs-full', 'all', 2000000, st, 201, 'pool', mix('hs'), [hp('big')], draw='weighted'),
         job_g4(f'{g}-lowpt-r0', 'all', 1000000, st, 300, 'xpool', mix('lowpt'), mb, sel=p['lowpt']['sel']),
         job_g4(f'{g}-fwd-r0', 'all', 1000000, st, 400, 'xpool', mix('fwd'), mb, sel=p['fwd']['sel']),
         job_g4(f'{g}-offroad-r0', 'all', 1000000, st, 500, 'opool', mix('offroad'), [hp('big')], draw='weighted')]
    F['g4'] = write_campaign(out, g, j, 1.5, 2500, me, 'B1 slice: Geant4 vertices from real pilot pools (mb, xpool windows, weighted hard-scatter pools)', dp,
                             after=[F['hsp']])
    # 3: chain events, every sample type in its production mode
    b = c['b1']
    vf = lambda job, grp: PG.dpath(dp, g, f'{g}-{job}.{grp}.npz')  # noqa: E731
    spec = [(k, s['classes'], 'all-full' if s['pass'] == 'all' else 'ni-full', 25000) for k, s in p['samples'].items()]
    spec = [(k, cl, src, 15000 if k == 'ni22' else n) for k, cl, src, n in spec]
    spec += [('hs', B1_CLASSES, 'hs-full', 25000), ('lowpt', B1_CLASSES, 'lowpt-r0', 25000), ('fwd', B1_CLASSES, 'fwd-r0', 25000),
             ('offroad', B1_CLASSES, 'offroad-r0', 25000)]
    j = []
    tr = lambda k: p['trunc'].get(k, p['trunc']['default'])  # noqa: E731
    for k, cl, src, nfull in spec:
        a = (p['beta_min'], vf(src, k), tr(k), p['n_road_orientations'], p['seam_ns'])
        for r, chunk in (('r0', 0), ('r1', 0), ('s', 3)):                       # same seed twice; same vertices, other seed
            j.append(job_b1(f'{b}-{k}-{r}', k, cl, 2000, f'pa.c0.{k}', chunk, 0, *a))
        j.append(job_b1(f'{b}-{k}-full', k, cl, nfull, f'pa.c0.{k}', 2, 2000, *a))
    a = lambda k: (p['beta_min'], vf('all-full', k), tr(k), p['n_road_orientations'], p['seam_ns'])  # noqa: E731
    j.append(job_b1(f'{b}-dif-xl', 'dif', ['dif', 'k0l'], 45000, 'pa.c0.dif', 4, 27000, *a('dif')))        # job-size scan
    j.append(job_b1(f'{b}-difc-xl', 'difc', ['difc'], 38000, 'pa.c0.difc', 4, 27000, *a('difc')))
    j.append(job_b1(f'{b}-nix-xl', 'nix', ['nix'], 38000, 'pa.c0.nix', 4, 27000, *a('nix')))
    # beta-cut scan on the events and seeds of nix-full (a slow fragment above the cut can get hits at unphysical times)
    for tagb, beta in (('b15', 0.15), ('b20', 0.2), ('b30', 0.3)):
        j.append(job_b1(f'{b}-nix-{tagb}', 'nix', ['nix'], 25000, 'pa.c0.nix', 2, 2000, beta, *a('nix')[1:]))
    # regression of the unchanged default path: the arguments of p2-c-px-hy-difc-r0 (hits must be bit-identical: sha_hits)
    j.append(PG.job_b1(f'{b}-reg-difc', 'difc', ['difc'], 2000, 'px.c0.difc', 0, 0, 0.1,
                       PG.dpath('p2c/px_validation', 'p2-c-px-g4', 'p2-c-px-g4-all-big.difc.npz'), 'hybrid', 21))
    F['b1'] = write_campaign(out, b, j, 1.0, 3000, me, 'B1 slice: chain events of every sample type in its production hand-over mode', dp,
                             after=[F['g4']])
    # 4: validation (two jobs: vertex and pool files; chain files)
    v = c['val1']
    j = [job_val(f'{v}-g4', campaign_outputs(F['hsp']) + campaign_outputs(F['g4'])), job_val(f'{v}-b1', campaign_outputs(F['b1']))]
    F['val1'] = write_campaign(out, v, j, 0.3, 3500, me, 'B1 slice: validation of every p2-c-pa slice output', dp, after=[F['g4'], F['b1']])
    log.info('queue order: %s', ' '.join(F[k] for k in ('val0', 'hsp', 'g4', 'b1', 'val1')))
    return F


# ---- yields ---------------------------------------------------------------------------------------------------------------
def kind_of(r, p):
    """Parent population of a validated vertex file record (p2x_validate.chk_g4)."""
    modes = r.get('pool_modes') or []
    sel = r.get('pool_selection')
    if modes == ['mbgen-x'] and r.get('pool_prefix') == 'pool' and not sel:
        return r['g4_pass']
    if modes == ['mbgen-x'] and r.get('pool_prefix') == 'xpool' and sel:
        for k in ('lowpt', 'fwd'):
            if [sel['pt_lo'], sel['pt_hi'], sel['abs_eta_lo'], sel['abs_eta_hi']] == [float(x) for x in p[k]['sel']]:
                return k
    if modes == ['hspool-x'] and r.get('pool_draw') == 'weighted':
        return {'pool': 'hs', 'opool': 'offroad'}.get(r.get('pool_prefix'))
    return None                                   # old-style slice pools (generator-level hard scatter, prefix lowpt): not used


def yields(out, val_jsons):
    p = copy.deepcopy(DEFAULTS)
    part = json.loads(PART.read_text())
    keys = B1_CLASSES + ['conversion', 'other']
    Y = {k: dict(n_fire=0, counts={c: 0 for c in keys}, sources=[], cpu_ms_per_firing=[]) for k in ('all', 'ni') + MIXED}
    Y['all']['n_fire'] += part['n_fire']
    for c in keys:
        Y['all']['counts'][c] += part['counts'].get(c, {}).get('all', 0)
    Y['all']['sources'].append(f'{PART.name} ({part["n_fire"]} firings)')
    seen = set(); bad = []
    for vj in val_jsons:
        val = json.loads(Path(vj).read_text())
        for r in val['files']:
            if r['mode'] != 'g4prod':
                continue
            kind = kind_of(r, p)
            key = (kind, r['stream'], r['chunk'], r['n_fire'])
            if kind is None or key in seen:
                continue
            seen.add(key)
            if not r['hard']:
                bad.append(r['file']); continue
            Y[kind]['n_fire'] += r['n_fire']
            for c in keys:
                Y[kind]['counts'][c] += r['counts'][c]
            Y[kind]['sources'].append(f"{Path(r['file']).name.split('.')[0]} (stream {r['stream']}, chunk {r['chunk']}, {r['n_fire']} firings)")
            Y[kind]['cpu_ms_per_firing'].append(r.get('g4_ms_per_firing'))
    for k in Y:
        nf = Y[k]['n_fire']
        Y[k]['per_firing'] = {c: (n / nf if nf else None) for c, n in Y[k]['counts'].items()}
        Y[k]['b1_vertices_per_firing'] = sum(Y[k]['counts'][c] for c in B1_CLASSES) / nf if nf else None
    Y['ni']['note'] = "only ni22, ni30, ni61 are complete in the 'ni' pass"
    Y['validation_jsons'] = [str(v) for v in val_jsons]
    Y['files_failing_validation_not_used'] = bad
    Path(out).write_text(json.dumps(Y, indent=1) + '\n')
    for k in ('all', 'ni') + MIXED:
        log.info('%s: %d firings, B1 vertices per firing %s, %s', k, Y[k]['n_fire'], Y[k]['b1_vertices_per_firing'], Y[k]['counts'])
    log.info('yields -> %s', out)


# ---- B1 campaigns -----------------------------------------------------------------------------------------------------------
def schedule(camps, nslot, last=()):
    """List scheduling on nslot lanes.  camps: {name: (cpu_h, [deps inside the plan])}.  A campaign starts when its lane is
    free and its dependencies are done; campaigns in `last` (they wait for campaigns outside the plan) go to the end.
    Returns (lanes: list of name lists, lane loads, wall hours)."""
    lanes = [[] for _ in range(nslot)]; free = [0.0] * nslot; end = {}
    for group in ([n for n in camps if n not in last], [n for n in camps if n in last]):
        todo = list(group)
        while todo:
            best = None
            for n in todo:
                cpu, deps = camps[n]
                if any(d in camps and d not in end for d in deps):
                    continue
                ready = max([end[d] for d in deps if d in end] + [0.0])
                for i in range(nslot):
                    start = max(free[i], ready)
                    cand = (start, -cpu, i, n)
                    if best is None or cand < best:
                        best = cand
            assert best is not None, 'dependency cycle'
            start, mcpu, i, n = best
            lanes[i].append(n); free[i] = start - mcpu; end[n] = free[i]; todo.remove(n)
    return lanes, [round(sum(camps[n][0] for n in ln), 1) for ln in lanes], round(max(free), 1)


def b1(p, outdir=None):
    is_test = '-pa-' in p['prefix']             # launch test of the machinery: validation prefix and pa.* streams only
    assert is_test == ('pa_validation' in p['data_prefix']) and (is_test or not p['data_prefix'].startswith('p2c')), \
        'B1 campaigns need the pilot data prefix; test campaigns (-pa-) the validation prefix p2c/pa_validation'
    tag = p['name']; pre = p['prefix'] + (f'-{tag}' if tag else ''); dp = p['data_prefix']
    enabled = ['class'] + [k for k in MIXED if p[k].get('enabled')]
    only = [b for b in (p.get('only') or enabled)]
    assert set(only) <= set(['class'] + list(MIXED)), f'only: {only}'
    for k in only:
        assert k == 'class' or p[k].get('enabled'), f'block {k} is in `only` but not enabled'
    outdir = Path(outdir) if outdir else CAMP_DIR / 'b1'
    me = f'python3 -I {SRC}/p2a_b1_campaigns.py b1 (parameters: the PLAN file of this directory -> params)'
    Y = json.loads(Path(p['yields']).read_text())
    cost = p['costs']; ovh = cost['job_overhead_s']; g4 = p['g4']
    plan = dict(name=tag, params=p, blocks=only, campaigns=[], samples={}, warnings=[], inputs={})
    for s in list(p['samples'].values()) + [p[k] for k in MIXED]:
        assert all(c in B1_CLASSES for c in s['classes']), f"unknown class in {s['classes']}"
    used = sum((s['classes'] for s in p['samples'].values()), [])
    assert len(used) == len(set(used)), 'a class is in two class samples'
    not_read = [c for c in B1_CLASSES if c not in used]
    if not_read and 'class' in only:
        plan['warnings'].append(f'classes in no class sample: {not_read}')
    assert g4['all_per_job'] <= 2_000_000 or p.get('allow_big_g4_jobs'), "ADD3 P7: 'all'-pass Geant4 jobs hold at most 2e6 firings"
    b1ms = lambda k: cost['b1_ms'].get(k, cost['b1_ms']['default'])  # noqa: E731
    b1by = lambda k: cost['b1_bytes'].get(k, cost['b1_bytes']['default'])  # noqa: E731
    trunc = lambda k: p['trunc'].get(k, p['trunc']['default'])  # noqa: E731
    deps = {}

    def add(name, jobs, cpu_s, rss, desc, bytes_, after=(), after_ext=(), events=None, unit='', per_job_s=None, block=''):
        ext = [a for a in after_ext] if p['wait_for_inputs'] else []
        f = write_campaign(outdir, name, jobs, cpu_s / 3600.0, rss, me, desc, dp, [outdir / f'{a}.json' for a in after] + ext)
        plan['campaigns'].append(dict(campaign=name, block=block, file=f, jobs=len(jobs), cpu_h=round(cpu_s / 3600.0, 2),
                                      max_job_min=round(per_job_s / 60.0, 1) if per_job_s else None, rss_request_mb=rss,
                                      storage_gb=round(bytes_ / 1e9, 2), after=list(after), after_external=[str(a) for a in after_ext],
                                      waits_for_external=bool(ext), size=events, unit=unit))
        deps[name] = list(after)
        return name

    def chain(block, key, classes, events, per_job, stream, cg, jl, camp_of_file=None):
        # job id and seed chunk = the running index i of the sample (unique across the parts); vertex file f of Geant4
        # job <cg>-<f>, which lives in the campaign camp_of_file(f)
        cof = camp_of_file or (lambda f: cg)
        assert sum(x[2] for x in jl) == events
        cgs = sorted({cof(f) for f, _, _ in jl})
        for a, cga in enumerate(cgs):
            cc = f'{pre}-c0-{key}' + (f'-{cga[-2:]}' if len(cgs) > 1 or cga != cg else '')
            sub = [(i, x) for i, x in enumerate(jl) if cof(x[0]) == cga]
            jobs = [job_b1(f'{pre}-c0-{key}-{i:04d}', key, classes, n, stream, i, first, p['beta_min'],
                           PG.dpath(dp, cga, f'{cg}-{f:04d}.{key}.npz'), trunc(key), p['n_road_orientations'], p['seam_ns'])
                    for i, (f, first, n) in sub]
            nev = sum(x[2] for _, x in sub); nmax = max(x[2] for _, x in sub)
            add(cc, jobs, nev * b1ms(key) * 1e-3 + len(jobs) * ovh, cost['rss_mb']['b1'],
                f"pilot: no-pile-up events of sample {key} = {'+'.join(classes)}, stream {stream}, hand-over {trunc(key)}",
                nev * b1by(key), after=[cga], events=nev, unit='events', per_job_s=nmax * b1ms(key) * 1e-3 + ovh, block=block)

    # --- inputs
    mbs = mb_files(p); n_mb = len(mbs); mb_cf = p['mb']['campaign_file']
    mbfile = lambda k: mbs[k % n_mb][1]  # noqa: E731
    plan['inputs']['mb'] = dict(campaign_file=mb_cf, files=[f for _, f in mbs], job_ids=[j for j, _ in mbs])

    # --- class samples: Geant4 passes over the pilot.mb pool, then one chain campaign per sample
    if 'class' in only:
        for gpass, per_job in (('all', g4['all_per_job']), ('ni', g4['ni_per_job'])):
            ss = {k: s for k, s in p['samples'].items() if s['pass'] == gpass}
            if not ss:
                continue
            y = Y[gpass]; lay = {}
            for k, s in ss.items():
                if gpass == 'ni':
                    assert all(c in ('ni22', 'ni30', 'ni61') for c in s['classes']), f"sample {k}: classes not complete in the 'ni' pass"
                nm = sum(y['counts'][c] for c in s['classes'])
                exp = nm / y['n_fire'] * per_job
                u = PG.usable(exp, nm, p)
                lay[k] = PG.sample_layout(s['events'], s['per_job'], u) + (exp, u)
            need = max(v[2] for v in lay.values())
            n_files = math.ceil(need * (1.0 + g4.get('extra_firings', 0.0)))
            cg = f'{pre}-g4{gpass[0]}'
            groups = {k: s['classes'] for k, s in ss.items()}
            nppj = g4['pool_files_per_job']; off = g4['pool_file_offset'][gpass]
            fpp = g4.get('files_per_part') or n_files
            n_parts = math.ceil(n_files / fpp)
            cof = (lambda f, cg=cg, fpp=fpp, n_parts=n_parts: f'{cg}-{f // fpp:02d}' if n_parts > 1 else cg)
            nv1 = sum(sum(y['counts'][c] for c in s['classes']) for s in ss.values()) / y['n_fire'] * per_job
            for a in range(n_parts):
                ks = range(a * fpp, min((a + 1) * fpp, n_files))
                jobs = [job_g4(f'{cg}-{k:04d}', gpass, per_job, g4['stream'], g4['chunk0'][gpass] + k, 'pool', groups,
                               [mbfile(off + nppj * k + i) for i in range(nppj)]) for k in ks]
                add(cof(ks[0]), jobs, len(ks) * per_job * cost['g4_ms'][gpass] * 1e-3 + len(ks) * ovh,
                    cost['rss_mb']['g4' if gpass == 'all' else 'g4_ni'],
                    f"pilot: Geant4 vertices of the pilot.mb pool, pass '{gpass}', stream {g4['stream']}, part {a}", nv1 * len(ks) * cost['vtx_bytes'],
                    after_ext=[mb_cf], events=len(ks) * per_job, unit='firings', per_job_s=per_job * cost['g4_ms'][gpass] * 1e-3 + ovh,
                    block='class')
            for k, s in ss.items():
                s_per, n, nf, jl, exp, u = lay[k]
                plan['samples'][k] = dict(classes=s['classes'], events=s['events'], g4_pass=gpass, expected_per_file=round(exp, 1),
                                          usable_per_file=u, jobs_per_file=s_per, events_per_job=n, files_used=nf,
                                          files_needed_by_largest=need, files_made=n_files, stream=s['stream'], handover=trunc(k),
                                          vertices_unused_fraction=round(1 - s['events'] / (exp * n_files), 3))
                chain('class', k, s['classes'], s['events'], s['per_job'], s['stream'], cg, jl, cof)

    # --- mixed samples: hs (H1), lowpt, fwd, offroad
    zall = znn_files(p)
    for key in MIXED:
        if key not in only:
            continue
        m = p[key]; y = Y[key]
        assert y['n_fire'] > 0, f'no measured yield for the population {key}: run its slice and `yields` first'
        nm = sum(y['counts'][c] for c in m['classes'])
        after = []; after_ext = []
        if m['source'] == 'znn':                 # pool builder over the Z(nunu) pilot files
            ch = f"{pre}-hp{key[0]}"
            nf = m['znn_files_per_pool_job']
            sets = [zall[i:i + nf] for i in range(0, len(zall), nf)]
            assert sets, 'no Z(nunu) pilot file in the chunk range'
            jobs = [job_hsp(f'{ch}-{i:03d}', m['pool_stream'], i, key == 'offroad', [x[2] for x in s]) for i, s in enumerate(sets)]
            nev = 5000 * len(zall)
            add(ch, jobs, len(zall) * cost['hsp_s_per_file'] + len(jobs) * ovh, cost['rss_mb']['hsp'],
                f"pilot: hard-scatter parent pool ({key}) from {len(zall)} Z(nunu) pilot files, stream {m['pool_stream']}",
                nev * cost['hsp_bytes_per_event'][key], after_ext=sorted({x[3] for x in zall}), events=len(zall), unit='Z(nunu) files',
                per_job_s=nf * cost['hsp_s_per_file'] + ovh, block=key)
            pools_all = [PG.dpath(dp, ch, f'{ch}-{i:03d}.npz') for i in range(len(sets))]
            after = [ch]
            plan['inputs'][f'znn_{key}'] = dict(files=[x[2] for x in zall], job_ids=[x[1] for x in zall],
                                                campaign_files=sorted({x[3] for x in zall}))
        else:
            pools_all = None; after_ext = [mb_cf]
        per_job = g4['all_per_job']
        n_fire_total = m['events'] / (nm / y['n_fire']) * 1.05
        nj = max(1, math.ceil(n_fire_total / per_job))
        while True:                              # nj jobs of equal size whose files hold `events` usable vertices
            fire = int(math.ceil(n_fire_total / nj / 1000.0) * 1000)
            if fire > per_job:
                nj += 1; continue
            u = int(PG.usable(nm / y['n_fire'] * fire, nm, p) * (1.0 - m.get('pool_margin', 0.10)))
            if u * nj >= m['events']:
                break
            n_fire_total *= 1.02
        cg = f'{pre}-g4{key[0]}'

        def pools_of(i):
            if pools_all is None:
                off = g4['pool_file_offset'][key]; nppj = g4['pool_files_per_job']
                return [mbfile(off + nppj * i + k) for k in range(nppj)]
            npj = m.get('pool_files_per_g4_job', 0)
            return pools_all if not npj else [pools_all[(i * npj + k) % len(pools_all)] for k in range(npj)]
        jobs = [job_g4(f'{cg}-{i:04d}', 'all', fire, g4['stream'], g4['chunk0'][key] + i, m['pool_prefix'], {key: m['classes']},
                       pools_of(i), sel=m.get('sel'), draw=m.get('draw', 'uniform')) for i in range(nj)]
        add(cg, jobs, nj * fire * cost['g4_ms'][key] * 1e-3 + nj * ovh, cost['rss_mb']['g4'],
            f"pilot: Geant4 vertices of the {key} parents (pool {m['pool_prefix']}, draw {m.get('draw', 'uniform')}, window {m.get('sel')}), stream {g4['stream']}",
            nj * fire * nm / y['n_fire'] * cost['vtx_bytes'], after=after, after_ext=after_ext, events=nj * fire, unit='firings',
            per_job_s=fire * cost['g4_ms'][key] * 1e-3 + ovh, block=key)
        s_per, n, nf, jl = PG.sample_layout(m['events'], m['per_job'], u)
        assert nf <= nj
        chain(key, key, m['classes'], m['events'], m['per_job'], m['stream'], cg, jl)
        plan['samples'][key] = dict(classes=m['classes'], events=m['events'], g4_pass='all', firings_per_file=fire, files_made=nj,
                                    usable_per_file=u, jobs_per_file=s_per, events_per_job=n, files_used=nf, stream=m['stream'],
                                    handover=trunc(key), pool_prefix=m['pool_prefix'], draw=m.get('draw', 'uniform'), window=m.get('sel'),
                                    vertices_per_firing=nm / y['n_fire'])

    # --- lanes
    by = {c['campaign']: c for c in plan['campaigns']}
    camps = {n: (by[n]['cpu_h'], deps[n]) for n in by}
    ext_wait = {n for n in by if by[n]['waits_for_external'] and by[n]['block'] in ('hs', 'offroad')}
    last = set(ext_wait)
    grew = True
    while grew:                                   # everything downstream of a campaign that waits for the Z(nunu) pilot goes last
        grew = False
        for n in by:
            if n not in last and any(d in last for d in deps[n]):
                last.add(n); grew = True
    plan['lanes'] = {}
    for nslot in p['slots']:
        lanes, load, wall = schedule(camps, nslot, last)
        plan['lanes'][str(nslot)] = dict(lanes=[[by[n]['file'] for n in ln] for ln in lanes], cpu_h=load, wall_h=wall)
    tot = sum(c['cpu_h'] for c in plan['campaigns'])
    plan['total'] = dict(cpu_h=round(tot, 1), storage_gb=round(sum(c['storage_gb'] for c in plan['campaigns']), 1),
                         jobs=sum(c['jobs'] for c in plan['campaigns']),
                         b1_events=sum(c['size'] for c in plan['campaigns'] if c['unit'] == 'events'),
                         by_block={b: dict(cpu_h=round(sum(c['cpu_h'] for c in plan['campaigns'] if c['block'] == b), 1),
                                           storage_gb=round(sum(c['storage_gb'] for c in plan['campaigns'] if c['block'] == b), 1),
                                           jobs=sum(c['jobs'] for c in plan['campaigns'] if c['block'] == b)) for b in only})
    plan['hashes'] = dict(scripts={s: PG.sha(HERE / s) for s in JOB_SCRIPTS + GEN_SCRIPTS},
                          inputs={i: (PG.sha(QV2 / i) if (QV2 / i).exists() else None) for i in INPUTS},
                          yields=PG.sha(p['yields']))
    plan['frozen_from_launch'] = [f'phase2_exploration/src/{x}' for x in JOB_SCRIPTS] + INPUTS
    plan['campaign_file_sha256'] = {c['campaign']: PG.sha(c['file']) for c in plan['campaigns']}
    stem = pre + '_b1' + ('' if only == enabled else '_' + '-'.join(only)) + (f"_{p['plan_suffix']}" if p.get('plan_suffix') else '')
    pf = outdir / f'PLAN_{stem}.json'
    plan['scripts'] = {}
    q = f'{SRC}/p2x_queue.sh'
    for nslot, v in plan['lanes'].items():
        lines = ['#!/bin/bash',
                 f'# launch of {stem} on {nslot} lane(s): one queue per lane, 1 job each.  Usage: LAUNCH NODE0 [NODE1 [NODE2]]',
                 '# (default schrodinger for every lane; lane i runs on NODEi, or on the last node given).',
                 '# Run on einstein AFTER: preflight ok, a line in phase2_exploration/SLOTS.md, the approval (orchestrator launches).',
                 '# Resume after any stop: run this script again with the same nodes (complete campaigns and done jobs are skipped).',
                 'NODES=("$@"); [ ${#NODES[@]} -eq 0 ] && NODES=(schrodinger)']
        for i, lane in enumerate(v['lanes']):
            if not lane:
                continue
            first = Path(lane[0]).stem
            pid = f'/home/scratch/jdochoa/drivers/{stem}_{nslot}slots_lane{i}.pid'
            logf = f'/home/scratch/jdochoa/drivers/{stem}_{nslot}slots_lane{i}.log'
            inner = f'echo \\$\\$ > {pid}; exec {q} $NODE 1 ' + ' '.join(lane)
            lines.append(f'NODE=${{NODES[{i}]:-${{NODES[-1]}}}}')
            lines.append('echo "lane ' + str(i) + ' on $NODE; qv2run jobs there now: $(ssh -x -o BatchMode=yes $NODE "pgrep -u jdochoa -af \'[q]v2run job\' | wc -l")"')
            lines.append(f'ssh -x -o BatchMode=yes $NODE "mkdir -p /home/scratch/jdochoa/drivers; rm -f /home/scratch/jdochoa/drivers/STOP.{first}; '
                         f'if [ -e {pid} ] && kill -0 \\$(cat {pid}) 2>/dev/null; then echo lane {i} already runs; else '
                         f"setsid nohup bash -c '{inner}' > {logf} 2>&1 < /dev/null & echo lane {i} started; fi\"")
        lf = outdir / f'LAUNCH_{stem}_{nslot}slots.sh'
        lf.write_text('\n'.join(lines) + '\n')
        plan['scripts'][f'launch_{nslot}slots'] = str(lf)
    st = ['#!/bin/bash', f'# status of {stem} from the markers.  Usage: STATUS [NODE ...] (the nodes given to LAUNCH; default schrodinger)',
          'NODES=("$@"); [ ${#NODES[@]} -eq 0 ] && NODES=(schrodinger)',
          'ssh -x -o BatchMode=yes ${NODES[0]} \'for f in ' + ' '.join(c['file'] for c in plan['campaigns']) +
          f'; do {RUNNER}/bin/qv2run status $f --json; done\'',
          'for N in $(printf "%s\\n" "${NODES[@]}" | sort -u); do echo "== $N"; ssh -x -o BatchMode=yes $N \'tail -n 2 /home/scratch/jdochoa/drivers/' + stem +
          '_*lane*.log 2>/dev/null; pgrep -u jdochoa -af "[q]v2run job" | wc -l\'; done']
    sf = outdir / f'STATUS_{stem}.sh'
    sf.write_text('\n'.join(st) + '\n')
    plan['scripts']['status'] = str(sf)
    plan['scripts']['stop'] = ('touch /home/scratch/jdochoa/drivers/STOP.<first campaign of the lane> on its node: the lane ends after its '
                               'running campaign; running jobs are never killed by it')
    pf.write_text(json.dumps(plan, indent=1) + '\n')
    log.info('plan: %s', pf)
    log.info('total: %s', plan['total'])
    for k, v in plan['lanes'].items():
        log.info('%s lanes: CPU-h per lane %s, wall %.1f h', k, v['cpu_h'], v['wall_h'])
    for c in plan['campaigns']:
        log.info('  %-22s %4d jobs %7.2f CPU-h %6.2f GB  max job %s min  %s %s', c['campaign'], c['jobs'], c['cpu_h'], c['storage_gb'],
                 c['max_job_min'], c['size'], c['unit'])
    for w in plan['warnings']:
        log.warning('%s', w)
    return plan


# ---- pre-flight ---------------------------------------------------------------------------------------------------------
def preflight(plan_file):
    """Read-only checks on einstein before a launch.  Returns the number of failed checks."""
    plan = json.loads(Path(plan_file).read_text())
    pp = plan['params']; bad = 0

    def check(ok, msg):
        nonlocal bad
        bad += 0 if ok else 1
        log.info('%s  %s', 'ok  ' if ok else 'FAIL', msg)
    st = os.statvfs('/nfs/cajuela/jdochoa/quirks_v2')
    free = st.f_bavail * st.f_frsize / 1e9; need = plan['total']['storage_gb']
    check(free > 3 * need, f'cajuela free {free:.0f} GB, the plan needs about {need:.0f} GB (required: 3x)')
    markers = QV2 / 'ledger' / 'markers'
    check(markers.is_dir() and os.access(markers, os.W_OK), f'markers directory writable: {markers}')
    dp = pp['data_prefix']; names = [c['campaign'] for c in plan['campaigns']]
    clash = [n for n in names if any(x.exists() for x in (markers / n, Path(DATA) / dp / n, Path(DATA) / n))]
    check(not clash, f'{len(names)} campaigns: no markers or data of those names yet' + (f' (found {clash})' if clash else ''))
    changed = [c['campaign'] for c in plan['campaigns'] if not Path(c['file']).exists() or PG.sha(c['file']) != plan['campaign_file_sha256'][c['campaign']]]
    check(not changed, f'campaign files unchanged since the plan' + (f' (changed: {changed})' if changed else ''))
    mine = {Path(c['file']).resolve() for c in plan['campaigns']}
    others = {q.stem for d in (REPO / 'tools' / 'runner' / 'campaigns', REPO / 'tools' / 'campaigns') if d.is_dir() for q in d.glob('*.json')} | \
             {q.stem for q in (REPO / 'tools' / 'runner' / 'examples').glob('*/*.json') if q.resolve() not in mine and not q.name.startswith('PLAN_')} | \
             {q.stem for q in (REPO / 'tools' / 'runner' / 'examples').glob('*/*/*.json') if q.resolve() not in mine and not q.name.startswith('PLAN_')}
    check(not (set(names) & others) and len(names) == len(set(names)), f'no campaign name clash with any other campaign file ({sorted(set(names) & others)})')
    ids = []; cmds = {}
    for c in plan['campaigns']:
        d = json.loads(Path(c['file']).read_text())
        ids += [j['id'] for j in d['jobs']]
        cmds[c['campaign']] = d
    check(len(ids) == len(set(ids)), f'{len(ids)} job ids, all distinct')
    have = {m.stem for m in markers.glob(f"{pp['prefix']}*/*/*.marker")}
    check(not (set(ids) & have), f'no job id of this plan has a marker yet ({len(set(ids) & have)} found)')
    for s, h in plan['hashes']['scripts'].items():
        check((HERE / s).exists() and PG.sha(HERE / s) == h, f'script unchanged since the plan: {s} {h[:12]}')
    for i, h in plan['hashes']['inputs'].items():
        check(h is not None and (QV2 / i).exists() and PG.sha(QV2 / i) == h, f'input unchanged since the plan: {i} {(h or "missing")[:12]}')
    check(Path(pp['yields']).exists() and PG.sha(pp['yields']) == plan['hashes']['yields'], f"yields file unchanged since the plan: {pp['yields']}")
    # every file a job reads is either an output of a job of this plan or a pilot input listed in the plan
    produced = {PG.dpath(dp, c, o) for c, d in cmds.items() for j in d['jobs'] for o in j['outputs']}
    inputs = {f for v in plan['inputs'].values() for f in v['files']}
    read = set()
    for d in cmds.values():
        for j in d['jobs']:
            read |= {w for w in j['command'].split() if w.startswith(DATA + '/')}
    stray = sorted(read - produced - inputs)
    check(not stray, f'{len(read)} input paths of the jobs: all are outputs of this plan or listed pilot inputs ({stray[:3]})')
    check(not any('px_validation' in w or 'pa_validation' in w for w in read) or '-pa-' in pp['prefix'], 'no job of a production plan reads a validation slice')
    # pilot inputs: done markers
    for key, v in plan['inputs'].items():
        camps_in = {j.rsplit('-', 1)[0] for j in v['job_ids']}
        done = set()
        for cf in ([v['campaign_file']] if 'campaign_file' in v else v['campaign_files']):
            done |= done_ids(Path(cf).stem)
        miss = [j for j in v['job_ids'] if j not in done]
        msg = f'pilot input {key}: {len(v["job_ids"]) - len(miss)} of {len(v["job_ids"])} files have a done marker'
        if pp['wait_for_inputs']:
            log.info('info  %s%s', msg, ' (the lanes wait for the rest: `after`)' if miss else '')
        else:
            check(not miss, msg + ' (wait_for_inputs = false: all are required)')
    streams = []
    if 'class' in plan['blocks']:
        streams += [s['stream'] for s in pp['samples'].values()]
    streams += [pp[k]['stream'] for k in MIXED if k in plan['blocks']] + [pp[k]['pool_stream'] for k in ('hs', 'offroad') if k in plan['blocks']]
    is_test = '-pa-' in pp['prefix']
    check(len(streams) == len(set(streams)) and pp['g4']['stream'] not in streams and all(s.startswith('pa.') == is_test for s in streams + [pp['g4']['stream']]),
          f"seed streams distinct; validation streams (pa.*) only in a test: {streams + [pp['g4']['stream']]}")
    ch = pp['g4']['chunk0']; nj = {}
    for c in plan['campaigns']:
        w = c['campaign'][len(pp['prefix']) + (len(pp['name']) + 1 if pp['name'] else 0) + 1:]
        if w.startswith('g4'):
            nj[w[2]] = nj.get(w[2], 0) + c['jobs']
    rng = sorted((ch[k], ch[k] + nj.get(k[0], 0)) for k in ch)
    check(all(a[1] <= b[0] for a, b in zip(rng, rng[1:])), f'Geant4 chunk ranges of stream {pp["g4"]["stream"]} do not overlap: {rng}')
    big = [c['campaign'] for c in plan['campaigns'] if (c['max_job_min'] or 0) > 30]
    check(not big, f'every job is estimated at 30 minutes or less ({big})')
    check(pp['beta_min'] == 0.1 and pp['seam_ns'] == 0.005 or bool(pp.get('unvalidated_ok')),
          f"beta cut {pp['beta_min']} and seam window {pp['seam_ns']} ns are the validated values (or unvalidated_ok is set)")
    log.info('%d failed checks. Manual: node counts (pgrep), Geant4 env on the node (/home/scratch/jdochoa/envs/g4), SLOTS.md line, approval.', bad)
    return bad


def main(argv):
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    what = argv[0]
    if what == 'slices':
        slices(int(argv[argv.index('--znn') + 1]) if '--znn' in argv else None,
               argv[argv.index('--sub') + 1] if '--sub' in argv else 'slices_pa', argv[argv.index('--ver') + 1] if '--ver' in argv else '')
    elif what == 'defaults':
        sys.stdout.write(json.dumps(DEFAULTS, indent=1) + '\n')
    elif what == 'yields':
        yields(argv[1], argv[2:])
    elif what == 'b1':
        p = copy.deepcopy(DEFAULTS); a = argv[1:]; outdir = None
        while a:
            k = a.pop(0)
            if k == '--params':
                PG.deep_update(p, json.loads(Path(a.pop(0)).read_text()))
            elif k == '--set':
                PG.set_path(p, a.pop(0))
            elif k == '--outdir':
                outdir = a.pop(0)
            else:
                raise SystemExit(f'unknown argument {k}')
        b1(p, outdir)
    elif what == 'preflight':
        raise SystemExit(1 if preflight(argv[1]) else 0)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
