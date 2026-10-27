"""stage5/make_placeholder_inputs.py -- SYNTHETIC Stage-4 outputs matching acts/stage4/analysis/inputs/schema.json
(version 1), to exercise stage5/make_figures.py before the real Stage-4 results exist.

EVERY NUMBER WRITTEN HERE IS MADE UP (smooth toy functions + a seeded RNG).  Nothing is read from production data,
no signal efficiency or limit is computed from any real sample.  Every JSON carries label 'PLACEHOLDER ...' and
placeholder = true, so every figure made from it is stamped PLACEHOLDER.

Read-only use of frozen code: the rung / fallback column names are imported from acts.stage4.analysis (constants
only, bytecode writing disabled); the files are checked with run_all.validate_outputs (the Stage-4 schema checker).

Also writes <out>/proposed/*: inputs that the Stage-5 figure list needs but schema.json (v1) does NOT define
(detector-level edges, sep_IT^det calibration, trigger+preselection acceptance, an event display).  Their format is
the PROPOSED extension in stage5/proposed_schema.json.

Run (from theory_track/):  nice -n 15 pixi run python stage5/make_placeholder_inputs.py [--out stage5/placeholder_inputs]
                           [--grid c1|full]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TT = HERE.parent
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C            # noqa: E402  (constants only)
from acts.stage4.analysis import signal as SG           # noqa: E402  (FB_NAMES only)
from acts.stage4.analysis.run_all import validate_outputs  # noqa: E402

LAB = 'PLACEHOLDER (synthetic Stage-4 outputs made by stage5/make_placeholder_inputs.py; NOT A RESULT)'
SEED = 424242
C1_POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]
C1_LAMS = [0.45, 0.6, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0]
FULL_MASSES = list(range(200, 1501, 100))
FULL_LAMS = [0.3, 0.45, 0.6, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
FB_COLS = [f + '&h>5&o>5' for f in SG.FB_NAMES]


def jdump(o, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, indent=1))


def cp68(k, n):
    lo, hi = C.clopper_pearson(np.atleast_1d(k), max(n, 1))
    return [float(lo[0]), float(hi[0])]


def toy_eps(m, lam):
    """Made-up smooth efficiency at R_A: rises in ln(Lambda) above a toy edge, falls slowly above 10 keV."""
    edge = 0.55 * (m / 500) ** 0.25
    return 0.55 / (1 + np.exp(-3.0 * np.log(lam / edge))) / (1 + (lam / 25.0) ** 2)


def toy_ladder(m, lam):
    """Cumulative toy efficiencies for the 23 ladder rungs (monotone non-increasing)."""
    e0 = toy_eps(m, lam) / 0.9
    f = np.ones(23)
    f[:4] = [1.0, 0.98, 0.95, 0.9]
    wfac = 1 / (1 + (1.0 / lam) ** 2)                 # toy: width rungs cost more at small Lambda
    for i, k in enumerate(range(4, 8)):
        f[k] = f[k - 1] * (0.95 - 0.12 * (i + 1) * (1 - wfac))
    for k, x in zip(range(8, 23), [0.97, 0.95, 0.92, 0.97, 0.95, 0.93, 0.97, 0.95, 0.9, 0.97, 0.95, 0.9,
                                   0.85 if m >= 500 else 0.3, 0.7 if m >= 900 else 0.2, 0.6 if m >= 1100 else 0.1]):
        f[k] = f[k - 1] * x
    f[4:] = np.minimum.accumulate(f[4:])
    return np.clip(e0 * f, 0, 1)


def tab(names, eps, n, rng):
    out = {}
    for nm, e in zip(names, eps):
        k = int(rng.binomial(n, min(max(e, 0.0), 1.0)))
        out[nm] = dict(k=k, eps=k / n if n else None, cp68=cp68(k, n))
    return out


def adm_toy(m, lam):
    lr = 0.43 * (m / 200) ** 0.28                      # toy Lambda_R(m), not the frozen table
    k = max([kk for kk in range(5) if kk == 0 or lam >= lr * 2 ** ((kk + 1) / 2)])
    e = (2.0 if m >= 1100 else 1.6 if m >= 900 else 1.3 if m >= 500 else None) if k == 4 else None
    fb = f'FB{k}' + (f'e>{e:g}' if e is not None else '')
    return dict(k_adm=k, k_adm_table=None, k_consistent=True, e_adm=e, fb_column=fb, r_fb=fb + '&h>5&o>5',
                width_cut_mm=C.W_K[k - 1] if k >= 1 else None)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'placeholder_inputs'))
    ap.add_argument('--grid', default='c1', choices=('c1', 'full'))
    a = ap.parse_args(argv)
    out = Path(a.out)
    if not out.is_absolute():
        out = TT / out
    if 'acts_stage4' in str(out) or 'acts/stage4' in str(out):
        raise SystemExit('REFUSED: placeholders are never written under acts/stage4 or data/acts_stage4')
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    pts = ([(s, m, l) for s, m in C1_POINTS for l in C1_LAMS] if a.grid == 'c1' else
           [('F', m, l) for m in FULL_MASSES for l in FULL_LAMS] + [('S', m, l) for m in (200, 500, 1000)
                                                                    for l in FULL_LAMS])
    nden = 1000 if a.grid == 'c1' else 200
    sha0 = {'stage5/make_placeholder_inputs.py': C.sha256(Path(__file__))}

    # ------------------------------------------------------------------ manifest.json
    jdump(dict(label=LAB, placeholder=True, dev=False, created='synthetic', campaigns=['PLACEHOLDER'], t_seed=4,
               governing_documents={}, analysis_code_sha256=sha0, input_sha256={}, status={}, inputs={},
               ambiguities=[], analysis_map=[], grid=a.grid), out / 'manifest.json')

    # ------------------------------------------------------------------ signal_eff.json + npz
    sig = dict(label=LAB, placeholder=True, admissibility={}, admissibility_inputs_sha256={})
    kind_pts = {'a2': pts, 'a1': pts[:: max(1, len(pts) // 10)], 'a5': pts[:: max(1, len(pts) // 5)]}
    obs = {k: [] for k in ('key', 'row', 'cand', 'met', 'phimet_reco', 'eta_axis', 'eta_pair', 'dedx', 'w_core', 'h',
                           'o', 'beta_tof', 'dt_earliest', 'M_est', 'f_ckf', 't_pv', 't_raw_in', 'pv', 'normal',
                           'axis', 'L', 'FB')}
    rows = {}
    srt = dict(window_ns=[2.0, 25.0], points={})
    for kind, kp in kind_pts.items():
        P = {}
        for s, m, l in kp:
            key = f'{kind.upper()}|{s}|{m:g}|{l:g}|BM'
            n = nden if kind == 'a2' else 200
            lad = toy_ladder(m, l) * (0.8 if s == 'S' else 1.0) * (1.15 if kind == 'a1' else 1.0)
            ad = adm_toy(m, l)
            fbe = np.array([lad[13] * (0.9 ** (k + 1)) * (1.0 if 'e>' not in nm else 0.6)
                            for k, nm in [(int(nm[2]), nm) for nm in SG.FB_NAMES]])
            ladder = tab(C.LADDER_NAMES, lad, n, rng)
            t = dict(sample=kind.upper(), spin=s, m=float(m), lam=float(l), cfg='BM', n_den=n, ladder=ladder,
                     ladder_T_present=tab(C.LADDER_NAMES, lad * 0.6, n, rng),
                     fallback=tab(FB_COLS, fbe, n, rng), fallback_T_present=tab(FB_COLS, fbe * 0.6, n, rng),
                     injob_columns=tab(C.RUNGS, np.interp(np.arange(43), np.arange(23), lad), n, rng),
                     lower_bound_columns=[C.RUNGS[i] for i in (0, 1, 2, 3)] + C.RUNGS[37:] + C.LADDER_NAMES[:4])
            t['report_rungs'] = {k: ladder[C.LADDER_NAMES[i]] for k, i in
                                 (('R_A', 3), ('R_B', 5), ('R_C', 7), ('R_D', 13), ('R_E', 22))}
            P[key] = t
            sig['admissibility'][f'{s}|{m:g}|{l:g}'] = ad
            if kind == 'a2':
                ne = int(rng.binomial(n, lad[3]))
                bg = 0.9 * (m / 500) ** -0.6 * (1 + 0.05 * rng.standard_normal(ne))       # toy beta*gamma
                met = np.abs(rng.normal(450 + 0.3 * m, 120, ne))
                eta = rng.normal(0, 0.5, ne)
                Lm = rng.random((ne, 23)) < (lad / max(lad[3], 1e-9))[None, :]
                Lm = np.logical_and.accumulate(Lm, axis=1)
                FBm = rng.random((ne, 20)) < (fbe / max(lad[3], 1e-9))[None, :]
                for i in range(ne):
                    obs['key'].append(key); obs['row'].append(i); obs['cand'].append(0)
                    obs['met'].append(met[i]); obs['phimet_reco'].append(rng.uniform(-np.pi, np.pi))
                    obs['eta_axis'].append(eta[i]); obs['eta_pair'].append(eta[i] + rng.normal(0, 0.05))
                    obs['dedx'].append(1.0 + 0.8 / max(bg[i], 0.2) ** 2 * 0.5); obs['w_core'].append(8 / l ** 2)
                    obs['h'].append(rng.exponential(8)); obs['o'].append(rng.exponential(8))
                    obs['beta_tof'].append(bg[i] / np.sqrt(1 + bg[i] ** 2))
                    obs['dt_earliest'].append(rng.exponential(5)); obs['f_ckf'].append(rng.beta(1, 12))
                    obs['M_est'].append(m * rng.lognormal(0, 0.15)); obs['t_pv'].append(rng.normal(0, 0.15))
                    obs['t_raw_in'].append(rng.exponential(10)); obs['pv'].append(rng.normal(0, [0.01, 0.01, 50]))
                    obs['normal'].append([0, 0, 1.0]); obs['axis'].append([1.0, 0, 0])
                    obs['L'].append(Lm[i]); obs['FB'].append(FBm[i])
                rows[f'{key}|rows'] = np.arange(n)
                for mk, w in (('L', 23), ('LT', 23), ('FB', 20), ('P', 43)):
                    rows[f'{key}|{mk}'] = rng.random((n, w)) < 0.3
                srt['points'][key] = dict(
                    n_den=n, ladder_SRT={nm: dict(k=v['k'] // 2, eps=v['k'] // 2 / n) for nm, v in ladder.items()},
                    fallback_SRT={nm: dict(k=v['k'] // 2, eps=v['k'] // 2 / n) for nm, v in t['fallback'].items()},
                    n_earliest_oot=int(rng.integers(0, 5)))
        sig[kind] = dict(n_files=len(kp), checks={}, self_consistency={}, points=P)
    jdump(sig, out / 'signal_eff.json')
    arr = {k: np.array(v) for k, v in obs.items()}
    arr['L_names'] = np.array(C.LADDER_NAMES)
    arr['FB_names'] = np.array(SG.FB_NAMES)
    np.savez_compressed(out / 'signal_obs_a2.npz', **arr)
    np.savez_compressed(out / 'signal_rows_a2.npz', **rows)
    jdump(dict(srt, label=LAB, placeholder=True), out / 'signal_srt.json')

    # ------------------------------------------------------------------ background.json
    x = np.arange(1, 44)
    p_direct = 0.3 * np.exp(-0.9 * (x - 1))                     # toy fake rate per trial vs column
    cols, es = [], []
    for i, nm in enumerate(C.RUNGS):
        nb1 = 20000 * 4 * p_direct[i]
        cols.append(dict(column=nm, B1_groups=float(rng.poisson(nb1)), B1_per_trial=float(rng.poisson(nb1) / 8e4),
                         P_thin=float(p_direct[i] * np.exp(rng.normal(0, 0.15))), s_ln_thin_boot=0.2,
                         B2_groups=float(max(1, 5000 * 2 * p_direct[i] * 1e3)), reachable_rho2=bool(i < 12),
                         P_main=float(p_direct[i] * np.exp(rng.normal(0, 0.1))), s_ln_main=0.25,
                         main_method='thinning' if i < 12 else 'factorisation (PLACEHOLDER)', zero_branch=False,
                         P_fact=float(p_direct[i] * 1.3), P_pow=float(p_direct[i]) if nb1 >= 10 else None))
        sl = 0.3 + 0.12 * i
        es.append(dict(column=nm, P_per_trial=float(p_direct[i] * 1.1), base=float(p_direct[i]),
                       base_method='thinning', closure_factor=1.0, trend_factor=1.0, closure_parts={}, T3='not factorised',
                       T3_factor=1.0, sigma_ln=sl, sigma_ln_components=dict(stat=0.2, model_spread=0.1, closure=sl * 0.5,
                                                                           trend=0, density=0.3, normalisation=0.2624,
                                                                           T3=0),
                       closure_factor_note='PLACEHOLDER', reachable_rho2=bool(i < 12), zero_branch=False))
    tpts = [dict(col=c, rung=C.RUNGS[c], x=c + 1, ln_r=float(rng.normal(0.05 * (c - 3), 0.12)), sig=0.15,
                 z=float(rng.normal()), N_obs=float(p_direct[c] * 8e4), N_pred=float(p_direct[c] * 8e4 * 0.95))
            for c in range(3, 12)]
    bkg = dict(label=LAB, placeholder=True, samples=dict(B1_trials=80000, B1_events=20000, B2_trials=10000,
                                                         B2_events=5000),
               closure=dict(T1=dict(test='T1', r1='R04_IP2>=7', ln_r=0.1, z=0.7, branch='nominal'),
                            T1w=dict(test='T1w', branch='nominal'), T1e=dict(test='T1e', branch='-> T3'),
                            trend=dict(points=tpts, slope=0.05, s_slope_boot=0.03, significant=False),
                            T1_governing_branch='nominal'),
               T3=dict(note='PLACEHOLDER'), c_test=dict(note='PLACEHOLDER'), reach={}, density=dict(available=False),
               rho_dens=dict(available=False), columns=cols, end_state=es, end_state_T=[dict(e, P_per_trial=e[
                   'P_per_trial'] * 0.02) for e in es], f1_factors={}, sm=None, cprime=None)
    jdump(bkg, out / 'background.json')
    jdump(dict(label=LAB, placeholder=True, edges=dict(t_min_ns=2.0, t_max_ns=25.0, R0_window=[2, 25],
                                                      R1_window=[2, 25], Rm_window_k_le_m1=[2, 25]),
               columns={nm: dict(own={}, late_population={}, P_late=dict(N=1, M=100), oot_population={},
                                 P_oot=dict(N=1, M=100, n_km=0), sigma_ln_PV=0.1, sigma_ln_sigma_t=0.1)
                        for nm in C.RUNGS}, kernel_check={}), out / 'srt.json')

    # ------------------------------------------------------------------ bsum_wp.json
    ntrig = 3.6e7
    lad = {'T': [], 'G': [], 'FB': {}}
    for c, f in (('T', 0.02), ('G', 1.0)):
        for r in range(1, 24):
            med = float(ntrig * p_direct[min(r - 1, 42)] * f * 10 ** (-0.35 * max(r - 14, 0)))
            sl = 0.4 + 0.08 * r
            lad[c].append(dict(rung=r, name=C.LADDER_NAMES[r - 1], B84=med * np.exp(sl), B_median=med, B_mean=med *
                               np.exp(sl ** 2 / 2), zero_branch=False,
                               terms=[dict(label='B_PU (PLACEHOLDER)', value=med, comps={}, zero_branch=False)]))
    for i, nm in enumerate(FB_COLS):
        lad['FB'][nm] = {c: dict(B84=0.5 * 3 ** -i * f * 4, B_median=0.5 * 3 ** -i * f, B_mean=0.6 * 3 ** -i * f,
                                 terms=[]) for c, f in (('T', 0.05), ('G', 1.0))}
    lad['missing_inputs'] = []
    lad['complete'] = True
    b84T = [x['B84'] for x in lad['T']]
    b84G = [x['B84'] for x in lad['G']]
    rT = next((i + 1 for i, v in enumerate(b84T) if v <= 0.11), None)
    rG = next((i + 1 for i, v in enumerate(b84G) if v <= 0.11), None)
    rule = dict(r_star_T=rT, r_star_G=rG, wp=dict(T=rT, G=rG, branch='PLACEHOLDER'), complete_inputs=True)
    jdump(dict(label=LAB, placeholder=True, n_trig=dict(value=ntrig), ladder=lad, rule=rule), out / 'bsum_wp.json')

    # ------------------------------------------------------------------ limits.json + workspaces
    lim = dict(label=LAB, placeholder=True, flags=['PLACEHOLDER: synthetic numbers'], points={})
    (out / 'workspaces').mkdir(exist_ok=True)
    for key, t in sig['a2']['points'].items():
        ad = sig['admissibility'][f"{t['spin']}|{t['m']:g}|{t['lam']:g}"]
        pr = {}
        s, b, sg, names = [], [], [], []
        for c in ('T', 'G'):
            r = rule['wp'][c]
            k_r = 0 if r is None or r <= 4 else min(4, r - 4)
            if r is not None and k_r <= ad['k_adm'] and r < 21:
                pr[c] = dict(kind='r*', rung=r, name=C.LADDER_NAMES[r - 1], background_free_claim=True)
                eps = t['ladder'][C.LADDER_NAMES[r - 1]]['eps']; bb = lad[c][r - 1]
            else:
                pr[c] = dict(kind='r_fb', rung=None, name=ad['r_fb'] + ('&SR-T' if c == 'T' else ''),
                             background_free_claim=False, why='no WP' if r is None else 'r* not admissible')
                eps = t['fallback'][ad['r_fb']]['eps']; bb = lad['FB'][ad['r_fb']][c]
            eps = (eps or 0) * (0.5 if c == 'T' else 0.5)
            s.append(eps); b.append(bb['B_median']); sg.append(float(np.log(bb['B84'] / bb['B_median'])))
            names.append(pr[c]['name'])
        pr['branch'] = 'PLACEHOLDER'
        pr['admissibility'] = ad
        ent = dict(primary=pr, s=s, b=b, sigma_ln=sg, selections=names)
        st = sum(s)
        if st > 0:
            med = (3.0 + 1.64 * np.sqrt(sum(b)) * 1.3) / st
            ent['expected_toys'] = dict(median=float(med), calculator='PLACEHOLDER', primary=True)
            ent['expected_asymptotic'] = dict(median=float(med * 0.93), band_1s=[float(med * 0.66), float(med * 1.45)],
                                              band_2s=[float(med * 0.48), float(med * 2.1)], calculator='PLACEHOLDER',
                                              primary=False)
            ent['expected_primary'] = float(med)
            ent['discovery'] = dict(mu_3events=None, mu_5sigma=float(med * 1.8))
        lim['points'][key] = ent
        jdump(dict(channels=[], observations=[], version='1.0.0', measurements=[], _placeholder=True),
              out / 'workspaces' / f"{key.replace('|', '_')}.json")
    lim['n_points'] = len(lim['points'])
    jdump(lim, out / 'limits.json')

    # ------------------------------------------------------------------ proposed extensions (NOT in schema v1)
    prop = out / 'proposed'
    ed = dict(label=LAB, placeholder=True, schema='stage5/proposed_schema.json#edges_det', points={})
    sp = dict(label=LAB, placeholder=True, schema='stage5/proposed_schema.json#sep_it_det', points={})
    ac = dict(label=LAB, placeholder=True, schema='stage5/proposed_schema.json#acceptance', points={})
    for s, m in sorted({(s, m) for s, m, _ in pts}):
        ed['points'][f'{s}|{m:g}'] = dict(
            lower=dict(value=float(0.55 * (m / 500) ** 0.25 * 1.4), stat_err=0.05, definition='eps = 50 % of plateau',
                       b84_label=None),
            upper=dict(value=float(18 * (m / 500) ** 0.2), stat_err=1.0, definition='merging', b84_label=None))
    for key, t in sig['a2']['points'].items():
        tr = 25.0 / t['lam'] ** 2
        sp['points'][key] = dict(sep_truth_median_mm=tr, sep_det_median_mm=float(tr * 1.08 + 0.4), err_mm=0.05 * tr + 0.1,
                                 n=int(t['report_rungs']['R_A']['k']))
        ac['points'][key] = dict(A_trig_presel=float(0.05 + 0.08 * (t['m'] / 1500)), err_rel=0.05)
    jdump(ed, prop / 'edges_det.json')
    jdump(sp, prop / 'sep_it_det.json')
    jdump(ac, prop / 'acceptance.json')
    # toy event display: PU hits on barrel layers + a coplanar quirk ribbon + the best PU fake candidate
    R = np.array([30, 61, 104, 158, 231, 351, 509, 685, 900, 1080])
    xs, ys, zs, cl = [], [], [], []
    for r in R:
        nh = int(4000 * (30 / r) ** 1.2)
        ph = rng.uniform(-np.pi, np.pi, nh)
        xs += list(r * np.cos(ph)); ys += list(r * np.sin(ph)); zs += list(rng.uniform(-1200, 1200, nh)); cl += [0] * nh
        for sgn in (+1, -1):                      # quirk pair: two arms bending around the MET direction phi = 0.6
            phi = 0.6 + sgn * 0.08 * np.sin(r / 180.0)
            xs.append(r * np.cos(phi)); ys.append(r * np.sin(phi)); zs.append(0.2 * r); cl.append(1)
        phf = -2.0 + rng.normal(0, 0.03)          # best PU fake
        xs.append(r * np.cos(phf)); ys.append(r * np.sin(phf)); zs.append(rng.uniform(-300, 300)); cl.append(2)
    np.savez_compressed(prop / 'event_display.npz', x=np.array(xs), y=np.array(ys), z=np.array(zs), cls=np.array(cl),
                        met_phi=np.array(0.6), cls_names=np.array(['PU hit', 'quirk hit (truth)', 'best PU fake']),
                        label=np.array(LAB))

    chk = validate_outputs(out)
    bad = {k: v for k, v in chk.items() if v != 'ok'}
    print('schema check (run_all.validate_outputs):', 'ALL OK' if not bad else bad, f'({len(chk)} files)')
    print(f'{len(pts)} points ({a.grid}); out = {out}')
    return 0 if not bad else 1


if __name__ == '__main__':
    raise SystemExit(main())
