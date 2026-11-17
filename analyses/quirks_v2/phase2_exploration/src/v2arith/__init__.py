"""v2arith -- the v2 background arithmetic (channel (i), Rosalie, 2026-11-16; COM C1-b).

Small, self-contained (numpy only; does not import any v1 module).  Importable by the Phase-3 estimators and the T1
builder:  from v2arith.core import Factor, chain, sm_value, cprime_value, pu_value, Term, sample_sum, b84
Conventions transcribed from v1 (each with its source):
  * factor chain (WP_RULE §4.2 zero/low-count rule; v1 acts/stage4/analysis/background.py Term.evaluate):
    a counted factor N/M has s_ln = max(given s_ln, 1/sqrt(N)); a fixed factor carries its own s_ln; among the zero
    counts only ONE enters, the one with the largest M (ties: the first), as 1.14/M with s_ln = 1; the other zero
    counts enter as 1 with s_ln = 0; the term's statistical s_ln is the quadrature sum.
  * values: SM  B = P x sigma[pb] x K x L[pb^-1];  C'  B = N_trig x rate x PV-line factor x P;  PU  B = N_trig x
    P_per_trial (P = base x closure x trend x T3) (v1 wp.py, background.py; L = 3e6 pb^-1, run_all.DEFAULTS).
  * log-normal sum: each term = value x exp(sum_c s_c z_c), components named in SHARED use one z per name across terms
    (and categories), the others an independent z per term; B84 = 84th percentile of the Monte-Carlo sum
    (v1 stats.py SHARED, sample_terms).
"""
