"""run_stage4.py -- Stage-4 production runner (C001 quirks theory track; Phase A, G1 integration 2026-10-13).

Pattern of sim/stage3/code/run_stage3.py: one job = one (campaign, sample, chunk); it writes ONE npz atomically (tmp
file, then os.replace); a rerun skips every job whose output exists and validates, so stopping and restarting is safe.
Run from theory_track/ in the TT pixi env (the finder's numba cache is keyed to the import path acts.stage4.finder):

  pixi run python -m acts.stage4.run_stage4 manifest                      write acts/stage4/jobs/{C1,C2,C4p,G3,smoke}.json
  pixi run python -m acts.stage4.run_stage4 run    --campaign C1 [--workers 7] [--mem-gb 18] [--max-jobs K]
  pixi run python -m acts.stage4.run_stage4 status --campaign C1          done/total, blocked, CPU-h, ETA
  pixi run python -m acts.stage4.run_stage4 check  --campaign C1          deep-validate every output
  pixi run python -m acts.stage4.run_stage4 smoke                         2 PU-only jobs (interim chain), ~5 min
Graceful stop: create data/acts_stage4/prod/<campaign>/STOP (no new job starts; running jobs finish).  Hard stop: kill
the processes; partial outputs are only *.tmp*.npz, removed at the next start.  Workers run at nice +10 (default).

Chain.  Every job first runs a chain step in the acts env (subprocess `pixi run --manifest-path acts/pixi.toml ...`):
  * the G1 production chain acts/stage4/code/run_chain.py (2026-10-13): direct SimParticle reader, 32 phi-sectors,
    smearing doMerge = False, GridTriplet + CKF (pT > 0.9 GeV) with a per-measurement CKF flag, V4-1 records;
    the TT side (finder/chain_inputs.py) then applies exact interaction ids, the TDR top-up, CKF removal and the U-5 b
    analysis-level merging;
  * (development only, --allow-interim with run_chain.py absent) the INTERIM chain pu_chain_interim.py.
Production manifests refuse to run before the freeze (acts/stage4/frozen_inputs.json with frozen = true and the
sha256 of WP_RULE.md); dev campaigns (smoke, smokeG1, g1bench) use the freeze-candidate data/acts_stage4/frozen/.
Job kinds run here (G1): 'pu' (B1/B2/G3), 'sm' (SM hard scatter + PU, block C), 'dens' (B-9 rho = 1 re-run of the S6
dumps at the low/high top-up, after B1).  Still listed as requires='G1' blocks: signal A1/A2/A5 and C' (G1_REPORT §7).
rho > 1 production jobs are BLOCKED until process_trial has btl= (SR-T in-job columns; require_btl=True is passed).

PU-only jobs (B1: rho = 1, 4 roads; B2: rho = 2, 2 roads) then run, per trial, acts.stage4.finder.production.
process_trial (finder, distinct-hit-set groups, rung tables, in-job weights, storage policy of WP_RULE.md §S).
Determinism: job seed = blake2b("stage4|<sample>|<chunk>"); event streams numpy SeedSequence(job seed).spawn; outputs
record every seed, code sha256s, the chain meta and timing.
"""
import argparse
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent                 # acts/stage4
TT = HERE.parents[1]
PROD = TT / 'data' / 'acts_stage4' / 'prod'
JOBS = HERE / 'jobs'
CODE = HERE / 'code'
CHAIN_PROD = CODE / 'run_chain.py'
CHAIN_INTERIM = CODE / 'pu_chain_interim.py'
ACTS_MANIFEST = TT / 'acts' / 'pixi.toml'
FROZEN = HERE / 'frozen_inputs.json'      # written at the WP_RULE.md freeze: {"frozen": true, "delta95": .., "mip_gev": ..,
                                         #  "wp_rule_sha256": ..}; production manifests refuse to run without it
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
import numpy as np  # noqa: E402

RUNNER_VERSION = 'g1-1'
# Timing constants re-timed after the T_seed := 4 action (G3_REPORT §4/§6, WP_RULE §6.4; HASH_ADDENDUM §5, 2026-10-14).
# Units: per-worker seconds UNDER THE 7-WORKER PRODUCTION LOAD (G3-measured), so est_s ~ job wall and the 'status'
# throughput ~ the number of busy workers.  Previous G1 values (1 process, T_seed 6): PU_S 4.83, T1_S 3.26, T2_S 20.1.
PU_S = 10.2                   # G3: chain per PU event in B1 jobs, under load (G1: 4.83, 1 process)
PU_S_RHO2 = 9.3               # G3: chain per PU event in B2 jobs, under load
T1_S = 8.02                   # G3 paired re-run at T_seed = 4, under load (T_seed 6: 5.52; G1 1-process: 3.26)
T2_S = 50.6                   # G3 paired re-run at T_seed = 4, incl. in-job weights, under load (T_seed 6: 34.4; G1: 20.1)
MEM_GB = {'B1': 1.5, 'B2': 4.0, 'G1': 1.0}     # peak RSS per job (G2b: 3.9 GB at rho = 2)
EVSTAT_COLS = ['n_fatras', 'n_topup', 'n_ckf_removed', 'n_pool', 'n_merged_groups', 'n_merged_hits', 'n_sigma_enlarged']
CODE_FILES = ['acts/stage4/run_stage4.py', 'acts/stage4/finder/finder.py', 'acts/stage4/finder/kernels.py',
              'acts/stage4/finder/weights.py', 'acts/stage4/finder/production.py', 'acts/stage4/finder/pu_inputs.py',
              'acts/stage4/code/pu_chain_interim.py', 'acts/stage4/WP_RULE.md', 'acts/stage4/finder/chain_inputs.py',
              'acts/stage4/code/run_chain.py', 'acts/stage4/code/s4pu.py', 'acts/stage4/code/s4geo.py',
              'acts/stage4/code/eloss.py', 'acts/stage4/code/s4sig.py', 'acts/stage4/code/s4cp.py',
              'data/acts_stage4/g1/pythia_init/mpi_cp5_14tev_minbias.dat']

# ----------------------------------------------------------------------------------------------- campaign contents
# plan §6.2 (frozen with WP_RULE.md).  PU-only blocks: (sample, n_events, events per job, roads, rho).
PU_BLOCKS = {
    'C1': [('B1', 0, 5000, 25, 4, 1), ('B2', 0, 1000, 10, 2, 2)],
    'C2': [('B1', 5000, 7000, 25, 4, 1), ('B2', 1000, 2000, 10, 2, 2)],
    'C4p': [],
    'G3': [('G3B1', 0, 2000, 25, 4, 1), ('G3B2', 0, 500, 10, 2, 2)],
    'smoke': [('SMB1', 0, 2, 2, 4, 1), ('SMB2', 0, 1, 1, 2, 2)],
    'smokeG1': [],
}
# SM hard scatter + PU (block C, plan §4.2/§6.2; G1 job kind 'sm'): (sample tag, s4pu.SM_SAMPLES name, ev0, n, per job).
# W(tau nu)+j: 'tau forced hadronic in one subsample' (plan §4.2) -> half of each W(tau nu) block is the forced-hadronic
# subsample Wtauhnu_j (G1 DECISION, flagged); events are seeded by (tag, chunk), so C2 adds to C1.
SM_BLOCKS = {
    'C1': [('C_Znunu_j', 'Znunu_j', 0, 2000, 20), ('C_Wtaunu_j', 'Wtaunu_j', 0, 1000, 20),
           ('C_Wtauhnu_j', 'Wtauhnu_j', 0, 1000, 20), ('C_ttbar_1l', 'ttbar_1l', 0, 2000, 20)],
    'C2': [('C_Wenu_j', 'Wenu_j', 0, 5000, 20), ('C_Wmunu_j', 'Wmunu_j', 0, 5000, 20),
           ('C_Znunu_j', 'Znunu_j', 2000, 3000, 20), ('C_Wtaunu_j', 'Wtaunu_j', 1000, 1500, 20),
           ('C_Wtauhnu_j', 'Wtauhnu_j', 1000, 1500, 20), ('C_ttbar_1l', 'ttbar_1l', 2000, 3000, 20)],
    'C4p': [], 'G3': [], 'smoke': [], 'smokeG1': [('SMC_Znunu_j', 'Znunu_j', 0, 2, 2)],
}
# blocks needing the G1 production chain: (name, description, CPU-h at the measured t1 (plan §6.2 arithmetic))
G1_BLOCKS = {
    'C1': [('A1', 'signal only, all 307 p2 + 60 mv points, both halves, no PU', 2.0),
           ('A2core', 'E200/500/1000/1500 + S500 x {0.45,0.6,0.85,1,1.5,2,3,5} keV, 200 events each, row-major (1000 rows)',
            (1000 * PU_S + 8000 * (0.1 + T1_S)) / 3600),
           ('A5core', '5 points, full chain (quirk hits through ACTS digitisation + CKF), 1000 events', 8.0 + 1000 * T1_S / 3600),
           ('C', 'Z(nunu)+j, W(taunu)+j, ttbar 1l x 2000, + PU 200', 6000 * (PU_S + T1_S) / 3600),
           ('Cp0', "C'0 guns/toys without PU (gamma, K0S/Lambda, PV pair, looper 1e5 each; NI 3 x 3e4; DIF 5e4)", 12.0),
           ('CpPU', "C'_PU 8 topologies x 500 with PU (NI/DIF: preselected C'0 toy events, stored hits inserted)",
            4000 * (PU_S + T1_S) / 3600),
           ('val', 'validation V4-1/V4-4 etc.', 15.0)],
    'C2': [('C', 'W(enu), W(munu) 5000 each; Z(nunu), W(taunu), ttbar +3000 each (-> 5 x 5000)', 19000 * (PU_S + T1_S) / 3600),
           ('val', 'validation', 5.0)],
    'C4p': [('A2rest', 'rest of A2: all 307 points (53 344 events, 2 400 rows)', (2400 * PU_S + 53344 * (0.1 + T1_S)) / 3600),
            ('A5rest', 'A5 -> 20 points + the PU-140 rerun', 22.0 + 3000 * T1_S / 3600),
            ('val', 'validation', 5.0)],
    'G3': [], 'smoke': [], 'smokeG1': [],
}
DEV_CAMPAIGNS = ('smoke', 'smokeG1', 'g1bench')     # development: no freeze needed, freeze-candidate config
RUNNABLE = ('pu', 'sm', 'dens')
G1B_KINDS = ('a1', 'a2', 'a5', 'cp0', 'cppu')      # G1b (run_g1b.py, HASH_ADDENDUM.md): signal A1/A2/A5, C'0, C'_PU
G1B_REPLACES = ('A1', 'A2core', 'A5core', 'Cp0', 'CpPU')    # G1_BLOCKS placeholders replaced by G1b jobs
RUNNABLE = RUNNABLE + G1B_KINDS
# plan §11 decision table, row '7-12 s' (G3 t1 = 8.02 s at T_seed = 4): C1 runs as two sequential sub-runs over the SAME
# C1 job list (identical job dicts, seeds and output paths under prod/C1/): C1a = the G1b kinds (A1, A2, A5, C'0, C'_PU),
# C1b = B1, B2, block C ('sm'), B-9 'dens' and the 'val' placeholder.  Progress/STOP/error files live in prod/C1/.
# C2B = C2-B (plan §11 row '5-7 s'; user-approved after C1, 2026-10-14): only the PU-only B1/B2 jobs of C2 (outputs and
# progress files under prod/C2/); C2-C (the 'sm' jobs) and the C2 'val' placeholder are not part of it.
SPLITS = {'C1a': ('C1', G1B_KINDS), 'C1b': ('C1', ('pu', 'sm', 'dens', 'g1')), 'C2B': ('C2', ('pu',))}
# B-9 (WP_RULE §4.1, PC-11): rho = 1 re-run of the S6 dump events (first 2 000 C1 B1 events = B1 chunks 0-79) at the
# low and high top-up; ~2 x 9 CPU-h; ordered after B1 (order 2) and run only when its source B1 file exists.
DENS_BLOCKS = {'C1': [('low', 'B1', 2000, 25), ('high', 'B1', 2000, 25)], 'smoke': [('low', 'SMB1', 2, 2)]}             # job kinds run_pu_job executes (G1); 'g1' blocks are still listed as BLOCKED
ROAD_DUMP = {('B1', 'C1'): 2000,     # plan §4.1 step 1 (critical C-10): chain output of the first 2 000 B1 events kept
             ('SMB1', 'smoke'): 2}   # exercise the dump path (and the B-9 dens re-run) in the smoke test


def hash_seed(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') & 0x7FFFFFFFFFFF


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def code_hashes():
    return {f: (sha256_file(TT / f) if (TT / f).exists() else None) for f in CODE_FILES}


def frozen_inputs():
    if not FROZEN.exists():
        return None
    d = json.loads(FROZEN.read_text())
    return d if d.get('frozen') else None


def make_manifest(camp):
    if camp in SPLITS:                    # sub-run: a kind filter of the parent manifest (job dicts unchanged)
        parent, kinds = SPLITS[camp]
        jobs = [j for j in make_manifest(parent)['jobs'] if j['kind'] in kinds]
        d = dict(campaign=camp, parent=parent, kinds=list(kinds), runner=RUNNER_VERSION,
                 created=time.strftime('%Y-%m-%d %H:%M'), jobs=jobs, note='plan §11 C1a/C1b sub-run of ' + parent)
        JOBS.mkdir(parents=True, exist_ok=True)
        (JOBS / f'{camp}.json').write_text(json.dumps(d, indent=1))
        return d
    jobs = []
    for (sample, ev0, nev, per, roads, rho) in PU_BLOCKS[camp]:
        for k, e0 in enumerate(range(ev0, ev0 + nev, per)):
            n = min(per, ev0 + nev - e0)
            chunk = e0 // per
            dump = ROAD_DUMP.get((sample, camp), 0)
            j = dict(id=f'{sample}_{chunk:05d}', campaign=camp, sample=sample, kind='pu', chunk=chunk, ev0=e0, n_events=n,
                     roads=roads, rho=rho, seed=hash_seed(f'stage4|{sample}|{chunk}'),
                     dump_events=max(0, min(n, dump - e0)) if dump else 0,
                     est_s=n * (rho * (PU_S if rho == 1 else PU_S_RHO2) + roads * (T1_S if rho == 1 else T2_S)), mem_gb=MEM_GB[sample[-2:]],
                     order=0 if rho == 1 else 1,
                     out=f'{camp}/{sample}/{sample}_{chunk:05d}.npz', requires='pu-chain')
            jobs.append(j)
    for (variant, src_sample, n_src_events, per) in DENS_BLOCKS.get(camp, []):
        for e0 in range(0, n_src_events, per):
            chunk = e0 // per
            src = f'{src_sample}_{chunk:05d}'
            jobs.append(dict(id=f'DENS{variant}_{chunk:05d}', campaign=camp, sample=f'DENS{variant}', kind='dens',
                             topup=variant, src_id=src, src_out=f'{camp}/{src_sample}/{src}.npz', chunk=chunk, ev0=e0,
                             n_events=per, roads=4, rho=1, seed=hash_seed(f'stage4|{src_sample}|{chunk}'),
                             dump_events=0, est_s=per * 4 * T1_S * 1.1, mem_gb=1.5, order=2,
                             needs=f'{camp}/{src_sample}/{src}.npz',
                             out=f'{camp}/DENS{variant}/DENS{variant}_{chunk:05d}.npz', requires='G1'))
    for (tag, smn, ev0, nev, per) in SM_BLOCKS.get(camp, []):
        for e0 in range(ev0, ev0 + nev, per):
            n = min(per, ev0 + nev - e0)
            chunk = e0 // per
            jobs.append(dict(id=f'{tag}_{chunk:05d}', campaign=camp, sample=tag, sm_sample=smn, kind='sm', chunk=chunk,
                             ev0=e0, n_events=n, roads=1, rho=1, seed=hash_seed(f'stage4|{tag}|{chunk}'), dump_events=0,
                             est_s=n * (PU_S + 0.5 + T1_S), mem_gb=1.5, order=1,
                             out=f'{camp}/{tag}/{tag}_{chunk:05d}.npz',
                             requires='G1'))
    from acts.stage4 import run_g1b as _G1B          # G1b kinds (HASH_ADDENDUM.md)
    g1b_jobs = _G1B.manifest_jobs(camp)
    jobs.extend(g1b_jobs)
    for name, desc, cpuh in G1_BLOCKS[camp]:
        if name == 'C' and SM_BLOCKS.get(camp):
            continue                      # replaced by the per-job SM manifest above
        if g1b_jobs and name in G1B_REPLACES:
            continue                      # replaced by the G1b per-job manifest
        jobs.append(dict(id=f'{camp}_{name}', campaign=camp, sample=name, kind='g1', description=desc,
                         est_s=cpuh * 3600, mem_gb=MEM_GB['G1'], out=f'{camp}/{name}/DONE.json', requires='G1'))
    d = dict(campaign=camp, runner=RUNNER_VERSION, created=time.strftime('%Y-%m-%d %H:%M'), jobs=jobs,
             note='plan §6.2 campaign content; PU-only jobs runnable now, requires=G1 jobs wait for run_chain.py')
    JOBS.mkdir(parents=True, exist_ok=True)
    (JOBS / f'{camp}.json').write_text(json.dumps(d, indent=1))
    return d


def load_jobs(camp):
    p = JOBS / f'{camp}.json'
    if not p.exists():
        make_manifest(camp)
    return json.loads(p.read_text())['jobs']


def out_path(job):
    return PROD.joinpath(*job['out'].split('/'))


def validate(job, deep=False):
    if job['kind'] in G1B_KINDS:
        from acts.stage4 import run_g1b as _G1B
        return _G1B.validate(job, deep)
    p = out_path(job)
    if job['kind'] == 'g1':
        return p.exists()
    if not p.is_file() or p.stat().st_size == 0:
        return False
    if not deep:
        return True
    try:
        with np.load(p, allow_pickle=False) as z:
            if str(z['job_id']) != job['id'] or int(z['complete']) != 1:
                return False
            if int(z['n_trials']) != job['n_events'] * job['roads'] or len(z['trials.n_loose']) != int(z['n_trials']):
                return False
        return True
    except Exception:
        return False


# ----------------------------------------------------------------------------------------------- worker side
def env_info():
    import numba
    return dict(platform=platform.platform(), hostname=socket.gethostname(), python=sys.version.split()[0],
                numpy=np.__version__, numba=numba.__version__)


def run_chain(job, tmp_npz, allow_interim):
    n_chain = job['n_events'] * job['rho']
    if CHAIN_PROD.exists():
        script = CHAIN_PROD
        args = ['pu', str(tmp_npz), str(n_chain), str(job['seed'])]
        if job['kind'] == 'sm':
            args = ['sm', str(tmp_npz), str(n_chain), str(job['seed']), '--sample', job['sm_sample']]
    else:
        if not allow_interim:
            raise RuntimeError('production chain acts/stage4/code/run_chain.py (gate G1) missing; '
                               'the interim chain is allowed only with --allow-interim (development)')
        script = CHAIN_INTERIM
        args = [str(tmp_npz), str(n_chain), str(job['seed'] % 900_000_000)]
    cmd = ['pixi', 'run', '--manifest-path', str(ACTS_MANIFEST), 'python', str(script)] + args
    t0 = time.time()
    p = subprocess.run(cmd, cwd=str(TT / 'acts'), capture_output=True, text=True)
    if p.returncode != 0 or not Path(tmp_npz).exists():
        raise RuntimeError(f'chain failed ({p.returncode}): {p.stderr[-3000:]}')
    return time.time() - t0, script.name


# B-9 density-normalisation variation (plan §1.4 'ratios at the lower and upper end of their ranges': IT cluster size
# 3 / 1.5 px vs the nominal 2; OT cluster size +-0.2 (PS 1.8, 2S 2.2) and +-5 % reading).  The TDR density scales as
# 1/cluster size, so ratio_var = ratio_nom x f, floored at 1 (G1 implementation of the plan text; flagged for review).
TOPUP_F = {'low': {'IT': 2.0 / 3.0, 'PS': (1.8 / 2.0) * 0.95, '2S': (2.2 / 2.4) * 0.95},
           'high': {'IT': 4.0 / 3.0, 'PS': (1.8 / 1.6) * 1.05, '2S': (2.2 / 2.0) * 1.05}}


def topup_ratios(variant):
    from acts.stage4.finder import pu_inputs as PI
    if variant in (None, 'nominal'):
        return None
    f = TOPUP_F[variant]
    kind = lambda n: 'IT' if n.startswith('TBPX') else ('PS' if n.startswith('TBPS') else '2S')  # noqa: E731
    return {n: max(1.0, r * f[kind(n)]) for n, r in PI.TOPUP.items()}


def dens_chain_from_dumps(job, tmp_chain):
    """Rebuild the G1 chain file of a C1 B1 job from its S6 dumps (pre-top-up chain output, barrel counting + BTL)."""
    src = PROD.joinpath(*job['src_out'].split('/'))
    t0 = time.time()
    out = {}
    with np.load(src, allow_pickle=False) as z:
        m = json.loads(str(z['meta_json']))
        cm = m['chain_meta']
        if not str(cm.get('chain', '')).startswith('g1'):
            raise RuntimeError('S6 dumps of %s are not from the G1 chain' % job['src_id'])
        for ie in range(job['n_events']):
            p = f'dump.{ie}_0.'
            n = len(z[p + 'sid'])
            ev = np.zeros((n, 13))
            ev[:, 0] = z[p + 'sid']; ev[:, 1:4] = z[p + 'xyz']; ev[:, 4:6] = z[p + 's01']; ev[:, 6] = z[p + 'flag']
            ev[:, 7] = z[p + 'vp']; ev[:, 8] = z[p + 'particle']; ev[:, 9] = z[p + 'gen']; ev[:, 10] = z[p + 'vsec']
            ev[:, 11] = z[p + 'dE']; ev[:, 12] = z[p + 't']
            out[f'ev{ie}'] = ev; out[f'tru{ie}'] = z[p + 'tru']; out[f'vz{ie}'] = z[p + 'vz'].astype(np.float64)
    meta = dict(cm, chain=cm['chain'], source='S6 dumps of ' + job['src_id'], v41_pass=cm.get('v41_pass'))
    np.savez(tmp_chain, meta=np.array(json.dumps(meta, default=str)), **out)
    return time.time() - t0


def finder_configs(fz, job, allow_interim):
    """Frozen finder + weight configuration (review WP_RULE R1 A-1): the road half-width delta_road = delta95 from
    frozen_inputs.json, identical in the hit road, the seeding and the fixed |dphi| cut.  Production campaigns refuse to
    run without the freeze; smoke/development runs use the planning value 0.25 rad and record frozen_inputs = null."""
    from acts.stage4.finder import finder as FF
    from acts.stage4.finder import production as PR
    if fz:
        cfg, wcfg = PR.config_from_frozen(fz)          # road = delta95, eta_max, mip_gev, finder_config (one helper)
        if abs(cfg.road - float(fz['delta95'])) > 1e-12 or abs(wcfg.eta_max - float(fz['eta_max'])) > 1e-12:
            raise RuntimeError('finder config does not match frozen_inputs.json (road/delta95/eta_max)')
    elif not (allow_interim or job['campaign'] in DEV_CAMPAIGNS):
        raise RuntimeError('frozen_inputs.json missing: production jobs need the frozen delta95/road, eta_max, mip_gev')
    else:      # development/smoke: the freeze CANDIDATE values if present (not frozen), else the planning values
        cand = TT / 'data' / 'acts_stage4' / 'frozen' / 'frozen_inputs.json'
        if cand.exists():
            cfg, wcfg = PR.config_from_frozen(json.loads(cand.read_text()))
        else:
            wcfg = PR.WCfg(); cfg = FF.Config(road=wcfg.delta95)
    return cfg, wcfg


def run_pu_job(job, allow_interim):
    import inspect
    from acts.stage4.finder import production as PR
    PT_PARAMS = inspect.signature(PR.process_trial).parameters
    from acts.stage4.finder import pu_inputs as PI
    from acts.stage4.finder import chain_inputs as CI
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    final = out_path(job)
    final.parent.mkdir(parents=True, exist_ok=True)
    tmp_chain = final.with_name(final.name[:-4] + f'.chain{os.getpid()}.npz')
    if job['kind'] == 'dens':      # B-9: rho = 1 re-run on the S6 dumps of a C1 B1 job, top-up at its low/high value
        t_chain, chain_name = dens_chain_from_dumps(job, tmp_chain), 'S6-dumps:' + job['src_id']
    else:
        t_chain, chain_name = run_chain(job, tmp_chain, allow_interim)
    z = np.load(tmp_chain)
    chain_meta = json.loads(str(z['meta']))
    g1 = str(chain_meta.get('chain', '')).startswith('g1')
    wcfg = PR.WCfg()
    fz = frozen_inputs()
    cfg, wcfg = finder_configs(fz, job, allow_interim)
    ss = np.random.SeedSequence(job['seed'])
    ev_streams = ss.spawn(job['n_events'])
    trials = []; cands = []; hitrec = []; btl = []; dumps = []; evstats = []
    rho = job['rho']
    for ie in range(job['n_events']):
        rs = np.random.default_rng(ev_streams[ie])
        parts = []
        for k in range(rho):
            ci = ie * rho + k
            if g1:      # G1 chain: exact interaction ids, top-up, CKF removal, U-5 b merging (finder/chain_inputs.py)
                parts.append(CI.prepare_event(z[f'ev{ci}'], z[f'tru{ci}'], z[f'vz{ci}'], k, rs,
                                              ratios=topup_ratios(job.get('topup', 'nominal'))))
                evstats.append([ie, k] + [parts[-1]['stats'][c] for c in EVSTAT_COLS])
            else:
                parts.append(PI.build_event(z[f'ev{ci}'], z[f'vz{ci}'], k, rs))
        H = np.concatenate([p_['H'] for p_ in parts]); sid = np.concatenate([p_['sid'] for p_ in parts])
        INT = np.concatenate([p_['INT'] for p_ in parts])
        uz = np.concatenate([p_['uz'] for p_ in parts])
        if job['kind'] == 'sm':
            # plan §1.7: PV = true hard-scatter vertex smeared by (10, 10, 15) um; MET = truth MET (neutrinos) smeared
            # per component with sigma_perp = 25 GeV; one road (a data event has one MET road)
            inf = chain_meta['ev_info'][ie]
            pv = np.array(inf['hs_vtx'][:3]) + rs.normal(0.0, 1.0, 3) * np.array([0.010, 0.010, 0.015])
            met = np.array(inf['hs_met']) + rs.normal(0.0, 25.0, 2)
            phi0 = float(np.arctan2(met[1], met[0]))
        else:
            pv = PI.lum_pv(rs)
            phi0 = rs.uniform(-np.pi, np.pi)
        dz = float(np.min(np.abs(uz - pv[2]))) if len(uz) else np.nan
        for k in range(rho):
            b = parts[k]['btl']
            btl.append(np.c_[np.full(len(b), ie), b[:, :6], b[:, 11:13], parts[k]['btl_INT']])
        if ie < job.get('dump_events', 0):
            # plan §4.1 step 1 (critical C-10): the event's chain output, pre-top-up (the top-up is regenerated from
            # the job seed: SeedSequence(seed).spawn(n_events)[ie]), barrel counting + BTL surfaces, typed columns
            for k in range(rho):
                ci = ie * rho + k
                e = z[f'ev{ci}']
                sd = e[:, 0].astype(np.int64)
                kp = (PI.FF.LC_OF[sd] >= 0) | (PI.KIND[sd] == 'BTL')
                e = e[kp]
                if g1:
                    dumps.append(dict(ev=ie, k=k, tru=z[f'tru{ci}'][kp].astype(np.float32),
                                      flag=e[:, 6].astype(np.int8)))
                dumps.append(dict(ev=ie, k=k, vz=z[f'vz{ci}'].astype(np.float32), sid=e[:, 0].astype(np.int16),
                                  xyz=e[:, 1:4].astype(np.float64), s01=e[:, 4:6].astype(np.float32),
                                  vp=e[:, 7].astype(np.int32), particle=e[:, 8].astype(np.int32),
                                  gen=e[:, 9].astype(np.int8), vsec=e[:, 10].astype(np.int32),
                                  dE=e[:, 11].astype(np.float32), t=e[:, 12].astype(np.float32)))
        for road in range(job['roads']):
            phimet = float((phi0 + road * 2 * np.pi / job['roads'] + np.pi) % (2 * np.pi) - np.pi)
            tseed = int(rs.integers(0, 2 ** 62))
            kw = {}
            if g1 and 'ckf' in PT_PARAMS:          # pre-removal CKF hits (f_CKF, review WP_RULE R1 B-6)
                kw['ckf'] = np.concatenate([p_['ckf'] for p_ in parts])
            if g1 and 'btl' in PT_PARAMS:          # BTL hits (G1 cols, t in ns, smeared 35 ps) + interaction ids (SR-T)
                kw['btl'] = (np.concatenate([p_['btl'] for p_ in parts]),
                             np.concatenate([p_['btl_INT'] for p_ in parts]))
                if rho > 1 and 'require_btl' in PT_PARAMS and job['campaign'] not in DEV_CAMPAIGNS:
                    kw['require_btl'] = True
            elif rho > 1 and job['campaign'] not in DEV_CAMPAIGNS:
                raise RuntimeError('rho > 1 production job needs process_trial(btl=...) (SR-T in-job columns, WP_RULE R2)')
            res = PR.process_trial(H, sid, INT, pv, phimet, float(rho), tseed, cfg=cfg, wcfg=wcfg, **kw)
            row = res['row']
            if 'road' in row:            # process_trial's road half-width (= delta95); 'road' below is the road index
                row['road_cfg'] = row['road']
            row.update(ev=job['ev0'] + ie, road=road, dz_nearest_pu=dz, trial_seed=tseed)
            ti = len(trials)
            trials.append(row)
            c = res['cand']; c['trial'] = np.full(len(c['idx']), ti, np.int32)
            if job['kind'] == 'sm':      # hard-scatter tagging (plan §4.2): HS hits (vp 3000) in each stored band
                hs = (INT % 1_000_000) == 3000
                c['n_hs_band'] = CI.ckf_band_counts(H[hs], pv, phimet, c['normal'], c['axis'], w_c=cfg.w_c,
                                                    road=cfg.road, t_tol=cfg.t_tol)
            if g1 and 'n_ckf_band' not in c:   # older process_trial without ckf=: same definition, computed here
                ck = np.concatenate([p_['ckf'] for p_ in parts])
                c['n_ckf_band'] = CI.ckf_band_counts(ck, pv, phimet, c['normal'], c['axis'], w_c=cfg.w_c, road=cfg.road,
                                                     t_tol=cfg.t_tol)
            cands.append(c)
            if res['hit'] is not None:
                hitrec.append((ti, res['hit']))
    v41 = z['v41'] if 'v41' in z.files else None
    ctim = z['timing'] if 'timing' in z.files else None
    z.close()
    tmp_chain.unlink()
    out = pack(job, trials, cands, hitrec, btl, dumps)
    if v41 is not None:
        out['chain.v41'] = v41
        out['chain.v41_cols'] = np.array(chain_meta['v41_cols'])
        out['chain.timing'] = ctim
        out['chain.timing_cols'] = np.array(chain_meta['timing_cols'])
    if evstats:
        out['chain.evstats'] = np.array(evstats, np.int64)
        out['chain.evstats_cols'] = np.array(['ev', 'k'] + EVSTAT_COLS)
    meta = dict(runner=RUNNER_VERSION, job=job, chain=chain_name, chain_meta=chain_meta, t_chain_s=t_chain,
                v41_pass=chain_meta.get('v41_pass'),
                code_sha256=code_hashes(), wcfg=vars(wcfg), finder_cfg=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol,
                                                                          tseed=cfg.tseed, iters=cfg.iters),
                frozen_inputs=fz, env=env_info(),
                created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                wall_s=time.perf_counter() - t_w0, cpu_s_tt=time.process_time() - t_c0, rungs=PR.RUNGS)
    out['meta_json'] = np.array(json.dumps(meta, default=str))
    tmp = final.with_name(final.name[:-4] + f'.tmp{os.getpid()}.npz')
    with open(tmp, 'wb') as f:
        np.savez_compressed(f, **out)
    os.replace(tmp, final)
    return dict(id=job['id'], wall=meta['wall_s'], est=job['est_s'], n_trials=len(trials), t_chain=t_chain,
                bytes=final.stat().st_size, v41_pass=chain_meta.get('v41_pass'))


def pack(job, trials, cands, hitrec, btl, dumps):
    out = dict(job_id=np.array(job['id']), complete=np.array(1), n_trials=np.array(len(trials)))
    scal = ['ev', 'road', 'rho', 'seed', 'trial_seed', 'phimet', 'dz_nearest_pu', 'n_road', 'n_trip', 'n_refit',
            'n_kept_all', 'n_loose', 'n_groups', 'n_ip2ge7', 'n_ip2ge6', 't_total']
    for k in scal:
        out['trials.' + k] = np.array([t[k] for t in trials])
    out['trials.pv'] = np.array([t['pv'] for t in trials])
    for k in ('n_pass', 'n_grp'):
        out['trials.' + k] = np.array([t[k] for t in trials], np.int64)
    tk = sorted(trials[0]['times'])
    out['trials.times'] = np.array([[t['times'].get(k, 0.0) for k in tk] for t in trials])
    out['trials.times_cols'] = np.array(tk)
    if job['rho'] > 1:
        for k in ('S_uni', 'S_ded', 'V_uni'):
            out['trials.' + k] = np.array([t[k] for t in trials])
        for k in ('n_is_groups', 'n_is_sets', 'is_zero_draw_frac', 'meanW_vs_dp', 'M_max', 'm_mean'):
            out['trials.' + k] = np.array([t[k] for t in trials])
    # per-trial keys the frozen rule needs (WP_RULE R2: SR-T in-job columns, run checks, config echo); each only if
    # process_trial produced it (trials[0]); a trial that lacks it (e.g. no candidate at rho > 1) gets NaN / -1.
    # 'road_cfg' = process_trial's row['road'] (the road half-width); trials.road stays the road index (0..roads-1)
    opt = ['n_pass_T', 'n_grp_T', 'n_btl', 'n_btl_int', 'n_btl_present', 'meanW_pull', 'n_aligned', 'road_cfg', 'delta95',
           'eta_max', 'mip_gev', 'n_ckf_hits']
    if job['rho'] > 1:
        opt += ['S_uni_T', 'S_ded_T', 'V_uni_T', 'meanW_pull_T']
    for k in opt:
        if k in trials[0]:
            ref = np.asarray(trials[0][k])
            fill = np.full(ref.shape, -1 if np.issubdtype(ref.dtype, np.integer) else np.nan, ref.dtype)
            out['trials.' + k] = np.array([np.asarray(t[k], ref.dtype) if k in t else fill for t in trials])
    for k in cands[0]:
        out['cand.' + k] = np.concatenate([c[k] for c in cands])
    if hitrec:
        hoff = 0; roff = 0
        acc = {}
        for ti, h in hitrec:
            acc.setdefault('trial', []).append(np.full(len(h['cand']), ti, np.int32))
            acc.setdefault('cand', []).append(h['cand'])
            acc.setdefault('off', []).append(h['off'][:-1].astype(np.int64) + roff)
            acc.setdefault('ref', []).append(h['ref'].astype(np.int64) + hoff)
            for k in ('xyz', 'sid', 's01', 'dE', 'INT', 'particle', 'gen', 't'):
                if k in h:
                    acc.setdefault(k, []).append(h[k])
            roff += len(h['ref']); hoff += len(h['xyz'])
        for k, v in acc.items():
            out['hit.' + k] = np.concatenate(v)
        out['hit.off'] = np.append(out['hit.off'], roff)
    if btl:
        out['btl'] = np.concatenate(btl).astype(np.float32)
        out['btl_cols'] = np.array(['ev', 'sid', 'x', 'y', 'z', 's0', 's1', 'dE', 't', 'INT'])
    for d in dumps:
        for k, v in d.items():
            if k not in ('ev', 'k'):
                out[f'dump.{d["ev"]}_{d["k"]}.{k}'] = v
    return out


def _worker_init(nice):
    if nice and hasattr(os, 'nice'):
        try:
            os.nice(nice)
        except OSError:
            pass
    os.environ.setdefault('OMP_NUM_THREADS', '1')


def _safe_run(job, allow_interim):
    try:
        if job['kind'] in G1B_KINDS:
            from acts.stage4 import run_g1b as _G1B
            return _G1B.run_job(job, allow_interim)
        return run_pu_job(job, allow_interim)
    except Exception:
        return dict(id=job['id'], error=traceback.format_exc())


# ----------------------------------------------------------------------------------------------- driver side
def warmup():
    from acts.stage4.finder import finder as FF, production as PR, trials as TR    # noqa: F401
    import acts.stage4.finder.weights  # noqa: F401


def cmd_manifest(a):
    for c in ('C1', 'C1a', 'C1b', 'C2', 'C2B', 'C4p', 'G3', 'smoke', 'smokeG1'):
        d = make_manifest(c)
        pu = [j for j in d['jobs'] if j['kind'] in RUNNABLE]; g1 = [j for j in d['jobs'] if j['kind'] == 'g1']
        print(f'{c}: {len(pu)} PU-only jobs ({sum(j["est_s"] for j in pu) / 3600:.1f} CPU-h), {len(g1)} G1-blocked '
              f'blocks ({sum(j["est_s"] for j in g1) / 3600:.1f} CPU-h)')
    return 0


def cmd_run(a):
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait
    camp = a.campaign
    out_dir = PROD / SPLITS.get(camp, (camp,))[0]
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in out_dir.rglob('*.tmp*.npz'):
        t.unlink(missing_ok=True)
    for t in out_dir.rglob('*.chain*.npz'):
        t.unlink(missing_ok=True)
    jobs = load_jobs(camp)
    blocked = [j for j in jobs if j['kind'] == 'g1']
    allow_interim = a.allow_interim or camp in DEV_CAMPAIGNS
    if not CHAIN_PROD.exists() and not allow_interim:
        print('[run_stage4] REFUSED: production chain acts/stage4/code/run_chain.py (gate G1) does not exist; '
              'use --allow-interim for development runs only.', flush=True)
        return 2
    fz = frozen_inputs()
    if camp not in DEV_CAMPAIGNS and not a.allow_interim:
        if fz is None:
            print('[run_stage4] REFUSED: WP_RULE.md is not frozen (acts/stage4/frozen_inputs.json missing or not frozen: '
                  'delta95, mip_gev, wp_rule_sha256).', flush=True)
            return 2
        if fz.get('wp_rule_sha256') != sha256_file(HERE / 'WP_RULE.md'):
            print('[run_stage4] REFUSED: WP_RULE.md changed after the freeze (sha256 mismatch).', flush=True)
            return 2
    todo = [j for j in jobs if j['kind'] in RUNNABLE and not validate(j, deep=True)]
    todo.sort(key=lambda j: (int(j.get('order', 0)), -float(j.get('est_s', 0.0))))
    if camp == 'C2B':      # orchestrator 2026-10-14 (C1_LAUNCH §4 option a): longest first regardless of rho, so B2
        todo.sort(key=lambda j: -float(j.get('est_s', 0.0)))     # (4 GB) and B1 share the memory budget; order only
    from acts.stage4.finder import production as PR_
    import inspect as _insp
    if camp not in DEV_CAMPAIGNS and 'btl' not in _insp.signature(PR_.process_trial).parameters:
        nb = [j for j in todo if j['rho'] > 1]
        if nb:
            print(f'[run_stage4] BLOCKED {len(nb)} rho > 1 jobs: process_trial has no btl= (SR-T in-job columns)',
                  flush=True)
        todo = [j for j in todo if j['rho'] == 1]
    if a.max_jobs:
        todo = todo[:a.max_jobs]
    host = socket.gethostname()
    prog = out_dir / f'_progress_{host}.jsonl'
    errlog = out_dir / f'_errors_{host}.log'
    stop = out_dir / 'STOP'
    print(f'[run_stage4] {camp} on {host}: {len(jobs)} jobs listed ({len(blocked)} blocked: need G1), '
          f'{len(todo)} PU-only jobs to run, {a.workers} workers, mem budget {a.mem_gb} GB; '
          f'est {sum(j["est_s"] for j in todo) / 3600:.1f} CPU-h; chain '
          f'{"run_chain.py" if CHAIN_PROD.exists() else "INTERIM"}', flush=True)
    with open(prog, 'a') as f:
        f.write(json.dumps(dict(event='start', campaign=camp, t=time.time(), workers=a.workers, n_todo=len(todo), env=env_info(),
                                code=code_hashes())) + '\n')
    if not todo:
        return 0
    warmup()
    n_ok = n_err = 0
    t0 = time.time()
    ctx = mp.get_context('spawn')
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=ctx, initializer=_worker_init, initargs=(a.nice,)) as ex:
        pending = list(todo)
        running = {}

        def submit_next():
            if stop.exists() or not pending:
                return False
            used = sum(j['mem_gb'] for j in running.values())
            for i, j in enumerate(pending):
                if j.get('needs') and not all(PROD.joinpath(*p_.split('/')).is_file() for p_ in
                                              ([j['needs']] if isinstance(j['needs'], str) else j['needs'])):
                    continue                     # dependency (B-9 source B1 file) not produced yet
                if len(running) < a.workers and used + j['mem_gb'] <= a.mem_gb:
                    pending.pop(i)
                    running[ex.submit(_safe_run, j, allow_interim)] = j
                    return True
            return False

        while submit_next():
            pass
        while running:
            done, _ = wait(list(running), return_when=FIRST_COMPLETED)
            for fu in done:
                running.pop(fu)
                r = fu.result()
                if 'error' in r:
                    n_err += 1
                    with open(errlog, 'a') as f:
                        f.write(f'--- {r["id"]} {time.strftime("%Y-%m-%d %H:%M:%S")}\n{r["error"]}\n')
                    print(f'[run_stage4] ERROR in {r["id"]} (see {errlog.name})', flush=True)
                else:
                    n_ok += 1
                    with open(prog, 'a') as f:
                        f.write(json.dumps(dict(event='done', t=time.time(), **r)) + '\n')
                    print(f'[run_stage4] {n_ok}/{len(todo)} done ({n_err} err), {r["id"]} {r["wall"]:.0f} s '
                          f'(chain {r["t_chain"]:.0f} s), elapsed {(time.time() - t0) / 3600:.2f} h', flush=True)
            while submit_next():
                pass
        if pending and not stop.exists():
            print(f'[run_stage4] {len(pending)} jobs left pending: their dependency (needs=) does not exist yet',
                  flush=True)
    with open(prog, 'a') as f:
        f.write(json.dumps(dict(event='end', campaign=camp, t=time.time(), n_ok=n_ok, n_err=n_err, stopped=stop.exists())) + '\n')
    print(f'[run_stage4] finished: {n_ok} ok, {n_err} errors, {(time.time() - t0) / 3600:.2f} h'
          + (' (STOP file present)' if stop.exists() else ''), flush=True)
    return 1 if n_err else 0


def cmd_status(a):
    camp = a.campaign
    out_dir = PROD / SPLITS.get(camp, (camp,))[0]
    jobs = load_jobs(camp)
    pu = [j for j in jobs if j['kind'] in RUNNABLE]; g1 = [j for j in jobs if j['kind'] == 'g1']
    done = [j for j in pu if validate(j, deep=a.deep)]
    est_tot = sum(j['est_s'] for j in pu); est_done = sum(j['est_s'] for j in done)
    print(f'{camp}: PU-only jobs {len(done)}/{len(pu)} done; est work {est_done / 3600:.1f}/{est_tot / 3600:.1f} CPU-h '
          f'(G3-timed per-worker s under load).  Blocked (need G1 run_chain.py): {len(g1)} blocks, {sum(j["est_s"] for j in g1) / 3600:.1f} CPU-h'
          + ('' if not CHAIN_PROD.exists() else ' [run_chain.py present]'))
    recs = []; starts = []
    ids = {j['id'] for j in jobs}
    for p in out_dir.glob('_progress_*.jsonl'):
        for line in open(p):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('event') == 'done' and d['id'] in ids:
                recs.append(d)
            elif d.get('event') == 'start' and (camp not in SPLITS or d.get('campaign') == camp):
                starts.append(d)
    if starts:
        st = max(starts, key=lambda d: d['t'])
        recent = [r for r in recs if r['t'] >= st['t']]
        el = time.time() - st['t']
        print(f'current run: started {time.strftime("%Y-%m-%d %H:%M", time.localtime(st["t"]))} ({el / 3600:.2f} h ago), '
              f'{st["workers"]} workers, {len(recent)} jobs finished since')
        if recent and el > 0:
            rate = sum(r['est'] for r in recent) / el
            act = sum(r['wall'] for r in recent); estr = sum(r['est'] for r in recent)
            print(f'throughput {rate:.2f} est-CPU-s per wall s; job wall/estimate {act / max(estr, 1e-9):.2f}; '
                  f'disk {sum(r.get("bytes", 0) for r in recs) / 1e9:.2f} GB so far')
            rem = est_tot - est_done
            if rate > 0:
                eta = rem / rate
                print(f'ETA {eta / 3600:.1f} h (finish ~ {time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() + eta))})')
    errs = list(out_dir.glob('_errors_*.log'))
    if errs:
        n = sum(open(p).read().count('--- ') for p in errs)
        print(f'errors logged: {n} ({", ".join(p.name for p in errs)})')
    if (out_dir / 'STOP').exists():
        print('STOP file present: no new jobs will start')
    return 0


def cmd_check(a):
    jobs = [j for j in load_jobs(a.campaign) if j['kind'] in RUNNABLE]
    bad = [j['id'] for j in jobs if out_path(j).exists() and not validate(j, deep=True)]
    missing = [j['id'] for j in jobs if not out_path(j).exists()]
    v41_fail = []
    for j in jobs:
        if out_path(j).exists() and j['id'] not in bad:
            with np.load(out_path(j)) as z:
                if json.loads(str(z['meta_json'])).get('v41_pass') is False:
                    v41_fail.append(j['id'])
    print(f'{len(jobs)} PU-only jobs: {len(jobs) - len(bad) - len(missing)} valid, {len(bad)} invalid, {len(missing)} missing; '
          f'V4-1 failures: {len(v41_fail)}')
    v410_fail = []
    for j in jobs:
        if j['kind'] in ('cp0', 'cppu') and out_path(j).exists() and j['id'] not in bad:
            from acts.stage4 import run_g1b as _G1B
            if _G1B.check_job(j).get('v410_pass') is False:
                v410_fail.append(j['id'])
    if any(j['kind'] in ('cp0', 'cppu') for j in jobs):
        print(f'V4-10 failures (C\'0 leak / C\'_PU hash): {len(v410_fail)}')
        for b in v410_fail[:20]:
            print('  V4-10 FAIL:', b)
        bad = bad + v410_fail
    for b in bad[:20]:
        print('  invalid:', b)
    for b in v41_fail[:20]:
        print('  V4-1 FAIL:', b)
    return 1 if (bad or v41_fail) else 0


def cmd_smoke(a):
    a.campaign = 'smoke'
    make_manifest('smoke')
    t0 = time.time()
    rc = cmd_run(a)
    jobs = [j for j in load_jobs('smoke') if j['kind'] == 'pu']
    ok = all(validate(j, deep=True) for j in jobs)
    from acts.stage4.finder.production import RUNGS
    for j in jobs:
        if not out_path(j).exists():
            continue
        with np.load(out_path(j)) as z:
            m = json.loads(str(z['meta_json']))
            npass = z['trials.n_pass']
            line = (f'  {j["id"]}: {int(z["n_trials"])} trials, n_loose {z["trials.n_loose"].tolist()}, '
                    f'N_pass R04 {npass[:, 3].tolist()}, R05 {npass[:, 4].tolist()}, stored cands {len(z["cand.idx"])}, '
                    f'hit refs {len(z["hit.ref"]) if "hit.ref" in z.files else 0}, file {out_path(j).stat().st_size / 1e6:.2f} MB, '
                    f'chain {m["chain"]} {m["t_chain_s"]:.0f} s, wall {m["wall_s"]:.0f} s')
            if j['rho'] > 1:
                S = z['trials.S_uni']
                line += f', S_uni R04 {np.round(S[:, 3], 2).tolist()} R05 {np.round(S[:, 4], 3).tolist()}'
            print(line)
    print(f'SMOKE {"PASS" if (ok and rc == 0) else "FAIL"} in {time.time() - t0:.0f} s (rungs: {len(RUNGS)})')
    return 0 if (ok and rc == 0) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('manifest', 'run', 'status', 'smoke', 'check'):
        p = sub.add_parser(name)
        p.add_argument('--campaign', default='C1', choices=['C1', 'C1a', 'C1b', 'C2', 'C2B', 'C4p', 'G3', 'smoke', 'smokeG1'])
        p.add_argument('--workers', type=int, default=7)
        p.add_argument('--mem-gb', type=float, default=19.0, help='sum of job memory estimates allowed at once')
        p.add_argument('--max-jobs', type=int, default=0)
        p.add_argument('--nice', type=int, default=10)
        p.add_argument('--deep', action='store_true')
        p.add_argument('--allow-interim', action='store_true', help='development only: run PU jobs on the interim chain')
    a = ap.parse_args(argv)
    return dict(manifest=cmd_manifest, run=cmd_run, status=cmd_status, smoke=cmd_smoke, check=cmd_check)[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
