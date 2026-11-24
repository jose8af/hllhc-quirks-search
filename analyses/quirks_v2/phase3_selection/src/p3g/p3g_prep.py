"""p3g_prep.py -- source events of the p3-g overlay campaigns (Tormod, 2026-11-24).  Runner job, tt environment.

  <tt python> p3g_prep.py --mode npo --part P --nparts NP --out /ABS/out.npz
  <tt python> p3g_prep.py --mode dif --out /ABS/out.npz [--n 1000]

npo  (STR §4.17 row 11, the pilot's near-pass overlays; seed stream pilot.ovl).  The pilot's B1 samples hold no near-pass
     event (P3A §3.3), so the near-pass events are Z(nunu) pilot events of the full-weight class (w_v1 >= 0.5) with an
     own-hit class k <= k_max = 3 at R05 (s = 0), reading BASE (S), label m of P3A (merged pool, PV draw) -- the counts
     P3A delivered; nothing reclassified for the count.  Stratified in k(R05) = 0, 1, 2, 3.  To bound the NFS reading,
     the events come from NF = 120 pilot files drawn (seeded) among the 181 files that hold a k = 0 row: every k = 0 row
     of those files, and the rest of the 1,000 split equally over k = 1, 2, 3 (seeded draw).  The selection is computed
     identically in every part; part P reads the files with index % NP == P.
     Per event: the stored rows (barrel counting surfaces + BTL; 13 columns), their truth positions, PV draw (P3A's
     'p2t-pv' seed), road axis phimet_reco_v1, and the own-hit class recomputed with the P3A classifier (imported
     unchanged) at R04w and R05 with its witness rows (for the pi_k prediction); the recomputed k must equal P3A's
     stored k (checked; the job fails otherwise).
dif  (STR §4.17 row 13a; seed stream dev.ovl.dif).  1,000 events drawn (seeded) without regard to their class from
     one pilot DIF file chosen by the same seed: stored SimHits of the overlaid event ('toy', TOY_COLS), stored rows,
     truth, PV and road axis phi_road (orientation 0, the one that contains the parent).
No signal file is read.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p3g_common as G  # noqa: E402
sys.path.insert(0, str(G.P2SRC))
sys.path.insert(0, str(G.P3SRC / 'p3a'))

log = G.setup_logging('p3g_prep')
ROWS = G.QV2 / 'phase3_selection' / 'outputs' / 'p3a' / 'p3a_counts.json.rows_m.npz'
NF = 120
NTOT = 1000
PV_SIGMA = np.array([0.010, 0.010, 0.015])
EV_COLS_NPO = ['row', 'path_idx', 'event', 'k_R04w', 'k_R05', 'k_R04w_re', 'k_R05_re', 'pv_x', 'pv_y', 'pv_z', 'phimet',
               'w', 'vtx_x', 'vtx_y', 'vtx_z', 'n_rows', 'n_wit4', 'n_wit5']
EV_COLS_DIF = ['file_event', 'pv_x', 'pv_y', 'pv_z', 'phimet', 'cls', 'parent_pdg', 'parent_pt0', 'vtx_r', 'first_arc',
               'n_rows', 'n_toy', 'n_early_prod']


def select_npo():
    z = np.load(ROWS)
    paths = [str(p) for p in z['paths']]
    term = z['term']; w = z['w']; pidx = z['path_idx']; ev = z['event']
    K = z['K']                                   # (reading, row, width, s, S/F); BASE = 0; R04w = 1, R05 = 2
    k5 = K[0, :, 2, 0, 0].astype(np.int64); k4 = K[0, :, 1, 0, 0].astype(np.int64)
    ok = (term == 'Z') & (w >= 0.5) & (k5 <= 3)
    rng = np.random.default_rng(G.qv2_seed('pilot.ovl', 'select'))
    f0 = np.unique(pidx[ok & (k5 == 0)])
    files = np.sort(rng.choice(f0, size=min(NF, len(f0)), replace=False))
    inf = np.isin(pidx, files) & ok
    sel = list(np.where(inf & (k5 == 0))[0])
    nrest = NTOT - len(sel)
    for kk in (1, 2, 3):
        cand = np.where(inf & (k5 == kk))[0]
        m = nrest // 3 + (1 if kk <= nrest % 3 else 0)
        sel += list(rng.choice(cand, size=min(m, len(cand)), replace=False))
    sel = np.array(sorted(sel))
    return dict(paths=paths, files=files, sel=sel, pidx=pidx, ev=ev, k4=k4, k5=k5, w=w)


def run_npo(a):
    import p2w_subset as B
    import p3a_subset as A
    RS, CI, FF, KK, GT, cfg, wcfg = B.load_frozen()
    S = select_npo()
    mine = [f for i, f in enumerate(S['files']) if i % a.nparts == a.part]
    if a.max_files:
        mine = mine[:a.max_files]
    rows = [r for r in S['sel'] if S['pidx'][r] in set(mine)]
    out = {}; E = []
    t0 = time.time()
    for fi in mine:
        path = S['paths'][fi]
        zz = np.load(path)
        meta = json.loads(str(zz['meta']))
        assert meta['stream'] == 'pilot.hs0.znn' and float(meta['mu']) == 0.0
        hits = zz['hits']; off = zz['hit_off']; tru = zz['tru']; evt = zz['evt']
        ec = meta['evt_cols']
        for r in [r for r in rows if S['pidx'][r] == fi]:
            i = int(S['ev'][r])
            s = slice(int(off[i]), int(off[i + 1]))
            Hall = hits[s].astype(np.float64); Tall = tru[s].astype(np.float64)
            h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
            vtx = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]].astype(np.float64)
            pv = vtx + np.random.default_rng(int.from_bytes(h, 'little')).normal(0.0, 1.0, 3) * PV_SIGMA
            phim = float(evt[i, ec.index('phimet_reco_v1')])
            b = FF.LC_OF[Hall[:, 0].astype(np.int64)] >= 0
            Hm = CI.merge_pool(Hall[b], Tall[b])[0]
            r4 = A.classify_pool(Hm, pv, phim, cfg, wcfg, FF, KK, tw=1)
            r5 = A.classify_pool(Hm, pv, phim, cfg, wcfg, FF, KK, tw=2)
            k4re = int(r4['kb'][1, 0, 0]); k5re = int(r5['kb'][2, 0, 0])
            if k4re != S['k4'][r] or k5re != S['k5'][r]:
                raise SystemExit(f'{path} event {i}: recomputed k (R04w {k4re}, R05 {k5re}) != P3A ({S["k4"][r]}, {S["k5"][r]})')
            j = len(E)
            out[f'h{j}'] = Hall; out[f't{j}'] = Tall
            out[f'wit4_{j}'] = r4['wit_rows']; out[f'wit5_{j}'] = r5['wit_rows']
            E.append([r, fi, i, S['k4'][r], S['k5'][r], k4re, k5re, *pv, phim, S['w'][r], *vtx, len(Hall),
                      len(r4['wit_rows']), len(r5['wit_rows'])])
        zz.close()
        log.info('file %d done (%d events so far, %.0f s)', fi, len(E), time.time() - t0)
    out['ev'] = np.array(E, np.float64).reshape(-1, len(EV_COLS_NPO))
    meta = dict(mode='npo', part=a.part, nparts=a.nparts, ev_cols=EV_COLS_NPO, n_events=len(E), n_files=len(mine),
                selection=dict(NF=NF, NTOT=NTOT, seed_stream='pilot.ovl|select', reading='BASE (S), s = 0, label m',
                               n_selected_total=int(len(S['sel'])),
                               n_per_k_total={str(k): int((S['k5'][S['sel']] == k).sum()) for k in range(4)}),
                columns=meta['columns'], rows_file=str(ROWS), rows_sha256=G.sha256_file(ROWS),
                code_sha256={p.name: G.sha256_file(p) for p in (Path(__file__), G.HERE / 'p3g_common.py',
                                                                 Path(A.__file__), Path(B.__file__))})
    return out, meta


def run_dif(a):
    rng = np.random.default_rng(G.qv2_seed('dev.ovl.dif', 'select'))
    files = sorted(str(p) for p in (G.DATA / 'pilot').glob('p2-c-pilot-c0-dif-0[0-3]/000/p2-c-pilot-c0-dif-*.npz'))
    path = files[int(rng.integers(0, len(files)))]
    zz = np.load(path)
    meta = json.loads(str(zz['meta']))
    assert meta['stream'] == 'pilot.c0.dif'
    nev = int(meta['n_events'])
    sel = np.sort(rng.choice(nev, size=a.n, replace=False))
    hits = zz['hits']; off = zz['hit_off']; tru = zz['tru']; evt = zz['evt']; toy = zz['toy']; toff = zz['toy_off']
    nep = zz['n_early_prod']
    ec = meta['evt_cols']
    out = {}; E = []
    for j, i in enumerate(sel):
        s = slice(int(off[i]), int(off[i + 1]))
        out[f'h{j}'] = hits[s].astype(np.float64); out[f't{j}'] = tru[s].astype(np.float64)
        out[f'toy{j}'] = toy[int(toff[i]):int(toff[i + 1])].astype(np.float64)
        g = dict(zip(ec, evt[i]))
        E.append([i, g['pv_x'], g['pv_y'], g['pv_z'], g['phi_road'], g['cls'], g['parent_pdg'], g['parent_pt0'], g['vtx_r'],
                  g['first_arc'], s.stop - s.start, toff[i + 1] - toff[i], nep[i]])
    out['ev'] = np.array(E, np.float64)
    m = dict(mode='dif', source_file=path, source_sha256_content=meta.get('content_sha256'), n_events=len(E),
             ev_cols=EV_COLS_DIF, columns=meta['columns'], toy_cols=meta['toy_cols'], seed_stream='dev.ovl.dif|select',
             road='orientation 0 (phi_road: the road that contains the parent)',
             code_sha256={p.name: G.sha256_file(p) for p in (Path(__file__), G.HERE / 'p3g_common.py')})
    return out, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['npo', 'dif'], required=True)
    ap.add_argument('--part', type=int, default=0)
    ap.add_argument('--nparts', type=int, default=1)
    ap.add_argument('--n', type=int, default=1000)
    ap.add_argument('--max-files', type=int, default=0, help='tests only')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    t0 = time.time()
    out, meta = run_npo(a) if a.mode == 'npo' else run_dif(a)
    meta['t_s'] = round(time.time() - t0, 1)
    p = Path(a.out)
    tmp = p.with_name(p.name + '.tmp.npz')
    np.savez_compressed(tmp, meta=np.array(json.dumps(meta, default=str)), **out)
    tmp.replace(p)
    log.info('%s: %d events, %.0f s', p.name, meta['n_events'], meta['t_s'])


if __name__ == '__main__':
    main()
