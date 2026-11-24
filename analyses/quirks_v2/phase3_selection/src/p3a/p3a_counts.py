"""p3a_counts.py -- counts of the FINAL pilot classification per term, width, s, reading and variant.  Aurora, 2026-11-24.

  <tt python> -I p3a_counts.py <out.json> <label>=<dir[,dir..]> [<label>=<dir> ...] [--phase2 <dir,dir,...>]
              [--expect-files label=N ...]

<dir> may be a glob pattern (e.g. .../p3-a-clsxz/000/*.m.npz).
label = a campaign of p3a_subset.py outputs (m = merged pool / PV draw / all streams; u = pool not merged; pv0 = true
vertex; pv2 = other PV seed).  Every pilot file must occur exactly once per label and completely.
Readings formed here from the stored categories (none is chosen here; see the artifact for what each one is):
  BASE    kb            p2w_subset.plane_best unchanged (Phase 2 "as produced": mixed axis convention, its heuristic)
  PLANS4  min(c0, c3)   full set with the finder's axis, else the PLAN-S4 centres as written
  OWN     min(c1..c4)   one single own-axis convention (full set and subsets), all searches
  HARD    c4            hard window (every IP hit of the subset inside 2W/1.4826)
  UNION   min(all)      information: best lower bound over both axis conventions and all searches
Terms: DIF (dif + k0l), DIFC, NI22, NI30, NI61, NIX, NIC, HS, LOWPT; Z (w_v1 >= 0.5), Zlow (0 < w_v1 < 0.5), Zzero
(w_v1 = 0: in no term under v1 weights; kept for a v2 MET-model weight).  m = number of (event, orientation) with
k <= floor(n/2) (3 at s = 0, 5 at s = 3).  'with' = all events, 'without' = events with n_early_prod > 0 removed.
"""
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np

log = logging.getLogger('p3a_counts')
STREAM_TERM = {'pilot.c0.dif': 'DIF', 'pilot.c0.difc': 'DIFC', 'pilot.c0.ni22': 'NI22', 'pilot.c0.ni30': 'NI30',
               'pilot.c0.ni61': 'NI61', 'pilot.c0.nix': 'NIX', 'pilot.c0.nic': 'NIC', 'pilot.c0.hs': 'HS',
               'pilot.c0.lowpt': 'LOWPT'}
TERMS = ['DIF', 'DIFC', 'NI22', 'NI30', 'NI61', 'NIX', 'NIC', 'HS', 'LOWPT', 'Z', 'Zlow', 'Zzero']
READINGS = ['BASE', 'PLANS4', 'OWN', 'HARD', 'UNION']
KMAX = (3, 5)
P2_W = ['R04', 'R05', 'R06', 'R07', 'R08']
P2_MAP = [0, 2, 3, 4, 5]


def load(dirs):
    """-> dict(rows_i, rows_f, term (per row), path (per row), meta info)."""
    fs = sorted(f for d in dirs.split(',') for f in glob.glob(d if '*' in d else str(Path(d) / '*.npz')))
    seen = {}
    RI = []; RF = []; term = []; rpath = []
    M = {t: 0.0 for t in TERMS}; Mfl = {t: 0.0 for t in TERMS}; nfiles = {t: 0 for t in TERMS}
    zi = dict(n_gen=0, n_full=0, n_low=0, n_zero=0, sum_w_full=0.0, sum_w_low=0.0, w_max=0.0, sum_w_writer=0.0,
              n_used=0)
    hand = {}; opts = None; cols = None; shas = set(); p2sha = set(); cpu = 0.0; nerr = 0; dumps = []
    tot = {}
    for f in fs:
        z = np.load(f)
        m = json.loads(str(z['meta']))
        if opts is None:
            opts = m['options']; cols = (m['i_cols'], m['f_cols']); wn = m['wnames']; cats = m['cats']
        elif m['options'] != opts or (m['i_cols'], m['f_cols']) != cols:
            raise SystemExit(f'{f}: options or columns differ within one label')
        shas.add(m['script_sha256']); p2sha.add(m['p2w_subset_sha256']); cpu += m['cpu_s']; nerr += m['n_errors']
        for k, v in m['totals'].items():
            tot[k] = max(tot.get(k, 0), v) if k.startswith('max') else tot.get(k, 0) + v
        ri = z['rows_i']; rf = z['rows_f']
        tof = {}
        for fi, fm in enumerate(m['files']):
            if fm['path'] in seen:
                raise SystemExit(f"{fm['path']} classified twice: {seen[fm['path']]} and {f}")
            seen[fm['path']] = f
            if fm['n_classified_range'] != fm['n_events']:
                raise SystemExit(f"{f}: partial file {fm['path']}")
            if fm['stream'] == 'pilot.hs0.znn':
                tof[fi] = 'Z'
                zi['n_gen'] += fm['n_events']; zi['n_full'] += fm['n_full']; zi['n_low'] += fm['n_low']
                zi['n_zero'] += fm['n_zero']; zi['sum_w_full'] += fm['sum_w_full']; zi['sum_w_low'] += fm['sum_w_low']
                zi['w_max'] = max(zi['w_max'], fm['w_max']); zi['sum_w_writer'] += fm['sum_w_v1'] or 0.0
                zi['n_used'] += fm['n_used']
                nfiles['Z'] += 1
                if fm['mu'] != 0.0:
                    raise SystemExit(f"{fm['path']}: mu = {fm['mu']}, not a no-pile-up file")
            else:
                t = STREAM_TERM[fm['stream']]
                tof[fi] = t
                M[t] += fm['n_events']; Mfl[t] += fm['n_early_events']; nfiles[t] += 1
            h = hand.setdefault(fm['stream'], dict(n_files=0, trunc_mode={}, beta_min={}, n_per_ev_mode={}, handover={},
                                                   mode={}))
            h['n_files'] += 1
            for key in ('trunc_mode', 'beta_min', 'handover', 'mode'):
                h[key][str(fm.get(key))] = h[key].get(str(fm.get(key)), 0) + 1
            for k, v in (fm.get('n_per_ev_mode') or {}).items():
                h['n_per_ev_mode'][k] = h['n_per_ev_mode'].get(k, 0) + v
        for d in m['dumps']:
            d['job'] = Path(f).name
            dumps.append(d)
        if len(ri):
            w = rf[:, cols[1].index('w')]
            for i in range(len(ri)):
                t = tof[int(ri[i, 0])]
                if t == 'Z':
                    t = 'Z' if w[i] >= 0.5 else ('Zlow' if w[i] > 0 else 'Zzero')
                term.append(t); rpath.append(m['files'][int(ri[i, 0])]['path'])
            RI.append(ri); RF.append(rf)
        z.close()
    ni = len(cols[0])
    RI = np.concatenate(RI) if RI else np.zeros((0, ni), np.int32)
    RF = np.concatenate(RF) if RF else np.zeros((0, len(cols[1])))
    return dict(RI=RI, RF=RF, term=np.array(term), path=np.array(rpath), M=M, Mfl=Mfl, nfiles=nfiles, z=zi, hand=hand,
                opts=opts, icols=cols[0], fcols=cols[1], wn=wn, cats=cats, n_outputs=len(fs), n_pilot_files=len(seen),
                script_sha256=sorted(shas), p2w_sha256=sorted(p2sha), cpu_s=cpu, n_errors=nerr, dumps=dumps, totals=tot)


def karrays(L):
    """-> K[reading] (nrow, nW, 2, 2) and KIP[reading] (nrow, nW, 2) (k_IP of the s = 3 best witness; BASE: -1)."""
    ic = L['icols']; RI = L['RI']; nW = len(L['wn']); nc = len(L['cats'])
    i0 = ic.index('kb_' + L['wn'][0] + '_s0_S')
    kb = RI[:, i0:i0 + nW * 4].reshape(-1, nW, 2, 2)
    j0 = i0 + nW * 4
    KC = RI[:, j0:j0 + nc * nW * 4].reshape(-1, nc, nW, 2, 2)
    l0 = j0 + nc * nW * 4
    KI = RI[:, l0:l0 + nc * nW * 2].reshape(-1, nc, nW, 2)
    assert ic[l0] == f"kip_{L['cats'][0]}_{L['wn'][0]}_S" and ic[j0] == f"k_{L['cats'][0]}_{L['wn'][0]}_s0_S"

    def comb(idx):
        k = KC[:, idx].min(1)
        # k_IP of the best s = 3 witness over the categories: lexicographic (k, k_IP)
        key = KC[:, idx][:, :, :, 1, :].astype(np.int64) * 1000 + KI[:, idx]
        return k, (key.min(1) % 1000)
    K = {}; KIP = {}
    K['BASE'] = kb; KIP['BASE'] = np.full((len(RI), nW, 2), -1)
    K['PLANS4'], KIP['PLANS4'] = comb([0, 3])
    K['OWN'], KIP['OWN'] = comb([1, 2, 3, 4])
    K['HARD'], KIP['HARD'] = comb([4])
    ku, kiu = comb([0, 1, 2, 3, 4])
    K['UNION'] = np.minimum(ku, kb); KIP['UNION'] = kiu
    return K, KIP, KC


def count_label(L):
    K, KIP, KC = karrays(L)
    RI = L['RI']; ic = L['icols']; term = L['term']
    nep = RI[:, ic.index('n_early_prod')]
    w = L['RF'][:, L['fcols'].index('w')]
    wmax = L['z']['w_max']
    out = dict(tables={}, by_k={}, by_kip_k2s={}, weighted_m_Z={}, checks={})
    for rd_name in READINGS:
        for wi, wn in enumerate(L['wn']):
            for si, s in enumerate((0, 3)):
                for ri_, r_ in enumerate('SF'):
                    k = K[rd_name][:, wi, si, ri_]
                    ok = k <= KMAX[si]
                    for var, keep in (('with', np.ones(len(k), bool)), ('without', nep == 0)):
                        name = f'{rd_name}_{r_}_{wn}_s{s}_{var}'
                        out['tables'][name] = {t: int((ok & keep & (term == t)).sum()) for t in TERMS}
                    name = f'{rd_name}_{r_}_{wn}_s{s}'
                    zf = ok & (term == 'Z')
                    out['by_k'][name] = {str(kk): int((zf & (k == kk)).sum()) for kk in range(KMAX[si] + 1)}
                    out['weighted_m_Z'][name] = float(w[zf].sum() / wmax) if wmax else None
                    if si == 1 and rd_name != 'BASE':
                        kip = KIP[rd_name][:, wi, ri_]
                        tab = {}
                        for a in range(0, 6):
                            for b in range(0, 4):
                                n = int((zf & (kip == a) & (k - kip == b)).sum())
                                if n:
                                    tab[f'{a},{b}'] = n
                        out['by_kip_k2s'][name] = tab
    # C2 of the plan: relations that hold by construction, counted (not removed)
    nW = len(L['wn'])
    c = out['checks']
    c['width_monotone_violations_c0_c1'] = int(sum((KC[:, cc, wi] > KC[:, cc, wi + 1]).sum() for cc in (0, 1)
                                                  for wi in range(nW - 1)))
    c['width_nonmonotone_rows_BASE'] = int(((K['BASE'][:, :-1] > K['BASE'][:, 1:]).any((1, 2, 3))).sum())
    c['width_nonmonotone_rows_OWN'] = int(((K['OWN'][:, :-1] > K['OWN'][:, 1:]).any((1, 2, 3))).sum())
    c['HARD_below_OWN'] = int((K['HARD'] < K['OWN']).sum())
    c['c0c2_above_BASE'] = int((np.minimum(KC[:, 0], KC[:, 2]) > K['BASE']).sum())
    c['F_below_S'] = int(sum((K[r][..., 1] < K[r][..., 0]).sum() for r in READINGS))
    # witness summary at the target (Z full class rows with a witness k <= 3)
    wk = RI[:, ic.index('wit_k')]
    zf = (term == 'Z') & (wk <= 3)
    g = lambda n: RI[zf, ic.index(n)]      # noqa: E731
    out['witness_Z_target'] = dict(
        n=int(zf.sum()), n_two_particles=int((g('wit_npart') == 2).sum()), n_three_particles=int((g('wit_npart') == 3).sum()),
        n_with_product_hit=int((g('wit_nprod') > 0).sum()), n_with_fatras_made_hit=int((g('wit_ngen') > 0).sum()),
        n_all_hits_ckf=int((g('wit_nckf') == g('wit_nhit')).sum()), n_half_hits_ckf=int((2 * g('wit_nckf') >= g('wit_nhit')).sum()),
        n_no_hit_ckf=int((g('wit_nckf') == 0).sum()))
    return out, K


def regress_phase2(L, K, p2dirs):
    """BASE rows against the Phase-2 rows of p2w_subset.py, events with w > 0, widths R04(none), R05..R08."""
    theirs = {}
    for d in p2dirs.split(','):
        for f in sorted(glob.glob(str(Path(d) / '*.npz'))):
            z = np.load(f); m = json.loads(str(z['meta'])); r = z['rows']; rc = m['row_cols']
            k0 = rc.index('k_R04_s0_S')
            for x in r:
                key = (m['files'][int(x[0])]['path'], int(x[1]), int(x[2]))
                if key in theirs:
                    raise SystemExit(f'Phase-2 row twice: {key}')
                theirs[key] = x[k0:k0 + 20].astype(np.int64)
            z.close()
    RI = L['RI']; w = L['RF'][:, L['fcols'].index('w')]
    kb = K['BASE'][:, P2_MAP].reshape(len(RI), -1)
    mine = {}
    for i in range(len(RI)):
        if w[i] > 0:
            mine[(L['path'][i], int(RI[i, 1]), int(RI[i, 2]))] = kb[i]
    n_equal = 0; diff = []; only_theirs = []; only_mine = 0
    for key, v in theirs.items():
        u = mine.get(key)
        if u is None:
            only_theirs.append(list(key))
        elif (u == v).all():
            n_equal += 1
        else:
            diff.append([list(key), v.tolist(), u.tolist()])
    kmx = np.tile(np.repeat(np.array(KMAX), 2), 5)
    for key, u in mine.items():
        if key not in theirs and (u <= kmx).any():
            only_mine += 1
    return dict(n_phase2_rows=len(theirs), n_equal=n_equal, n_different=len(diff), different=diff[:50],
                n_only_phase2=len(only_theirs), only_phase2=only_theirs[:50],
                n_only_mine_with_a_phase2_width_k_le_kmax=only_mine,
                passes=bool(len(diff) == 0 and len(only_theirs) == 0 and only_mine == 0))


def main(argv):
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    out_path = argv[0]
    labels = {}; p2 = None; expect = {}
    it = iter(argv[1:])
    for a in it:
        if a == '--phase2':
            p2 = next(it)
        elif a == '--expect-files':
            k, v = next(it).split('='); expect[k] = int(v)
        else:
            k, v = a.split('=', 1); labels[k] = v
    res = dict(readings=READINGS, terms=TERMS, kmax=KMAX, labels={})
    for lab, dirs in labels.items():
        L = load(dirs)
        if lab in expect and L['n_pilot_files'] != expect[lab]:
            raise SystemExit(f"label {lab}: {L['n_pilot_files']} pilot files, expected {expect[lab]}")
        cnt, K = count_label(L)
        z = L['z']
        M = dict(L['M'])
        if z['w_max']:
            M['Z'] = z['sum_w_full'] / z['w_max']; M['Zlow'] = M['Z']
        r = dict(options=L['opts'], n_outputs=L['n_outputs'], n_pilot_files=L['n_pilot_files'], n_files=L['nfiles'],
                 n_rows=int(len(L['RI'])), n_errors=L['n_errors'], cpu_s_in_jobs=L['cpu_s'], totals=L['totals'],
                 script_sha256=L['script_sha256'], p2w_subset_sha256=L['p2w_sha256'], widths=L['wn'], M=M,
                 M_flagged_events=L['Mfl'], z=z, handover=L['hand'], dumps=L['dumps'], **cnt)
        if p2 and lab == 'm':
            r['regression_phase2'] = regress_phase2(L, K, p2)
            log.info('regression against Phase 2: %s', {k: v for k, v in r['regression_phase2'].items()
                                                       if not isinstance(v, list)})
        res['labels'][lab] = r
        # row-level export (for a recount of m and M under other per-event weights, see p3a_rule1_dryrun.py)
        paths = sorted(set(L['path'].tolist()))
        pix = {p_: i for i, p_ in enumerate(paths)}
        np.savez_compressed(str(out_path) + f'.rows_{lab}.npz', paths=np.array(paths),
                            path_idx=np.array([pix[p_] for p_ in L['path']], np.int32), event=L['RI'][:, 1],
                            orient=L['RI'][:, 2], term=L['term'], w=L['RF'][:, L['fcols'].index('w')],
                            n_early_prod=L['RI'][:, L['icols'].index('n_early_prod')], readings=np.array(READINGS),
                            widths=np.array(L['wn']), K=np.stack([K[r_] for r_ in READINGS]).astype(np.int8),
                            cats=np.array(L['cats']), KC=karrays(L)[2].astype(np.int8),
                            wit=L['RI'][:, L['icols'].index('wit_k'):].astype(np.int16))
        for n in ('BASE_S_R08_s0_with', 'BASE_F_R08_s0_with', 'BASE_S_R08_s3_with', 'OWN_S_R08_s0_with',
                  'HARD_S_R08_s0_with', 'PLANS4_S_R08_s0_with', 'UNION_S_R08_s0_with', 'BASE_S_R04w_s3_with'):
            log.info('%s %s %s', lab, n, {t: v for t, v in cnt['tables'][n].items() if v})
        log.info('%s checks %s', lab, cnt['checks'])
    Path(out_path).write_text(json.dumps(res, indent=1, default=float))


if __name__ == '__main__':
    main(sys.argv[1:])
