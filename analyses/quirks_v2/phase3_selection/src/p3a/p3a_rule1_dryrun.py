"""p3a_rule1_dryrun.py -- rule-1 projection (STR §11.7 rule 1, ADD §4.3) on the FINAL pilot counts.  Aurora, 2026-11-24.

      *** NOT BINDING as run by work package p3-a (pile-up rows = v1-based EST, MET additions = planning N_trig). ***

  <tt python> p3a_rule1_dryrun.py <p3a_counts.json> <out.json> [--inputs DIR] [--write-default-inputs] [--tag TEXT]

The binding run swaps input FILES only (default DIR = phase3_selection/outputs/p3a/inputs/):
  pileup_rows.json   pile-up term per T2 candidate.  Now: the v1-based EST rows (strategy_budget.py l.669-685, the
                     rows of the approved addendum script).  Binding: the development occupancy model's rows (p3-b).
  met_ntrig.json     N_trig of Z(tautau), lost-lepton Z(ll), multijets.  Now: planning values (strategy_budget.py
                     l.83, l.87).  Binding: the MET model's values (p3-c).
  z_weights.json     per-event preselection weight of the Z(nunu) pilot.  Now: {"mode": "v1"} (M = 993,885.9).  Binding
                     (ADD l.607: M "replaced by the day-12 MET model"): {"mode": "file", "path": <npz with one float
                     array per pilot file, key = file stem>, "full_class_min": x}; m and M are then recounted from the
                     row export of p3a_counts.py (every Z event was classified, also those with w_v1 = 0).
Nothing of the rule is re-implemented beyond the 20 lines of p2t_rule1_prelim.reading (copied below with N_t and the
pile-up rows as arguments; checked to give its numbers bit for bit): constants, N_t, the unit-exponential and pile-up
streams are those of p2z_addendum1.py (the approved addendum's script), imported unchanged.
Checks before any count is used: (1) empty pilot = 160.8 / 238.3 / 262.3 / 283.8 (addendum1_v4_stdout.txt l.66);
(2) Ingvild's (S) reading with her M reproduces rule1_valid_b50_ingvild_2026-11-23.json exactly.
A term with count m contributes (N_t / M) Gamma(m + 1); B = sum + pile-up; B50 = median of 1e5 draws; a reading
>= 300 (1 - 0.003) = 299.1 pauses (STR l.2730-2757).
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[2]
sys.path.insert(0, str(QV2 / 'phase2_exploration' / 'src'))
import p2z_addendum1 as Z  # noqa: E402
import p2t_rule1_prelim as T  # noqa: E402

log = logging.getLogger('p3a_rule1_dryrun')
NS = Z.R.NS
ORDER = T.ORDER                                       # DIF, DIFC, NI22, NI30, NI61, NIX, NIC, HS, Z, Zlow
M_Z_SINGLE = 993885.9                                 # Ylva's review: the single M of the Z term (Bjorn's value)
LOWPT_NT = (2.6e8, 5.2e8)                             # ADD l.393-397 [E]
# T2 candidates (STR l.1794-1798) -> (width name in p3a_counts, s, pile-up row keys to read it with)
CANDS = [('R07', 'R07', 0, ['R07_direct']),
         ('R08', 'R08', 0, ['R08@88', 'R08@118', 'R08@148']),
         ('R09', 'R08', 0, ['R09']),
         ('R11', 'R08', 0, ['R11_lo', 'R11_hi']),
         ('R14=R17=R20', 'R08', 3, ['none', 'R14_lo', 'R14_hi']),
         ('FB(0) width none', 'R04n', 3, ['none']),
         ('FB(0) width 75 mm', 'R04w', 3, ['none']),
         ('FB(1)', 'R05', 3, ['none']),
         ('FB(2)', 'R06', 3, ['none']),
         ('FB(3)', 'R07', 3, ['none']),
         ('FB(4)', 'R08', 3, ['none', 'R14_lo', 'R14_hi'])]


def default_inputs():
    pu_cap = -NS['PU_CAP']
    rows = {'R09': dict(type='lognormal_capped', median=Z.R.PU9[0], s_tot=Z.R.PU9[1], cap_mean=-Z.R.PU9[2]),
            'none': dict(type='none')}
    for x in Z.O['R08_PILEUP']:
        rows[f'R08@{x:.0f}'] = dict(type='lognormal_capped', median=x, s_tot=0.43, cap_mean=pu_cap)
    for lab, v in zip(('lo', 'hi'), NS['PU_R11']):
        rows[f'R11_{lab}'] = dict(type='lognormal_capped', median=v, s_tot=NS['W_PU']['R11'], cap_mean=pu_cap)
        rows[f'R14_{lab}'] = dict(type='lognormal_capped', median=v, s_tot=NS['W_PU']['R14'], cap_mean=pu_cap)
    rows['R07_direct'] = dict(type='counted', count=35, trials=48000, n_trig=Z.NTRIG)
    pu = dict(status='v1-based EST rows; NOT the development occupancy model (p3-b delivers its replacement)',
              source='phase1_strategy/src/strategy_budget.py l.669-685 via p2c_rule1.NS; R09 and R08@x are the rows of '
                     'p2z_addendum1.PUS (approved addendum).  R11_*: PU_R11 ends with W_PU[R11] (no row in the approved '
                     'script: reading of STR l.1015-1018 by Aurora).  R14_*: "R14 is at most the R11 value" (STR l.1016) '
                     'with W_PU[R14].  R07_direct: "35 in 48,000 trials" (STR l.1013) read as a counted term, '
                     'N_trig / 48,000 x Gamma(36).  none: no pile-up term (a lower bound of B, valid for "above" only).',
              rows=rows)
    met = dict(status='planning N_trig; NOT the MET model (p3-c delivers the replacement)',
               source='strategy_budget.py l.83 (ADD_PLAN), l.87 (MJ_PLAN) via p2c_rule1',
               n_trig={'Z(tautau)': Z.SM['Z(tautau)'], 'Z(ll) lost': Z.SM['Z(ll) lost'], 'multijets': Z.MJ})
    zw = dict(mode='v1', full_class_min=0.5, M_single=M_Z_SINGLE,
              source='v1 preselection weight w_v1 stored in the pilot; M = sum w / w_max of the class w >= 0.5 '
                     '(review RULE1_B50_REVIEW_ylva_2026-11-23.md section 2)')
    return dict(pileup_rows=pu, met_ntrig=met, z_weights=zw)


def pu_draws(row, seed):
    nd = Z.O['ND']
    if row['type'] == 'none':
        return np.zeros(nd)
    if row['type'] == 'lognormal_capped':
        return np.asarray(Z.pustream((row['median'], row['s_tot'], -row['cap_mean']), seed), float)
    if row['type'] == 'counted':
        rng = np.random.default_rng([seed, 20261124, row['count']])
        return row['n_trig'] / row['trials'] * rng.gamma(row['count'] + 1, 1.0, nd)
    raise SystemExit(f"unknown pile-up row type {row['type']}")


def reading(counts, NT, pu_rows, seed=7, extra=()):
    """Copy of p2t_rule1_prelim.reading with N_t and the pile-up rows as arguments.  counts: {term: (m, M)}."""
    nd = Z.O['ND']
    rng = np.random.default_rng([seed, 20261119])
    tot = np.zeros(nd); parts = {}
    for i, t in enumerate(ORDER):
        m, M = counts[t]
        g = np.asarray(Z.estream(f't{i}', seed), float)
        if m > 0:
            g = g + rng.gamma(m, 1.0, nd)
        parts[t] = (NT[t] / M) * g
        tot += parts[t]
    for lab, k, m in extra:
        parts[lab] = k * rng.gamma(m + 1, 1.0, nd)
        tot += parts[lab]
    out = {}
    for pl, row in pu_rows:
        pud = pu_draws(row, seed)
        s = np.sort(tot + pud)
        med = s[int(0.5 * nd)]
        d = int(round(0.5 * np.sqrt(nd)))
        out[pl] = dict(B50=float(med), q16=float(s[int(0.16 * nd)]), q84=float(s[int(0.84 * nd)]),
                       mc_err=float(0.5 * (s[nd // 2 + d] - s[nd // 2 - d])), pauses=bool(med >= Z.LIMIT),
                       min_draw=float(s[0]), pileup_median=float(np.median(pud)),
                       term_medians={t: float(np.median(v)) for t, v in parts.items()})
    return out


def main(argv):
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    cin, cout = argv[0], argv[1]
    indir = QV2 / 'phase3_selection' / 'outputs' / 'p3a' / 'inputs'
    tag = 'NOT BINDING (dry run of p3-a: v1-based EST pile-up rows, planning N_trig of the three MET additions, v1 weights)'
    if '--inputs' in argv:
        indir = Path(argv[argv.index('--inputs') + 1])
    if '--tag' in argv:
        tag = argv[argv.index('--tag') + 1]
    if '--write-default-inputs' in argv:
        indir.mkdir(parents=True, exist_ok=True)
        for k, v in default_inputs().items():
            (indir / f'{k}.json').write_text(json.dumps(v, indent=1))
    I = {k: json.loads((indir / f'{k}.json').read_text()) for k in ('pileup_rows', 'met_ntrig', 'z_weights')}
    PR = I['pileup_rows']['rows']
    # ---- check 1: empty pilot with the approved constants ----
    appr = [(pl, dict(type='lognormal_capped', median=pu[0], s_tot=pu[1], cap_mean=-pu[2])) for pl, pu in Z.PUS]
    empty = reading({t: (0, T.MPLAN[t]) for t in ORDER}, T.NT, appr)
    for pl, v in T.EXPECT_EMPTY.items():
        if abs(empty[pl]['B50'] - v) > 0.06:
            raise SystemExit(f'empty-pilot check FAILED at {pl}: {empty[pl]["B50"]:.2f} against {v}')
    # ---- check 2: Ingvild's reading, bit for bit ----
    ing = json.loads((QV2 / 'phase2_exploration' / 'outputs' / 'rule1_valid_b50_ingvild_2026-11-23.json').read_text())
    chk2 = {}
    for name in ('subS_with', 'subF_with'):
        cnt = {t: tuple(ing['readings'][name]['counts'][t]) for t in ORDER}
        mine = reading(cnt, T.NT, appr)
        for pl in mine:
            ref = ing['readings'][name]['by_pileup'][pl]['B50']
            chk2[f'{name}:{pl}'] = [mine[pl]['B50'], ref]
            if mine[pl]['B50'] != ref:
                raise SystemExit(f'check 2 FAILED: {name} {pl}: {mine[pl]["B50"]!r} against {ref!r}')
    log.info('checks passed: empty pilot %s; Ingvild S/F reproduced exactly', {k: round(v['B50'], 1) for k, v in empty.items()})
    # ---- N_t with the MET additions from the input file ----
    v1sum = sum(v for k, v in Z.SM.items() if k not in ('Z(tautau)', 'Z(ll) lost'))
    ntz = v1sum + sum(I['met_ntrig']['n_trig'].values())
    NT = dict(T.NT, Z=ntz, Zlow=ntz * Z.O['LOW_CLASS']['Z'][1] / 0.98)
    C = json.loads(Path(cin).read_text())
    zw = I['z_weights']
    if zw['mode'] != 'v1':
        raise SystemExit('z_weights mode "file": recount m and M from <counts.json>.rows_m.npz with the per-event '
                         'weights (interface defined in the docstring; to be completed with the format p3-c delivers)')
    if '--smoke-partial' in argv:
        tag = 'SMOKE TEST ON A PARTIAL CAMPAIGN - NOT A RESULT'
    res = dict(tag=tag, limit=Z.LIMIT, nd=Z.O['ND'], inputs=I, N_t=NT, N_t_Z_planning_check=[ntz, T.NT['Z']],
               empty_check={pl: empty[pl]['B50'] for pl in empty}, check2=chk2, labels={})
    for lab, L in C['labels'].items():
        Mz_meas = L['M']['Z']
        partial = '--smoke-partial' in argv           # code test on an unfinished campaign only; never for a result
        if lab == 'm' and abs(Mz_meas - zw['M_single']) > 0.1 and not partial:
            raise SystemExit(f'M of the Z term measured {Mz_meas:.2f} differs from the single value {zw["M_single"]}')
        Mz = Mz_meas if partial else zw['M_single']
        out = dict(M_Z_measured_here=Mz_meas, M_Z_used=Mz, events_per_count={}, readings={})
        full = L['n_files'].get('DIF', 0) > 0                     # label with all streams
        base = C['labels']['m']
        for rd in C['readings']:
            for r_ in 'SF':
                for cname, wn, s, pus in CANDS:
                    for var in ('with', 'without'):
                        tab = L['tables'][f'{rd}_{r_}_{wn}_s{s}_{var}']
                        src = L if full else base            # Z-only labels: B1 / hs counts and M from label m (BASE)
                        tb1 = tab if full else base['tables'][f'BASE_{r_}_{wn}_s{s}_{var}']
                        cnt = {}
                        for t in ORDER:
                            if t in ('Z', 'Zlow'):
                                cnt[t] = (tab[t], Mz)
                            else:
                                Mb = src['M'][t] or (T.MPLAN[t] if partial else 0.0)       # smoke test: no B1 file yet
                                cnt[t] = (tb1[t], Mb - (src['M_flagged_events'][t] if var == 'without' else 0))
                        extra = []
                        ml = tb1['LOWPT']
                        if ml > 0:                          # alarm sample with a count: its lower N_t (ADD l.393-397)
                            Ml = src['M']['LOWPT'] - (src['M_flagged_events']['LOWPT'] if var == 'without' else 0)
                            extra = [('LOWPT_lo', LOWPT_NT[0] / Ml, ml)]
                        r = reading(cnt, NT, [(p, PR[p]) for p in pus], extra=extra)
                        if rd == 'BASE' and var == 'with':
                            seeds = [reading(cnt, NT, [(p, PR[p]) for p in pus], seed=sd, extra=extra) for sd in (11, 12, 13)]
                            for p in r:
                                r[p]['B50_other_seeds'] = [x[p]['B50'] for x in seeds]
                        else:
                            for p in r:
                                r[p].pop('term_medians')
                        out['readings'][f'{rd}|{r_}|{cname}|{var}'] = dict(counts={t: list(cnt[t]) for t in ORDER},
                                                                         lowpt_count=ml, by_pileup=r)
        out['events_per_count'] = {t: NT[t] / (Mz if t in ('Z', 'Zlow') else L['M'][t]) for t in ORDER if L['M'].get(t)}
        res['labels'][lab] = out
        for key in ('BASE|S|R09|with', 'BASE|F|R09|with', 'OWN|S|R09|with', 'HARD|S|R09|with', 'BASE|S|R07|with',
                    'BASE|S|R14=R17=R20|with', 'BASE|S|FB(0) width 75 mm|with'):
            v = out['readings'][key]
            log.info('%s %s m_Z %d: %s', lab, key, v['counts']['Z'][0],
                     {p: round(x['B50']) for p, x in v['by_pileup'].items()})
    Path(cout).write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main(sys.argv[1:])
