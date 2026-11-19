"""p2t_rule1_prelim.py -- PRELIMINARY rule-1 reading (STR §11.7 rule 1, addendum 1) from the classified pilot.  Tove, 2026-11-19.

  python3 -I p2t_rule1_prelim.py <counts.json> <out.json>

counts.json (written by p2t_counts.py): per reading variant, {term: [m, M]} for the terms DIF, DIFC, NI22, NI30, NI61,
NIX, NIC, HS, Z, Zlow, and optionally LOWPT: [m, M].
The rule is not re-implemented: constants (N_t, pile-up rows, LIMIT, tie rule, 1e5 draws) and the random streams are
those of p2z_addendum1.py (the approved addendum's script), imported unchanged.  Check before anything else: with every
m = 0 and the planned M the reading must equal addendum1_v4_stdout.txt l.66 (160.8; 238.3 / 262.3 / 283.8).
A term with count m contributes (N_t / M) * Gamma(m + 1): the stream's unit exponential (the m = 0 floor, common random
numbers) plus an independent Gamma(m) draw.
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2z_addendum1 as Z  # noqa: E402

log = logging.getLogger('p2t_rule1_prelim')
B1 = ['DIF', 'DIFC', 'NI22', 'NI30', 'NI61', 'NIX', 'NIC']
S2 = dict(DIF=4e6, DIFC=4e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=4e6, NIC=2e6)       # addendum table (ADD section 3)
KF, KL, MFULL = Z.sm_terms(Z.O['PILOT_HS_GENERATED'])
NT = dict({t: Z.NT_MB[t] for t in B1}, HS=Z.NT_HS, Z=Z.SMTOT, Zlow=KL * MFULL)     # Zlow: N such that N / M_full = KL
MPLAN = dict(S2, HS=Z.O['HS_SIZES']['H1'], Z=MFULL, Zlow=MFULL)
ORDER = B1 + ['HS', 'Z', 'Zlow']
EXPECT_EMPTY = {'R09': 160.8, 'R08@88': 238.3, 'R08@118': 262.3, 'R08@148': 283.8}   # addendum1_v4_stdout.txt l.66


def reading(counts, seed=7, extra=()):
    """counts: {term: (m, M)}; -> {pile-up label: dict(B50, q16, q84, mc_err, per-term medians)}"""
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
    for lab, k, m in extra:                      # terms outside the ten (alarm sample with a count)
        parts[lab] = k * rng.gamma(m + 1, 1.0, nd)
        tot += parts[lab]
    out = {}
    for pl, pu in Z.PUS:
        b = tot + np.asarray(Z.pustream(pu, seed), float)
        s = np.sort(b)
        med = s[int(0.5 * nd)]
        # Monte-Carlo error of the median: binomial order statistics, +-1 sigma ranks
        d = int(round(0.5 * np.sqrt(nd)))
        out[pl] = dict(B50=float(med), q16=float(s[int(0.16 * nd)]), q84=float(s[int(0.84 * nd)]),
                       mc_err=float(0.5 * (s[nd // 2 + d] - s[nd // 2 - d])), pauses=bool(med >= Z.LIMIT),
                       pileup_median=float(np.median(Z.pustream(pu, seed))),
                       term_medians={t: float(np.median(v)) for t, v in parts.items()},
                       term_means={t: float(np.mean(v)) for t, v in parts.items()})
    return out


def main(cin, cout):
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    empty = reading({t: (0, MPLAN[t]) for t in ORDER})
    for pl, v in EXPECT_EMPTY.items():
        if abs(empty[pl]['B50'] - v) > 0.06:
            raise SystemExit(f'empty-pilot check FAILED at {pl}: {empty[pl]["B50"]:.2f} against {v}')
    log.info('empty-pilot check passed: %s', {pl: round(empty[pl]['B50'], 1) for pl in empty})
    C = json.loads(Path(cin).read_text())
    res = dict(tag='PRELIMINARY', limit=Z.LIMIT, nd=Z.O['ND'], events_per_count_planned={t: NT[t] / MPLAN[t] for t in ORDER},
               N_t=NT, M_planned=MPLAN, empty_check={pl: empty[pl]['B50'] for pl in empty}, readings={})
    for name, var in C['variants'].items():
        cnt = {t: (var[t][0], var[t][1]) for t in ORDER}
        extra = [(lab, k, m) for lab, k, m in var.get('extra', [])]
        r = reading(cnt, extra=extra)
        seeds = [reading(cnt, seed=s, extra=extra) for s in (11, 12, 13)]
        for pl in r:
            r[pl]['B50_other_seeds'] = [x[pl]['B50'] for x in seeds]
        res['readings'][name] = dict(counts=var, events_per_count={t: NT[t] / cnt[t][1] for t in ORDER}, by_pileup=r)
        log.info('%s: %s', name, {pl: round(r[pl]['B50'], 1) for pl in r})
    Path(cout).write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
