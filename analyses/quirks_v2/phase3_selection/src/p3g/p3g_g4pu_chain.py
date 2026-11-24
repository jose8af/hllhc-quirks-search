"""p3g_g4pu_chain.py -- dev.g4pu chain (STR §2 "Pile-up-vertex secondaries", COM B1-g; §4.17 row 13).  acts env.

  <acts python> p3g_g4pu_chain.py <out.npz> <n_events> <job_seed>

Per event: a PU-200 event exactly as s4pu.MinBias.event (same seeds, vertices, Fatras rows: the nominal pile-up
event); in addition every final-state hadron of the 200 interactions that Fatras does not decay or absorb -- pi+-,
K+-, p, K0L, n (Pythia final state, the Fatras acceptance pT > 0.05 GeV, |eta| < 4, of s4pu.select_and_place) -- is
fired through Geant4 11.4.3 FTFP_BERT from its production point (p2c_g4vtx.run_g4, pass 'all', rmax 1200 mm, products
at the exit of their slab).  Every vertex of the addendum-1 B1 classes (dif, difc, k0l, ni22, ni30, ni61, nix, nic;
not conversions, not 'other') is handed to Fatras by the frozen per-stream rule of the B1 samples (ADD §3 P6,
p2c_handover.event_rows: products from the slab exit, beta < 0.1 not handed over, Pythia decays of unstable products):
products get vp = 3600 and vsec = 16 * (vertex number) + (their local vsec), so each secondary is counted once and
carries its vertex; the charged parent's Fatras SimHits are cut at the vertex: radius cut for first-arc classes
(v1 Truncate), time cut for the after-a-turn classes (difc, nic).  Reading, flagged: the after-a-turn parents are NOT
given their Geant4 crossings beyond half a turn (option (a) of the B1 samples): like every other pile-up particle of
every B2 sample they stop at half a turn ([L15]); only the products are added.  Photons are not fired: Fatras already
converts them (route table, STR §2) and their photonuclear vertices (0.4 % of the inelastic vertices, ADD §3 P3 table)
are left out.  Each secondary has its own vertex at its own z (own-z placement, STR §2 item 1).
Output: run_chain.finish layout (ev{i}, tru{i}, vz{i}, v41, timing, meta) + g4 summary per event in meta.
"""
import json
import math
import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

QV2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(QV2 / 'phase2_exploration' / 'src'))
import p2c_common as C  # noqa: E402
import p2c_b1 as B1  # noqa: E402
import p2c_handover as HO  # noqa: E402
import p2c_g4vtx as GV  # noqa: E402
import p2x_common as X  # noqa: E402
import p2x_b1 as XB  # noqa: E402

rc = B1.rc
s4pu = B1.s4pu
log = C.setup_logging('p3g_g4pu_chain')
G4_VP = 3600
FIRE = (211, 321, 2212, 130, 2112)
B1_KEEP = ('dif', 'difc', 'k0l', 'ni22', 'ni30', 'ni61', 'nix', 'nic')
AFTER_TURN = ('difc', 'nic')


def parents(gen, seeds, vtx, k):
    """Final-state particles of interaction k (s4pu.MinBias.generate output) placed at vtx, the Fatras acceptance of
    select_and_place; returns rows (pdg, q, m, x, y, z, t_ns, px, py, pz, vsec) of the hadrons to fire, and the Fatras
    rows of the interaction (identical to select_and_place)."""
    parts, _ = gen.generate(seeds[k])
    rows, psum, _ = s4pu.select_and_place(parts, k + 1, vtx[k])
    if not parts:
        return np.zeros((0, 11)), rows, psum
    a = np.array(parts, float)
    pdg = a[:, 0]; q = a[:, 1]
    pt = np.hypot(a[:, 3], a[:, 4]); pabs = np.sqrt(pt ** 2 + a[:, 5] ** 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        eta = np.arctanh(np.where(pabs > 0, a[:, 5] / np.maximum(pabs, 1e-300), 0.0))
    x = a[:, 7] + vtx[k][0]; y = a[:, 8] + vtx[k][1]; z = a[:, 9] + vtx[k][2]
    t = a[:, 10] / s4pu.C_MM_PER_NS + vtx[k][3]
    acc = (pt > s4pu.PT_MIN) & (np.abs(eta) < s4pu.ETA_MAX) & (np.hypot(x, y) < s4pu.RHO_MAX) & (np.abs(z) < s4pu.Z_MAX)
    # vsec of each particle as select_and_place numbers it (displaced Pythia vertices)
    disp = (np.abs(a[:, 7]) + np.abs(a[:, 8]) + np.abs(a[:, 9])) > 0
    vsec = np.zeros(len(a), np.int64)
    if disp.any():
        _, inv = np.unique(np.round(a[disp, 7:11], 9), axis=0, return_inverse=True)
        vsec[disp] = 1 + inv.ravel()
    fire = acc & np.isin(np.abs(pdg), FIRE)
    out = np.c_[pdg, q, a[:, 2], x, y, z, t, a[:, 3], a[:, 4], a[:, 5], vsec][fire]
    return out, rows, psum


def run(out, n_events, job_seed):
    t_start = time.time()
    HO.BETA_MIN = 0.1
    mb = s4pu.MinBias(rc.CP5, s4pu.load_beamspot(rc.TT), mu=200.0, tt=rc.TT)
    ev_seeds = [s4pu.hseed('g4pu', job_seed, i, mod=2 ** 62) for i in range(n_events)]
    dec = HO.Decayer(job_seed)
    scratch = tempfile.mkdtemp(prefix='p3g_g4pu_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        geom = GV.geom_file()
        events = {}; g4info = []
        t_g4 = 0.0
        for i in range(n_events):
            rng = np.random.default_rng(s4pu.hseed('pu-event', ev_seeds[i], mod=2 ** 63))
            n = int(rng.poisson(mb.mu))
            bs = mb.bs
            sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm'], bs['sigma_t_ps'] * 1e-3])
            vtx = rng.normal(0.0, 1.0, (n, 4)) * sig
            seeds = rng.integers(1, 900_000_000, n)
            rows = []; vz = []; fire = []
            for k in range(n):
                f, r, psum = parents(mb.gen, seeds, vtx, k)
                rows.append(r); vz.append((k + 1, *vtx[k], *psum))
                if len(f):
                    fire.append(np.c_[np.full(len(f), k + 1), f])
            P = np.concatenate(rows) if rows else np.zeros((0, 12))
            F = np.concatenate(fire) if fire else np.zeros((0, 12))
            # Fatras barcode of each Fatras row: running count per (vp, vsec) in input order (run_chain.ParticleSource)
            cnt = {}; bc = {}
            for j, rr in enumerate(P):
                key = (int(rr[0]), int(rr[1])); cnt[key] = cnt.get(key, 0) + 1
                bc[(key[0], key[1], round(rr[9], 9), round(rr[10], 9), round(rr[11], 9))] = (key[0], key[1], cnt[key])
            # Geant4: fire every selected hadron
            tg = time.time()
            fin = Path('prim_g4pu.txt'); fout = Path('vtx_g4pu.txt')
            with open(fin, 'w') as fh:
                for j, r in enumerate(F):
                    fh.write('%d %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n' % (j, r[1], r[4], r[5], r[6], r[7], r[8], r[9], r[10]))
            names = GV.Names()
            kv, _ = GV.run_g4([geom, 'FTFP_BERT', int(ev_seeds[i] % (2 ** 31 - 2)) + 1, fout, 'prim', fin, 1200.0, 'exit'])
            prim = np.c_[F[:, 1], F[:, 4:8], F[:, 8:11], np.arange(len(F))]
            V, PR_, Xc, np_, nx = GV.parse(fout, names, 0, list(GV.PASSES).index('all'), prim)
            fin.unlink(); fout.unlink()
            t_g4 += time.time() - tg
            A = GV.pack([dict(V=V, P=PR_, X=Xc, np=np_, nx=nx)])
            Vv = A['vtx']
            codes, _ = X.class_codes(Vv, names) if len(Vv) else (np.zeros(0, np.int8), None)
            vcols = GV.VCOLS
            prows = []; trunc = []; vinfo = []; seen = set(); nconv = 0; nother = 0; nmulti = 0
            nslow = 0
            for q_, v in enumerate(Vv):
                cname = X.CLASSES[int(codes[q_])]
                if cname not in B1_KEEP:
                    nconv += cname == 'conversion'; nother += cname == 'other'
                    continue
                fi = int(v[0])
                if fi in seen:
                    nmulti += 1
                    continue
                seen.add(fi)
                prods = A['prod'][A['prod_off'][q_]:A['prod_off'][q_ + 1]]
                Pv, tl, npg, ninj, ns = HO.event_rows(v, prods, vcols, dec, ev_seeds[i] * 7 + q_)
                nslow += ns
                nv = len(vinfo)
                pr = Pv[Pv[:, 1] >= 1].copy() if len(Pv) else Pv     # products only (the parent row is the Fatras row)
                if len(pr):
                    pr[:, 0] = G4_VP
                    pr[:, 1] = 16 * (nv + 1) + np.minimum(pr[:, 1], 15)
                    prows.append(pr)
                fr = F[fi]
                g = dict(zip(vcols, v))
                if abs(int(fr[1])) in (211, 321, 2212):
                    key = (int(fr[0]), int(fr[11]), round(fr[8], 9), round(fr[9], 9), round(fr[10], 9))
                    b = bc.get(key)
                    if b is not None:
                        mode = 'time' if cname in AFTER_TURN else 'radius'
                        trunc.append((b[0], b[1], b[2], float(math.hypot(g['x'], g['y'])), float(g['t']), mode))
                vinfo.append([nv + 1, int(fr[0]), X.CODE[cname], int(fr[1]), math.hypot(g['x'], g['y']), g['z'], g['t'],
                              len(pr), float(np.hypot(fr[8], fr[9]))])
            PP = np.concatenate([P] + prows) if prows else P
            events[i] = (PP, np.array(vz, float).reshape(-1, 8), dict(n_int=n, n_particles=len(PP), trunc=trunc,
                                                                    n_fired=len(F), n_vtx_b1=len(vinfo),
                                                                    n_conv=nconv, n_other=nother, n_multi=nmulti,
                                                                    n_products=int(sum(len(p) for p in prows)),
                                                                    n_slow=nslow, vinfo=vinfo,
                                                                    g4_event_cpu_s=float(kv.get('event_cpu_s', 'nan'))))
            g4info.append({k: events[i][2][k] for k in ('n_fired', 'n_vtx_b1', 'n_conv', 'n_other', 'n_multi',
                                                         'n_products', 'n_slow', 'g4_event_cpu_s')})
            log.info('event %d: %d interactions, %d fired, %d B1 vertices, %d products', i, n, len(F), len(vinfo),
                     events[i][2]['n_products'])
        store = {}
        rc.TIMES.clear()

        def provider(i):
            return events[i]
        trunc = XB.TruncateParent(lambda i: store[i]['info']['trunc'], store, 'per-event')
        s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True, truncate=trunc)
        s.run()
        meta = dict(mode='g4pu', job_seed=job_seed, mu=200.0, event_seeds=ev_seeds, g4=g4info, t_g4_s=round(t_g4, 2),
                    g4_vp=G4_VP, vsec_rule='16 * vertex number + local vsec', classes=X.CLASSES,
                    vinfo_cols=['vertex', 'vp', 'cls', 'parent_pdg', 'r', 'z', 't', 'n_products', 'parent_pt'],
                    code_sha256={Path(__file__).name: C.sha256_file(__file__)})
        meta['ev_info'] = [{k: v for k, v in store[i]['info'].items() if k != 'trunc'} for i in range(n_events)]
        meta = rc.finish(out, store, n_events, meta, t_start)
        print(json.dumps({k: meta[k] for k in ('chain', 'n_events', 't_total_s', 'v41_pass', 'mean_s_per_event')
                          if k in meta}))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], int(a[1]), int(a[2]))
