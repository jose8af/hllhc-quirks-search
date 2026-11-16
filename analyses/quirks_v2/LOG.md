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

### 05:00 — Phase 1 review cycle 7: ITERATE (0 A, 4 B, one family)
STRATEGY v7 (fixer Jules) cleared by Kenji (critical) and Klaus (constructive); Katya (physics) found two B items;
arbiter Lena confirmed both with the script's own functions, found a third and promoted a C to B — all one family
(V1): how the reading of the day-15 rule is described. Verdict: `phase1_strategy/review/arbiter/
STRATEGY_ARBITER_v7_lena_2026-11-14_04-30.md`. Facts established: branch (β) reads as (γ) at day 15 (its Z(νν) credit
exists only after the freeze) and is below 300 only up to about 60 pool counts; at decays in flight ×e⁻¹ a conversion
rejection of ×69–235 is needed (not ×31–52); at v1's central decays-in-flight size no conversion rejection alone is
enough; the fit-probability credit also acts on decays in flight, which option (c) as worded did not target. The
arbiter swept the whole family: 40 statements, 4 incorrect, 18 needing a label, and ordered a structural fix: a
script-printed day-15 table (branch → B₅₀ under rule 1 → above/below 300) plus a rejection grid for option (c), with
the text citing the table instead of paraphrasing it. The cycle-6 arbiter's fix text was the source of all four.
Arbiter's statement for the record: the design, criteria, samples, budget (4,609 CPU-h / 5,992 / 60 days), default
and expected outcome are settled; the defects are confined to the human-facing description of the day-15 decision.
History — A: 11 → 4 → 1 → 0 → 0 → 0 → 0; B: 24 → 14 → 15 → 5 → 3 → 1 → 4.
Orchestrator note: cycles 4–7 each found further sentences of the same family because each fix replaced prose with
prose. The table computed by the script removes the mechanism. Escalation rule stands: if cycle 9 does not pass,
stop and put the open list to the user instead of running to the cap of 10.
Next: fixer Leopold (opus) → STRATEGY v8 → cycle 8 narrow panel (physics recomputes the table; critical checks the
v7→v8 diff and greps; constructive checks the Gate-A package against the table) + arbiter.

### 05:40 — STRATEGY v8 (fixer Leopold): script-printed day-15 table and option-(c) rejection grid
Family V1 fixed structurally: `strategy_budget.py` prints the day-15 table (branch → B₅₀ under rule 1 → above/below
300) and the rejection grid; the text cites them. Printed numbers equal the cycle-7 arbiter's in every cell; no v7
value changed. Fixer's own sweep: 58 statements, all consistent. Orchestrator-ordered additions from the fixer's
proposals: O3 basis label on §0 "590–980" (confirmed after-CKF from stdout lines 314/316 and 365–366), O4 a stale
reference, O5 the runtime note (about 90 s). 32 hunks v7→v8, none unattributed.

### 06:55 — Phase 1 review cycle 8: ITERATE (0 A, 1 B = W1); root cause found
All three fresh reviewers (Ludmila, Magnus, Marcel) found the same single defect: the script-printed day-15 table
and option-(c) grid ordered in cycle 7 used pool exposures, not the pilot exposures rule 1 and the captions state.
Arbiter Margaret (fable; see MODEL_LEDGER): `phase1_strategy/review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`.
**Root cause of cycles 4–8: rule 1 (§11.7) is itself ambiguous** — it never said what the thirteen SM processes and
multijets without a day-15 sample contribute, so 15 Z(νν) pilot counts could read 242 (proceed) or 353 (pause).
Pinned reading (to be shown to the user as an overridable default): every SM process is read through the single
Z(νν) pilot count (18.1 events per count); no pool floor; option-(c) factors never multiply a zero-count floor.
Consequence: the day-15 limit becomes about 12 Z(νν) pilot counts, not about 20. Key cells (arbiter's run): empty
pilot 76; Z(νν) 11/12/13 counts → 281/300/317; decays in flight 3/4 counts → 266/331; (α1′) 3.2×10⁴–3.3×10⁵;
required conversion rejection ×44 (×30 at the 0.255 photon rate) with decays in flight removed, ×75–150 at 1/4,
×114 or none at e⁻¹, none at v1's central size. All three reviewers' numbers reproduced and reconciled. Fix: recompute
(complete replacement code; expected stdout sha256 0ca4af15…003433d; Monte-Carlo draws raised to 20,000 because 3,000
moved factors by up to 25 %), 18 exact text replacements, an 8-check self-test in the script, and a new text checker
`check_day15_text.py` (45/45 on the arbiter's scratch v9; 42 mismatches on v8). Outside this family nothing is open:
4,609 / 5,992 CPU-h, 60 days, defaults and expected outcome unchanged. History — A: 11→4→1→0→0→0→0→0; B:
24→14→15→5→3→1→4→1.
Note: the arbiter ran one read-only `git status` against its no-git instruction; no effect.
Next: fixer Mireille (opus) applies the verdict's §3–§5 only → STRATEGY v9 → cycle 9 (last before escalation).

### 07:25 — STRATEGY v9 (fixer Mireille): rule 1 clarified, tables recomputed on rule 1's own basis, mechanical guards
Applied the cycle-8 verdict's §3–§5 with code and text copied programmatically from the verdict file. Script stdout
sha256 equals the expected value (two runs); self-test 8/8 PASS; `check_day15_text.py` 45/45 on v9; outside the two
tables, the label line and the self-test lines the script output is byte-identical to v8. Orchestrator-ordered
addition O6: row Df-11 in the table of overridable defaults (the pinned reading of rule 1, citing the table row).
Correction to the orchestrator's own brief for O6: the alternative reading with a pool floor is the *lenient* one
per the verdict, not the stricter one; the fixer followed the verdict. 33 hunks v8→v9, none unattributed.

### CORRECTION (written 2026-11-14 01:20 -05, measured with `date`): the times in this log are not clock times
From the "14:45" entries onward the orchestrator wrote entry times, file-name timestamps and "spawned at" times from
its own running estimate without calling `date`. They drifted: the entries labelled 19:25 (13 Nov) to 07:55 (14 Nov)
were in fact written between 18:40 on 13 Nov and 01:05 on 14 Nov, and some earlier labels are off by 10–25 minutes
(for example the user's Geant4 decision, labelled 16:00, was committed at 15:39). **The git commit times are the
authoritative clock** (`git log --date=iso`). The labels remain valid as an ordering and as identifiers in file
names (reviews, verdicts, strategy versions), which are not renamed. Measured anchors: preflight 14:06 and 14:34;
out-of-memory incident 15:12 (reported by the user); reconciliation 15:35; strategy v1 committed 18:16; cycle-9
reviews committed 01:05 on 14 Nov. From this entry on, every time in this log comes from `date` or from git.

### 2026-11-14 01:10 (git) — Phase 1 review cycle 9: ITERATE (0 A, 1 B). Orchestrator stops by its own rule
STRATEGY v9 (fixer Mireille) reviewed by fresh sessions Nadia (physics: approve; 38/38 table cells recomputed with
separate code), Nikolai (critical: mechanical checks all pass; found the one B), Nora (constructive: sound and honest
basis for Gate A). Arbiter Odette (fable): `phase1_strategy/review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`.
W1 and the whole day-15 family: closed (sha256 of the script output equals the expected value; self-test 8/8; text
checker 45/45 on v9 and 41 mismatches on v8 as control; rule-1 clarification present). No number, criterion, budget
figure, default answer or expected outcome is open.
B-1 (stands at Category B): the "What is frozen when" table still says Gate A freezes "the ten defaults"; there are
eleven since the orchestrator-ordered addition O6 (Df-11, the pinned reading of rule 1), whose count update missed
this row. The arbiter judged it B because that row is the strategy's only list of what Gate A freezes and "ten"
reads as excluding Df-11. **The defect was introduced by the orchestrator's own addition O6.**
Also ordered, Category C, exact text given and tested against the checker on a scratch copy (13 hunks): what the
strategy should tell the human about Df-11 (the alternative reading is more lenient: about 20 instead of 12 Z(νν)
pilot counts; the pinned reading is itself a proxy that under-reads the other processes' conversions by about 8 %,
at most ×1.6; "≈ 12 counts" holds at an R09 candidate and is about 6–7 at R08), and one sentence in rule 1 (E6: at
least 10⁵ draws; a reading within that precision of 300 pauses) — the only edit touching a criterion, which the
human may drop. Gate-A package text corrected by the arbiter (1,496 words), copied to `gates/GATE_A_DRAFT.md`.
History — A: 11→4→1→0→0→0→0→0→0; B: 24→14→15→5→3→1→4→1→1.
DECISION: stop here and put the open list to the user, as committed in the entry on cycle 7 ("if cycle 9 does not
pass, stop"). Applying the edits and verifying them would be cycle 10, the hard cap of JFC 06 §6.5.
ALTERNATIVES: run cycle 10 without asking (within the cap, but against the orchestrator's own stated rule and with
nine ITERATEs behind it). CONFIDENCE: HIGH. FLAG FOR HUMAN: YES.

### 2026-11-14 01:18 (date) — CLUSTER FAULT: `/nfs/cajuela` hangs on einstein; ssh to all three workers hangs
Found while checking a load report from the cycle-9 arbiter (it saw load average 96–141 on einstein). Measured:
- `cat /proc/loadavg` on einstein: 159.23 138.09 94.08; 162 `kubelet` threads and one kernel thread
  `192.168.10.254-manager` in uninterruptible sleep (state D); CPU idle; memory fine (10 GB available).
- `timeout 8 ls /nfs/cajuela/jdochoa/quirks_v2` on einstein: no answer (killed by the timeout). The underlying
  `ls /mnt/cajuela` answers at once, so the disks and mergerfs respond and the hang is in the NFS mount of cajuela.
- `ssh -x <worker> …` with a 15 s timeout: no answer from landau, maxwell and schrodinger; all three answer `ping`.
  One older ssh to maxwell had been hanging for about 31 minutes, which dates the start to about 00:47.
- `kubectl get nodes`: all four nodes Ready. `/home` responds normally; the repository is unaffected.
The study had no job running on any worker and no process writing to cajuela at that time; the review agents on
einstein only read files under `/home` and ran a standard-library script (36 MB, 75 s, one at a time). Cause not
established. Per brief §7 this is a broken cluster service: no repair attempted; reported to the user.
Consequences: no repo bundle can be written to cajuela (the last bundle is `repo-2026-11-13.bundle`, made at 14:37);
no worker job or Argo campaign may be started until the user confirms the cluster is healthy.
Also cleaned: three stale processes of ours on einstein (a watcher loop left by the chain-port executor since about
17:46 that polled maxwell by ssh every 15 s, its hung ssh child, and one older waiting loop) were killed at 01:19.

## 2026-11-16 10:40 -05 (measured) — User: cluster healthy, cycle 10 authorised
- The user asked for the cycle-9 counts (answered: 0 A, 1 B, 17 C: 15 applied in the fix pass, 1 deferred to Phase 2,
  1 record only), then reported that the cluster test workflow passed, allowed the repo bundle and the workers again,
  kept the 10 GB cap and the "nothing heavy on einstein" rule, and **authorised review cycle 10** (the hard cap).
- Own checks at 10:40: `ls /nfs/cajuela/jdochoa/quirks_v2/backup` answers; ssh to landau, maxwell, schrodinger
  answers in about 1 s each. Load averages are still decaying (1-min: einstein 105, workers about 40).
- Repo bundle written: `/nfs/cajuela/jdochoa/quirks_v2/backup/repo-2026-11-16.bundle` (75,266,407 bytes, `--all`,
  written as `.part` then renamed, `git bundle verify` OK, sha256 `32811a67…46d1d74`). HEAD at the time: `9b0fced`.
- 10:45: fixer **Oscar** (Opus, default) spawned with the strict scope of the cycle-9 verdict §5 (E1–E14 incl. E6 and
  the bookkeeping) to produce STRATEGY v10. E6 (the precision sentence of rule 1) is applied; the user may still drop it.
  Next: the narrow check of verdict §9 (fresh critical reviewer, then arbiter).

## 2026-11-16 11:00 -05 (measured) — Phase-1 review PASS in cycle 10; stop at Gate A
- 10:45 fixer Oscar delivered STRATEGY v10 (`phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`): E1–E14 as
  exact text; sha256 before bookkeeping equal to the cycle-9 arbiter's prediction; checker 45 of 45. Commit `25b3ff5`.
- 10:49 critical reviewer Pauline (fresh, Opus): checks a–g PASS, 0 A, 0 B, 2 C. Commit `cdafef2`. Her two stated
  limits were closed from git by the orchestrator: nothing under `phase1_strategy/src/` changed in the fix;
  `COMMITMENTS.md` changed by +12/−4 lines.
- 10:55 arbiter Quentin (fresh, Opus): **PASS**, 0 A, 0 B, 2 C
  (`phase1_strategy/review/arbiter/STRATEGY_ARBITER_v10_quentin_2026-11-16_10-51.md`). The narrowed panel (one
  critical reviewer + arbiter) is what the cycle-9 arbiter ordered; Quentin records its limit: the arbiter-written
  text of cycle 9 was not read by a physics reviewer apart from its numbers.
- C-1 applied by the orchestrator as ordered (no re-review): v10 l.16 author list → "(the author of the version that
  introduced the sentence, §12.2)". v10 sha256 now `d806bb362a514b3fba687ad107018be9fe42ac7e3ad665cbb98b4432e020b779`
  (the arbiter's predicted value); checker re-run: 45 of 45, output identical to `day15_text_check_v10.txt`.
  C-2 (fixer ran one read-only `git diff`): record only.
- Orchestrator regression checklist: Phase 1 has no validation test, systematic, fit, goodness-of-fit, bin exclusion
  or measured result, so those boxes cannot be ticked; binding decisions D1–D10 of the brief are respected in v10
  (cycle-9 verdict §6, unchanged by the fix: endcap as outlook only, no cloud, no ρ = 3, no pile-up scan, no Open
  Data, no Stage 3 at Λ ≥ 15 keV). No regression trigger.
- `gates/GATE_A.md` written from the draft with the changes of verdict §9 (1,586 words); the draft file is removed.
- Stopped for the user's Gate A. Nothing runs.

## 2026-11-16 10:55 -05 (measured) — Time correction to the entry above
The heading "11:00" and the times "10:55" (arbiter) in the entry above were written ahead of the clock. Measured:
the commits are `25b3ff5` at 10:44, `cdafef2` at 10:49 and `87b6c04` (PASS, Gate A package) at 10:53. The repo bundle
`repo-2026-11-16.bundle` was rewritten after `87b6c04` (75,209,234 bytes, verified).

## 2026-11-16 11:50 -05 (measured) — GATE A PASSED BY THE USER
The user asked for the questions, then for the expected quality of the paper against v1 (answered: method clearly
stronger; headline expected at or near existing bounds, the "real background" paper; the strong result has no
demonstrated route), then answered: **"Q1 ●; Q2 ●; Q3 ●; Q4 ●; Q5 ● . Ok go ahead."**
- All five defaults taken; no rider; no default Df-1…Df-11 overridden; E6 kept. Recorded and frozen in
  `COMMITMENTS.md` ("Gate A answers"). Approved schedule: 4,609 CPU-h, stop-and-ask at 5,992, about 60 days.
- **Day 0 of the calendar = 2026-11-16.** Day 5 = 21 Nov, day 7 = 23 Nov, day 12 = 28 Nov, day 15 = 1 Dec (binding
  rule 1; a pause is expected there), freeze days 17–19 = 3–5 Dec, Gate B about day 49–51 = 4–6 Jan 2027,
  Gate C about day 58–60 = 13–15 Jan 2027.
- The user asked for a daily track of work and results: `STATUS.md` is updated at least daily and a dated report is
  written to `daily/YYYY-MM-DD.md` at the end of each working day.
- Phase 2 starts.

## 2026-11-16 11:52 -05 (measured) — Phase 2 started
Three executors spawned from `phase2_exploration/PHASE2_BRIEF.md`: channel (i) Rosalie (Opus; C1, C2), channel (ii)
Sebastian (Opus; S2, P1, retrievals, Herwig), channel (iii) Tatiana (Fable, logged; pilot, T1 builder, Geant4
hand-over). Slot caps per channel are in the brief. A session cron at 18:47 triggers the daily report
(`daily/`, `STATUS.md`, bundle).

## 2026-11-16 11:56 -05 (measured) — User authorises pushing; daily reports in LaTeX
The user: "I want you to commit and push the daily reports in the repository. I give you permission to do so. Start
right now with the phase 1 report and make sure to include all the improvements that are proposed and will be done
with respect to v1. The reports that are pushed should be in latex."
- This replaces the brief's "never push" for the daily reports (DEVIATIONS V14). A report commit sits on `v2-jfc`,
  so pushing it pushes the branch with all its commits (the remote already had `v2-jfc` at `31a6974`). Still
  never: force-push, history rewrite, pushing any other branch or tag.
- Reports live in `daily/` as `.tex` with the compiled `.pdf`: `phase1_report` now, then one per day.
- `daily/phase1_report.tex` written by the orchestrator (6 pages) from `COMMITMENTS.md`, `gates/GATE_A.md`,
  `phase1_strategy/outputs/FRAMING.md` and the cycle-10 verdict.

## 2026-11-16 12:15 -05 (measured) — Phase 2, channel (ii) reports 1 and 2; strategy-revision input on the MET model
- R-2 (trigger turn-on) sourced from the public L1 trigger TDR (retrieval #11). R-3 sourced only from the second
  public source (ATLAS notes, #12); the CMS note CMS-NOTE-2018-006 is not obtainable by an agent (CDS bot protection;
  not circumvented). Jet-response tail: not sourced after a second attempt (#14). Validation figure: #15.
- **Strategy-revision input (channel (ii)):** Phase 1 assumed the public soft-term parametrisation could be validated
  against a separate pile-up-200 figure. Phase 2 found the only explicit public formula (2013, made for μ ≤ 140) gives
  a MET resolution ×1.5–3 above the 2019 μ = 200 figure. Implication: a model built on the 2013 formula fails the
  external validation of B4-b; a model built on the 2019 figure has no independent validation figure left.
- **Orchestrator ruling (not a stop):** the stop-and-ask of STR §4.7 applies when no parameters can be sourced from
  two public sources; parameters are sourced. A model without a passing external validation is the strategy's own
  "not validated" branch (COM B4-b: full variation as width, stated). The choice between the two constructions is a
  pre-freeze design decision of the Phase-3 MET-model work (by day 10), reviewed with the pre-registration; the
  2013-against-2019 difference is the natural size of the "full variation". A second μ = 200 figure (the CMS note,
  if the user supplies it by hand) would restore an independent validation. The user was told on 16 Nov.
- Answers given to channel (ii): f₂₀₀ allowed (COM BL-1), A and m_mig not; S1 Stage-2 samples are not Phase 2;
  install slot granted for Herwig (node-local) and PDF4LHC21; Herwig comparison charged to S2 within 139 CPU-h.
- A channel (ii) smoke job overlapped for 11 minutes with channel (i)'s reserved ρ = 2 memory measurement on maxwell;
  channel (i) to state whether its measurement is affected.

## 2026-11-16 12:58 -05 (measured) — Phase 2, channel (i) interim report; fixed node shares
- Day-0 measurements (VERIFIED, channel (i)): ρ = 2 max RSS 1.60 / 1.59 / 1.74 / 2.12 GB at 1 / 2 / 4 / 8 events per
  job (with the pre-merge store; +0.5 GB) → 2 ρ = 2 jobs per node, 5 events per job; ρ = 2 cost 195 CPU-s per event
  (Table 4.0: 206); ρ = 1 cost 57–59 CPU-s per event (60.4); finder 11.3 ± 7.3 s per trial at road 0.15, so the ×0.77
  saving assumed in Table 4.0 is not seen; pre-merge store 34 MB per trial (STR: 3.6–14), projecting about 270 GB
  with the 4a ρ = 2 sample (planning value 200 GB, cap 400 GB: accepted, no change of the N_IP2 ≥ 6 threshold;
  enters the day-5 storage projection).
- The memory measurement was taken alone on the node; the ρ = 2 timing shared the node with a channel (ii) job for
  11 minutes (stated with the number).
- C1 campaigns p2-a-c1-pu1 (4,000 events) and p2-a-c1-pu2 (1,000 events) run; resume after a driver kill tested.
- Slot conflicts between the channels: replaced the per-channel caps by fixed node shares (`phase2_exploration/SLOTS.md`).
- Ruling: channel (i) produces the C1 signal inputs itself (Stage 2 at E 200 and E 500 with v1's cards, FSR off as
  S2-d keeps for C1; Stage 3 at the three C1 points), reusing channel (ii)'s generation job script.
