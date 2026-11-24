# Phase-3 daily notes (append-only; two lines per finished work package)

- 2026-11-24 14:20 p3-b (Casper): B2 development closure done — repaired thinning (s_model 0.51) and occupancy model (held-out R06: 0.355) BOTH above the cap 0.135 → STR §11.7 rule-1 pause condition; cause identified for both (estimators count hit sets that exist, the finder keeps fewer distinct sets at narrow widths).
  Day-15 pile-up term (occupancy, R04–R07 inputs) in outputs/p3b/pileup_term.json: R08 347, R09 4.1 events at N_trig 4.08e7; artifact outputs/P3B_PILEUP_casper_2026-11-24.md; 4.9 of 15 CPU-h.
- 2026-11-24 14:51 p3-e (Hilde): p3-e-devpu1 (dev.pu1, 298 × 20 = 5,960 events) defined and tested (devpu1-0000 done on maxwell, matches c1.pu1). Seeds disjoint. Launch command and pre-flight in outputs/P3E_hilde_2026-11-24.md; ≈ 98–100 CPU-h; not launched.
