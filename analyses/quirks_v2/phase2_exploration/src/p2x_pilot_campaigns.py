"""p2x_pilot_campaigns.py -- campaign generator of the pilot (Phase 2 channel (iii), executor Xavier, 2026-11-16).

  python3 -I p2x_pilot_campaigns.py slices [--ver g4=b,b1=b]                  validation slices  p2-c-px-<step><tag>
  python3 -I p2x_pilot_campaigns.py pilot  [--params F.json] [--set a.b=v ...] [--outdir D] [--name NAME]
  python3 -I p2x_pilot_campaigns.py preflight <PLAN.json>                    checks before a launch (read-only)
  python3 -I p2x_pilot_campaigns.py yields <validation.json> [out.json]         measured yields per firing for `pilot`
  python3 -I p2x_pilot_campaigns.py defaults                                 print the default parameter set

Light (standard library only): runs on einstein.  It writes campaign JSON files for tools/runner and a PLAN file;
it launches nothing.  Every size, class list, stream name and seed chunk of the pilot is a PARAMETER (DEFAULTS below
= strategy addendum 1 version 2, which is under review): a changed decision means `--set`/`--params` and a new set
of campaign files, no code change.

How sample sizes are made exact without knowing the outcome of the Geant4 campaigns: a chain job reads the vertices
[first, first + n) of its classes in ONE vertex file; n per file is the expected number of vertices of the sample in a
file (yield per firing x firings per file) minus a safety margin (3 x relative error of the measured yield and
5 sigma Poisson); a job fails loudly if its file holds fewer.  The number of Geant4 firings is derived from the
requested events.  Yields: outputs/pilot_yields_xavier.json (measured on p2-c-part-0 and on the p2-c-px slices).
"""
import copy
import hashlib
import json
import logging
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import p2c_campaigns as PC  # noqa: E402  (ENV and interpreter paths of Tatiana's campaigns; standard library only)

REPO = HERE.parents[3]
QV2 = REPO / 'analyses' / 'quirks_v2'
SRC = str(HERE)
ENV, ACTSPY = PC.ENV, PC.ACTSPY
CAMP_DIR = REPO / 'tools' / 'runner' / 'examples' / 'p2x'
DATA = '/nfs/cajuela/jdochoa/quirks_v2/data'
RUNNER = str(REPO / 'tools' / 'runner')
log = logging.getLogger('p2x_pilot_campaigns')
B1_CLASSES = ['dif', 'difc', 'k0l', 'ni22', 'ni30', 'ni61', 'nix', 'nic']
SCRIPTS = ['p2x_common.py', 'p2x_mbgen.py', 'p2x_hspool.py', 'p2x_g4prod.py', 'p2x_b1.py', 'p2x_hs0.py', 'p2x_validate.py',
           'p2x_pilot_campaigns.py', 'p2x_queue.sh', 'p2c_common.py', 'p2c_mbgen.py', 'p2c_g4vtx.py', 'p2c_handover.py',
           'p2c_b1.py', 'p2c_hs0.py', 'p2c_validate.py', 'p2c_campaigns.py', 'g4/g4hv.cc', 'g4/g4hv.sh', 'g4/make_geom_g4.py',
           'g4/CMakeLists.txt']
INPUTS = ['acts/stage4/code/run_chain.py', 'acts/stage4/code/s4pu.py', 'acts/stage4/code/s4geo.py', 'acts/stage4/code/s4cp.py',
          'acts/stage4/analysis/gen_d123.py', 'acts/geometry/cms_phase2_public.json', 'sim/stage3/code/surfaces_s3.json',
          'acts/scripts/pythia8_tune_CP5.dat', 'acts/pixi.lock', '../../tools/install/g4/pixi.lock',
          'phase2_exploration/outputs/pilot_yields_xavier.json']

# what each block of campaigns executes or reads: hashed into the PLAN, checked by `preflight`, and FROZEN (not to be
# edited) from the launch of that block until its last job is done -- jobs record the same hashes in their meta
CHAIN = ['acts/stage4/code/run_chain.py', 'acts/stage4/code/s4pu.py', 'acts/stage4/code/s4geo.py', 'acts/stage4/code/s4cp.py',
         'acts/geometry/cms_phase2_public.json', 'sim/stage3/code/surfaces_s3.json', 'acts/scripts/pythia8_tune_CP5.dat',
         'acts/pixi.lock']
BLOCK_FILES = {
    'mb': (['p2x_mbgen.py', 'p2x_common.py', 'p2c_mbgen.py', 'p2c_common.py', 'p2c_campaigns.py', 'p2x_queue.sh'],
           ['acts/stage4/code/s4pu.py', 'acts/scripts/pythia8_tune_CP5.dat', 'acts/pixi.lock']),
    'znn': (['p2x_hs0.py', 'p2x_common.py', 'p2c_hs0.py', 'p2c_common.py', 'p2c_campaigns.py', 'p2x_queue.sh'],
            CHAIN + ['acts/stage4/analysis/gen_d123.py']),
    'b1': (SCRIPTS, INPUTS),
}

# ---------------------------------------------------------------------------------------------------------------------
# Default parameter set = strategy addendum 1 version 2 (DRAFT under review).  Change with --params / --set.
DEFAULTS = {
    'name': '',                                # optional tag: campaign names are <prefix>[-<name>]-...
    'only': [],                                # [] = everything; or a subset of mb, b1 (Geant4 + chain + mixed samples), znn
    'prefix': 'p2-c-pilot',
    'data_prefix': 'pilot',                    # data/pilot/<campaign>/000/ ; never the validation prefix
    'beta_min': 0.1,                           # hand-over P6: the VALIDATED variant (0 would be the variant that failed)
    'n_road_orientations': 21,                 # review B-1 (recorded in every B1 file; Phase 3 tests them)
    'trunc': {'default': 'radius', 'difc': 'time', 'nic': 'time', 'hs': 'auto', 'lowpt': 'auto'},   # review A-1
    'yields': str(QV2 / 'phase2_exploration' / 'outputs' / 'pilot_yields_xavier.json'),
    # chunk0 / part0: to APPEND later, generate again with only=[mb] or [znn], chunk0 = first unused chunk, part0 = first
    # unused part, and the number of additional interactions / events: new job ids, new seeds, old files untouched
    'mb': {'stream': 'pilot.mb', 'interactions': 10_000_000, 'per_job': 250_000, 'chunk0': 0, 'part0': 0,
           'xpool_jobs': 40},                  # jobs (from chunk 0) that store the wider pool (0.3 < pT, |eta| < 1.5)
    'g4': {'stream': 'pilot.g4', 'all_per_job': 2_000_000, 'ni_per_job': 12_500_000, 'pool_files_per_job': 2,
           'chunk0': {'all': 0, 'ni': 1000, 'hs': 2000, 'lowpt': 3000},
           'margin_sigma': 5.0, 'margin_yield_err': 3.0,
           'extra_firings': 0.03},             # review C-7: 3 % more firings than the margins alone ask for
    # one entry per pilot sample: classes (of p2x_common.B1_CLASSES), events M, Geant4 pass, stream, events per job
    'samples': {
        'dif':  {'classes': ['dif', 'k0l'], 'events': 4_000_000, 'pass': 'all', 'stream': 'pilot.c0.dif', 'per_job': 25_000},
        'difc': {'classes': ['difc'], 'events': 4_000_000, 'pass': 'all', 'stream': 'pilot.c0.difc', 'per_job': 25_000},
        'ni22': {'classes': ['ni22'], 'events': 1_000_000, 'pass': 'ni', 'stream': 'pilot.c0.ni22', 'per_job': 25_000},
        'ni30': {'classes': ['ni30'], 'events': 1_000_000, 'pass': 'ni', 'stream': 'pilot.c0.ni30', 'per_job': 25_000},
        'ni61': {'classes': ['ni61'], 'events': 1_000_000, 'pass': 'ni', 'stream': 'pilot.c0.ni61', 'per_job': 25_000},
        'nix':  {'classes': ['nix'], 'events': 4_000_000, 'pass': 'all', 'stream': 'pilot.c0.nix', 'per_job': 25_000},
        'nic':  {'classes': ['nic'], 'events': 2_000_000, 'pass': 'all', 'stream': 'pilot.c0.nic', 'per_job': 25_000},
    },
    # mixed samples (every B1 class in its natural mixture, class recorded per event)
    'hs': {'enabled': True, 'stream': 'pilot.c0.hs', 'gen_stream': 'pilot.c0.hs.gen', 'gen_sample': 'Znunu_j',
           'gen_events': 20_000, 'gen_per_job': 10_000, 'events': 200_000, 'per_job': 25_000, 'classes': B1_CLASSES,
           'pool_margin': 0.10},
    'lowpt': {'enabled': True, 'stream': 'pilot.c0.lowpt', 'events': 200_000, 'per_job': 25_000, 'classes': B1_CLASSES,
              'pool_margin': 0.10},
    'znn': {'stream': 'pilot.hs0.znn', 'sample': 'Znunu_j', 'events': 2_300_000, 'per_job': 5_000, 'chunk0': 0, 'part0': 0,
            'parts': 16},
    # unit costs for the CPU, wall and storage estimates only (measured values, filled from the slices; see PILOT_READY)
    # measured on the slices p2-c-px-mbb and p2-c-px-znnb (markers and logs; see PILOT_READY): mb 3.56 ms and 215 B per
    # interaction with the wider pool (83 B without), max RSS 329 MB at 1.25e5; Z(nunu) 130.7 ms per event in the event loop
    # + 12 s per job, 33.56 kB per event, max RSS 1,252 MB at 5,000 events.  B1 values: Tatiana's slices until mine are done.
    'costs': {'mb_ms': 3.56, 'g4_all_ms': 0.305, 'g4_ni_ms': 0.047, 'b1_ms': 5.0, 'znn_ms': 130.7, 'hsgen_ms': 38.0,
              'job_overhead_s': 12.0, 'mb_bytes_per_int': 215.0, 'vtx_bytes': 800.0, 'b1_bytes': 3500.0, 'znn_bytes': 33561.0,
              'rss_mb': {'mb': 700, 'g4': 2500, 'b1': 2000, 'znn': 1500, 'hsgen': 300}},
    'slots': [2, 3],
}


def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, dict) and isinstance(d.get(k), dict):
            deep_update(d[k], v)
        else:
            d[k] = v
    return d


def set_path(d, spec):
    key, val = spec.split('=', 1)
    try:
        val = json.loads(val)
    except json.JSONDecodeError:
        pass
    ks = key.split('.')
    for k in ks[:-1]:
        d = d.setdefault(k, {})
    d[ks[-1]] = val


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_campaign(outdir, name, jobs, hours, rss, regenerate, description, data_prefix, after=()):
    assert len(name) <= 40, f'campaign name {name} longer than 40 characters'
    d = dict(campaign=name, tier='regenerable', data_prefix=data_prefix, regenerate=regenerate, description=description,
             expected_hours=round(hours, 2), defaults=dict(max_rss_mb=rss, timeout_s=1800),
             after=[str(outdir / f'{a}.json') for a in after],          # read by p2x_queue.sh only (the runner ignores it)
             jobs=jobs)
    outdir.mkdir(parents=True, exist_ok=True)
    tmp = outdir / f'.{name}.json.tmp'
    tmp.write_text(json.dumps(d, indent=1) + '\n')
    tmp.replace(outdir / f'{name}.json')
    log.info('%s: %d jobs -> %s', name, len(jobs), outdir / f'{name}.json')
    return str(outdir / f'{name}.json')


# ---- job builders ---------------------------------------------------------------------------------------------------
def dpath(data_prefix, camp, fname):
    return f'{DATA}/{data_prefix}/{camp}/000/{fname}'


def job_mb(jid, n, stream, chunk, keep):
    return dict(id=jid, outputs=[f'{jid}.npz', f'{jid}.npz.sha.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2x_mbgen.py $QV2_OUT_DIR/{jid}.npz {n} {stream} {chunk} {int(keep)}')


def job_hsg(jid, sample, n, stream, chunk):
    return dict(id=jid, outputs=[f'{jid}.npz', f'{jid}.npz.sha.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2x_hspool.py $QV2_OUT_DIR/{jid}.npz {sample} {n} {stream} {chunk}')


def groups_spec(groups):
    return ','.join(f'{g}=' + '+'.join(cl) for g, cl in groups.items())


def job_g4(jid, gpass, n, stream, chunk, pool_prefix, groups, pool_files):
    return dict(id=jid, outputs=[f'{jid}.{g}.npz' for g in groups] + [f'{jid}.sha.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2x_g4prod.py $QV2_OUT_DIR/{jid} {gpass} {n} {stream} {chunk} {pool_prefix} '
                              f'{groups_spec(groups)} ' + ' '.join(pool_files))


def job_b1(jid, sample, classes, n, stream, chunk, first, beta, vfile, trunc='radius', n_orient=21):
    return dict(id=jid, outputs=[f'{jid}.npz', f'{jid}.npz.sha.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2x_b1.py {sample} {"+".join(classes)} $QV2_OUT_DIR/{jid}.npz {n} {stream} '
                              f'{chunk} {first} {beta} {vfile} {trunc} {n_orient}')


def job_znn(jid, sample, n, stream, chunk):
    return dict(id=jid, outputs=[f'{jid}.npz', f'{jid}.npz.sha.json'],
                command=ENV + f'{ACTSPY} {SRC}/p2x_hs0.py {sample} $QV2_OUT_DIR/{jid}.npz {n} {stream} {chunk}')


# ---- validation slices ----------------------------------------------------------------------------------------------
def slices(ver='', val_keys=('mb', 'hsg', 'znn', 'g4', 'b1'), sub='slices'):
    """Small end-to-end slices of every sample type.  Streams px.*, data prefix p2c/px_validation: NOT pilot data."""
    out = CAMP_DIR / sub
    dp = 'p2c/px_validation'
    me = f'python3 -I {SRC}/p2x_pilot_campaigns.py slices' + (f' --ver {ver}' if ver else '')
    vmap = dict(x.split('=') for x in ver.split(',')) if ver else {}          # e.g. g4=b,b1=b -> p2-c-px-g4b, p2-c-px-b1b
    c = {k: f'p2-c-px-{k}{vmap.get(k, "")}' for k in ('mb', 'hsg', 'znn', 'g4', 'b1', 'val')}
    files = {}
    # 1 minimum bias: same seed twice, another chunk, and one job at half the pilot job size
    j = [job_mb(f'{c["mb"]}-r0', 20000, 'px.mb', 0, 1), job_mb(f'{c["mb"]}-r1', 20000, 'px.mb', 0, 1),
         job_mb(f'{c["mb"]}-d', 20000, 'px.mb', 1, 1), job_mb(f'{c["mb"]}-big', 125000, 'px.mb', 2, 1),
         job_mb(f'{c["mb"]}-nox', 20000, 'px.mb', 3, 0)]
    files['mb'] = write_campaign(out, c['mb'], j, 0.3, 1500, me, 'pilot code slice: minimum bias with main and low-pT pools', dp)
    # 2 hard-scatter parent pool
    j = [job_hsg(f'{c["hsg"]}-r0', 'Znunu_j', 2000, 'px.c0.hs.gen', 0), job_hsg(f'{c["hsg"]}-r1', 'Znunu_j', 2000, 'px.c0.hs.gen', 0),
         job_hsg(f'{c["hsg"]}-d', 'Znunu_j', 2000, 'px.c0.hs.gen', 1)]
    files['hsg'] = write_campaign(out, c['hsg'], j, 0.1, 1000, me, 'pilot code slice: hard-scatter parent pool (generator level)', dp)
    # 3 Z(nunu) no-pile-up events
    j = [job_znn(f'{c["znn"]}-r0', 'Znunu_j', 500, 'px.hs0.znn', 0), job_znn(f'{c["znn"]}-r1', 'Znunu_j', 500, 'px.hs0.znn', 0),
         job_znn(f'{c["znn"]}-d', 'Znunu_j', 500, 'px.hs0.znn', 1), job_znn(f'{c["znn"]}-big', 'Znunu_j', 5000, 'px.hs0.znn', 2)]
    files['znn'] = write_campaign(out, c['znn'], j, 0.3, 1800, me, 'pilot code slice: no-pile-up Z(nunu) events, extended summary', dp)
    # 4 Geant4 vertices from pool files
    mbf = lambda t: dpath(dp, c['mb'], f'{c["mb"]}-{t}.npz')  # noqa: E731
    hsf = lambda t: dpath(dp, c['hsg'], f'{c["hsg"]}-{t}.npz')  # noqa: E731
    g_all = {'dif': ['dif', 'k0l'], 'difc': ['difc'], 'nix': ['nix'], 'nic': ['nic'], 'ni22': ['ni22'], 'ni30': ['ni30'],
             'ni61': ['ni61']}
    g_ni = {'ni22': ['ni22'], 'ni30': ['ni30'], 'ni61': ['ni61']}
    g_hs = {'hs': B1_CLASSES}; g_lp = {'lowpt': B1_CLASSES}
    g = c['g4']
    j = [job_g4(f'{g}-all-r0', 'all', 200000, 'px.g4', 0, 'pool', g_all, [mbf('big')]),
         job_g4(f'{g}-all-r1', 'all', 200000, 'px.g4', 0, 'pool', g_all, [mbf('big')]),
         job_g4(f'{g}-all-d', 'all', 200000, 'px.g4', 1, 'pool', g_all, [mbf('big')]),
         job_g4(f'{g}-all-big', 'all', 2000000, 'px.g4', 2, 'pool', g_all, [mbf('big'), mbf('d')]),
         job_g4(f'{g}-ni-r0', 'ni', 1000000, 'px.g4', 100, 'pool', g_ni, [mbf('big')]),
         job_g4(f'{g}-ni-r1', 'ni', 1000000, 'px.g4', 100, 'pool', g_ni, [mbf('big')]),
         job_g4(f'{g}-ni-big', 'ni', 10000000, 'px.g4', 101, 'pool', g_ni, [mbf('big'), mbf('d')]),
         job_g4(f'{g}-hs-r0', 'all', 300000, 'px.g4', 200, 'pool', g_hs, [hsf('r0'), hsf('d')]),
         job_g4(f'{g}-hs-r1', 'all', 300000, 'px.g4', 200, 'pool', g_hs, [hsf('r0'), hsf('d')]),
         job_g4(f'{g}-lowpt-r0', 'all', 300000, 'px.g4', 300, 'lowpt', g_lp, [mbf('big')])]
    files['g4'] = write_campaign(out, g, j, 0.8, 2500, me, 'pilot code slice: Geant4 vertex production from pool files', dp)
    # 5 chain events for every sample
    b = c['b1']
    vf = lambda job, grp: dpath(dp, g, f'{g}-{job}.{grp}.npz')  # noqa: E731
    spec = [('dif', ['dif', 'k0l'], 'all-big'), ('difc', ['difc'], 'all-big'), ('nix', ['nix'], 'all-big'), ('nic', ['nic'], 'all-big'),
            ('ni22', ['ni22'], 'ni-big'), ('ni30', ['ni30'], 'ni-big'), ('ni61', ['ni61'], 'ni-big'), ('hs', B1_CLASSES, 'hs-r0'),
            ('lowpt', B1_CLASSES, 'lowpt-r0')]
    j = []
    for s, cl, src in spec:
        for r in ('r0', 'r1'):
            j.append(job_b1(f'{b}-{s}-{r}', s, cl, 2000, f'px.c0.{s}', 0, 0, 0.1, vf(src, s)))
    j.append(job_b1(f'{b}-dif-d', 'dif', ['dif', 'k0l'], 2000, 'px.c0.dif', 1, 2000, 0.1, vf('all-big', 'dif')))
    j.append(job_b1(f'{b}-dif-s', 'dif', ['dif', 'k0l'], 2000, 'px.c0.dif', 3, 0, 0.1, vf('all-big', 'dif')))   # same vertices, other seed
    j.append(job_b1(f'{b}-ni30-a', 'ni30', ['ni30'], 2000, 'px.c0.ni30', 1, 0, 0.1, vf('all-big', 'ni30')))    # NI from the 'all' pass
    for s, cl in (('dif', ['dif', 'k0l']), ('nix', ['nix']), ('nic', ['nic'])):
        j.append(job_b1(f'{b}-{s}-big', s, cl, 25000, f'px.c0.{s}', 2, 4000, 0.1, vf('all-big', s)))
    files['b1'] = write_campaign(out, b, j, 0.5, 2000, me, 'pilot code slice: chain events for every pilot sample type', dp)
    # 5b truncation of the parent (review A-1): the same events and seeds with v1's radius cut, the time cut, both
    tcamp = f'p2-c-px-tr{vmap.get("tr", "")}'
    j = [job_b1(f'{tcamp}-{s}-{mode}', s, cl, 2000, f'px.c0.{s}', 0, 0, 0.1, vf(src, s), mode)
         for s, cl, src in spec for mode in ('radius', 'time', 'both')]
    files['tr'] = write_campaign(out, tcamp, j, 0.2, 2000, me, 'pilot code slice: parent truncation by radius (v1), by time, by both', dp)
    c['tr'] = tcamp
    # 6 validation
    allf = []
    for camp_key in val_keys:
        d = json.loads(Path(files[camp_key]).read_text())
        allf += [dpath(dp, d['campaign'], o) for jb in d['jobs'] for o in jb['outputs'] if o.endswith('.npz')]
    v = c['val']
    part = QV2 / 'phase2_exploration' / 'outputs' / 'partition_p2-c-part-0.json'
    j = [dict(id=f'{v}-0', outputs=[f'{v}-0.json'],
              command=ENV + f'{ACTSPY} {SRC}/p2x_validate.py $QV2_OUT_DIR/{v}-0.json {part} ' + ' '.join(allf))]
    files['val'] = write_campaign(out, v, j, 0.1, 3000, me, 'pilot code slice: validation of every slice output', dp)
    log.info('launch order (one queue, 2 slots): %s', ' '.join(files[k] for k in ('mb', 'hsg', 'znn', 'g4', 'b1', 'val')))
    return files


# ---- pilot ----------------------------------------------------------------------------------------------------------
def usable(expected, n_meas, p):
    """Events that one vertex file safely holds: expectation minus yield error and Poisson margins."""
    rel = 1.0 / math.sqrt(max(n_meas, 1))
    return int(math.floor(expected * (1.0 - p['g4']['margin_yield_err'] * rel) - p['g4']['margin_sigma'] * math.sqrt(expected)))


def sample_layout(events, per_job_max, per_file):
    """(jobs per file S, events per job n, files needed, list of (file, first, n)) for an exact total of `events`."""
    assert per_file > 0, 'a vertex file is expected to hold no usable vertex of this sample'
    s_per = max(1, math.ceil(per_file / per_job_max))
    n = per_file // s_per
    jobs = []; left = events; f = 0
    while left > 0:
        for s in range(s_per):
            if left <= 0:
                break
            m = min(n, left)
            jobs.append((f, s * n, m)); left -= m
        f += 1
    return s_per, n, f, jobs


def pilot(p, outdir=None):
    is_test = '-px-' in p['prefix']            # launch test of the machinery: validation prefix and px.* streams only
    assert is_test == ('px_validation' in p['data_prefix']) and (is_test or not p['data_prefix'].startswith('p2c')), \
        'pilot campaigns need their own data prefix; test campaigns (-px-) the validation prefix'
    tag = p['name']; pre = p['prefix'] + (f'-{tag}' if tag else ''); dp = p['data_prefix']
    only = set(p.get('only') or ['mb', 'b1', 'znn'])
    assert only <= {'mb', 'b1', 'znn'}, f'only: {only}'
    outdir = Path(outdir) if outdir else CAMP_DIR / 'pilot'
    me = f'python3 -I {SRC}/p2x_pilot_campaigns.py pilot (parameters: PLAN_{pre}.json -> params)'
    Y = json.loads(Path(p['yields']).read_text()) if 'b1' in only else {}
    cost = p['costs']; ovh = cost['job_overhead_s']
    plan = dict(name=tag, params=p, campaigns=[], samples={}, warnings=[])
    for s in list(p['samples'].values()) + [p['hs'], p['lowpt']]:
        assert all(c in B1_CLASSES for c in s['classes']), f"unknown class in {s['classes']}"
    used = sum((s['classes'] for s in p['samples'].values()), [])
    assert len(used) == len(set(used)), 'a class is in two samples'
    not_read = [c for c in B1_CLASSES if c not in used]
    if not_read:
        plan['warnings'].append(f'classes in no pilot sample: {not_read}')

    def add(name, jobs, cpu_s, rss, desc, bytes_, after=(), events=None, unit=''):
        f = write_campaign(outdir, name, jobs, cpu_s / 3600.0 / 2, rss, me, desc, dp, after)
        plan['campaigns'].append(dict(campaign=name, file=f, jobs=len(jobs), cpu_h=round(cpu_s / 3600.0, 2),
                                      max_job_min=None, storage_gb=round(bytes_ / 1e9, 2), after=list(after), size=events,
                                      unit=unit))
        return name

    # --- minimum bias
    mb = p['mb']; n_mb = math.ceil(mb['interactions'] / mb['per_job'])
    cmb = f'{pre}-mb' + (f"-{mb['part0']:02d}" if mb['part0'] else '')
    mbid = lambda k: f"{pre}-mb-{mb['chunk0'] + k:04d}"  # noqa: E731   (job id = chunk number: unique across appended parts)
    if 'mb' in only:
        jobs = [job_mb(mbid(k), min(mb['per_job'], mb['interactions'] - k * mb['per_job']), mb['stream'], mb['chunk0'] + k,
                       mb['chunk0'] + k < mb['xpool_jobs']) for k in range(n_mb)]
        add(cmb, jobs, mb['interactions'] * cost['mb_ms'] * 1e-3 + n_mb * ovh, cost['rss_mb']['mb'],
            f"pilot: minimum bias, generator level, stream {mb['stream']}, chunks {mb['chunk0']}-{mb['chunk0'] + n_mb - 1}",
            mb['interactions'] * cost['mb_bytes_per_int'], events=mb['interactions'], unit='interactions')
    mbfile = lambda k: dpath(dp, cmb, f'{mbid(k % n_mb)}.npz')  # noqa: E731

    # --- Geant4 passes for the class samples
    g4 = p['g4']; vsrc = {}
    for gpass, per_job, ms in (('all', g4['all_per_job'], cost['g4_all_ms']), ('ni', g4['ni_per_job'], cost['g4_ni_ms'])) if 'b1' in only else ():
        ss = {k: s for k, s in p['samples'].items() if s['pass'] == gpass}
        if not ss:
            continue
        y = Y[gpass]
        lay = {}
        for k, s in ss.items():
            if gpass == 'ni':
                assert all(c in ('ni22', 'ni30', 'ni61') for c in s['classes']), f"sample {k}: classes not complete in the 'ni' pass"
            nm = sum(y['counts'][c] for c in s['classes'])
            exp = nm / y['n_fire'] * per_job
            u = usable(exp, nm, p)
            lay[k] = sample_layout(s['events'], s['per_job'], u) + (exp, u)
        n_files = math.ceil(max(v[2] for v in lay.values()) * (1.0 + g4.get('extra_firings', 0.0)))
        cg = f'{pre}-g4{gpass[0]}'
        groups = {k: s['classes'] for k, s in ss.items()}
        nppj = g4['pool_files_per_job']
        off = 0 if gpass == 'all' else 17          # the two passes start at different pool files
        jobs = [job_g4(f'{cg}-{k:04d}', gpass, per_job, g4['stream'], g4['chunk0'][gpass] + k, 'pool', groups,
                       [mbfile(off + nppj * k + i) for i in range(nppj)]) for k in range(n_files)]
        nv = sum(sum(y['counts'][c] for c in s['classes']) for s in ss.values()) / y['n_fire'] * per_job * n_files
        add(cg, jobs, n_files * per_job * ms * 1e-3 * 1.25 + n_files * ovh, cost['rss_mb']['g4'],
            f"pilot: Geant4 vertices, pass '{gpass}', stream {g4['stream']}", nv * cost['vtx_bytes'], after=[cmb],
            events=n_files * per_job, unit='firings')
        for k, s in ss.items():
            s_per, n, nf, jl, exp, u = lay[k]
            vsrc[k] = (cg, jl)
            plan['samples'][k] = dict(classes=s['classes'], events=s['events'], g4_pass=gpass, expected_per_file=round(exp, 1),
                                      usable_per_file=u, jobs_per_file=s_per, events_per_job=n, files_used=nf,
                                      files_made=n_files, stream=s['stream'],
                                      vertices_unused_fraction=round(1 - s['events'] / (exp * n_files), 3))

    # --- chain campaigns of the class samples
    for k, s in (p['samples'].items() if 'b1' in only else ()):
        cg, jl = vsrc[k]
        cc = f'{pre}-c0-{k}'
        jobs = [job_b1(f'{cc}-{i:04d}', k, s['classes'], n, s['stream'], i, first, p['beta_min'],
                       dpath(dp, cg, f'{cg}-{f:04d}.{k}.npz'), p['trunc'].get(k, p['trunc']['default']),
                       p['n_road_orientations']) for i, (f, first, n) in enumerate(jl)]
        assert sum(x[2] for x in jl) == s['events']
        add(cc, jobs, s['events'] * cost['b1_ms'] * 1e-3 + len(jobs) * ovh, cost['rss_mb']['b1'],
            f"pilot: no-pile-up events of sample {k} = {'+'.join(s['classes'])}, stream {s['stream']}",
            s['events'] * cost['b1_bytes'], after=[cg], events=s['events'], unit='events')

    # --- mixed samples: hard-scatter parents, low-pT parents
    for key, pool_prefix in (('hs', 'pool'), ('lowpt', 'lowpt')):
        m = p[key]
        if not m.get('enabled') or 'b1' not in only:
            continue
        y = Y[key]
        nm = sum(y['counts'][c] for c in m['classes'])
        if key == 'hs':
            ch = f'{pre}-hsg'
            ng = math.ceil(m['gen_events'] / m['gen_per_job'])
            jobs = [job_hsg(f'{ch}-{i:04d}', m['gen_sample'], min(m['gen_per_job'], m['gen_events'] - i * m['gen_per_job']),
                            m['gen_stream'], i) for i in range(ng)]
            add(ch, jobs, m['gen_events'] * cost['hsgen_ms'] * 1e-3 + ng * ovh, cost['rss_mb']['hsgen'],
                f"pilot: hard-scatter parent pool ({m['gen_sample']}, generator level), stream {m['gen_stream']}",
                m['gen_events'] * 60.0, events=m['gen_events'], unit='generated events')
            pools = [dpath(dp, ch, f'{ch}-{i:04d}.npz') for i in range(ng)]; dep = ch
        else:
            pools = [mbfile(i) for i in range(min(4, n_mb))]; dep = cmb
        per_job = g4['all_per_job']
        # firings so that the files hold `events` usable vertices: one or more jobs of equal size
        n_fire_total = m['events'] / (nm / y['n_fire']) * 1.05
        nj = max(1, math.ceil(n_fire_total / per_job))
        while True:
            fire = int(math.ceil(n_fire_total / nj / 1000.0) * 1000)
            u = int(usable(nm / y['n_fire'] * fire, nm, p) * (1.0 - m.get('pool_margin', 0.10)))   # small pool: its own yield varies
            if u * nj >= m['events']:
                break
            n_fire_total *= 1.02
        cg = f'{pre}-g4{key[0]}'
        jobs = [job_g4(f'{cg}-{i:04d}', 'all', fire, g4['stream'], g4['chunk0'][key] + i, pool_prefix, {key: m['classes']}, pools)
                for i in range(nj)]
        add(cg, jobs, nj * fire * cost['g4_all_ms'] * 1e-3 * 1.25 + nj * ovh, cost['rss_mb']['g4'],
            f"pilot: Geant4 vertices of the {key} parents, stream {g4['stream']}", nj * fire * nm / y['n_fire'] * cost['vtx_bytes'],
            after=[dep], events=nj * fire, unit='firings')
        s_per, n, nf, jl = sample_layout(m['events'], m['per_job'], u)
        assert nf <= nj
        cc = f'{pre}-c0-{key}'
        jobs = [job_b1(f'{cc}-{i:04d}', key, m['classes'], n_, m['stream'], i, first, p['beta_min'],
                       dpath(dp, cg, f'{cg}-{f:04d}.{key}.npz'), p['trunc'].get(key, p['trunc']['default']),
                       p['n_road_orientations']) for i, (f, first, n_) in enumerate(jl)]
        add(cc, jobs, m['events'] * cost['b1_ms'] * 1e-3 + len(jobs) * ovh, cost['rss_mb']['b1'],
            f"pilot: no-pile-up events of the mixed sample {key}, stream {m['stream']}", m['events'] * cost['b1_bytes'],
            after=[cg], events=m['events'], unit='events')
        plan['samples'][key] = dict(classes=m['classes'], events=m['events'], g4_pass='all', firings_per_file=fire,
                                    usable_per_file=u, jobs_per_file=s_per, events_per_job=n, files_used=nf, stream=m['stream'])

    # --- Z(nunu), in parts so that the lanes can be balanced
    z = p['znn']; nz = math.ceil(z['events'] / z['per_job']); parts = max(1, min(z['parts'], nz))
    per_part = math.ceil(nz / parts)
    for a in range(parts if 'znn' in only else 0):
        ks = range(a * per_part, min((a + 1) * per_part, nz))
        if not len(ks):
            continue
        cz = f"{pre}-znn-{z['part0'] + a:02d}"
        jobs = [job_znn(f"{pre}-znn-{z['chunk0'] + k:05d}", z['sample'], min(z['per_job'], z['events'] - k * z['per_job']),
                        z['stream'], z['chunk0'] + k) for k in ks]
        ne = sum(min(z['per_job'], z['events'] - k * z['per_job']) for k in ks)
        add(cz, jobs, ne * cost['znn_ms'] * 1e-3 + len(jobs) * ovh, cost['rss_mb']['znn'],
            f"pilot: no-pile-up {z['sample']} events, stream {z['stream']}, part {a}", ne * cost['znn_bytes'], events=ne,
            unit='events')

    # --- lanes: one queue per slot.  Lane 0 = minimum bias and everything that reads its 'all' pass; the other chains and
    # the Z(nunu) parts are spread greedily on CPU-h.  A campaign placed before its inputs exist only waits (p2x_queue.sh
    # checks the `after` list), so the order below matters for the wall time, not for correctness.
    by = {c['campaign']: c for c in plan['campaigns']}
    is_ni = lambda c: c['campaign'].endswith('-g4n') or c['campaign'].split('-c0-')[-1] in ('ni22', 'ni30', 'ni61')  # noqa: E731
    is_hs = lambda c: c['campaign'].endswith(('-hsg', '-g4h', '-c0-hs'))  # noqa: E731
    is_z = lambda c: '-znn-' in c['campaign']  # noqa: E731
    chain_a = [c for c in plan['campaigns'] if not (is_ni(c) or is_hs(c) or is_z(c))]
    chain_n = [c for c in plan['campaigns'] if is_ni(c)]
    chain_h = [c for c in plan['campaigns'] if is_hs(c)]
    zparts = [c for c in plan['campaigns'] if is_z(c)]
    mb_h = by[cmb]['cpu_h'] * 1.15 if cmb in by else 0.0
    plan['lanes'] = {}
    for nslot in p['slots']:
        lanes = [[] for _ in range(nslot)]; load = [0.0] * nslot

        def put(i, cs):
            for c in cs:
                lanes[i].append(c['file']); load[i] += c['cpu_h']
        put(0, chain_a)
        if nslot == 1:
            put(0, chain_h + chain_n + zparts)
        else:
            put(1, chain_h)
            zq = list(zparts); n_done = not chain_n
            while zq or not n_done:
                i = load.index(min(load))
                if not n_done and ((i != 0 and load[i] >= mb_h) or not zq):
                    put(i, chain_n); n_done = True
                elif zq:
                    put(i, [zq.pop(0)])
        plan['lanes'][str(nslot)] = dict(lanes=lanes, cpu_h=[round(x, 1) for x in load], wall_h=round(max(load), 1))
    tot = sum(c['cpu_h'] for c in plan['campaigns'])
    plan['total'] = dict(cpu_h=round(tot, 1), storage_gb=round(sum(c['storage_gb'] for c in plan['campaigns']), 1),
                         jobs=sum(c['jobs'] for c in plan['campaigns']),
                         b1_events=sum(s['events'] for s in p['samples'].values()) if 'b1' in only else 0)
    scr = sorted({x for b in only for x in BLOCK_FILES[b][0]}); inp = sorted({x for b in only for x in BLOCK_FILES[b][1]})
    plan['hashes'] = dict(scripts={s: sha(HERE / s) for s in scr if (HERE / s).exists()},
                          inputs={i: (sha(QV2 / i) if (QV2 / i).exists() else None) for i in inp})
    plan['frozen_from_launch'] = [f'phase2_exploration/src/{x}' for x in scr] + inp
    plan['campaign_file_sha256'] = {c['campaign']: sha(c['file']) for c in plan['campaigns']}
    pf = outdir / (f'PLAN_{pre}' + ('_' + '-'.join(sorted(only)) if only != {'mb', 'b1', 'znn'} else '') + (f"_{p['plan_suffix']}" if p.get('plan_suffix') else '') + '.json')
    # launch / status scripts (text; run from einstein; they are NOT executed by this generator)
    stem = pf.name[len('PLAN_'):-len('.json')]
    plan['scripts'] = {}
    q = f'{SRC}/p2x_queue.sh'
    for nslot, v in plan['lanes'].items():
        lines = ['#!/bin/bash', f'# launch of {stem} on {nslot} slot(s) of NODE (default schrodinger): one queue per slot, 1 job each.',
                 '# Run on einstein AFTER: preflight ok, a line in phase2_exploration/SLOTS.md, the go of the orchestrator.',
                 '# Resume after any stop: run this script again (complete campaigns and done jobs are skipped).',
                 'NODE=${1:-schrodinger}',
                 'echo "qv2run jobs on $NODE now: $(ssh -x -o BatchMode=yes $NODE "pgrep -u jdochoa -af \'[q]v2run job\' | wc -l")"']
        for i, lane in enumerate(v['lanes']):
            if not lane:
                continue
            first = Path(lane[0]).stem
            pid = f'/home/scratch/jdochoa/drivers/{stem}_{nslot}slots_lane{i}.pid'
            logf = f'/home/scratch/jdochoa/drivers/{stem}_{nslot}slots_lane{i}.log'
            inner = f'echo \\$\\$ > {pid}; exec {q} $NODE 1 ' + ' '.join(lane)
            lines.append(f'ssh -x -o BatchMode=yes $NODE "mkdir -p /home/scratch/jdochoa/drivers; rm -f /home/scratch/jdochoa/drivers/STOP.{first}; '
                         f'if [ -e {pid} ] && kill -0 \\$(cat {pid}) 2>/dev/null; then echo lane {i} already runs; else '
                         f"setsid nohup bash -c '{inner}' > {logf} 2>&1 < /dev/null & echo lane {i} started; fi\"")
        lf = outdir / f'LAUNCH_{stem}_{nslot}slots.sh'
        lf.write_text('\n'.join(lines) + '\n')
        plan['scripts'][f'launch_{nslot}slots'] = str(lf)
    st = ['#!/bin/bash', f'# status of {stem} from the markers (run on einstein; the runner itself runs on the worker)', 'NODE=${1:-schrodinger}',
          f'ssh -x -o BatchMode=yes $NODE \'for f in ' + ' '.join(c['file'] for c in plan['campaigns']) +
          f'; do {RUNNER}/bin/qv2run status $f --json; done; tail -n 2 /home/scratch/jdochoa/drivers/{stem}_*lane*.log 2>/dev/null; '
          'pgrep -u jdochoa -af "[q]v2run job" | wc -l\'']
    sf = outdir / f'STATUS_{stem}.sh'
    sf.write_text('\n'.join(st) + '\n')
    plan['scripts']['status'] = str(sf)
    plan['scripts']['stop'] = ('touch /home/scratch/jdochoa/drivers/STOP.<first campaign of the lane> on the node: the lane ends after its '
                               'running campaign; running jobs are never killed by it')
    pf.write_text(json.dumps(plan, indent=1) + '\n')
    log.info('plan: %s', pf)
    log.info('total: %s', plan['total'])
    for k, v in plan['lanes'].items():
        log.info('%s slots: CPU-h per lane %s, wall %.1f h', k, v['cpu_h'], v['wall_h'])
    for w in plan['warnings']:
        log.warning('%s', w)
    return plan


# ---- yields -----------------------------------------------------------------------------------------------------------
def yields(val_json, out=None):
    """Measured vertices per firing for the generator, from the partition file of p2-c-part-0 and the validation JSON of
    the slices (each distinct Geant4 job counted once: reruns with the same stream and chunk are the same firings)."""
    part_f = QV2 / 'phase2_exploration' / 'outputs' / 'partition_p2-c-part-0.json'
    part = json.loads(part_f.read_text())
    val = json.loads(Path(val_json).read_text())
    Y = {k: dict(n_fire=0, counts={c: 0 for c in B1_CLASSES + ['conversion', 'other']}, sources=[]) for k in ('all', 'ni', 'hs', 'lowpt')}
    Y['all']['n_fire'] += part['n_fire']
    for c in Y['all']['counts']:
        Y['all']['counts'][c] += part['counts'].get(c, {}).get('all', 0)
    Y['all']['sources'].append(str(part_f))
    seen = set()
    for r in val['files']:
        if r['mode'] != 'g4prod':
            continue
        kind = r['group'] if r['group'] in ('hs', 'lowpt') else r['g4_pass']
        key = (kind, r['stream'], r['chunk'], r['n_fire'])
        if key in seen:
            continue
        seen.add(key)
        Y[kind]['n_fire'] += r['n_fire']
        for c in Y[kind]['counts']:
            Y[kind]['counts'][c] += r['counts'][c]
        Y[kind]['sources'].append(f"{r['file'].rsplit('/', 1)[-1].split('.')[0]} (stream {r['stream']}, chunk {r['chunk']})")
    for k in Y:
        Y[k]['per_firing'] = {c: (n / Y[k]['n_fire'] if Y[k]['n_fire'] else None) for c, n in Y[k]['counts'].items()}
    Y['ni']['note'] = "only ni22, ni30, ni61 are complete in the 'ni' pass"
    Y['validation_json'] = str(val_json)
    out = Path(out) if out else QV2 / 'phase2_exploration' / 'outputs' / 'pilot_yields_xavier.json'
    out.write_text(json.dumps(Y, indent=1) + '\n')
    log.info('yields -> %s', out)
    for k in ('all', 'ni', 'hs', 'lowpt'):
        log.info('%s: %d firings %s', k, Y[k]['n_fire'], Y[k]['counts'])


# ---- pre-flight -----------------------------------------------------------------------------------------------------
def preflight(plan_file):
    """Read-only checks on einstein before a launch.  Returns the number of failed checks."""
    plan = json.loads(Path(plan_file).read_text())
    bad = 0

    def check(ok, msg):
        nonlocal bad
        bad += 0 if ok else 1
        log.info('%s  %s', 'ok  ' if ok else 'FAIL', msg)
    st = os.statvfs('/nfs/cajuela/jdochoa/quirks_v2')
    free = st.f_bavail * st.f_frsize / 1e9
    need = plan['total']['storage_gb']
    check(free > 3 * need, f'cajuela free {free:.0f} GB, pilot needs about {need:.0f} GB (required: 3x)')
    markers = QV2 / 'ledger' / 'markers'
    check(markers.is_dir() and os.access(markers, os.W_OK), f'markers directory writable: {markers}')
    dp = plan['params']['data_prefix']
    for c in plan['campaigns']:
        name = c['campaign']
        clash = [str(x) for x in (markers / name, Path(DATA) / dp / name, Path(DATA) / name) if x.exists()]
        check(not clash, f'{name}: no markers or data of that name yet' + (f' (found {clash})' if clash else ''))
        check(Path(c['file']).exists() and sha(c['file']) == plan['campaign_file_sha256'][name], f'{name}: campaign file unchanged since the plan')
    others = {p.stem for d in (REPO / 'tools' / 'runner' / 'campaigns', REPO / 'tools' / 'runner' / 'examples' / 'p2c',
                               REPO / 'tools' / 'runner' / 'examples' / 'p2v', CAMP_DIR / 'slices') if d.is_dir() for p in d.glob('*.json')}
    names = [c['campaign'] for c in plan['campaigns']]
    check(not (set(names) & others) and len(names) == len(set(names)), 'no campaign name clash with existing campaign files')
    ids = []
    for c in plan['campaigns']:
        ids += [j['id'] for j in json.loads(Path(c['file']).read_text())['jobs']]
    check(len(ids) == len(set(ids)), f'{len(ids)} job ids, all distinct')
    for s, h in plan['hashes']['scripts'].items():
        check((HERE / s).exists() and sha(HERE / s) == h, f'script unchanged since the plan: {s} {h[:12]}')
    for i, h in plan['hashes']['inputs'].items():
        check(h is not None and (QV2 / i).exists() and sha(QV2 / i) == h, f'input unchanged since the plan: {i} {(h or "missing")[:12]}')
    pp = plan['params']; only = set(pp.get('only') or ['mb', 'b1', 'znn'])
    streams = ([pp['mb']['stream']] if 'mb' in only else []) + ([pp['znn']['stream']] if 'znn' in only else [])
    if 'b1' in only:
        streams += [pp['g4']['stream']] + [s['stream'] for s in pp['samples'].values()] + \
                   [pp[k]['stream'] for k in ('hs', 'lowpt') if pp[k].get('enabled')] + \
                   ([pp['hs']['gen_stream']] if pp['hs'].get('enabled') else [])
    # appended parts: no job id of this plan may already have a marker (checked per campaign above by name; here by id)
    have = {m.stem for m in markers.glob(f"{pp['prefix']}*/*/*.marker")}
    check(not (set(ids) & have), f'no job id of this plan has a marker yet ({len(set(ids) & have)} found)')
    is_test = '-px-' in pp['prefix']
    check(len(streams) == len(set(streams)) and all(s.startswith('px.') == is_test for s in streams),
          f'seed streams distinct; validation streams (px.*) only in a test: {streams}')
    log.info('%d failed checks. Remaining manual checks: node count (pgrep), SLOTS.md line, approval of the addendum.', bad)
    return bad


def main(argv):
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    what = argv[0]
    if what == 'slices':
        slices(argv[argv.index('--ver') + 1] if '--ver' in argv else '',
               tuple(argv[argv.index('--val') + 1].split(',')) if '--val' in argv else ('mb', 'hsg', 'znn', 'g4', 'b1'),
               argv[argv.index('--sub') + 1] if '--sub' in argv else 'slices')
    elif what == 'defaults':
        sys.stdout.write(json.dumps(DEFAULTS, indent=1) + '\n')
    elif what == 'pilot':
        p = copy.deepcopy(DEFAULTS)
        a = argv[1:]; outdir = None
        while a:
            k = a.pop(0)
            if k == '--params':
                deep_update(p, json.loads(Path(a.pop(0)).read_text()))
            elif k == '--set':
                set_path(p, a.pop(0))
            elif k == '--outdir':
                outdir = a.pop(0)
            elif k == '--name':
                p['name'] = a.pop(0)
            else:
                raise SystemExit(f'unknown argument {k}')
        pilot(p, outdir)
    elif what == 'yields':
        yields(argv[1], argv[2] if len(argv) > 2 else None)
    elif what == 'preflight':
        raise SystemExit(1 if preflight(argv[1]) else 0)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
