"""p2x_validate.py -- validation of the pilot code slices (and, later, of pilot files: the checks are per file).

  <acts python> p2x_validate.py <out.json> <partition.json> <file.npz> [...]

Per file, by meta['mode'] (no rung, no candidate, no selection quantity is formed):
  mbgen-x  pools inside their phase space, no NaN, parents per interaction against the partition file
  hspool   pool inside its phase space and inside the road, weights
  g4prod   stored class of every vertex == class recomputed from the stored vertex row (one class each: asserted in
           p2x_common.class_codes), classes inside the group, first-arc flag consistent with the class, offsets,
           yields per firing against the partition file (z-scores; complete classes of the pass only)
  b1x      the hard checks of Tatiana's hand-over validation (p2c_validate.one, imported: V4-1 closure, no NaN,
           offsets, distinct seeds, no parent hit beyond the vertex radius, no product hit before its production time),
           plus: class of every event recomputed from its stored Geant4 vertex row == stored class, class in the
           sample's class list, parent inside the sample's phase space, |road offset| < 0.15, every hit owned by the
           gun vertex, vertex-file provenance present; and (review of addendum v2, A-1) the Geant4 crossings of the
           parent before the vertex that have no Fatras parent hit: at most 2 % of the crossings, on all events
  hs0x     V4-1 closure, no NaN, offsets, distinct seeds, truth MET > filter, every written hit has a row in the
           particle table, summaries finite
Albert, 2026-11-16 (files written before that date are checked exactly as before):
  hspool-x the hard-scatter parent pools of p2a_hspool.py (phase space, road / off-road, weights, source files)
  b1x      files that carry the per-event array `ev_mode`: "no parent hit beyond the vertex radius" is required of the
           events whose parent has the radius cut (ev_mode 0); of the events with a time cut or the hybrid parent
           (ev_mode 1, 3) "no parent hit later than the vertex time" is required instead (a parent that has turned
           was at larger radii before its vertex).  The parent phase space and the road condition are those recorded
           in the vertex file's meta (pool selection, pool prefix), so the optional samples are checked against
           their own definition.
Reproducibility: files with the same (mode, stream, chunk, size, sample/group/pass, first vertex) must have the same
content hash; files of the same kind with another chunk must differ.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

import p2c_common as C
import p2x_common as X

log = C.setup_logging('p2x_validate')


def key_of(m):
    return (m['mode'], m.get('sample', m.get('group', '')), m.get('g4_pass', ''), m['stream'], m['chunk'],
            m.get('n_events', m.get('n_fire', m.get('n_int'))), m.get('first_vertex', 0), m.get('vertex_file', ''),
            m.get('pool_prefix', ''), m.get('trunc_mode', ''))


def chk_mb(z, m, part):
    r = {}
    for pre, lo, hi, emax in (('pool', 0.5, 20.0, 1.0), ('xpool', 0.3, 20.0, 1.5)):
        if f'{pre}_pt' not in z.files:
            continue
        pt = z[f'{pre}_pt']; eta = z[f'{pre}_eta']
        r[f'{pre}_in_phase_space'] = bool(len(pt) and pt.min() > lo - 1e-6 and pt.max() <= hi + 1e-6 and np.abs(eta).max() < emax)
        if pre == 'xpool':
            r['xpool_disjoint_from_pool'] = bool(not np.any((pt > np.float32(0.5001)) & (np.abs(eta) < 0.9999)))
        r[f'{pre}_nan'] = int(np.isnan(pt).sum() + np.isnan(eta).sum())
        r[f'{pre}_species_ok'] = bool(np.all(np.isin(np.abs(z[f'{pre}_pdg']), (211, 321, 2212, 130, 2112, 22))))
    n = m['n_int']; ref = part['pool_per_interaction']
    v1 = part['v1_rates']
    r.update(n_pool_per_interaction=m['n_pool_per_interaction'], n_lowpt_per_interaction=m['n_lowpt_per_interaction'],
             n_xpool_per_interaction=m['n_xpool_per_interaction'], n_fwd_per_interaction=m['n_fwd_per_interaction'],
             v1_dif_rate_x200=200 * m['rate_per_interaction_in_road']['dif'], v1_dif_rate_x200_partition=200 * v1['dif'],
             z_pool_vs_partition=float((m['n_pool'] - ref * n) / np.sqrt(ref * n * 2.0)),     # crude: clustered counts
             rate_v1=m['rate_per_interaction_in_road'], cpu_ms_per_interaction=m['cpu_ms_per_interaction'])
    r['hard'] = bool(r.get('pool_in_phase_space') and r.get('pool_nan') == 0 and r.get('pool_species_ok')
                     and r.get('xpool_in_phase_space', True) and r.get('xpool_nan', 0) == 0 and r.get('xpool_disjoint_from_pool', True)
                     and abs(m['rate_per_interaction_in_road']['dif'] / v1['dif'] - 1) < 0.15
                     and not np.isnan(z['hist']).any() and z['hist'].sum() > 0)
    return r


def chk_hspool(z, m, part):
    pt = z['pool_pt']; eta = z['pool_eta']; d = z['pool_dphi']; e = z['evt']
    r = dict(n_pool=int(len(pt)), in_phase_space=bool(len(pt) and pt.min() > 0.5 and pt.max() < 20 and np.abs(eta).max() < 1),
             in_road=bool(np.abs(d).max() < 0.15), nan=int(np.isnan(e).sum()), met_min=float(np.hypot(e[:, 0], e[:, 1]).min()),
             pool_in_road_per_event=m['pool_in_road_per_event'], pool_in_road_per_event_weighted=m['pool_in_road_per_event_weighted'],
             pool_any_phi_per_event=m['pool_any_phi_per_event'], mean_w=m['sum_w'] / m['n_events'],
             mean_pt=float(pt.mean()), cpu_ms_per_event=m['cpu_ms_per_event'],
             seeds_distinct=bool(len(np.unique(e[:, -2] + e[:, -1] * 2.0 ** 31)) == len(e)))
    r['hard'] = bool(r['in_phase_space'] and r['in_road'] and r['nan'] == 0 and r['met_min'] >= 200.0 and r['seeds_distinct'])
    return r


def chk_g4(z, m, part):
    import p2c_g4vtx as GV
    nm = GV.Names(); nm.proc = m['proc_names']; nm.vol = m['vol_names']
    V = z['vtx']; cls = z['cls']; src = z['src']
    code, fa = X.class_codes(V, nm)
    sc = {k: i for i, k in enumerate(m['src_cols'])}
    want_fa = {'dif': 1, 'difc': 0, 'ni22': 1, 'ni30': 1, 'ni61': 1, 'nix': 1, 'nic': 0}
    fa_ok = all(np.all(src[cls == X.CODE[k], sc['first_arc']] == v) for k, v in want_fa.items())
    r = dict(group=m['group'], g4_pass=m['g4_pass'], n_fire=m['n_fire'], n_vertices=int(len(V)), n_per_class=m['n_per_class'],
             class_recomputed_equal=bool(np.array_equal(code, cls)),
             class_in_group=bool(np.all(np.isin(cls, [X.CODE[c] for c in m['group_classes']]))),
             first_arc_consistent=bool(fa_ok and np.array_equal(fa.astype(float), src[:, sc['first_arc']])),
             offsets_ok=bool(z['prod_off'][-1] == len(z['prod']) and z['cross_off'][-1] == len(z['cross'])
                             and len(z['prod_off']) == len(V) + 1 and len(z['cross_off']) == len(V) + 1),
             nan=int(np.isnan(V).sum() + np.isnan(z['prod']).sum() + np.isnan(z['cross']).sum()),
             partition_sum_ok=bool(m['counts_sum'] == sum(t['all'] for t in m['counts'].values())),
             counts={k: t['all'] for k, t in m['counts'].items()}, g4_ms_per_firing=m['g4_ms_per_firing'],
             products_per_vertex=float(len(z['prod']) / max(len(V), 1)), crossings_per_vertex=float(len(z['cross']) / max(len(V), 1)),
             bytes_per_vertex=float(m['bytes'] / max(len(V), 1)), pool_rows_used=int(len(np.unique(src[:, sc['pool_row']] + 1e9 * src[:, sc['pool_file']]))),
             pool_prefix=m['pool_prefix'], pool_modes=sorted({str(pf['mode']) for pf in m['pool_files']}),
             pool_selection=m.get('pool_selection'), pool_draw=m.get('pool_draw', 'uniform'),
             pool_rows_in_pass=m.get('pool_rows_in_pass'), pool_rows_fired_distinct=m.get('pool_rows_fired_distinct'),
             firings_per_distinct_pool_row=m.get('firings_per_distinct_pool_row'), g4=m.get('g4'),
             w_src_min_max=[float(src[:, sc['w_src']].min()), float(src[:, sc['w_src']].max())] if len(src) else None)
    if m['pool_prefix'] == 'pool' and all(pf['mode'] == 'mbgen-x' for pf in m['pool_files']) and not m.get('pool_selection'):
        zs = {}
        for k in m['complete_classes']:
            a = m['counts'][k]['all']; b = part['counts'].get(k, {}).get('all', 0)
            pa = a / m['n_fire']; pb = b / part['n_fire']
            zs[k] = float((pa - pb) / np.sqrt(max(pa / m['n_fire'] + pb / part['n_fire'], 1e-30)))
        r['z_yield_vs_partition'] = zs
    r['hard'] = bool(r['class_recomputed_equal'] and r['class_in_group'] and r['first_arc_consistent'] and r['offsets_ok']
                     and r['nan'] == 0 and r['partition_sum_ok'])
    return r


BARREL_COUNT = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4'] + [f'{a}_L{k}_{s}' for a in ('TBPS', 'TB2S') for k in (1, 2, 3)
                                                                for s in ('in', 'out')]          # run_chain.py l.59-60
A1_MAX = 0.02      # review of addendum v2, A-1: Geant4 pre-vertex crossings without a Fatras parent hit, per stream


def parent_crossings(z, m):
    """All events with a charged parent: per counting surface, number of Geant4 crossings of the parent before the vertex
    against number of written Fatras parent hits (multiplicities, so a parent that crosses a layer twice counts twice)."""
    import p2c_validate as PV
    H = z['hits']; ho = z['hit_off']; ev = z['evt']; gc = z['gcross']; gco = z['gcross_off']
    col = {k: i for i, k in enumerate(m['columns'])}
    code_name = {v: k for k, v in m['surface_names'].items()}
    cnt_sid = {i for i, nm in PV.SID_NAME.items() if nm in BARREL_COUNT}
    both = og = of = nev = 0
    for i in range(len(ev)):
        if ev[i, 8] <= 0:
            continue
        nev += 1
        h = H[ho[i]:ho[i + 1]]
        par = (h[:, col['vsec']] == 0) & (h[:, col['gen']] == 0) & (h[:, col['particle']] == 1)
        nf = {}
        for sid in h[par, col['sid']].astype(int):
            if sid in cnt_sid:
                nf[PV.SID_NAME[sid]] = nf.get(PV.SID_NAME[sid], 0) + 1
        ng = {}
        for c in gc[gco[i]:gco[i + 1], 0].astype(int):
            nm = code_name[c]
            if nm in BARREL_COUNT:
                ng[nm] = ng.get(nm, 0) + 1
        for nm in set(nf) | set(ng):
            a, b = ng.get(nm, 0), nf.get(nm, 0)
            both += min(a, b); og += max(0, a - b); of += max(0, b - a)
    return dict(a1_events=nev, a1_both=both, a1_g4_without_fatras=og, a1_fatras_without_g4=of,
                a1_frac_g4_without_fatras=og / max(both + og, 1), a1_frac_fatras_without_g4=of / max(both + of, 1))


def chk_hspool_x(z, m, part):
    """Pools of p2a_hspool.py: `pool_*` inside the road of the event, `opool_*` outside; both in the pool phase space."""
    r = dict(n_events=m['n_events'], n_files=len(m['source_files']), sum_w=m['sum_w'], n_w_full=m['n_w_full'], n_w_low=m['n_w_low'])
    ok = True
    for pre, inroad in (('pool', True), ('opool', False)):
        if f'{pre}_pt' not in z.files:
            continue
        pt = z[f'{pre}_pt']; eta = z[f'{pre}_eta']; d = z[f'{pre}_dphi']; w = z[f'{pre}_w']
        r[f'n_{pre}'] = int(len(pt))
        r[f'{pre}_in_phase_space'] = bool(len(pt) and pt.min() > 0.5 and pt.max() < 20 and np.abs(eta).max() < 1)
        r[f'{pre}_road_ok'] = bool(np.all(np.abs(d) < 0.15) if inroad else np.all((np.abs(d) >= 0.15) & (np.abs(d) <= np.pi + 1e-6)))
        r[f'{pre}_species_ok'] = bool(np.all(np.isin(np.abs(z[f'{pre}_pdg']), (211, 321, 2212, 130, 2112, 22))))
        r[f'{pre}_nan'] = int(np.isnan(pt).sum() + np.isnan(eta).sum() + np.isnan(d).sum() + np.isnan(w).sum())
        r[f'{pre}_w_range'] = [float(w.min()), float(w.max())] if len(w) else None
        r[f'{pre}_per_event'] = float(len(pt) / m['n_events'])
        r[f'{pre}_per_event_weighted'] = float(w.sum() / max(m['sum_w'], 1e-300))
        r[f'{pre}_mean_pt'] = float(pt.mean()) if len(pt) else None
        ok = ok and r[f'{pre}_in_phase_space'] and r[f'{pre}_road_ok'] and r[f'{pre}_species_ok'] and r[f'{pre}_nan'] == 0 \
            and w.min() >= 0
    e = z['evt']
    r['events_distinct'] = bool(len(np.unique(e[:, 0] * 1e6 + e[:, 1])) == len(e))
    r['hard'] = bool(ok and r['events_distinct'] and len(e) == m['n_events'])
    return r


def per_mode_parent_checks(z, m):
    """For files with `ev_mode`: parent hits beyond the vertex radius in radius-mode events, and parent hits later
    than the vertex time (+ 0.010 ns, as p2c_validate.one) in the events with a time cut or the hybrid parent."""
    import p2c_validate as PV
    H = z['hits']; ho = z['hit_off']; T = z['tru']; G = z['gvtx']; vc = {k: i for i, k in enumerate(m['vcols'])}
    col = {k: i for i, k in enumerate(m['columns'])}; em = z['ev_mode']
    btl_sid = {i for i, nm in PV.SID_NAME.items() if nm == 'BTL'}
    beyond_r = late_t = nr = nt = 0
    for i in range(len(em)):
        if em[i] < 0:
            continue
        h = H[ho[i]:ho[i + 1]]; t = T[ho[i]:ho[i + 1]]
        par = (h[:, col['vsec']] == 0) & (h[:, col['gen']] == 0) & (h[:, col['particle']] == 1)
        if not par.any():
            continue
        g = G[i]
        if em[i] == 0:
            nr += 1
            beyond_r += int(np.sum(par & (np.hypot(t[:, 0], t[:, 1]) > np.hypot(g[vc['x']], g[vc['y']]) + 1e-3)))
        else:
            nt += 1
            notbtl = np.array([int(sd) not in btl_sid for sd in h[:, col['sid']]], bool)
            late_t += int(np.sum(par & notbtl & (h[:, col['t']] > g[vc['t']] + 0.010)))
    return dict(radius_mode_events_with_parent_hits=nr, time_mode_events_with_parent_hits=nt,
                parent_hits_beyond_vertex_radius_in_radius_mode=beyond_r, parent_hits_later_than_vertex_time_in_time_mode=late_t)


def chk_b1(path, z, m, part):
    import p2c_g4vtx as GV
    import p2c_validate as PV
    sys.path.insert(0, str(C.CODE))
    import s4pu
    r = PV.one(path)
    ev = z['evt']; ec = {k: i for i, k in enumerate(m['evt_cols'])}
    nm = GV.Names(); nm.proc = m['proc_names']; nm.vol = m['surface_names']
    code, fa = X.class_codes(z['gvtx'], nm)
    lo = 0.3 if m['sample'] == 'lowpt' else 0.5
    hi = 0.5 if m['sample'] == 'lowpt' else 20.0
    elo, ehi = 0.0, 1.0
    vm = m.get('vertex_file_meta', {})
    if vm.get('pool_selection'):                 # the phase space the Geant4 job selected from a wider pool
        ps = vm['pool_selection']
        lo, hi, elo, ehi = ps['pt_lo'], ps['pt_hi'], ps['abs_eta_lo'], ps['abs_eta_hi']
    offroad = vm.get('pool_prefix') == 'opool'
    pt = ev[:, ec['parent_pt0']]; aeta = np.abs(ev[:, ec['parent_eta0']]); ard = np.abs(ev[:, ec['road_dphi']])
    H = z['hits']; hc = {k: i for i, k in enumerate(m['columns'])}
    r.update(parent_crossings(z, m))
    r.update(trunc_mode=m.get('trunc_mode', 'radius'), a1_ok=bool(r['a1_frac_g4_without_fatras'] <= A1_MAX),
             sample=m['sample'], classes=m['classes'], n_per_class=m['n_per_class'],
             class_recomputed_equal=bool(np.array_equal(code, ev[:, ec['cls']].astype(np.int8))),
             class_in_sample=bool(np.all(np.isin(ev[:, ec['cls']], [X.CODE[c] for c in m['classes']]))),
             first_arc_equal=bool(np.array_equal(fa.astype(float), ev[:, ec['first_arc']])),
             parent_in_phase_space=bool(pt.min() > lo - 1e-5 and pt.max() < hi + 1e-5 and aeta.max() < ehi + 1e-6
                                        and aeta.min() >= elo - 1e-6),
             parent_phase_space_checked=dict(pt_lo=lo, pt_hi=hi, abs_eta_lo=elo, abs_eta_hi=ehi, offroad=offroad),
             road_offset_ok=bool(ard.min() >= 0.15 - 1e-6 and ard.max() <= np.pi + 1e-6) if offroad else bool(ard.max() < 0.15),
             hits_all_gun=bool(len(H) == 0 or np.all(H[:, hc['vp']] == s4pu.GUN_VP)),
             evt_nan=int(np.isnan(ev).sum()), provenance=bool(m.get('vertex_file_sha256') and m['vertex_file_meta'].get('content_sha256')),
             beta_min=m['beta_min'], bytes_per_event=float(m['bytes'] / m['n_events']), s_per_event=m['mean_s_per_event'],
             t_total_s=m['t_total_s'], mean_pt0=float(pt.mean()), frac_ckf_flag=float((H[:, hc['flag']] > 0).mean()) if len(H) else 0.0,
             vertex_r_q=[float(q) for q in np.quantile(ev[:, ec['vtx_r']], (0.05, 0.5, 0.95))],
             w_src_mean=float(ev[:, ec['w_src']].mean()), gcross_per_event=float(len(z['gcross']) / m['n_events']))
    radius_ok = r['parent_hits_beyond_vertex_radius'] == 0
    if 'ev_mode' in z.files:
        r.update(per_mode_parent_checks(z, m))
        r.update(seam_window_ns=m.get('seam_window_ns'), n_per_ev_mode=m.get('n_per_ev_mode'),
                 parent_hits_injected_per_event=float(z['n_parent_inj'].mean()),
                 ev_mode_consistent=bool(np.all((z['ev_mode'] >= 0) == (ev[:, 8] > 0))))
        radius_ok = (r['parent_hits_beyond_vertex_radius_in_radius_mode'] == 0
                     and r['parent_hits_later_than_vertex_time_in_time_mode'] == 0 and r['ev_mode_consistent'])
    r['parent_truncation_ok'] = bool(radius_ok)
    r['hard'] = bool(r['v41_pass'] and r['nan_hits'] == 0 and r['offsets_ok'] and r['seeds_distinct']
                     and radius_ok and r['product_hits_earlier_than_vertex'] == 0
                     and r['class_recomputed_equal'] and r['class_in_sample'] and r['first_arc_equal']
                     and r['parent_in_phase_space'] and r['road_offset_ok'] and r['hits_all_gun'] and r['evt_nan'] == 0
                     and r['provenance'] and r['mean_injected_slow'] == 0)
    r['hard_without_a1'] = r['hard']
    r['hard'] = bool(r['hard'] and r['a1_ok'])
    return r


def nu_met_ok(z, m):
    """The stored neutrino list reproduces the stored truth MET vector of every event (float32 list: 1e-3 relative)."""
    nu = z['nu']; off = z['nu_off']; ev = z['evt']
    idx = np.repeat(np.arange(len(ev)), np.diff(off))
    mx = np.bincount(idx, nu[:, 1] * np.cos(nu[:, 3]), minlength=len(ev)); my = np.bincount(idx, nu[:, 1] * np.sin(nu[:, 3]), minlength=len(ev))
    return np.allclose(mx, ev[:, 0], rtol=2e-3, atol=0.05) and np.allclose(my, ev[:, 1], rtol=2e-3, atol=0.05)


def chk_hs0(z, m, part):
    H = z['hits']; ho = z['hit_off']; ev = z['evt']; ec = {k: i for i, k in enumerate(m['evt_cols'])}
    n = m['n_events']; w = ev[:, ec['w_v1']]
    r = dict(sample=m['sample'], n_events=n, v41_pass=m['v41_pass'], nan_hits=int(np.isnan(H).sum()),
             offsets_ok=bool(ho[0] == 0 and ho[-1] == len(H) and np.all(np.diff(ho) >= 0) and len(ho) == n + 1),
             seeds_distinct=bool(len(np.unique(ev[:, -2] + ev[:, -1] * 2.0 ** 31)) == n),
             met_min=float(np.hypot(ev[:, 0], ev[:, 1]).min()), hits_without_particle_row=m['n_hits_without_particle_row'],
             summaries_nan=int(np.isnan(z['gsum']).sum() + np.isnan(z['jets10']).sum() + np.isnan(z['tau']).sum()
                               + np.isnan(z['part']).sum() + np.isnan(ev).sum() + np.isnan(z['had']).sum() + np.isnan(z['nu']).sum()),
             had_per_event=float(len(z['had']) / n), nu_per_event=float(len(z['nu']) / n),
             nu_sum_equals_met=bool(nu_met_ok(z, m)), gen_weight_all_one=bool(np.all(z['gsum'][:, m['gsum_cols'].index('gen_weight')] == 1.0)),
             pthat_min=float(z['gsum'][:, m['gsum_cols'].index('pthat')].min()),
             rss_note='max RSS and CPU are in the job marker',
             part_rows_per_event=float(len(z['part']) / n), part_hits_sum_equal=bool(z['part'][:, -1].sum() == len(H)),
             hits_per_event=float(len(H) / n), bytes_per_event=float(m['bytes'] / n), s_per_event=m['mean_s_per_event'],
             t_total_s=m['t_total_s'], tries_per_event=m['sum_tries'] / n, mean_w_v1=float(w.mean()),
             frac_w_full=float((w > 0.5).mean()), frac_w_low=float(((w > 0) & (w <= 0.5)).mean()),
             replaced_events=len(m['replaced_events']), n_tau=int(len(z['tau'])),
             jets10_per_event=float(len(z['jets10']) / n), jets20_per_event=float(len(z['jets']) / n))
    r['hard'] = bool(r['v41_pass'] and r['nan_hits'] == 0 and r['offsets_ok'] and r['seeds_distinct'] and r['met_min'] >= 200.0
                     and r['hits_without_particle_row'] == 0 and r['summaries_nan'] == 0 and r['part_hits_sum_equal']
                     and r['nu_sum_equals_met'] and r['pthat_min'] >= 150.0)
    return r


def main(out, part_file, files):
    part = json.loads(Path(part_file).read_text())
    res = []; groups = defaultdict(list); kinds = defaultdict(set)
    for f in files:
        z, m = C.load_job(f)
        mode = m['mode']
        m['bytes'] = Path(f).stat().st_size          # the size is known only after the file is written: not in its meta
        r = dict(file=str(f), mode=mode, stream=m['stream'], chunk=m['chunk'], content_sha256=m['content_sha256'], bytes=m['bytes'])
        arrays = {k: z[k] for k in z.files if k != 'meta'}
        r['content_hash_recomputed_equal'] = bool(X.content_sha256(arrays) == m['content_sha256'])
        del arrays
        if mode == 'mbgen-x':
            r.update(chk_mb(z, m, part))
        elif mode == 'hspool':
            r.update(chk_hspool(z, m, part))
        elif mode == 'hspool-x':
            r.update(chk_hspool_x(z, m, part))
        elif mode == 'g4prod':
            r.update(chk_g4(z, m, part))
        elif mode == 'b1x':
            r.update(chk_b1(f, z, m, part))
        elif mode == 'hs0x':
            r.update(chk_hs0(z, m, part))
        else:
            r['hard'] = False
        r['hard'] = bool(r['hard'] and r['content_hash_recomputed_equal'])
        res.append(r)
        k = key_of(m)
        groups[k].append((str(f), m['content_sha256']))
        kinds[(k[0], k[1], k[2], k[8], k[9])].add(m['content_sha256'])
        log.info('%s', json.dumps({a: b for a, b in r.items() if a not in ('file',)}, default=str))
    rep = [dict(key=[str(x) for x in k], files=[a for a, _ in v], identical=len({h for _, h in v}) == 1)
           for k, v in groups.items() if len(v) > 1]
    keys_per_kind = defaultdict(int)
    for k in groups:
        keys_per_kind[(k[0], k[1], k[2], k[8], k[9])] += 1
    diff = [dict(kind=[str(x) for x in kd], n_distinct_jobs=keys_per_kind[kd], n_distinct_hashes=len(hs),
                 all_different=len(hs) == keys_per_kind[kd]) for kd, hs in kinds.items() if keys_per_kind[kd] > 1]
    ok = all(r['hard'] for r in res)
    summary = dict(all_hard_checks_pass=bool(ok), n_files=len(res), files_failing=[r['file'] for r in res if not r['hard']],
                   reproducible_pairs=len(rep), all_reruns_identical=bool(rep and all(x['identical'] for x in rep)),
                   different_seed_groups=len(diff), all_different_seeds_differ=bool(diff and all(x['all_different'] for x in diff)),
                   reruns=rep, different_seeds=diff, files=res)
    Path(out + '.tmp').write_text(json.dumps(summary, indent=1, default=str))
    Path(out + '.tmp').replace(out)
    log.info('hard checks pass: %s; reruns identical: %s (%d groups); other seeds differ: %s (%d kinds)', ok,
             summary['all_reruns_identical'], len(rep), summary['all_different_seeds_differ'], len(diff))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
