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
           gun vertex, vertex-file provenance present
  hs0x     V4-1 closure, no NaN, offsets, distinct seeds, truth MET > filter, every written hit has a row in the
           particle table, summaries finite
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
            m.get('pool_prefix', ''))


def chk_mb(z, m, part):
    r = {}
    for pre, lo, hi in (('pool', 0.5, 20.0), ('lowpt', m['lowpt_phase_space']['pt'][0], 0.5)):
        if f'{pre}_pt' not in z.files:
            continue
        pt = z[f'{pre}_pt']; eta = z[f'{pre}_eta']
        r[f'{pre}_in_phase_space'] = bool(len(pt) and pt.min() > lo - 1e-6 and pt.max() <= hi + 1e-6 and np.abs(eta).max() < 1.0)
        r[f'{pre}_nan'] = int(np.isnan(pt).sum() + np.isnan(eta).sum())
        r[f'{pre}_species_ok'] = bool(np.all(np.isin(np.abs(z[f'{pre}_pdg']), (211, 321, 2212, 130, 2112, 22))))
    n = m['n_int']; ref = part['pool_per_interaction']
    r.update(n_pool_per_interaction=m['n_pool_per_interaction'], n_lowpt_per_interaction=m['n_lowpt_per_interaction'],
             z_pool_vs_partition=float((m['n_pool'] - ref * n) / np.sqrt(ref * n * 2.0)),     # crude: clustered counts
             rate_v1=m['rate_per_interaction_in_road'], cpu_ms_per_interaction=m['cpu_ms_per_interaction'])
    r['hard'] = bool(r.get('pool_in_phase_space') and r.get('pool_nan') == 0 and r.get('pool_species_ok')
                     and r.get('lowpt_in_phase_space', True) and r.get('lowpt_nan', 0) == 0)
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
             bytes_per_vertex=float(m['bytes'] / max(len(V), 1)), pool_rows_used=int(len(np.unique(src[:, sc['pool_row']] + 1e9 * src[:, sc['pool_file']]))))
    if m['pool_prefix'] == 'pool' and all(pf['mode'] == 'mbgen-x' for pf in m['pool_files']):
        zs = {}
        for k in m['complete_classes']:
            a = m['counts'][k]['all']; b = part['counts'].get(k, {}).get('all', 0)
            pa = a / m['n_fire']; pb = b / part['n_fire']
            zs[k] = float((pa - pb) / np.sqrt(max(pa / m['n_fire'] + pb / part['n_fire'], 1e-30)))
        r['z_yield_vs_partition'] = zs
    r['hard'] = bool(r['class_recomputed_equal'] and r['class_in_group'] and r['first_arc_consistent'] and r['offsets_ok']
                     and r['nan'] == 0 and r['partition_sum_ok'])
    return r


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
    pt = ev[:, ec['parent_pt0']]
    H = z['hits']; hc = {k: i for i, k in enumerate(m['columns'])}
    r.update(sample=m['sample'], classes=m['classes'], n_per_class=m['n_per_class'],
             class_recomputed_equal=bool(np.array_equal(code, ev[:, ec['cls']].astype(np.int8))),
             class_in_sample=bool(np.all(np.isin(ev[:, ec['cls']], [X.CODE[c] for c in m['classes']]))),
             first_arc_equal=bool(np.array_equal(fa.astype(float), ev[:, ec['first_arc']])),
             parent_in_phase_space=bool(pt.min() > lo - 1e-5 and pt.max() < hi + 1e-5 and np.abs(ev[:, ec['parent_eta0']]).max() < 1.0 + 1e-6),
             road_offset_ok=bool(np.abs(ev[:, ec['road_dphi']]).max() < 0.15),
             hits_all_gun=bool(len(H) == 0 or np.all(H[:, hc['vp']] == s4pu.GUN_VP)),
             evt_nan=int(np.isnan(ev).sum()), provenance=bool(m.get('vertex_file_sha256') and m['vertex_file_meta'].get('content_sha256')),
             beta_min=m['beta_min'], bytes_per_event=float(m['bytes'] / m['n_events']), s_per_event=m['mean_s_per_event'],
             t_total_s=m['t_total_s'], mean_pt0=float(pt.mean()), frac_ckf_flag=float((H[:, hc['flag']] > 0).mean()) if len(H) else 0.0,
             vertex_r_q=[float(q) for q in np.quantile(ev[:, ec['vtx_r']], (0.05, 0.5, 0.95))],
             w_src_mean=float(ev[:, ec['w_src']].mean()), gcross_per_event=float(len(z['gcross']) / m['n_events']))
    r['hard'] = bool(r['v41_pass'] and r['nan_hits'] == 0 and r['offsets_ok'] and r['seeds_distinct']
                     and r['parent_hits_beyond_vertex_radius'] == 0 and r['product_hits_earlier_than_vertex'] == 0
                     and r['class_recomputed_equal'] and r['class_in_sample'] and r['first_arc_equal']
                     and r['parent_in_phase_space'] and r['road_offset_ok'] and r['hits_all_gun'] and r['evt_nan'] == 0
                     and r['provenance'] and r['mean_injected_slow'] == 0)
    return r


def chk_hs0(z, m, part):
    H = z['hits']; ho = z['hit_off']; ev = z['evt']; ec = {k: i for i, k in enumerate(m['evt_cols'])}
    n = m['n_events']; w = ev[:, ec['w_v1']]
    r = dict(sample=m['sample'], n_events=n, v41_pass=m['v41_pass'], nan_hits=int(np.isnan(H).sum()),
             offsets_ok=bool(ho[0] == 0 and ho[-1] == len(H) and np.all(np.diff(ho) >= 0) and len(ho) == n + 1),
             seeds_distinct=bool(len(np.unique(ev[:, -2] + ev[:, -1] * 2.0 ** 31)) == n),
             met_min=float(np.hypot(ev[:, 0], ev[:, 1]).min()), hits_without_particle_row=m['n_hits_without_particle_row'],
             summaries_nan=int(np.isnan(z['gsum']).sum() + np.isnan(z['jets10']).sum() + np.isnan(z['tau']).sum()
                               + np.isnan(z['part']).sum() + np.isnan(ev).sum()),
             part_rows_per_event=float(len(z['part']) / n), part_hits_sum_equal=bool(z['part'][:, -1].sum() == len(H)),
             hits_per_event=float(len(H) / n), bytes_per_event=float(m['bytes'] / n), s_per_event=m['mean_s_per_event'],
             t_total_s=m['t_total_s'], tries_per_event=m['sum_tries'] / n, mean_w_v1=float(w.mean()),
             frac_w_full=float((w > 0.5).mean()), frac_w_low=float(((w > 0) & (w <= 0.5)).mean()),
             replaced_events=len(m['replaced_events']), n_tau=int(len(z['tau'])),
             jets10_per_event=float(len(z['jets10']) / n), jets20_per_event=float(len(z['jets']) / n))
    r['hard'] = bool(r['v41_pass'] and r['nan_hits'] == 0 and r['offsets_ok'] and r['seeds_distinct'] and r['met_min'] >= 200.0
                     and r['hits_without_particle_row'] == 0 and r['summaries_nan'] == 0 and r['part_hits_sum_equal'])
    return r


def main(out, part_file, files):
    part = json.loads(Path(part_file).read_text())
    res = []; groups = defaultdict(list); kinds = defaultdict(set)
    for f in files:
        z, m = C.load_job(f)
        mode = m['mode']
        r = dict(file=str(f), mode=mode, stream=m['stream'], chunk=m['chunk'], content_sha256=m['content_sha256'], bytes=m['bytes'])
        arrays = {k: z[k] for k in z.files if k != 'meta'}
        r['content_hash_recomputed_equal'] = bool(X.content_sha256(arrays) == m['content_sha256'])
        del arrays
        if mode == 'mbgen-x':
            r.update(chk_mb(z, m, part))
        elif mode == 'hspool':
            r.update(chk_hspool(z, m, part))
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
        kinds[(k[0], k[1], k[2], k[8])].add(m['content_sha256'])
        log.info('%s', json.dumps({a: b for a, b in r.items() if a not in ('file',)}, default=str))
    rep = [dict(key=[str(x) for x in k], files=[a for a, _ in v], identical=len({h for _, h in v}) == 1)
           for k, v in groups.items() if len(v) > 1]
    keys_per_kind = defaultdict(int)
    for k in groups:
        keys_per_kind[(k[0], k[1], k[2], k[8])] += 1
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
