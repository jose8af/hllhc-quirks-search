"""run_stage3.py -- Stage-3 job runner (C001 quirks theory track; E7, 2026-10-11).  Pure Python + numpy + numba; runs the
same way on macOS (osx-arm64) and Windows (win-64).

One job = one (point, configuration, chunk of events); it writes ONE npz, atomically (tmp file, then os.replace).
A rerun skips every job whose output exists and validates, so stopping and restarting is always safe.

Commands (paths default to the bundle layout: <root>/code (this file), <root>/inputs, <root>/jobs, <root>/out):
  python run_stage3.py run    --jobs JOBS.json [JOBS2.json ...] --workers N [--inputs DIR] [--out DIR] [--max-jobs K]
  python run_stage3.py status --jobs JOBS.json [...] [--out DIR] [--deep]     done/total, CPU-h, ETA
  python run_stage3.py smoke  [--inputs DIR] [--out DIR]                      ~2 min end-to-end test (jobs/smoke.json)
  python run_stage3.py check  --jobs JOBS.json [...] [--out DIR]               validate every output file (slow)
Graceful stop: create the file <out>/STOP (no new jobs start; running jobs finish).  Hard stop: kill the processes;
partial outputs are only *.tmp*.npz files, removed at the next start.

Determinism: each event's kernel seed = blake2b("spin|m|row|lam|cfg") (independent of chunking, worker and machine);
the job seed blake2b(job id) is recorded.  numba caches go to NUMBA_CACHE_DIR = <root>/.numba_cache (set below, before
numba is imported).  Units in the output: mm, ns, GeV (ACTS conventions); thickness observables in micrometres.
Every output stores the code md5s, platform, hostname, numba/numpy versions and wall/CPU time.
"""
import argparse
import hashlib
import json
import os
import platform
import socket
import sys
import time
import traceback
from pathlib import Path

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
os.environ.setdefault('NUMBA_CACHE_DIR', str(ROOT / '.numba_cache'))
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
sys.dont_write_bytecode = True
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

import numpy as np  # noqa: E402

RUNNER_VERSION = 'r1.0'
B0 = 3.8112
C_CM_PER_NS = 29.9792458
# configuration name -> kernel settings (max_boost, vertex and recorder are per job)
CONFIGS = {
    'V': dict(B0=0.0, material=False),
    'B': dict(B0=B0, material=False),
    'B2': dict(B0=B0 / 2, material=False),
    'M': dict(B0=0.0, material=True),
    'BM': dict(B0=B0, material=True),
    'Mx0.5': dict(B0=0.0, material=True, mat_scale=0.5),
    'Mx2': dict(B0=0.0, material=True, mat_scale=2.0),
    'BMx0.5': dict(B0=B0, material=True, mat_scale=0.5),
    'BMx2': dict(B0=B0, material=True, mat_scale=2.0),
    'BE': dict(B0=B0, material=True, ms=False, strag=False),      # validation only (deterministic dE/dx)
    'BK': dict(B0=B0, material=False),                            # validation only (one deterministic 3 MeV kick)
}


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def hash_seed(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') & 0x7FFFFFFF


def event_seed(spin, m, row, lam, cfg):
    return hash_seed(f'{spin}|{int(m)}|{int(row)}|{float(lam):g}|{cfg}')


def load_jobs(paths):
    jobs = []
    seen = set()
    for p in paths:
        d = json.load(open(p))
        for j in d['jobs']:
            if j['id'] in seen:
                continue
            seen.add(j['id'])
            jobs.append(j)
    return jobs


def out_path(out_dir, job):
    return Path(out_dir).joinpath(*job['out'].split('/'))


def validate_output(path, job, deep=False):
    """True if the file exists, carries this job id, is complete and has the expected number of events."""
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        return False
    if not deep:
        return True
    try:
        with np.load(path, allow_pickle=False) as z:
            if str(z['job_id']) != job['id'] or int(z['complete']) != 1:
                return False
            if int(z['n_events']) != len(job['ev']) or len(z['hit_offsets']) != len(job['ev']) + 1:
                return False
            if int(z['hit_offsets'][-1]) != len(z['h_x']):
                return False
        return True
    except Exception:
        return False


# ------------------------------------------------------------------------------------------------ worker side
_INPUT_CACHE = {}
_MD5_CACHE = {}


def _input(inputs_dir, name):
    key = str(Path(inputs_dir) / name)
    if key not in _INPUT_CACHE:
        with np.load(key, allow_pickle=False) as z:
            _INPUT_CACHE[key] = {k: z[k] for k in z.files}
        _MD5_CACHE[key] = md5_file(key)
    return _INPUT_CACHE[key], _MD5_CACHE[key]


def code_md5s():
    if 'code' not in _MD5_CACHE:
        _MD5_CACHE['code'] = {n: md5_file(CODE / n) for n in ('T3_causal_s3.py', 's3_physics.py', 'run_stage3.py', 'surfaces_s3.json')}
    return _MD5_CACHE['code']


def env_info():
    import numba
    return dict(platform=platform.platform(), machine=platform.machine(), hostname=socket.gethostname(),
                python=sys.version.split()[0], numpy=np.__version__, numba=numba.__version__,
                processor=platform.processor())


def _worker_init(low_priority):
    if low_priority and os.name == 'nt':
        try:
            import ctypes
            k32 = ctypes.windll.kernel32
            k32.SetPriorityClass(k32.GetCurrentProcess(), 0x00004000)     # BELOW_NORMAL_PRIORITY_CLASS
        except Exception:
            pass


def run_job(job, inputs_dir, out_dir):
    """Run one job and write its npz atomically.  Returns a small summary dict."""
    from T3_causal_s3 import run_causal_s3, load_surfaces, KERNEL_VERSION, ORIG_MD5
    from s3_physics import pair_truth, plane_fit, dE_sensor
    t_wall0 = time.perf_counter(); t_cpu0 = time.process_time()
    final = out_path(out_dir, job)
    final.parent.mkdir(parents=True, exist_ok=True)
    inp, inp_md5 = _input(inputs_dir, job['input'])
    S = load_surfaces()
    surf = S['surf']; kinds = np.array(S['kinds']); nsurf = len(surf)
    is_t3v = np.where(kinds == 'T3V')[0]
    is_trk = np.where(np.isin(kinds, ['IT', 'PS', '2S']))[0]
    is_itps = np.where(np.isin(kinds, ['IT', 'PS']))[0]
    cfgname = job['cfg']
    kw = dict(CONFIGS[cfgname])
    lam = float(job['lam']); m = float(job['m']); spin = job['spin']
    mb = float(job['max_boost']); hmax = float(job.get('hmax', 0.2))
    ev = np.asarray(job['ev'], int)
    n = len(ev)
    Btruth = kw['B0'] if kw['B0'] != 0.0 else B0
    # per-event outputs
    E = {k: np.zeros(n) for k in ('gstar', 'x', 'ell_max', 'N_osc_vac', 'eps_B', 'eps_perp', 'bodd_l0', 'k_B', 'c_ev',
                                  'C_ev', 'ds_barrel_um', 'ds_all_um', 'ds_itps_um', 'res_max_um', 'cpu_s', 'wall_s')}
    status = np.zeros(n, np.int8); nsteps = np.zeros(n, np.int64); maxq = np.zeros(n, np.int64); seeds = np.zeros(n, np.int64)
    floor_flag = np.zeros(n, bool); rerun = np.zeros(n, np.int8); swapped = np.zeros(n, bool)
    X_end = np.zeros((n, 2, 4)); P_end = np.zeros((n, 2, 4)); eacc = np.zeros((n, 2)); n_plane = np.zeros((n, 3))
    vtx = np.zeros((n, 4)); nhit_surf = np.zeros((n, nsurf, 2), np.int16)
    H = []; offs = [0]
    for i, k in enumerate(ev):
        p1 = inp['p_qp'][k]; p2 = inp['p_qm'][k]; row = int(inp['row'][k])
        seed = event_seed(spin, m, row, lam, cfgname); seeds[i] = seed
        if job['vertex'] == 'lumi':
            v = inp['vtx_lumi'][k]                       # (x, y, z, t) mm, ns
            vtx[i] = v
            x0 = np.array([v[3] * C_CM_PER_NS, v[0] / 10.0, v[1] / 10.0, v[2] / 10.0])
        else:
            x0 = np.zeros(4)
        kick = None
        if cfgname == 'BK':
            u = np.cross(p1, [0.0, 0.0, 1.0]); u /= np.linalg.norm(u)
            kick = (0, 3.0, 3e-3 * u)
        tw = time.perf_counter(); tc = time.process_time()
        r = run_causal_s3(p1, p2, m, lam, max_boost=mb, hmax_trk=hmax, seed=seed, vertex=x0, kick=kick, **kw)
        if r['status'] in (3, 5):
            # queue overflow / step cap: rerun once with x4 caps (plan §6.3, V7)
            r = run_causal_s3(p1, p2, m, lam, max_boost=mb, hmax_trk=hmax, seed=seed, vertex=x0, kick=kick,
                              qcap=(1 << 21), max_steps=80_000_000_000, **kw)
            rerun[i] = 1
        E['cpu_s'][i] = time.process_time() - tc; E['wall_s'][i] = time.perf_counter() - tw
        h = r['hits']
        status[i] = r['status']; nsteps[i] = r['nsteps']; maxq[i] = r['maxq']; swapped[i] = r['swapped']
        X_end[i] = r['X']; P_end[i] = r['P']; eacc[i] = r['eacc']
        tr = pair_truth(p1, p2, m, lam, B=Btruth)
        for key in ('gstar', 'x', 'ell_max', 'N_osc_vac', 'eps_B', 'eps_perp', 'bodd_l0', 'k_B', 'c_ev', 'C_ev'):
            E[key][i] = tr[key]
        floor_flag[i] = tr['floor_flag']
        L = h[:, 1].astype(int) if len(h) else np.zeros(0, int)
        org = x0[1:]
        pos = h[:, 4:7] if len(h) else np.zeros((0, 3))
        d, _, _ = plane_fit(pos[np.isin(L, is_t3v)], org)
        E['ds_barrel_um'][i] = d * 1e4
        d, nrm, rmax = plane_fit(pos[np.isin(L, is_trk)], org)
        E['ds_all_um'][i] = d * 1e4; E['res_max_um'][i] = rmax * 1e4; n_plane[i] = nrm
        d, _, _ = plane_fit(pos[np.isin(L, is_itps)], org)
        E['ds_itps_um'][i] = d * 1e4
        if len(h):
            np.add.at(nhit_surf[i], (L, h[:, 0].astype(int)), 1)
            dE = dE_sensor(h, surf, S['t_sens'], m)
            hh = np.empty((len(h), 13))
            hh[:, :3] = h[:, :3]
            hh[:, 3] = h[:, 3] / C_CM_PER_NS
            hh[:, 4:7] = h[:, 4:7] * 10.0
            hh[:, 7:11] = h[:, 7:11]
            hh[:, 11] = dE
            hh[:, 12] = h[:, 11] * 10.0
            H.append(hh)
        offs.append(offs[-1] + len(h))
    HH = np.concatenate(H) if H else np.zeros((0, 13))
    wall = time.perf_counter() - t_wall0; cpu = time.process_time() - t_cpu0
    meta = dict(kernel_version=KERNEL_VERSION, runner_version=RUNNER_VERSION, code_md5=code_md5s(), orig_md5=ORIG_MD5,
                input=job['input'], input_md5=inp_md5, stage2_source=str(inp['source_file']),
                stage2_source_md5=str(inp['source_md5']), selection=json.loads(str(inp['selection_json'])),
                config=dict(name=cfgname, **{k: v for k, v in kw.items()}, max_boost=mb, hmax_trk=hmax, hmax_out=2.0,
                            vertex=job['vertex'], qcap=1 << 19, max_steps=20_000_000_000, r_exit=118.0, z_exit=293.0,
                            first_length=1e-7, disc_material=True, recorder='s3 all-roots surfaces'),
                seed_rule='event seed = blake2b("spin|m|row|lam|cfg") & 0x7fffffff (8-byte digest, little endian)',
                job_seed=hash_seed(job['id']), env=env_info(), created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                wall_s=wall, cpu_s=cpu, units=dict(length='mm', time='ns', momentum='GeV', thickness='um'),
                hit_columns=['quirk', 'surf', 'icross', 't', 'x', 'y', 'z', 'px', 'py', 'pz', 'E', 'dE_sensor', 'dl'])
    out = dict(
        job_id=np.array(job['id']), complete=np.array(1), n_events=np.array(n), meta_json=np.array(json.dumps(meta)),
        job_json=np.array(json.dumps(job)), kernel_version=np.array(KERNEL_VERSION), spin=np.array(spin), m=np.array(m),
        lam_keV=np.array(lam), cfg=np.array(cfgname), max_boost=np.array(mb), chunk=np.array(int(job['chunk'])),
        sigma_norm_fb=inp['sigma_norm_fb'], sigma_ref_fb=inp['sigma_ref_fb'], w_max=inp['w_max'],
        surf_table=surf, surf_names=np.array(S['names']), surf_kinds=kinds,
        wvar_names=inp['wvar_names'],
        # per event (Stage-2 provenance and weights)
        ev_index=ev, row=inp['row'][ev], src_chunk=inp['chunk'][ev], ievt_lhe=inp['ievt_lhe'][ev], py8_seed=inp['py8_seed'][ev],
        tt_split=inp['tt_split'][ev], in_eta25=inp['in_eta25'][ev], w=np.full(n, float(inp['w_max'])), w_orig=inp['w_orig'][ev],
        wvar_ratio=inp['wvar_ratio'][ev], w_lmax_up=inp['w_lmax_up'][ev], w_lmax_dn=inp['w_lmax_dn'][ev],
        w_qed=inp['w_qed'][ev], w_qed_19=inp['w_qed_19'][ev],
        p_qp=inp['p_qp'][ev], p_qm=inp['p_qm'][ev], recoil=inp['recoil'][ev], jets=inp['jets'][ev],
        cstar=inp['cstar'][ev], pt=inp['pt'][ev], eta=inp['eta'][ev], M=inp['M'][ev],
        vtx=vtx, seed=seeds, status=status, nsteps=nsteps, maxq=maxq, rerun=rerun, swapped=swapped,
        X_end=X_end, P_end=P_end, eacc=eacc, n_plane=n_plane, nhit_surf=nhit_surf, floor_flag=floor_flag,
        hit_offsets=np.asarray(offs, np.int64),
        h_quirk=HH[:, 0].astype(np.int8), h_surf=HH[:, 1].astype(np.int16), h_icross=HH[:, 2].astype(np.int32),
        h_t=HH[:, 3], h_x=HH[:, 4], h_y=HH[:, 5], h_z=HH[:, 6], h_px=HH[:, 7], h_py=HH[:, 8], h_pz=HH[:, 9], h_E=HH[:, 10],
        h_dE=HH[:, 11].astype(np.float32), h_dl=HH[:, 12].astype(np.float32),
        **{k: v for k, v in E.items()})
    tmp = final.with_name(final.name[:-4] + f'.tmp{os.getpid()}.npz')
    with open(tmp, 'wb') as f:
        np.savez_compressed(f, **out)
    for attempt in range(10):          # Windows: a virus scanner may hold the fresh file for a moment
        try:
            os.replace(tmp, final)
            break
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(1.0 + attempt)
    return dict(id=job['id'], wall=wall, cpu=cpu, n=n, est=float(job.get('est_s', 0.0)),
                nstat=int(np.sum(status > 1)), host=socket.gethostname())


def _safe_run(job, inputs_dir, out_dir):
    try:
        return run_job(job, inputs_dir, out_dir)
    except Exception:
        return dict(id=job['id'], error=traceback.format_exc())


# ------------------------------------------------------------------------------------------------ driver side
def warmup():
    """Compile / load the numba kernel once in the main process (both recorder modes are the same function)."""
    from T3_causal_s3 import run_causal_s3
    p1 = np.array([200.0, 300.0, 30.0]); p2 = np.array([-100.0, 280.0, -20.0])
    run_causal_s3(p1, p2, 500.0, 3.0, material=True)


def cmd_run(a):
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait
    out_dir = Path(a.out); inputs_dir = Path(a.inputs)
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in out_dir.rglob('*.tmp*.npz'):
        try:
            t.unlink()
        except OSError:
            pass
    jobs = load_jobs(a.jobs)
    todo = [j for j in jobs if not validate_output(out_path(out_dir, j), j, deep=True)]
    todo.sort(key=lambda j: -float(j.get('est_s', 0.0)))
    if a.max_jobs:
        todo = todo[:a.max_jobs]
    host = socket.gethostname()
    prog = out_dir / f'_progress_{host}.jsonl'
    errlog = out_dir / f'_errors_{host}.log'
    stop = out_dir / 'STOP'
    print(f'[run_stage3] host {host}: {len(jobs)} jobs listed, {len(jobs) - len(todo)} already done, {len(todo)} to run, '
          f'{a.workers} workers; est {sum(float(j.get("est_s", 0)) for j in todo) / 3600:.1f} CPU-h (Mac-M3 units)', flush=True)
    with open(prog, 'a') as f:
        f.write(json.dumps(dict(event='start', t=time.time(), workers=a.workers, n_todo=len(todo), jobs=a.jobs,
                                env=env_info())) + '\n')
    if not todo:
        return 0
    warmup()
    n_ok = n_err = 0
    t0 = time.time()
    ctx = mp.get_context('spawn')
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=ctx, initializer=_worker_init,
                             initargs=(a.low_priority,)) as ex:
        it = iter(todo)
        running = set()

        def submit_next():
            if stop.exists():
                return False
            j = next(it, None)
            if j is None:
                return False
            running.add(ex.submit(_safe_run, j, str(inputs_dir), str(out_dir)))
            return True

        for _ in range(2 * a.workers):
            if not submit_next():
                break
        while running:
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for fu in done:
                running.discard(fu)
                r = fu.result()
                if 'error' in r:
                    n_err += 1
                    with open(errlog, 'a') as f:
                        f.write(f'--- {r["id"]} {time.strftime("%Y-%m-%d %H:%M:%S")}\n{r["error"]}\n')
                    print(f'[run_stage3] ERROR in {r["id"]} (see {errlog.name})', flush=True)
                else:
                    n_ok += 1
                    with open(prog, 'a') as f:
                        f.write(json.dumps(dict(event='done', t=time.time(), **r)) + '\n')
                    if n_ok % 25 == 0 or r['wall'] > 600:
                        print(f'[run_stage3] {n_ok}/{len(todo)} done ({n_err} errors), last {r["id"]} {r["wall"]:.0f} s, '
                              f'elapsed {(time.time() - t0) / 3600:.2f} h', flush=True)
                submit_next()
    with open(prog, 'a') as f:
        f.write(json.dumps(dict(event='end', t=time.time(), n_ok=n_ok, n_err=n_err, stopped=stop.exists())) + '\n')
    print(f'[run_stage3] finished: {n_ok} ok, {n_err} errors, {(time.time() - t0) / 3600:.2f} h'
          + (' (STOP file present)' if stop.exists() else ''), flush=True)
    return 1 if n_err else 0


def cmd_status(a):
    out_dir = Path(a.out)
    jobs = load_jobs(a.jobs)
    done = [j for j in jobs if validate_output(out_path(out_dir, j), j, deep=a.deep)]
    est_tot = sum(float(j.get('est_s', 0)) for j in jobs); est_done = sum(float(j.get('est_s', 0)) for j in done)
    print(f'jobs: {len(done)}/{len(jobs)} done ({100 * len(done) / max(len(jobs), 1):.1f} %); '
          f'estimated work {est_done / 3600:.1f}/{est_tot / 3600:.1f} CPU-h (Mac-M3 units, {100 * est_done / max(est_tot, 1):.1f} %)')
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
            elif d.get('event') == 'start':
                starts.append(d)
    if starts:
        st = starts[-1]
        t_start = st['t']
        recent = [r for r in recs if r['t'] >= t_start]
        el = time.time() - t_start
        print(f'current run: started {time.strftime("%Y-%m-%d %H:%M", time.localtime(t_start))}, {el / 3600:.2f} h ago, '
              f'{st["workers"]} workers, {len(recent)} jobs finished since')
        if recent and el > 0:
            est_rate = sum(r['est'] for r in recent) / el           # Mac-M3 CPU-s of work per wall second
            act = sum(r['wall'] for r in recent); estr = sum(r['est'] for r in recent)
            rem = est_tot - est_done
            print(f'throughput: {est_rate:.2f} M3-CPU-s per wall s (job wall/estimate = {act / max(estr, 1e-9):.2f} per worker)')
            if est_rate > 0:
                eta = rem / est_rate
                print(f'ETA: {eta / 3600:.1f} h  (finish ~ {time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() + eta))}); '
                      f'early ETAs are pessimistic/optimistic because the expensive jobs run first')
    errs = list(out_dir.glob('_errors_*.log'))
    if errs:
        n = sum(open(p).read().count('\n--- ') + open(p).read().startswith('--- ') for p in errs)
        print(f'errors logged: {n} (files: {", ".join(p.name for p in errs)})')
    if (out_dir / 'STOP').exists():
        print('STOP file present: no new jobs will start')
    return 0


def cmd_check(a):
    out_dir = Path(a.out)
    jobs = load_jobs(a.jobs)
    bad = [j['id'] for j in jobs if out_path(out_dir, j).exists() and not validate_output(out_path(out_dir, j), j, deep=True)]
    missing = [j['id'] for j in jobs if not out_path(out_dir, j).exists()]
    print(f'{len(jobs)} jobs: {len(jobs) - len(bad) - len(missing)} valid, {len(bad)} invalid, {len(missing)} missing')
    for b in bad[:20]:
        print('  invalid:', b)
    return 1 if bad else 0


def cmd_smoke(a):
    a.jobs = [str(ROOT / 'jobs' / 'smoke.json')]
    a.out = str(Path(a.out) / '_smoke')
    a.max_jobs = 0; a.deep = True
    t0 = time.time()
    rc = cmd_run(a)
    jobs = load_jobs(a.jobs)
    ok = all(validate_output(out_path(a.out, j), j, deep=True) for j in jobs)
    for j in jobs:
        with np.load(out_path(a.out, j)) as z:
            print(f'  {j["id"]}: {int(z["n_events"])} events, {len(z["h_x"])} hits, status {np.bincount(z["status"]).tolist()}, '
                  f'median ds_all {np.nanmedian(z["ds_all_um"]):.2f} um, wall {json.loads(str(z["meta_json"]))["wall_s"]:.1f} s')
    print(f'SMOKE {"PASS" if (ok and rc == 0) else "FAIL"} in {time.time() - t0:.0f} s (includes numba compilation)')
    return 0 if (ok and rc == 0) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('run', 'status', 'smoke', 'check'):
        p = sub.add_parser(name)
        p.add_argument('--jobs', nargs='+', default=[])
        p.add_argument('--workers', type=int, default=max(1, (os.cpu_count() or 2) - 1))
        p.add_argument('--inputs', default=str(ROOT / 'inputs'))
        p.add_argument('--out', default=str(ROOT / 'out'))
        p.add_argument('--max-jobs', type=int, default=0)
        p.add_argument('--deep', action='store_true', help='open every output to validate it (slower)')
        p.add_argument('--low-priority', action='store_true', help='Windows: run workers at below-normal priority')
    a = ap.parse_args(argv)
    return dict(run=cmd_run, status=cmd_status, smoke=cmd_smoke, check=cmd_check)[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
