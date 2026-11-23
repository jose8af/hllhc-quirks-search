# Session log: Ulrika (executor, Opus), D2 robustness row "later arcs restored" — 2026-11-19

- 11:16 -0500 started. Read AGENT_RULES, PHASE2_BRIEF, COMMITMENTS l.300-361, ADD1 v5 §1.1-1.5, HALF_TURN / LOOPER_GUN /
  A1_OPTION_A (xavier), run_stage4.run_pu_job, run_chain.py, chain_inputs.prepare_event, pu_inputs.topup, p2x_b1.HybridParent,
  p2x_ht_g4, p2x_looper_chain. Nodes at 11:16: landau 0 jobs of mine, maxwell 1 (Sune FxFx), schrodinger 0.
- 11:19 plan written and committed (564fa1a): outputs/D2_PLAN_ulrika_2026-11-19.md.
- 11:23 code: src/p2u_d2_chain.py (acts env; Geant4 + HybridAll injection; checks vs nominal dumps), src/p2u_d2_find.py
  (tt env; dumps + injected rows, top-up exchange, frozen finder), src/p2u_d2_sum.py (reading). Campaigns in
  tools/runner/examples/d2/ (p2-c-d2s-* smoke, p2-c-d2-{chain,find,ctl,sum}).
- 11:24 landau full (Tove p2-c-pilot-cls, 3 jobs on landau and schrodinger); SLOTS line corrected to maxwell.
- 11:25 smoke p2-c-d2s-chain launched on maxwell (--max-per-node 1).
- 11:27 smoke p2-c-d2s-find: control (events 0-1, injection off, --check-prepare) reproduces c1pu1-0000's trials bit
  for bit (n_grp, n_pass, n_pass_T, n_grp_T, seeds, PV, phimet); varied failed: v1 index asserts a constant sigma per
  surface, injected rows had float64 s0/s1 vs float32 dumps -> injected s0, s1, dE, t rounded to float32 (p2u_d2_find.py).
- 11:30 p2-c-d2s-find2 (varied, events 0-1): runs, 41 s/event; pairing (seed, PV, phimet) identical; R04 groups 674 vs 942.
- 11:31 production p2-c-d2-chain launched on maxwell, 2 slots (driver maxwell:/home/scratch/jdochoa/drivers/p2-c-d2-chain.ssh.log).
  Check: tools/runner/bin/qv2-watch tools/runner/examples/d2/p2-c-d2-chain.json. Next: p2-c-d2-ctl, then p2-c-d2-find, then p2-c-d2-sum.
- 15:53 chain 30/30 done 15:43 (29,400 CPU-s; 8 events of 600 differ from the dump by ±1 written hit, lost-simhit level); p2-c-d2-ctl 2/2 reproduces c1pu1-0000 trials bit for bit (all 80 trials, 43 columns) -> c1pu1 serves as nominal partner. p2-c-d2-find running on landau (maxwell given 0 slots by the driver's load cap).
