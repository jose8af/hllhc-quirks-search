"""p3a_multi.py -- several variants of the final classification from ONE read of each Z(nunu) pilot file.
Aurora, 2026-11-24.  Reason: the jobs of p3-a-cls-m were NFS-bound (wall 3.6 x CPU; AGENT_RULES "never let many jobs
stream the same multi-GB file"); the variants u, pv0, m0, pv2 and the independent search would each have read the 77 GB
of Z(nunu) pilot files again.

  <tt python> p3a_multi.py --id ID --outdir /ABS/DIR --manifest m.json --all-z z_all.json
              [--variants m,u,pv0,m0,pv2,ind] [--max-events N]

Per file and variant, the per-event work is p3a_subset.classify_pool UNCHANGED (imported; p3a_subset.py is not
edited) with the options (B1 / hs / lowpt files: m and u only)
  m    merged pool, PV draw, w_v1 > 0              (= p3a_subset.py with its defaults = the Phase-2 configuration)
  u    pool not merged, PV draw, w_v1 > 0          (= p3a_subset.py --no-merge)
  pv0  merged, PV = true vertex, w_v1 > 0          (= --pv true)
  m0   merged, PV draw, w_v1 = 0 only              (= --w-select zero)
  pv2  merged, other PV seed string, w_v1 > 0, only files with global index % 4 == 0   (= --pv draw2)
  ind  Nils's search on the counted events (p3a_indep.classify unchanged), only files with global index % 2 == 0
  v2   as m, but with the per-event preselection weight AND the MET azimuth (road axis) of another MET model, read
       from --met-dir/<pilot file stem>.met.npz (arrays 'w' and 'phimet', one entry per event of the pilot file).
       INTERFACE FOR THE BINDING RUN (ADD l.360, l.607: the v1 preselection is replaced by the day-12 MET model);
       not run by p3-a.  With w = w_v1 and phimet = phimet_reco_v1 it must reproduce variant m (tested).
The file loop of p3a_subset.main is copied below (function do_variant) with the options as arguments.  Outputs:
<outdir>/<ID>.<variant>.npz in the format of p3a_subset.py (same columns, same meta keys) and <ID>.ind.json in the
format of p3a_indep.py.  Global index = position in the sorted list of the 460 Z(nunu) paths (--all-z).
No signal file is read; no efficiency is formed.
"""
import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p3a_subset as A  # noqa: E402
import p3a_indep as IND  # noqa: E402

B = A.B
log = logging.getLogger('p3a_multi')
VARIANTS = dict(m=dict(no_merge=False, pv='draw', w_select='pos'), u=dict(no_merge=True, pv='draw', w_select='pos'), pv0=dict(no_merge=False, pv='true', w_select='pos'),
                m0=dict(no_merge=False, pv='draw', w_select='zero'), pv2=dict(no_merge=False, pv='draw2', w_select='pos'),
                v2=dict(no_merge=False, pv='draw', w_select='pos'))
PV_SIGMA = np.array([0.010, 0.010, 0.015])


def do_variant(o, fi, path, meta, hits, off, evt, tru, nep_in, lc_all, sid_all, max_events, env, st, met=None):
    """Copy of the file loop of p3a_subset.main (both branches); o = dict(no_merge, pv, w_select)."""
    CI, FF, K, cfg, wcfg = env
    stream = meta['stream']; ec = meta['evt_cols']
    nev = int(meta['n_events'])
    is_z = stream == 'pilot.hs0.znn'
    if is_z:
        w = evt[:, ec.index('w_v1')].astype(np.float64); cls = np.full(nev, -1); nep = np.zeros(nev, np.int64)
        axis0 = evt[:, ec.index('phimet_reco_v1')].astype(np.float64); norient = 1
        if met is not None:                        # another MET model: its weight and its road axis
            w = met['w'].astype(np.float64); axis0 = met['phimet'].astype(np.float64)
            if len(w) != nev or len(axis0) != nev:
                raise SystemExit(f'{path}: MET file has {len(w)} entries, the pilot file {nev} events')
        vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]].astype(np.float64)
        use = {'pos': w > 0, 'zero': w == 0, 'all': np.ones(nev, np.bool_)}[o['w_select']].copy()
        pvs = np.zeros((nev, 3))
        tag = {'draw': 'p2t-pv', 'draw2': 'p3a-pv2'}.get(o['pv'])
        for i in np.where(use)[0]:
            if o['pv'] == 'true':
                pvs[i] = vtx[i]
            else:
                h = hashlib.blake2b(f'{tag}|{stream}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
                pvs[i] = vtx[i] + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
    else:
        w = np.ones(nev); cls = evt[:, ec.index('cls')].astype(np.int64); nep = nep_in.astype(np.int64)
        axis0 = evt[:, ec.index('phi_road')].astype(np.float64)
        norient = 1 if stream == 'pilot.c0.hs' else int(meta['road_orientations']['n'])
        pvs = evt[:, [ec.index('pv_x'), ec.index('pv_y'), ec.index('pv_z')]].astype(np.float64)
        use = np.ones(nev, np.bool_)
    nmax = nev if not max_events else min(nev, max_events)
    use[nmax:] = False
    pf = B.prefilter(hits[:, 1].astype(np.float64), hits[:, 2].astype(np.float64), hits[:, 3].astype(np.float64),
                     lc_all, FF.SIDE_OF[sid_all], off, pvs, axis0, use, norient, float(cfg.road), float(cfg.w_c))
    fm = dict(path=path, stream=stream, chunk=meta['chunk'], n_events=nev, n_classified_range=nmax, n_orient=norient,
              n_used=int(use.sum()), n_w_positive=int((w[:nmax] > 0).sum()),
              n_early_events=int((nep[:nmax] > 0).sum()), n_prefilter_pass=int(pf.sum()),
              content_sha256=meta.get('content_sha256'), mu=meta.get('mu'), mode=meta.get('mode'),
              trunc_mode=meta.get('trunc_mode'), n_per_ev_mode=meta.get('n_per_ev_mode'),
              beta_min=meta.get('beta_min'), handover=meta.get('handover'), sum_w_v1=meta.get('sum_w_v1'))
    if is_z:
        fm['w_max'] = float(w[:nmax].max())
        fm['sum_w_full'] = float(w[:nmax][w[:nmax] >= 0.5].sum()); fm['n_full'] = int((w[:nmax] >= 0.5).sum())
        fm['sum_w_low'] = float(w[:nmax][(w[:nmax] > 0) & (w[:nmax] < 0.5)].sum())
        fm['n_low'] = int(((w[:nmax] > 0) & (w[:nmax] < 0.5)).sum()); fm['n_zero'] = int((w[:nmax] == 0).sum())
    else:
        fm['cls_counts'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax], return_counts=True))}
        fm['cls_counts_flagged'] = {str(k): int(c) for k, c in zip(*np.unique(cls[:nmax][nep[:nmax] > 0],
                                                                             return_counts=True))}
    st['files'].append(fm)
    tot = st['tot']
    for i in np.where(pf.any(1))[0]:
        s = slice(int(off[i]), int(off[i + 1]))
        b = lc_all[s] >= 0
        H0 = hits[s][b].astype(np.float64)
        Hm = H0 if o['no_merge'] else CI.merge_pool(H0, tru[s][b].astype(np.float64))[0]
        for k in np.where(pf[i])[0]:
            phim = float((axis0[i] + 2 * np.pi * k / norient + np.pi) % (2 * np.pi) - np.pi)
            t0 = time.perf_counter()
            r = A.classify_pool(Hm, pvs[i], phim, cfg, wcfg, FF, K)
            tot['t_kernel'] += time.perf_counter() - t0
            tot['n_pref'] += 1; tot['n_seeds'] += r['n_seeds']; tot['n_planes'] += r['n_planes']
            tot['n_eval'] += r['n_eval']; tot['max_road'] = max(tot['max_road'], r['n_road'])
            if r['bad']:
                st['errors'].append(dict(file=fi, event=int(i), orient=int(k), error=f"{r['bad']} hits with non-constant sigma"))
                continue
            kb, KC, KI = r['kb'], r['KC'], r['KI']
            if ((kb[:, 0, :] <= A.KMAX[0]).any() or (kb[:, 1, :] <= A.KMAX[1]).any()
                    or (KC[:, :, 0, :] <= A.KMAX[0]).any() or (KC[:, :, 1, :] <= A.KMAX[1]).any()):
                ws_ = A.witness_summary(r['wit_rows'], FF)
                st['irows'].append([fi, i, k, cls[i], nep[i], r['n_road'], r['n_planes'], *kb.reshape(-1), *KC.reshape(-1),
                                    *KI.reshape(-1), r['wk'], *ws_])
                st['frows'].append([w[i], r['n_seeds']])
                if not is_z:                       # full witness tables, per width, for the attribution by truth
                    d = dict(file=fi, path=path, event=int(i), orient=int(k), cls=int(cls[i]),
                             n_early_prod=int(nep[i]), kb=kb.tolist(), witnesses={})
                    for tw in range(len(A.WL)):
                        rr = A.classify_pool(Hm, pvs[i], phim, cfg, wcfg, FF, K, tw=tw)
                        d['witnesses'][A.WNAMES[tw]] = dict(k=rr['wk'], hits=np.round(rr['wit_rows'], 4).tolist())
                    d['pool_columns'] = meta['columns']
                    d['evt'] = dict(zip(ec, [float(x) for x in evt[i]]))
                    st['dumps'].append(d)


def do_ind(gi, path, meta, hits, off, evt, tru, theirs, env, out):
    """Copy of the file loop of p3a_indep.main."""
    CI, FF, K, cfg, wcfg = env
    NR = IND.NR
    ec = meta['evt_cols']
    w = evt[:, ec.index('w_v1')]; ph = evt[:, ec.index('phimet_reco_v1')]
    vtx = evt[:, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
    for i in sorted(theirs[path]):
        assert w[i] > 0
        kk = theirs[path][i]
        widths = [W for wi, W in out['wmap'] if kk[wi, 0, 0] <= 3 or kk[wi, 1, 0] <= 5]
        if not widths:
            continue
        hsh = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
        pv = vtx[i] + np.random.default_rng(int.from_bytes(hsh, 'little')).normal(0.0, 1.0, 3) * NR.PV_SIGMA
        s = slice(int(off[i]), int(off[i + 1]))
        hh = hits[s].astype(np.float64); tt = tru[s].astype(np.float64)
        b = FF.LC_OF[hh[:, 0].astype(np.int64)] >= 0
        if b.sum() < 8:
            continue
        Hm = CI.merge_pool(hh[b], tt[b])[0]
        phim = float((ph[i] + np.pi) % (2 * np.pi) - np.pi)
        r, nb = IND.classify(Hm, pv, phim, FF, widths)
        out['n_bad'] += nb
        out['events'].append([path, i, float(w[i]), r, kk.reshape(-1).tolist()])
    out['files'].append(dict(gi=gi, path=path, n_rows=len(theirs[path])))


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s p3a_multi %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--all-z', required=True, help='JSON list of the 460 Z(nunu) pilot paths, sorted')
    ap.add_argument('--variants', default='m,u,pv0,m0,pv2,ind')
    ap.add_argument('--max-events', type=int, default=0)
    ap.add_argument('--met-dir', default='', help="variant v2: directory with <pilot stem>.met.npz ('w', 'phimet')")
    a = ap.parse_args()
    t_w0 = time.perf_counter(); t_c0 = time.process_time()
    variants = a.variants.split(',')
    p2w_sha = hashlib.sha256(Path(B.__file__).read_bytes()).hexdigest()
    if not p2w_sha.startswith(A.P2W_SHA256_PREFIX):
        raise SystemExit(f'p2w_subset.py sha256 {p2w_sha} is not the reviewed {A.P2W_SHA256_PREFIX}...')
    RS, CI, FF, K, GT, cfg, wcfg = B.load_frozen()
    if not np.allclose(GT.PV_SIGMA, PV_SIGMA):
        raise SystemExit('PV_SIGMA differs from v1 g1b_tt.PV_SIGMA')
    env = (CI, FF, K, cfg, wcfg)
    allz = json.loads(Path(a.all_z).read_text())
    if len(allz) != 460 or allz != sorted(allz):
        raise SystemExit('--all-z must be the sorted list of the 460 Z(nunu) pilot files')
    gidx = {p: i for i, p in enumerate(allz)}
    paths = json.loads(Path(a.manifest).read_text())[a.id]
    ST = {v: dict(files=[], irows=[], frows=[], errors=[], dumps=[], cpu=0.0,
                  tot=dict(n_pref=0, n_seeds=0, n_planes=0, n_eval=0, max_road=0, t_kernel=0.0)) for v in variants if v != 'ind'}
    ind = None
    if 'ind' in variants:
        import glob
        NR = IND.NR
        theirs = {}
        for f in sorted(glob.glob(f'{NR.V}/p2-c-r1v-s[23][ab]/000/r1v-s2-znn-*.npz')):
            z = np.load(f); m = json.loads(str(z['meta'])); r = z['rows']
            if any(abs(m['config'][k] - NR.CFG[k]) > 1e-12 for k in NR.CFG):
                raise SystemExit(f'{f}: config differs from CFG')
            k0 = m['row_cols'].index('k_R04_s0_S')
            for fi, fm in enumerate(m['files']):
                theirs[fm['path']] = {int(x[1]): x[k0:k0 + 20].astype(np.int64).reshape(5, 2, 2) for x in r[r[:, 0] == fi]}
            z.close()
        if len(theirs) != 460:
            raise SystemExit(f'{len(theirs)} Z files in the Phase-2 rows, expected 460')
        ind = dict(part=a.id, nparts=0, stride=2, offset=0, files=[], events=[], n_bad=0, cfg=NR.CFG, cpu_s=0.0,
                   wmap=[(0, 1e9), (0, 75.0), (1, 37.5), (2, 18.75), (3, 9.4), (4, 4.7)],
                   nils_sha256=hashlib.sha256(Path(NR.__file__).read_bytes()).hexdigest())
    for fi, path in enumerate(paths):
        gi = gidx.get(path, -1)
        z = np.load(path)
        meta = json.loads(str(z['meta']))
        is_z = meta['stream'] == 'pilot.hs0.znn'
        hits = z['hits']; off = z['hit_off'].astype(np.int64); evt = z['evt']; tru = z['tru']
        nep_in = None if is_z else z['n_early_prod']
        z.close()
        nev = int(meta['n_events'])
        if len(off) != nev + 1 or len(evt) != nev:
            raise SystemExit(f'{path}: offsets/evt do not match n_events')
        sid_all = hits[:, 0].astype(np.int64)
        lc_all = FF.LC_OF[sid_all]
        for v in variants:
            t0 = time.process_time()
            if v == 'ind':
                if is_z and gi % 2 == 0:
                    do_ind(gi, path, meta, hits, off, evt, tru, theirs, env, ind)
                ind['cpu_s'] += time.process_time() - t0
                continue
            if (v == 'pv2' and gi % 4 != 0) or (not is_z and v not in ('m', 'u')):
                continue
            st = ST[v]
            met = None
            if v == 'v2':
                if not a.met_dir:
                    raise SystemExit('variant v2 needs --met-dir')
                mz = np.load(Path(a.met_dir) / (Path(path).stem + '.met.npz'))
                met = dict(w=mz['w'], phimet=mz['phimet'])
            do_variant(VARIANTS[v], len(st['files']), path, meta, hits, off, evt, tru, nep_in, lc_all, sid_all, a.max_events,
                       env, st, met=met)
            st['cpu'] += time.process_time() - t0
        log.info('%s (gi %d): %s rows, %.1f s', Path(path).name, gi, {v: len(s['irows']) for v, s in ST.items()},
                 time.perf_counter() - t_w0)
    outdir = Path(a.outdir)
    my_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for v, st in ST.items():
        if not st['files']:
            continue                                  # variant not applicable to any file of this job
        o = VARIANTS[v]
        summ = dict(id=f'{a.id}.{v}', files=st['files'], i_cols=A.I_COLS, f_cols=A.F_COLS, widths=A.WL.tolist(),
                    wnames=A.WNAMES, cats=A.CATS, kmax=A.KMAX, n_errors=len(st['errors']), errors=st['errors'][:200],
                    totals=st['tot'], dumps=st['dumps'],
                    options=dict(no_merge=o['no_merge'], pv=o['pv'], w_select=o['w_select'], max_events=a.max_events,
                                 met_dir=(a.met_dir if v == 'v2' else ''),
                                 noff=int(B.NOFF), witness_target=A.WNAMES[A.TW_DEFAULT]),
                    config=dict(road=cfg.road, w_c=cfg.w_c, t_tol=cfg.t_tol, iters=cfg.iters, delta95=wcfg.delta95,
                                eta_max=wcfg.eta_max),
                    frozen_inputs_sha256=RS.sha256_file(RS.HERE / 'frozen_inputs.json'), p2w_subset_sha256=p2w_sha,
                    script_sha256=hashlib.sha256(Path(A.__file__).read_bytes()).hexdigest(), driver_sha256=my_sha,
                    wall_s=time.perf_counter() - t_w0, cpu_s=st['cpu'])
        out = outdir / f'{a.id}.{v}.npz'
        part = out.with_name(out.name + '.part')
        with open(part, 'wb') as f:
            np.savez_compressed(f, meta=json.dumps(summ),
                                rows_i=np.array(st['irows'], np.int32).reshape(-1, len(A.I_COLS)),
                                rows_f=np.array(st['frows'], np.float64).reshape(-1, len(A.F_COLS)))
            f.flush(); os.fsync(f.fileno())
        part.replace(out)
    if ind is not None and ind['files']:
        ind['wall_s'] = time.perf_counter() - t_w0
        ind['script_sha256'] = hashlib.sha256(Path(IND.__file__).read_bytes()).hexdigest(); ind['driver_sha256'] = my_sha
        p = outdir / f'{a.id}.ind.json'; part = p.with_name(p.name + '.part')
        with open(part, 'w') as f:
            f.write(json.dumps(ind)); f.flush(); os.fsync(f.fileno())
        part.replace(p)
    log.info('done: cpu %.1f s; rows %s; ind events %s', time.process_time() - t_c0,
             {v: len(s['irows']) for v, s in ST.items()}, len(ind['events']) if ind else None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
