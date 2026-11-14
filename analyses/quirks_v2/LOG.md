# Experiment log — quirks v2 (append-only)

Format: JFC 05 §5.1. One dated entry per material decision, discovery or failed attempt. Never edited, never deleted.

## 2026-11-13

### 14:06 — Preflight, first run: STOPPED
All checks passed except one. On cajuela, the first open after a rename returned `Stale file handle` (3/3 on einstein,
3/3 on landau, 3/3 in Argo pods; workflow `jdochoa-qv2-preflight-m5kz8` failed at `sha256sum` right after `mv`). Only
the renaming client was affected, only once; `/home/users` was not affected. Reported to the user with two options
(admin fix, or runner workaround). Details: `PREFLIGHT.md`.

### 14:30 — Admin fix to cajuela (user decision: option 1)
Cause, from the admin: mergerfs `inodecalc=path-hash` changed a file's inode on rename (kernel: "NFS: fileid changed").
Now `inodecalc=hybrid-hash`. The write-`.part`-then-rename rule of brief §5.2 is kept unchanged.
**Remaining limit, binding for all jobs: directories still get a path-based inode. Never rename a directory on
cajuela while other nodes are using it. Renaming files is fine.** Runner consequences: create campaign and shard
directories under their final names; never stage a directory as `dir.part`; reorganise trees only with no campaign
running, and log it here.

### 14:34 — Preflight, re-run: PASS
Rename pattern 3/3 on all four hosts with unchanged inode; cross-node read correct; Argo pods on the three workers
`stale_retries=0` (`jdochoa-qv2-preflight-cvncx`, deleted). Other findings carried into the pod template: `ubuntu:24.04`
was not pre-pulled (now pulled, digest `sha256:2198e4c6…caf5`); pods run with umask 000 (template sets `umask 022`);
use `ssh -x`; landau and schrodinger have a graphical session (cap 3 jobs each for now).

### 14:36 — Scaffold
Branch `v2-jfc`. JFC cloned from `jfc-mit/jfc` at `9eecb0e0b4c95c362053ad6b121760b47379bc54` (2026-03-31) and vendored
in `tools/jfc/`. `analyses/quirks_v2/` scaffolded as a search with system `python3` (pixi is not installed yet; the
scaffolder needs only the standard library). Deviations V1–V11 recorded in `DEVIATIONS.md`.
DECISION: vendor JFC as plain files instead of keeping a nested clone or a submodule.
ALTERNATIVES: git-ignored clone (repo not self-contained); submodule (needs network at clone time, second repo).
CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.

### 15:20 — NFS home stalls under small-file installs from workers
Found by Anselm: `pixi install` run over NFS from a worker wrote at ~1 MB/s, drove einstein's `/home` disk to 85–94 %
busy with all 8 nfsd threads blocked, and slowed NFS for the whole lab (46/148 packages in 20 min from maxwell,
against 5–27 s per environment when run on einstein locally). Cause: `sync` export of a rotational disk.
Rule added to `AGENT_RULES.md`: many-small-files writes under `/home/users/jdochoa` run only on einstein, niced and
`ionice -c3`, one at a time; workers compile on local disk and ship one tarball; jobs write one marker on NFS home.
Basil's install on schrodinger was told to stop and rerun on einstein; Boris was told to measure marker-write
latency under 12 concurrent jobs. Not a cluster fault and no admin action needed; it is a constraint on how we use it.

### 15:12 — INTERRUPTION: einstein out of memory; orchestrator and all three executors killed
Reported by the user. At 15:12 einstein ran out of memory and systemd-oomd killed the tmux session holding the
orchestrator and the feasibility executors Anselm, Basil and Boris with their background jobs. In the same incident
`/nfs/cajuela` returned I/O errors from 15:12 to 15:20; restored and verified on all nodes by the user. Nothing of the
study survived in Kubernetes or on the workers; no `.part` files were left.

Reconciliation (15:35–15:45, orchestrator):
- Git: HEAD was `31a6974`; everything the executors wrote after it was uncommitted and is committed now as
  "state at interruption" (code copies, runner, install scripts, partial feasibility outputs).
- Workers: no process of ours on landau, maxwell or schrodinger; no Argo workflow of ours; cajuela reachable from all.
  Leftovers: maxwell scratch `anselm_s3smoke/`, `anselm_smoke_acts/`, `cache/` (1 MB); schrodinger
  `/var/tmp/jdochoa/dl` (100 MB of downloaded tarballs, to be re-verified by sha256 before use); einstein
  `/var/tmp/jdochoa/{numba_einstein,pyhf_smoke,runner_tests}`.
- pixi environments, checked file by file against their `conda-meta/*.json` and `dist-info/RECORD` lists:
  complete, zero missing files, install marker written 90 s or more before the crash — JFC env (14:42), `tools/runner`
  (14:45), `envs/tt` (14:58), `acts` (14:58), `sim` ana and mg (14:59), `pyhf_bench` (15:01), `sw/envs/mg` (15:09).
  **`sw/envs/g4` was cut off** (90 conda packages linked, no install marker, last write 15:11:54): its `.pixi` was
  deleted; it must be reinstalled from its lockfile, not trusted.
- Ledger and markers: 2 markers (Anselm toy Stage-3 inputs, sha256 recorded) plus Boris test markers under
  `phase1_strategy/outputs/feasibility/runner_ledger/`. Feasibility test data on cajuela: `data/feasibility/{chain,runner}`.
- Unfinished at the interruption — Anselm: Stage-3 smoke done (3 jobs), ACTS smoke test was starting, no benchmark
  table, `FEAS_A` is a stub. Basil: downloads done, MG5 2.9.22 unpacked, LHAPDF data dir built, `mg` env installed, g4
  env cut off; no generation, no benchmark, no `FEAS_B`. Boris: runner package and 19 unit tests, accounting test,
  Argo and SSH 60-s tests (3 each), bundle tool test done; mini-campaign, kill/resume, memory test, pyhf benchmark
  timings and `FEAS_C` not done.
- Found while reconciling: `PREFLIGHT.md` had stayed in `tools/` (the scaffold move failed silently); moved to
  `analyses/quirks_v2/PREFLIGHT.md` now. A `__pycache__` written into the read-only `book/checks/` by an
  investigator was removed.

**New binding constraints from the user (supersede the 15:20 rule where they differ):**
1. The orchestrator runs in a systemd service capped at 10 GB (`MemoryMax=10G`); every subagent counts against it.
   Keep the number of concurrent subagents modest.
2. einstein is head node, NFS server and Kubernetes control plane: **no pixi installs, solves, builds or benchmarks
   on einstein.** They run on landau/maxwell/schrodinger or as Argo jobs. (This reverses the 15:20 rule that sent
   installs to einstein.)
3. At most one pixi install at a time on the shared cache; keep heavy metadata work off `/home` while jobs run.


### 16:00 — USER DECISION: Geant4 environment on each worker's local scratch
The Geant4 pixi environment (~3.3 GB of small files) is installed per worker at `/home/scratch/jdochoa/envs/g4`
(same absolute path on landau, maxwell, schrodinger and in pods through the scratch hostPath), not on the shared
home. Reason: an install to NFS home runs at ~1 MB/s and slows NFS for the lab for about an hour. Consequences:
the canonical `pixi.toml` + `pixi.lock` are tracked in the repo and each node installs `--frozen` from them with a
node-local package cache (`/home/scratch/jdochoa/cache/rattler`), so the three copies are identical by lockfile;
each install is verified (package file lists) and recorded with the lock sha256 in a per-node stamp file; the
environment counts against the 150 GB per-node scratch budget; Geant4 jobs can only run on a node whose stamp
matches the tracked lock. Deviation V13 from brief §5.2.

### 19:25 — Phase 1 review cycle 1: ITERATE
Panel: Casimir (physics; 5 A, 12 B, 8 C), Celeste (critical; 8 A, 16 B, 10 C), Cosima (constructive; 1 A, 16 B,
11 C); arbiter Dagmar merged them into 11 A (M1–M11) and 24 B (M12–M35): `phase1_strategy/review/arbiter/
STRATEGY_ARBITER_dagmar_2026-11-13_19-00.md`. Core problems: zero simulated counts drop out of the expected limit
(M1); zero-count floors of ~141 (PV pairs) and ~47 (SM) events at the planned sample sizes (M6); closure tested on
the rungs where corrections are derived, no extrapolation width (M3, M4); MUST criteria not evaluable at the planned
statistics (M5); 6, not 3, of the C1 signal counts are efficiencies of v2 candidate selections (blinding); the brief's
30 % stop-and-ask rule had been weakened to "report" (M10). The budget arithmetic was confirmed by the critical
reviewer (26 of 28 spot checks; `strategy_budget.py` reproduces all totals). No regression (Phase 1 is the origin).
Next: fixer Dmitri (fable: likelihood and closure redesign is the error-prone core) → STRATEGY v2 → re-review cycle 2
with fresh reviewers.

### 21:10 — Phase 1 review cycle 2: ITERATE
STRATEGY v2 (fixer Dmitri, `STRATEGY_dmitri_2026-11-13_19-25.md`) re-reviewed by fresh sessions Dolores (physics),
Dorothea (critical), Edmund (constructive); arbiter Eloise: `phase1_strategy/review/arbiter/
STRATEGY_ARBITER_v2_eloise_2026-11-13_20-45.md`. M1–M35: 20 resolved, 7 partial, 8 deferred to Gate A (accepted).
New: 4 A (N1–N4), 14 B (N5–N18). Core: the ceiling H is never tested as a ceiling; MUST closures left NOT TESTED
(brief D4); "target met" satisfiable by zero-count bounds alone; false-fail rates computed at zero model width
(41–71 % for the battery at the declared widths, not 10 %); extrapolation widths contradict the strategy's own rule;
PV pairs double-counted with the SM hard-scatter term (confirmed in v1 code); v1 already contained pile-up decays and
nuclear interactions. All numbers of v2 were reproduced by two reviewers. Arbiter's rulings net about −96 CPU-h
(ESTIMATE). Gate A reduced to 5 questions plus 8 overridable defaults. Iteration count: 2 (warn at 3).
Next: fixer Emeric (fable) → STRATEGY v3 → cycle 3 as a verification pass with fresh reviewers.

### 23:05 — Phase 1 review cycle 3: ITERATE (converging; iteration warning level reached)
STRATEGY v3 (fixer Emeric) reviewed by fresh sessions Estelle (physics: 0 A, 6 B), Fabian (critical: 0 A, 7 B),
Fabiola (constructive: 1 A, 6 B); arbiter Felix: `phase1_strategy/review/arbiter/
STRATEGY_ARBITER_v3_felix_2026-11-13_22-40.md`. Merged: 1 A (P1: Z(ττ) and lost-lepton Z without a no-pile-up pool
share) and 15 B (P2–P16), all text/table/script fixes, at most ~50 CPU-h of added samples, no redesign. All three
reviewers reproduced v3's numbers (budget, floor 11.7, widths, false-fail rates, reach mapping). Trend of merged
Category A: 11 → 4 → 1. JFC 06 §6.5 warning at 3 iterations noted: the arbiter judges that cycle 4 should be a pure
verification of P1–P16; taste and Phase-2-measurement items are already settled as dated rules or Gate-A defaults.
Headline correction ordered (P2): lead with the conservative reach (about 720 GeV, down to about 500–650 GeV under
v1's own counts for decays in flight and conversions), 790 GeV only as the upper edge; the day-15 pause for a large
background is a realistic branch.
Next: fixer Fiona (opus: well-specified text/table/script work) → STRATEGY v4 → cycle-4 verification panel.

## 2026-11-14

### 00:50 — Phase 1 review cycle 4: ITERATE (0 A, 5 B); the expected outcome of the default plan changes
STRATEGY v4 (fixer Fiona) reviewed by fresh sessions Florence (physics), Gerald (critical), Gertrude (constructive);
arbiter Greta: `phase1_strategy/review/arbiter/STRATEGY_ARBITER_v4_greta_2026-11-14_00-25.md`. P1–P16: 14 resolved,
2 partial. Merged Category A by cycle: 11 → 4 → 1 → 0. Open: R1 headline, R2 three Q3 annex rows, R3 pilot
classification schedule, R4 S_CKF test sample (0 CPU-h), R5 paired passes for eleven SM processes (+36 CPU-h, adopted).
**R1 is a physics finding for the human, not only wording.** Checked by the arbiter against the tracked v1 record
(`C12FC_v1/background.json`): hard-scatter conversions fell 86 → 13 → 2 over R05–R07 (about ×6.5 per rung); a
pile-up-like fall is rejected at p = 7×10⁻⁴ to 2×10⁻³. Extrapolated by the strategy's own rule, the default plan's
background at R08–R09 is of order 10⁴ events, led by conversions: reach about 270 GeV at the 84 % edge (median about
315; about 390 GeV if the background were known exactly) — ESTIMATE on v1 placeholder efficiencies. The day-15 rule is
therefore *expected* to pause the study before production. Gate-A question Q2 is reframed around this: pause and
ask (default), or pre-authorise the "real background" paper, or pre-authorise a pre-freeze conversion-veto redesign.
All numbers of v4 were reproduced by all three reviewers. Iteration count: 4 (strong warning at 5).
Next: fixer Gunnar (opus) → STRATEGY v5 limited to R1–R5 and the adopted C items → cycle-5 verification with a
v4→v5 diff check.

### 02:20 — Phase 1 review cycle 5: ITERATE (0 A, 3 B, all text; STRONG-WARNING level of JFC 06 §6.5 reached)
STRATEGY v5 (fixer Gunnar) reviewed by fresh sessions Hana (physics), Hedwig (critical: no A or B at all, diff check
clean, script output reproduced), Hiroshi (constructive); arbiter Hugo: `phase1_strategy/review/arbiter/
STRATEGY_ARBITER_v5_hugo_2026-11-14_01-55.md`. R2–R5 resolved; R1 partial. Open: T1 the expected reach was quoted
without the strategy's own normalisation width (0.17) — with it the expected branch has a reach below 243 GeV, at or
near existing bounds (~180 GeV); the background range is ≈ 0.7–1.0×10⁴ events (weighted versus highest v1 conversion
rate); T2 neither the first upside branch nor a conversion veto alone avoids the day-15 pause (B₅₀ 587–975; decays in
flight alone 385–647, above the 300 threshold); T3 the Q4 calendar omitted the expected pause (60 days with it, 57.8
without). H-C1 (ask Q2 at day 7 if B₅₀ ≥ 3,000; veto measured on pilot records; 1,000 γ overlays, +7 CPU-h) is not
adopted as a schedule change but offered to the human as an optional rider on Q2. All ESTIMATES on v1 placeholder
efficiencies. Merged Category A by cycle: 11 → 4 → 1 → 0 → 0.
Orchestrator note on the warning level: the last three cycles changed no method, sample or criterion of a MUST
item; they corrected how the expected outcome is stated to the human. That statement is the basis of Gate A, so the
iterations are warranted; no ESCALATE is needed because nothing is blocked on the user before the gate.
Next: fixer Ingrid (opus) → STRATEGY v6 (T1–T3 + listed C items) → cycle 6: three fresh reviewers with narrow scopes
(physics: T1, T2; critical: v5→v6 diff, greps, T3 figures; constructive: Q2 and Q4 as the human reads them) + arbiter.

### 03:40 — Phase 1 review cycle 6: ITERATE (0 A, 1 B)
STRATEGY v6 (fixer Ingrid) cleared by all three fresh reviewers (Isolde, Ivan, Jasper: 0 A, 0 B, 20 C; diff clean;
script output byte-identical). Arbiter Johanna, checking independently, re-classified two C items as B and merged
them into U1: the binding day-15 projection reads decays in flight and conversions on all own hits before track
finding, with no S_CKF and no conditional credit, while the Gate-A text describes the branches on v1's after-CKF,
credited basis (so the ×5–50 caveat applies at day 15 as well as day 7, "(α1) with fit-probability credit" is not a
branch that avoids the pause under the rule as written, the bar for option (c) is understated, and nothing defines
how a redesign is judged before the freeze). Text and two script print lines, 0 CPU-h; default (a) and the expected
outcome unchanged. Eight hardest earlier dispositions spot-checked and confirmed. Verdict:
`phase1_strategy/review/arbiter/STRATEGY_ARBITER_v6_johanna_2026-11-14_03-15.md`. C items: 10 to apply before commit,
3 for the Gate-A package only, 2 deferred, 5 absorbed into U1. Gate-A text (Jasper §5) is 2,590 words: must be cut to
3 pages; 11 corrections listed in the verdict §9. History by cycle — merged A: 11 → 4 → 1 → 0 → 0 → 0; merged B:
24 → 14 → 15 → 5 → 3 → 1. Latent regression trigger noted (a single systematic above 80 % of the total in the expected
branch); v6 already commits to investigating it.
Next: fixer Jules (opus) → STRATEGY v7 (U1 + the 10 C items) → cycle 7 narrow 4-bot re-review with fresh sessions.

### 04:05 — STRATEGY v7 (fixer Jules): U1, 10 C items, and two orchestrator-ordered consistency fixes
U1 fixed as the cycle-6 verdict worded it. The fixer reported two inconsistencies outside its strict scope; the
orchestrator ordered them fixed before review (O1: §4.4 point 4 now states that the C′_PU sample serves C1 and the
development estimate of a Q2 (c) redesign — background-only sample, no blinding issue, no size or CPU change; O2: the
background size in §0 and §12.5 now carries its basis label "after CKF, as v1 counted them"). The fixer declined the
word "credited" for O2 because 0.7–1.0×10⁴ is the no-credit row. It also added a "1–2 counts" caveat to two further
copies of the "conversions alone" claim. All are listed for the cycle-7 panel to verify. Script values of v6 unchanged.
DECISION: order O1/O2 now instead of letting cycle 7 find them. ALTERNATIVES: leave v7 exactly as the verdict ordered
(probable further ITERATE on a known contradiction). CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.
