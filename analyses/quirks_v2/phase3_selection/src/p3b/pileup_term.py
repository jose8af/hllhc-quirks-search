"""Day-15 pile-up term per T2 candidate (STR §11.7 rule 1; B2-f widths) from b2_dev_closure.json (p3-b, Casper).

  python pileup_term.py   -> outputs/p3b/pileup_term.json   (schema: outputs/p3b/SCHEMA.md)
Pure arithmetic on the closure JSON (no data access).  Every width is STR §4.0 point 7:
    s_tot² = s_model² + Σ s_f² + (b̂² + σ_b²) d_in² + b0² d_out²,   b0 = ln 1.5,
evaluated under two bookkeepings that the frozen text leaves open at day 15 (both reported, none chosen here):
  'planning_cap'  : the frozen projection's planning rows (STR l.516-519, script [12]): s_model at the cap 0.135, the
                    width family tested at R06-R07 (n = 2, b̂ := 0 before the test, σ_b = b0), 2S crossing credited
                    with s_f at the cap when 'with_2S_credit', fit-probability family untested (d_out);
  'measured_dev'  : s_model as measured on the development sample, the evaluable development test rungs only
                    (width family: R06 alone -> n = 1, b̂ := 0, σ_b := b0), s_f = r.m.s. of ln r over the evaluable
                    development 2S crossing rungs when every one of them is within ln 1.5.
Review cycle 1 (fixer Ivar, 2026-11-24; DOR B2, B4, B5) adds, without changing any v1 key:
  'planning_cap_lastR06_*' : the planning convention with R06 as the last evaluable width-test rung (P3B §3.4: R07 is
                    not evaluable at the development direct rate, 42 expected counts, σ_tot 0.159; it is at v1's rate);
  occupancy_B2b_model at R09 (and R09 ∧ N_2S2 ≥ 3) = the B2-b R08 value × the same fit-probability fraction;
  no_credit_value.events_zero_count_68_dev16000: the zero-count bound of the 16,000 development trials (a reading
                    to flag, DOR B2: "the samples that exist at day 15"; not chosen here);
  occupancy_day15.mc_rel_error_b3 (R08, R09 and their s = 3 rows; DOR B3): the model MC error re-estimated from
                    is_check.json / is_check_stats.json = max(within-seed IS error, precision of the paired plain-toy
                    check); the v1 key mc_rel_error (8-seed spread) is kept unchanged.
Review cycle 2 (fixer Ivar; Liv B-new-1) adds occupancy_day15.mc_rel_error_c2 (R08, R09 and their s = 3 rows), the
                    value to use: the stored IS error with the per-toy variance of the 10x-toy fresh run (R08 0.217),
                    and at R09 in quadrature the binomial error of the fit-probability fraction (0.145) -> 0.261.
                    Computed by is_check_c2.c2_errors (standard library); mc_rel_error_b3 (0.149) is superseded but
                    kept unchanged.
"""
import hashlib
import json
import logging
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'outputs' / 'p3b'
LN15 = np.log(1.5)
CAP = LN15 / 3
B0 = LN15
NTRIG = 4.0848e7     # phase1_strategy/src/strategy_budget.py l.68 ("bsum_wp.json -> n_trig.value"), the value the
                     # frozen projection script uses; p3-a substitutes the MET-model N_trig (rate × N_trig)
log = logging.getLogger('pileup_term')
CANDS = [('R04', 's0'), ('R05', 's0'), ('R06', 's0'), ('R07', 's0'), ('R08', 's0'), ('R09', 's0'),
         ('R04x2S>=3', 's3'), ('R05x2S>=3', 's3'), ('R06x2S>=3', 's3'), ('R07x2S>=3', 's3'), ('R08x2S>=3', 's3'),
         ('R09x2S>=3', 's3')]
WIDX = {'R04': 4, 'R05': 5, 'R06': 6, 'R07': 7, 'R08': 8, 'R09': 9}


def s_tot(smodel, sf, bhat, sigb, d_in, d_out):
    return float(np.sqrt(smodel ** 2 + sf ** 2 + (bhat ** 2 + sigb ** 2) * d_in ** 2 + B0 ** 2 * d_out ** 2))


def distances(c, last_width):
    """(d_in, d_out_fit, d_out_2S) for candidate c given the last evaluable cumulative width test rung."""
    base = c[:3]
    k = min(WIDX[base], 8)
    d_in = max(0, k - WIDX[last_width])
    d_fit = 1 if base == 'R09' else 0
    d_2s = 3 if 'x2S' in c else 0
    return d_in, d_fit, d_2s


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    src = OUT / 'b2_dev_closure.json'
    R = json.loads(src.read_text())
    occ = R['occupancy']; thin = R.get('thinning'); dr = R['direct']
    sm_occ = occ['s_model']
    # 2S crossing credit on the development sample (occupancy model, 2S family only)
    xr = [occ['predictions'][c]['const'] for c in occ['predictions'] if 'x2S' in c and c[:3] in ('R04', 'R05', 'R06')]
    xe = [x for x in xr if x['evaluable'] and x['ln_r'] is not None]
    sf_meas = float(np.sqrt(np.mean([x['ln_r'] ** 2 for x in xe]))) if xe else None
    cross_ok = bool(xe) and all(abs(x['ln_r']) <= LN15 for x in xe)
    f09 = occ['fitprob_fraction_from_R06_candidates']['0.001']
    lnA = occ['day15_scale']['lnA']
    c2 = None
    if (OUT / 'is_check_inputs').is_dir():
        import sys
        sys.path.insert(0, str(HERE))
        from is_check_c2 import c2_errors   # noqa: E402  (standard library only; same directory)
        c2 = c2_errors(OUT)['mc_rel_error_c2']
    b3 = None
    if (OUT / 'is_check.json').exists() and (OUT / 'is_check_stats.json').exists():
        ic = json.loads((OUT / 'is_check.json').read_text())
        st = json.loads((OUT / 'is_check_stats.json').read_text())['combined']['R08']
        b3 = dict(value=float(max(st['rel_within_pooled'], ic['R08']['plain_rel_err'])),
                  rel_within_pooled=st['rel_within_pooled'], rel_seed_spread=st['rel_seed_spread'],
                  plain_over_stored_IS=ic['R08']['plain_over_stored'], plain_pass_toys=ic['R08']['plain_pass_toys'],
                  plain_rel_err=ic['R08']['plain_rel_err'], fresh_over_stored_IS=ic['R08']['fresh_over_stored'])
    out = dict(schema='p3b.pileup_term.v1', source=str(src),
               source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
               N_trig_used=NTRIG, N_trig_source='phase1_strategy/src/strategy_budget.py l.68 (v1 bsum_wp n_trig)',
               no_credit_value=dict(events_mean=NTRIG / 96000, events_zero_count_68=NTRIG * 1.14 / 96000,
                                    events_zero_count_68_dev16000=NTRIG * 1.14 / 16000,
                                    note='STR l.1177 (485 events at v1 N_trig) and the frozen script draws '
                                         'N_trig/96,000 x Exp(1) as the cap of the pile-up term (strategy_budget.py '
                                         'l.678); unchanged by this work package'),
               estimators=dict(
                   occupancy=dict(s_model=sm_occ, cap=CAP, above_cap=occ['above_cap'],
                                  s_model_trend_variant=occ['s_model_trend_variant'],
                                  crossing_2S_dev=dict(evaluable=len(xe), all_within_ln15=cross_ok, s_f=sf_meas)),
                   thinning=None if thin is None else dict(
                       s_model_cumulative=thin['s_model_cumulative'], s_model_with_crossing=thin['s_model_with_crossing'],
                       cap=CAP, above_cap=thin['above_cap_cumulative'],
                       above_cap_with_crossing=thin['above_cap_with_crossing'])),
               candidates={})
    ab = [occ['above_cap']] + ([thin['above_cap_cumulative']] if thin else [True])
    out['both_estimators_above_cap'] = bool(all(ab))
    for c, fam in CANDS:
        base = c if c in occ['E_model'] else None
        if c.startswith('R09'):
            src_c = 'R08x2S>=3' if 'x2S' in c else 'R08'
            em = occ['E_model'][src_c] * f09
            mc = occ['E_model_relMC'][src_c]
        else:
            em = occ['E_model'][base]; mc = occ['E_model_relMC'][base]
        rate15 = float(np.exp(lnA) * em)
        rec = dict(family=fam,
                   occupancy_day15=dict(rate_per_trial=rate15, events=rate15 * NTRIG, mc_rel_error=mc,
                                        fitprob_fraction=f09 if c.startswith('R09') else None),
                   occupancy_B2b_model=None)
        if b3 is not None and c[:3] in ('R08', 'R09'):
            rec['occupancy_day15']['mc_rel_error_b3'] = b3['value']
            rec['occupancy_day15']['b3_check'] = b3
        if c2 is not None and c in c2:
            rec['occupancy_day15']['mc_rel_error_c2'] = c2[c]
            if rec['occupancy_B2b_model']:
                rec['occupancy_B2b_model']['mc_rel_error_c2'] = c2[c]
        if c in occ['predictions']:
            p = occ['predictions'][c]['const']
            rec['occupancy_B2b_model'] = dict(rate_per_trial=p['rate'], events=p['rate'] * NTRIG, ln_r_dev=p['ln_r'],
                                              sigma_tot_dev=p['sigma_tot'])
        elif c.startswith('R09'):
            p = occ['predictions']['R08x2S>=3' if 'x2S' in c else 'R08']['const']
            rec['occupancy_B2b_model'] = dict(rate_per_trial=p['rate'] * f09, events=p['rate'] * f09 * NTRIG,
                                              ln_r_dev=None, sigma_tot_dev=None, fitprob_fraction=f09)
        d_in_p, d_fit, d_2s = distances(c, 'R07')
        d_in_m, _, _ = distances(c, 'R06')
        sf_cap = CAP if 'x2S' in c else 0.0
        w = dict(planning_cap_with_2S_credit=s_tot(CAP, sf_cap, 0.0, B0, d_in_p, d_fit),
                 planning_cap_no_2S_credit=s_tot(CAP, 0.0, 0.0, B0, d_in_p, d_fit + d_2s),
                 measured_dev=s_tot(sm_occ, (sf_meas if (cross_ok and 'x2S' in c) else 0.0), 0.0, B0, d_in_m,
                                    d_fit + (0 if (cross_ok or 'x2S' not in c) else d_2s)),
                 planning_cap_lastR06_with_2S_credit=s_tot(CAP, sf_cap, 0.0, B0, d_in_m, d_fit),
                 planning_cap_lastR06_no_2S_credit=s_tot(CAP, 0.0, 0.0, B0, d_in_m, d_fit + d_2s))
        rec['width_s_tot'] = w
        rec['distances'] = dict(planning=dict(d_in=d_in_p, d_out=d_fit + d_2s),
                                measured_dev=dict(d_in=d_in_m, d_out=d_fit + (0 if cross_ok else d_2s)))
        if thin is not None and c in thin['rate']:
            rec['thinning'] = dict(rate_per_trial=thin['rate'][c], events=thin['rate'][c] * NTRIG,
                                   s_boot=thin['s_boot'][c], N_eff=thin['N_eff'][c])
        if c in dr['rate']:
            rec['direct_dev'] = dict(count=dr['counts'][c], trials=dr['trials'], rate_per_trial=dr['rate'][c],
                                     events=dr['rate'][c] * NTRIG)
        out['candidates'][c] = rec
    (OUT / 'pileup_term.json').write_text(json.dumps(out, indent=1))
    log.info('written %s', OUT / 'pileup_term.json')


if __name__ == '__main__':
    main()
