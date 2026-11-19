"""cpu_attrib.py -- C'_PU attribution: v1's link rule vs the frozen own-hit rule j >= n/2 (STR l.747-754).

  <tt python> cpu_attrib.py <data/phase2 dir> <surfaces_s3.json> <out.json>

Eskil (executor), 2026-11-19.  Plan: outputs/CPU_ATTRIB_PLAN_eskil_2026-11-19.md.  Read-only on the C1 reproduction
C'_PU outputs (p2-a-c1-cppua: dif, gamma, v0; p2-a-c1-cppub: pvpair).  No signal file.
v1 rule: cp.cand.attributed (g1b_tt.attribute).  Frozen rule: j = # IT+PS layers whose double crossing is made of toy
hits alone (INT mod 1e6 == 3500; IT >= 2 hits, PS >= 2 on each side), attributed iff j >= 4 (n = 7 at R04-R06).
Counts are candidates per slot; clusters = source C'0 event (cp.ev[:, 1]), as c1_compare.cppu_clusters.
"""
import glob
import json
import sys
from pathlib import Path

import numpy as np

LAYERS = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']
GUN_VP = 3500
NR = 43
RUNG = {'R02': 1, 'R04': 3, 'R05': 4, 'R06': 5}
NBOOT = 4000


def unpack(r):
    return np.unpackbits(np.asarray(r, np.uint8), axis=1)[:, :NR].astype(bool)


def jvals(z, lc_of, side_of, chk):
    """-> dict (trial, cand idx) -> (j_own, n_own_hits) for every candidate with a full hit record."""
    off = z['hit.off']; ref = z['hit.ref']; sid = z['hit.sid'].astype(np.int64); INT = z['hit.INT']
    out = {}
    cidx = {(int(t), int(i)): k for k, (t, i) in enumerate(zip(z['cand.trial'], z['cand.idx']))}
    cross = z['cand.cross']
    for k, (t, c) in enumerate(zip(z['hit.trial'], z['hit.cand'])):
        h = ref[off[k]:off[k + 1]]
        lc = lc_of[sid[h]]; sd = side_of[sid[h]]; own = (INT[h] % 1_000_000) == GUN_VP
        kc = cidx.get((int(t), int(c)))
        if kc is not None:
            cr = [int((lc == L).sum()) if L < 4 else int(min(((lc == L) & (sd == 1)).sum(), ((lc == L) & (sd == 2)).sum()))
                  for L in range(10)]
            chk['n'] += 1; chk['bad'] += cr != [int(x) for x in cross[kc]]
        j = 0
        for L in range(7):
            a = (lc == L) & own
            n = int(a.sum()) if L < 4 else int(min((a & (sd == 1)).sum(), (a & (sd == 2)).sum()))
            j += n >= 2
        out[(int(t), int(c))] = (j, int(own.sum()))
    return out


def main(d, surf, outp):
    S = json.loads(Path(surf).read_text())['surfaces']
    lc_of = np.full(len(S), -1); side_of = np.zeros(len(S), int)
    for i, s in enumerate(S):
        for k, p in enumerate(LAYERS):
            if s['name'] == p or s['name'].startswith(p + '_'):
                lc_of[i] = k; side_of[i] = 1 if s['name'].endswith('_in') else (2 if s['name'].endswith('_out') else 0)
    files = sorted(glob.glob(f'{d}/p2-a-c1-cppua/000/c1cppu-*.npz')) + sorted(glob.glob(f'{d}/p2-a-c1-cppub/000/c1cppu-*.npz'))
    rows = {}      # topo -> list of per-candidate tuples and per-slot clusters
    chk = dict(n=0, bad=0, rung_mismatch=0, v1_R04_not_in_cand=0)
    for f in files:
        topo = Path(f).name.split('-')[1]
        z = np.load(f)
        R = rows.setdefault(topo, dict(slot_cl=[], c=[]))
        tev = z['trials.ev'].astype(np.int64)
        cl = z['cp.ev'][tev, 1].astype(np.int64)            # cluster of each trial = source C'0 event
        R['slot_cl'].append(cl)
        J = jvals(z, lc_of, side_of, chk)
        Fc = unpack(z['cand.rungs']); tag = z['cand.tag']
        ct = z['cand.trial'].astype(np.int64); ci = z['cand.idx'].astype(np.int64)
        cmap = {(int(t), int(i)): k for k, (t, i) in enumerate(zip(ct, ci))}
        att = {}; lk = {}
        if 'cp.cand.attributed' in z.files:
            Fp = unpack(z['cp.cand.rungs'])
            NL, NY, MC = z['cp.cand.n_links'], z['cp.cand.n_layers'], z['cp.cand.max_cross']
            for k, (t, i, a) in enumerate(zip(z['cp.cand.trial'], z['cp.cand.idx'], z['cp.cand.attributed'])):
                att[(int(t), int(i))] = (bool(a), Fp[k])
                lk[(int(t), int(i))] = (int(NL[k]), int(NY[k]), int(MC[k]))
        keys = set(cmap) | {k for k, v in att.items() if v[0]}
        for key in keys:
            kc = cmap.get(key)
            a, Fp = att.get(key, (False, None))
            F = Fc[kc] if kc is not None else Fp
            if kc is not None and Fp is not None and not np.array_equal(Fc[kc], Fp):
                chk['rung_mismatch'] += 1
            if a and kc is None and F[3]:
                chk['v1_R04_not_in_cand'] += 1
            jj, nown = J.get(key, (-1, -1))
            R['c'].append((cl[key[0]], a, jj, nown, *[bool(F[RUNG[r]]) for r in RUNG], *lk.get(key, (-1, -1, -1))))
        z.close()
    res = dict(n_files=len(files), checks=chk, classes={})
    rng = np.random.default_rng(20261119)
    for topo, R in rows.items():
        scl = np.concatenate(R['slot_cl'])
        ids, M = np.unique(scl, return_counts=True)
        C = np.array(R['c'], dtype=np.int64) if R['c'] else np.zeros((0, 7 + len(RUNG)), np.int64)
        ii = np.searchsorted(ids, C[:, 0])
        out = dict(n_slots=int(len(scl)), n_clusters=int(len(ids)))
        for q, r in enumerate(RUNG):
            p = C[:, 4 + q] == 1
            a = C[:, 1] == 1; rec = C[:, 2] >= 0; jy = C[:, 2] >= 4
            cnt = lambda m: np.bincount(ii[p & m], minlength=len(ids)).astype(float)
            Nv1, Nj, Nb, Nun = cnt(a), cnt(jy), cnt(a & jy), cnt(~rec)
            e = dict(N_v1=int(Nv1.sum()), N_j=int(Nj.sum()), N_both=int(Nb.sum()),
                     N_v1_only=int((Nv1 - Nb).sum()), N_j_only=int((Nj - Nb).sum()),
                     N_pass=int(p.sum()), N_pass_no_record=int(Nun.sum()), N_v1_no_record=int(cnt(a & ~rec).sum()),
                     clusters_with_v1=int((Nv1 > 0).sum()), clusters_with_j=int((Nj > 0).sum()),
                     j_hist_v1=np.bincount(C[p & a & rec, 2], minlength=8).tolist(),
                     j_hist_all_recorded=np.bincount(C[p & rec, 2], minlength=8).tolist(),
                     # links-based upper bound (v1 core links, pre-merge): j_link >= 4 needs max_cross >= 2 and >= 4 link layers
                     N_v1_link_ub=int((p & a & (C[:, 10] >= 2) & (C[:, 9] >= 4)).sum()),
                     N_v1_link_ub_clusters=int(len(np.unique(C[p & a & (C[:, 10] >= 2) & (C[:, 9] >= 4), 0]))),
                     max_cross_hist_v1=np.bincount(np.clip(C[p & a, 10], 0, 9), minlength=10).tolist(),
                     sum_links_v1_rec=int(C[p & a & rec, 8].sum()), sum_own_hits_v1_rec=int(C[p & a & rec, 3].sum()),
                     rate_v1=float(Nv1.sum() / M.sum()), rate_j=float(Nj.sum() / M.sum()))
            if e['N_v1'] > 0:
                e['ratio'] = e['N_j'] / e['N_v1']
                b = rng.integers(0, len(ids), (NBOOT, len(ids)))
                w = np.stack([np.bincount(x, minlength=len(ids)) for x in b]).astype(float)
                rv1 = w @ Nv1; rj = w @ Nj; ok = rv1 > 0
                rr = rj[ok] / rv1[ok]
                e['ratio_q16_50_84'] = np.quantile(rr, [0.16, 0.5, 0.84]).tolist()
                e['s_ln_ratio'] = float(np.std(np.log(rr[rr > 0]), ddof=1)) if (rr > 0).sum() > 10 else None
                e['frac_boot_ratio_zero'] = float((rr == 0).mean())
                e['s_rel_Nv1_clustered'] = float(np.std(rv1, ddof=1) / max(e['N_v1'], 1))
            out[r] = e
        res['classes'][topo] = out
    Path(outp).write_text(json.dumps(res, indent=1))
    sys.stdout.write(json.dumps(res) + '\n')


if __name__ == '__main__':
    main(*sys.argv[1:4])
