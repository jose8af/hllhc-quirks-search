"""p3a_tables.py -- the decision-point-2 inputs of work package p3-a in one JSON and as markdown tables.  Aurora, 2026-11-24.

  <tt python> -I p3a_tables.py <p3a_counts.json> <p3a_rule1_dryrun.json | -> <p3a_indep_summary.json | -> <out.json> <out.md>

Reads only the result files of p3a_counts.py (and its row exports <counts.json>.rows_<label>.npz for the paired
comparisons between pool / PV variants on identical events), p3a_rule1_dryrun.py and p3a_indep_summary.py.  No pilot
file, no signal file.  Every number written is a count or simple arithmetic on counts (falls, ratios, 1/H).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

T2 = [('R07', 'R07', 0), ('R08 = R09 = R11', 'R08', 0), ('R14 = R17 = R20 = FB(4)', 'R08', 3),
      ('FB(0), width none', 'R04n', 3), ('FB(0), width 75 mm', 'R04w', 3), ('FB(1)', 'R05', 3), ('FB(2)', 'R06', 3),
      ('FB(3)', 'R07', 3)]
B1 = ['DIF', 'DIFC', 'NI22', 'NI30', 'NI61', 'NIX', 'NIC', 'HS', 'LOWPT']
U68 = -math.log(0.32)


def fmt(x):
    return f'{x:,}' if isinstance(x, int) else (f'{x:,.1f}' if abs(x) >= 100 else f'{x:.3g}')


def main(cin, din, iin, jout, mdout):
    C = json.loads(Path(cin).read_text())
    D = json.loads(Path(din).read_text()) if din != '-' else None
    IN = json.loads(Path(iin).read_text()) if iin != '-' else None
    L = C['labels']; m = L['m']
    R = C['readings']
    W = m['widths']
    md = []; J = dict(source=dict(counts=cin, dryrun=din, indep=iin), labels=sorted(L))
    P = md.append

    def tab(lab, rd, r_, wn, s, var='with'):
        return L[lab]['tables'][f'{rd}_{r_}_{wn}_s{s}_{var}']

    # ---- 1. m_H per term at every T2 candidate ----
    P('### T1. Ceiling counts m_H per term at every T2 candidate (label m: merged pool, PV draw; WITH flagged events)\n')
    P('| T2 candidate (width, s) | reading | Z full class (S / F) | Z 0.05 class (S / F) | ' + ' | '.join(B1) + ' |')
    P('|---|---|---|---|' + '---|' * len(B1))
    J['m_H'] = {}
    for cname, wn, s in T2:
        J['m_H'][cname] = {}
        for rd in R:
            tS = tab('m', rd, 'S', wn, s); tF = tab('m', rd, 'F', wn, s)
            J['m_H'][cname][rd] = dict(S=tS, F=tF)
            P(f"| {cname} ({wn}, s = {s}) | {rd} | {tS['Z']:,} / {tF['Z']:,} | {tS['Zlow']} / {tF['Zlow']} | "
              + ' | '.join(f"{tS[t]}" + (f" / {tF[t]}" if tF[t] != tS[t] else '') for t in B1) + ' |')
    # ---- 2. Z counts per width, all readings; falls ----
    P('\n### T2. Z(nunu) full-weight class per width, s = 0 and s = 3, every reading (S / F); label m\n')
    P('| reading | s | ' + ' | '.join(W) + ' |')
    P('|---|---|' + '---|' * len(W))
    J['Z_by_width'] = {}
    for rd in R:
        for s in (0, 3):
            row = [(tab('m', rd, 'S', wn, s)['Z'], tab('m', rd, 'F', wn, s)['Z']) for wn in W]
            J['Z_by_width'][f'{rd}_s{s}'] = {wn: dict(S=a, F=b) for wn, (a, b) in zip(W, row)}
            P(f'| {rd} | {s} | ' + ' | '.join(f'{a:,} / {b:,}' for a, b in row) + ' |')
    P('\n### T3. Fall per width step, Z(nunu) full class, s = 0 (count ratio wide / narrow); extrapolation R07 -> R08\n')
    P('| reading | R05/R06 | R06/R07 | R07/R08 | R07 count / (R06/R07 fall) [EST of R08] | R08 counted |')
    P('|---|---|---|---|---|---|')
    J['falls'] = {}
    for rd in R:
        for r_ in 'SF':
            c = {wn: tab('m', rd, r_, wn, 0)['Z'] for wn in W}
            if min(c['R06'], c['R07'], c['R08']) == 0:
                continue
            f1, f2, f3 = c['R05'] / c['R06'], c['R06'] / c['R07'], c['R07'] / c['R08']
            J['falls'][f'{rd}_{r_}'] = dict(R05_R06=f1, R06_R07=f2, R07_R08=f3, R08_extrapolated=c['R07'] / f2, R08=c['R08'])
            P(f"| {rd} ({r_}) | {f1:.2f} | {f2:.2f} | {f3:.2f} | {c['R07'] / f2:,.0f} | {c['R08']:,} |")
    # ---- 3. own-hit classes ----
    P('\n### T4. Own-hit classes: Z(nunu) full class by deficit k (reading BASE, S; label m)\n')
    P('| width | s = 0: k = 0 / 1 / 2 / 3 | s = 3: k = 0 / 1 / 2 / 3 / 4 / 5 |')
    P('|---|---|---|')
    J['by_k'] = {k: v for k, v in m['by_k'].items()}
    for wn in W:
        a = m['by_k'][f'BASE_S_{wn}_s0']; b = m['by_k'][f'BASE_S_{wn}_s3']
        P(f"| {wn} | " + ' / '.join(f'{a[str(k)]:,}' for k in range(4)) + ' | ' + ' / '.join(f'{b[str(k)]:,}' for k in range(6)) + ' |')
    P('\n### T5. k per layer type at s = 3 (k_IP, k_2S of the best witness; reading PLANS4 and OWN, S; R08 and R04w)\n')
    P('| reading, width | (k_IP, k_2S): count |')
    P('|---|---|')
    J['by_kip_k2s'] = m['by_kip_k2s']
    for rd in ('PLANS4', 'OWN', 'UNION'):
        for wn in ('R08', 'R04w'):
            t = m['by_kip_k2s'][f'{rd}_S_{wn}_s3']
            P(f'| {rd}, {wn} | ' + '; '.join(f'({k}): {v}' for k, v in sorted(t.items())) + ' |')
    # ---- 4. variants ----
    P('\n### T6. Variants at the T2 widths: Z(nunu) full class, reading BASE (S / F), each label\n')
    P('| label (pool, PV, files) | ' + ' | '.join(f'{wn} s={s}' for _, wn, s in T2) + ' | M (Z) | pilot files |')
    P('|---|' + '---|' * (len(T2) + 2))
    J['variants'] = {}
    for lab, v in L.items():
        row = [(tab(lab, 'BASE', 'S', wn, s)['Z'], tab(lab, 'BASE', 'F', wn, s)['Z']) for _, wn, s in T2]
        J['variants'][lab] = dict(options=v['options'], counts={c[0]: dict(S=a, F=b) for c, (a, b) in zip(T2, row)},
                                  M_Z=v['M'].get('Z'), n_Z_files=v['n_files']['Z'])
        o = v['options']
        P(f"| {lab} ({'not merged' if o['no_merge'] else 'merged'}, PV {o['pv']}, w {o['w_select']}) | "
          + ' | '.join(f'{a:,} / {b:,}' for a, b in row) + f" | {v['M'].get('Z', 0):,.1f} | {v['n_files']['Z']} Z + "
          f"{v['n_pilot_files'] - v['n_files']['Z']} |")
    # paired comparisons on identical (file, event): label x against label m
    P('\n### T7. Paired comparison with label m on the same pilot files (Z full class, BASE S): counted in both / only m / only variant\n')
    P('| variant | width, s | both | only m | only variant | m on these files | variant |')
    P('|---|---|---|---|---|---|---|')
    J['paired'] = {}

    def keyset(lab, wn, s, rd='BASE', ri=0):
        z = np.load(cin + f'.rows_{lab}.npz')
        Kk = z['K'][list(z['readings']).index(rd)][:, list(z['widths']).index(wn), 0 if s == 0 else 1, ri]
        ok = (z['term'] == 'Z') & (Kk <= (3 if s == 0 else 5))
        paths = z['paths']
        return {(str(paths[a]), int(b)) for a, b in zip(z['path_idx'][ok], z['event'][ok])}, {str(p) for p in paths}
    for lab in L:
        if lab in ('m', 'm0'):
            continue
        for cname, wn, s in T2:
            a, pa = keyset('m', wn, s); b, pb = keyset(lab, wn, s)
            a = {x for x in a if x[0] in pb} if L[lab]['n_files']['Z'] < 460 else a
            J['paired'][f'{lab}|{cname}'] = dict(both=len(a & b), only_m=len(a - b), only_variant=len(b - a), m=len(a), variant=len(b))
            P(f'| {lab} | {wn}, s = {s} | {len(a & b):,} | {len(a - b)} | {len(b - a)} | {len(a):,} | {len(b):,} |')
    # ---- 4b. is a hard-window count a ceiling for finder-type full sets? ----
    z = np.load(cin + '.rows_m.npz')
    zt = z['term'] == 'Z'
    wl = list(z['widths']); cats = list(z['cats']); rdl = list(z['readings'])
    P('\n### T7b. Full sets judged as the finder judges them (c0, finder axis, w_core < W) against the other readings; Z full class, s = 0, S\n')
    P('| width | c0 counted (k <= 3) | of them without a HARD witness (k <= 3) | without an OWN witness | BASE counted | BASE without OWN | BASE without HARD |')
    P('|---|---|---|---|---|---|---|')
    J['c0_vs_readings'] = {}
    for wn in wl:
        wi = wl.index(wn)
        c0 = zt & (z['KC'][:, cats.index('c0'), wi, 0, 0] <= 3)
        hard = z['K'][rdl.index('HARD')][:, wi, 0, 0] <= 3
        own = z['K'][rdl.index('OWN')][:, wi, 0, 0] <= 3
        base = zt & (z['K'][rdl.index('BASE')][:, wi, 0, 0] <= 3)
        J['c0_vs_readings'][wn] = dict(c0=int(c0.sum()), c0_not_hard=int((c0 & ~hard).sum()), c0_not_own=int((c0 & ~own).sum()),
                                       base=int(base.sum()), base_not_own=int((base & ~own).sum()), base_not_hard=int((base & ~hard).sum()))
        d = J['c0_vs_readings'][wn]
        P(f"| {wn} | {d['c0']:,} | {d['c0_not_hard']:,} | {d['c0_not_own']:,} | {d['base']:,} | {d['base_not_own']:,} | {d['base_not_hard']:,} |")
    # off-road orientations and multi-orientation events in the B1 class streams (ADD l.384-390)
    nz = ~np.isin(z['term'], ['Z', 'Zlow', 'Zzero'])
    J['b1_rows'] = [dict(term=str(t_), file=str(z['paths'][p_]).split('/')[-1], event=int(e_), orient=int(o_), n_early_prod=int(n_),
                         kb_S_s0={wn: int(z['K'][0][i, wl.index(wn), 0, 0]) for wn in wl},
                         kb_S_s3={wn: int(z['K'][0][i, wl.index(wn), 1, 0]) for wn in wl},
                         union_S_s0={wn: int(z['K'][rdl.index('UNION')][i, wl.index(wn), 0, 0]) for wn in wl},
                         union_S_s3={wn: int(z['K'][rdl.index('UNION')][i, wl.index(wn), 1, 0]) for wn in wl})
                    for i, (t_, p_, e_, o_, n_) in enumerate(zip(z['term'], z['path_idx'], z['event'], z['orient'], z['n_early_prod'])) if nz[i]]
    P('\n### T7c. Every stored row of the B1 / hs / lowpt samples (any k within k_max at any width in any category)\n')
    P('| term | file | event | orientation | flagged | BASE S k at s = 0 (R04n..R08) | BASE S k at s = 3 | UNION S s = 0 | UNION S s = 3 |')
    P('|---|---|---|---|---|---|---|---|---|')
    for r in J['b1_rows']:
        P(f"| {r['term']} | {r['file']} | {r['event']} | {r['orient']} | {r['n_early_prod']} | " + ' / '.join(str(v) for v in r['kb_S_s0'].values())
          + ' | ' + ' / '.join(str(v) for v in r['kb_S_s3'].values()) + ' | ' + ' / '.join(str(v) for v in r['union_S_s0'].values())
          + ' | ' + ' / '.join(str(v) for v in r['union_S_s3'].values()) + ' |')
    # ---- 5. flagged events ----
    P('\n### T8. Flagged events (n_early_prod > 0): events per stream, and counted rows WITH minus WITHOUT (all readings, widths, s)\n')
    diff = {t: 0 for t in C['terms']}
    for name, t in m['tables'].items():
        if name.endswith('_with'):
            o = m['tables'][name[:-5] + '_without']
            for k in t:
                diff[k] = max(diff[k], t[k] - o[k])
    J['flagged'] = dict(events=m['M_flagged_events'], max_with_minus_without=diff)
    P('| term | ' + ' | '.join(B1) + ' |')
    P('|---|' + '---|' * len(B1))
    P('| flagged events | ' + ' | '.join(f"{int(m['M_flagged_events'][t])}" for t in B1) + ' |')
    P('| largest WITH - WITHOUT count in any table | ' + ' | '.join(str(diff[t]) for t in B1) + ' |')
    # ---- 6. enrichment 1/H(R06) ----
    P('\n### T9. H(R06) and the enrichment E = 1/H(R06) per term (s = 0; BASE S; H = Gamma(m + 1)/M: mean (m + 1)/M; m = 0: 68 % upper value 1.14/M)\n')
    P('| term | m(R06) | M | H(R06) mean | E = 1/H | m(R07) | m(R08) |')
    P('|---|---|---|---|---|---|---|')
    J['enrichment_R06'] = {}
    for t in ['Z'] + B1:
        mm = tab('m', 'BASE', 'S', 'R06', 0)[t]; M = m['M'][t]
        if not M:
            continue
        H = (mm + 1) / M
        J['enrichment_R06'][t] = dict(m=mm, M=M, H_mean=H, E=1 / H, H_68=(U68 / M if mm == 0 else None),
                                      m_R07=tab('m', 'BASE', 'S', 'R07', 0)[t], m_R08=tab('m', 'BASE', 'S', 'R08', 0)[t])
        P(f"| {t} | {mm:,} | {M:,.1f} | {H:.3g} | {1 / H:,.0f}" + (f' (>= {M / U68:,.0f} at 68 %)' if mm == 0 else '')
          + f" | {tab('m', 'BASE', 'S', 'R07', 0)[t]:,} | {tab('m', 'BASE', 'S', 'R08', 0)[t]:,} |")
    # ---- 7. hand-over census ----
    P('\n### T10. Hand-over variant per stream as recorded in the pilot files (label m)\n')
    P('| stream | files | trunc_mode | events per mode (-1 neutral, 0 radius, 3 hybrid) | beta_min |')
    P('|---|---|---|---|---|')
    J['handover'] = m['handover']
    for st, h in sorted(m['handover'].items()):
        P(f"| {st} | {h['n_files']} | {h['trunc_mode']} | {h['n_per_ev_mode']} | {h['beta_min']} |")
    # ---- 8. checks, regression, witness composition ----
    J['regression_phase2'] = {k: v for k, v in m.get('regression_phase2', {}).items()}
    J['checks'] = {lab: v['checks'] for lab, v in L.items()}
    J['witness_Z_R08'] = m['witness_Z_target']
    J['weighted_m_Z'] = {k: m['weighted_m_Z'][k] for k in ('BASE_S_R08_s0', 'BASE_F_R08_s0', 'BASE_S_R07_s0', 'BASE_S_R08_s3')}
    J['z'] = {lab: v['z'] for lab, v in L.items()}
    J['cpu_s_in_jobs'] = {lab: v['cpu_s_in_jobs'] for lab, v in L.items()}
    J['n_non_Z_dumps'] = len(m['dumps'])
    # ---- 9. independent search ----
    if IN:
        P('\n### T11. Independent search (Nils\'s code) on the counted Z events of every 2nd pilot file\n')
        P('| width, s, reading | counted (Phase-2 rows) | confirmed (verified witness, k <= k_max) | of which k same or lower | not found | with a hard-window witness (S only) |')
        P('|---|---|---|---|---|---|')
        J['independent'] = IN
        for k in sorted(IN['tables']):
            t = IN['tables'][k]
            P(f"| {k} | {t['counted']:,} | {t['confirmed']:,} ({100 * t['confirmed'] / max(t['counted'], 1):.1f} %) | {t['same_or_lower']:,} | {t['not_found']} | "
              + (f"{t['hard']:,}" if k.endswith('S') else '') + ' |')
    # ---- 10. dry run ----
    if D:
        P('\n### T12. Rule-1 projection, DRY RUN, **NOT BINDING** (' + D['tag'] + ')\n')
        P('| T2 candidate | pile-up row | reading | m_Z (S) | B50 (S) [16-84 %] | m_Z (F) | B50 (F) | pauses |')
        P('|---|---|---|---|---|---|---|---|')
        J['dryrun'] = {}
        dm = D['labels']['m']['readings']
        cands = []
        for k in dm:
            c = k.split('|')[2]
            if c not in cands:
                cands.append(c)
        for c in cands:
            for rd in R:
                vS = dm[f'{rd}|S|{c}|with']; vF = dm[f'{rd}|F|{c}|with']
                for p in vS['by_pileup']:
                    a = vS['by_pileup'][p]; b = vF['by_pileup'][p]
                    J['dryrun'][f'{c}|{p}|{rd}'] = dict(m_Z_S=vS['counts']['Z'][0], B50_S=a['B50'], q16_S=a['q16'], q84_S=a['q84'],
                                                       m_Z_F=vF['counts']['Z'][0], B50_F=b['B50'], pauses=a['pauses'] and b['pauses'],
                                                       min_draw_S=a['min_draw'], mc_err_S=a['mc_err'])
                    P(f"| {c} | {p} | {rd} | {vS['counts']['Z'][0]:,} | {a['B50']:,.0f} [{a['q16']:,.0f}-{a['q84']:,.0f}] | "
                      f"{vF['counts']['Z'][0]:,} | {b['B50']:,.0f} | {'yes' if a['pauses'] and b['pauses'] else 'NO'} |")
        allp = [x for lab in D['labels'].values() for v in lab['readings'].values() for x in v['by_pileup'].values()]
        J['dryrun_summary'] = dict(n_readings=len(allp), n_pause=sum(x['pauses'] for x in allp), min_B50=min(x['B50'] for x in allp),
                                   max_B50=max(x['B50'] for x in allp), limit=D['limit'], tag=D['tag'])
        P(f"\nAll labels, readings, candidates, pile-up rows, flagged variants: {len(allp)} projections, {sum(x['pauses'] for x in allp)} "
          f"at or above {D['limit']:.1f}; smallest B50 {min(x['B50'] for x in allp):,.0f}, largest {max(x['B50'] for x in allp):,.0f}.")
        wv = [(k, v) for lab in D['labels'].values() for k, v in lab['readings'].items()]
        dmax = 0.0
        for k, v in dm.items():
            if k.endswith('|with'):
                o = dm[k[:-5] + '|without']
                for p in v['by_pileup']:
                    dmax = max(dmax, abs(v['by_pileup'][p]['B50'] - o['by_pileup'][p]['B50']))
        J['dryrun_summary']['max_abs_with_minus_without_B50'] = dmax
        P(f'Largest |B50(WITH) - B50(WITHOUT flagged events)| over label m: {dmax:.3f} events.')
        del wv
    Path(jout).write_text(json.dumps(J, indent=1, default=float))
    Path(mdout).write_text('\n'.join(md) + '\n')


if __name__ == '__main__':
    main(*sys.argv[1:6])
