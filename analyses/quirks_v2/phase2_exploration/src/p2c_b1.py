"""p2c_b1.py -- no-pile-up B1 events: one Geant4 vertex per event, handed to Fatras (pilot of STR §4.4 pt 5).

  <acts python> p2c_b1.py <term: dif|ni22|ni30|ni61> <out.npz> <n_events> <stream> <chunk> <first_vertex> <vtx.npz> [...]

The events are the vertices of class <term> (p2c_g4vtx.classify) of the given vertex files, in file order, starting
at <first_vertex>.  Chain: run_chain.build_sequencer unchanged, with v1's Truncate for the parent (variant A) and the
SimHits of the event stored on every surface (`toy`, run_chain.TOY_COLS) for the later overlays.
Output (p2c_common layout) plus:
  evt (n_ev, len(EVT_COLS)), gvtx (n_ev, len(VCOLS)) the Geant4 vertex row, gprod/gprod_off the Geant4 products,
  gcross/gcross_off the parent's Geant4 crossings before the vertex (variant B input), inj/inj_off the rows given to
  Fatras (s4pu.PCOLS), toy/toy_off the stored SimHits.
The road and the PV are NOT fixed here: `pv_*` is an independent luminous-region draw and `phimet` a uniform draw,
both seeded per event and stored for convenience; Phase 3 chooses the convention (plan O8).
"""
import json
import shutil
import sys
import tempfile
import time

import numpy as np

import p2c_common as C
import p2c_g4vtx as GV
import p2c_handover as HO

sys.path.insert(0, str(C.CODE))
import run_chain as rc  # noqa: E402
import s4pu  # noqa: E402

log = C.setup_logging('p2c_b1')
EVT_COLS = ['vertex_index', 'pv_x', 'pv_y', 'pv_z', 'phimet', 'n_products_g4', 'n_injected', 'n_trunc_dropped',
            'parent_charged', 'n_injected_beta_lt_0p1', 'ev_seed_lo', 'ev_seed_hi']


def load_vertices(files, term, first, n):
    """First n vertices of class `term` from the files, starting at index `first` of that class."""
    V = []; PR = []; CR = []; names = None; seen = 0; vcols = None
    for f in files:
        z, meta = C.load_job(f)
        nm = GV.Names(); nm.proc = meta['proc_names']; nm.vol = meta['vol_names']
        m, _, _ = GV.classify(z['vtx'], nm)
        idx = np.nonzero(m[term])[0]
        take = idx[max(first - seen, 0):][:n - len(V)]
        seen += len(idx)
        vcols = meta['vcols']; names = meta['vol_names']
        po = z['prod_off']; xo = z['cross_off']; prod = z['prod']; cross = z['cross']; vtx = z['vtx']
        for i in take:
            V.append(vtx[i]); PR.append(prod[po[i]:po[i + 1]]); CR.append(cross[xo[i]:xo[i + 1]])
        if len(V) >= n:
            break
    if len(V) < n:
        raise RuntimeError(f'only {len(V)} vertices of class {term} available, {n} asked')
    return V, PR, CR, vcols, names


def run(term, out, n_events, stream, chunk, first, files):
    t_start = time.time()
    job_seed = C.qv2_seed(stream, chunk)
    V, PR, CR, vcols, surf_names = load_vertices(files, term, first, n_events)
    ev_seeds = [s4pu.hseed('p2c-b1', term, job_seed, i, mod=2 ** 62) for i in range(n_events)]
    dec = HO.Decayer(job_seed)
    bs = s4pu.load_beamspot(rc.TT)
    sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm']])
    scratch = tempfile.mkdtemp(prefix='p2c_b1_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        store = {}; aux = {}
        rc.TIMES.clear()

        def provider(i):
            P, trunc, npg, ninj, nslow = HO.event_rows(V[i], PR[i], vcols, dec, ev_seeds[i])
            rng = np.random.default_rng(s4pu.hseed('p2c-b1-pv', term, ev_seeds[i], mod=2 ** 63))
            pv = rng.normal(0, 1, 3) * sig
            phimet = rng.uniform(-np.pi, np.pi)
            g = dict(zip(vcols, V[i]))
            vz = np.array([[s4pu.GUN_VP, g['x0'], g['y0'], g['z0'], g['t0'], g['px0'], g['py0'], g['pz0']]])
            aux[i] = (P, pv, phimet, npg, ninj, len(trunc), nslow)
            return P, vz, dict(trunc=trunc, n_particles=len(P))
        trunc = rc.Truncate(lambda i: store[i]['info']['trunc'], store)
        s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True, truncate=trunc,
                               store_vp={s4pu.GUN_VP})
        s.run()
        v41 = np.zeros((n_events, len(rc.V41_COLS))); tim = np.zeros((n_events, len(rc.T_COLS)))
        st = {}
        for e, nm, t in rc.TIMES:
            st.setdefault(e, {})[nm] = t
        evt = np.zeros((n_events, len(EVT_COLS)))
        hits = []; tru = []; vzs = []; toys = []; inj = []
        for i in range(n_events):
            r = store[i]; ev = r['ev']
            v41[i] = (r['nh'], r['nm'], r['nmap'], r['bij'], r['nunm'], len(ev), r['onsurf'], 0, 0, 0, r['ntr'],
                      r['nckf'], r['n_in'])
            x = st.get(i, {})
            t2 = x.get('t2_digi', 0.0); t3 = x.get('t3_seed', t2); t4 = x.get('t4_ckf', t3)
            tim[i] = (r['t_gen'], r['t_source'], t2 - x.get('t1_source', t2), t3 - t2, t4 - t3, r['t_dump'])
            P, pv, phimet, npg, ninj, ntr, nslow = aux[i]
            evt[i] = (first + i, *pv, phimet, npg, ninj, r.get('n_trunc_dropped', 0), ntr, nslow, ev_seeds[i] % 2 ** 31,
                      ev_seeds[i] // 2 ** 31)
            hits.append(ev); tru.append(r['tru']); vzs.append(r['vz']); toys.append(r['toy_simhits']); inj.append(P)
        H, hoff = C.concat(hits, len(rc.COLS), np.float32)
        T, _ = C.concat(tru, 3, np.float32)
        VZ, voff = C.concat(vzs, 8, np.float64)
        TOY, toff = C.concat(toys, len(rc.TOY_COLS), np.float64)
        INJ, ioff = C.concat(inj, 12, np.float64)
        GP, gpoff = C.concat(PR, 9, np.float64)
        GC, gcoff = C.concat(CR, 8, np.float32)
        v41_pass = bool(np.all(v41[:, 3] == 1) and np.all(v41[:, 4] == 0) and np.all(v41[:, 6] < 1.0)
                        and np.all(v41[:, 0] - v41[:, 1] <= np.maximum(2, 1e-5 * v41[:, 0])))
        meta = dict(mode='b1', term=term, stream=stream, chunk=chunk, job_seed=job_seed, n_events=n_events,
                    first_vertex=first, vertex_files=[str(f) for f in files], handover=f'A (Fatras parent, v1 Truncate); products with beta < {HO.BETA_MIN} not handed over',
                    chain=rc.CHAIN, columns=rc.COLS, v41_cols=rc.V41_COLS, timing_cols=rc.T_COLS, evt_cols=EVT_COLS,
                    vcols=vcols, toy_cols=rc.TOY_COLS, pcols=s4pu.PCOLS, surface_names=surf_names,
                    prod_cols=['pdg', 'px', 'py', 'pz', 'E', 'x', 'y', 'z', 't'],
                    cross_cols=['surface', 'x', 'y', 'z', 't', 'px', 'py', 'pz'], v41_pass=v41_pass,
                    n_lost_simhits=int(np.sum(v41[:, 0] - v41[:, 1])),
                    code_sha256=C.code_hashes([__file__, C.HERE / 'p2c_common.py', C.HERE / 'p2c_handover.py',
                                               C.HERE / 'p2c_g4vtx.py']),
                    t_total_s=round(time.time() - t_start, 3),
                    mean_s_per_event={c: float(tim[:, k].mean()) for k, c in enumerate(rc.T_COLS)},
                    n_hits=int(len(H)), n_simhits=int(len(TOY)), n_ckf_tracks=int(v41[:, 10].sum()),
                    mean_injected=float(evt[:, 6].mean()), mean_trunc_dropped=float(evt[:, 7].mean()),
                    mean_injected_slow=float(evt[:, 9].mean()))
        nbytes = C.save_job(out, dict(hits=H, hit_off=hoff, tru=T, vz=VZ, vz_off=voff, v41=v41, timing=tim, evt=evt,
                                      gvtx=np.array(V, float), gprod=GP, gprod_off=gpoff, gcross=GC, gcross_off=gcoff,
                                      inj=INJ, inj_off=ioff, toy=TOY, toy_off=toff), meta)
        meta['bytes'] = nbytes
        log.info(json.dumps({k: meta[k] for k in ('term', 'n_events', 't_total_s', 'v41_pass', 'mean_s_per_event',
                                                  'n_hits', 'n_simhits', 'mean_injected', 'mean_injected_slow', 'mean_trunc_dropped',
                                                  'bytes')}))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]), int(a[5]), a[6:])
